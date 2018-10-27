from cadlib.util.matrix import Matrix
from tests.unit_test import TestCase
from cadlib.util.vector import Vector, X, Y, Z
from cadlib.util.geometry import affine_matrix, rotation_matrix
from cadlib.util import degree

class TestGeometry(TestCase):
    def test_affine_matrix(self):
        self.assertAlmostEqual(affine_matrix(X, Y, Z), Matrix(rows = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]))
        self.assertAlmostEqual(affine_matrix(X, Y, Z, [1, 2, 3]), Matrix(rows = [
            [1, 0, 0, 1],
            [0, 1, 0, 2],
            [0, 0, 1, 3],
            [0, 0, 0, 1],
        ]))

    def test_rotation_matrix(self):
        self.assertAlmostEqual(rotation_matrix(0, 0 * degree), affine_matrix(X, Y, Z))

        self.assertAlmostEqual(rotation_matrix(0, 90 * degree), affine_matrix( X,  Z, -Y))
        self.assertAlmostEqual(rotation_matrix(1, 90 * degree), affine_matrix(-Z,  Y,  X))
        self.assertAlmostEqual(rotation_matrix(2, 90 * degree), affine_matrix( Y, -X,  Z))

        self.assertOrthogonal(rotation_matrix(0,  0 * degree))

        rx = rotation_matrix(0, 10 * degree)
        ry = rotation_matrix(1, 10 * degree)
        rz = rotation_matrix(2, 10 * degree)

        self.assertOrthogonal(rx)
        self.assertOrthogonal(ry)
        self.assertOrthogonal(rz)
        self.assertOrthogonal(rx * ry * rz)
        self.assertOrthogonal(rx * rx * rx)
