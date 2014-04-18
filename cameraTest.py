# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 12:02:02 2014

@author: koenigin
"""

import cv2.cv
import cv2
import numpy as np


def singleImageCap(camera):
    '''Code below will use the camera to capture a single image'''
    # Initialize the camera    
    capture = cv2.cv.CaptureFromCAM(camera)  # 0 -> index of camera
    if capture:     # Camera initialized without any errors
       f = cv2.cv.QueryFrame(capture)     # capture the frame
       if f:
#           ShowImage("cam-test",f)
#           WaitKey(0)
            cv2.cv.SaveImage('capture.jpeg', f)
            return 'capture.jpeg'
        
def filterForRed(image):
    '''will take in the image that the camera has just captured and filter
    so that only the red remains'''
        
    copy = image
    # Convert BGR to HSVimage
    hsv = cv2.cvtColor(copy, cv2.COLOR_BGR2HSV)
    
    # define range of laser color in HSV        
    lower_red = np.array([0,100,100])
    upper_red = np.array([45,255,255])
    
    # Threshold the HSV image to get only laser colors
    mask = cv2.inRange(hsv, np.uint8(lower_red), np.uint8(upper_red))
    kernel = np.ones((9,9),np.uint8)
    closed_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # Bitwise-AND mask and original image
    #res = cv2.bitwise_and(copy,mask, mask= closed_mask)
    
#    cv2.imshow('copy', copy)
#    cv2.waitKey(0)
    return mask
pic = cv2.imread(singleImageCap(1))    
cv2.imshow('pic', pic)
cv2.waitKey(0)
cv2.imshow('red filtered', filterForRed(pic)) 
cv2.waitKey(0)
print filterForRed(pic).shape  


def rememberOnlyRed(image):
    '''Takes in an image and returns a list of the the average red position in each row'''
    Red = []
    c =[]
    #should create a list of the columns containing red values in every row
    for row in range(image.shape(0)):
        for column in range(image.shape(1)):
            if image[row, column] != 0:
                c.append(column)
        #if red values exist, add them to Red otherwise add the number 0 to red
        if len(c) >= 0:
            Red.append(c)
        else:
            Red.append(0)
    for index in len(Red):
        #should keep just the average value for the rows that red exists, in every column
        sum = 0
        for value in range(len(Red[index])):
            sum += value
        Red[index] = sum/len(Red[index])
    return Red
    
Y = 5           #distance in cm b/n cameraline and laser
X = 9.8         #distance in cm from camera to center
H = 10.95       #distance in cm from laser to center      
def findColumnOffset(Y, H, redPosition):
    '''Takes in the original camera/laxer position parameters and uses them
    to calculate the depth of the object we are measuring for a single lazer
    image'''
    coordinates = []
    for index in range(len(redPosition)):
        height = len(redPosition) - index
        yPrime = redPosition[index] - Y
        depth = H*yPrime/Y
        coordinates.append((height, depth))
        
    
              
                
    
        



