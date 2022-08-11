import RPi.GPIO as gpio
import time 

def distance(measure= 'cm'):            #define distance and the pins on raspberry
	gpio.setmode(gpio.BOARD)
	gpio.setup(26, gpio.OUT)
	gpio.setup(24, gpio.IN)
	gpio.output(26, False)
	
	while gpio.input(24) == 0:
		nosig = time.time()     #no signal

	while gpio.input(24) == 1:
		sig = time.time()       #signal

	t1 = sig - nosig                #time/distance measured

	if measure == 'cm':                     #measure the distance in cm
		distances = t1 / 0.000058
	elif measure == 'in':
		distances = t1 / 0.0000148      ##measure the distance in inch
	else:
		print('Improper choice of measurement: in or cm')
		distances = None

	gpio.cleanup()
	return distances

