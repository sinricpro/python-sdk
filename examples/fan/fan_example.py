"""SinricPro Fan Example - Ceiling/desk fan control with speed settings."""
import asyncio
import os
from typing import Any

from sinricpro import SinricPro, SinricProFan, SinricProConfig


# Device ID from SinricPro portal
DEVICE_ID = "YOUR_DEVICE_ID_HERE"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR_APP_KEY_HERE")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR_APP_SECRET_HERE")

power_state = False  # Current power state
fan_speed = 0  # Current fan speed (0-100 or 0-5 for discrete levels)

async def on_power_state(state: bool) -> bool:
    """
    Handle power state change requests.

    Args:
        state: True for ON, False for OFF

    Returns:
        True if successful, False otherwise
    """
    global power_state
    print(f"\n[Callback] Power: {'ON' if state else 'OFF'}")
    power_state = state

    # TODO: Control your physical fan
    # Example with GPIO relay:
    # GPIO.output(RELAY_PIN, GPIO.HIGH if state else GPIO.LOW)

    print(f"[Hardware] Fan turned {'on' if state else 'off'}")
    return True


async def on_range_value(speed: int, instance_id: str) -> bool:
    """
    Handle fan speed change requests.

    Args:
        speed: Fan speed level (0-100)
        instance_id: Instance ID for multi-instance range control (not used for fan)

    Returns:
        True if successful, False otherwise
    """
    global fan_speed
    print(f"\n[Callback] Fan Speed: {speed}")
    fan_speed = speed

    # TODO: Control your fan speed
    # Example 1: PWM control (continuous 0-100)
    # pwm.ChangeDutyCycle(speed)

    # Example 2: Discrete speed levels (convert 0-100 to 0-5)
    # discrete_speed = int(speed / 20)  # 0-5 levels
    # set_discrete_speed(discrete_speed)

    print(f"[Hardware] Fan speed set to {speed}")
    return True


async def on_adjust_range_value(speed_delta: int, instance_id: str) -> bool:
    """
    Handle relative fan speed adjustment requests.

    Args:
        speed_delta: Change in speed (-100 to +100)
        instance_id: Instance ID for multi-instance range control (not used for fan)

    Returns:
        True if successful, False otherwise
    """
    global fan_speed
    new_speed = max(0, min(4, fan_speed + speed_delta))
    print(f"\n[Callback] Adjust fan speed by {speed_delta:+d} → {new_speed}")
    fan_speed = new_speed

    # TODO: Adjust your fan speed
    # pwm.ChangeDutyCycle(new_speed)

    print(f"[Hardware] Fan speed adjusted to {new_speed}")
    return True


async def on_setting(setting: str, value: Any) -> bool:
    """
    Handle device setting changes.

    Args:
        setting: Setting name (e.g., "oscillate", "direction", "timer")
        value: Setting value

    Returns:
        True if successful, False otherwise
    """
    print(f"\n[Setting] {setting} = {value}")
    return True


async def simulate_physical_control(fan: SinricProFan) -> None:
    """Simulate physical fan speed control and send events."""
    await asyncio.sleep(10)  # Wait 10 seconds

    print("\n[Simulating physical speed dial adjustment to speed 4]")
    global fan_speed
    fan_speed = 4

    # Send speed update event to SinricPro
    success = await fan.send_range_value_event(fan_speed)
    if success:
        print(f"[Event] Fan speed event sent: {fan_speed}")
    else:
        print("[Event] Failed to send speed event (rate limited or disconnected)")


async def main() -> None:
    # Create SinricPro instance and fan device
    sinric_pro = SinricPro.get_instance()
    fan = SinricProFan(DEVICE_ID)

    # Register callbacks
    fan.on_power_state(on_power_state)
    fan.on_range_value(on_range_value)
    fan.on_adjust_range_value(on_adjust_range_value)
    fan.on_setting(on_setting)

    # Add device to SinricPro
    sinric_pro.add(fan)

    # Configure connection
    config = SinricProConfig(app_key=APP_KEY, app_secret=APP_SECRET)

    try:
        print("=" * 60)
        print("SinricPro Fan Example")
        print("=" * 60)
        print("\nConnecting to SinricPro...")
        await sinric_pro.begin(config)
        print("✓ Connected! Fan is ready.")

        print("\n" + "=" * 60)
        print("Voice Commands:")
        print("=" * 60)
        print("  • 'Alexa, turn on [device name]'")
        print("  • 'Alexa, turn off [device name]'")
        print("  • 'Alexa, set [device name] to 50 percent'")
        print("  • 'Alexa, increase [device name]'")
        print("  • 'Alexa, decrease [device name]'")

        print("\n" + "=" * 60)
        print("Features:")
        print("=" * 60)
        print("  • Power State Control: On/Off")
        print("  • Fan Speed Control: 0-100 (continuous or discrete)")
        print("  • Relative Speed Adjustments: Increase/Decrease")
        print("  • Setting Controller: Oscillation, Direction, Timer")
        print("  • Push Notifications: Alert user of events")
        print("  • Event Reporting: Report physical speed dial changes")

        print("\n" + "=" * 60)
        print("Press Ctrl+C to exit")
        print("=" * 60)

        # Start physical control simulation
        asyncio.create_task(simulate_physical_control(fan))

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
