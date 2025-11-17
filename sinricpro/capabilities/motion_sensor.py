"""
MotionSensor Capability

Provides motion detection functionality.
"""

from typing import Any, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_MOTION
from sinricpro.core.types import EVENT_LIMIT_SENSOR_VALUE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice


class MotionSensor:
    """
    Mixin providing motion sensor capability.

    Provides methods to send motion detection events.

    Example:
        >>> class MyMotionSensor(SinricProDevice, MotionSensor):
        ...     pass
        >>> sensor = MyMotionSensor("device_id", "MOTION_SENSOR")
        >>> await sensor.send_motion_event(True)  # Motion detected
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize MotionSensor mixin."""
        super().__init__(*args, **kwargs)
        self._motion_limiter = EventLimiter()

    async def send_motion_event(self, detected: bool, cause: str = "PHYSICAL_INTERACTION") -> bool:
        """
        Send a motion detection event to SinricPro.

        Args:
            detected: True if motion detected, False if no motion
            cause: Cause of the event (PHYSICAL_INTERACTION or APP_INTERACTION)

        Returns:
            True if event was sent successfully, False if rate limited

        Example:
            >>> await sensor.send_motion_event(True)  # Motion detected
            True
            >>> await sensor.send_motion_event(False)  # No motion
            True
        """
        # Check rate limiting
        if not self._motion_limiter.can_send_event():
            SinricProLogger.warn("Motion event rate limited")
            return False

        # Type check - ensure self is a SinricProDevice
        if not hasattr(self, "send_event"):
            SinricProLogger.error("MotionSensor must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(
            action=ACTION_MOTION,
            value={"state": "detected" if detected else "notDetected"},
            cause=cause,
        )   

        if success:
            self._motion_limiter.event_sent()

        return success
