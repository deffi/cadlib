from cadlib.transform.primitives import RotateXyz, ScaleXyz, Translate
def test_case(name, transform):
    print(name)
    print("    Cadlib tree:")
    print(transform.to_tree().format(top_indent="        "))
    print("    OpenSCAD tree:")
    print(transform.to_scad(None).to_tree().format(top_indent="        "))


rotate    = RotateXyz(90, 0, 45)
scale     = ScaleXyz(1, 1, 2)
translate = Translate([10, 10, 2])

test_case("One", rotate)
test_case("Two", rotate * scale)
test_case("Three (0)", rotate * scale * translate)
test_case("Three (1)", (rotate * scale) * translate)
test_case("Three (2)", rotate * (scale * translate))
test_case("Four (1)" , (rotate * scale) * (rotate * scale))
rs = rotate * scale
test_case("Four (2)" , rs * rs)
