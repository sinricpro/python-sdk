"""
Type Definitions and Constants

Common types, protocols, and constants used throughout the SDK.
"""

from dataclasses import dataclass, field
from typing import Protocol, Any, Callable, Awaitable
import re

from sinricpro.core.exceptions import SinricProConfigurationError

# Constants
SINRICPRO_SERVER_URL = "ws.sinric.pro"
SINRICPRO_SERVER_PORT = 80
SINRICPRO_SERVER_SSL_PORT = 443
WEBSOCKET_PING_INTERVAL = 300000  # 5 minutes in milliseconds
WEBSOCKET_PING_TIMEOUT = 10000  # 10 seconds in milliseconds
EVENT_LIMIT_STATE = 1000  # 1 second in milliseconds
EVENT_LIMIT_SENSOR_VALUE = 60000  # 60 seconds in milliseconds

# Interaction types
PHYSICAL_INTERACTION = "PHYSICAL_INTERACTION"
APP_INTERACTION = "APP_INTERACTION"


# Type aliases
MessageType = str  # "request" or "response"
CallbackResult = bool
RequestHandler = Callable[[dict[str, Any]], Awaitable[CallbackResult]]
ConnectedCallback = Callable[[], None]
DisconnectedCallback = Callable[[], None]
PongCallback = Callable[[int], None]

# Module-level setting callback: (setting_id, value) -> bool
ModuleSettingCallback = Callable[[str, Any], Awaitable[bool]]


@dataclass
class SinricProConfig:
    """
    Configuration for SinricPro SDK.

    Attributes:
        app_key: SinricPro app key (UUID format)
        app_secret: SinricPro app secret (min 32 characters)
        server_url: WebSocket server URL (default: ws.sinric.pro)
        debug: Enable debug logging
    """

    app_key: str
    app_secret: str
    server_url: str = SINRICPRO_SERVER_URL
    debug: bool = False

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        self._validate_app_key()
        self._validate_app_secret()
        self._validate_server_url()

    def _validate_app_key(self) -> None:
        """Validate app_key format (UUID)."""
        if not self.app_key or not isinstance(self.app_key, str):
            raise SinricProConfigurationError("app_key is required and must be a string")

        # UUID format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        uuid_pattern = re.compile(r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$", re.IGNORECASE)
        if not uuid_pattern.match(self.app_key):
            raise SinricProConfigurationError(
                "Invalid app_key format. Expected format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            )

    def _validate_app_secret(self) -> None:
        """Validate app_secret length."""
        if not self.app_secret or not isinstance(self.app_secret, str):
            raise SinricProConfigurationError("app_secret is required and must be a string")

        if len(self.app_secret) < 32:
            raise SinricProConfigurationError(
                "Invalid app_secret: must be at least 32 characters long"
            )

    def _validate_server_url(self) -> None:
        """Validate server_url format."""
        if not self.server_url or not isinstance(self.server_url, str):
            raise SinricProConfigurationError("server_url must be a non-empty string")

        if not self.server_url.strip():
            raise SinricProConfigurationError("server_url must be a non-empty string")


@dataclass
class SinricProRequest:
    """
    Represents a request from SinricPro.

    Attributes:
        action: The action to perform (e.g., "setPowerState")
        instance: Instance ID for the request
        request_value: Input values for the request
        response_value: Output values to send in response
        error_message: Error message if request failed
    """

    action: str
    instance: str = ""
    request_value: dict[str, Any] = field(default_factory=dict)
    response_value: dict[str, Any] = field(default_factory=dict)
    error_message: str | None = None


@dataclass
class SinricProMessage:
    """
    Represents a SinricPro message.

    Attributes:
        header: Message header with version info
        payload: Message payload with action and data
        signature: Message signature for validation
    """

    header: dict[str, Any] = field(default_factory=dict)
    payload: dict[str, Any] = field(default_factory=dict)
    signature: dict[str, str] = field(default_factory=dict)


class ISinricPro(Protocol):
    """Protocol defining the SinricPro interface for devices."""

    async def send_message(self, message: dict[str, Any]) -> None:
        """Send a message to SinricPro."""
        ...

    def get_timestamp(self) -> int:
        """Get current timestamp in seconds."""
        ...

    def sign(self, message: str) -> str:
        """Sign a message."""
        ...
