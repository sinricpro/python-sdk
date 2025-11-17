"""SinricPro PowerSensor Example - Energy monitoring and power measurement."""
import asyncio
import os
import random
from typing import Any

from sinricpro import SinricPro, SinricProPowerSensor, SinricProConfig


# Device ID from SinricPro portal
DEVICE_ID = "YOUR_DEVICE_ID_HERE"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR_APP_KEY_HERE")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR_APP_SECRET_HERE")

# Sensor settings
reporting_interval = 60  # Seconds between reports
power_threshold = 1000.0  # Alert if power exceeds this (watts)

async def on_setting(setting: str, value: Any) -> bool:
    """
    Handle device setting changes.

    Args:
        setting: Setting name
        value: Setting value

    Returns:
        True if successful, False otherwise
    """
    print(f"\n[Setting] {setting} = {value}")
 

    print(f"[Warning] Unknown setting: {setting}")
    return False

async def simulate_power_consumption(sensor: SinricProPowerSensor) -> None:
    """Monitor power consumption and send periodic updates."""
    print("\n[Starting power consumption monitor]")
    print(f"[Settings] Reporting every {reporting_interval}s")
    print(f"[Settings] Alert threshold: {power_threshold}W")

    await asyncio.sleep(3)  # Initial delay

    while True:
        # TODO: Replace with actual sensor readings
        # Example with INA219/INA3221 power sensor:
        # voltage = ina219.voltage()
        # current = ina219.current() / 1000.0  # Convert mA to A
        # power = ina219.power() / 1000.0  # Convert mW to W

        # Simulate realistic power readings for demo
        voltage = 120.0 + random.uniform(-2, 2)  # 118-122V
        voltage = round(voltage, 2)

        current = random.uniform(0.5, 5.0)  # 0.5-5.0A
        current = round(current, 2)

        power = voltage * current  # Watts (assuming PF=1 for simplicity)
        power = round(power, 2)

        # Calculate apparent power and power factor for more advanced monitoring
        power_factor = random.uniform(0.85, 0.99)  # Typical PF range
        power_factor = round(power_factor, 2)

        apparent_power = power / power_factor  # VA
        apparent_power = round(apparent_power, 2)

        reactive_power = (apparent_power**2 - power**2) ** 0.5  # VAR
        reactive_power = round(reactive_power, 2)

        print("\n" + "=" * 60)
        print("[Power Measurement]")
        print("=" * 60)
        print(f"  Voltage:         {voltage:.2f} V")
        print(f"  Current:         {current:.3f} A")
        print(f"  Active Power:    {power:.2f} W")
        print(f"  Apparent Power:  {apparent_power:.2f} VA")
        print(f"  Reactive Power:  {reactive_power:.2f} VAR")
        print(f"  Power Factor:    {power_factor:.3f}")
        print("  Note: wattHours calculated automatically by SDK")

        # Send power measurement event to SinricPro
        success = await sensor.send_power_sensor_event(
            voltage=voltage,
            current=current,
            power=power,
            apparent_power=apparent_power,
            reactive_power=reactive_power,
            factor=power_factor,
        )

        if success:
            print("[Event] Power measurement sent to SinricPro")

            # Check power threshold and send alert if needed
            if power > power_threshold:
                alert_message = f"High power consumption alert: {power:.1f}W (threshold: {power_threshold}W)"
                notification_success = await sensor.send_push_notification(alert_message)
                if notification_success:
                    print(f"[Alert] {alert_message}")
        else:
            print("[Event] Failed to send power measurement (rate limited or disconnected)")

        # Wait for next reporting interval
        await asyncio.sleep(reporting_interval)

async def main() -> None:
    # Create SinricPro instance and power sensor device
    sinric_pro = SinricPro.get_instance()
    sensor = SinricProPowerSensor(DEVICE_ID)

    # Register callbacks
    sensor.on_setting(on_setting)

    # Add device to SinricPro
    sinric_pro.add(sensor)

    # Configure connection
    config = SinricProConfig(app_key=APP_KEY, app_secret=APP_SECRET)

    try:
        print("=" * 60)
        print("SinricPro PowerSensor Example")
        print("=" * 60)
        print("\nConnecting to SinricPro...")
        await sinric_pro.begin(config)
        print("✓ Connected! Power sensor is ready.")

        print("\n" + "=" * 60)
        print("Features:")
        print("=" * 60)
        print("  • Voltage Measurement: Monitor line voltage (V)")
        print("  • Current Measurement: Monitor current draw (A)")
        print("  • Power Measurement: Active power consumption (W)")
        print("  • Apparent Power: Total power including reactive (VA)")
        print("  • Reactive Power: Non-working power (VAR)")
        print("  • Power Factor: Efficiency metric (0-1)")
        print("  • Energy Tracking: Auto-calculated wattHours (Wh)")
        print("  • Periodic Reporting: Configurable interval")
        print("  • Power Threshold Alerts: Notify on high consumption")
        print("  • Push Notifications: Alert user of threshold events")

        print("\n" + "=" * 60)
        print("Hardware Setup:")
        print("=" * 60)
        print("  • INA219: I2C current/voltage/power sensor")
        print("  • INA3221: Triple-channel power monitor")
        print("  • PZEM-004T: AC power meter (UART)")
        print("  • ACS712: Hall-effect current sensor (analog)")
        print("  • SCT-013: Split-core current transformer")

        print("\n" + "=" * 60)
        print("Use Cases:")
        print("=" * 60)
        print("  • Appliance power monitoring")
        print("  • Energy consumption tracking")
        print("  • Load monitoring and balancing")
        print("  • Power quality analysis")
        print("  • Energy cost estimation")
        print("  • Standby power detection")

        print("\n" + "=" * 60)
        print("Press Ctrl+C to exit")
        print("=" * 60)

        # Start power consumption monitoring
        asyncio.create_task(simulate_power_consumption(sensor))

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
