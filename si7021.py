#!/usr/bin/python
# -*- coding: latin-1 -*-

import smbus
bus = smbus.SMBus(1)
address = 0x40

def crc(data):
  rem = 0
  for b in data:
    rem ^= b
    for bit in range(8):
      if rem & 128:
        rem = (rem << 1) ^ 0x31
      else:
        rem = (rem << 1)
  return rem & 0xFF

def readTemperature():
  r = bus.read_i2c_block_data(address,0xE3)
  t_val = (r[0]<<8) + r[1]
  return ((175.72 * t_val)/65536.0) - 46.85

def readHumidity():
  r = bus.read_i2c_block_data(address,0xE5)
  rh_val = (r[0]<<8) + r[1]
  return ((125.0 * rh_val)/65536.0) - 6.0

def main():
  print ("Temperature : " + str(readTemperature()) + " °C")
  print ("Humidity : " + str(readHumidity()) + " %")
   
if __name__=="__main__":
   main()

