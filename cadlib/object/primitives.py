from numbers import Number

from cadlib import infinity as inf
from cadlib.geometry import *
from cadlib.object.object import Object
from cadlib.scad.scad import ScadObject


class Cube(Object):
    def __init__(self, size):
        if isinstance(size, Number):
            self._size = [size, size, size]
        elif len(size) == 3:
            self._size = size
        else:
            raise ValueError("Invalid size: {}".format(size))

    def __eq__(self, other):
        return isinstance(other, Cube) and other._size == self._size

    def __repr__(self):
        return "Cube with size {}".format(self._size)

    def to_scad(self):
        return ScadObject("cube", [self._size], None, None)

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

class Sphere(Object):
    def __init__(self, r):
        self._r = r

    def __eq__(self, other):
        return isinstance(other, Sphere) and other._r == self._r

    def __repr__(self):
        return "Sphere with radius {}".format(self._r)

    def to_scad(self):
        return ScadObject("sphere", [self._r], None, None)

# TODO unit test
class Plane(Object):
    def __init__(self, normal, offset):
        self._normal = normal
        self._offset = offset

    def __eq__(self, other):
        return isinstance(other, Plane) and other._normal == self._normal and other._offset == self._offset

    def __repr__(self):
        return "Plane with normal {}, offset {}".format(self._normal, self._offset)

    def to_scad(self):
        return Cube([inf, inf, inf]) \
            .translate([-inf / 2, -inf / 2, -inf]) \
            .up(self._offset) \
            .rotate(frm = Z, to = self._normal, ignore_ambiguity = True) \
            .to_scad()

# TODO unit test
class Slice(Object):
    def __init__(self, normal, offset1, offset2):
        self._normal = normal
        self._offset1 = offset1
        self._offset2 = offset2

    def __eq__(self, other):
        if not isinstance(other, Slice): return False
        return other._normal == self._normal and other._offset1 == self._offset1 and other._offset2 == self._offset2

    def __repr__(self):
        return "Slice with normal {}, offsets {}, {}".format(self._normal, self._offset1, self._offset2)

    def to_scad(self):
        o1 = min(self._offset1, self._offset2)
        o2 = max(self._offset1, self._offset2)

        return Cube([inf, inf, o2 - o1]) \
            .translate([-inf / 2, -inf / 2, 0]) \
            .up(o1) \
            .rotate(frm = Z, to = self._normal, ignore_ambiguity = True) \
            .to_scad()
