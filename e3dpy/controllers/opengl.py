import ctypes
import numpy as np
import OpenGL.GL as GL
from ..core.utils import *
from ..core.constants import DrawMode, UsageMode
from ..core.controllers import Render

__all__ = ['OpenGLShader', 
           'OpenGLTexture',
           'OpenGLBuffer',
           'OpenGLRender',
           'Thread']

opengl_usagemode_wrapper = {
    UsageMode.stream_draw  : GL.GL_STREAM_DRAW,
    UsageMode.stream_read  : GL.GL_STREAM_READ,
    UsageMode.stream_copy  : GL.GL_STREAM_COPY,
    UsageMode.static_draw  : GL.GL_STATIC_DRAW,
    UsageMode.static_read  : GL.GL_STATIC_READ,
    UsageMode.static_copy  : GL.GL_STATIC_COPY,
    UsageMode.dynamic_draw : GL.GL_DYNAMIC_DRAW,
    UsageMode.dynamic_read : GL.GL_DYNAMIC_READ,
    UsageMode.dynamic_copy : GL.GL_DYNAMIC_COPY 
}

opengl_drawmode_wrapper = {
    DrawMode.triangles    : GL.GL_TRIANGLES,
    DrawMode.points       : GL.GL_POINTS,
    DrawMode.lines        : GL.GL_LINES, 
    DrawMode.quads        : GL.GL_QUADS,
    DrawMode.tfan         : GL.GL_TRIANGLE_FAN,
    DrawMode.lstrip       : GL.GL_LINE_STRIP,
    DrawMode. tstrip      : GL.GL_TRIANGLE_STRIP,
}

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

def gldtype(dtype):
    """
        This function will convert the types supported by OpenGL from
        numpy types. 
        If dtype is not founded into the GLtypes the function will
        return GL.GL_FLOAT as default Open GL type
    """
    # Check for some posibilities with the input, np.int32, 'int32','np.int32'
    if isinstance(dtype, (np.dtype)):
        dtype = dtype.name
    elif not isinstance(dtype, (str)):
        dtype = dtype.__name__
    # get the second part in case it can be splitted
    if len(dtype.split(".")) > 1:
        dtype = dtype.split(".")[-1]
    #Check the type of data has to be converted
    datatypes = {
        "int8"     :    GL.GL_BYTE, 			
        "uint8"    :    GL.GL_UNSIGNED_BYTE,	
	    "int16"    :    GL.GL_SHORT,			
	    "uint16"   :    GL.GL_UNSIGNED_SHORT,	
	    "int32"    :    GL.GL_INT,				
	    "uint32"   :    GL.GL_UNSIGNED_INT,		
	    "float16"  :    GL.GL_HALF_FLOAT,		
	    "float32"  :    GL.GL_FLOAT,			
	    "float64"  :    GL.GL_DOUBLE,
        "fixed"    :    GL.GL_FIXED # More compatibility for OS (float32)
    }	
    # Check if the current datatype exists
    if dtype in datatypes:		
        return datatypes[dtype]
    # if the data type does't exit returns default GL type
    return datatypes[np.float32]

class OpenGLShader:
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

class OpenGLTexture:
    """
        This class will create and store all the elements needed
        to create the texture.
        The module needed to load the images is Pillow
            from PIL import Image
    """
    # Maximun number of textures
    max_textures = 32

    def __init__(self, filename):
        # Initialize all the variables
        self.filename = filename
        # Create a texture variable with the pointer to the buffer
        self._texture = None
        # Initiali<e variables and Window
        self._initialize()

    def __enter__(self):
        # Enter will always return the object itself. Use with With expressons
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Clean all the memery stored
        self._dispose()

    def _dispose(self):
        pass

    def _initialize(self):
        # Create the texture and copy into OpenGL
        self._texture = self._load_Texture(self.filename)

    def _load_Texture(self,filename):
        # Check if the file exists
        if file_exists(filename):
            # Load the image using the path configured
            img_data, size = load_image(filename)
            width, height = size
            # Generate texture buffer to load into GPU
            texture = GL.glGenTextures(1)
            # Set initial parameters needed prior send the image to OpenGL
            GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
            # Bind current texture buffer to load the data
            GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
            # Set parameters to tell OpenGL how to draw the image
            GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
            GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR_MIPMAP_LINEAR)
            GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
            GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
            GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, width, height, 0,
                            GL.GL_RGB, gldtype(img_data.dtype), img_data)
            # Create different Mipmaps for the current texure
            GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
            return texture
        # If not exist return None
        return None
    
    def bind(self, count):
        """
            This method will bind the current texture to be used to the graphic card
            Parameter:
                count: this is used to assign a free slot to the texture into OpenGL
                    [   Some graphic cards could have a limitation in the number of   ]
                    [   textures that can store, depending on the memory.             ]
        """
        if self._texture and (count > 0 and count < Texture.max_textures + 1 ):
            # Following we will activate the texture in a slot 
            GL.glActiveTexture(GL.GL_TEXTURE0 + count)
            GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture)

