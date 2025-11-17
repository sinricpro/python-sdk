# Motion Sensor Example

This example demonstrates how to create a motion sensor device using the SinricPro Python SDK.

## Features

- Send motion detection events to SinricPro
- Real-time notifications in Alexa app
- Works with PIR sensors (HC-SR501, etc.)

## Hardware Setup

Connect a PIR motion sensor to your device:
- VCC → 5V
- GND → GND
- OUT → GPIO pin (e.g., GPIO 4 on Raspberry Pi)

## Software Setup

1. Install dependencies:
```bash
pip install websockets
# For Raspberry Pi GPIO:
pip install RPi.GPIO
```

2. Get credentials from [SinricPro Portal](https://portal.sinric.pro):
   - Create a Motion Sensor device and copy the Device ID
   - Copy your App Key and App Secret

3. Update the example with your credentials:
```python
DEVICE_ID = "your_device_id_here"
```

Or set environment variables:
```bash
export SINRICPRO_APP_KEY="your_app_key"
export SINRICPRO_APP_SECRET="your_app_secret"
```

## Run

```bash
python motion_sensor_example.py
```

## Real Hardware Integration

Replace the simulation with actual GPIO code:

```python
import RPi.GPIO as GPIO

# Setup
MOTION_PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTION_PIN, GPIO.IN)

async def monitor_motion(sensor: SinricProMotionSensor) -> None:
    """Monitor PIR sensor and send events."""
    last_state = False

    while True:
        current_state = GPIO.input(MOTION_PIN)

        if current_state != last_state:
            if current_state:
                print("Motion detected!")
                await sensor.send_motion_event(True)
            else:
                print("No motion")
                await sensor.send_motion_event(False)

            last_state = current_state

        await asyncio.sleep(0.1)
```

## Alexa Integration

Once connected, you'll receive notifications when motion is detected:
- "Motion was detected at Front Door"
- Check motion status: "Alexa, is there motion at Front Door?"

## Tips

- Adjust PIR sensor sensitivity with the potentiometer
- Most PIR sensors have a 2-3 second trigger delay
- Use rate limiting to avoid excessive events
