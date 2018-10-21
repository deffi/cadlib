from cadlib.transform.primitives import Translate, RotateYpr

__all__ = [
    'right', 'left', 'forward', 'back', 'up', 'down',
    'yaw_left', 'yaw_right', 'pitch_up', 'pitch_down', 'roll_right', 'roll_left',
]

def right  (x): return Translate([ x,  0,  0])
def left   (x): return Translate([-x,  0,  0])
def forward(y): return Translate([ 0,  y,  0])
def back   (y): return Translate([ 0, -y,  0])
def up     (z): return Translate([ 0,  0,  z])
def down   (z): return Translate([ 0,  0, -z])

def yaw_left  (y): return RotateYpr( y,  0,  0)
def yaw_right (y): return RotateYpr(-y,  0,  0)
def pitch_up  (p): return RotateYpr( 0,  p,  0)
def pitch_down(p): return RotateYpr( 0, -p,  0)
def roll_right(r): return RotateYpr( 0,  0,  r)
def roll_left (r): return RotateYpr( 0,  0, -r)

