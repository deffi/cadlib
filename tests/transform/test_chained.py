from tests.unit_test import TestCase
from cadlib.transform.chained import Chained
from cadlib.transform.primitives import ScaleAxes, RotateXyz, Translate, ScaleUniform
from cadlib.scad import ScadObject

class TestChained(TestCase):
    def test_construction(self):
        # Parameters
        t1 = ScaleAxes(1, 1, 1)
        t2 = ScaleAxes(2, 2, 2)
        t3 = ScaleAxes(3, 3, 3)

        # Valid
        self.assertEqual(Chained([t1, t2, t3]).transforms, [t1, t2, t3])
        with self.assertNothingRaised(): chained0 = Chained([])                       # No children
        with self.assertNothingRaised(): chained1 = Chained([t1, t2, t3])             # Regular
        with self.assertNothingRaised(): chained2 = Chained([t1, t1, t1])             # Repeated child
        with self.assertNothingRaised(): chained3 = Chained([chained1, t1, chained2]) # Chained child

        # From generator
        self.assertEqual(Chained(tf for tf in [t1, t2, t3]), Chained([t1, t2, t3]))

        # Invalid
        with self.assertRaises(TypeError): Chained(None)
        with self.assertRaises(TypeError): Chained([None])
        with self.assertRaises(TypeError): Chained([1])

    def test_equality(self):
        r = RotateXyz( 60, 30, 15 )
        s = ScaleAxes(1, 2, -1)
        t = Translate([60, 30, 15])
        c = Chained([r, s, t])


        # Same object
        self.assertEqualToItself(c)
        self.assertEqualToItself(Chained([]))

        # Equal objects
        self.assertEqual(Chained([]), Chained([]))
        self.assertEqual(
            Chained([r, s, t]),
            Chained([r, s, t])) # Identical children
        self.assertEqual(
            Chained([RotateXyz( 60, 30, 15 ), ScaleAxes(60, 30, 15), Translate([60, 30, 15])]),
            Chained([RotateXyz( 60, 30, 15 ), ScaleAxes(60, 30, 15), Translate([60, 30, 15])])) # Equal children

        # Different objects
        self.assertNotEqual(Chained([r, s, t]), Chained([r, s]   )) # Different number of children
        self.assertNotEqual(Chained([r, s, t]), Chained([r, t, s])) # Different order of children
        self.assertNotEqual(
            Chained([RotateXyz(60, 30, 15), RotateXyz(60, 30, 15), Translate([60, 30, 15])]),
            Chained([RotateXyz(60, 30, 15), RotateXyz(60, 30, 15), Translate([60, 30, 16])])) # Unequal children

    def test_inverse(self):
        tf1 = ScaleAxes(1, 2, -1) * Translate([1, 2, 3])
        tf2 = Translate([-1, -2, -3]) * ScaleAxes(1, 0.5, -1)
        self.assertInverse(tf1, tf2)

        self.assertInverse(Chained([]), Chained([]))

    def test_to_scad(self):
        # Create some transforms
        r = RotateXyz(60, 30, 15)
        s = ScaleAxes (1, 2, -1)
        t = Translate([30, 20, 10])

        # Non-empty chained with None target
        self.assertEqual(Chained([r, s, t]).to_scad(None),
            ScadObject("rotate", [[60, 30, 15]], None, [
                ScadObject("scale", [[1, 2, -1]], None, [
                    ScadObject("translate", [[30, 20, 10]], None, None)
                ])
            ])
        )

        # Empty chained with valid target
        dummy = ScadObject("dummy", None, None, None)
        self.assertEqual(Chained([]).to_scad(dummy), dummy)

        # Empty chained with None target
        self.assertEqual(Chained([]).to_scad(None), ScadObject(None, None, None, None))

    def test_repr(self):
        self.assertRepr(Chained([ScaleUniform(1), ScaleUniform(2), ScaleUniform(3)]),
            "Chained([ScaleUniform(1), ScaleUniform(2), ScaleUniform(3)])")

    def test_str(self):
        self.assertStr(Chained([ScaleUniform(1), ScaleUniform(2), ScaleUniform(3)]),
            "Chained transform")

    def test_to_matrix(self):
        t = Translate([1, 2, 3])
        r = RotateXyz(0, 0, 90)

        # First rotate, then translate
        self.assertAlmostEqual(Chained([t, r]).to_matrix().row_values, [
            [0, -1, 0, 1],
            [1, 0, 0, 2],
            [0, 0, 1, 3],
            [0, 0, 0, 1],
        ])

        # First translate, then rotate
        self.assertAlmostEqual(Chained([r, t]).to_matrix().row_values, [
            [0, -1, 0, -2],
            [1,  0, 0,  1],
            [0,  0, 1,  3],
            [0,  0, 0,  1],
        ])

        # Empty
        self.assertIdentity(Chained([]).to_matrix())
