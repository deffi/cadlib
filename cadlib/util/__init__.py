import math

from .matrix import Matrix
from .vector import Vector

degree = math.pi / 180

X = Vector(1, 0, 0)
Y = Vector(0, 1, 0)
Z = Vector(0, 0, 1)


def both(a, b):
    return a is not None and b is not None
