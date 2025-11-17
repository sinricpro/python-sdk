"""
AirQualitySensor Capability

Provides air quality sensing functionality (PM1.0, PM2.5, PM10).
"""

from typing import Any, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_AIR_QUALITY
from sinricpro.core.types import EVENT_LIMIT_SENSOR_VALUE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice


class AirQualitySensor:
    """
    Mixin providing air quality sensor capability.

    Provides methods to send air quality measurements (PM1.0, PM2.5, PM10).

    Example:
        >>> class MyAirSensor(SinricProDevice, AirQualitySensor):
        ...     pass
        >>> sensor = MyAirSensor("device_id", "AIR_QUALITY_SENSOR")
        >>> await sensor.send_air_quality_event(pm1_0=10, pm2_5=25, pm10=50)
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize AirQualitySensor mixin."""
        super().__init__(*args, **kwargs)
        self._air_quality_limiter = EventLimiter(EVENT_LIMIT_SENSOR_VALUE)

    async def send_air_quality_event(
        self,
        pm1_0: int,
        pm2_5: int,
        pm10: int,
        cause: str = "PHYSICAL_INTERACTION",
    ) -> bool:
        """
        Send an air quality event to SinricPro.

        Args:
            pm1_0: PM1.0 particulate matter concentration (μg/m³)
            pm2_5: PM2.5 particulate matter concentration (μg/m³)
            pm10: PM10 particulate matter concentration (μg/m³)
            cause: Cause of the event (PHYSICAL_INTERACTION or APP_INTERACTION)

        Returns:
            True if event was sent successfully, False if rate limited

        Example:
            >>> await sensor.send_air_quality_event(pm1_0=10, pm2_5=25, pm10=50)
            True
        """
        # Check rate limiting
        if not self._air_quality_limiter.can_send_event():
            SinricProLogger.warn("Air quality event rate limited")
            return False

        # Type check - ensure self is a SinricProDevice
        if not hasattr(self, "send_event"):
            SinricProLogger.error("AirQualitySensor must be mixed with SinricProDevice")
            return False

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(
            action=ACTION_AIR_QUALITY,
            value={"pm1": pm1_0, "pm2_5": pm2_5, "pm10": pm10},
            cause=cause,
        )

        if success:
            self._air_quality_limiter.event_sent()

        return success
