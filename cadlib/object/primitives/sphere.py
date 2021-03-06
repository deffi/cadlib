from warnings import warn

from cadlib.object import Object, Anchor  # TODO remove anchor?
from cadlib.scad import ScadObject
from cadlib.util import number


class Sphere(Object):
    def __init__(self, r):
        super().__init__()

        self._radius = number.convert(r, "radius")

        if self._radius == 0: warn("radius is 0")

        self.add_anchor("center", [0, 0, 0])
        #self.center = Anchor(self, [0, 0, 0])

    def __eq__(self, other):
        return (isinstance(other, Sphere)
            and other._radius == self._radius)

    def __repr__(self):
        return f"Sphere(r={self._radius!r})"

    def __str__(self):
        return f"Sphere with radius {self._radius}"

    def to_scad(self):
        return ScadObject("sphere", [self._radius], None, None)
