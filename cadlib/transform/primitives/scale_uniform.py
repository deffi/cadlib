from cadlib.scad import ScadObject
from cadlib.transform import Transform
from cadlib.util.number import to_number

class ScaleUniform(Transform):
    def __init__(self, factor):
        self._factor = to_number(factor, 1, "factor")

    def __eq__(self, other):
        return isinstance(other, ScaleUniform) and other._factor == self._factor

    def __str__(self):
        return "Uniform scale by {}".format(self._factor)

    def __repr__(self):
        return f"ScaleUniform({self._factor!r})"

    def to_scad(self, target):
        children = [target] if target is not None else []
        f = self._factor
        return ScadObject("scale", [[f, f, f]], None, children)
