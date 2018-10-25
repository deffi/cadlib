import math

from cadlib.object.primitives import Cylinder
from cadlib.util.vector import Vector, X, Y, Z
from cadlib.scad import ScadObject
from tests.unit_test import TestCase

class TestCylinder(TestCase):
    def test_construction(self):
        # Direction/length
        with self.assertNothingRaised(): Cylinder(X, 5, 1)
        with self.assertNothingRaised(): Cylinder(X, 5, r = 1)
        with self.assertNothingRaised(): Cylinder(X, 5, d = 2)

        # Base/cap
        with self.assertNothingRaised(): Cylinder(X              , Y, 1)
        with self.assertNothingRaised(): Cylinder(X              , Y, r = 1)
        with self.assertNothingRaised(): Cylinder(X              , Y, d = 2)
        with self.assertNothingRaised(): Cylinder(Vector(0, 0, 0), Y, d = 2) # Zero vector is allowed as base

        # Zero/cap
        with self.assertNothingRaised(): Cylinder(0, Y, 1)
        with self.assertNothingRaised(): Cylinder(0, Y, r = 1)
        with self.assertNothingRaised(): Cylinder(0, Y, d = 2)

        # Zero size
        with self.assertWarnsRegex(UserWarning, r'length is 0')         : Cylinder(X, 0, 1)
        with self.assertWarnsRegex(UserWarning, r'cap is equal to base'): Cylinder(X, X, 1)
        with self.assertWarnsRegex(UserWarning, r'radius is 0')         : Cylinder(X, 1, 0)
        with self.assertWarnsRegex(UserWarning, r'diameter is 0')       : Cylinder(X, 1, d=0)

        # Invalid
        with self.assertRaises(ValueError): Cylinder(5              , 5)       # First is not a vector
        with self.assertRaises(ValueError): Cylinder(X              , "")      # Second is not a vector or number
        with self.assertRaises(ValueError): Cylinder(X              , 5)       # Radius missing
        with self.assertRaises(ValueError): Cylinder(X              , 5, 1, 1) # Radius and diameter
        with self.assertRaises(ValueError): Cylinder(Vector(0, 0, 0), 5)       # Zero vector is not allowed as direction

    def test_equality(self):
        # Same object
        self.assertEqualToItself(Cylinder(X, 5, 1))

        # Equal objects
        self.assertEqual (Cylinder(X, 5, 1), Cylinder(X, 5, 1))

        # Different objects
        self.assertNotEqual (Cylinder(X, 5, 1), Cylinder(Y, 5, 1))
        self.assertNotEqual (Cylinder(X, 5, 1), Cylinder(X, 6, 1))
        self.assertNotEqual (Cylinder(X, 5, 1), Cylinder(X, 5, 2))

        # Equal objects from different specifications
        self.assertEqual (Cylinder(X, 5, 1), Cylinder(X, 5, d = 2))
        self.assertEqual (Cylinder(X, 5, 1), Cylinder(0, X*5, 1))

    def test_to_scad(self):
        self.ignore_scad_comments = True

        # Along Z axis
        self.assertScadObject(Cylinder(Z, 5,   1  ), "cylinder", [5], [('r', 1)])
        self.assertScadObject(Cylinder(Z, 5,   d=2), "cylinder", [5], [('r', 1)])
        self.assertScadObject(Cylinder(0, Z*4, 1  ), "cylinder", [4], [('r', 1)])

        # Along other axes (X, Y, -X, -Y, -Z)
        cylinder_scad = ScadObject("cylinder", [5], [('r', 1)], None)
        self.assertEqual(Cylinder(X, 5, 1).to_scad(),
            ScadObject("rotate", [], [('a', 90.0), ('v', [0.0, 1.0, 0.0])], [
                cylinder_scad]))
        self.assertEqual(Cylinder(Y, 5, 1).to_scad(),
            ScadObject("rotate", [], [('a', 90.0), ('v', [-1.0, 0.0, 0.0])], [
                cylinder_scad]))
        self.assertEqual(Cylinder(-X, 5, 1).to_scad(),
            ScadObject("rotate", [], [('a', 90.0), ('v', [0.0, -1.0, 0.0])], [
                cylinder_scad]))
        self.assertEqual(Cylinder(-Y, 5, 1).to_scad(),
            ScadObject("rotate", [], [('a', 90.0), ('v', [1.0, 0.0, 0.0])], [
                cylinder_scad]))
        self.assertEqual(Cylinder(-Z, 5, 1).to_scad(),
            ScadObject("rotate", [], [('a', 180.0), ('v', [1.0, 0.0, 0.0])], [
                cylinder_scad]))

        # Parallel to Z axis (shifted along X, X/Y, X/Y/Z)
        cylinder_scad = ScadObject("cylinder", [5], [('r', 1)], None)
        self.assertEqual(Cylinder([1, 0, 0], [1, 0, 5], 1).to_scad(),
            ScadObject("translate", [[1, 0, 0]], [], [
                cylinder_scad]))
        self.assertEqual(Cylinder([1, 2, 0], [1, 2, 5], 1).to_scad(),
            ScadObject("translate", [[1, 2, 0]], [], [
                cylinder_scad]))
        self.assertEqual(Cylinder([1, 2, 3], [1, 2, 8], 1).to_scad(),
            ScadObject("translate", [[1, 2, 3]], [], [
                cylinder_scad]))

        # Parallel to other axis (X)
        cylinder_scad = ScadObject("cylinder", [5], [('r', 1)], None)
        self.assertEqual(Cylinder([0, 1, 2], [5, 1, 2], 1).to_scad(),
            ScadObject("translate", [[0, 1, 2]], [], [
                ScadObject("rotate", [], [('a', 90.0), ('v', [0.0, 1.0, 0.0])], [
                    cylinder_scad])]))

        # Not parallel to axis (in the XZ plane without and with translation)
        cylinder_scad = ScadObject("cylinder", [5*math.sqrt(2)], [('r', 1)], None)
        self.assertEqual(Cylinder([0, 0, 0], [5, 0, 5], 1).to_scad(),
            ScadObject("rotate", [], [('a', 45.0), ('v', [0.0, 1.0, 0.0])], [
                cylinder_scad]))
        self.assertEqual(Cylinder([5, 0, 0], [0, 0, 5], 1).to_scad(),
            ScadObject("translate", [[5, 0, 0]], [], [
                ScadObject("rotate", [], [('a', 45.0), ('v', [0.0, -1.0, 0.0])], [
                    cylinder_scad])]))

    def test_repr(self):
        self.assertRepr(Cylinder(0, 5*X,   1), "Cylinder(Vector(0, 0, 0), Vector(5, 0, 0), r=1")
        self.assertRepr(Cylinder(X, 5  , d=2), "Cylinder(Vector(0, 0, 0), Vector(5.0, 0.0, 0.0), r=1.0")