class OpenGLRender(Render):
    """
        This Class will render the Buffers stored in GPU
        openGL. It will use OpenGL and a double buffer so
        it can sweep between the buffers per frame.
    """

    # Default Background Color
    defaulBGColor = [0.0, 0.0, 0.0, 1.0]

    def __init__(self, *args, **kwargs):
        """ Initialize the Render Class
        """
        super().__init__(*args, **kwargs)

    def init(self):
         """ This function will initialize OpenGL with some functions
         by default. This case depth test is enabled by default initially.
         """
         GL.glEnable(GL.GL_DEPTH_TEST)

    def clear(self, color = defaulBGColor):
        """ This function wll clean the buffers on the GPU
        """
        GL.glClearColor(*color)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    def render(self):
        """
        """
        # Bind the created Vertex Array Object
        GL.glBindVertexArray(self._VAO)
        # Draw the current geoemtry. Check if indices have been added
        if self._has_indices():
            GL.glDrawElements(self.mode, len(self._dfPrims.index) * 3, 
                              typeGL(Geometry.index_type), ctypes.c_void_p(0))
        else:
            GL.glDrawArrays(self.mode, 0, len(self._dfPoints.index))
        # Unbind VAO from GPU
        GL.glBindVertexArray(0)
     
class OpenGLBuffer(object):
    """
        This element will create and store all the elements needed
        to Render a Geometrt
    """
  
    def __init__(self, usage=UsageMode.static_draw):
        # Initialize all the variables
        self.usage = usage
        # Vertex Array Object for all the Attributtes, elements, etc.
        self._VAO = None
        # Vertex Arrays Buffers for all the Attributes
        self._VAB = {}
        # Element Array Buffers for all the Attrbiutes
        self._EAB = None

    def _dispose(self):
        # Dispose all the objects and memory allocated
        GL.glDeleteVertexArrays(1,self._VAO)

    def _create_vertex_buffer_array(self, name, attribute_name = None):
        """
            This function only make sense to do when working with
            points (vertex) attributes.S
            The function  will return the bind attribute attached
            to the shader. This could be stored into a list to 
            detach later when copy all the buffers and after unbind
            VAO object.
        """
        # Check if not attribute name has been mapped for the bidinng
        if attribute_name is None:
            attribute_name = name
        # Get the current vertices (flatten is not needed)
        vertices = self._dfPoints[self._pointAttribCols[name]].values
        # Create the vertex array buffer and send the positions into the GPU buffers
        self._VAB[name] = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._VAB[name] )
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, self.usage)

        # Bind Attribute to the current shader. 
        return self.shader.bind(attribute_name, len(vertices[0]), vertices.dtype)

    def _copy_to_buffer(self):
        # Bind the shaders attributes for the current geometry
        if self.shader is None:
            print("ERROR: No shader specified")
      
        # Create a list with the attributes created and binded
        shader_attributes = []

        # Create a new VAO (Vertex Array Object). Only (1) VAO.
        #   Note. Using bpp > 16bits doesn't work. This depend on the Graphic Card.
        self._VAO = GL.glGenVertexArrays(1)
        # Every time we want to use VAO we just have to bind it
        GL.glBindVertexArray(self._VAO)

        # Create the first attribute "position" (location = 0) (Mandatory)
        shader_attributes.append(self._create_vertex_buffer_array("P","position"))
        
        # Check wether the geometry has indexes
        if self._has_indices():
            # Get the current indices (flatten)
            indices = self._dfPrims[self._primAttribCols["Id"]].values
            # Create the element array buffer and send the positions into the GPU buffers
            self._EAB = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER,  self._EAB);
            GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, self.usage);
        
        # Create and bind other Attributes
        for attrib in self._pointAttribCols.keys():
            if attrib != "P":
                shader_attributes.append(self._create_vertex_buffer_array(attrib))

        # Unbind VAO from OpenGL. Set to None = 0
        GL.glBindVertexArray(0)
        # Remove and unbind buffers
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        # Unbind all the Attributes "position" + Additionals
        for attribute in shader_attributes:
            self.shader.unbind(attribute)
  
    def update(self):
        # Depenging on the method to update the vertices using GPU or 
        # inmediate OpenGL the update will be different.
        self._copy_to_buffer()
