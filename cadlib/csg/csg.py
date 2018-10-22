from cadlib.util.tree import Node
from cadlib.object import Object


class Csg(Object):
    def __init__(self, children):
        children = list(children)

        # Check parameters
        for child in children:
            if not isinstance(child, Object):
                raise TypeError("Children of Csg must be objects, {} found.".format(type(child)))

        self._children = children

    @classmethod
    def empty(cls):
        return cls([])

    @property
    def children(self):
        return self._children

    def to_tree(self):
        return Node(self, [child.to_tree() for child in self._children])
