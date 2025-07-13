DEBUG = False
import machine
import time
import json
import struct
import os

# Determine the UART port to use
uart_port = 2
# Initialize UART
uart = machine.UART(uart_port, baudrate=9600, tx=17, rx=16)  # Adjust TX and RX pins as needed

def read_data():
    try:
        if uart.any() > 0:
            data = uart.read()
            if DEBUG:
                print("Data received: ", data)  
            return data
        if DEBUG:
            print("No data received")
        return None
        #return {0,0,0,0,0,0,0,0,0,0,0,0,0}
        #return (b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    except Exception as e:
        print("Error reading data: ", e)
        #return {0,0,0,0,0,0,0,0,0,0,0,0,0}
        #return (b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
        return None

def write_data(data):
    try:
        uart.write(data)
        return True
    except Exception as e:
        print("Error writing data: ", e)
        return False
    
def convert(s):
    if s != None:
        if len(s) >= 9 and s[0] == 0x16 and s[1] == 0x0B:
          return {s[3]*256 + s[4],
                  s[5]*256 + s[6],
                  (s[7]*256 + s[8])*0.1,
                  ((s[9]*256 + s[10])-500)*0.1,
                  s[11]*256 + s[12]
                  }
        else: 
          return {0,0,0,0,0}
           
def read_multisensor_data():
    write_data(b"\x11\x02\x01\x00\xEC")
    z=read_data()
    if z != None:
        if len(z) >= 9 and z[0] == 0x16 and z[1] == 0x0B:
          return (z[3]*256 + z[4],
                  z[5]*256 + z[6],
                  (z[7]*256 + z[8])*0.1,
                  ((z[9]*256 + z[10])-500)*0.1,
                  z[11]*256 + z[12]
          )
        else: 
          return (0,0,0,0,0)


def read_multisensor_param():
    write_data(b"\x11\x02\x01\x00\xEC")
    s=read_data()
    if s != None:    
        if len(s) >= 9 and s[0] == 0x16 and s[1] == 0x0B:
          return {'co2': s[3]*256 + s[4],
                  'voc': s[5]*256 + s[6],
                  'humidity': (s[7]*256 + s[8])*0.1,
                  'temperature': ((s[9]*256 + s[10])-500)*0.1,
                  'pm2.5': s[11]*256 + s[12]
                  }
    #return None

def read_multisensor():
    try:
         (co2,voc,humidity,temp_ms,pm25) =  read_multisensor_data()
    except Exception as e:
        print("Error reading multisensor data: ", e)
        co2 = 0
        voc = 0
        humidity = 0
        temp_ms = 0
        pm25 = 0
    finally:
        return co2, voc, humidity, temp_ms, pm25    