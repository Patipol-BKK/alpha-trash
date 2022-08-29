# import RPi.GPIO as GPIO
import time	 
from picamera import PiCamera

# from action import *
# from moveframe import *


# import _thread
camera = PiCamera()
while True:

	input()
	camera.capture('testimg.jpeg')
# exit()
# i = 0
# while True:
# 	move(i)
# 	i = (i+1)%4
# 	time.sleep(0.5)
#get_position()
#move(0)
