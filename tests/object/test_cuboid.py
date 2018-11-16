from tests.unit_test import TestCase
from cadlib.object.primitives import Cuboid


class TestCuboid(TestCase):
    def test_construction(self):
        # Equal sides
        Cuboid(11, 11, 11)

        # Different sides
        Cuboid(11, 22, 33)

        # Zero size
        with self.assertWarnsRegex(UserWarning, r'size is 0'): Cuboid(0, 0, 0)
        with self.assertWarnsRegex(UserWarning, r'x size is 0'): Cuboid(0, 2, 3)
        with self.assertWarnsRegex(UserWarning, r'y size is 0'): Cuboid(1, 0, 3)
        with self.assertWarnsRegex(UserWarning, r'z size is 0'): Cuboid(1, 2, 0)
        with self.assertWarnsRegex(UserWarning, r'x size is 0'): Cuboid(0, 0, 0)
        with self.assertWarnsRegex(UserWarning, r'y size is 0'): Cuboid(0, 0, 0)
        with self.assertWarnsRegex(UserWarning, r'z size is 0'): Cuboid(0, 0, 0)

        # Invalid
        with self.assertRaises(TypeError): Cuboid()            # No parameters
        with self.assertRaises(TypeError): Cuboid(11, 22)      # Parameter missing
        with self.assertRaises(TypeError): Cuboid((1, 2, 3))   # Tuple is not allowed
        with self.assertRaises(TypeError): Cuboid([1, 2, 3])   # List is not allowed
        with self.assertRaises(TypeError): Cuboid(1, 2, None)  # Invalid number
        with self.assertRaises(TypeError): Cuboid(1, 2, "3")   # Invalid number


    def test_equality(self):
        # Same object
        self.assertEqualToItself(Cuboid(11, 11, 11))

        # Equal objects
        self.assertEqual (Cuboid(11, 11, 11), Cuboid(11, 11, 11))

        # Different objects
        self.assertNotEqual(Cuboid(11, 11, 11), Cuboid(11, 11, 12))

    def test_to_scad(self):
        self.assertScadObject(Cuboid(11, 11, 11), "cube", [[11, 11, 11]], None, None)
        self.assertScadObject(Cuboid(11, 22, 33), "cube", [[11, 22, 33]], None, None)

    def test_repr(self):
        # TODO repr must be changed
        self.assertRepr(Cuboid(11, 22, 33), "Cuboid([11, 22, 33])")

    def test_str(self):
        self.assertStr(Cuboid(11, 22, 33), "Cuboid with width 11, depth 22, and height 33")
        self.assertStr(Cuboid(44, 44, 44), "Cube with size 44")
