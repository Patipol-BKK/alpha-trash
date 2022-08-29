import RPi.GPIO as GPIO
import time	 

from moveframe import *
from action import *
from tensor import *

# move_middle()
# exit()
# i = 0
# while True:
# 	move(i)
# 	i = (i+1)%4
# 	time.sleep(0.5)
#get_position()
while True:
	print("Ready")
	while distance_infra() == 1:
		time.sleep(0.2)
	while distance_infra() == 0:
		time.sleep(0.2)
	time.sleep(0.4)
	
	print("Capturing")
	capture()
	start = time.time()
	print("Classifying")
	result = classify()
	print(result)
	print("Elapsed time = ",time.time() - start)
	if result['type'] == 'metal':
		move(0)
	elif result['type'] == 'general':
		move(1)
	elif result['type'] == 'danger':
		move(2)
	elif result['type'] == 'plastic' or result['type'] == 'paper':
		move(3)
