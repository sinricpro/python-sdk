"""
SinricPro Thermostat Example

Demonstrates thermostat control with temperature monitoring.
"""

import asyncio
import os
import random

from sinricpro import SinricPro, SinricProThermostat, SinricProConfig

# Device ID from SinricPro portal
DEVICE_ID = "YOUR_DEVICE_ID_HERE"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR_APP_KEY_HERE")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR_APP_SECRET_HERE")

# Current state
current_mode = "OFF"
target_temp = 20.0
current_temp = 22.0

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

async def on_thermostat_mode(mode: str) -> bool:
    """
    Handle thermostat mode changes.

    Args:
        mode: Thermostat mode (AUTO, COOL, HEAT, ECO, OFF)

    Returns:
        True if successful
    """
    global current_mode
    print(f"Thermostat mode changed to: {mode}")
    current_mode = mode

    # TODO: Control your HVAC system here
    # - Turn on/off heating/cooling
    # - Set to appropriate mode

    return True


async def on_target_temperature(temperature: float) -> bool:
    """
    Handle target temperature changes.

    Args:
        temperature: Target temperature in Celsius

    Returns:
        True if successful
    """
    global target_temp
    print(f"Target temperature set to: {temperature}°C")
    target_temp = temperature

    # TODO: Adjust HVAC system target temperature

    return True


async def simulate_thermostat(thermostat: SinricProThermostat) -> None:
    """Simulate temperature monitoring and send to SinricPro."""
    global current_temp, target_temp, current_mode

    while True:
        await asyncio.sleep(60)  # Update every 60 seconds

        # Simulate temperature changes based on mode
        if current_mode == "COOL" and current_temp > target_temp:
            current_temp -= 0.5  # Cooling
        elif current_mode == "HEAT" and current_temp < target_temp:
            current_temp += 0.5  # Heating
        elif current_mode == "AUTO":
            if current_temp > target_temp + 1:
                current_temp -= 0.5  # Cooling
            elif current_temp < target_temp - 1:
                current_temp += 0.5  # Heating
        else:
            # Drift toward room temperature
            current_temp += round(random.uniform(-0.2, 0.2),2)

        # Add some humidity simulation
        humidity = 50.0 + round(random.uniform(-5, 5), 2)

        print(f"Current: {current_temp:.1f}°C, Target: {target_temp:.1f}°C, Mode: {current_mode}")
        await thermostat.send_temperature_event(current_temp, humidity)


async def main() -> None:
    """Main function."""
    # Create SinricPro instance
    sinric_pro = SinricPro.get_instance()

    # Create thermostat device
    my_thermostat = SinricProThermostat(DEVICE_ID)

    # Register callbacks
    my_thermostat.on_power_state(on_power_state)
    my_thermostat.on_thermostat_mode(on_thermostat_mode)
    my_thermostat.on_target_temperature(on_target_temperature)

    # Add device to SinricPro
    sinric_pro.add(my_thermostat)

    # Configure and connect
    config = SinricProConfig(app_key=APP_KEY, app_secret=APP_SECRET)

    try:
        print("Connecting to SinricPro...")
        await sinric_pro.begin(config)
        print("Connected! Thermostat is ready.")
        print()
        print("Try these voice commands:")
        print("  - 'Alexa, set [device name] to 22 degrees'")
        print("  - 'Alexa, set [device name] to cool'")
        print("  - 'Alexa, set [device name] to heat'")
        print("  - 'Alexa, turn off [device name]'")
        print("  - 'Alexa, what's the temperature in [device name]?'")
        print()
        print("Press Ctrl+C to exit")

        # Start thermostat simulatation
        await simulate_thermostat(my_thermostat)

    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await sinric_pro.stop()


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
