# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 10:38:43 2014

@author: koenigin
"""


import cv2.cv
import cv2
import numpy as np

class image(object):
    
    def __init__(self, image, rotation):
        self.image = image
        self.rotation = rotation    #angle of rotation
        self.Y = 5                  #distance in cm b/n cameraline and laser
        self.X = 9.8                #distance in cm from camera to center
        self.H = 10.95              #distance in cm from laser to center 
    
    def filterForredPosition(self,image):
        '''will take in the image that the camera has just capturedPosition and filter
        so that only the redPosition remains'''
            
        copy = image
        # Convert BGR to HSVimage
        hsv = cv2.cvtColor(copy, cv2.COLOR_BGR2HSV)
        
        # define range of laser color in HSV        
        lower_redPosition = np.array([0,100,100])
        upper_redPosition = np.array([45,255,255])
        
        # Threshold the HSV image to get only laser colors
        mask = cv2.inRange(hsv, np.uint8(lower_redPosition), np.uint8(upper_redPosition))
        kernel = np.ones((9,9),np.uint8)
        closed_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        # Bitwise-AND mask and original image
        #res = cv2.bitwise_and(copy,mask, mask= closed_mask)
        
    #    cv2.imshow('copy', copy)
    #    cv2.waitKey(0)
        return closed_mask


    def rememberOnlyredPosition(self,image):
        '''Takes in an image and returns a list of the the average redPosition position in each row'''
        redPosition = []
        c =[]
        #should create a list of the columns containing redPosition values in every row
        for row in range(image.shape(0)):
            for column in range(image.shape(1)):
                if image[row, column] != 0:
                    c.append(column)
            #if redPosition values exist, add them to redPosition otherwise add the number 0 to redPosition
            if len(c) >= 0:
                redPosition.append(c)
            else:
                redPosition.append(-1)
        for index in len(redPosition):
            #should keep just the average value for the rows that redPosition exists, in every column
            sum = 0
            for value in range(len(redPosition[index])):
                sum += value
            redPosition[index] = sum/len(redPosition[index])
        return redPosition
        
    def cyl2Car(self, r, theta, height):
        '''takes in cylindrical coordinates and converts to cartesian'''
        x = r*np.cos(theta)
        y = r*np.sin(theta)
        z = height
        return (x, y, z)
        

    def getsPointsFromImage(self,redPositionPosition):
        '''Takes in the original camera/lazer position parameters and uses them
        to calculate the depth of the object we are measuring for a single lazer
        image'''
        coordinates = []
        for index in range(len(redPositionPosition)):
            height = len(redPositionPosition) - index
            yPrime = redPositionPosition[index] - self.Y
            depth = self.H*yPrime/self.Y
            coordinates.append(self.cyl2Car(depth, self.rotation, height))
        return coordinates
            
    
            
            
            
            
            
            
            
            