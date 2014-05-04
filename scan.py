"""
scan.py
-------
Author: Nick Francisci & Celine Ta
Status: Complete & Tested
Description:
The main class for an instance of the scanning program.

"""

import hardware
import image
import time
import mesh as m
import Queue as q
import threading as t


class Scan(object):

    """ The wrapper class for the program. """

    def __init__(self, resolution=None, verbose=False, debug=False):
        """
        Initilizes the scanner with the given parameters.

        Arguments:
            - resolution: the desired fidelity of the scan. Defaults to the setresolution default.
            - verbose: a boolean used to run this class with additional output text indicating its current state.
            - debug: a boolean used to run extra debug operations. Debug mode will automatically enable verbose mode.
        """

        # Initilize debug attributes
        self.debug = debug
        if verbose or debug:
            self.verbose = True
        else:
            self.verbose = False

        # Initilize class attributes
        self.setresolution(resolution)
        self.hardware = self.findhardware()
        self.meshs = []

    # ----- Public Methods ----- #
    def setresolution(self, resolution=None):
        """
        Sets or resets the resolution of the scan class.

        Arguments:
            - resolution = the desired value of resolution
        """

        if not resolution:
            resolution = 6.0

        self.resolution = resolution
        if self.verbose:
            print("Resolution set to " + str(resolution))

    def scan(self, lock_wait_time=1, name=None):
        """
        Performs a single scan.

        Arguments:
            - lockWaitTime: the amount of time for the scanner to wait between attempts to access the hardware.
        """

        # Construct and initialize a Mesh object with the name mesh + index, EG mesh0
        if name is None:
            name = "mesh" + str(len(self.meshs))
        mesh = m.Mesh(name=name)

        # Setup hardware lock
        while self.hardware.islocked():
            time.sleep(lock_wait_time)
        self.hardware.togglelock()

        # Begin turntable rotation and start videocamera
        self.hardware.beginscan()

        #  Begin taking images at regular intrevals and processing when possible
        img_queue = q.Queue()
        t.Thread(target=self.begincapture, args=[img_queue]).start()
        img_list = self.processimgs(img_queue)

        # Collect average velocity from the hardware and release hardware lock
        avg_vel = self.hardware.getavgvel()
        self.hardware.togglelock()

        # Add points from image objects to mesh
        for i in img_list:
            points = i.getpoints(avg_vel)
            print points
            mesh.addpoints(points)
            

        # Add mesh to the meshs list
        self.meshs.append(mesh)

        if self.verbose:
            print("Scan complete. Mesh is in index " + str(len(self.meshs)-1) + " of the mesh array.")

    def exportmesh(self, mesh_index=None, export_file_type="CSV", filename=None):
        """
        Exports the mesh as a file if the requested filetype is supported.

        Arguments:
            - export_file_type: a string indicating the desired filetype.
            - filename: a string indicating the desired name of the saved file.
        """

        export_file_type.upper()

        if mesh_index is None or mesh_index > len(self.meshs):
            mesh = self.meshs[-1]
        elif mesh_index < 0:
            mesh = self.meshes[0]

        if export_file_type in ["CSV", ".CSV"]:
            mesh.exportcsv(filename)
        else:
            print("The inputted file type is not supported.")

    # ----- Private Methods ----- #
    def begincapture(self, img_queue):
        """
        Takes pictures at regular intervals and adds them to the queue
        of unprocessed images.
        """
        i = 0
        while not self.hardware.isdone():
            if self.verbose:
                print("Taking image number " + str(i))

            img_queue.put(self.hardware.captureimage())
            time.sleep(1.0/self.resolution)
            i += 1

        if self.verbose:
            print("Image capture complete.")

    def processimgs(self, img_queue):
        """
        Check for new captured images to process.
        Returns an img_list of processed image objects once processing is complete.
        """

        img_list = []
        i = 0
        while not img_queue.empty() or not self.hardware.isdone():
            try:
                print('initializing image ' + str(i))
                img = image.Image(img_queue.get(True, 0.25))
                img_list.append(img)
                i += 1
            except q.Empty:
                continue

        return img_list

    def findhardware(self):
        """
        Finds the existing instance of hardware and returns a reference to it.

        Returns: the current instance of the hardware class to use.
        """

        #TODO: Actually find the hardware!
        return hardware.Hardware(debug=self.debug)

# ----- Unit Testing ----- #
if __name__ == "__main__":
        s = Scan(resolution=10, debug=True)

        print("Beginning scan...")
        s.scan()
        s.exportmesh()
