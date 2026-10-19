"""Tenochtitlan / Mexico City landmark miniatures: Mexica temples, palaces, market and causeway works (1350–1519),
and the Spanish viceregal city of 1620. Builders face south (-Y); the landmark rotation turns them on the map."""
import math
import bpy
from chronokit import Model, box, cylinder, dome, join, shade, gable_roof, hip_roof, mesh_from
from worldkit import *

# ---------------------------------------------------------------- palette
STUCCO_W = "#EEE7D6"      # burnished lime stucco
STUCCO_G = "#DCD3C0"
PAVE = "#D8CDB6"          # stucco paving of plazas
EARTH = "#B39A74"         # beaten earth
MUD = "#8F7A5A"
OCHRE_RED = "#A54A34"     # Huitzilopochtli's red
TLALOC_BLUE = "#4C7FA8"   # Tlaloc's blue
JADE = "#4E8A6E"
TEZONTLE = "#8A4537"      # red volcanic stone of colonial Mexico
CHILUCA = "#A8A398"       # grey cut stone
CLOTH = "#F1EBDD"
MAT = "#C8AE78"           # woven palm and reed mats
LAKE = "#5C8486"
REED = "#8E9A5C"
SKULL = "#F2EEE4"
WOOD = "#7A5A3C"
LEAF = "#6F8A5C"


# ---------------------------------------------------------------- small helpers

def rz(o, deg):
    """Rotate about the world Z axis (worldkit.rot turns about the object's own origin)."""
    bpy.context.scene.cursor.location = (0, 0, 0)
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    return rot(o, deg)


def place(o, deg=0, x=0, y=0, z=0):
    if deg:
        o = rz(o, deg)
    return move(o, x, y, z)


def flight(name, w, x, y0, y1, z0, z1, n, color):
    """A solid flight of steps rising from (y0, z0) at the front to (y1, z1) at the back (y1 > y0)."""
    parts = []
    for k in range(n):
        ya = y0 + (y1 - y0) * k / n
        za, zb = z0 + (z1 - z0) * k / n, z0 + (z1 - z0) * (k + 1) / n
        parts.append(box(f"{name}{k}", w, y1 - ya, zb - za, (x, (ya + y1) / 2, za), color))
    return join(parts, name)


