"""SinricPro Doorbell Example - Smart doorbell with button press detection."""
import asyncio
import os
from typing import Any

from sinricpro import SinricPro, SinricProDoorbell, SinricProConfig

# Device ID from SinricPro portal
DEVICE_ID = "YOUR_DEVICE_ID_HERE"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR_APP_KEY_HERE")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR_APP_SECRET_HERE")


async def on_setting(setting: str, value: Any) -> bool:
    """
    Handle device setting changes.

    Args:
        setting: Setting name (e.g., "volume", "chime_type")
        value: Setting value

    Returns:
        True if successful, False otherwise
    """
    global chime_volume, chime_type
    print(f"\n[Setting] {setting} = {value}") 
    return True

async def simulate_doorbell_button(doorbell: SinricProDoorbell) -> None:
    """Monitor physical doorbell button and send events when pressed."""
    print("\n[Starting doorbell button monitor]")

    # Simulate button presses for demo purposes
    # In a real application, you would use GPIO interrupts
    await asyncio.sleep(10)  # Wait 10 seconds before first simulation

    while True:
        # TODO: Replace with actual GPIO button monitoring
        # Example with GPIO:
        # GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING,
        #                       callback=on_button_press, bouncetime=300)

        print("\n" + "=" * 60)
        print("[Simulating doorbell button press]")
        print("=" * 60)

        
        # Send doorbell press event to SinricPro
        success = await doorbell.send_doorbell_event()
        if success:
            print("[Event] Doorbell press event sent to SinricPro")
        else:
            print("[Event] Failed to send doorbell event (rate limited or disconnected)")

        # Wait before next simulated press (in real app, this would be event-driven)
        await asyncio.sleep(30)


async def main() -> None:
    # Create SinricPro instance and doorbell device
    sinric_pro = SinricPro.get_instance()
    doorbell = SinricProDoorbell(DEVICE_ID)

    # Register callbacks
    doorbell.on_setting(on_setting)

    # Add device to SinricPro
    sinric_pro.add(doorbell)

    # Configure connection
    config = SinricProConfig(app_key=APP_KEY, app_secret=APP_SECRET)

    try:
        print("=" * 60)
        print("SinricPro Doorbell Example")
        print("=" * 60)
        print("\nConnecting to SinricPro...")
        await sinric_pro.begin(config)
        print("✓ Connected! Doorbell is ready.")

        print("\n" + "=" * 60)
        print("Features:")
        print("=" * 60)
        print("  • Doorbell Press Detection: GPIO button monitoring")
        print("  • Event Reporting: Send press events to SinricPro")
        print("  • Push Notifications: Alert users when doorbell is pressed")
        print("  • Setting Controller: Volume, chime type, LED brightness")
        print("  • Rate Limiting: Prevent event spam")

        print("\n" + "=" * 60)
        print("Hardware Setup:")
        print("=" * 60)
        print("  • Connect doorbell button to GPIO pin (with pull-up)")
        print("  • Connect speaker/buzzer for local chime")
        print("  • Optional: LED indicator for status")
        print("  • Use interrupt-driven GPIO for best performance")

        print("\n" + "=" * 60)
        print("Event Flow:")
        print("=" * 60)
        print("  1. User presses doorbell button")
        print("  2. Local chime plays (immediate feedback)")
        print("  3. Event sent to SinricPro cloud")
        print("  4. Push notification sent to all linked devices")
        print("  5. Users see notification on phone/tablet")

        print("\n" + "=" * 60)
        print("Press Ctrl+C to exit")
        print("=" * 60)

        # Start doorbell button monitoring
        asyncio.create_task(simulate_doorbell_button(doorbell))

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
