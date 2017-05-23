

- Some linear Algebra

Thr operation lookat is used to get the transformation Matrix that 
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
