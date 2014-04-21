Author: Nick Francisci
Description: An outline for all of the objects used in the laser scanning software and their public interfaces.
========================

class scan
	""" 
	The wrapper class for an instance of the program.
	"""

	has a list of meshObjects
	has a Hardware class (which may be shared with other instances of this class)
	has a default resolution attribute

	public function init([opt.] resolution)
		"""
		Initilizes the class for scanning
		"""

		Arguments:
		- resolution: the default resolution desired for scans. Defaults to the setResolution default.

		"""

	public function scan([opt.] resolution):
		"""
		Locks the hardware, scans a new object, and adds it to the list of mesh objects.

		Arguments:
			- resolution: the resolution to use for the scan if not the default setting.

		"""

	public function exportMesh(export_file_type, [opt.] mesh_index):
		"""
		Exports the mesh as the specified file type or prints a statement that the requested file type is not supported. This function wraps the meshObject export functions.

		Arguments:
		- export_file_type: the name (as a string) of the type of file to be exported
		- mesh_index: the index of the mesh in the list of meshObjects to be exported. Defaults to the most recently scanned mesh.

		"""

	public function setResolution([opt.] resolution):
		"""
		Sets the default resolution.

		Arguments: 
			- resolution: the value with which to update the default resolution. Defaults to 4.

		"""



class Hardware
	""" All methods pretaining to hardware sensing and actuation """

	has a locked boolean attribute
	has an isdone boolean attribute
	has an avgvel numeric attribute

	public function init()
		""" Sets up class variables. """

	public function islocked()
		""" Returns the value of the the locked attribute. """

	public function togglelock()
		""" Inverts the value of the locked attribute. """

	public function isdone()
		""" Returns the value of the isdone attribute. """

	public function beginscan()
		""" 
		Starts the turntable rotation and returns once the hardware is prepped to take images.
		"""

	public getavgvel():
		""" Returns the angular velocity of the last. """

	public function captureimage()
		""" 
		Takes and returns one image.

		Returns:
		- a numpy array representing an image
		- the time it was taken after the image capturing rotation was done
		"""



class imageObject
	has an image file attribute
	has a timestamp attribute

	public function init(image, timestamp):
		""" Stores the image and timestamp. """

	public function getpoints((start_timestamp, dTheta/dt)):
		"""
		Gets a list of points ((x, y, z) tuples) based on filtering the image and transforming from polar to euclidean representation.

		Arguments:
		- A tuple (start_timestamp, dTheta/dt) of the time the scan rotation started and the angular velocity of the rotation.

		Returns :
		- List of (x,y,z) tuples
		"""



class meshObject
	has a mesh (unordered list of points as (x,y,z) tuples in euclidean space)

	public function addPoints(Points)
		"""
		Adds the inputed points to the mesh.

		Arguments:
		- Points: an unordered list of points as (x,y,z) tuples in euclidean space.	

		Returns: None	
		"""

	public function exportAs*()
		"""
		Exports mesh as * filetype. (There will be multiple functions of this description with a different *).

		Arguments: None

		Returns: None
		"""