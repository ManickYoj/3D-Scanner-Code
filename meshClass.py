# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 10:28:47 2014

@author: koenigin
"""

class mesh(object):
    def __init__(self):
        self.mesh = [];
        
    def addPoints(self, Points):
        self.mesh.append(Points);

    def exportAsOBJ(self, filepath = None):
        #TODO: Implement


