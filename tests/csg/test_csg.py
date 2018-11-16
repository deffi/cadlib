from cadlib.object.primitives import Sphere, Cuboid, Frustum
from cadlib.csg import Csg, Intersection, Difference, Union
from cadlib.scad import ScadObject
from cadlib.util.vector import Z, origin
from tests.unit_test import TestCase

class TestCsg(TestCase):
    def test_construction(self):
        sphere   = Sphere(11)
        cube     = Cuboid(22)
        cylinder = Frustum(origin, Z, 11, 11)
        object_list = [sphere, cube, cylinder]

        # Empty
        Csg([])

        # With objects
        self.assertEqual(Csg(object_list).children, object_list)

        # With generator
        self.assertEqual(Csg(o for o in object_list).children, object_list)

        # With invalid objects
        with self.assertRaises(TypeError): Csg(None)           # None instead of empty list
        with self.assertRaises(TypeError): Csg([Sphere])       # Class instead of object
        with self.assertRaises(TypeError): Csg(sphere)         # Object instead of list
        with self.assertRaises(TypeError): Csg([None])         # List with invalid value
        with self.assertRaises(TypeError): Csg([sphere, None]) # List with object and invalid value

    def test_equality(self):
        sphere   = Sphere(11)
        cube     = Cuboid(22)
        cylinder = Frustum(origin, Z, 11, 11)
        objects = [sphere, cube, cylinder]

        # Different types of CSG are not equal, even if their children are identical
        self.assertNotEqual(Union       (objects), Intersection(objects))
        self.assertNotEqual(Intersection(objects), Difference  (objects))
        self.assertNotEqual(Difference  (objects), Union       (objects))

    def test_to_scad(self):
        sphere   = Sphere(2)
        cube     = Cuboid(10)
        cylinder = Frustum(origin, Z, 5, 5)

        mixed = Union([Intersection([sphere, cylinder]), Difference([cube, sphere])])
        self.assertEqual(mixed.to_scad(), ScadObject("union", None, None, [
            ScadObject("intersection", None, None, [ sphere  .to_scad(), cylinder.to_scad() ]),
            ScadObject("difference"  , None, None, [ cube    .to_scad(), sphere  .to_scad() ]),
        ]))
