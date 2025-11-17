"""
SinricPro Light Example

Demonstrates RGB light control with power, brightness, color, and color temperature.
"""

import asyncio
import os

from sinricpro import SinricPro, SinricProLight, SinricProConfig

# Device ID from SinricPro portal
DEVICE_ID = "YOUR_DEVICE_ID_HERE"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR_APP_KEY_HERE")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR_APP_SECRET_HERE")

async def on_power_state(state: bool) -> bool:
    """
    Handle power state changes.

    Args:
        state: True for On, False for Off

    Returns:
        True if successful
    """
    print(f"Light turned {'ON' if state else 'OFF'}")

    # TODO: Control your physical light
    # For example:
    # - Turn LED strip on/off
    # - Send command to smart bulb

    return True

async def on_brightness(brightness: int) -> bool:
    """
    Handle brightness changes.

    Args:
        brightness: Brightness level (0-100)

    Returns:
        True if successful
    """
    print(f"Brightness set to {brightness}%")

    # TODO: Set brightness of your physical light
    # For example:
    # - Adjust PWM duty cycle
    # - Send brightness command to smart bulb

    return True

async def on_color(r: int, g: int, b: int) -> bool:
    """
    Handle color changes.

    Args:
        r: Red component (0-255)
        g: Green component (0-255)
        b: Blue component (0-255)

    Returns:
        True if successful
    """
    print(f"Color set to RGB({r}, {g}, {b})")

    # TODO: Set color of your physical light
    # For example:
    # - Set RGB LED strip colors
    # - Send color command to smart bulb

    return True

async def on_color_temperature(temperature: int) -> bool:
    """
    Handle color temperature changes.

    Args:
        temperature: Color temperature in Kelvin (2000-7000)

    Returns:
        True if successful
    """
    print(f"Color temperature set to {temperature}K")

    # TODO: Set color temperature of your physical light
    # For example:
    # - Adjust warm/cool white LEDs
    # - Send temperature command to smart bulb

    return True

async def main() -> None:
    """Main function."""
    # Create SinricPro instance
    sinric_pro = SinricPro.get_instance()

    # Create light device
    my_light = SinricProLight(DEVICE_ID)

    # Register callbacks
    my_light.on_power_state(on_power_state)
    my_light.on_brightness(on_brightness)
    my_light.on_color(on_color)
    my_light.on_color_temperature(on_color_temperature)

    # Add device to SinricPro
    sinric_pro.add(my_light)

    # Configure and connect
    config = SinricProConfig(
        app_key=APP_KEY,
        app_secret=APP_SECRET
    )

    try:
        print("Connecting to SinricPro...")
        await sinric_pro.begin(config)
        print("Connected! You can now control your light via Alexa or Google Home.")
        print("Try saying:")
        print("  - 'Alexa, turn on <device name>'")
        print("  - 'Alexa, set <device name> to 50%'")
        print("  - 'Alexa, set <device name> to red'")
        print("  - 'Alexa, set <device name> to warm white'")
        print()
        print("Press Ctrl+C to exit")

        # Keep the application running
        while True:
            await asyncio.sleep(1)

            # Example: Send events to update SinricPro with physical changes
            # Uncomment to test:
            # await asyncio.sleep(20)
            # await my_light.send_power_state_event(True)
            # await asyncio.sleep(20)
            # await my_light.send_brightness_event(60)
            # await asyncio.sleep(20)
            # await my_light.send_color_event(255, 0, 0)  # Red
            # await asyncio.sleep(20)
            # await my_light.send_color_temperature_event(4000)

    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await sinric_pro.stop()


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
