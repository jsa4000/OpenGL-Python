import numpy as np
from ..core.utils import read_json
from ..core import Actions
from .geometry import Geometry
from .material import Material

def triangle():
    #Create default vertices 4f
    vertices = [ -0.5, -0.5, 0.0,
                0.0,  0.5, 0.0,
                0.5, -0.5, 0.0]
    indices = [ 0, 1, 2 ]
    colors = [ 1.0, 0.0, 0.0, 1.0,
            0.0, 1.0, 0.0, 1.0,
            0.0, 0.0, 1.0, 1.0]
    textcoords = [0.0, 0.0,
        0.5, 1.0,
        1.0, 0.0 ]

    return Geometry(vertices=vertices, 
                    indices=indices, 
                    colors=colors, 
                    textcoords=textcoords, 
                    size=[3,3,None,4,2])

def rectangle():
    vertices = [
        -0.5, -0.5, 0.0, 1.0,
        0.5, -0.5, 0.0, 1.0,
        0.5,  0.5, 0.0, 1.0,
        -0.5,  0.5, 0.0, 1.0
        ]
    indices = [
        0, 1, 2, 
        2, 3, 0
    ]
    return (np.asarray(vertices, dtype=np.float32),np.asarray(indices, dtype=np.uint32))

def cube(origin = [0.0,0.0,0.0], transform = None):
    """
        This function will return a cube using normalized units in
        worl space. You can transform the oject by performing a
        transformation later.
        Also the position of he object by default will be the origin
        of the scene, in this case [0,0,0]
        In general the position will be defined in 4D position, since the
        transformation matrix need to be in 4-dimension to allow the trans-
        lation too. The fourth value will be always 1.0.
    """
    # In order to create a cube or any other 3D geoemtry it's needed
    # to store all the information previousl in a buffer. This buffer
    # will be created and managed by opengl so at the end will be used
    # to represent the content of the buffer into the scene. 
    # I addition to this it's needed to create Shaders (vertex and
    # fragment) so the graphics card can use to know what it's needed
    # prior to represent the data.
    # At the end, we are just defining attributes. But in this 
    # particular case the first attribute that will be defined it's the
    # position. After the position we can define: vertex color, pscale,
    # normals, etc...
    # A cube will have a total of 8 vertices
    # 
    #      2    3
    #      1    0
    #
    vertices = [
        # First we represent the vertices on the bottom y = -1
        -0.5, -0.5, 0.5, 1.0, # right, bottom, back vertex. (0)
        0.5, -0.5, 0.5, 1.0, # left, bottom, back vertex. (1)
        0.5,  0.5, 0.5, 1.0, # left, bottom, ack vertex. (2)
        -0.5,  0.5, 0.5, 1.0, # right, bottom, back vertex. (3)   
        # The same vertex positions but on the top of the cube Y= 1
        -0.5, -0.5, -0.5, 1.0, # left, bottom, front vertex. (4)
        0.5, -0.5, -0.5, 1.0, # right, bottom, front vertex. (5)
        0.5,  0.5, -0.5, 1.0, # right, bottom, front vertex. (6)
        -0.5,  0.5, -0.5, 1.0 # left, bottom, front vertex. (7)
    ]
    #Conver the array into a numpy array (copy vs reference)
    nvertices = np.asarray(vertices, dtype=np.float32)
    # Defne the elements, in opengl it's needed to define triangles.
    # For each triangle we need to use 3 points or three vertices.
    # In this case we are going to define the indices, that corresponds
    # with the indexes of the vertices in the previos array. 
    # A cube has a total of 6 faces: 4 for the sides + top + bottom.
    # However, we have to define triangles, so each face will be divided
    # by two. At the end we need 6 * 2 = 12 triangles in total
    # The trianglulation will be made in clockwise way. This is important
    # to know where the faces will be facing for shading them (normals).
    indices = [
        0, 1, 2, 2, 3, 0, # Bottom face
        4, 5, 6, 6, 7, 4, # Front face
        4, 5, 1, 1, 0, 4, # left side
        6, 7, 3, 3, 2, 6, # back face
        5, 6, 2, 2, 1, 5, # Right Side
        7, 4, 0, 0, 3, 7 # Top face
    ]
    #Conver the array into a numpy array (copy vs reference)
    nindices = np.asarray(indices, dtype=np.uint32)
    # The vertices are not repeated. You can have the vertices repeated if
    # you need different attrbiutes for them, like the normals, This will
    # be used to shade the elements in different ways. In some programs
    # This is called vertex normals. An it's used to crease or decrease
    # the weight for the transition between face to face. It's like define
    # smooth areas between the hard-surface areas.
    
    # It will return a tuple with the vertices and indices.
    #return (nvertices,nindices)
    return (vertices,indices)

def default_actions_from_file():
    actions = read_json('scripts\settings.json')
    return Actions(actions)

def default_actions():
    actions = {
            "orbit" :
                { "event": [ 
                    { "type" : "DeviceEvent.MOUSEMOTION", 
                      "buttons": ["MouseButton.MIDDLE","MouseButton.LEFT"]},
                    { "type" : "DeviceEvent.KEYSPRESSED","keys": "Key.K_SPACE" }],
                  "script": "print('Acabas de pulsar la combinación')"
                },
            "pan" :  
                { "event_1": { "type":"DeviceEvent.KEYUP","key":"Key.K_a"},
                  "event_2": { "type":"DeviceEvent.KEYUP","key":"Key.K_s"},
                  "event_3": { "type":"DeviceEvent.KEYUP","key":"Key.K_d"},
                  "event_4": { "type":"DeviceEvent.KEYUP","key":"Key.K_f"},
                  "script": "print('Acabas de pulsar una tecla')"
                },
            "write" :  
                { "condition": "event.type==DeviceEvent.KEYUP and \
                                event.key==Key.K_c",
                  "script": "print('Acabas de pulsar la Condition')"
                },
            "quit" :  
                { "event_1": { "type":"DeviceEvent.QUIT"},
                  "event_2": { "type":"DeviceEvent.KEYUP","key":"Key.K_ESCAPE"},
                  "script": "engine.running = False"
                }
            }
    return Actions(actions) 

def default_material():
        return Material("./assets/images/texture.png")

def default_geometry():
        return triangle()