import RPi.GPIO as GPIO
import pyfirmata
import time
from picamera import PiCamera

#PiCamera
try:
	camera = PiCamera()
except:
	print("Cant connect to Camera")

#Ultrasonic
trig = 8
echo = 25

GPIO.setmode(GPIO.BCM)

GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

#servo
board = pyfirmata.Arduino('/dev/ttyACM0')
pin6 = board.get_pin('d:6:s')
pin13 = board.get_pin('d:13:o')
pin6.write(170)
time.sleep(0.7)
#infrared
infra = 14
GPIO.setup(infra, GPIO.IN)

def servo():
	# for a in range(100):
	# 	print("loop")
	# 	pin13.write(0)
	# 	time.sleep(0.5)
	# 	pin13.write(1)
	# 	time.sleep(0.5)
	pin6.write(170)
	time.sleep(0.1)
	pin6.write(70)
	time.sleep(0.5)
	pin6.write(170)
	time.sleep(0.1)

def led_on():
	pin13.write(1)

def led_off():
	pin13.write(0)

def distance_ultra():
	GPIO.output(trig, True)
	time.sleep(0.00001)
	GPIO.output(trig, False)

	StartTime = time.time()
	StopTime = time.time()

	errlog = 0
	while GPIO.input(echo) == 0:
		StartTime = time.time()
		errlog += 1
		if errlog > 100000:
			return 100
	errlog = 0
	while GPIO.input(echo) == 1:
		StopTime = time.time()
		errlog += 1
		if errlog > 100000:
			return 100

	TimeElapsed = StopTime - StartTime
	distance = (TimeElapsed * 34300)/2

	print("Distance = ",distance)
	return distance

def distance_infra():
	return GPIO.input(infra)

def capture():
	try:
		camera.resolution = (640, 360)
		camera.capture("image.jpeg")
		camera.resolution = (160, 90)
		camera.capture("upload.jpeg")
		print("Image Captured")
	except:
		print("Capture Fail")

