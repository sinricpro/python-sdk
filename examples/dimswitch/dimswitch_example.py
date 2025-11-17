"""SinricPro DimSwitch Example - Dimmable switch/light control."""
import asyncio
import os
from typing import Any

from sinricpro import SinricPro, SinricProDimSwitch, SinricProConfig


# Device ID from SinricPro portal
DEVICE_ID = "YOUR_DEVICE_ID_HERE"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR_APP_KEY_HERE")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR_APP_SECRET_HERE")

power_state = False  # Current power state
power_level = 0  # Current power level (0-100)

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

    # TODO: Control your physical device
    # Example with GPIO:
    # GPIO.output(RELAY_PIN, GPIO.HIGH if state else GPIO.LOW)

    print(f"[Hardware] Device turned {'on' if state else 'off'}")
    return True


async def on_power_level(level: int) -> bool:
    """
    Handle power level change requests.

    Args:
        level: Power level (0-100)

    Returns:
        True if successful, False otherwise
    """
    global power_level
    print(f"\n[Callback] Power Level: {level}%")
    power_level = level

    # TODO: Control your dimmer
    # Example with PWM:
    # pwm.ChangeDutyCycle(level)  # 0-100% duty cycle

    print(f"[Hardware] Power level set to {level}%")
    return True


async def on_adjust_power_level(level_delta: int) -> tuple[bool, int]:
    """
    Handle relative power level adjustment requests.

    Args:
        level_delta: Change in power level (-100 to +100)

    Returns:
        True if successful, False otherwise
    """
    global power_level
    new_level = max(0, min(100, power_level + level_delta))
    print(f"\n[Callback] Adjust power level by {level_delta:+d}% → {new_level}%")
    power_level = new_level

    # TODO: Adjust your dimmer
    # pwm.ChangeDutyCycle(new_level)

    print(f"[Hardware] Power level adjusted to {new_level}%")
    return True, new_level


async def on_setting(setting: str, value: Any) -> bool:
    """
    Handle device setting changes.

    Args:
        setting: Setting name
        value: Setting value

    Returns:
        True if successful, False otherwise
    """
    print(f"\n[Setting] {setting} = {value}")
    return True

async def simulate_physical_control(dimswitch: SinricProDimSwitch) -> None:
    """Simulate physical dimmer control and send events."""
    await asyncio.sleep(10)  # Wait 10 seconds

    print("\n[Simulating physical dimmer adjustment to 75%]")
    global power_level
    power_level = 75

    # Send power level update event to SinricPro
    success = await dimswitch.send_power_level_event(power_level)
    if success:
        print(f"[Event] Power level event sent: {power_level}%")
    else:
        print("[Event] Failed to send power level event (rate limited or disconnected)")


async def main() -> None:
    # Create SinricPro instance and dimswitch device
    sinric_pro = SinricPro.get_instance()
    dimswitch = SinricProDimSwitch(DEVICE_ID)

    # Register callbacks
    dimswitch.on_power_state(on_power_state)
    dimswitch.on_power_level(on_power_level)
    dimswitch.on_adjust_power_level(on_adjust_power_level)
    dimswitch.on_setting(on_setting)

    # Add device to SinricPro
    sinric_pro.add(dimswitch)

    # Configure connection
    config = SinricProConfig(app_key=APP_KEY, app_secret=APP_SECRET)

    try:
        print("=" * 60)
        print("SinricPro DimSwitch Example")
        print("=" * 60)
        print("\nConnecting to SinricPro...")
        await sinric_pro.begin(config)
        print("✓ Connected! DimSwitch is ready.")

        print("\n" + "=" * 60)
        print("Voice Commands:")
        print("=" * 60)
        print("  • 'Alexa, turn on [device name]'")
        print("  • 'Alexa, turn off [device name]'")
        print("  • 'Alexa, set [device name] to 50 percent'")
        print("  • 'Alexa, dim [device name]'")
        print("  • 'Alexa, brighten [device name]'")

        print("\n" + "=" * 60)
        print("Features:")
        print("=" * 60)
        print("  • Power State Control: On/Off")
        print("  • Power Level Control: 0-100%")
        print("  • Relative Adjustments: Dim/Brighten")
        print("  • Setting Controller: Custom device settings")
        print("  • Push Notifications: Alert user of events")
        print("  • Event Reporting: Report physical dimmer changes")

        print("\n" + "=" * 60)
        print("Press Ctrl+C to exit")
        print("=" * 60)

        # Start physical control simulation
        asyncio.create_task(simulate_physical_control(dimswitch))

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
