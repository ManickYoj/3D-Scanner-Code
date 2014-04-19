"""
mesh.py
-------
Author: Nick Francisci
Status: Incomplete & Untested
Description: 
A storage unit for meshs both as they are scanned and after a scan is complete.
The mesh class also supports export methods.

"""

import csv

class mesh(object):
    def __init__(self, name=None):
        self.mesh = [];
        self.name = name;
    
    # ----- General Public Methods ----- #

    def addPoint(self, Point):
    	""" Adds a tuple of a point's (x,y,z) onto the mesh object. """
        self.mesh.append(Point);

    def addPoints(self, Points):
    	""" Adds a list of tuples of points's (x,y,z) values onto the mesh object. """
    	self.mesh.extend(Points);

    def setName(self, name):
    	""" Setter method for an optional name field for a potential GUI feature. """
    	self.name = name;

    def getName(self):
    	""" Getter method for an optional name field for potential GUI feature. """
    	return self.name;

   	# ----- Public Export Methods ----- #

    def exportAsCSV(self, filename, filepath = None):
    	""" Exports a file in excel CSV format. """
    	with open(filename + '.csv', 'wb') as expFile:
    		w = csv.writer(expFile);
    		w.writerows(self.mesh);

    def exportAsOBJ(self, filename, filepath = None):
        #TODO: Implement
        return;