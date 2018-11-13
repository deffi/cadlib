from cadlib.util import Vector, Matrix
from cadlib.scad import ScadObject
from cadlib.transform import Transform


class Translate(Transform):
    def __init__(self, vector):
        self._vector = Vector.convert(vector, "vector", required_length=3)

    def __eq__(self, other):
        return (isinstance(other, Translate)
            and other._vector == self._vector)

    def __str__(self):
        return "Translate by {}".format(self._vector)

    def __repr__(self):
        return f"Translate({self._vector!r})"

    def inverse(self):
        return Translate(-self._vector)

    def to_scad(self, target):
        children = [target] if target is not None else []
        return ScadObject("translate", [list(self._vector)], None, children)

    def to_matrix(self):
        x, y, z = self._vector
        return Matrix.from_rows(
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1],
        )
