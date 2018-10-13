def test_case(name, object):
    print(name)
    print("    Cadlib tree:")
    print(object.to_tree().format(top_indent="        "))
    print("    OpenSCAD tree:")
    print(object.to_scad().to_tree().format(top_indent="        "))


from transform.transform import Rotate, Scale, Translate
from object.primitives import Cube

cube = Cube([5, 5, 2])

rotate = Rotate([90, 0, 45])
scale = Scale([1, 1, 2])
translate = Translate([10, 10, 2])

test_case("Simple object", cube)
test_case("Simple transform", translate * cube)
test_case("Dual transform (1)", (rotate * translate) * cube)
test_case("Dual transform (2)", rotate * (translate * cube))
