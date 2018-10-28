from cadlib.scad import ScadObject
from cadlib.transform import Transform, Chained
from cadlib.transform.primitives import RotateXyz
from cadlib.util.number import to_number
from cadlib.util.geometry import rotation_matrix
from cadlib.util import degree

class RotateYpr(Transform):
    def __init__(self, yaw, pitch, roll):
        yaw   = to_number(yaw  , None, "yaw"  , [])
        pitch = to_number(pitch, None, "pitch", [])
        roll  = to_number(roll , None, "roll" , [])
        self._ypr = [yaw, pitch, roll]

    def __eq__(self, other):
        if isinstance(other, RotateYpr):
            return self._ypr == other._ypr
        else:
            return False

    def __str__(self):
        return "Yaw-pitch-roll by by {} degrees".format(self._ypr)

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
        return self._equivalent().to_scad(target).comment(repr(self))

    def to_matrix(self):
        # Alternative - direct generation:
        # return rotation_matrix(2, yaw*degree) * rotation_matrix(0, pitch*degree) * rotation_matrix(1, roll*degree)

        return self._equivalent().to_matrix()
