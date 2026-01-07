"""SinricPro Module Settings Example - Handle module-level configuration."""

import asyncio
import os
from typing import Any

from sinricpro import SinricPro, SinricProSwitch, SinricProConfig

# Device ID from SinricPro portal
DEVICE_ID = "YOUR_DEVICE_ID_HERE"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR_APP_KEY_HERE")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR_APP_SECRET_HERE")

# Module configuration values
module_config = {
    "id_wifi_retry_count": 3,
    "id_log_level": "INFO",
    "id_heartbeat_interval": 300,
}


async def on_power_state(state: bool) -> bool:
    """Handle power state change for the switch device."""
    print(f"\n[Device] Power: {'ON' if state else 'OFF'}")
    return True


async def on_module_setting(setting_id: str, value: Any) -> bool:
    """
    Handle module-level setting changes.

    Module settings are configuration values for the module (dev board) itself,
    not for individual devices. Examples include WiFi settings, logging level,
    or other module-wide configurations.

    Args:
        setting_id: The setting identifier (e.g., "wifi_retry_count")
        value: The new value for the setting (can be int, float, bool, or string)

    Returns:
        True if the setting was applied successfully, False otherwise
    """
    print(f"\n[Module Setting] {setting_id} = {value}")

    # Handle different setting types
    if setting_id == "id_wifi_retry_count":
        if isinstance(value, int) and 1 <= value <= 10:
            module_config["wifi_retry_count"] = value
            print(f"  WiFi retry count set to {value}")
            return True
        else:
            print(f"  Invalid wifi_retry_count value: {value}")
            return False

    elif setting_id == "id_log_level":
        valid_levels = ["DEBUG", "INFO", "WARN", "ERROR"]
        if isinstance(value, str) and value.upper() in valid_levels:
            module_config["log_level"] = value.upper()
            print(f"  Log level set to {value.upper()}")
            return True
        else:
            print(f"  Invalid log_level value: {value}")
            return False

    elif setting_id == "id_heartbeat_interval":
        if isinstance(value, int) and 60 <= value <= 600:
            module_config["heartbeat_interval"] = value
            print(f"  Heartbeat interval set to {value} seconds")
            return True
        else:
            print(f"  Invalid heartbeat_interval value: {value}")
            return False

    else:
        print(f"  Unknown setting: {setting_id}")
        return False


async def main() -> None:
    # Get SinricPro instance
    sinric_pro = SinricPro.get_instance()

    # Create a switch device (module settings work alongside device settings)
    switch = SinricProSwitch(DEVICE_ID)
    switch.on_power_state(on_power_state)

    # Add device to SinricPro
    sinric_pro.add(switch)

    # Register module-level setting callback
    # This is separate from device-level settings (device.on_setting())
    sinric_pro.on_set_setting(on_module_setting)

    # Example function to demonstrate sending module setting events
    async def send_example_module_setting():
        """Send an example module setting event after connection."""
        await asyncio.sleep(5)  # Wait for connection to stabilize
        print("\n[Example] Sending module setting event...")
        sent = await sinric_pro.send_setting_event("id_wifi_retry_count", 5)
        print(f"  Module setting event sent: {sent}")

    # Configure connection
    config = SinricProConfig(app_key=APP_KEY, app_secret=APP_SECRET)

    try:
        print("=" * 60)
        print("SinricPro Module Settings Example")
        print("=" * 60)
        print("\nConnecting to SinricPro...")
        await sinric_pro.begin(config)
        print("Connected!")

        print("\n" + "=" * 60)
        print("Module Settings vs Device Settings:")
        print("=" * 60)
        print("  Module Settings: Configuration for the module/board itself")
        print("    - Receive via: sinric_pro.on_set_setting(callback)")
        print("    - Send via: sinric_pro.send_setting_event(setting_id, value)")
        print("    - Examples: WiFi retry count, log level, heartbeat interval")
        print("")
        print("  Device Settings: Configuration for individual devices")
        print("    - Receive via: device.on_setting(callback)")
        print("    - Send via: device.send_setting_event(setting_id, value)")
        print("    - Examples: Device-specific modes, thresholds, etc.")

        print("\n" + "=" * 60)
        print("Current Module Configuration:")
        print("=" * 60)
        for key, value in module_config.items():
            print(f"  {key}: {value}")

        print("\n" + "=" * 60)
        print("Press Ctrl+C to exit")
        print("=" * 60)

        # Start the example setting event task
        #asyncio.create_task(send_example_module_setting())

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
