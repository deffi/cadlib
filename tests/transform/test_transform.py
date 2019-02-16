from cadlib.transform.primitives import RotateAxisAngle, RotateFromTo, RotateXyz, RotateYpr, ScaleAxisFactor, ScaleUniform, ScaleAxes, Translate
from cadlib.transform import Transform
from cadlib.transform.chained import Chained
from tests.unit_test import TestCase
from cadlib.util import X, Y, Z
from cadlib.util import Vector

class TestTransform(TestCase):
    def test_inequality(self):
        # Different-type transformations are not equal (even if the values are identical)
        transforms = [
            RotateAxisAngle(X, 0),
            RotateFromTo(X, X),
            RotateXyz(0, 0, 0),
            RotateYpr(0, 0, 0),
            ScaleAxisFactor(X, 1),
            ScaleUniform(1),
            ScaleAxes (1, 1, 1),
            Translate([0, 0, 0]),
        ]

        for t1 in transforms:
            for t2 in transforms:
                if t1 is not t2:
                    self.assertNotEqual(t1, t2)

    def test_not_implemented(self):
        tf = Transform()
        with self.assertRaises(NotImplementedError): tf.inverse()
        with self.assertRaises(NotImplementedError): tf.to_scad(None)
        with self.assertRaises(NotImplementedError): tf.to_matrix()

    def test_multiplication(self):
        # Create some transform
        r = RotateXyz(60, 30, 15)
        s = ScaleAxes (1, 2, -1)
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

        # Empty chained
        self.assertEqual(Chained([]) * Chained([]), Chained([]))
        self.assertEqual(Chained([]) * r, Chained([r]))
        self.assertEqual(r * Chained([]), Chained([r]))

    def test_multiplication_with_vector(self):
        r = RotateAxisAngle(X, 90)
        s = ScaleAxes (1, 2, -1)
        t = Translate([1, 2, 3])

        self.assertAlmostEqual(r * Vector( 0,  0,  0), Vector( 0,   0,  0))
        self.assertAlmostEqual(r * Vector(10, 20, 30), Vector(10, -30, 20))

        self.assertAlmostEqual(s * Vector( 0,  0,  0), Vector( 0,  0,   0))
        self.assertAlmostEqual(s * Vector(10, 20, 30), Vector(10, 40, -30))

        self.assertAlmostEqual(t * Vector( 0,  0,  0), Vector( 1,  2,  3))
        self.assertAlmostEqual(t * Vector(10, 20, 30), Vector(11, 22, 33))

        self.assertAlmostEqual((t *  s) * Vector(10, 20, 30) , Vector(11, 42, -27))
        self.assertAlmostEqual( t * (s  * Vector(10, 20, 30)), Vector(11, 42, -27))

        with self.assertRaises(ValueError): r * Vector(0, 0)

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
