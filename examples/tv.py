from sinric import SinricPro 
import asyncio
 
APP_KEY = ''
APP_SECRET = ''
TV_ID = ''

def power_state(device_id, state):
    print('state : ', state)
    # Do Something
    return True, state


def set_volume(device_id, volume):
    print('volume : ', volume)

    # Do Somethign
    return True, volume


def adjust_volume(device_id, volume):
    print('volume : ', volume)
    # Do something with volume
    return True, volume


def media_control(device_id, control):
    print('control : ', control)
    # Do something with control
    return True, control


def select_input(device_id, input):
    print('input : ', input)
    # Do something with input
    return True, input


def change_channel(device_id, channel_name):
    print('channel_name : ', channel_name)
    # Change Channel
    return True, channel_name


def skip_channels(device_id, channel_count):
    print('channel_count : ', channel_count)
    # Skip them
    return True, channel_count


callbacks = {
    'powerState': power_state,
    'setVolume': set_volume,
    'adjustVolume': adjust_volume,
    'mediaControl': media_control,
    'selectInput': select_input,
    'changeChannel': change_channel,
    'skipChannels': skip_channels
}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [TV_ID], callbacks, enable_log=False, restore_states=False, secretKey=APP_SECRET)
    loop.run_until_complete(client.connect())

# To update the TV state on server:
# client.event_handler.raiseEvent(tvId, 'setVolume',data={'volume': 0})
# client.event_handler.raiseEvent(tvId, 'mediaControl',data={'control': 'FastForward'})
# client.event_handler.raiseEvent(tvId, 'changeChannel',data={'name': 'HBO'})
# client.event_handler.raiseEvent(tvId, 'selectInput',data={"input":"HDMI"})
