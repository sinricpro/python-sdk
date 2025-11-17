"""
TemperatureSensor Capability

Provides temperature and humidity sensing functionality.
"""

from typing import Any, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_CURRENT_TEMPERATURE
from sinricpro.core.types import EVENT_LIMIT_SENSOR_VALUE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice


class TemperatureSensor:
    """
    Mixin providing temperature and humidity sensor capability.

    Provides methods to send temperature and humidity events.

    Example:
        >>> class MyTempSensor(SinricProDevice, TemperatureSensor):
        ...     pass
        >>> sensor = MyTempSensor("device_id", "TEMPERATURE_SENSOR")
        >>> await sensor.send_temperature_event(22.5, 65.0)  # 22.5°C, 65% humidity
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize TemperatureSensor mixin."""
        super().__init__(*args, **kwargs)
        self._temperature_limiter = EventLimiter(EVENT_LIMIT_SENSOR_VALUE)

    async def send_temperature_event(
        self,
        temperature: float,
        humidity: float | None = None,
        cause: str = "PHYSICAL_INTERACTION",
    ) -> bool:
        """
        Send a temperature (and optionally humidity) event to SinricPro.

        Args:
            temperature: Temperature value in Celsius
            humidity: Optional humidity value in percentage (0-100)
            cause: Cause of the event (PHYSICAL_INTERACTION or APP_INTERACTION)

        Returns:
            True if event was sent successfully, False if rate limited

        Example:
            >>> await sensor.send_temperature_event(22.5)  # Temperature only
            True
            >>> await sensor.send_temperature_event(22.5, 65.0)  # Temperature + humidity
            True
        """
        # Check rate limiting
        if not self._temperature_limiter.can_send_event():
            SinricProLogger.warn("Temperature event rate limited")
            return False

        # Type check - ensure self is a SinricProDevice
        if not hasattr(self, "send_event"):
            SinricProLogger.error("TemperatureSensor must be mixed with SinricProDevice")
            return False

        # Build value dict
        value: dict[str, Any] = {"temperature": temperature}
        if humidity is not None:
            value["humidity"] = humidity

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(
            action=ACTION_CURRENT_TEMPERATURE,
            value=value,
            cause=cause,
        )

        if success:
            self._temperature_limiter.event_sent()

        return success
