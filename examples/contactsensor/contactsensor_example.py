"""SinricPro ContactSensor Example - Door/window open/close detection."""
import asyncio
import os
from typing import Any

from sinricpro import SinricPro, SinricProContactSensor, SinricProConfig

# Device ID from SinricPro portal
DEVICE_ID = "YOUR_DEVICE_ID_HERE"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR_APP_KEY_HERE")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR_APP_SECRET_HERE")

# Sensor settings
sensitivity = "normal"  # Sensitivity level

async def on_setting(setting: str, value: Any) -> bool:
    """
    Handle device setting changes.

    Args:
        setting: Setting name (e.g., "sensitivity")
        value: Setting value

    Returns:
        True if successful, False otherwise
    """
    print(f"\n[Setting] {setting} = {value}")
    return True

async def monitor_contact_sensor(sensor: SinricProContactSensor) -> None:
    """Monitor physical contact sensor and send events when state changes."""
    print("\n[Starting contact sensor monitor]")

    # Track previous state to detect changes
    previous_state = None

    # Simulate state changes for demo purposes
    # In a real application, you would use GPIO interrupts
    states = [
        (False, 3),   # Closed for 3 seconds
        (True, 5),    # Open for 5 seconds (door opened)
        (False, 10),  # Closed for 10 seconds (door closed)
        (True, 3),    # Open for 3 seconds
        (False, None) # Closed indefinitely
    ]

    for is_open, duration in states:
        # TODO: Replace with actual GPIO monitoring
        # Example with GPIO:
        # GPIO.add_event_detect(SENSOR_PIN, GPIO.BOTH,
        #                       callback=on_state_change, bouncetime=50)

        # Check if state changed
        if previous_state != is_open:
            state_str = "OPEN" if is_open else "CLOSED"
            print("\n" + "=" * 60)
            print(f"[Sensor State Change Detected: {state_str}]")
            print("=" * 60)

            # Send contact state event to SinricPro
            success = await sensor.send_contact_event(is_open)
            if success:
                print(f"[Event] Contact state event sent: {state_str}")
            else:
                print("[Event] Failed to send contact event (rate limited or disconnected)")

            previous_state = is_open

        if duration is None:
            # Remain in this state indefinitely
            while True:
                await asyncio.sleep(1)
        else:
            await asyncio.sleep(duration)


async def main() -> None:
    # Create SinricPro instance and contact sensor device
    sinric_pro = SinricPro.get_instance()
    sensor = SinricProContactSensor(DEVICE_ID)

    # Register callbacks
    sensor.on_setting(on_setting)

    # Add device to SinricPro
    sinric_pro.add(sensor)

    # Configure connection
    config = SinricProConfig(app_key=APP_KEY, app_secret=APP_SECRET)

    try:
        print("=" * 60)
        print("SinricPro ContactSensor Example")
        print("=" * 60)
        print("\nConnecting to SinricPro...")
        await sinric_pro.begin(config)
        print("✓ Connected! Contact sensor is ready.")

        print("\n" + "=" * 60)
        print("Features:")
        print("=" * 60)
        print("  • Contact State Detection: Detect open/closed state")
        print("  • Event Reporting: Send state changes to SinricPro")
        print("  • Push Notifications: Alert when door/window opens/closes")
        print("  • Setting Controller: Sensitivity, notification preferences")
        print("  • Rate Limiting: Prevent event spam")

        print("\n" + "=" * 60)
        print("Hardware Setup:")
        print("=" * 60)
        print("  • Magnetic reed switch (common for doors/windows)")
        print("  • Connect to GPIO pin with pull-up resistor")
        print("  • Pin LOW = closed, Pin HIGH = open")
        print("  • Use interrupt-driven GPIO for instant detection")
        print("  • Optional: Add debounce capacitor for stability")

        print("\n" + "=" * 60)
        print("Use Cases:")
        print("=" * 60)
        print("  • Door/window open detection")
        print("  • Home security monitoring")
        print("  • Garage door state tracking")
        print("  • Cabinet/safe monitoring")
        print("  • Mailbox notification")

        print("\n" + "=" * 60)
        print("Press Ctrl+C to exit")
        print("=" * 60)

        # Start contact sensor monitoring
        asyncio.create_task(monitor_contact_sensor(sensor))

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
