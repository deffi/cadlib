from cadlib.util.tree import Node
from cadlib.transform import Transform, shortcuts, generators
from cadlib.object import Anchor # TODO remove? TODO from cadlib.object.anchor

# Adding objects: it's not as simple as it seems.
#
# First of all, the basic operation is
#   (1) Object + Object -> Union  (Union is a subclass of Object)
#
# This is easily done in Object.__add__, but adding (in either order) an
# Object and a Union (which is a subclass of Object) would create nested Unions
# and therefore, addition would not be associative:
#     o1 + (o2 + o3) -> o1 + Union(o2, o3) -> Union(o1, Union(o2, o3))
#     (o1 + o2) + o3 -> Union(o1, o2) + o3 -> Union(Union(o1, o2), o3)
#
# Both results describe the same object, but the non-associativity is
# unsatisfactory; besides, adding multiple objects/unions would result in deeply
# and confusingly nested Unions.
#
# What we want instead is:
#     o1 + (o2 + o3) -> o1 + Union(o2, o3) -> Union(o1, o2, o3)
#     (o1 + o2) + o3 -> Union(o1, o2) + o3 -> Union(o1, o2, o3)
# And also:
#     Union(o1, o2) + Union(o3, o4) -> Union(o1, o2, o3, o4)
#
# This means that we have to explicitly handle the following special cases:
#   (2) Union + Union  -> Union
#   (3) Union + Object -> Union
#   (4) Object + Union -> Union
# These special cases extract the individual objects from the Union operands
# instead of simply using the Union as an object.
#
# Now where to implement these operations? Ideally we'd implement them in the
# Union class so the Object class does not need to know how to extract objects
# from a Union. (2) and (3) are naturally implemented in Union.__add__. For (4),
# the Python documentation states that
#     "If the right operand’s type is a [direct or indirect] subclass of the
#     left operand’s type and that subclass provides the reflected method for
#     the operation, this method will be called before the left operand’s non-
#     reflected method. This behavior allows subclasses to override their
#     ancestors’ operations." [1]
# Overriding an ancestor's operation in a subclass is exactly the kind of
# situation we're dealing with here, so we should be able to implement (4) in
# Union.__radd__ and be done, right?
#
# Welll not so fast. We won't be using direct instances of Object - we will be
# using instances of an Object subclass - for example, Cube:
#   (1b) Cube + Cube
#   (2b) Union + Union
#   (3b) Union + Cube
#   (4b) Cube + Union
#
# Since Object subclasses won't be overriding __add__, (1b) will still call
# Object.__add__. (2b) is identical to (2) and (3b) will still call
# Union.__add__. What about (4b)?
#
# The Liskov substitution principle states that objects of one type can be
# replaced with an object of a subtype. Since Cube is a subtype of Object, (4b)
# should still result in a call to Union.__radd__.
#
# Python has a different opinion on this matter: since Union is not a (direct or
# indirect) subclass of Cube, the rule from [1] does not apply and Cube.__add__
# (inherited from Object.__add__) will be called.
#
# (As an aside, this violation of the Liskov substitution principle might be a
# flaw in the design of Python. The condition of the rule from [1] might be
# restated as "If the right operand’s type is a [direct or indirect] subclass of
# _the class that defines the non-reflected method for the operation_").
#
# As a workaround, Object.__add__ checks whether the `other` object is a Union
# and returns NotImplemented in this case, in order to defer to Union.__radd__.
# Note that this requires object.py to import Union, which is unfortunate
# because it creates a circular dependency (of course, union.py has to import
# Object in order to inherit from it).
#
# Alternatively, we could have handled Object + Union in Object.__add__, but
# that would have introduced knowledge about the more specific Union into the
# more general Object. It would also have separated the "prepend to union" case
# from the analogous "append to union" case in Union.__add__, unless we handled
# that case in Object.__add__ as well, which would have introduced... On the
# plus side, we could get rid of Union.__add__ and Union.__radd__ completely
# that way, concentrating all of the arithmetic in a single place. Less pure,
# but maybe more maintainable? Note that even in the purer case, Object has to
# know about Union in order to defer to Union.__radd__ in the appropriate case.
# On the other hand, this means that we would have the check whether self is a
# Union in Object.__add__, which is ridiculous, OO-wise.
#
# The same issue applies to Intersection (with the __mul__ and __rmul__ methods)
# and Difference (with the __sub__ and __rsub__ methods). __mul__ is further
# complicated by the following operations:
#   * Transform * Transform,
#   * Transform * Chained and Chained * Transform
#   * Transform * Object
#   * Transform * Transformed
#
# [1] https://docs.python.org/3/reference/datamodel.html

