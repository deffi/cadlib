from warnings import warn

from cadlib.util import Vector
from cadlib.scad import ScadObject
from cadlib.transform import Transform


class RotateFromTo(Transform):
    def __init__(self, frm, to, ignore_ambiguity = False):
        frm = Vector.convert(frm, "frm", 3)
        to  = Vector.convert(to , "to" , 3)

        if frm.is_zero:
            raise ValueError("frm may not be zero-length")
        if to.is_zero:
            raise ValueError("frm may not be zero-length")

        if not ignore_ambiguity:
            if frm.collinear(to) and frm.dot(to) < 0:
                warn("Rotation from {} to {} is ambiguous because the vectors are colinear and opposite"
                     .format(frm.values, to.values), UserWarning, 2)

        self._frm = frm
        self._to  = to

    def __eq__(self, other):
        if isinstance(other, RotateFromTo):
            return self._frm == other._frm and self._to == other._to
        else:
            return False

    def __str__(self):
        return "Rotate from {} to {}".format(self._frm, self._to)

    def __repr__(self):
        return f"RotateFromTo({self._frm!r}, {self._to!r})"

    def inverse(self):
        return RotateFromTo(self._to, self._frm)

    def to_scad(self, target):
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


        if axis is None:
            # No rotation
            return target
        else:
            # Yes rotation
            axis = axis.normalized()
            children = [target] if target is not None else []
            comment = repr(self)
            return ScadObject("rotate", None, [("a", angle), ("v", axis.values)], children, comment)