def side_prism(name, pts_yz, x0, x1, color):
    """Extrude a profile [(y, z), ...] drawn in the YZ plane between x0 and x1."""
    n = len(pts_yz)
    verts = [(x0, y, z) for y, z in pts_yz] + [(x1, y, z) for y, z in pts_yz]
    faces = [tuple(range(n)), tuple(range(2 * n - 1, n - 1, -1))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def alfarda(name, x, wb, y0, y1, z0, z1, color, hb=1.4, dado=True):
    """A stair balustrade: a sloping ramp beside the steps, steepening into a vertical dado at the top, a serpent head at the foot."""
    parts = []
    if dado:
        yk = y1 - (y1 - y0) * 0.12
        zk = z0 + (z1 - z0) * 0.80
        prof = [(y0, z0), (y0, z0 + hb), (yk, zk + hb), (yk + 0.6, z1 + hb * 1.6), (y1, z1 + hb * 1.6), (y1, z0)]
    else:
        prof = [(y0, z0), (y0, z0 + hb), (y1, z1 + hb), (y1, z0)]
    parts.append(side_prism(name, prof, x - wb / 2, x + wb / 2, color))
    parts.append(serpent_head(name + "_head", (x, y0 - 0.9, z0), 0, max(0.6, wb / 1.4), JADE))
    return join(parts, name)


def tiers(name, w0, d0, w1, d1, h, n, loc=(0, 0, 0), color=STUCCO_W, band=None, ledge=1.0):
    """Stacked battered platforms from a w0 x d0 base to a w1 x d1 summit; each tier with a projecting band at its top."""
    x, y, z = loc
    parts = []
    th = h / n
    for i in range(n):
        a = w0 + (w1 - w0) * i / n
        b = d0 + (d1 - d0) * i / n
        a2 = w0 + (w1 - w0) * (i + 1) / n + ledge * 2
        b2 = d0 + (d1 - d0) * (i + 1) / n + ledge * 2
        parts.append(frustum(f"{name}_t{i}", a, b, a2, b2, th * 0.86, (x, y, z + th * i), shade(color, -0.03 * (i % 2))))
        parts.append(box(f"{name}_b{i}", a2 + 0.3, b2 + 0.3, th * 0.14, (x, y, z + th * i + th * 0.86), band or shade(color, -0.12)))
    return join(parts, name)


def shrine(name, w, d, h, loc, wall=STUCCO_W, roof=OCHRE_RED, roof_h=None, band=None, stripes=None, crest=None, thatch=False):
    """A temple-top shrine: a stuccoed cella with a dark doorway (facing -Y) and a tall roof, optional painted band, stripes and roof crest."""
    x, y, z = loc
    rh = roof_h or h * 1.1
    parts = [box(name + "_w", w, d, h, (x, y, z), wall)]
    parts.append(arch_panel(name + "_door", w * 0.34, h * 0.72, (x, y - d / 2, z), "S", DARK, False, 0.3))
    if band:
        parts.append(box(name + "_band", w + 0.25, d + 0.25, h * 0.2, (x, y, z + h * 0.8), band))
    if stripes:
        n = 5
        for i in range(n):
            if i % 2 == 0:
                parts.append(box(f"{name}_st{i}", w / n * 0.9, 0.2, h * 0.75, (x - w / 2 + w / n * (i + 0.5), y - d / 2 - 0.1, z), stripes))
    if thatch:
        parts.append(cylinder(name + "_roof", max(w, d) * 0.72, rh, (x, y, z + h), THATCH, verts=4, r_top=0.3))
        parts[-1].rotation_euler[2] = math.pi / 4
    else:
        parts.append(frustum(name + "_roof", w * 1.06, d * 1.06, w * 0.72, d * 0.5, rh, (x, y, z + h), roof))
        parts.append(box(name + "_rband", w * 0.75, d * 0.53, rh * 0.12, (x, y, z + h + rh * 0.55), shade(roof, 0.35)))
    if crest:
        n = max(3, int(w / 1.6))
        for i in range(n):
            px = x - w * 0.34 + w * 0.68 * i / (n - 1)
            parts.append(box(f"{name}_cr{i}", 0.7, 0.5, rh * 0.45, (px, y, z + h + rh), crest))
    return join(parts, name)


def stepped_merlons(name, w, d, z, loc=(0, 0), size=1.0, color=STUCCO_W):
    """Aztec stepped crenellations (almenas) round the top of a w x d block."""
    o = merlons(name, w, d, z, size, size * 0.9, color, "stepped")
    return move(o, loc[0], loc[1], 0)


def canoe(name, length, loc, deg=0, color=WOOD, cargo=None):
    """A dugout canoe, pointed at both ends, with an optional load."""
    x, y, z = loc
    L, W = length, length * 0.16
    pts = [(-L / 2, 0), (-L * 0.36, -W / 2), (L * 0.36, -W / 2), (L / 2, 0), (L * 0.36, W / 2), (-L * 0.36, W / 2)]
    parts = [prism(name + "_h", pts, 0.45, (0, 0, 0), color)]
    parts.append(prism(name + "_in", [(px * 0.86, py * 0.7) for px, py in pts], 0.08, (0, 0, 0.4), shade(color, -0.35)))
    if cargo:
        parts.append(box(name + "_c", L * 0.36, W * 0.62, 0.5, (0, 0, 0.42), cargo))
    o = join(parts, name)
    return place(o, deg, x, y, z)


def water_plate(name, w, d, loc=(0, 0, 0), h=0.12):
    return box(name, w, d, h, loc, LAKE)


def stall(name, loc, goods, awning=CLOTH, deg=0, mat_only=False):
    """A market stall: goods on a mat, either open or under a cloth awning on a pole."""
    x, y, z = loc
    if mat_only:
        parts = [box(name + "_m", 2.8, 2.2, 0.12, (0, 0, 0), MAT),
                 box(name + "_g", 2.0, 1.2, 0.45, (0, -0.1, 0.12), goods)]
    else:
        parts = [box(name + "_g", 2.2, 1.4, 0.55, (0, -0.2, 0.0), goods),
                 box(name + "_p", 0.18, 0.18, 2.5, (0, 0.95, 0), WOOD),
                 box(name + "_a", 3.1, 2.6, 0.12, (0, 0.1, 2.45), awning)]
    o = join(parts, name)
    return place(o, deg, x, y, z)


def porter(name, loc, deg=0, load=MAT):
    """A tameme, a porter carrying a load on his back with a tumpline."""
    x, y, z = loc
    p = [cylinder(name + "_b", 0.26, 1.1, (0, 0, 0), "#E6DCC6", verts=6),
         cylinder(name + "_l", 0.2, 0.5, (0, 0, 0), "#8A5A3C", verts=6),
         dome(name + "_h", 0.22, (0, 0.05, 1.25), "#8A5A3C", segments=8, rings=4),
         box(name + "_load", 0.7, 0.55, 0.75, (0, 0.42, 0.75), load),
         box(name + "_tump", 0.08, 0.5, 0.06, (0, 0.2, 1.42), WOOD)]
    o = join(p, name)
    return place(o, deg, x, y, z)


def house_block(name, w, d, h, loc, color=STUCCO_W, door="S", parapet=True):
    return flat_house(name, w, d, h, loc, color, parapet, door)


def colonial_church(name, length, width, h, loc=(0, 0, 0), color=CHILUCA, trim=TEZONTLE, towers=1, dome_r=0, merlon=True, roof=None):
    """A Mexican colonial church facing -Y: a long single nave with buttresses and a flat, merloned roof (or a timber gable),
    a stone portal with a choir window, a belfry tower at the front corner, optionally a dome over the crossing."""
    x, y, z = loc
    parts = [box(name + "_nave", width, length, h, (x, y, z), color)]
    n = max(3, int(length / 9))
    for i in range(n + 1):
        by = y - length / 2 + length * i / n
        for s in (-1, 1):
            parts.append(box(f"{name}_bu{i}{s}", 1.8, 2.4, h * 0.9, (x + s * (width / 2 + 0.9), by, z), shade(color, -0.07)))
        if i < n:
            for s in (-1, 1):
                parts.append(arch_panel(f"{name}_win{i}{s}", 1.4, 3.2, (x + s * width / 2, by + length / n / 2, z + h * 0.55), "E" if s > 0 else "W", DARK, False, 0.3))
    if roof:
        g = gable_roof(name + "_roof", width, length, width * 0.35, (x, y, z + h), roof, 0.5)
        parts.append(g)
    else:
        parts.append(box(name + "_par", width + 0.3, length + 0.3, 0.7, (x, y, z + h), shade(color, -0.04)))
        if merlon:
            parts.append(stepped_merlons(name + "_mer", width, length, z + h + 0.7, (x, y), 0.8, shade(color, -0.04)))
    # facade: portal, choir window, a raised gable
    fy = y - length / 2
    parts.append(box(name + "_fac", width + 1.0, 1.4, h + 3.5, (x, fy + 0.2, z), shade(color, 0.04)))
    parts.append(box(name + "_portal", width * 0.36, 0.6, h * 0.62, (x, fy - 0.6, z), trim))
    parts.append(arch_panel(name + "_door", width * 0.2, h * 0.45, (x, fy - 0.95, z), "S", DARK, False, 0.4))
    w_ = cylinder(name + "_choir", width * 0.09, 0.5, (x, fy - 0.55, z + h * 0.72), DARK, verts=12)
    w_.rotation_euler[0] = math.pi / 2
    parts.append(w_)
    th = h * 1.75
    corners = [1] if towers == 1 else [-1, 1]
    for s in corners:
        tx, ty, tw = x + s * (width / 2 + 0.5), fy + width * 0.18, width * 0.42
        parts.append(box(f"{name}_tw{s}", tw, tw, th, (tx, ty, z), color))
        parts.append(box(f"{name}_tc{s}", tw + 0.6, tw + 0.6, 0.6, (tx, ty, z + th), shade(color, 0.1)))
        parts.append(box(f"{name}_bel{s}", tw * 0.78, tw * 0.78, h * 0.42, (tx, ty, z + th + 0.6), color))
        for f, (dx, dy) in (("S", (0, -1)), ("N", (0, 1)), ("E", (1, 0)), ("W", (-1, 0))):
            parts.append(arch_panel(f"{name}_ba{s}{f}", tw * 0.3, h * 0.3, (tx + dx * tw * 0.39, ty + dy * tw * 0.39, z + th + 0.8), f, DARK, False, 0.3))
        parts.append(dome(f"{name}_td{s}", tw * 0.36, (tx, ty, z + th + 0.6 + h * 0.42), TILE_GOLD if dome_r else shade(color, -0.05), segments=12, rings=6))
        parts.append(cylinder(f"{name}_cross{s}", 0.15, 2.4, (tx, ty, z + th + 0.6 + h * 0.42 + tw * 0.34), DARK, verts=4))
    if dome_r:
        cy = y + length * 0.28
        parts.append(cylinder(name + "_drum", dome_r, dome_r * 0.7, (x, cy, z + h), color, verts=16))
        parts.append(dome(name + "_dome", dome_r, (x, cy, z + h + dome_r * 0.7), TILE_GOLD, segments=16, rings=8))
        parts.append(cylinder(name + "_lantern", dome_r * 0.22, dome_r * 0.5, (x, cy, z + h + dome_r * 1.65), color, verts=8))
    return join(parts, name)


def colonial_range(name, w, d, h, loc, color=STUCCO, trim=TEZONTLE, storeys=2, face="S", arcade_ground=False, merlon=True, msize=0.7):
    """A colonial two-storey range: rows of windows, a stone string course, a flat roof with spouts and merlons."""
    x, y, z = loc
    parts = [box(name + "_b", w, d, h, (x, y, z), color)]
    parts.append(box(name + "_sc", w + 0.3, d + 0.3, 0.5, (x, y, z + h / storeys), trim))
    parts.append(box(name + "_par", w + 0.3, d + 0.3, 0.8, (x, y, z + h), shade(color, -0.05)))
    along = w if face in ("S", "N") else d
    n = max(3, int(along / 4.5))
    fy = {"S": (0, -d / 2), "N": (0, d / 2), "E": (w / 2, 0), "W": (-w / 2, 0)}[face]
    for s in range(storeys):
        if s == 0 and arcade_ground:
            parts.append(arcade(f"{name}_arc", along * 0.96, h / storeys * 0.85, n, (x + fy[0] * 1.01, y + fy[1] * 1.01, z), face, DARK, False, 0.72, 0.4))
        else:
            parts.append(arcade(f"{name}_win{s}", along * 0.92, h / storeys * 0.5, n, (x + fy[0] * 1.01, y + fy[1] * 1.01, z + h / storeys * s + h / storeys * 0.22), face, DARK, False, 0.32, 0.3))
    if merlon:
        parts.append(stepped_merlons(name + "_m", w, d, z + h + 0.8, (x, y), msize, shade(color, -0.05)))
    return join(parts, name)


def frame_band(name, w, d, z, loc=(0, 0), color=OCHRE_RED, t=0.5, over=0.25):
    """A painted band round the outside of a w x d block (or courtyard ring), leaving its roof and court open."""
    x, y = loc
    parts = [box(name + "_s", w + 2 * over, over, t, (x, y - d / 2 - over / 2, z), color), box(name + "_n", w + 2 * over, over, t, (x, y + d / 2 + over / 2, z), color),
             box(name + "_w", over, d, t, (x - w / 2 - over / 2, y, z), color), box(name + "_e", over, d, t, (x + w / 2 + over / 2, y, z), color)]
    return join(parts, name)


def tree_row(name, pts, r=2.6, color=LEAF):
    return join([tree(f"{name}{i}", r, (px, py, 0), color) for i, (px, py) in enumerate(pts)], name)


# ---------------------------------------------------------------- the Templo Mayor

def serpent_head(name, loc, deg=0, s=1.0, color=JADE):
    """A carved feathered-serpent head, snout toward -Y before turning: head, snout, jaw, tongue, eyes, fangs, plume crest."""
    x, y, z = loc
    p = [box(name + "_h", 1.4 * s, 1.8 * s, 1.1 * s, (0, 0, 0), color),
         box(name + "_sn", 1.2 * s, 0.8 * s, 0.5 * s, (0, -1.25 * s, 0.5 * s), color),
         box(name + "_jaw", 1.1 * s, 0.7 * s, 0.35 * s, (0, -1.15 * s, 0.0), shade(color, -0.18)),
         box(name + "_tg", 0.3 * s, 0.7 * s, 0.08 * s, (0, -1.75 * s, 0.38 * s), OCHRE_RED),
         box(name + "_e1", 0.32 * s, 0.22 * s, 0.32 * s, (-0.46 * s, -0.9 * s, 0.78 * s), SKULL),
         box(name + "_e2", 0.32 * s, 0.22 * s, 0.32 * s, (0.46 * s, -0.9 * s, 0.78 * s), SKULL),
         box(name + "_f1", 0.16 * s, 0.16 * s, 0.4 * s, (-0.38 * s, -1.5 * s, 0.1 * s), SKULL),
         box(name + "_f2", 0.16 * s, 0.16 * s, 0.4 * s, (0.38 * s, -1.5 * s, 0.1 * s), SKULL),
         box(name + "_pl", 1.6 * s, 0.5 * s, 0.6 * s, (0, 0.55 * s, 1.0 * s), shade(color, 0.18)),
         box(name + "_pl2", 1.2 * s, 0.4 * s, 0.4 * s, (0, 0.95 * s, 1.5 * s), shade(color, 0.3))]
    o = join(p, name)
    return place(o, deg, x, y, z)


def serpent_body(name, a, b, z, s=1.0, color=JADE, amp=0.5, step=1.1):
    """An undulating serpent body of segments from a to b (x, y), lying on the ground at z."""
    ax, ay = a
    bx, by = b
    L = math.hypot(bx - ax, by - ay)
    ux, uy = (bx - ax) / L, (by - ay) / L
    nx, ny = -uy, ux
    n = max(2, int(L / step))
    parts = []
    for k in range(n):
        t = (k + 0.5) / n
        off = amp * math.sin(t * L * 0.55)
        cx, cy = ax + (bx - ax) * t + nx * off, ay + (by - ay) * t + ny * off
        ang = math.atan2(uy, ux)
        parts.append(box(f"{name}{k}", step * 1.05 * s, 0.9 * s, 0.7 * s, (cx, cy, z), color if k % 3 else shade(color, 0.15), rot_z=ang))
    return join(parts, name)


def merlon_line(name, a, b, z, size=0.9, color=STUCCO_W, gap=0.9):
    """A row of stepped merlons (almenas) along a straight line."""
    ax, ay = a
    bx, by = b
    L = math.hypot(bx - ax, by - ay)
    ang = math.atan2(by - ay, bx - ax)
    n = max(1, int(L / (size + gap)))
    parts = []
    for k in range(n):
        t = (k + 0.5) / n
        cx, cy = ax + (bx - ax) * t, ay + (by - ay) * t
        parts.append(box(f"{name}{k}a", size, size * 0.6, size * 0.6, (cx, cy, z), color, rot_z=ang))
        parts.append(box(f"{name}{k}b", size * 0.55, size * 0.5, size * 0.5, (cx, cy, z + size * 0.6), color, rot_z=ang))
    return join(parts, name)


def studs(name, w, d, z, loc=(0, 0), step=2.2, size=0.55, color=STUCCO_G, skip_front=None):
    """Projecting stone tenons (clavos) round the band of a tier; skip_front = half-width of the front span left clear."""
    x, y = loc
    parts = []
    for side, (length, fixed, horiz) in enumerate([(w, -d / 2, True), (w, d / 2, True), (d, -w / 2, False), (d, w / 2, False)]):
        n = max(1, int(length / step))
        for i in range(n):
            t = -length / 2 + (i + 0.5) * length / n
            px, py = (t, fixed) if horiz else (fixed, t)
            if skip_front and side == 0 and abs(px) < skip_front:
                continue
            parts.append(box(f"{name}{side}_{i}", size, size, size * 0.8, (x + px, y + py, z), color))
    return join(parts, name) if parts else None


def brazier(name, loc, r=1.0, color=OCHRE_RED):
    x, y, z = loc
    p = [cylinder(name + "_f", r * 0.45, r * 0.7, (x, y, z), shade(color, -0.2), verts=12, r_top=r * 0.6),
         cylinder(name + "_b", r * 0.6, r * 1.1, (x, y, z + r * 0.7), color, verts=16, r_top=r),
         cylinder(name + "_c", r * 0.85, r * 0.12, (x, y, z + r * 1.72), "#2E241C", verts=16),
         cylinder(name + "_fl", r * 0.5, r * 0.9, (x, y, z + r * 1.8), "#E08A3A", verts=8, r_top=0.05)]
    return join(p, name)


def bearer(name, loc, deg=0, banner="#E8D9A0"):
    """A stone standard-bearer figure holding a banner pole."""
    x, y, z = loc
    p = [box(name + "_ped", 1.0, 1.0, 0.5, (0, 0, 0), STUCCO_G),
         cylinder(name + "_body", 0.38, 1.4, (0, 0, 0.5), "#B9A88A", verts=8),
         dome(name + "_head", 0.36, (0, 0, 1.95), "#B9A88A", segments=8, rings=4),
         box(name + "_arm", 0.7, 0.25, 0.25, (0.3, -0.25, 1.4), "#B9A88A"),
         cylinder(name + "_pole", 0.08, 4.2, (0.55, -0.35, 0.5), WOOD, verts=4),
         box(name + "_ban", 0.08, 1.4, 1.0, (0.55, -0.35 + 0.7, 3.6), banner)]
    o = join(p, name)
    return place(o, deg, x, y, z)


def chacmool(name, loc):
    x, y, z = loc
    p = [box(name + "_base", 2.2, 1.1, 0.4, (x, y, z), STUCCO_G),
         box(name + "_legs", 0.9, 0.9, 0.9, (x - 0.55, y, z + 0.4), "#9C9283"),
         box(name + "_torso", 1.2, 0.9, 0.5, (x + 0.35, y, z + 0.4), "#9C9283"),
         box(name + "_bowl", 0.6, 0.6, 0.2, (x + 0.3, y, z + 0.9), "#8A8073"),
         box(name + "_head", 0.5, 0.5, 0.6, (x + 0.95, y, z + 0.8), "#9C9283")]
    return join(p, name)


def tm_shrine(name, kind, w, d, h, loc, rh):
    """A shrine on top of the Templo Mayor. kind 'tlaloc': blue-and-white bands, chalchihuite discs, a cresting of cloud rings;
    kind 'huitz': red with a raised frieze of skulls and a cresting of skulls and butterflies."""
    x, y, z = loc
    blue = kind == "tlaloc"
    main = TLALOC_BLUE if blue else OCHRE_RED
    parts = [box(name + "_base", w + 1.6, d + 1.6, 0.6, (x, y, z), STUCCO_G)]
    z1 = z + 0.6
    parts.append(box(name + "_w", w, d, h, (x, y, z1), STUCCO_W))
    # doorway with jambs and lintel
    parts.append(arch_panel(name + "_door", w * 0.3, h * 0.7, (x, y - d / 2, z1), "S", DARK, False, 0.35))
    for s in (-1, 1):
        parts.append(box(f"{name}_jamb{s}", 0.7, 0.5, h * 0.74, (x + s * w * 0.19, y - d / 2 - 0.15, z1), main))
    parts.append(box(name + "_lint", w * 0.46, 0.55, 0.6, (x, y - d / 2 - 0.15, z1 + h * 0.7), main))
    if blue:
        n = 9
        for i in range(n):
            if i % 2:
                continue
            u = -0.5 + (i + 0.5) / n
            parts.append(box(f"{name}_sf{i}", w / n * 0.95, 0.22, h * 0.62, (x + u * w, y - d / 2 - 0.1, z1), main))
            parts.append(box(f"{name}_sb{i}", w / n * 0.95, 0.22, h * 0.62, (x + u * w, y + d / 2 + 0.1, z1), main))
            for s in (-1, 1):
                parts.append(box(f"{name}_ss{i}{s}", 0.22, d / n * 0.95, h * 0.62, (x + s * (w / 2 + 0.1), y + u * d, z1), main))
        parts.append(frame_band(name + "_fr", w, d, z1 + h * 0.66, (x, y), main, h * 0.28, 0.3))
        for i in range(7):
            u = -0.5 + (i + 0.5) / 7
            for (px, py, fx) in ((x + u * w, y - d / 2 - 0.5, 0), (x + u * w, y + d / 2 + 0.5, 0), (x - w / 2 - 0.5, y + u * d, 1), (x + w / 2 + 0.5, y + u * d, 1)):
                c = cylinder(f"{name}_ch{i}{px:.0f}{py:.0f}", 0.42, 0.25, (px, py, z1 + h * 0.8), SKULL, verts=10)
                c.rotation_euler[0 if not fx else 1] = math.pi / 2
                parts.append(c)
    else:
        parts.append(frame_band(name + "_dado", w, d, z1, (x, y), main, h * 0.32, 0.25))
        parts.append(frame_band(name + "_fr", w, d, z1 + h * 0.62, (x, y), main, h * 0.36, 0.3))
        for i in range(10):
            u = -0.5 + (i + 0.5) / 10
            for (px, py, along_x) in ((x + u * w, y - d / 2 - 0.55, True), (x + u * w, y + d / 2 + 0.55, True), (x - w / 2 - 0.55, y + u * d, False), (x + w / 2 + 0.55, y + u * d, False)):
                parts.append(box(f"{name}_sk{i}{px:.0f}{py:.0f}", 0.55 if along_x else 0.25, 0.25 if along_x else 0.55, 0.45, (px, py, z1 + h * 0.74), SKULL))
                parts.append(box(f"{name}_sj{i}{px:.0f}{py:.0f}", 0.35 if along_x else 0.22, 0.22 if along_x else 0.35, 0.18, (px, py, z1 + h * 0.74 - 0.2), SKULL))
    # the tall roof with painted bands and a roof comb (cresting)
    zr = z1 + h
    parts.append(frustum(name + "_roof", w * 1.08, d * 1.08, w * 0.72, d * 0.42, rh, (x, y, zr), main))
    for k, t in enumerate((0.3, 0.62)):
        ww, dd = w * 1.08 + (w * 0.72 - w * 1.08) * t, d * 1.08 + (d * 0.42 - d * 1.08) * t
        parts.append(frustum(f"{name}_rb{k}", ww + 0.3, dd + 0.3, ww + 0.2, dd + 0.15, rh * 0.09, (x, y, zr + rh * t), SKULL if blue else STUCCO_W))
    zc = zr + rh
    parts.append(box(name + "_comb", w * 0.68, 0.5, rh * 0.55, (x, y, zc), STUCCO_W))
    parts.append(box(name + "_combb", w * 0.7, 0.6, rh * 0.12, (x, y, zc + rh * 0.2), main))
    n = 9
    for i in range(n):
        px = x - w * 0.32 + w * 0.64 * i / (n - 1)
        if blue:
            c = cylinder(f"{name}_cl{i}", 0.45, 0.3, (px, y, zc + rh * 0.55 + 0.45), SKULL, verts=12)
            c.rotation_euler[0] = math.pi / 2
            parts.append(c)
            parts.append(box(f"{name}_cs{i}", 0.25, 0.3, 0.45, (px, y, zc + rh * 0.55), SKULL))
        else:
            parts.append(box(f"{name}_cs{i}", 0.6, 0.45, 0.55, (px, y, zc + rh * 0.55), SKULL))
            if i % 2 == 0:
                parts.append(box(f"{name}_bf{i}", 0.9, 0.3, 0.5, (px, y, zc + rh * 0.55 + 0.55), "#E8C46A"))
    return join(parts, name)


def nopal(name, loc, h=2.2):
    x, y, z = loc
    p = [cylinder(name + "_t", 0.45, h, (x, y, z), "#5E7F4A", verts=6)]
    for i, (dx, dz, a) in enumerate(((-0.9, 0.8, 0.3), (0.9, 1.1, -0.3), (0, 1.7, 0.0), (-0.7, 1.9, 0.5), (0.7, 2.1, -0.5))):
        p.append(box(f"{name}_p{i}", 1.3, 0.35, 1.6, (x + dx, y, z + dz), "#6E9254", rot_z=a))
    return join(p, name)


def maize_plot(name, w, d, loc, rows=6, per=12):
    """A chinampa bed with rows of maize plants, edged with willow stakes."""
    x, y, z = loc
    p = [box(name + "_bed", w, d, 0.35, (x, y, z), "#6E5A40")]
    for r in range(rows):
        for k in range(per):
            px = x - w / 2 + w * (k + 0.5) / per
            py = y - d / 2 + d * (r + 0.5) / rows
            p.append(cylinder(f"{name}_m{r}_{k}", 0.35, 1.8, (px, py, z + 0.35), "#7FA05A" if (r + k) % 3 else "#A9B65A", verts=5, r_top=0.05))
    for k in range(4):
        p.append(cylinder(f"{name}_w{k}", 0.15, 3.2, (x - w / 2 + w * k / 3, y - d / 2 - 0.3, z), WOOD, verts=4))
    return join(p, name)


def templo_mayor(stage="1519"):
    m = Model("templo-mayor-" + stage)
    if stage == "1350":
        # the first temple: an earthen platform with two thatched shrines, among reed houses and chinampa beds
        m.add(0, box("ground", 100, 100, 0.25, (0, 0, 0), EARTH), "ground")
        m.add(0, box("yard", 40, 36, 0.12, (0, 2, 0.25), "#C2AA80"))
        m.add(0, tiers("plat", 22, 20, 17, 14, 4.0, 2, (0, 4, 0.37), MUD, shade(MUD, -0.15), 0.4))
        m.add(0, studs("pst", 22.8, 20.8, 1.6, (0, 4), 1.6, 0.4, shade(MUD, -0.25), 4.5))
        m.add(1, flight("stair", 7, 0, -9, -3.0, 0.37, 4.37, 14, shade(MUD, 0.1)), "stair")
        for s in (-1, 1):
            m.add(1, alfarda(f"alf{s}", s * 4.1, 1.0, -9, -3.0, 0.37, 4.37, shade(MUD, -0.05), 0.8, False))
        for s in (-1, 1):
            m.add(2, shrine(f"sh{s}", 5.5, 5, 3.2, (s * 3.6, 6, 4.37), "#D8C9A8", THATCH, 4.0, OCHRE_RED if s > 0 else TLALOC_BLUE, None, None, thatch=True), "shrines")
            m.add(2, brazier(f"br{s}", (s * 6.5, -1.5, 4.37), 0.6))
        # a fence of reed posts round the temple yard
        for i in range(48):
            t = i / 48
            per = 2 * (40 + 36)
            dist = t * per
            if dist < 40:
                px, py = -20 + dist, -16
            elif dist < 76:
                px, py = 20, -16 + (dist - 40)
            elif dist < 116:
                px, py = 20 - (dist - 76), 20
            else:
                px, py = -20, 20 - (dist - 116)
            if py == -16 and abs(px) < 5:
                continue
            m.add(1, cylinder(f"fence{i}", 0.15, 1.6, (px, py, 0.25), REED, verts=5))
        # the eagle on the cactus
        m.add(2, nopal("nopal", (14, -24, 0.25), 2.2))
        m.add(2, box("eagle", 0.8, 0.6, 1.0, (14, -24, 0.25 + 3.9), "#5A4532"))
        m.add(2, box("wings", 2.8, 0.3, 0.5, (14, -24, 0.25 + 4.5), "#5A4532"))
        m.add(2, box("snake", 1.6, 0.18, 0.18, (14.6, -24.4, 0.25 + 4.1), JADE))
        # reed and mud houses with granaries, and chinampa beds
        huts = ((-34, -34), (-38, -14), (-36, 24), (-22, 38), (32, 34), (38, 14), (36, -30), (24, -40), (-6, -40), (0, 40))
        for i, (hx, hy) in enumerate(huts):
            m.add(1, house_block(f"hut{i}", 7, 5, 2.6, (hx, hy, 0.25), "#CDB892", "S" if hy < 0 else "N", False))
            m.add(2, cylinder(f"hutr{i}", 4.6, 2.6, (hx, hy, 2.85), THATCH, verts=4, r_top=0.2))
            m.stages[2][-1].rotation_euler[2] = math.pi / 4
            gx, gy = hx + (5 if hx < 0 else -5), hy + (3 if hy < 0 else -3)
            m.add(2, cylinder(f"gran{i}", 1.1, 1.8, (gx, gy, 0.25), "#B79C6E", verts=10))
            m.add(2, cylinder(f"granr{i}", 1.4, 1.2, (gx, gy, 2.05), THATCH, verts=10, r_top=0.1))
        for i, (px, py, pw, pd) in enumerate(((-36, 2, 14, 12), (36, 0, 14, 12), (-14, -32, 16, 9), (14, 32, 16, 9), (-30, 44, 14, 8), (30, -44, 14, 8), (44, 44, 10, 8), (-44, -44, 10, 8))):
            m.add(2, maize_plot(f"plot{i}", pw, pd, (px, py, 0.25), 6, 14))
        return m
    if stage == "1620":
        # the stump of the temple quarried away, houses of the new city built round it
        m.add(0, box("ground", 100, 100, 0.25, (0, 0, 0), PAVE), "ground")
        m.add(0, tiers("mound", 46, 42, 30, 26, 4.5, 2, (0, 4, 0.25), "#9C8F7C", "#857664", 0.5), "ruin")
        m.add(0, flight("stub", 18, 0, -21, -12, 0.25, 3.0, 8, "#A89A86"))
        rnd = [((i * 37) % 23 - 11.5, (i * 53) % 21 - 10.5, 0.8 + (i * 7) % 5 * 0.4) for i in range(160)]
        for i, (bx, by, sz) in enumerate(rnd):
            ring = 1.6 + (i % 4) * 0.3
            m.add(1, box(f"blk{i}", sz * 1.4, sz, sz * 0.7, (bx * ring, by * ring + 4, 0.25 + (4.5 if abs(bx) < 7 and abs(by) < 6 and i % 2 else 0)), CHILUCA if i % 3 else TEZONTLE, rot_z=i * 0.7), "rubble" if i == 0 else None)
        for i in range(6):
            m.add(1, serpent_head(f"sh{i}", (-24 + i * 9, -26, 0.25), (i * 40) % 360, 0.9, "#8E9C86"))
        for i, (hx, hy, hw, hd, face) in enumerate(((-40, 0, 16, 92, "E"), (40, 6, 16, 72, "W"), (0, 42, 52, 14, "S"), (6, -42, 40, 14, "N"),
                                                    (-40, -42, 16, 14, "N"), (40, -38, 16, 22, "W"))):
            m.add(2, colonial_range(f"h{i}", hw, hd, 7.5, (hx, hy, 0.25), STUCCO if i % 2 else "#E2D2B8", TEZONTLE, 2, face, False, False), "houses")
            m.add(2, frame_band(f"hb{i}", hw, hd, 3.3, (hx, hy), TEZONTLE, 0.4, 0.15))
        for i, (tx, ty) in enumerate(((-26, 34), (26, 32), (-28, -32))):
            m.add(2, tree(f"t{i}", 2.4, (tx, ty, 0.25), LEAF))
        m.add(2, box("crossb", 2, 2, 1.2, (20, -22, 0.25), CHILUCA))
        m.add(2, box("cross", 0.4, 0.4, 4.5, (20, -22, 1.45), CHILUCA))
        m.add(2, box("crossa", 2.0, 0.4, 0.4, (20, -22, 4.6), CHILUCA))
        return m
    big = stage == "1519"
    m.add(0, box("plat", 100, 100, 1.8, (0, 0, 0), PAVE), "platform")
    m.add(0, flight("pstair", 60, 0, -50, -47.5, 0, 1.8, 6, shade(PAVE, 0.06)))
    m.add(0, frame_band("pband", 100, 100, 0.6, (0, 0), OCHRE_RED, 0.5, 0.2))
    # almenas round the platform edge (not over its front stair)
    m.add(0, merlon_line("pmw", (-49.5, -49.5), (-49.5, 49.5), 1.8, 0.9, STUCCO_W))
    m.add(0, merlon_line("pme", (49.5, -49.5), (49.5, 49.5), 1.8, 0.9, STUCCO_W))
    m.add(0, merlon_line("pmn", (-49.5, 49.5), (49.5, 49.5), 1.8, 0.9, STUCCO_W))
    for s in (-1, 1):
        m.add(0, merlon_line(f"pmf{s}", (s * 49.5, -49.5), (s * 31, -49.5), 1.8, 0.9, STUCCO_W))
    if big:
        W0, D0, W1, D1, H, N = 78, 72, 46, 36, 30.0, 4
        yc = 4.0
    else:
        W0, D0, W1, D1, H, N = 52, 46, 32, 24, 18.0, 3
        yc = 6.0
    z0 = 1.8
    ledge = 1.0
    m.add(1, tiers("pyr", W0, D0, W1, D1, H, N, (0, yc, z0), STUCCO_W, shade(STUCCO_W, -0.16), ledge), "pyramid")
    th = H / N
    yfront = yc - D0 / 2 - (11 if big else 7)
    ytop = yc - D1 / 2 + 0.5
    zt = z0 + H
    sw = W0 * 0.19
    # tenons along every tier band, and a painted band at the foot of each talud
    for i in range(N):
        a2 = W0 + (W1 - W0) * (i + 1) / N + ledge * 2 + 0.3
        b2 = D0 + (D1 - D0) * (i + 1) / N + ledge * 2 + 0.3
        m.add(1, studs(f"stud{i}", a2, b2, z0 + th * i + th * 0.88, (0, yc), 2.4, 0.55, STUCCO_G, sw + 4.5))
        a0 = W0 + (W1 - W0) * i / N
        b0 = D0 + (D1 - D0) * i / N
        m.add(1, frame_band(f"talb{i}", a0, b0, z0 + th * i, (0, yc), OCHRE_RED if i % 2 == 0 else TLALOC_BLUE, 0.35, 0.12))
    # the twin stairs: real steps, balustrades steepening near the top, serpent heads at the foot
    for s in (-1, 1):
        xs = s * (sw / 2 + 1.8)
        n = 60 if big else 34
        m.add(1, flight(f"stair{s}", sw, xs, yfront, ytop, z0, zt, n, shade(STUCCO_W, 0.04)))
        for k in range(0, n, 2):
            ya = yfront + (ytop - yfront) * k / n
            za = z0 + (zt - z0) * (k + 1) / n
            m.add(1, box(f"nose{s}{k}", sw, 0.12, 0.08, (xs, ya - 0.04, za - 0.02), shade(STUCCO_W, -0.12)))
        m.add(1, alfarda(f"alf_out{s}", s * (sw + 2.6), 1.6, yfront, ytop, z0, zt, STUCCO_G))
    m.add(1, alfarda("alf_mid", 0, 3.2, yfront, ytop, z0, zt, STUCCO_G))
    # the coatepetl serpents along the foot of the pyramid (sides and back)
    ex, ey0, ey1 = W0 / 2 + 3.5, yc - D0 / 2 + 2, yc + D0 / 2 + 3.5
    segs = [((-ex, ey0), (-ex, ey1), -90), ((ex, ey0), (ex, ey1), 90), ((-ex, ey1), (ex, ey1), 180)]
    for j, (a, b, deg) in enumerate(segs):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        ns = max(2, int(L / 18))
        for q in range(ns):
            t0, t1 = q / ns, (q + 0.85) / ns
            pa = (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0)
            pb = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)
            m.add(1, serpent_body(f"sb{j}_{q}", pa, pb, z0, 0.9, JADE, 0.45))
            ox, oy = {-90: (-1.6, 0), 90: (1.6, 0), 180: (0, 1.6)}[deg]
            m.add(1, serpent_head(f"shd{j}_{q}", (pb[0] + ox, pb[1] + oy, z0), deg, 0.9, JADE))
    # serpent heads on the front of the platform, braziers
    for i in range(-3, 4):
        if abs(i) > 1:
            m.add(1, serpent_head(f"serp{i}", (i * 6.5, yfront - 1.5, z0), 0, 1.0, JADE))
    for s in (-1, 1):
        m.add(1, brazier(f"braz{s}", (s * 24, yfront + 2, z0), 1.4))
    for i, (cx, cy) in enumerate(((-46, -46), (46, -46), (-46, 46), (46, 46))):
        m.add(1, brazier(f"cbz{i}", (cx, cy, z0), 1.0))
    if big:
        # the Coyolxauhqui stone at the foot of Huitzilopochtli's stair (Huitzilopochtli = +X here, south on the map)
        m.add(1, cylinder("coyol", 1.6, 0.3, (sw / 2 + 1.8, yfront - 3.5, z0), "#C9B48A", verts=24))
        m.add(1, cylinder("coyolc", 1.1, 0.06, (sw / 2 + 1.8, yfront - 3.5, z0 + 0.3), OCHRE_RED, verts=16))
    # the summit: almenas round its edge, the shrines, sacrificial stone, chacmool, braziers, standard-bearers
    sa, sb = W1 + 2 * ledge, D1 + 2 * ledge
    m.add(2, merlon_line("smw", (-sa / 2, yc - sb / 2), (-sa / 2, yc + sb / 2), zt, 0.7, STUCCO_W), "shrines")
    m.add(2, merlon_line("sme", (sa / 2, yc - sb / 2), (sa / 2, yc + sb / 2), zt, 0.7, STUCCO_W))
    m.add(2, merlon_line("smn", (-sa / 2, yc + sb / 2), (sa / 2, yc + sb / 2), zt, 0.7, STUCCO_W))
    for s in (-1, 1):
        m.add(2, merlon_line(f"smf{s}", (s * sa / 2, yc - sb / 2), (s * (sw + 4.0), yc - sb / 2), zt, 0.7, STUCCO_W))
    shw, shd, shh = (W1 * 0.36, D1 * 0.5, 7.0) if big else (W1 * 0.36, D1 * 0.5, 5.0)
    sy = yc + D1 * 0.12
    m.add(2, tm_shrine("huitz", "huitz", shw, shd, shh, (W1 * 0.24, sy, zt), shh * 1.2))
    m.add(2, tm_shrine("tlaloc", "tlaloc", shw, shd, shh, (-W1 * 0.24, sy, zt), shh * 1.2))
    fy = sy - shd / 2 - 2.6
    m.add(2, box("techcatl", 1.0, 0.7, 0.9, (W1 * 0.24, fy, zt), "#5E5A56"))
    m.add(2, box("techcatlb", 1.6, 1.2, 0.2, (W1 * 0.24, fy, zt), "#7A7068"))
    m.add(2, chacmool("chac", (-W1 * 0.24, fy, zt)))
    for i, bx in enumerate((-W1 * 0.44, -W1 * 0.06, W1 * 0.06, W1 * 0.44)):
        m.add(2, brazier(f"tbraz{i}", (bx, ytop + 1.6, zt), 0.9))
    for i, bx in enumerate((-(sw + 2.6), -3.3, 3.3, sw + 2.6)):
        m.add(2, bearer(f"std{i}", (bx, ytop + 0.9, zt), 0))
    return m


