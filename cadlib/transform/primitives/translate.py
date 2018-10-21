from cadlib.util import Vector
from cadlib.scad import ScadObject
from cadlib.transform.transform import Transform


class Translate(Transform):
    def __init__(self, vector):
        self._vector = Vector.convert(vector, "vector", 3)

    def __eq__(self, other):
        return isinstance(other, Translate) and other._vector == self._vector

    def __str__(self):
        return "Translate by {}".format(self._vector)

    def to_scad(self, target):
        children = [target] if target is not None else []
        return ScadObject("translate", [list(self._vector)], None, children)