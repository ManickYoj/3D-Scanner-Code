"""
scan.py
-------
Author: Nick Francisci & Celine Ta
Status: Incomplete & Untested
Description: 
The main class for an instance of the scanning program. 

"""

import hardware, image, time
import mesh as m
import Queue as q
import threading as t
import cv2 

class Scan(object):
    """ The wrapper class for the program. """
    
    def __init__(self, resolution = None, verbose = False, debug = False):
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

    def setresolution(self, resolution = None):
        """ 
        Sets or resets the resolution of the scan class. 

        Arguments: 
            - resolution = the desired value of resolution
        """

        if resolution == None:
            resolution = 5.0
        
        self.resolution = resolution
        if self.verbose:
            print "Resolution set to " + str(resolution)


    def scan(self, lock_wait_time = 1, name = None):
        """
        Performs a single scan.

        Arguments:
            - lockWaitTime: the amount of time for the scanner to wait between attempts to access the hardware.
        """

        # Construct and initialize a Queue of tuples of captured images (unprocessed) and time stamps
        img_queue = q.Queue()
        
        # Construct and initialize a new Thread for processing Images
        process_thread = t.Thread(target=self.begincapture, args=[img_queue])
                
        # Construct and initialize a Mesh object with the name mesh + index, EG mesh0
        if name == None:
            name = "mesh" + str(len(self.meshs))
        mesh = m.Mesh(name = name)
        
        # Setup hardware lock
        while self.hardware.islocked():
            time.sleep(lock_wait_time)
        self.hardware.togglelock()

        #begin rotation, returns after one rotation (motor keeps rotating)
        self.hardware.beginscan()

        #begin taking and processing images
        process_thread.start()
        img_list = self.processimgs(img_queue)

        # Release hardware lock
        avg_vel = self.hardware.getavgvel()
        self.hardware.togglelock()
        
        # add points from image objects to mesh
        for i in img_list:
            mesh.addpoints(i.getpoints(avg_vel))

        # add mesh to the meshs list
        self.meshs.append(mesh)

        if self.verbose:
            print "Scan complete. Mesh is in index " + str(len(self.meshs)-1) + " of the mesh array."
            
        self.exportmesh()


    def exportmesh(self, mesh_index = None, export_file_type = "CSV", filename = None):
        """
        Exports the mesh as a file if the requested filetype is supported.

        Arguments:
            - export_file_type: a string indicating the desired filetype.
            - filename: a string indicating the desired name of the saved file.
        """

        export_file_type.upper()
        
        if mesh_index is None or mesh_index>len(self.meshs):
            mesh = self.meshs[-1]
        elif mesh_index < 0:
            mesh = self.meshes[0]

        if export_file_type in ["CSV", ".CSV"]:
            mesh.exportcsv(filename)
        else:
            print "The inputted file type is not supported."


    # ----- Private Methods ----- #

    def begincapture(self, img_queue):
        """ Scans an object """
        i = 0
        while not self.hardware.isdone():
          
            if self.verbose:
                print "Taking image number " + str(i)                
            # adds a the data to create a new image to the queue
            new_image=self.hardware.captureimage()
#            cv2.imshow('frame', new_image[0])
#            cv2.waitKey(0)
            img_queue.put(new_image)
            time.sleep(1/self.resolution)
            i += 1

        if self.verbose:
            print "Image capture complete."


    def processimgs(self, img_queue):
        """
        Check for new captured images to process.
        Returns an img_list of processed image objects once processing is complete. 
        """
        img_list=[]
        
        while not img_queue.empty() or not self.hardware.isdone():
            # process the next image in queue and initializes as new Image
            if not img_queue.empty():
                img = image.Image(img_queue.get())
                print(".")
                # add to list of processed points
                img_list.append(img) 

        return img_list


    def findhardware(self):
        """ 
        Finds the existing instance of hardware and returns a reference to it. 

        Returns: the current instance of the hardware class to use.
        """

        #TODO: Actually find the hardware!
        return hardware.Hardware(debug = self.debug)

# ----- Unit Testing ----- #

if __name__ == "__main__":
        s = Scan(debug = True)
        print "Beginning scan..."
        s.scan()
        print(s.meshs[0].mesh)
        s.exportmesh()