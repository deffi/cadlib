import math

from .matrix import Matrix
from .vector import Vector, X, Y, Z, origin

degree = math.pi / 180

def both(a, b):
    """Returns True if both a and b are non-None, or False otherwise"""
    return a is not None and b is not None

def neither(a, b):
    """Returns True if both a and b are None, or False otherwise"""
    return a is None and b is None