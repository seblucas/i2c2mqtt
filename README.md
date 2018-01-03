# i2c2mqtt
Get values from sensors in your i2c bus and send it to your MQTT broker

# Usage

## Prerequisite

You simply need Python3 (never tested with Python2.7) and the only dependencies are `smbus` (to access the i2c) and `paho-mqtt` (for MQTT broker interaction) so this line should be enough  :

```bash
pip3 install paho-mqtt cffi smbus-cffi
```

You may have to also install `libffi-dev` and `python3-dev` because it may need to recompile some stuff. If you're using Debian the you can use `python-smbus`

## Using the script

Easy, first try a dry-run command :

```bash
./i2c2mqtt.py -d <DEVICE> -d <ANOTHER_DEVICE> -n -v
```

For now the device can be :

 * bh1750
 * si7201
 * bme280

PR welcomed to add more.

and then a real command to add to your crontab :

```bash
./netatmo2MQTT.py -d <DEVICE>
```

## Help

```bash
seb@minus~/src/i2c2mqtt# ./i2c2mqtt.py --help
usage: i2c2mqtt.py [-h] [-d DEVICES] [-m HOST] [-n] [-t TOPIC] [-T TOPIC] [-v]

Read current temperature,illuminance and humidity from i2c sensors and send
them to a MQTT broker.

optional arguments:
  -h, --help            show this help message and exit
  -d DEVICES, --device DEVICES
                        Specify the devices to probe in the I2C bus. Can be
                        called many times. (default: None)
  -m HOST, --mqtt-host HOST
                        Specify the MQTT host to connect to. (default:
                        127.0.0.1)
  -n, --dry-run         No data will be sent to the MQTT broker. (default:
                        False)
  -t TOPIC, --topic TOPIC
                        The MQTT topic on which to publish the message (if it
                        was a success). (default: sensor/i2c)
  -T TOPIC, --topic-error TOPIC
                        The MQTT topic on which to publish the message (if it
                        wasn't a success). (default: error/sensor/i2c)
  -v, --verbose         Enable debug messages. (default: False)
```

# Credits

 * bme280.py comes from [this repository](https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/bme280.py)
 * bh1750.py also comes from [this repository](https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/bh1750.py)
 * si7201.py was mostly written by me.

# License

This program is licenced with GNU GENERAL PUBLIC LICENSE version 3 by Free Software Foundation, Inc.