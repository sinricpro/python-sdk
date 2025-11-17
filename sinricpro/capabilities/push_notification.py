"""
PushNotification Capability

Provides push notification functionality.
"""

from typing import Any, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_PUSH_NOTIFICATION
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice


class PushNotification:
    """
    Mixin providing push notification capability.

    Allows devices to send push notifications to user's phone/app.

    Example:
        >>> class MyDevice(SinricProDevice, PushNotification):
        ...     pass
        >>> device = MyDevice("device_id", "SWITCH")
        >>> await device.send_push_notification("Door opened!")
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize PushNotification mixin."""
        super().__init__(*args, **kwargs)
        self._push_notification_limiter = EventLimiter(EVENT_LIMIT_STATE)

    async def send_push_notification(
        self, notification: str, cause: str = "PHYSICAL_INTERACTION"
    ) -> bool:
        """
        Send a push notification to SinricPro.

        Args:
            notification: The notification message text
            cause: Cause of the event (PHYSICAL_INTERACTION or APP_INTERACTION)

        Returns:
            True if notification was sent successfully, False if rate limited

        Example:
            >>> await device.send_push_notification("Motion detected at front door!")
            True
        """
        # Check rate limiting
        if not self._push_notification_limiter.can_send_event():
            SinricProLogger.warn("Push notification event rate limited")
            return False

        # Type check - ensure self is a SinricProDevice
        if not hasattr(self, "send_event"):
            SinricProLogger.error("PushNotification must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(
            action=ACTION_PUSH_NOTIFICATION,
            value={"alert": notification},
            cause=cause,
        )

        if success:
            self._push_notification_limiter.event_sent()

        return success
