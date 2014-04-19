# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 10:53:30 2014

@author: koenigin
"""

import cv2.cv
import cv2
import numpy as np
import time

class hardwareInterface(object):
    def __init__(self, step_size = 1, camera = 0):
        self.rotation = 0
        self.step_size = step_size;
        self.locked = False;
        self.camera = camera
        self.startTime = time.time()

    def isLocked(self):
        return self.locked;

    def toggleLock(self):
        self.locked = not self.locked;

    def getRotation(self):
        return rotation;

    def setStepSize(self, step_size):
        self.step_size = step_size;

    def advanceTurntable(self, step_size = None):
        if step_size is None:
            step_size = self.step_size;

        # TODO: Actually step hardware by the step_size

    def singleImageCap(self):
        """Code below will use the camera to capture a single image"""
        # Initialize the camera    
        capture = cv2.cv.CaptureFromCAM(self.camera)  # 0 -> index of camera
        if capture:     # Camera initialized without any errors
           f = cv2.cv.QueryFrame(capture)     # capture the frame
           if f:
    #           ShowImage("cam-test",f)
    #           WaitKey(0)
                cv2.cv.SaveImage('capture.jpeg', f)
                return 'capture.jpeg'   # Does this actually return the image? I assume this is just a string
                
    def ConversionFactor(endTime):
        factor = (endTime-self.startTime)/ (2*pi)
        return factor            
                