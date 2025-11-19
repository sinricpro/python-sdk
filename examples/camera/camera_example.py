"""SinricPro Camera Example - Smart camera with snapshot and motion detection."""
import asyncio
import os
from typing import Any
from pathlib import Path
import aiohttp
import base64
import sys

from sinricpro import SinricPro, SinricProCamera, SinricProConfig

# Device ID from SinricPro portal
DEVICE_ID = "YOUR_DEVICE_ID_HERE"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR_APP_KEY_HERE")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR_APP_SECRET_HERE")

# Camera state
camera_powered_on = False


async def on_power_state(state: bool) -> bool:
    """
    Handle camera power state changes.

    Args:
        state: True for On, False for Off

    Returns:
        True if successful, False otherwise
    """
    global camera_powered_on
    print(f"\n[Power] Camera turned {'ON' if state else 'OFF'}")

    camera_powered_on = state

    # TODO: Add your code here to control the physical camera
    # For example:
    # - Start/stop camera streaming
    # - Enable/disable motion detection
    # - Control camera LED indicators
    # - Manage power to camera module

    return True

async def on_snapshot(device_id: str) -> bool:
    """
    Handle snapshot request from SinricPro.

    Args:
        device_id: The device ID requesting the snapshot

    Returns:
        True if snapshot was captured and sent successfully
    """
    print(f"\n[Snapshot] Snapshot requested for device {device_id}")

    if not camera_powered_on:
        print("[Snapshot] Camera is powered off, cannot capture snapshot")
        return False

    try:
        # TODO: Replace with actual camera capture code
        # For example:
        # - Capture image from camera module (picamera, OpenCV, etc.)
        # - Process/compress image if needed
        # - Return the image data as bytes

        # Example with picamera (Raspberry Pi):
        # from picamera import PiCamera
        # camera = PiCamera()
        # camera.capture('snapshot.jpg')
        # with open('snapshot.jpg', 'rb') as f:
        #     image_data = f.read()

        # For demonstration, we'll create a dummy image
        # In production, replace this with actual camera capture
        print("[Snapshot] Capturing image from camera...")
        await asyncio.sleep(1)  # Simulate capture time

        # Create a simple test image (1x1 pixel JPEG)
        # This is just for demonstration - use real camera data in production!
        dummy_image = bytes([
            0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46,
            0x49, 0x46, 0x00, 0x01, 0x01, 0x00, 0x00, 0x01,
            0x00, 0x01, 0x00, 0x00, 0xFF, 0xD9
        ])

        # Get camera device and send snapshot
        sinric_pro = SinricPro.get_instance()
        camera_device = sinric_pro.get_device(device_id)

        if camera_device and isinstance(camera_device, SinricProCamera):
            print("[Snapshot] Uploading snapshot to SinricPro...")
            success = await camera_device.send_snapshot(dummy_image)
            if success:
                print("[Snapshot] ✓ Snapshot uploaded successfully")
                return True
            else:
                print("[Snapshot] ✗ Failed to upload snapshot")
                return False

        return False

    except Exception as e:
        print(f"[Snapshot] Error capturing snapshot: {e}")
        return False

async def on_setting(setting: str, value: Any) -> bool:
    """
    Handle camera setting changes.

    Args:
        setting: Setting name (e.g., "resolution", "night_mode", "sensitivity")
        value: Setting value

    Returns:
        True if successful, False otherwise
    """
    print(f"\n[Setting] {setting} = {value}")

    # TODO: Add your code here to handle camera settings
    # Common camera settings:
    # - resolution: "720p", "1080p", "4K"
    # - night_mode: true/false
    # - motion_sensitivity: 0-100
    # - recording_mode: "continuous", "motion", "scheduled"
    # - flip_image: "horizontal", "vertical", "both"

    return True

async def on_get_stream_url(device_id: str, protocol: str) -> tuple[bool, str]:
    # Google Home: RTSP protocol not supported. Requires a Chromecast TV or Google Nest Hub
    # Alexa: RTSP url must be interleaved TCP on port 443 (for both RTP and RTSP) over TLS 1.2 port 443

    print('Sending the streaming url for device_id: {} protocol: {}'.format(device_id, protocol))

    if protocol == "rtsp":
        return True, 'rtsp://rtspurl:443'   # RTSP.
    else:
        return True, 'https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8' # HLS

async def on_get_webrtc_answer(device_id: str, offer: str) -> tuple[bool, str]:
    sdp_offer = base64.b64decode(offer)
    print('device_id: {} offer: {}'.format(device_id, offer))

    # PORT 8889 for WebRTC. eg: for PiCam, use http://<mediamtx-hostname>:8889/cam/whep
    mediamtx_url = "http://<mediamtx-hostname>:8889/<device>/whep"
    headers = {"Content-Type": "application/sdp"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(mediamtx_url, headers=headers, data=sdp_offer) as response:
                if response.status == 201:
                    content = await response.read()
                    answer = base64.b64encode(content).decode("utf-8")
                    return True, answer
                else:
                    return False, ""
    except Exception as e:
        print(f"Error getting WebRTC answer: {e}")
        return False, "" 
    
async def main() -> None:
    # Create SinricPro instance and camera device
    sinric_pro = SinricPro.get_instance()
    camera = SinricProCamera(DEVICE_ID)

    # Register callbacks
    camera.on_power_state(on_power_state)
    camera.on_snapshot(on_snapshot)
    camera.on_setting(on_setting)
    camera.on_get_stream_url(on_get_stream_url)
    camera.on_get_webrtc_answer(on_get_webrtc_answer)

    # Add device to SinricPro
    sinric_pro.add(camera)

    # Configure connection
    config = SinricProConfig(app_key=APP_KEY, app_secret=APP_SECRET)

    try:
        print("=" * 60)
        print("SinricPro Camera Example")
        print("=" * 60)
        print("\nConnecting to SinricPro...")
        await sinric_pro.begin(config)
        print("✓ Connected! Camera is ready.")
 
        print("\n" + "=" * 60)
        print("Press Ctrl+C to exit")
        print("=" * 60)
 
        # Keep the application running
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\n\nShutting down...")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await sinric_pro.stop()
        print("Disconnected.")

if __name__ == "__main__":
    asyncio.run(main())
