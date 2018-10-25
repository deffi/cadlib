from cadlib.transform.primitives import Translate
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
        self.assertScadCode(shortcuts.yaw_left  (1), "rotate([0, 0, 1]);")
        self.assertScadCode(shortcuts.yaw_right (2), "rotate([0, 0, -2]);")
        self.assertScadCode(shortcuts.pitch_up  (3), "rotate([3, 0, 0]);")
        self.assertScadCode(shortcuts.pitch_down(4), "rotate([-4, 0, 0]);")
        self.assertScadCode(shortcuts.roll_right(5), "rotate([0, 5, 0]);")
        self.assertScadCode(shortcuts.roll_left (6), "rotate([0, -6, 0]);")
