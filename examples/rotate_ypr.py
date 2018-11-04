from cadlib.simple import *

cuboid = cuboid([20, 5, 1])
tf = rotate(ypr = [45, -10, -20])

render_to_file(tf * cuboid, "rotate_ypr.scad")
