DEBUG = False
import time
from machine import SoftI2C, Pin
from bme280 import BME280 

# comunicación I2C
I2C_SCL = 22
I2C_SDA = 21
BME280_ADDR = 118
# BME280_ADDR = 0x76 Utilizar direccion en Hexadecimal dio errores

if DEBUG:
    print("Pines I2C declarados: sclPin = {sclPin}, " \
    "sdaPin = {sdaPin}, BME280_ADDR = {BME280_ADDR}")

# iniciar I2C
i2c = SoftI2C(scl=Pin(I2C_SCL), sda=Pin(I2C_SDA))
if DEBUG:
    print("I2C iniciado...")    

# iniciar BME280
bme280 = BME280(i2c, BME280_ADDR)
if DEBUG:
    print("BME280 iniciado...")

def medir_temperatura_bme():
    try:
        temp = bme280.temperature
        if DEBUG:
            print(f"Temperatura medida: {temp} °C")
        return temp
    except Exception as e:
        print(f"Error al medir temperatura BME280: {e}")
        return None

def medir_humedad_bme():
    try:
        hum = bme280.humidity
        if DEBUG:
            print(f"Humedad medida: {hum} %RH")
        return hum
    except Exception as e:
        print(f"Error al medir humedad BME280: {e}")
        return None

def medir_presion_bme():
    try:
        pres = bme280.pressure / 100  # Convertir a hPa
        if DEBUG:
            print(f"Presión medida: {pres} hPa")
        return pres
    except Exception as e:
        print(f"Error al medir presión BME280: {e}")
        return None
# Fin de la implementación del sensor BME280


# Print temperature, pressure, and humidity
if DEBUG:
    medir_temperatura_bme()
    medir_presion_bme()
    medir_humedad_bme()