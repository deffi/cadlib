from cadlib.util.tree import Node
from cadlib.transform import Transform, shortcuts, generators

# Note that, while Union is a subclass of Object, the special case of adding an
# Object and a Union (in either order) or adding two Unions is handled
# differently from adding two generic Objects: rather than nested Unions, a
# merged Union is created (this ensures the associativity of the addition
# operator).
# This special case is handled in the __add__ and __radd__ methods of the Union
# class. Thus, for an expression of the form `Object + Union`, Union.__radd__
# must be called instead of Object.__add__.
# The Python documentation states that
#     "If the right operand’s type is a [direct or indirect] subclass of the
#     left operand’s type and that subclass provides the reflected method for
#     the operation, this method will be called before the left operand’s non-
#     reflected method." [1]
# In this particular case, this means that Union.__radd__ is called before
# Object.__add__.
# However, this does not apply if a subclass of Object (such as Cube) is used
# instead: for an expression of the form `Cube + Union`, Object.__add__ will be
# called first (Cube does not override __add__) because Union is not a subclass
# of Cube. This is a violation of the Liskov substitution principle (by Python)
# and may be a flaw in the language design.
# As a workaround, Object.__add__ checks whether the "other" object is a Union
# and returns NotImplemented in this case, in order to defer to Union.__radd__.
#
# The same issue applies to Intersection (with the __mul__ and __rmul__) methods
# and Difference (with the __sub__ and __rsub__) methods.
#
# [1] https://docs.python.org/3/reference/datamodel.html

class Object:
    # Implementations must always return a valid ScadObject (except when they
    # raise an exception), so that .comment can be called on the result
    # unconditionally.
    def to_scad(self):
        raise NotImplementedError("In {}".format(type(self)))

    def to_tree(self):
        return Node(self, [])


    ################
    ## Arithmetic ##
    ################

    def __add__(self, other):
        from cadlib.csg import Union
        if isinstance(other, Union):
            # Object + Union - defer to Union.__radd__ (see note above)
            return NotImplemented
        elif isinstance(other, Object):
            # Object + Object - create Union
            return Union([self, other])
        else:
            # Object + other - unknown
            return NotImplemented

    def __sub__(self, other):
        """
        Handles:
            Object(1) - Object(2) => Difference(1, 2)
        Needs special case:
            Object(1) - Difference(2, 3) => Difference(1, Difference(2, 3)) # No special case
            Difference(1, 2) - Object(3) => Difference(1, 2, 3)
        But currently:
            Object(1) - Difference(2, 3) => Difference(1, Difference(2, 3))
            Difference(1, 2) - Object(3) => Difference(Difference(1, 2), 3)
        """
        from cadlib.csg import Difference

        if isinstance(other, Object):
            return Difference([self, other])
        else:
            return NotImplemented

        if isinstance(other, Difference):
            # Object - Difference - defer to Difference.__rsub__ (see note above)
            return NotImplemented
        elif isinstance(other, Object):
            # Object - Object - create Difference
            return Difference([self, other])
        else:
            # Object - other - unknown
            return NotImplemented

    def __mul__(self, other):
        from cadlib.csg.intersection import Intersection
        if isinstance(other, Intersection):
            # Object * Intersection - defer to Intersection.__rmul__ (see note above)
            return NotImplemented
        elif isinstance(other, Object):
            # Object * Object - create Intersection
            return Intersection([self, other])
        else:
            # Object * other - unknown
            return NotImplemented

    def __rmul__(self, other):
        from cadlib.object import Transformed
        if isinstance(other, Transform):
            # Transform * Object - create Transformed Object
            return Transformed(other, self)
        else:
            # other * Object - unknown
            return NotImplemented


    #######################
    ## Postfix transform ##
    #######################

    def rotate   (self, *args, **kwargs): return generators.rotate   (*args, **kwargs) * self
    def scale    (self, *args, **kwargs): return generators.scale    (*args, **kwargs) * self
    def translate(self, *args, **kwargs): return generators.translate(*args, **kwargs) * self

    def transform(self, transform):
        if not isinstance(transform, Transform):
            raise TypeError()
        return transform * self


    #########################
    ## Transform shortcuts ##
    #########################

    def up     (self, a): return shortcuts.up     (a) * self
    def down   (self, a): return shortcuts.down   (a) * self
    def left   (self, a): return shortcuts.left   (a) * self
    def right  (self, a): return shortcuts.right  (a) * self
    def forward(self, a): return shortcuts.forward(a) * self
    def back   (self, a): return shortcuts.back   (a) * self

    def yaw_left  (self, a): return shortcuts.yaw_left  (a) * self
    def yaw_right (self, a): return shortcuts.yaw_right (a) * self
    def pitch_up  (self, a): return shortcuts.pitch_up  (a) * self
    def pitch_down(self, a): return shortcuts.pitch_down(a) * self
    def roll_right(self, a): return shortcuts.roll_right(a) * self
    def roll_left (self, a): return shortcuts.roll_left (a) * self
