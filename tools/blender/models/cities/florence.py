"""Florence landmark miniatures: the Duomo with Brunelleschi's dome, the Baptistery and Giotto's campanile, the Palazzo
Vecchio and the Piazza della Signoria, the bridges over the Arno, the friars' churches, Brunelleschi's and Michelozzo's
Renaissance buildings, the Pitti and the Medici fortresses, and Roman Florentia.

Conventions as worldkit: metres, origin at the ground centre, +X east, +Y north, +Z up, main front to the south (-Y).
Helpers build at the origin and are put in place with place(). Bespoke Florentine parts: rusticated ashlar,
Gothic and Renaissance bifore, Guelf and Ghibelline crenellations, the corbelled gallery (ballatoio) with
machicolations, white-and-green marble panelling, the octagonal ribbed dome with its lantern, Brunelleschi's
arcade, arched bridges with shops.
"""
import math
import bpy
from chronokit import Model, box, cylinder, dome, join, shade, gable_roof, hip_roof, mesh_from, ellipse_ring, ellipse_disc, ring_extrude, ellipse_pts, mini_temple, columns
from worldkit import *

# ---------------------------------------------------------------- palette
PF = "#C4A67C"        # pietra forte, golden-brown sandstone
PF_D = "#A98C64"
PF_L = "#D6BE98"
SERENA = "#8F918C"    # pietra serena, grey sandstone
SERENA_D = "#767873"
WHITE_M = "#EEEAE0"   # Carrara marble
GREEN_M = "#4F6E5A"   # Prato serpentine
PINK_M = "#D7A597"    # Maremma pink
PLAST_F = "#EDE3CF"
OCHRE_F = "#E0C38E"
COPPI = "#B5603F"     # terracotta roof tiles
COPPI_D = "#9E5236"
DOME_RED = "#B65A3C"
BRICK_F = "#B16C4A"
LEAD_F = "#8B9298"
GOLD_F = "#D4AE55"
BRONZE_F = "#8A6A3A"
GLASS_F = "#3B4658"
PAVE_F = "#B8AE9C"
PAVE_L = "#CFC6B4"
SAND_F = "#D9C79E"
GRASS_F = "#8C9C68"
HEDGE_F = "#6F8754"
WATER_F = "#638A8C"
TIMBER_F = "#7A5A3E"
SHUTTER = "#6E4A2E"
LAPIS = "#3F5F9E"
RED_F = "#A3342A"
C22 = math.cos(math.pi / 8)


# ---------------------------------------------------------------- placement and primitives (after venice.py)
def place(o, ang=0.0, x=0.0, y=0.0, z=0.0):
    """Rotate an object built at the origin (degrees counter-clockwise from above), then move it."""
    if ang:
        o = rot(o, ang)
    if x or y or z:
        o = move(o, x, y, z)
    return o


def apply_rot(o, rx=0.0, ry=0.0):
    o.rotation_euler[0] += rx
    o.rotation_euler[1] += ry
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(rotation=True)
    return o


def plate(w, d, color=PAVE_F, h=0.3, x=0, y=0, name="plate"):
    return box(name, w, d, h, (x, y, 0), color)


def multi_slab(name, polys, depth, color, y0=0.0):
    """Many flat 2D outlines [(u, v)] in the XZ plane, each extruded through depth along Y (front face at y0 - depth/2)."""
    verts, faces = [], []
    for pts in polys:
        n = len(pts)
        b = len(verts)
        verts += [(u, y0 - depth / 2, v) for u, v in pts] + [(u, y0 + depth / 2, v) for u, v in pts]
        faces.append(tuple(b + i for i in range(n)))
        faces.append(tuple(b + i for i in range(2 * n - 1, n - 1, -1)))
        faces += [(b + i, b + (i + 1) % n, b + n + (i + 1) % n, b + n + i) for i in range(n)]
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def on_wall(o, x, y, z, normal_deg):
    """Put a piece built facing -Y at the origin onto a wall whose outward normal points at normal_deg (0 = +X, 90 = +Y)."""
    return place(o, normal_deg + 90, x, y, z)


def arch_pts(w, h, kind="round"):
    """Outline (u, v) of an arched opening w wide and h high, base at v = 0. kind: round | pointed | flat."""
    r = w / 2
    if kind == "round":
        rh = max(0.0, h - r)
        top = [(r * math.cos(math.pi * i / 8), rh + r * math.sin(math.pi * i / 8)) for i in range(9)]
    elif kind == "pointed":
        tip = min(h, w * 0.75)
        rh = h - tip
        half = [(r, rh), (r * 0.93, rh + tip * 0.38), (r * 0.72, rh + tip * 0.7), (r * 0.4, rh + tip * 0.9), (0, rh + tip)]
        top = half + [(-u, v) for u, v in reversed(half[:-1])]
    else:
        top = [(r, h), (-r, h)]
    pts = [(-r, 0.0), (r, 0.0)] + top
    out = []
    for p in pts:
        if not out or abs(out[-1][0] - p[0]) > 1e-6 or abs(out[-1][1] - p[1]) > 1e-6:
            out.append(p)
    if abs(out[-1][0] - out[0][0]) < 1e-6 and abs(out[-1][1] - out[0][1]) < 1e-6:
        out.pop()
    return out


def opening(name, w, h, x, y, z, normal_deg, kind="round", color=DARK, depth=0.3):
    return on_wall(multi_slab(name, [arch_pts(w, h, kind)], depth, color), x, y, z, normal_deg)


def openings(name, length, n, w, h, x, y, z, normal_deg, kind="round", color=DARK, depth=0.3, skip=()):
    bay = length / n
    polys = []
    for i in range(n):
        if i in skip:
            continue
        u0 = -length / 2 + bay * (i + 0.5)
        polys.append([(u0 + u, v) for u, v in arch_pts(w, h, kind)])
    if not polys:
        return None
    return on_wall(multi_slab(name, polys, depth, color), x, y, z, normal_deg)


def rects(name, items, x, y, z, normal_deg, color, depth=0.2, y0=0.0):
    """Flat rectangles [(u0, v0, u1, v1)] on a wall face."""
    polys = [[(a, b), (c, b), (c, d), (a, d)] for a, b, c, d in items if c - a > 1e-3 and d - b > 1e-3]
    if not polys:
        return None
    return on_wall(multi_slab(name, polys, depth, color, y0), x, y, z, normal_deg)


def disc(name, r, x, y, z, normal_deg, color=GOLD_F, t=0.3, verts=20):
    """A flat round plate on a wall (oculus, roundel, clock)."""
    o = cylinder(name, r, t, (0, 0, -t / 2), color, verts=verts)
    apply_rot(o, rx=math.pi / 2)
    return place(o, normal_deg + 90, x, y, z)


def oculus(name, r, x, y, z, normal_deg, frame=WHITE_M, glass=DARK, verts=20):
    return join([disc(name + "_f", r * 1.25, x, y, z, normal_deg, frame, 0.25, verts),
                 disc(name + "_g", r, x + 0.12 * math.cos(math.radians(normal_deg)), y + 0.12 * math.sin(math.radians(normal_deg)), z, normal_deg, glass, 0.25, verts)], name)


def column(name, x, y, z, r, h, color=SERENA, cap=True, verts=10, cap_color=None):
    parts = [cylinder(name + "_s", r, h, (x, y, z), color, verts=verts)]
    if cap:
        parts.append(box(name + "_c", r * 2.6, r * 2.6, r * 1.1, (x, y, z + h - r * 0.4), cap_color or color))
        parts.append(box(name + "_b", r * 2.4, r * 2.4, r * 0.5, (x, y, z), color))
    return join(parts, name)


def statue(name, x, y, z, h=2.0, color=WHITE_M):
    return join([cylinder(name + "_b", h * 0.13, h * 0.78, (x, y, z), color, verts=8, r_top=h * 0.09),
                 dome(name + "_h", h * 0.1, (x, y, z + h * 0.82), color, segments=8, rings=4)], name)


def roof_x(name, w, d, h, x=0, y=0, z=0, color=COPPI, over=0.4):
    """Gable roof with the ridge along X."""
    return place(gable_roof(name, d, w, h, (0, 0, 0), color, overhang=over), 90, x, y, z)


def roof_y(name, w, d, h, x=0, y=0, z=0, color=COPPI, over=0.4):
    return place(gable_roof(name, w, d, h, (0, 0, 0), color, overhang=over), 0, x, y, z)


def hip(name, w, d, h, x=0, y=0, z=0, color=COPPI, ridge=0.45, over=0.4):
    if w > d:
        return place(hip_roof(name, d, w, h, (0, 0, 0), color, ridge=ridge, overhang=over), 90, x, y, z)
    return place(hip_roof(name, w, d, h, (0, 0, 0), color, ridge=ridge, overhang=over), 0, x, y, z)


def lean_to(name, x0, x1, y0, y1, z_low, z_high, color=COPPI):
    """A roof slab sloping from z_low along x0 up to z_high along x1."""
    t = 0.3
    verts = [(x0, y0, z_low), (x1, y0, z_high), (x1, y1, z_high), (x0, y1, z_low),
             (x0, y0, z_low + t), (x1, y0, z_high + t), (x1, y1, z_high + t), (x0, y1, z_low + t)]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def lean_to_y(name, x0, x1, y0, y1, z_low, z_high, color=COPPI):
    """A roof slab sloping from z_low along y0 up to z_high along y1."""
    t = 0.3
    verts = [(x0, y0, z_low), (x1, y0, z_low), (x1, y1, z_high), (x0, y1, z_high),
             (x0, y0, z_low + t), (x1, y0, z_low + t), (x1, y1, z_high + t), (x0, y1, z_high + t)]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def pediment(name, w, h, x, y, z, normal_deg, color=WHITE_M, depth=1.0):
    return on_wall(multi_slab(name, [[(-w / 2, 0), (w / 2, 0), (0, h)]], depth, color), x, y, z, normal_deg)


def beam(name, a, b, t=0.4, color=TIMBER_F):
    """A square beam between two 3D points."""
    ax, ay, az = a
    bx, by, bz = b
    dx, dy, dz = bx - ax, by - ay, bz - az
    L = math.sqrt(dx * dx + dy * dy + dz * dz) or 1e-3
    # a side vector perpendicular to the beam
    sx, sy, sz = (-dy, dx, 0.0) if abs(dx) + abs(dy) > 1e-6 else (1.0, 0.0, 0.0)
    sl = math.sqrt(sx * sx + sy * sy + sz * sz)
    sx, sy, sz = sx / sl * t / 2, sy / sl * t / 2, sz / sl * t / 2
    # up vector = beam x side
    ux, uy, uz = dy * sz - dz * sy, dz * sx - dx * sz, dx * sy - dy * sx
    ul = math.sqrt(ux * ux + uy * uy + uz * uz) or 1e-3
    ux, uy, uz = ux / ul * t / 2, uy / ul * t / 2, uz / ul * t / 2
    verts = []
    for (px, py, pz) in (a, b):
        for s1, s2 in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            verts.append((px + s1 * sx + s2 * ux, py + s1 * sy + s2 * uy, pz + s1 * sz + s2 * uz))
    faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def face(w, d, side, cx=0.0, cy=0.0, off=0.0):
    """(x, y, normal_deg, length) of a box side S | N | E | W."""
    return {"S": (cx, cy - d / 2 - off, -90, w), "N": (cx, cy + d / 2 + off, 90, w),
            "E": (cx + w / 2 + off, cy, 0, d), "W": (cx - w / 2 - off, cy, 180, d)}[side]


# ---------------------------------------------------------------- Florentine parts
def _hash(i, j, k=0):
    return (math.sin(i * 12.9898 + j * 78.233 + k * 37.719) * 43758.5453) % 1.0


def rusticate(name, w, h, x, y, z, normal_deg, color=PF, bw=2.4, bh=1.1, relief=0.32, gap=0.14, vary=True, smooth=False):
    """Rusticated ashlar (bugnato) on a wall face: staggered raised blocks, irregular in depth."""
    groups = {0: [], 1: []}
    rows = max(1, int(round(h / bh)))
    rh = h / rows
    for r in range(rows):
        off = (r % 2) * bw * 0.5
        u = -w / 2 - off
        k = 0
        while u < w / 2 - 1e-6:
            u0 = max(-w / 2, u) + gap / 2
            u1 = min(w / 2, u + bw * (0.8 + 0.4 * _hash(r, k) if vary and not smooth else 1.0)) - gap / 2
            if u1 - u0 > 0.25:
                groups[1 if (vary and _hash(k, r, 3) > 0.55) else 0].append([(u0, r * rh + gap / 2), (u1, r * rh + gap / 2), (u1, (r + 1) * rh - gap / 2), (u0, (r + 1) * rh - gap / 2)])
            u = u1 + gap / 2
            k += 1
    parts = []
    if groups[0]:
        parts.append(multi_slab(name + "_a", groups[0], relief, color, y0=-relief / 2))
    if groups[1]:
        parts.append(multi_slab(name + "_b", groups[1], relief * 1.6, shade(color, -0.05), y0=-relief * 0.8))
    return on_wall(join(parts, name), x, y, z, normal_deg)


def rustic_box(name, w, d, h, cx=0.0, cy=0.0, z=0.0, color=PF, sides="SNEW", bw=2.4, bh=1.1, relief=0.32, vary=True):
    parts = [box(name + "_core", w, d, h, (cx, cy, z), shade(color, -0.25))]
    for s in sides:
        fx, fy, deg, L = face(w, d, s, cx, cy)
        parts.append(rusticate(f"{name}_r{s}", L, h, fx, fy, z, deg, color, bw, bh, relief, vary=vary))
    return join(parts, name)


def bifore(name, length, n, w, h, x, y, z, normal_deg, kind="round", frame=PF_L, dark=DARK, mullion=True, roundel=True):
    """A row of n two-light windows: a stone arch frame, a dark opening, a colonnette and two small arches (and an oculus)."""
    bay = length / n
    fr, dk, ml = [], [], []
    for i in range(n):
        u0 = -length / 2 + bay * (i + 0.5)
        fr.append([(u0 + u, v - 0.25) for u, v in arch_pts(w + 0.7, h + 0.55, kind)])
        dk.append([(u0 + u, v) for u, v in arch_pts(w, h, kind)])
        if mullion:
            rect_h = h - w / 2 * (1.1 if kind == "pointed" else 1.0)
            ml.append([(u0 - 0.13, 0), (u0 + 0.13, 0), (u0 + 0.13, rect_h * 0.98), (u0 - 0.13, rect_h * 0.98)])
            ml.append([(u0 - w / 2, rect_h * 0.98), (u0 + w / 2, rect_h * 0.98), (u0 + w / 2, rect_h * 0.98 + 0.25), (u0 - w / 2, rect_h * 0.98 + 0.25)])
            if roundel:
                c = (u0, rect_h + w * 0.28)
                ml.append([(c[0] + w * 0.12 * math.cos(math.tau * k / 10), c[1] + w * 0.12 * math.sin(math.tau * k / 10)) for k in range(10)])
    parts = [multi_slab(name + "_fr", fr, 0.2, frame, y0=-0.02), multi_slab(name + "_dk", dk, 0.3, dark, y0=-0.05)]
    if ml:
        parts.append(multi_slab(name + "_ml", ml, 0.2, frame, y0=-0.28))
    return on_wall(join(parts, name), x, y, z, normal_deg)


def crenel_polys(length, size, kind, gap=None):
    gap = size * 0.7 if gap is None else gap
    n = max(1, int(length / (size + gap)))
    bay = length / n
    polys = []
    for i in range(n):
        u0 = -length / 2 + bay * (i + 0.5)
        s = size / 2
        H = size * 1.25
        if kind == "ghibelline":
            polys.append([(u0 - s, 0), (u0 + s, 0), (u0 + s, H * 1.25), (u0 + s * 0.3, H * 1.25), (u0, H * 0.82), (u0 - s * 0.3, H * 1.25), (u0 - s, H * 1.25)])
        else:
            polys.append([(u0 - s, 0), (u0 + s, 0), (u0 + s, H), (u0 - s, H)])
    return polys


def crenels(name, length, x, y, z, normal_deg, size=1.0, kind="guelf", color=PF, depth=0.6):
    """Battlements along a wall top: guelf (square) or ghibelline (swallow-tail) merlons."""
    return on_wall(multi_slab(name, crenel_polys(length, size, kind), depth, color, y0=depth / 2), x, y, z, normal_deg)


def crenel_ring(name, w, d, z, size=1.0, kind="guelf", color=PF, cx=0.0, cy=0.0, depth=0.6):
    parts = []
    for s in "SNEW":
        fx, fy, deg, L = face(w, d, s, cx, cy)
        parts.append(crenels(f"{name}{s}", L - (0 if s in "SN" else depth * 2), fx, fy, z, deg, size, kind, color, depth))
    return join(parts, name)


def corbel_gallery(name, w, d, z, out=1.5, h_par=2.6, corb_h=2.4, spacing=2.6, color=PF, kind="guelf", size=1.1, cx=0.0, cy=0.0,
                   shields=None, sides="SNEW"):
    """A projecting battlemented gallery (ballatoio) on corbels with arches between them (machicolations).
    The wall below is w x d centred on (cx, cy); the gallery floor is at z."""
    W, D = w + 2 * out, d + 2 * out
    t = 0.7
    sw = out + 1.2
    parts = [box(name + "_slS", W, sw, 0.6, (cx, cy - D / 2 + sw / 2, z - 0.6), shade(color, -0.04)),
             box(name + "_slN", W, sw, 0.6, (cx, cy + D / 2 - sw / 2, z - 0.6), shade(color, -0.04)),
             box(name + "_slE", sw, D, 0.6, (cx + W / 2 - sw / 2, cy, z - 0.6), shade(color, -0.04)),
             box(name + "_slW", sw, D, 0.6, (cx - W / 2 + sw / 2, cy, z - 0.6), shade(color, -0.04))]
    for s in "SNEW":
        fx, fy, deg, L = face(W - t, D - t, s, cx, cy)
        if s in "SN":
            parts.append(box(f"{name}_p{s}", W, t, h_par, (fx, fy, z), color))
        else:
            parts.append(box(f"{name}_p{s}", t, D, h_par, (fx, fy, z), color))
        parts.append(crenels(f"{name}_c{s}", L if s in "SN" else D - 2 * t, *face(W, D, s, cx, cy)[:2], z + h_par, deg, size, kind, color, t))
    for s in sides:
        fx, fy, deg, L = face(w, d, s, cx, cy)
        n = max(2, int(round(L / spacing)))
        bay = L / n
        corb, span = [], []
        for i in range(n + 1):
            u = -L / 2 + bay * i
            # corbel in side view is stepped: three blocks sticking out further as they rise
            for k in range(3):
                corb.append(box(f"{name}_k{s}{i}{k}", 0.75, out * (k + 1) / 3, corb_h / 3, (u, -out * (k + 1) / 6, z - corb_h + corb_h * k / 3), shade(color, -0.06)))
        for i in range(n):
            u0, u1 = -L / 2 + bay * i + 0.38, -L / 2 + bay * (i + 1) - 0.38
            mid = (u0 + u1) / 2
            r = (u1 - u0) / 2
            arc = [(mid + r * math.cos(math.pi * (1 - k / 8)), z - 0.9 + r * 0.55 * math.sin(math.pi * k / 8)) for k in range(9)]
            span.append([(u0, z - 1.2)] + arc + [(u1, z - 1.2), (u1, z), (u0, z)])
        g = [multi_slab(f"{name}_sp{s}", span, 0.5, color, y0=-out + 0.25)]
        g.append(box(f"{name}_dk{s}", L, 0.2, corb_h, (0, -0.1, z - corb_h), DARK))
        parts.append(on_wall(join(corb + g, f"{name}_side{s}"), fx, fy, 0, deg))
        if shields:
            sh = []
            for i in range(n):
                u = -L / 2 + bay * (i + 0.5)
                sh.append(disc(f"{name}_sh{s}{i}", 0.45, 0, 0, 0, -90, shields[i % len(shields)], 0.15, 8))
                sh[-1] = move(sh[-1], u, -0.25, z - corb_h * 0.55)
            parts.append(on_wall(join(sh, f"{name}_shs{s}"), fx, fy, 0, deg))
    return join(parts, name)


def marble_grid(name, w, h, x, y, z, normal_deg, nx, ny, color=GREEN_M, t=0.55, depth=0.14, ys=None):
    """White-and-green marble panelling: a grid of coloured strips on a wall face (the wall itself gives the white)."""
    items = []
    for i in range(nx + 1):
        u = -w / 2 + w * i / nx
        items.append((max(-w / 2, u - t / 2), 0, min(w / 2, u + t / 2), h))
    levels = ys if ys is not None else [h * j / ny for j in range(ny + 1)]
    for v in levels:
        items.append((-w / 2, max(0, v - t / 2), w / 2, min(h, v + t / 2)))
    return rects(name, items, x, y, z, normal_deg, color, depth, y0=-depth / 2)


def octo_pts(rf, cx=0.0, cy=0.0, rot_deg=0.0):
    """Corners of an octagon with its flats facing the axes (rf = half the width across flats)."""
    rc = rf / C22
    return [(cx + rc * math.cos(math.radians(22.5 + 45 * k + rot_deg)), cy + rc * math.sin(math.radians(22.5 + 45 * k + rot_deg))) for k in range(8)]


def octo_prism(name, rf, h, x=0.0, y=0.0, z=0.0, color=WHITE_M):
    return prism(name, octo_pts(rf, x, y), h, (0, 0, z), color)


def octo_lathe(name, prof, x=0.0, y=0.0, z=0.0, color=WHITE_M, cap_top=True):
    """An octagonal solid from a profile [(corner radius, z)], flats facing the axes."""
    o = lathe(name, prof, (0, 0, 0), color, verts=8, cap_top=cap_top)
    return place(o, 22.5, x, y, z)


def octo_faces(rf, cx=0.0, cy=0.0):
    """(x, y, normal_deg) at the middle of each flat of an octagon (normals 0, 45, ... 315)."""
    return [(cx + rf * math.cos(math.radians(45 * k)), cy + rf * math.sin(math.radians(45 * k)), 45 * k) for k in range(8)]


def lantern(name, x, y, z, r=3.4, h=9.0, color=WHITE_M, roof=WHITE_M, ball=GOLD_F, buttresses=True, cone=7.0):
    """Brunelleschi's lantern: an octagonal marble shrine with arched openings and volute buttresses, a fluted cone and a gilt ball."""
    parts = [octo_prism(name + "_base", r * 1.3, 1.6, x, y, z, shade(color, -0.04))]
    parts.append(octo_prism(name + "_body", r, h, x, y, z + 1.6, color))
    for k, (fx, fy, deg) in enumerate(octo_faces(r * 1.01, x, y)):
        parts.append(opening(f"{name}_o{k}", r * 0.48, h * 0.72, fx, fy, z + 1.6 + h * 0.12, deg, "round", DARK, 0.25))
    if buttresses:
        for k in range(8):
            a = math.radians(22.5 + 45 * k)
            rc = r / C22
            prof = [(0, 0), (r * 0.85, 0), (r * 0.85, h * 0.18), (r * 0.35, h * 0.45), (r * 0.18, h * 0.9), (0, h * 0.95)]
            b = multi_slab(f"{name}_bt{k}", [prof], 0.6, shade(color, -0.03))
            b = place(b, math.degrees(a), x + rc * 0.92 * math.cos(a), y + rc * 0.92 * math.sin(a), z + 1.6)
            parts.append(b)
    parts.append(octo_prism(name + "_corn", r * 1.12, 0.8, x, y, z + 1.6 + h, shade(color, -0.05)))
    zc = z + 2.4 + h
    parts.append(octo_lathe(name + "_cone", [(r * 0.95 / C22, 0), (r * 0.7 / C22, cone * 0.25), (r * 0.2, cone)], x, y, zc, roof))
    parts.append(dome(name + "_ball", max(0.6, r * 0.32), (x, y, zc + cone + r * 0.28), ball, segments=12, rings=8))
    parts.append(box(name + "_ballb", 0.3, 0.3, r * 0.4, (x, y, zc + cone - 0.2), ball))
    parts.append(box(name + "_cr1", 0.22, 0.22, r * 0.7, (x, y, zc + cone + r * 0.6), ball))
    parts.append(box(name + "_cr2", r * 0.4, 0.22, 0.22, (x, y, zc + cone + r * 1.0), ball))
    return join(parts, name)


