"""
Architectural detail kit for the hero miniatures. Everything in metres, origin at
ground, +Y north, +Z up. Pieces are built at real detail; the bake pipeline
merges flat faces, caps triangles and paints the rest into the texture.
"""
import math
import bpy, bmesh
from mathutils import Vector, Matrix
from chronokit import box, cylinder, dome, join, shade, material, mesh_from, ellipse_ring, _finish, boolean_cut

MARBLE, TRAV, BRICK, TILE, BRONZE, GOLD, DARK, PLASTER = "#EDE6D6", "#D9C7A5", "#B98B6A", "#A65238", "#8A7A58", "#C9A24A", "#3A2A1E", "#E3D9C6"


# ---------------------------------------------------------------- helpers

def place(o, loc=(0, 0, 0), rot_z=0.0):
    o.rotation_euler[2] += rot_z
    o.location = Vector(loc) + o.location
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return o


def copy_at(src, loc, rot_z=0.0, name=None):
    d = src.copy()
    d.data = src.data.copy()
    d.name = name or src.name + "_c"
    bpy.context.collection.objects.link(d)
    d.matrix_world = Matrix.Translation(Vector(loc)) @ Matrix.Rotation(rot_z, 4, "Z")
    return d


def cyl_x(name, r, length, loc, color, verts=16):
    """Cylinder lying along X."""
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=length, location=loc, rotation=(0, math.pi / 2, 0))
    o = bpy.context.active_object
    bpy.ops.object.transform_apply(rotation=True)
    return _finish(o, name, color)


def cyl_y(name, r, length, loc, color, verts=16):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=length, location=loc, rotation=(math.pi / 2, 0, 0))
    o = bpy.context.active_object
    bpy.ops.object.transform_apply(rotation=True)
    return _finish(o, name, color)


def half_cyl_y(name, r, length, loc, color, verts=20):
    """Upper half of a cylinder along Y (barrel vault), sitting with its axis at loc.z."""
    o = cyl_y(name, r, length, loc, color, verts)
    bm = bmesh.new()
    bm.from_mesh(o.data)
    bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=Vector(loc), plane_no=(0, 0, 1), clear_inner=True)
    edges = [e for e in bm.edges if all(abs(v.co.z - loc[2]) < 1e-4 for v in e.verts)]
    bmesh.ops.contextual_create(bm, geom=edges)
    bm.to_mesh(o.data)
    bm.free()
    return o


def half_cyl_x(name, r, length, loc, color, verts=20):
    o = cyl_x(name, r, length, loc, color, verts)
    bm = bmesh.new()
    bm.from_mesh(o.data)
    bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=Vector(loc), plane_no=(0, 0, 1), clear_inner=True)
    edges = [e for e in bm.edges if all(abs(v.co.z - loc[2]) < 1e-4 for v in e.verts)]
    bmesh.ops.contextual_create(bm, geom=edges)
    bm.to_mesh(o.data)
    bm.free()
    return o


# ---------------------------------------------------------------- orders

