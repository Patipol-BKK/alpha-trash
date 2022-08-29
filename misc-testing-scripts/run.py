import RPi.GPIO as GPIO
import time	 
import datetime

from server import *
from moveframe import *
from action import *
from tensor import *

import threading
# i = 0
# while True:
# 	move(i)
# 	i = (i+1)%4
# 	time.sleep(0.5)
#get_position()
move_middle()
is_use = 0
is_send = 0
def open_image():
	with open("upload.jpeg", "rb") as imageFile:
		pix = base64.b64encode(imageFile.read())
		return pix.decode('utf-8')

def update(confidence, category, sub_category,value):
	while is_use == 1:
		time.sleep(0.05)
	is_send = 1
	update_log("DLTrash Unit-Prototype",open_image(),str(confidence),category,"The Street Ratchada",str(datetime.datetime.now()))
	if sub_category != "main":
		update_trash(category, "main")
		update_record(category, "main")
	update_trash(category, sub_category, value)
	update_record(category, sub_category)
	is_send = 0

def connect_on():
	while True:
		while is_send == 1:
			time.sleep(0.05)
		try:
			is_use = 1
			get_record("Recycle","Plastic")
			print(datetime.datetime.now(),": Server Status : Connected")
		except:
			print("Disconnected from Server!")
		is_use = 0
		time.sleep(180)


def light():
	lo = 0
	for lo in range(23):
		led_on()
		time.sleep(0.1)
		led_off()
		time.sleep(0.1)

def calibrate_empty():
	for i in range(6):
		dist = move(i)


if __name__ == "__main__":
	thread3 = threading.Thread(target=connect_on,args=())
	thread3.start()
	while True:
		print("Ready")
		led_on()
		while distance_infra() == 1:
			time.sleep(0.02)
		while distance_infra() == 0:
			time.sleep(0.02)
		led_off()
		time.sleep(0.4)	
		
		print("Capturing")
		capture()
		thread1 = threading.Thread(target=light,args=())
		thread1.start()
		start = time.time()
		print("Classifying")
		result = classify()
		if result['score'] < 0.6:
			result['type'] = 'General'
			result['sub_type'] = 'main'
		print(result)
		print("Elapsed time = ",time.time() - start)
		# update_record(result['type'])

		if result['type'] == 'Recycle' and result['sub_type'] == 'Metal':
			val = move(0)
		elif result['type'] == 'Recycle' and result['sub_type'] == 'Plastic':
			val = move(1)
		elif result['type'] == 'Recycle' and result['sub_type'] == 'Paper':
			val = move(2)
		elif result['type'] == 'Organic':
			val = move(4)
		elif result['type'] == 'Danger':
			val = move(5)
		elif result['type'] == 'General':
			val = move(3)

		thread = threading.Thread(target=update,args=(result['score'],result['type'],result['sub_type'],val))
		thread.start()
