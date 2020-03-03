import picamera
import time

camera = picamera.PiCamera()

camera.capture('maze_v2.jpg')
camera.close()
