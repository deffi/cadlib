// This file was auto-generated by cadlib
$fn = 60;

difference() {
    union() {
        sphere(0.6);
        cube([1, 2, 3]);
    }
    cylinder(4.0, r = 0.5);
}