"""SettingController Capability - Generic settings management."""
from typing import Any, Callable, Awaitable, TYPE_CHECKING
from sinricpro.utils.logger import SinricProLogger

if TYPE_CHECKING:
    from sinricpro.core.sinric_pro_device import SinricProDevice

SettingCallback = Callable[[str, Any], Awaitable[bool]]

class SettingController:
    """Mixin providing settings management capability."""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._setting_callback: SettingCallback | None = None

    def on_setting(self, callback: SettingCallback) -> None:
        """Register callback for setting changes (setting name, value)."""
        self._setting_callback = callback

    async def handle_setting_request(self, setting: str, value: Any, device: "SinricProDevice") -> tuple[bool, dict[str, Any]]:
        """Handle setSetting request."""
        if not self._setting_callback:
            SinricProLogger.error(f"No setting callback registered for {device.get_device_id()}")
            return False, {}
        try:
            success = await self._setting_callback(setting, value)
            return (True, {"setting": setting, "value": value}) if success else (False, {})
        except Exception as e:
            SinricProLogger.error(f"Error in setting callback: {e}")
            return False, {}
