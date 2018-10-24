from tests.unit_test import TestCase
from cadlib.object.primitives import Slice
from cadlib.util.vector import Vector
from cadlib.util.vector import X, Y, Z
from cadlib.scad import ScadObject
from cadlib import infinity

class TestSlice(TestCase):
    def test_construction(self):
        # Single size
        with self.assertNothingRaised(): Slice(Vector(1, 2, 3), 4, 5)
        with self.assertNothingRaised(): Slice(      [1, 2, 3], 4, 5)

        # Invalid
        with self.assertRaises(ValueError): Slice(Vector(0, 0, 0), 4, 5) # Zero normal
        with self.assertRaises(TypeError) : Slice(Vector(1, 2, 3))       # Offsets missing
        with self.assertRaises(TypeError) : Slice(Vector(1, 2, 3), 4)    # Offset missing
        with self.assertRaises(TypeError) : Slice(1, 4, 5)               # Wrong type

    def test_equality(self):
        # Same object
        self.assertEqualToItself(Slice(X, 4, 5))

        # Equal objects
        self.assertEqual (Slice(X, 4, 5), Slice(X, 4, 5))

        # Different objects
        self.assertNotEqual (Slice(X, 4, 5), Slice(Y, 4, 5)) # Different normal
        self.assertNotEqual (Slice(X, 4, 5), Slice(X, 5, 4)) # Different offsets (even though equivalent)

        # Equal objects from different specifications
        self.assertEqual(Slice(X, 4, 5), Slice([1, 0, 0], 4, 5))  # Different normal

    def test_to_scad(self):
        self.ignore_scad_comments = True

        # General case, with the normal vector in the Y/Z plane
        self.assertEqual(Slice([0, 1, 1], 2, 2.5).to_scad(),
            ScadObject("rotate", None, [('a', 45.0), ('v', [-1.0, 0.0, 0.0])], [
                ScadObject("translate", [[0, 0, 2]], None, [
                    ScadObject("translate", [[-infinity/2, -infinity/2, 0]], None, [
                        ScadObject("cube", [[infinity, infinity, 0.5]], None, None)
                    ])
                ])
            ]))

    def test_repr(self):
        self.assertRepr(Slice(X, 2, 3), "Slice(Vector(1, 0, 0), 2, 3)")
