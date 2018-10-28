import math
from tests.unit_test import TestCase
from cadlib.transform.primitives import ScaleAxisFactor
from cadlib.util import Vector, degree
from cadlib.scad import ScadObject
from cadlib.util.vector import X, Y, Z

class TestScaleAxisFactor(TestCase):
    def test_construction(self):
        # Valid
        ScaleAxisFactor(      [1, 2, 3], 4)
        ScaleAxisFactor(Vector(1, 2, 3), 4)

        # Valid, but with warning
        with self.assertWarns(UserWarning): ScaleAxisFactor([1, 2, 3], 0)  # Valid, though useless

        # Invalid
        with self.assertRaises(ValueError): ScaleAxisFactor([0, 0,  0 ],  4 )
        with self.assertRaises(TypeError ): ScaleAxisFactor([1, 2, "3"],  4 )
        with self.assertRaises(TypeError ): ScaleAxisFactor([1, 2,  3 ], "4")
        with self.assertRaises(TypeError ): ScaleAxisFactor(1          , "4")

    def test_equality(self):
        # Same object
        self.assertEqualToItself(ScaleAxisFactor([1, 2, 3], 4))

        # Equal objects
        self.assertEqual(ScaleAxisFactor([1, 2, 3], 4), ScaleAxisFactor([1, 2, 3], 4))

        # Different objects
        self.assertNotEqual(ScaleAxisFactor([1, 2, 3], 4), ScaleAxisFactor([1, 2, 4], 5))
        self.assertNotEqual(ScaleAxisFactor([1, 2, 3], 4), ScaleAxisFactor([1, 2, 3], 5))

        # Equal objects from different specifications
        self.assertEqual(ScaleAxisFactor(Vector(1, 2, 3), 4), ScaleAxisFactor([1, 2, 3], 4))

    def test_inverse(self):
        self.assertInverse(ScaleAxisFactor(X, 2), ScaleAxisFactor(X, 0.5))

    def test_to_scad(self):
        self.ignore_scad_comments = True

        # Special case: axis aligned with one of the coordinate axes
        # X
        self.assertEqual(ScaleAxisFactor(X, 2).to_scad(None),
            ScadObject("scale", [[2, 1, 1]], None, None))
        # Y
        self.assertEqual(ScaleAxisFactor(Y, 3).to_scad(None),
            ScadObject("scale", [[1, 3, 1]], None, None))
        # Z
        self.assertEqual(ScaleAxisFactor(Z, 4).to_scad(None),
            ScadObject("scale", [[1, 1, 4]], None, None))
        # -Z
        self.assertEqual(ScaleAxisFactor(-Z, 4).to_scad(None),
            ScadObject("scale", [[1, 1, 4]], None, None))

        # Special case: factor 1 (aligned or non-aligned)
        self.assertEqual(ScaleAxisFactor(X, 1).to_scad(None),
            ScadObject("scale", [[1, 1, 1]], None, None))
        self.assertEqual(ScaleAxisFactor(Vector(1, 1, 0), 1).to_scad(None),
            ScadObject("scale", [[1, 1, 1]], None, None))

        # General case, with the scale axis in the Y/Z plane. The scale axis is
        # rotated to the X axis.
        # Note that we're comparing floating point numbers here - rounding
        # errors might become an issue.
        angle = math.atan(1/2) / degree
        self.assertEqual(ScaleAxisFactor([2, 1, 0], 3).to_scad(None),
                ScadObject("rotate", None, [('a', angle), ('v', [0.0, 0.0, 1.0])], [
                    ScadObject("scale", [[3, 1, 1]], None, [
                        ScadObject("rotate", None, [('a', angle), ('v', [0.0, 0.0, -1.0])], None)
                    ])]))

    def test_repr(self):
        self.assertRepr(ScaleAxisFactor(X, 2), "ScaleAxisFactor(Vector(1, 0, 0), 2)")

    def test_str(self):
        self.assertStr(ScaleAxisFactor(X, 2), "Scale by 2 along <1, 0, 0>")

    def test_to_matrix(self):
        self.assertAlmostEqual(ScaleAxisFactor(X, 2).to_matrix().row_values, [
            [2, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])
        self.assertAlmostEqual(ScaleAxisFactor(X+Y, 2).to_matrix().row_values, [
            [1.5, 0.5, 0, 0],
            [0.5, 1.5, 0, 0],
            [0  , 0  , 1, 0],
            [0  , 0  , 0, 1],
        ])
