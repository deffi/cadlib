from warnings import warn

from cadlib.util import Vector, Matrix
from cadlib.transform import Transform
from cadlib.transform.primitives import RotateAxisAngle, RotateXyz

class RotateFromTo(Transform):
    def __init__(self, frm, to, ignore_ambiguity = False):
        frm = Vector.convert(frm, "frm", required_length=3)
        to  = Vector.convert(to , "to" , required_length=3)

        if frm.is_zero:
            raise ValueError("frm may not be zero-length")
        if to.is_zero:
            raise ValueError("frm may not be zero-length")

        if not ignore_ambiguity:
            if frm.collinear(to) and frm.dot(to) < 0:
                warn("Rotation from {} to {} is ambiguous because the vectors are colinear and opposite"
                     .format(frm, to), UserWarning, 2)

        self._frm = frm
        self._to  = to

    def __eq__(self, other):
        return (isinstance(other, RotateFromTo)
            and self._frm == other._frm
            and self._to  == other._to)

    def __str__(self):
        return "Rotate from {} to {}".format(self._frm, self._to)

    def __repr__(self):
        return f"RotateFromTo({self._frm!r}, {self._to!r})"

    def inverse(self):
        return RotateFromTo(self._to, self._frm)

    def _to_axis_angle(self):
        if self._frm.collinear(self._to):
            # Special case: the vectors are collinear
            if self._frm.dot(self._to) > 0:
                # Same direction. No rotation.
                axis  = None
                angle = None
            else:
                # Opposite directions. Rotation by 180 degrees, axis is
                # ambiguous.
                axis  = self._frm.normal()  # Arbitrary
                angle = 180
        else:
            # Regular case
            axis  = self._frm.cross(self._to)
            angle = self._frm.angle(self._to)

        return axis, angle

    def to_scad(self, target):
        axis, angle = self._to_axis_angle()

        if axis is None:
            # No rotation. Generate a zero XYZ transform instead of simply
            # returning the target. This improves code clarity and also ensures
            # that a valid ScadObject is returned even if target is None.
            return RotateXyz(0, 0, 0).to_scad(target).comment(str(self))
        else:
            # Yes rotation
            return RotateAxisAngle(axis.normalized(), angle).to_scad(target).comment(str(self))

    def to_matrix(self):
        axis, angle = self._to_axis_angle()

        if axis is None:
            # No rotation
            return Matrix.identity(4)
        else:
            # Yes rotation
            return RotateAxisAngle(axis, angle).to_matrix()
