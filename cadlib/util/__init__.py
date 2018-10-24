import math

from .matrix import Matrix
from .vector import Vector, X, Y, Z

degree = math.pi / 180

def both(a, b):
    return a is not None and b is not None

def neither(a, b):
    return a is None and b is None