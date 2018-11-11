from numbers import Number

from cadlib.object.primitives import Cuboid, Frustum, Plane, Slice, Sphere
from cadlib.util import both, neither
from cadlib.util.number import to_number
from cadlib.util import Vector

__all__ = ['cuboid', 'cube', 'cylinder', 'plane', 'slice', 'sphere']


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
    size = to_number(size, None, "size", [])
    return Cuboid([size, size, size])

def _get_radius(r, d):
    if both(r, d):
        raise ValueError("radius and diameter cannot be specified together")
    elif r is not None:
        return r
    elif d is not None:
        return d / 2
    else:
        raise ValueError("radius or diameter must be specified")


def cylinder(direction_or_base, length_or_cap, r = None, d = None):
    # Signatures (convenience forms only):
    #   * Cylinder (direction, length, radius)
    #   * Cylinder (direction, length, d = diameter)
    #   * Cylinder (base, cap, radius)
    #   * Cylinder (base, cap, d = diameter)

    # Radius or diameter
    radius = _get_radius(r, d)

    # length_or_base must be a vector or a number
    if isinstance(length_or_cap, Number):
        # Number - direction/length
        return Frustum.direction_length(direction_or_base, length_or_cap, radius, radius)

    elif isinstance(length_or_cap, (Vector, list, tuple)):
        # Vector type - base/cap
        return Frustum(direction_or_base, length_or_cap, radius, radius)

    else:
        raise ValueError("Invalid call signature: length_or_cap must be a vector type or a number")


def plane(normal, offset):
    return Plane(normal, offset)


def slice(normal, offset1, offset2):
    return Slice(normal, offset1, offset2)


def sphere(r = None, d = None):
    # TODO Sphere construction like Frustum
    return Sphere(r, d)
