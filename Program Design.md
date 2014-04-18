Author: Nick Francisci
Description: An outline for all of the objects used in the laser scanning software and their public interfaces.
========================



class scan
	""" 
	The wrapper class for an instance of the program.
	"""

	has a meshObject
	has a hardwareInterface (which may be shared with other instances of this class)
	has a resolution attribute (default 1)

	public function init(hardware, resolution)
		"""
		Scans a new object into a mesh.

		1. Creates a lock on hardwareInterface when it becomes available.
		2. Runs a loop that, for the duration of 2*pi*resolution:
			a. Creates a new imageObject with hardwareInterface's captureImage() and getRotation()
			b. Calls the meshObject's addPoints() method with the current imageObject's getPointsFromImage() method
			c. Advances the turntable with harwareInterface
		3. Releases lock on hardwareInterface

		Arguments:
		- hardware: the hardwareInterface object to use for data capture

		Returns: None.
		"""

	public function exportMesh(export_file_type)
		"""
		Exports the mesh as the specified file type or prints a statement that the requested file type is not supported. This function wraps the meshObject export functions.

		Arguments:
		- export_file_type: the name (as a string) of the type of file to be exported

		Returns: None
		"""



class hardwareInterface
	""" All methods pretaining to hardware sensing and actuation """

	has a current_rotation attribute (default 0)
	has an locked boolean attribute
	has a step_size attribute (default=1) which is the inverse of resolution

	public function init(step_size)

	public function setStepSize(step_size)
		""" Sets the step_size attribute. """

	public function isLocked()
		""" Returns the value of the the locked attribute. """

	public function toggleLock()
		""" Inverts the value of the locked attribute. """

	public function getRotation()
		""" Returns the value of the current_rotation attribute. """

	public function advanceTurntable(amount)
		""" 
		Advances the turntable and adds that to the rotation variable. This function
		pauses the program until the rotation is complete.

		Arguments:
		- amount: the amount to rotate the turntable in radians
		"""

	public function captureImage()
		""" 
		Takes a picture.

		Arguments: None

		Returns:
		- an image file (probably a .jpeg)
		"""



class imageObject
	has an image file attribute
	has a rotation attribute

	public function init(image, rotation)

	public function getPointsFromImage()
		"""
		Gets a list of points ((x, y, z) tuples) based on filtering the image and transforming from polar to euclidean representation.

		Arguments: None

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