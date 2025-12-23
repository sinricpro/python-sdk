"""
SinricPro Temperature Sensor Example

Demonstrates temperature and humidity monitoring.
"""

import asyncio
import os
import random

from sinricpro import SinricPro, SinricProTemperatureSensor, SinricProConfig

# Device ID from SinricPro portal
DEVICE_ID = "YOUR-DEVICE-ID"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR-APP-KEY")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR-APP-SECRET")

async def simulate_sensor_readings(sensor: SinricProTemperatureSensor) -> None:
    """Simulate temperature/humidity readings for testing."""
    temperature = 20.0
    humidity = 50.0

    while True:
        # Wait 60 seconds between readings (rate limit is 60 seconds for sensors)
        await asyncio.sleep(60)

        # Simulate small variations
        temperature += random.uniform(-0.5, 0.5)
        humidity += random.uniform(-2.0, 2.0)

        # Keep in reasonable ranges
        temperature = round(max(15.0, min(30.0, temperature)), 2)
        humidity = round(max(30.0, min(80.0, humidity)), 2)

        # Send temperature and humidity event
        success = await sensor.send_temperature_event(temperature, humidity)
        if success:
            print(f"[Event] Temperature: {temperature:.1f}°C, Humidity: {humidity:.1f}% sent")
        else:
            print("[Event] Failed to send temperature event (rate limited or disconnected)")

async def main() -> None:
    """Main function."""
    # Create SinricPro instance
    sinric_pro = SinricPro.get_instance()

    # Create temperature sensor device
    temp_sensor = SinricProTemperatureSensor(DEVICE_ID)

    # Add device to SinricPro
    sinric_pro.add(temp_sensor)

    # Configure and connect
    config = SinricProConfig(app_key=APP_KEY, app_secret=APP_SECRET)

    try:
        print("Connecting to SinricPro...")
        await sinric_pro.begin(config)
        print("Connected! Temperature sensor is ready.")
        print()
        print("This example will send temperature readings every 60 seconds.")
        print("In a real implementation, read from DHT22, BME280, etc.")
        print()
        print("Check temperature in Alexa app or ask:")
        print("  'Alexa, what's the temperature in [device name]?'")
        print()
        print("Press Ctrl+C to exit")

        # Start sensor simulation
        await simulate_sensor_readings(temp_sensor)

    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await sinric_pro.stop()


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