def column(name, x, y, z, h, r, order="corinthian", color=MARBLE, flutes=16):
    """A full column: base, tapered shaft, capital and abacus. ~150-250 faces."""
    parts = []
    if order != "tuscan":
        parts += [cylinder(name + "_plinth", r * 1.35, r * 0.25, (x, y, z), color, verts=8),
                  cylinder(name + "_torus", r * 1.22, r * 0.22, (x, y, z + r * 0.25), shade(color, 0.04), verts=flutes)]
    zb = z + (0 if order == "tuscan" else r * 0.47)
    cap_h = {"tuscan": r * 0.8, "doric": r * 0.7, "ionic": r * 0.8, "corinthian": r * 2.2}[order]
    shaft_h = h - (zb - z) - cap_h
    parts.append(cylinder(name + "_shaft", r, shaft_h, (x, y, zb), color, verts=flutes, r_top=r * 0.86))
    zc = zb + shaft_h
    if order == "corinthian":
        parts.append(cylinder(name + "_bell", r * 0.9, cap_h * 0.8, (x, y, zc), shade(color, -0.02), verts=flutes, r_top=r * 1.25))
        for k in range(8):
            a = k * math.pi / 4
            parts.append(box(f"{name}_leaf{k}", r * 0.35, r * 0.18, cap_h * 0.45, (x + math.cos(a) * r * 0.95, y + math.sin(a) * r * 0.95, zc), shade(color, -0.06), rot_z=a))
        parts.append(box(name + "_abacus", r * 2.7, r * 2.7, cap_h * 0.2, (x, y, zc + cap_h * 0.8), color))
    elif order == "ionic":
        parts.append(box(name + "_echinus", r * 2.1, r * 1.5, cap_h * 0.45, (x, y, zc), color))
        for s in (-1, 1):
            parts.append(cyl_y(f"{name}_volute{s}", r * 0.38, r * 1.6, (x + s * r * 1.05, y, zc + cap_h * 0.3), shade(color, -0.04), verts=10))
        parts.append(box(name + "_abacus", r * 2.4, r * 2.4, cap_h * 0.2, (x, y, zc + cap_h * 0.6), color))
    else:
        parts.append(cylinder(name + "_echinus", r * 0.95, cap_h * 0.5, (x, y, zc), color, verts=flutes, r_top=r * 1.3))
        parts.append(box(name + "_abacus", r * 2.6, r * 2.6, cap_h * 0.5, (x, y, zc + cap_h * 0.5), color))
    return join(parts, name)


def colonnade(name, pts, z, h, r, order="corinthian", color=MARBLE):
    """Many columns: one is built, the rest are linked copies, then joined."""
    proto = column(name + "_proto", 0, 0, 0, h, r, order, color)
    objs = [copy_at(proto, (x, y, z), name=f"{name}{i}") for i, (x, y) in enumerate(pts)]
    bpy.data.objects.remove(proto, do_unlink=True)
    return join(objs, name)


def entablature(name, x0, x1, y0, y1, z, h, color=MARBLE, dentils=True, frieze_color=None):
    """Architrave (two fasciae), frieze and a projecting cornice with a dentil course, around a rectangle."""
    w, d = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    a = h * 0.38
    f = h * 0.3
    c = h * 0.32
    parts = [box(name + "_arch1", w, d, a * 0.5, (cx, cy, z), shade(color, -0.03)),
             box(name + "_arch2", w + h * 0.06, d + h * 0.06, a * 0.5, (cx, cy, z + a * 0.5), color),
             box(name + "_frieze", w, d, f, (cx, cy, z + a), frieze_color or shade(color, -0.05)),
             box(name + "_cornice", w + h * 0.5, d + h * 0.5, c * 0.55, (cx, cy, z + a + f + c * 0.45), shade(color, 0.04)),
             box(name + "_corona", w + h * 0.3, d + h * 0.3, c * 0.45, (cx, cy, z + a + f), color)]
    if dentils:
        step = max(h * 0.18, 0.3)
        for side, (sx0, sy0, sx1, sy1) in enumerate([(x0, y0, x1, y0), (x0, y1, x1, y1), (x0, y0, x0, y1), (x1, y0, x1, y1)]):
            L = math.hypot(sx1 - sx0, sy1 - sy0)
            n = int(L / step)
            horiz = sy0 == sy1
            out = -1 if (horiz and sy0 == y0) or (not horiz and sx0 == x0) else 1
            for k in range(n):
                t = (k + 0.5) / n
                px, py = sx0 + (sx1 - sx0) * t, sy0 + (sy1 - sy0) * t
                if horiz:
                    py += out * (h * 0.12)
                else:
                    px += out * (h * 0.12)
                parts.append(box(f"{name}_d{side}_{k}", step * 0.5, step * 0.5, c * 0.25, (px, py, z + a + f + c * 0.15), shade(color, 0.06)))
    return join(parts, name)


