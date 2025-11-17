"""ThermostatController Capability - Provides thermostat control."""
from typing import Any, Callable, Awaitable, TYPE_CHECKING
from sinricpro.core.event_limiter import EventLimiter
from sinricpro.core.actions import ACTION_SET_THERMOSTAT_MODE, ACTION_TARGET_TEMPERATURE
from sinricpro.core.types import EVENT_LIMIT_STATE
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice

ThermostatModeCallback = Callable[[str], Awaitable[bool]]
TargetTemperatureCallback = Callable[[float], Awaitable[bool]]

class ThermostatController:
    """Mixin providing thermostat control capability."""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._thermostat_mode_callback: ThermostatModeCallback | None = None
        self._target_temperature_callback: TargetTemperatureCallback | None = None
        self._thermostat_limiter = EventLimiter(EVENT_LIMIT_STATE)

    def on_thermostat_mode(self, callback: ThermostatModeCallback) -> None:
        """Register callback for mode changes (AUTO, COOL, HEAT, ECO, OFF)."""
        self._thermostat_mode_callback = callback

    def on_target_temperature(self, callback: TargetTemperatureCallback) -> None:
        """Register callback for target temperature changes."""
        self._target_temperature_callback = callback

    async def handle_thermostat_mode_request(self, mode: str, device: "SinricProDevice") -> tuple[bool, dict[str, Any]]:
        """Handle setThermostatMode request."""
        if not self._thermostat_mode_callback:
            SinricProLogger.error(f"No thermostat mode callback for {device.get_device_id()}")
            return False, {}
        try:
            success = await self._thermostat_mode_callback(mode)
            return (True, {"thermostatMode": mode}) if success else (False, {})
        except Exception as e:
            SinricProLogger.error(f"Error in thermostat mode callback: {e}")
            return False, {}

    async def handle_target_temperature_request(self, temperature: float, device: "SinricProDevice") -> tuple[bool, dict[str, Any]]:
        """Handle setTargetTemperature request."""
        if not self._target_temperature_callback:
            SinricProLogger.error(f"No target temperature callback for {device.get_device_id()}")
            return False, {}
        try:
            success = await self._target_temperature_callback(temperature)
            return (True, {"temperature": temperature}) if success else (False, {})
        except Exception as e:
            SinricProLogger.error(f"Error in target temperature callback: {e}")
            return False, {}

    async def send_thermostat_mode_event(self, mode: str, cause: str = "PHYSICAL_INTERACTION") -> bool:
        """Send thermostat mode event."""
        if not self._thermostat_limiter.can_send_event():
            return False
        if not hasattr(self, "send_event"):
            return False
        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(action=ACTION_SET_THERMOSTAT_MODE, value={"thermostatMode": mode}, cause=cause)
        if success:
            self._thermostat_limiter.event_sent()
        return success

    async def send_target_temperature_event(self, temperature: float, cause: str = "PHYSICAL_INTERACTION") -> bool:
        """Send target temperature event."""
        if not self._thermostat_limiter.can_send_event():
            return False
        if not hasattr(self, "send_event"):
            return False
        device: SinricProDevice = self  # type: ignore
        success = await device.send_event(action=ACTION_TARGET_TEMPERATURE, value={"temperature": temperature}, cause=cause)
        if success:
            self._thermostat_limiter.event_sent()
        return success
