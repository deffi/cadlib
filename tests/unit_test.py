from unittest import TestCase as OriginalTestCase
from cadlib.transform import Transform
from contextlib import contextmanager
from cadlib.scad import ScadObject
from cadlib.object import Object

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


    def assertScadObject(self, thing, id, parameters, kw_parameters, children = None):
        actual = thing.to_scad().clear_comment()
        expected = ScadObject(id, parameters, kw_parameters, children)
        self.assertEqual(actual, expected)

    def assertScadObjectTarget(self, thing, target, id, parameters, kw_parameters, children = None):
        actual = thing.to_scad(target).clear_comment()
        expected = ScadObject(id, parameters, kw_parameters, children)
        self.assertEqual(actual, expected)

    def assertScadCode(self, thing, code):
        if isinstance(thing, Transform):
            self.assertEqual(thing.to_scad(None).to_code(inline=True, simplify=True), code)
        else:
            self.assertEqual(thing.to_scad().to_code(inline=True, simplify=True), code)

    def assertRepr(self, thing, expected):
        self.assertEqual(repr(thing), expected)
