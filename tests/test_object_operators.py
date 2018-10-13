from cadlib.csg.intersection import Intersection
from cadlib.csg.difference import Difference
from cadlib.csg.union import Union
from cadlib.object.transformed import Transformed
from cadlib.object.primitives import Sphere, Cube, Cylinder
from cadlib.transform.primitives.translate import Translate
from tests.unit_test import TestCase

class TestOperators(TestCase):
    def test_union(self):
        a = Sphere(2)
        b = Cube([10, 10, 10])
        c = Cylinder(5, 5)
        d = Cube(20)

        self.assertEqual(   a +  b                 , Union([a, b      ]))
        self.assertEqual(   c +  c                 , Union([c, c      ]))
        self.assertEqual(  (a +  b) + c            , Union([a, b, c   ]))
        self.assertEqual(   a + (b  + c)           , Union([a, b, c   ]))
        self.assertEqual(    a  +  b  +  c  + d    , Union([a, b, c, d]))
        self.assertEqual(  ((a  +  b) +  c) + d    , Union([a, b, c, d]))
        self.assertEqual(    a  + (b  + (c  + d))  , Union([a, b, c, d]))
        self.assertEqual(   (a  +  b) + (c  + d)   , Union([a, b, c, d]))

    def test_intersection(self):
        a = Sphere(2)
        b = Cube([10, 10, 10])
        c = Cylinder(5, 5)
        d = Cube(20)

        self.assertEqual(    a  *  b               , Intersection([a, b      ]))
        self.assertEqual(    c  *  c               , Intersection([c, c      ]))
        self.assertEqual(   (a  *  b) * c          , Intersection([a, b, c   ]))
        self.assertEqual(    a  * (b  * c)         , Intersection([a, b, c   ]))
        self.assertEqual(    a  *  b  *  c  * d    , Intersection([a, b, c, d]))
        self.assertEqual(  ((a  *  b) *  c) * d    , Intersection([a, b, c, d]))
        self.assertEqual(    a  * (b  * (c  * d))  , Intersection([a, b, c, d]))
        self.assertEqual(   (a  *  b) * (c  * d)   , Intersection([a, b, c, d]))

    def test_difference(self):
        a = Sphere(2)
        b = Cube([10, 10, 10])
        c = Cylinder(5, 5)
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

    def test_intersection_and_transform(self):
        a = Sphere(2)
        b = Cube(3)
        t = Translate([0, 0, 0])

        self.assertEqual( t * (a  * b), Transformed(t, Intersection([a, b])))
        self.assertEqual((t *  a) * b , Intersection([Transformed(t, a), b]))
