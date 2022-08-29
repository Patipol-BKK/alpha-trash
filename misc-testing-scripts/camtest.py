from tensor import *
from picamera import PiCamera
import time

camera = PiCamera()

print("Ready")
while True:
	input()
	print("Capturing")
	camera.capture('image.jpeg')
	start = time.time()
	print("Classifying")
	print(classify())
	print("Elapsed time = ",time.time() - start)