from numbers import Number

from cadlib.scad.scad import ScadObject
from cadlib.transform.transform import Transform
from cadlib.util.number import to_list_of_numbers

class Scale(Transform):
    def __init__(self, xyz):
        if isinstance(xyz, Number):
            self._xyz = [xyz, xyz, xyz]
        else:
            self._xyz = to_list_of_numbers(xyz, "xyz", 3)

    def __eq__(self, other):
        return isinstance(other, Scale) and other._xyz == self._xyz

    def __str__(self):
        return "Scale by {}".format(self._xyz)

    def to_scad(self, target):
        children = [target] if target is not None else []
        return ScadObject("scale", [self._xyz], None, children)