from object.primitives import *
from scad.scad import render_to_file

object = Cube([2, 3, 4])
rotate = Rotate([20, 0, 45])
assembly = rotate * object

render_to_file(assembly, "adhoc_test.scad")