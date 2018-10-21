from numbers import Number

from cadlib.scad import ScadObject
from cadlib.transform.transform import Transform
from cadlib.util.number import to_number

class ScaleXyz(Transform):
    def __init__(self, x, y, z):
        x = to_number(x, None, "x", [])
        y = to_number(y, None, "y", [])
        z = to_number(z, None, "z", [])
        self._xyz = [x, y, z]

    def __eq__(self, other):
        return isinstance(other, ScaleXyz) and other._xyz == self._xyz

    def __str__(self):
        return "Scale by {}".format(self._xyz)

    def to_scad(self, target):
        children = [target] if target is not None else []
        return ScadObject("scale", [self._xyz], None, children)