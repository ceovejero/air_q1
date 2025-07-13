DEBUG = False
WIFI = False
RTC = True
OLED = True
DHT22 = True
BME280 = True
MULTISENSOR = True
SD = True
WDTimer = True
NVStorage = False
reset_reason_str = 'None'
#==================Import=========================
import time
if WIFI:
    from lib.net import conectar_wifi  
    from lib.net import obtener_hora_actual
    if DEBUG:
        print("importando lib.net...")
if RTC:
    from lib.rtc import leer_fecha_hora
    if DEBUG:   
        print("importando lib,rtc...")
if OLED:
    from lib.oled_display import mostrar_datos
    if DEBUG:
        print("importando lib.oled_display...")
if DHT22:
    from lib.sensor_dht22 import medir_temperatura, medir_humedad
    if DEBUG:
        print("importando lib.sensor_dht22...")
if BME280:
    from lib.sensor_bme280 import medir_temperatura_bme, medir_humedad_bme, medir_presion_bme
    if DEBUG:
        print("importando lib.sensor_bme280...")
if MULTISENSOR:
    from lib.multisensor import read_multisensor, read_multisensor_param
    import json
    import struct
    if DEBUG:
        print("importando lib.multisensor...")
if SD:
    import os, machine
    from machine import SDCard, Pin
    if DEBUG:
        print("importando lib.sd...")
    os.mount(machine.SDCard(slot=2, width=1, sck=18, cs=5, miso=19, mosi=23), "/sd")
    if DEBUG:
        print("montando SD Card...")
if WDTimer:
    from machine import WDT, reset_cause, DEEPSLEEP_RESET, HARD_RESET, SOFT_RESET, WDT_RESET, PWRON_RESET
    if DEBUG:
        print("importando lib.wdt...")
    wdt = WDT(timeout=10000)
if NVStorage:
    from machine import NVS
    if DEBUG:
        print("importando lib.nvs...")
    

#==================Inicializacion=========================

#==================Conexion WiFi=========================
if WIFI:
    conectar_wifi
    if DEBUG:
        print("conectando a wifi...")   
#==================Preparacion SD Card====================
if SD:
    os.listdir()
    os.chdir("sd")
    os.listdir()
    if DEBUG:
        print("preparando SD Card...")

if WDTimer:
    RESET_CODES = {
                    PWRON_RESET: 'PWRON',
                    HARD_RESET: 'HARD',
                    WDT_RESET: 'WDT',
                    DEEPSLEEP_RESET: 'DEEPSLEEP',
                    SOFT_RESET: 'SOFT',
                    }
    
    # Obtener el motivo del reinicio
    reset_reason = reset_cause()
    reset_reason_str = RESET_CODES.get(reset_reason, 'UNKNOWN')
    # Mostrar el motivo del reinicio por consola
    if DEBUG:
        print("Motivo del reinicio: ", reset_reason_str)
    
if NVStorage:        
    nvs = NVS('storage')
    if reset_cause == 1:
        nvs.set('reset_count', nvs.get('reset_count', 0)+1)
    if DEBUG:
        print("almacenando en NVS...")


while True:
    
    if WDTimer:
        wdt.feed()
        if DEBUG:
            print("reiniciar watchdog timer...")

    if WIFI:
        datos_hora = obtener_hora_actual()
        
    if DHT22:
        dht_temp = medir_temperatura()
        time.sleep(0.5) # Evita errores en la toma de mediciones
        dht_hum = medir_humedad()
        if DEBUG:       
            print("DHT medicion temp hum ok...")
        time.sleep(1)
        if DEBUG:
            if dht_temp is not None:
               print('Temperatura: {}°C'.format(dht_temp))
            if dht_hum is not None:
               print('Humedad: {}%'.format(dht_hum))
    
    if RTC: 
        now = leer_fecha_hora()
        year, month, date, day, hour, minute, second = now
        if DEBUG:
            print("lectura fecha hora ok...")   
            if now is not None:
               print('Hora: {}'.format(now))
    
    if BME280:
        bme_temp = medir_temperatura_bme()
        bme_hum = medir_humedad_bme()
        bme_pres = medir_presion_bme()
        if DEBUG:
            print("medicion BME280 ok...")
            if bme_temp is not None:
                print('Temperatura BME280: {}°C'.format(bme_temp))
            if bme_hum is not None:
                print('Humedad BME280: {}%'.format(bme_hum))
            if bme_pres is not None:
                print('Presión BME280: {} hPa'.format(bme_pres))

    if MULTISENSOR:
        #value = read_multisensor_param()
        (co2,voc,ms_hum,ms_temp,pm25) = read_multisensor()

        if DEBUG:
            print("lectura multisensor ok...")
            #print (json.dumps(value))        


    print('Data Log: {:02d}:{:02d}:{:02d}:{:02d}:{:02d}:{:02d} co2: {} voc: {} PM2.5: {} reset_reason {}'
               .format(year, month, date, hour, minute, second, co2, voc, pm25, reset_reason_str))
    
    print('Data Log: {:02d}:{:02d}:{:02d}:{:02d}:{:02d}:{:02d} bme_temp: {}°C bme_hum: {}% bme_pres: {}hPa'
               .format(year, month, date, hour, minute, second, bme_temp, bme_hum, bme_pres))

    print('Data Log: {:02d}:{:02d}:{:02d}:{:02d}:{:02d}:{:02d} dht_temp: {}°C dht_hum: {}% '
               .format(year, month, date, hour, minute, second, dht_temp, dht_hum))

    print('Data Log: {:02d}:{:02d}:{:02d}:{:02d}:{:02d}:{:02d} Ms_Temp: {}°C Ms_Hum: {}% '
               .format(year, month, date, hour, minute, second, ms_temp, ms_hum))

    
    if OLED:
        mostrar_datos(dht_temp, dht_hum)

    if SD:
        file=open("Datalogger.txt","a")
        file.write ('{:02d},{:02d},{:02d},{:02d},{:02d},{:02d}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n'
               .format(year, month, date, hour, minute, second, dht_temp, dht_hum, bme_temp, bme_hum, bme_pres, ms_temp, ms_hum, co2, pm25, voc, reset_reason_str))
        if DEBUG:
            file.write ('year, month, date, hour, minute, second, dht_temp, dht_hum, bme_temp, bme_hum, bme_pres_hPa, ms_temp, ms_hum, co2, pm25, voc, reset_reason_str\n')
        file.close()
        if DEBUG:
            print("escribiendo en SD Card...")
            
    if WDTimer:
        if reset_reason_str != 'None':
            reset_reason_str = 'None'

    # Esperar 2 segundos antes de la siguiente lectura
    time.sleep(4)        