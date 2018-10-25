from warnings import warn

from cadlib.scad import ScadObject
from cadlib.transform import Transform
from cadlib.util.number import to_number

class ScaleXyz(Transform):
    def __init__(self, x, y, z):
        x = to_number(x, None, "x", [])
        y = to_number(y, None, "y", [])
        z = to_number(z, None, "z", [])

        if x == 0: warn("x is 0")
        if y == 0: warn("y is 0")
        if z == 0: warn("z is 0")

        self._xyz = [x, y, z]

    def __eq__(self, other):
        return isinstance(other, ScaleXyz) and other._xyz == self._xyz

    def __repr__(self):
        x, y, z = self._xyz
        return f"ScaleXyz({x!r}, {y!r}, {z!r})"

    def __str__(self):
        return "Scale by {}".format(self._xyz)

    def inverse(self):
        x, y, z = self._xyz
        return ScaleXyz(1/x, 1/y, 1/z)

    def to_scad(self, target):
        children = [target] if target is not None else []
        return ScadObject("scale", [self._xyz], None, children)