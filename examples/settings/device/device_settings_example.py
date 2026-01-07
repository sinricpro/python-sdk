"""SinricPro Device Settings Example - Handle device-level configuration."""
import asyncio
import os
from typing import Any

from sinricpro import SinricPro, SinricProBlinds, SinricProConfig

# Device ID from SinricPro portal
DEVICE_ID = "YOUR_DEVICE_ID_HERE"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR_APP_KEY_HERE")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR_APP_SECRET_HERE")

# Device state
power_state = False
position = 0  # 0-100

# Device-specific settings
device_settings = {
    "id_tilt": 50,           # Tilt angle (0-100)
    "id_direction": "up",    # Movement direction preference
    "id_speed": "normal",    # Movement speed: slow, normal, fast
    "id_auto_close": False,  # Auto-close after timeout
    "id_close_timeout": 300, # Auto-close timeout in seconds
}


async def on_power_state(state: bool) -> bool:
    """Handle power state change requests."""
    global power_state
    print(f"\n[Callback] Power: {'ON' if state else 'OFF'}")
    power_state = state
    return True
 

async def on_device_setting(setting_id: str, value: Any) -> bool:
    """
    Handle device-level setting changes.

    Device settings are configuration values specific to this device,
    such as tilt angle, movement direction, speed preferences, etc.

    Args:
        setting_id: The setting identifier (e.g., "tilt", "direction")
        value: The new value for the setting (can be int, float, bool, or string)

    Returns:
        True if the setting was applied successfully, False otherwise
    """
    print(f"\n[Device Setting] {setting_id} = {value} (type: {type(value).__name__})")

    # Handle tilt setting
    if setting_id == "id_tilt":
        if isinstance(value, (int, float)) and 0 <= value <= 100:
            device_settings["tilt"] = int(value)
            print(f"  Tilt angle set to {int(value)}%")
            # TODO: Apply tilt to physical device
            # set_blinds_tilt(int(value))
            return True
        else:
            print(f"  Invalid tilt value: {value} (must be 0-100)")
            return False

    # Handle direction setting
    elif setting_id == "id_direction":
        valid_directions = ["up", "down"]
        if isinstance(value, str) and value.lower() in valid_directions:
            device_settings["direction"] = value.lower()
            print(f"  Direction preference set to '{value.lower()}'")
            return True
        else:
            print(f"  Invalid direction value: {value} (must be 'up' or 'down')")
            return False

    # Handle speed setting
    elif setting_id == "id_speed":
        valid_speeds = ["slow", "normal", "fast"]
        if isinstance(value, str) and value.lower() in valid_speeds:
            device_settings["speed"] = value.lower()
            print(f"  Movement speed set to '{value.lower()}'")
            # TODO: Apply speed to physical device
            # set_motor_speed(value.lower())
            return True
        else:
            print(f"  Invalid speed value: {value} (must be 'slow', 'normal', or 'fast')")
            return False

    # Handle auto_close setting
    elif setting_id == "id_auto_close":
        if isinstance(value, bool):
            device_settings["auto_close"] = value
            print(f"  Auto-close {'enabled' if value else 'disabled'}")
            return True
        else:
            print(f"  Invalid auto_close value: {value} (must be boolean)")
            return False

    # Handle close_timeout setting
    elif setting_id == "id_close_timeout":
        if isinstance(value, (int, float)) and 60 <= value <= 3600:
            device_settings["close_timeout"] = int(value)
            print(f"  Close timeout set to {int(value)} seconds")
            return True
        else:
            print(f"  Invalid close_timeout value: {value} (must be 60-3600)")
            return False

    else:
        print(f"  Unknown setting: {setting_id}")
        return False


async def main() -> None:
    # Get SinricPro instance
    sinric_pro = SinricPro.get_instance()

    # Create a blinds device
    blinds = SinricProBlinds(DEVICE_ID)

    # Register device callbacks
    blinds.on_power_state(on_power_state) 

    # Register device-level setting callback
    # This handles settings specific to this device
    blinds.on_setting(on_device_setting)

    # Add device to SinricPro
    sinric_pro.add(blinds)

    # Example function to demonstrate sending device setting events
    async def send_example_setting():
        """Send an example device setting event after connection."""
        await asyncio.sleep(5)  # Wait for connection to stabilize
        print("\n[Example] Sending device setting event...")
        sent = await blinds.send_setting_event("id_tilt", 75)
        print(f"  Device setting event sent: {sent}")

    # Configure connection
    config = SinricProConfig(app_key=APP_KEY, app_secret=APP_SECRET)

    try:
        print("=" * 60)
        print("SinricPro Device Settings Example")
        print("=" * 60)
        print("\nConnecting to SinricPro...")
        await sinric_pro.begin(config)
        print("Connected!")

        print("\n" + "=" * 60)
        print("Device Settings vs Module Settings:")
        print("=" * 60)
        print("  Device Settings: Configuration for THIS specific device")
        print("    - Receive via: device.on_setting(callback)")
        print("    - Send via: device.send_setting_event(setting_id, value)")
        print("    - Examples: Tilt angle, speed, direction, auto-close")
        print("    - Callback receives: (setting_id, value)")
        print("")
        print("  Module Settings: Configuration for the module/board")
        print("    - Receive via: sinric_pro.on_set_setting(callback)")
        print("    - Send via: sinric_pro.send_setting_event(setting_id, value)")
        print("    - Examples: WiFi retry count, log level")

        print("\n" + "=" * 60)
        print("Current Device Settings:")
        print("=" * 60)
        for key, value in device_settings.items():
            print(f"  {key}: {value}")

        print("\n" + "=" * 60)
        print("Voice Commands:")
        print("=" * 60)
        print("  'Alexa, turn on [device name]'")
        print("  'Alexa, set [device name] to 50 percent'")
        print("  (Device settings are configured via SinricPro portal)")

        print("\n" + "=" * 60)
        print("Press Ctrl+C to exit")
        print("=" * 60)

        # Start the example setting event task
        #asyncio.create_task(send_example_setting())

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
