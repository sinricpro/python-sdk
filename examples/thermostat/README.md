# Thermostat Example

Smart thermostat control with temperature monitoring and multiple modes.

## Features

- **Thermostat Modes:** AUTO, COOL, HEAT, ECO, OFF
- **Target Temperature:** Set desired temperature
- **Temperature Monitoring:** Send current temperature/humidity readings
- **Voice Control:** Full Alexa integration

## Hardware Requirements

**Minimum:**
- Temperature sensor (DHT22, BME280, etc.)
- Relay module for HVAC control
- Raspberry Pi or similar

**Complete Setup:**
- Temperature/humidity sensor
- 2 relays (heating + cooling) or
- 4 relays (heat, cool, fan, reversing valve)
- Optional: Fan control relay

## Wiring Example

```
DHT22 → GPIO 4
Heating Relay → GPIO 17
Cooling Relay → GPIO 27
Fan Relay → GPIO 22
```

## Installation

```bash
pip install websockets
pip install adafruit-circuitpython-dht
pip install RPi.GPIO
```

## Basic HVAC Control

```python
import RPi.GPIO as GPIO

HEAT_PIN = 17
COOL_PIN = 27
FAN_PIN = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(HEAT_PIN, GPIO.OUT)
GPIO.setup(COOL_PIN, GPIO.OUT)
GPIO.setup(FAN_PIN, GPIO.OUT)

async def on_thermostat_mode(mode: str) -> bool:
    # Turn everything off first
    GPIO.output(HEAT_PIN, GPIO.LOW)
    GPIO.output(COOL_PIN, GPIO.LOW)
    GPIO.output(FAN_PIN, GPIO.LOW)

    if mode == "HEAT":
        GPIO.output(HEAT_PIN, GPIO.HIGH)
        GPIO.output(FAN_PIN, GPIO.HIGH)
    elif mode == "COOL":
        GPIO.output(COOL_PIN, GPIO.HIGH)
        GPIO.output(FAN_PIN, GPIO.HIGH)
    elif mode == "AUTO":
        # AUTO mode: you control based on temp difference
        GPIO.output(FAN_PIN, GPIO.HIGH)
    # OFF mode: everything stays off

    return True
```

## Temperature Control Logic

```python
async def monitor_and_control(thermostat):
    while True:
        current_temp = read_temperature()

        if mode == "AUTO":
            if current_temp > target_temp + 1:
                # Start cooling
                GPIO.output(COOL_PIN, GPIO.HIGH)
                GPIO.output(HEAT_PIN, GPIO.LOW)
            elif current_temp < target_temp - 1:
                # Start heating
                GPIO.output(HEAT_PIN, GPIO.HIGH)
                GPIO.output(COOL_PIN, GPIO.LOW)
            else:
                # Within range, turn off
                GPIO.output(HEAT_PIN, GPIO.LOW)
                GPIO.output(COOL_PIN, GPIO.LOW)

        # Send current temperature to SinricPro
        humidity = read_humidity()
        await thermostat.send_temperature_event(current_temp, humidity)

        await asyncio.sleep(60)
```

## Voice Commands

**Set Mode:**
- "Alexa, set [device name] to cool"
- "Alexa, set [device name] to heat"
- "Alexa, set [device name] to auto"
- "Alexa, turn off [device name]"

**Set Temperature:**
- "Alexa, set [device name] to 22 degrees"
- "Alexa, make [device name] warmer"
- "Alexa, make [device name] cooler"

**Check Status:**
- "Alexa, what's the temperature in [device name]?"

## Safety Features

Add these safety features:

```python
# Temperature limits
MIN_TEMP = 10.0  # Don't cool below this
MAX_TEMP = 32.0  # Don't heat above this

# Compressor protection (prevent rapid cycling)
last_mode_change = 0
MIN_CYCLE_TIME = 300  # 5 minutes between mode changes

async def on_thermostat_mode(mode: str) -> bool:
    global last_mode_change

    # Check minimum cycle time
    if time.time() - last_mode_change < MIN_CYCLE_TIME:
        print("Waiting for compressor protection...")
        return False

    # Apply mode change
    last_mode_change = time.time()
    return True

# Temperature validation
async def on_target_temperature(temp: float) -> bool:
    if temp < MIN_TEMP or temp > MAX_TEMP:
        print(f"Temperature out of range: {temp}")
        return False
    return True
```

## Advanced Features

**Schedule:**
- Auto mode changes based on time
- Energy-saving modes at night
- Vacation mode

**Smart Features:**
- Adaptive learning
- Weather integration
- Occupancy detection

**Monitoring:**
- Energy usage tracking
- Runtime statistics
- Maintenance alerts

## Testing

Test mode changes without hardware:

```bash
python thermostat_example.py
```

The example includes simulation mode that shows:
- Temperature changes based on mode
- Target vs actual temperature
- Mode transitions

## Production Considerations

1. **Safety:** Add temperature limits and cycle protection
2. **Efficiency:** Implement deadband (e.g., ±1°C)
3. **Reliability:** Add failsafe defaults
4. **Monitoring:** Log all mode changes and temperatures
5. **Backup:** Manual override controls
