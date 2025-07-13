DEBUG = True
import machine
# impport the required libraries
from machine import I2C, Pin
from ds1307 import DS1307
import utime

# declarar pines para comunicación I2C
sclPin = Pin(22) # serial clock pin
sdaPin = Pin(21) # serial data pin
if DEBUG:
    print("Pines I2C declarados: sclPin = {sclPin}, sdaPin = {sdaPin}")

# Initiate I2C 
i2c_object = I2C(0,              # argumento posicional - I2C id
                  scl = sclPin,  # argumento con nombre - serial clock pin
                  sda = sdaPin,  # argumento con nombre - serial data pin
                  freq = 400000 )# argumento con nombre - frecuencia i2c 
if DEBUG:
    print("I2C iniciado...")

# clock object at the dedicated i2c port
rtc = DS1307(i2c_object)
if DEBUG:
    print("RTC iniciado...")

def leer_fecha_hora():
        try:
            (year,month,date,day,hour,minute,second,p1)=rtc.datetime()  
            #year, month, date, day, hour, minute, second = now
            #return year, month, date, day, hour, minute, second
        except Exception as e:
            print(f"Error al leer fecha y hora - {e}")
            year = 0
            month = 0
            date = 0
            day = 0
            hour = 0
            minute = 0
            second = 0
        finally:        
            return year, month, date, day, hour, minute, second

#print(rtc.datetime())
#print("probando func...")
#ver = leer_fecha_hora()
#print("func ok...")
#print(ver)