class Object:
    """A description of an object. Object instances are immutable.

    Implementations must override to_scad and, if they can have children,
    to_tree.

    Objects can be added, multiplied, and subtracted to create unions,
    differences, and intersections, respectively. Objects can be left-multipled
    with transforms to create transformed objects.
    """

    def __init__(self):
        self._anchors = dict()

    def to_scad(self):
        """Converts the object to an OpenSCAD representation.

        Implementations must always return a valid ScadObject (except when they
        raise an exception), so that .comment can be called on the result
        unconditionally."""
        raise NotImplementedError("In {}".format(type(self)))

    def to_tree(self):
        """Creates a tree representation for this object.

        Returns a tree.Node with this object as the data and tree
        representations of the object's children as child nodes.

        Implementations that can have children must override this method to
        create child nodes for the children.
        """
        return Node(self, [])


    ################
    ## Arithmetic ##
    ################

    def __add__(self, other):
        """Adding objects creates a union.

        As a special case, adding an object and a union (in either order) or a
        union and a union will create a flat union with multiple children rather
        than nested unions.
        """

        from cadlib.csg import Union
        if isinstance(other, Union):
            # Object + Union - defer to Union.__radd__ (see note above).
            return NotImplemented
        elif isinstance(other, Object):
            # Object + Object - create Union
            return Union([self, other])
        else:
            # Object + other - unknown
            return NotImplemented

    def __mul__(self, other):
        """Multiplying objects creates an intersection.

        As a special case, multiplying an object and an intersectino (in either
        order) or an intersection and an intersection will create a flat
        intersection with multiple children rather than nested intersection.
        """

        from cadlib.csg.intersection import Intersection
        if isinstance(other, Intersection):
            # Object * Intersection - defer to Intersection.__rmul__ (see note above)
            return NotImplemented
        elif isinstance(other, Object):
            # Object * Object - create Intersection
            return Intersection([self, other])
        else:
            # Object * other - unknown
            # In particular, we cannot do Object * Transform.
            return NotImplemented

    def __sub__(self, other):
        """Subtracting objects creates a difference.

        As a special case, subtracting an object from a difference will create
        a difference with a union as the subtrahend, rather than nested
        differences. Note that this does not apply to subtracting a difference
        from an object or from another difference.
        """
        from cadlib.csg import Difference

        if isinstance(other, Object):
            # Object - Object - create Difference
            return Difference([self, other])
        else:
            # Object - other - unknown
            return NotImplemented


    #######################
    ## Postfix transform ##
    #######################

    def rotate(self, *args, **kwargs):
        """Create a rotated copy of the object.

        See generators.rotate for possible parameters.
        """
        return generators.rotate(*args, **kwargs) * self

    def scale(self, *args, **kwargs):
        """Create a scaled copy of the object.

        See generators.rotate for possible parameters.
        """
        return generators.scale(*args, **kwargs) * self

    def translate(self, *args, **kwargs):
        """Create a translated copy of the object.

        See generators.rotate for possible parameters.
        """
        return generators.translate(*args, **kwargs) * self

    def transform(self, transform):
        """Create a transformed copy of the object.

        This is the same as transform * self.

        transform must be a Transform.
        """
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


    #############
    ## Anchors ##
    #############

    def add_anchor(self, name, position):
        anchor = Anchor(self, name, position)
        self._anchors[name] = anchor
        setattr(self, name, anchor)

    @property
    def anchors(self):
        return self._anchors
