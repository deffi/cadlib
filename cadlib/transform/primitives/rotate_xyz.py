from cadlib.scad import ScadObject
from cadlib.transform.transform import Transform
from cadlib.util.number import to_number


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

    def to_scad(self, target):
        children = [target] if target is not None else []
        return ScadObject("rotate", [list(self._xyz)], None, children)