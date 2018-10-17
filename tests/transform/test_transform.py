from cadlib.transform.primitives.translate import Translate
from cadlib.transform.primitives.scale import Scale
from cadlib.transform.primitives.rotate_xyz import RotateXyz
from cadlib.transform.primitives.rotate_ypr import RotateYpr
from cadlib.transform.chained import Chained
from tests.unit_test import TestCase
from cadlib.transform import shortcuts

class TestTransform(TestCase):
    def test_inequality(self):
        # Different-type transformations are not equal (even if the values are identical)
        transforms = [
            Scale    ([1, 2, 3]),
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
            with self.assertRaises(TypeError): t * invalid
            with self.assertRaises(TypeError): invalid * t

    def test_invalid_operators(self):
        t = Translate([30, 20, 10])

        for other in [t, None, 0, 0.0, ""]:
            with self.assertRaises(TypeError): t + other
            with self.assertRaises(TypeError): t - other
            with self.assertRaises(TypeError): other + t
            with self.assertRaises(TypeError): other - t


    ###############
    ## Shortcuts ##
    ###############

    def test_translate_shortcuts(self):
        self.assertEqual(shortcuts.up     (1), Translate([ 0,  0,  1]))
        self.assertEqual(shortcuts.down   (2), Translate([ 0,  0, -2]))
        self.assertEqual(shortcuts.left   (3), Translate([-3,  0,  0]))
        self.assertEqual(shortcuts.right  (4), Translate([ 4,  0,  0]))
        self.assertEqual(shortcuts.forward(5), Translate([ 0,  5,  0]))
        self.assertEqual(shortcuts.back   (6), Translate([ 0, -6,  0]))

    def test_rotate_shortcuts(self):
        self.assertScadCode(shortcuts.yaw_left  (1), "rotate([0, 0, 1]);")
        self.assertScadCode(shortcuts.yaw_right (2), "rotate([0, 0, -2]);")
        self.assertScadCode(shortcuts.pitch_up  (3), "rotate([3, 0, 0]);")
        self.assertScadCode(shortcuts.pitch_down(4), "rotate([-4, 0, 0]);")
        self.assertScadCode(shortcuts.roll_right(5), "rotate([0, 5, 0]);")
        self.assertScadCode(shortcuts.roll_left (6), "rotate([0, -6, 0]);")
