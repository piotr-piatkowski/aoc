import bpy

from mathutils import *


D = bpy.data
C = bpy.context

def add_cuboid(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    center = (p1[0]+dx/2, p1[1]+dy/2, p1[2]+dz/2)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=center)
    bpy.ops.transform.resize(value=(dx, dy, dz))
    bpy.ops.object.transform_apply(scale=True)
    bpy.ops.rigidbody.object_add()
    bpy.context.object.rigid_body.type = 'PASSIVE'
    return bpy.context.object

def add_ball(x, y):
    center = (x+0.5, y+0.5, 0.5)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=center)
    bpy.ops.object.shade_smooth()
    bpy.ops.rigidbody.object_add()
    return bpy.context.object

#f = open('/home/kompas/git/aoc/2023/s14')
f = open('/home/kompas/git/aoc/2023/input-d14.txt')
lines = [l.strip() for l in f]

ROWS = len(lines)
COLS = len(lines[0])
print(ROWS, COLS)

assert ROWS == COLS
SZ = ROWS

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

BSZ = 0.2
floor = add_cuboid((0, 0, -0.2), (SZ, SZ, 0))
# floor.name = 'floor'
# floor.editmode_set()
# #bpy.ops.mesh.subdivide(number_cuts=10)
# print("OK")


# Add barrier
add_cuboid((-BSZ, -BSZ, -0.2), (SZ+BSZ, 0, 0.6))
add_cuboid((-BSZ, SZ+BSZ, -0.2), (SZ+BSZ, SZ, 0.6))
add_cuboid((-BSZ, 0, -0.2), (0, SZ, 0.6))
add_cuboid((SZ, 0, -0.2), (SZ+BSZ, SZ, 0.6))


cnt = 0
for y, l in enumerate(lines):
    for x, c in enumerate(l):
        if c == '#':
            add_cuboid((x, y, 0), (x+1, y+1, 1))
        if c == 'O':
            add_ball(x, y)
        cnt += 1
    if cnt > 4000:
        break

bpy.ops.object.select_all(action='SELECT')
bpy.ops.transform.rotate(
    value=0.3,
    orient_axis='X',
    orient_type='GLOBAL',
    orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
    orient_matrix_type='GLOBAL',
)
