#!/usr/bin/env python

from lib.lib_sensors import mhz19
from lib.Adafruit_BME280 import *

if __name__ == '__main__':

        sensor_co2 = mhz19()
        co2_value = sensor_co2.read_co2()
        sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8, address=0x76)

        degrees = sensor.read_temperature()
        pascals = sensor.read_pressure()
        hectopascals = pascals / 100
        humidity = sensor.read_humidity()
        print("===mhz19==")
        print("Co2 result = %s" % co2_value)
        print("===BME280==")
        print('Temp      = {0:0.3f} deg C'.format(degrees))
        print('Pressure  = {0:0.2f} hPa'.format(hectopascals))
        print('Humidity  = {0:0.2f} %'.format(humidity))
