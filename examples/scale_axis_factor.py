from cadlib.simple import *

cube = Cube(20)
tf = scale(axis=[3, 2, 1], factor=2)

render_to_file(tf*cube, "rotate_axis_angle.scad")
