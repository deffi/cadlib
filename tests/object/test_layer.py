from tests.unit_test import TestCase
from cadlib.object.primitives import Layer
from cadlib.util.vector import Vector
from cadlib.util.vector import X, Y, Z
from cadlib.scad import ScadObject
from cadlib import infinity

class TestLayer(TestCase):
    def test_construction(self):
        # Valid
        with self.assertNothingRaised(): Layer(Vector(1, 2, 3), 0, 5)
        with self.assertNothingRaised(): Layer(Vector(1, 2, 3), 5, 0)
        with self.assertNothingRaised(): Layer(Vector(1, 2, 3), 4, 5)
        with self.assertNothingRaised(): Layer([1, 2, 3], 4, 5)

        # Zero size
        with self.assertWarnsRegex(UserWarning, r'offsets are equal'): Layer(X, 4, 4)

        # Invalid
        with self.assertRaises(ValueError): Layer(Vector(0, 0, 0), 4, 5) # Zero normal
        with self.assertRaises(TypeError) : Layer(Vector(1, 2, 3), "0", 5)
        with self.assertRaises(TypeError) : Layer(Vector(1, 2, 3), 0, "5")
        with self.assertRaises(TypeError) : Layer(Vector(1, 2, 3))       # Offsets missing
        with self.assertRaises(TypeError) : Layer(Vector(1, 2, 3), 4)    # Offset missing
        with self.assertRaises(TypeError) : Layer(1, 4, 5)               # Wrong type

    def test_equality(self):
        # Same object
        self.assertEqualToItself(Layer(X, 4, 5))

        # Equal objects
        self.assertEqual (Layer(X, 4, 5), Layer(X, 4, 5))

        # Different objects
        self.assertNotEqual (Layer(X, 4, 5), Layer(Y, 4, 5)) # Different normal
        self.assertNotEqual (Layer(X, 4, 5), Layer(X, 5, 4)) # Different offsets (even though equivalent)

        # Equal objects from different specifications
        self.assertEqual(Layer(X, 4, 5), Layer([1, 0, 0], 4, 5))  # Different normal

    def test_to_scad(self):
        self.ignore_scad_comments = True

        # General case, with the normal vector in the Y/Z plane
        self.assertEqual(Layer([0, 1, 1], 2, 2.5).to_scad(),
                         ScadObject("rotate", None, [('a', 45.0), ('v', [-1.0, 0.0, 0.0])], [
                ScadObject("translate", [[0, 0, 2]], None, [
                    ScadObject("translate", [[-infinity/2, -infinity/2, 0]], None, [
                        ScadObject("cube", [[infinity, infinity, 0.5]], None, None)
                    ])
                ])
            ]))

    def test_repr(self):
        self.assertRepr(Layer(X, 2, 3), "Layer(Vector(1, 0, 0), 2, 3)")

    def test_str(self):
        self.assertStr(Layer(X, 2, 3), "Layer with normal <1, 0, 0> from 2 to 3")
