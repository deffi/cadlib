from cadlib.scad import ScadObject
from cadlib.transform import Transform
from cadlib.util.number import to_number
from cadlib.util import Vector
from cadlib.util.vector import X, Y, Z
from cadlib.transform.primitives import ScaleXyz, RotateFromTo

class ScaleAxisFactor(Transform):
    def __init__(self, axis, factor):
        axis = Vector.convert(axis, "axis", 3)
        if axis.is_zero:
            raise ValueError("axis may not be zero-length")

        self._axis   = axis
        self._factor = to_number(factor, self._axis.length, "factor")

    def __eq__(self, other):
        return isinstance(other, ScaleAxisFactor) \
            and other._axis == self._axis \
            and other._factor == self._factor

    def __str__(self):
        return "Scale along {} by {}".format(self._axis, self._factor)

    def to_scad(self, target):
        # Since OpenSCAD does not have axis/factor scaling, it has to be
        # translated to corresponding XYZ scales, potentially combined with
        # rotations.

        children = [target] if target is not None else []

        # Special case: if the factor is 1, the scale can be expressed as the
        # unit scale
        if self._factor == 1:
            return ScadObject("scale", [[1, 1, 1]], None, children)

        # Special case: if the axis is aligned with one of the coordinate axes,
        # the scale can be expressed as an XYZ scale along that axis.
        if self._axis.collinear(X):
            return ScadObject("scale", [[self._factor, 1, 1]], None, children)
        if self._axis.collinear(Y):
            return ScadObject("scale", [[1, self._factor, 1]], None, children)
        if self._axis.collinear(Z):
            return ScadObject("scale", [[1, 1, self._factor]], None, children)

        # General case
        # TODO as single multiplication
        transform_axis = self._axis.closest_axis()
        equivalent = RotateFromTo(self._axis, transform_axis)
        equivalent = ScaleXyz(*(transform_axis * self._factor).values) * equivalent
        equivalent = RotateFromTo(transform_axis, self._axis) * equivalent

        return equivalent.to_scad(target)
