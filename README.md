# Xbox-Controlled-RC-Car
This project contains all of the requirements to program an xbox controller and RC car using a RaspberryPi and Adafruit_PCA9685 board. 

This involves an Adafruit_PCA9685 board, pygame, xboxdrv, xbox controller python code, and a controller-to-rc car python code.

All of these libraries and files will be included in this repository EXCEPT xboxdrv.


To download ans setup the Adafruit library, use:

  `sudo apt-get install git build-essential python-dev`

  `cd ~ git clone https://github.com/adafruit/Adafruit_Python_PCA9685.git`

  `cd Adafruit_Python_PCA9685`

  `sudo python setup.py install`

To download adafruit GPIO, run:
  `git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
  cd Adafruit_Python_GPIO
  sudo python setup.py install`

To download xboxdrv on the pi, run the command: 
  `sudo apt-get install xboxdrv`

You must have xboxdrv running in background, so run:

  `sudo xboxdrv --silent --detach-kernel-driver &`

You also must have pygame, run:
  `pip3 install pygame`

Download repository, run:
`git clone https://github.com/stinsun/Xbox-Controlled-RC-Car.git`

run: `python/home/pi/Xbox-Controlled-RC-Car/control.py`


To calibrate the throttle and steering, use the control.py code.
