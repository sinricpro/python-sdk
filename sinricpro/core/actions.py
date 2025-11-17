"""
SinricPro Action Constants

Centralized action string constants used across the SinricPro SDK.
"""

# Power Control Actions
ACTION_SET_POWER_STATE = "setPowerState"

# Brightness Control Actions
ACTION_SET_BRIGHTNESS = "setBrightness"
ACTION_ADJUST_BRIGHTNESS = "adjustBrightness"

# Power Level Control Actions
ACTION_SET_POWER_LEVEL = "setPowerLevel"
ACTION_ADJUST_POWER_LEVEL = "adjustPowerLevel"

# Color Control Actions
ACTION_SET_COLOR = "setColor"
ACTION_SET_COLOR_TEMPERATURE = "setColorTemperature"
ACTION_INCREASE_COLOR_TEMPERATURE = "increaseColorTemperature"
ACTION_DECREASE_COLOR_TEMPERATURE = "decreaseColorTemperature"

# Range/Position Control Actions
ACTION_SET_RANGE_VALUE = "setRangeValue"
ACTION_ADJUST_RANGE_VALUE = "adjustRangeValue"

# Lock Control Actions
ACTION_SET_LOCK_STATE = "setLockState"

# Door Control Actions
ACTION_SET_MODE = "setMode"

# Thermostat Control Actions
ACTION_SET_THERMOSTAT_MODE = "setThermostatMode"
ACTION_TARGET_TEMPERATURE = "targetTemperature"

# Settings Actions
ACTION_SET_SETTING = "setSetting"

# Sensor Event Actions
ACTION_MOTION = "motion"
ACTION_SET_CONTACT_STATE = "setContactState"
ACTION_CURRENT_TEMPERATURE = "currentTemperature"
ACTION_AIR_QUALITY = "airQuality"
ACTION_POWER_USAGE = "powerUsage"

# Notification Actions
ACTION_PUSH_NOTIFICATION = "pushNotification"

# Doorbell Actions
ACTION_DOORBELL_PRESS = "DoorbellPress"

# Percentage Control Actions (Legacy)
ACTION_SET_PERCENTAGE = "setPercentage"


# Export all action constants
__all__ = [
    # Power Control
    "ACTION_SET_POWER_STATE",
    # Brightness Control
    "ACTION_SET_BRIGHTNESS",
    "ACTION_ADJUST_BRIGHTNESS",
    # Power Level Control
    "ACTION_SET_POWER_LEVEL",
    "ACTION_ADJUST_POWER_LEVEL",
    # Color Control
    "ACTION_SET_COLOR",
    "ACTION_SET_COLOR_TEMPERATURE",
    "ACTION_INCREASE_COLOR_TEMPERATURE",
    "ACTION_DECREASE_COLOR_TEMPERATURE",
    # Range/Position Control
    "ACTION_SET_RANGE_VALUE",
    "ACTION_ADJUST_RANGE_VALUE",
    # Lock Control
    "ACTION_SET_LOCK_STATE",
    # Door Control
    "ACTION_SET_MODE",
    # Thermostat Control
    "ACTION_SET_THERMOSTAT_MODE",
    "ACTION_TARGET_TEMPERATURE",
    # Settings
    "ACTION_SET_SETTING",
    # Sensor Events
    "ACTION_MOTION",
    "ACTION_SET_CONTACT_STATE",
    "ACTION_CURRENT_TEMPERATURE",
    "ACTION_AIR_QUALITY",
    "ACTION_POWER_USAGE",
    # Notifications
    "ACTION_PUSH_NOTIFICATION",
    # Doorbell
    "ACTION_DOORBELL_PRESS",
    # Legacy
    "ACTION_SET_PERCENTAGE",
]
