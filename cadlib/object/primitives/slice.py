from cadlib import infinity as inf
from cadlib.geometry import Z
from cadlib.object.object import Object
from cadlib.object.primitives.cube import Cube


class Slice(Object):
    # TODO unit test
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