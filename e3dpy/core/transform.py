from pyrr import Quaternion, matrix44, Matrix44, Vector3
from .utils import *

class Transform:
    """
        This class will manage the basic transformation that can be
        performed to a geometry.

        This class uses pyrr module that it's a packadge with many
        operations that can be used directly with OpenGL. In this class
        the selected approach will be Object Oriented because its features.
        Documentation can be founf in the following link:
        
        https://github.com/adamlwgriffiths/Pyrr

        Parameters:
            default position, rotation and scale can be set intially.
        
        To-Do:
            Pivot implementation. So it's rotate based on a point.
            Advanced transformations such as shear, bend, twist, et..

    """
    def __init__(self, position=None, rotation=None, scale=None):
        # Create private members for the setters (properties)
        self.__position = self._get_Vector3(position)
        self.__rotation = self._get_Vector3(rotation)
        self.__scale = self._get_Vector3(scale)
        # Initiali<e variables and Window
        self._initialize()

    def _get_Vector3(self, value):
        if empty(value):
            return None
        # Check if it's already a Vector3 instance
        if isinstance(value,(Vector3)):
            return value
        else:
            return Vector3(value)

    def _initialize(self):
         # Create default transformations: position, rotation and scale
        if self.position is None:
            self.position = Vector3([0.0,0.0,0.0])
        if self.rotation is None:
            self.rotation = Vector3([0.0,0.0,0.0])
        if self.scale is None:
            self.scale = Vector3([1.0,1.0,1.0])

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = self._get_Vector3(value)

    @property
    def rotation(self):
        return self.__rotation

    @rotation.setter
    def rotation(self, value):
        self.__rotation = self._get_Vector3(value)

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, value):
        self.__scale = self._get_Vector3(value)

    @property
    def model(self):
        """
            This property will perform the current transformation and
            return a 4x4 matrix with the  transformation matrix. This
            matrix could be send to the shader so it can perform the
            model-view transformation for any geometry
        """
        # Create scale matrix transformation
        scale = Matrix44.from_scale(self.scale)

        #Convert the current degrees vector into radians
        rotation = np.radians(self.rotation)
        rotationY = Quaternion.from_x_rotation(rotation.x)
        rotationX = Quaternion.from_y_rotation(rotation.y)
        rotationZ = Quaternion.from_z_rotation(rotation.z)
        # compute all rotations.
        rotation = rotationX * rotationY * rotationZ

        # Create translation matrix transformation
        translation = Matrix44.from_translation(self.position)

        # Compute transformation matrix. convert to float32
        return  np.array(scale * rotation * translation,dtype=np.float32)

    def transform(self, point):
        """
            This function will apply the current transformation to
            the following point. 
        """
        # Get the current tranformation matrix
        matrix = self.model
        # transform our point by the matrix to model-view
        return matrix * self._get_Vector3(point)

    def __enter__(self):
        # Enter will always return the object itself. Use with With expressons
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Clean all the memery stored
        self._dispose()

    def _dispose(self):
        pass