from tests.unit_test import TestCase
from cadlib.transform.primitives import RotateFromTo
from cadlib.util import Vector

class TestRotateFromTo(TestCase):
    def test_construction(self):
        # Valid
        RotateFromTo(      [1, 2, 3],       [4, 5, 6])
        RotateFromTo(Vector(1, 2, 3), Vector(4, 5, 6))

        # Invalid
        with self.assertRaises(ValueError): RotateFromTo([0, 0, 0], [4, 5, 6])
        with self.assertRaises(ValueError): RotateFromTo([1, 2, 3], [0, 0, 0])
        with self.assertRaises(TypeError ): RotateFromTo([1, 2, 3], 45 )
        with self.assertRaises(TypeError ): RotateFromTo(45, [1, 2, 3])
        with self.assertRaises(TypeError ): RotateFromTo([1, 2, "3"], [4, 5,  6])
        with self.assertRaises(TypeError ): RotateFromTo([1, 2,  3 ], [4, 5, "6"])

    def test_equality(self):
        # Same object
        self.assertEqualToItself(RotateFromTo(Vector(1, 2, 3), Vector(4, 5, 6)))

        # Equal objects
        self.assertEqual(RotateFromTo([1, 2, 3], [4, 5, 6]), RotateFromTo([1, 2, 3], [4, 5, 6])) # Equal

        # Different objects
        self.assertNotEqual(RotateFromTo([1, 2, 3], [4, 5, 6]), RotateFromTo([1, 2, 3], [4, 5, 7])) # Different from
        self.assertNotEqual(RotateFromTo([1, 2, 3], [4, 5, 6]), RotateFromTo([1, 2, 7], [4, 5, 6])) # Different to

    def test_to_scad(self):
        pass
        # TODO variouse cases
        # r = RotateFromTo([1, 2, 3], 45)
        # self.assertScadObjectTarget(r, None, "rotate", None, [('a', 45), ('v', [1, 2, 3])], None)
        # Canonical from/to
        # From test_transform_generators:
        # self.assertEqual(rotate(frm = X        , to = Y        ), RotateAxisAngle(Z, 90)) # Vectors
        # self.assertEqual(rotate(frm = [1, 0, 0], to = [0, 1, 0]), RotateAxisAngle(Z, 90)) # Lists
        # self.assertEqual(rotate(frm = X        , to = Y * 2    ), RotateAxisAngle(Z, 90)) # Independent of vector length
        # # Unit axis to unit axis
        # self.assertEqual(rotate(frm = X, to = Y), RotateAxisAngle( Z, 90))
        # self.assertEqual(rotate(frm = Y, to = Z), RotateAxisAngle( X, 90))
        # self.assertEqual(rotate(frm = Z, to = X), RotateAxisAngle( Y, 90))
        # self.assertEqual(rotate(frm = Y, to = X), RotateAxisAngle(-Z, 90))
        # self.assertEqual(rotate(frm = Z, to = Y), RotateAxisAngle(-X, 90))
        # self.assertEqual(rotate(frm = X, to = Z), RotateAxisAngle(-Y, 90))
        # # Different signs for X/Y axes
        # self.assertEqual(rotate(frm =  X, to =  Y), RotateAxisAngle( Z, 90))
        # self.assertEqual(rotate(frm =  X, to = -Y), RotateAxisAngle(-Z, 90))
        # self.assertEqual(rotate(frm = -X, to =  Y), RotateAxisAngle(-Z, 90))
        # self.assertEqual(rotate(frm = -X, to = -Y), RotateAxisAngle( Z, 90))
        # self.assertEqual(rotate(frm =  Y, to =  X), RotateAxisAngle(-Z, 90))
        # self.assertEqual(rotate(frm =  Y, to = -X), RotateAxisAngle( Z, 90))
        # self.assertEqual(rotate(frm = -Y, to =  X), RotateAxisAngle( Z, 90))
        # self.assertEqual(rotate(frm = -Y, to = -X), RotateAxisAngle(-Z, 90))
        # # Using lists
        # self.assertEqual(rotate(frm = [1, 0, 0], to = [0, 1, 0]), RotateAxisAngle(Z, 90))
        # self.assertEqual(rotate(frm = [1, 0, 0], to = [1, 1, 0]), RotateAxisAngle(Z, 45))
        # # Same direction (no effect) - note different  type
        # self.assertEqual(rotate(frm = [1, 0, 0], to = [1, 0, 0]), RotateXyz(0, 0, 0))
        # self.assertEqual(rotate(frm = [1, 2, 3], to = [2, 4, 6]), RotateXyz(0, 0, 0))
        # # Opposite direction (ambiguous rotation)
        # with self.assertWarns(RuntimeWarning):
        #     self.assertEqual(rotate(frm = [1, 0, 0], to = [-1,  0,  0])._angle, 180)
        # with self.assertWarns(RuntimeWarning):
        #     self.assertEqual(rotate(frm = [1, 2, 3], to = [-2, -4, -6])._angle, 180)
        # # Zero vectors
        # O = Vector.zero(3)
        # with self.assertRaises(ValueError): rotate(frm = X, to = O)
        # with self.assertRaises(ValueError): rotate(frm = X, to = O)
        # with self.assertRaises(ValueError): rotate(frm = O, to = O)
