"""
WebSocket Client

Manages WebSocket connection to SinricPro server with auto-reconnection
and heartbeat monitoring.
"""

import asyncio
import time
from typing import Callable

import websockets
from websockets.client import WebSocketClientProtocol

from sinricpro import __version__
from sinricpro.core.exceptions import SinricProConnectionError, SinricProTimeoutError
from sinricpro.core.types import (
    SINRICPRO_SERVER_SSL_PORT,
    WEBSOCKET_PING_INTERVAL,
    WEBSOCKET_PING_TIMEOUT,
)
from sinricpro.utils.logger import SinricProLogger


class WebSocketConfig:
    """Configuration for WebSocket connection."""

    def __init__(
        self,
        server_url: str,
        app_key: str,
        device_ids: list[str],
        platform: str = "Python",
        sdk_version: str | None = None,
    ) -> None:
        self.server_url = server_url
        self.app_key = app_key
        self.device_ids = device_ids
        self.platform = platform
        self.sdk_version = sdk_version or __version__


class WebSocketClient:
    """
    WebSocket client for SinricPro communication.

    Handles connection, auto-reconnection, and heartbeat monitoring.
    """

    def __init__(self, config: WebSocketConfig) -> None:
        """
        Initialize WebSocket client.

        Args:
            config: WebSocket configuration
        """
        self.config = config
        self.ws: WebSocketClientProtocol | None = None
        self.connected = False
        self.should_reconnect = True
        self.last_ping_time = 0.0
        self._ping_task: asyncio.Task[None] | None = None
        self._pong_timeout_task: asyncio.Task[None] | None = None
        self._reconnect_task: asyncio.Task[None] | None = None
        self._message_callbacks: list[Callable[[str], None]] = []
        self._connected_callbacks: list[Callable[[], None]] = []
        self._disconnected_callbacks: list[Callable[[], None]] = []
        self._pong_callbacks: list[Callable[[int], None]] = []
        self._error_callbacks: list[Callable[[Exception], None]] = []

    def on_message(self, callback: Callable[[str], None]) -> None:
        """Register callback for incoming messages."""
        self._message_callbacks.append(callback)

    def on_connected(self, callback: Callable[[], None]) -> None:
        """Register callback for connection event."""
        self._connected_callbacks.append(callback)

    def on_disconnected(self, callback: Callable[[], None]) -> None:
        """Register callback for disconnection event."""
        self._disconnected_callbacks.append(callback)

    def on_pong(self, callback: Callable[[int], None]) -> None:
        """Register callback for pong responses."""
        self._pong_callbacks.append(callback)

    def on_error(self, callback: Callable[[Exception], None]) -> None:
        """Register callback for errors."""
        self._error_callbacks.append(callback)

    async def connect(self) -> None:
        """
        Connect to SinricPro WebSocket server.

        Raises:
            SinricProConnectionError: If connection fails
        """
        if self.connected:
            SinricProLogger.warn("WebSocket already connected")
            return

        protocol = "wss"
        port = SINRICPRO_SERVER_SSL_PORT
        uri = f"{protocol}://{self.config.server_url}:{port}/"

        headers = {
            "appkey": self.config.app_key,
            "deviceids": ";".join(self.config.device_ids),
            "platform": self.config.platform,
            "SDKVersion": self.config.sdk_version,
        }

        SinricProLogger.debug(f"Connecting to {uri}")
        SinricProLogger.debug(f"WebSocket headers: {headers}")

        try:
            self.ws = await websockets.connect(uri, additional_headers=headers)
            self.connected = True
            SinricProLogger.debug("WebSocket connected")

            # Start heartbeat
            self._start_heartbeat()

            # Notify connected callbacks
            for callback in self._connected_callbacks:
                callback()

            # Start message handler
            asyncio.create_task(self._handle_messages())

        except Exception as e:
            error_msg = f"WebSocket connection failed: {e}"
            SinricProLogger.error(error_msg)
            for callback in self._error_callbacks:
                callback(e)
            raise SinricProConnectionError(error_msg) from e

    async def _handle_messages(self) -> None:
        """Handle incoming WebSocket messages."""
        if not self.ws:
            return

        try:
            async for message in self.ws:
                if isinstance(message, str):
                    SinricProLogger.debug(f"WebSocket received: {message}")
                    for callback in self._message_callbacks:
                        callback(message)
                elif isinstance(message, bytes):
                    # Handle pong messages
                    latency = int((time.time() - self.last_ping_time) * 1000)
                    SinricProLogger.debug(f"WebSocket pong received (latency: {latency}ms)")

                    # Cancel pong timeout
                    if self._pong_timeout_task:
                        self._pong_timeout_task.cancel()
                        self._pong_timeout_task = None

                    for callback in self._pong_callbacks:
                        callback(latency)

        except websockets.exceptions.ConnectionClosed:
            SinricProLogger.info("WebSocket connection closed")
        except Exception as e:
            SinricProLogger.error(f"Error handling messages: {e}")
        finally:
            await self._handle_disconnect()

    async def _handle_disconnect(self) -> None:
        """Handle disconnection."""
        self.connected = False
        self._stop_heartbeat()
        SinricProLogger.info("WebSocket disconnected")

        # Notify disconnected callbacks
        for callback in self._disconnected_callbacks:
            callback()

        if self.should_reconnect:
            self._schedule_reconnect()

    def send(self, message: str) -> None:
        """
        Send a message through the WebSocket.

        Args:
            message: Message string to send

        Raises:
            SinricProConnectionError: If not connected
        """
        if not self.ws or not self.connected:
            error_msg = "Cannot send message: WebSocket not connected"
            SinricProLogger.error(error_msg)
            raise SinricProConnectionError(error_msg)

        SinricProLogger.debug(f"WebSocket sending: {message}")
        asyncio.create_task(self.ws.send(message))

    def is_connected(self) -> bool:
        """Check if WebSocket is connected."""
        return self.connected

    def _start_heartbeat(self) -> None:
        """Start heartbeat ping/pong."""
        self._ping_task = asyncio.create_task(self._heartbeat_loop())

    async def _heartbeat_loop(self) -> None:
        """Heartbeat loop to send pings."""
        while self.connected and self.ws:
            await asyncio.sleep(WEBSOCKET_PING_INTERVAL / 1000.0)  # Convert to seconds

            if self.ws and self.connected:
                try:
                    self.last_ping_time = time.time()
                    await self.ws.ping()
                    SinricProLogger.debug("WebSocket ping sent")

                    # Set timeout for pong
                    self._pong_timeout_task = asyncio.create_task(self._pong_timeout())

                except Exception as e:
                    SinricProLogger.error(f"Error sending ping: {e}")

    async def _pong_timeout(self) -> None:
        """Handle pong timeout."""
        try:
            await asyncio.sleep(WEBSOCKET_PING_TIMEOUT / 1000.0)
            SinricProLogger.error("WebSocket pong timeout - connection appears dead")

            # Force close connection
            if self.ws:
                await self.ws.close()

        except asyncio.CancelledError:
            # Pong was received in time
            pass

    def _stop_heartbeat(self) -> None:
        """Stop heartbeat tasks."""
        if self._ping_task:
            self._ping_task.cancel()
            self._ping_task = None

        if self._pong_timeout_task:
            self._pong_timeout_task.cancel()
            self._pong_timeout_task = None

    def _schedule_reconnect(self) -> None:
        """Schedule automatic reconnection."""
        if self._reconnect_task:
            self._reconnect_task.cancel()

        self._reconnect_task = asyncio.create_task(self._reconnect())

    async def _reconnect(self) -> None:
        """Attempt to reconnect."""
        await asyncio.sleep(5)  # Wait 5 seconds before reconnecting
        SinricProLogger.info("Attempting to reconnect...")

        try:
            await self.connect()
        except Exception as e:
            SinricProLogger.error(f"Reconnection failed: {e}")

    def update_device_list(self, device_ids: list[str]) -> None:
        """
        Update the list of devices.

        Args:
            device_ids: New list of device IDs
        """
        self.config.device_ids = device_ids

    async def disconnect(self) -> None:
        """Disconnect from WebSocket server."""
        self.should_reconnect = False

        if self._reconnect_task:
            self._reconnect_task.cancel()
            self._reconnect_task = None

        self._stop_heartbeat()

        if self.ws:
            await self.ws.close()
            self.ws = None

        self.connected = False
