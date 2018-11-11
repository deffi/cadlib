from cadlib.object.generators import *
from cadlib.object.primitives import Cuboid, Frustum, Plane, Slice, Sphere
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
        # Cylinder
        self.assertEqual(cylinder(X, Y, r = 2), Frustum(X, Y, 2, 2)) # Base, cap, radius
        self.assertEqual(cylinder(X, Y, d = 4), Frustum(X, Y, 2, 2)) # Base, cap, diameter
        self.assertEqual(cylinder(X, 1, r = 2), Frustum(0, X, 2, 2)) # Direction, length, radius

        # Cone
        self.assertEqual(cone(X, Y, r = 2), Frustum(X, Y, 2, 0)) # Base, cap, radius
        self.assertEqual(cone(X, Y, d = 4), Frustum(X, Y, 2, 0)) # Base, cap, diameter
        self.assertEqual(cone(X, 1, r = 2), Frustum(0, X, 2, 0)) # Direction, length, radius

        # Frustum
        self.assertEqual(frustum(X, Y, r = (2, 3)), Frustum(X, Y, 2, 3)) # Base, cap, radius
        self.assertEqual(frustum(X, Y, d = (4, 6)), Frustum(X, Y, 2, 3)) # Base, cap, diameter
        self.assertEqual(frustum(X, 1, r = (2, 3)), Frustum(0, X, 2, 3)) # Direction, length, radius

    def test_sphere_generators(self):
        self.assertEqual(sphere(2), Sphere(2))
        self.assertEqual(sphere(r = 2), Sphere(r = 2))
        self.assertEqual(sphere(d = 2), Sphere(d = 2))

    def test_plane_generators(self):
        self.assertEqual(plane(X, 1), Plane(X, 1))

    def test_slice_generators(self):
        self.assertEqual(slice(X, 1, 2), Slice(X, 1, 2))
