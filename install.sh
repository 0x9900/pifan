#!/bin/bash
#
# (c) W6BSD Fred Cirera.
# https://github.com/0x9900/pifan
#

echo 'Installing fan.py'
cp fan.py /usr/local/bin/fan
chmod a+x /usr/local/bin/fan

echo 'Installing the fan service'
cp fan.service /lib/systemd/system/fan.service

echo 'Starting the service'
systemctl enable fan.service
systemctl start fan.service
sleep 2
systemctl status fan.service
