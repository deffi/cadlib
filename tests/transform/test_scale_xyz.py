from tests.unit_test import TestCase
from cadlib.transform.primitives import ScaleXyz
from cadlib.util.vector import Vector

class TestScaleXyz(TestCase):
    def test_construction(self):
        # Valid
        ScaleXyz(1, 2, 3)

        # Invalid
        with self.assertRaises(TypeError): ScaleXyz(1, 2, "3")
        with self.assertRaises(TypeError): ScaleXyz(2)
        with self.assertRaises(TypeError): ScaleXyz([1, 2, 1])
        with self.assertRaises(TypeError): ScaleXyz("3")
        with self.assertRaises(TypeError): ScaleXyz(Vector(1, 2, 3))


    def test_equality(self):
        # Same object
        self.assertEqualToItself(ScaleXyz(60, 30, 15))

        # Equal objects
        self.assertEqual(ScaleXyz(60, 30, 15), ScaleXyz(60, 30, 15))

        # Different objects
        self.assertNotEqual(ScaleXyz(60, 30, 15), ScaleXyz(60, 30, 16))

    def test_to_scad(self):
        s = ScaleXyz(1, 2, -1)

        self.assertScadObjectTarget(s, None, "scale", [[1, 2, -1]], None, None)

    def test_repr(self):
        self.assertRepr(ScaleXyz(1, 2, 3), "ScaleXyz(1, 2, 3)")
