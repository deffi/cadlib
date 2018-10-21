from numbers import Number
from warnings import warn

from cadlib.transform.primitives import RotateAxisAngle, RotateXyz, RotateYpr, RotateFromTo, \
    ScaleXyz, ScaleUniform, ScaleAxisFactor, Translate
from cadlib.util import Vector
from cadlib.util import both

__all__ = ['rotate', 'scale', 'translate']

def rotate(axis_or_frm = None, angle_or_to = None, axis = None, angle = None, frm = None, to = None, xyz = None, ypr = None, ignore_ambiguity = False):
    # Signatures (canonical forms):
    #   * rotate(axis = x, angle = 45)
    #   * rotate(frm = x, to = y)
    #   * rotate(xyz = [45, 0, 30])
    #   * rotate(ypr = [45, -30, 10])
    # Signatures (convenience forms):
    #   * rotate(x, 45)
    #   * rotate(x, angle = 45)
    #   * rotate(x, y)
    #   * rotate(x, to = y)
    #
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
    if both(axis_or_frm, axis ): raise ValueError("axis"  " cannot be specified together with axis_or_frm")
    if both(axis_or_frm, frm  ): raise ValueError("frm"   " cannot be specified together with axis_or_frm")
    if both(angle_or_to, angle): raise ValueError("angle" " cannot be specified together with angle_or_to")
    if both(angle_or_to, to   ): raise ValueError("to"    " cannot be specified together with angle_or_to")

    # Transform the convenience forms to canonical form
    if axis_or_frm is not None:
        if not isinstance(axis_or_frm, (Vector, list, tuple)):
            raise TypeError("axis must be a vector type")

        if angle_or_to is not None:
            if isinstance(angle_or_to, Number):
                # Axis/angle (implicit)
                axis = axis_or_frm
                angle = angle_or_to
            elif isinstance(angle_or_to, (Vector, list, tuple)):
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
    if axis  is not None and angle is None: raise ValueError("angle" " is required when " "axis"  " is given")
    if angle is not None and axis  is None: raise ValueError("axis"  " is required when " "angle" " is given")
    if frm   is not None and to    is None: raise ValueError("to"    " is required when " "frm"   " is given")
    if to    is not None and frm   is None: raise ValueError("frm"   " is required when " "to"    " is given")

    # Handle the different cases
    if axis is not None:
        # Check that no other specification is given
        if frm is not None: raise ValueError("frm" " cannot be specified together with axis")
        if xyz is not None: raise ValueError("xyz" " cannot be specified together with axis")
        if ypr is not None: raise ValueError("ypr" " cannot be specified together with axis")

        return RotateAxisAngle(axis, angle)

    elif frm is not None:
        # Check that no other specification is given
        if axis is not None: raise ValueError("axis" " cannot be specified together with frm")
        if xyz  is not None: raise ValueError("xyz"  " cannot be specified together with frm")
        if ypr  is not None: raise ValueError("ypr"  " cannot be specified together with frm")

        return RotateFromTo(frm, to, ignore_ambiguity)

    elif xyz is not None:
        # Check that no other specification is given
        if axis is not None: raise ValueError("axis" " cannot be specified together with frm")
        if frm  is not None: raise ValueError("frm"  " cannot be specified together with axis")
        if ypr  is not None: raise ValueError("ypr"  " cannot be specified together with axis")

        return RotateXyz(*xyz)

    elif ypr is not None:
        # Check that no other specification is given
        if axis is not None: raise ValueError("axis" " cannot be specified together with frm")
        if frm  is not None: raise ValueError("frm"  " cannot be specified together with axis")
        if xyz  is not None: raise ValueError("xyz"  " cannot be specified together with axis")

        return RotateYpr(*ypr)

    else:
        raise ValueError("Invalid call signature")

def scale(xyz_or_axis_or_factor = None, factor = None, xyz = None, axis = None):
    # Signatures (canonical forms):
    #   * scale(xyz = [2, 1, 1])
    #   * scale(factor = 2)
    #   * scale(axis = X, factor = 2)
    # Signatures (convenience forms):
    #   * scale([2, 1, 1])
    #   * scale(2)
    #   * scale(X, 2)
    #
    # Canonical forms:
    #     xyz_or_axis_or_factor  factor   xyz  axis
    #                         -       -  list     -  # XYZ
    #                         -     num     -   vec  # Axis/factor
    #                         -     num     -     -  # Uniform
    # Convenience forms (-: must be None, *: overwritten)
    #                       vec     num     -     *  # Axis/factor (implicit or explicit)
    #                      list       -     *     -  # XYZ
    #                       num       *     -     -  # Isotropic XYZ
    #
    # "Vector type" is Vector, list, or tuple
    #
    # Make sure that there are no conflicts between convenience parameters and canonical parameters
    if both(xyz_or_axis_or_factor, xyz ): raise ValueError("xyz"   " cannot be specified together with xyz_or_axis")
    if both(xyz_or_axis_or_factor, axis): raise ValueError("axis"  " cannot be specified together with xyz_or_axis")

    # Transform the convenience forms to canonical form
    if xyz_or_axis_or_factor is not None:
        if not isinstance(xyz_or_axis_or_factor, (Vector, list, tuple, Number)):
            raise TypeError("xyz_or_axis_or_factor must be a vector type or a number")

        if factor is not None:
            axis = xyz_or_axis_or_factor
        elif isinstance(xyz_or_axis_or_factor, Number):
            factor = xyz_or_axis_or_factor
        else:
            xyz = xyz_or_axis_or_factor

    # Check the parameters that must appear in pairs
    if axis is not None and factor is None: raise ValueError("factor" " is required when " "axis" " is given")

    # Handle the different cases
    if axis is not None:
        # Check that no other specification is given
        if xyz is not None: raise ValueError("xyz" " cannot be specified together with axis")

        return ScaleAxisFactor(axis, factor)

    elif xyz is not None:
        # Check that no other specification is given
        if axis   is not None: raise ValueError("axis"   " cannot be specified together with xyz")
        if factor is not None: raise ValueError("factor" " cannot be specified together with xyz")

        return ScaleXyz(*xyz)

    elif factor is not None:
        return ScaleUniform(factor)

    else:
        raise ValueError("Invalid call signature")



def translate(vector):
    return Translate(vector)
