from unittest import TestCase as OriginalTestCase
from cadlib.transform.transform_primitives import Transform
from contextlib import contextmanager

class TestCase(OriginalTestCase):
    def assertEqualToItself(self, x):
        self.assertEqual(x, x)

    @contextmanager
    def assertNothingRaised(self):
        """
        Similar to assertRaises, this method will raise the original exception, if any is raised.
        """

        # ...this makes the implementation very simple:
        yield

    def assertScadCode(self, thing, code):
        if isinstance(thing, Transform):
            self.assertEqual(thing.to_scad(None).to_code(inline=True, simplify=True), code)
        else:
            self.assertEqual(thing.to_scad().to_code(inline=True, simplify=True), code)

