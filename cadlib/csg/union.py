from cadlib.csg import Csg
from cadlib.object import Object
from cadlib.scad import ScadObject


class Union(Csg):
    def __eq__(self, other):
        return (isinstance(other, Union)
            and other._children == self._children)

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
        # other cannot be a Union: Union + Union calls Union.__add__.
        if isinstance(other, Object):
            # Object + Union (deferred from Object.__add__) - prepend to union
            return Union([other] + self._children)
        else:
            # Other + Union - unknown (no __radd__ in superclass)
            return NotImplemented
            # return super().__radd__(other)

    def to_scad(self):
        children = [child.to_scad() for child in self._children]
        return ScadObject("union", None, None, children)