# ---------------------------------------------------------------- the Sacred Precinct

def sacred_precinct(stage="1519"):
    m = Model("sacred-precinct-" + stage)
    W, D = 290, 300
    if stage == "1440":
        m.add(0, box("ground", W, D, 0.15, (0, 0, 0), EARTH), "ground")
        x0, x1, y0, y1 = -80, 135, -100, 130
        m.add(0, box("pave", x1 - x0, y1 - y0, 0.3, ((x0 + x1) / 2, (y0 + y1) / 2, 0), PAVE))
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
        m.add(1, wall_run("wall", pts, 2.6, 2.0, (0, 0, 0), STUCCO_W, towers=False, merlon=None), "wall")
        for i, (gx, gy) in enumerate(((x0, 108), (-98 + 60, y0), (x1, -25))):
            m.add(2, box(f"gate{i}", 9 if gx in (x0, x1) else 12, 12 if gx in (x0, x1) else 9, 4.2, (gx, gy, 0), STUCCO_G), "gates")
        for i, (hx, hy) in enumerate(((-60, 110), (-60, -80), (110, 110), (110, -85))):
            m.add(2, house_block(f"pr{i}", 22, 9, 3.6, (hx, hy, 0), STUCCO_W, "S"))
        return m
    m.add(0, box("pave", W, D, 0.25, (0, 0, 0), PAVE), "paving")
    # the serpent wall with its gates (W at y=108, S and N at x=-98, E at y=-25.5)
    gates = {"W": (-W / 2, 108), "S": (-98, -D / 2), "N": (-98, D / 2), "E": (W / 2, -25.5)}
    gw = 12
    segs = []
    # south and north walls split at x=-98
    for yy in (-D / 2, D / 2):
        segs.append(((-W / 2, yy), (-98 - gw / 2, yy)))
        segs.append(((-98 + gw / 2, yy), (W / 2, yy)))
    segs.append(((-W / 2, -D / 2), (-W / 2, 108 - gw / 2)))
    segs.append(((-W / 2, 108 + gw / 2), (-W / 2, D / 2)))
    segs.append(((W / 2, -D / 2), (W / 2, -25.5 - gw / 2)))
    segs.append(((W / 2, -25.5 + gw / 2), (W / 2, D / 2)))
    for i, (a, b) in enumerate(segs):
        m.add(1, wall_run(f"wall{i}", [a, b], 3.0, 2.2, (0, 0, 0), STUCCO_W, towers=False, merlon=None), "coatepantli")
        m.add(1, merlon_line(f"wm{i}", a, b, 3.0, 0.9, STUCCO_W, 0.8))
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        n = int(L / 6)
        for k in range(n):
            t = (k + 0.5) / n
            hx, hy = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            # serpent heads on the outer face
            ox = 1.5 if hx >= W / 2 - 0.1 else (-1.5 if hx <= -W / 2 + 0.1 else 0)
            oy = 1.5 if hy >= D / 2 - 0.1 else (-1.5 if hy <= -D / 2 + 0.1 else 0)
            m.add(1, box(f"sh{i}_{k}", 1.1, 1.1, 0.9, (hx + ox, hy + oy, 0.6), JADE))
        m.add(1, box(f"band{i}", abs(b[0] - a[0]) + 2.5, abs(b[1] - a[1]) + 2.5, 0.4, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 2.3), OCHRE_RED))
    for f, (gx, gy) in gates.items():
        along_x = f in ("S", "N")
        for s in (-1, 1):
            px, py = (gx + s * (gw / 2 + 2), gy) if along_x else (gx, gy + s * (gw / 2 + 2))
            m.add(2, box(f"pier{f}{s}", 4, 4, 5.5, (px, py, 0), STUCCO_G), "gates")
            m.add(2, stepped_merlons(f"pm{f}{s}", 4, 4, 5.5, (px, py), 0.8, STUCCO_W))
        m.add(2, box(f"lint{f}", gw + 8 if along_x else 4.4, 4.4 if along_x else gw + 8, 1.0, (gx, gy, 5.5), OCHRE_RED))
    # priests' houses along the inside of the wall, kept clear of the gates and the main buildings
    ranges = [((-120, 141), 44, 8, "S"), ((-40, 141), 70, 8, "S"), ((60, 141), 60, 8, "S"), ((118, 141), 30, 8, "S"),
              ((-115, -141), 50, 8, "N"), ((-30, -141), 90, 8, "N"), ((90, -141), 90, 8, "N"),
              ((-140, -60), 8, 120, "E"), ((-140, 60), 8, 70, "E"), ((140, -100), 8, 70, "W"), ((140, 80), 8, 100, "W")]
    for i, ((rx, ry), rw, rd, face) in enumerate(ranges):
        m.add(2, house_block(f"pr{i}", rw, rd, 3.6, (rx, ry, 0.25), STUCCO_W, face))
        m.add(2, box(f"prb{i}", rw + 0.3, rd + 0.3, 0.35, (rx, ry, 3.2), OCHRE_RED))
    # lesser temples, the gladiatorial stone and altars in the open plaza
    t1 = step_pyramid("tez", 22, 22, 3, 9, (0, 0, 0), STUCCO_W, temple=True, temple_color=STUCCO_W, stair_face="S", roof_color="#5A5A66")
    m.add(2, place(t1, 180, 60, -112, 0.25), "temples")
    t2 = step_pyramid("xip", 18, 18, 3, 7, (0, 0, 0), STUCCO_W, temple=True, temple_color=STUCCO_W, stair_face="S", roof_color=OCHRE_RED)
    m.add(2, place(t2, -90, -110, -90, 0.25))
    t3 = step_pyramid("cih", 16, 16, 2, 6, (0, 0, 0), STUCCO_W, temple=True, temple_color=STUCCO_W, stair_face="S", roof_color=JADE)
    m.add(2, place(t3, 0, -110, 90, 0.25))
    m.add(2, tiers("temal", 9, 9, 7, 7, 1.6, 1, (-10, -92, 0.25), STUCCO_W, OCHRE_RED, 0.2))
    m.add(2, cylinder("temalacatl", 1.6, 0.8, (-10, -92, 1.85), "#8C8478", verts=16))
    for i, (ax, ay) in enumerate(((20, -100), (-60, -40), (-70, 50), (60, 110), (-120, 130), (0, 125))):
        m.add(2, box(f"momox{i}", 3.2, 3.2, 1.4, (ax, ay, 0.25), STUCCO_G))
        m.add(2, cylinder(f"mbz{i}", 0.6, 0.8, (ax, ay, 1.65), OCHRE_RED, verts=8, r_top=0.8))
    return m


