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

class Mesh(object):
    """
    An object for holding a mesh before it is exported and providing those
    export methods.
    """

    def __init__(self, name=None):
        self.mesh = []
        self.name = name
    
    # ----- General Public Methods ----- #

    def addpoint(self, point):
        """ Adds a tuple of a point's (x,y,z) onto the mesh object. """
        self.mesh.append(point)

    def addpoints(self, points):
        """ 
        Adds a list of tuples of points's (x,y,z) values onto the mesh object. 
        """
        self.mesh.extend(points)

    def setname(self, name):
        """ 
        Setter method for an optional name field for a potential GUI feature. 
        """
        self.name = name

    def getname(self):
        """
        Getter method for an optional name field for potential GUI feature.
        """
        return self.name

    # ----- Public Export Methods ----- #

    def exportcsv(self, filename):
        """ Exports a file in excel CSV format. """
        with open(filename + '.csv', 'wb') as expfile:
            csvwriter = csv.writer(expfile)
            csvwriter.writerows(self.mesh)


if __name__ == "__main__":
    TestMesh = Mesh()
    TestMesh.addpoint((15,23,34))
    TestMesh.addpoints([(134,23,34),(32,17,35)])
    print TestMesh.mesh