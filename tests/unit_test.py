from unittest import TestCase as OriginalTestCase
from cadlib.transform import Transform
from contextlib import contextmanager
from cadlib.scad import ScadObject

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
        self.assertEqual(thing.to_scad(), ScadObject(id, parameters, kw_parameters, children))

    def assertScadObjectTarget(self, thing, target, id, parameters, kw_parameters, children = None):
        self.assertEqual(thing.to_scad(target), ScadObject(id, parameters, kw_parameters, children))

    def assertScadCode(self, thing, code):
        if isinstance(thing, Transform):
            self.assertEqual(thing.to_scad(None).to_code(inline=True, simplify=True), code)
        else:
            self.assertEqual(thing.to_scad().to_code(inline=True, simplify=True), code)
