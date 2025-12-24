"""
SinricPro Device Base Class

Abstract base class for all SinricPro device types.
"""

import time
from abc import ABC
from typing import Any, TYPE_CHECKING

from sinricpro.core.types import SinricProRequest, RequestHandler
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro import SinricPro


class SinricProDevice(ABC):
    """
    Base class for all SinricPro devices.

    Provides common functionality for device communication,
    request handling, and event sending.
    """

    def __init__(self, device_id: str, product_type: str, **kwargs: Any) -> None:
        """
        Initialize a SinricPro device.

        Args:
            device_id: Unique device ID (24 hex characters)
            product_type: Device product type (e.g., "SWITCH", "LIGHT")
            **kwargs: Additional arguments for mixin classes
        """
        super().__init__(**kwargs)
        self._device_id = device_id
        self._product_type = product_type
        self._sinric_pro: "SinricPro | None" = None
        self._request_handlers: list[RequestHandler] = []

    def get_device_id(self) -> str:
        """
        Get the device ID.

        Returns:
            The device ID string
        """
        return self._device_id

    def get_product_type(self) -> str:
        """
        Get the product type.

        Returns:
            The product type string
        """
        return self._product_type

    def set_sinric_pro(self, sinric_pro: "SinricPro") -> None:
        """
        Set the parent SinricPro instance.

        Args:
            sinric_pro: The SinricPro instance managing this device
        """
        self._sinric_pro = sinric_pro

    def register_request_handler(self, handler: RequestHandler) -> None:
        """
        Register a request handler.

        Args:
            handler: Async function to handle requests

        Example:
            >>> async def handle_request(request: dict) -> bool:
            ...     return True
            >>> device.register_request_handler(handle_request)
        """
        self._request_handlers.append(handler)

    async def handle_request(self, request: SinricProRequest) -> bool:
        """
        Handle an incoming request by calling all registered handlers.

        Args:
            request: The request to handle

        Returns:
            True if request was handled successfully, False otherwise
        """
        try:
            for handler in self._request_handlers:
                success = await handler(request.__dict__)
                if not success:
                    return False
            return True
        except Exception as e:
            SinricProLogger.error(f"Error handling request: {e}")
            return False

    async def send_event(
        self,
        action: str,
        value: dict[str, Any],
        cause: str = "PHYSICAL_INTERACTION",
        instance_id: str = "",
    ) -> bool:
        """
        Send an event to SinricPro.

        Args:
            action: The action type (e.g., "setPowerState")
            value: Event data
            cause: Cause of the event (PHYSICAL_INTERACTION or APP_INTERACTION)
            instance_id: Optional instance ID for multi-instance capabilities

        Returns:
            True if event was sent successfully, False if rate limited

        Example:
            >>> await device.send_event("setPowerState", {"state": "On"})
            True
        """
        if not self._sinric_pro:
            SinricProLogger.error("Device not added to SinricPro instance")
            return False

        payload: dict[str, Any] = {
            "action": action,
            "cause": {"type": cause},
            "createdAt": self._sinric_pro.get_timestamp(),
            "deviceId": self._device_id,
            "type": "event",
            "value": value,
        }

        # Include instanceId if provided
        if instance_id:
            payload["instanceId"] = instance_id

        message = {
            "header": {
                "payloadVersion": 2,
                "signatureVersion": 1,
            },
            "payload": payload,
        }

        try:
            await self._sinric_pro.send_message(message)
            return True
        except Exception as e:
            SinricProLogger.error(f"Failed to send event: {e}")
            return False

    def generate_message_id(self) -> str:
        """
        Generate a unique message ID.

        Returns:
            A unique message ID string

        Example:
            >>> device.generate_message_id()
            '1699999999999-abc123def'
        """
        import random
        import string

        timestamp = int(time.time() * 1000)
        random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=9))
        return f"{timestamp}-{random_str}"