def temple_of_ehecatl():
    m = Model("temple-of-ehecatl")
    # a platform with a square front and a rounded back, two tiers
    def outline(fw, r, front, n=14):
        pts = [(-fw / 2, front), (fw / 2, front), (fw / 2, 0)]
        for i in range(1, n):
            a = -math.pi * i / n
            pts.append((r * math.cos(a), -r * math.sin(a)))
        pts.append((-fw / 2, 0))
        return pts
    m.add(0, prism("t1", outline(34, 17, -18), 3.6, (0, 3, 0), STUCCO_W), "platform")
    m.add(0, box("b1", 34.4, 0.4, 0.5, (0, 3 - 18, 3.1), OCHRE_RED))
    m.add(0, prism("t2", outline(27, 13.5, -14), 3.0, (0, 3, 3.6), shade(STUCCO_W, -0.03)))
    m.add(1, flight("stair", 10, 0, -17.5, -10.5, 0, 6.6, 18, shade(STUCCO_W, 0.04)), "stair")
    for s in (-1, 1):
        m.add(1, alfarda(f"alf{s}", s * 5.8, 1.4, -17.5, -10.5, 0, 6.6, STUCCO_G, 1.2, False))
    # the round cella with its conical thatch and a serpent-jaw door
    cz = 6.6
    m.add(2, cylinder("cella", 7, 6.0, (0, 6, cz), STUCCO_W, verts=28), "cella")
    m.add(2, cylinder("cband", 7.15, 1.0, (0, 6, cz + 4.8), OCHRE_RED, verts=28))
    m.add(2, cylinder("roof", 8.4, 7.5, (0, 6, cz + 6.0), THATCH, verts=28, r_top=0.4))
    m.add(2, cylinder("finial", 0.5, 1.6, (0, 6, cz + 13.5), OCHRE_RED, verts=8, r_top=0.1))
    m.add(2, box("jaw", 4.6, 1.2, 5.0, (0, -0.6, cz), OCHRE_RED))
    m.add(2, arch_panel("door", 2.6, 3.6, (0, -1.25, cz), "S", DARK, False, 0.3))
    for i in range(5):
        m.add(2, box(f"fang{i}", 0.35, 0.3, 0.6, (-1.1 + i * 0.55, -1.35, cz + 3.0), SKULL))
    return m


def huey_tzompantli():
    m = Model("huey-tzompantli")
    m.add(0, box("plat", 34, 12, 1.6, (0, 0, 0), STUCCO_W), "platform")
    m.add(0, frame_band("band", 34, 12, 1.1, (0, 0), OCHRE_RED, 0.3))
    m.add(0, flight("stair", 8, 0, -8.5, -6, 0, 1.6, 4, shade(STUCCO_W, 0.04)))
    # the rack: rows of posts with crossbars, skulls threaded on them
    rows, bays, levels = 3, 8, 4
    L = 30.0
    for r in range(rows):
        yy = -3.6 + r * 3.6
        for b in range(bays + 1):
            xx = -L / 2 + L * b / bays
            m.add(1, box(f"post{r}_{b}", 0.35, 0.35, 6.4, (xx, yy, 1.6), WOOD), "rack")
        for lv in range(levels):
            zz = 2.4 + lv * 1.2
            m.add(1, box(f"bar{r}_{lv}", L, 0.14, 0.14, (0, yy, zz + 0.32), WOOD))
            for b in range(bays):
                for k in range(6):
                    xx = -L / 2 + L * b / bays + L / bays * (k + 0.75) / 6.5
                    m.add(2, box(f"sk{r}_{lv}_{b}_{k}", 0.34, 0.36, 0.38, (xx, yy, zz), SKULL), "skulls")
    for s in (-1, 1):
        m.add(2, cylinder(f"tower{s}", 2.0, 4.2, (s * 16.2, 0, 1.6), "#E4DCCB", verts=14))
        m.add(2, cylinder(f"towerc{s}", 2.1, 0.4, (s * 16.2, 0, 5.8), "#D6CCB8", verts=14))
    return m


