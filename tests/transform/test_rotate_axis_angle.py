from tests.unit_test import TestCase
from cadlib.transform.primitives import RotateAxisAngle
from cadlib.util import Vector

class TestRotateAxisAngle(TestCase):
    def test_construction(self):
        # Valid
        RotateAxisAngle(      [1, 2, 3], 45)
        RotateAxisAngle(Vector(1, 2, 3), 45)

        # Invalid
        with self.assertRaises(ValueError): RotateAxisAngle([0, 0,  0 ], 45 )
        with self.assertRaises(TypeError ): RotateAxisAngle([1, 2, "3"],  4 )
        with self.assertRaises(TypeError ): RotateAxisAngle([1, 2,  3 ], "4")
        with self.assertRaises(TypeError ): RotateAxisAngle(1          , "4")

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

    def test_to_scad(self):
        r = RotateAxisAngle([1, 2, 3], 45)
        self.assertScadObjectTarget(r, None, "rotate", None, [('a', 45), ('v', [1, 2, 3])], None)
