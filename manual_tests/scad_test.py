from cadlib.object.primitives import Cuboid, Cylinder, Sphere
from cadlib.transform.primitives import RotateXyz, ScaleAxes, Translate
from cadlib.util.vector import Z


def test_case(name, object):
    print(name)
    print("    Cadlib tree:")
    print(object.to_tree().format(top_indent="        "))
    print("    OpenSCAD tree:")
    print(object.to_scad().to_tree().format(top_indent="        "))
    print("    OpenSCAD source:")
    print(object.to_scad().to_code(top_indent="        "))


o1 = Cuboid(10, 10, 10)
o2 = Cylinder(Z, 5, 5)
o3 = Sphere(2)

rotate = RotateXyz(90, 0, 45)
scale = ScaleAxes(1, 1, 2)
translate = Translate([10, 10, 2])

test_case("Translated object", translate * o1)
test_case("Intersection", o1 * o2 * o3)
test_case("Complex", rotate * (translate * scale * (o2 + o3) + o1))
