#!/usr/bin/env python

import os
import requests
import pytz, datetime, time
import struct
import array
from lib.lib_sensors import mhz19
#from lib_sensors import HTU21D,mhz19
from lib.Adafruit_BME280 import *
#from lib_led import my_ws_2812

# Main program logic follows:
if __name__ == '__main__':

        tz = pytz.timezone('Europe/Kiev')
#        # Sleeptime
#        timed_bright=1
#        now_h = (datetime.datetime.now()).hour
#        if now_h >= 8 and now_h <= 23:
#           timed_bright=15
#        lstrip = my_ws_2812(BRIGHTNESS=timed_bright)
#        c_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        sensor_co2 = mhz19()
        co2_value = sensor_co2.read_co2()
        print("Result:%s" % co2_value)

        sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8, address=0x76)
        
        degrees = sensor.read_temperature()
        pascals = sensor.read_pressure()
        hectopascals = pascals / 100
        humidity = sensor.read_humidity()
        
        print 'Temp      = {0:0.3f} deg C'.format(degrees)
        print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)
        print 'Humidity  = {0:0.2f} %'.format(humidity)

#
#        t_value = sensor_ht.read_temperature()
#        pascals = sensor_ht.read_pressure()
#        hectopascals_value = pascals / 100
#        # convert to millimeter of mercury
#        pressure_value = hectopascals_value * 0.750064
#        humid_value = sensor_ht.read_humidity()
#
#        print "{} \nCo2:{}. Temp:{}. Humidity:{}. Pressure:{}\n".format(c_time, co2_value, t_value, humid_value, pressure_value)
#
#        # since co2_value could be None, we should skip whole string for thingspeak:
#        co2_ts_string = "&field1={}".format(co2_value)
#        if co2_value is None:
#            co2_ts_string = None
#        # import ipdb;ipdb.set_trace()
#        lstrip.to_level(co2_value)
#        thingspeak_key = os.environ.get("THINGSPEAK_KEY")
#        requests.get('https://api.thingspeak.com/update?api_key={}{}&field2={}&field3={}&field4={}'.format(thingspeak_key,co2_ts_string,t_value,humid_value,pressure_value))
