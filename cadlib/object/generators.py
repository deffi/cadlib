from numbers import Number

from cadlib.object.primitives import Cuboid, Frustum, Plane, Layer, Sphere
from cadlib.util import both, neither
from cadlib.util import number
from cadlib.util import Vector

__all__ = ['cone', 'cuboid', 'cube', 'cylinder', 'frustum', 'plane', 'layer', 'sphere']


def _get_radius(r, d):
    if both(r, d):
        raise ValueError("radius and diameter cannot be specified together")
    elif r is not None:
        return number.to_number(r, "radius")
    elif d is not None:
        return number.to_number(d, "diameter") / 2
    else:
        raise ValueError("radius or diameter must be specified")

def _get_radii(r, d):
    if both(r, d):
        raise ValueError("radii and diameters cannot be specified together")
    elif r is not None:
        if not isinstance(r, (tuple, list)):
            raise TypeError("r must be a tuple or a list")
        elif len(r) != 2:
            raise ValueError("r must have two values")
        else:
            return tuple(r)
    elif d is not None:
        if not isinstance(d, (tuple, list)):
            raise TypeError("d must be a tuple or a list")
        elif len(d) != 2:
            raise ValueError("d must have two values")
        else:
            return tuple(x/2 for x in d)
    else:
        raise ValueError("radii or diameters must be specified")


def cuboid(size_or_x, y = None, z = None):
    # Signatures (convenience forms only):
    #   * cuboid([1, 2, 3])
    #   * cuboid(1, 2, 3)

    if both(y, z):
        return Cuboid([size_or_x, y, z])
    elif neither(y, z):
        return Cuboid(size_or_x)
    else:
        raise ValueError("y and z can only be specified together")


def cube(size):
    # Signatures (convenience forms only):
    #   * cube(size)
    size = number.to_number(size, "size")
    return Cuboid([size, size, size])


def cylinder(direction_or_base, length_or_cap, r = None, d = None):
    # Signatures (convenience forms only):
    #   * cylinder (direction, length, radius)
    #   * cylinder (direction, length, d = diameter)
    #   * cylinder (base, cap, radius)
    #   * cylinder (base, cap, d = diameter)

    # Radius or diameter
    radius = _get_radius(r, d)

    # length_or_base must be a vector or a number
    if number.valid(length_or_cap):
        # Number - direction/length
        return Frustum.direction_length(direction_or_base, length_or_cap, radius, radius)

    elif Vector.valid_type(length_or_cap):
        # Vector type - base/cap
        return Frustum(direction_or_base, length_or_cap, radius, radius)

    else:
        raise TypeError("Invalid call signature: length_or_cap must be a vector type or a number")


def cone(direction_or_base, length_or_cap, r = None, d = None):
    # Signatures (convenience forms only):
    #   * cone (direction, length, radius)
    #   * cone (direction, length, d = diameter)
    #   * cone (base, cap, radius)
    #   * cone (base, cap, d = diameter)

    # Radius or diameter
    radius = _get_radius(r, d)

    # length_or_base must be a vector or a number
    if number.valid(length_or_cap):
        # Number - direction/length
        return Frustum.direction_length(direction_or_base, length_or_cap, radius, 0)

    elif Vector.valid_type(length_or_cap):
        # Vector type - base/cap
        return Frustum(direction_or_base, length_or_cap, radius, 0)

    else:
        raise ValueError("Invalid call signature: length_or_cap must be a vector type or a number")

def frustum(direction_or_base, length_or_cap, r = None, d = None):
    # Signatures (convenience forms only):
    #   * frustum (direction, length, radius)
    #   * frustum (direction, length, d = diameter)
    #   * frustum (base, cap, radius)
    #   * frustum (base, cap, d = diameter)

    # Radius or diameter
    radii = _get_radii(r, d)

    # length_or_base must be a vector or a number
    if number.valid(length_or_cap):
        # Number - direction/length
        return Frustum.direction_length(direction_or_base, length_or_cap, *radii)

    elif Vector.valid_type(length_or_cap):
        # Vector type - base/cap
        return Frustum(direction_or_base, length_or_cap, *radii)

    else:
        raise ValueError("Invalid call signature: length_or_cap must be a vector type or a number")


def plane(normal, offset):
    return Plane(normal, offset)


def layer(normal, offset1, offset2):
    return Layer(normal, offset1, offset2)


def sphere(r = None, d = None):
    r = _get_radius(r, d)
    return Sphere(r)
