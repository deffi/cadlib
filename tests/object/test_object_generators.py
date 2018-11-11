from cadlib.object.generators import *
from cadlib.object.generators import _get_radius, _get_radii
from cadlib.object.primitives import Cuboid, Frustum, Plane, Slice, Sphere
from cadlib.util import Vector, X, Y, Z
from tests.unit_test import TestCase

class TestObjectGenerators(TestCase):
    def test_get_radius_helper(self):
        self.assertEqual(_get_radius(r=1   , d=None), 1)
        self.assertEqual(_get_radius(r=None, d=4   ), 2)

        with self.assertRaises(ValueError): _get_radius(r=None, d=None)
        with self.assertRaises(ValueError): _get_radius(r=1   , d=4   )

    def test_get_radii_helper(self):
        # TODO implement
        pass
        # self.assertEqual(_get_radius(r=1   , d=None), 1)
        # self.assertEqual(_get_radius(r=None, d=4   ), 2)
        #
        # with self.assertRaises(ValueError): _get_radius(r=None, d=None)
        # with self.assertRaises(ValueError): _get_radius(r=1   , d=4   )


    def test_cuboid_generators(self):
        self.assertEqual(cuboid(1), Cuboid(1))
        self.assertEqual(cuboid([1, 2, 3]), Cuboid([1, 2, 3]))
        self.assertEqual(cuboid(1, 2, 3), Cuboid([1, 2, 3]))
        self.assertEqual(cube(1), Cuboid([1, 1, 1]))
        with self.assertRaises(ValueError): cuboid(1, 2)
        with self.assertRaises(ValueError): cuboid(1, 2, None)
        with self.assertRaises(ValueError): cuboid(1, None, 2)

    def test_frustum_generators(self):
        # Cylinder - base/cap
        self.assertEqual(cylinder(X, Y,     2), Frustum(X, Y, 2, 2))
        self.assertEqual(cylinder(X, Y, r = 2), Frustum(X, Y, 2, 2))
        self.assertEqual(cylinder(X, Y, d = 4), Frustum(X, Y, 2, 2))
        self.assertEqual(cylinder(0, Y,     2), Frustum(0, Y, 2, 2)) # 0 is allowed as base
        # 0 is not allowed as cap because it would be interpreted as
        # direction/length

        # Cylinder - direction/length
        self.assertEqual(cylinder(X, 1,     2), Frustum(0, X, 2, 2))
        self.assertEqual(cylinder(X, 1, r = 2), Frustum(0, X, 2, 2))
        self.assertEqual(cylinder(X, 1, d = 4), Frustum(0, X, 2, 2))

        # Cylinder - invalid
        with self.assertRaises(TypeError) : cylinder(5              , 5, 1)    # First is not a vector
        with self.assertRaises(TypeError) : cylinder(X              , "", 1)   # Second is not a vector or number
        with self.assertRaises(ValueError): cylinder(X              , 5)       # Radius missing
        with self.assertRaises(ValueError): cylinder(X              , 5, 1, 1) # Radius and diameter
        with self.assertRaises(ValueError): cylinder(Vector(0, 0, 0), 5)       # Zero vector is not allowed as direction

        # Cone - base/cap
        self.assertEqual(cone(X, Y,     2), Frustum(X, Y, 2, 0))
        self.assertEqual(cone(X, Y, r = 2), Frustum(X, Y, 2, 0))
        self.assertEqual(cone(X, Y, d = 4), Frustum(X, Y, 2, 0))

        # Cone - direction/length
        self.assertEqual(cone(X, 1,     2), Frustum(0, X, 2, 0))
        self.assertEqual(cone(X, 1, r = 2), Frustum(0, X, 2, 0))
        self.assertEqual(cone(X, 1, d = 4), Frustum(0, X, 2, 0))

        # Frustum - base/cap
        self.assertEqual(frustum(X, Y,     (2, 3)), Frustum(X, Y, 2, 3))
        self.assertEqual(frustum(X, Y, r = (2, 3)), Frustum(X, Y, 2, 3))
        self.assertEqual(frustum(X, Y, d = (4, 6)), Frustum(X, Y, 2, 3))

        # Frustum - direction/length
        self.assertEqual(frustum(X, 1,     (2, 3)), Frustum(0, X, 2, 3))
        self.assertEqual(frustum(X, 1, r = (2, 3)), Frustum(0, X, 2, 3))
        self.assertEqual(frustum(X, 1, d = (4, 6)), Frustum(0, X, 2, 3))

    def test_sphere_generators(self):
        self.assertEqual(sphere(2), Sphere(2))
        self.assertEqual(sphere(r = 2), Sphere(r = 2))
        self.assertEqual(sphere(d = 2), Sphere(d = 2))

    def test_plane_generators(self):
        self.assertEqual(plane(X, 1), Plane(X, 1))

    def test_slice_generators(self):
        self.assertEqual(slice(X, 1, 2), Slice(X, 1, 2))
