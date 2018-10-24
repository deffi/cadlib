from cadlib.simple import *

# TODO rename to scale_example and add all relevant scale types

cube = cube(20)
tf1 = scale(axis=[3, 2, 1], factor=2)
tf2 = scale(axis=[3, 0, 0], factor=2)
tf3 = scale(2)

assembly = tf1 * cube
assembly = assembly + (tf2 * cube).right(50)
assembly = assembly + (tf3 * cube).right(100)


render_to_file(assembly, "scale_axis_factor.scad")
