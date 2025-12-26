"""
SinricPro SDK for Python

Official Python SDK for SinricPro - Control IoT devices with Alexa and Google Home.

Copyright (c) 2019-2025 Sinric. All rights reserved.
Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)

This file is part of the SinricPro Python SDK (https://github.com/sinricpro/)
"""

__version__ = "5.0.1"

from sinricpro.core.sinric_pro import SinricPro, SinricProConfig
from sinricpro.core.sinric_pro_device import SinricProDevice
from sinricpro.utils.logger import SinricProLogger, LogLevel

# Devices - Lighting & Switches
from sinricpro.devices.sinric_pro_switch import SinricProSwitch
from sinricpro.devices.sinric_pro_light import SinricProLight
from sinricpro.devices.sinric_pro_dimswitch import SinricProDimSwitch

# Devices - Sensors
from sinricpro.devices.sinric_pro_motion_sensor import SinricProMotionSensor
from sinricpro.devices.sinric_pro_contact_sensor import SinricProContactSensor
from sinricpro.devices.sinric_pro_temperature_sensor import SinricProTemperatureSensor
from sinricpro.devices.sinric_pro_air_quality_sensor import SinricProAirQualitySensor
from sinricpro.devices.sinric_pro_power_sensor import SinricProPowerSensor

# Devices - Control
from sinricpro.devices.sinric_pro_blinds import SinricProBlinds
from sinricpro.devices.sinric_pro_garage_door import SinricProGarageDoor
from sinricpro.devices.sinric_pro_lock import SinricProLock

# Devices - Climate
from sinricpro.devices.sinric_pro_thermostat import SinricProThermostat
from sinricpro.devices.sinric_pro_window_ac import SinricProWindowAC

# Devices - Other
from sinricpro.devices.sinric_pro_fan import SinricProFan
from sinricpro.devices.sinric_pro_doorbell import SinricProDoorbell
from sinricpro.devices.sinric_pro_camera import SinricProCamera
from sinricpro.devices.sinric_pro_custom_device import SinricProCustomDevice
from sinricpro.devices.sinric_pro_speaker import SinricProSpeaker
from sinricpro.devices.sinric_pro_tv import SinricProTV

# Exceptions
from sinricpro.core.exceptions import (
    SinricProError,
    SinricProConnectionError,
    SinricProConfigurationError,
    SinricProDeviceError,
    SinricProSignatureError,
    SinricProTimeoutError,
)

__all__ = [
    # Main classes
    "SinricPro",
    "SinricProConfig",
    "SinricProDevice",
    # Devices - Lighting & Switches
    "SinricProSwitch",
    "SinricProLight",
    "SinricProDimSwitch",
    # Devices - Sensors
    "SinricProMotionSensor",
    "SinricProContactSensor",
    "SinricProTemperatureSensor",
    "SinricProAirQualitySensor",
    "SinricProPowerSensor",
    # Devices - Control
    "SinricProBlinds",
    "SinricProGarageDoor",
    "SinricProLock",
    # Devices - Climate
    "SinricProThermostat",
    "SinricProWindowAC",
    # Devices - Other
    "SinricProFan",
    "SinricProDoorbell",
    "SinricProCamera",
    "SinricProCustomDevice",
    "SinricProSpeaker",
    "SinricProTV",
    # Logger
    "SinricProLogger",
    "LogLevel",
    # Exceptions
    "SinricProError",
    "SinricProConnectionError",
    "SinricProConfigurationError",
    "SinricProDeviceError",
    "SinricProSignatureError",
    "SinricProTimeoutError",
]
