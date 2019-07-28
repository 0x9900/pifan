# Pi Fan

I build "embedded" systems based on the Raspberry Pi. For heat
dissipation these systems have a fan. This little program check the
temperature of the Raspberry Pi and turn on a fan connected on a GPIO
port.

Here is an example of such system: [AllStar Node](http://0x9900.com/mobile-allstar-node/)

## Dependencies

The program `fan` does not require any dependencies beside the
RPi.GPIO library to access the GPIO pins on your board. If you are
using an image made for the Raspberry Pi it comes pre-installed. In
case you still need to install it here are the instructions.

First you need to update the available package versions:

```
sudo apt-get update
```

Then install the RPi.GPIO package:

```
sudo apt-get install rpi.gpio
```

If it is already installed it will be upgraded if a newer version is
available. If it is not already installed it will be installed.

## Installation

To install the program `fan` and the service just run the install
script.

```
sudo install.sh
```

This will install and run the service. The next time you boot your
system, the fan service will be automatically started.


## Manual installation

To install the program `fan` just copy the file `fan.py` from this
directory to `/usr/local/bin/fan`. Then make sure that file is
executable.

```
sudo cp fan.py /usr/local/bin/fan
sudo chmod a+x /usr/local/bin/fan
```

## Running

To start `fan` at boot time. You need to install the fan service. Copy
the file `fan.service` into the directory `/lib/systemd/system`, then
inform `systemd` that it needs to run that service.

```
systemctl enable fan.service

```

## Example

```
07:29:46 WARNING: Temperature: 41.86
07:29:46 INFO: Fan(26) -> OFF
07:30:17 WARNING: Temperature: 41.86
07:30:48 WARNING: Temperature: 42.93
07:30:48 INFO: Fan(26) -> ON
07:31:19 WARNING: Temperature: 42.93
07:31:50 WARNING: Temperature: 42.39
07:32:21 WARNING: Temperature: 41.86
07:32:21 INFO: Fan(26) -> OFF
07:32:52 WARNING: Temperature: 41.86
07:33:23 WARNING: Temperature: 42.39
07:33:23 INFO: Fan(26) -> ON
07:33:54 WARNING: Temperature: 41.86
07:33:54 INFO: Fan(26) -> OFF
07:34:25 WARNING: Temperature: 42.93
07:34:25 INFO: Fan(26) -> ON
07:34:56 WARNING: Temperature: 41.86
07:34:56 INFO: Fan(26) -> OFF
07:35:28 WARNING: Temperature: 42.39
07:35:28 INFO: Fan(26) -> ON
07:35:59 WARNING: Temperature: 42.93
07:36:30 WARNING: Temperature: 41.86
07:36:30 INFO: Fan(26) -> OFF
```
