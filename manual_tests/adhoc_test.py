from cadlib.object.primitives import Cube
from cadlib.scad import render_to_file
from cadlib.transform.primitives import RotateXyz

object = Cube([2, 3, 4])
rotate = RotateXyz([20, 0, 45])
assembly = rotate * object

render_to_file(assembly, "adhoc_test.scad")
