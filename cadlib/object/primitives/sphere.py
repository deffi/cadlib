from warnings import warn

from cadlib.object import Object
from cadlib.scad import ScadObject
from cadlib.util import both


class Sphere(Object):
    def __init__(self, r = None, d = None):
        # Radius or diameter
        if both(r, d):
            raise ValueError("radius and diameter cannot be specified together")
        elif r is not None:
            if r == 0: warn("radius is 0")
            self._radius = r
        elif d is not None:
            if d == 0: warn("diameter is 0")
            self._radius = d / 2
        else:
            raise ValueError("radius or diameter must be specified")

    def __eq__(self, other):
        return isinstance(other, Sphere) and other._radius == self._radius

    def __repr__(self):
        return f"Sphere(r={self._radius!r})"

    def to_scad(self):
        return ScadObject("sphere", [self._radius], None, None)
