# import math
#
from tests.unit_test import TestCase
from cadlib.object.primitives import Cube
# from cadlib.geometry.vector import X, Y, Z
# from cadlib.scad.scad import ScadObject
#
class TestSphere(TestCase):
    def test_construction(self):
        # Single size
        cube1 = Cube(11)

        # Different sides
        cube2 = Cube([11, 22, 33])

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
