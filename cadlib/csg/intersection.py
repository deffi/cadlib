from cadlib.csg import Csg
from cadlib.object import Object
from cadlib.scad import ScadObject


class Intersection(Csg):
    def __eq__(self, other):
        return isinstance(other, Intersection) and other._children == self._children

    def __str__(self):
        return "Intersection"

    def __mul__(self, other):
        if isinstance(other, Intersection):
            # Intersection * Intersection - merge intersections
            return Intersection(self._children + other._children)
        elif isinstance(other, Object):
            # Intersectino * Object - append to intersection
            return Intersection(self._children + [other])
        else:
            # Intersection * other - defer to superclass
            return super().__mul__(other)

    def __rmul__(self, other):
        if isinstance(other, Intersection):
            # Intersection * Intersection - merge intersections
            return Intersection(other._children + self._children)
        elif isinstance(other, Object):
            # Object * Intersection - prepend to intersection
            return Intersection([other] + self._children)
        else:
            # Other * Intersection - defer to superclass
            return super().__rmul__(other)

    def to_scad(self):
        children = [child.to_scad() for child in self._children]
        return ScadObject("intersection", None, None, children)
