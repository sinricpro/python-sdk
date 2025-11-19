# SinricPro Custom Device Example

Build flexible IoT devices with any combination of capabilities using `SinricProCustomDevice`.

## Overview

The `SinricProCustomDevice` is a flexible device type that supports **all SinricPro capabilities**. Instead of being limited to predefined device types, you can:

- ✅ Mix and match any capabilities you need
- ✅ Create unique device combinations
- ✅ Prototype quickly without creating new device classes
- ✅ Match custom device types from SinricPro portal
- ✅ Only implement the features you actually use

## When to Use Custom Device

Use `SinricProCustomDevice` when:

1. **Unique Combinations**: You need capabilities not available in standard devices
   - Smart mirror with display, camera, and sensors
   - Environmental station with multiple sensors
   - Multi-function control panel

2. **Rapid Prototyping**: Testing ideas quickly
   - Proof of concept projects
   - Hackathon projects
   - Educational demonstrations

3. **SinricPro Portal Custom Types**: Matching custom device types you created in the portal
   - Your portal device has custom capability combinations
   - Experimental features

## All Supported Capabilities

### Power Control
```python
# Power state (on/off)
device.on_power_state(callback)
await device.send_power_state_event(True)

# Power level (0-100)
device.on_power_level(callback)
device.on_adjust_power_level(callback)
await device.send_power_level_event(75)
```

### Lighting Control
```python
# Brightness (0-100)
device.on_brightness(callback)
device.on_adjust_brightness(callback)
await device.send_brightness_event(80)

# RGB Color
device.on_color(callback)
await device.send_color_event(255, 0, 0)  # Red

# Color Temperature (2200-7000K)
device.on_color_temperature(callback)
device.on_increase_color_temperature(callback)
device.on_decrease_color_temperature(callback)
await device.send_color_temperature_event(3000)
```

### Position & Range
```python
# Range value
device.on_range_value(callback)
device.on_adjust_range_value(callback)
await device.send_range_value_event(50)

# Percentage (legacy)
device.on_percentage(callback)
await device.send_percentage_event(75)
```

### Climate Control
```python
# Temperature sensor
await device.send_temperature_event(23.5)

# Thermostat
device.on_thermostat_mode(callback)  # AUTO, COOL, HEAT, etc.
device.on_target_temperature(callback)
await device.send_thermostat_mode_event("HEAT")
await device.send_target_temperature_event(22.0)
```

### Security & Access
```python
# Lock control
device.on_lock_state(callback)  # LOCK/UNLOCK
await device.send_lock_state_event("LOCK")

# Door control
device.on_door_mode(callback)  # OPEN/CLOSE
await device.send_door_mode_event("OPEN")

# Motion sensor
await device.send_motion_event(True)

# Contact sensor
await device.send_contact_event("OPEN")
```

### Camera
```python
# Snapshot
device.on_snapshot(callback)
await device.send_snapshot(image_data)

# Streaming
device.on_get_stream_url(callback)
device.on_get_webrtc_answer(callback)

# Motion detection
await device.send_motion_event(motion_data)
```

### Environmental Sensors
```python
# Air quality
await device.send_air_quality_event(pm25=12, pm10=8, co2=450)

# Power sensor
await device.send_power_usage_event(voltage=120, current=5.2, power=624)
```

### Common Features
```python
# Settings
device.on_setting(callback)

# Push notifications
await device.send_push_notification("Alert message!")
```

## Example Use Cases

### 1. Smart Mirror
```python
from sinricpro import SinricProCustomDevice

mirror = SinricProCustomDevice("device-id", "SMART_MIRROR")

# Display control
mirror.on_power_state(on_power)
mirror.on_brightness(on_brightness)

# Camera for video calls
mirror.on_snapshot(on_snapshot)

# Environmental sensors
async def update_sensors():
    await mirror.send_temperature_event(temp)
    await mirror.send_air_quality_event(pm25=pm25)
```

### 2. Multi-Sensor Weather Station
```python
station = SinricProCustomDevice("device-id", "WEATHER_STATION")

# Send multiple sensor readings
async def update_weather():
    await station.send_temperature_event(temp)
    await station.send_air_quality_event(pm25=pm25, co2=co2)
    await station.send_push_notification(f"Weather update: {temp}°C")
```

### 3. Smart Garden Controller
```python
garden = SinricProCustomDevice("device-id", "GARDEN_CONTROLLER")

# Water pump control
garden.on_power_state(control_pump)

# Soil moisture (using percentage)
garden.on_percentage(set_water_level)
await garden.send_percentage_event(soil_moisture)

# Temperature monitoring
await garden.send_temperature_event(soil_temp)

# Motion detection for animals
await garden.send_motion_event(True)
```

### 4. RGB LED Strip with Sensors
```python
led_strip = SinricProCustomDevice("device-id", "LED_STRIP")

# LED control
led_strip.on_power_state(on_power)
led_strip.on_brightness(on_brightness)
led_strip.on_color(on_color)

# Temperature sensor in controller
await led_strip.send_temperature_event(controller_temp)
```

