from cadlib.object.transformed import Transformed
from cadlib.object.primitives import Sphere, Cube, Cylinder
from cadlib.transform.chained import Chained
from cadlib.transform.primitives.translate import Translate
from cadlib.transform.primitives.scale import Scale
from cadlib.transform.primitives.rotate_xyz import RotateXyz
from cadlib.util.vector import Z
from tests.unit_test import TestCase
from cadlib.csg.intersection import Intersection
from cadlib.csg.difference import Difference
from cadlib.csg.union import Union

class TestObject(TestCase):
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

    def test_addition(self):
        a = Sphere(2)
        b = Cube([10, 10, 10])
        c = Cylinder(Z, 5, 5)
        d = Cube(20)

        self.assertEqual(   a +  b                 , Union([a, b      ]))
        self.assertEqual(   c +  c                 , Union([c, c      ]))
        self.assertEqual(  (a +  b) + c            , Union([a, b, c   ]))
        self.assertEqual(   a + (b  + c)           , Union([a, b, c   ]))
        self.assertEqual(    a  +  b  +  c  + d    , Union([a, b, c, d]))
        self.assertEqual(  ((a  +  b) +  c) + d    , Union([a, b, c, d]))
        self.assertEqual(    a  + (b  + (c  + d))  , Union([a, b, c, d]))
        self.assertEqual(   (a  +  b) + (c  + d)   , Union([a, b, c, d]))

    def test_multiplication(self):
        a = Sphere(2)
        b = Cube([10, 10, 10])
        c = Cylinder(Z, 5, 5)
        d = Cube(20)

        self.assertEqual(    a  *  b               , Intersection([a, b      ]))
        self.assertEqual(    c  *  c               , Intersection([c, c      ]))
        self.assertEqual(   (a  *  b) * c          , Intersection([a, b, c   ]))
        self.assertEqual(    a  * (b  * c)         , Intersection([a, b, c   ]))
        self.assertEqual(    a  *  b  *  c  * d    , Intersection([a, b, c, d]))
        self.assertEqual(  ((a  *  b) *  c) * d    , Intersection([a, b, c, d]))
        self.assertEqual(    a  * (b  * (c  * d))  , Intersection([a, b, c, d]))
        self.assertEqual(   (a  *  b) * (c  * d)   , Intersection([a, b, c, d]))

    def test_subtractino(self):
        a = Sphere(2)
        b = Cube([10, 10, 10])
        c = Cylinder(Z, 5, 5)
        d = Cube(20)

        self.assertEqual(    a  -  b               , Difference([a, b      ]))
        self.assertEqual(    c  -  c               , Difference([c, c      ]))
        self.assertEqual(   (a  -  b) - c          , Difference([a, b, c   ]))
        self.assertEqual(    a  - (b  - c)         , Difference([a, Difference([b, c])]))
        self.assertEqual(    a  -  b  -  c  - d    , Difference([a, b, c, d]))
        self.assertEqual(  ((a  -  b) -  c) - d    , Difference([a, b, c, d]))
        self.assertEqual(    a  - (b  - (c  - d))  , Difference([a, Difference([b, Difference([c, d])])]))
        self.assertEqual(   (a  -  b) - (c  - d)   , Difference([Difference([a, b]), Difference([c, d])]))

    def test_invalid_operations(self):
        a = Sphere(2)

        for invalid in [None, 0, 0.0, ""]:
            with self.assertRaises(TypeError): a + invalid
            with self.assertRaises(TypeError): a - invalid
            with self.assertRaises(TypeError): a * invalid
            with self.assertRaises(TypeError): invalid + a
            with self.assertRaises(TypeError): invalid - a
            with self.assertRaises(TypeError): invalid * a

    def test_operators_with_transforms(self):
        a = Sphere(2)
        t = Translate([0, 0, 0])

        # The only operation we can do with a Transform is Transform*Object, which results in a Transformed Object.
        with self.assertRaises(TypeError): a + t
        with self.assertRaises(TypeError): a - t
        with self.assertRaises(TypeError): a * t
        with self.assertRaises(TypeError): t + a
        with self.assertRaises(TypeError): t - a
        self.assertEqual(t * a, Transformed(t, a))

    def test_multiplication_with_object_and_transform(self):
        # Multiplication is used for both intersection (Object * Object) and transform (Transform * Object)
        a = Sphere(2)
        b = Cube(3)
        t = Translate([0, 0, 0])

        self.assertEqual( t * (a  * b), Transformed(t, Intersection([a, b])))
        self.assertEqual((t *  a) * b , Intersection([Transformed(t, a), b]))
