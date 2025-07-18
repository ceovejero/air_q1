from machine import Pin, I2C 
import ssd1306

# Configurar I2C
i2c = I2C(0,
           scl=Pin(22), 
           sda=Pin(21) )

# Inicializar la pantalla OLED
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def mostrar_datos(temp, hum):
    try:
        oled.fill(0)  # Limpiar la pantalla
        oled.text('Temp: {}C'.format(temp), 0, 0)
        oled.text('Hum: {}%'.format(hum), 0, 21)
        oled.show()
    except Exception as e:
        print('Error al mostrar datos en la pantalla OLED:', e)
        pass
    