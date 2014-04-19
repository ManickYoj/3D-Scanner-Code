# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 10:53:30 2014

@author: koenigin
"""

import cv2.cv
import cv2
import numpy as np
import time
import pyserial

class Hardware(object):
    def __init__(self, step_size = 1, camera = 1):
        self.rotation = 0
        self.step_size = step_size;
        self.locked = False;
        self.camera = camera
        self.start_time = time.time()
        self.frames = []
        self.done = False

    def islocked(self):
        return self.locked;

    def togglelock(self):
        self.locked = not self.locked;

    def getrotation(self):
        return self.rotation;
        
    def isdone(self):
        '''Checks once clears videocap, checks to see if rotated around
        twice changes self.done to True'''
        pass
        
    def arduinocontrol(self):
        pass

    def videocap(self):
        '''If not done, will take video and append each frame to a list 
        with the relevant timestamp'''
        cap = cv2.VideoCapture(self.camera)
        while(not self.done):        
            # Take each frame
            _, frame = cap.read()
            self.frames.append((frame, time.time()-self.start_time))
            
    def captureimage(self):
        '''If  scanning is not done, return the last image added to the list
        '''
        if not self.done:
            return self.frames(-1)
        return None
                
    def conversionfactor(self, end_time):
        factor = (end_time-self.start_time)/ (2*np.pi)
        return factor            
        
        
        
        
        
                