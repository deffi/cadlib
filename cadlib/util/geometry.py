from cadlib.util import Matrix
import math

# TODO test
def affine_matrix(x, y, z, t = None):
    t = t or [0, 0, 0]
    return Matrix(rows = [
        [x[0], y[0], z[0], t[0]],
        [x[1], y[1], z[1], t[1]],
        [x[2], y[2], z[2], t[2]],
        [0   , 0   , 0   , 1],
    ])

# TODO test
def rotation_matrix(axis_index, angle):
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