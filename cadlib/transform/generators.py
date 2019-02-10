from numbers import Number

from cadlib.transform.primitives import RotateAxisAngle, RotateXyz, RotateYpr, RotateFromTo
from cadlib.transform.primitives import ScaleAxes, ScaleUniform, ScaleAxisFactor
from cadlib.transform.primitives import Translate
from cadlib.util import Vector
from cadlib.util import both
from cadlib.util import number

__all__ = ['rotate', 'scale', 'translate']

def rotate(axis_or_frm = None, angle_or_to = None, axis = None, angle = None, frm = None, to = None, xyz = None, ypr = None, ignore_ambiguity = False):
    """Generate a rotation around an axis through the origin.

    Signatures (canonical forms):
      * rotate(axis = x, angle = 45)
      * rotate(frm = x, to = y)
      * rotate(xyz = [45, 0, 30])
      * rotate(ypr = [45, -30, 10])
    Signatures (convenience forms):
      * rotate(x, 45)
      * rotate(x, angle = 45)
      * rotate(x, y)
      * rotate(x, to = y)
    """

    # Canonical forms:
    #     axis_or_axmag_or_frm  angle_or_to  axis  angle  frm   to   xyz   ypr
    #                        -            -   vec    num    -    -     -     -  # Axis/angle
    #                        -            -     -      -  vec  vec     -     -  # From/to
    #                        -            -     -      -    -    -  list     -  # XYZ
    #                        -            -     -      -    -    -     -  list  # Yaw/pitch/roll
    # Convenience forms (-: must be None, *: overwritten)
    #                      vec          num     *      *    -    -     -     -  # Axis/angle (implicit)
    #                      vec            -     *    num    -    -     -     -  # Axis/angle (explicit)
    #                      vec          vec     -      -    *    *     -     -  # From/to (implicit)
    #                      vec            -     -      -    *  vec     -     -  # From/to (explicit)
    #
    # "Vector type" is Vector, list, or tuple

    # Make sure that there are no conflicts between convenience parameters and canonical parameters
    if both(axis_or_frm, axis ): raise TypeError("axis"  " cannot be specified together with axis_or_frm")
    if both(axis_or_frm, frm  ): raise TypeError("frm"   " cannot be specified together with axis_or_frm")
    if both(angle_or_to, angle): raise TypeError("angle" " cannot be specified together with angle_or_to")
    if both(angle_or_to, to   ): raise TypeError("to"    " cannot be specified together with angle_or_to")

    # Transform the convenience forms to canonical form
    if axis_or_frm is not None:
        if not Vector.valid_type(axis_or_frm):
            raise TypeError("axis must be a vector type")

        if angle_or_to is not None:
            if number.valid(angle_or_to):
                # Axis/angle (implicit)
                axis = axis_or_frm
                angle = angle_or_to
            elif Vector.valid_type(angle_or_to):
                # From/to (implicit)
                frm = axis_or_frm
                to = angle_or_to
            else:
                raise TypeError("angle_or_to must be a number or a vector type")
        elif angle is not None:
            # Axis/angle (explicit)
            axis = axis_or_frm
        elif to is not None:
            # From/to (explicit)
            frm = axis_or_frm

    # Check the parameters that must appear in pairs
    if axis  is not None and angle is None: raise TypeError("angle" " is required when " "axis"  " is given")
    if angle is not None and axis  is None: raise TypeError("axis"  " is required when " "angle" " is given")
    if frm   is not None and to    is None: raise TypeError("to"    " is required when " "frm"   " is given")
    if to    is not None and frm   is None: raise TypeError("frm"   " is required when " "to"    " is given")

    # Handle the different cases
    if axis is not None:
        # Check that no other specification is given
        if frm is not None: raise TypeError("frm" " cannot be specified together with axis")
        if xyz is not None: raise TypeError("xyz" " cannot be specified together with axis")
        if ypr is not None: raise TypeError("ypr" " cannot be specified together with axis")

        return RotateAxisAngle(axis, angle)

    elif frm is not None:
        # Check that no other specification is given
        if axis is not None: raise TypeError("axis" " cannot be specified together with frm")
        if xyz  is not None: raise TypeError("xyz"  " cannot be specified together with frm")
        if ypr  is not None: raise TypeError("ypr"  " cannot be specified together with frm")

        return RotateFromTo(frm, to, ignore_ambiguity)

    elif xyz is not None:
        # Check that no other specification is given
        if axis is not None: raise TypeError("axis" " cannot be specified together with frm")
        if frm  is not None: raise TypeError("frm"  " cannot be specified together with axis")
        if ypr  is not None: raise TypeError("ypr"  " cannot be specified together with axis")

        return RotateXyz(*xyz)

    elif ypr is not None:
        # Check that no other specification is given
        if axis is not None: raise TypeError("axis" " cannot be specified together with frm")
        if frm  is not None: raise TypeError("frm"  " cannot be specified together with axis")
        if xyz  is not None: raise TypeError("xyz"  " cannot be specified together with axis")

        return RotateYpr(*ypr)

    else:
        raise TypeError("Invalid call signature")

