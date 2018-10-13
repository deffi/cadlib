from cadlib.object.object import Object
from cadlib.scad.scad import ScadObject


class Sphere(Object):
    def __init__(self, r):
        self._r = r

    def __eq__(self, other):
        return isinstance(other, Sphere) and other._r == self._r

    def __repr__(self):
        return "Sphere with radius {}".format(self._r)

    def to_scad(self):
        return ScadObject("sphere", [self._r], None, None)