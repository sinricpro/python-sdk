from sinric import SinricPro, SinricProConstants
import asyncio

APP_KEY = ''
APP_SECRET = ''
TV_ID = ''


def power_state(device_id, state):
    print('state : ', state)
    return True, state


def set_volume(device_id, volume):
    print('volume : ', volume)
    return True, volume


def adjust_volume(device_id, volume):
    print('volume : ', volume)
    return True, volume


def media_control(device_id, control):
    print('control : ', control)
    return True, control


def select_input(device_id, input):
    print('input : ', input)
    return True, input


def change_channel(device_id, channel_name):
    print('channel_name : ', channel_name)
    return True, channel_name


def skip_channels(device_id, channel_count):
    print('channel_count : ', channel_count)
    return True, channel_count


callbacks = {
    SinricProConstants.SET_POWER_STATE: power_state,
    SinricProConstants.SET_VOLUME: set_volume,
    SinricProConstants.ADJUST_VOLUME: adjust_volume,
    SinricProConstants.MEDIA_CONTROL: media_control,
    SinricProConstants.SELECT_INPUT: select_input,
    SinricProConstants.CHANGE_CHANNEL: change_channel,
    SinricProConstants.SKIP_CHANNELS: skip_channels
}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [TV_ID], callbacks, enable_log=False,
                       restore_states=False, secret_key=APP_SECRET)
    loop.run_until_complete(client.connect())

# To update the TV state on server:
# client.event_handler.raise_event(TV_ID, SinricProConstants.SET_VOLUME, data={'volume': 0})
# client.event_handler.raise_event(TV_ID, SinricProConstants.MEDIA_CONTROL, data={'control': 'FastForward'})
# client.event_handler.raise_event(TV_ID, SinricProConstants.CHANGE_CHANNEL, data={'name': 'HBO'})
# client.event_handler.raise_event(TV_ID, SinricProConstants.SELECT_INPUT, data={"input":"HDMI"})
