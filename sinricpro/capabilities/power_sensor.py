"""
PowerSensor Capability

Provides power consumption monitoring functionality with energy tracking.
"""

import time
from typing import Any, TYPE_CHECKING

from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_POWER_USAGE
from sinricpro.core.types import EVENT_LIMIT_SENSOR_VALUE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice


class PowerSensor:
    """
    Mixin providing power sensor capability.

    Provides methods to send power consumption measurements with energy tracking.
    Automatically calculates wattHours (energy consumption) based on time and power.

    Example:
        >>> class MyPowerSensor(SinricProDevice, PowerSensor):
        ...     pass
        >>> sensor = MyPowerSensor("device_id", "POWER_SENSOR")
        >>> await sensor.send_power_sensor_event(voltage=120.0, current=2.5, power=300.0)
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize PowerSensor mixin."""
        super().__init__(*args, **kwargs)
        self._power_sensor_limiter = EventLimiter(EVENT_LIMIT_SENSOR_VALUE)
        self._start_time: int = 0  # Timestamp when last event was sent
        self._last_power: float = 0.0  # Last power reading in watts

    def _get_watt_hours(self, current_timestamp: int) -> float:
        """
        Calculate energy consumption (wattHours) since last event.

        Args:
            current_timestamp: Current Unix timestamp in seconds

        Returns:
            Energy consumption in watt-hours (Wh)
        """
        if self._start_time == 0:
            return 0.0

        # Calculate time difference in hours
        time_hours = (current_timestamp - self._start_time) / 3600.0

        # Energy = Power × Time
        watt_hours = self._last_power * time_hours

        return watt_hours

    async def send_power_sensor_event(
        self,
        voltage: float,
        current: float,
        power: float | None = None,
        apparent_power: float | None = None,
        reactive_power: float | None = None,
        factor: float | None = None,
        cause: str = "PERIODIC_POLL",
    ) -> bool:
        """
        Send a power measurement event to SinricPro.

        Args:
            voltage: Voltage in volts (V)
            current: Current in amperes (A)
            power: Optional active power in watts (W). If not provided, calculated as voltage × current
            apparent_power: Optional apparent power in volt-amperes (VA)
            reactive_power: Optional reactive power in volt-amperes reactive (VAR)
            factor: Optional power factor (0-1). If not provided but apparentPower is, calculated as power / apparentPower
            cause: Cause of the event (default: "PERIODIC_POLL")

        Returns:
            True if event was sent successfully, False if rate limited

        Example:
            >>> await sensor.send_power_sensor_event(120.0, 2.5)  # Auto-calculate power
            True
            >>> await sensor.send_power_sensor_event(120.0, 2.5, 300.0, 310.0, 50.0, 0.97)
            True
        """
        # Check rate limiting
        if not self._power_sensor_limiter.can_send_event():
            SinricProLogger.warn("Power sensor event rate limited")
            return False

        # Type check - ensure self is a SinricProDevice
        if not hasattr(self, "send_event"):
            SinricProLogger.error("PowerSensor must be mixed with SinricProDevice")
            return False

        # Auto-calculate power if not provided
        if power is None:
            power = voltage * current

        # Auto-calculate power factor if apparentPower is provided but factor is not
        if factor is None and apparent_power is not None and apparent_power > 0:
            factor = power / apparent_power

        # Get current timestamp
        current_timestamp = int(time.time())

        # Calculate wattHours
        watt_hours = self._get_watt_hours(current_timestamp)

        # Build value dict
        value: dict[str, Any] = {
            "startTime": self._start_time,
            "voltage": voltage,
            "current": current,
            "power": power,
            "apparentPower": apparent_power if apparent_power is not None else -1,
            "reactivePower": reactive_power if reactive_power is not None else -1,
            "factor": factor if factor is not None else -1,
            "wattHours": watt_hours,
        }

        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(
            action=ACTION_POWER_USAGE,
            value=value,
            cause=cause,
        )

        if success:
            self._power_sensor_limiter.event_sent()
            # Update tracking variables for next calculation
            self._start_time = current_timestamp
            self._last_power = power

        return success
