"""
mesh.py
-------
Author: Nick Francisci
Status: Complete & Tested
Description:
A storage unit for meshs both as they are scanned and after a scan is complete.
The mesh class also supports export methods.

"""

import csv
import os


class Mesh(object):

    """
    An object for holding a mesh before it is exported and providing those
    export methods.
    """

    def __init__(self, name=None, savefolder="Exported Meshes"):
        self.mesh = []
        self.name = name
        self.savefolder = savefolder

    # ----- General Public Methods ----- #

    def addpoint(self, point):
        """ Adds a tuple of a point's (x,y,z) onto the mesh object. """
        self.mesh.append(point)

    def addpoints(self, points):
        """ Adds a list of tuples of points's (x,y,z) values onto the mesh object. """
        self.mesh.extend(points)

    def setname(self, name):
        """ Setter method for an optional name field for a potential GUI feature. """
        self.name = name

    def getname(self):
        """ Getter method for an optional name field for potential GUI feature. """
        return self.name

    def setsavefolder(self, savefolder):
        """
        Setter method for the field that determines the name of the directory in
        which this mesh is saved.
        """

        self.savefolder = savefolder

    # ----- Public Export Methods ----- #

    def exportcsv(self, filename=None):
        """ Exports a file in excel CSV format. """

        filename = self.assignfilename(filename)
        with open(filename + '.csv', 'wb') as expfile:
            csvwriter = csv.writer(expfile)
            csvwriter.writerows(self.mesh)

    # ----- Private Export Helper Methods ----- #

    def assignfilename(self, filename):
        """
        A helper method for export methods that applies an appropriate
        filename if none is specified.
        """

        if filename is None:
            if self.name is not None:
                filename = self.name
            else:
                filename = "default"

        return self.assignfilepath(filename)

    def assignfilepath(self, filename):
        """
        A helper method for export methods that appends an appropriate
        file directory to the filename and creates that directory if it
        does not exist.
        """

        if not os.path.exists(self.savefolder):
            os.makedirs(self.savefolder)

        return os.path.join(self.savefolder, filename)


# ----- Unit Testing ----- #

def runtests():
    """ Runs methods of the Mesh class for testing. """

    testmesh = Mesh("Test File")
    testmesh.setname("Different Test File")
    testmesh.setsavefolder("Test Exports")

    testmesh.addpoint((15, 23, 34))
    testmesh.addpoints([(134, 23, 34), (32, 17, 35)])
    testmesh.exportcsv()

    print(testmesh.getname())
    print(testmesh.mesh)

if __name__ == "__main__":
    runtests()
