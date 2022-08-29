import RPi.GPIO as GPIO
import numpy as np
from action import *
import time

stepPin = 24
dirPin = 23

#switch pins
HomePin = 21
LfPin = 20
RtPin = 16

#define speed
speed = 0.0002
speed_i = 0.0004
speed_f = 0.000105
steps = 20
damp = 300

step_width = np.floor(damp/steps)
speed_different = (speed_i - speed_f)/steps

GPIO.setmode(GPIO.BCM)

GPIO.setup(RtPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LfPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(HomePin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(stepPin, GPIO.OUT)
GPIO.setup(dirPin, GPIO.OUT)

GPIO.output(dirPin,1)

def get_position():
	loop = 0
	GPIO.output(dirPin,1)
	while GPIO.input(LfPin) == 0:
		print("Left",GPIO.input(LfPin))
		GPIO.output(stepPin, True)
		time.sleep(speed)
		GPIO.output(stepPin, False)
		time.sleep(speed)
	while True:
		print(loop)
		print("Adjust : ")
		adjust = int(input())
		loop += adjust
		if adjust > 0:
			GPIO.output(dirPin,0)
			for i in range(np.abs(adjust)):
				GPIO.output(stepPin, True)
				time.sleep(speed)
				GPIO.output(stepPin, False)
				time.sleep(speed)
		else:
			GPIO.output(dirPin,1)
			for i in range(np.abs(adjust)):
				GPIO.output(stepPin, True)
				time.sleep(speed)
				GPIO.output(stepPin, False)
				time.sleep(speed)




def get_width():
	loop = 0
	GPIO.output(dirPin,1)
	while GPIO.input(LfPin) == 0:
		print("Left",GPIO.input(LfPin))
		GPIO.output(stepPin, True)
		time.sleep(0.00015)
		GPIO.output(stepPin, False)
		time.sleep(0.00015)
	GPIO.output(dirPin,0)
	while GPIO.input(RtPin) == 0:
		print("Right",GPIO.input(RtPin))
		GPIO.output(stepPin, True)
		time.sleep(0.00015)
		GPIO.output(stepPin, False)
		time.sleep(0.00015)
		loop += 1
	print(loop)
def move_middle():
	loop = 0
	GPIO.output(dirPin,1)
	while GPIO.input(LfPin) == 0:
		GPIO.output(stepPin, True)
		time.sleep(0.00018)
		GPIO.output(stepPin, False)
		time.sleep(0.00018)
	GPIO.output(dirPin,0)
	time.sleep(0.4)
	while GPIO.input(RtPin) == 0:
		GPIO.output(stepPin, True)
		time.sleep(0.00018)
		GPIO.output(stepPin, False)
		time.sleep(0.00018)
		loop += 1
	print(loop)
	time.sleep(0.4)
	GPIO.output(dirPin,1)
	for l in range(int(loop/2)):
		GPIO.output(stepPin, True)
		time.sleep(0.00018)
		GPIO.output(stepPin, False)
		time.sleep(0.00018)
def move(position):
	trash_position = [700,3000,5300,7600,9900,12200]
	home = 6450
	pos = home

	i = speed_f
	dist = 0

	if position < len(trash_position)/2:
		GPIO.output(dirPin,1)
		while GPIO.input(LfPin) == 0 and pos > trash_position[position]:
			# print(pos,i)
			gap_i = np.abs(pos - home)
			gap_f = np.abs(pos - trash_position[position])

			if gap_i < damp:
				current_step = gap_i / step_width
				i = speed_i - speed_different * current_step

			if gap_f < damp:
				current_step = gap_f / step_width
				i = speed_i - speed_different * current_step

			GPIO.output(stepPin, True)
			time.sleep(i)
			GPIO.output(stepPin, False)
			time.sleep(i)
			pos -= 1
		servo()
		dist = distance_ultra()
		GPIO.output(dirPin,0)
		while GPIO.input(RtPin) == 0 and pos < home:
			gap_f = np.abs(pos - home)
			gap_i = np.abs(pos - trash_position[position])

			if gap_i < damp:
				current_step = gap_i / step_width
				i = speed_i - speed_different * current_step

			if gap_f < damp:
				current_step = gap_f / step_width
				i = speed_i - speed_different * current_step

			GPIO.output(stepPin, True)
			time.sleep(i)
			GPIO.output(stepPin, False)
			time.sleep(i)
			pos += 1

	else:
		GPIO.output(dirPin,0)
		while GPIO.input(RtPin) == 0 and pos < trash_position[position]:
			# print(pos,i)
			gap_i = np.abs(pos - home)
			gap_f = np.abs(pos - trash_position[position])

			if gap_i < damp:
				current_step = gap_i / step_width
				i = speed_i - speed_different * current_step

			if gap_f < damp:
				current_step = gap_f / step_width
				i = speed_i - speed_different * current_step

			GPIO.output(stepPin, True)
			time.sleep(i)
			GPIO.output(stepPin, False)
			time.sleep(i)
			pos += 1
		servo()
		dist = distance_ultra()
		GPIO.output(dirPin,1)
		while GPIO.input(LfPin) == 0 and pos > home:
			gap_f = np.abs(pos - home)
			gap_i = np.abs(pos - trash_position[position])

			if gap_i < damp:
				current_step = gap_i / step_width
				i = speed_i - speed_different * current_step

			if gap_f < damp:
				current_step = gap_f / step_width
				i = speed_i - speed_different * current_step

			GPIO.output(stepPin, True)
			time.sleep(i)
			GPIO.output(stepPin, False)
			time.sleep(i)
			pos -= 1
	return dist