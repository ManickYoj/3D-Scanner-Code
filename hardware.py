"""
hardware.py
-------
Author: Lindsey Vanderlyn
Status: Complete & In Testing
Description: An interface class to access the camera and Arduino

"""

import cv2
import time
import threading as t
from arduino import Arduino


class Hardware(object):

    def __init__(self, camera=0, motor_pin=4, debug=False):
        self.debug = debug
        self.camera = camera
        self.motor_pin = motor_pin
        self.locked = False
        self.board = Arduino()

        self.board.output([self.motor_pin])
        time.sleep(0.1)

    # ----- Public Functions ----- #
    def islocked(self):
        return self.locked

    def togglelock(self):
        self.locked = not self.locked

    def isdone(self):
        """ Checks to see if table has completed one full rotation. """
        return bool(self.total_time)

    def beginscan(self):
        '''starts the arduino and after one rotation, starts the camera'''
        # Initilize variables
        self.total_time = None
        self.angle_vel = None
        self.frames = []

        # Start motor and video camera
        print('Beginning Scan')
        self.board.setHigh(self.motor_pin)
        time.sleep(0.1)
        t.Thread(target=self.videocap).start()

        # Wait until video camera has begun capture, start timer, and return
        while not self.frames:
            time.sleep(0.01)
#        self.start_time = time.time()

    def captureimage(self):
        """ Returns the most recent image, or none if scan is complete. """
        if not self.total_time:
            return self.frames[-1]
        return None

    def getavgvel(self):
        """ Calculates the average angular velocity (rads/sec) of the most recent scan. """
        if self.total_time:
            return (6.28)/(self.total_time)

    # ----- Private Functions ----- #
    def checkrotation(self):
        current_time = time.time() - self.start_time
        if current_time >= 13.2:
            self.total_time = current_time

    def videocap(self):
        '''If not done, will take video and append each frame to a list with
        the relevant time_stamp

        camera: the index of video camera being used [should be 1]'''
        cap = cv2.VideoCapture(self.camera)
        self.start_time = time.time()

        # Take video until rotation is complete
        while not self.total_time:
            # Take one frame
            frame = cap.read()
            t_stamp = time.time()-self.start_time
            self.frames.append((frame[1], t_stamp))

            # Sets the self.total_time attribute to true when complete
            self.checkrotation()
            time.sleep(0.01)

        self.stopmotor()

    def stopmotor(self):
        ''' Stops the motor from rotating. '''
        self.board.setLow(self.motor_pin)
        
if __name__ == '__main__':
    test = Hardware()
    test.beginscan()
