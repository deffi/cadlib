from tests.unit_test import TestCase
from cadlib.object.primitives import Cube


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

    def test_repr(self):
        self.assertRepr(Cube([11, 22, 33]), "Cube([11, 22, 33])")
        self.assertRepr(Cube(44)          , "Cube([44, 44, 44])")
