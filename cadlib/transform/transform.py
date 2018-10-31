from cadlib.util.tree import Node

# Multiplying transforms:
#
# A Transform can be multiplied with another Transform or with an Object:
#   (1) Transform * Transform -> Chained   (Chained is a subclass of Transform)
#   (2) Transform * Object -> Transformed  (Transformed is a subclass of Object)
#
# Similar to Object + Union (see object.py), this is not sufficient to make
# multiplication associative:
#     t1 * (t2 * t3) -> t1 * Chained(t2, t3) -> Chained(t1, Chained(t2, t3))
#     (t1 * t2) * t3 -> Chained(t1, t2) * t3 -> Chained(Chained(t1, t2), t3)
# The same is true for multiplication with an Object:
#     (t1 * t2) * o -> Chained(t1, t2) * o     -> Transformed(Chained(t1, t2), o))
#     t1 * (t2 * o) -> t1 * Transformed(t2, o) -> Transformed(t1, Transformed(t2, o))
#
# In both cases, both results describe the same object, but as with Unions, the
# non-associativity is unsatisfactory.
#
# What we want instead is:
#     t1 * (t2 * t3) -> t1 * Chained(t2, t3) -> Chained(t1, t2, t3)
#     (t1 * t2) * t3 -> Chained(t1, t2) * t3 -> Chained(t1, t2, t3)
# And:
#     (t1 * t2) * o -> Chained(t1, t2) * o     -> Transformed(Chained(t1, t2), o))
#     t1 * (t2 * o) -> t1 * Transformed(t2, o) -> Transformed(Chained(t1, t2), o))
#
# This means that we have to explicitly handle the following special cases:
#   (3) Chained * Chained       -> Chained
#   (4) Chained * Transform     -> Chained
#   (5) Transform * Chained     -> Chained
#   (6) Transform * Transformed -> Transformed
#
# The solution is basically the same as described in object.py.

class Transform:
    def __mul__(self, other):
        from cadlib.transform.chained import Chained
        from cadlib.object import Object, Transformed

        if isinstance(other, Chained):
            # Transform * Chained - defer to Chained.__rmul__
            return NotImplemented
        elif isinstance(other, Transform):
            # Transform * Transform - create Chained
            return Chained([self, other])
        elif isinstance(other, Transformed):
            # Transform * Transformed - defer to Transformed.__rmul__
            return NotImplemented
        elif isinstance(other, Object):
            # Transform * Object - create Transformed
            return Transformed(self, other)
        else:
            # Transform * other - unknown
            return NotImplemented

    def to_tree(self):
        return Node(self, [])

    def inverse(self):
        raise NotImplementedError("inverse not implemented in {}".format(type(self)))

    def to_scad(self, target):
        raise NotImplementedError("to_scad not implemented in {}".format(type(self)))

    def to_matrix(self):
        raise NotImplementedError("to_matrix not implemented in {}".format(type(self)))
