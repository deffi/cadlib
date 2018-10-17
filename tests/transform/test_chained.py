from tests.unit_test import TestCase
from cadlib.transform.chained import Chained
from cadlib.transform.primitives.scale import Scale
from cadlib.transform.primitives.rotate_xyz import RotateXyz
from cadlib.transform.primitives.translate import Translate
from cadlib.scad.scad import ScadObject

class TestChained(TestCase):
    def test_construction(self):
        # Parameters
        t1 = Scale([1, 1, 1])
        t2 = Scale([2, 2, 2])
        t3 = Scale([3, 3, 3])

        # Valid
        with self.assertNothingRaised(): chained0 = Chained([])                       # No children
        with self.assertNothingRaised(): chained1 = Chained([t1, t2, t3])             # Regular
        with self.assertNothingRaised(): chained2 = Chained([t1, t1, t1])             # Repeated child
        with self.assertNothingRaised(): chained3 = Chained([chained1, t1, chained2]) # Chained child

        # Invalid
        with self.assertRaises(TypeError): Chained(None)
        with self.assertRaises(TypeError): Chained([None])
        with self.assertRaises(TypeError): Chained([1])

    def test_equality(self):
        r = RotateXyz( 60, 30, 15 )
        s = Scale([1, 2, -1])
        t = Translate([60, 30, 15])
        c = Chained([r, s, t])


        # Same object
        self.assertEqualToItself(c)

        # Equal objects
        self.assertEqual(
            Chained([r, s, t]),
            Chained([r, s, t])) # Identical children
        self.assertEqual(
            Chained([RotateXyz( 60, 30, 15 ), Scale([60, 30, 15]), Translate([60, 30, 15])]),
            Chained([RotateXyz( 60, 30, 15 ), Scale([60, 30, 15]), Translate([60, 30, 15])])) # Equal children

        # Different objects
        self.assertNotEqual(Chained([r, s, t]), Chained([r, s]   )) # Different number of children
        self.assertNotEqual(Chained([r, s, t]), Chained([r, t, s])) # Different order of children
        self.assertNotEqual(
            Chained([RotateXyz(60, 30, 15), RotateXyz(60, 30, 15), Translate([60, 30, 15])]),
            Chained([RotateXyz(60, 30, 15), RotateXyz(60, 30, 15), Translate([60, 30, 16])])) # Unequal children

    def test_to_scad(self):
        # Create some transform
        r = RotateXyz(60, 30, 15)
        s = Scale    ([1, 2, -1])
        t = Translate([30, 20, 10])

        self.assertEqual(Chained([r, s, t]).to_scad(None),
            ScadObject("rotate", [[60, 30, 15]], None, [
                ScadObject("scale", [[1, 2, -1]], None, [
                    ScadObject("translate", [[30, 20, 10]], None, None)
                ])
            ])
        )
