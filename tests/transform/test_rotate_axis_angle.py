from tests.unit_test import TestCase
from cadlib.transform.primitives.rotate_axis_agle import RotateAxisAngle
from cadlib.util import Vector, to_vector

class TestRotateAxisAngle(TestCase):
    def test_construction(self):
        # Valid
        RotateAxisAngle(Vector(1, 2, 3), 45)

        # Invalid
        with self.assertRaises(ValueError): RotateAxisAngle(Vector(0, 0, 0), 45)

    def test_equality(self):
        # Same object
        self.assertEqualToItself(RotateAxisAngle(Vector(1, 2, 3), 45))

        # Equal objects
        self.assertEqual   (RotateAxisAngle(Vector(1, 2, 3), 45), RotateAxisAngle(Vector(1, 2, 3), 45)) # Equal

        # Different objects
        self.assertNotEqual(RotateAxisAngle(Vector(1, 2, 3), 45), RotateAxisAngle(Vector(1, 2, 4), 45)) # Different axis
        self.assertNotEqual(RotateAxisAngle(Vector(1, 2, 3), 45), RotateAxisAngle(Vector(1, 2, 3), 46)) # Different angle

        # Equal objects from different specifications
        self.assertEqual(RotateAxisAngle([1, 2, 3], 45), RotateAxisAngle(Vector(1, 2, 3), 45)) # list vs. Vector

        pass


    def test_to_scad(self):
        # TODO test SCAD object instead
        self.assertScadCode(RotateAxisAngle([1, 2, 3], 45), "rotate(a = 45, v = [1, 2, 3]);")
