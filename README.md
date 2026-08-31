# SinricPro Python SDK

Official Python SDK for [SinricPro](https://sinric.pro) - Control your IoT devices with Alexa and Google Home.

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-CC%20BY--SA%204.0-green.svg)](LICENSE)

## Features

- ✅ **Easy to Use** - Simple, pythonic API with async/await support
- ✅ **Type Safe** - Full type hints for better IDE support and error detection
- ✅ **Voice Control** - Works with Alexa and Google Home
- ✅ **Real-time** - WebSocket-based bidirectional communication
- ✅ **Local Control** - Keeps answering the app over the LAN when the cloud is unreachable
- ✅ **Secure** - HMAC-SHA256 message signatures
- ✅ **Reliable** - Auto-reconnection and heartbeat monitoring
- ✅ **Flexible** - Support for multiple device types and capabilities
- ✅ **Cross-Platform** - Works on Linux, Windows, macOS, and Raspberry Pi

## Supported Devices

**Lighting & Switches:**
- Smart Switch - On/Off control
- Smart Light - RGB color, brightness, color temperature
- Dimmable Switch - On/Off with brightness control

**Sensors:**
- Motion Sensor - Detect movement
- Contact Sensor - Door/window open/closed detection
- Temperature Sensor - Temperature and humidity monitoring
- Air Quality Sensor - PM1.0, PM2.5, PM10 measurements
- Power Sensor - Voltage, current, power monitoring

**Control Devices:**
- Blinds - Position control (0-100%)
- Garage Door - Open/close control
- Smart Lock - Lock/unlock control

**Climate Control:**
- Thermostat - Temperature control with modes (AUTO, COOL, HEAT, ECO)
- Window AC - Air conditioning control

**Other Devices:**
- Fan - On/Off control
- Doorbell - Doorbell press events

## Installation

```bash
pip install sinricpro
```
 
Local control announces the device over mDNS so the app can discover it on the LAN.
The announcement uses `zeroconf`, installed with the SDK:

```bash
pip install sinricpro
```

## Requirements

- Python 3.10 or higher
- `websockets` library (automatically installed)
- `zeroconf` - the mDNS announcement used by local control

## Platform Support

The SDK works on:

- **Linux** (Ubuntu, Debian, Raspberry Pi OS, etc.)
- **Windows** 10/11
- **macOS** 10.14+
- **Raspberry Pi** (All models with Python 3.10+)

## Local Control

Devices answer signed commands over the LAN as well as through the cloud, so they
keep responding to the app when sinric.pro is unreachable. It is on by default and
needs no code change - a LAN request runs the same capability callbacks a cloud
request does. UDP listener on port `3333`, joined to multicast group `224.9.9.9` and answering unicast on the same port. Replies go back to the peer that sent the request, never to the cloud websocket.

## Logging

Enable debug logging to see detailed information:

```python
from sinricpro import SinricProLogger, LogLevel

# Set log level
SinricProLogger.set_level(LogLevel.DEBUG)
```

Available log levels: `DEBUG`, `INFO`, `WARN`, `ERROR`, `NONE`
 

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/sinricpro/python-sdk.git
cd python-sdk

# Install development dependencies
pip install -e ".[dev]"

# Import sinricpro for development.
```python
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sinricpro import SinricPro, SinricProAirQualitySensor, SinricProConfig
```

# Run tests
pytest

# Format code
black .

# Type check
mypy sinricpro

### Running Examples

```bash
# Set environment variables
export SINRICPRO_APP_KEY="your-app-key"
export SINRICPRO_APP_SECRET="your-app-secret"

# Run an example
python examples/switch/switch_example.py
```

## API Reference

Full API documentation is available at [Read the Docs](https://sinricpro-python.readthedocs.io) (Coming soon!)

## Troubleshooting

### Connection Issues

1. **Check credentials** - Ensure APP_KEY and APP_SECRET are correct
2. **Check device ID** - Verify the device ID is exactly 24 hexadecimal characters
3. **Check network** - Ensure you have internet connectivity
4. **Enable debug logging** - Set `debug=True` in config to see detailed logs

### Local Control Issues

1. **No device found on the LAN** - check the log for
   `Local control listening on UDP 3333`. A failed multicast join leaves nothing
   listening, and the log line says so.
2. **No mDNS record** - confirm `zeroconf` imported cleanly; the SDK logs a warning and falls back to UDP-only when it did not.
3. **Discovery answers on the wrong network** - set `local_control_interface` to the
   LAN address of the host.
4. **Android clients need a `WifiManager.MulticastLock`**, and iOS clients need
   `_sinricpro._udp` listed in `NSBonjourServices`, or discovery returns nothing.

### Common Errors

**"Invalid app_key format"**
- App key must be a valid UUID (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)

**"Invalid app_secret: must be at least 32 characters"**
- App secret must be at least 32 characters long

**"Invalid device_id format"**
- Device ID must be exactly 24 hexadecimal characters

 
## Support

- **Documentation**: [help.sinric.pro](https://help.sinric.pro)
- **Community**: [Discord](https://discord.gg/W5299EgB59)
- **Issues**: [GitHub Issues](https://github.com/sinricpro/python-sdk/issues)
- **Email**: support@sinric.pro

## License

Copyright (c) 2019-2025 Sinric. All rights reserved.

This project is licensed under the Creative Commons Attribution-Share Alike 4.0 International License (CC BY-SA 4.0) - see the [LICENSE](LICENSE) file for details.

You are free to share and adapt this work for any purpose (including commercially), as long as you give appropriate credit and distribute your contributions under the same license.

## Acknowledgments

- Based on the official [SinricPro C++ SDK](https://github.com/sinricpro/esp8266-esp32-sdk)
- Inspired by the [SinricPro Node.js SDK](https://github.com/sinricpro/nodejs-sdk)

## Related Projects

- [SinricPro ESP8266/ESP32 SDK](https://github.com/sinricpro/esp8266-esp32-sdk)
- [SinricPro Node.js SDK](https://github.com/sinricpro/nodejs-sdk)
- [SinricPro Documentation](https://github.com/sinricpro/help-docs)

---

## Vibe Coding

If you are to develop agent via vibe coding the llms.txt and the llms-full.txt can be used as context to LLM. While the former one is a summarized one and the later one has the full information in case your LLM has big enough context window.

Made with ❤️ by the SinricPro Team
