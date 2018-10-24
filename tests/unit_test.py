from unittest import TestCase as OriginalTestCase
from cadlib.transform import Transform
from contextlib import contextmanager
from cadlib.scad import ScadObject
from cadlib.object import Object

class TestCase(OriginalTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO test
        self._ignore_scad_comments = False

    @property
    def ignore_scad_comments(self):
        return self._ignore_scad_comments

    @ignore_scad_comments.setter
    def ignore_scad_comments(self, value):
        self._ignore_scad_comments = value

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
        actual = thing.to_scad()
        if self._ignore_scad_comments:
            actual = actual.clear_comment(recursive = True)
        expected = ScadObject(id, parameters, kw_parameters, children)
        self.assertEqual(actual, expected)

    def assertScadObjectTarget(self, thing, target, id, parameters, kw_parameters, children = None):
        actual = thing.to_scad(target)
        if self._ignore_scad_comments:
            actual = actual.clear_comment(recursive = True)
        expected = ScadObject(id, parameters, kw_parameters, children)
        self.assertEqual(actual, expected)

    def assertScadCode(self, thing, code):
        if isinstance(thing, Transform):
            self.assertEqual(thing.to_scad(None).to_code(inline=True, simplify=True), code)
        else:
            self.assertEqual(thing.to_scad().to_code(inline=True, simplify=True), code)

    def assertEqual(self, first, second, msg=None):
        if self._ignore_scad_comments:
            if isinstance(first, ScadObject):
                first = first.clear_comment(recursive=True)
            if isinstance(second, ScadObject):
                second = second.clear_comment(recursive=True)

        super().assertEqual(first, second, msg)

    def assertRepr(self, thing, expected):
        self.assertEqual(repr(thing), expected)
