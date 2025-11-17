"""SinricPro Blinds Example - Motorized blinds/shades control."""
import asyncio
import os
from typing import Any

from sinricpro import SinricPro, SinricProBlinds, SinricProConfig


# Device ID from SinricPro portal
DEVICE_ID = "YOUR_DEVICE_ID_HERE"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR_APP_KEY_HERE")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR_APP_SECRET_HERE")

power_state = False  # Motor power state
current_position = 0  # 0 = fully closed, 100 = fully open

async def on_open_close(position: int) -> bool:
    """
    Handle open/close position change requests.

    Args:
        position: Target position (0=closed, 100=open)

    Returns:
        True if successful, False otherwise
    """
    global current_position
    print(f"\n[Callback] Moving blinds to {position}% (0=closed, 100=open)")
    current_position = position

    # TODO: Control your motor to move blinds
    # Example for stepper motor:
    # steps_per_revolution = 200
    # total_steps = steps_per_revolution * 10  # 10 revolutions = full range
    # target_steps = int((position / 100.0) * total_steps)
    # motor.move_to(target_steps)

    print(f"[Hardware] Blinds moved to {position}%")
    return True

async def on_power_state(state: bool) -> bool:
    """
    Handle power state change requests.

    Args:
        state: True for ON, False for OFF

    Returns:
        True if successful, False otherwise
    """
    global power_state
    print(f"\n[Callback] Blinds motor power: {'ON' if state else 'OFF'}")
    power_state = state

    # TODO: Control motor power
    # if state:
    #     # Enable motor driver
    #     GPIO.output(ENABLE_PIN, GPIO.HIGH)
    # else:
    #     # Disable motor driver
    #     GPIO.output(ENABLE_PIN, GPIO.LOW)

    print(f"[Hardware] Motor power {'enabled' if state else 'disabled'}")
    return True

async def on_setting(setting: str, value: Any) -> bool:
    """
    Handle device setting changes.

    Args:
        setting: Setting name (e.g., "speed", "direction")
        value: Setting value

    Returns:
        True if successful, False otherwise
    """
    print(f"\n[Setting] {setting} = {value}")

    # Handle custom settings
    if setting == "speed":
        print(f"[Hardware] Motor speed set to {value}")
        return True
    elif setting == "direction":
        print(f"[Hardware] Motor direction set to {value}")
        return True

    print(f"[Warning] Unknown setting: {setting}")
    return False

async def simulate_physical_control(blinds: SinricProBlinds) -> None:
    """Simulate physical button control and send events."""
    await asyncio.sleep(10)  # Wait 10 seconds

    print("\n[Simulating physical button press - Opening to 75%]")
    global current_position
    current_position = 75

    # Send position update event to SinricPro
    success = await blinds.send_open_close_event(current_position)
    if success:
        print(f"[Event] Position event sent: {current_position}%")
    else:
        print("[Event] Failed to send position event (rate limited or disconnected)")

async def main() -> None:
    # Create SinricPro instance and blinds device
    sinric_pro = SinricPro.get_instance()
    blinds = SinricProBlinds(DEVICE_ID)

    # Register callbacks
    blinds.on_power_state(on_power_state)
    blinds.on_open_close(on_open_close)
    blinds.on_setting(on_setting)

    # Add device to SinricPro
    sinric_pro.add(blinds)

    # Configure connection
    config = SinricProConfig(app_key=APP_KEY, app_secret=APP_SECRET)

    try:
        print("=" * 60)
        print("SinricPro Blinds Example")
        print("=" * 60)
        print("\nConnecting to SinricPro...")
        await sinric_pro.begin(config)
        print("✓ Connected! Blinds are ready.")

        print("\n" + "=" * 60)
        print("Voice Commands:")
        print("=" * 60)
        print("  • 'Alexa, turn on [device name]'  - Enable motor power")
        print("  • 'Alexa, turn off [device name]' - Disable motor power")
        print("  • 'Alexa, set [device name] to 50 percent'")
        print("  • 'Alexa, open [device name]'")
        print("  • 'Alexa, close [device name]'")

        print("\n" + "=" * 60)
        print("Features:")
        print("=" * 60)
        print("  • Power State Control: Turn motor on/off")
        print("  • Open/Close Control: 0-100% (0=closed, 100=open)")
        print("  • Setting Controller: Custom device settings")
        print("  • Push Notifications: Alert user of events")
        print("  • Event Reporting: Report physical button presses")

        print("\n" + "=" * 60)
        print("Press Ctrl+C to exit")
        print("=" * 60)

        # Start physical control simulation
        #asyncio.create_task(simulate_physical_control(blinds))

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
