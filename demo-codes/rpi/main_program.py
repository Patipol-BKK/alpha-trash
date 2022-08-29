from picamera import PiCamera
from time import sleep
import subprocess
from PIL import Image

#Define Ultrasonic
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
trig = 7
echo = 11

GPIO.setmode(GPIO.BOARD)

GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

camera = PiCamera()

def distance():
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)
    
    StartTime = time.time()
    StopTime = time.time()
    
    while GPIO.input(echo) == 0:
        StartTime = time.time()
    while GPIO.input(echo) == 1:
        StopTime = time.time()
        
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300)/2
    
    return distance
def classify():
	print("Classifying...")
	p = subprocess.Popen("python3 classify_operation.py", stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	
	p_status = p.wait()
	return output.decode('utf-8')

def capture():
    try:
        print("Capturing...")
        camera.capture('image.jpeg')
    except:
        return 0
def resize_img():
	Image.open('image.jpeg').resize(size=(160, 90)).save('image.jpeg', 'JPEG')	

if __name__ == "__main__":
	loop = 1
	while True:
		print("\n",loop,"Ready!")
		loop+=1
		detect = False
		while detect == False:
			dist = distance()
			#print("Distance = ",dist)
			if dist <  20:
				detect = True
				print("Object Detected!")
		capture()
		resize_img()
		try:
			start = time.time()
			result = classify()
			print("------------")
			print("Result = ",result)
			print("Elapsed time = ",time.time() - start," seconds")
			print("------------")
		except:
			print("Classification Error")
		print("Waiting...")
		#time.sleep(10)
		
        