def scale(xyz_or_axis_or_factor = None, factor = None, xyz = None, axis = None):
    """Generate a scaling transform around the origin.

    Signatures (canonical forms):
      * scale(xyz = [2, 1, 1])
      * scale(factor = 2)
      * scale(axis = X, factor = 2)
    Signatures (convenience forms):
      * scale([2, 1, 1])
      * scale(2)
      * scale(X, 2)

    Vectors can be specified as Vector, list, or tuple. Note that a Vector can
    be used for xyz even though xyz is not strictly a vector.
    """

    # Canonical forms:
    #     xyz_or_axis_or_factor  factor   xyz  axis
    #                         -       -  list     -  # XYZ
    #                         -     num     -   vec  # Axis/factor
    #                         -     num     -     -  # Uniform
    # Convenience forms (-: must be None, *: overwritten)
    #                       vec     num     -     *  # Axis/factor (implicit or explicit)
    #                       vec       -     *     -  # XYZ
    #                       num       *     -     -  # Isotropic XYZ
    #

    # Make sure that there are no conflicts between convenience parameters and canonical parameters
    if both(xyz_or_axis_or_factor, xyz ): raise TypeError("xyz"   " cannot be specified together with xyz_or_axis")
    if both(xyz_or_axis_or_factor, axis): raise TypeError("axis"  " cannot be specified together with xyz_or_axis")

    # Transform the convenience forms to canonical form
    if xyz_or_axis_or_factor is not None:
        if Vector.valid_type(xyz_or_axis_or_factor):
            if factor is None:
                # Xyz
                xyz = xyz_or_axis_or_factor
            else:
                # Axis part of axis/factor
                axis = xyz_or_axis_or_factor
        elif number.valid(xyz_or_axis_or_factor):
            if factor is None:
                # Factor
                factor = xyz_or_axis_or_factor
            else:
                raise TypeError("factor cannot be specified together with numeric xyz_or_axis")
        else:
            raise TypeError("xyz_or_axis_or_factor must be a vector type or a number")

    # Check the parameters that must appear in pairs
    if axis is not None and factor is None: raise TypeError("factor" " is required when " "axis" " is given")

    # Handle the different cases
    if axis is not None:
        # Check that no other specification is given
        if xyz is not None: raise TypeError("xyz" " cannot be specified together with axis")

        return ScaleAxisFactor(axis, factor)

    elif xyz is not None:
        # Check that no other specification is given
        if axis   is not None: raise TypeError("axis"   " cannot be specified together with xyz")
        if factor is not None: raise TypeError("factor" " cannot be specified together with xyz")

        return ScaleAxes(*xyz)

    elif factor is not None:
        return ScaleUniform(factor)

    else:
        raise TypeError("Invalid call signature")



def translate(vector):
    """Generate a translation.

    Signatures (canonical forms):
      * scale(xyz = [2, 1, 1])
    """
    return Translate(vector)