def pediment(name, w, d, z, h, y_front, color=MARBLE, roof=TILE, ridges=True, statues=True):
    """Gabled roof over a w x d rectangle with a framed tympanum on the front (at y_front, facing -Y)."""
    over = h * 0.15
    W, D = w + over * 2, d + over * 2
    v = [(-W / 2, -D / 2, 0), (W / 2, -D / 2, 0), (0, -D / 2, h), (-W / 2, D / 2, 0), (W / 2, D / 2, 0), (0, D / 2, h)]
    # slopes and soffit only: the front gable is the framed tympanum below, the back gets a plain wall
    f = [(0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]
    cy = y_front + d / 2
    parts = [mesh_from(name + "_roof", v, f, (0, cy, z), roof)]
    parts.append(mesh_from(name + "_back_gable", [(-w / 2, 0, 0), (w / 2, 0, 0), (0, 0, h * (w / W))], [(0, 1, 2)], (0, y_front + d - 0.2, z), shade(color, -0.04)))
    # raking cornices along the front gable
    L = math.hypot(W / 2, h)
    ang = math.atan2(h, W / 2)
    for s in (-1, 1):
        rc = box(f"{name}_rake{s}", L, 0.9, 0.45, (0, 0, 0), shade(color, 0.04))
        rc.rotation_euler = (0, s * ang, 0)
        place(rc, (s * W / 4, y_front - over - 0.2, z + h / 2 - 0.25))
        parts.append(rc)
    # recessed tympanum
    tv = [(-w / 2, 0, 0), (w / 2, 0, 0), (0, 0, h * (w / W))]
    tymp = mesh_from(name + "_tymp", [(x, y_front + 0.3, zz + z) for x, _, zz in tv] + [(x, y_front + 0.9, zz + z) for x, _, zz in tv], [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)], (0, 0, 0), shade(color, -0.07))
    parts.append(box(name + "_horiz_cornice", W, 1.0, 0.5, (0, y_front - over * 0.5 + 0.2, z - 0.1), shade(color, 0.04)))
    parts.append(tymp)
    if statues:
        for k in range(5):
            t = (k + 1) / 6
            sx = -w * 0.35 + w * 0.7 * t
            sh = (h - 0.8) * (1 - abs(sx) / (w / 2)) * 0.7
            if sh > 0.6:
                parts.append(statue(f"{name}_ped{k}", sx, y_front - 0.3, z + 0.3, sh, shade(color, -0.12)))
        for s in (-1, 0, 1):
            ax = s * (W / 2 - 0.4)
            parts.append(statue(f"{name}_acro{s}", ax, y_front - over, z + (h if s == 0 else 0.2), 1.8, BRONZE if s == 0 else shade(color, -0.1)))
    if ridges:
        n = max(6, int(D / 1.2))
        for k in range(n):
            yy = cy - D / 2 + (k + 0.5) * D / n
            for s in (-1, 1):
                rr = box(f"{name}_imbrex{s}_{k}", L * 0.98, 0.22, 0.18, (0, 0, 0), shade(roof, 0.1))
                rr.rotation_euler = (0, s * ang, 0)
                place(rr, (s * W / 4, yy, z + h / 2 + 0.05))
                parts.append(rr)
        parts.append(box(name + "_ridge", 0.5, D, 0.4, (0, cy, z + h - 0.1), shade(roof, -0.1)))
    return join(parts, name)


def statue(name, x, y, z, h, color=BRONZE):
    """A tiny standing figure on a plinth."""
    return join([box(name + "_base", h * 0.32, h * 0.32, h * 0.12, (x, y, z), shade(color, 0.1)),
                 cylinder(name + "_body", h * 0.13, h * 0.62, (x, y, z + h * 0.12), color, verts=8, r_top=h * 0.08),
                 dome(name + "_head", h * 0.09, (x, y, z + h * 0.74), color, squash=1.6, segments=8, rings=4)], name)


def steps_front(name, w, h, n, y_front, z=0, color=TRAV, tread=0.45):
    """A flight of steps rising toward +Y and ending at y_front. Each step is a solid column of its own: no overlapping faces."""
    parts = []
    rise = h / n
    for i in range(n):
        y = y_front - tread * (n - i) + tread / 2
        parts.append(box(f"{name}_{i}", w, tread, rise * (i + 1), (0, y, z), color))
    return join(parts, name)


