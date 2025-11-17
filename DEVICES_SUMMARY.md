# SinricPro Python SDK - Devices & Capabilities Summary

## Overview

The SinricPro Python SDK now includes **16 device types** with **13 capabilities** for comprehensive IoT device control.

## Implemented Capabilities (13)

### Basic Control
1. **PowerStateController** - On/Off control
2. **BrightnessController** - Brightness control (0-100%)
3. **ColorController** - RGB color control (0-255 per channel)
4. **ColorTemperatureController** - Color temperature (Kelvin)
5. **PercentageController** - Position/level control (0-100%)

### Sensors
6. **MotionSensor** - Motion detection events
7. **ContactSensor** - Contact state events (open/closed)
8. **TemperatureSensor** - Temperature & humidity monitoring
9. **AirQualitySensor** - Air quality measurements (PM1.0, PM2.5, PM10)
10. **PowerSensor** - Power consumption monitoring

### Advanced Control
11. **DoorController** - Door state control (Open/Close)
12. **LockController** - Lock/unlock control
13. **ThermostatController** - Thermostat mode & temperature control

## Implemented Devices (16)

### Lighting & Switches (3)

#### 1. SinricProSwitch
```python
from sinricpro import SinricProSwitch

switch = SinricProSwitch("device_id")
switch.on_power_state(async_callback)
await switch.send_power_state_event(True)
```
**Capabilities:** PowerStateController
**Actions:** setPowerState
**Use Cases:** Smart plugs, relays, simple on/off devices

#### 2. SinricProLight
```python
from sinricpro import SinricProLight

light = SinricProLight("device_id")
light.on_power_state(power_callback)
light.on_brightness(brightness_callback)
light.on_color(color_callback)
light.on_color_temperature(temp_callback)
```
**Capabilities:** PowerState, Brightness, Color, ColorTemperature
**Actions:** setPowerState, setBrightness, setColor, setColorTemperature
**Use Cases:** RGB LED strips, smart bulbs, mood lighting

#### 3. SinricProDimSwitch
```python
from sinricpro import SinricProDimSwitch

dimswitch = SinricProDimSwitch("device_id")
dimswitch.on_power_state(power_callback)
dimswitch.on_brightness(brightness_callback)
```
**Capabilities:** PowerState, Brightness
**Actions:** setPowerState, setBrightness, adjustBrightness
**Use Cases:** Dimmable wall switches, PWM-controlled loads

---

### Sensors (5)

#### 4. SinricProMotionSensor
```python
from sinricpro import SinricProMotionSensor

sensor = SinricProMotionSensor("device_id")
await sensor.send_motion_event(True)  # Motion detected
```
**Capabilities:** MotionSensor
**Events:** setMotion (detected/notDetected)
**Use Cases:** PIR sensors, security systems

#### 5. SinricProContactSensor
```python
from sinricpro import SinricProContactSensor

sensor = SinricProContactSensor("device_id")
await sensor.send_contact_event(False)  # Closed
await sensor.send_contact_event(True)   # Open
```
**Capabilities:** ContactSensor
**Events:** setContactState (open/closed)
**Use Cases:** Door/window sensors, magnetic switches

#### 6. SinricProTemperatureSensor
```python
from sinricpro import SinricProTemperatureSensor

sensor = SinricProTemperatureSensor("device_id")
await sensor.send_temperature_event(22.5, 65.0)  # °C, % humidity
```
**Capabilities:** TemperatureSensor
**Events:** currentTemperature
**Use Cases:** DHT22, BME280, environmental monitoring

#### 7. SinricProAirQualitySensor
```python
from sinricpro import SinricProAirQualitySensor

sensor = SinricProAirQualitySensor("device_id")
await sensor.send_air_quality_event(pm1_0=10, pm2_5=25, pm10=50)
```
**Capabilities:** AirQualitySensor
**Events:** currentAirQuality
**Use Cases:** Air quality monitors, HEPA filter systems

#### 8. SinricProPowerSensor
```python
from sinricpro import SinricProPowerSensor

sensor = SinricProPowerSensor("device_id")
await sensor.send_power_sensor_event(
    voltage=120.0,
    current=2.5,
    power=300.0,
    apparent_power=310.0,
    reactive_power=50.0,
    factor=0.97
)
```
**Capabilities:** PowerSensor
**Events:** currentPowerConsumption
**Use Cases:** Power meters, energy monitoring

---

### Control Devices (3)

#### 9. SinricProBlinds
```python
from sinricpro import SinricProBlinds

blinds = SinricProBlinds("device_id")
blinds.on_percentage(percentage_callback)
await blinds.send_percentage_event(75)  # 75% open
```
**Capabilities:** PercentageController
**Actions:** setPercentage, adjustPercentage
**Use Cases:** Motorized blinds, shades, curtains

#### 10. SinricProGarageDoor
```python
from sinricpro import SinricProGarageDoor

door = SinricProGarageDoor("device_id")
door.on_door_state(door_callback)
await door.send_door_state_event("Open")
```
**Capabilities:** DoorController
**Actions:** setDoorState (Open/Close)
**Use Cases:** Garage door openers, automatic gates

