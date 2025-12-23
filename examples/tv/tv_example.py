"""
SinricPro TV Example

Demonstrates:
- Power control
- Volume control
- Mute control
- Channel control
- Input selection
- Media controls
"""

import asyncio
import os
from typing import TypedDict

from sinricpro import SinricPro, SinricProTV, SinricProConfig

# Device ID from SinricPro portal
DEVICE_ID = "YOUR_DEVICE_ID_HERE"  # Replace with your device ID

# Credentials from SinricPro portal
APP_KEY = os.getenv("SINRICPRO_APP_KEY", "YOUR_APP_KEY_HERE")
APP_SECRET = os.getenv("SINRICPRO_APP_SECRET", "YOUR_APP_SECRET_HERE")


class ChannelInfo(TypedDict, total=False):
    name: str
    number: str


# TV state
tv_state = {
    "power": False,
    "volume": 50,
    "muted": False,
    "channel": {"name": "HBO", "number": "501"},
    "input": "HDMI1",
}


async def on_power_state(state: bool) -> bool:
    """Handle power state changes from SinricPro."""
    print(f"[Power] TV turned {'ON' if state else 'OFF'}")
    tv_state["power"] = state
    return True


async def on_volume(volume: int) -> bool:
    """Handle volume changes from SinricPro."""
    print(f"[Volume] Set to {volume}")
    tv_state["volume"] = volume
    return True


async def on_adjust_volume(volume_delta: int) -> bool:
    """Handle volume adjustments from SinricPro."""
    print(f"[Volume] Adjust by {'+' if volume_delta > 0 else ''}{volume_delta}")
    tv_state["volume"] = max(0, min(100, tv_state["volume"] + volume_delta))
    print(f"  New volume: {tv_state['volume']}")
    return True


async def on_mute(mute: bool) -> bool:
    """Handle mute state changes from SinricPro."""
    print(f"[Mute] {'ON' if mute else 'OFF'}")
    tv_state["muted"] = mute
    return True


async def on_change_channel(channel: ChannelInfo) -> bool:
    """Handle channel changes from SinricPro."""
    channel_name = channel.get("name") or channel.get("number")
    print(f"[Channel] Changed to: {channel_name}")
    tv_state["channel"] = channel
    return True


async def on_skip_channels(count: int) -> bool:
    """Handle channel skip from SinricPro."""
    direction = "forward" if count > 0 else "backward"
    print(f"[Channel] Skip {direction} {abs(count)} channels")
    return True


async def on_select_input(input_name: str) -> bool:
    """Handle input selection from SinricPro."""
    print(f"[Input] Switched to: {input_name}")
    tv_state["input"] = input_name
    return True


async def on_media_control(control: str) -> bool:
    """Handle media control commands from SinricPro."""
    print(f"[Media] {control}")
    return True


async def main() -> None:
    """Main function."""
    print("=" * 60)
    print("SinricPro Smart TV Example")
    print("=" * 60)

    # Create SinricPro instance
    sinric_pro = SinricPro.get_instance()

    # Create TV device
    my_tv = SinricProTV(DEVICE_ID)

    # Register callbacks
    my_tv.on_power_state(on_power_state)
    my_tv.on_volume(on_volume)
    my_tv.on_adjust_volume(on_adjust_volume)
    my_tv.on_mute(on_mute)
    my_tv.on_change_channel(on_change_channel)
    my_tv.on_skip_channels(on_skip_channels)
    my_tv.on_select_input(on_select_input)
    my_tv.on_media_control(on_media_control)

    # Add device to SinricPro
    sinric_pro.add(my_tv)

    # Configure and connect
    config = SinricProConfig(
        app_key=APP_KEY,
        app_secret=APP_SECRET
    )

    try:
        print("Connecting to SinricPro...")
        await sinric_pro.begin(config)
        print("Connected! You can now control your TV via Alexa or Google Home.")
        print()
        print("Try saying:")
        print('  "Alexa, turn on the TV"')
        print('  "Alexa, change channel to HBO"')
        print('  "Alexa, set volume to 50"')
        print('  "Alexa, mute the TV"')
        print('  "Alexa, switch to HDMI 1"')
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