def tiled_hip_roof(name, w, d, h, loc, color=TILE):
    """Hipped roof with ridge and tile courses."""
    from chronokit import hip_roof
    parts = [hip_roof(name, w, d, h, loc, color, ridge=0.5, overhang=0.6)]
    n = max(4, int(min(w, d) / 2.4))
    for k in range(1, n):
        f = k / n
        parts.append(box(f"{name}_course{k}", (w + 1.2) * (1 - f * 0.95), (d + 1.2) * (1 - f * 0.55), 0.12, (loc[0], loc[1], loc[2] + h * f - 0.06), shade(color, 0.08)))
    return join(parts, name)


def arch_bay(name, w, h, t, r, spring, color, keystone=True):
    """A wall panel w x h, thickness t, with a round-headed opening of radius r springing at `spring`. Faces -Y."""
    wall = box(name, w, t, h, (0, 0, 0), color)
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=r, depth=t + 2, location=(0, 0, spring), rotation=(math.pi / 2, 0, 0))
    c1 = bpy.context.active_object
    wall = boolean_cut(wall, c1)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, spring / 2 - 0.02))
    c2 = bpy.context.active_object
    c2.scale = (r * 2, t + 2, spring + 0.04)
    bpy.ops.object.transform_apply(scale=True)
    wall = boolean_cut(wall, c2)
    parts = [wall]
    # archivolt ring and impost blocks
    for s in (-1, 1):
        parts.append(box(f"{name}_impost{s}", 0.5, t + 0.25, 0.35, (s * (r + 0.1), 0, spring - 0.35), shade(color, 0.06)))
    if keystone:
        parts.append(box(name + "_key", 0.7, t + 0.3, 0.9, (0, 0, spring + r - 0.3), shade(color, 0.08)))
    return join(parts, name)


def thermal_window(name, r, t, loc, color, frame=PLASTER, rot_z=0.0):
    """A semicircular 'Diocletian' window (two mullions) set into a wall: frame + dark glazing."""
    parts = [half_cyl_y(name + "_glass", r, t * 0.4, (0, 0, 0), DARK, verts=16)]
    for s in (-1, 1):
        parts.append(box(f"{name}_mull{s}", 0.35, t * 0.6, r * 0.95, (s * r / 3, 0, 0), frame))
    ring = ellipse_ring(name + "_ring", r + 0.45, r + 0.45, r / (r + 0.45), t * 0.6, (0, 0, 0), frame, n=24, arc=math.pi, start=0)
    ring.rotation_euler = (math.pi / 2, 0, 0)
    place(ring, (0, t * 0.3, 0))
    parts.append(ring)
    o = join(parts, name)
    o.rotation_euler[2] = rot_z
    return place(o, loc)


def stepped_dome(name, r, z, color, steps=5, oculus=0.0):
    """A low dome with step rings around its base (Pantheon type)."""
    parts = []
    for k in range(steps):
        rr = r * (1.0 - k * 0.035)
        parts.append(cylinder(f"{name}_step{k}", rr, r * 0.05, (0, 0, z + k * r * 0.05), shade(color, 0.03 * (k % 2)), verts=40))
    parts.append(dome(name + "_cap", r * (1 - steps * 0.035), (0, 0, z + steps * r * 0.05), color, squash=0.72, segments=40, rings=12))
    if oculus:
        top = z + steps * r * 0.05 + r * (1 - steps * 0.035) * 0.72
        parts.append(cylinder(name + "_oculus_ring", oculus + 0.6, 0.5, (0, 0, top - 0.35), BRONZE, verts=24))
        parts.append(cylinder(name + "_oculus", oculus, 0.3, (0, 0, top - 0.1), DARK, verts=24))
    return join(parts, name)


def ring_of(proto_fn, n, rx, ry, z, name, face_out=True, skip=None):
    """Lay n copies of a piece around an ellipse, each turned to face outward. proto_fn() -> object facing -Y."""
    proto = proto_fn()
    objs = []
    for i in range(n):
        a = math.tau * i / n
        if skip and skip(i, a):
            continue
        x, y = rx * math.cos(a), ry * math.sin(a)
        # outward normal of the ellipse
        nx, ny = math.cos(a) / rx, math.sin(a) / ry
        rot = math.atan2(ny, nx) + math.pi / 2 if face_out else 0
        objs.append(copy_at(proto, (x, y, z), rot, name=f"{name}{i}"))
    bpy.data.objects.remove(proto, do_unlink=True)
    return join(objs, name) if objs else None
