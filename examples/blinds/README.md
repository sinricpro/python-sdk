# Blinds Example

Control motorized blinds/shades with voice commands using the OpenCloseController capability.

## Features

- **Power State Control**: Turn motor power on/off for energy savings
- **Open/Close Control**: Set position from 0% (closed) to 100% (open)
- **Setting Controller**: Configure custom device settings (motor speed, direction, etc.)
- **Push Notifications**: Send alerts to users about blind status
- **Event Reporting**: Report physical button presses to keep cloud in sync

## Hardware Options

**Stepper Motor (Recommended):**
- 28BYJ-48 stepper motor + ULN2003 driver
- NEMA 17 stepper + A4988/DRV8825 driver
- Precise position control
- No encoder needed

**Servo Motor:**
- Standard servo (0-180°)
- Continuous rotation servo with encoder
- Simple control

**DC Motor:**
- L298N or TB6612 motor driver
- Requires limit switches or encoder
- Position feedback essential

## Installation

```bash
# Core dependencies
pip install websockets

# For motor control (Raspberry Pi)
pip install RPi.GPIO
pip install RpiMotorLib  # For stepper motors

# For other platforms
pip install pyserial  # For Arduino control
```

## Basic Usage

```python
from sinricpro import SinricPro, SinricProBlinds, SinricProConfig

# Create blinds device
blinds = SinricProBlinds("YOUR_DEVICE_ID")

# Register callback for power state changes
async def on_power_state(state: bool) -> bool:
    """Handle power on/off: True=on, False=off"""
    print(f"Motor power: {'ON' if state else 'OFF'}")
    # TODO: Enable/disable motor driver here
    return True

# Register callback for position changes
async def on_open_close(position: int) -> bool:
    """Handle position change: 0=closed, 100=open"""
    print(f"Moving to {position}%")
    # TODO: Control your motor here
    return True

blinds.on_power_state(on_power_state)
blinds.on_open_close(on_open_close)

# Add to SinricPro
sinric_pro = SinricPro.get_instance()
sinric_pro.add(blinds)
```

## Power State Control

Control motor power for energy efficiency:

```python
import RPi.GPIO as GPIO

ENABLE_PIN = 17  # Motor driver enable pin

async def on_power_state(state: bool) -> bool:
    """Enable or disable motor driver power."""
    if state:
        GPIO.output(ENABLE_PIN, GPIO.HIGH)  # Enable motor
        print("Motor driver enabled")
    else:
        GPIO.output(ENABLE_PIN, GPIO.LOW)   # Disable motor
        print("Motor driver disabled")
    return True

blinds.on_power_state(on_power_state)
```

## Stepper Motor Implementation

```python
from RpiMotorLib import RpiMotorLib

motor = RpiMotorLib.BYJMotor("BlindMotor", "28BYJ")
GPIO_pins = [18, 23, 24, 25]  # GPIO pins
STEPS_PER_REV = 2048  # 28BYJ-48 full cycle

async def on_open_close(position: int) -> bool:
    """Move blinds to target position using stepper motor."""
    # Calculate steps needed (assume 10 revolutions = full range)
    total_steps = STEPS_PER_REV * 10
    target_steps = int((position / 100.0) * total_steps)

    # Move to position
    motor.motor_run(GPIO_pins, 0.001, target_steps, False, False, "half", 0.05)
    print(f"Moved to {position}% ({target_steps} steps)")
    return True

blinds.on_open_close(on_open_close)
```

## Settings Controller

```python
async def on_setting(setting: str, value: Any) -> bool:
    """Handle custom device settings."""
    if setting == "speed":
        # Adjust motor speed
        motor_speed = value  # e.g., "slow", "medium", "fast"
        print(f"Motor speed set to: {motor_speed}")
        return True
    elif setting == "direction":
        # Set motor direction preference
        print(f"Direction set to: {value}")
        return True
    return False

blinds.on_setting(on_setting)
```

## Sending Events

Report physical button presses to keep cloud synchronized:

```python
# When user presses physical button to open blinds
current_position = 75  # Move to 75%
success = await blinds.send_open_close_event(current_position)

if success:
    print("Position event sent to cloud")
```

## Push Notifications

Send alerts to user's phone:

```python
# Notify user when blinds are fully open
if current_position == 100:
    await blinds.send_push_notification("Blinds are fully open")
```

## Voice Commands

- **"Alexa, turn on [device name]"** - Enable motor power
- **"Alexa, turn off [device name]"** - Disable motor power
- **"Alexa, set [device name] to 75 percent"** - Set to 75% open
- **"Alexa, open [device name]"** - Fully open (100%)
- **"Alexa, close [device name]"** - Fully close (0%)
- **"Alexa, set [device name] to 50"** - Half open (50%)

## Complete Wiring Example (28BYJ-48)

```
28BYJ-48 Stepper + ULN2003 Driver:
- IN1 → GPIO 18
- IN2 → GPIO 23
- IN3 → GPIO 24
- IN4 → GPIO 25
- EN (Enable) → GPIO 17  # Optional: for power control
- VCC → 5V
- GND → GND

Note: Enable pin allows you to turn motor power on/off
      for energy savings when not in use.
```

## Troubleshooting

**Motor doesn't move:**
- Check GPIO pin connections
- Verify 5V power supply (steppers need external power)
- Ensure motor power is ON (check power state)
- Test motor with simple script first

**Motor won't turn on:**
- Check enable pin connection (GPIO 17)
- Verify power state callback is registered
- Try sending power ON command via voice or app

**Position drift:**
- Use stepper motors for best accuracy
- Add home/calibration routine on startup
- Consider adding limit switches

**Slow response:**
- Reduce motor steps per command
- Use faster step delay (but not too fast)
- Check network latency

**Power saving tips:**
- Use power state control to disable motor when not in use
- Implement auto-off after position reached
- Motor drivers can get hot - power control extends lifespan
