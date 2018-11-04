from cadlib.transform.primitives import RotateXyz, ScaleXyz, Translate
from cadlib.object.primitives import Cuboid


def test_case(name, object):
    print(name)
    print("    Cadlib tree:")
    print(object.to_tree().format(top_indent="        "))
    print("    OpenSCAD tree:")
    print(object.to_scad().to_tree().format(top_indent="        "))


cube = Cuboid([5, 5, 2]) # TODO cube

rotate = RotateXyz(90, 0, 45)
scale = ScaleXyz(1, 1, 2)
translate = Translate([10, 10, 2])

test_case("Simple object", cube) # TODO cube
test_case("Simple transform", translate * cube) # TODO cube
test_case("Dual transform (1)", (rotate * translate) * cube) # TODO cube
test_case("Dual transform (2)", rotate * (translate * cube)) # TODO cube
