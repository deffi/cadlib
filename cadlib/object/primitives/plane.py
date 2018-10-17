from cadlib import infinity as inf
from cadlib.util import Z
from cadlib.object.object import Object
from cadlib.object.primitives.cube import Cube


class Plane(Object):
    # TODO unit test
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