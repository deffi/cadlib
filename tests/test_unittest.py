from tests.unit_test import TestCase

class Foo(Exception):
    pass

class Bar(Exception):
    pass

class TestUnitTest(TestCase):
    def test_assertRaises(self):
        # Expected raise
        with self.assertRaises(Foo):
            raise Foo

        # Nothing raised
        with self.assertRaises(AssertionError):
            with self.assertRaises(Foo):
                pass

        # Wrong exception raised
        with self.assertRaises(Bar):
            with self.assertRaises(Foo):
                raise Bar

    def test_assertNothingRaised(self):
        # Expected nothing
        with self.assertNothingRaised():
            pass

        # Unexpected raise
        with self.assertRaises(Foo):
            with self.assertNothingRaised():
                raise Foo