#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#
#  i2c2mqtt.py
#
#  Copyright 2016 Sébastien Lucas <sebastien@slucas.fr>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
#

import bh1750
import bme280
import si7201
import time, json, argparse
import paho.mqtt.publish as publish # pip install paho-mqtt

verbose = False

def debug(msg):
  if verbose:
    print (msg + "\n")

def getI2cSensors(devices):
  tstamp = int(time.time())

  newObject = {"time": tstamp}

  if not isinstance(devices, list):
    newObject['message'] = 'No devices specified.'
    return (False, newObject)

  if 'bh1750' in devices:
    ###### Get luminosity ##
    lux = bh1750.readLight()
    # Drop the first (usually bad)
    lux = bh1750.readLight()
    newObject['lum'] = int (lux)
    debug ("Light Level : " + str(newObject['lum']) + " lx")

  if 'si7201' in devices:
    ###### Get temperature & humidity from si7201 ##
    T = si7201.readTemperature()
    newObject['temp'] = round (T, 1)
    RH = si7201.readHumidity()
    newObject['hum'] = int (RH)
    debug ("Temperature : " + str(newObject['temp']) + " °C")
    debug ("Humidity : " + str(newObject['hum']) + " %")

  if 'bme280' in devices:
    ###### Get temperature, pressure & humidity from bme280 ##
    T, P, RH = bme280.readBME280All()
    newObject['temp'] = round (T, 1)
    newObject['hum'] = int (RH)
    newObject['pres'] = int(P)
    debug ("Temperature : " + str(newObject['temp']) + " °C")
    debug ("Humidity : " + str(newObject['hum']) + " %")
    debug ("Pressure : " + str(newObject['pres']) + " hPa")

  return (True, newObject)

parser = argparse.ArgumentParser(description='Read current temperature,illuminance and humidity from i2c sensors and send them to a MQTT broker.',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-d', '--device', dest='devices', action="append",
                   help='Specify the devices to probe in the I2C bus. Can be called many times.')
parser.add_argument('-m', '--mqtt-host', dest='host', action="store", default="127.0.0.1",
                   help='Specify the MQTT host to connect to.')
parser.add_argument('-n', '--dry-run', dest='dryRun', action="store_true", default=False,
                   help='No data will be sent to the MQTT broker.')
parser.add_argument('-t', '--topic', dest='topic', action="store", default="sensor/i2c",
                   help='The MQTT topic on which to publish the message (if it was a success).')
parser.add_argument('-T', '--topic-error', dest='topicError', action="store", default="error/sensor/i2c", metavar="TOPIC",
                   help='The MQTT topic on which to publish the message (if it wasn\'t a success).')
parser.add_argument('-v', '--verbose', dest='verbose', action="store_true", default=False,
                   help='Enable debug messages.')

args = parser.parse_args()
verbose = args.verbose;

status, data = getI2cSensors(args.devices)
jsonString = json.dumps(data)
if status:
  debug("Success with message (for current readings) <{0}>".format(jsonString))
  if not args.dryRun:
    publish.single(args.topic, jsonString, hostname=args.host)
else:
  debug("Failure with message <{0}>".format(jsonString))
  if not args.dryRun:
    publish.single(args.topicError, jsonString, hostname=args.host)
