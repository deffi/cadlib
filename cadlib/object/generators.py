from numbers import Number

from cadlib.object.primitives import Cuboid, Frustum, Plane, Layer, Sphere
from cadlib.util import both, neither
from cadlib.util import number
from cadlib.util import Vector

__all__ = ['cone', 'cuboid', 'cube', 'cylinder', 'frustum', 'plane', 'layer', 'sphere']


def _get_radius(r, d):
    """Given either a radius or a diameter, determine the radius.

    Either r or d, but not both, must be given (non-None). Otherwise, an
    exception will be raised. The given value is also converted to a number.
    """
    if both(r, d):
        raise TypeError("radius and diameter cannot be specified together")
    elif r is not None:
        return number.convert(r, "radius")
    elif d is not None:
        return number.convert(d, "diameter") / 2
    else:
        raise TypeError("radius or diameter must be specified")


def _get_radii(r, d):
    """Like _get_radius, but the given value for r or d must either be a tuple
    or a list and must have exactly 2 elements.
    """
    if both(r, d):
        raise TypeError("radii and diameters cannot be specified together")
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
        raise TypeError("radii or diameters must be specified")


def cuboid(size_or_x_or_xyz, y = None, z = None):
    """Generate a cuboid.

    The cuboid will have one corner at the origin, will be aligned with the
    axes, and extend in the positive axis directions.

    Signatures (convenience forms only):
      * cuboid(size)
      * cuboid(x, y, z)
      * cuboid(xyz)

    xzy can be Vector, list, or tuple. Note that for convenience, a Vector can
    be used for xyz even though xyz is not strictly a vector.
    """

    if both(y, z):
        return Cuboid(size_or_x_or_xyz, y, z)
    elif neither(y, z) and number.valid(size_or_x_or_xyz):
        return Cuboid(size_or_x_or_xyz, size_or_x_or_xyz, size_or_x_or_xyz)
    elif neither(y, z) and Vector.valid_type(size_or_x_or_xyz):
        return Cuboid(*size_or_x_or_xyz)
    else:
        raise TypeError("y and z can only be specified together")


def cube(size):
    """Generate a cube.

    The cube will have one corner at the origin, will be aligned with the
    axes, and extend in the positive axis directions.

    Signatures (convenience forms only):
      * cube(size)
    """

    size = number.convert(size, "size")
    return Cuboid(size, size, size)


def cylinder(direction_or_base, length_or_cap, r = None, d = None):
    """Generate a cylinder.

    Signatures (convenience forms only):
      * cylinder(direction, length, radius)
      * cylinder(direction, length, d = diameter)
      * cylinder(base, cap, radius)
      * cylinder(base, cap, d = diameter)
    """

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
    """Generate a cone.

    For the forms with a direction, the base will be at the origin.

    Signatures (convenience forms only):
      * cone(direction, length, radius)
      * cone(direction, length, d = diameter)
      * cone(base, cap, radius)
      * cone(base, cap, d = diameter)
    """
    # TODO should use r = None, *, d = None? (not just here)
    # TODO should be tip instead of cap

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
        raise TypeError("Invalid call signature: length_or_cap must be a vector type or a number")


def frustum(direction_or_base, length_or_cap, r = None, d = None):
    """Generate a frustum.

    For the forms with a direction, the base will be at the origin.

    Signatures (convenience forms only):
      * frustum (direction, length, radii)
      * frustum (direction, length, d = diameters)
      * frustum (base, cap, radii)
      * frustum (base, cap, d = diameters)
    """

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
        raise TypeError("Invalid call signature: length_or_cap must be a vector type or a number")


def plane(normal, offset):
    """Generate a plane or, more precisely, a half-space.

    The normal vector points outside. If offset is 0, the plane will contain the
    origin. Otherwise, the plane will be translated by offset along the normal
    vector.

    The normal vector needs not be normalized.
    """
    return Plane(normal, offset)


def layer(normal, offset1, offset2):
    """Generate a layer, i. e. a region of space between two planes.

    If either offset is 0, the respective plane will contain the origin.
    Otherwise, the plane will be translated by offset along the normal vector.

    The normal vector needs not be normalized.
    """
    return Layer(normal, offset1, offset2)


def sphere(r = None, d = None):
    """Generate a sphere.

    Signatures (canonical forms):
      * sphere(r = radius)
      * sphere(d = diameter)

    Signatures (convenience forms):
      * sphere(radius)

    The sphere will be centered at the origin.
    """
    r = _get_radius(r, d)
    return Sphere(r)
