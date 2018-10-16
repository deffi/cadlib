from tests.unit_test import TestCase
from cadlib.transform.primitives.scale import Scale

class TestScale(TestCase):
    def test_construction(self):
        # Valid
        Scale([1, 2, 3])

        # Invalid
        with self.assertRaises(TypeError): Scale([1, 2, "3"])

    def test_equality(self):
        # Same object
        self.assertEqualToItself(Scale([60, 30, 15]))

        # Equal objects
        self.assertEqual(Scale([60, 30, 15]), Scale([60, 30, 15]))

        # Different objects
        self.assertNotEqual(Scale([60, 30, 15]), Scale([60, 30, 16]))

        # TODO can we pass a single value?

    def test_to_scad(self):
        s = Scale([1, 2, -1])

        self.assertScadObjectTarget(s, None, "scale", [[1, 2, -1]], None, None)
