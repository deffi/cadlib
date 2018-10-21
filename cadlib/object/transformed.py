from cadlib.object.object import Object
from cadlib.transform.transform import Transform
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
        return isinstance(other, Transformed) and \
            other._transform == self._transform and \
            other._object    == self._object

    def __str__(self):
        return "Transformed object"

    def __repr__(self):
        return f"Transformed({self._transform!r}, {self._object!r})"

    def __rmul__(self, other):
        if isinstance(other, Transform):
            # Transformation of an already-transformed object. Instead of transforming the object twice, we merge the
            # individual transform. While this is not strictly required, we want the following two terms to be equal:
            #   (a) (transform2 * transform1) * object
            #   (b) transform2 * (transform1 * object)
            # Basically, we're turning case (b) into case (a).
            return Transformed(other * self._transform, self._object)
        else:
            # Defer to the base class
            return super().__rmul__(other)

    def to_tree(self):
        return Node(self, [self._transform.to_tree(), self._object.to_tree()])

    def to_scad(self):
       return self._transform.to_scad(self._object.to_scad())
