from tests.unit_test import TestCase
from cadlib.transform.primitives import ScaleUniform

class TestScaleUniform(TestCase):
    def test_construction(self):
        # Valid
        ScaleUniform(2)

        # Valid, but with warning
        with self.assertWarns(UserWarning): ScaleUniform(0)

        # Invalid
        with self.assertRaises(TypeError): ScaleUniform([1, 2, 3])
        with self.assertRaises(TypeError): ScaleUniform("2")

    def test_equality(self):
        # Same object
        self.assertEqualToItself(ScaleUniform(2))

        # Equal objects
        self.assertEqual(ScaleUniform(2), ScaleUniform(2))

        # Different objects
        self.assertNotEqual(ScaleUniform(2), ScaleUniform(3))

    def test_inverse(self):
        self.assertInverse(ScaleUniform(2), ScaleUniform(0.5))

    def test_to_scad(self):
        self.ignore_scad_comments = True

        s = ScaleUniform(2)

        self.assertScadObjectTarget(s, None, "scale", [[2, 2, 2]], None, None)

    def test_repr(self):
        self.assertRepr(ScaleUniform(2), "ScaleUniform(2)")
