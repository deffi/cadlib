from cadlib.simple import *

sphere   = sphere(10)

objects = [
    sphere * plane(Z           ,  0),  # Not rotated
    sphere * plane(-Z          ,  0),  # Rotated by 180 degrees, should not print a warning about unambiguous rotation
    sphere * plane([2, -0.5, 1],  0),  # Arbitrary vector
    sphere * plane([2, -0.5, 1],  5),  # Positive offset
    sphere * plane([2, -0.5, 1], -5),  # Negative offset
]

assembly = union([object.right(30*i) for i, object in enumerate(objects)])

render_to_file(assembly, "plane.scad", fn=24)
