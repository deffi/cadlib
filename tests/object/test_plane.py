from tests.unit_test import TestCase
from cadlib.object.primitives import Plane
from cadlib.util.vector import Vector
from cadlib.util.vector import X, Y, Z
from cadlib.scad import ScadObject
from cadlib import infinity

class TestPlane(TestCase):
    def test_construction(self):
        # Single size
        with self.assertNothingRaised(): Plane(Vector(1, 2, 3), 0)
        with self.assertNothingRaised(): Plane(      [1, 2, 3], 0)

        # Invalid
        with self.assertRaises(ValueError): Plane(Vector(0, 0, 0), 0)  # Zero normal
        with self.assertRaises(TypeError): Plane(Vector(1, 2, 3), "0")  # Wrong offset type
        with self.assertRaises(TypeError): Plane(Vector(1, 2, 3))  # Offset missing
        with self.assertRaises(TypeError): Plane(1, 0)  # Wrong type

    def test_equality(self):
        # Same object
        self.assertEqualToItself(Plane(X, 0))

        # Equal objects
        self.assertEqual (Plane(X, 0), Plane(X, 0))

        # Different objects
        self.assertNotEqual (Plane(X, 0), Plane(Y, 0)) # Different normal
        self.assertNotEqual (Plane(X, 0), Plane(X, 1)) # Different offset

        # Equal objects from different specifications
        self.assertEqual(Plane(X, 0), Plane([1, 0, 0], 0))  # Different normal

    def test_to_scad(self):
        self.ignore_scad_comments = True

        # General case, with the normal vector in the Y/Z plane
        self.assertEqual(Plane([0, 1, 1], 2).to_scad(),
            ScadObject("rotate", None, [('a', 45.0), ('v', [-1.0, 0.0, 0.0])], [
                ScadObject("translate", [[0, 0, 2]], None, [
                    ScadObject("translate", [[-infinity/2, -infinity/2, -infinity]], None, [
                        ScadObject("cube", [[infinity, infinity, infinity]], None, None)
                    ])
                ])
            ]))

    def test_repr(self):
        self.assertRepr(Plane(X, 2), "Plane(Vector(1, 0, 0), 2)")
