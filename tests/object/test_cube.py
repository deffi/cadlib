from tests.unit_test import TestCase
from cadlib.object.primitives import Cube


class TestSphere(TestCase):
    def test_construction(self):
        # Single size
        Cube(11)

        # Different sides
        Cube([11, 22, 33])

        # Zero size
        with self.assertWarnsRegex(UserWarning, r'size is 0'): Cube(0)
        with self.assertWarnsRegex(UserWarning, r'x size is 0'): Cube([0, 2, 3])
        with self.assertWarnsRegex(UserWarning, r'y size is 0'): Cube([1, 0, 3])
        with self.assertWarnsRegex(UserWarning, r'z size is 0'): Cube([1, 2, 0])
        with self.assertWarnsRegex(UserWarning, r'x size is 0'): Cube([0, 0, 0])
        with self.assertWarnsRegex(UserWarning, r'y size is 0'): Cube([0, 0, 0])
        with self.assertWarnsRegex(UserWarning, r'z size is 0'): Cube([0, 0, 0])

        # Invalid
        with self.assertRaises(ValueError): Cube([])  # Empty size
        with self.assertRaises(ValueError): Cube([11, 22])  # Wrong-size size

    def test_equality(self):
        # Same object
        self.assertEqualToItself(Cube(11))

        # Equal objects
        self.assertEqual (Cube(11), Cube(11))

        # Different objects
        self.assertNotEqual(Cube(11), Cube(12))

        # Equal objects from different specifications
        self.assertEqual(Cube(11), Cube([11, 11, 11]))

    def test_to_scad(self):
        self.assertScadObject(Cube(11          ), "cube", [[11, 11, 11]], None, None)
        self.assertScadObject(Cube([11, 22, 33]), "cube", [[11, 22, 33]], None, None)

    def test_repr(self):
        self.assertRepr(Cube([11, 22, 33]), "Cube([11, 22, 33])")
        self.assertRepr(Cube(44)          , "Cube([44, 44, 44])")

    def test_str(self):
        self.assertStr(Cube([11, 22, 33]), "Cuboid with width 11, depth 22, and height 33")
        self.assertStr(Cube(44)          , "Cube with size 44")
