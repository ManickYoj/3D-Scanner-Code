Author: Nick Francisci
Description: An outline for all of the objects used in the laser scanning software and their public interfaces.
========================

class Scan
	""" 
	The wrapper class for an instance of the program.
	"""

	has a list of Mesh objects
	has a Hardware object (which may be shared with other instances of this class)
	has a resolution attribute

	public method init([opt.] resolution)
		"""
		Initilizes the class for scanning

		Arguments:
		- resolution: the default resolution desired for scans. Defaults to the setresolution default.
		"""

	public method scan([opt.] resolution):
		"""
		Locks the hardware, scans a new object into the list of mesh objects, and releases the hardware lock.

		Arguments:
			- resolution: the resolution to use for the scan if not the default setting.
		"""

	public method exportmesh(export_file_type, [opt.] mesh_index):
		"""
		Exports the mesh as the specified file type or prints a statement that the requested file type is not supported. This method wraps the Mesh object's export methods.

		Arguments:
		- export_file_type: the name (as a string) of the type of file to be exported
		- mesh_index: the index of the mesh in the list of Mesh objects to be exported. Defaults to the most recently scanned mesh.
		"""

	public method setresolution([opt.] resolution):
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

	public method init()
		""" Sets up class variables. """

	public method islocked()
		""" Returns the value of the the locked attribute. """

	public method togglelock()
		""" Inverts the value of the locked attribute. """

	public method isdone()
		""" Returns the value of the isdone attribute. """

	public method beginscan()
		""" 
		Starts the turntable rotation and returns once the hardware is prepped to take images.
		"""

	public getavgvel():
		""" Returns the angular velocity of the last. """

	public method captureimage()
		""" 
		Takes and returns one image.

		Returns:
		- a numpy array representing an image
		- the time it was taken after the image capturing rotation was done
		"""



class Image
	has an image_array attribute

	public method init(image_array, time_created):
		""" 
		Sets up the class variables for the object.

		Arguments:
		- image_array: a numpy array representing the image.
		- time_created: the time that the image was taken after the start of the rotation on which it was taken.
		"""

	public method getpoints(avg_vel):
		"""
		Gets a list of points ((x, y, z) tuples) based on filtering the image and transforming from polar to euclidean representation.

		Arguments:
		- avg_vel: the angular velocity of the rotation for this scan.

		Returns :
		- List of points as (x,y,z) tuples in euclidean space.
		"""



class Mesh
	has a mesh (unordered list of points as (x,y,z) tuples in euclidean space)
	has a name string
	has a savefolder string

	public method init([opt.] name, [opt.] savefolder):
		"""
		Sets up the class variables for the object.

		Arguments:
		- name: the name of the object. Defaults to a Nonetype
		- savefolder: the name of the folder in which to save the object. Defaults to "Exported Meshes"
		""

	public method addpoint(point):
		""" 
		Adds the inputted point to the mesh.

		Arguments:
		- point: an (x,y,z) tuple in euclidean space
		"""

	public method addpoints(points)
		"""
		Adds the inputed points to the mesh.

		Arguments:
		- points: an unordered list of points as (x,y,z) tuples in euclidean space.	
		"""

	public method setname(name):
		""" Setter method for the name attribute. """

	public method getname():
		""" Getter method for the name attribute. """

	public method setsavefolder(savefolder):
		""" Setter method for the savefolder attribute. """

	public method export*([opt.] filename)
		"""
		EG: exportcsv()

		Exports mesh as * filetype. (There will be multiple methods of this description with a different *).

		Arguments:
		- filename: the name to save the file with if not the mesh's name. Defaults to "default"

		Returns: None
		"""