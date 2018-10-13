from cadlib.transform.chained import Chained
from cadlib.transform.primitives.translate import Translate
from cadlib.transform.primitives.scale import Scale
from cadlib.transform.primitives.rotate_xyz import RotateXyz
from cadlib.scad.scad import ScadObject
from tests.unit_test import TestCase

class TestTransform(TestCase):
    def test_construction(self):
        # Primitives
        r = RotateXyz( 60, 30, 15 )
        s = Scale    ([1, 2, -1])
        t = Translate([30, 20, 10])

        # Chained transform
        chained0 = Chained([])                           # No children
        chained1 = Chained([r, s, t])   # Regular
        chained2 = Chained([r, r, r])     # Repeated child
        chained3 = Chained([chained1, r, chained2]) # Chained child
        with self.assertRaises(TypeError): Chained(None)
        with self.assertRaises(TypeError): Chained([None])
        with self.assertRaises(TypeError): Chained([1])

    def test_equality(self):
        # For each type (rotate, scale, translate, chained), 1a and 1b have the same parameters, and 2 has different
        # parameters.
        r = RotateXyz( 60, 30, 15 )
        s = Scale    ([60, 30, 15])
        t = Translate([60, 30, 15])
        c = Chained([r, s, t])

        # Any transform is equal to itself
        self.assertEqualToItself(r)
        self.assertEqualToItself(s)
        self.assertEqualToItself(t)
        self.assertEqualToItself(c)

        # Same-type transformations with equal parameters are equal
        self.assertEqual(RotateXyz( 60, 30, 15 ), RotateXyz( 60, 30, 15 ))
        self.assertEqual(Scale    ([60, 30, 15]), Scale    ([60, 30, 15]))
        self.assertEqual(Translate([60, 30, 15]), Translate([60, 30, 15]))
        self.assertEqual(
            Chained([r, s, t]),
            Chained([r, s, t])) # Identical children
        self.assertEqual(
            Chained([RotateXyz( 60, 30, 15 ), Scale([60, 30, 15]), Translate([60, 30, 15])]),
            Chained([RotateXyz( 60, 30, 15 ), Scale([60, 30, 15]), Translate([60, 30, 15])])) # Equal children

        # Same-type transformations with unequal parameters are not equal
        self.assertNotEqual(RotateXyz( 60, 30, 15 ), RotateXyz( 60, 30, 16 ))
        self.assertNotEqual(Scale    ([60, 30, 15]), Scale    ([60, 30, 16]))
        self.assertNotEqual(Translate([60, 30, 15]), Translate([60, 30, 16]))
        self.assertNotEqual(Chained([r, s, t]), Chained([r, s]   )) # Different number of children
        self.assertNotEqual(Chained([r, s, t]), Chained([r, t, s])) # Different order of children
        self.assertNotEqual(
            Chained([RotateXyz(60, 30, 15), RotateXyz(60, 30, 15), Translate([60, 30, 15])]),
            Chained([RotateXyz(60, 30, 15), RotateXyz(60, 30, 15), Translate([60, 30, 16])])) # Unequal children

        # Different-type transformations are not equal (even if the values are identical)
        self.assertNotEqual(r, s)
        self.assertNotEqual(s, t)
        self.assertNotEqual(t, c)
        self.assertNotEqual(c, r)

    def test_multiplication(self):
        # Create some transform
        r = RotateXyz(60, 30, 15)
        s = Scale    ([1, 2, -1])
        t = Translate([30, 20, 10])

        # 2-chained
        self.assertEqual(r * s, Chained([r, s]))

        # 3-chained
        self.assertEqual(   r *  s  * t   , Chained([r, s, t]))
        self.assertEqual(  (r *  s) * t   , Chained([r, s, t]))
        self.assertEqual(   r * (s  * t)  , Chained([r, s, t]))

        # Multiplication is associative, but not commutative (kind-of already follows from the other tests)
        self.assertEqual   (  (r * s) * t, r * (s * t)  )
        self.assertNotEqual(  r * s      , s * r        )

        # 4-chained
        self.assertEqual(    r  *  s  *  r  * s    , Chained([r, s, r, s]))
        self.assertEqual(   (r  *  s) * (r  * s)   , Chained([r, s, r, s]))
        self.assertEqual(  ((r  *  s) *  r) * s    , Chained([r, s, r, s]))
        self.assertEqual(    r  * (s  * (r  * s))  , Chained([r, s, r, s]))
        rs = r * s
        self.assertEqual(          rs * rs         , Chained([r, s, r, s]))

    def test_multiplication_with_invalid(self):
        t = Translate([30, 20, 10])

        for invalid in [None, 0, 0.0, ""]:
            with self.assertRaises(TypeError): t + invalid
            with self.assertRaises(TypeError): t - invalid
            with self.assertRaises(TypeError): t * invalid
            with self.assertRaises(TypeError): invalid + t
            with self.assertRaises(TypeError): invalid - t
            with self.assertRaises(TypeError): invalid * t

    def test_to_scad(self):
        # Create some transform
        r = RotateXyz(60, 30, 15)
        s = Scale    ([1, 2, -1])
        t = Translate([30, 20, 10])

        # A chained transform (of None) maps to a non-branching tree.
        self.assertEqual((r * s * t).to_scad(None),
            ScadObject("rotate", [[60, 30, 15]], None, [
                ScadObject("scale", [[1, 2, -1]], None, [
                    ScadObject("translate", [[30, 20, 10]], None, None)
                ])
            ])
        )
