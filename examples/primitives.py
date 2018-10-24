from cadlib.simple import *

cube     = cube([3, 2, 1])  .right(0 * 5)
sphere   = sphere(1)        .right(1 * 5)
cylinder = cylinder(Z, 2, 1).right(2 * 5)

render_to_file(cube + sphere + cylinder, "object.scad", fn=24)
