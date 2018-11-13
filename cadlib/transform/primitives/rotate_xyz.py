from cadlib.scad import ScadObject
from cadlib.transform import Transform
from cadlib.util.number import to_number
from cadlib.util.geometry import rotation_matrix
from cadlib.util import degree

class RotateXyz(Transform):
    def __init__(self, x, y, z):
        x = to_number(x, "x")
        y = to_number(y, "y")
        z = to_number(z, "z")
        self._xyz = [x, y, z]

    def __eq__(self, other):
        return (isinstance(other, RotateXyz)
            and self._xyz == other._xyz)

    def __str__(self):
        x, y, z = self._xyz

        parts = []
        if x != 0: parts.append(f"{x}° around X")
        if y != 0: parts.append(f"{y}° around Y")
        if z != 0: parts.append(f"{z}° around Z")

        if len(parts) == 0:
            return "Rotate by 0° around X, Y, and Z"
        elif len(parts) == 1:
            return f"Rotate by {', '.join(parts)}"
        elif len(parts) == 2:
            return f"Rotate by {' and '.join(parts)}"
        else:
            parts[-1] = "and " + parts[-1]
            return f"Rotate by {', '.join(parts)}"

    def __repr__(self):
        x, y, z = self._xyz
        return f"RotateXyz({x!r}, {y!r}, {z!r})"

    def inverse(self):
        x, y, z = self._xyz
        return RotateXyz(-x, 0, 0) * RotateXyz(0, -y, 0) * RotateXyz(0, 0, -z)

    def to_scad(self, target):
        children = [target] if target is not None else []
        return ScadObject("rotate", [list(self._xyz)], None, children)

    def to_matrix(self):
        x, y, z = self._xyz
        return rotation_matrix(2, z*degree) * rotation_matrix(1, y*degree) * rotation_matrix(0, x*degree)
