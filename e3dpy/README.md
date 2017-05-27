
RENDER GL NOTES
====================================

Great useful resource to learn OpenGL and all the concepts needed for understanding ligths, materials, shaders, transformations, etc..
    URL: https://learnopengl.com/, https://open.gl/drawing


1. Tasks

For my OpenGL I will need the following classes or objects.

[DONE] Display: window that manage the 3D view and Input Events 
            fom the user. Also this class will be the one that
            implement the main loop for all the render.
                    
Shader: This class will be enable the creation of shaders
        programs that will be added to the main shader program
        that will be used.
        We can create Vertex, Fragment or Geoemtry shaders. These
        will be inked and use every time we want to render the
        geometry. 
Geometry: The class will be the main container for storing
        vertices, indices (element), vertex colors, normals and
        other attributes. Also the geometry will manage the uvs
        attributes and the materials that will be used for this
        particular geoemtry.
            - Vertices/Points
            - Indices (Faces)
            - Attributes (list with the Attrbiutes)
                Default attributes like Cd, N, P Uv could be 
                created automatically for each object since they
                are used by default in all the 3D applications.

Material: Each geoemtry obejct could have more that one material.
        In this case we have to decide if we are going to use
        different shaders or only one for the entire geometry.
Camera: This class will allow the creation of different cameras
        to swtich indide the progrm. The camera will configure
        the View and Projection matrix.

Light:  Every scene have a light to lit the objects. These
        lights will be passed to the shaders to the objects
        would be shaded accordingly to these lights.
        
        There are several types of lights:
            Directional lights, Aerial lights, Spot lights,
            Ambient lights, Point lights.
        
        Also there are another indirect light that will be computed
        in real-time or render time that will depend on the environment.
        Ths light will be specular lights or bouncing lights.

        Finally, effects like Fresnel, bump, dissplacement, sub-surface
        scattering, reflection, refraction, translucency, layers, etc..
        are a cmobination between Materials and lights

Volumes (VDB): The type of geoemtry is different from the way
        that polygons are created. This type of geometry
        requires additional manipulation and pipelone.

Particles/Instances: This is used to represent millions of 
        GEoemtry that will be packed into points. So the 
        vertices, and indices will be instances.

Sprites: Sprites is used for 2D and 3D. The idea is sprites
        will alway be facing to the camera. So there is no
        distorsion or perspective transformation that affect
        to this objects.

Image: Image class will be used to create Interface controls,
        dashboard elements, etc.. 

2. Notes

 The new pipeline used for OpenGL is that all operations, transformations, etc.. will be performed in the GPU. In order to do this these operations must be implemented into the shaders programs instead, so the GPU will be able to compile those shaders and execute them in Parallel.

 OpenGL works using states, so for eac state we configure the buffers, arrays, shaders, etc.. and finally draw. We perform the sema operation for all the geoemtry we have. Since the geometry could have different configuration and attributes, and shaders we need to operate with them separately.

 When the entire scene is complete, and all the geoemtry all correctly renderer it's time to flip the buffers to start the next frame.


4. Links


https://codereview.stackexchange.com/questions/92769/managing-shaders-in-opengl-a-shader-class
https://www.packtpub.com/books/content/tips-and-tricks-getting-started-opengl-and-glsl-40
http://dominium.maksw.com/articles/physically-based-rendering-pbr/pbr-part-one/   
http://www.opengl-tutorial.org/beginners-tutorials/tutorial-8-basic-shading/
https://www.tomdalling.com/blog/modern-opengl/08-even-more-lighting-directional-lights-spotlights-multiple-lights/

https://github.com/adamlwgriffiths/Pyrr/tree/master/pyrr
https://www.opengl.org/discussion_boards/showthread.php/199031-How-to-sort-draw-and-shader-calls-for-multiple-models
https://www.khronos.org/opengl/wiki/Vertex_Specification_Best_Practices

https://gamedev.stackexchange.com/questions/92832/in-opengl-whats-quicker-lots-of-smaller-vaos-or-one-large-one-updated-each-fr
https://www.opengl.org/discussion_boards/showthread.php/197893-View-and-Perspective-matrices
https://www.gamedev.net/topic/609159-would-like-help-with-glulookat-and-python-code/


http://pyopengl.sourceforge.net/documentation/manual-3.0/gluLookAt.html
http://stackoverflow.com/questions/3380100/how-do-i-use-glulookat-properly
http://stackoverflow.com/questions/15006905/how-do-i-modify-the-perspective-of-an-opengl-using-glulookat
http://stackoverflow.com/questions/26949617/pyopengl-glulookat-behaviour
http://stackoverflow.com/questions/19078620/rotate-cube-to-look-at-mouse-from-python-in-opengl