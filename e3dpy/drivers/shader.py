import ctypes
import numpy as np
import OpenGL.GL as GL
from ..core.fileutils import *
from .utils import *

  
# Shader typas allow and extension for the files to use
ShaderTypes = {
    "VERTEX_SHADER"     : { "id":"vs", "type":GL.GL_VERTEX_SHADER   }, 
    "FRAGMENT_SHADER"   : { "id":"fs", "type":GL.GL_FRAGMENT_SHADER },
    "GEOMETRY_SHADER"   : { "id":"gs", "type":GL.GL_GEOMETRY_SHADER }
    }

# Transforms types availabile in shader
TransformTypes = {
    "WORLD_MATRIX"        : { "name":"world_matrix",      "size":16, "dtype":np.float32 }, 
    "VIEW_MATRIX"         : { "name":"view_matrix",       "size":16, "dtype":np.float32 },    
    "PROJECTION_MATRIX"   : { "name":"projection_matrix", "size":16, "dtype":np.float32 }
    }

# Transforms types availabile in shader
GeometryAttributeTypes = {
    "TEXTURE_COORDINATES"   : { "name":"v_textcoord", "size":2, "dtype":np.float32 },       
    "NORMAL"                : { "name":"v_normal",    "size":3, "dtype":np.float32 },      
    "POSITION"              : { "name":"v_pos",       "size":3, "dtype":np.float32 },     
    "COLOR"                 : { "name":"v_color",     "size":4, "dtype":np.float32 }
    }

