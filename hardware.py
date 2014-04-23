# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 10:53:30 2014

@author: koenigin
"""

import cv2.cv
import cv2
import numpy as np
import time
import threading as t
from arduino import Arduino

class Hardware(object):
    def __init__(self, step_size = 1, camera = 1):
        self.locked = False
        self.start_time = -1
        self.frames = []
        self.done = False
        self.end_time = -1
        self.angle_vel = -1
        self.rotation = False 
        self.board = Arduino('/dev/ttyUSB0')
        
        
    def islocked(self):
        return self.locked;

    def togglelock(self):
        self.locked = not self.locked;
      
    def isdone(self):
        '''Checks to see if table has completed a rotation around'''
        return self.done
        
    def checkrotation(self):
        current_time = time.time()- self.start_time
        if current_time >= 13.25 and current_time <= 13.27:        #if the time is within end range
            self.done = True   
        return self.done        
        
    def beginscan(self):
        '''starts the arduino and after one rotation, starts the camera'''
        self.board.input([5])
        self.board.setHigh(5)
        videocap_thread = t.Thread(target = self.videocap())
        time.sleep(2)
        videocap_thread.run()         

    def videocap(self, camera):
        '''If not done, will take video and append each frame to a list with 
        the relevant timestamp
        
        camera: the index of video camera being used [should be 1]'''
        cap = cv2.VideoCapture(camera)         
        while(not self.done):        
            # Take each frame
            _, frame = cap.read()
            t_stamp = time.time()-self.start_time
            self.frames.append((frame, t_stamp))
            if self.checkrotation():
                self.stopmotor()
                self.end_time = time.time()
            time.sleep(0.01)
            
    def stopmotor(self):
        self.board.setLow(5)        #where 5 is in place of the motor pin
            
    
    def captureimage(self):
        '''If  scanning is not done, return the last image added to the list
        '''
        if not self.done:
            return self.frames(-1)
        return None
                
    def getavgvel(self):
        '''calculates and returns the angular velocity based on how long it 
        takes to rotate the table 2pi rad'''
        if self.done:        
            angle_vel= (self.end_time-self.start_time)/ (2*np.pi)
            return angle_vel
        
        
        
        
        
                