def brunelleschi_dome(name, rf, x, y, z, tile=DOME_RED, rib=WHITE_M, k=1.5, lantern_r=None, eyes=True):
    """The octagonal pointed dome: eight brick-red webs on a fifth-pointed profile with eight white marble ribs,
    small oculi, a closing ring and the lantern. rf = half-width across the flats at the springing."""
    rc = rf / C22
    t_top = math.acos((0.12 + (k - 1)) / k)
    ts = [t_top * i / 22 for i in range(23)]
    prof = [(rc * (k * math.cos(t) - (k - 1)), rc * k * math.sin(t)) for t in ts]
    shell = octo_lathe(name + "_shell", prof, x, y, z, tile, cap_top=True)
    ribs = []
    for c in range(8):
        a = math.radians(22.5 + 45 * c)
        ca, sa = math.cos(a), math.sin(a)
        verts, faces = [], []
        for i, (r, zz) in enumerate(prof):
            w = 1.9 * (1 - 0.5 * i / len(prof))
            for rr, tt in ((r - 0.2, -w / 2), (r + 0.55, -w / 2), (r + 0.55, w / 2), (r - 0.2, w / 2)):
                verts.append((x + rr * ca - tt * sa, y + rr * sa + tt * ca, z + zz + 0.05))
        for i in range(len(prof) - 1):
            a0, b0 = 4 * i, 4 * (i + 1)
            faces += [(a0, b0, b0 + 1, a0 + 1), (a0 + 1, b0 + 1, b0 + 2, a0 + 2), (a0 + 2, b0 + 2, b0 + 3, a0 + 3)]
        ribs.append(mesh_from(f"{name}_rib{c}", verts, faces, (0, 0, 0), rib))
    # the white ring at the springing and the closing ring at the top
    ribs.append(octo_prism(name + "_spring", rf + 0.5, 1.0, x, y, z - 0.2, rib))
    for i in (5, 10, 15):
        r, zz = prof[i]
        r2, zz2 = prof[i + 1]
        ribs.append(octo_lathe(f"{name}_crs{i}", [(r + 0.08, 0), (r2 + 0.08, zz2 - zz)], x, y, z + zz, shade(tile, -0.12), cap_top=False))
    ztop = z + prof[-1][1]
    ribs.append(octo_prism(name + "_eye", prof[-1][0] * C22 + 0.8, 1.2, x, y, ztop - 0.6, rib))
    if eyes:
        for c in range(8):
            a = math.radians(45 * c)
            r, zz = prof[7]
            fr = r * C22 + 0.15
            ribs.append(disc(f"{name}_oc{c}", 0.7, x + fr * math.cos(a), y + fr * math.sin(a), z + zz, 45 * c, WHITE_M, 0.3, 10))
    lan = lantern(name + "_lan", x, y, ztop + 0.6, lantern_r or rf * 0.15, rf * 0.36, WHITE_M, WHITE_M, GOLD_F, True, rf * 0.3)
    return shell, join(ribs, name + "_ribs"), lan


def half_octo_pts(r, axis_deg, cx, cy):
    """Five sides of an octagon (six corners) round the axis direction, closed by the chord: a polygonal apse."""
    pts = []
    rc = r / C22
    for k in range(6):
        a = math.radians(axis_deg - 112.5 + 45 * k)
        pts.append((cx + rc * math.cos(a), cy + rc * math.sin(a)))
    return pts


def apse_polygon(name, r, axis_deg, cx, cy, h, color=WHITE_M, roof=COPPI, roof_h=None, win=None, panel=GREEN_M, z=0.0):
    """A polygonal (half-octagon) apse with panelled faces, tall windows and a ribbed half-pyramid roof."""
    pts = half_octo_pts(r, axis_deg, cx, cy)
    parts = [prism(name + "_b", pts, h, (0, 0, z), color)]
    for k in range(5):
        (ax, ay), (bx, by) = pts[k], pts[k + 1]
        mx, my = (ax + bx) / 2, (ay + by) / 2
        L = math.hypot(bx - ax, by - ay)
        deg = math.degrees(math.atan2(my - cy, mx - cx))
        if panel:
            parts.append(marble_grid(f"{name}_g{k}", L, h, mx, my, z, deg, 2, 3, panel, 0.5))
        if win:
            parts.append(opening(f"{name}_w{k}", win[0], win[1], mx + 0.15 * math.cos(math.radians(deg)), my + 0.15 * math.sin(math.radians(deg)), z + win[2], deg, "pointed", DARK, 0.3))
    for k in range(6):
        px, py = pts[k]
        if k in (0, 5):
            continue
        parts.append(cylinder(f"{name}_pin{k}", 0.55, 2.6, (px, py, z + h), color, verts=4, r_top=0.05))
    rh = roof_h or r * 0.55
    apex = (cx, cy, z + h + rh)
    verts = [(px, py, z + h) for px, py in pts] + [apex]
    faces = [(k, k + 1, 6) for k in range(5)] + [(0, 5, 6), tuple(range(6))[::-1]]
    parts.append(mesh_from(name + "_r", verts, faces, (0, 0, 0), roof))
    return join(parts, name)


# ---------------------------------------------------------------- the Duomo
def duomo_nave(name, y0, y1, nave_w, nave_h, aisle_w, aisle_h, bays=4, finished=True):
    """The marble-clad nave of Santa Maria del Fiore from y0 (front) to y1."""
    L = y1 - y0
    cy = (y0 + y1) / 2
    W = nave_w + 2 * aisle_w
    walls = [box(name + "_nave", nave_w, L, nave_h, (0, cy, 0), WHITE_M)]
    roofs = [roof_y(name + "_nr", nave_w, L, nave_w * 0.32, 0, cy, nave_h, COPPI, 0.6)]
    for s in (-1, 1):
        ax = s * (nave_w / 2 + aisle_w / 2)
        walls.append(box(f"{name}_aisle{s}", aisle_w, L, aisle_h, (ax, cy, 0), WHITE_M))
        roofs.append(lean_to(f"{name}_ar{s}", s * W / 2, s * nave_w / 2, y0, y1, aisle_h, aisle_h + 4.5, COPPI))
        deg = 0 if s > 0 else 180
        fx = s * (W / 2 + 0.05)
        walls.append(marble_grid(f"{name}_ag{s}", L, aisle_h, fx, cy, 0, deg, bays * 2, 4, GREEN_M, 0.55, 0.16, ys=[0.3, 3.0, aisle_h * 0.45, aisle_h * 0.8, aisle_h - 0.3]))
        walls.append(rects(f"{name}_pk{s}", [(-L / 2 + L / bays * (i + 0.5) - 1.6, aisle_h * 0.47, -L / 2 + L / bays * (i + 0.5) + 1.6, aisle_h * 0.78) for i in range(bays)], fx, cy, 0, deg, PINK_M, 0.12, y0=-0.12))
        walls.append(bifore(f"{name}_aw{s}", L, bays, 2.6, aisle_h * 0.42, fx + s * 0.1, cy, aisle_h * 0.36, deg, "pointed", WHITE_M, DARK, True, False))
        # clerestory oculi
        for i in range(bays):
            by = y0 + L / bays * (i + 0.5)
            walls.append(oculus(f"{name}_oc{s}{i}", 1.7, s * (nave_w / 2 + 0.1), by, aisle_h + (nave_h - aisle_h) * 0.55, deg, WHITE_M, DARK, 16))
        walls.append(marble_grid(f"{name}_ng{s}", L, nave_h - aisle_h - 4.5, s * (nave_w / 2 + 0.05), cy, aisle_h + 4.5, deg, bays, 1, GREEN_M, 0.5, 0.14))
        walls.append(openings(f"{name}_ct{s}", L - 2, int(L / 1.6), 0.9, 1.1, fx + s * 0.05, cy, aisle_h - 1.5, deg, "round", GREEN_M, 0.15))
        walls.append(openings(f"{name}_cn{s}", L - 2, int(L / 1.6), 0.9, 1.1, s * (nave_w / 2 + 0.1), cy, nave_h - 1.5, deg, "round", GREEN_M, 0.15))
        walls.append(box(f"{name}_cc{s}", 1.0, L, 0.6, (s * (W / 2 + 0.2), cy, aisle_h - 0.4), WHITE_M))
        # buttress piers between bays on the aisle walls, crowned with little pinnacles
        for i in range(bays + 1):
            by = y0 + L * i / bays
            walls.append(box(f"{name}_bp{s}{i}", 1.4, 1.8, aisle_h + 1.0, (s * (W / 2 + 0.5), by, 0), WHITE_M))
            walls.append(cylinder(f"{name}_bpn{s}{i}", 0.6, 2.4, (s * (W / 2 + 0.5), by, aisle_h + 1.0), WHITE_M, verts=4, r_top=0.05))
        # the side doors
        if finished:
            dy = y0 + L * 0.62
            walls.append(rects(f"{name}_dr{s}", [(-2.8, 0, 2.8, 8.5)], fx + s * 0.2, dy, 0, deg, WHITE_M, 0.5, y0=-0.25))
            walls.append(opening(f"{name}_do{s}", 3.0, 6.5, fx + s * 0.55, dy, 0, deg, "pointed", DARK, 0.3))
            walls.append(pediment(f"{name}_dp{s}", 6.4, 3.4, fx + s * 0.45, dy, 8.5, deg, WHITE_M, 0.6))
    return join(walls, name + "_walls"), join(roofs, name + "_roofs")


def duomo_front(name, y, W, nave_w, nave_h, aisle_h, stage="1490"):
    """Arnolfo's unfinished façade: a marble lower storey with three portals and statue niches, rough stone above.
    stage "1300": only the lower storey stands."""
    parts = []
    top = aisle_h + 3.0
    if stage == "1300":
        prof = [(-W / 2, 0), (W / 2, 0), (W / 2, 14.0), (-W / 2, 14.0)]
    else:
        prof = [(-W / 2, 0), (W / 2, 0), (W / 2, top), (nave_w / 2, top + 2.0), (nave_w / 2, nave_h + 1.5), (0, nave_h + 1.5 + nave_w * 0.32),
                (-nave_w / 2, nave_h + 1.5), (-nave_w / 2, top + 2.0), (-W / 2, top)]
    parts.append(on_wall(multi_slab(name + "_w", [prof], 2.0, PF_L if stage != "1300" else WHITE_M, y0=1.0), 0, y, 0, -90))
    # the marble lower storey
    low_h = 14.0
    parts.append(on_wall(box(name + "_low", W + 0.6, 0.6, low_h, (0, 0, 0), WHITE_M), 0, y - 0.3, 0, -90))
    parts.append(marble_grid(name + "_lg", W + 0.6, low_h, 0, y - 0.62, 0, -90, 8, 2, GREEN_M, 0.5, 0.14, ys=[0.3, low_h * 0.62, low_h - 0.3]))
    for k, u in enumerate((-W * 0.3, 0, W * 0.3)):
        pw = 4.2 if u == 0 else 3.2
        ph = 10.0 if u == 0 else 8.0
        parts.append(rects(f"{name}_pf{k}", [(u - pw / 2 - 1.0, 0, u + pw / 2 + 1.0, ph + 0.8)], 0, y - 0.65, 0, -90, PINK_M, 0.4, y0=-0.2))
        parts.append(on_wall(multi_slab(f"{name}_pd{k}", [[(u + a, b) for a, b in arch_pts(pw, ph, "pointed")]], 0.3, DARK), 0, y - 1.0, 0, -90))
        parts.append(on_wall(multi_slab(f"{name}_pl{k}", [[(u + a, b + ph * 0.62) for a, b in arch_pts(pw * 0.86, ph * 0.38, "pointed")]], 0.2, GOLD_F), 0, y - 1.12, 0, -90))
        parts.append(pediment(f"{name}_pp{k}", pw + 2.4, 2.6, u, y - 0.9, ph + 0.8, -90, WHITE_M, 0.5))
    # a row of statue niches in the upper part of the marble storey
    niches = []
    for i in range(10):
        u = -W / 2 + 2.4 + (W - 4.8) * i / 9
        if min(abs(u), abs(u - W * 0.3), abs(u + W * 0.3)) < 3.3:
            continue
        niches.append([(u + a, b + 9.2) for a, b in arch_pts(1.5, 3.4, "round")])
    parts.append(on_wall(multi_slab(name + "_ni", niches, 0.3, DARK), 0, y - 0.7, 0, -90))
    for i, p in enumerate(niches):
        u = sum(a for a, b in p) / len(p)
        parts.append(statue(f"{name}_st{i}", u, y - 1.0, 9.3, 2.8, "#E2DBCB"))
    if stage != "1300":
        parts.append(oculus(name + "_rose", 3.2, 0, y - 1.05, nave_h * 0.72, -90, WHITE_M, DARK, 24))
        for s in (-1, 1):
            parts.append(oculus(f"{name}_sr{s}", 1.6, s * (nave_w / 2 + (W / 2 - nave_w / 2) / 2), y - 1.05, aisle_h * 0.78, -90, WHITE_M, DARK, 16))
    return join(parts, name)


def octagon_east(name, oy, rf, core_h, trib_r, trib_h, chap_r, chap_h):
    """The east end: the crossing octagon, three polygonal tribunes ringed with chapels, corner sacristies and the exedrae."""
    walls = [octo_prism(name + "_core", rf, core_h, 0, oy, 0, WHITE_M)]
    for k, (fx, fy, deg) in enumerate(octo_faces(rf + 0.05, 0, oy)):
        walls.append(marble_grid(f"{name}_cg{k}", rf * 2 * math.tan(math.pi / 8), core_h, fx, fy, 0, deg, 2, 4, GREEN_M, 0.5))
    for axis in (0, 90, 180):
        a = math.radians(axis)
        tc = (rf * math.cos(a), oy + rf * math.sin(a))
        walls.append(apse_polygon(f"{name}_ch{axis}", chap_r, axis, tc[0], tc[1], chap_h, WHITE_M, COPPI, chap_r * 0.25, (2.0, chap_h * 0.5, chap_h * 0.25)))
        walls.append(apse_polygon(f"{name}_tr{axis}", trib_r, axis, tc[0], tc[1], trib_h, WHITE_M, COPPI, trib_r * 0.62, (2.6, trib_h * 0.32, chap_h + 2.5)))
        hp = half_octo_pts(trib_r, axis, tc[0], tc[1])
        for k in range(5):
            (ax_, ay_), (bx_, by_) = hp[k], hp[k + 1]
            deg = math.degrees(math.atan2((ay_ + by_) / 2 - tc[1], (ax_ + bx_) / 2 - tc[0]))
            walls.append(oculus(f"{name}_to{axis}{k}", 1.0, (ax_ + bx_) / 2 + 0.15 * math.cos(math.radians(deg)), (ay_ + by_) / 2 + 0.15 * math.sin(math.radians(deg)), trib_h - 3.5, deg, WHITE_M, DARK, 12))
        # the small lantern on each tribune roof
        lx, ly = tc[0] + math.cos(a) * trib_r * 0.15, tc[1] + math.sin(a) * trib_r * 0.15
        walls.append(lantern(f"{name}_tl{axis}", lx, ly, trib_h + trib_r * 0.5, 1.3, 3.0, WHITE_M, WHITE_M, GOLD_F, False, 2.2))
    # corner blocks (sacristies) in the angles and the four exedrae (tribune morte) on top of the diagonal faces
    for k, axis in enumerate((45, 135, -45, -135)):
        a = math.radians(axis)
        cx, cy = (rf + 4.5) * math.cos(a), oy + (rf + 4.5) * math.sin(a)
        blk = box(f"{name}_sac{k}", 12, 12, chap_h + 4, (0, 0, 0), WHITE_M)
        walls.append(place(blk, axis, cx, cy, 0))
        walls.append(marble_grid(f"{name}_sg{k}", 12, chap_h + 4, cx + 6.05 * math.cos(a), cy + 6.05 * math.sin(a), 0, axis, 2, 3, GREEN_M, 0.5))
        ex, ey = (rf + 1.5) * math.cos(a), oy + (rf + 1.5) * math.sin(a)
        ez = chap_h + 4
        walls.append(cylinder(f"{name}_ex{k}", 4.2, 9.0, (ex, ey, ez), WHITE_M, verts=16))
        walls.append(openings(f"{name}_exn{k}", 6.0, 3, 1.0, 4.0, ex + 4.25 * math.cos(a), ey + 4.25 * math.sin(a), ez + 2.0, axis, "round", DARK, 0.25))
        walls.append(dome(f"{name}_exd{k}", 4.4, (ex, ey, ez + 9.0), WHITE_M, squash=0.75, segments=16, rings=6))
    return join(walls, name)


def duomo(variant="1490"):
    m = Model("duomo")
    front, nave_end = -78.5, 6.0
    rf = 25.0
    oy = nave_end + rf          # crossing centre
    nave_w, nave_h, aisle_w, aisle_h = 20.0, 42.0, 11.5, 24.0
    m.add(0, plate(94, 159, PAVE_L, 0.3), "ground")
    w, r = duomo_nave("dn", front + 2.0, nave_end, nave_w, nave_h, aisle_w, aisle_h, 4)
    m.add(0, w, "walls")
    m.add(0, duomo_front("df", front + 2.0, nave_w + 2 * aisle_w, nave_w, nave_h, aisle_h), "walls")
    m.add(0, octagon_east("de", oy, rf, 44.0, 15.5, 33.0, 20.5, 18.0), "walls")
    m.add(1, r, "roofs")
    drum_z, drum_h = 44.0, 12.0
    drum = [octo_prism("dd_drum", rf + 1.0, drum_h, 0, oy, drum_z, WHITE_M)]
    for k, (fx, fy, deg) in enumerate(octo_faces(rf + 1.05, 0, oy)):
        fw = 2 * (rf + 1.0) * math.tan(math.pi / 8)
        drum.append(marble_grid(f"dd_g{k}", fw, drum_h, fx, fy, drum_z, deg, 1, 1, GREEN_M, 0.7))
        drum.append(rects(f"dd_p{k}", [(-fw / 2 + 1.0, 1.0, -fw / 2 + 2.0, drum_h - 1.0), (fw / 2 - 2.0, 1.0, fw / 2 - 1.0, drum_h - 1.0)], fx, fy, drum_z, deg, PINK_M, 0.12, y0=-0.06))
        drum.append(oculus(f"dd_o{k}", 2.3, fx + 0.1 * math.cos(math.radians(deg)), fy + 0.1 * math.sin(math.radians(deg)), drum_z + drum_h * 0.52, deg, WHITE_M, DARK, 20))
    drum.append(octo_prism("dd_corn", rf + 1.6, 0.9, 0, oy, drum_z + drum_h, shade(WHITE_M, -0.05)))
    m.add(1, join(drum, "dd"), "drum")
    shell, ribs, lan = brunelleschi_dome("dome", rf + 0.6, 0, oy, drum_z + drum_h + 0.9)
    m.add(2, join([shell, ribs], "dome_shell"), "dome")
    m.add(3, lan, "lantern")
    return m


