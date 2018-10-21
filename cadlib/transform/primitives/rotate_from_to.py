from warnings import warn

from cadlib.util import Vector
from cadlib.scad.scad import ScadObject
from cadlib.transform.transform import Transform
from cadlib.transform.primitives import RotateXyz, RotateAxisAngle


class RotateFromTo(Transform):
    def __init__(self, frm, to, ignore_ambiguity = False):
        frm = Vector.convert(frm, "frm", 3)
        to  = Vector.convert(to , "to" , 3)

        # TODO use isZero (everwhere; see also lengthSquared)
        if frm.length == 0:
            raise ValueError("frm may not be zero-length")
        if to.length == 0:
            raise ValueError("frm may not be zero-length")

        self._frm = frm
        self._to  = to
        self._ignore_ambiguity = ignore_ambiguity

    def __eq__(self, other):
        if isinstance(other, RotateFromTo):
            return self._frm == other._frm and self._to == other._to
        else:
            return False

    def __str__(self):
        return "Rotate from {} to {}".format(self._frm, self._to)

    def to_scad(self, target):
        axis = self._frm.cross(self._to)
        if axis.length == 0:
            # Special case: the vectors are colinear. This means either no rotation (same direction, dot product
            # positive) or rotation by 180 around ambiguous axis (opposite directions, dot product negative).
            if self._frm.dot(self._to) > 0:
                # Rotation has no effect - return an identity transform
                return RotateXyz(0, 0, 0).to_scad(target) # TODO meh
            else:
                # Rotation is ambiguous
                # TODO do this in the constructor
                if not self._ignore_ambiguity:
                    warn("Rotation from {} to {} is ambiguous because the vectors are colinear and opposite"
                         .format(self._frm.values, self._to.values), RuntimeWarning, 2)
                return RotateAxisAngle(self._frm.normal().normalized(), 180).to_scad(target) # TODO meh
        else:
            # Regular case
            angle = self._frm.angle(self._to)
            return RotateAxisAngle(axis.normalized(), angle).to_scad(target) # TODO meh


        children = [target] if target is not None else []
        return ScadObject("rotate", None, [("a", self._angle), ("v", list(self._axis))], children)
