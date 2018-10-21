from cadlib.object.primitives import Sphere, Slice
from cadlib.csg import Union
from cadlib.scad import render_to_file
from cadlib.util.vector import Z

sphere   = Sphere(1)

objects = [
    sphere * Slice(Z           , 0.25, 0.75), # Not rotated
    sphere * Slice(-Z          , 0.25, 0.75), # Rotated by 180 degrees, should not print a warning about unambiguous rotation
    sphere * Slice([2, -0.5, 1], -0.5, 0.5),  # Arbitrary vector
]

assembly = Union([object.right(3*i) for i, object in enumerate(objects)])

render_to_file(assembly, "slice.scad", fn=24)
