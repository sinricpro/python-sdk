# Garage Door Example

Control your garage door with voice commands.

## Safety First ⚠️

- Add obstruction detection (IR sensors)
- Implement safety reversing
- Add manual override
- Test thoroughly
- Consider UL 325 requirements

## Hardware Setup

**Basic Setup:**
- Relay module (5V or 12V)
- Existing garage door opener
- Limit switches (optional, for position detection)

**Connection:**
```
Relay → Garage Door Opener Wall Button Terminals
(Simulates button press)
```

## Installation

```bash
pip install websockets
pip install RPi.GPIO
```

## Implementation

```python
import RPi.GPIO as GPIO
import asyncio

RELAY_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)

async def trigger_door():
    """Pulse relay to trigger door opener."""
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    await asyncio.sleep(0.5)  # 500ms pulse
    GPIO.output(RELAY_PIN, GPIO.LOW)

async def on_door_state(state: str) -> bool:
    await trigger_door()
    return True
```

## Add Position Detection

Use limit switches or reed switches to detect:
- Fully open position
- Fully closed position

```python
OPEN_SWITCH_PIN = 22
CLOSE_SWITCH_PIN = 23

GPIO.setup(OPEN_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(CLOSE_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def is_door_open():
    return GPIO.input(OPEN_SWITCH_PIN) == GPIO.LOW

def is_door_closed():
    return GPIO.input(CLOSE_SWITCH_PIN) == GPIO.LOW
```

## Advanced Features

- Add camera integration
- Motion sensor for auto-close
- Notifications when door left open
- Schedule-based auto-close
