from cadlib.simple import *

sphere   = Sphere(10)

objects = [
    sphere * Slice(Z         ,  2.5, 7.5),  # Not rotated
    sphere * Slice(-Z        ,  2.5, 7.5),  # Rotated by 180 degrees, should not print a warning about unambiguous rotation
    sphere * Slice([3, 2, -1], -5.0, 5.0),  # Arbitrary vector
]

assembly = union([object.right(30*i) for i, object in enumerate(objects)])

render_to_file(assembly, "slice.scad", fn=24)