def ballcourt_precinct():
    m = Model("ballcourt")
    m.add(0, box("floor", 56, 20, 0.2, (0, 0, 0), PAVE), "floor")
    m.add(1, ballcourt("court", 50, 12.5, (0, 0, 0.2), STUCCO_W, 3.8), "court")
    for s in (-1, 1):
        m.add(1, box(f"band{s}", 35, 0.4, 0.4, (0, s * 4.6, 3.6), OCHRE_RED))
    m.add(2, box("altar", 3, 3, 1.2, (0, -9, 0.2), STUCCO_G), "altar")
    m.add(2, cylinder("ball", 0.5, 0.9, (3, 0, 0.2), "#2E2A26", verts=10))
    return m


def calmecac():
    m = Model("calmecac")
    m.add(0, box("plat", 50, 30, 1.5, (0, 0, 0), STUCCO_G), "platform")
    m.add(0, flight("stair", 12, 0, -17, -15, 0, 1.5, 4, STUCCO_W))
    m.add(1, courtyard_ring("rooms", 46, 26, 4.2, 7, (0, 0, 1.5), STUCCO_W, DARK, True), "rooms")
    m.add(1, arch_panel("door", 3.2, 3.0, (0, -13, 1.5), "S", DARK, False, 0.3))
    m.add(2, frame_band("band", 46, 26, 4.9, (0, 0)), "roof")
    m.add(2, stepped_merlons("mer", 46, 26, 5.7, (0, 0), 0.7, STUCCO_W))
    m.add(2, shrine("sh", 6, 5, 3.0, (0, 9.5, 5.7), STUCCO_W, OCHRE_RED, 2.6))
    m.add(2, tree("tree", 2.4, (6, 1, 1.5), LEAF))
    return m


def house_of_eagles():
    m = Model("house-of-eagles")
    m.add(0, box("plat", 40, 28, 1.8, (0, 0, 0), STUCCO_G), "platform")
    m.add(0, flight("stair", 10, -6, -16.5, -14, 0, 1.8, 5, STUCCO_W))
    for s in (-1, 1):
        m.add(0, alfarda(f"alf{s}", -6 + s * 5.6, 1.2, -16.5, -14, 0, 1.8, STUCCO_W, 0.8, False))
    # L-shaped hall: a main hall at the back, a wing at the east, a pillared porch in front
    m.add(1, box("hall", 36, 11, 5.0, (0, 6.5, 1.8), STUCCO_W), "hall")
    m.add(1, box("wing", 11, 12, 5.0, (12.5, -5, 1.8), STUCCO_W))
    m.add(1, arch_panel("door1", 3, 3.4, (-6, 1.0, 1.8), "S", DARK, False, 0.3))
    m.add(1, arch_panel("door2", 2.6, 3.0, (7.0, -5, 1.8), "W", DARK, False, 0.3))
    for i in range(6):
        m.add(1, box(f"pil{i}", 1.1, 1.1, 4.4, (-16 + i * 4.4, -3.5, 1.8), STUCCO_W))
    m.add(2, box("porch_roof", 24, 9, 0.6, (-6, -3.0, 6.2), shade(STUCCO_W, -0.05)), "roofs")
    m.add(2, box("band", 36.3, 11.3, 0.6, (0, 6.5, 5.4), OCHRE_RED))
    m.add(2, box("bandw", 11.3, 12.3, 0.6, (12.5, -5, 5.4), OCHRE_RED))
    m.add(2, stepped_merlons("mer", 36, 11, 6.8, (0, 6.5), 0.7, STUCCO_W))
    # the two clay eagle warriors flanking the doorway
    for s in (-1, 1):
        ex = -6 + s * 3.0
        m.add(2, box(f"ped{s}", 1.2, 1.2, 0.6, (ex, -1.2, 1.8), STUCCO_G))
        m.add(2, cylinder(f"war{s}", 0.42, 1.7, (ex, -1.2, 2.4), "#B07A50", verts=8))
        m.add(2, box(f"wing{s}", 1.9, 0.2, 0.8, (ex, -1.2, 3.2), "#9A6A44"))
        m.add(2, dome(f"head{s}", 0.42, (ex, -1.2, 4.1), "#9A6A44", segments=8, rings=4))
    return m


# ---------------------------------------------------------------- palaces

def moctezuma_palace():
    """Facade on -Y (west once rotated): the great court, the raised throne hall at the back, side courts, a garden."""
    m = Model("moctezuma-palace")
    W, D = 210, 230
    m.add(0, box("plat", W, D, 1.5, (0, 0, 0), STUCCO_G), "platform")
    m.add(0, flight("fstair", 40, 0, -116.5, -115, 0, 1.5, 3, STUCCO_W))
    # the front range of two storeys round the great court
    cy = -50
    m.add(1, courtyard_ring("court", 200, 120, 6.0, 15, (0, cy, 1.5), STUCCO_W, DARK, True), "courts")
    m.add(1, box("front2", 120, 15, 4.5, (0, cy - 52.5, 7.5), STUCCO_W))
    m.add(1, arcade("front2w", 112, 3.0, 16, (0, cy - 60.1, 8.2), "S", DARK, False, 0.45))
    m.add(1, arcade("front1", 190, 4.2, 26, (0, cy - 60.1, 1.5), "S", DARK, False, 0.4))
    m.add(1, arch_panel("gate", 8, 5.2, (0, cy - 60.2, 1.5), "S", DARK, False, 0.5))
    # the throne hall raised on a stepped platform at the back of the court
    m.add(1, tiers("tplat", 76, 30, 68, 24, 4.5, 2, (0, 28, 1.5), STUCCO_W, OCHRE_RED, 0.5))
    m.add(1, flight("tstair", 20, 0, 9, 16, 1.5, 6.0, 9, shade(STUCCO_W, 0.04)))
    m.add(2, box("throne", 58, 18, 7.0, (0, 30, 6.0), STUCCO_W), "halls")
    m.add(2, arcade("thr_arc", 50, 5.0, 8, (0, 20.9, 6.0), "S", DARK, False, 0.6))
    m.add(2, frame_band("thr_band", 58, 18, 11.9, (0, 30), OCHRE_RED, 0.7))
    m.add(2, stepped_merlons("thr_mer", 58, 18, 13.0, (0, 30), 0.9, STUCCO_W))
    # council halls either side of the throne hall
    for s in (-1, 1):
        m.add(2, box(f"council{s}", 28, 16, 5.5, (s * 60, 28, 1.5), STUCCO_W))
        m.add(2, arcade(f"cou_arc{s}", 24, 3.8, 5, (s * 60, 19.9, 1.5), "S", DARK, False, 0.6))
    # side courts at the back corners (wives' quarters, storehouses, armoury)
    for s in (-1, 1):
        m.add(2, courtyard_ring(f"side{s}", 70, 60, 5.0, 11, (s * 66, 82, 1.5), STUCCO_W, DARK, True))
        m.add(2, frame_band(f"sband{s}", 70, 60, 5.7, (s * 66, 82)))
    # the garden with a pool at the back centre
    m.add(2, box("garden", 52, 52, 0.25, (0, 85, 1.5), "#879E6E"))
    m.add(2, water_plate("pool", 22, 14, (0, 85, 1.75), 0.15))
    for i, (tx, ty) in enumerate(((-18, 70), (18, 70), (-18, 100), (18, 100), (0, 104), (-20, 85), (20, 85))):
        m.add(2, tree(f"gt{i}", 2.6, (tx, ty, 1.75), LEAF))
    for i, (tx, ty) in enumerate(((-60, -70), (60, -70), (-60, -30), (60, -30))):
        m.add(2, tree(f"ct{i}", 3.0, (tx, ty, 1.5), LEAF))
    # pillared porticoes with flat roofs along the inner sides of the great court
    for s in (-1, 1):
        px = s * (100 - 15 - 2.5)
        for k in range(24):
            m.add(2, box(f"por{s}{k}", 0.9, 0.9, 5.0, (px, cy - 54 + k * 4.6, 1.5), STUCCO_W))
        m.add(2, box(f"porr{s}", 6.0, 112, 0.6, (s * (100 - 15 - 0.5), cy, 6.5), shade(STUCCO_W, -0.05)))
        m.add(2, frame_band(f"porb{s}", 6.0, 112, 6.2, (s * (100 - 15 - 0.5), cy), OCHRE_RED, 0.3, 0.15))
    m.add(2, stepped_merlons("ringm", 200, 120, 7.5, (0, cy), 0.9, STUCCO_W))
    # gardens and pools in the side courts, a colonnade round the garden pool
    for s in (-1, 1):
        m.add(2, box(f"sg{s}", 46, 36, 0.2, (s * 66, 82, 1.5), "#879E6E"))
        m.add(2, box(f"spr{s}", 18, 11, 0.5, (s * 66, 82, 1.5), STUCCO_G))
        m.add(2, water_plate(f"sp{s}", 16, 9, (s * 66, 82, 1.7), 0.35))
        for k, (dx, dy) in enumerate(((-16, -12), (16, -12), (-16, 12), (16, 12), (0, 14))):
            m.add(2, tree(f"st{s}{k}", 2.4, (s * 66 + dx, 82 + dy, 1.7), LEAF if k % 2 else "#5F7E50"))
        m.add(2, stepped_merlons(f"sidem{s}", 70, 60, 6.5, (s * 66, 82), 0.8, STUCCO_W))
    for k in range(10):
        for (px, py) in ((-14 + k * 3.1, 76), (-14 + k * 3.1, 94)):
            m.add(2, cylinder(f"gcol{k}{py}", 0.4, 3.2, (px, py, 1.75), STUCCO_W, verts=8))
    for py in (76, 94):
        m.add(2, box(f"gcr{py}", 30, 2.4, 0.4, (0, py, 4.95), shade(STUCCO_W, -0.05)))
    for k in range(6):
        m.add(2, box(f"bird{k}", 0.6, 0.35, 0.4, (-8 + k * 3, 84 + (k % 2) * 2, 1.9), ["#F0EEE8", "#D86A7A", "#3E6E9A"][k % 3]))
    for i, (tx, ty) in enumerate(((-24, 62), (24, 62), (-24, 108), (24, 108), (-8, 110), (8, 110))):
        m.add(2, tree(f"gx{i}", 2.2, (tx, ty, 1.75), "#5F7E50"))
    m.add(2, tiers("caltar", 8, 8, 6, 6, 1.6, 1, (0, -50, 1.5), STUCCO_W, OCHRE_RED, 0.2))
    # roof crests on the great court
    m.add(2, frame_band("cband", 200, 120, 6.8, (0, cy), OCHRE_RED, 0.6))
    m.add(2, stepped_merlons("cmer", 120, 15, 12.0, (0, cy - 52.5), 0.9, STUCCO_W))
    m.add(2, frame_band("f2band", 120, 15, 11.2, (0, cy - 52.5)))
    return m


def axayacatl_palace():
    m = Model("axayacatl-palace")
    m.add(0, box("plat", 130, 120, 1.3, (0, 0, 0), STUCCO_G), "platform")
    m.add(0, flight("stair", 24, 0, -61.5, -60, 0, 1.3, 3, STUCCO_W))
    m.add(1, courtyard_ring("court", 120, 80, 5.5, 13, (0, -15, 1.3), STUCCO_W, DARK, True), "courts")
    m.add(1, arch_panel("gate", 6, 4.4, (0, -55.1, 1.3), "S", DARK, False, 0.5))
    m.add(1, arcade("front", 110, 3.8, 18, (0, -55.1, 1.3), "S", DARK, False, 0.35))
    m.add(1, courtyard_ring("inner", 70, 34, 5.0, 10, (-22, 42, 1.3), STUCCO_W, DARK, True))
    m.add(2, frame_band("band", 120, 80, 6.1, (0, -15)), "roofs")
    m.add(2, stepped_merlons("mer", 120, 80, 6.9, (0, -15), 0.8, STUCCO_W))
    m.add(2, frame_band("iband", 70, 34, 5.6, (-22, 42)))
    # the palace's own temple
    t = step_pyramid("tem", 22, 22, 3, 10, (0, 0, 0), STUCCO_W, temple=True, temple_color=STUCCO_W, stair_face="S", roof_color=OCHRE_RED)
    m.add(2, place(t, -90, 40, 42, 1.3), "temple")
    m.add(2, tree("t1", 2.6, (0, -15, 1.3), LEAF))
    m.add(2, tree("t2", 2.2, (-14, -22, 1.3), LEAF))
    return m


