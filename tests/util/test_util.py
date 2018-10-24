import unittest

from cadlib import util

class TestUtil(unittest.TestCase):
    def test_both(self):
        # Both non-None, even if they are falsey
        self.assertTrue(util.both (1, 1))
        self.assertTrue(util.both (0, 0))
        self.assertTrue(util.both (False, False))

        # One None
        self.assertFalse(util.both(None, 1))
        self.assertFalse(util.both(1, None))

        # Both None
        self.assertFalse(util.both(None, None))

    def test_neigher(self):
        # Both non-None, even if they are falsey
        self.assertFalse(util.neither(1, 1))
        self.assertFalse(util.neither(0, 0))
        self.assertFalse(util.neither(False, False))

        # One None
        self.assertFalse(util.neither(None, 1))
        self.assertFalse(util.neither(1, None))

        # Both None
        self.assertTrue(util.neither(None, None))


if __name__ == '__main__':
    unittest.main()
