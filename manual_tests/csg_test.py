def test_case(name, object):
    print(name)
    print("    Cadlib tree:")
    print(object.to_tree().format(top_indent="        "))
    print("    OpenSCAD tree:")
    print(object.to_scad().to_tree().format(top_indent="        "))


from object.primitives import Cube, Cylinder, Sphere

o1 = Cube([10, 10, 10])
o2 = Cylinder(5, 5)
o3 = Sphere(2)

test_case("2-intersection", o1 * o2)
test_case("3-intersection (1)", (o1 * o2) * o3)
test_case("3-intersection (2)", o1 * (o2 * o3))
test_case("2-union", o1 + o2)
test_case("2-difference", o1 - o2)
