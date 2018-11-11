from cadlib.object.generators import *
from cadlib.object.primitives import Cuboid, Cylinder, Plane, Slice, Sphere
from cadlib.util import Vector, X, Y, Z
from tests.unit_test import TestCase

class TestObjectGenerators(TestCase):
    def test_cuboid_generators(self):
        self.assertEqual(cuboid(1), Cuboid(1))
        self.assertEqual(cuboid([1, 2, 3]), Cuboid([1, 2, 3]))
        self.assertEqual(cuboid(1, 2, 3), Cuboid([1, 2, 3]))
        self.assertEqual(cube(1), Cuboid([1, 1, 1]))
        with self.assertRaises(ValueError): cuboid(1, 2)
        with self.assertRaises(ValueError): cuboid(1, 2, None)
        with self.assertRaises(ValueError): cuboid(1, None, 2)

    def test_frustum_generators(self):
        pass


    def test_cylinder_generators(self):
        self.assertEqual(cylinder(X, Y, r = 2), Cylinder(X, Y, r = 2))
        self.assertEqual(cylinder(X, 1, d = 3), Cylinder(X, 1, d = 3))

    def test_sphere_generators(self):
        self.assertEqual(sphere(2), Sphere(2))
        self.assertEqual(sphere(r = 2), Sphere(r = 2))
        self.assertEqual(sphere(d = 2), Sphere(d = 2))

    def test_plane_generators(self):
        self.assertEqual(plane(X, 1), Plane(X, 1))

    def test_slice_generators(self):
        self.assertEqual(slice(X, 1, 2), Slice(X, 1, 2))
