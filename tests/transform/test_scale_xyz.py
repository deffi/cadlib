from tests.unit_test import TestCase
from cadlib.transform.primitives.scale_xyz import ScaleXyz

class TestScaleXyz(TestCase):
    def test_construction(self):
        # Valid
        ScaleXyz([1, 2, 3])
        ScaleXyz(2)

        # Invalid
        with self.assertRaises(TypeError): ScaleXyz([1, 2, "3"])
        # TODO this should be a TypeError
        with self.assertRaises(ValueError): ScaleXyz("3")

    def test_equality(self):
        # Same object
        self.assertEqualToItself(ScaleXyz([60, 30, 15]))

        # Equal objects
        self.assertEqual(ScaleXyz([60, 30, 15]), ScaleXyz([60, 30, 15]))

        # Different objects
        self.assertNotEqual(ScaleXyz([60, 30, 15]), ScaleXyz([60, 30, 16]))

        # Equal objects from different specifications
        self.assertEqual(ScaleXyz(2), ScaleXyz([2, 2, 2]))

    def test_to_scad(self):
        s = ScaleXyz([1, 2, -1])

        self.assertScadObjectTarget(s, None, "scale", [[1, 2, -1]], None, None)
