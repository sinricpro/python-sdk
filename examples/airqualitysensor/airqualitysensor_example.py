"""SinricPro AirQualitySensor Example - Air quality and temperature monitoring."""
import asyncio
import os
import random
from typing import Any

from sinricpro import SinricPro, SinricProAirQualitySensor, SinricProConfig

# Device ID from SinricPro portal
DEVICE_ID = "YOUR_DEVICE_ID_HERE"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR_APP_KEY_HERE")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR_APP_SECRET_HERE")

# Sensor settings
reporting_interval = 60  # Seconds between reports
pm2_5_threshold = 35  # μg/m³ - WHO 24-hour guideline
alert_enabled = True  # Enable air quality alerts


# Air Quality Index (AQI) calculation helper
def calculate_aqi(pm2_5: int) -> tuple[int, str]:
    """
    Calculate AQI from PM2.5 concentration.

    Returns:
        Tuple of (AQI value, category string)
    """
    if pm2_5 <= 12:
        return (int((50 / 12) * pm2_5), "Good")
    elif pm2_5 <= 35:
        return (int(50 + ((100 - 50) / (35 - 12)) * (pm2_5 - 12)), "Moderate")
    elif pm2_5 <= 55:
        return (int(100 + ((150 - 100) / (55 - 35)) * (pm2_5 - 35)), "Unhealthy for Sensitive Groups")
    elif pm2_5 <= 150:
        return (int(150 + ((200 - 150) / (150 - 55)) * (pm2_5 - 55)), "Unhealthy")
    elif pm2_5 <= 250:
        return (int(200 + ((300 - 200) / (250 - 150)) * (pm2_5 - 150)), "Very Unhealthy")
    else:
        return (int(300 + ((500 - 300) / (500 - 250)) * min(pm2_5 - 250, 250)), "Hazardous")


async def on_setting(setting: str, value: Any) -> bool:
    """
    Handle device setting changes.

    Args:
        setting: Setting name
        value: Setting value

    Returns:
        True if successful, False otherwise
    """
    global reporting_interval, pm2_5_threshold, alert_enabled
    print(f"\n[Setting] {setting} = {value}")

    # Handle reporting interval setting
    if setting == "reporting_interval":
        reporting_interval = int(value)
        if reporting_interval < 10:
            print(f"[Error] Interval too short: {reporting_interval}s (minimum 10s)")
            return False
        print(f"[Setting] Reporting interval set to {reporting_interval}s")
        return True

    # Handle PM2.5 threshold setting
    elif setting == "pm2_5_threshold":
        pm2_5_threshold = int(value)
        print(f"[Setting] PM2.5 threshold set to {pm2_5_threshold} μg/m³")
        return True

    # Handle alert enable/disable
    elif setting == "alert_enabled":
        alert_enabled = bool(value)
        print(f"[Setting] Alerts {'enabled' if alert_enabled else 'disabled'}")
        return True

    print(f"[Warning] Unknown setting: {setting}")
    return False


