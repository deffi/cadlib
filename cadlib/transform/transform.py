from cadlib.util.tree import Node


class Transform:
    def __mul__(self, other):
        """
        Handles:
            Transform(1) * Transform(2) => Chained(1, 2)
        Special case:
            Transform(1) * Chained(2, 3) => Chained(1, 2, 3)
            Chained(1, 2) * Transform(3) => Chained(1, 2, 3)
        Does not handle:
            Transform * Object # Defer to Object.__rmul__
            TODO update
        """
        from cadlib.transform.chained import Chained
        from cadlib.object import Object, Transformed

        if isinstance(other, Transform):
            # Transform * Transform - chain into single multi-element transform
            # TODO get rid of _transform_list and handle this like Object.__add__
            return Chained(self._transform_list() + other._transform_list())
            # Transform * Transform - create nested transform
            # return Chained([self, other])
        elif isinstance(other, Transformed):
            # Defer to Transformed.__rmul__
            return NotImplemented
        elif isinstance(other, Object):
            # Transform * Object - create Transformed Object
            return Transformed(self, other)

        else:
            return NotImplemented

    def to_tree(self):
        return Node(self, [])

    def _transform_list(self):
        return [self]

    def inverse(self):
        raise NotImplementedError("inverse not implemented in {}".format(type(self)))

    def to_scad(self, target):
        raise NotImplementedError("to_scad not implemented in {}".format(type(self)))

    def to_matrix(self):
        raise NotImplementedError("to_matrix not implemented in {}".format(type(self)))
