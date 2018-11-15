from cadlib.scad import ScadObject
from cadlib.transform import Transform, Chained
from cadlib.transform.primitives import RotateXyz
from cadlib.util import number
from cadlib.util.geometry import rotation_matrix
from cadlib.util import degree


class RotateYpr(Transform):
    def __init__(self, yaw, pitch, roll):
        yaw   = number.convert(yaw, "yaw")
        pitch = number.convert(pitch, "pitch")
        roll  = number.convert(roll, "roll")
        self._ypr = [yaw, pitch, roll]

    def __eq__(self, other):
        return (isinstance(other, RotateYpr)
            and self._ypr == other._ypr)

    def __str__(self):
        y, p, r = self._ypr

        parts = []
        if y != 0: parts.append(f"yaw {y}°")
        if p != 0: parts.append(f"pitch {p}°")
        if r != 0: parts.append(f"roll {r}°")

        if len(parts) == 0:
            return "Yaw, pitch, and roll by 0°"
        else:
            return f"{', '.join(parts)}".capitalize()

    def __repr__(self):
        y, p, r = self._ypr
        return f"RotateYpr({y!r}, {p!r}, {r!r})"

    def inverse(self):
        y, p, r = self._ypr
        return RotateYpr(0, 0, -r) * RotateYpr(0, -p, 0) * RotateYpr(-y, 0, 0)

    def _equivalent(self):
        yaw, pitch, roll = self._ypr

        # yaw-pitch-roll in local coordinates corresponds to roll-pitch-yaw in
        # global coordinates.
        transforms = []
        if yaw != 0 or pitch != 0: transforms.append(RotateXyz(pitch, 0   , yaw))
        if roll != 0             : transforms.append(RotateXyz(0    , roll, 0  ))
        return Chained(transforms)

    def to_scad(self, target):
        equivalent = self._equivalent()

        if equivalent == Chained([]):
            # The equivalent transform is empty (this can happen if yaw, pitch,
            # and roll are all 0). This would result in an empty ScadObject
            # (with children if target is not None). Instead, generate an empty
            # rotation for improved clarity of the generated code.
            equivalent = RotateXyz(0, 0, 0)

        return equivalent.to_scad(target).comment(str(self))

    def to_matrix(self):
        # Alternative - direct generation:
        # return rotation_matrix(2, yaw*degree) * rotation_matrix(0, pitch*degree) * rotation_matrix(1, roll*degree)

        return self._equivalent().to_matrix()
