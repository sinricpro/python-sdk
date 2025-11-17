"""SinricPro Smart Lock Example - Lock/unlock control."""
import asyncio
import os

from sinricpro import SinricPro, SinricProLock, SinricProConfig

# Device ID from SinricPro portal
DEVICE_ID = "YOUR_DEVICE_ID_HERE"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR_APP_KEY_HERE")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR_APP_SECRET_HERE")

async def on_lock_state(locked: bool) -> bool:
    """Handle lock/unlock requests."""
    if locked:
        print("🔒 Locking door...")
        # TODO: Activate lock mechanism
        # - Control solenoid lock
        # - Rotate servo to lock position
        # - Send signal to electronic lock
    else:
        print("🔓 Unlocking door...")
        # TODO: Deactivate lock mechanism
        # - Release solenoid
        # - Rotate servo to unlock position
        # - Send unlock signal

    print(f"Lock is now: {'LOCKED' if locked else 'UNLOCKED'}")
    return True

async def main() -> None:
    sinric_pro = SinricPro.get_instance()
    lock = SinricProLock(DEVICE_ID)
    lock.on_lock_state(on_lock_state)
    sinric_pro.add(lock)

    config = SinricProConfig(app_key=APP_KEY, app_secret=APP_SECRET)

    try:
        print("Connecting to SinricPro...")
        await sinric_pro.begin(config)
        print("Connected! Smart lock is ready.")
        print("\nVoice commands:")
        print("  - 'Alexa, lock [device name]'")
        print("  - 'Alexa, unlock [device name]'")
        print("\nPress Ctrl+C to exit")

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
