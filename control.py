# Scott Stinson
# Main Control code that takes input from an Xbox Controller to control an RC car
# with one servo and one dc motor using an Adafruit PCA9685 board and RPi
# Needs Adafruit_PCA9685 Library, XboxController.py code, and pygame to interpret xbox controller
# events
#import subprocess
#command = subprocess.run(["sudo", "xboxdrv", "--silent", "--detach-kernel-driver", "&"])
import Adafruit_PCA9685
import XboxController
# Initialise the PCA9685
pwm = Adafruit_PCA9685.PCA9685()

# import some python function which are used
import time, sys, os

# Set the PWM frequency for to control the servo and ESC. Ours is 60 Hz which is common

pwm.frequency = 60

# Creating a class for the communication between the RC car and Xbox Controller
#  using call backs
class controller:
    def __init__(pwm):
        # Setup default Xbox Controller Call Back
        pwm.xboxCont = XboxController.XboxController(deadzone = 30,
                                                scale = 100,
                                                invertYAxis = True)
        # Setup call backs for the Throttle, steering, booting the ESC, stopping the motor,
        # and ending the program
        pwm.xboxCont.setupControlCallback(pwm.xboxCont.XboxControls.LTHUMBY, pwm.leftThumbY)
        pwm.xboxCont.setupControlCallback(pwm.xboxCont.XboxControls.RTHUMBX, pwm.rightThumbX)
        pwm.xboxCont.setupControlCallback(pwm.xboxCont.XboxControls.A, pwm.A_button)
        pwm.xboxCont.setupControlCallback(pwm.xboxCont.XboxControls.B, pwm.B_button)
        pwm.xboxCont.setupControlCallback(pwm.xboxCont.XboxControls.X, pwm.X_button)
        # Start Controller
        pwm.xboxCont.start()
        pwm.running = True
    # definition of each call back button
    # in each definition, we use set_pwm(channel, on, off) to set PWM signal to PCA9685 board
    # To elaborate:
    #    channel = channel on PCA9685 board, in our case its 0 for throttle, 1 for steering
    #    on = The tick (between 0 & 4095) when signal should transition from low to high,
    #              default value set to: 0, we don't neet to change it in our case
    #    off = the tick (between 0 & 4095) when the signal should transition from high to low,
    #              this is the PWM signal we send to the PCA9685 board
    # The left toggle is for throttle, (y - value)
    def leftThumbY(self, yValue):
        stop = 1210
        go = 1210
        fwdmax = 1320
        revmax = 1050
        print (yValue)
        if yValue > 0:
            go = go + int(round((fwdmax-go)*(yValue/100)))
            pwm.set_pwm(0,0,go)
        if yValue < 0:
            go=stop
            pwm.set_pwm(0,0,go)
            time.sleep(0.001)
            go = go + int(round((go-revmax)*(yValue/100)))
            pwm.set_pwm(0,0,go)
        if yValue == 0:
            pwm.set_pwm(0,0,go)
    # We are using the right toggle for the steering (x-value)
    def rightThumbX(self, xValue):
        print (xValue)
        steering_value = 975
        steering_value_init = steering_value
        steering_max_left = 500
        steering_max_right = 1500
        if xValue > 0:
            steering_value =  steering_value + int(round((steering_max_left-steering_value)*(xValue/100)))
            pwm.set_pwm(1,0,steering_value)
        if xValue < 0:
            steering_value =  steering_value - int(round((steering_max_right-steering_value)*(xValue/100)))
            pwm.set_pwm(1,0,steering_value)
        if xValue ==0:
            pwm.set_pwm(1,0,steering_value)
        
 # Initializes the ESC by sending PWM value of max speed       
    def A_button(self, Avalue):
        pwm.Avalue = Avalue
        print (Avalue)
        fwdmax = 1210
        revmax = 400
        go = fwdmax
        pwm.set_pwm(0, 0, go)
        time.sleep(0.2)
        stop = go
        fwdmax = 1320
        revmax = 1050
    # Stops the motor and returns steering back to original value ( 0 degrees)
    def B_button(self, Bvalue):
        pwm.Bvalue = Bvalue
        print (pwm.Bvalue)
        steering_value = 900
        steering_value_init = steering_value
        go = 1210
        steering_value = steering_value_init
        pwm.set_pwm(0,0,go)
        pwm.set_pwm(1,0,steering_value)
# End the program using X button on controller
    def X_button(self, X):
        self.running = False
        stop=1210
        steering_value = 1000
        pwm.set_pwm(0,0,stop)
        pwm.set_pwm(1,0,steering_value)
        self.xboxCont.stop()
        print('Program ended')

# program loop to control the RC car via an Xbox Controller

control = controller()
while control.running:
    time.sleep(0.1)
# Other Notes:
# inputed value displayed in CL everytime the input changes,
# ex. print(xValue) in the def leftThumbX module