class Shader:
    """
        This element will create and store all the elements needed
        to create a shader.
    """

    # Shaders types
    shader_types = ShaderTypes

    # These are the default transforms that will be used
    uniform_transforms = TransformTypes
    
    def __init__(self, name=None, filepath="./"):
        # Initialize all the variables
        self.name = name
        self.filepath = filepath
        # Initial variables
        self._shaders = {}
        self._uniforms = {}
        self._program = None
        # variable to tell if the shader has been initialized correctly
        self.initialized = False
        # Initiali<e variables and Window
        self._initialize()

    def __enter__(self):
        # Enter will always return the object itself. Use with With expressons
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Clean all the memery stored
        self._dispose()

    def _dispose(self):
        # Dispose all the object and memory allocated
        for shader in self._shaders:
            GL.glDetachShader(self._program, self._shaders[shader])
            GL.glDeleleShader(self._shaders[shader])
        # Delete Shader Program
        if self._program:
            GL.glDeleteProgram(self._program)
        # Set initialized to false
        self.initialized = False

    def _initialize(self):
        # Dispose previous elemens created
        self._dispose()
        # Create the variables needed for the shader program
        self._shaders = {}
        self._uniforms = {}

        # Set initialized to false
        self.initialized = False

        # Create the main shader program
        self._program = GL.glCreateProgram()
        
        # Arrach the default shaders to the current program
        self._attach_default_shaders()

        # Bind and mapping the default attributes variables to the shader
        #   - Bind location must be done before the linking process.
        #   - Get  location must be done after the linking process.
        self._bind_location_attributes()

        # Link the current shader program
        GL.glLinkProgram(self._program)
        # Check for link errors                
        if self._check_shader_error(self._program, GL.GL_LINK_STATUS,True):    
            return
        
        # Validate Program
        GL.glValidateProgram(self._program)
         # Check for link errors                
        if self._check_shader_error(self._program, GL.GL_VALIDATE_STATUS,True):
            return
                        
        # Get location uniforms variablesfrom the shader
        self._get_location_uniforms()

        # if all ok then set initialized to true
        self.initialized = True

    def _get_location_uniforms(self):
        for key,value in Shader.uniform_transforms.items():
            # Get the location for the curren shader loaded
            self._uniforms[key] = GL.glGetUniformLocation(self._program, value["name"])

    def _bind_location_attributes(self):
        pass

    def _attach_default_shaders(self):
        # Generate the main path for the shaders to load
        filename = self.filepath + "/" + self.name + "."
        # Read all shader type files and link into the progrma
        for key,value in Shader.shader_types.items():
            shader = self._load_shader(filename + value["id"], value["type"])
            # Check the current shader has been loaded correctly
            if shader:
                # Finally attach the current shader into the program
                GL.glAttachShader(self._program, shader)
                # Add current shader
                self._shaders[key] = shader

    def _load_shader(self, filename, shader_type):
        # Check if the file exists
        if file_exists(filename):
            #Load current shader code-source from file
            shader_source = read_file(filename)
            # Create curent shader
            shader = GL.glCreateShader(shader_type)
            # Set the source for the current sshader
            GL.glShaderSource(shader, shader_source) 
            # Compile current shadershader
            GL.glCompileShader(shader)
            # Check for compiler errors                
            if self._check_shader_error(shader, GL.GL_COMPILE_STATUS):
                return None
            # Return the current shader
            return shader
        #Return None if no file exists
        return None

    def _check_shader_error(self,shader,status,isProgram=False):
        if isProgram:
            # Check for errors in Programs               
            if GL.glGetProgramiv(shader,status) != GL.GL_TRUE:
                print('Program load failed: {}'.format(GL.glGetProgramInfoLog(shader)))
                return True
        else:
            # Check for errors in Shaders                
            if GL.glGetShaderiv(shader,status) != GL.GL_TRUE:
                print('Shader load failed: {}'.format(GL.glGetShaderInfoLog(shader)))
                return True
        return False    

    def load(self, name):
        # Set the current file and initialize
        self.name = name
        # Call to initialize so it will load again the program and shader
        self._initialize()

    def use(self,use=True):
        """
            Function to tell Open GL to use this Shader program.
            If the shader won't be used anymore then use use=False.
        """
        if self.initialized:
            # Tell Open GL to use/not-use the current progrma
            if use:
                GL.glUseProgram(self._program)
            else:
                GL.glUseProgram(0)
            return True
        # Not initialized
        return False

    def bind(self, attribute_name, size, dtype=np.float32):
        """
            This function will allow to bind attributes from the array buffer object
            to the shader. This operation will be done per VAO since it can store this
            binding. Again when a VAO will be opened and binding to OpenGL, this
            will bind again all the bindings previously performed during the creation.

            After unbind the current VAO and after loading all the buffers needed
            is very convenient to unbind the attribute after.

            Parameters:
                attribute_name (str): 
                    name of the attribute to use into the shader source-code.
                size:
                    size of the current attribute. This is the number of elements, not
                    de number of bytes etc.. ej. vector3 will have size = 3
                dtype:
                    data-type of the values for the given attribute. If the vector contains
                    int, float32, unit32, etc.. This must be given using GL types. Use
                    typeGL function to convert numpy types into OpenGL types

        """
        if self.initialized:
            # Get the location of the 'attribute_name' in parameter of our shader and bind it.
            attribute_id = GL.glGetAttribLocation(self._program, attribute_name)
            # Check if the current attribute is in the Shader
            if attribute_id != -1:
                #Enable current attribute in the shader
                GL.glEnableVertexAttribArray(attribute_id)
                # Describe the attribute data layout in the buffer
                GL.glVertexAttribPointer(attribute_id, size, gldtype(dtype),
                                    False, 0, ctypes.c_void_p(0))
                # Return the attribute id
                return attribute_id
            else:
                # Attribute has been discarted for the compiler or doesn't exist.
                print ("Warning: Current attribute {} is not in the shader".format(attribute_name))
        # Return false is not initialized
        return False

    def unbind(self, attribute_id):
        """
            This operation will be performed after unbind the VAO obhect. The parameter
            needed will be the result of the previous result that the bind function call
            returns with the attribute id.
        """
        if self.initialized:
            # Unbind Attribute
            GL.glDisableVertexAttribArray(attribute_id)
        
    def update(self, name, value):
        # Depending on the uniform name to update we have to select the proper operator.
        GL.glUniformMatrix4fv(self._uniforms[name], 1, GL.GL_FALSE, value)