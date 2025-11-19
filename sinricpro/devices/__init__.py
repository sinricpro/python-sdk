"""
SinricPro Devices

Device implementations for SinricPro.
"""

# Lighting & Switches
from sinricpro.devices.sinric_pro_light import SinricProLight
from sinricpro.devices.sinric_pro_switch import SinricProSwitch
from sinricpro.devices.sinric_pro_dimswitch import SinricProDimSwitch

# Sensors
from sinricpro.devices.sinric_pro_motion_sensor import SinricProMotionSensor
from sinricpro.devices.sinric_pro_contact_sensor import SinricProContactSensor
from sinricpro.devices.sinric_pro_temperature_sensor import SinricProTemperatureSensor
from sinricpro.devices.sinric_pro_air_quality_sensor import SinricProAirQualitySensor
from sinricpro.devices.sinric_pro_power_sensor import SinricProPowerSensor

# Control Devices
from sinricpro.devices.sinric_pro_blinds import SinricProBlinds
from sinricpro.devices.sinric_pro_garage_door import SinricProGarageDoor
from sinricpro.devices.sinric_pro_lock import SinricProLock

# Climate Control
from sinricpro.devices.sinric_pro_thermostat import SinricProThermostat
from sinricpro.devices.sinric_pro_window_ac import SinricProWindowAC

# Other
from sinricpro.devices.sinric_pro_fan import SinricProFan
from sinricpro.devices.sinric_pro_doorbell import SinricProDoorbell
from sinricpro.devices.sinric_pro_camera import SinricProCamera

__all__ = [
    # Lighting & Switches
    "SinricProSwitch",
    "SinricProLight",
    "SinricProDimSwitch",
    # Sensors
    "SinricProMotionSensor",
    "SinricProContactSensor",
    "SinricProTemperatureSensor",
    "SinricProAirQualitySensor",
    "SinricProPowerSensor",
    # Control Devices
    "SinricProBlinds",
    "SinricProGarageDoor",
    "SinricProLock",
    # Climate Control
    "SinricProThermostat",
    "SinricProWindowAC",
    # Other
    "SinricProFan",
    "SinricProDoorbell",
    "SinricProCamera",
]
