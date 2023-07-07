class SinricProConstants(object):

    # actions
    DOORBELLPRESS = 'DoorbellPress'
    CURRENT_TEMPERATURE = 'currentTemperature'
    SET_POWER_STATE = 'setPowerState'
    SET_POWER_LEVEL = 'setPowerLevel'
    ADJUST_POWER_LEVEL = 'adjustPowerLevel'
    SET_BRIGHTNESS = 'setBrightness'
    ADJUST_BRIGHTNESS = 'adjustBrightness'
    SET_COLOR = 'setColor'
    SET_COLOR_TEMPERATURE = 'setColorTemperature'
    INCREASE_COLOR_TEMPERATURE = 'increaseColorTemperature'
    DECREASE_COLOR_TEMPERATURE = 'decreaseColorTemperature'
    SET_THERMOSTAT_MODE = 'setThermostatMode'
    SET_RANGE_VALUE = 'setRangeValue'
    ADJUST_RANGE_VALUE = 'adjustRangeValue'
    TARGET_TEMPERATURE = 'targetTemperature'
    ADJUST_TARGET_TEMPERATURE = 'adjustTargetTemperature'
    SET_VOLUME = 'setVolume'
    ADJUST_VOLUME = 'adjustVolume'
    MEDIA_CONTROL = 'mediaControl'
    SELECT_INPUT = 'selectInput'
    CHANGE_CHANNEL = 'changeChannel'
    SKIP_CHANNELS = 'skipChannels'
    SET_MUTE = 'setMute'
    SET_BANDS = 'setBands'
    ADJUST_BANDS = 'adjustBands'
    RESET_BANDS = 'resetBands'
    SET_MODE = 'setMode'
    SET_LOCK_STATE = 'setLockState'
    GET_WEBRTC_ANSWER = 'getWebRTCAnswer'
    GET_CAMERA_STREAM_URL = 'getCameraStreamUrl'
    PUSH_NOTIFICATION = 'pushNotification'
    MOTION = 'motion'
    SET_CONTACT_STATE = 'setContactState'

    # payload attributes
    POWER_LEVEL = 'powerLevel'
    POWER_LEVEL_DELTA = 'powerLevelDelta'
    BRIGHTNESS = 'brightness'
    BRIGHTNESS_DELTA = 'brightnessDelta'
    COLOR = 'color'
    COLOR_TEMPERATURE = 'colorTemperature'
    POWER_STATE = 'powerState'
    STATE = 'state'
    HUMIDITY = 'humidity'
    TEMPERATURE = 'temperature'

    # message attributes
    DEVICEID = 'deviceId'
    INSTANCE_ID = 'instanceId'
    VALUE = 'value'
    RANGE_VALUE = 'rangeValue'
    LEVEL_DELTA = 'levelDelta'
    LEVELDIRECTION = 'levelDirection'
    LEVEL = 'level'
    NAME = 'name'
    BANDS = 'bands' 
    THERMOSTATMODE = 'thermostatMode'
    MODE = 'mode'
    

    # values
    LOCK_STATE_LOCKED = 'LOCKED'
    LOCK_STATE_UNLOCKED = 'UNLOCKED'

    POWER_STATE_ON = 'On'
    POWER_STATE_OFF = 'Off'

    CLOSE = "Close"
    OPEN = "Open"

    VOLUME = 'volume'

    INPUT = 'input'
    CONTROL = 'control'

    RED = 'r'
    GREEN = 'g'
    BLUE = 'b'

    MUTE = 'mute'

    def __setattr__(self, *_):
        pass
