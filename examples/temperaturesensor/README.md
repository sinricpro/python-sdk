# Temperature Sensor Example

Monitor temperature and humidity with SinricPro.

## Supported Sensors

- DHT11 / DHT22 / DHT21
- BME280 / BMP280
- SHT31 / SHT35
- AHT10 / AHT20
- DS18B20 (temperature only)

## Hardware Setup

### DHT22 Example
```
DHT22 Sensor:
  VCC → 3.3V
  GND → GND
  DATA → GPIO 4 (with 10kΩ pull-up resistor)
```

### BME280 Example (I2C)
```
BME280 Sensor:
  VCC → 3.3V
  GND → GND
  SDA → GPIO 2 (SDA)
  SCL → GPIO 3 (SCL)
```

## Installation

```bash
pip install websockets

# For DHT sensors:
pip install adafruit-circuitpython-dht

# For BME280 (I2C):
pip install adafruit-circuitpython-bme280
```

## Real Hardware Integration

### DHT22 Example
```python
import board
import adafruit_dht

# Initialize DHT22
dht_device = adafruit_dht.DHT22(board.D4)

async def read_dht22(sensor: SinricProTemperatureSensor) -> None:
    """Read DHT22 and send events."""
    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity

            if temperature is not None and humidity is not None:
                print(f"Temp: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
                await sensor.send_temperature_event(temperature, humidity)

        except RuntimeError as e:
            print(f"Reading failed: {e}")

        await asyncio.sleep(60)  # Read every 60 seconds
```

### BME280 Example
```python
import board
import adafruit_bme280

# Initialize BME280
i2c = board.I2C()
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

async def read_bme280(sensor: SinricProTemperatureSensor) -> None:
    """Read BME280 and send events."""
    while True:
        temperature = bme280.temperature
        humidity = bme280.humidity

        print(f"Temp: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
        await sensor.send_temperature_event(temperature, humidity)

        await asyncio.sleep(60)
```

## Voice Commands

Once connected, ask Alexa:
- "Alexa, what's the temperature in [device name]?"
- "Alexa, what's the humidity in [device name]?"

Check in the Alexa app for historical data and charts.

## Important Notes

- **Rate Limiting**: Temperature sensors have a 60-second rate limit
- **Accuracy**: DHT22 ±0.5°C temperature, ±2% humidity
- **Power**: DHT sensors need 2-3 seconds between readings
- **I2C**: BME280 provides better accuracy and also measures pressure
