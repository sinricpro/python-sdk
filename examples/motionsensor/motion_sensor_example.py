"""
SinricPro Motion Sensor Example

Demonstrates motion detection events.
"""

import asyncio
import os

from sinricpro import SinricPro, SinricProMotionSensor, SinricProConfig

# Device ID from SinricPro portal
DEVICE_ID = "YOUR_DEVICE_ID_HERE"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR_APP_KEY_HERE")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR_APP_SECRET_HERE")

async def simulate_motion_detection(sensor: SinricProMotionSensor) -> None:
    """Simulate motion detection for testing."""
    while True:
        # Wait 10 seconds
        await asyncio.sleep(10)

        # Send motion detected event
        success = await sensor.send_motion_event(True)
        if success:
            print("[Event] Motion detected event sent")
        else:
            print("[Event] Failed to send motion detected event (rate limited or disconnected)")

        # Wait 5 seconds
        await asyncio.sleep(5)

        # Send no motion event
        success = await sensor.send_motion_event(False)
        if success:
            print("[Event] No motion event sent")
        else:
            print("[Event] Failed to send event (rate limited or disconnected)")

async def main() -> None:
    """Main function."""
    # Create SinricPro instance
    sinric_pro = SinricPro.get_instance()

    # Create motion sensor device
    motion_sensor = SinricProMotionSensor(DEVICE_ID)

    # Add device to SinricPro
    sinric_pro.add(motion_sensor)

    # Configure and connect
    config = SinricProConfig(app_key=APP_KEY, app_secret=APP_SECRET)

    try:
        print("Connecting to SinricPro...")
        await sinric_pro.begin(config)
        print("Connected! Motion sensor is ready.")
        print()
        print("This example will simulate motion detection every 10 seconds.")
        print("In a real implementation, connect to your PIR sensor.")
        print()
        print("Press Ctrl+C to exit")

        # Start motion simulation
        await simulate_motion_detection(motion_sensor)

    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await sinric_pro.stop()


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
