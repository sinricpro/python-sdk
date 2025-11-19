"""
SinricPro Custom Device Example

Demonstrates how to use SinricProCustomDevice to create flexible devices
with any combination of capabilities you need.
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sinricpro import SinricPro, SinricProCustomDevice, SinricProConfig

# Device ID from SinricPro portal
DEVICE_ID = "YOUR_DEVICE_ID_HERE"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR_APP_KEY_HERE")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR_APP_SECRET_HERE")

# Device state
device_state = {
    "power": False,
    "brightness": 0,
    "temperature": 22.0,
    "color": {"r": 255, "g": 255, "b": 255},
}


async def on_power_state(state: bool) -> bool:
    """Handle power state changes."""
    global device_state
    device_state["power"] = state
    print(f"\n[Power] Device turned {'ON' if state else 'OFF'}")
    return True


async def on_brightness(brightness: int) -> bool:
    """Handle brightness changes."""
    global device_state
    device_state["brightness"] = brightness
    print(f"\n[Brightness] Set to {brightness}%")
    return True


async def on_adjust_brightness(brightness_delta: int) -> bool:
    """Handle brightness adjustments."""
    global device_state
    new_brightness = max(0, min(100, device_state["brightness"] + brightness_delta))
    device_state["brightness"] = new_brightness
    print(f"\n[Brightness] Adjusted by {brightness_delta} to {new_brightness}%")
    return True


async def on_color(r: int, g: int, b: int) -> bool:
    """Handle color changes."""
    global device_state
    device_state["color"] = {"r": r, "g": g, "b": b}
    print(f"\n[Color] Set to RGB({r}, {g}, {b})")
    return True


async def on_color_temperature(color_temp: int) -> bool:
    """Handle color temperature changes."""
    print(f"\n[Color Temperature] Set to {color_temp}K")
    return True


async def on_target_temperature(temperature: float) -> bool:
    """Handle target temperature changes."""
    global device_state
    device_state["temperature"] = temperature
    print(f"\n[Temperature] Target set to {temperature}°C")
    return True


async def on_thermostat_mode(mode: str) -> bool:
    """Handle thermostat mode changes."""
    print(f"\n[Thermostat] Mode set to {mode}")
    return True


async def on_lock_state(state: str) -> bool:
    """Handle lock state changes."""
    print(f"\n[Lock] State set to {state}")
    return True


async def on_setting(setting: str, value: Any) -> bool:
    """Handle device setting changes."""
    print(f"\n[Setting] {setting} = {value}")
    return True

async def main() -> None:
    """Main function."""
    print("=" * 70)
    print("SinricPro Custom Device Example")
    print("=" * 70)
    print("\nThis example demonstrates a custom device that combines:")
    print("  • Power control (on/off)")
    print("  • Brightness control (0-100%)")
    print("  • Color control (RGB)")
    print("  • Color temperature control")
    print("  • Temperature sensor (reporting)")
    print("  • Thermostat control")
    print("  • Lock control")
    print("  • Settings control")
    print("\nYou can mix and match any capabilities you need!")
    print("=" * 70)

    # Create SinricPro instance
    sinric_pro = SinricPro.get_instance()

    # Create custom device
    # You can use any product_type from your SinricPro portal
    custom_device = SinricProCustomDevice(DEVICE_ID)

    # Register callbacks for capabilities you want to use
    # You only need to register the ones you'll actually use!

    # Power & Lighting
    custom_device.on_power_state(on_power_state)
    custom_device.on_brightness(on_brightness)
    custom_device.on_adjust_brightness(on_adjust_brightness)
    custom_device.on_color(on_color)
    custom_device.on_color_temperature(on_color_temperature)

    # Climate
    custom_device.on_target_temperature(on_target_temperature)
    custom_device.on_thermostat_mode(on_thermostat_mode)

    # Security
    custom_device.on_lock_state(on_lock_state)

    # Common
    custom_device.on_setting(on_setting)

    # Add device to SinricPro
    sinric_pro.add(custom_device)

    # Configure connection
    config = SinricProConfig(app_key=APP_KEY, app_secret=APP_SECRET)

    try:
        print("\nConnecting to SinricPro...")
        await sinric_pro.begin(config)
        print("✓ Connected! Custom device is ready.")

        print("\n" + "=" * 70)
        print("Press Ctrl+C to exit")
        print("=" * 70)

        # Keep running
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
