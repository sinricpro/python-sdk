"""SinricPro Garage Door Example - Garage door control."""
import asyncio
import os

from sinricpro import SinricPro, SinricProGarageDoor, SinricProConfig

# Device ID from SinricPro portal
DEVICE_ID = "YOUR_DEVICE_ID_HERE"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR_APP_KEY_HERE")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR_APP_SECRET_HERE")

current_state = "Close"  # "Open" or "Close"

async def on_mode_state(state: str) -> bool:
    """
    Handle garage door open/close requests.
    
    Args:
        state: "Open" or "Close"
    """
    global current_state
    print(f"Garage door command: {state}")
    
    if state == "Open" and current_state == "Close":
        print("🚪 Opening garage door...")
        # TODO: Trigger relay to open door
        # - Pulse relay for 500ms
        # - Wait for door to fully open
        # - Monitor limit switch
        current_state = "Open"
    elif state == "Close" and current_state == "Open":
        print("🚪 Closing garage door...")
        # TODO: Trigger relay to close door
        # - Check for obstructions
        # - Pulse relay for 500ms
        # - Wait for door to fully close
        # - Monitor limit switch
        current_state = "Close"
    else:
        print(f"Door already {current_state}")
    
    return True


async def simulate_physical_control(garage_door: SinricProGarageDoor) -> None:
    """Simulate physical button control and send events."""
    await asyncio.sleep(10)  # Wait 10 seconds

    print("\n[Simulating physical Open button press]")
    global current_state
    current_state = "Open"

    # Send update event to SinricPro
    success = await garage_door.send_mode_event(current_state)
    if success:
        print(f"[Event] Door event: {current_state} sent")
    else:
        print("[Event] Failed to send door event (rate limited or disconnected)")

async def main() -> None:
    sinric_pro = SinricPro.get_instance()
    garage_door = SinricProGarageDoor(DEVICE_ID)
    garage_door.on_mode_state(on_mode_state)
    sinric_pro.add(garage_door)

    config = SinricProConfig(app_key=APP_KEY, app_secret=APP_SECRET)

    try:
        print("Connecting to SinricPro...")
        await sinric_pro.begin(config)
        print("Connected! Garage door controller is ready.")
        print("\nVoice commands:")
        print("  - 'Alexa, open [device name]'")
        print("  - 'Alexa, close [device name]'")
        print("\nPress Ctrl+C to exit")

        # Start physical control simulation
        asyncio.create_task(simulate_physical_control(garage_door))

        while True:
            await asyncio.sleep(1)

            
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await sinric_pro.stop()

if __name__ == "__main__":
    asyncio.run(main())