def totocalli():
    m = Model("totocalli")
    m.add(0, box("ground", 120, 90, 0.3, (0, 0, 0), "#A9B58A"), "garden")
    pts = [(-60, -45), (60, -45), (60, 45), (-60, 45), (-60, -45)]
    m.add(0, wall_run("wall", pts, 2.4, 1.2, (0, 0, 0), STUCCO_W, towers=False, merlon=None))
    # pools for waterbirds, salt and fresh
    for i, (px, py, pw, pd) in enumerate(((-36, -18, 24, 16), (-8, -22, 18, 12), (-36, 12, 20, 14), (-8, 10, 16, 12))):
        m.add(1, box(f"rim{i}", pw + 1.6, pd + 1.6, 0.6, (px, py, 0.3), STUCCO_G), "pools")
        m.add(1, box(f"pool{i}", pw, pd, 0.5, (px, py, 0.45), LAKE if i % 2 == 0 else "#6A9AA0"))
        for k in range(4):
            m.add(2, box(f"bird{i}{k}", 0.6, 0.35, 0.4, (px - pw * 0.3 + k * pw * 0.2, py + (k % 2 - 0.5) * pd * 0.3, 0.95), ["#F0EEE8", "#D86A7A", "#3E6E9A", "#E0C050"][k]))
    # galleries of cages along the east side, a house of beasts at the back
    m.add(1, box("gallery", 26, 70, 4.5, (40, -2, 0.3), STUCCO_W), "galleries")
    m.add(1, arcade("cages", 66, 3.2, 12, (26.9, -2, 0.3), "W", "#4A3A2A", False, 0.8, 0.3))
    m.add(1, box("beasts", 40, 12, 4.0, (-20, 36, 0.3), STUCCO_W))
    m.add(1, arcade("bcages", 36, 2.8, 8, (-20, 29.9, 0.3), "S", "#4A3A2A", False, 0.8, 0.3))
    m.add(2, box("gband", 26.3, 70.3, 0.5, (40, -2, 4.8), OCHRE_RED), "roofs")
    m.add(2, box("bband", 40.3, 12.3, 0.5, (-20, 36, 4.3), OCHRE_RED))
    for i, (tx, ty) in enumerate(((-52, -38), (-52, 0), (-52, 38), (12, 34), (12, -38), (-22, -3), (5, -5))):
        m.add(2, tree(f"t{i}", 2.6, (tx, ty, 0.3), LEAF))
    return m


# ---------------------------------------------------------------- Tlatelolco

GOODS = ["#D9B44A", "#B23A2A", "#F1EBDD", "#C77A3E", "#7D9A6C", "#8C5A3C", "#3E3A38", "#E8D9A0", "#5F8A5A", "#A65238", "#D4AE55", "#6B4F7A"]


def tlatelolco_market(stage="1519"):
    m = Model("tlatelolco-market-" + stage)
    W, D = 220, 200
    full = stage == "1519"
    m.add(0, box("pave", W, D, 0.2, (0, 0, 0), PAVE if full else EARTH), "plaza")
    # a canal landing along the east edge
    m.add(0, water_plate("canal", 10, D, (W / 2 - 5, 0, 0.0), 0.3))
    for i, cy in enumerate((-70, -40, 10, 45, 80)):
        m.add(2, canoe(f"cn{i}", 7, (W / 2 - 5, cy, 0.3), 90, WOOD, GOODS[i % len(GOODS)]))
    if full:
        # arcades round three sides
        for i, (ax, ay, aw, ad, face) in enumerate(((0, -D / 2 + 5, W - 30, 10, "N"), (0, D / 2 - 5, W - 30, 10, "S"), (-W / 2 + 5, 0, 10, D - 30, "E"))):
            m.add(1, box(f"arc{i}", aw, ad, 4.6, (ax, ay, 0.2), STUCCO_W), "arcades")
            off = {"N": (0, ad / 2), "S": (0, -ad / 2), "E": (aw / 2, 0)}[face]
            m.add(1, arcade(f"arcp{i}", (aw if face in ("N", "S") else ad) * 0.96, 3.6, int((aw if face in ("N", "S") else ad) / 5), (ax + off[0] * 1.01, ay + off[1] * 1.01, 0.2), face, DARK, False, 0.75, 0.3))
            m.add(1, box(f"arcb{i}", aw + 0.3, ad + 0.3, 0.4, (ax, ay, 4.1), OCHRE_RED))
            m.add(1, stepped_merlons(f"arcm{i}", aw, ad, 4.8, (ax, ay), 1.4, STUCCO_W))
    # rows of stalls, each kind of goods in its own street
    x0, x1 = -W / 2 + (16 if full else 8), W / 2 - 16
    y0, y1 = -D / 2 + (16 if full else 8), D / 2 - (16 if full else 8)
    rowstep, stallstep = 8.0, 4.6
    r = 0
    y = y0
    count = 0
    while y < y1:
        if abs(y) < 7:                       # the main cross street
            y += rowstep
            continue
        x = x0
        g = GOODS[r % len(GOODS)]
        aw = CLOTH if r % 3 else MAT
        k = 0
        while x < x1:
            if abs(x + 10) < 7 or (full and abs(x - 52) < 16 and abs(y + 50) < 14):   # cross street, judges' house
                x += stallstep
                k += 1
                continue
            if full or (k + r) % 3 == 0:
                m.add(1 if count % 2 else 2, stall(f"s{r}_{k}", (x, y, 0.2), shade(g, ((k * 7) % 5 - 2) * 0.05), aw, 0, (k + r) % 3 == 0), "stalls" if count == 0 else None)
                count += 1
            x += stallstep
            k += 1
        y += rowstep
        r += 1
    if full:
        # the judges' house and a small market shrine
        m.add(2, box("jplat", 30, 20, 1.2, (52, -50, 0.2), STUCCO_G), "court")
        m.add(2, box("judges", 24, 14, 4.2, (52, -48, 1.4), STUCCO_W))
        m.add(2, arcade("jarc", 20, 3.0, 5, (52, -55.1, 1.4), "S", DARK, False, 0.6))
        m.add(2, box("jband", 24.3, 14.3, 0.4, (52, -48, 4.9), OCHRE_RED))
        m.add(2, stepped_merlons("jmer", 24, 14, 5.6, (52, -48), 0.7, STUCCO_W))
    # porters arriving from the canal landing and crossing the market streets
    for i in range(26 if full else 10):
        px = (W / 2 - 14) - (i % 6) * 2.2 if i < 8 else -90 + (i * 37) % 170
        py = -60 + (i * 23) % 120 if i < 8 else (2.5 if i % 2 else -2.5)
        m.add(2, porter(f"por{i}", (px, py, 0.2), 90 if i >= 8 and i % 2 else -90, GOODS[(i * 5) % len(GOODS)]))
    t = step_pyramid("mshrine", 9, 9, 2, 4.5, (0, 0, 0), STUCCO_W, temple=True, temple_color=STUCCO_W, stair_face="S", roof_color=OCHRE_RED)
    m.add(2, place(t, 0, -10, 0, 0.2))
    return m


def tlatelolco_temple(stage="1519"):
    """The walled precinct of Tlatelolco: facade (-Y) toward the west once rotated; the pyramid at the back (east)."""
    m = Model("tlatelolco-temple-" + stage)
    W, D = 200, 230
    if stage == "early":
        m.add(0, box("ground", W, D, 0.2, (0, 0, 0), EARTH), "ground")
        m.add(0, box("plaza", 90, 110, 0.3, (0, 20, 0), "#C8B48E"))
        m.add(1, tiers("pyr", 32, 28, 20, 16, 10, 3, (0, 45, 0.3), "#D8CCB0", shade("#D8CCB0", -0.18), 0.6), "temple")
        m.add(1, flight("stair", 10, 0, 26, 37.5, 0.3, 10.3, 14, "#E2D8C0"))
        for s in (-1, 1):
            m.add(2, shrine(f"sh{s}", 7, 6, 3.6, (s * 4.6, 47, 10.3), "#E6DCC6", OCHRE_RED if s > 0 else TLALOC_BLUE, 4.0, None, None, None, thatch=True), "shrines")
        for i, (hx, hy) in enumerate(((-60, -40), (-55, 70), (60, 75), (62, -30), (-20, -80), (30, -85))):
            m.add(2, house_block(f"hut{i}", 9, 6, 2.8, (hx, hy, 0.2), "#CDB892", "S", False))
            m.add(2, cylinder(f"hutr{i}", 5.8, 2.8, (hx, hy, 3.0), THATCH, verts=4, r_top=0.2))
        return m
    m.add(0, box("pave", W, D, 0.25, (0, 0, 0), PAVE), "paving")
    pts = [(-W / 2, -D / 2), (-8, -D / 2)]
    m.add(0, wall_run("wallS1", [(-W / 2, -D / 2), (-8, -D / 2)], 2.8, 2.0, (0, 0, 0), STUCCO_W, towers=False, merlon=None))
    m.add(0, wall_run("wallS2", [(8, -D / 2), (W / 2, -D / 2)], 2.8, 2.0, (0, 0, 0), STUCCO_W, towers=False, merlon=None))
    m.add(0, wall_run("wallR", [(W / 2, -D / 2), (W / 2, D / 2), (-W / 2, D / 2), (-W / 2, -D / 2)], 2.8, 2.0, (0, 0, 0), STUCCO_W, towers=False, merlon=None))
    for s in (-1, 1):
        m.add(0, box(f"gp{s}", 3.5, 3.5, 4.8, (s * 9.5, -D / 2, 0), STUCCO_G))
    # the twin-temple pyramid at the back, stairs toward the plaza
    yc, W0, D0, W1, D1, H = 55, 60, 56, 36, 28, 24.0
    m.add(1, tiers("pyr", W0, D0, W1, D1, H, 4, (0, yc, 0.25), STUCCO_W, shade(STUCCO_W, -0.16), 0.8), "pyramid")
    yfront, ytop = yc - D0 / 2 - 8, yc - D1 / 2 + 0.5
    sw = W0 * 0.19
    for s in (-1, 1):
        xs = s * (sw / 2 + 1.4)
        m.add(1, flight(f"stair{s}", sw, xs, yfront, ytop, 0.25, 0.25 + H, 28, shade(STUCCO_W, 0.04)))
        m.add(1, alfarda(f"alfo{s}", s * (sw + 2.2), 1.4, yfront, ytop, 0.25, 0.25 + H, STUCCO_G))
    m.add(1, alfarda("alfm", 0, 2.6, yfront, ytop, 0.25, 0.25 + H, STUCCO_G))
    zt = 0.25 + H
    m.add(2, shrine("huitz", 12, 13, 6.0, (W1 * 0.24, yc + 3, zt), STUCCO_W, OCHRE_RED, 6.5, OCHRE_RED, None, SKULL), "shrines")
    m.add(2, shrine("tlaloc", 12, 13, 6.0, (-W1 * 0.24, yc + 3, zt), STUCCO_W, TLALOC_BLUE, 6.5, TLALOC_BLUE, TLALOC_BLUE, SKULL))
    # the round temple in front, on the axis, and the calendar temple
    m.add(2, tiers("rplat", 22, 22, 18, 18, 3.0, 2, (0, -30, 0.25), STUCCO_W, OCHRE_RED, 0.3), "temples")
    m.add(2, flight("rstair", 7, 0, -43, -39.5, 0.25, 3.25, 6, STUCCO_W))
    m.add(2, cylinder("rcella", 5.5, 5.0, (0, -28, 3.25), STUCCO_W, verts=24))
    m.add(2, cylinder("rroof", 6.6, 6.0, (0, -28, 8.25), THATCH, verts=24, r_top=0.3))
    m.add(2, arch_panel("rdoor", 2.2, 3.0, (0, -33.4, 3.25), "S", DARK, False, 0.3))
    cal = step_pyramid("cal", 14, 14, 2, 5, (0, 0, 0), STUCCO_W, temple=True, temple_color=STUCCO_W, stair_face="S", roof_color=JADE)
    m.add(2, place(cal, 0, -55, -10, 0.25))
    # priests' houses along the side walls
    for i, (hx, hy, hw, hd, face) in enumerate(((-92, 0, 10, 150, "E"), (92, 0, 10, 150, "W"), (-55, 108, 70, 9, "S"), (55, 108, 70, 9, "S"))):
        m.add(2, house_block(f"pr{i}", hw, hd, 3.6, (hx, hy, 0.25), STUCCO_W, face))
        m.add(2, box(f"prb{i}", hw + 0.3, hd + 0.3, 0.35, (hx, hy, 3.4), OCHRE_RED))
    for i, (ax, ay) in enumerate(((30, -60), (-30, -75), (40, 0))):
        m.add(2, box(f"alt{i}", 3, 3, 1.3, (ax, ay, 0.25), STUCCO_G))
    return m


# ---------------------------------------------------------------- causeways and water works

def xoloc():
    m = Model("xoloc")
    m.add(0, water_plate("lake", 50, 36, (0, 0, 0)), "water")
    m.add(0, box("cw_n", 12, 22, 1.2, (0, 7, 0), EARTH), "causeway")
    m.add(0, box("cw_s", 12, 7, 1.2, (0, -14.5, 0), EARTH))
    # the fort: a wall across the causeway with two towers and a gate
    m.add(1, box("wallw", 18, 4, 4.0, (-13, 2, 1.0), STUCCO_W), "fort")
    m.add(1, box("walle", 18, 4, 4.0, (13, 2, 1.0), STUCCO_W))
    for s in (-1, 1):
        m.add(1, box(f"tw{s}", 7, 7, 8.5, (s * 6.5, 2, 1.0), STUCCO_W))
        m.add(1, stepped_merlons(f"twm{s}", 7, 7, 9.5, (s * 6.5, 2), 0.8, STUCCO_W))
        m.add(1, box(f"twb{s}", 7.3, 7.3, 0.5, (s * 6.5, 2, 8.4), OCHRE_RED))
        m.add(1, stepped_merlons(f"wm{s}", 18, 4, 5.0, (s * 13, 2), 0.7, STUCCO_W))
        m.add(1, box(f"wb{s}", 18.3, 4.3, 0.4, (s * 13, 2, 4.3), OCHRE_RED))
    m.add(1, box("lintel", 6.5, 4.4, 1.6, (0, 2, 5.6), STUCCO_W))
    m.add(1, arch_panel("gate", 5.5, 4.4, (0, -0.1, 1.2), "S", DARK, False, 0.4))
    # a gap in the causeway in front, spanned by a timber drawbridge
    for i in range(7):
        m.add(2, box(f"plank{i}", 1.3, 4.2, 0.35, (-4.2 + i * 1.4, -9, 0.9), WOOD), "bridge")
    for s in (-1, 1):
        m.add(2, box(f"bpost{s}", 0.5, 0.5, 3.0, (s * 5.6, -6.8, 1.0), WOOD))
    m.add(2, canoe("c1", 7, (-14, -9, 0.1), 15, WOOD, "#D9B44A"))
    m.add(2, canoe("c2", 6, (16, -12, 0.1), -20, WOOD))
    m.add(2, canoe("c3", 6.5, (-17, 12, 0.1), 80, WOOD, CLOTH))
    return m


