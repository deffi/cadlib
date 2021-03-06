from cadlib.simple import *

sphere   = sphere(10)

objects = [
    sphere * layer(Z, 2.5, 7.5),  # Not rotated
    sphere * layer(-Z, 2.5, 7.5),  # Rotated by 180 degrees, should not print a warning about unambiguous rotation
    sphere * layer([3, 2, -1], -5.0, 5.0),  # Arbitrary vector
]

assembly = union([object.right(30*i) for i, object in enumerate(objects)])

render_to_file(assembly, "layer.scad", fn=24)
