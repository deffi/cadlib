from cadlib.transform.primitives.rotate_axis_agle import RotateAxisAngle
from cadlib.transform.primitives.rotate_xyz import RotateXyz
from cadlib.transform.primitives.rotate_ypr import RotateYpr
from cadlib.transform.primitives.scale_xyz import ScaleXyz
from cadlib.transform.primitives.scale_axis_factor import ScaleAxisFactor
from cadlib.transform.primitives.scale_uniform import ScaleUniform
from cadlib.transform.primitives.translate import Translate
from tests.unit_test import TestCase
from cadlib.transform.generators import *
from cadlib.util import Vector, X, Y, Z

class TestTransformGenerators(TestCase):
    def test_rotate(self):
        # Canonical axis/angle
        self.assertEqual(rotate(axis = Vector(1, 2, 3), angle = 45), RotateAxisAngle(Vector(1, 2, 3), 45)) # Vector
        self.assertEqual(rotate(axis =       [1, 2, 3], angle = 45), RotateAxisAngle(Vector(1, 2, 3), 45)) # List

        # Canonical from/to
        self.assertEqual(rotate(frm = X        , to = Y        ), RotateAxisAngle(Z, 90)) # Vectors
        self.assertEqual(rotate(frm = [1, 0, 0], to = [0, 1, 0]), RotateAxisAngle(Z, 90)) # Lists
        self.assertEqual(rotate(frm = X        , to = Y * 2    ), RotateAxisAngle(Z, 90)) # Independent of vector length
        # Unit axis to unit axis
        self.assertEqual(rotate(frm = X, to = Y), RotateAxisAngle( Z, 90))
        self.assertEqual(rotate(frm = Y, to = Z), RotateAxisAngle( X, 90))
        self.assertEqual(rotate(frm = Z, to = X), RotateAxisAngle( Y, 90))
        self.assertEqual(rotate(frm = Y, to = X), RotateAxisAngle(-Z, 90))
        self.assertEqual(rotate(frm = Z, to = Y), RotateAxisAngle(-X, 90))
        self.assertEqual(rotate(frm = X, to = Z), RotateAxisAngle(-Y, 90))
        # Different signs for X/Y axes
        self.assertEqual(rotate(frm =  X, to =  Y), RotateAxisAngle( Z, 90))
        self.assertEqual(rotate(frm =  X, to = -Y), RotateAxisAngle(-Z, 90))
        self.assertEqual(rotate(frm = -X, to =  Y), RotateAxisAngle(-Z, 90))
        self.assertEqual(rotate(frm = -X, to = -Y), RotateAxisAngle( Z, 90))
        self.assertEqual(rotate(frm =  Y, to =  X), RotateAxisAngle(-Z, 90))
        self.assertEqual(rotate(frm =  Y, to = -X), RotateAxisAngle( Z, 90))
        self.assertEqual(rotate(frm = -Y, to =  X), RotateAxisAngle( Z, 90))
        self.assertEqual(rotate(frm = -Y, to = -X), RotateAxisAngle(-Z, 90))
        # Using lists
        self.assertEqual(rotate(frm = [1, 0, 0], to = [0, 1, 0]), RotateAxisAngle(Z, 90))
        self.assertEqual(rotate(frm = [1, 0, 0], to = [1, 1, 0]), RotateAxisAngle(Z, 45))
        # Same direction (no effect) - note different  type
        self.assertEqual(rotate(frm = [1, 0, 0], to = [1, 0, 0]), RotateXyz(0, 0, 0))
        self.assertEqual(rotate(frm = [1, 2, 3], to = [2, 4, 6]), RotateXyz(0, 0, 0))
        # Opposite direction (ambiguous rotation)
        with self.assertWarns(RuntimeWarning):
            self.assertEqual(rotate(frm = [1, 0, 0], to = [-1,  0,  0])._angle, 180)
        with self.assertWarns(RuntimeWarning):
            self.assertEqual(rotate(frm = [1, 2, 3], to = [-2, -4, -6])._angle, 180)
        # Zero vectors
        O = Vector.zero(3)
        with self.assertRaises(ValueError): rotate(frm = X, to = O)
        with self.assertRaises(ValueError): rotate(frm = X, to = O)
        with self.assertRaises(ValueError): rotate(frm = O, to = O)

        # Canonical XYZ
        self.assertEqual(rotate(xyz = [45, 0, 30]), RotateXyz(45, 0, 30))

        # Canonical yaw/pitch/roll
        self.assertEqual(rotate(ypr = [90, -20, 5]), RotateYpr(90, -20, 5))

        # Convenience axis/angle (implicit)
        self.assertEqual(rotate(Vector(1, 2, 3), 45), RotateAxisAngle(Vector(1, 2, 3), 45)) # Vector
        self.assertEqual(rotate(      [1, 2, 3], 45), RotateAxisAngle(Vector(1, 2, 3), 45)) # List

        # Convenience axis/angle (explicit)
        self.assertEqual(rotate(Vector(1, 2, 3), angle = 45), RotateAxisAngle(Vector(1, 2, 3), 45)) # Vector
        self.assertEqual(rotate(      [1, 2, 3], angle = 45), RotateAxisAngle(Vector(1, 2, 3), 45)) # List

        # Convenience from/to (implicit)
        self.assertEqual(rotate(X        , Y        ), RotateAxisAngle(Z, 90)) # Vectors
        self.assertEqual(rotate([1, 0, 0], [0, 1, 0]), RotateAxisAngle(Z, 90)) # Lists

        # Convenience from/to (explicit)
        self.assertEqual(rotate(X        , to = Y        ), RotateAxisAngle(Z, 90)) # Vectors
        self.assertEqual(rotate([1, 0, 0], to = [0, 1, 0]), RotateAxisAngle(Z, 90)) # Lists

    def test_rotate_invalid(self):
        # Nothing at all
        with self.assertRaises(ValueError): rotate()

        # Canonical forms - multiple specifications
        with self.assertRaises(ValueError): rotate(axis = X, angle = 45, frm = X)
        with self.assertRaises(ValueError): rotate(axis = X, angle = 45, to = X)
        with self.assertRaises(ValueError): rotate(axis = X, angle = 45, xyz = [1, 2, 3])
        with self.assertRaises(ValueError): rotate(axis = X, angle = 45, ypr = [1, 2, 3])
        with self.assertRaises(ValueError): rotate(frm = X, to = Y, axis = X)
        with self.assertRaises(ValueError): rotate(frm = X, to = Y, angle = 45)
        with self.assertRaises(ValueError): rotate(frm = X, to = Y, xyz = [1, 2, 3])
        with self.assertRaises(ValueError): rotate(frm = X, to = Y, ypr = [1, 2, 3])
        with self.assertRaises(ValueError): rotate(xyz = [1, 2, 3], ypr = [1, 2, 3])

        # Canonical forms - incomplete specification
        with self.assertRaises(ValueError): rotate(axis = X)    # Missing angle
        with self.assertRaises(ValueError): rotate(angle = 45)  # Missing axis
        with self.assertRaises(ValueError): rotate(frm = X)     # Missing to
        with self.assertRaises(ValueError): rotate(to = Y)      # Missing from

        # Canonical forms - invalid types
        with self.assertRaises(TypeError): rotate(axis = 0        , angle = 45)
        with self.assertRaises(TypeError): rotate(axis = [1, 2, 3], angle = "")
        with self.assertRaises(TypeError): rotate(frm = 0, to = Y)
        with self.assertRaises(TypeError): rotate(frm = X, to = 0)
        with self.assertRaises(TypeError): rotate(xyz = 0)
        with self.assertRaises(TypeError): rotate(ypr = 0)

        # Convenience forms, duplicate specification
        with self.assertRaises(ValueError): rotate(X, 45, axis = X)
        with self.assertRaises(ValueError): rotate(X, 45, angle = 45)
        with self.assertRaises(ValueError): rotate(X, Y, frm  = X)
        with self.assertRaises(ValueError): rotate(X, Y, to = Y)

        # Convenience forms, multiple specifications
        with self.assertRaises(ValueError): rotate(X, 45, frm = X)
        with self.assertRaises(ValueError): rotate(X, 45, to = X)
        with self.assertRaises(ValueError): rotate(X, 45, xyz = [1, 2, 3])
        with self.assertRaises(ValueError): rotate(X, 45, ypr = [1, 2, 3])
        with self.assertRaises(ValueError): rotate(X, Y, axis = X)
        with self.assertRaises(ValueError): rotate(X, Y, angle = 45)
        with self.assertRaises(ValueError): rotate(X, Y, xyz = [1, 2, 3])
        with self.assertRaises(ValueError): rotate(X, Y, ypr = [1, 2, 3])

        # Convenience forms - incomplete specification
        with self.assertRaises(ValueError): rotate(X)

        # Convenience forms - invalid type
        with self.assertRaises(TypeError): rotate(0)     # First argument must be a vector either way
        with self.assertRaises(TypeError): rotate(X, "") # Invalid second argument
        with self.assertRaises(TypeError): rotate(0, 0)  # Invalid second argument
        with self.assertRaises(TypeError): rotate(0, X)  # Would have been correct if switched

    def test_scale(self):
        # Canonical axis/factor
        self.assertEqual(scale(axis = Vector(1, 2, 3), factor = 4), ScaleAxisFactor(Vector(1, 2, 3), 4))
        self.assertEqual(scale(axis =       [1, 2, 3], factor = 4), ScaleAxisFactor(      [1, 2, 3], 4))

        # Canonical XYZ
        self.assertEqual(scale(xyz = Vector(1, 2, 3)), ScaleXyz(1, 2, 3))
        self.assertEqual(scale(xyz =       [1, 2, 3]), ScaleXyz(1, 2, 3))

        # Canonical uniform
        self.assertEqual(scale(factor = 2), ScaleUniform(2))


        # Convenience axis/factor (implicit)
        self.assertEqual(scale(Vector(1, 2, 3), 4), ScaleAxisFactor(Vector(1, 2, 3), 4))
        self.assertEqual(scale(      [1, 2, 3], 4), ScaleAxisFactor(      [1, 2, 3], 4))

        # Convenience axis/factor (explicit)
        self.assertEqual(scale(Vector(1, 2, 3), factor = 4), ScaleAxisFactor(Vector(1, 2, 3), 4))
        self.assertEqual(scale(      [1, 2, 3], factor = 4), ScaleAxisFactor(      [1, 2, 3], 4))

        # Convenience XYZ
        self.assertEqual(scale(Vector(1, 2, 3)), ScaleXyz(1, 2, 3))
        self.assertEqual(scale(      [1, 2, 3]), ScaleXyz(1, 2, 3))

        # Convenience uniform
        self.assertEqual(scale(2), ScaleUniform(2))

    def test_scale_invalid(self):
        # Nothing at all
        with self.assertRaises(ValueError): scale()

        # Canonical forms - multiple specifications
        with self.assertRaises(ValueError): scale(xyz = [1, 1, 1], factor = 2)
        with self.assertRaises(ValueError): scale(xyz = [1, 1, 1], axis = X)

        # Canonical forms - incomplete specification
        with self.assertRaises(ValueError): scale(axis = X)  # Missing factor

        # Canonical forms - invalid types
        with self.assertNothingRaised():   scale(axis = X, factor = 2)
        with self.assertRaises(TypeError): scale(axis = 1, factor = 2)
        with self.assertRaises(TypeError): scale(axis = 0, factor = 2)
        with self.assertRaises(TypeError): scale(axis = X, factor = "")
        with self.assertRaises(TypeError): scale(xyz = "")
        with self.assertRaises(TypeError): scale(xyz = 2)

        # Convenience forms, duplicate specification
        with self.assertRaises(ValueError): scale(X, 2, axis = X)
        with self.assertRaises(ValueError): scale(X,    xyz = X)

        # Convenience forms, multiple specifications
        with self.assertRaises(ValueError): scale(X, 2, xyz = X)
        with self.assertRaises(ValueError): scale(2,    xyz = X)

        # Convenience forms - incomplete specification
        # No such thing here because an incomplete axis/factor will be a valid XYZ

        # Convenience forms - invalid type
        with self.assertRaises(TypeError): scale("")    # First argument must be a vector or a number
        with self.assertRaises(TypeError): scale(X, "") # Invalid second argument
        with self.assertRaises(TypeError): scale(X, X)  # Invalid second argument
        with self.assertRaises(TypeError): scale(0, X)  # Would have been correct if switched

    def test_translate(self):
        self.assertEqual(translate(Vector(1, 2, 3)), Translate(Vector(1, 2, 3)))
        self.assertEqual(translate(      [1, 2, 3]), Translate(Vector(1, 2, 3)))
