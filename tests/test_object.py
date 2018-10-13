from cadlib.object.transformed import Transformed
from cadlib.object.primitives import Sphere, Cube, Cylinder
from cadlib.transform.chained import Chained
from cadlib.transform.primitives.translate import Translate
from cadlib.transform.primitives.scale import Scale
from cadlib.transform.primitives.rotate_xyz import RotateXyz
from cadlib.scad.scad import ScadObject
from tests.unit_test import TestCase

# Operations with objects are tested in test_csg.py

class TestObject(TestCase):
    def test_construction(self):
        # Primitives
        sphere = Sphere(11)
        cube1 = Cube(11)
        cube2 = Cube([11, 22, 33])
        with self.assertRaises(ValueError): Cube([])       # Empty size
        with self.assertRaises(ValueError): Cube([11, 22]) # Wrong-size size
        cylinder = Cylinder(11, 22)

        # Transformed object
        t = Translate([10, 20, 30])
        Transformed(t, cube1)
        with self.assertRaises(TypeError): Transformed(t, t)
        with self.assertRaises(TypeError): Transformed(cube1, cube1)
        with self.assertRaises(TypeError): Transformed(t, None)
        with self.assertRaises(TypeError): Transformed(None, cube1)

    def test_equality(self):
        self.assertEqualToItself(Sphere(11)) # Same object
        self.assertEqual        (Sphere(11), Sphere(11)) # Equal object
        self.assertNotEqual     (Sphere(11), Sphere(22)) # Different objects

        # Parameters can be specified in different ways, leading to equal objects if they have the same SCAD
        # representation.
        self.assertEqual(Cube(11), Cube([11, 11, 11]))

        # Objects of different class are not equal
        self.assertNotEqual(Cube(11), Sphere(11))

        # Transformed object
        r  = RotateXyz(60, 30, 15)
        r2 = RotateXyz(60, 30, 15)
        t  = Translate([60, 30, 15])
        sphere = Sphere(11)
        cube1 = Cube(11)
        cube2 = Cube(11)
        self.assertEqual   (Transformed(r, cube1), Transformed(r , cube2))  # Equal objects
        self.assertEqual   (Transformed(r, cube1), Transformed(r2, cube1))  # Equal transform
        self.assertNotEqual(Transformed(r, cube1), cube1)                  # Transformed / original
        self.assertNotEqual(Transformed(r, cube1), Transformed(t, cube1))  # Different transform
        self.assertNotEqual(Transformed(r, cube1), Transformed(r, sphere)) # Different objects

    def test_multiplication_with_transform(self):
        r = RotateXyz(60, 30, 15)
        s = Scale([1, 2, -1])
        cube = Cube(11)

        # Simple transform
        self.assertEqual(r * cube, Transformed(r, cube))

        # Wrong order
        with self.assertRaises(TypeError): cube * r

        # Multiple transform
        self.assertEqual(  (r *  s) * cube   , Transformed(Chained([r, s]), cube))
        self.assertEqual(   r * (s  * cube)  , Transformed(Chained([r, s]), cube))

    def test_to_scad(self):
        # Primitives
        self.assertEqual(Cube    (11          ).to_scad(), ScadObject("cube"    , [[11, 11, 11]], None      , None))
        self.assertEqual(Cube    ([11, 22, 33]).to_scad(), ScadObject("cube"    , [[11, 22, 33]], None      , None))
        self.assertEqual(Sphere  (11          ).to_scad(), ScadObject("sphere"  , [11]          , None      , None))
        self.assertEqual(Cylinder(11, 4       ).to_scad(), ScadObject("cylinder", [11]          , [('r', 4)], None))

        r = RotateXyz(60, 30, 15)
        s = Scale([1, 2, -1])
        cube = Cube(11)

        # Simple transform
        self.assertEqual(Transformed(r, cube).to_scad(),
            ScadObject("rotate", [[60, 30, 15]], None, [
                ScadObject("cube", [[11, 11, 11]], None, None),
            ])
        )

        # Chained transform
        self.assertEqual(Transformed(Chained([r, s]), cube).to_scad(),
            ScadObject("rotate", [[60, 30, 15]], None, [
                ScadObject("scale", [[1, 2, -1]], None, [
                    ScadObject("cube", [[11, 11, 11]], None, None),
                ])
            ])
        )

    def test_to_scad_code(self):
        # Primitives
        self.assertScadCode(Cube    (11          ), "cube([11, 11, 11]);")
        self.assertScadCode(Cube    (11          ), "cube([11, 11, 11]);")
        self.assertScadCode(Cube    ([11, 22, 33]), "cube([11, 22, 33]);")
        self.assertScadCode(Sphere  (11          ), "sphere(11);")
        self.assertScadCode(Cylinder(11, 4       ), "cylinder(11, r = 4);")

    def test_postfix_transform(self):
        cube = Cube(11)

        # Vectors
        rv = [60, 34, 30]
        sv = [ 2,  1,  1]
        tv = [10, 20, 30]

        # Transforms
        r = RotateXyz(*rv)
        s = Scale    (sv)
        t = Translate(tv)

        # Long shortcuts
        self.assertEqual(cube.rotate   (xyz = rv).scale(sv)   .translate(tv), t * s * r * cube)
        self.assertEqual(cube.transform(r)       .scale(sv)   .transform(t) , t * s * r * cube)
        self.assertEqual(cube.rotate   (xyz = rv).transform(s).translate(tv), t * s * r * cube)
        self.assertEqual(cube.transform(s * r)   .transform(t)              , t * s * r * cube)

        # Error
        with self.assertRaises(TypeError): cube.transform(cube)

    def test_transform_shortcuts(self):
        cube = Cube(11)

        self.assertEqual(cube.up(10), Translate([0, 0, 10]) * cube)
