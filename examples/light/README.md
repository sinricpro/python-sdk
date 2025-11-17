# Light Example

This example demonstrates how to create a smart RGB light device using the SinricPro Python SDK.

## Features

- Power state control (On/Off)
- Brightness control (0-100%)
- RGB color control
- Color temperature control (Warm/Cool white)
- Handle commands from Alexa/Google Home
- Send events to SinricPro

## Setup

1. Install the SinricPro SDK:

```bash
pip install sinricpro
```

2. Get your credentials from the [SinricPro Portal](https://portal.sinric.pro):
   - Create a Light device and copy the Device ID
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
python light_example.py
```

## Voice Commands

Once connected, you can control your light using:

**Power:**
- "Alexa, turn on [device name]"
- "Alexa, turn off [device name]"

**Brightness:**
- "Alexa, set [device name] to 50%"
- "Alexa, dim [device name]"
- "Alexa, brighten [device name]"

**Color:**
- "Alexa, set [device name] to red"
- "Alexa, set [device name] to blue"
- "Alexa, change [device name] to green"

**Color Temperature:**
- "Alexa, set [device name] to warm white"
- "Alexa, set [device name] to cool white"
- "Alexa, set [device name] to daylight"

## Implementation Notes

Implement the callbacks to control your physical light:

```python
async def on_power_state(state: bool) -> bool:
    # Turn your LED strip/bulb on or off
    return True

async def on_brightness(brightness: int) -> bool:
    # Set brightness (0-100)
    # e.g., PWM duty cycle = brightness
    return True

async def on_color(r: int, g: int, b: int) -> bool:
    # Set RGB color (each 0-255)
    # e.g., control RGB LED strip
    return True

async def on_color_temperature(temperature: int) -> bool:
    # Set color temperature (2000-7000K)
    # e.g., mix warm and cool white LEDs
    return True
```

To send events when physical controls are used:

```python
await my_light.send_power_state_event(True)
await my_light.send_brightness_event(75)
await my_light.send_color_event(255, 0, 0)  # Red
await my_light.send_color_temperature_event(4000)  # 4000K
```

## Hardware Examples

This SDK works with various RGB light hardware:

- **WS2812B LED Strips** - Use with libraries like `rpi_ws281x` or `adafruit_circuitpython_neopixel`
- **RGB LED Strips** - Control via PWM on GPIO pins
- **Smart Bulbs** - Send commands via WiFi/Bluetooth
- **ESP32/ESP8266** - Use as bridge to control lights via serial/MQTT