async def monitor_air_quality(sensor: SinricProAirQualitySensor) -> None:
    """Monitor air quality and temperature, send periodic updates."""
    print("\n[Starting air quality monitor]")
    print(f"[Settings] Reporting every {reporting_interval}s")
    print(f"[Settings] PM2.5 alert threshold: {pm2_5_threshold} μg/m³")

    await asyncio.sleep(3)  # Initial delay

    while True:
        # TODO: Replace with actual sensor readings
        # Example with PMS5003/PMS7003 particulate sensor:
        # import pms5003
        # sensor_data = pms5003.read()
        # pm1_0 = sensor_data.pm1_0
        # pm2_5 = sensor_data.pm2_5
        # pm10 = sensor_data.pm10

        # Example with DHT22 for temperature:
        # import Adafruit_DHT
        # humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHT_PIN)

        # Simulate realistic air quality readings for demo
        pm1_0 = random.randint(5, 30)  # PM1.0 (μg/m³)
        pm2_5 = random.randint(10, 60)  # PM2.5 (μg/m³)
        pm10 = random.randint(15, 80)  # PM10 (μg/m³)

        # Calculate AQI from PM2.5
        aqi, aqi_category = calculate_aqi(pm2_5)

        print("\n" + "=" * 60)
        print("[Air Quality Measurement]")
        print("=" * 60)
        print(f"  PM1.0:       {pm1_0:3d} μg/m³")
        print(f"  PM2.5:       {pm2_5:3d} μg/m³")
        print(f"  PM10:        {pm10:3d} μg/m³")
        print(f"  AQI:         {aqi:3d} ({aqi_category})")

        # Send air quality event to SinricPro
        success = await sensor.send_air_quality_event(
            pm1_0=pm1_0,
            pm2_5=pm2_5,
            pm10=pm10,
        )

        if success:
            print("[Event] Air quality data sent to SinricPro")

            # Check PM2.5 threshold and send alert if needed
            if alert_enabled and pm2_5 > pm2_5_threshold:
                alert_message = (
                    f"Air quality alert: PM2.5 is {pm2_5} μg/m³ "
                    f"(threshold: {pm2_5_threshold} μg/m³). "
                    f"AQI: {aqi} ({aqi_category})"
                )
                notification_success = await sensor.send_push_notification(alert_message)
                if notification_success:
                    print(f"[Alert] {alert_message}")
        else:
            print("[Event] Failed to send air quality data (rate limited or disconnected)")

        # Wait for next reporting interval
        await asyncio.sleep(reporting_interval)


async def main() -> None:
    # Create SinricPro instance and air quality sensor device
    sinric_pro = SinricPro.get_instance()
    sensor = SinricProAirQualitySensor(DEVICE_ID)

    # Register callbacks
    sensor.on_setting(on_setting)

    # Add device to SinricPro
    sinric_pro.add(sensor)

    # Configure connection
    config = SinricProConfig(app_key=APP_KEY, app_secret=APP_SECRET)

    try:
        print("=" * 60)
        print("SinricPro AirQualitySensor Example")
        print("=" * 60)
        print("\nConnecting to SinricPro...")
        await sinric_pro.begin(config)
        print("✓ Connected! Air quality sensor is ready.")

        print("\n" + "=" * 60)
        print("Features:")
        print("=" * 60)
        print("  • PM1.0 Measurement: Fine particulate matter (μg/m³)")
        print("  • PM2.5 Measurement: Fine particulate matter (μg/m³)")
        print("  • PM10 Measurement: Coarse particulate matter (μg/m³)")
        print("  • AQI Calculation: Air Quality Index from PM2.5")
        print("  • Temperature Sensing: Current temperature (°C)")
        print("  • Humidity Sensing: Current humidity (%)")
        print("  • Periodic Reporting: Configurable interval")
        print("  • Air Quality Alerts: Notify on poor air quality")
        print("  • Push Notifications: Alert user of threshold events")

        print("\n" + "=" * 60)
        print("Hardware Setup:")
        print("=" * 60)
        print("  • PMS5003/PMS7003: Laser particulate sensor (UART)")
        print("  • SDS011: Nova PM sensor (UART)")
        print("  • DHT22/AM2302: Temperature & humidity sensor")
        print("  • BME280: Temperature, humidity, pressure (I2C)")
        print("  • MH-Z19: CO2 sensor (optional, UART)")

        print("\n" + "=" * 60)
        print("Air Quality Index (AQI) Categories:")
        print("=" * 60)
        print("  • 0-50:    Good")
        print("  • 51-100:  Moderate")
        print("  • 101-150: Unhealthy for Sensitive Groups")
        print("  • 151-200: Unhealthy")
        print("  • 201-300: Very Unhealthy")
        print("  • 301+:    Hazardous")

        print("\n" + "=" * 60)
        print("Use Cases:")
        print("=" * 60)
        print("  • Indoor air quality monitoring")
        print("  • Smart home ventilation control")
        print("  • Health monitoring for sensitive individuals")
        print("  • Air purifier automation")
        print("  • Environmental awareness")

        print("\n" + "=" * 60)
        print("Press Ctrl+C to exit")
        print("=" * 60)

        # Start air quality monitoring
        asyncio.create_task(monitor_air_quality(sensor))

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
