"""
hardware.py
-------
Author: Lindsey Vanderlyn
Status: Complete & In Testing
Description: An interface class to access the camera and Arduino

"""

import cv2.cv
import cv2
import numpy as np
import time
import os
import threading as t
from arduino import Arduino
import pickle


class Hardware(object):

    def __init__(self, camera=0, motor_pin=4, debug = False):
        self.locked = False
        self.start_time = -1
        self.frames = []
        self.done = False
        self.end_time = -1
        self.angle_vel = -1
        self.rotation = False
        self.board = Arduino()
        self.motor_pin = motor_pin
        self.board.output([self.motor_pin])
        self.debug = debug
        self.camera = camera

    # ----- Public Functions ----- #
    def islocked(self):
        return self.locked

    def togglelock(self):
        self.locked = not self.locked

    def isdone(self):
        '''Checks to see if table has completed a rotation around'''
        return self.done

    def beginscan(self):
        '''starts the arduino and after one rotation, starts the camera'''
        time.sleep(0.2)
        self.board.setHigh(self.motor_pin)   # Turns on motor
        videocap_thread = t.Thread(target=self.videocap)
        time.sleep(2)
        self.start_time = time.time()
        videocap_thread.start()
        while len(self.frames)==0:
            time.sleep(0.01)

    def captureimage(self):
        '''If  scanning is not done, return the last image added to the list
        '''
        if not self.done and self.frames is not None:
            return self.frames[-1]
        return None

    def getavgvel(self):
        '''calculates and returns the angular velocity based on how long it
        takes to rotate the table 2pi rad'''
        if self.done:
            if self.end_time != -1:
                angle_vel = (2*3.1415)/(self.end_time-self.start_time)
                print self.end_time-self.start_time                
                print angle_vel
                return angle_vel

    # ----- Private Functions ----- #
    def checkrotation(self):
        current_time = time.time() - self.start_time
        if current_time >= 13:
            self.end_time = time.time()
            self.done = True

    def videocap(self):
        '''If not done, will take video and append each frame to a list with
        the relevant time_stamp

        camera: the index of video camera being used [should be 1]'''
        cap = cv2.VideoCapture(self.camera)
        n = 0
        while not self.done:  # Take video until rotation is complete
            # Take one frame
            frame = cap.read()
            t_stamp = time.time()-self.start_time
            self.frames.append((frame[1], t_stamp))
#            cv2.imwrite(os.path.join('Images', 'mTapepic'+str(n)+'.jpg'), frame[1])
#            n+=1
            self.checkrotation()
            time.sleep(0.01)

        self.stopmotor()  # Stops motor when rotation is complete

        # Captures full set of picture arrays and saves them to a debug file
        if self.debug:
            if not os.path.exists("Debug"):
                os.makedirs("Debug")
            path = os.path.join("Debug", "debug_frames.pkl")
            with open(path, "wb") as dump_file:
                pickle.dump(self.frames, dump_file)

    def stopmotor(self):
        ''' Stops the motor from rotating. '''
        self.board.setLow(self.motor_pin)
        time.sleep(0.1)

# ----- Unit Testing ------ #
if __name__ == '__main__':
    pass
    
    