def santa_reparata():
    """1300: old Santa Reparata still standing, the lower storey of Arnolfo's façade and the first bays of the new walls."""
    m = Model("santa-reparata")
    front = -78.5
    W = 43.0
    m.add(0, plate(94, 159, PAVE_L, 0.3), "ground")
    # old basilica inside the line of the new nave
    nw, nh, aw, ah = 12.0, 20.0, 6.5, 11.0
    y0, y1 = -62.0, 6.0
    cy = (y0 + y1) / 2
    old = [box("sr_nave", nw, y1 - y0, nh, (0, cy, 0), PLAST_F),
           roof_y("sr_nr", nw, y1 - y0, 4.0, 0, cy, nh, COPPI, 0.4)]
    for s in (-1, 1):
        old.append(box(f"sr_ai{s}", aw, y1 - y0, ah, (s * (nw / 2 + aw / 2), cy, 0), PLAST_F))
        old.append(lean_to(f"sr_ar{s}", s * (nw / 2 + aw), s * nw / 2, y0, y1, ah, ah + 3, COPPI))
        old.append(openings(f"sr_cw{s}", y1 - y0 - 6, 8, 1.2, 3.0, s * (nw / 2 + 0.05), cy, ah + 4.0, 0 if s > 0 else 180, "round", DARK, 0.3))
        old.append(openings(f"sr_aw{s}", y1 - y0 - 6, 8, 1.0, 2.6, s * (nw / 2 + aw + 0.05), cy, 5.0, 0 if s > 0 else 180, "round", DARK, 0.3))
    old.append(cylinder("sr_apse", nw / 2, nh * 0.8, (0, y1, 0), PLAST_F, verts=16))
    old.append(cylinder("sr_apr", nw / 2 + 0.3, 3.0, (0, y1, nh * 0.8), COPPI, verts=16, r_top=0.4))
    old.append(on_wall(multi_slab("sr_front", [[(-nw / 2 - aw, 0), (nw / 2 + aw, 0), (nw / 2 + aw, ah + 2), (nw / 2, ah + 4), (nw / 2, nh), (0, nh + 4), (-nw / 2, nh), (-nw / 2, ah + 4), (-nw / 2 - aw, ah + 2)]], 1.0, PLAST_F), 0, y0 - 0.5, 0, -90))
    old.append(opening("sr_door", 3.0, 5.5, 0, y0 - 1.05, 0, -90, "round", DARK, 0.3))
    # its bell tower on the south side
    old.append(box("sr_tw", 6, 6, 32, (nw / 2 + aw + 3.5, y1 - 12, 0), PLAST_F))
    old.append(openings("sr_tb", 4.4, 2, 1.0, 3.0, nw / 2 + aw + 3.5, y1 - 15.05, 25, -90, "round", DARK, 0.3))
    old.append(cylinder("sr_tws", 4.4, 6.0, (nw / 2 + aw + 3.5, y1 - 12, 32), COPPI, verts=4, r_top=0.1))
    m.add(0, join(old, "sr_old"), "old church")
    # the new work: Arnolfo's lower façade and the first bays of the new walls with scaffolding
    new = [duomo_front("sr_nf", front + 2.0, W, 20.0, 42.0, 24.0, "1300")]
    for s in (-1, 1):
        new.append(box(f"sr_nw{s}", 2.2, 30.0, 11.0, (s * (W / 2 - 1.1), front + 2.0 + 15.0, 0), WHITE_M))
        new.append(marble_grid(f"sr_ng{s}", 30.0, 11.0, s * (W / 2 + 0.05), front + 17.0, 0, 0 if s > 0 else 180, 4, 1, GREEN_M, 0.5))
        new.append(box(f"sr_fd{s}", 2.0, 52.0, 1.0, (s * (W / 2 - 1.0), front + 2.0 + 30.0 + 26.0, 0), PF_D))
    new.append(box("sr_fdx", W, 2.0, 1.0, (0, front + 84.0, 0), PF_D))
    m.add(1, join(new, "sr_new"), "new walls")
    scaff = []
    for s in (-1, 1):
        for i in range(7):
            yy = front + 3.0 + i * 4.6
            scaff.append(box(f"sr_sp{s}{i}", 0.3, 0.3, 15.0, (s * (W / 2 + 1.4), yy, 0), TIMBER_F))
        for zz in (4.0, 8.0, 12.0):
            scaff.append(box(f"sr_sb{s}{zz}", 0.25, 30.0, 0.25, (s * (W / 2 + 1.4), front + 16.8, zz), TIMBER_F))
            scaff.append(box(f"sr_sk{s}{zz}", 1.6, 30.0, 0.15, (s * (W / 2 + 0.7), front + 16.8, zz), TIMBER_F))
    for i in range(8):
        u = -W / 2 + 2 + (W - 4) * i / 7
        scaff.append(box(f"sr_fp{i}", 0.3, 0.3, 17.0, (u, front - 0.6, 0), TIMBER_F))
    scaff.append(box("sr_fb1", W, 0.25, 0.25, (0, front - 0.6, 8), TIMBER_F))
    scaff.append(box("sr_fb2", W, 0.25, 0.25, (0, front - 0.6, 14), TIMBER_F))
    # a treadwheel crane and blocks of marble in the yard
    scaff.append(box("sr_crm", 0.6, 0.6, 22, (14, -30, 0), TIMBER_F))
    scaff.append(beam("sr_crj", (14, -30, 21), (22, -38, 24), 0.4))
    scaff.append(cylinder("sr_wheel", 2.2, 1.0, (14, -27.5, 2.2), TIMBER_F, verts=12))
    scaff[-1] = apply_rot(scaff[-1], rx=math.pi / 2)
    for i in range(6):
        scaff.append(box(f"sr_blk{i}", 2.4, 1.4, 1.2, (-30 + 5 * (i % 3), -22 + 6 * (i // 3), 0), WHITE_M if i % 2 else GREEN_M))
    m.add(2, join(scaff, "sr_scaff"), "scaffolding")
    return m


# ---------------------------------------------------------------- Baptistery and campanile
def baptistery():
    m = Model("baptistery")
    rf, ox = 12.8, 3.2
    m.add(0, plate(34, 27, PAVE_L, 0.25), "ground")
    walls = [octo_prism("bp_body", rf, 24.5, ox, 0, 0, WHITE_M)]
    fw = 2 * rf * math.tan(math.pi / 8)
    for k, (fx, fy, deg) in enumerate(octo_faces(rf + 0.03, ox, 0)):
        # first storey: corner pilasters and two tall panels; second: three arches with windows; attic: stripes
        walls.append(rects(f"bp_g1{k}", [(-fw / 2, 0, -fw / 2 + 0.7, 11.0), (fw / 2 - 0.7, 0, fw / 2, 11.0), (-0.3, 0, 0.3, 11.0),
                                         (-fw / 2, 0, fw / 2, 0.6), (-fw / 2, 10.4, fw / 2, 11.0), (-fw / 2 + 1.2, 1.4, -0.9, 1.9), (0.9, 1.4, fw / 2 - 1.2, 1.9),
                                         (-fw / 2 + 1.2, 9.0, -0.9, 9.5), (0.9, 9.0, fw / 2 - 1.2, 9.5), (-fw / 2 + 1.2, 1.4, -fw / 2 + 1.7, 9.5), (-1.4, 1.4, -0.9, 9.5),
                                         (0.9, 1.4, 1.4, 9.5), (fw / 2 - 1.7, 1.4, fw / 2 - 1.2, 9.5)], fx, fy, 0, deg, GREEN_M, 0.14, y0=-0.07))
        arches = []
        for j in range(3):
            u = -fw / 2 + fw * (j + 0.5) / 3
            arches.append([(u + a, b + 11.6) for a, b in arch_pts(fw / 3 - 0.6, 8.0, "round")])
        walls.append(on_wall(multi_slab(f"bp_ar{k}", arches, 0.16, GREEN_M, y0=-0.08), fx, fy, 0, deg))
        inner = [[(-fw / 2 + fw * (j + 0.5) / 3 + a, b + 11.9) for a, b in arch_pts(fw / 3 - 1.4, 7.4, "round")] for j in range(3)]
        walls.append(on_wall(multi_slab(f"bp_ai{k}", inner, 0.18, WHITE_M, y0=-0.14), fx, fy, 0, deg))
        win = rects(f"bp_wn{k}", [(-0.55, 13.0, 0.55, 16.0)], fx, fy, 0, deg, DARK, 0.2, y0=-0.2)
        walls.append(win)
        walls.append(pediment(f"bp_wp{k}", 1.9, 0.9, fx + 0.22 * math.cos(math.radians(deg)), fy + 0.22 * math.sin(math.radians(deg)), 16.1, deg, GREEN_M, 0.15))
        walls.append(rects(f"bp_at{k}", [(-fw / 2 + i * fw / 12, 20.6, -fw / 2 + i * fw / 12 + fw / 24, 24.0) for i in range(12)] + [(-fw / 2, 20.0, fw / 2, 20.6)], fx, fy, 0, deg, GREEN_M, 0.14, y0=-0.07))
        if deg in (0, 90, 270):
            walls.append(rects(f"bp_df{k}", [(-2.9, 0, 2.9, 8.6)], fx, fy, 0, deg, WHITE_M, 0.6, y0=-0.3))
            walls.append(rects(f"bp_dr{k}", [(-2.2, 0, 2.2, 7.4)], fx, fy, 0, deg, GOLD_F, 0.3, y0=-0.7))
            walls.append(rects(f"bp_dd{k}", [(-0.05, 0.2, 0.05, 7.2)] + [(-2.0, 0.6 + 1.4 * i, 2.0, 0.75 + 1.4 * i) for i in range(5)], fx, fy, 0, deg, BRONZE_F, 0.1, y0=-0.85))
            walls.append(box(f"bp_dl{k}", 6.6, 1.4, 0.8, (0, 0, 0), WHITE_M))
            walls[-1] = place(walls[-1], deg + 90, fx + 0.5 * math.cos(math.radians(deg)), fy + 0.5 * math.sin(math.radians(deg)), 8.6)
    walls.append(octo_prism("bp_corn", rf + 0.5, 0.7, ox, 0, 24.5, shade(WHITE_M, -0.05)))
    # the scarsella on the west
    sx = ox - rf - 3.2
    walls.append(box("bp_sc", 6.6, 10.4, 14.0, (sx, 0, 0), WHITE_M))
    walls.append(marble_grid("bp_scg", 10.4, 14.0, sx - 3.35, 0, 0, 180, 3, 2, GREEN_M, 0.5))
    for s in (-1, 1):
        walls.append(marble_grid(f"bp_scs{s}", 6.6, 14.0, sx, s * 5.25, 0, 90 * s, 2, 2, GREEN_M, 0.5))
    m.add(0, join(walls, "bp_walls"), "walls")
    roof = [octo_lathe("bp_roof", [((rf + 0.4) / C22, 0), (3.0 / C22, 6.6)], ox, 0, 25.2, "#E2DED3")]
    roof.append(roof_x("bp_scr", 6.6, 10.4, 2.2, sx, 0, 14.0, "#E2DED3", 0.3))
    m.add(1, join(roof, "bp_roofs"), "roof")
    lan = [octo_prism("bp_lb", 3.0, 0.8, ox, 0, 31.7, WHITE_M), octo_prism("bp_lan", 2.4, 4.0, ox, 0, 32.5, WHITE_M)]
    for k, (fx, fy, deg) in enumerate(octo_faces(2.42, ox, 0)):
        lan.append(opening(f"bp_lo{k}", 0.9, 2.8, fx, fy, 33.0, deg, "round", DARK, 0.2))
    lan.append(octo_lathe("bp_lc", [(2.8 / C22, 0), (0.3, 2.6)], ox, 0, 36.5, WHITE_M))
    lan.append(dome("bp_ball", 0.5, (ox, 0, 39.1), GOLD_F, segments=10, rings=6))
    m.add(2, join(lan, "bp_lan"), "lantern")
    return m


def campanile_g():
    m = Model("campanile")
    w = 14.45
    H = 81.0
    m.add(0, plate(15.5, 15.5, PAVE_L, 0.25), "ground")
    body = [box("cg_shaft", w - 1.2, w - 1.2, H, (0, 0, 0), WHITE_M)]
    for sx in (-1, 1):
        for sy in (-1, 1):
            body.append(cylinder(f"cg_pil{sx}{sy}", 1.05, H, (sx * (w / 2 - 0.9), sy * (w / 2 - 0.9), 0), WHITE_M, verts=8))
            body.append(rects(f"cg_pg{sx}{sy}", [(-0.25, 0, 0.25, H)], sx * (w / 2 - 0.9), sy * (w / 2 - 0.9) + sy * 1.06, 0, 90 if sy > 0 else -90, GREEN_M, 0.1, y0=-0.05))
    m.add(0, join(body, "cg_body"), "shaft")
    deco = []
    inner = w - 3.6
    zones = [0, 7.5, 15.0, 27.0, 40.0, 53.0, 72.0, H]
    for s in "SNEW":
        fx, fy, deg, _ = face(w - 1.2, w - 1.2, s, 0, 0, 0.02)
        # coloured bands between zones
        deco.append(rects(f"cg_b{s}", [(-inner / 2 - 1, z0 - 0.35, inner / 2 + 1, z0 + 0.35) for z0 in zones[1:-1]] + [(-inner / 2 - 1, 0, inner / 2 + 1, 0.8)], fx, fy, 0, deg, GREEN_M, 0.14, y0=-0.07))
        deco.append(rects(f"cg_p{s}", [(-inner / 2, z0 + 0.6, -inner / 2 + 0.4, z1 - 0.6) for z0, z1 in zip(zones[3:-1], zones[4:])] +
                          [(inner / 2 - 0.4, z0 + 0.6, inner / 2, z1 - 0.6) for z0, z1 in zip(zones[3:-1], zones[4:])], fx, fy, 0, deg, PINK_M, 0.14, y0=-0.07))
        # reliefs: two rows of hexagons and one of lozenges
        hexes = []
        for row, zc in ((0, 3.6), (1, 11.2)):
            for i in range(5):
                u = -inner / 2 + inner * (i + 0.5) / 5
                if row == 0:
                    hexes.append([(u + 1.1 * math.cos(math.tau * k / 6), zc + 1.1 * math.sin(math.tau * k / 6)) for k in range(6)])
                else:
                    hexes.append([(u, zc - 1.6), (u + 1.0, zc), (u, zc + 1.6), (u - 1.0, zc)])
        deco.append(on_wall(multi_slab(f"cg_hx{s}", hexes, 0.16, "#D6CFC0", y0=-0.08), fx, fy, 0, deg))
        # statue niches
        nich = [[(-inner / 2 + inner * (i + 0.5) / 4 + a, b + 18.0) for a, b in arch_pts(1.8, 6.0, "pointed")] for i in range(4)]
        deco.append(on_wall(multi_slab(f"cg_ni{s}", nich, 0.3, DARK), fx, fy, 0, deg))
        for i in range(4):
            u = -inner / 2 + inner * (i + 0.5) / 4
            st = statue(f"cg_st{s}{i}", 0, 0, 0, 4.2, "#E4DDCD")
            deco.append(on_wall(move(st, u, -0.1, 18.6), fx, fy, 0, deg))
        # two storeys of paired windows, then the tall three-light storey
        for k, (z0, n) in enumerate(((zones[3] + 2.5, 2), (zones[4] + 2.5, 2))):
            deco.append(bifore(f"cg_bf{s}{k}", inner * 0.8, n, 2.2, 7.5, fx, fy, z0, deg, "pointed", WHITE_M, DARK, True, False))
        deco.append(rects(f"cg_tf{s}", [(-3.6, zones[5] + 2.0, 3.6, zones[5] + 3.0)], fx, fy, 0, deg, WHITE_M, 0.3, y0=-0.15))
        tri = [[(u + a, b + zones[5] + 3.0) for a, b in arch_pts(2.0, 13.0, "pointed")] for u in (-2.3, 0, 2.3)]
        deco.append(on_wall(multi_slab(f"cg_tw{s}", tri, 0.3, DARK), fx, fy, 0, deg))
        deco.append(on_wall(multi_slab(f"cg_tg{s}", [[(-3.6 + a * 1.0, b) for a, b in [(0, zones[5] + 16.0), (7.2, zones[5] + 16.0), (7.2, zones[5] + 18.5), (0, zones[5] + 18.5)]]], 0.25, WHITE_M, y0=-0.2), fx, fy, 0, deg))
    m.add(1, join([d for d in deco if d is not None], "cg_deco"), "marble")
    top = [box("cg_cornb", w + 1.6, w + 1.6, 1.0, (0, 0, H), WHITE_M)]
    for s in "SNEW":
        fx, fy, deg, L = face(w, w, s, 0, 0)
        for i in range(9):
            u = -L / 2 + L * (i + 0.5) / 9
            top.append(on_wall(box(f"cg_cb{s}{i}", 0.6, 0.8, 1.6, (u, -0.4, 0), WHITE_M), fx, fy, H - 1.6, deg))
    top.append(box("cg_par", w + 1.8, w + 1.8, 0.4, (0, 0, H + 1.0), GREEN_M))
    top.append(box("cg_parw", w + 1.8, w + 1.8, 1.8, (0, 0, H + 1.4), WHITE_M))
    top.append(box("cg_roof", w - 1.0, w - 1.0, 0.8, (0, 0, H + 1.4), LEAD_F))
    for s in "SNEW":
        fx, fy, deg, L = face(w + 1.8, w + 1.8, s, 0, 0, 0.02)
        top.append(openings(f"cg_parw{s}", L - 1.0, 8, 0.8, 1.2, fx, fy, H + 1.6, deg, "pointed", GREEN_M, 0.15))
    m.add(2, join(top, "cg_top"), "cornice")
    return m


# ---------------------------------------------------------------- Palazzo Vecchio
PV_SHIELDS = ["#F0ECE2", RED_F, LAPIS, GOLD_F, "#F0ECE2", RED_F, "#2E5A3A", LAPIS, GOLD_F]


def pv_tower(name, x, y, z0, w=8.4):
    """Arnolfo's tower: a plain shaft cantilevered on the gallery, its own machicolated gallery with swallow-tail merlons,
    the open bell chamber on four pillars and the crowning cupola with the lion vane."""
    parts = []
    shaft_top = z0 + 34.0
    parts.append(rustic_box(name + "_sh", w, w, shaft_top - z0, x, y, z0, PF, "SNEW", 2.2, 1.1, 0.25))
    parts.append(disc(name + "_clock", 1.6, x, y - w / 2 - 0.3, z0 + 18.0, -90, "#F2EAD6", 0.2, 20))
    parts.append(disc(name + "_clockh", 0.25, x, y - w / 2 - 0.45, z0 + 18.0, -90, DARK, 0.2, 8))
    parts.append(corbel_gallery(name + "_g", w, w, shaft_top + 2.2, 1.2, 2.2, 2.2, 2.1, PF, "ghibelline", 0.95, x, y))
    z = shaft_top + 2.2 + 2.2
    pw = w * 0.62
    for sx in (-1, 1):
        for sy in (-1, 1):
            parts.append(box(f"{name}_pil{sx}{sy}", 1.3, 1.3, 7.0, (x + sx * (pw / 2 - 0.65), y + sy * (pw / 2 - 0.65), z), PF))
    parts.append(box(name + "_bell", 1.6, 1.6, 1.8, (x, y, z + 3.4), BRONZE_F))
    parts.append(box(name + "_bc", pw + 0.6, pw + 0.6, 1.0, (x, y, z + 7.0), PF_D))
    parts.append(crenel_ring(name + "_bcm", pw + 0.6, pw + 0.6, z + 8.0, 0.7, "ghibelline", PF, x, y, 0.4))
    parts.append(octo_lathe(name + "_cup", [(pw * 0.42 / C22, 0), (pw * 0.4 / C22, 1.4), (pw * 0.3 / C22, 3.2), (0.25, 5.2)], x, y, z + 8.0, LEAD_F))
    parts.append(box(name + "_pole", 0.2, 0.2, 2.6, (x, y, z + 13.0), BRONZE_F))
    parts.append(box(name + "_lion", 1.4, 0.2, 1.0, (x + 0.4, y, z + 15.0), GOLD_F))
    return join(parts, name)


def palazzo_vecchio(variant="1490"):
    m = Model("palazzo-vecchio")
    W, D = 46.0, 40.0
    cy = -30.0 + D / 2         # main block from y=-30 to +10
    H = 34.0
    m.add(0, plate(50, 62, PAVE_F, 0.3), "ground")
    if variant == "1300":
        return palazzo_vecchio_1300(m, W, D, cy)
    walls = [rustic_box("pv_main", W, D, H, 0, cy, 0, PF, "SNEW", 2.6, 1.2, 0.3)]
    # the windows: small barred ones below, two rows of Gothic bifore above
    for s in "SNEW":
        fx, fy, deg, L = face(W, D, s, 0, cy, 0.35)
        n = 5 if s in "SN" else 4
        walls.append(bifore(f"pv_b1{s}", L * 0.84, n, 2.4, 5.0, fx, fy, 13.5, deg, "round", PF_L, DARK, True, True))
        walls.append(bifore(f"pv_b2{s}", L * 0.84, n, 2.4, 5.0, fx, fy, 23.5, deg, "round", PF_L, DARK, True, True))
        walls.append(rects(f"pv_cr{s}", [(-L / 2, 12.3, L / 2, 12.8), (-L / 2, 22.3, L / 2, 22.8)], fx, fy, 0, deg, PF_L, 0.3, y0=-0.1))
        walls.append(openings(f"pv_g{s}", L * 0.7, 4 if s in "SN" else 3, 1.0, 1.6, fx, fy, 6.5, deg, "flat", DARK, 0.3))
    walls.append(opening("pv_door", 3.4, 5.6, 0, cy - D / 2 - 0.5, 0, -90, "round", DARK, 0.4))
    walls.append(pediment("pv_dped", 5.0, 1.6, 0, cy - D / 2 - 0.5, 5.8, -90, PF_L, 0.5))
    walls.append(rects("pv_frieze", [(-1.4, 6.6, 1.4, 8.6)], 0, cy - D / 2 - 0.5, 0, -90, LAPIS, 0.2, y0=-0.2))
    # the ringhiera: the stone platform for speakers along the front
    walls.append(box("pv_ring", W + 6, 3.2, 1.0, (0, cy - D / 2 - 1.6, 0), PF_D))
    walls.append(box("pv_ringn", 3.2, 14.0, 1.0, (-W / 2 - 1.6, cy - D / 2 + 7.0, 0), PF_D))
    for i in range(6):
        walls.append(box(f"pv_rs{i}", 0.5, 0.5, 1.0, (-W / 2 - 2 + (W + 4) * i / 5, cy - D / 2 - 3.0, 1.0), PF_D))
    m.add(0, join(walls, "pv_walls"), "walls")
    # the later wings behind (the Dogana, the Salone of 1495 and the ducal additions), plainer and lower
    back = [box("pv_back", 44.0, 18.0, 26.0, (0, 20.5, 0), PLAST_F),
            hip("pv_backr", 44.0, 18.0, 3.6, 0, 20.5, 26.0, COPPI, 0.6, 0.5)]
    for s in "NEW":
        fx, fy, deg, L = face(44.0, 18.0, s, 0, 20.5, 0.05)
        back.append(openings(f"pv_bw{s}", L * 0.85, max(3, int(L / 4)), 1.3, 2.6, fx, fy, 9.0, deg, "flat", DARK, 0.3))
        back.append(openings(f"pv_bx{s}", L * 0.85, max(3, int(L / 4)), 1.3, 2.6, fx, fy, 17.0, deg, "flat", DARK, 0.3))
        back.append(rects(f"pv_bq{s}", [(-L / 2, 0, L / 2, 4.0)], fx, fy, 0, deg, PF, 0.3, y0=-0.1))
    m.add(0, join(back, "pv_back"), "walls")
    gal = [corbel_gallery("pv_gal", W, D, H + 2.6, 1.6, 2.8, 2.6, 2.7, PF, "guelf", 1.15, 0, cy, PV_SHIELDS)]
    gal.append(box("pv_roof", W - 1.0, D - 1.0, 1.0, (0, cy, H), COPPI_D))
    gal.append(hip("pv_roofh", W - 6, D - 6, 2.4, 0, cy, H + 1.0, COPPI, 0.5, 0.2))
    # the courtyard light well
    gal.append(box("pv_court", 12, 12, 0.6, (0, cy + 4, H + 1.0), DARK))
    m.add(1, join(gal, "pv_gallery"), "gallery")
    tx, ty = 3.5, cy - D / 2 + 4.2 - 1.6
    m.add(2, pv_tower("pv_tower", tx, ty, H), "tower")
    return m


def palazzo_vecchio_1300(m, W, D, cy):
    """1300: the walls of the priors' palace rising round the old Foraboschi tower, scaffolds and a crane."""
    h = 16.0
    t = 3.0
    walls = [box("pv3_ws", W, t, h, (0, cy - D / 2 + t / 2, 0), PF_D), box("pv3_wn", W, t, h, (0, cy + D / 2 - t / 2, 0), PF_D),
             box("pv3_we", t, D, h, (W / 2 - t / 2, cy, 0), PF_D), box("pv3_ww", t, D, h, (-W / 2 + t / 2, cy, 0), PF_D),
             box("pv3_fl", W - 2 * t, D - 2 * t, 6.5, (0, cy, 0), PF_D)]
    for s_ in "SNEW":
        fx, fy, deg, L = face(W, D, s_, 0, cy)
        walls.append(rusticate(f"pv3_r{s_}", L, h, fx, fy, 0, deg, PF, 2.6, 1.2, 0.3))
    for i in range(6):
        walls.append(box(f"pv3_jo{i}", 0.4, D - 2 * t, 0.4, (-W / 2 + t + (W - 2 * t) * (i + 0.5) / 6, cy, 11.5), TIMBER_F))
    for s in "SNEW":
        fx, fy, deg, L = face(W, D, s, 0, cy, 0.35)
        walls.append(bifore(f"pv3_b1{s}", L * 0.84, 5 if s in "SN" else 4, 2.4, 5.0, fx, fy, 13.5 - 4.0, deg, "round", PF_L, DARK, True, False))
        walls.append(openings(f"pv3_g{s}", L * 0.7, 4 if s in "SN" else 3, 1.0, 1.6, fx, fy, 4.5, deg, "flat", DARK, 0.3))
    walls.append(opening("pv3_door", 3.4, 5.6, 0, cy - D / 2 - 0.5, 0, -90, "round", DARK, 0.4))
    # ragged top course
    for i in range(14):
        u = -W / 2 + 2 + (W - 4) * i / 13
        walls.append(box(f"pv3_rg{i}", 2.6, 2.0, 1.2 + 1.4 * _hash(i, 3), (u, cy - D / 2 + 1.0, h), PF))
        walls.append(box(f"pv3_rh{i}", 2.6, 2.0, 1.2 + 1.4 * _hash(i, 5), (u, cy + D / 2 - 1.0, h), PF))
    # the Vacca tower of the Foraboschi, which Arnolfo built his tower on
    walls.append(rustic_box("pv3_vacca", 8.4, 8.4, 34.0, 3.5, cy - D / 2 + 2.6, 0, PF_D, "SNEW", 2.0, 1.0, 0.25))
    walls.append(crenel_ring("pv3_vm", 8.4, 8.4, 34.0, 0.8, "ghibelline", PF_D, 3.5, cy - D / 2 + 2.6, 0.4))
    m.add(0, join(walls, "pv3_walls"), "walls")
    sc = []
    for s in "SNEW":
        fx, fy, deg, L = face(W + 3.0, D + 3.0, s, 0, cy)
        n = int(L / 4)
        for i in range(n + 1):
            u = -L / 2 + L * i / n
            sc.append(on_wall(box(f"pv3_sp{s}{i}", 0.3, 0.3, h + 4.0, (u, 0, 0), TIMBER_F), fx, fy, 0, deg))
        for zz in (5.0, 10.0, 15.0):
            sc.append(on_wall(box(f"pv3_sb{s}{zz}", L, 1.4, 0.18, (0, -0.6, zz), TIMBER_F), fx, fy, 0, deg))
    sc.append(box("pv3_crm", 0.6, 0.6, 26, (-12, cy, 0), TIMBER_F))
    sc.append(beam("pv3_crj", (-12, cy, 25), (-2, cy - 8, 28), 0.4))
    sc.append(box("pv3_rope", 0.08, 0.08, 18.0, (-2, cy - 8, 10), "#5A4A3A"))
    for i in range(5):
        sc.append(box(f"pv3_st{i}", 2.0, 1.2, 1.0, (-18 + 3 * i, cy - D / 2 - 6.0, 0), PF))
    m.add(1, join(sc, "pv3_scaff"), "scaffolding")
    return m


# ---------------------------------------------------------------- bridges
def arch_profile(L, deck, spans, steps=12):
    """Elevation outline of a bridge (u along its length, v up): the deck line on top, arches cut from below.
    spans: [(u_centre, half_span, spring_z, rise)] (rise = half_span for a round arch, less for segmental and elliptical ones)."""
    bot = [(-L / 2, 0.0)]
    for uc, hs, sz, rise in sorted(spans):
        bot.append((uc - hs, 0.0))
        for k in range(steps + 1):
            t = math.pi * (1 - k / steps)
            bot.append((uc + hs * math.cos(t), sz + rise * math.sin(t)))
        bot.append((uc + hs, 0.0))
    bot.append((L / 2, 0.0))
    top = [(u, deck(u)) for u in [L / 2 - L * i / 24 for i in range(25)]]
    pts = bot + top
    out = []
    for p in pts:
        if not out or abs(out[-1][0] - p[0]) > 1e-4 or abs(out[-1][1] - p[1]) > 1e-4:
            out.append(p)
    return out


def bridge_body(name, L, W, deck, spans, color=PF, cutwater=True, cut_h=None, parapet=1.1, ring=None):
    """A stone bridge running along Y: arched body, pointed cutwaters on both faces at each pier, parapets."""
    body = multi_slab(name + "_b", [arch_profile(L, deck, spans)], W, color)
    parts = [place(body, 90)]
    if ring:
        for s in (-1, 1):
            vs = []
            for uc, hs, sz, rise in spans:
                nv = max(9, int(hs * 1.4))
                for k in range(nv):
                    t0 = math.pi * (k + 0.06) / nv
                    t1 = math.pi * (k + 0.94) / nv
                    e = 1.1 + 0.25 * (k % 2)
                    vs.append([(uc - hs * math.cos(t0), sz + rise * math.sin(t0)), (uc - hs * math.cos(t1), sz + rise * math.sin(t1)),
                               (uc - (hs + e) * math.cos(t1), sz + (rise + e) * math.sin(t1)), (uc - (hs + e) * math.cos(t0), sz + (rise + e) * math.sin(t0))])
            r = multi_slab(f"{name}_ring{s}", vs, 0.3, ring)
            parts.append(place(r, 90, s * (W / 2 + 0.1), 0, 0))
    if cutwater:
        sp = sorted(spans)
        for i in range(len(sp) - 1):
            u = (sp[i][0] + sp[i][1] + sp[i + 1][0] - sp[i + 1][1]) / 2
            pw = (sp[i + 1][0] - sp[i + 1][1]) - (sp[i][0] + sp[i][1])
            h = cut_h or sp[i][2] + sp[i][3] * 0.5
            for s in (-1, 1):
                tri = [(s * W / 2, u - pw / 2), (s * (W / 2 + pw * 0.75), u), (s * W / 2, u + pw / 2)]
                parts.append(prism(f"{name}_cw{i}{s}", tri if s > 0 else tri[::-1], h, (0, 0, 0), shade(color, -0.05)))
                parts.append(mesh_from(f"{name}_cwr{i}{s}", [(s * W / 2, u - pw / 2, h), (s * (W / 2 + pw * 0.75), u, h), (s * W / 2, u + pw / 2, h), (s * W / 2, u, h + pw * 0.45)],
                                       [(0, 1, 3), (1, 2, 3), (0, 3, 2), (0, 2, 1)], (0, 0, 0), shade(color, -0.08)))
    if parapet:
        for s in (-1, 1):
            par = multi_slab(f"{name}_par{s}", [[(u, deck(u)) for u in [-L / 2 + L * i / 24 for i in range(25)]] + [(u, deck(u) + parapet) for u in [L / 2 - L * i / 24 for i in range(25)]]], 0.5, shade(color, 0.06))
            parts.append(place(par, 90, s * (W / 2 - 0.25), 0, 0))
    return join(parts, name)


def shop_row(name, y0, y1, x_in, x_out, deck_z, side, seed=0, wall=(PLAST_F, OCHRE_F, "#E6CBA8", "#D9B48C", PF_L), roof=COPPI, overhang=3.6, uniform=None):
    """A row of shops on a bridge between y0 and y1 on one side (side = -1 west / +1 east), from x_in (by the roadway)
    to x_out (the bridge face), with back rooms (retrobotteghe) hanging out over the river on timber brackets."""
    parts = []
    y = y0
    k = 0
    while y < y1 - 0.5:
        bw = min(y1 - y, 3.2 + 2.4 * _hash(seed, k))
        h = uniform or (4.2 + 4.6 * _hash(k, seed, 1))
        col = wall[int(_hash(seed, k, 2) * len(wall)) % len(wall)]
        cy = y + bw / 2
        xin, xout = side * x_in, side * x_out
        cx = (xin + xout) / 2
        depth = abs(xout - xin)
        parts.append(box(f"{name}_s{k}", depth, bw - 0.15, h, (cx, cy, deck_z), col))
        # the shutters toward the roadway
        parts.append(box(f"{name}_sh{k}", 0.2, bw * 0.7, 2.4, (xin - side * 0.1, cy, deck_z + 0.4), SHUTTER))
        parts.append(box(f"{name}_sw{k}", 0.2, bw * 0.4, 1.0, (xin - side * 0.1, cy, deck_z + h - 1.8), DARK) if h > 5.5 else None)
        parts.append(box(f"{name}_sg{k}", 0.6, 0.12, 0.5, (xin - side * 0.4, cy - bw / 2 + 0.4, deck_z + 3.0), GOLD_F if _hash(k, seed, 7) > 0.5 else RED_F))
        parts.append(box(f"{name}_ow{k}", 0.2, bw * 0.3, 1.1, (xout + side * 0.1, cy, deck_z + h * 0.62), DARK) if h > 4.6 else None)
        if h > 5.5:
            parts.append(box(f"{name}_uw{k}", 0.2, 0.7, 1.1, (xin - side * 0.1, cy - bw * 0.25, deck_z + h - 1.9), DARK))
        parts.append(box(f"{name}_ow2{k}", 0.2, 0.6, 0.9, (xout + side * 0.1, cy + bw * 0.28, deck_z + 1.2), DARK))
        if _hash(k, seed, 9) > 0.55 and h > 5.2:
            parts.append(box(f"{name}_spo{k}", 1.0, bw - 0.5, h - 3.4, (xin - side * 0.5, cy, deck_z + 3.4), shade(col, -0.04)))
            parts.append(box(f"{name}_spw{k}", 0.2, 0.8, 1.0, (xin - side * 1.05, cy, deck_z + 4.4), DARK))
            for dy in (-bw / 2 + 0.5, bw / 2 - 0.5):
                parts.append(beam(f"{name}_spb{k}{dy:.0f}", (xin, cy + dy, deck_z + 2.2), (xin - side * 0.95, cy + dy, deck_z + 3.4), 0.18))
        if _hash(k, seed, 8) > 0.45:
            parts.append(box(f"{name}_ch{k}", 0.6, 0.6, 1.6, (cx + side * 0.6, cy + bw * 0.25, deck_z + h + 0.4), shade(col, -0.1)))
            parts.append(box(f"{name}_cc{k}", 0.9, 0.9, 0.25, (cx + side * 0.6, cy + bw * 0.25, deck_z + h + 2.0), COPPI_D))
        # back room over the water
        oh = overhang * (0.6 + 0.6 * _hash(k, seed, 4))
        bh = 2.6 + 2.2 * _hash(k, seed, 5)
        bz = deck_z - 1.6 - 1.2 * _hash(k, seed, 6)
        bx = xout + side * oh / 2
        parts.append(box(f"{name}_br{k}", oh, bw - 0.3, bh, (bx, cy, bz), shade(col, -0.06)))
        parts.append(box(f"{name}_bw{k}", 0.2, bw * 0.35, 1.0, (xout + side * (oh + 0.05), cy, bz + bh * 0.45), DARK))
        parts.append(lean_to(f"{name}_brr{k}", xout + side * (oh + 0.3), xout, cy - bw / 2 + 0.1, cy + bw / 2 - 0.1, bz + bh, bz + bh + 0.8, roof))
        for dy in (-bw / 2 + 0.5, bw / 2 - 0.5):
            parts.append(beam(f"{name}_bk{k}{dy:.0f}", (xout, cy + dy, bz - 2.6), (xout + side * oh * 0.9, cy + dy, bz), 0.22))
        parts.append(lean_to(f"{name}_r{k}", xin - side * 0.4, xout + side * 0.3, y + 0.05, y + bw - 0.05, deck_z + h, deck_z + h + 1.2, roof) if side > 0 else
                     lean_to(f"{name}_r{k}", xin - side * 0.4, xout + side * 0.3, y + 0.05, y + bw - 0.05, deck_z + h, deck_z + h + 1.2, roof))
        y += bw
        k += 1
    return join(parts, name)


def ponte_vecchio(variant="1490"):
    m = Model("ponte-vecchio")
    L, W = 108.0, 19.0
    spans = [(-33.0, 13.0, 2.0, 4.4), (0.0, 15.0, 2.0, 5.0), (33.0, 13.0, 2.0, 4.4)]

    def deck(u):
        return 9.0 + 0.6 * (1 - (u / (L / 2)) ** 2)

    m.add(0, bridge_body("pvb", L, W, deck, spans, PF, True, 6.0, 0.0, PF_L), "bridge")
    dz = 9.3
    shops = []
    for side in (-1, 1):
        for seg, (a, b) in enumerate(((-46.0, -8.5), (8.5, 48.0))):
            shops.append(shop_row(f"pvs{side}{seg}", a, b, 3.6, W / 2, dz, side, seed=side * 7 + seg * 3, uniform=7.0 if (variant == "1600" and side > 0) else None))
        # the open terrace in the middle with its three arches on each side
        shops.append(box(f"pvt{side}", W / 2 - 3.6, 17.0, 0.6, (side * (W / 2 + 3.6) / 2, 0, dz), PF_L))
        shops.append(box(f"pvtp{side}", 0.6, 17.0, 1.2, (side * (W / 2 - 0.3), 0, dz + 0.6), PF_L))
    shops.append(box("pv_road", 7.2, L - 4, 0.25, (0, 0, dz - 0.1), PAVE_F))
    # the stone cornice on corbels that carries the shop fronts along both faces of the bridge
    for side in (-1, 1):
        shops.append(box(f"pv_cor{side}", 0.9, L - 6.0, 0.6, (side * (W / 2 + 0.2), 0, dz - 0.9), PF_L))
        n = int((L - 8.0) / 1.4)
        for i in range(n):
            yy = -(L - 8.0) / 2 + (L - 8.0) * (i + 0.5) / n
            shops.append(box(f"pv_cb{side}{i}", 0.7, 0.45, 0.9, (side * (W / 2 + 0.25), yy, dz - 1.8), PF_L))
    m.add(1, join(shops, "pv_shops"), "shops")
    # the Mannelli tower at the south-east end (the corridor goes round it)
    tx, ty = 6.5, -50.5
    tw = [rustic_box("pv_mann", 7.0, 7.0, 26.0, tx, ty, 0, PF_D, "SNEW", 2.0, 1.0, 0.25),
          corbel_gallery("pv_mg", 7.0, 7.0, 26.0, 0.8, 1.6, 1.6, 2.0, PF_D, "guelf", 0.8, tx, ty),
          opening("pv_mw", 1.0, 2.0, tx, ty - 3.9, 14.0, -90, "round", DARK, 0.3),
          opening("pv_mw2", 1.0, 2.0, tx, ty - 3.9, 20.0, -90, "round", DARK, 0.3)]
    if variant == "1600":
        cor = []
        cz = dz + 7.0
        cx = W / 2 - 2.6
        cor.append(box("pvc_c", 4.6, 98.0, 4.4, (cx, 1.0, cz), PLAST_F))
        cor.append(hip("pvc_r", 5.0, 98.0, 1.4, cx, 1.0, cz + 4.4, COPPI, 0.9, 0.3))
        for s in (-1, 1):
            cor.append(openings(f"pvc_w{s}", 94.0, 26, 1.0, 1.4, cx + s * 2.35, 1.0, cz + 1.5, 0 if s > 0 else 180, "flat", DARK, 0.25))
        # over the middle terrace the corridor stands on three arches
        cor.append(box("pvc_ma", 1.2, 17.0, 7.0, (W / 2 - 0.6, 0, dz), PLAST_F))
        cor.append(openings("pvc_mo", 15.0, 3, 3.6, 5.6, W / 2 + 0.05, 0, dz, 0, "round", DARK, 0.4))
        cor.append(box("pvc_mi", 1.2, 17.0, 7.0, (W / 2 - 4.6, 0, dz), PLAST_F))
        cor.append(openings("pvc_mo2", 15.0, 3, 3.6, 5.6, W / 2 - 5.25, 0, dz, 180, "round", DARK, 0.4))
        # its swing round the Mannelli tower on brackets, out over the river side
        ax = tx + 3.5 + 2.3
        cor.append(box("pvc_s1", ax - cx + 2.3, 4.6, 4.4, ((ax + cx) / 2, -45.6, cz), PLAST_F))
        cor.append(box("pvc_s2", 4.6, 11.0, 4.4, (ax, -51.0, cz), PLAST_F))
        cor.append(box("pvc_s3", ax - cx + 2.3, 4.6, 4.4, ((ax + cx) / 2, -54.2, cz), PLAST_F))
        cor.append(hip("pvc_s2r", 4.6, 11.0, 1.2, ax, -51.0, cz + 4.4, COPPI, 0.6, 0.3))
        for i in range(3):
            cor.append(beam(f"pvc_sb{i}", (tx + 3.5, -54.0 + i * 3.0, cz - 4.0), (ax + 1.8, -54.0 + i * 3.0, cz), 0.35))
        cor.append(openings("pvc_s2w", 10.0, 4, 1.0, 1.4, ax + 2.35, -51.0, cz + 1.5, 0, "flat", DARK, 0.25))
        cor.append(box("pvc_nl", 5.0, 5.0, cz, (cx, 51.0, 0), PLAST_F))
        cor.append(openings("pvc_nla", 4.0, 1, 3.0, cz - 2.0, cx, 48.45, 0, -90, "round", DARK, 0.3))
        m.add(2, join(tw + cor, "pv_corridor"), "corridor")
    else:
        m.add(2, join(tw, "pv_tower"), "tower")
    return m


def ponte_vecchio_old():
    """Before 1333: a heavier stone bridge on five round arches with low timber shops, the statue of 'Mars' at its north end."""
    m = Model("ponte-vecchio-old")
    L, W = 108.0, 13.0
    spans = [(-36.0, 7.5, 1.8, 7.0), (-18.0, 7.5, 1.8, 7.0), (0.0, 7.5, 1.8, 7.0), (18.0, 7.5, 1.8, 7.0), (36.0, 7.5, 1.8, 7.0)]

    def deck(u):
        return 10.5 + 0.8 * (1 - (u / (L / 2)) ** 2)

    m.add(0, bridge_body("pvo", L, W, deck, spans, PF_D, True, 5.0, 1.0, None), "bridge")
    shops = []
    for side in (-1, 1):
        for i in range(10):
            y = -45 + i * 9.6
            if abs(y) < 5:
                continue
            h = 3.4 + 1.4 * _hash(i, side)
            shops.append(box(f"pvo_s{side}{i}", 3.0, 6.0, h, (side * 4.6, y, deck(y)), TIMBER_F if i % 2 else "#9A7650"))
            shops.append(lean_to(f"pvo_r{side}{i}", side * 6.4, side * 2.8, y - 3.2, y + 3.2, deck(y) + h - 0.4, deck(y) + h + 0.8, COPPI))
    m.add(1, join(shops, "pvo_shops"), "shops")
    mars = [box("pvo_ped", 2.0, 2.0, 3.0, (-5.0, 50.0, deck(50.0)), PF_L), statue("pvo_mars", -5.0, 50.0, deck(50.0) + 3.0, 2.6, "#B8B0A0")]
    m.add(2, join(mars, "pvo_mars"), "statue")
    return m




# ---------------------------------------------------------------- arcades, domes and church parts
def arcade_front(name, length, n, pier, spring, top, x, y, z, normal_deg, color=PF, depth=1.2, kind="round", rise=None):
    """A wall of n open arches on piers (pier = 0 for arches springing from columns), from the ground to top."""
    bay = (length - (n + 1) * pier) / n
    polys = []
    if pier > 0:
        for i in range(n + 1):
            u0 = -length / 2 + i * (bay + pier)
            polys.append([(u0, 0), (u0 + pier, 0), (u0 + pier, spring), (u0, spring)])
    for i in range(n):
        a = -length / 2 + pier + i * (bay + pier)
        b = a + bay
        mid, r = (a + b) / 2, bay / 2
        rs = rise or r
        if kind == "pointed":
            arc = [(mid - r * math.cos(math.pi * k / 12), spring + rs * 1.25 * math.sin(math.pi * k / 12) ** 0.7) for k in range(13)]
        else:
            arc = [(mid - r * math.cos(math.pi * k / 12), spring + rs * math.sin(math.pi * k / 12)) for k in range(13)]
        polys.append(arc + [(b, top), (a, top)])
    return on_wall(multi_slab(name, polys, depth, color, y0=depth / 2), x, y, z, normal_deg)


def ren_dome(name, r, x, y, z, drum_h, color=COPPI, drum_color=PLAST_F, windows=12, rise=1.0, lantern_color=WHITE_M, ribs=12, rib_color=None, verts=32, lan=True):
    """A Renaissance dome: a drum with round windows, a tiled dome with stone ribs and a small lantern."""
    parts = [cylinder(name + "_drum", r, drum_h, (x, y, z), drum_color, verts=verts),
             cylinder(name + "_dc", r * 1.05, max(0.4, drum_h * 0.1), (x, y, z + drum_h * 0.9), shade(drum_color, -0.06), verts=verts)]
    for k in range(windows):
        a = math.tau * (k + 0.5) / windows
        parts.append(disc(f"{name}_w{k}", min(r * 0.13, drum_h * 0.3), x + math.cos(a) * r * 1.01, y + math.sin(a) * r * 1.01, z + drum_h * 0.48, math.degrees(a), DARK, 0.25, 10))
    prof = [(r * 1.02, 0)] + [(r * 1.02 * math.cos(t), r * rise * math.sin(t)) for t in [math.pi / 2 * i / 8 for i in range(1, 9)]]
    prof[-1] = (r * 0.16, prof[-1][1] * 0.985)
    zt = z + drum_h
    parts.append(lathe(name + "_d", prof, (x, y, zt), color, verts=verts))
    for k in range(ribs):
        a = math.tau * k / ribs
        pts = [(r * 1.03 * math.cos(math.pi / 2 * i / 8 * 0.94), r * rise * 1.01 * math.sin(math.pi / 2 * i / 8 * 0.94)) for i in range(9)]
        vs = []
        for (rr, zz) in pts:
            for sgn in (-1, 1):
                vs.append((math.cos(a) * rr - math.sin(a) * sgn * 0.22, math.sin(a) * rr + math.cos(a) * sgn * 0.22, zz))
        fs = [(2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2) for i in range(len(pts) - 1)]
        parts.append(mesh_from(f"{name}_rib{k}", vs, fs, (x, y, zt), rib_color or WHITE_M))
    if lan:
        lt = zt + r * rise * 0.97
        lr = max(0.7, r * 0.17)
        parts.append(cylinder(name + "_lan", lr, lr * 2.2, (x, y, lt), lantern_color, verts=12))
        parts.append(openings(name + "_lw", lr * 1.6, 3, lr * 0.4, lr * 1.3, x, y - lr * 1.01, lt + lr * 0.4, -90, "round", DARK, 0.15))
        parts.append(cylinder(name + "_lc", lr * 1.05, lr * 1.4, (x, y, lt + lr * 2.2), lantern_color, verts=12, r_top=0.1))
        parts.append(dome(name + "_lb", lr * 0.35, (x, y, lt + lr * 3.7), GOLD_F, segments=10, rings=6))
    return join(parts, name)


def nave_block(name, y0, y1, nave_w, nave_h, aisle_w, aisle_h, wall=PLAST_F, roof=COPPI, kind="round", bays=8, clere="oculus", trim=SERENA,
               chapel_w=0.0, chapel_h=None, buttress=False):
    """Nave and aisles (and a strip of side chapels) from y0 to y1 with lean-to aisle roofs and windows. Returns (walls, roofs)."""
    L = y1 - y0
    cy = (y0 + y1) / 2
    W = nave_w + 2 * aisle_w
    walls = [box(name + "_nave", nave_w, L, nave_h, (0, cy, 0), wall)]
    roofs = [roof_y(name + "_nr", nave_w, L, nave_w * 0.3, 0, cy, nave_h, roof, 0.5)]
    for s in (-1, 1):
        deg = 0 if s > 0 else 180
        walls.append(box(f"{name}_ai{s}", aisle_w, L, aisle_h, (s * (nave_w / 2 + aisle_w / 2), cy, 0), wall))
        roofs.append(lean_to(f"{name}_ar{s}", s * (W / 2 + 0.4), s * nave_w / 2, y0, y1, aisle_h, aisle_h + aisle_w * 0.3, roof))
        if clere == "oculus":
            walls.append(join([disc(f"{name}_co{s}{i}", 1.0, s * (nave_w / 2 + 0.08), y0 + L * (i + 0.5) / bays, aisle_h + aisle_w * 0.3 + (nave_h - aisle_h - aisle_w * 0.3) * 0.5, deg, DARK, 0.25, 12) for i in range(bays)], f"{name}_co{s}"))
        else:
            walls.append(openings(f"{name}_co{s}", L * 0.9, bays, 1.6, (nave_h - aisle_h) * 0.45, s * (nave_w / 2 + 0.05), cy, aisle_h + aisle_w * 0.3 + 1.0, deg, kind, DARK, 0.3))
        ox = s * (W / 2 + 0.05)
        if chapel_w:
            ch = chapel_h or aisle_h * 0.7
            walls.append(box(f"{name}_cp{s}", chapel_w, L, ch, (s * (W / 2 + chapel_w / 2), cy, 0), wall))
            roofs.append(lean_to(f"{name}_cpr{s}", s * (W / 2 + chapel_w + 0.3), s * W / 2, y0, y1, ch, ch + 1.2, roof))
            ox = s * (W / 2 + chapel_w + 0.05)
            walls.append(openings(f"{name}_aw{s}", L * 0.9, bays, 1.2, ch * 0.4, ox, cy, ch * 0.35, deg, kind, DARK, 0.3))
        else:
            walls.append(openings(f"{name}_aw{s}", L * 0.9, bays, 1.6, aisle_h * 0.42, ox, cy, aisle_h * 0.3, deg, kind, DARK, 0.3))
        if buttress:
            for i in range(bays + 1):
                walls.append(box(f"{name}_bt{s}{i}", 1.4, 1.6, aisle_h * 0.85, (s * (W / 2 + 0.7), y0 + L * i / bays, 0), shade(wall, -0.06)))
        if trim:
            walls.append(box(f"{name}_tc{s}", 0.6, L, 0.5, (s * (nave_w / 2 + 0.2), cy, nave_h - 0.5), trim))
    return join(walls, name + "_w"), join(roofs, name + "_r")


def church_front(name, y, W, nave_w, nave_h, aisle_h, color=PF, doors=3, rose=True, door_kind="round", curved=False, gable=True, trim=None, holes=False):
    """A plain church front: nave gable over sloping aisle shoulders (or curved scrolls), doors and an oculus."""
    if curved:
        rise = (nave_h - aisle_h) * 0.7
        sc = [(W / 2 - (W / 2 - nave_w / 2) * math.sin(math.pi / 2 * k / 6), aisle_h + rise * (1 - math.cos(math.pi / 2 * k / 6))) for k in range(7)]
        prof = [(-W / 2, 0), (W / 2, 0)] + sc + [(nave_w / 2, nave_h)] + \
               [(nave_w / 2 * math.cos(math.pi * k / 10), nave_h + 2.2 * math.sin(math.pi * k / 10)) for k in range(1, 10)] + [(-nave_w / 2, nave_h)] + \
               [(-u, v) for u, v in reversed(sc)]
    elif gable:
        prof = [(-W / 2, 0), (W / 2, 0), (W / 2, aisle_h), (nave_w / 2, aisle_h + (W / 2 - nave_w / 2) * 0.3), (nave_w / 2, nave_h), (0, nave_h + nave_w * 0.3),
                (-nave_w / 2, nave_h), (-nave_w / 2, aisle_h + (W / 2 - nave_w / 2) * 0.3), (-W / 2, aisle_h)]
    else:
        prof = [(-W / 2, 0), (W / 2, 0), (W / 2, nave_h), (-W / 2, nave_h)]
    parts = [on_wall(multi_slab(name + "_w", [prof], 1.2, color, y0=0.6), 0, y, 0, -90)]
    xs = [0] if doors == 1 else ([-W * 0.3, 0, W * 0.3] if doors == 3 else [-W * 0.18, W * 0.18])
    for k, u in enumerate(xs):
        dw = 3.6 if u == 0 else 2.6
        dh = 7.0 if u == 0 else 5.4
        parts.append(on_wall(multi_slab(f"{name}_d{k}", [[(u + a, b) for a, b in arch_pts(dw, dh, door_kind)]], 0.3, DARK), 0, y - 0.05, 0, -90))
        if trim:
            parts.append(on_wall(multi_slab(f"{name}_dt{k}", [[(u + a, b) for a, b in arch_pts(dw + 1.2, dh + 0.7, door_kind)]], 0.2, trim), 0, y + 0.02, 0, -90))
    if rose:
        parts.append(oculus(name + "_ro", nave_w * 0.13, 0, y - 0.1, aisle_h + (nave_h - aisle_h) * 0.55, -90, trim or shade(color, 0.12), DARK, 20))
    if holes:
        hs = []
        for j in range(6):
            for i in range(9):
                u = -W / 2 + W * (i + 0.5) / 9
                v = 3.0 + j * (nave_h - 3) / 6
                if v < nave_h - 1 and (abs(u) < nave_w / 2 or v < aisle_h - 1) and min(abs(u - xx) for xx in xs) > 2.5:
                    hs.append((u - 0.25, v, u + 0.25, v + 0.4))
        parts.append(rects(name + "_holes", hs, 0, y - 0.05, 0, -90, DARK, 0.2))
    return join(parts, name)


def transept(name, y0, y1, half_w, h, wall=PLAST_F, roof=COPPI, kind="round"):
    cy, d = (y0 + y1) / 2, y1 - y0
    walls = [box(name + "_b", 2 * half_w, d, h, (0, cy, 0), wall)]
    roofs = [roof_x(name + "_r", 2 * half_w, d, d * 0.3, 0, cy, h, roof, 0.5)]
    for s in (-1, 1):
        walls.append(opening(f"{name}_w{s}", 2.4, h * 0.38, s * (half_w + 0.05), cy, h * 0.3, 0 if s > 0 else 180, kind, DARK, 0.3))
        walls.append(disc(f"{name}_o{s}", 1.4, s * (half_w + 0.08), cy, h * 0.8, 0 if s > 0 else 180, DARK, 0.25, 14))
    return join(walls, name + "_w"), join(roofs, name + "_r")


def bell_tower(name, x, y, w, h, color=PF, top="spire", cap=COPPI, belfry_z=None, storeys=4):
    """A Florentine church campanile: a plain shaft with string courses, a belfry with paired arches, and a spire or a cupola."""
    parts = [box(name + "_s", w, w, h, (x, y, 0), color)]
    for k in range(1, storeys):
        parts.append(box(f"{name}_sc{k}", w + 0.4, w + 0.4, 0.4, (x, y, h * k / storeys), shade(color, 0.1)))
    bz = belfry_z or h * 0.8
    for s in "SNEW":
        fx, fy, deg, L = face(w, w, s, x, y, 0.05)
        parts.append(openings(f"{name}_b{s}", w * 0.75, 2, w * 0.24, h - bz - 1.5, fx, fy, bz, deg, "round", DARK, 0.3))
        parts.append(openings(f"{name}_m{s}", w * 0.5, 1, w * 0.14, h * 0.08, fx, fy, h * 0.45, deg, "round", DARK, 0.3))
    parts.append(box(name + "_c", w + 1.0, w + 1.0, 0.8, (x, y, h), shade(color, 0.1)))
    if top == "spire":
        sp = cylinder(name + "_sp", w * 0.6, w * 2.2, (x, y, h + 0.8), cap, verts=4, r_top=0.1)
        sp.rotation_euler[2] = math.pi / 4
        parts.append(sp)
    elif top == "cupola":
        parts.append(cylinder(name + "_dr", w * 0.36, w * 0.4, (x, y, h + 0.8), color, verts=12))
        parts.append(dome(name + "_cu", w * 0.36, (x, y, h + 0.8 + w * 0.4), cap, squash=1.4, segments=12, rings=6))
        parts.append(cylinder(name + "_cs", 0.12, w * 0.5, (x, y, h + 0.8 + w * 0.9), GOLD_F, verts=4))
    elif top == "crenels":
        parts.append(crenel_ring(name + "_cr", w + 1.0, w + 1.0, h + 0.8, 0.8, "guelf", color, x, y, 0.5))
    return join([p for p in parts if p is not None], name)


# ---------------------------------------------------------------- Piazza della Signoria
def loggia_lanzi(variant="1490"):
    m = Model("loggia-lanzi")
    W, D, H = 38.0, 14.6, 20.0
    fl = 1.2
    m.add(0, plate(39, 16.5, PAVE_F, 0.25), "ground")
    base = [box("ll_floor", W, D, fl, (0, 0, 0), PF_D)]
    for i in range(4):
        base.append(box(f"ll_step{i}", W - 4 + 0, 0.6, fl * (4 - i) / 4, (0, -D / 2 - 0.3 - 0.6 * i, 0), PF_D))
    base.append(box("ll_back", W, 1.4, H, (0, D / 2 - 0.7, fl), PF))
    base.append(box("ll_dark", W - 3.0, D - 3.0, H - 5.0, (0, 0.3, fl), "#3A3028"))
    m.add(0, join(base, "ll_base"), "platform")
    arches = [arcade_front("ll_front", W, 3, 2.6, 10.5, H - 1.0, 0, -D / 2, fl, -90, PF, 1.6),
              arcade_front("ll_e", D, 1, 2.6, 10.5, H - 1.0, W / 2, 0, fl, 0, PF, 1.6),
              arcade_front("ll_w", D, 1, 2.6, 10.5, H - 1.0, -W / 2, 0, fl, 180, PF, 1.6)]
    bay = (W - 4 * 2.6) / 3
    for i in range(4):
        u = -W / 2 + 1.3 + i * (bay + 2.6)
        for dx in (-1.1, 0, 1.1):
            arches.append(cylinder(f"ll_cl{i}{dx}", 0.45, 10.5, (u + dx, -D / 2 - 0.15, fl), PF_L, verts=8))
        arches.append(box(f"ll_cap{i}", 3.2, 1.2, 0.8, (u, -D / 2 - 0.1, fl + 10.1), PF_L))
    for i in range(4):
        u = -W / 2 + 1.3 + i * (bay + 2.6)
        if 0 < i < 3:
            arches.append(disc(f"ll_vq{i}", 1.3, u, -D / 2 - 0.1, fl + 15.4, -90, LAPIS, 0.25, 12))
            arches.append(disc(f"ll_vf{i}", 0.7, u, -D / 2 - 0.25, fl + 15.4, -90, WHITE_M, 0.2, 8))
    m.add(1, join(arches, "ll_arches"), "arches")
    top = [box("ll_corn", W + 1.0, D + 1.0, 1.0, (0, 0, fl + H - 1.0), PF_L),
           box("ll_terr", W, D, 0.4, (0, 0, fl + H), COPPI_D)]
    for s in "SNEW":
        fx, fy, deg, L = face(W + 1.0, D + 1.0, s, 0, 0, 0.02)
        top.append(openings(f"ll_ct{s}", L - 1.0, int(L / 1.3), 0.7, 0.9, fx, fy, fl + H - 2.0, deg, "round", DARK, 0.15))
    top.append(crenel_ring("ll_par", W + 0.6, D + 0.6, fl + H, 0.9, "guelf", PF, 0, 0, 0.5))
    m.add(2, join(top, "ll_top"), "terrace")
    if variant == "1600":
        st = [box("ll_ped1", 2.2, 2.2, 2.4, (-W / 2 + 2.6 + bay / 2, -D / 2 + 2.4, fl), WHITE_M),
              statue("ll_perseus", -W / 2 + 2.6 + bay / 2, -D / 2 + 2.4, fl + 2.4, 3.6, BRONZE_F),
              box("ll_ped2", 2.6, 2.6, 2.0, (W / 2 - 2.6 - bay / 2, -D / 2 + 2.6, fl), WHITE_M),
              statue("ll_sab1", W / 2 - 2.6 - bay / 2 - 0.4, -D / 2 + 2.6, fl + 2.0, 4.0, WHITE_M),
              statue("ll_sab2", W / 2 - 2.6 - bay / 2 + 0.5, -D / 2 + 2.8, fl + 2.0, 3.2, WHITE_M),
              box("ll_ped3", 2.0, 2.0, 2.0, (0, D / 2 - 3.0, fl), WHITE_M), statue("ll_ant", 0, D / 2 - 3.0, fl + 2.0, 3.0, WHITE_M)]
        m.add(3, join(st, "ll_statues"), "statues")
    return m


def uffizi():
    m = Model("uffizi")
    W, D, H = 68.0, 116.0, 24.0
    ww, rw = 23.0, 14.0
    gap = W - 2 * ww
    m.add(0, plate(70, 118, PAVE_F, 0.25), "ground")
    walls, roofs = [], []
    y0 = -D / 2 + rw
    L = D / 2 - y0
    cy = (y0 + D / 2) / 2
    for s in (-1, 1):
        cx = s * (gap / 2 + ww / 2)
        walls.append(box(f"uf_w{s}", ww, L, H, (cx, cy, 0), PLAST_F))
        roofs.append(hip(f"uf_r{s}", ww, L, 4.0, cx, cy, H + 0.8, COPPI, 0.9, 0.5))
        walls.append(box(f"uf_c{s}", ww + 0.8, L + 0.8, 0.8, (cx, cy, H), SERENA))
        inner = (s * -1)
        fx = cx + inner * (ww / 2 + 0.05)
        deg = 180 if s > 0 else 0
        # the portico along the piazzale: a dark recess, paired Doric columns and piers
        walls.append(box(f"uf_pd{s}", 0.3, L - 2, 8.5, (fx + inner * 0.1, cy, 0), DARK))
        n = int((L - 2) / 4.2)
        for i in range(n + 1):
            yy = y0 + 1 + (L - 2) * i / n
            if i % 3 == 0:
                walls.append(box(f"uf_pp{s}{i}", 1.6, 1.6, 8.5, (fx + inner * 0.8, yy, 0), SERENA))
            else:
                walls.append(column(f"uf_pc{s}{i}", fx + inner * 0.8, yy, 0, 0.42, 8.0, SERENA, True, 8))
        walls.append(box(f"uf_ent{s}", 1.8, L - 2, 1.0, (fx + inner * 0.8, cy, 8.0), SERENA))
        # three storeys of windows on both faces, the open loggia on top
        for f, ff in ((deg, fx + inner * 1.0), (180 - deg if deg else 180, cx - inner * (ww / 2 + 0.05))):
            nn = int(L / 4.2)
            walls.append(openings(f"uf_m{s}{f}", L - 4, nn, 1.1, 1.0, ff, cy, 9.5, f, "flat", DARK, 0.3))
            walls.append(openings(f"uf_x{s}{f}", L - 4, nn, 1.3, 2.6, ff, cy, 12.0, f, "flat", DARK, 0.3))
            walls.append(rects(f"uf_xp{s}{f}", [(-L / 2 + 2 + (L - 4) * (i + 0.5) / nn - 1.1, 14.8, -L / 2 + 2 + (L - 4) * (i + 0.5) / nn + 1.1, 15.2) for i in range(nn)], ff, cy, 0, f, SERENA, 0.25, y0=-0.12))
            walls.append(openings(f"uf_y{s}{f}", L - 4, nn, 1.1, 1.0, ff, cy, 16.2, f, "flat", DARK, 0.3))
            walls.append(box(f"uf_lg{s}{f}", 0.3, L - 2, 4.4, (ff, cy, 18.8), DARK) if f == deg else None)
            walls.append(rects(f"uf_bd{s}{f}", [(-L / 2, 8.6, L / 2, 9.0), (-L / 2, 18.4, L / 2, 18.8)], ff, cy, 0, f, SERENA, 0.25, y0=-0.12))
        nn = int((L - 2) / 3.0)
        for i in range(nn + 1):
            yy = y0 + 1 + (L - 2) * i / nn
            walls.append(box(f"uf_lc{s}{i}", 0.5, 0.5, 4.4, (fx + inner * 0.25, yy, 18.8), SERENA))
    # the river wing with its great arch (the serliana)
    ry = -D / 2 + rw / 2
    walls.append(box("uf_river", W, rw, H, (0, ry, 0), PLAST_F))
    roofs.append(hip("uf_rr", W, rw, 3.6, 0, ry, H + 0.8, COPPI, 0.6, 0.5))
    walls.append(box("uf_rc", W + 0.8, rw + 0.8, 0.8, (0, ry, H), SERENA))
    for f, yy in ((-90, -D / 2 - 0.05), (90, -D / 2 + rw + 0.05)):
        walls.append(opening(f"uf_arch{f}", 9.0, 14.0, 0, yy, 0, f, "round", DARK, 0.4))
        walls.append(opening(f"uf_ar2{f}", 10.6, 14.8, 0, yy + (0.1 if f > 0 else -0.1) * -1, 0, f, "round", SERENA, 0.25))
        for sx in (-1, 1):
            walls.append(opening(f"uf_sa{f}{sx}", 2.4, 8.0, sx * 7.5, yy, 0, f, "flat", DARK, 0.4))
            walls.append(openings(f"uf_rw{f}{sx}", 22.0, 5, 1.3, 2.6, sx * 22.0, yy, 12.0, f, "flat", DARK, 0.3))
            walls.append(openings(f"uf_rv{f}{sx}", 22.0, 5, 1.1, 1.0, sx * 22.0, yy, 16.2, f, "flat", DARK, 0.3))
        walls.append(openings(f"uf_rl{f}", 12.0, 3, 2.6, 4.2, 0, yy, 18.8, f, "round", DARK, 0.3))
    m.add(0, join([w for w in walls if w is not None], "uf_walls"), "walls")
    m.add(1, join(roofs, "uf_roofs"), "roofs")
    return m


# ---------------------------------------------------------------- bridges
def ponte_alle_grazie():
    m = Model("ponte-alle-grazie")
    L, W = 120.0, 9.0
    n = 9
    pier = 4.2
    bay = (L - 12.0 - (n - 1) * pier) / n
    spans = []
    u = -L / 2 + 6.0
    for i in range(n):
        spans.append((u + bay / 2, bay / 2, 1.5, bay / 2 * 0.85))
        u += bay + pier

    def deck(u):
        return 8.0 + 0.4 * (1 - (u / (L / 2)) ** 2)

    m.add(0, bridge_body("pg", L, W, deck, spans, PF_D, True, 4.5, 1.0, PF), "bridge")
    houses = []
    u = -L / 2 + 6.0 + bay
    for i in range(n - 1):
        pc = u + pier / 2
        side = 1 if i % 2 == 0 else -1
        hh = 4.0 + 2.5 * _hash(i, 9)
        col = (PLAST_F, OCHRE_F, "#E6CBA8")[i % 3]
        houses.append(box(f"pg_h{i}", 4.0, 5.6, hh, (side * (W / 2 + 0.2), pc, deck(pc) - 1.0), col))
        houses.append(lean_to(f"pg_hr{i}", side * (W / 2 + 2.4), side * (W / 2 - 1.9), pc - 3.0, pc + 3.0, deck(pc) - 1.0 + hh, deck(pc) + hh, COPPI))
        houses.append(opening(f"pg_hd{i}", 1.0, 2.2, side * (W / 2 - 1.85), pc, deck(pc), 180 if side > 0 else 0, "round", DARK, 0.3))
        houses.append(box(f"pg_hw{i}", 0.2, 1.0, 1.0, (side * (W / 2 + 2.25), pc, deck(pc) + 1.0), DARK))
        for dy in (-2.2, 2.2):
            houses.append(beam(f"pg_hb{i}{dy:.0f}", (side * (W / 2 + 0.3), pc + dy, deck(pc) - 3.2), (side * (W / 2 + 2.0), pc + dy, deck(pc) - 1.0), 0.25))
        if i in (3, 4):
            houses.append(box(f"pg_bell{i}", 0.8, 1.6, 1.8, (side * (W / 2 + 0.2), pc, deck(pc) - 1.0 + hh + 0.6), PLAST_F))
            houses.append(opening(f"pg_bo{i}", 0.6, 1.0, side * (W / 2 + 0.2), pc - 0.85, deck(pc) - 1.0 + hh + 0.9, -90, "round", DARK, 0.2))
        u += bay + pier
    m.add(1, join(houses, "pg_houses"), "houses")
    return m


def ponte_santa_trinita(variant="1600"):
    m = Model("ponte-santa-trinita" + ("" if variant == "1600" else "-old"))
    L, W = 112.0, 10.0
    if variant == "1600":
        spans = [(-33.5, 14.0, 3.2, 4.0), (0.0, 16.0, 3.4, 4.6), (33.5, 14.0, 3.2, 4.0)]

        def deck(u):
            return 9.4 + 1.1 * (1 - (u / (L / 2)) ** 2)

        m.add(0, bridge_body("pt", L, W, deck, spans, "#D2C4A8", True, 8.0, 1.1, "#DED2BA"), "bridge")
        orn = []
        for uc, hs, sz, rise in spans:
            for s in (-1, 1):
                c = box(f"pt_cart{uc:.0f}{s}", 0.4, 2.2, 2.2, (s * (W / 2 + 0.3), uc, sz + rise + 0.3), WHITE_M)
                orn.append(c)
                orn.append(disc(f"pt_arms{uc:.0f}{s}", 0.6, s * (W / 2 + 0.55), uc, sz + rise + 1.4, 0 if s > 0 else 180, "#C8402E", 0.15, 10))
        for u in (-L / 2 + 1.0, L / 2 - 1.0):
            for s in (-1, 1):
                orn.append(box(f"pt_ped{u:.0f}{s}", 1.2, 1.2, 2.2, (s * (W / 2 - 0.6), u, deck(u)), "#DED2BA"))
        m.add(1, join(orn, "pt_orn"), "ornament")
    else:
        spans = [(-36.0, 7.6, 1.8, 7.0), (-18.0, 7.6, 1.8, 7.0), (0.0, 7.6, 1.8, 7.0), (18.0, 7.6, 1.8, 7.0), (36.0, 7.6, 1.8, 7.0)]

        def deck(u):
            return 11.0 + 0.8 * (1 - (u / (L / 2)) ** 2)

        m.add(0, bridge_body("pto", L, W, deck, spans, PF_D, True, 5.0, 1.0, PF), "bridge")
        m.add(1, join([box("pto_shr", 2.0, 2.4, 3.2, (W / 2 - 1.0, 0, deck(0)), PLAST_F), roof_x("pto_shrr", 2.0, 2.4, 1.0, W / 2 - 1.0, 0, deck(0) + 3.2, COPPI, 0.2),
                       opening("pto_sho", 1.0, 1.8, W / 2 - 1.0, -1.25, deck(0) + 0.4, -90, "round", DARK, 0.2)], "pto_shrine"), "shrine")
    return m


# ---------------------------------------------------------------- civic palaces
def bargello():
    m = Model("bargello")
    W, D = 44.0, 56.0
    m.add(0, plate(45, 57, PAVE_F, 0.25), "ground")
    fy0, fy1 = -28.0, -10.0
    walls = [rustic_box("bg_front", W, fy1 - fy0, 31.0, 0, (fy0 + fy1) / 2, 0, PF, "SEW", 2.7, 1.2, 0.24)]
    for s in (-1, 1):
        walls.append(rustic_box(f"bg_side{s}", 8.0, 30.0, 24.0, s * (W / 2 - 4.0), 5.0, 0, PF, "EW", 2.7, 1.2, 0.24))
    walls.append(rustic_box("bg_back", W, 8.0, 22.0, 0, 24.0, 0, PF_D, "NEW", 2.7, 1.2, 0.24))
    for s in "SEW":
        fx, fy, deg, L = face(W, fy1 - fy0, s, 0, (fy0 + fy1) / 2, 0.3)
        walls.append(bifore(f"bg_bf{s}", L * 0.7, 3 if s == "S" else 2, 2.2, 5.0, fx, fy, 19.0, deg, "round", PF_L, DARK, True, True))
        walls.append(openings(f"bg_sw{s}", L * 0.6, 3, 0.9, 1.4, fx, fy, 9.0, deg, "flat", DARK, 0.3))
    walls.append(opening("bg_door", 3.4, 5.4, 6.0, fy0 - 0.35, 0, -90, "round", DARK, 0.4))
    for s in (-1, 1):
        walls.append(openings(f"bg_sws{s}", 26.0, 4, 1.0, 1.6, s * (W / 2 + 0.3), 5.0, 14.0, 0 if s > 0 else 180, "round", DARK, 0.3))
    # the courtyard: paving, the open loggia and the outside staircase
    walls.append(box("bg_court", W - 16.0, 30.0, 0.35, (0, 5.0, 0), PAVE_L))
    walls.append(arcade_front("bg_lg", W - 16.0, 3, 1.4, 4.5, 8.0, 0, 20.0, 0, -90, PF_L, 1.0))
    walls.append(box("bg_lgd", W - 18.0, 3.0, 7.0, (0, 18.0 + 3.5, 0), DARK))
    walls.append(stair("bg_stair", 3.0, 8.0, 14.0, 12, (-W / 2 + 9.5, -2.0, 0), "E", PF_L))
    walls.append(box("bg_land", 3.0, 4.0, 8.0, (-W / 2 + 9.5, 7.0, 0), PF_L))
    m.add(0, join(walls, "bg_walls"), "walls")
    top = [corbel_gallery("bg_gal", W, fy1 - fy0, 31.0, 1.0, 1.8, 2.0, 2.4, PF, "guelf", 1.0, 0, (fy0 + fy1) / 2, None, "SEW")]
    top.append(hip("bg_roof", W - 2, fy1 - fy0 - 2, 2.6, 0, (fy0 + fy1) / 2, 31.0, COPPI, 0.5, 0.2))
    for s in (-1, 1):
        top.append(lean_to(f"bg_sr{s}", s * (W / 2 + 0.3), s * (W / 2 - 8.3), fy1, 20.0, 24.0, 26.0, COPPI))
        top.append(crenels(f"bg_sc{s}", 30.0, s * W / 2, 5.0, 24.0, 0 if s > 0 else 180, 0.9, "guelf", PF, 0.6))
    top.append(hip("bg_br", W, 8.0, 2.0, 0, 24.0, 22.0, COPPI, 0.5, 0.3))
    m.add(1, join(top, "bg_top"), "battlements")
    tx, ty, tw = 12.0, -23.5, 8.6
    tower = [rustic_box("bg_tw", tw, tw, 46.0, tx, ty, 0, PF, "SNEW", 2.2, 1.1, 0.24)]
    tower.append(corbel_gallery("bg_tg", tw, tw, 48.0, 0.9, 1.8, 2.0, 2.2, PF, "guelf", 0.9, tx, ty))
    tower.append(box("bg_tf", tw, tw, 2.0, (tx, ty, 46.0), PF))
    tower.append(box("bg_bell", 3.0, 3.0, 4.0, (tx, ty, 49.8), PF_L))
    tower.append(opening("bg_bo", 1.6, 2.6, tx, ty - 1.55, 50.4, -90, "round", DARK, 0.2))
    tower.append(roof_y("bg_bellr", 3.0, 3.0, 1.2, tx, ty, 53.8, COPPI, 0.2))
    m.add(2, join(tower, "bg_tower"), "tower")
    return m


def orsanmichele(variant="1490"):
    if variant == "loggia":
        m = Model("orsanmichele-loggia")
        W, D = 25.0, 40.0
        m.add(0, plate(26, 41, PAVE_F, 0.25), "ground")
        posts = []
        for i in range(4):
            for j in range(6):
                x = -W / 2 + 1.0 + (W - 2.0) * i / 3
                y = -D / 2 + 1.0 + (D - 2.0) * j / 5
                if 0 < i < 3 and 0 < j < 5:
                    posts.append(box(f"om_p{i}{j}", 1.2, 1.2, 9.0, (x, y, 0), BRICK_F))
                else:
                    posts.append(box(f"om_p{i}{j}", 1.6, 1.6, 9.0, (x, y, 0), BRICK_F))
        for s in "SNEW":
            fx, fy, deg, L = face(W, D, s, 0, 0)
            posts.append(arcade_front(f"om_a{s}", L, 3 if s in "SN" else 5, 1.6, 6.0, 9.6, fx, fy, 0, deg, BRICK_F, 0.8))
        posts.append(box("om_img", 0.4, 1.0, 1.4, (-W / 2 + 1.0, 0, 3.0), GOLD_F))
        for i in range(8):
            posts.append(box(f"om_sack{i}", 1.2, 0.8, 0.8, (-6 + 3.4 * (i % 4), -8 + 14 * (i // 4), 0), "#C9B28A"))
        m.add(0, join(posts, "om_posts"), "piers")
        m.add(1, hip("om_roof", W + 1.0, D + 1.0, 5.0, 0, 0, 9.6, COPPI, 0.5, 0.8), "roof")
        return m
    m = Model("orsanmichele")
    W, D, H = 25.0, 40.0, 34.0
    m.add(0, plate(26, 41, PAVE_F, 0.25), "ground")
    body = [box("om_b", W, D, H, (0, 0, 0), PF)]
    for s in "SNEW":
        fx, fy, deg, L = face(W, D, s, 0, 0, 0.05)
        n = 2 if s in "SN" else 3
        body.append(bifore(f"om_ar{s}", L * 0.82, n, L * 0.82 / n * 0.62, 11.0, fx, fy, 1.0, deg, "pointed", PF_L, "#4A4A55", True, True))
        body.append(rects(f"om_band{s}", [(-L / 2, 13.2, L / 2, 13.8), (-L / 2, 23.2, L / 2, 23.7)], fx, fy, 0, deg, PF_L, 0.3, y0=-0.1))
        body.append(bifore(f"om_u1{s}", L * 0.7, n, 2.4, 5.6, fx, fy, 15.6, deg, "round", PF_L, DARK, True, True))
        body.append(bifore(f"om_u2{s}", L * 0.7, n, 2.4, 5.6, fx, fy, 25.6, deg, "round", PF_L, DARK, True, True))
        # tabernacles with the guild saints on the piers
        bay = L * 0.82 / n
        for k in range(n + 1):
            u = -L * 0.41 + bay * k
            nm = f"om_t{s}{k}"
            tab = [multi_slab(nm + "_f", [[(u + a, b + 1.6) for a, b in arch_pts(2.4, 5.4, "pointed")]], 0.3, WHITE_M, y0=-0.2),
                   multi_slab(nm + "_n", [[(u + a, b + 2.0) for a, b in arch_pts(1.6, 4.6, "pointed")]], 0.3, DARK, y0=-0.3),
                   multi_slab(nm + "_g", [[(u - 1.4, 7.0), (u + 1.4, 7.0), (u, 9.0)]], 0.3, WHITE_M, y0=-0.25)]
            st = statue(nm + "_s", u, -0.45, 2.1, 3.0, BRONZE_F if k % 2 else "#E2DBCB")
            body.append(on_wall(join(tab + [st], nm), fx, fy, 0, deg))
    m.add(0, join(body, "om_body"), "walls")
    top = [box("om_corn", W + 1.6, D + 1.6, 1.0, (0, 0, H), PF_L)]
    for s in "SNEW":
        fx, fy, deg, L = face(W, D, s, 0, 0)
        for i in range(int(L / 1.6)):
            u = -L / 2 + L * (i + 0.5) / int(L / 1.6)
            top.append(on_wall(box(f"om_mo{s}{i}", 0.5, 0.8, 0.8, (u, -0.4, 0), PF_L), fx, fy, H - 0.8, deg))
    top.append(hip("om_roof", W, D, 3.0, 0, 0, H + 1.0, COPPI, 0.5, 0.4))
    m.add(1, join(top, "om_top"), "roof")
    return m


def palazzo_medici():
    m = Model("palazzo-medici")
    W, D = 42.0, 56.0
    y0, y1 = -28.0, 12.0
    cy = (y0 + y1) / 2
    H1, H2, H3 = 9.5, 17.5, 25.5
    m.add(0, plate(43, 57, PAVE_F, 0.25), "ground")
    walls = []
    dd = y1 - y0
    walls.append(box("pm_fr", W, 14.0, H3, (0, y0 + 7.0, 0), PF_D))
    walls.append(box("pm_bk", W, 12.0, H3, (0, y1 - 6.0, 0), PF_D))
    for s in (-1, 1):
        walls.append(box(f"pm_sd{s}", 13.0, dd, H3, (s * (W / 2 - 6.5), cy, 0), PF_D))
    for s in "SEW":
        fx, fy, deg, L = face(W, dd, s, 0, cy)
        walls.append(rusticate(f"pm_r1{s}", L, H1, fx, fy, 0, deg, PF, 2.8, 1.25, 0.55, vary=True))
        walls.append(rusticate(f"pm_r2{s}", L, H2 - H1, fx, fy, H1, deg, PF_L, 2.4, 0.95, 0.14, vary=False))
        walls.append(rects(f"pm_r3{s}", [(-L / 2, 0, L / 2, H3 - H2)], fx, fy, H2, deg, "#DCCAA6", 0.1, y0=-0.05))
        walls.append(rects(f"pm_sc{s}", [(-L / 2, H1 - 0.3, L / 2, H1 + 0.3), (-L / 2, H2 - 0.3, L / 2, H2 + 0.3)], fx, fy, 0, deg, PF_L, 0.6, y0=-0.3))
        n = 10 if s == "S" else 9
        walls.append(bifore(f"pm_b2{s}", L * 0.92, n, 2.0, 4.6, fx + 0.2 * math.cos(math.radians(deg)), fy + 0.2 * math.sin(math.radians(deg)), H1 + 1.4, deg, "round", PF_L, DARK, True, True))
        walls.append(bifore(f"pm_b3{s}", L * 0.92, n, 2.0, 4.6, fx + 0.2 * math.cos(math.radians(deg)), fy + 0.2 * math.sin(math.radians(deg)), H2 + 1.4, deg, "round", PF_L, DARK, True, True))
        walls.append(box(f"pm_bench{s}", L if s == "S" else 0.9, 0.9 if s == "S" else L, 0.6, (fx + 0.45 * math.cos(math.radians(deg)), fy + 0.45 * math.sin(math.radians(deg)), 0), PF_L))
    # the ground floor: the portal on Via Larga, small high windows, the open corner loggia
    walls.append(opening("pm_door", 3.6, 6.6, 4.0, y0 - 0.6, 0, -90, "round", DARK, 0.5))
    walls.append(openings("pm_gw", 18.0, 3, 1.4, 1.6, 8.0, y0 - 0.6, 5.2, -90, "flat", DARK, 0.4))
    walls.append(box("pm_lgd", 13.0, 0.4, 8.0, (-W / 2 + 7.0, y0 - 0.45, 0), DARK))
    walls.append(arcade_front("pm_lg", 13.5, 3, 1.0, 5.0, H1 - 0.2, -W / 2 + 6.75, y0 - 0.75, 0, -90, PF, 0.9))
    walls.append(box("pm_lgdw", 0.4, 10.0, 8.0, (-W / 2 - 0.45, y0 + 5.5, 0), DARK))
    walls.append(arcade_front("pm_lgw", 10.0, 2, 1.0, 5.0, H1 - 0.2, -W / 2 - 0.75, y0 + 5.5, 0, 180, PF, 0.9))
    walls.append(box("pm_armsb", 1.8, 0.4, 2.0, (-W / 2 + 1.2, y0 - 0.9, H1 + 0.4), GOLD_F))
    # courtyard with Michelozzo's arcade
    walls.append(box("pm_court", 16.0, 14.0, 0.3, (0, y0 + 14.0 + 7.0, 0), PAVE_L))
    for s in "SNEW":
        fx, fy, deg, L = face(16.0, 14.0, s, 0, y0 + 21.0)
        walls.append(box(f"pm_cd{s}", L if s in "SN" else 0.3, 0.3 if s in "SN" else L, 6.5, (fx - 0.6 * math.cos(math.radians(deg)), fy - 0.6 * math.sin(math.radians(deg)), 0), DARK))
        walls.append(arcade_front(f"pm_ca{s}", L, 3 if s in "SN" else 3, 0.0, 4.2, 7.0, fx, fy, 0, deg + 180, PF_L, 0.6))
        for k in range(4):
            u = -L / 2 + L * k / 3
            cx_ = fx + u * math.cos(math.radians(deg + 90))
            cy_ = fy + u * math.sin(math.radians(deg + 90))
            walls.append(column(f"pm_cc{s}{k}", cx_ - 0.4 * math.cos(math.radians(deg)), cy_ - 0.4 * math.sin(math.radians(deg)), 0, 0.32, 4.2, SERENA, True, 8))
    m.add(0, join(walls, "pm_walls"), "walls")
    top = [box("pm_cornS", W + 4.4, 16.2, 1.8, (0, y0 + 6.9, H3), PF_L), box("pm_cornN", W + 4.4, 14.2, 1.8, (0, y1 - 4.9, H3), PF_L)]
    for s_ in (-1, 1):
        top.append(box(f"pm_cornE{s_}", 15.2, dd + 4.4, 1.8, (s_ * (W / 2 - 5.4), cy, H3), PF_L))
    for s in "SEW":
        fx, fy, deg, L = face(W, dd, s, 0, cy)
        n = int(L / 1.5)
        for i in range(n):
            u = -L / 2 + L * (i + 0.5) / n
            top.append(on_wall(box(f"pm_mo{s}{i}", 0.5, 2.0, 0.9, (u, -1.0, 0), PF_L), fx, fy, H3 - 0.9, deg))
    for s in (-1, 1):
        top.append(lean_to(f"pm_rs{s}", s * (W / 2 + 1.6), s * 8.0, y0, y1, H3 + 1.8, H3 + 5.0, COPPI))
    top.append(lean_to_y("pm_rf", -8.0, 8.0, y0 - 1.6, y0 + 14.0, H3 + 1.8, H3 + 5.0, COPPI))
    top.append(lean_to_y("pm_rb", -8.0, 8.0, y1 + 1.6, y1 - 12.0, H3 + 1.8, H3 + 5.0, COPPI))
    m.add(1, join(top, "pm_top"), "cornice")
    gd = [box("pm_gard", W, D / 2 - y1, 0.35, (0, (y1 + D / 2) / 2, 0), GRASS_F),
          box("pm_gw1", W, 0.8, 4.0, (0, D / 2 - 0.4, 0), PF_L), box("pm_gw2", 0.8, D / 2 - y1, 4.0, (W / 2 - 0.4, (y1 + D / 2) / 2, 0), PF_L),
          box("pm_gw3", 0.8, D / 2 - y1, 4.0, (-W / 2 + 0.4, (y1 + D / 2) / 2, 0), PF_L)]
    for i in range(5):
        gd.append(tree(f"pm_t{i}", 1.8, (-14 + 7 * i, 21.0 + 3.0 * (i % 2), 0.3), HEDGE_F, TIMBER_F, "round" if i % 2 else "cypress"))
    gd.append(box("pm_hedge", 20.0, 1.0, 1.0, (0, 16.5, 0.3), HEDGE_F))
    gd.append(statue("pm_judith", 0, 22.0, 0.3, 2.6, BRONZE_F))
    m.add(2, join(gd, "pm_garden"), "garden")
    return m


# ---------------------------------------------------------------- churches
def san_lorenzo(variant="1490"):
    m = Model("san-lorenzo" + {"1490": "", "1600": "-1600", "old": "-old"}[variant])
    m.add(0, plate(60, 100, PAVE_F, 0.25), "ground")
    if variant == "old":
        w, r = nave_block("slo", -40.0, 18.0, 10.0, 17.0, 6.0, 9.5, PLAST_F, COPPI, "round", 9, "window", None)
        fr = church_front("slo_f", -40.0, 22.0, 10.0, 17.0, 9.5, PLAST_F, 1, False, "round")
        ap = join([cylinder("slo_ap", 5.0, 13.0, (0, 18.0, 0), PLAST_F, verts=16), cylinder("slo_apr", 5.3, 2.6, (0, 18.0, 13.0), COPPI, verts=16, r_top=0.3)], "slo_apse")
        m.add(0, join([w, fr, ap], "slo_walls"), "walls")
        m.add(1, r, "roofs")
        m.add(2, bell_tower("slo_tw", 14.0, 8.0, 6.0, 30.0, PLAST_F, "spire", COPPI), "campanile")
        return m
    w, r = nave_block("sl", -48.0, 12.0, 12.0, 21.0, 6.0, 12.5, PLAST_F, COPPI, "round", 8, "oculus", SERENA, 4.5, 8.5)
    fr = church_front("sl_f", -48.0, 33.0, 12.0, 21.0, 12.5, BRICK_F, 3, False, "round", False, True, None, True)
    tw, tr = transept("sl_t", 12.0, 26.0, 28.0, 21.0, PLAST_F, COPPI)
    cw, cr = transept("sl_c", 26.0, 38.0, 6.0, 21.0, PLAST_F, COPPI)
    side = []
    for s in (-1, 1):
        side.append(box(f"sl_cc{s}", 10.0, 12.0, 12.0, (s * 11.0, 32.0, 0), PLAST_F))
        side.append(roof_y(f"sl_ccr{s}", 10.0, 12.0, 2.4, s * 11.0, 32.0, 12.0, COPPI, 0.3))
    m.add(0, join([w, fr, tw, cw] + side, "sl_walls"), "walls")
    m.add(1, join([r, tr, cr], "sl_roofs"), "roofs")
    domes = [ren_dome("sl_dome", 6.4, 0, 19.0, 21.0 + 3.6, 3.0, COPPI, PLAST_F, 12, 0.9, WHITE_M, 12, PLAST_F)]
    domes.append(box("sl_dbase", 13.0, 13.0, 3.6, (0, 19.0, 21.0), PLAST_F))
    # the Old Sacristy on the west transept arm, and Michelangelo's New Sacristy on the east (1600)
    sx = -18.5
    domes.append(box("sl_os", 11.0, 11.0, 14.0, (sx, 32.0, 0), PLAST_F))
    for s in "WN":
        fx, fy, deg, L = face(11.0, 11.0, s, sx, 32.0, 0.05)
        domes.append(rects(f"sl_osp{s}", [(-L / 2, 0, -L / 2 + 0.6, 14.0), (L / 2 - 0.6, 0, L / 2, 14.0), (-L / 2, 13.2, L / 2, 14.0)], fx, fy, 0, deg, SERENA, 0.2, y0=-0.1))
        domes.append(opening(f"sl_osw{s}", 1.6, 3.2, fx, fy, 8.0, deg, "round", DARK, 0.3))
    domes.append(ren_dome("sl_osd", 4.6, sx, 32.0, 14.0, 1.6, COPPI, PLAST_F, 12, 0.75, WHITE_M, 12, PLAST_F))
    if variant == "1600":
        nx = 18.5
        domes.append(box("sl_ns", 11.0, 11.0, 16.0, (nx, 32.0, 0), PLAST_F))
        for s in "EN":
            fx, fy, deg, L = face(11.0, 11.0, s, nx, 32.0, 0.05)
            domes.append(rects(f"sl_nsp{s}", [(-L / 2, 0, -L / 2 + 0.6, 16.0), (L / 2 - 0.6, 0, L / 2, 16.0), (-L / 2, 15.2, L / 2, 16.0)], fx, fy, 0, deg, SERENA, 0.2, y0=-0.1))
            domes.append(opening(f"sl_nsw{s}", 1.6, 3.2, fx, fy, 9.0, deg, "round", DARK, 0.3))
        domes.append(ren_dome("sl_nsd", 4.6, nx, 32.0, 16.0, 3.0, LEAD_F, PLAST_F, 8, 0.85, WHITE_M, 8, PLAST_F))
        # the Laurentian Library along the west side of the cloister
        domes.append(box("sl_lib", 10.0, 46.0, 15.0, (-25.0, -14.0, 0), PLAST_F))
        domes.append(roof_y("sl_libr", 10.0, 46.0, 3.0, -25.0, -14.0, 15.0, COPPI, 0.3))
        domes.append(openings("sl_libw", 44.0, 15, 1.0, 2.6, -30.05, -14.0, 10.0, 180, "flat", DARK, 0.3))
    m.add(2, join([d for d in domes if d is not None], "sl_domes"), "domes")
    return m


def santo_spirito(variant="1490"):
    m = Model("santo-spirito" + ("-1600" if variant == "1600" else ""))
    m.add(0, plate(60, 98, PAVE_F, 0.25), "ground")
    w, r = nave_block("ss", -47.0, 10.0, 12.5, 25.0, 6.5, 13.5, OCHRE_F, COPPI, "round", 8, "oculus", SERENA, 3.5, 10.5)
    fr = church_front("ss_f", -47.0, 33.0, 12.5, 25.0, 13.5, "#E9D7AE", 3, True, "round", True, True, SERENA)
    tw, tr = transept("ss_t", 10.0, 38.0, 29.0, 25.0, OCHRE_F, COPPI)
    cw, cr = transept("ss_c", 38.0, 48.0, 12.0, 25.0, OCHRE_F, COPPI)
    m.add(0, join([w, fr, tw, cw], "ss_walls"), "walls")
    m.add(1, join([r, tr, cr], "ss_roofs"), "roofs")
    dm = [box("ss_db", 14.0, 14.0, 3.0, (0, 24.0, 25.0), OCHRE_F),
          ren_dome("ss_dome", 7.0, 0, 24.0, 28.0, 3.6, COPPI, OCHRE_F, 12, 0.95, WHITE_M, 12, "#E8DDC6")]
    if variant == "1600":
        dm.append(bell_tower("ss_tw", 21.0, 42.0, 6.0, 52.0, "#E2CFA6", "cupola", COPPI, 41.0, 5))
        dm.append(rects("ss_twp", [(-3.0, 0, -2.5, 52.0), (2.5, 0, 3.0, 52.0)], 21.0, 38.95, 0, -90, SERENA, 0.2))
    m.add(2, join(dm, "ss_dome"), "dome")
    return m


def pazzi_chapel(name, x, y):
    """Brunelleschi's chapter house in the cloister of Santa Croce: a portico of six columns, a dome on a drum, a small dome over the porch."""
    W, D, H = 18.0, 11.0, 12.0
    parts = [box(name + "_b", W, D, H, (x, y, 0), PLAST_F)]
    py = y - D / 2 - 2.6
    parts.append(box(name + "_attic", W, 5.2, 3.6, (x, py, 8.0), PLAST_F))
    parts.append(rects(name + "_ap", [(-W / 2 + 1.0 + i * 2.0, 1.0, -W / 2 + 1.6 + i * 2.0, 3.0) for i in range(9)], x, py - 2.62, 8.0, -90, SERENA, 0.2))
    for i in range(6):
        u = -W / 2 + 1.0 + (W - 2.0) * i / 5
        if i in (2, 3):
            continue
        parts.append(column(f"{name}_c{i}", x + u, py - 2.0, 0, 0.4, 7.4, SERENA, True, 8))
    parts.append(opening(name + "_arch", 5.2, 10.6, x, py - 2.62, 0, -90, "round", DARK, 0.2))
    parts.append(box(name + "_pd", W - 1.0, 0.3, 7.4, (x, py + 2.4, 0), DARK))
    parts.append(roof_x(name + "_pr", W, 5.2, 1.4, x, py, 11.6, COPPI, 0.3))
    parts.append(ren_dome(name + "_d", 4.6, x, y, H, 2.0, COPPI, PLAST_F, 12, 0.8, WHITE_M, 12, PLAST_F))
    parts.append(dome(name + "_pdome", 2.0, (x, py, 13.0), COPPI, squash=0.6, segments=12, rings=5))
    return join(parts, name)


def santa_croce(variant="1490"):
    m = Model("santa-croce" + ("-1300" if variant == "1300" else ""))
    m.add(0, plate(75, 118, PAVE_F, 0.25), "ground")
    nave_w, nave_h, aisle_w, aisle_h = 19.0, 31.0, 10.0, 18.0
    if variant == "1300":
        # Arnolfo's east end rising round the friars' first church
        old = [box("sc3_old", 14.0, 38.0, 13.0, (0, -22.0, 0), PLAST_F), roof_y("sc3_oldr", 14.0, 38.0, 3.6, 0, -22.0, 13.0, COPPI, 0.3),
               church_front("sc3_of", -41.0, 14.0, 14.0, 13.0, 13.0, PLAST_F, 1, True, "round", False, False),
               openings("sc3_ow1", 34.0, 6, 1.2, 3.0, 7.05, -22.0, 6.0, 0, "pointed", DARK, 0.3), openings("sc3_ow2", 34.0, 6, 1.2, 3.0, -7.05, -22.0, 6.0, 180, "pointed", DARK, 0.3)]
        m.add(0, join(old, "sc3_old"), "old church")
        new = [box("sc3_tr", 74.0, 2.0, 12.0, (0, 22.5, 0), PF), box("sc3_tr2", 74.0, 2.0, 9.0, (0, 35.0, 0), PF)]
        for s in (-1, 1):
            new.append(box(f"sc3_te{s}", 2.0, 14.0, 10.0, (s * 36.0, 29.0, 0), PF))
            new.append(box(f"sc3_nw{s}", 2.0, 30.0, 6.0 + 2.0 * (s > 0), (s * 19.5, 6.0, 0), PF))
            new.append(box(f"sc3_fd{s}", 2.0, 50.0, 0.8, (s * 19.5, -34.0, 0), PF_D))
        for i in range(9):
            u = -32.0 + 8.0 * i
            if abs(u) < 8:
                continue
            new.append(box(f"sc3_ch{i}", 1.0, 8.0, 8.0 + 3 * _hash(i, 2), (u, 40.0, 0), PF))
        new.append(apse_polygon("sc3_apse", 8.0, 90, 0, 44.0, 16.0, PF, PF, 0.1, (1.6, 8.0, 3.0), None))
        m.add(1, join(new, "sc3_new"), "new walls")
        sc = []
        for i in range(10):
            sc.append(box(f"sc3_sp{i}", 0.3, 0.3, 18.0, (-36.0 + 8.0 * i, 21.0, 0), TIMBER_F))
        sc.append(box("sc3_sb", 74.0, 1.2, 0.2, (0, 21.0, 9.0), TIMBER_F))
        sc.append(box("sc3_sb2", 74.0, 1.2, 0.2, (0, 21.0, 14.0), TIMBER_F))
        sc.append(box("sc3_cr", 0.6, 0.6, 24.0, (10.0, 30.0, 0), TIMBER_F))
        sc.append(beam("sc3_crj", (10.0, 30.0, 23.0), (18.0, 22.0, 26.0), 0.4))
        m.add(2, join(sc, "sc3_scaff"), "scaffolding")
        return m
    w, r = nave_block("sc", -57.0, 22.0, nave_w, nave_h, aisle_w, aisle_h, PF_L, COPPI, "pointed", 7, "window", None, 0, None, True)
    fr = church_front("sc_f", -57.0, nave_w + 2 * aisle_w, nave_w, nave_h, aisle_h, PF, 3, True, "pointed")
    tw, tr = transept("sc_t", 22.0, 36.0, 37.0, 26.0, PF_L, COPPI, "pointed")
    ch = []
    for s in (-1, 1):
        ch.append(box(f"sc_ch{s}", 26.0, 8.0, 14.0, (s * 23.5, 40.0, 0), PF_L))
        ch.append(lean_to_y(f"sc_chr{s}", s * 10.0, s * 36.5, 44.3, 35.8, 14.0, 16.0, COPPI) if s > 0 else lean_to_y(f"sc_chr{s}", -36.5, -10.0, 44.3, 35.8, 14.0, 16.0, COPPI))
        ch.append(openings(f"sc_chw{s}", 24.0, 5, 0.9, 4.0, s * 23.5, 44.05, 5.0, 90, "pointed", DARK, 0.3))
    ch.append(apse_polygon("sc_apse", 8.0, 90, 0, 40.0, 27.0, PF_L, COPPI, 6.0, (1.8, 15.0, 5.0), None))
    m.add(0, join([w, fr, tw] + ch, "sc_walls"), "walls")
    m.add(1, join([r, tr], "sc_roofs"), "roofs")
    clo = [box("sc_clp", 17.0, 40.0, 0.3, (28.0, -22.0, 0), GRASS_F)]
    for (cx, cy, w_, d_, ff) in ((28.0, -43.0, 18.0, 4.0, 90), (37.0 - 1.5, -22.0, 3.0, 40.0, 180)):
        clo.append(box(f"sc_cl{ff}", w_, d_, 7.0, (cx, cy, 0), PLAST_F))
        clo.append(hip(f"sc_clr{ff}", w_, d_, 1.4, cx, cy, 7.0, COPPI, 0.8, 0.3))
    clo.append(arcade_front("sc_cla", 17.0, 5, 0.0, 3.6, 6.0, 28.0, -41.0, 0, 90, PLAST_F, 0.5))
    clo.append(pazzi_chapel("sc_pazzi", 28.0, 6.5))
    m.add(2, join(clo, "sc_cloister"), "Pazzi Chapel")
    return m


def alberti_front(name, y, W, nave_w, nave_h, aisle_h):
    """Alberti's façade of Santa Maria Novella: a striped Gothic lower storey with a classical portal, an attic band,
    a temple front with an oculus and pediment, and two great scrolls over the aisles."""
    parts = []
    lo = aisle_h + 0.5
    parts.append(on_wall(box(name + "_low", W, 1.2, lo, (0, 0.6, 0), WHITE_M), 0, y, 0, -90))
    stripes = [(-W / 2 + i * W / 26, 0.6, -W / 2 + i * W / 26 + W / 52, lo - 3.0) for i in range(26)]
    parts.append(rects(name + "_st", [it for it in stripes if abs((it[0] + it[2]) / 2) > 4.2], 0, y - 0.05, 0, -90, GREEN_M, 0.12, y0=-0.06))
    for k, u in enumerate((-W / 2 + 0.9, -nave_w / 2 - 0.2, nave_w / 2 + 0.2, W / 2 - 0.9)):
        parts.append(rects(f"{name}_pil{k}", [(u - 0.8, 0, u + 0.8, lo - 2.5)], 0, y - 0.15, 0, -90, WHITE_M, 0.4, y0=-0.2))
        parts.append(rects(f"{name}_pis{k}", [(u - 0.8, 0.5 + j * 1.2, u + 0.8, 1.0 + j * 1.2) for j in range(int((lo - 3.5) / 1.2))], 0, y - 0.45, 0, -90, GREEN_M, 0.1, y0=-0.05))
    av = [[(u + a, b + 0.6) for a, b in arch_pts(2.2, 4.6, "pointed")] for u in (-W / 2 + 3.2, -W / 2 + 6.2, -W / 2 + 9.2, W / 2 - 3.2, W / 2 - 6.2, W / 2 - 9.2)]
    parts.append(on_wall(multi_slab(name + "_av", av, 0.25, GREEN_M, y0=-0.15), 0, y, 0, -90))
    parts.append(on_wall(multi_slab(name + "_dfr", [arch_pts(5.6, 10.0, "round")], 0.4, GREEN_M, y0=-0.25), 0, y, 0, -90))
    parts.append(opening(name + "_door", 3.6, 7.6, 0, y - 0.5, 0, -90, "round", DARK, 0.3))
    parts.append(rects(name + "_attic", [(-W / 2, lo - 2.6, W / 2, lo)], 0, y - 0.3, 0, -90, WHITE_M, 0.4, y0=-0.2))
    parts.append(rects(name + "_atq", [(-W / 2 + 1.0 + i * W / 14, lo - 2.1, -W / 2 + 2.0 + i * W / 14, lo - 0.5) for i in range(14)], 0, y - 0.55, 0, -90, GREEN_M, 0.1, y0=-0.05))
    # the upper temple front
    up_h = nave_h - lo
    parts.append(on_wall(box(name + "_up", nave_w, 1.0, up_h, (0, 0.5, lo), WHITE_M), 0, y, 0, -90))
    for k in range(4):
        u = -nave_w / 2 + 0.7 + (nave_w - 1.4) * k / 3
        parts.append(rects(f"{name}_upp{k}", [(u - 0.6, lo, u + 0.6, nave_h - 1.2)], 0, y - 0.1, 0, -90, GREEN_M, 0.2, y0=-0.1))
    parts.append(oculus(name + "_oc", 2.2, 0, y - 0.2, lo + up_h * 0.5, -90, GREEN_M, DARK, 20))
    parts.append(rects(name + "_ent", [(-nave_w / 2 - 0.4, nave_h - 1.2, nave_w / 2 + 0.4, nave_h)], 0, y - 0.25, 0, -90, WHITE_M, 0.5, y0=-0.25))
    parts.append(pediment(name + "_ped", nave_w + 0.8, nave_w * 0.24, 0, y - 0.1, nave_h, -90, WHITE_M, 1.0))
    parts.append(disc(name + "_sun", 1.2, 0, y - 0.7, nave_h + nave_w * 0.09, -90, GOLD_F, 0.2, 16))
    for s in (-1, 1):
        r0 = W / 2 - nave_w / 2
        pts = [(s * nave_w / 2, lo)] + [(s * (nave_w / 2 + r0 * (1 - math.cos(math.pi / 2 * k / 8))), lo + up_h * 0.62 * (1 - math.sin(math.pi / 2 * k / 8))) for k in range(9)]
        pts = [(s * nave_w / 2, lo + up_h * 0.62)] + pts[1:]
        if s < 0:
            pts = list(reversed(pts))
        parts.append(on_wall(multi_slab(f"{name}_scroll{s}", [pts], 0.8, WHITE_M, y0=0.2), 0, y, 0, -90))
        parts.append(disc(f"{name}_sce{s}", 1.4, s * (nave_w / 2 + 1.6), y - 0.35, lo + up_h * 0.42, -90, GREEN_M, 0.2, 14))
        parts.append(disc(f"{name}_scf{s}", 0.8, s * (nave_w / 2 + 1.6), y - 0.5, lo + up_h * 0.42, -90, WHITE_M, 0.2, 10))
    return join(parts, name)


def santa_maria_novella(variant="1490"):
    m = Model("santa-maria-novella" + ("-1300" if variant == "1300" else ""))
    m.add(0, plate(62, 100, PAVE_F, 0.25), "ground")
    nave_w, nave_h, aisle_w, aisle_h = 14.0, 28.0, 8.0, 17.0
    W = nave_w + 2 * aisle_w
    tw, tr = transept("smn_t", 22.0, 34.0, 31.0, 24.0, PF_L, COPPI, "pointed")
    ch = [box("smn_mc", 12.0, 14.0, 22.0, (0, 41.0, 0), PF_L), roof_y("smn_mcr", 12.0, 14.0, 3.6, 0, 41.0, 22.0, COPPI, 0.3),
          opening("smn_mcw", 2.2, 12.0, 0, 48.05, 6.0, 90, "pointed", DARK, 0.3), oculus("smn_mco", 1.6, 0, 48.1, 19.0, 90, PF_L, DARK, 14)]
    for s in (-1, 1):
        for k in range(2):
            cx = s * (10.5 + 9.0 * k)
            ch.append(box(f"smn_ch{s}{k}", 8.0, 12.0, 15.0, (cx, 40.0, 0), PF_L))
            ch.append(roof_y(f"smn_chr{s}{k}", 8.0, 12.0, 2.4, cx, 40.0, 15.0, COPPI, 0.3))
            ch.append(opening(f"smn_chw{s}{k}", 1.4, 7.0, cx, 46.05, 4.0, 90, "pointed", DARK, 0.3))
    if variant == "1300":
        nv = [box("smn3_e", W, 18.0, aisle_h, (0, 13.0, 0), PF_L), box("smn3_en", nave_w, 18.0, nave_h - 4.0, (0, 13.0, 0), PF_L)]
        for s in (-1, 1):
            nv.append(box(f"smn3_n{s}", 1.6, 52.0, 3.0 + 3.0 * (s > 0), (s * (W / 2 - 0.8), -22.0, 0), PF_L))
            nv.append(box(f"smn3_p{s}", 1.6, 52.0, 1.0, (s * (nave_w / 2), -22.0, 0), PF_D))
        sc = [box(f"smn3_sp{i}", 0.3, 0.3, 26.0, (-W / 2 - 1.0 + (W + 2.0) * (i % 2), 4.0 + 6.0 * (i // 2), 0), TIMBER_F) for i in range(6)]
        sc.append(box("smn3_crm", 0.6, 0.6, 30.0, (0, -10.0, 0), TIMBER_F))
        sc.append(beam("smn3_crj", (0, -10.0, 29.0), (6.0, 2.0, 32.0), 0.4))
        m.add(0, join(nv + [tw] + ch, "smn3_walls"), "walls")
        m.add(1, join([tr], "smn3_roofs"), "roofs")
        m.add(2, join(sc, "smn3_scaff"), "scaffolding")
        return m
    w, r = nave_block("smn", -48.0, 22.0, nave_w, nave_h, aisle_w, aisle_h, PF_L, COPPI, "pointed", 6, "oculus", None, 0, None, True)
    fr = alberti_front("smn_f", -48.0, W, nave_w, nave_h, aisle_h)
    tower = bell_tower("smn_tw", 23.0, 41.0, 7.0, 50.0, "#C9B08A", "spire", COPPI, 40.0, 5)
    m.add(0, join([w, tw] + ch, "smn_walls"), "walls")
    m.add(1, join([r, tr], "smn_roofs"), "roofs")
    m.add(2, join([fr, tower], "smn_front"), "façade")
    return m


def san_miniato():
    m = Model("san-miniato")
    m.add(0, plate(48, 75, "#B9B49C", 0.3), "ground")
    nave_w, nave_h, aisle_w, aisle_h = 12.0, 18.0, 6.0, 10.0
    W = nave_w + 2 * aisle_w
    y0 = -31.0
    w, r = nave_block("sm", y0, 20.0, nave_w, nave_h, aisle_w, aisle_h, PF_L, COPPI, "round", 6, "window", None)
    ap = [cylinder("sm_ap", 6.0, 15.0, (0, 20.0, 0), PF_L, verts=16), cylinder("sm_apr", 6.3, 3.0, (0, 20.0, 15.0), COPPI, verts=16, r_top=0.3)]
    m.add(0, join([w] + ap, "sm_walls"), "walls")
    m.add(1, r, "roofs")
    # the inlaid marble front
    fr = []
    prof = [(-W / 2, 0), (W / 2, 0), (W / 2, aisle_h), (nave_w / 2, aisle_h + 2.0), (nave_w / 2, nave_h), (0, nave_h + nave_w * 0.3), (-nave_w / 2, nave_h), (-nave_w / 2, aisle_h + 2.0), (-W / 2, aisle_h)]
    fr.append(on_wall(multi_slab("sm_fw", [prof], 1.0, WHITE_M, y0=0.5), 0, y0, 0, -90))
    arc = [[(u + a, b + 0.4) for a, b in arch_pts(3.4, 7.6, "round")] for u in [-W / 2 + 2.4 + (W - 4.8) * i / 4 for i in range(5)]]
    fr.append(on_wall(multi_slab("sm_arc", arc, 0.2, GREEN_M, y0=-0.1), 0, y0, 0, -90))
    inner = [[(u + a, b + 0.4) for a, b in arch_pts(2.4, 7.0, "round")] for u in [-W / 2 + 2.4 + (W - 4.8) * i / 4 for i in range(5)]]
    fr.append(on_wall(multi_slab("sm_arci", inner, 0.2, WHITE_M, y0=-0.2), 0, y0, 0, -90))
    for k, u in enumerate((-W / 2 + 2.4 + (W - 4.8) / 4, 0, W / 2 - 2.4 - (W - 4.8) / 4)):
        fr.append(rects(f"sm_door{k}", [(u - 1.0, 0.4, u + 1.0, 4.6)], 0, y0 - 0.35, 0, -90, DARK, 0.2))
    fr.append(rects("sm_band", [(-W / 2, aisle_h - 0.6, W / 2, aisle_h)], 0, y0 - 0.1, 0, -90, GREEN_M, 0.2))
    geo = []
    for i in range(6):
        u = -nave_w / 2 + 1.0 + (nave_w - 2.0) * i / 5
        geo.append((u - 0.25, aisle_h + 0.6, u + 0.25, nave_h - 0.6))
    for j in range(3):
        v = aisle_h + 1.4 + j * 2.4
        geo += [(-W / 2 + 0.6, v, -nave_w / 2 - 0.4, v + 0.3), (nave_w / 2 + 0.4, v, W / 2 - 0.6, v + 0.3)]
    fr.append(rects("sm_geo", geo, 0, y0 - 0.1, 0, -90, GREEN_M, 0.2))
    fr.append(rects("sm_win", [(-1.2, aisle_h + 1.2, 1.2, aisle_h + 4.0)], 0, y0 - 0.25, 0, -90, DARK, 0.2))
    fr.append(pediment("sm_wped", 3.6, 1.2, 0, y0 - 0.2, aisle_h + 4.0, -90, GREEN_M, 0.3))
    fr.append(rects("sm_mos", [(-2.6, nave_h - 4.2, 2.6, nave_h - 0.8)], 0, y0 - 0.2, 0, -90, GOLD_F, 0.2))
    fr.append(pediment("sm_ped", nave_w, nave_w * 0.3, 0, y0 - 0.1, nave_h, -90, WHITE_M, 0.8))
    fr.append(rects("sm_pedg", [(-0.3, nave_h + 0.4, 0.3, nave_h + nave_w * 0.24)], 0, y0 - 0.35, 0, -90, GREEN_M, 0.2))
    fr.append(box("sm_eagle", 1.4, 0.6, 1.2, (0, y0 - 0.2, nave_h + nave_w * 0.3), BRONZE_F))
    fr.append(box("sm_terrace", W + 6.0, 6.0, 0.8, (0, y0 - 3.0, 0), PF_D))
    fr.append(stair("sm_steps", 14.0, 0.8, 3.0, 4, (0, y0 - 6.0, 0), "S", PF_D))
    m.add(2, join(fr, "sm_front"), "façade")
    pal = [box("sm_pal", 11.0, 26.0, 17.0, (18.5, -14.0, 0), PF_L), hip("sm_palr", 11.0, 26.0, 2.0, 18.5, -14.0, 17.0, COPPI, 0.6, 0.3),
           crenel_ring("sm_palc", 11.0, 26.0, 17.0, 0.9, "guelf", PF_L, 18.5, -14.0, 0.5)]
    for s in "SE":
        fx, fy, deg, L = face(11.0, 26.0, s, 18.5, -14.0, 0.05)
        pal.append(bifore(f"sm_pb{s}", L * 0.8, 2 if s == "S" else 4, 2.0, 4.0, fx, fy, 9.0, deg, "pointed", WHITE_M, DARK, True, False))
    pal.append(bell_tower("sm_tw", 17.0, 15.0, 7.0, 36.0, PF_L, "crenels", COPPI, 29.0, 4))
    m.add(3, join(pal, "sm_palace"), "palace and tower")
    return m


def innocenti():
    m = Model("innocenti")
    W, D = 72.0, 70.0
    m.add(0, plate(72, 70, PAVE_F, 0.25), "ground")
    fl = 1.4
    ly0 = -D / 2 + 2.6
    base = [box("in_steps%d" % i, W - 6.0, 0.5, fl * (5 - i) / 5, (0, -D / 2 + 0.25 + 0.5 * i, 0), SERENA) for i in range(5)]
    base.append(box("in_floor", W, 6.6, fl, (0, ly0 + 3.3, 0), SERENA))
    m.add(0, join(base, "in_base"), "steps")
    # Brunelleschi's loggia: nine round arches on slender Corinthian columns, roundels in the spandrels
    n = 9
    span = W - 4.0
    bay = span / n
    lo = [box("in_back", W, 1.0, 13.0, (0, ly0 + 6.6, fl), PLAST_F), box("in_dk", W - 4.0, 0.3, 11.0, (0, ly0 + 6.0, fl), "#3A3430")]
    for s in (-1, 1):
        lo.append(box(f"in_end{s}", 2.0, 6.6, 13.0, (s * (W / 2 - 1.0), ly0 + 3.3, fl), PLAST_F))
        lo.append(rects(f"in_endp{s}", [(-0.5, 0, 0.5, 11.6)], s * (W / 2 - 1.0), ly0 - 0.05, fl, -90, SERENA, 0.25))
    lo.append(arcade_front("in_arc", span, n, 0.0, 7.6, 11.4, 0, ly0, fl, -90, PLAST_F, 0.9))
    for i in range(n + 1):
        u = -span / 2 + bay * i
        lo.append(column(f"in_c{i}", u, ly0 + 0.3, fl, 0.36, 7.6, SERENA, True, 10))
        if 0 < i < n:
            lo.append(disc(f"in_rd{i}", 1.05, u, ly0 - 0.1, fl + 9.6, -90, LAPIS, 0.2, 14))
            lo.append(disc(f"in_rw{i}", 0.6, u, ly0 - 0.25, fl + 9.6, -90, WHITE_M, 0.2, 10))
    lo.append(box("in_ent", W, 1.2, 1.2, (0, ly0 + 0.2, fl + 11.4), SERENA))
    lo.append(box("in_upper", W, 6.6, 5.2, (0, ly0 + 3.3, fl + 12.6), PLAST_F))
    for i in range(n):
        u = -span / 2 + bay * (i + 0.5)
        lo.append(rects(f"in_uw{i}", [(u - 0.7, 1.2, u + 0.7, 3.4)], 0, ly0 - 0.05, fl + 12.6, -90, DARK, 0.25))
        lo.append(pediment(f"in_up{i}", 2.4, 0.8, u, ly0 - 0.1, fl + 12.6 + 3.6, -90, SERENA, 0.3))
    lo.append(box("in_eave", W + 1.0, 7.6, 0.4, (0, ly0 + 3.3, fl + 17.8), SERENA))
    m.add(1, join([x for x in lo if x is not None], "in_loggia"), "loggia")
    body = []
    ry0 = ly0 + 6.6
    body.append(box("in_front", W, 10.0, 18.0, (0, ry0 + 5.0, 0), PLAST_F))
    body.append(roof_x("in_frontr", W, 17.0, 3.0, 0, ry0 + 1.5, 19.2, COPPI, 0.5))
    body.append(box("in_rear", W, 9.0, 14.0, (0, D / 2 - 4.5, 0), PLAST_F))
    body.append(roof_x("in_rearr", W, 9.0, 2.4, 0, D / 2 - 4.5, 14.0, COPPI, 0.4))
    yc0, yc1 = ry0 + 10.0, D / 2 - 9.0
    cyc = (yc0 + yc1) / 2
    body.append(box("in_church", 12.0, yc1 - yc0, 17.0, (0, cyc, 0), PLAST_F))
    body.append(roof_y("in_churchr", 12.0, yc1 - yc0, 3.0, 0, cyc, 17.0, COPPI, 0.4))
    for s in (-1, 1):
        body.append(box(f"in_side{s}", 6.0, yc1 - yc0, 13.0, (s * (W / 2 - 3.0), cyc, 0), PLAST_F))
        body.append(roof_y(f"in_sider{s}", 6.0, yc1 - yc0, 1.8, s * (W / 2 - 3.0), cyc, 13.0, COPPI, 0.3))
        ccx = s * (6.0 + (W / 2 - 12.0) / 2 + 0.0)
        cw = W / 2 - 12.0
        body.append(box(f"in_cour{s}", cw, yc1 - yc0, 0.3, (ccx, cyc, 0), PAVE_L if s < 0 else GRASS_F))
        for f, (fx, fy, deg, L) in (("S", face(cw, yc1 - yc0, "S", ccx, cyc)), ("N", face(cw, yc1 - yc0, "N", ccx, cyc))):
            body.append(arcade_front(f"in_ca{s}{f}", L, 5, 0.0, 4.4, 6.5, fx, fy, 0, deg + 180, PLAST_F, 0.6))
            body.append(box(f"in_cad{s}{f}", L, 0.3, 6.0, (fx, fy + (1.0 if f == "S" else -1.0), 0), "#3A3430"))
            for k in range(6):
                u = -L / 2 + L * k / 5
                body.append(column(f"in_cc{s}{f}{k}", ccx + (u if f == "S" else -u), fy + (0.4 if f == "S" else -0.4), 0, 0.28, 4.4, SERENA, True, 8))
    for s in "EW":
        fx, fy, deg, L = face(W, D - 6.6, s, 0, 3.3, 0.05)
        body.append(openings(f"in_sw{s}", L * 0.85, 9, 1.2, 2.2, fx, fy, 8.0, deg, "flat", DARK, 0.3))
    m.add(2, join(body, "in_body"), "hospital")
    return m


def palazzo_pitti(variant="1490"):
    m = Model("palazzo-pitti" + ("-1600" if variant == "1600" else ""))
    W, D = 78.0, 110.0
    fy0 = -D / 2 + 1.0
    bd = 34.0
    H = 36.0
    m.add(0, plate(W, D, GRASS_F if variant == "1490" else "#A9AE84", 0.3), "ground")
    m.add(0, box("pp_piazza", W, 0.4, 0.4, (0, fy0 - 0.2, 0), PAVE_F), "ground")
    blk = [rustic_box("pp_blk", W, bd, H, 0, fy0 + bd / 2, 0, "#C8B18A", "SNEW" if variant == "1490" else "SEW", 3.2, 1.6, 0.6)]
    n = 7
    for k, z0 in enumerate((0.0, 12.0, 24.0)):
        for s in ("S", "N") if variant == "1490" else ("S",):
            fx, fy, deg, L = face(W, bd, s, 0, fy0 + bd / 2, 1.05)
            if k == 0:
                polys = []
                for i in range(n):
                    u = -L / 2 + L * (i + 0.5) / n
                    if i in (0, 3, 6):
                        polys.append([(u + a, b) for a, b in arch_pts(5.0, 9.0, "round")])
                    else:
                        polys.append([(u - 1.2, 3.5), (u + 1.2, 3.5), (u + 1.2, 7.5), (u - 1.2, 7.5)])
                blk.append(on_wall(multi_slab(f"pp_g{s}", polys, 0.4, DARK), fx, fy, 0, deg))
            else:
                blk.append(openings(f"pp_w{k}{s}", L, n, 4.8, 8.4, fx, fy, z0 + 1.6, deg, "round", DARK, 0.4))
                blk.append(box(f"pp_bal{k}{s}", L, 2.0, 0.6, (fx + 0.6 * math.cos(math.radians(deg)), fy + 0.6 * math.sin(math.radians(deg)), z0), "#D8C8A6") if s in "SN" else None)
                blk.append(rects(f"pp_bp{k}{s}", [(-L / 2 + i * 0.8, 0.6, -L / 2 + i * 0.8 + 0.35, 1.6) for i in range(int(L / 0.8))], fx + 1.5 * math.cos(math.radians(deg)), fy + 1.5 * math.sin(math.radians(deg)), z0, deg, "#D8C8A6", 0.2))
    blk.append(box("pp_corn", W + 1.6, bd + 1.6, 1.2, (0, fy0 + bd / 2, H), "#D8C8A6"))
    blk.append(hip("pp_roof", W, bd, 3.6, 0, fy0 + bd / 2, H + 1.2, COPPI, 0.6, 0.3))
    m.add(1, join([b for b in blk if b is not None], "pp_block"), "palace")
    if variant == "1490":
        gd = []
        for j in range(6):
            yy = fy0 + bd + 8.0 + j * 9.0
            gd.append(box(f"pp_ter{j}", W - 10.0, 1.0, 1.0 + j * 0.6, (0, yy, 0), "#B5A27C"))
            for i in range(10):
                gd.append(tree(f"pp_v{j}{i}", 0.9, (-W / 2 + 8.0 + i * 6.8, yy + 3.5, 0.3), "#7D8F55", TIMBER_F, "round"))
        gd.append(box("pp_quarry", 22.0, 14.0, 4.0, (22.0, D / 2 - 9.0, 0), "#C3AE88"))
        m.add(2, join(gd, "pp_hill"), "hillside")
        return m
    # Ammannati's courtyard and wings, the grotto terrace and the first Boboli amphitheatre
    cy0, cy1 = fy0 + bd, fy0 + bd + 40.0
    wings = []
    for s in (-1, 1):
        wings.append(rustic_box(f"pp_wing{s}", 16.0, 40.0, 30.0, s * (W / 2 - 8.0), (cy0 + cy1) / 2, 0, "#C8B18A", "EW", 3.2, 1.6, 0.6))
        wings.append(hip(f"pp_wingr{s}", 16.0, 40.0, 2.8, s * (W / 2 - 8.0), (cy0 + cy1) / 2, 30.0, COPPI, 0.8, 0.3))
        fx = s * (W / 2 - 16.0) - s * 0.05
        for k, z0 in enumerate((0.0, 10.0, 20.0)):
            wings.append(box(f"pp_cd{s}{k}", 0.3, 36.0, 7.0, (fx - s * 0.2, (cy0 + cy1) / 2, z0 + 1.0), DARK))
            for i in range(6):
                yy = cy0 + 2.0 + 36.0 * i / 5
                wings.append(box(f"pp_cp{s}{k}{i}", 2.0, 2.4, 9.0, (fx - s * 1.0, yy, z0), "#C8B18A"))
                for t in range(4):
                    wings.append(box(f"pp_cr{s}{k}{i}{t}", 2.6, 2.8, 0.9, (fx - s * 1.0, yy, z0 + 0.6 + t * 2.2), "#B9A27C"))
    wings.append(box("pp_cfloor", W - 32.0, 40.0, 0.4, (0, (cy0 + cy1) / 2, 0), PAVE_L))
    wings.append(box("pp_grotto", W - 32.0, 6.0, 9.0, (0, cy1 - 3.0, 0), "#C8B18A"))
    wings.append(arcade_front("pp_ga", W - 32.0, 3, 2.0, 4.0, 8.0, 0, cy1 - 6.0, 0, -90, "#B9A27C", 0.8))
    wings.append(box("pp_gterr", W - 32.0, 6.0, 0.8, (0, cy1 - 3.0, 9.0), "#D8C8A6"))
    m.add(2, join(wings, "pp_court"), "courtyard")
    amp = []
    ac = cy1 + 2.0
    for k in range(5):
        rx, ry = 30.0 - k * 4.0, 22.0 - k * 3.0
        outer, _ = ellipse_pts(rx, ry, 24, math.pi, 0)
        inner, _ = ellipse_pts(rx - 3.6, ry - 3.0, 24, math.pi, 0)
        amp.append(ring_extrude(f"pp_am{k}", outer, inner, 6.0 - k * 1.1, (0, ac, 0), "#8F9E66" if k % 2 else "#A3AE78", closed=False))
    amp.append(ellipse_disc("pp_arena", 11.0, 8.0, 0.4, (0, ac + 2.0, 0), SAND_F, 24))
    for i in range(12):
        a = math.pi * (i + 0.5) / 12
        amp.append(tree(f"pp_cy{i}", 1.0, (32.5 * math.cos(a), ac + 24.0 * math.sin(a), 0), HEDGE_F, TIMBER_F, "cypress"))
    m.add(3, join(amp, "pp_boboli"), "Boboli")
    return m


# ---------------------------------------------------------------- fortresses and the gate
def bastion_trace(pts, b=38.0, f=26.0, fl=14.0):
    """A bastioned trace round a polygon: at each corner an arrow-head bastion with flanks and faces."""
    n = len(pts)
    cx = sum(p[0] for p in pts) / n
    cy = sum(p[1] for p in pts) / n
    out = []
    for i in range(n):
        px, py = pts[i]
        ax, ay = pts[i - 1]
        bx, by = pts[(i + 1) % n]
        da = math.hypot(ax - px, ay - py)
        db = math.hypot(bx - px, by - py)
        ua = ((ax - px) / da, (ay - py) / da)
        ub = ((bx - px) / db, (by - py) / db)
        bis = (-(ua[0] + ub[0]), -(ua[1] + ub[1]))
        bl = math.hypot(*bis)
        bis = (bis[0] / bl, bis[1] / bl)
        # outward normals of the two curtains
        na = (ua[1], -ua[0]) if (ua[1] * (px - cx) - ua[0] * (py - cy)) > 0 else (-ua[1], ua[0])
        nb = (-ub[1], ub[0]) if (-ub[1] * (px - cx) + ub[0] * (py - cy)) > 0 else (ub[1], -ub[0])
        ca = (px + ua[0] * f, py + ua[1] * f)
        cb = (px + ub[0] * f, py + ub[1] * f)
        out += [ca, (ca[0] + na[0] * fl, ca[1] + na[1] * fl), (px + bis[0] * b, py + bis[1] * b), (cb[0] + nb[0] * fl, cb[1] + nb[1] * fl), cb]
    return out


def scale_pts(pts, k, cx=0.0, cy=0.0):
    return [(cx + (x - cx) * k, cy + (y - cy) * k) for x, y in pts]


def fortezza_da_basso():
    m = Model("fortezza-da-basso")
    m.add(0, plate(320, 270, "#B9B49C", 0.25), "ground")
    R = 92.0
    pent = [(1.25 * R * math.cos(math.radians(-90 + 72 * k)), R * math.sin(math.radians(-90 + 72 * k))) for k in range(5)]
    trace = bastion_trace(pent, 34.0, 26.0, 14.0)
    ditch = ring_extrude("fb_ditch", scale_pts(trace, 1.1), trace, 0.15, (0, 0, 0.25), WATER_F)
    m.add(0, ditch, "ground")
    inner = scale_pts(trace, 0.9)
    wall = [ring_extrude("fb_wall", trace, inner, 12.0, (0, 0, 0), BRICK_F)]
    wall.append(ring_extrude("fb_cord", scale_pts(trace, 1.004), scale_pts(trace, 0.99), 0.8, (0, 0, 9.5), PF_L))
    wall.append(ring_extrude("fb_top", scale_pts(inner, 1.0), scale_pts(trace, 0.94), 0.6, (0, 0, 12.0), "#9C8A6A"))
    for k in range(5):
        tip = trace[5 * k + 2]
        wall.append(box(f"fb_q{k}", 4.0, 4.0, 12.5, (tip[0], tip[1], 0), PF_L))
    m.add(1, join(wall, "fb_walls"), "bastions")
    # the keep at the gate toward the city (south-east), faced with diamond-point rustication
    gx, gy = 0.0, -R - 4.0
    keep = [box("fb_keep", 46.0, 22.0, 16.0, (gx, gy + 6.0, 0), PF)]
    dia = []
    for j in range(7):
        for i in range(20):
            u = -22.0 + 1.1 + i * 2.2 + (j % 2) * 1.1
            v = 1.0 + j * 2.1
            if u < 22.0 - 1.0:
                dia.append([(u - 1.0, v), (u, v - 1.0), (u + 1.0, v), (u, v + 1.0)])
    keep.append(on_wall(multi_slab("fb_dia", dia, 0.6, PF_L, y0=-0.3), gx, gy - 5.0, 0, -90))
    keep.append(opening("fb_gate", 5.0, 8.0, gx, gy - 5.6, 0, -90, "round", DARK, 0.5))
    keep.append(disc("fb_arms", 1.8, gx, gy - 5.5, 11.0, -90, RED_F, 0.3, 14))
    keep.append(box("fb_bridge", 6.0, 16.0, 1.2, (gx, gy - 13.0, 0), PF_D))
    m.add(2, join(keep, "fb_keep"), "keep")
    inside = []
    for i, (x, y, w, d) in enumerate(((-55, 10, 60, 12), (55, 10, 60, 12), (0, 45, 70, 12), (-30, -40, 30, 10), (30, -40, 30, 10))):
        inside.append(box(f"fb_bk{i}", w, d, 8.0, (x, y, 0), PLAST_F))
        inside.append(hip(f"fb_bkr{i}", w, d, 2.4, x, y, 8.0, COPPI, 0.7, 0.3))
        for s in "SN":
            fx, fy, deg, L = face(w, d, s, x, y, 0.05)
            inside.append(openings(f"fb_bw{i}{s}", L * 0.9, int(L / 4), 1.0, 1.8, fx, fy, 3.0, deg, "flat", DARK, 0.3))
    inside.append(box("fb_parade", 120.0, 60.0, 0.3, (0, 0, 0), SAND_F))
    inside.append(box("fb_chapel", 12.0, 18.0, 10.0, (0, 20.0, 0), PLAST_F))
    inside.append(roof_y("fb_chr", 12.0, 18.0, 3.0, 0, 20.0, 10.0, COPPI, 0.3))
    m.add(3, join(inside, "fb_inside"), "barracks")
    return m


def forte_belvedere():
    m = Model("forte-belvedere")
    m.add(0, plate(190, 95, "#A7AA82", 0.3), "ground")
    star = [(-93, 0), (-66, -26), (-50, -18), (-34, -45), (-10, -32), (10, -32), (34, -45), (50, -18), (66, -26), (93, 0),
            (66, 26), (50, 18), (34, 45), (10, 33), (-10, 33), (-34, 45), (-50, 18), (-66, 26)]
    inner = scale_pts(star, 0.88)
    wall = [ring_extrude("bv_wall", star, inner, 10.0, (0, 0, 0), PF_L),
            ring_extrude("bv_cord", scale_pts(star, 1.005), scale_pts(star, 0.985), 0.6, (0, 0, 8.0), WHITE_M),
            ring_extrude("bv_top", inner, scale_pts(star, 0.93), 0.5, (0, 0, 10.0), "#A99877")]
    wall.append(box("bv_yard", 140.0, 50.0, 0.3, (0, 0, 0), "#C9B993"))
    m.add(0, join(wall, "bv_walls"), "bastions")
    gate = [box("bv_gate", 12.0, 6.0, 12.0, (0, 30.0, 0), PF_L), opening("bv_go", 3.2, 5.4, 0, 33.05, 0, 90, "round", DARK, 0.4),
            disc("bv_arms", 1.2, 0, 33.1, 8.5, 90, RED_F, 0.2, 12)]
    m.add(1, join(gate, "bv_gate"), "gate")
    pal = [box("bv_pal", 32.0, 15.0, 15.0, (0, 0, 0), PLAST_F)]
    for s in "SNEW":
        fx, fy, deg, L = face(32.0, 15.0, s, 0, 0, 0.05)
        pal.append(openings(f"bv_pw1{s}", L * 0.85, max(2, int(L / 4)), 1.3, 2.4, fx, fy, 3.0, deg, "flat", DARK, 0.3))
        pal.append(openings(f"bv_pw2{s}", L * 0.85, max(2, int(L / 4)), 1.3, 2.4, fx, fy, 9.0, deg, "flat", DARK, 0.3))
        pal.append(rects(f"bv_pq{s}", [(-L / 2, 0, -L / 2 + 0.8, 15.0), (L / 2 - 0.8, 0, L / 2, 15.0)], fx, fy, 0, deg, SERENA, 0.2))
    pal.append(box("bv_pc", 33.0, 16.0, 0.6, (0, 0, 15.0), SERENA))
    pal.append(hip("bv_pr", 32.0, 15.0, 2.4, 0, 0, 15.6, COPPI, 0.5, 0.4))
    pal.append(box("bv_lg", 10.0, 7.0, 5.0, (0, 0, 15.6), PLAST_F))
    for s in "SN":
        fx, fy, deg, L = face(10.0, 7.0, s, 0, 0, 0.05)
        pal.append(openings(f"bv_lgo{s}", 9.0, 3, 2.0, 3.6, fx, fy, 15.6, deg, "round", DARK, 0.3))
    pal.append(hip("bv_lgr", 10.0, 7.0, 1.6, 0, 0, 20.6, COPPI, 0.5, 0.3))
    m.add(2, join(pal, "bv_palazzina"), "palazzina")
    return m


def porta_romana():
    m = Model("porta-romana")
    m.add(0, plate(30, 18, PAVE_F, 0.25), "ground")
    tw = [rustic_box("pr_tw", 15.0, 13.0, 24.0, 0, 0, 0, PF, "SNEW", 2.0, 1.0, 0.28)]
    tw.append(opening("pr_arch", 5.6, 10.0, 0, -6.95, 0, -90, "round", DARK, 0.5))
    tw.append(opening("pr_archn", 5.6, 10.0, 0, 6.95, 0, 90, "round", DARK, 0.5))
    tw.append(rects("pr_lun", [(-2.6, 11.0, 2.6, 13.6)], 0, -6.95, 0, -90, "#B98A62", 0.3))
    tw.append(disc("pr_mad", 0.9, 0, -7.2, 12.3, -90, LAPIS, 0.2, 12))
    tw.append(rects("pr_door", [(-2.6, 0.2, -0.1, 9.0), (0.1, 0.2, 2.6, 9.0)], 0, -6.6, 0, -90, TIMBER_F, 0.2))
    tw.append(corbel_gallery("pr_gal", 15.0, 13.0, 25.6, 0.9, 1.6, 1.6, 2.2, PF, "guelf", 0.9))
    tw.append(box("pr_roof", 14.0, 12.0, 0.6, (0, 0, 24.0), COPPI_D))
    m.add(1, join(tw, "pr_tower"), "gate tower")
    wl = []
    for s in (-1, 1):
        wl.append(rustic_box(f"pr_w{s}", 7.6, 3.4, 11.5, s * 11.2, 2.0, 0, PF_D, "SN", 2.0, 1.0, 0.2))
        wl.append(crenels(f"pr_wm{s}", 7.6, s * 11.2, 2.0 - 1.7, 11.5, -90, 0.9, "guelf", PF_D, 0.6))
        wl.append(box(f"pr_wk{s}", 7.6, 2.0, 0.4, (s * 11.2, 2.4, 11.5), PF_D))
    m.add(0, join(wl, "pr_walls"), "walls")
    return m


# ---------------------------------------------------------------- Roman Florentia
def forum():
    m = Model("forum")
    W, D = 90.0, 120.0
    m.add(0, plate(W, D, "#C9BFA8", 0.25), "ground")
    fw, fd = 66.0, 64.0
    fy = -10.0
    m.add(0, box("fo_pave", fw, fd, 0.4, (0, fy, 0), "#DCD3BF"), "ground")
    por = []
    for s in (-1, 1):
        x = s * (fw / 2 + 3.0)
        por.append(columns(f"fo_ce{s}", [(s * (fw / 2 + 0.6), fy - fd / 2 + 2 + (fd - 4) * i / 12) for i in range(13)], 0.45, 6.0, (0, 0, 0.4), "#E8E0CC"))
        por.append(box(f"fo_cw{s}", 1.0, fd, 7.0, (x + s * 2.6, fy, 0), "#D6C9AC"))
        por.append(lean_to(f"fo_cr{s}", s * (fw / 2 + 0.2), s * (fw / 2 + 6.2), fy - fd / 2, fy + fd / 2, 6.6, 7.6, COPPI))
        por.append(openings(f"fo_tab{s}", fd - 6, 9, 2.4, 3.6, x + s * 2.05, fy, 0, 180 if s > 0 else 0, "flat", DARK, 0.3))
        # shops behind the porticoes
        por.append(box(f"fo_sh{s}", 6.0, fd, 6.0, (s * (fw / 2 + 9.6), fy, 0), "#D9C4A0"))
        por.append(roof_y(f"fo_shr{s}", 6.0, fd, 1.6, s * (fw / 2 + 9.6), fy, 6.0, COPPI, 0.3))
    # the basilica closing the south side
    by = fy - fd / 2 - 9.0
    por.append(box("fo_bas", 64.0, 16.0, 11.0, (0, by, 0), "#E2D6BC"))
    por.append(box("fo_basc", 52.0, 8.0, 15.0, (0, by, 0), "#E2D6BC"))
    por.append(roof_x("fo_basr", 52.0, 8.0, 2.0, 0, by, 15.0, COPPI, 0.3))
    for s in (-1, 1):
        por.append(lean_to_y(f"fo_basa{s}", -32.0, 32.0, by + s * 8.3, by + s * 4.0, 11.0, 12.6, COPPI) if s > 0 else lean_to_y(f"fo_basa{s}", -32.0, 32.0, by - 8.3, by - 4.0, 11.0, 12.6, COPPI))
    por.append(columns("fo_bcol", [(-30 + 60 * i / 14, by + 8.6) for i in range(15)], 0.5, 9.0, (0, 0, 0), "#EEE6D2"))
    por.append(openings("fo_basw", 50.0, 10, 1.6, 2.4, 0, by - 4.05, 11.6, -90, "round", DARK, 0.3))
    m.add(1, join(por, "fo_porticoes"), "porticoes")
    base, body, roof = mini_temple("fo_cap", 26.0, 34.0, 4.0, 11.0, 6, 3, (0, fy + fd / 2 + 17.0, 0), "#EEE6D2", COPPI, 0.75)
    m.add(1, base, "porticoes")
    m.add(2, body, "Capitolium")
    m.add(3, roof, "roof")
    mid = [box("fo_colb", 2.4, 2.4, 2.0, (0, fy, 0.4), "#E8E0CC"), cylinder("fo_col", 0.7, 11.0, (0, fy, 2.4), "#E8E0CC", verts=12),
           statue("fo_cst", 0, fy, 13.4, 2.4, BRONZE_F)]
    for i, (x, y) in enumerate(((-18, fy + 18), (18, fy + 18), (-22, fy - 20), (22, fy - 20))):
        mid.append(box(f"fo_ped{i}", 2.0, 3.6, 2.2, (x, y, 0.4), "#E8E0CC"))
        mid.append(statue(f"fo_eq{i}", x, y, 2.6, 2.4, BRONZE_F))
    m.add(2, join(mid, "fo_column"), "Capitolium")
    return m


def amphitheatre():
    m = Model("amphitheatre")
    rx, ry = 57.0, 45.5
    m.add(0, plate(115, 92, "#C2B89E", 0.25), "ground")
    outer = ellipse_ring("am_outer", rx, ry, 0.95, 18.0, (0, 0, 0), "#D9CDB2", 72)
    cav = []
    for k in range(6):
        f0 = 0.95 - k * 0.07
        cav.append(ellipse_ring(f"am_cav{k}", rx * f0, ry * f0, (f0 - 0.07) / f0, 16.0 - k * 2.6, (0, 0, 0), "#CBBE9F" if k % 2 else "#D3C7AA", 64))
    m.add(0, join(cav, "am_cavea"), "cavea")
    arches = [outer]
    n = 40
    for row, (z0, h) in enumerate(((0.0, 6.4), (8.4, 5.6))):
        for i in range(n):
            t = math.tau * (i + 0.5) / n
            x, y = rx * 1.002 * math.cos(t), ry * 1.002 * math.sin(t)
            deg = math.degrees(math.atan2(y / ry ** 2, x / rx ** 2))
            arches.append(opening(f"am_a{row}_{i}", 3.6, h, x, y, z0 + 0.6, deg, "round", DARK, 0.4))
    arches.append(ellipse_ring("am_band", rx * 1.01, ry * 1.01, 0.985, 0.6, (0, 0, 7.6), "#E6DCC4", 72))
    arches.append(ellipse_ring("am_crown", rx * 1.01, ry * 1.01, 0.985, 0.8, (0, 0, 17.2), "#E6DCC4", 72))
    m.add(1, join(arches, "am_facade"), "arcades")
    ar = [ellipse_disc("am_arena", rx * 0.53, ry * 0.42, 0.5, (0, 0, 0), SAND_F, 48),
          ellipse_ring("am_podium", rx * 0.55, ry * 0.445, 0.95, 3.0, (0, 0, 0), "#E6DCC4", 48)]
    for s in (-1, 1):
        ar.append(box(f"am_gate{s}", 8.0, 5.0, 6.0, (s * rx * 0.97, 0, 0), DARK))
    m.add(2, join(ar, "am_arena"), "arena")
    return m


BUILDERS = {
    "florence/duomo": duomo,
    "florence/santa-reparata": santa_reparata,
    "florence/baptistery": baptistery,
    "florence/campanile": campanile_g,
    "florence/palazzo-vecchio": palazzo_vecchio,
    "florence/palazzo-vecchio-1300": lambda: palazzo_vecchio("1300"),
    "florence/loggia-lanzi": loggia_lanzi,
    "florence/loggia-lanzi-1600": lambda: loggia_lanzi("1600"),
    "florence/uffizi": uffizi,
    "florence/ponte-vecchio": ponte_vecchio,
    "florence/ponte-vecchio-old": ponte_vecchio_old,
    "florence/ponte-vecchio-1600": lambda: ponte_vecchio("1600"),
    "florence/ponte-alle-grazie": ponte_alle_grazie,
    "florence/ponte-santa-trinita": ponte_santa_trinita,
    "florence/ponte-santa-trinita-old": lambda: ponte_santa_trinita("old"),
    "florence/bargello": bargello,
    "florence/orsanmichele": orsanmichele,
    "florence/orsanmichele-loggia": lambda: orsanmichele("loggia"),
    "florence/palazzo-medici": palazzo_medici,
    "florence/san-lorenzo": san_lorenzo,
    "florence/san-lorenzo-old": lambda: san_lorenzo("old"),
    "florence/san-lorenzo-1600": lambda: san_lorenzo("1600"),
    "florence/santa-croce": santa_croce,
    "florence/santa-croce-1300": lambda: santa_croce("1300"),
    "florence/santa-maria-novella": santa_maria_novella,
    "florence/santa-maria-novella-1300": lambda: santa_maria_novella("1300"),
    "florence/santo-spirito": santo_spirito,
    "florence/santo-spirito-1600": lambda: santo_spirito("1600"),
    "florence/innocenti": innocenti,
    "florence/palazzo-pitti": palazzo_pitti,
    "florence/palazzo-pitti-1600": lambda: palazzo_pitti("1600"),
    "florence/san-miniato": san_miniato,
    "florence/fortezza-da-basso": fortezza_da_basso,
    "florence/forte-belvedere": forte_belvedere,
    "florence/forum": forum,
    "florence/amphitheatre": amphitheatre,
    "florence/porta-romana": porta_romana,
}
