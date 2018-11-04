from cadlib.object.primitives import Cuboid, Cylinder, Plane, Slice, Sphere
from cadlib.util import both, neither

__all__ = ['cuboid', 'cylinder', 'plane', 'slice', 'sphere']


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


def cylinder(direction_or_base, length_or_cap, r = None, d = None):
    return Cylinder(direction_or_base, length_or_cap, r, d)


def plane(normal, offset):
    return Plane(normal, offset)


def slice(normal, offset1, offset2):
    return Slice(normal, offset1, offset2)


def sphere(r = None, d = None):
    return Sphere(r, d)
