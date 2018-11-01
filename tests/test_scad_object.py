from cadlib.scad import ScadObject, render_to_file
from tests.unit_test import TestCase
from cadlib.util.tree import Node
from cadlib.object.primitives import Sphere, Cube, Cylinder
from tempfile import mkstemp
import os

class TestScadObject(TestCase):
    def test_construction(self):
        # Name only
        o1 = ScadObject("Dummy", None, None, None)

        # Name, parameters and keyword parameters
        o2 = ScadObject("Cylinder", [11], [("r", 2)], None)

        # Children
        o3 = ScadObject("Union", None, None, [o2, o1]) # Two children
        o4 = ScadObject("Union", None, None, [o3, o2]) # One child has children, and o2 appears in the tree twice

        # Empty without children
        ScadObject(None, None, None, None)

        # Empty with children
        ScadObject(None, None, None, [o2, o1])

    def test_invalid_construction(self):
        dummy = ScadObject("Dummy", None, None, None)

        # Invalid name
        with self.assertNothingRaised():    ScadObject("Dummy", None, None, None) # Reference
        with self.assertRaises(TypeError):  ScadObject(0      , None, None, None)
        with self.assertRaises(TypeError):  ScadObject([""]   , None, None, None)
        with self.assertRaises(TypeError):  ScadObject(("",)  , None, None, None)
        with self.assertRaises(ValueError): ScadObject(""     , None, None, None)

        # Empty with parameters
        with self.assertNothingRaised():    ScadObject(None   , None, None, None)  # Reference
        with self.assertRaises(ValueError): ScadObject(None   , [11], None, None)
        with self.assertRaises(ValueError): ScadObject(None   , None, [("r", 2)], None)

        # Invalid keyword parameters
        with self.assertNothingRaised():   ScadObject("Dummy", None, []           , None)
        with self.assertRaises(TypeError): ScadObject("Dummy", None, ("r", 2)     , None) # Not in a list
        with self.assertRaises(TypeError): ScadObject("Dummy", None, [["r", 2]]   , None) # Not a tuple
        with self.assertRaises(TypeError): ScadObject("Dummy", None, [("r", 2, 3)], None)  # Not a 2-tuple
        with self.assertRaises(TypeError): ScadObject("Dummy", None, [("r", )]    , None)  # Not a 2-tuple
        with self.assertRaises(TypeError): ScadObject("Dummy", None, [(1, 2)]     , None)  # Not a string

        # Invalid children
        with self.assertNothingRaised():   ScadObject("Dummy", None, None, [dummy])
        with self.assertRaises(TypeError): ScadObject("Dummy", None, None, dummy)  # Not in a list
        with self.assertRaises(TypeError): ScadObject("Dummy", None, None, [None]) # Invalid value
        with self.assertRaises(TypeError): ScadObject("Dummy", None, None, [0])    # Invalid value
        with self.assertRaises(TypeError): ScadObject("Dummy", None, None, [""])   # Invalid value

    def test_render_value(self):
        # Basic data types: integer, float, string, list
        self.assertEqual(ScadObject.render_value(1              ), "1"        )
        self.assertEqual(ScadObject.render_value(1.1            ), "1.1"      )
        self.assertEqual(ScadObject.render_value("Hello"        ), '"Hello"'  )
        self.assertEqual(ScadObject.render_value([1, 2, 3]      ), "[1, 2, 3]")

        # String escaping
        cr = "\r"
        lf = "\n"
        tab = "\t"
        bs = "\\"  # Single backslash
        dq = '"'   # Double quote
        # Single special characters
        self.assertEqual(ScadObject.render_value(cr) , r'"\r"') # CR  -> "\r"
        self.assertEqual(ScadObject.render_value(lf) , r'"\n"') # LF  -> "\n"
        self.assertEqual(ScadObject.render_value(tab), r'"\t"') # TAB -> "\t"
        self.assertEqual(ScadObject.render_value(dq) , r'"\""') # "   -> "\""
        self.assertEqual(ScadObject.render_value(bs) , r'"\\"') # \   -> "\\"
        # Combinations of special characters; in particular, with backslash
        self.assertEqual(ScadObject.render_value(bs + bs), r'"\\\\"') # \\ -> "\\\\"
        self.assertEqual(ScadObject.render_value(bs + dq), r'"\\\""') # \" -> "\\\""
        self.assertEqual(ScadObject.render_value(dq + bs), r'"\"\\"') # "\ -> "\"\\"

        # Make sure that recursion works, even though it is probably useless
        self.assertEqual(ScadObject.render_value(["a", "b", "c"]), '["a", "b", "c"]')
        self.assertEqual(ScadObject.render_value([["a", "b"], ["c", "d"]]), '[["a", "b"], ["c", "d"]]')


    def test_equality(self):
        # Equal to itself
        self.assertEqualToItself(ScadObject("Cylinder", [11], [("r", 2)], None))

        # Without children
        self.assertEqual   (
            ScadObject("Cylinder", [11], [("r", 2)], None),
            ScadObject("Cylinder", [11], [("r", 2)], None)) # Equal
        self.assertNotEqual(
            ScadObject("Cylinder", [11], [("r", 2)], None),
            ScadObject("Cone"    , [11], [("r", 2)], None)) # Different ID
        self.assertNotEqual(
            ScadObject("Cylinder", [11], [("r", 2)], None),
            ScadObject("Cylinder", [12], [("r", 2)], None)) # Different parameter
        self.assertNotEqual(
            ScadObject("Cylinder", [11], [("r", 2)], None),
            ScadObject("Cylinder", [11], [("d", 2)], None)) # Different keyword parameter key
        self.assertNotEqual(
            ScadObject("Cylinder", [11], [("r", 2)], None),
            ScadObject("Cylinder", [11], [("r", 3)], None)) # Different keyword parameter value
        self.assertNotEqual(
            ScadObject("Cylinder", None, [("h", 11), ("r",  2)], None),
            ScadObject("Cylinder", None, [("r",  3), ("h", 11)], None)) # Different keyword parameter order
        self.assertNotEqual(
            ScadObject("Cylinder", [11], [("r", 2)], None, "foo"),
            ScadObject("Cylinder", [11], [("r", 2)], None, "bar")) # Different comments

        # With children
        self.assertEqual(
            ScadObject("Dummy", [], None, []  ),
            ScadObject("Dummy", [], None, None)) # [] or None
        self.assertEqual(
            ScadObject("Dummy", [], None, [ScadObject("Child", None, None, None)]),
            ScadObject("Dummy", [], None, [ScadObject("Child", None, None, None)])) # Equal child
        self.assertNotEqual(
            ScadObject("Dummy", [], None, []),
            ScadObject("Dummy", [], None, [ScadObject("Child", None, None, None)])) # No child / one child
        self.assertNotEqual(
            ScadObject("Dummy", [], None, [ScadObject("Child", None, None, None)]),
            ScadObject("Dummy", [], None, [ScadObject("Child", None, None, None), ScadObject("Child", None, None, None)])) # One child / two children
        self.assertNotEqual(
            ScadObject("Dummy", [], None, [ScadObject("Child1", None, None, None)]),
            ScadObject("Dummy", [], None, [ScadObject("Child2", None, None, None)])) # Different children

    def test_comment(self):
        o = ScadObject("dummy", [], [], [], "one")

        # Pre-check
        self.assertEqual(o, ScadObject("dummy", [], [], [], "one"))

        # Replace
        self.assertEqual(o.replace_comment("foo"), ScadObject("dummy", [], [], [], "foo"))

        # Clear
        self.assertEqual(o.clear_comment(), ScadObject("dummy", [], [], [], None))

        # Add with default separator
        self.assertEqual(o.comment(prepend = "zero"), ScadObject("dummy", [], [], [], "zero\none"))
        self.assertEqual(o.comment(append  = "two" ), ScadObject("dummy", [], [], [], "one\ntwo"))
        self.assertEqual(o.comment(prepend = "zero", append  = "two"), ScadObject("dummy", [], [], [], "zero\none\ntwo"))

        # Adding None as a comment does not change it
        self.assertEqual(o.comment(prepend = None), ScadObject("dummy", [], [], [], "one"))
        self.assertEqual(o.comment(append  = None), ScadObject("dummy", [], [], [], "one"))

        # Add with non-default separator
        self.assertEqual(o.comment(prepend = "zero", sep = ""), ScadObject("dummy", [], [], [], "zeroone"))
        self.assertEqual(o.comment(append  = "two" , sep = ""), ScadObject("dummy", [], [], [], "onetwo"))
        self.assertEqual(o.comment(prepend = "zero", append  = "two", sep = ""), ScadObject("dummy", [], [], [], "zeroonetwo"))

        # Add (convenience form)
        self.assertEqual(o.comment("zero"), ScadObject("dummy", [], [], [], "zero\none"))

        # Post-check - it's immutable
        self.assertEqual(o, ScadObject("dummy", [], [], [], "one"))

        # If there is no comment in the first place...
        o = ScadObject("dummy", [], [], [], None)

        # ...we can still prepend and append stuff
        self.assertEqual(o.comment(prepend = "zero"), ScadObject("dummy", [], [], [], "zero"))
        self.assertEqual(o.comment(append  = "two" ), ScadObject("dummy", [], [], [], "two"))
        self.assertEqual(o.comment(prepend = "zero", append = "two"), ScadObject("dummy", [], [], [], "zero\ntwo"))

    def test_clear_comment(self):
        both  = ScadObject("a", [], [], [ScadObject("b", [], [], [], "b")], "a")
        inner = ScadObject("a", [], [], [ScadObject("b", [], [], [], "b")])
        none  = ScadObject("a", [], [], [ScadObject("b", [], [], [])])

        self.assertEqual   (both.clear_comment(), inner)
        self.assertNotEqual(both.clear_comment(), none)
        self.assertEqual   (both.clear_comment(recursive=True), none)


    def test_value_rendering(self):
        # Also tests a bit of to_code

        # Valid types
        self.assertEqual(ScadObject("Dummy", [1              ], None, None).to_code(), 'Dummy(1);'        )
        self.assertEqual(ScadObject("Dummy", [1.1            ], None, None).to_code(), 'Dummy(1.1);'      )
        self.assertEqual(ScadObject("Dummy", ["foo"          ], None, None).to_code(), 'Dummy("foo");'    )
        self.assertEqual(ScadObject("Dummy", [[1, 2, 3]      ], None, None).to_code(), 'Dummy([1, 2, 3]);')

        # Invalid values or types
        with self.assertRaises(ValueError): ScadObject("Dummy", [[]       ], None, None).to_code();
        with self.assertRaises(TypeError):  ScadObject("Dummy", [None     ], None, None).to_code();
        with self.assertRaises(TypeError):  ScadObject("Dummy", [(1, 2, 3)], None, None).to_code();
        with self.assertRaises(TypeError):  ScadObject("Dummy", [dict()   ], None, None).to_code();
        with self.assertRaises(TypeError):  ScadObject("Dummy", [set()    ], None, None).to_code();

        # String escaping
        self.assertEqual(ScadObject("Dummy", [r'foobar'        ], None, None).to_code(), r'Dummy("foobar");'    )
        self.assertEqual(ScadObject("Dummy", [r'foo"bar'       ], None, None).to_code(), r'Dummy("foo\"bar");'  )
        self.assertEqual(ScadObject("Dummy", [r'foo\bar'       ], None, None).to_code(), r'Dummy("foo\\bar");'  )

    def test_to_scad(self):
        o = ScadObject("cylinder", [4], [("r", 0.5)], None)

        self.assertEqual(o.to_scad(), o)

    def test_to_code(self):
        sphere   = ScadObject("sphere"  , [0.6]       , None, None)
        cube     = ScadObject("cube"    , [[1, 2, 3]] , None, None)
        cylinder = ScadObject("cylinder", [4], [("r", 0.5)], None)

        union      = ScadObject("union"     , None, None, [sphere, cylinder])
        difference = ScadObject("difference", None, None, [union, cube])

        chain1 = ScadObject("union", None, None, [cube]);
        chain2 = ScadObject("intersection", None, None, [chain1]);

        # Simple object
        self.assertEqual(sphere  .to_code(), "sphere(0.6);"       ) # Basic
        self.assertEqual(cube    .to_code(), "cube([1, 2, 3]);"   ) # List parameter
        self.assertEqual(cylinder.to_code(), "cylinder(4, r = 0.5);") # Multiple parameters

        # Nested CSG
        self.assertEqual(difference.to_code(), "\n".join([
            "difference() {",
            "    union() {",
            "        sphere(0.6);",
            "        cylinder(4, r = 0.5);",
            "    }",
            "    cube([1, 2, 3]);",
            "}"
        ]))

        # Different indents
        self.assertEqual(union.to_code(""), "\n".join([
            "union() {",
            "sphere(0.6);",
            "cylinder(4, r = 0.5);",
            "}"
        ])) # No indent
        self.assertEqual(union.to_code("", "    "), "\n".join([
            "    union() {",
            "    sphere(0.6);",
            "    cylinder(4, r = 0.5);",
            "    }"
        ])) # Top indent only
        self.assertEqual(union.to_code("  ", "    "), "\n".join([
            "    union() {",
            "      sphere(0.6);",
            "      cylinder(4, r = 0.5);",
            "    }"
        ])) # Indent and top indent

        # Inline
        self.assertEqual(union.to_code(inline = True), "union() { sphere(0.6); cylinder(4, r = 0.5); }")

        # With comments
        sphere_with_comment = ScadObject("sphere", [1], None, None, "A sphere!")
        union_with_comment  = ScadObject("union", None, None, [sphere_with_comment], "A union!\nIt can contain multiple objects.")
        self.assertEqual(sphere_with_comment.to_code(" ", "  "), "\n".join([
            "  // A sphere!",
            "  sphere(1);",
        ]))
        self.assertEqual(union_with_comment.to_code(" ", "  "), "\n".join([
            "  // A union!",
            "  // It can contain multiple objects.",
            "  union() {",
            "   // A sphere!",
            "   sphere(1);",
            "  }"
        ]))
        self.assertEqual(sphere_with_comment.to_code(inline = True), "sphere(1);")

        # Simplify
        self.assertEqual(chain2.to_code(inline = True                 ), "intersection() { union() { cube([1, 2, 3]); } }")
        self.assertEqual(chain2.to_code(inline = True, simplify = True), "intersection() union() cube([1, 2, 3]);")


    def test_to_code_empty(self):
        sphere   = ScadObject("sphere"  , [0.6]       , None, None)
        cube     = ScadObject("cube"    , [[1, 2, 3]] , None, None)

        # Empty SCAD object
        empty_comment = ScadObject(None, None, None, None)
        self.assertEqual(empty_comment.to_code(), "\n".join([
            ";",
        ]))

        # Empty SCAD object with comment
        empty_comment = ScadObject(None, None, None, None).comment("Empty")
        self.assertEqual(empty_comment.to_code(), "\n".join([
            "// Empty",
            ";",
        ]))

        # Empty SCAD object with children
        empty_children = ScadObject(None, None, None, [sphere, cube])
        self.assertEqual(empty_children.to_code(), "\n".join([
            "{",
            "    sphere(0.6);",
            "    cube([1, 2, 3]);",
            "}",
        ]))

        # Empty SCAD object with children and comment
        empty_children_comment = ScadObject(None, None, None, [sphere, cube]).comment("Empty")
        self.assertEqual(empty_children_comment.to_code(), "\n".join([
            "// Empty",
            "{",
            "    sphere(0.6);",
            "    cube([1, 2, 3]);",
            "}",
        ]))

    def test_repr(self):
        self.assertRepr(ScadObject("foo", [1, 2], [('a', 3), ('b', 4)], [ScadObject("c1", [], [], []), ScadObject("c2", None, None, None)]),
            "ScadObject('foo', [1, 2], [('a', 3), ('b', 4)], [ScadObject('c1', [], [], []), ScadObject('c2', [], [], [])])")

    def test_to_tree(self):
        sphere   = ScadObject("sphere"  , [0.6]       , None, None)
        cube     = ScadObject("cube"    , [[1, 2, 3]] , None, None)
        cylinder = ScadObject("cylinder", [4], [("r", 0.5)], None)

        union      = ScadObject("union"     , None, None, [sphere, cylinder])
        difference = ScadObject("difference", None, None, [union, cube])

        self.assertEqual(difference.to_tree(),
            Node("difference()", [
                Node("union()", [
                    Node("sphere(0.6)"),
                    Node("cylinder(4, r = 0.5)"),
                ]),
                Node("cube([1, 2, 3])"),
            ]))

    def test_render_to_file(self):
        part = Sphere(0.6) + Cube([1, 2, 3]) - Cylinder([0, 0, 1], 4, r=0.5)

        expected_file_name = os.path.join(os.path.dirname(__file__), "test_scad_object_render_to_file_expected.scad")
        actual_file_name   = os.path.join(os.path.dirname(__file__), "test_scad_object_render_to_file_actual.scad")

        self.assertTrue(os.path.isfile(expected_file_name))
        self.assertFalse(os.path.exists(actual_file_name))

        try:
            render_to_file(part, actual_file_name, fn=60)
            with open(actual_file_name) as actual_file:
                actual = actual_file.read()
            with open(expected_file_name) as expected_file:
                expected = expected_file.read()

            self.assertNotEqual(expected, "")
            self.assertEqual(actual, expected)
        finally:
            if os.path.exists(actual_file_name):
                os.unlink(actual_file_name)
