from tests.unit_test import TestCase
from cadlib.object.primitives import Cuboid


class TestCuboid(TestCase):
    def test_construction(self):
        # Single size
        Cuboid(11)

        # Different sides
        Cuboid([11, 22, 33])

        # Zero size
        with self.assertWarnsRegex(UserWarning, r'size is 0'): Cuboid(0)
        with self.assertWarnsRegex(UserWarning, r'x size is 0'): Cuboid([0, 2, 3])
        with self.assertWarnsRegex(UserWarning, r'y size is 0'): Cuboid([1, 0, 3])
        with self.assertWarnsRegex(UserWarning, r'z size is 0'): Cuboid([1, 2, 0])
        with self.assertWarnsRegex(UserWarning, r'x size is 0'): Cuboid([0, 0, 0])
        with self.assertWarnsRegex(UserWarning, r'y size is 0'): Cuboid([0, 0, 0])
        with self.assertWarnsRegex(UserWarning, r'z size is 0'): Cuboid([0, 0, 0])

        # Invalid
        with self.assertRaises(ValueError): Cuboid([])  # Empty size
        with self.assertRaises(ValueError): Cuboid([11, 22])  # Wrong-size size

    def test_equality(self):
        # Same object
        self.assertEqualToItself(Cuboid(11))

        # Equal objects
        self.assertEqual (Cuboid(11), Cuboid(11))

        # Different objects
        self.assertNotEqual(Cuboid(11), Cuboid(12))

        # Equal objects from different specifications
        self.assertEqual(Cuboid(11), Cuboid([11, 11, 11]))

    def test_to_scad(self):
        self.assertScadObject(Cuboid(11)          , "cube", [[11, 11, 11]], None, None)
        self.assertScadObject(Cuboid([11, 22, 33]), "cube", [[11, 22, 33]], None, None)

    def test_repr(self):
        self.assertRepr(Cuboid([11, 22, 33]), "Cuboid([11, 22, 33])")
        self.assertRepr(Cuboid(44), "Cuboid([44, 44, 44])")

    def test_str(self):
        self.assertStr(Cuboid([11, 22, 33]), "Cuboid with width 11, depth 22, and height 33")
        self.assertStr(Cuboid(44), "Cube with size 44")
