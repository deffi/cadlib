from cadlib.object.primitives import Cube, Sphere, Cylinder
from cadlib.scad import render_to_file
from cadlib.util.vector import Z

cube     = Cube([3, 2, 1])  .right(0 * 5)
sphere   = Sphere(1)        .right(1 * 5)
cylinder = Cylinder(Z, 2, 1).right(2 * 5)

render_to_file(cube + sphere + cylinder, "object.scad", fn=24)