#### 11. SinricProLock
```python
from sinricpro import SinricProLock

lock = SinricProLock("device_id")
lock.on_lock_state(lock_callback)  # True=lock, False=unlock
await lock.send_lock_state_event(True)  # Locked
```
**Capabilities:** LockController
**Actions:** setLockState (LOCKED/UNLOCKED)
**Use Cases:** Smart locks, electronic deadbolts

---

### Climate Control (2)

#### 12. SinricProThermostat
```python
from sinricpro import SinricProThermostat

thermostat = SinricProThermostat("device_id")
thermostat.on_thermostat_mode(mode_callback)  # AUTO, COOL, HEAT, ECO, OFF
thermostat.on_target_temperature(temp_callback)
await thermostat.send_temperature_event(22.5, 65.0)  # Current temp/humidity
await thermostat.send_thermostat_mode_event("COOL")
await thermostat.send_target_temperature_event(20.0)
```
**Capabilities:** ThermostatController, TemperatureSensor
**Actions:** setThermostatMode, targetTemperature
**Use Cases:** Smart thermostats, HVAC control

#### 13. SinricProWindowAC
```python
from sinricpro import SinricProWindowAC

ac = SinricProWindowAC("device_id")
ac.on_power_state(power_callback)
ac.on_thermostat_mode(mode_callback)
ac.on_target_temperature(temp_callback)
```
**Capabilities:** PowerState, ThermostatController, TemperatureSensor
**Actions:** setPowerState, setThermostatMode, targetTemperature
**Use Cases:** Window AC units, portable air conditioners

---

### Other Devices (3)

#### 14. SinricProFan
```python
from sinricpro import SinricProFan

fan = SinricProFan("device_id")
fan.on_power_state(power_callback)
await fan.send_power_state_event(True)
```
**Capabilities:** PowerStateController
**Actions:** setPowerState
**Use Cases:** Ceiling fans, desk fans, exhaust fans

#### 15. SinricProDoorbell
```python
from sinricpro import SinricProDoorbell

doorbell = SinricProDoorbell("device_id")
await doorbell.send_doorbell_event()  # Button pressed
```
**Capabilities:** None (event-only device)
**Events:** DoorbellPress
**Use Cases:** Smart doorbells, button press notifications

---

## Capability Usage Matrix

| Device | Power | Brightness | Color | ColorTemp | Percentage | Motion | Contact | Temp | AirQuality | Power | Door | Lock | Thermostat |
|--------|-------|------------|-------|-----------|------------|--------|---------|------|------------|-------|------|------|------------|
| Switch | ✓ | | | | | | | | | | | | |
| Light | ✓ | ✓ | ✓ | ✓ | | | | | | | | | |
| DimSwitch | ✓ | ✓ | | | | | | | | | | | |
| MotionSensor | | | | | | ✓ | | | | | | | |
| ContactSensor | | | | | | | ✓ | | | | | | |
| TempSensor | | | | | | | | ✓ | | | | | |
| AirQualitySensor | | | | | | | | | ✓ | | | | |
| PowerSensor | | | | | | | | | | ✓ | | | |
| Blinds | | | | | ✓ | | | | | | | | |
| GarageDoor | | | | | | | | | | | ✓ | | |
| Lock | | | | | | | | | | | | ✓ | |
| Thermostat | | | | | | | | ✓ | | | | | ✓ |
| WindowAC | ✓ | | | | | | | ✓ | | | | | ✓ |
| Fan | ✓ | | | | | | | | | | | | |
| Doorbell | | | | | | | | | | | | | |

## Quick Import Guide

```python
# Core
from sinricpro import SinricPro, SinricProConfig

# Lighting & Switches
from sinricpro import SinricProSwitch, SinricProLight, SinricProDimSwitch

# Sensors
from sinricpro import (
    SinricProMotionSensor,
    SinricProContactSensor,
    SinricProTemperatureSensor,
    SinricProAirQualitySensor,
    SinricProPowerSensor,
)

# Control
from sinricpro import SinricProBlinds, SinricProGarageDoor, SinricProLock

# Climate
from sinricpro import SinricProThermostat, SinricProWindowAC

# Other
from sinricpro import SinricProFan, SinricProDoorbell
```

## Common Patterns

### Sensor Pattern (Send Events Only)
```python
sensor = SinricProMotionSensor("device_id")
# No callbacks needed - sensors only send events
await sensor.send_motion_event(True)
```

### Controller Pattern (Receive Commands)
```python
switch = SinricProSwitch("device_id")

async def on_power_state(state: bool) -> bool:
    # Control physical device
    return True

switch.on_power_state(on_power_state)
```

### Hybrid Pattern (Both Send & Receive)
```python
thermostat = SinricProThermostat("device_id")

# Receive commands
thermostat.on_thermostat_mode(mode_callback)
thermostat.on_target_temperature(temp_callback)

# Send sensor readings
await thermostat.send_temperature_event(22.5, 65.0)
```

## Status Summary

✅ **Implemented:** 16 devices, 13 capabilities
✅ **Tested:** Switch, Light working
✅ **Ready to use:** All devices exported and importable
📝 **Examples:** Switch and Light examples available
🚧 **Future:** TV, Speaker (need media capabilities), Camera (needs streaming)

## Next Steps

To use any device:
1. Import the device class
2. Create instance with device ID from SinricPro portal
3. Register callbacks for controllable devices
4. Add to SinricPro instance
5. Send events as needed for sensors

All devices follow the same pattern and integrate seamlessly with the SinricPro SDK!
