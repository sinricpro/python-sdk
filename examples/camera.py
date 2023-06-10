from sinric import SinricPro, SinricProConstants
import requests
import asyncio
import base64

APP_KEY = ''
APP_SECRET = ''
CAMERA_ID = ''


def webrtc_offer(device_id, format, offer):
    sdp_offer = base64.b64decode(offer)
    print('device_id: {} format: {} offer: {}'.format(
        device_id, format, sdp_offer))

    mediamtx_url = "http://<mediamtx-hostname>:8889/<device>/whep"  # PORT 8889 for WebRTC
    headers = {"Content-Type": "application/sdp"}
    response = requests.post(mediamtx_url, headers=headers, data=sdp_offer)

    if response.status_code == 201:
        answer = base64.b64encode(response.content).decode("utf-8")
        return True, answer
    else:
        return False


def power_state(device_id, state):
    print('device_id: {} state: {}'.format(device_id, state))
    return True, state


callbacks = {
    SinricProConstants.WEBRTC_OFFER: webrtc_offer,
    SinricProConstants.SET_POWER_STATE: power_state
}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [CAMERA_ID], callbacks,
                       enable_log=False, restore_states=False, secret_key=APP_SECRET)
    loop.run_until_complete(client.connect())
