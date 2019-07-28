#!/usr/bin/python
#
# (c) W6BSD Fred Cirera
# https://github.com/0x9900/pifan
#

import atexit
import logging
import time

import RPi.GPIO as io

TEMPFILE = "/sys/class/thermal/thermal_zone0/temp"
THRESHOLD = 42.0
FAN_PIN = 26
SLEEP = 31

io.setmode(io.BCM)

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%H:%M:%S', level=logging.INFO)

class Fan(object):
  def __init__(self, pin=FAN_PIN):
    self._pin = pin
    io.setup(self._pin, io.OUT, initial=io.LOW)
    logging.info('GPIO pin(%s) configured', self._pin)

  def on(self):
    if io.input(self._pin) is io.HIGH:
      return
    io.output(self._pin, io.HIGH)
    logging.debug('Fan(%d) -> ON', self._pin)

  def off(self):
    if io.input(self._pin) is io.LOW:
      return
    io.output(self._pin, io.LOW)
    logging.debug('Fan(%d) -> OFF', self._pin)

  def cleanup(self):
    logging.info('cleanup')
    io.cleanup()

def get_temp():
  try:
    with open(TEMPFILE, "r") as tempfd:
      rawtemp = tempfd.readline().strip()
  except IOError as err:
    logging.error(err)
    return 0

  temp = float(rawtemp) / 1000
  logging.debug("Temperature: %.2f", temp)
  return temp

def main():
  fan = Fan(FAN_PIN)
  atexit.register(fan.cleanup)

  while True:
    if get_temp() > THRESHOLD:
      fan.on()
    else:
      fan.off()
    time.sleep(SLEEP)

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    logging.critical('Interrupted by user')
