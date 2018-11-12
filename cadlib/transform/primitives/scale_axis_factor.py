from warnings import warn

from cadlib.scad import ScadObject
from cadlib.transform import Transform
from cadlib.util.number import to_number
from cadlib.util import Vector
from cadlib.util.vector import X, Y, Z
from cadlib.transform.primitives import ScaleXyz, RotateFromTo

class ScaleAxisFactor(Transform):
    def __init__(self, axis, factor):
        axis = Vector.convert(axis, "axis", required_length=3)
        if axis.is_zero:
            raise ValueError("axis may not be zero-length")

        self._axis   = axis
        self._factor = to_number(factor, self._axis.length, "factor")

        if self._factor == 0: warn("factor is 0")


    def __eq__(self, other):
        return isinstance(other, ScaleAxisFactor) \
            and other._axis == self._axis \
            and other._factor == self._factor

    def __str__(self):
        return f"Scale by {self._factor} along {self._axis}"

    def __repr__(self):
        return f"ScaleAxisFactor({self._axis!r}, {self._factor!r})"

    def inverse(self):
        return ScaleAxisFactor(self._axis, 1 / self._factor)

    def _equivalent(self):
        transform_axis = self._axis.closest_axis()

        forward_rotation = RotateFromTo(self._axis, transform_axis)
        scale = ScaleXyz(*(transform_axis * self._factor).replace(0, 1))
        back_rotation = RotateFromTo(transform_axis, self._axis)

        return back_rotation * scale * forward_rotation

    def to_scad(self, target):
        # Since OpenSCAD does not have axis/factor scaling, it has to be
        # translated to corresponding XYZ scales, potentially combined with
        # rotations.

        children = [target] if target is not None else []
        comment = str(self)

        # Special case: if the factor is 1, the scale can be expressed as the
        # unit scale
        if self._factor == 1:
            return ScadObject("scale", [[1, 1, 1]], None, children, comment)

        # Special case: if the axis is aligned with one of the coordinate axes,
        # the scale can be expressed as an XYZ scale along that axis.
        if self._axis.collinear(X):
            return ScadObject("scale", [[self._factor, 1, 1]], None, children, comment)
        if self._axis.collinear(Y):
            return ScadObject("scale", [[1, self._factor, 1]], None, children, comment)
        if self._axis.collinear(Z):
            return ScadObject("scale", [[1, 1, self._factor]], None, children, comment)

        # General case
        return self._equivalent().to_scad(target).comment(comment)

    def to_matrix(self):
        # No special-case handling here, the result would be identical
        return self._equivalent().to_matrix()
