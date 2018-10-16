from tests.unit_test import TestCase
from cadlib.transform.primitives.rotate_xyz import RotateXyz

class TestRotateXyz(TestCase):
    def test_construction(self):
        # Valid
        r = RotateXyz( 60, 30, 15 )

        # Invalid
        with self.assertRaises(TypeError): RotateXyz(1, 2, "3")

    def test_equality(self):
        # Same object
        self.assertEqualToItself(RotateXyz( 60, 30, 15 ))

        # Equal objects
        self.assertEqual(RotateXyz( 60, 30, 15 ), RotateXyz( 60, 30, 15 ))

        # Different objects
        self.assertNotEqual(RotateXyz( 60, 30, 15 ), RotateXyz( 60, 30, 16 ))

        # Equal objects from different specifications

        pass


    def test_to_scad(self):
        r = RotateXyz(60, 30, 15)

        self.assertScadObjectTarget(r, None, "rotate", [[60, 30, 15]], None, None)
