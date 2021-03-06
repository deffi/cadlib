from tests.unit_test import TestCase
from cadlib.transform.primitives import RotateAxisAngle
from cadlib.util import Vector, X, Y, Z
from cadlib.util.geometry import affine_matrix

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

    def test_inverse(self):
        self.assertInverse(RotateAxisAngle(X, 45), RotateAxisAngle(-X, 45))

    def test_to_scad(self):
        r = RotateAxisAngle([1, 2, 3], 45)
        self.assertScadObjectTarget(r, None, "rotate", None, [('a', 45), ('v', [1, 2, 3])], None)

    def test_repr(self):
        self.assertRepr(RotateAxisAngle([1, 0, 0], 45), "RotateAxisAngle(Vector(1, 0, 0), 45)")

    def test_str(self):
        self.assertStr(RotateAxisAngle([1, 0, 0], 45), "Rotate by 45° around <1, 0, 0>")

    def test_to_matrix(self):
        self.assertAlmostEqual(RotateAxisAngle(X        , 90 ).to_matrix(), affine_matrix(X, Z, -Y))
        self.assertAlmostEqual(RotateAxisAngle(X + Y    , 180).to_matrix(), affine_matrix(Y, X, -Z))
        self.assertAlmostEqual(RotateAxisAngle(X + Y + Z, 120).to_matrix(), affine_matrix(Y, Z,  X))
