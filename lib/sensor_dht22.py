import machine
import dht

# Configurar pin de conexion DHT22
dht_pin = machine.Pin(14)
sensor = dht.DHT22(dht_pin)

def medir_temperatura():
    try:
        sensor.measure()
        return sensor.temperature()
    except OSError as e:
        print('Error al leer la temperatura DHT:', e)
        return 0


def medir_humedad():
    try:
        sensor.measure()
        return sensor.humidity()
    except OSError as e:
        print('Error al leer la humedad DHT:', e)
        return 0
    
    