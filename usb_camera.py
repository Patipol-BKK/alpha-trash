import os

def capture_usb():
	try:
		os.system("fswebcam -r 1280x720 --no-banner image.jpeg")
	except:
		print("Capture Failed")
