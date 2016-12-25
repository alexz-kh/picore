#!/usr/bin/env python

"""
import os
import requests
import pytz, datetime, time
import struct
import array
from lib_sensors import HTU21D,mhz19
from Adafruit_BME280 import *
from lib_led import my_ws_2812
https://github.com/SergSlipushenko/espinaca/blob/master/mqtt_console/mqtt_console.py
"""

import datetime
import logging as LOG
import os
import pprint
import sys
import time

import yaml
import pytz
import paho.mqtt.client as mqtt

# Vars:
CFG_FILE = 'etc/picore.yaml'

LOG.basicConfig(level=LOG.DEBUG, datefmt='%Y-%m-%d %H:%M:%S',
                format='%(asctime)-15s - [%(levelname)s] %(module)s: '
                       '%(message)s', )


def read_yaml(config_file):
    data = {}
    if os.path.exists(config_file):
        with open(config_file) as f:
            data = yaml.load(f)
            return data
    else:
        LOG.error("The config file couldn't be found: {0}"
                         .format(config_file))
        sys.exit(1)


def get_bright(cfg):
    # Sleeptime
    if cfg.get('sleep', False):
        from_h, from_m = cfg['sleep']['from'].split(':')
        to_h, to_m = cfg['sleep']['to'].split(':')
        now_time = datetime.datetime.now(pytz.timezone(cfg['timezone']))
        datetime.datetime.strptime("16:30", "%H:%M")
        from_time = now_time.replace(hour=int(from_h), minute=int(from_m))
        to_time = now_time.replace(hour=int(to_h), minute=int(to_m))
        if from_time <= now_time <= to_time:
            LOG.info("Sleep time activated")
            return cfg['sleep'].get('night_bright', 0)
    else:
        return cfg.get('default_bright', 128)

####

def get_lux():
    return



def on_message(client, userdata, message):
    LOG.debug(
        "UD:{}\n MSG_toppic:{}\n MSG_payload:{}".format(userdata, message.topic,
                                                        message.payload))


    #if message.topic in self.routes:
        #self.routes[message.topic](message.payload)


def on_connect(client, userdata, rc):
    if rc != 0:
        LOG.error("Connection returned result: %d" % rc)
        sys.exit(1)
    else:
        LOG.info("Mqtt connected")



# Main program logic follows:
if __name__ == '__main__':

        cfg = read_yaml(CFG_FILE)['picorecfg']
        LOG.debug("Loaded config: \n%s", pprint.pformat(cfg))

        led_bright = get_bright(cfg)
        mq = mqtt.Client(client_id=cfg['mqtt'].get('client_id', "mqtt_client"))
        #mq.username_pw_set(user, passwd)

        mq.on_connect = on_connect
        mq.on_message = on_message
        mq.connect(cfg['mqtt']['server'], port=cfg['mqtt']['port'], keepalive=60)
        mq.loop_start()
        mq.subscribe('nodemcu/#')
        import ipdb;ipdb.set_trace()
        #mq.publish('node/%s/stdin' % node, ' ')

        while True:
            # inp = raw_input()
            #mq.publish('nodemcu/picore' , "z")
            time.sleep(1)





        sys.exit(0)
        lstrip = my_ws_2812(BRIGHTNESS=led_bright)
        sensor_ht = BME280(mode=BME280_OSAMPLE_8, address=0x76)
        sensor_co2 = mhz19()
        c_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        co2_value = sensor_co2.read_co2()

        t_value = sensor_ht.read_temperature()
        pascals = sensor_ht.read_pressure()
        hectopascals_value = pascals / 100
        # convert to millimeter of mercury
        pressure_value = hectopascals_value * 0.750064
        humid_value = sensor_ht.read_humidity()

        print "{} \nCo2:{}. Temp:{}. Humidity:{}. Pressure:{}\n".format(c_time, co2_value, t_value, humid_value, pressure_value)

        # since co2_value could be None, we should skip whole string for thingspeak:
        co2_ts_string = "&field1={}".format(co2_value)
        if co2_value is None:
            co2_ts_string = None
        # import ipdb;ipdb.set_trace()
        lstrip.to_level(co2_value)
        thingspeak_key = os.environ.get("THINGSPEAK_KEY")
        requests.get('https://api.thingspeak.com/update?api_key={}{}&field2={}&field3={}&field4={}'.format(thingspeak_key,co2_ts_string,t_value,humid_value,pressure_value))
