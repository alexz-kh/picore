#!/usr/bin/env python

import os,requests
from lib.lib_sensors import mhz19,HTU21D
from lib.Adafruit_BME280 import *

if __name__ == '__main__':

  sensor_co2 = mhz19()
  co2_value = sensor_co2.read_co2()
  sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8, address=0x76)

  sensor_ht = HTU21D()
  degrees1 = sensor_ht.read_temperature()
  humidity = sensor_ht.read_humidity()
  print("===htu21d==")
  print("Temp: %s C" % degrees1)
  print("Humid: %s %% rH" % humidity)

  degrees2 = sensor.read_temperature()
  pascals = sensor.read_pressure()
  hectopascals = pascals / 100
  mmHg = hectopascals * 0.75
#  humidity = sensor.read_humidity()
  print("===BMP280==")
  print('Temp      = {0:0.3f} deg C'.format(degrees2))
  print('Pressure  = {0:0.2f} hPa'.format(hectopascals))

  degrees = (degrees1 + degrees2) / 2
  print("==Result===")
  print("Co2       = %s" % co2_value)
  print('Temp      = {0:0.3f} deg C'.format(degrees))
  print('Humidity  = {0:0.2f} %'.format(humidity))
  print('Pressure  = {0:0.2f} mmHg'.format(mmHg))

  # since co2_value could be None, we should skip whole string for thingspeak:
  co2_ts_string = "&field1={}".format(co2_value)
  if co2_value is None:
    co2_ts_string = None
  # import ipdb;ipdb.set_trace()
  thingspeak_key = os.environ.get("THINGSPEAK_KEY","B40EVCJK06UWGMMM")
  requests.get('https://api.thingspeak.com/update?api_key={}{}&field2={}&field3={}&field4={}'.format(thingspeak_key,co2_ts_string,degrees,humidity,mmHg))

