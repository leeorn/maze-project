#!/usr/bin/env python
import freenect
import time
new_dev = freenect.open_device(freenect.init(), 0)
def rotate():
    led = 0
    for i in range(31):
        freenect.set_tilt_degs(new_dev, i)
        print(f"iterataion number {i}")
        time.sleep(0.1)
        
        if i % 5 == 0:
            freenect.set_led(new_dev, led)
            led += 1


def handler(signum, frame):
    """Sets up the kill handler, catches SIGINT"""
    global keep_running
    keep_running = False
# print('Press Ctrl-C in terminal to stop')
# signal.signal(signal.SIGINT, handler)
# freenect.runloop(body=body)
while(True):
    rotate()
