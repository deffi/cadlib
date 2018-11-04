from cadlib.csg import Union, Intersection, Difference
from cadlib.csg.generators import *
from cadlib.object.primitives import Sphere, Cuboid, Cylinder
from cadlib.util import Vector, X, Y, Z
from tests.unit_test import TestCase

class TestTransformGenerators(TestCase):
    def test_csg_generators(self):
        sphere   = Sphere(11)
        cuboid   = Cuboid([11, 22, 33])
        cylinder = Cylinder(Z, 11, 22)
        object_list = [sphere, cuboid, cylinder]

        self.assertEqual(union       (object_list), Union       (object_list))
        self.assertEqual(difference  (object_list), Difference  (object_list))
        self.assertEqual(intersection(object_list), Intersection(object_list))

    def test_empty(self):
        self.assertEqual(union       (), Union       ([]))
        self.assertEqual(difference  (), Difference  ([]))
        self.assertEqual(intersection(), Intersection([]))
