from tests.unit_test import TestCase
from cadlib.transform.primitives.rotate_ypr import RotateYpr

class TestRotateYpr(TestCase):
    def test_construction(self):
        # Valid
        RotateYpr(10, 20, 30)

        # Invalid
        with self.assertRaises(TypeError): RotateYpr(1, 2, "3")

    def test_equality(self):
        # Same object
        self.assertEqualToItself(RotateYpr(10, 20, 30))

        # Equal objects
        self.assertEqual   (RotateYpr(10, 20, 30), RotateYpr(10, 20, 30)) # Equal

        # Different objects
        self.assertNotEqual(RotateYpr(10, 20, 30), RotateYpr(10, 20, 40)) # Different values

        # Equal objects from different specifications

        pass


    def test_to_scad(self):
        # TODO test to_scad instead
        self.assertScadCode(RotateYpr(1, 2, 3), "rotate([0, 0, 1]) rotate([2, 0, 0]) rotate([0, 3, 0]);")
        self.assertScadCode(RotateYpr(0, 2, 3), "rotate([2, 0, 0]) rotate([0, 3, 0]);")
        self.assertScadCode(RotateYpr(1, 0, 3), "rotate([0, 0, 1]) rotate([0, 3, 0]);")
        self.assertScadCode(RotateYpr(1, 2, 0), "rotate([0, 0, 1]) rotate([2, 0, 0]);")
        self.assertScadCode(RotateYpr(1, 0, 0), "rotate([0, 0, 1]);")
        self.assertScadCode(RotateYpr(0, 2, 0), "rotate([2, 0, 0]);")
        self.assertScadCode(RotateYpr(0, 0, 3), "rotate([0, 3, 0]);")
        self.assertScadCode(RotateYpr(0, 0, 0), "rotate([0, 0, 0]);")
