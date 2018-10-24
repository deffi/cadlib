from cadlib.simple import *

sphere   = Sphere(10)

objects = [
    sphere * Plane(Z           ,  0),  # Not rotated
    sphere * Plane(-Z          ,  0),  # Rotated by 180 degrees, should not print a warning about unambiguous rotation
    sphere * Plane([2, -0.5, 1],  0),  # Arbitrary vector
    sphere * Plane([2, -0.5, 1],  5),  # Positive offset
    sphere * Plane([2, -0.5, 1], -5),  # Negative offset
]

assembly = union([object.right(30*i) for i, object in enumerate(objects)])

render_to_file(assembly, "plane.scad", fn=24)
