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

class Scan(object):
	""" The wrapper class for the program. """
	
	def __init__(self, resolution = None, verbose = False, debug = False):
		"""
		Initilizes the scanner with the given parameters.

		Arguments:
			- resolution: the desired fidelity of the scan. A resolution of 1 will take 6 images. Defaults to the setresolution default.
			- verbose: a boolean used to run this class with additional output text indicating its current state.
			- debug: a boolean used to run extra debug operations. Debug mode will automatically enable verbose mode.
		"""

		# Initilize debug attributes
		self.debug = debug;
		if verbose or debug:
			self.verbose = True;
		else:
			self.verbose = False;

		# Initilize class attributes
		self.setresolution(resolution);
		self.hardware = self.findhardware();
        self.meshs = [];


	def setresolution(self, resolution = None):
		""" 
		Sets or resets the resolution of the scan class. 

		Arguments: 
			- resolution = the desired value of resolution
		"""

		if resolution == None:
			resolution = 4;
        
		self.resolution = resolution;
		if self.verbose:
			print "Resolution set to " + resolution;


	def findhardware(self):
		""" 
		Finds the existing instance of hardware and returns a reference to it. 

		Returns: the current instance of the hardware class to use.
		"""

		#TODO: Actually find the hardware!
		return hardware.Hardware(1/self.resolution);


	def scan(self, lockWaitTime = 1, name = None):
		"""
		Performs a single scan.

		Arguments:
			- lockWaitTime: the amount of time for the scanner to wait between attempts to access the hardware.
		"""

        # Construct and initialize a Queue of tuples of captured images (unprocessed) and time stamps
        img_queue = q.Queue();
        
        # Construct and initialize a new Thread for processing Images
        process_thread = t.Thread(target=begincapture)
                
        # Construct and initialize a Mesh object with the name mesh + index, EG mesh0
        if name = None:
        	name = "mesh" + str(len(self.meshs)
        mesh = m.Mesh(name = name)
        
		# Setup hardware lock
		while(self.hardware.isLocked()):
			time.sleep(lockWaitTime);
		self.hardware.toggleLock();

		#begin rotation, returns after one rotation (motor keeps rotating)
		self.hardware.beginscan();

		#begin taking in images
		processthread.run()
        
        # Keep checking for new captured images to process
        imglist=[]; 
    	while(not imgqueue.empty()):
          	# process the next image in queue and initializes as new Image
        	img= image.Image(imgqueue.get());
            # add to list of processed points
            imglist.append(img) 

		# Release hardware lock
		self.hardware.toggleLock();
        
        # add to mesh
        for i in imglist:
          onemesh.addpoints(i.getpoints());
        self.meshs.append(onemesh)
        
    def begincapture():
        """ Scans an object """
		i=0;
        while(i<2*math.pi):
          
			if self.verbose:
				print "Taking image " + i + " of " + int(2*math.pi/self.resolution);
                
                # adds a new (imgfile, timestamp) tuple to the queue
                imgqueue.put(self.hardware.captureimage()); 
                i=i+(1/self.resolution);                     

		if self.verbose:
			print "Image capture complete.";



	def exportmesh(self, mesh_index = None, export_file_type = "CSV", filename = None):
		"""
		Exports the mesh as a file if the requested filetype is supported.

		Arguments:
			- export_file_type: a string indicating the desired filetype.
			- filename: a string indicating the desired name of the saved file.
		"""

		#TODO: Actually support these operations in the mesh class
		#TODO: Support the filepath argument

		export_file_type.upper();
		
		if mesh_index is None or mesh_index>len(self.meshs):
			mesh_index = self.meshs[-1]
		elif mesh_index < 0
			mesh_index = 0

		if export_file_type is in ["CSV", ".CSV"]:
			self.mesh.exportcsv(filename)
		else:
			print "The inputted file type is not supported."


if __name__ == "__main__":
		s = scan(verbose = True);
		print "Beginning scan...";
		s.scan();
		s.exportMesh();