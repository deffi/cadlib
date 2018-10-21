from cadlib.scad import ScadObject
from cadlib.transform.transform import Transform
from cadlib.util.number import to_number


class RotateYpr(Transform):
    def __init__(self, yaw, pitch, roll):
        yaw   = to_number(yaw  , None, "yaw  ", [])
        pitch = to_number(pitch, None, "pitch", [])
        roll  = to_number(roll , None, "roll ", [])
        self._ypr = [yaw, pitch, roll]

    def __eq__(self, other):
        if isinstance(other, RotateYpr):
            return self._ypr == other._ypr
        else:
            return False

    def __str__(self):
        return "Yaw-pitch-roll by by {} degrees".format(self._ypr)

    def to_scad(self, target):
        # yaw-pitch-roll in local coordinates corresponds to roll-pitch-yaw in global coordinates.
        yaw, pitch, roll = self._ypr

        # Start with the target and apply the transform
        result = target;
        if roll  != 0: result = ScadObject("rotate", [[0    , roll, 0  ]], None, [result] if result is not None else []);
        if pitch != 0: result = ScadObject("rotate", [[pitch, 0   , 0  ]], None, [result] if result is not None else []);
        if yaw   != 0: result = ScadObject("rotate", [[0    , 0   , yaw]], None, [result] if result is not None else []);

        # The result can be None if (a) the target was None, and (b) no transform were applied. Since this method is
        # not supposed to return None, return a null rotation.
        if result is None:
            result = ScadObject("rotate", [[0, 0, 0]], None, None);

        return result