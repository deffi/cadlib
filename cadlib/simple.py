"""The recommended import for most applications.

Most applications will want to do
    import cadlib.simple as cl
or
    from cadlib.simple import *

This module contains all generators (for objects, CSGs, and transforms), all
transform shortcuts, base vectors X, Y, and Z, and render_to_file.
"""
from cadlib.util.vector import X, Y, Z
from cadlib.object.generators import *
from cadlib.csg.generators import *
from cadlib.transform.generators import *
from cadlib.transform.shortcuts import *

from cadlib.scad import render_to_file
