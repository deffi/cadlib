from cadlib.transform.primitives import Translate, ScaleXyz, RotateXyz, RotateYpr
from cadlib.transform.chained import Chained
from tests.unit_test import TestCase

class TestTransform(TestCase):
    def test_inequality(self):
        # Different-type transformations are not equal (even if the values are identical)
        transforms = [
            ScaleXyz (1, 2, 3),
            Translate([1, 2, 3]),
            RotateXyz(1, 2, 3),
            RotateYpr(1, 2, 3),
        ]

        for t1 in transforms:
            for t2 in transforms:
                if t1 is not t2:
                    self.assertNotEqual(t1, t2)

    def test_multiplication(self):
        # Create some transform
        r = RotateXyz(60, 30, 15)
        s = ScaleXyz (1, 2, -1)
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
            with self.assertRaises(TypeError): t * invalid
            with self.assertRaises(TypeError): invalid * t

    def test_invalid_operators(self):
        t = Translate([30, 20, 10])

        for other in [t, None, 0, 0.0, ""]:
            with self.assertRaises(TypeError): t + other
            with self.assertRaises(TypeError): t - other
            with self.assertRaises(TypeError): other + t
            with self.assertRaises(TypeError): other - t
