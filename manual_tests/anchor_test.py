from cadlib.object.primitives import Sphere, Cuboid, Frustum
# from cadlib.object.generators import *
#from cadlib.transform.primitives import RotateXyz, ScaleAxes, Translate
from cadlib.util.vector import X, Y, Z
from cadlib.scad import render_to_file

# def test_case(name, object):
#     print(name)
#     print("    Cadlib tree:")
#     print(object.to_tree().format(top_indent="        "))
#     print("    OpenSCAD tree:")
#     print(object.to_scad().to_tree().format(top_indent="        "))
#     print("    OpenSCAD source:")
#     print(object.to_scad().to_code(top_indent="        "))

c = Cuboid(50, 50, 50).rotate(Z, 30).right(25)

#c = Frustum(0, 20*Y, 5, 5)  # TODO base/cap/center
print(c.to_tree().format())
s = Sphere(25)

#c2 = Cuboid(10, 10, 10).top_face.at([0, 0, 0])

assembly = c + s.center.at(c.top_face) + c2

print(assembly.to_scad().to_tree().format())
print(assembly.to_scad().to_code())


render_to_file(assembly, "anchor_test.scad", fn=30)
