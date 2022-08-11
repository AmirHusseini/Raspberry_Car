import RPi.GPIO as gpio         # a class to control the GPIO (general-purpose input/output) pins on the Raspberry Pi
from time import sleep          # it pauses the Python program
import time, signal, sys, os    # (time) to see the datetime and calendar,(signal) provides mechanisms to use signal handlers in Python
                                # (sys) provides information about constants, functions and methods of the Python interpreter,
                                # (os) module in python provides functions for interacting with the operating system.
from sensor import distance     # get the distance from sensor.py       
from Adafruit_ADS1x15 import ADS1x15 # to make the analog to digital convertor work
import sqlite3                  # to gather and save the data in sqlite3


gpio.setwarnings(False)         #ignore the warnings

delayTime = 0.5                 # in seconds

# assigning the ADS1x15 ADC
ADS1015 = 0x00  # 12-bit ADC
ADS1115 = 0x01  # 16-bit

# choosing the amplifing gain
gain = 4096  # +/- 4.096V - the chip can read values from -4.096 volts to +4.096 volts
sps = 64  # 64 Samples per second

# assigning the ADC-Channel (1-4)
adc_channel_0 = 0  # Channel 0 
adc_channel_1 = 1  # Channel 1
adc_channel_2 = 2  # Channel 2
adc_channel_3 = 3  # Channel 3

# initialise ADC (ADS1115) as we have ADs1115
adc = ADS1x15(ic=ADS1115)
# Get the time in the right format
dtg1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
# Opens a file called measurements and form a connection
db = sqlite3.connect('measurements.db')
# Get a cursor object
cr = db.cursor()

def commitToSQL(action1):
    # Commit to database
    # read values
    adc01 = adc.readADCSingleEnded(adc_channel_0, gain, sps)
    adc1 = adc.readADCSingleEnded(adc_channel_1, gain, sps)
    adc2 = adc.readADCSingleEnded(adc_channel_2, gain, sps)
    adc3 = adc.readADCSingleEnded(adc_channel_3, gain, sps)
    # Print the time and volt values.
    print "Local current time:", dtg1
    print "Voltage value via ADC:", adc01 / 1000
    #Insert command to save Time and voltage values read by ADs 1115 converter and relative actions into the voltageAction table
    cr.execute('''INSERT INTO voltageAction(dtg,adc0,action)
                   VALUES(?,?,?)''', (dtg1, adc01, action1))
    db.commit()

#initalise the pins
def init():
    gpio.setmode(gpio.BOARD)    # referring to the pins by the number of the pin (The GPIO.BCM option "Broadcom SOC channel" number)
    gpio.setup(7, gpio.OUT)     # set up a channel as an output (the wheels)
    gpio.setup(11, gpio.OUT)
    gpio.setup(40, gpio.OUT)
    gpio.setup(15, gpio.OUT)

#going forward
def forward():
    gpio.output(7, False)       # We can even use LOW or HIGH as in Arduino
    gpio.output(11, True)
    gpio.output(40, True)
    gpio.output(15, False)
    time.sleep(1)               #pause 1 second
    gpio.cleanup()              #resets the used ports back to input mode

#going backward
def reverse():
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(40, False)
    gpio.output(15, True)
    time.sleep(1)
    gpio.cleanup()

#turn left
def turn_left():
    gpio.output(7, True)
    gpio.output(11, True)
    gpio.output(40, True)
    gpio.output(15, False)
    time.sleep(1)
    gpio.cleanup()

#turn right
def turn_right():
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(40, False)
    gpio.output(15, False)
    time.sleep(1)
    gpio.cleanup()

#pivot left
def pivot_left():
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(40, True)
    gpio.output(15, False)
    time.sleep(1)
    gpio.cleanup()

#pivot right
def pivot_right():
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(40, False)
    gpio.output(15, True)
    time.sleep(1)
    gpio.cleanup()

#turn the servo/ultrasonic straight
def servo():
    gpio.setmode(gpio.BOARD)
    gpio.setup(18, gpio.OUT)
    pwm = gpio.PWM(18, 50)    #With the use of PWM, we can simulate varying levels of output energy to an electrical device
                              #Initialize PWM on pwmPin 18 with 50Hz frequency
    pwm.start(7.5)            #Start PWM with 7,5% duty cycle
    pwm.ChangeDutyCycle(7.5)  # turn towards 90 degree
    time.sleep(1)             # sleep 1 second
    gpio.cleanup()

#turn the servo/ultrasonic to the left
def servo_left():
    gpio.setmode(gpio.BOARD)
    gpio.setup(18, gpio.OUT)
    pwm = gpio.PWM(18, 40)
    pwm.start(7.5)
    pwm.ChangeDutyCycle(2.5)  # turn towards 0 degree
    time.sleep(1)  # sleep 1 second
    gpio.cleanup()
    
#turn the servo/ultrasonic to the right
def servo_right():
    gpio.setmode(gpio.BOARD)
    gpio.setup(18, gpio.OUT)
    pwm = gpio.PWM(18, 50)
    pwm.start(7.5)
    pwm.ChangeDutyCycle(12.5)  # (2.5) turn towards 180 degree
    time.sleep(1)  # sleep 1 second
    gpio.cleanup()


while True:
    #python user input function
    inp = raw_input()
    if inp == "1":
        #initialise the BOARD pins
        init()
        forward()
        # function call to record time and voltage values into the table
        commitToSQL("forward")

        curDis = distance()                 #get the distance and print
        print('The distance is: ', curDis)
        if curDis < 5:                      #if the distance is less than 5 cm reverse for 1 second
            init()
            reverse(1)
        print "robot moving in fwd direction"
    elif inp == "2":
        init()
        reverse()
        commitToSQL("reverse")
        print"robot moving in rev direction"

    elif inp == "3":
        init()
        turn_left()
        commitToSQL("left")
        print"robot turn left"

    elif inp == "4":
        init()
        turn_right()
        commitToSQL("right")
        print"robot turn right"

    elif inp == "5":
        init()
        commitToSQL("pivotleft")
        pivot_left()

    elif inp == "6":
        init()
        commitToSQL("pivotright")
        pivot_right()

    elif inp == "7":
        servo()
        curDis = distance()
        commitToSQL("servodistance")
        print('The distance is: ', curDis)

    elif inp == "8":
        servo_right()
        curDis = distance()
        commitToSQL("servorightdistance")
        print('The distance is: ', curDis)

    elif inp == "9":
        servo_left()
        curDis = distance()
        commitToSQL("servoleftdistance")
        print('The distance is: ', curDis)
    else:
        pass

gpio.cleanup()
