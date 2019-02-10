from tests.unit_test import TestCase
from cadlib.transform.primitives import ScaleAxes
from cadlib.util.vector import Vector

class TestScaleAxes(TestCase):
    def test_construction(self):
        # Valid
        ScaleAxes(1, 2, 3)

        # Valid, but with warning
        with self.assertWarns(UserWarning): ScaleAxes(0, 2, 3)
        with self.assertWarns(UserWarning): ScaleAxes(1, 0, 3)
        with self.assertWarns(UserWarning): ScaleAxes(1, 2, 0)
        with self.assertWarns(UserWarning): ScaleAxes(0, 0, 0)

        # Invalid
        with self.assertRaises(TypeError): ScaleAxes(1, 2, "3")
        with self.assertRaises(TypeError): ScaleAxes(2)
        with self.assertRaises(TypeError): ScaleAxes([1, 2, 1])
        with self.assertRaises(TypeError): ScaleAxes("3")
        with self.assertRaises(TypeError): ScaleAxes(Vector(1, 2, 3))


    def test_equality(self):
        # Same object
        self.assertEqualToItself(ScaleAxes(60, 30, 15))

        # Equal objects
        self.assertEqual(ScaleAxes(60, 30, 15), ScaleAxes(60, 30, 15))

        # Different objects
        self.assertNotEqual(ScaleAxes(60, 30, 15), ScaleAxes(60, 30, 16))

    def test_inverse(self):
        self.assertInverse(ScaleAxes(1, 2, 4), ScaleAxes(1, 0.5, 0.25))

    def test_to_scad(self):
        s = ScaleAxes(1, 2, -1)

        self.assertScadObjectTarget(s, None, "scale", [[1, 2, -1]], None, None)

    def test_repr(self):
        self.assertRepr(ScaleAxes(1, 2, 3), "ScaleAxes(1, 2, 3)")

    def test_str(self):
        self.assertStr(ScaleAxes(1, 1, 1), "Scale by 1 along X, Y, and Z")
        self.assertStr(ScaleAxes(2, 1, 1), "Scale by 2 along X")
        self.assertStr(ScaleAxes(1, 3, 1), "Scale by 3 along Y")
        self.assertStr(ScaleAxes(1, 1, 4), "Scale by 4 along Z")
        self.assertStr(ScaleAxes(2, 3, 1), "Scale by 2 along X and 3 along Y")
        self.assertStr(ScaleAxes(2, 1, 4), "Scale by 2 along X and 4 along Z")
        self.assertStr(ScaleAxes(1, 3, 4), "Scale by 3 along Y and 4 along Z")
        self.assertStr(ScaleAxes(2, 3, 4), "Scale by 2 along X, 3 along Y, and 4 along Z")


    def test_to_matrix(self):
        self.assertEqual(ScaleAxes(1, 2, 3).to_matrix().row_values, [
            [1, 0, 0, 0],
            [0, 2, 0, 0],
            [0, 0, 3, 0],
            [0, 0, 0, 1],
        ])
