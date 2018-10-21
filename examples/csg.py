from cadlib.simple import *

sphere_r = 1
cube_size = 1.6

cube     = Cube(cube_size).translate([-cube_size/2, -cube_size/2, -cube_size/2])
sphere   = Sphere(1)

assembly = \
    (cube + sphere).right(0 * 2) + \
    (cube * sphere).right(1 * 2) + \
    (cube - sphere).right(2 * 2)

render_to_file(assembly, "csg.scad", fn=60)
