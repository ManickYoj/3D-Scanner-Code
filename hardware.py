# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 10:53:30 2014

@author: koenigin
"""

import cv2.cv
import cv2
import numpy as np
import time
import serial

class Hardware(object):
    def __init__(self, step_size = 1, camera = 1):
        self.locked = False
        self.camera = camera
        self.start_time = -1
        self.frames = []
        self.done = False
        self.end_time = -1
        self.angle_vel = -1
        self.rotation = False 
        
        
    def islocked(self):
        return self.locked;

    def togglelock(self):
        self.locked = not self.locked;
      
    def isdone(self):
        '''Checks to see if rotated around'''
        return self.done
        
    def checkrotation(self):
        ser = serial.Serial('/dev/tty.usbserial', 9600)
        
    
        
    def beginscan(self):
        '''starts the arduino and after one rotation, starts the camera'''
        #insert arduino code
        time.sleep(0.1)
        if self.rotation:
            self.videocap()
        
            

    def videocap(self):
        '''If not done, will take video and append each frame to a list 
        with the relevant timestamp'''
        cap = cv2.VideoCapture(self.camera)
        while(not self.done):        
            # Take each frame
            _, frame = cap.read()
            self.frames.append((frame, time.time()-self.start_time))
            time.sleep(0.1)
           
     def captureimage(self):
        '''If  scanning is not done, return the last image added to the list
        '''
        if not self.done:
            return self.frames(-1)
        return None
                
    def getavgvel(self):
        if self.done:        
            angle_vel= (self.end_time-self.start_time)/ (2*np.pi)
            return angle_vel
        
        
        
        
        
                