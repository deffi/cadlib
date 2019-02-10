from warnings import warn

from cadlib.util import Matrix
from cadlib.scad import ScadObject
from cadlib.transform import Transform
from cadlib.util import number


class ScaleAxes(Transform):
    def __init__(self, x, y, z):
        x = number.convert(x, "x")
        y = number.convert(y, "y")
        z = number.convert(z, "z")

        if x == 0: warn("x is 0")
        if y == 0: warn("y is 0")
        if z == 0: warn("z is 0")

        # TODO property name (can also be two-dimensional)
        self._xyz = [x, y, z]

    def __eq__(self, other):
        return (isinstance(other, ScaleAxes)
            and other._xyz == self._xyz)

    def __repr__(self):
        x, y, z = self._xyz
        return f"ScaleAxes({x!r}, {y!r}, {z!r})"

    def __str__(self):
        x, y, z = self._xyz

        parts = []
        if x != 1: parts.append(f"{x} along X")
        if y != 1: parts.append(f"{y} along Y")
        if z != 1: parts.append(f"{z} along Z")

        if len(parts) == 0:
            return "Scale by 1 along X, Y, and Z"
        elif len(parts) == 1:
            return f"Scale by {', '.join(parts)}"
        elif len(parts) == 2:
            return f"Scale by {' and '.join(parts)}"
        else:
            parts[-1] = "and " + parts[-1]
            return f"Scale by {', '.join(parts)}"

    def inverse(self):
        x, y, z = self._xyz
        return ScaleAxes(1 / x, 1 / y, 1 / z)

    def to_scad(self, target):
        children = [target] if target is not None else []
        return ScadObject("scale", [self._xyz], None, children)

    def to_matrix(self):
        x, y, z = self._xyz
        return Matrix(rows=[
            [x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1],
        ])
