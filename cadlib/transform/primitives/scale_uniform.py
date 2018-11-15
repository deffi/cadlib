from warnings import warn

from cadlib.util import Matrix
from cadlib.scad import ScadObject
from cadlib.transform import Transform
from cadlib.util import number

class ScaleUniform(Transform):
    def __init__(self, factor):
        self._factor = number.convert(factor, "factor")

        if self._factor == 0: warn("factor is 0")


    def __eq__(self, other):
        return (isinstance(other, ScaleUniform)
            and other._factor == self._factor)

    def __str__(self):
        return "Scale by {}".format(self._factor)

    def __repr__(self):
        return f"ScaleUniform({self._factor!r})"

    def inverse(self):
        return ScaleUniform(1 / self._factor)

    def to_scad(self, target):
        children = [target] if target is not None else []
        f = self._factor
        return ScadObject("scale", [[f, f, f]], None, children, repr(self))

    def to_matrix(self):
        f = self._factor
        return Matrix.from_rows(
            [f, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, f, 0],
            [0, 0, 0, 1],
        )
