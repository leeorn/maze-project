import picamera
import time

camera = picamera.PiCamera()

camera.capture('maze.jpg')
camera.close()
