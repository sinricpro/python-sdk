"""
SinricPro Main Class

Main SDK class managing connections, devices, and message routing.
"""

import asyncio
import json
import re
import time
from typing import Any

from sinricpro import __version__
from sinricpro.core.exceptions import (
    SinricProConfigurationError,
    SinricProDeviceError,
)
from sinricpro.core.local_control import MdnsAnnouncer, UdpListener
from sinricpro.core.message_queue import MessageQueue
from sinricpro.core.signature import Signature
from sinricpro.core.sinric_pro_device import SinricProDevice
from sinricpro.core.types import (
    SinricProConfig,
    SinricProRequest,
    ConnectedCallback,
    DisconnectedCallback,
    MessageOrigin,
    PongCallback,
    ModuleSettingCallback,
    QueuedMessage,
    Transport,
    EVENT_LIMIT_STATE,
    PHYSICAL_INTERACTION,
    SEND_QUEUE_MAX,
    WEBSOCKET_ORIGIN,
)
from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.websocket_client import WebSocketClient, WebSocketConfig
from sinricpro.utils.logger import SinricProLogger, LogLevel


class SinricPro:
    """
    Main SinricPro SDK class.

    Singleton class managing WebSocket connection, device registration,
    and message routing.

    Example:
        >>> sinric_pro = SinricPro.get_instance()
        >>> await sinric_pro.begin(config)
    """

    _instance: "SinricPro | None" = None

    def __init__(self) -> None:
        """Initialize SinricPro (use get_instance() instead)."""
        if SinricPro._instance is not None:
            raise RuntimeError("Use SinricPro.get_instance() instead of constructor")

        self.config: SinricProConfig | None = None
        self.devices: dict[str, SinricProDevice] = {}
        self.websocket: WebSocketClient | None = None
        self.receive_queue = MessageQueue()
        self.send_queue = MessageQueue(max_size=SEND_QUEUE_MAX)
        self.signature: Signature | None = None
        self.udp_listener: UdpListener | None = None
        self.mdns: MdnsAnnouncer | None = None
        self.is_initialized = False
        self._processing_tasks: list[asyncio.Task[None]] = []
        self._connected_callbacks: list[ConnectedCallback] = []
        self._disconnected_callbacks: list[DisconnectedCallback] = []
        self._pong_callbacks: list[PongCallback] = []
        self._module_setting_callback: ModuleSettingCallback | None = None
        self._setting_event_limiter = EventLimiter(EVENT_LIMIT_STATE)

    @classmethod
    def get_instance(cls) -> "SinricPro":
        """
        Get the singleton instance of SinricPro.

        Returns:
            The SinricPro singleton instance

        Example:
            >>> sinric_pro = SinricPro.get_instance()
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def begin(self, config: SinricProConfig | dict[str, Any]) -> None:
        """
        Initialize and connect to SinricPro service.

        Args:
            config: Configuration object or dict with app_key, app_secret, etc.

        Raises:
            SinricProConfigurationError: If configuration is invalid

        A cloud connection failure is not fatal: the SDK stays up, retries in
        the background, and keeps answering local control. Call
        :meth:`is_connected` to check cloud state.

        Example:
            >>> config = SinricProConfig(
            ...     app_key="your-app-key",
            ...     app_secret="your-app-secret",
            ...     debug=True
            ... )
            >>> await sinric_pro.begin(config)
        """
        if self.is_initialized:
            SinricProLogger.warn("SinricPro already initialized")
            return

        # Convert dict to SinricProConfig if needed
        if isinstance(config, dict):
            config = SinricProConfig(**config)

        # Validate config (happens in __post_init__)
        self.config = config

        # Set log level
        if self.config.debug:
            SinricProLogger.set_level(LogLevel.DEBUG)

        SinricProLogger.info("Initializing SinricPro SDK...")

        # Initialize signature handler
        self.signature = Signature(self.config.app_secret)

        try:
            ws_config = WebSocketConfig(
                server_url=self.config.server_url,
                app_key=self.config.app_key,
                device_ids=list(self.devices.keys()),
            )

            self.websocket = WebSocketClient(ws_config)
            self._setup_websocket_handlers()

            # Local control comes up before the cloud so a host that never
            # reaches sinric.pro still answers the app over the LAN.
            await self._start_local_control()

            self.is_initialized = True
            self._start_message_processor()

            try:
                await self.websocket.connect()
            except Exception as e:
                # Transport failure is never fatal -- the reconnect timer is
                # armed and local control already answers. Only invalid
                # configuration raises, and it has done so above.
                SinricProLogger.warn(
                    f"Cloud connection failed ({e}); will keep retrying"
                )
                self.websocket.schedule_reconnect()

            SinricProLogger.info("SinricPro SDK initialized successfully")

        except Exception as e:
            SinricProLogger.error(f"Failed to initialize SinricPro: {e}")
            self.is_initialized = False
            await self._stop_local_control()
            raise

    async def _start_local_control(self) -> None:
        """Bring up the LAN listener and the mDNS announcement."""
        if not self.config or not self.config.local_control:
            SinricProLogger.info("Local control disabled by configuration")
            return

        listener = UdpListener(
            self.receive_queue, interface_ip=self.config.local_control_interface
        )
        if not await listener.start():
            return
        self.udp_listener = listener

        if not self.config.mdns:
            SinricProLogger.info("mDNS announcement disabled by configuration")
            return

        announcer = MdnsAnnouncer(
            sdk_version=__version__, interface_ip=self.config.local_control_interface
        )
        if await announcer.start(list(self.devices.keys())):
            self.mdns = announcer

    async def _stop_local_control(self) -> None:
        """Tear down the LAN listener and the mDNS announcement."""
        if self.mdns:
            await self.mdns.stop()
            self.mdns = None
        if self.udp_listener:
            await self.udp_listener.stop()
            self.udp_listener = None

    def add(self, device: SinricProDevice) -> SinricProDevice:
        """
        Add a device to SinricPro.

        Args:
            device: The device instance to add

        Returns:
            The added device instance

        Raises:
            SinricProDeviceError: If device ID is invalid

        Example:
            >>> my_switch = SinricProSwitch("5dc1564130xxxxxxxxxxxxxx")
            >>> sinric_pro.add(my_switch)
        """
        device_id = device.get_device_id()

        # Validate device ID format (24 hex characters)
        if not device_id or not isinstance(device_id, str):
            raise SinricProDeviceError("Invalid device: device_id is required and must be a string")

        if not re.match(r"^[a-f0-9]{24}$", device_id, re.IGNORECASE):
            raise SinricProDeviceError(
                f"Invalid device_id format: {device_id}. Expected 24 hexadecimal characters"
            )

        if device_id in self.devices:
            SinricProLogger.warn(f"Device {device_id} already exists, returning existing instance")
            return self.devices[device_id]

        device.set_sinric_pro(self)
        self.devices[device_id] = device

        SinricProLogger.info(f"Device added: {device_id} ({device.get_product_type()})")

        # Update WebSocket device list if already connected
        if self.is_initialized and self.websocket:
            self.websocket.update_device_list(list(self.devices.keys()))

        # The mDNS record is refreshed only when the device list changes.
        if self.mdns:
            try:
                asyncio.get_running_loop().create_task(
                    self.mdns.update(list(self.devices.keys()))
                )
            except RuntimeError:
                SinricProLogger.warn("No running event loop, mDNS record not refreshed")

        return device

    def get(self, device_id: str) -> SinricProDevice | None:
        """
        Get a device by its ID.

        Args:
            device_id: The device ID to look up

        Returns:
            The device instance if found, None otherwise
        """
        return self.devices.get(device_id)

    def on_connected(self, callback: ConnectedCallback) -> None:
        """
        Register a callback for when connected to SinricPro.

        Args:
            callback: Function to call when connected

        Example:
            >>> def on_connected():
            ...     print("Connected!")
            >>> sinric_pro.on_connected(on_connected)
        """
        self._connected_callbacks.append(callback)

    def on_disconnected(self, callback: DisconnectedCallback) -> None:
        """
        Register a callback for when disconnected from SinricPro.

        Args:
            callback: Function to call when disconnected
        """
        self._disconnected_callbacks.append(callback)

    def on_pong(self, callback: PongCallback) -> None:
        """
        Register a callback for heartbeat pong responses.

        Args:
            callback: Function to call with latency in milliseconds
        """
        self._pong_callbacks.append(callback)

    def on_set_setting(self, callback: ModuleSettingCallback) -> None:
        """
        Register a callback for module-level setting changes.

        Module settings are configuration values for the module (dev board) itself,
        not for individual devices. Use this to handle settings like WiFi retry count,
        logging level, or other module-wide configurations.

        Args:
            callback: Async function that receives setting_id and value, returns True on success.
                      Signature: async def callback(setting_id: str, value: Any) -> bool

        Example:
            >>> async def on_module_setting(setting_id: str, value: Any) -> bool:
            ...     if setting_id == "wifi_retry_count":
            ...         set_wifi_retry_count(value)
            ...     return True
            >>> sinric_pro.on_set_setting(on_module_setting)
        """
        self._module_setting_callback = callback

    async def send_setting_event(
        self,
        setting_id: str,
        value: Any,
        cause: str = PHYSICAL_INTERACTION
    ) -> bool:
        """
        Send a module-level setting event to SinricPro server.

        Module settings are configuration values for the module (dev board) itself.
        Use this to report setting changes like WiFi configuration, logging level,
        or other module-wide settings.

        Args:
            setting_id: The setting identifier
            value: The setting value (can be any JSON-serializable type)
            cause: Reason for the event (default: 'PHYSICAL_INTERACTION')

        Returns:
            True if event was sent, False if rate limited or failed

        Example:
            >>> await sinric_pro.send_setting_event('wifi_retry_count', 5)
            >>> await sinric_pro.send_setting_event('debug_mode', True)
        """
        if self._setting_event_limiter.is_limited():
            return False

        if not self.is_connected():
            SinricProLogger.error("Cannot send setting event: Not connected to SinricPro")
            return False

        event_message: dict[str, Any] = {
            "header": {
                "payloadVersion": 2,
                "signatureVersion": 1,
            },
            "payload": {
                "action": "setSetting",
                "replyToken": self._generate_message_id(),
                "type": "event",
                "createdAt": self.get_timestamp(),
                "cause": {"type": cause},
                "scope": "module",
                "value": {"id": setting_id, "value": value},
            },
        }

        try:
            await self.send_message(event_message)
            SinricProLogger.debug(f"Module setting event sent: {setting_id} = {value}")
            return True
        except Exception as e:
            SinricProLogger.error(f"Failed to send module setting event {setting_id}: {e}")
            return False

    def _generate_message_id(self) -> str:
        """Generate a unique message ID."""
        import random
        import string

        timestamp = int(time.time() * 1000)
        random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=9))
        return f"{timestamp}-{random_str}"

    def is_connected(self) -> bool:
        """
        Check if currently connected to SinricPro.

        Returns:
            True if connected, False otherwise
        """
        return self.websocket.is_connected() if self.websocket else False

    async def stop(self) -> None:
        """
        Stop the SinricPro SDK and disconnect from the server.

        Example:
            >>> await sinric_pro.stop()
        """
        SinricProLogger.info("Stopping SinricPro SDK...")
        self.is_initialized = False

        # Cancel processing tasks
        for task in self._processing_tasks:
            task.cancel()
        self._processing_tasks.clear()

        await self._stop_local_control()

        # Disconnect WebSocket
        if self.websocket:
            await self.websocket.disconnect()

        # Clear queues
        self.receive_queue.clear()
        self.send_queue.clear()

        SinricProLogger.info("SinricPro SDK stopped")

    async def send_message(self, message: dict[str, Any]) -> None:
        """
        Send a message to SinricPro (for internal use by devices).

        Args:
            message: Message dictionary to send
        """
        if not self.signature:
            SinricProLogger.error("Signature handler not initialized")
            return

        self.send_queue.push_sync(self.signature.sign_message(message), WEBSOCKET_ORIGIN)

    def get_timestamp(self) -> int:
        """
        Get current timestamp in seconds.

        Returns:
            Current Unix timestamp in seconds
        """
        return int(time.time())

    def _setup_websocket_handlers(self) -> None:
        """Set up WebSocket event handlers."""
        if not self.websocket:
            return

        self.websocket.on_message(lambda msg: self.receive_queue.push_sync(msg))

        self.websocket.on_connected(lambda: self._handle_connected())

        self.websocket.on_disconnected(lambda: self._handle_disconnected())

        self.websocket.on_pong(lambda latency: self._handle_pong(latency))

        self.websocket.on_error(lambda error: SinricProLogger.error(f"WebSocket error: {error}"))

    def _handle_connected(self) -> None:
        """Handle WebSocket connected event."""
        for callback in self._connected_callbacks:
            try:
                callback()
            except Exception as e:
                SinricProLogger.error(f"Error in connected callback: {e}")

    def _handle_disconnected(self) -> None:
        """Handle WebSocket disconnected event."""
        for callback in self._disconnected_callbacks:
            try:
                callback()
            except Exception as e:
                SinricProLogger.error(f"Error in disconnected callback: {e}")

    def _handle_pong(self, latency: int) -> None:
        """Handle WebSocket pong event."""
        for callback in self._pong_callbacks:
            try:
                callback(latency)
            except Exception as e:
                SinricProLogger.error(f"Error in pong callback: {e}")

    def _start_message_processor(self) -> None:
        """Start message processing tasks."""
        receive_task = asyncio.create_task(self._process_receive_queue())
        send_task = asyncio.create_task(self._process_send_queue())
        self._processing_tasks.extend([receive_task, send_task])

    async def _process_receive_queue(self) -> None:
        """Process received messages."""
        while self.is_initialized:
            try:
                entry = await self.receive_queue.pop()
                if entry:
                    await self._handle_message(entry)
                else:
                    await asyncio.sleep(0.01)  # Small delay if queue is empty
            except asyncio.CancelledError:
                break
            except Exception as e:
                SinricProLogger.error(f"Error processing received message: {e}")

    async def _handle_message(self, entry: QueuedMessage) -> None:
        """Handle a received message, from either the cloud or the LAN."""
        try:
            message = json.loads(entry.message)
            origin = entry.origin

            # Handle timestamp message
            if "timestamp" in message:
                return

            # Validated against the received bytes: the sender's key order and
            # spacing are its own, so a re-serialized dict would not match.
            if not self.signature or not self.signature.validate(entry.message):
                SinricProLogger.error("Invalid message signature")
                self._send_invalid_signature_response(message, origin)
                return

            # Route message. LAN requests land in the same handlers as cloud
            # requests - there is no second dispatch path.
            if message["payload"]["type"] == "request":
                # Check scope to determine if this is a module or device request
                scope = message["payload"].get("scope", "device")
                if scope == "module":
                    await self._handle_module_request(message, origin)
                else:
                    await self._handle_request(message, origin)
            elif message["payload"]["type"] == "response":
                # Response messages (not typically used in device SDK)
                pass

        except Exception as e:
            SinricProLogger.error(f"Error handling message: {e}")

    async def _handle_request(
        self, message: dict[str, Any], origin: MessageOrigin = WEBSOCKET_ORIGIN
    ) -> None:
        """Handle an incoming request."""
        device_id = message["payload"].get("deviceId")
        device = self.devices.get(device_id) if device_id else None

        if not device:
            SinricProLogger.error(f"Device not found: {device_id}")
            self._send_error_response(message, f"Device {device_id} not found", origin)
            return

        request = SinricProRequest(
            action=message["payload"]["action"],
            instance=message["payload"].get("instanceId", ""),
            request_value=message["payload"].get("value", {}),
        )

        success = await device.handle_request(request)
        self._send_response(
            message, success, request.response_value, request.error_message, origin
        )

    async def _handle_module_request(
        self, message: dict[str, Any], origin: MessageOrigin = WEBSOCKET_ORIGIN
    ) -> None:
        """Handle an incoming module-level request."""
        action = message["payload"].get("action", "")
        request_value = message["payload"].get("value", {})

        if action == "setSetting":
            if not self._module_setting_callback:
                SinricProLogger.error("No module setting callback registered")
                self._send_module_response(
                    message, False, {}, "No module setting callback registered", origin
                )
                return

            setting_id = request_value.get("id", "")
            value = request_value.get("value")

            try:
                success = await self._module_setting_callback(setting_id, value)
                response_value = {"id": setting_id, "value": value} if success else {}
                self._send_module_response(message, success, response_value, origin=origin)
            except Exception as e:
                SinricProLogger.error(f"Error in module setting callback: {e}")
                self._send_module_response(message, False, {}, str(e), origin)
        else:
            SinricProLogger.error(f"Unknown module action: {action}")
            self._send_module_response(
                message, False, {}, f"Unknown module action: {action}", origin
            )

    def _send_module_response(
        self,
        request_message: dict[str, Any],
        success: bool,
        value: dict[str, Any],
        error_message: str | None = None,
        origin: MessageOrigin = WEBSOCKET_ORIGIN,
    ) -> None:
        """Send a module-level response message (without deviceId)."""
        request_payload = request_message.get("payload", {})
        response_message: dict[str, Any] = {
            "header": {
                "payloadVersion": 2,
                "signatureVersion": 1,
            },
            "payload": {
                "action": request_payload.get("action", ""),
                "clientId": request_payload.get("clientId", ""),
                "createdAt": self.get_timestamp(),
                "message": error_message if error_message else ("OK" if success else "Request failed"),
                "replyToken": request_payload.get("replyToken", ""),
                "scope": "module",
                "success": success,
                "type": "response",
                "value": value,
            },
        }

        self._enqueue_response(response_message, origin)

    def _send_response(
        self,
        request_message: dict[str, Any],
        success: bool,
        value: dict[str, Any],
        error_message: str | None = None,
        origin: MessageOrigin = WEBSOCKET_ORIGIN,
    ) -> None:
        """Send a response message."""
        # A request that failed verification may be missing anything, so every
        # echoed field is read defensively.
        request_payload = request_message.get("payload", {})
        response_message: dict[str, Any] = {
            "header": {
                "payloadVersion": 2,
                "signatureVersion": 1,
            },
            "payload": {
                "action": request_payload.get("action", ""),
                "clientId": request_payload.get("clientId", ""),
                "createdAt": self.get_timestamp(),
                "deviceId": request_payload.get("deviceId", ""),
                "message": error_message if error_message else ("OK" if success else "Request failed"),
                "replyToken": request_payload.get("replyToken", ""),
                "scope": "device",
                "success": success,
                "type": "response",
                "value": value,
            },
        }

        if "instanceId" in request_payload:
            response_message["payload"]["instanceId"] = request_payload["instanceId"]

        self._enqueue_response(response_message, origin)

    def _enqueue_response(
        self, response_message: dict[str, Any], origin: MessageOrigin
    ) -> None:
        """Sign a response and queue it for the transport it must go back on."""
        if not self.signature:
            SinricProLogger.error("Signature handler not initialized")
            return
        self.send_queue.push_sync(self.signature.sign_message(response_message), origin)

    def _send_error_response(
        self,
        message: dict[str, Any],
        error_message: str,
        origin: MessageOrigin = WEBSOCKET_ORIGIN,
    ) -> None:
        """Send an error response."""
        self._send_response(message, False, {"error": error_message}, error_message, origin)

    def _send_invalid_signature_response(
        self, message: dict[str, Any], origin: MessageOrigin = WEBSOCKET_ORIGIN
    ) -> None:
        """Answer a request that failed verification.

        Answering rather than dropping is deliberate: it lets a client tell a
        wrong app secret apart from an unreachable device.
        """
        self._send_response(message, False, {}, "Signature is invalid", origin)

    async def _process_send_queue(self) -> None:
        """Process outgoing messages."""
        while self.is_initialized:
            try:
                # Gate per message, not per queue: a cloud message waiting for
                # the socket must not hold up a LAN reply queued behind it.
                connected = self.is_connected()
                entry = self.send_queue.pop_sync(
                    lambda m: connected or m.origin.transport is not Transport.WEBSOCKET
                )

                if entry is None:
                    await asyncio.sleep(0.01)
                    continue

                if entry.origin.transport is Transport.UDP:
                    # LAN responses are never echoed to the cloud socket.
                    if self.udp_listener:
                        self.udp_listener.send(entry.message, entry.origin.peer)
                    continue

                if not self.websocket:
                    continue

                try:
                    self.websocket.send(entry.message)
                except Exception as e:
                    self.send_queue.push_front_sync(entry)
                    SinricProLogger.error(f"Failed to send message, will retry later: {e}")
                    await asyncio.sleep(1)

            except asyncio.CancelledError:
                break
            except Exception as e:
                SinricProLogger.error(f"Error processing send queue: {e}")
                await asyncio.sleep(0.01)
