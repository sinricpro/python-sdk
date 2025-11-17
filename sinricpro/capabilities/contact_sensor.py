"""
ContactSensor Capability

Provides contact/door sensor functionality.
"""

from typing import Any, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_SET_CONTACT_STATE
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice


class ContactSensor:
    """
    Mixin providing contact sensor capability.

    Provides methods to send contact state events (open/closed).

    Example:
        >>> class MyContactSensor(SinricProDevice, ContactSensor):
        ...     pass
        >>> sensor = MyContactSensor("device_id", "CONTACT_SENSOR")
        >>> await sensor.send_contact_event(False)  # Door closed
        >>> await sensor.send_contact_event(True)   # Door open
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize ContactSensor mixin."""
        super().__init__(*args, **kwargs)
        self._contact_limiter = EventLimiter(EVENT_LIMIT_STATE)

    async def send_contact_event(self, detected: bool, cause: str = "PHYSICAL_INTERACTION") -> bool:
        """
        Send a contact state event to SinricPro.

        Args:
            detected: True if contact detected (open), False if not detected (closed)
            cause: Cause of the event (PHYSICAL_INTERACTION or APP_INTERACTION)

        Returns:
            True if event was sent successfully, False if rate limited

        Example:
            >>> await sensor.send_contact_event(True)   # Contact open
            True
            >>> await sensor.send_contact_event(False)  # Contact closed
            True
        """
        # Check rate limiting
        if not self._contact_limiter.can_send_event():
            SinricProLogger.warn("Contact event rate limited")
            return False

        # Type check - ensure self is a SinricProDevice
        if not hasattr(self, "send_event"):
            SinricProLogger.error("ContactSensor must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(
            action=ACTION_SET_CONTACT_STATE,
            value={"state": "open" if detected else "closed"},
            cause=cause,
        )

        if success:
            self._contact_limiter.event_sent()

        return success
