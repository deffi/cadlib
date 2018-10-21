import math

from .matrix import Matrix
from .vector import Vector, X, Y, Z

degree = math.pi / 180

def both(a, b):
    return a is not None and b is not None
