Author: Nick Francisci
Description: An outline for all of the objects used in the laser scanning software and their public interfaces.
========================

class scan
	""" 
	The wrapper class for an instance of the program.
	"""

	has a list of meshObjects
	has a hardwareInterface (which may be shared with other instances of this class)
	has a default resolution attribute

	public function init(hardware, [opt.] resolution)
		"""
		Initilizes the class for scanning
		"""

		Arguments:
		- hardware: the hardwareInterface object to use for data capture
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



class hardwareInterface
	""" All methods pretaining to hardware sensing and actuation """

	has a locked boolean attribute
	has a rotationComplete boolean attribute

	public function init()
		""" Sets up class variables. """

	public function isLocked()
		""" Returns the value of the the locked attribute. """

	public function toggleLock()
		""" Inverts the value of the locked attribute. """

	public function getRotation()
		""" Returns the value of the current_rotation attribute. """

	public function beginScan()
		""" 
		Sets the rotationComplete boolean to false. Begins the turntable's rotation, and returns after the warmup rotation is complete.
		Begins a thread to track the turntable rotation, stop it when it is done, and set the rotationComplete attribute to True.
		The turntable continues rotating after this function returns.
		"""

	public getRotationRegression():
		"""
		Returns a (timestamp, dTheta/dt) tuple representing the start time of the scan rotation and the speed of the turntable over the
		scan period.
		"""

	public function captureImage()
		""" 
		Takes and returns a picture.

		Arguments: None

		Returns:
		- an image file (probably a .jpeg)
		- a timestamp of when the image was taken
		"""



class imageObject
	has an image file attribute
	has a timestamp attribute

	public function init(image, timestamp):
		""" Stores the image and timestamp. """

	public function getPointsFromImage((start_timestamp, dTheta/dt)):
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