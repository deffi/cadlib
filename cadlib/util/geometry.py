from cadlib.util import Matrix
import math


def affine_matrix(x, y, z, t = None):
    """Create a 4x4 matrix representing an arbitrary affine transform.

    The created matrix describes an affine transform in 3D homogeneous
    coordinates:
        v -> (v1 * x + t1, v2 * y + t2, v3 * z + t3)

    The base vectors x, y, and z are not required to be orthogonal or
    normalized. The translation vector t can be omitted if it is the zero
    vector.
    """
    t = t or [0, 0, 0]
    return Matrix(rows = [
        [x[0], y[0], z[0], t[0]],
        [x[1], y[1], z[1], t[1]],
        [x[2], y[2], z[2], t[2]],
        [0   , 0   , 0   , 1],
    ])


def rotation_matrix(axis_index, angle):
    """Create a 4x4 matrix representing a rotation around a single axis.

    The created matrix describes a rotation around the axis specified by its
    index. axis_index can be 0, 1, or 2. The angle is specified in radians.
    """

    i1 = (axis_index + 1) % 3
    i2 = (axis_index + 2) % 3

    s = math.sin(angle)
    c = math.cos(angle)

    rows = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]

    rows[i1][i1] = c
    rows[i1][i2] = -s
    rows[i2][i1] = s
    rows[i2][i2] = c

    return Matrix(rows = rows)
