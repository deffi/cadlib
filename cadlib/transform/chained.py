from cadlib.transform.transform import Transform
from cadlib.util.tree import Node


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