from cadlib.object.primitives import Sphere, Cube, Cylinder
from cadlib.csg import Intersection, Difference, Union
from cadlib.scad import ScadObject
from cadlib.util.vector import Z
from tests.unit_test import TestCase

class TestCsg(TestCase):
    def test_construction(self):
        sphere   = Sphere(11)
        cube     = Cube([11, 22, 33])
        cylinder = Cylinder(Z, 11, 22)
        object_list = [sphere, cube, cylinder]

        # Empty
        Union([])
        Intersection([])
        Difference([])

        # Explicitly empty CSG
        self.assertEqual(Union       .empty(), Union       ([]))
        self.assertEqual(Intersection.empty(), Intersection([]))
        self.assertEqual(Difference  .empty(), Difference  ([]))

        # With objects
        self.assertEqual(Union       (object_list).children, object_list)
        self.assertEqual(Intersection(object_list).children, object_list)
        self.assertEqual(Difference  (object_list).children, object_list)

        # With generator
        self.assertEqual(Union       (o for o in object_list), Union       (object_list))
        self.assertEqual(Intersection(o for o in object_list), Intersection(object_list))
        self.assertEqual(Difference  (o for o in object_list), Difference  (object_list))

        # With invalid objects
        with self.assertRaises(TypeError): Union(None)           # None instead of empty list
        with self.assertRaises(TypeError): Union(sphere)         # Object instead of list
        with self.assertRaises(TypeError): Union([None])         # List with invalid value
        with self.assertRaises(TypeError): Union([Sphere, None]) # List with object and invalid value


    def test_equality(self):
        sphere   = Sphere(11)
        cube     = Cube([11, 22, 33])
        cylinder = Cylinder(Z, 11, 22)

        # A CSG objects is equal to itself
        self.assertEqualToItself(Union       ([]))
        self.assertEqualToItself(Intersection([]))
        self.assertEqualToItself(Difference  ([]))
        self.assertEqualToItself(Union       ([sphere, cube, cylinder]))
        self.assertEqualToItself(Intersection([sphere, cube, cylinder]))
        self.assertEqualToItself(Difference  ([sphere, cube, cylinder]))

        # Same-type CSG objects are equal if their children are equal
        self.assertEqual(Union       ([]), Union       ([]))
        self.assertEqual(Intersection([]), Intersection([]))
        self.assertEqual(Difference  ([]), Difference  ([]))
        self.assertEqual(Union       ([sphere, cube, cylinder]), Union       ([sphere, cube, cylinder]))
        self.assertEqual(Intersection([sphere, cube, cylinder]), Intersection([sphere, cube, cylinder]))
        self.assertEqual(Difference  ([sphere, cube, cylinder]), Difference  ([sphere, cube, cylinder]))

        # CSG objects are not equal if their children are different
        self.assertNotEqual(Union       ([sphere, cube, cylinder]), Union       ([sphere, cube]))
        self.assertNotEqual(Intersection([sphere, cube, cylinder]), Intersection([sphere, cube]))
        self.assertNotEqual(Difference  ([sphere, cube, cylinder]), Difference  ([sphere, cube]))

        # CSG objects are not equal if their children are in different order (!)
        self.assertNotEqual(Union       ([cube, sphere]), Union       ([sphere, cube]))
        self.assertNotEqual(Intersection([cube, sphere]), Intersection([sphere, cube]))
        self.assertNotEqual(Difference  ([cube, sphere]), Difference  ([sphere, cube]))

        # Different types of CSG are not equal
        self.assertNotEqual(Union       ([cube, sphere]), Intersection([sphere, cube]))
        self.assertNotEqual(Intersection([cube, sphere]), Difference  ([sphere, cube]))
        self.assertNotEqual(Difference  ([cube, sphere]), Union       ([sphere, cube]))

    def test_to_scad(self):
        sphere   = Sphere(2)
        cube     = Cube([10, 10, 10])
        cylinder = Cylinder(Z, 5, 5)

        self.assertEqual(Union([sphere, cube, cylinder]).to_scad(), ScadObject("union", None, None, [
            sphere  .to_scad(),
            cube    .to_scad(),
            cylinder.to_scad(),
        ]))
        self.assertEqual(Intersection([sphere, cube, cylinder]).to_scad(), ScadObject("intersection", None, None, [
            sphere  .to_scad(),
            cube    .to_scad(),
            cylinder.to_scad(),
        ]))
        self.assertEqual(Difference([sphere, cube, cylinder]).to_scad(), ScadObject("difference", None, None, [
            sphere  .to_scad(),
            cube    .to_scad(),
            cylinder.to_scad(),
        ]))

        mixed = Union([Intersection([sphere, cylinder]), Difference([cube, sphere])])
        self.assertEqual(mixed.to_scad(), ScadObject("union", None, None, [
            ScadObject("intersection", None, None, [ sphere  .to_scad(), cylinder.to_scad() ]),
            ScadObject("difference"  , None, None, [ cube    .to_scad(), sphere  .to_scad() ]),
        ]))

    def test_sum(self):
        sphere   = Sphere(2)
        cube     = Cube([10, 10, 10])
        cylinder = Cylinder(Z, 5, 5)

        objects = [sphere, cube, cylinder]

        self.assertEqual(sum(objects, Union.empty()), Union(objects))