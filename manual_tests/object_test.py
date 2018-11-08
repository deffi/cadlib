from cadlib.transform.primitives import RotateXyz, ScaleXyz, Translate
from cadlib.object.primitives import Cuboid


def test_case(name, object):
    print(name)
    print("    Cadlib tree:")
    print(object.to_tree().format(top_indent="        "))
    print("    OpenSCAD tree:")
    print(object.to_scad().to_tree().format(top_indent="        "))


cuboid = Cuboid([5, 5, 2])

rotate = RotateXyz(90, 0, 45)
scale = ScaleXyz(1, 1, 2)
translate = Translate([10, 10, 2])

test_case("Simple object", cuboid)
test_case("Simple transform", translate * cuboid)
test_case("Dual transform (1)", (rotate * translate) * cuboid)
test_case("Dual transform (2)", rotate * (translate * cuboid))
