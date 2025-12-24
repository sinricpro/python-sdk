"""
SinricPro Speaker Example

Demonstrates:
- Power control
- Volume control
- Mute control
- Media playback controls
- Equalizer settings
- Mode selection
"""

import asyncio
import os

from sinricpro import SinricPro, SinricProSpeaker, SinricProConfig

# Device ID from SinricPro portal
DEVICE_ID = "YOUR_DEVICE_ID_HERE"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR_APP_KEY_HERE")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR_APP_SECRET_HERE")

# Speaker state
speaker_state = {
    "power": False,
    "volume": 50,
    "muted": False,
    "mode": "MUSIC",
    "equalizer": {
        "bass": 0,
        "midrange": 0,
        "treble": 0,
    },
}

async def on_power_state(state: bool) -> bool:
    """Handle power state changes from SinricPro."""
    print(f"[Power] Speaker turned {'ON' if state else 'OFF'}")
    speaker_state["power"] = state
    return True


async def on_volume(volume: int) -> bool:
    """Handle volume changes from SinricPro."""
    print(f"[Volume] Set to {volume}")
    speaker_state["volume"] = volume
    return True


async def on_adjust_volume(volume_delta: int) -> bool:
    """Handle volume adjustments from SinricPro."""
    print(f"[Volume] Adjust by {'+' if volume_delta > 0 else ''}{volume_delta}")
    speaker_state["volume"] = max(0, min(100, speaker_state["volume"] + volume_delta))
    print(f"  New volume: {speaker_state['volume']}")
    return True


async def on_mute(mute: bool) -> bool:
    """Handle mute state changes from SinricPro."""
    print(f"[Mute] {'ON' if mute else 'OFF'}")
    speaker_state["muted"] = mute
    return True


async def on_media_control(control: str) -> bool:
    """Handle media control commands from SinricPro."""
    print(f"[Media] {control}")
    # control can be: Play, Pause, Stop, Next, Previous, Rewind, FastForward
    return True


async def on_set_bands(bands: dict) -> bool:
    """Handle equalizer band settings from SinricPro."""
    print(f"[Equalizer] Bands set: {bands}")
    speaker_state["equalizer"].update(bands)
    return True


async def on_adjust_bands(bands: dict) -> bool:
    """Handle equalizer band adjustments from SinricPro."""
    print(f"[Equalizer] Bands adjusted: {bands}")
    for band, delta in bands.items():
        if band in speaker_state["equalizer"]:
            speaker_state["equalizer"][band] += delta
    return True


async def on_mode(mode: str, instance_id: str) -> bool:
    """Handle mode changes from SinricPro."""
    print(f"[Mode] Set to {mode}")
    speaker_state["mode"] = mode
    # Mode can be: MUSIC, MOVIE, NIGHT, SPORT, TV, etc.
    return True


async def main() -> None:
    """Main function."""
    print("=" * 60)
    print("SinricPro Smart Speaker Example")
    print("=" * 60)

    # Create SinricPro instance
    sinric_pro = SinricPro.get_instance()

    # Create speaker device
    my_speaker = SinricProSpeaker(DEVICE_ID)

    # Register callbacks
    my_speaker.on_power_state(on_power_state)
    my_speaker.on_volume(on_volume)
    my_speaker.on_adjust_volume(on_adjust_volume)
    my_speaker.on_mute(on_mute)
    my_speaker.on_media_control(on_media_control)
    my_speaker.on_set_bands(on_set_bands)
    my_speaker.on_adjust_bands(on_adjust_bands)
    my_speaker.on_mode_state(on_mode)

    # Add device to SinricPro
    sinric_pro.add(my_speaker)

    # Configure and connect
    config = SinricProConfig(
        app_key=APP_KEY,
        app_secret=APP_SECRET
    )

    try:
        print("Connecting to SinricPro...")
        await sinric_pro.begin(config)
        print("Connected! You can now control your speaker via Alexa or Google Home.")
        print()
        print("Try saying:")
        print('  "Alexa, turn on the speaker"')
        print('  "Alexa, set volume to 50"')
        print('  "Alexa, mute the speaker"')
        print('  "Alexa, play music"')
        print('  "Alexa, increase bass"')
        print()
        print("Press Ctrl+C to exit")

        # Keep the application running
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await sinric_pro.stop()


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
