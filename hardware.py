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
        pin = 11                        #the output pin for the tripsensor
        self.board.output([pin])
        self.rotation = self.board.getState(pin)
        return self.rotation        
        
    def beginscan(self):
        '''starts the arduino and after one rotation, starts the camera'''
        #insert arduino code
        videocap_thread = t.Thread(target = self.videocap())
        while(not self.rotation):
            self.checkrotation()
            time.sleep(0.01)  
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
            self.done = self.checkrotation()
            self.stopmotor()
            time.sleep(0.01)
            
    def stopmotor(self):
        if self.done:
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
        
        
        
        
        
                