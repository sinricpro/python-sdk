"""
SinricPro SDK Exceptions

Custom exception hierarchy for clear error handling.
"""


class SinricProError(Exception):
    """Base exception for all SinricPro SDK errors."""

    pass


class SinricProConnectionError(SinricProError):
    """Raised when WebSocket connection errors occur."""

    pass


class SinricProConfigurationError(SinricProError):
    """Raised when configuration validation fails."""

    pass


class SinricProDeviceError(SinricProError):
    """Raised for device-related errors."""

    pass


class SinricProSignatureError(SinricProError):
    """Raised when message signature validation fails."""

    pass


class SinricProTimeoutError(SinricProError):
    """Raised when timeout errors occur (ping/pong, etc.)."""

    pass
