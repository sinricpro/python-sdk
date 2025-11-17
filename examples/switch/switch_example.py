"""
SinricPro Switch Example

Demonstrates basic switch control with power state.
"""

import asyncio
import os

from sinricpro import SinricPro, SinricProSwitch, SinricProConfig

# Device ID from SinricPro portal
DEVICE_ID = "YOUR_DEVICE_ID_HERE"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR_APP_KEY_HERE")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR_APP_SECRET_HERE")


async def on_power_state(state: bool) -> bool:
    """
    Handle power state changes from SinricPro.

    Args:
        state: True for On, False for Off

    Returns:
        True if the state was successfully changed
    """
    print(f"Switch turned {'ON' if state else 'OFF'}")

    # TODO: Add your code here to control the physical device
    # For example:
    # - Set GPIO pin high/low
    # - Send command to smart plug
    # - Toggle relay

    return True  # Return True if successful


async def main() -> None:
    """Main function."""
    # Create SinricPro instance
    sinric_pro = SinricPro.get_instance()

    # Create switch device
    my_switch = SinricProSwitch(DEVICE_ID)

    # Register power state callback
    my_switch.on_power_state(on_power_state)

    # Add device to SinricPro
    sinric_pro.add(my_switch)

    # Configure and connect
    config = SinricProConfig(
        app_key=APP_KEY,
        app_secret=APP_SECRET
    )

    try:
        print("Connecting to SinricPro...")
        await sinric_pro.begin(config)
        print("Connected! You can now control your switch via Alexa or Google Home.")
        print("Try saying: 'Alexa, turn on <device name>'")
        print()
        print("Press Ctrl+C to exit")

        # Keep the application running
        while True:
            await asyncio.sleep(1)

            # Example: Send a power state event every 30 seconds
            # Uncomment the following to test sending events:
            #await asyncio.sleep(30)
            #await my_switch.send_power_state_event(False)

    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await sinric_pro.stop()


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
