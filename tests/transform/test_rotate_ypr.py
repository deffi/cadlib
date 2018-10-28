from tests.unit_test import TestCase
from cadlib.transform.primitives import RotateYpr
from cadlib.scad import ScadObject
from cadlib.util.geometry import affine_matrix
from cadlib.util import X, Y, Z

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

    def test_inverse(self):
        self.assertInverse(RotateYpr(10, 20, 30),
            RotateYpr(0, 0, -30) * RotateYpr(0, -20, 0) * RotateYpr(-10, 0, 0),
            symmetric=False)

    def test_to_scad(self):
        self.ignore_scad_comments = True

        # Since OpenSCAD does not have YPR rotations, they have to translated to
        # corresponding XYZ rotations.

        # A zero YPR transform is a zero XYZ transform (not an empty ScadObject,
        # which would also be possible).
        self.assertEqual(RotateYpr(0, 0, 0).to_scad(None),
            ScadObject("rotate", [[0, 0, 0]], None, None))

        # A single-axis YPR rotation can be expressed as a single-axis YPR
        # rotation.
        # Yaw - Z axis
        self.assertEqual(RotateYpr(1, 0, 0).to_scad(None),
            ScadObject("rotate", [[0, 0, 1]], None, None))
        # Pitch - X axis
        self.assertEqual(RotateYpr(0, 2, 0).to_scad(None),
            ScadObject("rotate", [[2, 0, 0]], None, None))
        # Roll - Y axis
        self.assertEqual(RotateYpr(0, 0, 3).to_scad(None),
            ScadObject("rotate", [[0, 3, 0]], None, None))

        # A dual-axis YPR rotation must be expressed as a chain of two single-
        # axis XYZ rotations (except in the case of yaw and pitch, which can be
        # combined).
        self.assertEqual(RotateYpr(0, 2, 3).to_scad(None),
            ScadObject("rotate", [[2, 0, 0]], None, [
            ScadObject("rotate", [[0, 3, 0]], None, None)]))
        self.assertEqual(RotateYpr(1, 0, 3).to_scad(None),
            ScadObject("rotate", [[0, 0, 1]], None, [
            ScadObject("rotate", [[0, 3, 0]], None, None)]))
        self.assertEqual(RotateYpr(1, 2, 0).to_scad(None),
            ScadObject("rotate", [[2, 0, 1]], None, None))

        # A tripel-axis YPR rotation must be expressed as a chain of two
        # single-axis XYZ rotations (yaw and pitch can be combined).
        self.assertEqual(RotateYpr(1, 2, 3).to_scad(None),
            ScadObject("rotate", [[2, 0, 1]], None, [
            ScadObject("rotate", [[0, 3, 0]], None, None)]))

    def test_repr(self):
        self.assertRepr(RotateYpr(1, 2, 3), "RotateYpr(1, 2, 3)")

    def test_to_matrix(self):
        # No rotation
        self.assertAlmostEqual(RotateYpr( 0 , 0,  0).to_matrix(), affine_matrix(X, Y, Z))

        # 90 degrees around a single axis
        self.assertAlmostEqual(RotateYpr(90,  0,  0).to_matrix(), affine_matrix( Y, -X,  Z)) # Yaw left
        self.assertAlmostEqual(RotateYpr( 0, 90,  0).to_matrix(), affine_matrix( X,  Z, -Y)) # Pitch up
        self.assertAlmostEqual(RotateYpr( 0,  0, 90).to_matrix(), affine_matrix(-Z,  Y,  X)) # Roll right

        # 180 degrees around a single axis
        self.assertAlmostEqual(RotateYpr(180,   0,   0).to_matrix(), affine_matrix(-X, -Y,  Z)) # Yaw
        self.assertAlmostEqual(RotateYpr(  0, 180,   0).to_matrix(), affine_matrix( X, -Y, -Z)) # Pitch
        self.assertAlmostEqual(RotateYpr(  0,   0, 180).to_matrix(), affine_matrix(-X,  Y, -Z)) # Roll

        # 90 degrees each around two axes
        self.assertAlmostEqual(RotateYpr(90, 90,  0).to_matrix(), affine_matrix( Y,  Z, X)) # Yaw left, pitch up
        self.assertAlmostEqual(RotateYpr(90,  0, 90).to_matrix(), affine_matrix(-Z, -X, Y)) # Yaw left, roll right
        self.assertAlmostEqual(RotateYpr( 0, 90, 90).to_matrix(), affine_matrix( Y,  Z, X)) # Pitch up, roll right

        # 90 degrees each around all three axes
        self.assertAlmostEqual(RotateYpr(90, 90, 90).to_matrix(), affine_matrix(-X, Z, Y)) # Yaw left, pitch up, roll right
