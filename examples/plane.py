from cadlib.simple import *

sphere   = Sphere(1)

objects = [
    sphere * Plane(Z           , 0),    # Not rotated
    sphere * Plane(-Z          , 0),    # Rotated by 180 degrees, should not print a warning about unambiguous rotation
    sphere * Plane([2, -0.5, 1], 0),    # Arbitrary vector
    sphere * Plane([2, -0.5, 1], 0.5),  # Positive offset
    sphere * Plane([2, -0.5, 1], -0.5), # Negative offset
]

assembly = Union([object.right(3*i) for i, object in enumerate(objects)])

render_to_file(assembly, "plane.scad", fn=24)
