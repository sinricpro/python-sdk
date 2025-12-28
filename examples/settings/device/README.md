# Device Settings Example

This example demonstrates how to handle **device-level settings** in SinricPro.

## Device Settings vs Module Settings

SinricPro supports two types of settings:

### Device Settings
- Configuration for **this specific device**
- Registered via: `device.on_setting(callback)`
- Examples: Tilt angle, speed, direction, auto-close timeout
- Callback signature: `async def callback(setting_id: str, value: Any) -> bool`
- Settings are configured per-device in the SinricPro portal

### Module Settings
- Configuration for the **module (dev board)** itself
- Registered via: `sinric_pro.on_set_setting(callback)`
- Examples: WiFi retry count, log level, heartbeat interval
- Callback signature: `async def callback(setting_id: str, value: Any) -> bool`

## Usage

```python
from sinricpro import SinricProBlinds

blinds = SinricProBlinds("your-device-id")

# Register device-level setting callback
async def on_device_setting(setting_id: str, value: Any) -> bool:
    if setting_id == "tilt":
        set_blinds_tilt(value)
        return True
    elif setting_id == "speed":
        set_motor_speed(value)
        return True
    return False

blinds.on_setting(on_device_setting)
```

## Setting Value Types

Device settings can have different value types:

| Setting | Type | Example Values |
|---------|------|----------------|
| `tilt` | Integer | 0-100 |
| `direction` | String | "up", "down" |
| `speed` | String | "slow", "normal", "fast" |
| `auto_close` | Boolean | true, false |
| `close_timeout` | Integer | 60-3600 (seconds) |

## Running the Example

1. Replace `YOUR_DEVICE_ID_HERE` with your actual device ID
2. Set environment variables or replace credentials:
   ```bash
   export SINRICPRO_APP_KEY="your-app-key"
   export SINRICPRO_APP_SECRET="your-app-secret"
   ```
3. Run the example:
   ```bash
   python device_settings_example.py
   ```

## Configuring Settings in SinricPro Portal

Device settings are configured in the SinricPro portal:

1. Go to [sinric.pro](https://sinric.pro)
2. Navigate to your device
3. Click on "Settings" tab
4. Add or modify settings with their IDs and values
5. Save changes - the SDK will receive the new values via the callback

## Best Practices

1. **Validate Values**: Always validate setting values before applying them
2. **Type Checking**: Check the value type matches what you expect
3. **Range Validation**: Ensure numeric values are within valid ranges
4. **Return False on Error**: Return `False` if a setting cannot be applied
5. **Persist Settings**: Consider saving settings to non-volatile storage
