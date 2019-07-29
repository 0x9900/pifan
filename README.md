# Pi Fan

I build "embedded" systems based on the Raspberry Pi. For heat
dissipation, these systems have a fan. This little program checks the
temperature of the Raspberry Pi and turns on a fan connected on a GPIO
port.

Here is an example of such a system: [AllStar Node](http://0x9900.com/mobile-allstar-node/)
I am also using this program for the ParachuteMobile [APRS iGate](http://0x9900.com/aprs-igate-for-parachute-mobile/).
You can also check that my [blog](http://0x9900.com/keeping-your-allstar-node-cool/) on this little project.


## Dependencies

The program `fan` does not require any dependencies besides the
RPi.GPIO library to access the GPIO pins on your board. If you are
using an image made for the Raspberry Pi it comes pre-installed. In
case you still need to install it here are the instructions.

### Installing the GPIO library on any Debian based distro

First, you need to update the available package versions:

```
 $ sudo apt-get update
```

Then install the RPi.GPIO package:

```
 $ sudo apt-get install rpi.gpio
```

If it is already installed it will be upgraded if a newer version is
available. If it is not already installed it will be installed.

### GPIO Library installation on Allstar distro from hamvoip

The Allstar distribution built by hamvoip doesn't provide the GPIO
library. Also, at the time I am writing these lines hamvoip uses an
older ArchLinux distro with an old GPIO library. Therefore the best
way to have GPIO library in good working condition is to install it
from the sources. Don't worry, it is not that hard.

The version of the GPIO library used in the following lines is the
version 0.7.0. In your installation, you should use the latest
version.

From your shell, prompt here are the command to use

```
 # cd /tmp

 # wget https://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.7.0.tar.gz

 # tar xzvf RPi.GPIO-0.7.0.tar.gz

 # cd RPi.GPIO-0.7.0/

 # python ./setup.py install
```


## Installation

To install the program `fan` and the service just run the install
script.

```
 $ sudo install.sh
```

This will install and run the service. The next time you boot your
the system, the fan service will be automatically started.

### Typical installation's output

```
$ sudo install.sh
Installing fan.py
Installing the fan service
Starting the service
* fan.service - Fan Service
   Loaded: loaded (/usr/lib/systemd/system/fan.service; static; vendor preset: disabled)
   Active: active (running) since Sun 2019-07-28 10:38:16 PDT; 2s ago
 Main PID: 9771 (fan)
    Tasks: 1 (limit: 512)
   CGroup: /system.slice/fan.service
           `-9771 /usr/bin/python /usr/local/bin/fan

Jul 28 10:38:16 echostar systemd[1]: Started Fan Service.
Jul 28 10:38:16 echostar fan[9771]: 10:38:16 INFO: GPIO pin(26) configured
```

## Manual installation

To install the program `fan` just copy the file `fan.py` from this
directory to `/usr/local/bin/fan`. Then make sure that file is
executable.

```
$ sudo cp fan.py /usr/local/bin/fan
$ sudo chmod a+x /usr/local/bin/fan
```

## Running

To start `fan` at boot time. You need to install the fan service. Copy
the file `fan.service` into the directory `/lib/systemd/system`, then
inform `systemd` that it needs to run that service.

```
$ systemctl enable fan.service

```

## Example

Debug output of the program `fan` running.
```
11:29:46 INFO: GPIO pin(26) configured
11:29:46 WARNING: Temperature: 41.86
11:29:46 INFO: Fan(26) -> OFF
11:30:17 WARNING: Temperature: 41.86
11:30:48 WARNING: Temperature: 42.93
11:30:48 INFO: Fan(26) -> ON
11:31:19 WARNING: Temperature: 42.93
11:31:50 WARNING: Temperature: 42.39
11:32:21 WARNING: Temperature: 41.86
11:32:21 INFO: Fan(26) -> OFF
11:32:52 WARNING: Temperature: 41.86
11:33:23 WARNING: Temperature: 42.39
11:33:23 INFO: Fan(26) -> ON
11:33:54 WARNING: Temperature: 41.86
11:33:54 INFO: Fan(26) -> OFF
11:34:25 WARNING: Temperature: 42.93
11:34:25 INFO: Fan(26) -> ON
11:34:56 WARNING: Temperature: 41.86
11:34:56 INFO: Fan(26) -> OFF
11:35:28 WARNING: Temperature: 42.39
11:35:28 INFO: Fan(26) -> ON
11:35:59 WARNING: Temperature: 42.93
11:36:30 WARNING: Temperature: 41.86
11:36:30 INFO: Fan(26) -> OFF
```
