 NOTES
 ================================
 
1. Engine Entity-component Based

The engine is going to be implemented using entity-component pattern.
This will mean the egnine are not going to use inheritances that could limit
the behaviour of the entity and the component can be reusable for any components.

There are going to be several basic components like, camera, transformation, renderable,
etc. that will be use for the workers or manager to render the entire scene.

The idea with Entity components is the following:

 - Entity (root)
 |  - Entity  [component1, component2]
 |  |  - Entity  [component2, component7]
 |  |  | - Entity [component2]
 |  |  |
 |  |  | - Entity  [component2]
 |  - Entity  [component10, component2]
 |     ...
 |  - Entity 
 |     ...

Each component will be stored in a separated graph so the workers will use that hierarchy to
use in the computation. Another aproach is to loop over the hierarchy and look for the components
that correspond to that particular node and start updating... This could be slower since the three
implementation will requeire a search tree algorith that loop over all the graph (it supose there 
is no infinite loops in the graph). Each component will store a pointer to the entity so it can
be used later if needed.

For each entity we will have some other properties. I have to consider if the entity will
save a list with all the managers to update their-self automatically or hide this abstraction
so the entity don't know anything about the manager and let the managers to update the entity
and components if required. The entity will need to have a status to know if is still alive/active or 
not.. In this case this entity won't be considered for the computation.

After setup all the scene-graph based on entity-component pattern, workers or manager
will enter into place. There is no direct relation between manger-component since a
worker can use several components to use in the computation. The workers should perform
some basic functions like: init(), update(), render(), destroy(), etc..


2. APIs

For the engine the API that will be use is OpenGL, there are another several options 
like DirectX, Vulkan, CUDA, etc.. some of them will be using low level interface with
GPU, however they will be more flexible. In this particular engine I will be using OpenGL
that is using Vulkan drivers. OpenGL will hide all the low level functionalty implemented
in Vulkan, since it's a lot of slower.

There are some future implementation that could be done to increase the performances of this
engine:
- C++ implementation. Implements some pacakdge using C++ to be used in Python that 
implements some functionality quicker. This will provide real multi-thread routines
and better performances when loops operations that are too slow using python.
- CUDA API. This will be useful to compute very intensive task that cannot be performed
using regulat OpenGL instructions. Since OpenGL only deal with graphics computation and
rasterization, it cannot be used to perform low level operation that can be used to
performa raycasting or execute parallel task using the GPU to speed up the process.
- Physics (Rigid bodies, collisions), Simulations, Volumes (VDB), Raycasting. These tasks
are very intensive to use python GIL for the computations, since there is only thread
to do all the computations. Another attampt that can be used is to launch multiple process
and share the memory between the process to work together and do the computation more faster. 

3. Some linear Algebra

The operation lookat is used to get the transformation Matrix that 
will move the vertices (world) to the camera-view matrix. The matrix
will rotate and translate all the points so the facing to the camera.

Only to reinforce vector operations.
    - Add two vectors: the result (A-B (p)) + (B-C (v)) => p + v => result a new vector from A-C.
        -> The second vector will be placed on point B, not using the center of the axis.
    - Add point to a vector. A + (B-C (v)) => C => Displace the point A to the direction of the vector 
    - Substract two points. This give the vector from point A to B. Depending on the order the
        vector will point in oposites direction.
    - Substract two vectors. Similar to add two vectors by the computation will substracting a vector
        to another. The visualization is like adding two vectors.
    - Point multiplied by a vector. This will scale the vector by using the scalar.

    Since point and vector are very similar in the way they are represented the operation
    will vary a lot. Once you know the way they are represented, this will makes the things 
    a lot easier. 
        - Point. it's just a point in scpace. (2,3) 
        - Vector. its a vector from the center axis to the point representing the vector. v(2,3).
            -> vectors have properties like direction and magnitude.
        - Normalized vector (unit vector): vector / magnitude
        - Magnitude: sqrt(a**2 + b***2)
    
    There are a lot more related to vectors, however these are only some foundamentals mandatory
    to understand the basics of linear algebra.

