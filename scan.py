"""
scan.py
-------
Author: Nick Francisci
Status: Untested
Description: 
The main class for an instance of the scanning program. 
This class should serve as the complete UI for the program.

TODO: See findHardware() & exportMesh()
"""

import hardwareInterfaceClass as h
import imageClass as i
import meshClass as m
import time


class scan(object):

	def __init__(self, resolution = 1, verbose = False, debug = False):
		"""
		Initilizes the scanner with the given parameters.

		Arguments:
			- resolution: the desired fidelity of the scan as a float. A resolution of 1 will take 6 images.
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
		self.setResolution(resolution);
		self.mesh = m.mesh();
		self.hardware = self.findHardware();


	def setResolution(self, resolution):
		""" 
		Sets or resets the resolution of the scan class. 

		Arguments: 
			- resolution = the desired value of resolution
		"""

		self.resolution = resolution;
		if self.verbose:
			print "Resolution set to " + resolution;


	def findHardware(self):
		""" 
		Finds the existing instance of hardware and returns a reference to it. 

		Returns: the current instance of the hardware class to use.
		"""

		#TODO: Actually find the hardware!
		return h.hardwareInterface(1/self.resolution);


	def scan(self, lockWaitTime = 1):
		"""
		Performs a single scan.

		Arguments:
			- lockWaitTime: the amount of time for the scanner to wait between attempts to access the hardware.
		"""

		# Setup hardware lock
		while(self.hardware.isLocked()):
			time.sleep(lockWaitTime);
		self.hardware.toggleLock();

		self.hardware.setStepSize(1/self.resolution);

		# Scan an object
		for (i = 0; i<2*math.pi; i+(1/self.resolution)):
			if self.verbose:
				print "Taking image " + i + " of " + int(2*math.pi/self.resolution);
			newImage = i.image(self.hardware.singleImageCap(), self.hardware.getRotation);
			self.hardware.advanceTurntable();
			self.mesh.addPoints(newImage.getPointsFromImage());

		if self.verbose:
			print "Image capture complete.";

		# Release hardware lock
		self.hardware.toggleLock();


	def exportMesh(self, export_file_type = "OBJ", filepath = None):
		"""
		Exports the mesh as a file if the requested filetype is supported.

		Arguments:
			- export_file_type: a string indicating the desired filetype in format "OBJ" or ".OBJ"
			- filepath: (currently unsupported) a string indicating where to save the file if not the directory of this program.
		"""

		#TODO: Actually support these operations in the mesh class
		#TODO: Support the filepath argument

		export_file_type.upper();

		if (export_file_type is in ["OBJ", ".OBJ"]):
			self.mesh.exportAsOBJ(filepath);
		else:
			print "The inputted file type is not supported.";


if __name__ == "__main__":
		s = scan(verbose = True);
		print "Beginning scan...";
		s.scan();
		s.exportMesh();