from cadlib.simple import *

cube = cube([20, 5, 1])
tf = rotate(ypr = [45, -10, -20])

render_to_file(tf*cube, "rotate_ypr.scad")
