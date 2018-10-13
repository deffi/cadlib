from cadlib.util.tree import Node


###################
## Basic classes ##
###################

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
        """
        if isinstance(other, Transform):
            # Transform * Transform - chain into single multi-element transform
            return Chained(self._transform_list() + other._transform_list())
            # Transform * Transform - create nested transform
            # return Chained([self, other])
        else:
            return NotImplemented

    def to_tree(self):
        return Node(self, [])

    def _transform_list(self):
        return [self]

    def to_scad(self, target):
        raise NotImplementedError("In {}".format(type(self)))

class Chained(Transform):
    def __init__(self, transforms):
        # Check parameters
        for transform in transforms:
            if not isinstance(transform, Transform):
                raise TypeError("Children of chained transform must be transform.")

        self._transforms = transforms

    def __eq__(self, other):
        return isinstance(other, Chained) and other._transforms == self._transforms

    def __str__(self):
        return "Chained transform ({} transform)".format(len(self._transforms))

    def _transform_list(self):
        return self._transforms

    def to_tree(self):
        return Node(self, [tf.to_tree() for tf in self._transforms])

    def to_scad(self, target):
        result = target
        for transform in self._transforms[::-1]:
            result = transform.to_scad(result)
        return result