### 5. Security Control Panel
```python
panel = SinricProCustomDevice("device-id", "SECURITY_PANEL")

# Lock control
panel.on_lock_state(on_lock)

# Sensors
await panel.send_motion_event(motion_detected)
await panel.send_contact_event("OPEN" if door_open else "CLOSED")

# Alerts
await panel.send_push_notification("Security alert!")

# Camera
panel.on_snapshot(capture_snapshot)
```

## Installation

1. Install the SDK:
```bash
pip install sinricpro
```

2. Create a custom device in [SinricPro Portal](https://portal.sinric.pro):
   - Go to Devices → Add Device
   - Select "Custom Device" or any device type
   - Add the capabilities you need
   - Copy your Device ID

3. Set up your credentials:
```bash
export SINRICPRO_APP_KEY="your-app-key"
export SINRICPRO_APP_SECRET="your-app-secret"
```

4. Run the example:
```bash
python customdevice_example.py
```

## Quick Start

```python
import asyncio
from sinricpro import SinricPro, SinricProCustomDevice, SinricProConfig

# Create custom device
device = SinricProCustomDevice("device-id", "MY_CUSTOM_TYPE")

# Register only the callbacks you need
async def on_power_state(state: bool) -> bool:
    print(f"Power: {'On' if state else 'Off'}")
    # Control your hardware here
    return True

async def on_brightness(brightness: int) -> bool:
    print(f"Brightness: {brightness}%")
    # Control brightness here
    return True

device.on_power_state(on_power_state)
device.on_brightness(on_brightness)

# Connect
sinric_pro = SinricPro.get_instance()
sinric_pro.add(device)

config = SinricProConfig(app_key="...", app_secret="...")
await sinric_pro.begin(config)

# Send events
await device.send_power_state_event(True)
await device.send_brightness_event(75)
```

## Best Practices

### 1. Only Register Needed Callbacks
```python
# ✅ Good - Only register what you use
device.on_power_state(on_power)
device.on_brightness(on_brightness)

# ❌ Bad - Don't register everything if you don't use it
device.on_power_state(on_power)
device.on_brightness(on_brightness)
device.on_color(on_color)  # Not used - don't register
device.on_thermostat_mode(on_thermostat)  # Not used - don't register
```

### 2. Use Meaningful Product Types
```python
# ✅ Good - Descriptive type
device = SinricProCustomDevice("id", "WEATHER_STATION")
device = SinricProCustomDevice("id", "SMART_MIRROR")

# ❌ Less clear
device = SinricProCustomDevice("id", "DEVICE1")
```

### 3. Validate State Before Events
```python
# ✅ Good - Check if it makes sense
if device_powered_on:
    await device.send_brightness_event(brightness)

# ❌ Bad - Sending events when device is off
await device.send_brightness_event(brightness)  # Device might be off!
```

### 4. Handle Errors Gracefully
```python
# ✅ Good
async def on_brightness(brightness: int) -> bool:
    try:
        set_hardware_brightness(brightness)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# ❌ Bad - Unhandled exceptions
async def on_brightness(brightness: int) -> bool:
    set_hardware_brightness(brightness)  # Might crash!
    return True
```

## Limitations

1. **Portal Configuration**: Make sure your SinricPro portal device has the capabilities enabled
2. **Voice Assistant Logic**: Some capability combinations may not make sense for voice control
3. **Rate Limiting**: Event sending is rate-limited (60 seconds for state events)
4. **Callback Registration**: You must register callbacks before calling `begin()`

## Common Issues

### Callbacks Not Called
- Ensure the capability is enabled in SinricPro portal
- Check that you registered the callback before `begin()`
- Verify device ID matches portal

### Events Not Sending
- Check rate limiting (max 1 event per 60 seconds for state events)
- Verify device is connected
- Check network connectivity

### "Missing callback function" Error
- You received a request for a capability without a registered callback
- Register the callback or ignore the capability

## Comparison with Specific Device Types

| Feature | Custom Device | Specific Device (e.g., SinricProLight) |
|---------|--------------|---------------------------------------|
| Flexibility | ✅ All capabilities | ❌ Fixed capabilities |
| Simplicity | ❌ More code | ✅ Less code |
| Type Safety | ✅ Good | ✅ Better |
| Use Case | Unique combinations | Standard devices |
| Examples | Weather station, Smart mirror | Light, Switch, Thermostat |

**When to use specific device types:**
- Your device matches a standard type exactly
- You want simpler, more focused code
- You're building a common IoT device

**When to use custom device:**
- You need unique capability combinations
- Rapid prototyping
- Experimental features

## Related Examples

- [Light](../light/) - Dedicated light device
- [Thermostat](../thermostat/) - Dedicated climate control
- [Camera](../camera/) - Dedicated camera device
- [Switch](../switch/) - Simple on/off device

## Additional Resources

- [SinricPro Documentation](https://sinricpro.github.io/python-sdk/)
- [Custom Device API Reference](https://sinricpro.github.io/python-sdk/devices/#sinricprocustomdevice)
- [Capabilities Reference](https://sinricpro.github.io/python-sdk/capabilities/)
- [SinricPro Portal](https://portal.sinric.pro)
