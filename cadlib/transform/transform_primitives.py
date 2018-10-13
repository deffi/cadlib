from numbers import Number
from cadlib.geometry import Vector
from cadlib.transform.transform import Transform
from cadlib.scad.scad import ScadObject

# Where a vector is appropriate, a list of 3 numbers will also be accepted. Note that, in particular, this does not
# apply to RotateXyz and RotateRpy, whose arguments are not vectors.

#############
## Helpers ##
#############

def _to_vector(value, label, required_length):
    if required_length is not None and len(value) != required_length:
        raise ValueError("Invalid length for {}, must be {}".format(label, required_length))

    if isinstance(value, Vector):
        return value
    elif isinstance(value, (list, tuple)):
        return Vector(*value)
    else:
        raise TypeError("Invalid {}: {}".format(label, value))

def _to_list_of_numbers(value, label, required_length):
    if required_length is not None and len(value) != required_length:
        raise ValueError("Invalid length for {}, must be {}".format(label, required_length))

    for x in value:
        if not isinstance(x, Number):
            raise TypeError("Must be a number: {}".format(x))

    if isinstance(value, (Vector, list, tuple)):
        return list(value)
    else:
        raise TypeError("Invalid {}: {}".format(label, value))

def _to_number(value, default, label, default_values = [None]):
    if value in default_values:
        return default
    elif isinstance(value, Number):
        return value
    else:
        raise TypeError("Invalid {}: {} ({})".format(label, repr(value), type(value)))


###############
## Rotations ##
###############

class RotateAxisAngle(Transform):
    def __init__(self, axis, angle = None):
        axis = _to_vector(axis, "axis", 3)
        if axis.length == 0:
            raise ValueError("axis may not be zero-length")

        self._axis  = axis
        self._angle = _to_number(angle, self._axis.length, "angle")

    def __eq__(self, other):
        if isinstance(other, RotateAxisAngle):
            return self._axis == other._axis and self._angle == other._angle
        else:
            return False

    def __str__(self):
        return "Rotate by {} degrees around {}".format(self._angle, self._axis)

    def to_scad(self, target):
        children = [target] if target is not None else []
        return ScadObject("rotate", None, [("a", self._angle), ("v", list(self._axis))], children)


class RotateXyz(Transform):
    def __init__(self, x, y, z):
        x = _to_number(x, None, "x", [])
        y = _to_number(y, None, "y", [])
        z = _to_number(z, None, "z", [])
        self._xyz = [x, y, z]

    def __eq__(self, other):
        if isinstance(other, RotateXyz):
            return self._xyz == other._xyz
        else:
            return False

    def __str__(self):
        return "Rotate by {} degrees around x, y, and z".format(self._xyz)

    def to_scad(self, target):
        children = [target] if target is not None else []
        return ScadObject("rotate", [list(self._xyz)], None, children)


class RotateYpr(Transform):
    def __init__(self, yaw, pitch, roll):
        yaw   = _to_number(yaw  , None, "yaw  ", [])
        pitch = _to_number(pitch, None, "pitch", [])
        roll  = _to_number(roll , None, "roll ", [])
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


###########
## Scale ##
###########

class Scale(Transform):
    def __init__(self, xyz):
        self._xyz = _to_list_of_numbers(xyz, "xyz", 3)

    def __eq__(self, other):
        return isinstance(other, Scale) and other._xyz == self._xyz

    def __str__(self):
        return "Scale by {}".format(self._xyz)

    def to_scad(self, target):
        children = [target] if target is not None else []
        return ScadObject("scale", [self._xyz], None, children)


###############
## Translate ##
###############

class Translate(Transform):
    def __init__(self, vector):
        self._vector = _to_vector(vector, "vector", 3)

    def __eq__(self, other):
        return isinstance(other, Translate) and other._vector == self._vector

    def __str__(self):
        return "Translate by {}".format(self._vector)

    def to_scad(self, target):
        children = [target] if target is not None else []
        return ScadObject("translate", [list(self._vector)], None, children)
