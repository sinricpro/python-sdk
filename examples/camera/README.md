# SinricPro Camera Example

A comprehensive example demonstrating how to integrate a smart camera with SinricPro, supporting snapshot capture, motion detection, and power control.

## Features

- **Power Control**: Turn camera on/off via voice or app
- **Snapshot Capture**: Capture and upload images on request
- **Motion Detection**: Send alerts when motion is detected
- **Push Notifications**: Alert users of camera events
- **Settings Control**: Configure resolution, night mode, sensitivity

## Hardware Options

### Raspberry Pi
```python
# Install: pip install picamera2
from picamera2 import Picamera2
camera = Picamera2()
camera.start()
image_data = camera.capture_file("snapshot.jpg")
```

### ESP32-CAM
- Built-in OV2640 camera module
- Motion detection via frame comparison
- Upload images via HTTP/HTTPS

### OpenCV
```python
# Install: pip install opencv-python
import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
_, image_data = cv2.imencode('.jpg', frame)
```

## Installation

1. Install dependencies:
```bash
pip install sinricpro opencv-python  # or picamera2 for Raspberry Pi
```

2. Configure your device:
   - Create a Camera device in [SinricPro Portal](https://portal.sinric.pro)
   - Copy your Device ID, App Key, and App Secret
   - Update the constants in `camera_example.py`

3. Run the example:
```bash
python camera_example.py
```

## Usage

### Power Control
```python
async def on_power_state(state: bool) -> bool:
    if state:
        # Turn on camera, start streaming
        camera.start()
    else:
        # Turn off camera, stop streaming
        camera.stop()
    return True

camera.on_power_state(on_power_state)
```

### Snapshot Capture
```python
async def on_snapshot(device_id: str) -> bool:
    # Capture image from camera
    image_data = capture_image()

    # Upload to SinricPro
    await camera.send_snapshot(image_data)
    return True

camera.on_snapshot(on_snapshot)
```

### Motion Detection
```python
# Send motion event with optional video data
async def detect_motion():
    if motion_detected():
        # Simple event
        await camera.send_motion_event()

        # Or with video data
        video_data = capture_motion_video()
        await camera.send_motion_event(motion_data=video_data)
```

### Settings Control
```python
async def on_setting(setting: str, value: Any) -> bool:
    if setting == "resolution":
        camera.set_resolution(value)  # "720p", "1080p", "4K"
    elif setting == "night_mode":
        camera.set_night_mode(value)  # True/False
    elif setting == "motion_sensitivity":
        camera.set_sensitivity(value)  # 0-100
    return True

camera.on_setting(on_setting)
```

## Complete Example: Raspberry Pi Camera

```python
import asyncio
from picamera2 import Picamera2
from sinricpro import SinricPro, SinricProCamera, SinricProConfig

# Initialize camera
pi_camera = Picamera2()
config = pi_camera.create_still_configuration()
pi_camera.configure(config)

async def on_snapshot(device_id: str) -> bool:
    try:
        # Capture snapshot
        pi_camera.start()
        pi_camera.capture_file("snapshot.jpg")
        pi_camera.stop()

        # Read image data
        with open("snapshot.jpg", "rb") as f:
            image_data = f.read()

        # Upload to SinricPro
        camera = SinricPro.get_instance().get_device(device_id)
        await camera.send_snapshot(image_data)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# Setup camera device
camera = SinricProCamera("YOUR_DEVICE_ID")
camera.on_snapshot(on_snapshot)
```

## Complete Example: OpenCV Motion Detection

```python
import asyncio
import cv2
import numpy as np
from sinricpro import SinricPro, SinricProCamera

async def motion_detection_loop(camera: SinricProCamera):
    cap = cv2.VideoCapture(0)
    prev_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # Convert to grayscale and blur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if prev_frame is None:
            prev_frame = gray
            continue

        # Compute difference
        frame_delta = cv2.absdiff(prev_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        # Check for motion
        if np.sum(thresh) > 10000:  # Threshold for motion
            print("Motion detected!")

            # Capture snapshot
            _, image_data = cv2.imencode('.jpg', frame)

            # Send motion event
            await camera.send_motion_event()

            # Wait before next detection
            await asyncio.sleep(30)

        prev_frame = gray
        await asyncio.sleep(0.1)

    cap.release()
```

## Voice Commands

Once configured, you can control your camera with:

- **Alexa**: "Alexa, turn on the camera"
- **Alexa**: "Alexa, turn off the camera"
- **Google Home**: "Hey Google, turn on the camera"
- **App**: Request snapshots, view motion events

## Advanced Features

### Night Mode
```python
async def on_setting(setting: str, value: Any) -> bool:
    if setting == "night_mode":
        if value:
            # Enable IR LEDs
            enable_ir_leds()
        else:
            # Disable IR LEDs
            disable_ir_leds()
    return True
```

### Recording Modes
```python
recording_mode = "motion"  # or "continuous", "scheduled"

async def on_setting(setting: str, value: Any) -> bool:
    if setting == "recording_mode":
        global recording_mode
        recording_mode = value
        configure_recording(value)
    return True
```

### Privacy Mode
```python
privacy_mode = False

async def on_power_state(state: bool) -> bool:
    global privacy_mode
    if not state:
        # Camera off - enable privacy mode
        privacy_mode = True
        disable_camera()
        cover_lens()  # Physical privacy shutter
    else:
        privacy_mode = False
        enable_camera()
        uncover_lens()
    return True
```

## Troubleshooting

### Camera Not Capturing
- Verify camera is connected and accessible
- Check camera permissions
- Test camera independently first

### Motion Events Not Sending
- Check rate limiting (max 1 event per 60 seconds by default)
- Verify camera is powered on
- Check network connectivity

### Snapshots Not Uploading
- Verify image format (JPEG recommended)
- Check image size (< 5MB recommended)
- Ensure proper authentication

## Related Examples

- [Motion Sensor](../motionsensor/) - PIR motion detection
- [Doorbell](../doorbell/) - Doorbell with button press
- [Switch](../switch/) - Basic power control

## Additional Resources

- [SinricPro Documentation](https://sinricpro.github.io/python-sdk/)
- [Camera API Reference](https://sinricpro.github.io/python-sdk/capabilities/#cameracontroller)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Raspberry Pi Camera](https://www.raspberrypi.com/documentation/computers/camera_software.html)
