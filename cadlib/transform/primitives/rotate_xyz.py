from cadlib.scad import ScadObject
from cadlib.transform import Transform
from cadlib.util.number import to_number
from cadlib.util.geometry import rotation_matrix
from cadlib.util import degree

class RotateXyz(Transform):
    def __init__(self, x, y, z):
        x = to_number(x, None, "x", [])
        y = to_number(y, None, "y", [])
        z = to_number(z, None, "z", [])
        self._xyz = [x, y, z]

    def __eq__(self, other):
        if isinstance(other, RotateXyz):
            return self._xyz == other._xyz
        else:
            return False

    def __str__(self):
        return "Rotate by {} degrees around x, y, and z".format(self._xyz)

    def __repr__(self):
        x, y, z = self._xyz
        return f"RotateXyz({x!r}, {y!r}, {z!r})"

    def inverse(self):
        x, y, z = self._xyz
        return RotateXyz(0, 0, -z) * RotateXyz(0, -y, 0) * RotateXyz(-x, 0, 0)

    def to_scad(self, target):
        children = [target] if target is not None else []
        return ScadObject("rotate", [list(self._xyz)], None, children)

    def to_matrix(self):
        x, y, z = self._xyz
        return rotation_matrix(2, z*degree) * rotation_matrix(1, y*degree) * rotation_matrix(0, x*degree)
