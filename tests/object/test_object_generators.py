from cadlib.object.generators import *
from cadlib.object.generators import _get_radius, _get_radii
from cadlib.object.primitives import Cuboid, Frustum, Plane, Layer, Sphere
from cadlib.util import Vector, X, Y, Z, origin
from tests.unit_test import TestCase

class TestObjectGenerators(TestCase):
    def test_get_radius_helper(self):
        self.assertEqual(_get_radius(r=1   , d=None), 1)
        self.assertEqual(_get_radius(r=None, d=4   ), 2)

        with self.assertRaises(ValueError): _get_radius(r=None, d=None)
        with self.assertRaises(ValueError): _get_radius(r=1   , d=4   )

    def test_get_radii_helper(self):
        self.assertEqual(_get_radii(r=(1, 2)  , d=None  ), (1, 2))
        self.assertEqual(_get_radii(r=None    , d=(4, 6)), (2, 3))

        self.assertEqual(_get_radii(r=[1, 2]  , d=None  ), (1, 2))
        self.assertEqual(_get_radii(r=None    , d=[4, 6]), (2, 3))

        with self.assertRaises(TypeError): _get_radii(r="xy")
        with self.assertRaises(TypeError): _get_radii(d="xy")

        with self.assertRaises(ValueError): _get_radii(r=None  , d=None  )
        with self.assertRaises(ValueError): _get_radii(r=(1, 2), d=(4, 6))

        with self.assertRaises(ValueError): _get_radii(r=(1, 2, 3), d=None     )
        with self.assertRaises(ValueError): _get_radii(r=None     , d=(4, 6, 8))

        with self.assertRaises(TypeError): _get_radii(r=1     , d=None  )
        with self.assertRaises(TypeError): _get_radii(r=None  , d=4     )


    def test_cuboid_generators(self):
        self.assertEqual(cuboid(1)              , Cuboid(1, 1, 1))
        self.assertEqual(cuboid(1, 2, 3)        , Cuboid(1, 2, 3))
        self.assertEqual(cuboid([1, 2, 3])      , Cuboid(1, 2, 3))
        self.assertEqual(cuboid((1, 2, 3))      , Cuboid(1, 2, 3))
        self.assertEqual(cuboid(Vector(1, 2, 3)), Cuboid(1, 2, 3))

        self.assertEqual(cube(1), Cuboid(1, 1, 1))

        with self.assertRaises(ValueError): cuboid(1, 2)
        with self.assertRaises(ValueError): cuboid(None)
        with self.assertRaises(ValueError): cuboid("1")
        with self.assertRaises(ValueError): cuboid(1, 2, None)
        with self.assertRaises(ValueError): cuboid(1, None, 2)
        with self.assertRaises(TypeError) : cuboid(1, 2, "3")

    def test_frustum_generators(self):
        v0 = Vector (0, 0, 0)

        # Cylinder - base/cap
        self.assertEqual(cylinder(X     , Y,     2), Frustum(X     , Y, 2, 2))
        self.assertEqual(cylinder(X     , Y, r = 2), Frustum(X     , Y, 2, 2))
        self.assertEqual(cylinder(X     , Y, d = 4), Frustum(X     , Y, 2, 2))
        self.assertEqual(cylinder(origin, Y,     2), Frustum(origin, Y, 2, 2)) # 0 is allowed as base
        # 0 is not allowed as cap because it would be interpreted as
        # direction/length

        # Cylinder - direction/length
        self.assertEqual(cylinder(X, 1,     2), Frustum(origin, X, 2, 2))
        self.assertEqual(cylinder(X, 1, r = 2), Frustum(origin, X, 2, 2))
        self.assertEqual(cylinder(X, 1, d = 4), Frustum(origin, X, 2, 2))

        # Cylinder - invalid
        with self.assertNothingRaised()   : cylinder(X , 5 , 1)        # Reference
        with self.assertRaises(TypeError) : cylinder(5 , 5 , 1)        # First is not a vector
        with self.assertRaises(TypeError) : cylinder(X , "", 1)        # Second is not a vector or number
        with self.assertRaises(ValueError): cylinder(X , 5    )        # Neither radius nor diameter
        with self.assertRaises(ValueError): cylinder(X , 5 , 1, 1)     # Both radius and diameter
        with self.assertRaises(ValueError): cylinder(v0, 5 , 1)        # Zero vector is not allowed as direction
        with self.assertRaises(TypeError) : cylinder(X , 5 , r=(1, 2)) # Radii
        with self.assertRaises(TypeError) : cylinder(X , 5 , d=(1, 2)) # Diameters

        # Cone - base/cap
        self.assertEqual(cone(X, Y,     2), Frustum(X, Y, 2, 0))
        self.assertEqual(cone(X, Y, r = 2), Frustum(X, Y, 2, 0))
        self.assertEqual(cone(X, Y, d = 4), Frustum(X, Y, 2, 0))

        # Cone - direction/length
        self.assertEqual(cone(X, 1,     2), Frustum(origin, X, 2, 0))
        self.assertEqual(cone(X, 1, r = 2), Frustum(origin, X, 2, 0))
        self.assertEqual(cone(X, 1, d = 4), Frustum(origin, X, 2, 0))

        # Cone - invalid
        with self.assertNothingRaised():    cone(X , 5 , 1)        # Reference
        with self.assertRaises(TypeError) : cone(5 , 5 , 1)        # First is not a vector
        with self.assertRaises(TypeError) : cone(X , "", 1)        # Second is not a vector or number
        with self.assertRaises(ValueError): cone(X , 5    )        # Neither radius nor diameter
        with self.assertRaises(ValueError): cone(X , 5 , 1, 1)     # Both radius and diameter
        with self.assertRaises(ValueError): cone(v0, 5 , 1)        # Zero vector is not allowed as direction
        with self.assertRaises(TypeError) : cone(v0, 5 , r=(1, 2)) # Radii
        with self.assertRaises(TypeError) : cone(v0, 5 , d=(1, 2)) # Diameters

        # Frustum - base/cap
        self.assertEqual(frustum(X, Y,     (2, 3)), Frustum(X, Y, 2, 3))
        self.assertEqual(frustum(X, Y, r = (2, 3)), Frustum(X, Y, 2, 3))
        self.assertEqual(frustum(X, Y, d = (4, 6)), Frustum(X, Y, 2, 3))

        # Frustum - direction/length
        self.assertEqual(frustum(X, 1,     (2, 3)), Frustum(origin, X, 2, 3))
        self.assertEqual(frustum(X, 1, r = (2, 3)), Frustum(origin, X, 2, 3))
        self.assertEqual(frustum(X, 1, d = (4, 6)), Frustum(origin, X, 2, 3))

        # Frustum - invalid
        with self.assertNothingRaised():    frustum(X , 5 , (1, 2))         # Reference
        with self.assertRaises(TypeError) : frustum(5 , 5 , (1, 2))         # First is not a vector
        with self.assertRaises(TypeError) : frustum(X , "", (1, 2))         # Second is not a vector or number
        with self.assertRaises(ValueError): frustum(X , 5)                  # Neither radii nor diameters
        with self.assertRaises(ValueError): frustum(X , 5 , (1, 2), (1, 2)) # Both radii and diameters
        with self.assertRaises(ValueError): frustum(v0, 5 , (2, 3))         # Zero vector is not allowed as direction
        with self.assertRaises(TypeError) : frustum(X , 1, r = 2)           # Single radius
        with self.assertRaises(TypeError) : frustum(X , 1, d = 4)           # Single diameter

        # Errors caught by _get_radii
        with self.assertRaises(ValueError): frustum(X, 1, r=(2, 3), d=(4, 6))  # Both radius and diameter
        with self.assertRaises(ValueError): frustum(X, 1)                      # Neither radius nor diameter
        with self.assertRaises(ValueError): frustum(X, 1, r = (2, 3, 4)) # Too many radii
        with self.assertRaises(ValueError): frustum(X, 1, d = (4, 6, 8)) # Too many diameters
        with self.assertRaises(ValueError): frustum(X, 1, r = (2, )) # Too few radii
        with self.assertRaises(ValueError): frustum(X, 1, d = (4, )) # Too few diameters

    def test_sphere_generators(self):
        self.assertEqual(sphere(2), Sphere(2))
        self.assertEqual(sphere(r = 2), Sphere(r = 2))
        self.assertEqual(sphere(d = 2), Sphere(r = 1))

        # Invalid
        with self.assertRaises(TypeError): sphere(r = "2")
        with self.assertRaises(TypeError): sphere(d = "2")

        # Errors caught by _get_radius
        with self.assertRaises(ValueError): sphere(r=2, d=2)  # Both radius and diameter
        with self.assertRaises(ValueError): sphere()          # Neither radius nor diameter

    def test_plane_generators(self):
        self.assertEqual(plane(X, 1), Plane(X, 1))

    def test_layer_generators(self):
        self.assertEqual(layer(X, 1, 2), Layer(X, 1, 2))
