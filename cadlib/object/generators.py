from cadlib.object.primitives import Cube, Cylinder, Plane, Slice, Sphere

__all__ = ['cube', 'cylinder', 'plane', 'slice', 'sphere']


def cube(size):
    return Cube(size)


def cylinder(direction_or_base, length_or_cap, r = None, d = None):
    return Cylinder(direction_or_base, length_or_cap, r, d)


def plane(normal, offset):
    return Plane(normal, offset)


def slice(normal, offset1, offset2):
    return Slice(normal, offset1, offset2)


def sphere(r = None, d = None):
    return Sphere(r, d)
