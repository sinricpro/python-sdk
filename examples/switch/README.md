# Switch Example

This example demonstrates how to create a simple switch device using the SinricPro Python SDK.

## Features

- Power state control (On/Off)
- Handle commands from Alexa/Google Home
- Send events to SinricPro

## Setup

1. Install the SinricPro SDK:

```bash
pip install sinricpro
```

2. Get your credentials from the [SinricPro Portal](https://portal.sinric.pro):
   - Create a Switch device and copy the Device ID
   - Copy your App Key and App Secret from the Credentials page

3. Update the example code with your credentials:

```python
DEVICE_ID = "your_device_id_here"
APP_KEY = "your_app_key_here"
APP_SECRET = "your_app_secret_here"
```

Alternatively, set environment variables:

```bash
export SINRICPRO_APP_KEY="your_app_key_here"
export SINRICPRO_APP_SECRET="your_app_secret_here"
```

## Run

```bash
python switch_example.py
```

## Voice Commands

Once connected, you can control your switch using:

- "Alexa, turn on [device name]"
- "Alexa, turn off [device name]"
- "Hey Google, turn on [device name]"
- "Hey Google, turn off [device name]"

## Implementation Notes

The `on_power_state` callback is called when the device receives a power state command. You should implement your device-specific logic here:

```python
async def on_power_state(state: bool) -> bool:
    if state:
        # Turn on your device
        # e.g., GPIO.output(PIN, GPIO.HIGH)
        pass
    else:
        # Turn off your device
        # e.g., GPIO.output(PIN, GPIO.LOW)
        pass
    return True
```

To send events (when physical button is pressed, for example):

```python
await my_switch.send_power_state_event(True)  # Device turned on
```
