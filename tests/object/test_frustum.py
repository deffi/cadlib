import math

from cadlib.object.primitives import Frustum
from cadlib.util.vector import Vector, X, Y, Z
from cadlib.scad import ScadObject
from tests.unit_test import TestCase

class TestFrustum(TestCase):
    def test_construction(self):
        with self.assertNothingRaised(): Frustum(X, Y, 1, 0)
        with self.assertNothingRaised(): Frustum(0, Y, 1, 0) # Zero as shortcut
        with self.assertNothingRaised(): Frustum(X, 0, 1, 0) # Zero as shortcut

        # Zero size
        with self.assertWarnsRegex(UserWarning, r'length is 0'): Frustum(X, X, 1, 2)
        with self.assertWarnsRegex(UserWarning, r'length is 0'): Frustum(X, (1, 0, 0), 1, 2)
        with self.assertWarnsRegex(UserWarning, r'radius is 0'): Frustum(0, X, 0, 0)

        # Invalid
        Frustum(X, Y, 1, 2)  # Reference
        with self.assertRaises(TypeError): Frustum(1, Y, 1, 2) # Base is not a vector
        with self.assertRaises(TypeError): Frustum(X, 1, 1, 2) # Cap is not a vector
        with self.assertRaises(TypeError): Frustum(X, Y, X, 2) # Base radius is not a number
        with self.assertRaises(TypeError): Frustum(X, Y, 1, X) # Base radius is not a number

    def test_direction_length(self):
        self.assertEqual(Frustum.direction_length(X, 5, 1, 2), Frustum(0, X*5, 1, 2))

        # Zero size
        with self.assertWarnsRegex(UserWarning, r'length is 0'): Frustum.direction_length(X, 0, 1, 2)

    def test_equality(self):
        # Same object
        self.assertEqualToItself(Frustum(0, X, 2, 1))

        # Equal objects
        self.assertEqual(Frustum(X, Y, 1, 2), Frustum(X, Y, 1, 2))
        self.assertEqual(Frustum(X, 0, 1, 2), Frustum(X, 0, 1, 2))

        # Different objects
        self.assertNotEqual(Frustum(X, Y, 1, 2), Frustum(Y, X, 1, 2))
        self.assertNotEqual(Frustum(X, Y, 1, 2), Frustum(X, Y, 2, 1))
        self.assertNotEqual(Frustum(X, Y, 1, 2), Frustum(Y, X, 2, 1))

        # Equal objects from different specifications
        self.assertEqual(Frustum(X, Y, 1, 2), Frustum((1, 0, 0), Y, 1, 2))

    def test_to_scad(self):
        self.ignore_scad_comments = True

        # Cylinder along Z axis
        self.assertScadObject(Frustum(0, 5*Z, 1, 1), "cylinder", [5.0], [('r', 1)])

        # Cone along Z axis
        self.assertScadObject(Frustum(0, 5*Z, 1, 0), "cylinder", [5.0], [('r1', 1), ('r2', 0)])

        # Frustum along Z axis
        self.assertScadObject(Frustum(0, 5*Z, 2, 1), "cylinder", [5.0], [('r1', 2), ('r2', 1)])

        # Cylinder along other axes (X, Y, -X, -Y, -Z)
        cylinder_scad = ScadObject("cylinder", [5], [('r', 1)], None)
        self.assertEqual(Frustum(0, 5*X, 1, 1).to_scad(),
            ScadObject("rotate", [], [('a', 90.0), ('v', [0.0, 1.0, 0.0])], [
                cylinder_scad]))
        self.assertEqual(Frustum(0, 5*Y, 1, 1).to_scad(),
            ScadObject("rotate", [], [('a', 90.0), ('v', [-1.0, 0.0, 0.0])], [
                cylinder_scad]))
        self.assertEqual(Frustum(0, -5*X, 1, 1).to_scad(),
            ScadObject("rotate", [], [('a', 90.0), ('v', [0.0, -1.0, 0.0])], [
                cylinder_scad]))
        self.assertEqual(Frustum(0, -5*Y, 1, 1).to_scad(),
            ScadObject("rotate", [], [('a', 90.0), ('v', [1.0, 0.0, 0.0])], [
                cylinder_scad]))
        self.assertEqual(Frustum(0, -5*Z, 1, 1).to_scad(),
            ScadObject("rotate", [], [('a', 180.0), ('v', [1.0, 0.0, 0.0])], [
                cylinder_scad]))

        # Parallel to Z axis (shifted along X, X/Y, X/Y/Z)
        cylinder_scad = ScadObject("cylinder", [5], [('r', 1)], None)
        self.assertEqual(Frustum([1, 0, 0], [1, 0, 5], 1, 1).to_scad(),
            ScadObject("translate", [[1, 0, 0]], [], [
                cylinder_scad]))
        self.assertEqual(Frustum([1, 2, 0], [1, 2, 5], 1, 1).to_scad(),
            ScadObject("translate", [[1, 2, 0]], [], [
                cylinder_scad]))
        self.assertEqual(Frustum([1, 2, 3], [1, 2, 8], 1, 1).to_scad(),
            ScadObject("translate", [[1, 2, 3]], [], [
                cylinder_scad]))

        # Parallel to other axis (X)
        cylinder_scad = ScadObject("cylinder", [5], [('r', 1)], None)
        self.assertEqual(Frustum([0, 1, 2], [5, 1, 2], 1, 1).to_scad(),
            ScadObject("translate", [[0, 1, 2]], [], [
                ScadObject("rotate", [], [('a', 90.0), ('v', [0.0, 1.0, 0.0])], [
                    cylinder_scad])]))

        # Not parallel to axis (in the XZ plane without and with translation)
        cylinder_scad = ScadObject("cylinder", [5*math.sqrt(2)], [('r', 1)], None)
        self.assertEqual(Frustum([0, 0, 0], [5, 0, 5], 1, 1).to_scad(),
            ScadObject("rotate", [], [('a', 45.0), ('v', [0.0, 1.0, 0.0])], [
                cylinder_scad]))
        self.assertEqual(Frustum([5, 0, 0], [0, 0, 5], 1, 1).to_scad(),
            ScadObject("translate", [[5, 0, 0]], [], [
                ScadObject("rotate", [], [('a', 45.0), ('v', [0.0, -1.0, 0.0])], [
                    cylinder_scad])]))

    def test_repr(self):
        self.assertRepr(Frustum(0, 5*X, 1, 2), "Frustum(Vector(0, 0, 0), Vector(5, 0, 0), 1, 2)")

    def test_str(self):
        self.assertStr(Frustum(Y, 5*X, 1, 2), "Frustum with base <0, 1, 0> (base radius 1) and cap <5, 0, 0> (cap radius 2)")
