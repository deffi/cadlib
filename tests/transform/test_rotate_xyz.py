from tests.unit_test import TestCase
from cadlib.transform.primitives import RotateXyz
from cadlib.util.geometry import affine_matrix
from cadlib.util import X, Y, Z

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

    def test_inverse(self):
        self.assertInverse(RotateXyz(30, 60, 90),
            RotateXyz(-30, 0, 0) * RotateXyz(0, -60, 0) * RotateXyz(0, 0, -90),
            symmetric=False)

    def test_to_scad(self):
        r = RotateXyz(0, 0, 0)
        self.assertScadObjectTarget(r, None, "rotate", [[0, 0, 0]], None, None)

        r = RotateXyz(60, 30, 15)
        self.assertScadObjectTarget(r, None, "rotate", [[60, 30, 15]], None, None)

    def test_repr(self):
        self.assertRepr(RotateXyz(1, 2, 3), "RotateXyz(1, 2, 3)")

    def test_str(self):
        self.assertStr(RotateXyz(0, 0, 0), "Rotate by 0° around X, Y, and Z")
        self.assertStr(RotateXyz(1, 0, 0), "Rotate by 1° around X")
        self.assertStr(RotateXyz(0, 2, 0), "Rotate by 2° around Y")
        self.assertStr(RotateXyz(0, 0, 3), "Rotate by 3° around Z")
        self.assertStr(RotateXyz(1, 2, 0), "Rotate by 1° around X and 2° around Y")
        self.assertStr(RotateXyz(1, 0, 3), "Rotate by 1° around X and 3° around Z")
        self.assertStr(RotateXyz(0, 2, 3), "Rotate by 2° around Y and 3° around Z")
        self.assertStr(RotateXyz(1, 2, 3), "Rotate by 1° around X, 2° around Y, and 3° around Z")

    def test_to_matrix(self):
        # No rotation
        self.assertAlmostEqual(RotateXyz( 0 , 0,  0).to_matrix(), affine_matrix(X, Y, Z))

        # 90 degrees around a single axis
        self.assertAlmostEqual(RotateXyz(90,  0,  0).to_matrix(), affine_matrix( X,  Z, -Y))
        self.assertAlmostEqual(RotateXyz( 0, 90,  0).to_matrix(), affine_matrix(-Z,  Y,  X))
        self.assertAlmostEqual(RotateXyz( 0,  0, 90).to_matrix(), affine_matrix( Y, -X,  Z))

        # 180 degrees around a single axis
        self.assertAlmostEqual(RotateXyz(180,   0,   0).to_matrix(), affine_matrix( X, -Y, -Z))
        self.assertAlmostEqual(RotateXyz(  0, 180,   0).to_matrix(), affine_matrix(-X,  Y, -Z))
        self.assertAlmostEqual(RotateXyz(  0,   0, 180).to_matrix(), affine_matrix(-X, -Y,  Z))

        # 90 degrees each around two axes
        self.assertAlmostEqual(RotateXyz(90, 90,  0).to_matrix(), affine_matrix(-Z,  X, -Y))
        self.assertAlmostEqual(RotateXyz(90,  0, 90).to_matrix(), affine_matrix( Y,  Z,  X))
        self.assertAlmostEqual(RotateXyz( 0, 90, 90).to_matrix(), affine_matrix(-Z, -X,  Y))

        # 90 degrees each around all three axes
        self.assertAlmostEqual(RotateXyz(90, 90, 90).to_matrix(), affine_matrix(-Z, Y, X))
