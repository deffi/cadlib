from cadlib.csg import Csg
from cadlib.object import Object
from cadlib.scad import ScadObject


class Difference(Csg):
    def __eq__(self, other):
        return isinstance(other, Difference) and other._children == self._children

    def __str__(self):
        return "Difference"

    def __sub__(self, other):
        if isinstance(other, Difference):
            # Difference - Difference - create nested Difference
            return Difference([self, other])
        elif isinstance(other, Object):
            # Difference - Object - append to difference
            return Difference(self._children + [other])
        else:
            # Difference - other - defer to superclass
            return super().__sub__(other)

    def to_scad(self):
        children = [child.to_scad() for child in self._children]
        return ScadObject("difference", None, None, children)
