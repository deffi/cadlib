from tests.unit_test import TestCase
from cadlib.transform.primitives import RotateFromTo
from cadlib.util import Vector, X, Y, Z
from cadlib.object.primitives import Cube

class TestRotateFromTo(TestCase):
    def test_construction(self):
        # Valid
        RotateFromTo(      [1, 2, 3],       [4, 5, 6])
        RotateFromTo(Vector(1, 2, 3), Vector(4, 5, 6))

        # Invalid
        with self.assertRaises(TypeError ): RotateFromTo([1, 2, 3], 45 )
        with self.assertRaises(TypeError ): RotateFromTo(45, [1, 2, 3])
        with self.assertRaises(TypeError ): RotateFromTo([1, 2, "3"], [4, 5,  6])
        with self.assertRaises(TypeError ): RotateFromTo([1, 2,  3 ], [4, 5, "6"])

        # Zero vectors
        o = Vector.zero(3)
        with self.assertRaises(ValueError): RotateFromTo(X, o)
        with self.assertRaises(ValueError): RotateFromTo(X, o)
        with self.assertRaises(ValueError): RotateFromTo(o, o)

        # Opposite direction (ambiguous rotation)
        with self.assertWarns(UserWarning): RotateFromTo([1, 0, 0], [-1,  0,  0])
        with self.assertWarns(UserWarning): RotateFromTo([1, 2, 3], [-2, -4, -6])

    def test_equality(self):
        # Same object
        self.assertEqualToItself(RotateFromTo(Vector(1, 2, 3), Vector(4, 5, 6)))

        # Equal objects
        self.assertEqual(RotateFromTo([1, 2, 3], [4, 5, 6]), RotateFromTo([1, 2, 3], [4, 5, 6])) # Equal

        # Different objects
        self.assertNotEqual(RotateFromTo([1, 2, 3], [4, 5, 6]), RotateFromTo([1, 2, 3], [4, 5, 7])) # Different from
        self.assertNotEqual(RotateFromTo([1, 2, 3], [4, 5, 6]), RotateFromTo([1, 2, 7], [4, 5, 6])) # Different to

        # Equal objects from different specifications
        self.assertEqual(RotateFromTo(Vector(1, 2, 3), [4, 5, 6]), RotateFromTo([1, 2, 3], [4, 5, 6]))
        self.assertEqual(RotateFromTo([1, 2, 3], Vector(4, 5, 6)), RotateFromTo([1, 2, 3], [4, 5, 6]))

    def test_inverse(self):
        self.assertEqual(RotateFromTo(X, Y).inverse(), RotateFromTo(Y, X))

    def test_to_scad(self):
        self.ignore_scad_comments = True

        # Unit axis to unit axis
        self.assertScadObjectTarget(RotateFromTo(X, Y), None, "rotate", None, [("a", 90), ("v", [ 0,  0,  1])], None)
        self.assertScadObjectTarget(RotateFromTo(Y, Z), None, "rotate", None, [("a", 90), ("v", [ 1,  0,  0])], None)
        self.assertScadObjectTarget(RotateFromTo(Z, X), None, "rotate", None, [("a", 90), ("v", [ 0,  1,  0])], None)
        self.assertScadObjectTarget(RotateFromTo(Y, X), None, "rotate", None, [("a", 90), ("v", [ 0,  0, -1])], None)
        self.assertScadObjectTarget(RotateFromTo(Z, Y), None, "rotate", None, [("a", 90), ("v", [-1,  0,  0])], None)
        self.assertScadObjectTarget(RotateFromTo(X, Z), None, "rotate", None, [("a", 90), ("v", [ 0, -1,  0])], None)

        # Unit axis to unit axis with different length
        self.assertScadObjectTarget(RotateFromTo(X, 2 * Y), None, "rotate", None, [("a", 90), ("v", [0, 0, 1])], None)

        # Different signs for X/Y axes
        self.assertScadObjectTarget(RotateFromTo( X,  Y), None, "rotate", None, [("a", 90), ("v", [ 0,  0,  1])], None)
        self.assertScadObjectTarget(RotateFromTo( X, -Y), None, "rotate", None, [("a", 90), ("v", [ 0,  0, -1])], None)
        self.assertScadObjectTarget(RotateFromTo(-X,  Y), None, "rotate", None, [("a", 90), ("v", [ 0,  0, -1])], None)
        self.assertScadObjectTarget(RotateFromTo(-X, -Y), None, "rotate", None, [("a", 90), ("v", [ 0,  0,  1])], None)
        self.assertScadObjectTarget(RotateFromTo( Y,  X), None, "rotate", None, [("a", 90), ("v", [ 0,  0, -1])], None)
        self.assertScadObjectTarget(RotateFromTo( Y, -X), None, "rotate", None, [("a", 90), ("v", [ 0,  0,  1])], None)
        self.assertScadObjectTarget(RotateFromTo(-Y,  X), None, "rotate", None, [("a", 90), ("v", [ 0,  0,  1])], None)
        self.assertScadObjectTarget(RotateFromTo(-Y, -X), None, "rotate", None, [("a", 90), ("v", [ 0,  0, -1])], None)

        # Same direction (no effect) - no transform
        cube = Cube(2)
        self.assertEqual(RotateFromTo(X        , X        ).to_scad(cube), cube)
        self.assertEqual(RotateFromTo([1, 2, 3], [2, 4, 6]).to_scad(cube), cube)

        # Opposite direction (ambiguous rotation)
        self.assertIn(("a", 180), RotateFromTo(X        , -X          , ignore_ambiguity=True).to_scad(None)._kw_parameters)
        self.assertIn(("a", 180), RotateFromTo([1, 2, 3], [-2, -4, -6], ignore_ambiguity=True).to_scad(None)._kw_parameters)

    def test_repr(self):
        self.assertRepr(RotateFromTo(X, Y), "RotateFromTo(Vector(1, 0, 0), Vector(0, 1, 0))")
