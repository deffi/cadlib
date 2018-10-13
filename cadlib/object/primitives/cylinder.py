from cadlib.object.object import Object
from cadlib.scad.scad import ScadObject


class Cylinder(Object):
    def __init__(self, l, r):
        self._l = l
        self._r = r

    def __eq__(self, other):
        return isinstance(other, Cylinder) and other._l == self._l and other._r == self._r

    def __repr__(self):
        return "Cylinder with radius {} and length {}".format(self._r, self._l)

    def to_scad(self):
        return ScadObject("cylinder", [self._l], [('r', self._r)], None)