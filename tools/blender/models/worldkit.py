"""
World architecture kit: parts for building the miniatures of every city outside
Rome (Islamic, Mughal and Indian, Chinese and Japanese, Gothic and Byzantine,
Egyptian and Mesopotamian, Mesoamerican and Andean, African). Same conventions
as chronokit: metres, origin at the ground centre, +X east, +Y north, +Z up,
flat clay colours. Openings are dark inset panels rather than boolean holes:
they read the same at miniature scale and stay light to bake.

Every function returns one joined object; compose them into a chronokit.Model.
"""
import math
import bpy, bmesh
from mathutils import Vector
from chronokit import box, cylinder, dome, join, shade, mesh_from, hip_roof, gable_roof, _finish

# palette by material, shared by every city
RED_SANDSTONE, BUFF_SANDSTONE, MARBLE, PLASTER, MUDBRICK, BRICK = "#A8553F", "#C9A06A", "#EEE8DC", "#E6DCC8", "#B48A62", "#B5714F"
LIMESTONE, GRANITE, BASALT, TUFA, ADOBE, WHITEWASH = "#D8CBB0", "#9C9690", "#5E5A56", "#C9B48A", "#C29B70", "#F0EBE0"
TILE_GREY, TILE_GREEN, TILE_GOLD, TILE_RED, SLATE, LEAD = "#5E5F62", "#5F8A5A", "#C9A24A", "#A65238", "#5C6068", "#7D8590"
TIMBER, TIMBER_RED, LACQUER, THATCH, GILT, BRONZE = "#8C6A4A", "#9A3A2C", "#B23A2A", "#B39A5E", "#D4AE55", "#7E6E4E"
GLAZE_BLUE, GLAZE_TURQ, DARK, WATER, GREEN, STUCCO = "#3E5C9A", "#3F9A9A", "#2E241C", "#5F878C", "#7D9A6C", "#E8DCC2"


def lathe(name, profile, loc=(0, 0, 0), color=MARBLE, verts=24, cap_top=True, cap_bottom=True):
    """Solid of revolution about Z from [(radius, z), ...] going upward."""
    bm = bmesh.new()
    rings = []
    for r, z in profile:
        ring = []
        for i in range(verts):
            a = math.tau * i / verts
            ring.append(bm.verts.new((loc[0] + r * math.cos(a), loc[1] + r * math.sin(a), loc[2] + z)))
        rings.append(ring)
    for a, b in zip(rings, rings[1:]):
        for i in range(verts):
            j = (i + 1) % verts
            bm.faces.new((a[i], a[j], b[j], b[i]))
    if cap_bottom and profile[0][0] > 1e-4:
        bm.faces.new(list(reversed(rings[0])))
    if cap_top and profile[-1][0] > 1e-4:
        bm.faces.new(rings[-1])
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    return _finish(o, name, color)


def prism(name, pts, h, loc=(0, 0, 0), color=LIMESTONE):
    """Extrude a closed 2D outline [(x, y), ...] (counter-clockwise) up by h."""
    n = len(pts)
    verts = [(x, y, 0) for x, y in pts] + [(x, y, h) for x, y in pts]
    faces = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return mesh_from(name, verts, faces, loc, color)


def frustum(name, w0, d0, w1, d1, h, loc=(0, 0, 0), color=LIMESTONE):
    """A box with a smaller top: battered walls, pylons, pyramid tiers, platforms."""
    verts = [(-w0 / 2, -d0 / 2, 0), (w0 / 2, -d0 / 2, 0), (w0 / 2, d0 / 2, 0), (-w0 / 2, d0 / 2, 0),
             (-w1 / 2, -d1 / 2, h), (w1 / 2, -d1 / 2, h), (w1 / 2, d1 / 2, h), (-w1 / 2, d1 / 2, h)]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return mesh_from(name, verts, faces, loc, color)


def rot(o, deg):
    """Turn a part about the vertical axis through the world origin (where every part is built)."""
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    o.rotation_euler[2] += math.radians(deg)
    bpy.ops.object.transform_apply(rotation=True)
    return o


def move(o, x=0, y=0, z=0):
    o.location = (o.location[0] + x, o.location[1] + y, o.location[2] + z)
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=True)
    return o


