# -*- coding: utf-8 -*-

import cv2.cv
import cv2
import numpy as np


class Image(object):
    
    def __init__(self, tup):
        self.image = tup[0]         #Stores original image 
        self.mask = []
        self.timeStamp = tup[1]              
        self.redPosition = []
        self.radii = []
        self.heights = []  
        self.coordinates = []
        self.angle = 0         
        self.Y = 5                  #distance in cm b/n cameraline and laser
        self.X = 9.8                #distance in cm from camera to center
        self.H = 10.95              #distance in cm from laser to center 
        print('initializing image')        
        self.center = 350           #Measured number        
        self.filterforredposition()
        self.rememberonlyredposition()
        self.getdepth()
        self.findheight()
        
    
    def filterforredposition(self): 
        '''will take in the image that the camera has just capturedPosition
        and filter so that only the redPosition remains'''
            
        # Convert BGR to HSVimage
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        
        # define range of laser color in HSV        
        lower_redPosition = np.array([0,0,50])
        upper_redPosition = np.array([200,100,255])
        
        # Threshold the HSV image to get only laser colors
        mask = cv2.inRange(hsv, np.uint8(lower_redPosition), 
                           np.uint8(upper_redPosition))
        kernel = np.ones((9,9),np.uint8)
        closed_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        # Bitwise-AND mask and original image
        self.mask = closed_mask
#        cv2.imshow('mask', self.mask)
#        cv2.waitKey(0)

    def rememberonlyredposition(self):
        '''Takes in an image and returns a list of the the average 
        redPosition position in each row'''
        #should create a list of the columns containing redPosition values 
        #in every row
        for row in range(self.mask.shape[0]):
            c =[]
            for column in range(self.mask.shape[1]):
                if self.mask[row, column] != 0:
                    c.append(column)
            #if redPosition values exist, add them to redPosition otherwise 
            #add the number 0 to redPosition
            if len(c) > 0:
                self.redPosition.append(c)
            else:
                self.redPosition.append([-1])
        for index in range(len(self.redPosition)):
            #should keep just the average value for the rows that redPosition
            #exists, in every column
            sum1 = 0
            for value in range(len(self.redPosition[index])):
                sum1 += self.redPosition[index][value]
            
            self.redPosition[index] = float(sum1)/len(self.redPosition[index])


    def getdepth(self):
        '''Takes in the original camera/lazer position parameters and uses 
        them to calculate the depth of the object we are measuring for a 
        single lazer image'''
        for index in range(len(self.redPosition)):
            if self.redPosition[index] != -1:        #If a red value exists:
                yPrime = self.redPosition[index] - self.center
                depth = ((self.H*yPrime)/self.Y)
                self.radii.append(depth)
        #Needs more math to stop distortion
        
    def cyltocar(self, r, theta, height):
        '''takes in cylindrical coordinates and converts to cartesian'''
        x = r*np.cos(theta)
        y = r*np.sin(theta)
        z = height
        return (x, y, z)
        
    def findheight(self):
        '''takes in the y pixel location and transforms to height based on
        depth of the image and math!'''
        for index in range(len(self.redPosition)):
            if self.redPosition[index] != -1:
                #Turns the index into a height, below is no longer an index
                self.heights.append(index)

    
    def convertangle(self, conversion):
        self.angle = self.timeStamp *conversion
        return self.angle        
        
    def getpoints(self, factor):
        '''takes in the time, depth, and conversion factor, outputs cartesian
        coordinates for the image'''
        for index in range(len(self.radii)):
            self.coordinates.append(self.cyltocar(self.radii[index], 
                                                  self.convertangle(factor), 
                                                  self.heights[len(self.heights)-1 - index]))
        return self.coordinates
        
if __name__ == '__main__':
    cam = cv2.VideoCapture(1)
    s, img = cam.read() 
    cv2.imshow('show', img)
    cv2.cv.WaitKey(0)
    test = Image((img, 0.1))
    

    
            



            
    
            
            
            
            
            
            
            
            