def toltec_bridge():
    m = Model("toltec-bridge")
    m.add(0, box("land_w", 9, 24, 1.0, (-11.5, 0, 0), EARTH), "banks")
    m.add(0, box("land_e", 9, 24, 1.0, (11.5, 0, 0), EARTH))
    m.add(0, water_plate("canal", 14, 24, (0, 0, 0), 0.3))
    for s in (-1, 1):
        m.add(0, box(f"rev{s}", 0.8, 24, 1.3, (s * 7.2, 0, 0), CHILUCA))
        m.add(0, box(f"road{s}", 9, 8, 0.15, (s * 11.5, 0, 1.0), "#C9B48A"))
    # the deck of heavy beams that could be pulled away
    for i in range(6):
        m.add(1, box(f"beam{i}", 15.5, 1.1, 0.6, (0, -2.75 + i * 1.1, 1.0), WOOD), "bridge")
    for s in (-1, 1):
        m.add(1, box(f"sill{s}", 1.0, 7.5, 0.5, (s * 7.5, 0, 1.0), shade(WOOD, -0.2)))
    # small guard platforms with a brazier and a lookout post
    for s in (-1, 1):
        m.add(2, box(f"gpl{s}", 4, 3.5, 1.2, (s * 11, -7.5 * s, 1.0), STUCCO_W), "guards")
        m.add(2, cylinder(f"gbr{s}", 0.6, 0.8, (s * 11, -7.5 * s, 2.2), OCHRE_RED, verts=8, r_top=0.8))
        m.add(2, box(f"gpo{s}", 0.3, 0.3, 4.0, (s * 12.5, 7.5 * s, 1.0), WOOD))
    m.add(2, canoe("c1", 6, (0, -8.5, 0.1), 90, WOOD, "#C77A3E"))
    m.add(2, canoe("c2", 5.5, (1.5, 8.5, 0.1), 95, WOOD))
    return m


def aqueduct(stage="1519"):
    """A stretch of the Tlacopan causeway in the lake, the aqueduct beside it (-Y side), a gap with a timber bridge."""
    m = Model("aqueduct-" + stage)
    L = 140
    if stage == "1620":
        m.add(0, box("ground", L, 34, 0.2, (0, 0, 0), "#9FAE86"), "ground")
        m.add(0, box("road", L, 11, 0.5, (0, 8, 0.2), "#C9B48A"))
        n = 28
        for i in range(n):
            px = -L / 2 + L * (i + 0.5) / n
            m.add(1, box(f"pier{i}", 1.6, 2.4, 4.2, (px, -7, 0.2), CHILUCA), "arcade")
        m.add(1, box("spandrel", L, 2.4, 1.4, (0, -7, 4.4), CHILUCA))
        m.add(1, arcade("arches_s", L, 4.0, n, (0, -8.25, 0.2), "S", DARK, False, 0.66, 0.2))
        m.add(1, arcade("arches_n", L, 4.0, n, (0, -5.75, 0.2), "N", DARK, False, 0.66, 0.2))
        m.add(2, box("channel", L, 2.6, 0.5, (0, -7, 5.8), shade(CHILUCA, -0.08)), "channel")
        m.add(2, box("water", L, 1.4, 0.1, (0, -7, 6.3), LAKE))
        for i, tx in enumerate((-55, -20, 25, 60)):
            m.add(2, tree(f"t{i}", 2.4, (tx, 14.5, 0.2), LEAF))
        return m
    m.add(0, water_plate("lake", L, 34, (0, 0, 0)), "water")
    gap = (20, 30)
    for i, (a, b) in enumerate(((-L / 2, gap[0]), (gap[1], L / 2))):
        cx, w = (a + b) / 2, b - a
        m.add(0, box(f"road{i}", w, 10, 1.4, (cx, 8, 0), EARTH), "causeway")
        m.add(0, box(f"rface{i}", w, 0.6, 1.5, (cx, 2.7, 0), CHILUCA))
        # the aqueduct embankment with twin channels on top
        m.add(1, box(f"dike{i}", w, 4.6, 1.9, (cx, -6, 0), CHILUCA), "aqueduct")
        for k, dy in enumerate((-2.1, 0, 2.1)):
            m.add(1, box(f"lip{i}{k}", w, 0.4, 0.6, (cx, -6 + dy, 1.9), shade(CHILUCA, -0.1)))
        for k, dy in enumerate((-1.05, 1.05)):
            m.add(1, box(f"wat{i}{k}", w, 1.6, 0.4, (cx, -6 + dy, 1.9), LAKE))
    # the gap: beams across for the road, a wooden trough for the water
    for k in range(7):
        m.add(2, box(f"beam{k}", gap[1] - gap[0] + 2, 1.3, 0.5, ((gap[0] + gap[1]) / 2, 4 + k * 1.35, 1.0), WOOD), "bridge")
    m.add(2, box("trough", gap[1] - gap[0] + 2, 2.2, 0.8, ((gap[0] + gap[1]) / 2, -6, 1.5), WOOD))
    m.add(2, box("trough_w", gap[1] - gap[0] + 2, 1.4, 0.1, ((gap[0] + gap[1]) / 2, -6, 2.25), LAKE))
    for s in (-1, 1):
        m.add(2, box(f"tpost{s}", 0.5, 0.5, 1.5, ((gap[0] + gap[1]) / 2 + s * 3, -6, 0), WOOD))
    # water-sellers' canoes under the trough, and canoes in the lake
    m.add(2, canoe("ws1", 6, (25, -11, 0.1), 0, WOOD, "#C77A3E"))
    m.add(2, canoe("ws2", 5.5, (24, -15, 0.1), 10, WOOD, "#C77A3E"))
    m.add(2, canoe("c3", 7, (-40, -13, 0.1), 5, WOOD, MAT))
    m.add(2, canoe("c4", 6.5, (50, 15, 0.1), -8, WOOD))
    return m


def dike():
    """A stretch of the dike of Nezahualcoyotl along Y; the salt lake on the east (+X), a sluice gate in the middle."""
    m = Model("dike")
    L = 300
    m.add(0, water_plate("lake", 24, L, (0, 0, 0)), "water")
    for i, (a, b) in enumerate(((-L / 2, -4), (4, L / 2))):
        cy, l = (a + b) / 2, b - a
        m.add(0, frustum(f"emb{i}", 16, l, 11, l, 2.4, (0, cy, 0), EARTH), "embankment")
        m.add(1, box(f"face{i}", 1.0, l, 2.0, (7.6, cy, 0), CHILUCA), "facing")
        m.add(1, box(f"path{i}", 5, l, 0.12, (0, cy, 2.4), "#C9B48A"))
        n = int(l / 3)
        for k in range(n):
            yy = a + (k + 0.5) * l / n
            for s in (-1, 1):
                m.add(1, cylinder(f"stk{i}_{k}{s}", 0.22, 3.0, (s * 8.6, yy, 0), WOOD, verts=5))
    # the sluice: posts, a beam and a gate of planks, a guard hut
    for s in (-1, 1):
        m.add(2, box(f"spost{s}", 1.2, 1.2, 4.2, (s * 5.5, s * 4.6, 0), WOOD), "sluice")
        m.add(2, box(f"spier{s}", 11, 1.6, 2.6, (0, s * 4.8, 0), CHILUCA))
    m.add(2, box("sbeam", 12, 0.8, 0.7, (0, 0, 3.6), WOOD))
    m.add(2, box("sgate", 9, 0.4, 1.6, (0, 0, 1.0), shade(WOOD, -0.2)))
    m.add(2, house_block("hut", 5, 4, 2.6, (0, 20, 2.4), STUCCO_W, "W"))
    m.add(2, cylinder("hutr", 3.5, 2.0, (0, 20, 5.0), THATCH, verts=4, r_top=0.2))
    m.add(2, canoe("c1", 6.5, (-9, -12, 0.1), 80, WOOD, REED))
    m.add(2, canoe("c2", 6, (9.5, 40, 0.1), 95, WOOD))
    m.add(2, canoe("c3", 6, (-9.5, 70, 0.1), 85, WOOD, MAT))
    return m


# ---------------------------------------------------------------- the Spanish city

def cathedral_1620():
    """The first cathedral (east-west, facade west) in the south, the new cathedral rising behind it (facade toward -Y)."""
    m = Model("cathedral-1620")
    m.add(0, box("atrium", 70, 130, 0.25, (0, 0, 0), PAVE), "atrium")
    # the old cathedral: a low timber-roofed nave with a small tower
    m.add(1, box("old", 50, 14, 11, (0, -48, 0.25), STUCCO_W), "old church")
    m.add(1, place(gable_roof("oldr", 14, 50, 4.5, (0, 0, 0), TILE_RED, 0.5), 90, 0, -48, 11.25))
    for i in range(5):
        m.add(1, arch_panel(f"oldw{i}", 1.4, 3.2, (-18 + i * 9, -55.05, 5.5), "S", DARK, False, 0.3))
    m.add(1, box("oldfac", 1.4, 15, 14, (-25.4, -48, 0.25), CHILUCA))
    m.add(1, arch_panel("olddoor", 3.2, 5.0, (-26.2, -48, 0.25), "W", DARK, False, 0.4))
    m.add(1, box("oldtw", 6, 6, 18, (-22, -38, 0.25), CHILUCA))
    m.add(1, box("oldbel", 5, 5, 4.5, (-22, -38, 18.25), CHILUCA))
    for f, (dx, dy) in (("S", (0, -2.5)), ("W", (-2.5, 0)), ("N", (0, 2.5)), ("E", (2.5, 0))):
        m.add(1, arch_panel(f"oldba{f}", 1.6, 2.8, (-22 + dx, -38 + dy, 18.6), f, DARK, False, 0.3))
    m.add(1, cylinder("oldcap", 3.4, 3.0, (-22, -38, 22.75), TILE_RED, verts=4, r_top=0.1))
    # the new cathedral under construction: outer walls, chapels and the first piers, no vaults yet
    ny0, ny1, nw = -28, 64, 58
    m.add(0, box("found", nw + 4, ny1 - ny0 + 4, 1.2, (0, (ny0 + ny1) / 2, 0.25), CHILUCA), "foundations")
    for s in (-1, 1):
        m.add(2, box(f"nwall{s}", 2.4, ny1 - ny0, 16, (s * (nw / 2 - 1.2), (ny0 + ny1) / 2, 1.45), CHILUCA), "new cathedral")
        n = 8
        for k in range(n):
            yy = ny0 + (ny1 - ny0) * (k + 0.5) / n
            m.add(2, box(f"nbut{s}{k}", 2.6, 2.4, 13 - (k % 3), (s * (nw / 2 + 1.3), yy, 1.45), shade(CHILUCA, -0.06)))
            m.add(2, arch_panel(f"nwin{s}{k}", 3.0, 6.0, (s * nw / 2, yy, 6.0), "E" if s > 0 else "W", DARK, True, 0.3))
        for k in range(1, 7):
            for c in (-1, 1):
                yy = ny0 + (ny1 - ny0) * k / 7
                hgt = 14 if k > 2 else 8
                m.add(2, box(f"pier{s}{k}{c}", 2.2, 2.2, hgt, (c * (nw * 0.17 if s < 0 else nw * 0.34), yy, 1.45), CHILUCA))
    m.add(2, box("apsew", nw, 2.4, 18, (0, ny1 - 1.2, 1.45), CHILUCA))
    for s in (-1, 1):
        m.add(2, box(f"ntower{s}", 14, 14, 9 - 3 * s, (s * (nw / 2 - 7), ny0 + 7, 1.45), CHILUCA))
    # scaffolding and a crane at the work face
    for k in range(4):
        m.add(2, box(f"scaf{k}", 0.3, 0.3, 18, (-nw / 2 + 4 + k * 3, 40, 1.45), WOOD))
    m.add(2, box("scafd", 12, 1.6, 0.3, (-nw / 2 + 8.5, 40, 12), WOOD))
    m.add(2, box("crane", 0.5, 0.5, 22, (8, 30, 1.45), WOOD))
    m.add(2, box("jib", 0.4, 14, 0.4, (8, 24, 23), WOOD))
    m.add(2, box("stones", 10, 6, 1.4, (18, -14, 1.45), CHILUCA))
    return m


