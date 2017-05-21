from pyrr import Quaternion, matrix44, Matrix44, Vector3
from ..core.convert import *

class Camera:
    """
        This class will manage the basic functionality that can be
        performed with a camera.

        This class uses pyrr module that it's a packadge with many
        operations that can be used directly with OpenGL. In this class
        the selected approach will be Object Oriented because its features.
        Documentation can be founf in the following link:
        
        https://github.com/adamlwgriffiths/Pyrr

        Parameters:
            default perspective, rotation and scale can be set intially.
        
        To-Do:
            Pivot implementation. So it's rotate based on a point.
            Advanced transformations such as shear, bend, twist, et..

    """
    def __init__(self, position=[0.0,0.0,-3.0], fov=70.0, aspect=1.33, zNear=0.01, zFar=1000.0):
        # Create private members for the setters (properties)
        # View Matrix
        self.__position = Vector3(convert(position))
        self._forward = convert([0.0,0.0,1.0])
        self._up = convert([0.0,1.0,0.0])
        # Prejection Matrix
        self._fov = fov
        self._aspect = aspect
        self._zNear = zNear
        self._zFar = zFar
        
        # Initiali<e variables and Window
        self._initialize()

    def _initialize(self):
        pass

    def pan(self, value):
        """
            Rotate using up direction
        """
        

    def tilt(self, value):
        """
            Rotate using cross product between up and forward vectors.
        """
        pass

    def roll(self, value):
        """
            Rotate using the forward direction
        """
        pass

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = Vector3(convert(value))

    def setPerspective(fov=70.0, aspect=1.33, zNear=0.01, zFar=1000.0):
        """
            Redefine the perspective view of the Camera
        """
        self._fov = fov
        self._aspect = aspect
        self._zNear = zNear
        self._zFar = zFar
       
    @property
    def view(self):
        return self.lookAt(self.position,self.position + self._forward, self._up)

    def lookAt(self, position, target, up):
        ez = position - target
        ez = ez / np.linalg.norm(ez)

        ex = np.cross(up, ez)
        ex = ex / np.linalg.norm(ex)

        ey = np.cross(ez, ex)
        ey = ey / np.linalg.norm(ey)

        rmat = np.eye(4)
        rmat[0][0] = ex[0]
        rmat[0][1] = ex[1]
        rmat[0][2] = ex[2]

        rmat[1][0] = ey[0]
        rmat[1][1] = ey[1]
        rmat[1][2] = ey[2]

        rmat[2][0] = ez[0]
        rmat[2][1] = ez[1]
        rmat[2][2] = ez[2]

        tmat = np.eye(4)
        tmat[0][3] = -position[0]
        tmat[1][3] = -position[1]
        tmat[2][3] = -position[2]

        return np.dot(rmat, tmat).transpose()


    @property
    def projection(self):
        return matrix44.create_perspective_projection_matrix(self._fov,self._aspect,self._zNear,self._zFar)

    def __enter__(self):
        # Enter will always return the object itself. Use with With expressons
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Clean all the memery stored
        self._dispose()

    def _dispose(self):
        pass