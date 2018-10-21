from tests.unit_test import TestCase
from cadlib.transform.primitives import ScaleAxisFactor
from cadlib.util import Vector
from cadlib.scad import ScadObject
from cadlib.util.vector import X, Y, Z

class TestScaleAxisFactor(TestCase):
    def test_construction(self):
        # Valid
        ScaleAxisFactor(      [1, 2, 3], 4)
        ScaleAxisFactor(Vector(1, 2, 3), 4)
        ScaleAxisFactor(      [1, 2, 3], 0)  # Valid, though useless

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

    def test_to_scad(self):
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

        # Now the general case is just too ridiculous to test, but we should
        # expect it to execute without raising an exception.
        ScaleAxisFactor(Vector(1, 2,  3), 4).to_scad(None)
        ScaleAxisFactor(Vector(1, 2, -3), 4).to_scad(None)