def viceregal_palace():
    """Facade on -Y (west onto the Plaza Mayor once rotated): two storeys, corner towers, several patios."""
    m = Model("viceregal-palace")
    W, D = 210, 230
    m.add(0, box("ground", W, D, 0.3, (0, 0, 0), PAVE), "ground")
    m.add(1, colonial_range("front", 196, 18, 13, (0, -D / 2 + 12, 0.3), STUCCO, TEZONTLE, 2, "S", False, True, 1.3), "ranges")
    for s in (-1, 1):
        m.add(1, colonial_range(f"side{s}", 18, 190, 11, (s * (W / 2 - 12), 8, 0.3), STUCCO, TEZONTLE, 2, "W" if s < 0 else "E", False, True, 1.3))
    m.add(1, colonial_range("back", 160, 16, 10, (0, D / 2 - 14, 0.3), STUCCO, TEZONTLE, 2, "N", False, True, 1.3))
    for k, yy in enumerate((-35, 45)):
        m.add(1, colonial_range(f"cross{k}", 160, 14, 11, (0, yy, 0.3), STUCCO, TEZONTLE, 2, "S", False, True, 1.3))
    m.add(1, colonial_range("spine", 14, 66, 11, (0, 5, 0.3), STUCCO, TEZONTLE, 2, "E", False, True, 1.3))
    # inner arcades round the main patio
    m.add(2, arcade("pat_n", 150, 4.5, 20, (0, -42.1, 0.3), "S", DARK, True, 0.7, 0.3), "patios")
    m.add(2, arcade("pat_s", 150, 4.5, 20, (0, -D / 2 + 21.1, 0.3), "N", DARK, True, 0.7, 0.3))
    # the main portal and corner towers with battlements
    m.add(2, box("portal", 12, 2.0, 15, (0, -D / 2 + 2.0, 0.3), TEZONTLE), "towers")
    m.add(2, arch_panel("pdoor", 5, 7.5, (0, -D / 2 + 0.9, 0.3), "S", DARK, False, 0.4))
    m.add(2, box("balcony", 8, 1.6, 0.5, (0, -D / 2 + 0.6, 8.0), DARK))
    for i, (tx, ty) in enumerate(((-W / 2 + 10, -D / 2 + 10), (W / 2 - 10, -D / 2 + 10), (-W / 2 + 10, D / 2 - 12), (W / 2 - 10, D / 2 - 12))):
        m.add(2, box(f"tw{i}", 16, 16, 17, (tx, ty, 0.3), CHILUCA))
        m.add(2, merlons(f"twm{i}", 16, 16, 17.3, 1.0, 1.0, CHILUCA))
        m.stages[2][-1] = move(m.stages[2][-1], tx, ty, 0)
    # a fountain in the main patio
    m.add(2, cylinder("fount", 3.0, 0.9, (0, -78, 0.3), CHILUCA, verts=16))
    m.add(2, cylinder("fountc", 0.6, 2.2, (0, -78, 1.2), CHILUCA, verts=8))
    for i, (tx, ty) in enumerate(((-40, 80), (-60, 75), (-30, 70))):
        m.add(2, tree(f"t{i}", 2.6, (tx, ty, 0.3), LEAF))
    return m


def plaza_mayor(stage="1620"):
    m = Model("plaza-mayor-" + stage)
    W, D = 175, 190
    if stage == "1519":
        m.add(0, box("pave", W, D, 0.2, (0, 0, 0), PAVE), "square")
        m.add(1, box("curb", W, 1.0, 0.5, (0, -D / 2 + 0.5, 0.2), STUCCO_G), "curb")
        m.add(1, box("curbw", 1.0, D, 0.5, (-W / 2 + 0.5, 0, 0.2), STUCCO_G))
        m.add(2, tiers("altar", 10, 10, 8, 8, 2.0, 1, (20, 30, 0.2), STUCCO_W, OCHRE_RED, 0.2), "altars")
        m.add(2, cylinder("pole", 0.35, 14, (-30, 10, 0.2), WOOD, verts=6))
        m.add(2, box("plat", 14, 10, 1.0, (-30, -40, 0.2), STUCCO_W))
        for i in range(8):
            m.add(2, stall(f"s{i}", (-60 + (i % 4) * 5, -70 + (i // 4) * 8, 0.2), GOODS[i], MAT))
        return m
    m.add(0, box("pave", W, D, 0.2, (0, 0, 0), "#CFC2A6"), "square")
    # the portals: arcaded two-storey ranges on the west (merchants) and south (city hall) sides
    m.add(1, colonial_range("portal_w", 16, D - 20, 11, (-W / 2 + 8, 5, 0.2), STUCCO, TEZONTLE, 2, "E", True, False), "portales")
    m.add(1, colonial_range("cabildo", W - 20, 16, 12, (10, -D / 2 + 8, 0.2), STUCCO, TEZONTLE, 2, "N", True, True))
    # wooden shops (cajones) and Indian stalls under mats
    for r in range(4):
        for k in range(9):
            m.add(2, box(f"caj{r}{k}", 4.5, 3.5, 2.8, (-40 + k * 6, 40 - r * 9, 0.2), WOOD), "market")
            m.add(2, box(f"cajr{r}{k}", 5.0, 4.0, 0.25, (-40 + k * 6, 40 - r * 9, 3.0), shade(WOOD, -0.2)))
    n = 0
    for r in range(5):
        for k in range(12):
            if (r * 12 + k) % 4 == 3:
                continue
            m.add(2, stall(f"st{r}{k}", (-50 + k * 6.5, -18 - r * 8, 0.2), GOODS[(r + k) % len(GOODS)], MAT if (r + k) % 2 else CLOTH))
            n += 1
    # the fountain, the gallows and the pillory
    m.add(2, cylinder("fbasin", 4.5, 1.0, (30, 10, 0.2), CHILUCA, verts=20))
    m.add(2, cylinder("fwater", 4.0, 0.1, (30, 10, 1.2), LAKE, verts=20))
    m.add(2, cylinder("fcol", 0.7, 3.5, (30, 10, 0.2), CHILUCA, verts=8))
    for s in (-1, 1):
        m.add(2, box(f"gal{s}", 0.5, 0.5, 5.0, (55 + s * 2, -60, 0.2), WOOD))
    m.add(2, box("galb", 5, 0.5, 0.5, (55, -60, 5.2), WOOD))
    m.add(2, cylinder("pillory", 0.6, 4.0, (45, 60, 0.2), CHILUCA, verts=8))
    return m


def san_francisco():
    """The Franciscan convent: atrium with posas at the front (-Y, west once rotated), church, open chapel, cloister."""
    m = Model("san-francisco")
    W, D = 170, 150
    m.add(0, box("ground", W, D, 0.25, (0, 0, 0), "#B9AE90"), "ground")
    m.add(0, box("atrium", 150, 60, 0.15, (0, -42, 0.25), PAVE))
    pts = [(-75, -12), (-75, -72), (75, -72), (75, -12)]
    m.add(1, wall_run("awall1", [(-75, -12), (-75, -72), (-6, -72)], 2.4, 1.0, (0, 0, 0), STUCCO, towers=False, merlon="box"), "atrium")
    m.add(1, wall_run("awall2", [(6, -72), (75, -72), (75, -12)], 2.4, 1.0, (0, 0, 0), STUCCO, towers=False, merlon="box"))
    for i, (px, py) in enumerate(((-70, -67), (70, -67), (-70, -17), (70, -17))):
        m.add(1, box(f"posa{i}", 6, 6, 4.5, (px, py, 0.25), STUCCO))
        m.add(1, cylinder(f"posar{i}", 4.6, 2.6, (px, py, 4.75), TEZONTLE, verts=4, r_top=0.2))
        m.stages[1][-1].rotation_euler[2] = math.pi / 4
    m.add(1, box("crossb", 2.5, 2.5, 1.5, (0, -42, 0.25), CHILUCA))
    m.add(1, box("cross", 0.5, 0.5, 6, (0, -42, 1.75), CHILUCA))
    m.add(1, box("crossa", 2.8, 0.5, 0.5, (0, -42, 6.0), CHILUCA))
    # the church (facade toward the atrium), with a tower
    m.add(2, colonial_church("church", 70, 16, 15, (-35, 23, 0.25), CHILUCA, TEZONTLE, 1, 5.5), "church")
    # the open chapel of San José de los Naturales
    m.add(2, box("capilla", 40, 14, 9, (25, -4, 0.25), STUCCO), "chapel")
    m.add(2, arcade("capa", 38, 7.5, 7, (25, -11.1, 0.25), "S", DARK, False, 0.8, 0.4))
    m.add(2, box("capr", 40.4, 14.4, 0.6, (25, -4, 9.25), shade(STUCCO, -0.06)))
    # the cloister and convent ranges
    m.add(2, courtyard_ring("cloister", 46, 42, 9, 9, (25, 34, 0.25), STUCCO, DARK, True), "convent")
    m.add(2, frame_band("clr", 46, 42, 8.6, (25, 34), shade(STUCCO, -0.1), 0.6))
    m.add(2, colonial_range("school", 14, 40, 8, (70, 30, 0.25), STUCCO, TEZONTLE, 2, "W", False, False))
    for i, (tx, ty) in enumerate(((-70, 60), (-58, 66), (60, 66), (72, 58), (-10, 66), (5, 62))):
        m.add(2, tree(f"t{i}", 2.6, (tx, ty, 0.25), LEAF))
    return m


def santa_cruz_tlatelolco():
    """Santiago Tlatelolco and the Colegio de Santa Cruz: church facade toward -Y (west once rotated)."""
    m = Model("santa-cruz-tlatelolco")
    W, D = 110, 100
    m.add(0, box("ground", W, D, 0.25, (0, 0, 0), "#B9AE90"), "ground")
    m.add(0, box("atrium", 70, 26, 0.15, (-12, -36, 0.25), PAVE))
    m.add(1, wall_run("awall", [(-47, -24), (-47, -49), (-16, -49)], 2.2, 0.9, (0, 0, 0), STUCCO, towers=False, merlon="box"), "atrium")
    m.add(1, wall_run("awall2", [(-8, -49), (23, -49), (23, -24)], 2.2, 0.9, (0, 0, 0), STUCCO, towers=False, merlon="box"))
    m.add(1, box("cross", 0.5, 0.5, 5, (-12, -38, 0.4), CHILUCA))
    m.add(1, box("crossa", 2.4, 0.5, 0.5, (-12, -38, 4.2), CHILUCA))
    m.add(2, colonial_church("church", 60, 16, 15, (-26, 7, 0.25), CHILUCA, TEZONTLE, 1, 0), "church")
    m.add(2, courtyard_ring("convent", 34, 32, 8, 8, (14, 18, 0.25), STUCCO, DARK, True), "colegio")
    m.add(2, frame_band("convr", 34, 32, 7.6, (14, 18), shade(STUCCO, -0.1), 0.6))
    m.add(2, courtyard_ring("colegio", 36, 28, 7.5, 8, (36, -20, 0.25), STUCCO, DARK, True))
    m.add(2, frame_band("colr", 36, 28, 7.1, (36, -20), shade(STUCCO, -0.1), 0.6))
    for i, (tx, ty) in enumerate(((44, 42), (30, 44), (-46, 40), (50, 10))):
        m.add(2, tree(f"t{i}", 2.4, (tx, ty, 0.25), LEAF))
    return m


BUILDERS = {
    "tenochtitlan/templo-mayor": lambda: templo_mayor("1519"),
    "tenochtitlan/templo-mayor-1350": lambda: templo_mayor("1350"),
    "tenochtitlan/templo-mayor-1440": lambda: templo_mayor("1440"),
    "tenochtitlan/templo-mayor-1620": lambda: templo_mayor("1620"),
    "tenochtitlan/sacred-precinct": lambda: sacred_precinct("1519"),
    "tenochtitlan/sacred-precinct-1440": lambda: sacred_precinct("1440"),
    "tenochtitlan/temple-of-ehecatl": temple_of_ehecatl,
    "tenochtitlan/huey-tzompantli": huey_tzompantli,
    "tenochtitlan/ballcourt": ballcourt_precinct,
    "tenochtitlan/calmecac": calmecac,
    "tenochtitlan/house-of-eagles": house_of_eagles,
    "tenochtitlan/moctezuma-palace": moctezuma_palace,
    "tenochtitlan/axayacatl-palace": axayacatl_palace,
    "tenochtitlan/totocalli": totocalli,
    "tenochtitlan/tlatelolco-market": lambda: tlatelolco_market("1519"),
    "tenochtitlan/tlatelolco-market-1440": lambda: tlatelolco_market("1440"),
    "tenochtitlan/tlatelolco-temple": lambda: tlatelolco_temple("1519"),
    "tenochtitlan/tlatelolco-temple-early": lambda: tlatelolco_temple("early"),
    "tenochtitlan/xoloc": xoloc,
    "tenochtitlan/toltec-bridge": toltec_bridge,
    "tenochtitlan/aqueduct": lambda: aqueduct("1519"),
    "tenochtitlan/aqueduct-1620": lambda: aqueduct("1620"),
    "tenochtitlan/dike": dike,
    "tenochtitlan/cathedral-1620": cathedral_1620,
    "tenochtitlan/viceregal-palace": viceregal_palace,
    "tenochtitlan/plaza-mayor": lambda: plaza_mayor("1620"),
    "tenochtitlan/plaza-1519": lambda: plaza_mayor("1519"),
    "tenochtitlan/san-francisco": san_francisco,
    "tenochtitlan/santa-cruz-tlatelolco": santa_cruz_tlatelolco,
}
