from cadlib.object.primitives import Sphere
from cadlib.object.transformed import Transformed
from cadlib.transform.primitives.translate import Translate
from cadlib.transform.primitives.rotate_ypr import RotateYpr
from cadlib.transform.shortcuts import *
from tests.unit_test import TestCase

class TestTransform(TestCase):
    def test_translate_shortcuts(self):
        self.assertEqual(up     (1), Translate([ 0,  0,  1]))
        self.assertEqual(down   (2), Translate([ 0,  0, -2]))
        self.assertEqual(left   (3), Translate([-3,  0,  0]))
        self.assertEqual(right  (4), Translate([ 4,  0,  0]))
        self.assertEqual(forward(5), Translate([ 0,  5,  0]))
        self.assertEqual(back   (6), Translate([ 0, -6,  0]))

    def test_rotate_shortcuts(self):
        self.assertScadCode(yaw_left  (1), "rotate([0, 0, 1]);")
        self.assertScadCode(yaw_right (2), "rotate([0, 0, -2]);")
        self.assertScadCode(pitch_up  (3), "rotate([3, 0, 0]);")
        self.assertScadCode(pitch_down(4), "rotate([-4, 0, 0]);")
        self.assertScadCode(roll_right(5), "rotate([0, 5, 0]);")
        self.assertScadCode(roll_left (6), "rotate([0, -6, 0]);")


    def test_translate_object_shortcuts(self):
        a = Sphere(2)

        self.assertEqual(a.up     (1), Transformed(Translate([ 0,  0,  1]), a))
        self.assertEqual(a.down   (2), Transformed(Translate([ 0,  0, -2]), a))
        self.assertEqual(a.left   (3), Transformed(Translate([-3,  0,  0]), a))
        self.assertEqual(a.right  (4), Transformed(Translate([ 4,  0,  0]), a))
        self.assertEqual(a.forward(5), Transformed(Translate([ 0,  5,  0]), a))
        self.assertEqual(a.back   (6), Transformed(Translate([ 0, -6,  0]), a))

    def test_translate_object_shortcuts(self):
        a = Sphere(2)

        self.assertEqual(a.yaw_left  (1), Transformed(RotateYpr( 1,  0,  0), a))
        self.assertEqual(a.yaw_right (2), Transformed(RotateYpr(-2,  0,  0), a))
        self.assertEqual(a.pitch_up  (3), Transformed(RotateYpr( 0,  3,  0), a))
        self.assertEqual(a.pitch_down(4), Transformed(RotateYpr( 0, -4,  0), a))
        self.assertEqual(a.roll_right(5), Transformed(RotateYpr( 0,  0,  5), a))
        self.assertEqual(a.roll_left (6), Transformed(RotateYpr( 0,  0, -6), a))
