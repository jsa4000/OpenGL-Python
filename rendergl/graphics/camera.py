from math import sin, cos, radians
from pyrr import Quaternion, quaternion, matrix44, Matrix44, Vector3
from ..core.convert import *
from ..core.utils import *

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
    sensitivity = 0.1

    def __init__(self, position=[0.0,0.0,-3.0], fov=70.0, aspect=1.33, 
                       near=0.01, far=1000.0, orthorect = None, speed=0.05 ):
        # Create private members for the setters (properties)
        self._speed = speed

        # View Matrix
        self.__position = Vector3(convert(position))
        self._forward = normalize(convert([0.0,0.0,1.0]))
        self._up = normalize(convert([0.0,1.0,0.0]))
        self._side = normalize(np.cross(self._up, self._forward))
        # Projection Matrix
        self._fov = fov
        self._aspect = aspect
        self._orthorect = orthorect
        self._zNear = near
        self._zFar = far
   
        # Initiali<e variables
        self._initialize()

    def _initialize(self):
        pass
   
    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = Vector3(convert(value))
       
    @property
    def view(self):
        """It returns the matrix transformation for the current position and axis
        The current axis need to be already pointing to the target.
        """
        return self._look_at(self.position,self.position + self._forward, self._up)

    @property
    def perspective_projection(self):
        return matrix44.create_perspective_projection_matrix(self._fov,self._aspect,self._zNear,self._zFar)

    @property
    def orthogonal_projection(self,):
        """ [left, right, bottom, top]
        """
        return matrix44.create_orthogonal_projection_matrix(self._orthorect[0],self._orthorect[1],
                                                            self._orthorect[2],self._orthorect[3],
                                                            self._zNear,self._zFar)      
  
    def __enter__(self):
        # Enter will always return the object itself. Use with With expressons
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Clean all the memery stored
        self._dispose()

    def _dispose(self):
        pass

    def _update_camera_vectors(self):
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self._yaw)) * cos(radians(self._pitch))
        front.y = sin(radians(self._pitch))
        front.z = sin(radians(self._yaw)) * cos(radians(self._pitch))
        self._forward = normalize(front)
        self._side = vector.normalise(vector3.cross(self._forward, Vector3([0.0, 1.0, 0.0])))
        self._up = vector.normalise(vector3.cross(self._side, self._forward))

    def _look_at(self, position, target, up):
        """Method to set the camera to look at a target
        """
        # Get the new orientation from camera to target
        zaxis = normalize(position - target)
        # Get the rest of axises
        xaxis = normalize(np.cross(up, zaxis))
        yaxis = normalize(np.cross(zaxis, xaxis))
        # Create the matrix for the rotation
        rotation = np.eye(4)
        rotation[0,0:3] = xaxis[0:3]
        rotation[1,0:3] = yaxis[0:3]
        rotation[2,0:3] = zaxis[0:3]
        # Create the matrix for the translation
        translation = np.eye(4)
        translation[0:3,3] = -position[None,0:3]
        # Finally create the projection matrix and rotate (transpose)
        return np.dot(rotation, translation).transpose()

    def yaw(self, value):
        """Rotate using up direction
        """
        rotation = Quaternion.from_axis_rotation(self._up, value*self._speed)
        self._forward = normalize(quaternion.apply_to_vector(rotation, self._forward))
        self._side = normalize(np.cross(self._up, self._forward))

    def pitch(self, value):
        """ Rotate using cross product between up and forward vectors (side).
        """
        rotation = Quaternion.from_axis_rotation(self._side, value*self._speed)
        self._forward = normalize(quaternion.apply_to_vector(rotation, self._forward))
        self._up = normalize(np.cross(self._forward, self._side))
  
    def roll(self, value):
        """Rotate using the forward direction
        """
        rotation = Quaternion.from_axis_rotation(self._forward, value*self._speed)
        self._side = normalize(quaternion.apply_to_vector(rotation, self._side))
        self._up = normalize(np.cross(self._forward, self._side,))

    def orbit(self, target, x, y):
        pass
    
    def zoom(self, value):
        """Move towards the target (forward vector)
        """
        self.position += self._forward * (self._speed * -value)

    def strafe(self, value):
        """Move towards the side vector
            Rigth: value > 0
            Left:  value < 0
        """
        self.position += self._side * (self._speed * value)
  
    def orient(self,x,y):
        """ Orient the current camera with the current x,y 
        """
        self.yaw(x*self._speed)
        self.pitch(y*self._speed)

    def pan(self, x, y):
        """It moves the camera using the up and side vectors
        """
        # First move in the up direction
        self.position += self._up * (self._speed * y * Camera.sensitivity)
        self.position += self._side * (self._speed * x * Camera.sensitivity)
