from cadlib.util.tree import Node
from cadlib.object.object import Object
from cadlib.scad.scad import ScadObject

class Csg(Object):
    def __init__(self, children):
        # Check parameters
        for child in children:
            if not isinstance(child, Object):
                raise TypeError("Children of Csg must be objects, {} found.".format(type(child)))

        self._children = children

    def to_tree(self):
        return Node(self, [child.to_tree() for child in self._children])

class Union(Csg):
    def __eq__(self, other):
        return isinstance(other, Union) and other._children == self._children

    def __str__(self):
        return "Union"

    def __add__(self, other):
        if isinstance(other, Union):
            # Union + Union - merge unions
            return Union(self._children + other._children)
        elif isinstance(other, Object):
            # Union + Object - append to union
            return Union(self._children + [other])
        else:
            # Union + other - defer to superclass
            return super().__add__(other)

    def __radd__(self, other):
        if isinstance(other, Union):
            # Union + Union - merge unions
            return Union(other._children + self._children)
        elif isinstance(other, Object):
            # Object + Union - prepend to union
            return Union([other] + self._children)
        else:
            # Other + Union - defer to superclass
            return super().__radd__(other)

    def to_scad(self):
        children = [child.to_scad() for child in self._children]
        return ScadObject("union", None, None, children)

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
            # Difference -Object - append to difference
            return Difference(self._children + [other])
        else:
            # Difference - other - defer to superclass
            return super().__sub__(other)

    def __rsub__(self, other):
        if isinstance(other, Difference):
            # Difference - Difference - create nested Difference
            return Difference([other, self])
        elif isinstance(other, Object):
            # Object - Difference - create nested Difference
            return Difference([other, self])
        else:
            # Other - Difference - defer to superclass
            return super().__rsub__(other)

    def to_scad(self):
        children = [child.to_scad() for child in self._children]
        return ScadObject("difference", None, None, children)


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
