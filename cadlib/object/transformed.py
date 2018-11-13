from cadlib.object import Object
from cadlib.transform import Transform
from cadlib.util.tree import Node


class Transformed(Object):
    def __init__(self, transform, object):
        # Parameter check
        if not isinstance(transform, Transform):
            raise TypeError("transform must be a Transform")
        if not isinstance(object, Object):
            raise TypeError("object must be an Object")

        self._transform = transform
        self._object    = object

    def __eq__(self, other):
        return (isinstance(other, Transformed)
            and other._transform == self._transform
            and other._object    == self._object)

    def __str__(self):
        return "Transformed object"

    def __repr__(self):
        return f"Transformed({self._transform!r}, {self._object!r})"

    def __rmul__(self, other):
        if isinstance(other, Transform):
            # Transform * Transformed (deferred from Transform.__mul__) - insert Transform into own transform
            # This basically turns
            #     transform2 * (transform1 * object)
            # into
            #     (transform2 * transform1) * object
            # See transform.py for details.
            return Transformed(other * self._transform, self._object)
        else:
            # Other * Transformed - unknown (no __rmul__ in superclass)
            return NotImplemented

    def to_tree(self):
        return Node(self, [self._transform.to_tree(), self._object.to_tree()])

    def to_scad(self):
       return self._transform.to_scad(self._object.to_scad())
