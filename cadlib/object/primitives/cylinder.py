from numbers import Number
from warnings import warn

from cadlib.util import Vector, X, Y, Z
from cadlib.object import Object
from cadlib.scad import ScadObject
from cadlib.transform.primitives import RotateFromTo, Translate
from cadlib.util import both

class Cylinder(Object):
    def __init__(self, direction_or_base, length_or_cap, r = None, d = None):
        # Signatures:
        #   * Cylinder (direction, length, radius)
        #   * Cylinder (direction, length, d = diameter)
        #   * Cylinder (base, cap, radius)
        #   * Cylinder (base, cap, d = diameter)

        # direction_or_base must be a vector type, or 0 as a shortcut for (0, 0, 0)
        if isinstance(direction_or_base, (Vector, list, tuple)):
            # Vector type
            direction_or_base = Vector.convert(direction_or_base, "direction_or_base", 3)
        elif direction_or_base == 0:
            # Zero
            direction_or_base = Vector(0, 0, 0)
        else:
            raise ValueError("direction_or_base must be a vector type or 0")

        # length_or_base must be a vector or a number
        if isinstance (length_or_cap, Number):
            # Number - direction/length
            if direction_or_base.is_zero:
                raise ValueError("direction must be non-zero")

            if length_or_cap == 0: warn("length is 0")

            self._base = Vector(0, 0, 0)
            self._cap  = direction_or_base.normalized() * length_or_cap
        elif isinstance(length_or_cap, (Vector, list, tuple)):
            # Vector type - base/cap
            self._base = direction_or_base
            self._cap  = Vector.convert(length_or_cap, "length_or_cap", 3)

            if self._base == self._cap: warn("cap is equal to base")

        else:
            raise ValueError("length_or_cap must be a vector type or a number")

        # Radius or diameter
        if both(r, d):
            raise ValueError("radius and diameter cannot be specified together")
        elif r is not None:
            if r == 0: warn("radius is 0")
            self._radius = r
        elif d is not None:
            if d == 0: warn("diameter is 0")
            self._radius = d / 2
        else:
            raise ValueError("radius or diameter must be specified")

    def __eq__(self, other):
        return isinstance(other, Cylinder) \
            and other._base   == self._base \
            and other._cap    == self._cap \
            and other._radius == self._radius

    def __repr__(self):
        return f"Cylinder({self._base!r}, {self._cap!r}, r={self._radius!r}"

    def __str__(self):
        return f"Cylinder with radius {self._radius} from {self._base} to {self._cap}"

    def to_scad(self):
        length = (self._cap - self._base).length
        direction = (self._cap - self._base).normalized()

        # Create the cylinder
        cylinder = ScadObject("cylinder", [length], [('r', self._radius)], None)

        # Rotate to the correct orientation (skip if it is along the Z axis)
        if direction != Z:
            cylinder = RotateFromTo(frm = Z, to = direction, ignore_ambiguity = True).to_scad(cylinder)

        # Move to the correct position (skip if the base is at the origin)
        if self._base != Vector(0, 0, 0):
            cylinder = Translate(self._base).to_scad(cylinder)

        return cylinder
