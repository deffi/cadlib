def test_case(name, object):
    print(name)
    print("    Cadlib tree:")
    print(object.to_tree().format(top_indent="        "))
    print("    OpenSCAD tree:")
    print(object.to_scad().to_tree().format(top_indent="        "))
    print("    OpenSCAD source:")
    print(object.to_scad().to_code(top_indent="        "))


from object.primitives import Cube, Cylinder, Sphere
from transform.transform import Rotate, Scale, Translate

o1 = Cube([10, 10, 10])
o2 = Cylinder(5, 5)
o3 = Sphere(2)

rotate = Rotate([90, 0, 45])
scale = Scale([1, 1, 2])
translate = Translate([10, 10, 2])

test_case("Translated object", translate * o1)
test_case("Intersection", o1 * o2 * o3)
test_case("Complex", rotate * (translate * scale * (o2 + o3) + o1))
