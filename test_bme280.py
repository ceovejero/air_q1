from machine import SoftI2C, Pin
from lib.bme280 import BME280

# Initialize the I2C bus and BME280 sensor
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
bme_sensor = BME280(i2c)

try:
  # Read sensor data
  bme_sensor.read()

  # Print temperature, pressure, and humidity
  print(f"{bme_sensor.temperature} °C")
  print(f"{bme_sensor.pressure/100} hPa")
  print(f"{bme_sensor.humidity} %RH")

except Exception as e:
  print(f"An error occurred: {e}")
