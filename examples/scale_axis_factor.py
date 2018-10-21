from cadlib.simple import *

cube = Cube(2)
tf = scale(axis=[3, 3, 1], factor=2)

render_to_file(tf*cube, "rotate_axis_angle.scad")
