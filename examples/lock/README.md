# Smart Lock Example

Control electronic locks with voice commands.

## ⚠️ Security Warning

**IMPORTANT:** Smart locks control physical security. Consider:
- Add PIN verification in Alexa app
- Use backup mechanical key
- Test thoroughly before deployment
- Add failsafe mechanisms
- Log all lock/unlock events

## Hardware Options

**Solenoid Lock:**
- 12V DC solenoid lock
- MOSFET or relay for switching
- Flyback diode for protection

**Servo Motor:**
- MG996R servo (high torque)
- Attach to existing deadbolt

**Electronic Strike:**
- 12V electric strike plate
- Works with existing door latch

## Installation

```bash
pip install websockets
pip install RPi.GPIO
```

## Solenoid Lock Example

```python
import RPi.GPIO as GPIO

LOCK_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LOCK_PIN, GPIO.OUT)

async def on_lock_state(locked: bool) -> bool:
    if locked:
        GPIO.output(LOCK_PIN, GPIO.HIGH)  # Energize solenoid
    else:
        GPIO.output(LOCK_PIN, GPIO.LOW)   # Release solenoid
    return True
```

## Features to Add

- Door sensor integration (check if door is closed before locking)
- Auto-lock timer
- Unlock notifications
- Access logs
- Battery backup
