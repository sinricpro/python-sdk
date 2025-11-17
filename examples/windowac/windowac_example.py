"""SinricPro WindowAC Example - Air conditioner control with thermostat."""
import asyncio
import os
from typing import Any

from sinricpro import SinricPro, SinricProWindowAC, SinricProConfig

# Device ID from SinricPro portal
DEVICE_ID = "YOUR_DEVICE_ID_HERE"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR_APP_KEY_HERE")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR_APP_SECRET_HERE")
 
power_state = False  # Current power state
thermostat_mode = "AUTO"  # Current mode: AUTO, COOL, HEAT, ECO, etc.
target_temperature = 22.0  # Target temperature in Celsius
current_temperature = 25.0  # Current room temperature
fan_speed = 50  # Fan speed (0-100)

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

    # TODO: Control your physical AC unit
    # Example with IR remote or relay:
    # if state:
    #     send_ir_command("POWER_ON")
    # else:
    #     send_ir_command("POWER_OFF")

    print(f"[Hardware] AC turned {'on' if state else 'off'}")
    return True


async def on_thermostat_mode(mode: str) -> bool:
    """
    Handle thermostat mode change requests.

    Args:
        mode: Thermostat mode (AUTO, COOL, HEAT, ECO, etc.)

    Returns:
        True if successful, False otherwise
    """
    global thermostat_mode
    print(f"\n[Callback] Thermostat Mode: {mode}")
    thermostat_mode = mode

    # TODO: Control your AC mode
    # send_ir_command(f"MODE_{mode}")

    print(f"[Hardware] AC mode set to {mode}")
    return True


async def on_target_temperature(temperature: float) -> bool:
    """
    Handle target temperature change requests.

    Args:
        temperature: Target temperature in Celsius

    Returns:
        True if successful, False otherwise
    """
    global target_temperature
    print(f"\n[Callback] Target Temperature: {temperature}°C")
    target_temperature = temperature

    # TODO: Control your AC target temperature
    # send_ir_command(f"TEMP_{int(temperature)}")

    print(f"[Hardware] Target temperature set to {temperature}°C")
    return True


async def on_range_value(speed: int) -> bool:
    """
    Handle fan speed change requests.

    Args:
        speed: Fan speed level (0-100)

    Returns:
        True if successful, False otherwise
    """
    global fan_speed
    print(f"\n[Callback] Fan Speed: {speed}")
    fan_speed = speed

    # TODO: Control your AC fan speed
    # Convert to discrete levels if needed
    # if speed < 33:
    #     send_ir_command("FAN_LOW")
    # elif speed < 66:
    #     send_ir_command("FAN_MEDIUM")
    # else:
    #     send_ir_command("FAN_HIGH")

    print(f"[Hardware] Fan speed set to {speed}")
    return True


async def on_adjust_range_value(speed_delta: int) -> bool:
    """
    Handle relative fan speed adjustment requests.

    Args:
        speed_delta: Change in speed (-100 to +100)

    Returns:
        True if successful, False otherwise
    """
    global fan_speed
    new_speed = max(0, min(100, fan_speed + speed_delta))
    print(f"\n[Callback] Adjust fan speed by {speed_delta:+d} → {new_speed}")
    fan_speed = new_speed

    print(f"[Hardware] Fan speed adjusted to {new_speed}")
    return True


async def on_setting(setting: str, value: Any) -> bool:
    """
    Handle device setting changes.

    Args:
        setting: Setting name (e.g., "swing", "sleep_mode", "turbo")
        value: Setting value

    Returns:
        True if successful, False otherwise
    """
    print(f"\n[Setting] {setting} = {value}")
    return True

async def simulate_temperature_sensor(ac: SinricProWindowAC) -> None:
    """Simulate temperature sensor readings and send events."""
    await asyncio.sleep(5)  # Wait 5 seconds

    global current_temperature

    while True:
        # Simulate temperature reading
        print(f"\n[Simulating temperature sensor reading: {current_temperature}°C]")

        # Send temperature update event to SinricPro
        success = await ac.send_temperature_event(current_temperature)
        if success:
            print(f"[Event] Temperature event sent: {current_temperature}°C")
        else:
            print("[Event] Failed to send temperature event (rate limited or disconnected)")

        # Simulate temperature changing (cooling when AC is on)
        if power_state and thermostat_mode == "COOL":
            if current_temperature > target_temperature:
                current_temperature -= 0.5
        elif power_state and thermostat_mode == "HEAT":
            if current_temperature < target_temperature:
                current_temperature += 0.5

        await asyncio.sleep(61)  # Send update every 60 seconds


async def main() -> None:
    # Create SinricPro instance and AC device
    sinric_pro = SinricPro.get_instance()
    ac = SinricProWindowAC(DEVICE_ID)

    # Register callbacks
    ac.on_power_state(on_power_state)
    ac.on_thermostat_mode(on_thermostat_mode)
    ac.on_target_temperature(on_target_temperature)
    ac.on_range_value(on_range_value)
    ac.on_adjust_range_value(on_adjust_range_value)
    ac.on_setting(on_setting)

    # Add device to SinricPro
    sinric_pro.add(ac)

    # Configure connection
    config = SinricProConfig(app_key=APP_KEY, app_secret=APP_SECRET)

    try:
        print("=" * 60)
        print("SinricPro WindowAC Example")
        print("=" * 60)
        print("\nConnecting to SinricPro...")
        await sinric_pro.begin(config)
        print("✓ Connected! AC is ready.")

        print("\n" + "=" * 60)
        print("Voice Commands:")
        print("=" * 60)
        print("  • 'Alexa, turn on [device name]'")
        print("  • 'Alexa, turn off [device name]'")
        print("  • 'Alexa, set [device name] to 22 degrees'")
        print("  • 'Alexa, set [device name] to cool mode'")
        print("  • 'Alexa, set [device name] to heat mode'")
        print("  • 'Alexa, increase fan speed on [device name]'")

        print("\n" + "=" * 60)
        print("Features:")
        print("=" * 60)
        print("  • Power State Control: On/Off")
        print("  • Thermostat Mode: AUTO, COOL, HEAT, ECO")
        print("  • Target Temperature: Set desired temperature")
        print("  • Temperature Sensor: Report current room temperature")
        print("  • Fan Speed Control: 0-100 (or discrete levels)")
        print("  • Setting Controller: Swing, Sleep mode, Turbo")
        print("  • Push Notifications: Alert user of events")

        print("\n" + "=" * 60)
        print("Press Ctrl+C to exit")
        print("=" * 60)

        # Start temperature sensor simulation
        asyncio.create_task(simulate_temperature_sensor(ac))

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
