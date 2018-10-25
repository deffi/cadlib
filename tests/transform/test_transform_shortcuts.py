from cadlib.transform.primitives import Translate, RotateYpr
from tests.unit_test import TestCase
from cadlib.transform import shortcuts


class TestTransformShortcuts(TestCase):
    def test_translate_shortcuts(self):
        self.assertEqual(shortcuts.up     (1), Translate([ 0,  0,  1]))
        self.assertEqual(shortcuts.down   (2), Translate([ 0,  0, -2]))
        self.assertEqual(shortcuts.left   (3), Translate([-3,  0,  0]))
        self.assertEqual(shortcuts.right  (4), Translate([ 4,  0,  0]))
        self.assertEqual(shortcuts.forward(5), Translate([ 0,  5,  0]))
        self.assertEqual(shortcuts.back   (6), Translate([ 0, -6,  0]))

    def test_rotate_shortcuts(self):
        self.assertEqual(shortcuts.yaw_left  (1), RotateYpr( 1,  0,  0))
        self.assertEqual(shortcuts.yaw_right (2), RotateYpr(-2,  0,  0))
        self.assertEqual(shortcuts.pitch_up  (3), RotateYpr( 0,  3,  0))
        self.assertEqual(shortcuts.pitch_down(4), RotateYpr( 0, -4,  0))
        self.assertEqual(shortcuts.roll_right(5), RotateYpr( 0,  0,  5))
        self.assertEqual(shortcuts.roll_left (6), RotateYpr( 0,  0, -6))
