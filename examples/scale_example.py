from cadlib.simple import *

cuboid = cuboid(20, 15, 10)

uniform = [
    scale(1),
    scale(2),
]
xyz = [
    scale(xyz = [2, 2, 2]),
    scale(xyz = [1/2, 1/1.5, 1]),
]
axis_factor = [
    scale(axis=[3, 2, 1], factor=2),
    scale(axis=[3, 0, 0], factor=2),
]

groups = [uniform, xyz, axis_factor]

assembly = union()
for i, group in enumerate(groups):
    for j, tf in enumerate(group):
        assembly = assembly + (tf * cuboid).forward(i*50).right(j*50)


render_to_file(assembly, "scale_example.scad")
