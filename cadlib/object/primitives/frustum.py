from warnings import warn

from cadlib.util import Vector, X, Y, Z
from cadlib.object import Object
from cadlib.scad import ScadObject
from cadlib.transform.primitives import RotateFromTo, Translate
from cadlib.util import number

class Frustum(Object):
    def __init__(self, base, cap, base_radius, cap_radius):
        self._base = Vector.convert(base, "base", required_length=3)
        self._cap  = Vector.convert(cap , "cap" , required_length=3)
        self._base_radius = number.convert(base_radius, "base_radius")
        self._cap_radius  = number.convert(cap_radius, "cap_radius")

        # Warn if the cap is equal to the base (zero length) or both radii are
        # zero (zero thickness; note that it is allowed for *one* of the radii
        # to be zero).
        if self._base == self._cap:                    warn("length is 0")
        if self._base_radius == self._cap_radius == 0: warn("radius is 0")

    @classmethod
    def direction_length(cls, direction, length, base_radius, cap_radius):
        direction = Vector.convert(direction, "direction", required_length=3)
        length    = number.convert(length, "length")

        if direction.is_zero:
            raise ValueError("direction must be non-zero")

        base = Vector(0, 0, 0)
        cap = direction.normalized() * length
        return cls(base, cap, base_radius, cap_radius)

    def __eq__(self, other):
        return (isinstance(other, Frustum)
            and other._base        == self._base
            and other._cap         == self._cap
            and other._base_radius == self._base_radius
            and other._cap_radius  == self._cap_radius)

    def __repr__(self):
        return f"Frustum({self._base!r}, {self._cap!r}, {self._base_radius!r}, {self._cap_radius!r})"

    def __str__(self):
        return f"Frustum with base {self._base} (base radius {self._base_radius}) and cap {self._cap} (cap radius {self._cap_radius})"

    def to_scad(self):
        length = (self._cap - self._base).length
        direction = (self._cap - self._base).normalized()

        # Create the cylinder
        if self._base_radius == self._cap_radius:
            cylinder = ScadObject("cylinder", [length], [('r', self._base_radius)], None)
        else:
            cylinder = ScadObject("cylinder", [length], [('r1', self._base_radius), ('r2', self._cap_radius)], None)

        # Rotate to the correct orientation (skip if it is along the Z axis)
        if direction != Z:
            cylinder = RotateFromTo(frm = Z, to = direction, ignore_ambiguity = True).to_scad(cylinder)

        # Move to the correct position (skip if the base is at the origin)
        if self._base != Vector(0, 0, 0):
            cylinder = Translate(self._base).to_scad(cylinder)

        return cylinder
