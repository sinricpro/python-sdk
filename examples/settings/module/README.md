# Module Settings Example

This example demonstrates how to handle **module-level settings** in SinricPro.

## Module Settings vs Device Settings

SinricPro supports two types of settings:

### Module Settings
- Configuration for the **module (dev board)** itself
- Registered via: `sinric_pro.on_set_setting(callback)`
- Examples: WiFi retry count, log level, heartbeat interval
- Callback signature: `async def callback(setting_id: str, value: Any) -> bool`

### Device Settings
- Configuration for **individual devices**
- Registered via: `device.on_setting(callback)`
- Examples: Device-specific modes, thresholds, tilt settings
- Callback signature: `async def callback(setting_id: str, value: Any) -> bool`

## Usage

```python
from sinricpro import SinricPro

sinric_pro = SinricPro.get_instance()

# Register module-level setting callback
async def on_module_setting(setting_id: str, value: Any) -> bool:
    if setting_id == "wifi_retry_count":
        set_wifi_retry_count(value)
        return True
    return False

sinric_pro.on_set_setting(on_module_setting)
```

## Running the Example

1. Replace `YOUR_DEVICE_ID_HERE` with your actual device ID
2. Set environment variables or replace credentials:
   ```bash
   export SINRICPRO_APP_KEY="your-app-key"
   export SINRICPRO_APP_SECRET="your-app-secret"
   ```
3. Run the example:
   ```bash
   python modulesettings_example.py
   ```

## Setting Value Types

Module settings can have different value types:
- **Integer**: `wifi_retry_count`, `heartbeat_interval`
- **String**: `log_level`
- **Boolean**: `debug_mode`
- **Float**: `temperature_offset`

Always validate the value type and range before applying settings.
