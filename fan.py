#!/usr/bin/python3
#
# (c) W6BSD Fred Cirera
# https://github.com/0x9900/pifan
#

import asyncio
import atexit
import logging
import os
import signal
import sys
import time

from configparser import ConfigParser
from functools import partial
from io import StringIO

import RPi.GPIO as io


io.setmode(io.BCM)

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%H:%M:%S', level=logging.INFO)


CONFIG_FILE = "/etc/fan.conf"
CONFIG_DEFAULT = u"""
[FAN]
thermal_file: /sys/class/thermal/thermal_zone0/temp
pin: 26
sleep: 31
threshold: 42.0
"""

def Config():
  parser = ConfigParser()
  parser.readfp(StringIO(CONFIG_DEFAULT))

  if not os.path.exists(CONFIG_FILE):
    logging.info('Using default config')
    return parser

  try:
    logging.info('Reading config file')
    with open(CONFIG_FILE, 'r') as fdc:
      parser.readfp(fdc)
    logging.info('Config file %s read', CONFIG_FILE)
  except (IOError, SystemError):
    raise SystemError('No [vault] section configured')
  return parser

class Fan(object):
  """Manages the fan. This class initialise the GPIO pin and provide the
  methods to turn on and off the fan"""

  def __init__(self, pin):
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

  async def run(self, config):
    get_temp = partial(read_temp, config.get('FAN', 'thermal_file'))
    while True:
      if get_temp() > config.getfloat('FAN', 'threshold'):
        self.on()
      else:
        self.off()
      await asyncio.sleep(config.getint('FAN', 'sleep'))

  @staticmethod
  def cleanup():
    logging.info('cleanup')
    io.cleanup()

def read_temp(tempfile):
  try:
    with open(tempfile, "r") as tempfd:
      rawtemp = tempfd.readline().strip()
  except IOError as err:
    logging.error(err)
    return 0

  temp = float(rawtemp) / 1000
  logging.debug("Temperature: %.2f", temp)
  return temp

def set_loglevel():
  log_level = os.getenv('LOGLEVEL')
  if not log_level:
    return

  logger = logging.getLogger()
  try:
    level = logging._checkLevel(log_level.upper())
  except ValueError as err:
    logging.error(err)
  else:
    logger.setLevel(level)

def sig_handler(sig, frame):
  logging.critical('Signal: %d caught', sig)
  sys.exit(0)

async def log_temperature(config):
  get_temp = partial(read_temp, config.get('FAN', 'thermal_file'))
  while True:
    logging.info("CPU temperature %.3f", get_temp())
    await asyncio.sleep(907)

def main():
  set_loglevel()
  config = Config()

  fan = Fan(config.getint('FAN', 'pin'))

  atexit.register(fan.cleanup)
  signal.signal(signal.SIGQUIT, sig_handler)
  signal.signal(signal.SIGTERM, sig_handler)

  loop = asyncio.get_event_loop()
  loop.create_task(log_temperature(config))
  loop.create_task(fan.run(config))
  try:
    loop.run_forever()
  except KeyboardInterrupt:
    logging.info('Program interrupted')

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    logging.critical('Interrupted by user')
