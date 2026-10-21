"""Venice landmark miniatures: San Marco and the Piazza, the Doge's Palace, the Rialto bridge and market, the Arsenal,
the friars' brick churches, Palladio's and Longhena's white churches, the Ghetto and the Bucintoro.

Conventions as worldkit: metres, origin at the ground centre, +X east, +Y north, +Z up, main front to the
south (-Y). Helpers build at the origin and are put in place with place(). Bespoke Venetian parts: open Gothic
arcades, quatrefoil bands, the diamond-patterned wall, decorative merli, Byzantine domes with lanterns,
the Venetian campanile, a palazzo with its water-gate, the squero (covered slipway), gondolas and galleys.
"""
import math
import bpy
from chronokit import Model, box, cylinder, dome, join, shade, gable_roof, hip_roof, mesh_from
from worldkit import *

# ---------------------------------------------------------------- palette
ISTRIA = "#EEEAE0"      # Istrian stone
ISTRIA_D = "#D8D1C2"
MARBLE_V = "#E6DCCB"    # weathered marble revetment
PINK = "#E3B5A2"        # Verona pink of the palace wall
ROSSO = "#B9624E"       # Verona red marble
BRICK_V = "#B0654A"
BRICK_D = "#93513B"
PLAST_V = "#E5CDAE"
OCHRE = "#D3A26C"
FRESCO = "#C98E6E"
LEAD_V = "#8A9299"
COPPER = "#6E9C88"
GOLD = "#D4AE55"
MOSAIC = "#C99B3A"
TILE = "#B4634A"
GLASS_V = "#3C4A60"
BLUE = "#2F4C8C"
PAVE_V = "#A9A39A"
PAVE_L = "#CBC5B8"
YARD = "#C3AE8C"
WATER_V = "#5E8A8C"
TIMBER_V = "#7A5A3E"
TIMBER_D = "#4F3A2A"
BLACK = "#26221E"
RED_CLOTH = "#A3302A"
GREEN_V = "#7F946A"
MARSH_V = "#97A487"
BRONZE_G = "#A88545"
GRANITE_G = "#8F8A86"
GRANITE_R = "#A08078"


# ---------------------------------------------------------------- placement and primitives
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


def plate(w, d, color=PAVE_V, h=0.3, x=0, y=0, name="plate"):
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
    """Outline (u, v) of an arched opening w wide and h high, base at v = 0. kind: round | pointed | ogee | flat."""
    r = w / 2
    if kind == "round":
        rh = max(0.0, h - r)
        top = [(r * math.cos(math.pi * i / 8), rh + r * math.sin(math.pi * i / 8)) for i in range(9)]
    elif kind in ("pointed", "ogee"):
        tip = min(h, w * (0.75 if kind == "pointed" else 0.95))
        rh = h - tip
        if kind == "pointed":
            half = [(r, rh), (r * 0.93, rh + tip * 0.38), (r * 0.72, rh + tip * 0.7), (r * 0.4, rh + tip * 0.9), (0, rh + tip)]
        else:
            half = [(r, rh), (r * 0.96, rh + tip * 0.3), (r * 0.75, rh + tip * 0.55), (r * 0.42, rh + tip * 0.68), (r * 0.16, rh + tip * 0.82), (0, rh + tip)]
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
    """A dark arched opening (or a coloured arched panel) on a wall."""
    return on_wall(multi_slab(name, [arch_pts(w, h, kind)], depth, color), x, y, z, normal_deg)


def openings(name, length, n, w, h, x, y, z, normal_deg, kind="round", color=DARK, depth=0.3, skip=()):
    """A row of n arched openings centred on (x, y) along a wall."""
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


def quatrefoils(name, length, n, r, x, y, z, normal_deg, color=DARK, depth=0.3):
    """A row of four-lobed roundels (Gothic tracery)."""
    bay = length / n
    polys = []
    for i in range(n):
        u0 = -length / 2 + bay * (i + 0.5)
        pts = []
        for k in range(20):
            t = math.tau * k / 20
            rr = r * (0.62 + 0.38 * abs(math.cos(2 * t)))
            pts.append((u0 + rr * math.cos(t), rr * math.sin(t)))
        polys.append(pts)
    return on_wall(multi_slab(name, polys, depth, color), x, y, z, normal_deg)


def merli(name, length, x, y, z, normal_deg, size=0.9, color=ISTRIA, gap=0.35, depth=0.35):
    """Venetian decorative crenellation: a row of pointed white merlons along a roofline."""
    n = max(1, int(length / (size + gap)))
    bay = length / n
    polys = []
    for i in range(n):
        u0 = -length / 2 + bay * (i + 0.5)
        s = size / 2
        polys.append([(u0 - s, 0), (u0 + s, 0), (u0 + s, size * 0.8), (u0 + s * 0.35, size * 1.05), (u0, size * 1.55), (u0 - s * 0.35, size * 1.05), (u0 - s, size * 0.8)])
    return on_wall(multi_slab(name, polys, depth, color), x, y, z, normal_deg)


def merli_ring(name, w, d, z, size=0.9, color=ISTRIA, cx=0, cy=0, sides="SNEW"):
    parts = []
    if "S" in sides:
        parts.append(merli(name + "s", w, cx, cy - d / 2, z, -90, size, color))
    if "N" in sides:
        parts.append(merli(name + "n", w, cx, cy + d / 2, z, 90, size, color))
    if "E" in sides:
        parts.append(merli(name + "e", d, cx + w / 2, cy, z, 0, size, color))
    if "W" in sides:
        parts.append(merli(name + "w", d, cx - w / 2, cy, z, 180, size, color))
    return join(parts, name)


def column(name, x, y, z, r, h, color=ISTRIA, cap=True, verts=12, cap_color=None):
    parts = [cylinder(name + "_s", r, h, (x, y, z), color, verts=verts)]
    if cap:
        parts.append(box(name + "_c", r * 2.6, r * 2.6, r * 1.1, (x, y, z + h - r * 0.4), cap_color or color))
        parts.append(box(name + "_b", r * 2.4, r * 2.4, r * 0.5, (x, y, z), color))
    return join(parts, name)


def arcade_open(name, length, n, h, x, y, z, normal_deg, wall=ISTRIA, kind="pointed", col_r=0.45, depth=3.0, head=None, col_color=None,
                inner=DARK, piers=False):
    """An open arcade on a façade line through (x, y): dark interior, columns (or piers), arched heads cut into a stone band."""
    bay = length / n
    head_h = head or min(h * 0.45, bay * (0.75 if kind == "pointed" else 0.5) + 0.6)
    spring = h - head_h
    parts = [box(name + "_back", length, 0.4, h, (0, depth, 0), inner),
             box(name + "_band", length, 0.9, head_h, (0, 0.45, spring), wall),
             box(name + "_end0", bay * 0.22, depth, h, (-length / 2 + bay * 0.11, depth / 2, 0), wall),
             box(name + "_end1", bay * 0.22, depth, h, (length / 2 - bay * 0.11, depth / 2, 0), wall),
             box(name + "_ceil", length, depth, 0.3, (0, depth / 2, h - 0.3), wall)]
    heads = []
    for i in range(n):
        u0 = -length / 2 + bay * (i + 0.5)
        heads.append([(u0 + u, v + spring - 0.02) for u, v in arch_pts(bay - col_r * 2.6, head_h * 0.82, kind if kind != "flat" else "round")])
    parts.append(multi_slab(name + "_heads", heads, 0.2, inner, y0=-0.05))
    for i in range(1, n):
        u = -length / 2 + bay * i
        if piers:
            parts.append(box(f"{name}_p{i}", col_r * 2.2, col_r * 2.2, spring, (u, 0.5, 0), col_color or wall))
        else:
            parts.append(column(f"{name}_c{i}", u, 0.5, 0, col_r, spring, col_color or wall, True, 10))
    o = join(parts, name)
    return on_wall(o, x, y, z, normal_deg)


def diamond_wall(name, w, h, x, y, z, normal_deg, base=PINK, line=ISTRIA, s=2.2, thick=0.6):
    """The Doge's Palace upper wall: pink marble with a lattice of white lozenges."""
    parts = [box(name + "_b", w, thick, h, (0, thick / 2, 0), base)]
    polys = []
    rows = int((h - 0.3) / (s * 0.62))
    for j in range(rows):
        v = s * 0.45 + j * s * 0.62
        off = (j % 2) * s / 2
        u = -w / 2 + s * 0.45 + off
        while u < w / 2 - s * 0.4:
            polys.append([(u - s * 0.24, v), (u, v - s * 0.31), (u + s * 0.24, v), (u, v + s * 0.31)])
            u += s
    if polys:
        parts.append(multi_slab(name + "_lz", polys, 0.1, line, y0=-0.03))
    return on_wall(join(parts, name), x, y, z, normal_deg)


def statue(name, x, y, z, h=2.0, color=ISTRIA):
    return join([cylinder(name + "_b", h * 0.13, h * 0.78, (x, y, z), color, verts=8, r_top=h * 0.09),
                 dome(name + "_h", h * 0.1, (x, y, z + h * 0.82), color, segments=8, rings=4)], name)


def pinnacle(name, x, y, z, w=1.4, h=4.0, color=ISTRIA, spire=COPPER, statue_top=True):
    """A Gothic tabernacle: a little shrine box with a spire (and a figure)."""
    parts = [box(name + "_b", w, w, h * 0.55, (x, y, z), color)]
    parts.append(cylinder(name + "_s", w * 0.62, h * 0.45, (x, y, z + h * 0.55), spire, verts=8, r_top=0.05))
    if statue_top:
        parts.append(statue(name + "_f", x, y, z + h, h * 0.35, color))
    return join(parts, name)


def chimney(name, x, y, z, r=0.45, h=2.6, color=PLAST_V):
    """A Venetian funnel chimney (camin a fumaiolo)."""
    return join([cylinder(name + "_s", r * 0.6, h * 0.65, (x, y, z), color, verts=8),
                 cylinder(name + "_f", r * 0.6, h * 0.35, (x, y, z + h * 0.65), color, verts=8, r_top=r * 1.5)], name)


def roof_x(name, w, d, h, x=0, y=0, z=0, color=TILE, over=0.4):
    """Gable roof with the ridge along X."""
    return place(gable_roof(name, d, w, h, (0, 0, 0), color, overhang=over), 90, x, y, z)


def roof_y(name, w, d, h, x=0, y=0, z=0, color=TILE, over=0.4):
    return place(gable_roof(name, w, d, h, (0, 0, 0), color, overhang=over), 0, x, y, z)


def hip(name, w, d, h, x=0, y=0, z=0, color=TILE, ridge=0.45, over=0.4):
    if w > d:
        return place(hip_roof(name, d, w, h, (0, 0, 0), color, ridge=ridge, overhang=over), 90, x, y, z)
    return place(hip_roof(name, w, d, h, (0, 0, 0), color, ridge=ridge, overhang=over), 0, x, y, z)


def lean_to(name, x0, x1, y0, y1, z_low, z_high, color=TILE):
    """A roof slab sloping from z_low along x0 up to z_high along x1."""
    t = 0.3
    verts = [(x0, y0, z_low), (x1, y0, z_high), (x1, y1, z_high), (x0, y1, z_low),
             (x0, y0, z_low + t), (x1, y0, z_high + t), (x1, y1, z_high + t), (x0, y1, z_low + t)]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def pediment(name, w, h, x, y, z, normal_deg, color=ISTRIA, depth=1.0):
    return on_wall(multi_slab(name, [[(-w / 2, 0), (w / 2, 0), (0, h)]], depth, color), x, y, z, normal_deg)


def disc(name, r, x, y, z, normal_deg, color=GOLD, t=0.3, verts=20):
    """A flat round plate on a wall (clock dial, oculus, roundel)."""
    o = cylinder(name, r, t, (0, 0, -t / 2), color, verts=verts)
    apply_rot(o, rx=math.pi / 2)
    return place(o, normal_deg + 90, x, y, z)


# ---------------------------------------------------------------- domes and towers
def byz_dome(name, r, x, y, z, color=LEAD_V, drum_color=MARBLE_V, lantern=True, tall=True):
    """A San Marco dome: a low drum with windows, a tall timber-and-lead outer shell, a lantern with an onion cap and a cross."""
    dh = r * 0.36
    parts = [cylinder(name + "_drum", r, dh, (x, y, z), drum_color, verts=24)]
    polys = []
    nwin = 16
    for k in range(nwin):
        a = math.tau * (k + 0.5) / nwin
        w = opening(f"{name}_w{k}", r * 0.28, dh * 0.7, x + math.cos(a) * r * 1.01, y + math.sin(a) * r * 1.01, z + dh * 0.12, math.degrees(a), "round", DARK, 0.25)
        parts.append(w)
    if tall:
        prof = [(r * 1.03, 0), (r * 1.05, r * 0.18), (r * 1.02, r * 0.48), (r * 0.92, r * 0.8), (r * 0.74, r * 1.08), (r * 0.5, r * 1.28), (r * 0.24, r * 1.4), (0.0, r * 1.44)]
    else:
        prof = [(r * 1.02, 0)] + [(r * 1.02 * math.cos(t), r * 0.5 * math.sin(t)) for t in [math.pi / 2 * i / 6 for i in range(1, 7)]]
        prof[-1] = (0.0, prof[-1][1])
    parts.append(lathe(name + "_shell", prof, (x, y, z + dh), color, verts=40))
    parts.append(cylinder(name + "_base", r * 1.08, r * 0.08, (x, y, z + dh - r * 0.04), shade(drum_color, -0.08), verts=40))
    top = z + dh + prof[-1][1]
    if lantern:
        lr = max(0.5, r * 0.15)
        parts.append(cylinder(name + "_lan", lr, lr * 2.0, (x, y, top - lr * 0.3), color, verts=10))
        parts.append(onion_dome(name + "_on", lr * 1.05, (x, y, top + lr * 1.7), GOLD, bulb=1.25, height=1.5, drum=0.1, finial=False))
        ct = top + lr * 1.7 + lr * 1.8
        parts.append(box(name + "_cr1", 0.16, 0.16, lr * 2.4, (x, y, ct), GOLD))
        parts.append(box(name + "_cr2", lr * 1.3, 0.16, 0.16, (x, y, ct + lr * 1.5), GOLD))
    return join(parts, name)


def classical_dome(name, r, x, y, z, drum_h, color=LEAD_V, drum_color=ISTRIA, windows=12, rise=1.05, lantern_color=ISTRIA, top_statue=True, verts=32):
    """A Renaissance dome: a drum with arched windows and pilasters, a raised lead dome with ribs, a lantern."""
    parts = [cylinder(name + "_drum", r, drum_h, (x, y, z), drum_color, verts=verts),
             cylinder(name + "_dc", r * 1.04, drum_h * 0.08, (x, y, z + drum_h * 0.92), shade(drum_color, -0.05), verts=verts)]
    for k in range(windows):
        a = math.tau * (k + 0.5) / windows
        parts.append(opening(f"{name}_w{k}", r * 0.24, drum_h * 0.55, x + math.cos(a) * r * 1.01, y + math.sin(a) * r * 1.01, z + drum_h * 0.18, math.degrees(a), "round", DARK, 0.25))
        b = math.tau * k / windows
        parts.append(box(f"{name}_pl{k}", r * 0.09, r * 0.09, drum_h * 0.9, (x + math.cos(b) * r * 1.02, y + math.sin(b) * r * 1.02, z), shade(drum_color, -0.06), rot_z=b))
    prof = [(r * 1.02, 0)] + [(r * 1.02 * math.cos(t), r * rise * math.sin(t)) for t in [math.pi / 2 * i / 8 for i in range(1, 9)]]
    prof[-1] = (r * 0.16, prof[-1][1] * 0.985)
    zt = z + drum_h
    parts.append(lathe(name + "_d", prof, (x, y, zt), color, verts=verts))
    nrib = 16
    for k in range(nrib):
        a = math.tau * k / nrib
        pts = []
        for i in range(9):
            t = math.pi / 2 * i / 8 * 0.94
            pts.append((r * 1.03 * math.cos(t), r * rise * 1.01 * math.sin(t)))
        verts = []
        for (rr, zz) in pts:
            for s in (-1, 1):
                verts.append((math.cos(a) * rr - math.sin(a) * s * 0.18, math.sin(a) * rr + math.cos(a) * s * 0.18, zz))
        faces = [(2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2) for i in range(len(pts) - 1)]
        rib = mesh_from(f"{name}_rib{k}", verts, faces, (x, y, zt), shade(color, 0.12))
        parts.append(rib)
    lt = zt + r * rise * 0.97
    lr = r * 0.17
    parts.append(cylinder(name + "_lan", lr, lr * 2.2, (x, y, lt), lantern_color, verts=12))
    parts.append(openings(name + "_lw", lr * 1.6, 3, lr * 0.4, lr * 1.3, x, y - lr * 1.01, lt + lr * 0.4, -90, "round", DARK, 0.15))
    parts.append(dome(name + "_lc", lr * 1.05, (x, y, lt + lr * 2.2), color, squash=1.1, segments=12, rings=6))
    if top_statue:
        parts.append(statue(name + "_st", x, y, lt + lr * 3.3, max(1.6, r * 0.22), GOLD))
    return join(parts, name)


def venetian_campanile(name, w, x, y, shaft_h, variant="1514", color=BRICK_V):
    """The Venetian bell tower: a brick shaft with pilaster strips, a belfry loggia, and (1514) an attic and a pyramid spire."""
    parts = [box(name + "_plinth", w * 1.06, w * 1.06, 1.4, (x, y, 0), ISTRIA_D),
             box(name + "_shaft", w, w, shaft_h, (x, y, 0), color)]
    nl = 5
    for f, (nx, ny) in {"S": (0, -1), "N": (0, 1), "E": (1, 0), "W": (-1, 0)}.items():
        for k in range(nl):
            u = -w / 2 + w * (k + 0.5) / nl
            px, py = (x + u, y + ny * (w / 2 + 0.12)) if ny else (x + nx * (w / 2 + 0.12), y + u)
            parts.append(box(f"{name}_ls{f}{k}", 0.55 if ny else 0.3, 0.3 if ny else 0.55, shaft_h - 3, (px, py, 1.4), shade(color, -0.07)))
        deg = {"S": -90, "N": 90, "E": 0, "W": 180}[f]
        fx, fy = x + nx * (w / 2 + 0.05), y + ny * (w / 2 + 0.05)
        parts.append(openings(f"{name}_tarc{f}", w * 0.92, nl - 1, w * 0.12, 1.1, fx, fy, shaft_h - 1.9, deg, "round", shade(color, -0.25), 0.2))
    z = shaft_h
    if variant == "1514":
        bh = w * 0.95
        parts.append(box(name + "_bel_floor", w * 1.04, w * 1.04, 1.0, (x, y, z), ISTRIA))
        parts.append(box(name + "_bel", w * 0.96, w * 0.96, bh, (x, y, z + 1.0), ISTRIA))
        for f, (nx, ny) in {"S": (0, -1), "N": (0, 1), "E": (1, 0), "W": (-1, 0)}.items():
            deg = {"S": -90, "N": 90, "E": 0, "W": 180}[f]
            fx, fy = x + nx * (w * 0.48 + 0.05), y + ny * (w * 0.48 + 0.05)
            parts.append(openings(f"{name}_bw{f}", w * 0.86, 4, w * 0.15, bh * 0.66, fx, fy, z + 2.0, deg, "round", DARK, 0.4))
        z += 1.0 + bh
        parts.append(box(name + "_cor", w * 1.04, w * 1.04, 0.8, (x, y, z), ISTRIA_D))
        ah = w * 0.6
        parts.append(box(name + "_attic", w * 0.92, w * 0.92, ah, (x, y, z + 0.8), ISTRIA))
        for f, (nx, ny) in {"S": (0, -1), "N": (0, 1), "E": (1, 0), "W": (-1, 0)}.items():
            deg = {"S": -90, "N": 90, "E": 0, "W": 180}[f]
            fx, fy = x + nx * (w * 0.46 + 0.05), y + ny * (w * 0.46 + 0.05)
            parts.append(on_wall(box(f"{name}_rel{f}", w * 0.42, 0.25, ah * 0.6, (0, 0, 0), "#CDB98A"), fx, fy, z + 0.8 + ah * 0.2, deg))
        z += 0.8 + ah
        sp = cylinder(name + "_spire", w * 0.92 / math.sqrt(2), w * 2.05, (x, y, z), COPPER, verts=4, r_top=0.15)
        sp.rotation_euler[2] = math.pi / 4
        parts.append(sp)
        for cx in (-1, 1):
            for cy in (-1, 1):
                parts.append(cylinder(f"{name}_pin{cx}{cy}", 0.45, 2.4, (x + cx * w * 0.44, y + cy * w * 0.44, z), ISTRIA, verts=6, r_top=0.05))
        z += w * 2.05
        parts.append(cylinder(name + "_ag_b", 0.5, 1.0, (x, y, z), GOLD, verts=8))
        parts.append(statue(name + "_angel", x, y, z + 1.0, 3.2, GOLD))
        parts.append(box(name + "_wing", 2.4, 0.15, 1.0, (x, y, z + 2.6), GOLD))
    else:
        bh = w * 0.75
        parts.append(box(name + "_bel", w * 0.98, w * 0.98, bh, (x, y, z), shade(color, 0.05)))
        for f, (nx, ny) in {"S": (0, -1), "N": (0, 1), "E": (1, 0), "W": (-1, 0)}.items():
            deg = {"S": -90, "N": 90, "E": 0, "W": 180}[f]
            fx, fy = x + nx * (w * 0.49 + 0.05), y + ny * (w * 0.49 + 0.05)
            parts.append(openings(f"{name}_bw{f}", w * 0.8, 3, w * 0.18, bh * 0.66, fx, fy, z + 1.2, deg, "round", DARK, 0.4))
        z += bh
        parts.append(box(name + "_cor", w * 1.04, w * 1.04, 0.7, (x, y, z), ISTRIA))
        sp = cylinder(name + "_spire", w * 0.98 / math.sqrt(2), w * 1.3, (x, y, z + 0.7), "#8E6A4E", verts=4, r_top=0.12)
        sp.rotation_euler[2] = math.pi / 4
        parts.append(sp)
        parts.append(box(name + "_cross", 0.2, 0.2, 2.4, (x, y, z + 0.7 + w * 1.3), GOLD))
    return join(parts, name)


# ---------------------------------------------------------------- boats
def boat_hull(name, L, beam, h, color=BLACK, sheer=0.0, n=10):
    """A pointed hull lofted along X (bow at +X): lens-shaped plan, flat bottom, optional sheer at the ends."""
    verts, faces = [], []
    xs = [-L / 2 + L * i / n for i in range(n + 1)]
    for x in xs:
        t = 2 * x / L
        hw = max(0.04, beam / 2 * (1 - t ** 2) ** 0.6)
        lift = sheer * t ** 4
        verts += [(x, -hw * 0.7, lift * 0.6), (x, hw * 0.7, lift * 0.6), (x, hw, h + lift), (x, -hw, h + lift)]
    for i in range(n):
        a, b = 4 * i, 4 * (i + 1)
        faces += [(a, b, b + 1, a + 1), (a + 1, b + 1, b + 2, a + 2), (a + 2, b + 2, b + 3, a + 3), (a + 3, b + 3, b, a)]
    faces.append((3, 2, 1, 0))
    e = 4 * n
    faces.append((e, e + 1, e + 2, e + 3))
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def gondola(name, x, y, ang=0.0, z=0.0, L=10.8):
    parts = [boat_hull(name + "_h", L, 1.4, 0.55, BLACK, sheer=0.9),
             box(name + "_ferro", 0.12, 0.08, 0.9, (L / 2 - 0.2, 0, 0.9), "#C9C9C9"),
             box(name + "_seat", 1.2, 1.0, 0.25, (-0.6, 0, 0.45), RED_CLOTH),
             box(name + "_oar", 3.6, 0.07, 0.07, (-L / 2 + 1.4, 0.5, 1.4), TIMBER_V)]
    return place(join(parts, name), ang, x, y, z)


def galley(name, L, x, y, ang=0.0, z=0.0, oars=True, color="#6E4A32", canopy=RED_CLOTH, mast=True, n_oars=24):
    """A Venetian galley: long low hull, poop with a canopy, mast and lateen yard, banks of oars."""
    beam = L * 0.13
    parts = [boat_hull(name + "_hull", L, beam, 1.8, color, sheer=0.5, n=12),
             box(name + "_deck", L * 0.82, beam * 0.62, 0.15, (0, 0, 1.75), shade(color, 0.25)),
             box(name + "_beak", L * 0.12, 0.35, 0.35, (L / 2 + L * 0.05, 0, 1.6), color),
             box(name + "_poop", L * 0.12, beam * 0.7, 1.4, (-L * 0.38, 0, 1.8), canopy)]
    if mast:
        parts.append(cylinder(name + "_mast", 0.22, L * 0.42, (L * 0.1, 0, 1.8), TIMBER_D, verts=6))
        yard = box(name + "_yard", L * 0.62, 0.15, 0.15, (L * 0.1, 0, 1.8 + L * 0.36), TIMBER_D)
        parts.append(place(yard, 0, 0, 0, 0))
    if oars:
        verts, faces = [], []
        for side in (-1, 1):
            for i in range(n_oars):
                ox = -L * 0.32 + L * 0.68 * i / (n_oars - 1)
                y0, y1 = side * beam * 0.5, side * (beam * 0.5 + L * 0.2)
                z0, z1 = 1.6, 0.05
                b = len(verts)
                verts += [(ox - 0.08, y0, z0), (ox + 0.08, y0, z0), (ox + 0.08, y1, z1), (ox - 0.08, y1, z1)]
                faces.append((b, b + 1, b + 2, b + 3) if side > 0 else (b + 3, b + 2, b + 1, b))
        parts.append(mesh_from(name + "_oars", verts, faces, (0, 0, 0), TIMBER_V))
    return place(join(parts, name), ang, x, y, z)


# ---------------------------------------------------------------- buildings
def squero(name, x, y, w, l, h, ang=0.0, hull=True, roof=TILE, wall=BRICK_V, piers=4):
    """A covered slipway (squero or Arsenal tesa): brick piers carrying a long gable roof, open to the water at the front (-Y)."""
    parts = []
    for s in (-1, 1):
        for k in range(piers + 1):
            py = -l / 2 + l * k / piers
            parts.append(box(f"{name}_p{s}{k}", 1.4, 1.6, h, (s * (w / 2 - 0.7), py, 0), wall))
        parts.append(box(f"{name}_beam{s}", 1.0, l, 1.0, (s * (w / 2 - 0.5), 0, h - 1.0), shade(wall, -0.08)))
    parts.append(box(name + "_back", w, 1.2, h, (0, l / 2 - 0.6, 0), wall))
    parts.append(box(name + "_shade", w - 2.4, l - 1.4, 0.2, (0, 0, h - 0.3), DARK))
    parts.append(roof_y(name + "_roof", w, l, w * 0.32, 0, 0, h, roof, 0.4))
    parts.append(pediment(name + "_gab", w, w * 0.32, 0, -l / 2 - 0.05, h, -90, shade(wall, 0.06), 0.3))
    if hull:
        parts.append(place(boat_hull(name + "_g", l * 0.8, l * 0.1, 1.6, "#7A5638", 0.3, 8), 90, 0, 0, 0.6))
        parts.append(box(name + "_cradle", l * 0.06, l * 0.7, 0.6, (0, 0, 0), TIMBER_D))
    return place(join(parts, name), ang, x, y, 0)


def palazzo_water(name, w, d, h, x=0, y=0, ang=0.0, color=PLAST_V, style="gothic", storeys=3, roof=TILE):
    """A Venetian palazzo with its water-gate on the canal front (-Y): portego windows on the piano nobile, side windows, chimneys."""
    parts = [box(name + "_b", w, d, h, (0, 0, 0), color)]
    sh = h / storeys
    kind = "pointed" if style == "gothic" else "round"
    trim = ISTRIA
    parts.append(opening(name + "_gate", w * 0.22, sh * 0.82, 0, -d / 2 - 0.05, 0, -90, "round" if style != "gothic" else "pointed", DARK, 0.4))
    parts.append(box(name + "_step", w * 0.3, 0.8, 0.35, (0, -d / 2 - 0.4, 0), ISTRIA_D))
    for s in range(1, storeys):
        z = sh * s + sh * 0.18
        nob = s == 1
        n_mid = 4 if nob else 3
        parts.append(openings(f"{name}_mid{s}", w * 0.36, n_mid, w * 0.36 / n_mid * 0.72, sh * (0.62 if nob else 0.5), 0, -d / 2 - 0.05, z, -90, kind, DARK, 0.3))
        if nob:
            parts.append(box(f"{name}_bal{s}", w * 0.4, 0.8, 0.3, (0, -d / 2 - 0.35, z - 0.2), trim))
        for sx in (-1, 1):
            parts.append(openings(f"{name}_side{s}{sx}", w * 0.22, 2, w * 0.05, sh * 0.48, sx * w * 0.36, -d / 2 - 0.05, z, -90, kind, DARK, 0.3))
        parts.append(box(f"{name}_band{s}", w + 0.2, d + 0.2, 0.25, (0, 0, sh * s), trim))
    for sx in (-1, 1):
        parts.append(box(f"{name}_q{sx}", 0.5, 0.5, h, (sx * (w / 2 - 0.15), -d / 2 + 0.15, 0), trim))
    parts.append(box(name + "_corn", w + 0.6, d + 0.6, 0.5, (0, 0, h), trim))
    parts.append(hip(name + "_r", w, d, min(w, d) * 0.22, 0, 0, h + 0.5, roof, 0.5, 0.3))
    parts.append(chimney(name + "_ch1", -w * 0.3, d * 0.15, h + 0.5))
    parts.append(chimney(name + "_ch2", w * 0.32, -d * 0.2, h + 0.5))
    return place(join(parts, name), ang, x, y, 0)


def range_block(name, cx, cy, w, d, h, wall=PLAST_V, roof=TILE, rows=2, faces=("S",), kind="round", win=None, axis=None):
    """A plain range of rooms with a hipped roof and rows of windows on the given faces."""
    parts = [box(name + "_b", w, d, h, (cx, cy, 0), wall)]
    parts.append(hip(name + "_r", w, d, min(w, d) * 0.3, cx, cy, h, roof))
    st = h / rows
    for f in faces:
        L = w if f in "SN" else d
        n = win or max(2, int(L / 3.6))
        fx, fy, deg = {"S": (cx, cy - d / 2 - 0.05, -90), "N": (cx, cy + d / 2 + 0.05, 90), "E": (cx + w / 2 + 0.05, cy, 0), "W": (cx - w / 2 - 0.05, cy, 180)}[f]
        for r in range(rows):
            parts.append(openings(f"{name}_w{f}{r}", L * 0.9, n, min(1.3, L * 0.9 / n * 0.45), st * 0.5, fx, fy, st * r + st * 0.25, deg, kind, DARK, 0.25))
    return join(parts, name)


def classical_front(name, w, h, x, y, z, normal_deg, cols=4, col_r=0.8, pedestal=0.0, color=ISTRIA, ped_h=None, portal=True, statues=True, attic=0.0):
    """A temple front on a wall: giant half-columns (on pedestals), entablature, pediment, portal, figures."""
    parts = []
    ph = pedestal
    ch = h - ph - h * 0.09
    span = w - col_r * 3
    for i in range(cols):
        u = -span / 2 + span * i / (cols - 1)
        if ph:
            parts.append(box(f"{name}_ped{i}", col_r * 2.8, col_r * 2.2, ph, (u, col_r * 0.4, 0), color))
        parts.append(cylinder(f"{name}_c{i}", col_r, ch, (u, col_r * 0.3, ph), color, verts=14))
        parts.append(box(f"{name}_cap{i}", col_r * 2.7, col_r * 2.2, col_r * 0.9, (u, col_r * 0.3, ph + ch - col_r * 0.5), color))
    parts.append(box(name + "_ent", w, col_r * 2.6, h * 0.09, (0, col_r * 0.5, ph + ch), shade(color, -0.04)))
    parts.append(box(name + "_wall", w, 0.5, ph + ch, (0, col_r * 0.3 + 0.35, 0), shade(color, -0.02)))
    et = ph + ch + h * 0.09
    if attic:
        parts.append(box(name + "_att", w * 0.94, col_r * 1.6, attic, (0, col_r * 0.6, et), color))
        et += attic
    parts.append(multi_slab(name + "_ped", [[(-w / 2 - 0.4, et), (w / 2 + 0.4, et), (0, et + w * 0.2)]], col_r * 2.4, shade(color, 0.02), y0=col_r * 0.5))
    parts.append(multi_slab(name + "_tym", [[(-w / 2 + 1.0, et + 0.45), (w / 2 - 1.0, et + 0.45), (0, et + w * 0.2 - 0.6)]], 0.2, shade(color, -0.07), y0=-col_r * 0.75))
    if portal:
        pw = min(span / (cols - 1) * 0.62, 5.0)
        parts.append(multi_slab(name + "_door", [arch_pts(pw, min(ch * 0.42, pw * 2.1), "flat")], 0.4, DARK, y0=0.1))
        parts.append(multi_slab(name + "_dped", [[(-pw * 0.7, min(ch * 0.42, pw * 2.1) + 0.3), (pw * 0.7, min(ch * 0.42, pw * 2.1) + 0.3), (0, min(ch * 0.42, pw * 2.1) + 0.3 + pw * 0.35)]], 0.5, color, y0=0.0))
    if statues:
        for u, v in ((0, et + w * 0.2), (-w / 2, et), (w / 2, et)):
            parts.append(statue(f"{name}_st{u}", u, col_r * 0.5, v, max(1.8, h * 0.08), color))
    return on_wall(join(parts, name), x, y, z, normal_deg)


# ---------------------------------------------------------------- San Marco
def san_marco(variant="full"):
    m = Model("san-marco")
    full = variant == "full"
    early = variant == "1204"
    if variant == "832":
        return san_marco_832()
    wall = MARBLE_V if full else "#C99F84"
    m.add(0, plate(62, 77, PAVE_L), "ground")
    H, cy = 22.0, 2.0
    core = [box("sm_cross", 22, 22, H, (0, cy, 0), wall),
            box("sm_armS", 22, 20, H, (0, -19, 0), wall),
            box("sm_armN", 22, 17, H, (0, cy + 19.5, 0), BRICK_V if full else wall),
            box("sm_armW", 17, 22, H, (-19.5, cy, 0), wall),
            box("sm_armE", 17, 22, H, (19.5, cy, 0), wall)]
    for sx in (-1, 1):
        for syy in (-19.0, cy + 19.5):
            core.append(box(f"sm_corner{sx}{syy}", 17, 17 if syy > 0 else 20, 14, (sx * 19.5, syy, 0), shade(wall, -0.04)))
    core.append(cylinder("sm_apse", 9, H * 0.8, (0, 30, 0), BRICK_V, verts=20))
    core.append(box("sm_narthex", 62, 9.5, 13, (0, -33.75, 0), wall))
    core.append(box("sm_narthexW", 6.5, 42, 12, (-27.75, -8, 0), wall))
    core.append(box("sm_treasury", 6.5, 30, 12, (27.75, -14, 0), wall))
    core.append(box("sm_upper", 62, 6, 10, (0, -32, 13), wall))
    m.add(0, join(core, "sm_core"), "walls")

    f = []
    front = -38.55
    # five portals with gold lunettes, piers with two tiers of columns
    for i, (u, pw) in enumerate(((-24, 8.2), (-12, 8.2), (0, 10.5), (12, 8.2), (24, 8.2))):
        ph = 11.0 if u == 0 else 10.0
        f.append(opening(f"sm_portal{i}", pw, ph, u, front, 0, -90, "round", DARK, 1.6))
        f.append(opening(f"sm_lun{i}", pw * 0.78, pw * 0.39, u, front - 0.1, ph - pw * 0.5, -90, "round", MOSAIC if not early else "#B89A60", 0.4))
        for j, (dw, col) in enumerate(((1.4, ISTRIA), (2.6, ROSSO), (3.6, ISTRIA_D))):
            ring = [(px_, pz_) for px_, pz_ in arch_pts(pw + dw, ph + dw / 2, "round") if pz_ > ph - pw / 2 - 0.1]
            inner = [(px_, pz_) for px_, pz_ in arch_pts(pw + dw - 1.1, ph + dw / 2 - 0.55, "round") if pz_ > ph - pw / 2 - 0.1]
            band = ring[::-1] + inner if False else [p_ for p_ in ring if p_[1] > 0] 
            outer = [(px_, pz_) for px_, pz_ in arch_pts(pw + dw, ph + dw / 2, "round")][2:]
            innr = [(px_, pz_) for px_, pz_ in arch_pts(pw + dw - 1.0, ph + dw / 2 - 0.5, "round")][2:]
            f.append(on_wall(multi_slab(f"sm_ring{i}{j}", [outer + innr[::-1]], 0.3, col), u, front - 0.2 + j * 0.25, 0, -90))
    for k, u in enumerate((-30.2, -18, -6, 6, 18, 30.2)):
        for t, (zt, ht) in enumerate(((0.8, 5.0), (6.2, 4.2))):
            for du in (-1.15, -0.4, 0.4, 1.15):
                f.append(cylinder(f"sm_col{k}{t}{du}", 0.3, ht, (u + du, front - 0.6 - abs(du) * 0.3, zt), ROSSO if (k + t) % 2 else "#8A9A8C", verts=12))
                f.append(box(f"sm_colcap{k}{t}{du}", 0.7, 0.7, 0.35, (u + du, front - 0.6 - abs(du) * 0.3, zt + ht - 0.3), ISTRIA))
        f.append(box(f"sm_pierbase{k}", 3.2, 1.4, 0.8, (u, front - 0.5, 0), ISTRIA_D))
    # terrace balustrade
    f.append(box("sm_terrace", 62, 0.5, 1.1, (0, front + 0.3, 13), ISTRIA))
    f.append(box("sm_cornice13", 62.6, 1.2, 0.5, (0, front + 0.5, 12.6), ISTRIA_D))
    # upper façade: five round lunettes, crowned with ogee arches and pinnacles after c. 1400
    upper_y = -35.05
    for i, (u, lw) in enumerate(((-24, 9.0), (-12, 9.0), (0, 12.0), (12, 9.0), (24, 9.0))):
        lh = 15.0 if u else 16.5
        f.append(opening(f"sm_uframe{i}", lw, lh, u, upper_y, 13.4, -90, "round", ISTRIA, 0.9))
        inner = GLASS_V if u == 0 else (MOSAIC if not early else "#C2A378")
        f.append(opening(f"sm_umos{i}", lw * 0.8, lh - 1.2, u, upper_y - 0.4, 13.8, -90, "round", inner, 0.3))
        if u == 0:
            f.append(openings("sm_tracery", lw * 0.74, 5, 0.25, lh - 3, 0, upper_y - 0.6, 14.2, -90, "flat", ISTRIA, 0.2))
        if full:
            zs = 13.4 + lh - lw / 2
            f.append(opening(f"sm_ogee{i}", lw + 1.8, lw / 2 + lw * 0.95 + 0.4, u, upper_y + 0.5, zs, -90, "ogee", ISTRIA, 0.6))
            f.append(statue(f"sm_ustat{i}", u, upper_y + 0.4, zs + lw / 2 + lw * 0.95 + 0.4, 2.6 if u else 3.2, GOLD if u == 0 else ISTRIA))
    if full:
        for k, u in enumerate((-30.0, -18, -6, 6, 18, 30.0)):
            f.append(pinnacle(f"sm_tab{k}", u, upper_y + 1.0, 23.0, 1.8, 7.5, ISTRIA, COPPER))
            for t in range(2):
                for du in (-0.55, 0.55):
                    f.append(cylinder(f"sm_ucol{k}{t}{du}", 0.22, 4.4, (u + du, upper_y - 0.4, 13.6 + t * 4.7), ISTRIA_D if t else ROSSO, verts=10))
        # the four horses on the loggia
        for k, u in enumerate((-4.6, -1.55, 1.55, 4.6)):
            hz = 13.6
            hy = front + 2.2
            hp = [box(f"sm_hped{k}", 1.2, 2.6, 0.9, (u, hy, hz), ISTRIA_D),
                  box(f"sm_hbody{k}", 0.75, 2.1, 0.9, (u, hy, hz + 2.0), BRONZE_G),
                  box(f"sm_hneck{k}", 0.5, 0.7, 1.2, (u, hy - 1.05, hz + 2.6), BRONZE_G),
                  box(f"sm_hhead{k}", 0.4, 0.95, 0.42, (u, hy - 1.5, hz + 3.55), BRONZE_G)]
            for lx in (-0.25, 0.25):
                for ly in (-0.8, 0.8):
                    raise_ = 0.35 if (ly < 0 and lx < 0 and k % 2 == 0) else 0.0
                    hp.append(box(f"sm_hleg{k}{lx}{ly}", 0.18, 0.18, 1.1 - raise_, (u + lx, hy + ly, hz + 0.9 + raise_), BRONZE_G))
            f.append(join(hp, f"sm_horse{k}"))
        # transept ends with crowned arches
        for s in (-1, 1):
            f.append(opening(f"sm_tend{s}", 14, 17, s * 28.05, cy, 4, 0 if s > 0 else 180, "round", ISTRIA, 0.8))
            f.append(opening(f"sm_tmos{s}", 11, 15, s * 28.5, cy, 4.5, 0 if s > 0 else 180, "round", MOSAIC, 0.3))
            f.append(opening(f"sm_togee{s}", 15.6, 7 + 13.3, s * 27.6, cy, 14, 0 if s > 0 else 180, "ogee", ISTRIA, 0.5))
            for dy in (-8.5, 8.5):
                f.append(pinnacle(f"sm_ttab{s}{dy}", s * 28.0, cy + dy, H, 1.5, 6.0, ISTRIA, COPPER))
    else:
        for s in (-1, 1):
            f.append(opening(f"sm_tend{s}", 13, 16, s * 28.05, cy, 4, 0 if s > 0 else 180, "round", shade(wall, 0.08), 0.6))
    # flank arcades of the narthex and treasury
    f.append(arcade_open("sm_flankW", 40, 8, 9.5, -31.0, -8, 0, 180, wall, "round", 0.35, 2.5, None, ROSSO))
    f.append(openings("sm_flankWm", 36, 8, 2.6, 1.6, -31.25, -8, 7.6, 180, "round", MOSAIC if not early else "#B89A60", 0.2))
    f.append(arcade_open("sm_flankE", 28, 6, 9.0, 31.0, -14, 0, 0, wall, "round", 0.35, 2.5, None, ROSSO))
    for sx in (-1, 1):
        for k in range(10):
            f.append(on_wall(box(f"sm_panel{sx}{k}", 2.8, 0.2, 3.6, (0, 0, 0), ("#C9B9A8", "#B5A08E", "#D6CCBE")[k % 3]), sx * 28.1, -20 + k * 4.4 if sx > 0 else -20 + k * 4.4, 15.5, 0 if sx > 0 else 180))
    f.append(openings("sm_apsewin", 10, 3, 1.4, 4.5, 0, 39.05, 9, 90, "round", DARK, 0.3))
    m.add(1, join(f, "sm_facade"), "facade")

    d = []
    if early:
        for i, (x, y, r) in enumerate(((0, cy, 7.4), (0, -19, 6.9), (0, cy + 19.5, 6.4), (-19.5, cy, 6.4), (19.5, cy, 6.4))):
            d.append(byz_dome(f"sm_dome{i}", r, x, y, H, LEAD_V, wall, lantern=True, tall=False))
    else:
        for i, (x, y, r) in enumerate(((0, cy, 7.6), (0, -19, 7.2), (0, cy + 19.5, 6.6), (-19.5, cy, 6.6), (19.5, cy, 6.6))):
            d.append(byz_dome(f"sm_dome{i}", r, x, y, H, LEAD_V, MARBLE_V, lantern=True, tall=True))
    m.add(2, join(d, "sm_domes"), "domes")
    return m


def san_marco_832():
    m = Model("san-marco-832")
    m.add(0, plate(62, 77, "#C4B08C"), "ground")
    w = [box("sm1_nave", 14, 42, 11, (0, 2, 0), BRICK_V),
         box("sm1_tr", 36, 12, 11, (0, 8, 0), BRICK_V),
         cylinder("sm1_apse", 6.5, 9, (0, 23, 0), BRICK_V, verts=16),
         box("sm1_porch", 18, 5, 6, (0, -21.5, 0), PLAST_V)]
    w.append(openings("sm1_porcharc", 16, 5, 2.2, 4.4, 0, -24.05, 0, -90, "round", DARK, 0.3))
    w.append(opening("sm1_door", 2.6, 5, 0, -19.05, 0, -90, "round", DARK, 0.3))
    for s in (-1, 1):
        w.append(openings(f"sm1_win{s}", 30, 6, 1.0, 2.6, s * 7.05, -4, 6.5, 0 if s > 0 else 180, "round", DARK, 0.2))
    m.add(0, join(w, "sm1_walls"), "walls")
    r = [roof_y("sm1_rn", 14, 42, 4.5, 0, 2, 11, TILE),
         roof_x("sm1_rt", 36, 12, 4.5, 0, 8, 11, TILE),
         lean_to("sm1_rp", -9, 9, -24, -19, 6, 6, TILE)]
    r.append(dome("sm1_ad", 6.5, (0, 23, 9), TILE, squash=0.5, segments=16, rings=6))
    m.add(1, join(r, "sm1_roofs"), "roofs")
    m.add(2, join([cylinder("sm1_drum", 5, 3, (0, 8, 11), BRICK_V, verts=16), shallow_dome("sm1_dome", 5.2, (0, 8, 14), LEAD_V, rise=0.5),
                   box("sm1_cross", 0.2, 0.2, 1.6, (0, 8, 16.6), GOLD)], "sm1_dome"), "dome")
    return m


# ---------------------------------------------------------------- Campanile
def campanile_sm(variant="1514"):
    m = Model("campanile")
    m.add(0, plate(22, 18, PAVE_L, 0.25), "ground")
    tx = -5.0
    tower = venetian_campanile("cmp", 12, tx, 0, 50, variant, BRICK_V)
    m.add(1, tower, "tower")
    if variant == "1514":
        lg = [box("lg_body", 6.5, 16, 8.5, (4.25, 0, 0), ROSSO),
              box("lg_attic", 6.5, 16, 2.6, (4.25, 0, 8.5), ISTRIA),
              box("lg_terrace", 3.4, 16, 1.1, (9.2, 0, 0), ISTRIA_D)]
        lg.append(openings("lg_arches", 14, 3, 2.8, 6.2, 7.55, 0, 1.0, 0, "round", DARK, 0.4))
        for k, yy in enumerate((-7.6, -2.6, 2.6, 7.6)):
            for dy in (-0.55, 0.55):
                lg.append(cylinder(f"lg_col{k}{dy}", 0.28, 6.4, (7.8, yy + dy, 1.0), ISTRIA, verts=8))
        lg.append(openings("lg_rel", 14, 3, 3.2, 1.8, 7.55, 0, 8.9, 0, "flat", "#CDB98A", 0.2))
        for k in range(9):
            lg.append(box(f"lg_bal{k}", 0.3, 0.3, 0.9, (10.7, -7.6 + k * 1.9, 1.1), ISTRIA))
        lg.append(box("lg_rail", 0.4, 16, 0.25, (10.7, 0, 2.0), ISTRIA))
        m.add(2, join(lg, "loggetta"), "loggetta")
    else:
        stalls = []
        for k, yy in enumerate((-5.5, 0, 5.5)):
            stalls.append(box(f"st_b{k}", 3.5, 4.6, 2.8, (2.75, yy, 0), TIMBER_V))
            stalls.append(lean_to(f"st_r{k}", 4.8, 1.0, yy - 2.5, yy + 2.5, 2.8, 3.6, TILE))
        m.add(2, join(stalls, "stalls"), "stalls")
    return m


# ---------------------------------------------------------------- Doge's Palace
def gothic_facade(name, L, n, x, y, normal_deg, top=24.5, windows=(), balcony=True, bal_u=0.0):
    """The Doge's Palace front: ground arcade, traceried loggia, diamond wall with great windows, merli."""
    parts = [arcade_open(name + "_ground", L, n, 7.2, 0, 0, 0, -90, ISTRIA, "pointed", 0.62, 4.0, 2.3, ISTRIA_D),
             arcade_open(name + "_loggia", L, n * 2, 6.0, 0, 0, 7.2, -90, ISTRIA, "pointed", 0.26, 3.0, 2.6),
             quatrefoils(name + "_qf", L - 1.0, n * 2, 0.62, 0, -0.08, 12.55, -90, DARK, 0.2),
             box(name + "_bal", L, 0.6, 1.0, (0, -0.25, 7.2), ISTRIA),
             box(name + "_band", L + 0.4, 1.2, 0.5, (0, 0.3, 13.2), ISTRIA_D),
             diamond_wall(name + "_dw", L, top - 13.7, 0, 0, 13.7, -90, PINK, ISTRIA, 2.1)]
    for u in windows:
        parts.append(opening(f"{name}_win{u}", 2.6, 5.0, u, -0.25, 16.2, -90, "pointed", DARK, 0.4))
        parts.append(opening(f"{name}_winf{u}", 3.2, 5.6, u, -0.15, 15.9, -90, "pointed", ISTRIA, 0.25))
    for u in (-L * 0.21, L * 0.21):
        parts.append(disc(f"{name}_oc{u}", 0.9, u, -0.25, 21.4, -90, DARK, 0.3, 12))
    if balcony:
        parts.append(opening(name + "_bwin", 3.4, 7.2, bal_u, -0.35, 14.3, -90, "pointed", DARK, 0.4))
        parts.append(box(name + "_bbal", 5.0, 1.5, 0.6, (bal_u, -0.9, 14.0), ISTRIA))
        parts.append(opening(name + "_btab", 6.0, 11.8, bal_u, -0.6, 14.0, -90, "ogee", ISTRIA, 0.5))
        parts.append(opening(name + "_bwin2", 3.4, 7.2, bal_u, -0.9, 14.3, -90, "pointed", DARK, 0.2))
        parts.append(statue(name + "_justice", bal_u, -0.6, 25.9, 2.4, ISTRIA))
        for su in (-2.6, 2.6):
            parts.append(pinnacle(f"{name}_bp{su}", bal_u + su, -0.8, 14.6, 0.8, 7.5, ISTRIA, ISTRIA, False))
    parts.append(merli(name + "_merli", L, 0, -0.05, top, -90, 1.0, ISTRIA, 0.45, 0.4))
    o = join(parts, name)
    return on_wall(o, x, y, 0, normal_deg)


def byzantine_front(name, L, n, h, x, y, normal_deg, wall=PLAST_V):
    """The 12th-century palace front: two storeys of round-arched porticoes, crenellated."""
    parts = [arcade_open(name + "_g", L, n, h * 0.45, 0, 0, 0, -90, wall, "round", 0.5, 3.5, None, ISTRIA),
             arcade_open(name + "_u", L, n * 2, h * 0.32, 0, 0, h * 0.45, -90, wall, "round", 0.22, 2.5, None, ISTRIA),
             box(name + "_top", L, 1.0, h * 0.23, (0, 0.5, h * 0.77), wall),
             merli(name + "_m", L, 0, -0.05, h, -90, 0.9, ISTRIA, 0.6, 0.4)]
    parts.append(openings(name + "_tw", L * 0.9, n, 0.9, h * 0.14, 0, -0.05, h * 0.8, -90, "round", DARK, 0.2))
    return on_wall(join(parts, name), x, y, 0, normal_deg)


def doges_palace(variant="full"):
    if variant == "castle":
        return doges_castle()
    m = Model("doges-palace")
    m.add(0, plate(72, 100, PAVE_L), "ground")
    H = 24.5
    gothic_w = variant in ("full", "1400")
    w = []
    if gothic_w:
        w.append(box("dp_lag", 72, 22, H, (0, -39, 0), PINK))
    else:
        w.append(box("dp_lag", 72, 20, 15, (0, -40, 0), PLAST_V))
    if variant == "full":
        w.append(box("dp_pz", 22, 54, H, (-25, -1, 0), PINK))
        w.append(box("dp_east", 22, 78, 26, (25, 11, 0), ISTRIA_D))
        w.append(box("dp_north", 50, 10, 20, (-11, 45, 0), PLAST_V))
    else:
        w.append(box("dp_pz", 20, 56, 15, (-26, -2, 0), PLAST_V))
        w.append(box("dp_east", 20, 78, 16, (26, 11, 0), "#D9B79C"))
        w.append(box("dp_north", 52, 10, 14, (-10, 45, 0), PLAST_V))
    m.add(0, join(w, "dp_body"), "walls")

    f = []
    if variant == "full":
        f.append(gothic_facade("dp_S", 72, 17, 0, -50.0, -90, H, (-28.5, -19.5, -9.5, 9.5, 19.5, 28.5), True, 0.0))
        f.append(gothic_facade("dp_W", 75, 18, -36.0, -12.5, 180, H, (-31, -22, -12.5, 12.5, 22, 31), True, 0.0))
        # Porta della Carta between the palace and the basilica
        pc = [box("pc_b", 1.6, 8.0, 17, (-36.6, 30, 0), ISTRIA),
              opening("pc_door", 4.0, 9, -37.45, 30, 0, 180, "round", DARK, 0.4),
              opening("pc_win", 3.6, 5.5, -37.45, 30, 10.5, 180, "pointed", DARK, 0.4),
              opening("pc_crown", 7.6, 9.0, -37.3, 30, 15.5, 180, "ogee", ISTRIA, 0.5),
              statue("pc_st", -37.0, 30, 24.4, 2.2, ISTRIA)]
        for dy in (-3.6, 3.6):
            pc.append(pinnacle(f"pc_pin{dy}", -36.8, 30 + dy, 0, 1.0, 21, ISTRIA, ISTRIA, True))
        f.append(join(pc, "porta_carta"))
        # Rizzo's east wing on the Rio di Palazzo
        f.append(arcade_open("dp_Ecourt_g", 60, 12, 7.0, 13.95, 12, 0, 180, ISTRIA, "round", 0.5, 3.0, None, ISTRIA))
        f.append(openings("dp_Ecourt_1", 60, 12, 1.6, 4.2, 13.9, 12, 9.0, 180, "round", DARK, 0.3))
        f.append(openings("dp_Ecourt_2", 60, 12, 1.4, 3.6, 13.9, 12, 15.5, 180, "round", DARK, 0.3))
        f.append(openings("dp_Ecourt_3", 60, 12, 1.2, 3.0, 13.9, 12, 21.0, 180, "flat", DARK, 0.3))
        for r_, z in enumerate((2.0, 8.5, 15.0, 21.0)):
            f.append(openings(f"dp_Eout{r_}", 76, 16, 1.4, 3.6 if r_ else 2.6, 36.05, 11, z, 0, "round" if r_ < 3 else "flat", DARK, 0.3))
        f.append(merli("dp_Emerli", 78, 36.0, 11, 26, 0, 0.9, ISTRIA))
        # courtyard: Scala dei Giganti, wellheads, arcades of the Gothic wings
        f.append(stair("dp_giants", 7, 8, 12, 14, (8.0, 30, 0), "W", ISTRIA))
        f.append(box("dp_landing", 6, 7, 0.6, (11, 30, 7.6), ISTRIA))
        f.append(statue("dp_mars", 9.2, 27.2, 8.2, 3.4, ISTRIA))
        f.append(statue("dp_neptune", 9.2, 32.8, 8.2, 3.4, ISTRIA))
        for k, yy in enumerate((-5, 12)):
            f.append(cylinder(f"dp_well{k}", 1.3, 1.2, (-2, yy, 0), BRONZE_G, verts=14))
        f.append(arcade_open("dp_courtS", 28, 7, 7.0, 0, -27.95, 0, 90, ISTRIA, "pointed", 0.45, 2.5))
        f.append(arcade_open("dp_courtW", 52, 12, 7.0, -13.95, -1, 0, 0, ISTRIA, "pointed", 0.45, 2.5))
        f.append(openings("dp_courtW1", 52, 12, 1.4, 4.0, -13.9, -1, 10, 0, "pointed", DARK, 0.3))
        f.append(openings("dp_courtS1", 28, 7, 1.4, 4.0, 0, -27.9, 10, 90, "pointed", DARK, 0.3))
        for cx, cy in ((-36, -50), (36, -50), (-36, 26)):
            f.append(pinnacle(f"dp_corner{cx}{cy}", cx, cy, H, 1.6, 6.5, ISTRIA, ISTRIA, False))
    elif variant == "1400":
        f.append(gothic_facade("dp_S", 72, 17, 0, -50.0, -90, H, (-28.5, -19.5, -9.5, 9.5, 19.5, 28.5), True, 0.0))
        f.append(byzantine_front("dp_W", 56, 10, 15, -36.0, -2, 180))
        f.append(openings("dp_Eout", 76, 14, 1.4, 3.2, 36.05, 11, 6, 0, "pointed", DARK, 0.3))
        f.append(merli("dp_Emerli", 78, 36.0, 11, 16, 0, 0.9, ISTRIA))
        f.append(arcade_open("dp_courtS", 28, 7, 7.0, 0, -27.95, 0, 90, ISTRIA, "pointed", 0.45, 2.5))
        f.append(cylinder("dp_well", 1.3, 1.2, (-2, 5, 0), BRONZE_G, verts=14))
        for cx, cy in ((-36, -50), (36, -50)):
            f.append(pinnacle(f"dp_corner{cx}{cy}", cx, cy, H, 1.6, 6.5, ISTRIA, ISTRIA, False))
    else:  # Ziani's palace
        f.append(byzantine_front("dp_S", 72, 14, 15, 0, -50.0, -90))
        f.append(byzantine_front("dp_W", 56, 10, 15, -36.0, -2, 180))
        f.append(openings("dp_Eout", 76, 14, 1.4, 3.0, 36.05, 11, 6, 0, "round", DARK, 0.3))
        for k, (cx, cy) in enumerate(((-32, -46), (32, -46), (-32, 42))):
            f.append(box(f"dp_tower{k}", 9, 9, 22, (cx, cy, 0), "#C8A68A"))
            f.append(merli_ring(f"dp_tm{k}", 9, 9, 22, 0.9, "#C8A68A", cx, cy))
            f.append(openings(f"dp_tw{k}", 6, 2, 1.0, 2.6, cx, cy - 4.55, 15, -90, "round", DARK, 0.2))
        f.append(cylinder("dp_well", 1.3, 1.2, (-2, 5, 0), ISTRIA_D, verts=14))
    m.add(1, join([o for o in f if o], "dp_facades"), "facades")

    r = []
    if variant == "full":
        r.append(hip("dp_rlag", 72, 22, 6.5, 0, -39, H, LEAD_V, 0.6, 0.2))
        r.append(hip("dp_rpz", 22, 54, 6.5, -25, -1, H, LEAD_V, 0.6, 0.2))
        r.append(hip("dp_reast", 22, 78, 5.0, 25, 11, 26, LEAD_V, 0.6, 0.2))
        r.append(hip("dp_rnorth", 50, 10, 3.5, -11, 45, 20, TILE))
        for k, (cx, cy) in enumerate(((-20, -42), (20, -42), (-28, 10), (30, 30))):
            r.append(chimney(f"dp_ch{k}", cx, cy, H + 3.0, 0.55, 3.2, PLAST_V))
    elif variant == "1400":
        r.append(hip("dp_rlag", 72, 22, 6.5, 0, -39, H, LEAD_V, 0.6, 0.2))
        r.append(hip("dp_rpz", 20, 56, 4.5, -26, -2, 15, TILE))
        r.append(hip("dp_reast", 20, 78, 4.5, 26, 11, 16, TILE))
        r.append(hip("dp_rnorth", 52, 10, 3.5, -10, 45, 14, TILE))
    else:
        r.append(hip("dp_rlag", 72, 20, 4.5, 0, -40, 15, TILE))
        r.append(hip("dp_rpz", 20, 56, 4.5, -26, -2, 15, TILE))
        r.append(hip("dp_reast", 20, 78, 4.5, 26, 11, 16, TILE))
        r.append(hip("dp_rnorth", 52, 10, 3.5, -10, 45, 14, TILE))
    m.add(2, join(r, "dp_roofs"), "roofs")
    return m


def doges_castle():
    m = Model("doges-castle")
    m.add(0, plate(72, 100, "#BFA986"), "ground")
    pts = [(-32, -46), (32, -46), (32, 44), (-32, 44), (-32, -46)]
    m.add(0, wall_run("dc_wall", pts, 9, 2.2, (0, 0, 0), "#B38A6A", towers=False, merlon="box"), "walls")
    t = []
    for k, (cx, cy) in enumerate(((-32, -46), (32, -46), (32, 44), (-32, 44))):
        t.append(box(f"dc_t{k}", 9, 9, 16, (cx, cy, 0), "#A97E5E"))
        t.append(merli_ring(f"dc_tm{k}", 9, 9, 16, 1.0, "#A97E5E", cx, cy))
    t.append(gatehouse("dc_gate", 12, 9, 11, (-32, -5, 0), "W", "#A97E5E", ISTRIA, "roman"))
    t.append(box("dc_hall", 34, 14, 11, (2, 12, 0), "#C39C7C"))
    t.append(openings("dc_hallw", 30, 7, 1.4, 3.0, 2, 4.95, 6, -90, "round", DARK, 0.3))
    t.append(arcade_open("dc_hallarc", 30, 7, 5.0, 2, 4.95, 0, -90, "#C39C7C", "round", 0.4, 2.5, None, "#C39C7C", DARK, True))
    t.append(roof_x("dc_hallr", 34, 14, 5, 2, 12, 11, TILE))
    t.append(box("dc_wing", 12, 40, 8, (22, -18, 0), TIMBER_V))
    t.append(roof_y("dc_wingr", 12, 40, 4, 22, -18, 8, "#8C7656"))
    for k in range(5):
        t.append(box(f"dc_gal{k}", 1.2, 8, 0.4, (15.4, -36 + k * 9, 5), TIMBER_D))
    m.add(1, join(t, "dc_towers"), "towers")
    return m


# ---------------------------------------------------------------- Piazza and its buildings
def piazza(variant="1780"):
    m = Model("piazza")
    tirali = variant == "1780"
    poles = variant in ("1580", "1780")
    base = "#97928A" if tirali else "#B27C5F"
    m.add(0, plate(170, 64, base, 0.25), "paving")
    st = []
    if tirali:
        for yy in (-30, -18, -6, 6, 18, 30):
            st.append(box(f"pz_l{yy}", 160, 0.8, 0.08, (5, yy, 0.25), ISTRIA))
        for k in range(14):
            st.append(box(f"pz_t{k}", 0.8, 60, 0.08, (-70 + k * 11.5, 0, 0.25), ISTRIA))
        for k in range(13):
            for yy in (-12, 12):
                cx = -64 + k * 11.5
                st.append(place(box(f"pz_d{k}{yy}", 6.5, 0.6, 0.08, (0, 0, 0), ISTRIA), 35 if yy > 0 else -35, cx, yy, 0.25))
    else:
        for k in range(17):
            st.append(box(f"pz_t{k}", 0.9, 62, 0.08, (-75 + k * 9.6, 0, 0.25), ISTRIA))
        for yy in (-20, 0, 20):
            st.append(box(f"pz_l{yy}", 160, 0.9, 0.08, (5, yy, 0.25), ISTRIA))
    m.add(0, join(st, "pz_stripes"), "paving")
    g = []
    # San Geminiano closing the west end
    if variant in ("1580", "1780"):
        g += [box("sg_body", 14, 20, 15, (-78, 0, 0), ISTRIA_D),
              classical_front("sg_front", 16, 16, -70.95, 0, 0, 0, 4, 0.55, 0.0, ISTRIA, None, True, True, 3.0),
              hip("sg_roof", 14, 20, 4, -78, 0, 15, LEAD_V),
              cylinder("sg_drum", 3.6, 2.5, (-78, 0, 19), ISTRIA, verts=16),
              dome("sg_dome", 3.7, (-78, 0, 21.5), LEAD_V, squash=0.9, segments=16, rings=6),
              venetian_campanile("sg_camp", 4, -82, 8.5, 20, "old", BRICK_V)]
    else:
        g += [box("sg_body", 13, 20, 11, (-78, 0, 0), BRICK_V),
              roof_x("sg_roof", 13, 20, 4.5, -78, 0, 11, TILE),
              opening("sg_door", 2.4, 4.2, -71.45, 0, 0, 0, "round", DARK, 0.3),
              disc("sg_rose", 1.4, -71.45, 0, 8, 0, DARK, 0.3, 12),
              venetian_campanile("sg_camp", 4, -82, 8.5, 18, "old", BRICK_V)]
    if poles:
        for k, yy in enumerate((-15, 0, 15)):
            g += [cylinder(f"pz_pb{k}", 1.4, 1.0, (79, yy, 0.25), BRONZE_G, verts=12),
                  cylinder(f"pz_pb2{k}", 1.0, 1.6, (79, yy, 1.25), BRONZE_G, verts=12, r_top=0.6),
                  cylinder(f"pz_pole{k}", 0.24, 21, (79, yy, 2.8), "#8A4A32", verts=8),
                  box(f"pz_flag{k}", 0.1, 3.8, 5.2, (79, yy - 1.95, 17.5), RED_CLOTH),
                  box(f"pz_flagl{k}", 0.12, 1.2, 1.2, (79, yy - 1.95, 20.0), GOLD)]
    if variant == "1780":
        for k, (bx, by) in enumerate(((-30, 22), (-10, 24), (20, -24), (40, 22))):
            g.append(box(f"pz_booth{k}", 4, 3, 2.6, (bx, by, 0.25), TIMBER_V))
            g.append(roof_x(f"pz_boothr{k}", 4.4, 3.4, 1.2, bx, by, 2.85, "#B83A30"))
    m.add(1, join(g, "pz_things"), "buildings")
    return m


def procuratie_vecchie(variant="1514"):
    m = Model("procuratie-vecchie")
    L, D = 150, 22
    if variant == "1514":
        H = 20.0
        b = [box("pv_body", L, D, H, (0, 0, 0), ISTRIA)]
        b.append(arcade_open("pv_arc", L, 50, 8.0, 0, -11, 0, -90, ISTRIA, "round", 0.38, 4.0, 3.0, ISTRIA))
        for r_, z in enumerate((9.4, 14.6)):
            b.append(openings(f"pv_win{r_}", L - 2, 100, 0.85, 3.5, 0, -11.05, z, -90, "round", DARK, 0.25))
            b.append(box(f"pv_band{r_}", L, 0.8, 0.4, (0, -11.2, z - 0.8), ISTRIA_D))
            b.append(openings(f"pv_back{r_}", L - 2, 50, 1.0, 3.0, 0, 11.05, z, 90, "round", DARK, 0.25))
        b.append(box("pv_corn", L + 0.6, D + 0.6, 0.7, (0, 0, H), ISTRIA_D))
        m.add(0, join(b, "pv_body"), "walls")
        m.add(1, join([merli("pv_merli", L, 0, -11.2, H + 0.7, -90, 0.95, ISTRIA, 0.6),
                       hip("pv_roof", L, D - 2, 4.5, 0, 0, H + 0.7, TILE, 0.9, 0.0)] +
                      [chimney(f"pv_ch{k}", -70 + k * 14, 4, H + 2.5) for k in range(11)], "pv_top"), "roof")
    else:
        H = 12.0
        b = [box("pv_body", L, D, H, (0, 0, 0), PLAST_V)]
        b.append(arcade_open("pv_arc", L, 42, 6.2, 0, -11, 0, -90, PLAST_V, "round", 0.35, 3.5, None, ISTRIA))
        b.append(arcade_open("pv_up", L, 84, 4.4, 0, -11, 6.4, -90, PLAST_V, "round", 0.18, 2.0, None, ISTRIA))
        b.append(box("pv_band", L, 0.8, 0.4, (0, -11.2, 6.0), ISTRIA))
        m.add(0, join(b, "pv_body"), "walls")
        m.add(1, join([merli("pv_merli", L, 0, -11.1, H, -90, 0.9, ISTRIA, 0.7),
                       hip("pv_roof", L, D - 2, 4.0, 0, 0, H, TILE, 0.9, 0.0)], "pv_top"), "roof")
    return m


def classical_range(name, L, n, H, color=ISTRIA, depth=22, third=True):
    """Sansovino's two orders (and Scamozzi's third): arcaded Doric ground floor, arched windows above, entablatures."""
    bay = L / n
    parts = [box(name + "_body", L, depth, H, (0, 0, 0), color)]
    zs = [0.0, H * 0.43, H * 0.72 if third else H]
    parts.append(arcade_open(name + "_g", L, n, zs[1] - 1.4, 0, -depth / 2, 0, -90, color, "round", 0.42, 4.0, None, color, DARK, True))
    for i in range(n + 1):
        u = -L / 2 + bay * i
        parts.append(cylinder(f"{name}_hc{i}", 0.42, zs[1] - 1.6, (u, -depth / 2 - 0.25, 0), color, verts=10))
        parts.append(cylinder(f"{name}_hc2{i}", 0.34, (zs[2] if third else H) - zs[1] - 1.6, (u, -depth / 2 - 0.25, zs[1]), color, verts=10))
        if third:
            parts.append(cylinder(f"{name}_hc3{i}", 0.3, H - zs[2] - 1.4, (u, -depth / 2 - 0.25, zs[2]), color, verts=10))
    for z in zs[1:] + [H]:
        parts.append(box(f"{name}_ent{z}", L + 0.4, 1.3, 1.4, (0, -depth / 2 + 0.3, z - 1.4), shade(color, -0.05)))
    parts.append(openings(name + "_w1", L, n, bay * 0.42, (zs[2] if third else H) - zs[1] - 3.6, 0, -depth / 2 - 0.05, zs[1] + 0.8, -90, "round", DARK, 0.3))
    parts.append(openings(name + "_bal1", L, n, bay * 0.52, 1.0, 0, -depth / 2 - 0.4, zs[1], -90, "flat", color, 0.6))
    if third:
        parts.append(openings(name + "_w2", L, n, bay * 0.36, H - zs[2] - 3.4, 0, -depth / 2 - 0.05, zs[2] + 0.6, -90, "flat", DARK, 0.3))
    return join(parts, name)


def procuratie_nuove():
    m = Model("procuratie-nuove")
    L, D, H = 120, 22, 24.0
    m.add(0, classical_range("pn", L, 30, H, ISTRIA, D, True), "orders")
    r = [hip("pn_roof", L, D - 2, 4.5, 0, 0, H, TILE, 0.9, 0.0)]
    r += [chimney(f"pn_ch{k}", -55 + k * 12, 5, H + 2.0) for k in range(10)]
    r.append(box("pn_florian", 8, 0.3, 2.2, (-30, -11.6, 2.4), "#6E2E2A"))
    m.add(1, join(r, "pn_roof"), "roof")
    return m


def torre_orologio():
    m = Model("torre-orologio")
    t = [box("to_tower", 10, 10, 24, (0, 0, 0), ISTRIA),
         opening("to_arch", 4.6, 7.6, 0, -5.05, 0, -90, "round", DARK, 0.5),
         opening("to_arch_n", 4.6, 7.6, 0, 5.05, 0, 90, "round", DARK, 0.5),
         disc("to_dialring", 3.6, 0, -5.1, 12.0, -90, GOLD, 0.3, 28),
         disc("to_dial", 3.0, 0, -5.3, 12.0, -90, BLUE, 0.3, 28),
         disc("to_dialc", 0.9, 0, -5.5, 12.0, -90, GOLD, 0.3, 16),
         box("to_hand", 0.25, 0.2, 2.6, (0, -5.6, 12.0), GOLD),
         opening("to_madonna", 2.6, 3.2, 0, -5.15, 15.9, -90, "round", BLUE, 0.3),
         statue("to_mstat", 0, -5.3, 16.2, 1.8, GOLD),
         box("to_lionfield", 6.2, 0.3, 3.4, (0, -5.1, 19.6), BLUE),
         box("to_lion", 2.8, 0.25, 1.4, (0, -5.35, 20.4), GOLD),
         box("to_corn", 10.6, 10.6, 0.6, (0, 0, 24), ISTRIA_D)]
    for k in range(12):
        a = math.tau * k / 12
        t.append(box(f"to_star{k}", 0.25, 0.1, 0.25, (2.8 * math.cos(a) * 0.9, -5.28, 21.8 + 0.25 * math.sin(a)), GOLD))
    m.add(0, join(t, "to_tower"), "tower")
    w = []
    for s in (-1, 1):
        w.append(box(f"to_wing{s}", 8, 9, 15, (s * 9, 0.5, 0), ISTRIA))
        w.append(opening(f"to_wingarch{s}", 3.4, 6, s * 9, -4.05, 0, -90, "round", DARK, 0.4))
        for r_, z in enumerate((7.6, 11.6)):
            w.append(openings(f"to_wingwin{s}{r_}", 7, 3, 1.2, 2.6, s * 9, -4.05, z, -90, "round", DARK, 0.3))
        w.append(box(f"to_wingbal{s}", 8, 9, 0.9, (s * 9, 0.5, 15), ISTRIA_D))
    m.add(1, join(w, "to_wings"), "wings")
    top = [box("to_terr", 9, 9, 0.8, (0, 0, 24.6), ISTRIA),
           cylinder("to_bellpost", 0.25, 2.4, (0, 0, 25.4), BRONZE_G, verts=6),
           dome("to_bell", 1.4, (0, 0, 27.6), BRONZE_G, squash=1.2, segments=14, rings=6)]
    for s in (-1, 1):
        top.append(statue(f"to_moor{s}", s * 2.4, 0, 25.4, 2.8, "#4D4A40"))
        top.append(box(f"to_hammer{s}", 1.2, 0.15, 0.15, (s * 1.7, 0, 27.6), "#4D4A40"))
    m.add(2, join(top, "to_top"), "moors")
    return m


def marciana(variant="full"):
    m = Model("marciana")
    L, D, H = 74, 22, 19.5
    n = 21
    bay = L / n
    built = n if variant == "full" else 16
    Lb = bay * built
    cx = L / 2 - Lb / 2
    body = classical_range("lib", Lb, built, H, ISTRIA, D, False)
    body = move(body, cx, 0, 0)
    m.add(0, body, "orders")
    top = [box("lib_frieze", Lb + 0.4, 1.6, 2.0, (cx, -D / 2 + 0.4, H), shade(ISTRIA, -0.06)),
           openings("lib_garl", Lb, built, bay * 0.6, 1.2, cx, -D / 2 - 0.45, H + 0.4, -90, "flat", "#C9B48A", 0.2),
           box("lib_bal", Lb, 1.0, 1.4, (cx, -D / 2 + 0.6, H + 2.0), ISTRIA),
           hip("lib_roof", Lb, D - 2, 4.0, cx, 0.5, H + 2.0, LEAD_V, 0.8, 0.0)]
    for i in range(built + 1):
        u = cx - Lb / 2 + bay * i
        top.append(statue(f"lib_st{i}", u, -D / 2 + 0.5, H + 3.4, 2.3, ISTRIA))
    for s in (-1, 1):
        if s > 0 or variant == "full":
            top.append(cylinder(f"lib_ob{s}", 0.7, 4.0, (cx + s * Lb / 2, -D / 2 + 1.2, H + 3.4), ISTRIA, verts=4, r_top=0.1))
    m.add(1, join(top, "lib_top"), "balustrade")
    if variant != "full":
        old = []
        rest = L - Lb
        ox = -L / 2 + rest / 2
        for k in range(3):
            hx = ox - rest / 2 + rest * (k + 0.5) / 3
            old.append(box(f"old_h{k}", rest / 3 - 0.6, D - 4, 8 + k, (hx, 0, 0), PLAST_V if k % 2 else OCHRE))
            old.append(roof_x(f"old_r{k}", rest / 3 - 0.6, D - 4, 3, hx, 0, 8 + k, TILE))
            old.append(openings(f"old_w{k}", rest / 3 - 2, 2, 1.2, 2.2, hx, -D / 2 + 1.95, 4, -90, "round", DARK, 0.2))
        for k in range(5):
            old.append(cylinder(f"scaf{k}", 0.15, 20, (-L / 2 + rest + 0.6, -D / 2 - 0.5 + k * 5.5, 0), TIMBER_V, verts=4))
        m.add(1, join(old, "lib_old"), "balustrade")
    return m


def columns_molo():
    m = Model("columns")
    m.add(0, plate(22, 6, PAVE_L, 0.2), "ground")
    parts = []
    for s, col, top in ((-1, GRANITE_R, "theodore"), (1, GRANITE_G, "lion")):
        x = s * 8.0
        for k, (sw, sh) in enumerate(((4.4, 0.45), (3.7, 0.45), (3.0, 0.45))):
            parts.append(box(f"cl_step{s}{k}", sw, sw, sh, (x, 0, 0.2 + k * 0.45), ISTRIA_D))
        parts.append(box(f"cl_plinth{s}", 2.2, 2.2, 1.6, (x, 0, 1.55), ISTRIA))
        parts.append(cylinder(f"cl_shaft{s}", 0.78, 12.5, (x, 0, 3.15), col, verts=24))
        parts.append(box(f"cl_cap{s}", 2.3, 2.3, 1.4, (x, 0, 15.65), ISTRIA))
        parts.append(box(f"cl_abacus{s}", 2.7, 2.7, 0.5, (x, 0, 17.05), ISTRIA_D))
        z = 17.55
        if top == "lion":
            parts += [box("cl_lion_b", 1.2, 3.0, 1.2, (x, 0, z + 0.5), "#4E5A47"),
                      box("cl_lion_h", 1.1, 1.0, 1.1, (x, -1.6, z + 1.2), "#4E5A47"),
                      box("cl_lion_mane", 1.4, 0.6, 1.4, (x, -1.0, z + 1.0), "#4E5A47")]
            for lx in (-0.4, 0.4):
                for ly in (-1.1, 1.1):
                    parts.append(box(f"cl_lleg{lx}{ly}", 0.3, 0.3, 0.6, (x + lx, ly, z), "#4E5A47"))
            for wx in (-1, 1):
                wing = box(f"cl_wing{wx}", 0.15, 1.8, 1.4, (0, 0, 0), "#4E5A47")
                parts.append(place(wing, 0, x + wx * 0.7, 0.4, z + 1.6))
        else:
            parts += [box("cl_croc", 0.7, 3.0, 0.45, (x, 0.2, z), "#9A9078"),
                      statue("cl_theo", x, -0.2, z + 0.45, 2.6, ISTRIA),
                      box("cl_spear", 0.1, 0.1, 3.4, (x + 0.6, -0.2, z + 0.6), "#8A8A80"),
                      box("cl_shield", 0.2, 0.9, 1.1, (x - 0.55, -0.2, z + 1.4), ISTRIA_D)]
    m.add(1, join(parts, "cl_cols"), "columns")
    return m


def bucintoro(variant="1729"):
    m = Model("bucintoro")
    late = variant == "1729"
    L = 35.0 if late else 30.0
    beam = 7.4 if late else 6.0
    hull = [boat_hull("bu_hull", L, beam, 2.0, "#8A2E24", sheer=0.6, n=14),
            box("bu_gilt", L * 0.86, beam * 1.0, 0.7, (0, 0, 1.6), GOLD),
            box("bu_deck", L * 0.84, beam * 0.88, 0.25, (0, 0, 2.2), "#9B7B4A"),
            box("bu_beak", 5.0, 0.6, 0.6, (L / 2 + 2.2, 0, 1.6), GOLD),
            statue("bu_justice", L / 2 - 0.6, 0, 2.4, 2.8 if late else 2.0, GOLD)]
    n_oars = 21 if late else 18
    verts, faces = [], []
    for side in (-1, 1):
        for i in range(n_oars):
            ox = -L * 0.36 + L * 0.72 * i / (n_oars - 1)
            y0, y1 = side * beam * 0.5, side * 7.8
            b = len(verts)
            verts += [(ox - 0.1, y0, 1.6), (ox + 0.1, y0, 1.6), (ox + 0.1, y1, 0.05), (ox - 0.1, y1, 0.05)]
            faces.append((b, b + 1, b + 2, b + 3) if side > 0 else (b + 3, b + 2, b + 1, b))
    hull.append(mesh_from("bu_oars", verts, faces, (0, 0, 0), "#7A2A22"))
    m.add(0, join(hull, "bu_hull"), "hull")
    top = []
    cl = L * (0.72 if late else 0.5)
    cx = -L * 0.08
    top.append(box("bu_cab", cl, beam * 0.86, 2.6, (cx, 0, 2.45), RED_CLOTH))
    vault = cylinder("bu_vault", beam * 0.43, cl, (0, 0, -cl / 2), RED_CLOTH, verts=16)
    apply_rot(vault, ry=math.pi / 2)
    top.append(place(vault, 0, cx, 0, 5.05))
    for k in range(int(cl / 2.4)):
        rib = cylinder(f"bu_rib{k}", beam * 0.43 + 0.06, 0.22, (0, 0, -0.11), GOLD, verts=16)
        apply_rot(rib, ry=math.pi / 2)
        top.append(move(rib, cx - cl / 2 + 1.2 + k * 2.4, 0, 5.05))
    for s in (-1, 1):
        top.append(openings(f"bu_win{s}", cl - 1.0, int(cl / 2.0), 1.1, 1.9, cx, s * beam * 0.43 + s * 0.05, 2.7, 90 if s > 0 else -90, "round", GOLD, 0.15))
    top.append(box("bu_throne", 2.0, 2.2, 2.8, (-L / 2 + 2.4, 0, 2.45), GOLD))
    top.append(dome("bu_shell", 1.6, (-L / 2 + 2.4, 0, 5.2), GOLD, squash=0.8, segments=12, rings=5))
    top.append(cylinder("bu_flagpole", 0.12, 7, (-L / 2 + 0.8, 0, 2.4), GOLD, verts=6))
    top.append(box("bu_flag", 0.08, 2.6, 1.7, (-L / 2 + 0.8, -1.35, 7.4), RED_CLOTH))
    if late:
        for s in (-1, 1):
            for k in range(10):
                top.append(statue(f"bu_putto{s}{k}", -L * 0.4 + k * L * 0.08, s * beam * 0.5, 2.3, 0.9, GOLD))
    m.add(1, join(top, "bu_top"), "canopy")
    return m


# ---------------------------------------------------------------- Rialto
def rialto_bridge(variant="stone"):
    if variant == "wood":
        return rialto_wood()
    if variant == "pontoon":
        return rialto_pontoon()
    m = Model("rialto-bridge")
    half_span, rise, deck_end, deck_top, W = 14.4, 7.5, 1.4, 10.0, 22.9
    xs = [-26 + 52 * i / 40 for i in range(41)]

    def zu(x):
        return rise * max(0.0, 1 - (x / half_span) ** 2) ** 0.55 if abs(x) < half_span else 0.0

    def zt(x):
        return deck_end + (deck_top - deck_end) * (1 - abs(x) / 26)

    verts, faces = [], []
    for x in xs:
        verts += [(x, -W / 2, zu(x)), (x, W / 2, zu(x)), (x, W / 2, zt(x)), (x, -W / 2, zt(x))]
    for i in range(len(xs) - 1):
        a, b = 4 * i, 4 * (i + 1)
        faces += [(a, a + 1, b + 1, b), (a + 1, a + 2, b + 2, b + 1), (a + 2, a + 3, b + 3, b + 2), (a + 3, a, b, b + 3)]
    faces.append((0, 3, 2, 1))
    e = 4 * (len(xs) - 1)
    faces.append((e, e + 1, e + 2, e + 3))
    m.add(0, mesh_from("rb_body", verts, faces, (0, 0, 0), ISTRIA), "arch")
    ring = []
    for s in (-1, 1):
        pts = []
        for k in range(17):
            x = -half_span + 2 * half_span * k / 16
            pts.append((x, zu(x)))
        band = [(x, z) for x, z in pts] + [(x, z + 1.0) for x, z in reversed(pts)]
        ring.append(on_wall(multi_slab(f"rb_ring{s}", [band], 0.3, ISTRIA_D), 0, s * (W / 2 + 0.1), 0, 90 if s > 0 else -90))
        for u in (-8, 8):
            ring.append(on_wall(box(f"rb_relief{s}{u}", 2.6, 0.2, 2.2, (0, 0, 0), "#D9CDB2"), u, s * (W / 2 + 0.15), zu(u) + 1.3, 90 if s > 0 else -90))
    m.add(0, join(ring, "rb_ring"), "arch")
    shops = []
    for side in (-1, 1):
        for sgn in (-1, 1):
            for k in range(6):
                x0 = sgn * (3.2 + k * 3.1)
                x1 = sgn * (3.2 + (k + 1) * 3.1)
                xc = (x0 + x1) / 2
                base = zt(max(abs(x0), abs(x1)) * sgn)
                yc = side * 5.7
                shops.append(box(f"rb_shop{side}{sgn}{k}", 3.1, 4.6, 4.6 + (zt(xc) - base), (xc, yc, base), ISTRIA))
                shops.append(opening(f"rb_sa{side}{sgn}{k}", 2.2, 3.4, xc, yc - side * 2.35, zt(xc), -90 if side < 0 else 90, "round", DARK, 0.25))
                shops.append(opening(f"rb_sb{side}{sgn}{k}", 2.2, 3.4, xc, yc + side * 2.35, zt(xc), 90 if side > 0 else -90, "round", DARK, 0.25))
            xa, xb = sgn * 3.0, sgn * 22.0
            shops.append(lean_to(f"rb_roof{side}{sgn}", xb, xa, side * 3.0, side * 8.4, zt(xb) + 4.6, zt(xa) + 4.6, LEAD_V) if sgn > 0 else
                         lean_to(f"rb_roof{side}{sgn}", xb, xa, side * 3.0, side * 8.4, zt(xb) + 4.6, zt(xa) + 4.6, LEAD_V))
    for s in (-1, 1):
        for sgn in (-1, 1):
            xa, xb = sgn * 0.5, sgn * 26
            shops.append(lean_to(f"rb_par{s}{sgn}", xb, xa, s * W / 2 - (0.6 if s > 0 else 0), s * W / 2 + (0 if s > 0 else 0.6), zt(xb), zt(xa), ISTRIA_D))
    portico = [box("rb_port", 6.4, 16.4, 6.0, (0, 0, deck_top), ISTRIA),
               opening("rb_port_e", 4.0, 5.0, 3.25, 0, deck_top, 0, "round", DARK, 0.4),
               opening("rb_port_w", 4.0, 5.0, -3.25, 0, deck_top, 180, "round", DARK, 0.4),
               pediment("rb_ped_s", 6.8, 2.2, 0, -8.25, deck_top + 6.0, -90, ISTRIA, 0.6),
               pediment("rb_ped_n", 6.8, 2.2, 0, 8.25, deck_top + 6.0, 90, ISTRIA, 0.6),
               roof_y("rb_port_r", 6.4, 16.4, 2.2, 0, 0, deck_top + 6.0, LEAD_V, 0.2)]
    shops += portico
    m.add(1, join(shops, "rb_shops"), "shops")
    m.add(2, gondola("rb_gondola", 4, -2, 15, 0), "boats")
    return m


def rialto_wood():
    m = Model("rialto-bridge-wood")
    W = 13.0
    zc = 6.6

    def zt(x):
        ax = abs(x)
        return zc if ax < 6 else 1.2 + (zc - 1.2) * (26 - ax) / 20

    piles = []
    for x in (-24, -18, -12, -6.5, 6.5, 12, 18, 24):
        for y in (-5.5, -2, 2, 5.5):
            piles.append(cylinder(f"rw_pile{x}{y}", 0.35, zt(x), (x, y, 0), TIMBER_D, verts=6))
        piles.append(box(f"rw_cap{x}", 0.8, W, 0.6, (x, 0, zt(x) - 0.6), TIMBER_D))
    for sgn in (-1, 1):
        piles.append(lean_to(f"rw_deck{sgn}", sgn * 26, sgn * 6, -W / 2, W / 2, 1.0, zc - 0.2, TIMBER_V))
    m.add(0, join(piles, "rw_piles"), "piles")
    top = []
    for sgn in (-1, 1):
        for side in (-1, 1):
            for k in range(5):
                xc = sgn * (8.0 + k * 3.4)
                top.append(box(f"rw_shop{sgn}{side}{k}", 3.2, 3.6, 3.4, (xc, side * 4.6, zt(xc) - 0.1), "#9A6E4A" if k % 2 else TIMBER_V))
                top.append(opening(f"rw_shopo{sgn}{side}{k}", 2.2, 2.4, xc, side * 2.75, zt(xc), 90 if side < 0 else -90, "flat", DARK, 0.2))
            top.append(lean_to(f"rw_roof{sgn}{side}", sgn * 24.5, sgn * 6.4, side * 2.6 if side > 0 else -6.8, side * 6.8 if side > 0 else -2.6, zt(24.5) + 3.4, zt(6.4) + 3.4, TILE))
    # the central lifting span between its two timber gantries
    top.append(box("rw_leafA", 6.0, W - 1, 0.5, (-3.0, 0, zc - 0.3), TIMBER_V))
    leaf = box("rw_leafB", 6.0, W - 1, 0.5, (3.0, 0, 0), TIMBER_V)
    apply_rot(leaf, ry=-math.radians(12))
    top.append(move(leaf, 0, 0, zc + 0.3))
    for x in (-6.2, 6.2):
        for y in (-6.0, 6.0):
            top.append(box(f"rw_post{x}{y}", 0.6, 0.6, 7.5, (x, y, zc), TIMBER_D))
        top.append(box(f"rw_lintel{x}", 0.7, W + 0.4, 0.7, (x, 0, zc + 7.5), TIMBER_D))
        top.append(roof_y(f"rw_gantryroof{x}", 1.6, W + 1, 1.0, x, 0, zc + 8.2, TILE, 0.2))
    for s in (-1, 1):
        for sgn in (-1, 1):
            top.append(lean_to(f"rw_rail{s}{sgn}", sgn * 26, sgn * 6, s * W / 2 - 0.15, s * W / 2 + 0.15, 2.0, zc + 1.0, TIMBER_D))
    m.add(1, join(top, "rw_shops"), "shops")
    m.add(2, gondola("rw_gondola", -1, -9, 10, 0), "boats")
    return m


def rialto_pontoon():
    m = Model("rialto-pontoon")
    boats = []
    for k in range(9):
        x = -22 + k * 5.5
        boats.append(place(boat_hull(f"rp_boat{k}", 12.0, 2.6, 1.0, "#5E4632", sheer=0.4, n=8), 90, x, 0, 0))
    m.add(0, join(boats, "rp_boats"), "boats")
    d = [box("rp_deck", 48, 4.4, 0.3, (0, 0, 1.0), TIMBER_V)]
    for k in range(25):
        d.append(box(f"rp_plank{k}", 0.15, 4.6, 0.05, (-23 + k * 1.9, 0, 1.3), TIMBER_D))
    for x in (-25.5, 25.5):
        d.append(lean_to(f"rp_ramp{x}", x + (1.5 if x > 0 else -1.5), x, -2.2, 2.2, 0.3, 1.3, TIMBER_V))
        for y in (-3.0, 3.0):
            d.append(cylinder(f"rp_post{x}{y}", 0.25, 3.0, (x, y, 0), TIMBER_D, verts=6))
    for s in (-1, 1):
        d.append(box(f"rp_rope{s}", 48, 0.08, 0.08, (0, s * 2.2, 2.1), "#C9B48A"))
        for k in range(9):
            d.append(cylinder(f"rp_stan{s}{k}", 0.08, 1.1, (-22 + k * 5.5, s * 2.2, 1.3), TIMBER_D, verts=4))
    m.add(1, join(d, "rp_deck"), "deck")
    return m


def stall(name, x, y, color, awning=None):
    return join([box(name + "_t", 2.6, 1.6, 0.9, (x, y, 0.3), TIMBER_V),
                 box(name + "_g", 2.2, 1.2, 0.3, (x, y, 1.2), color),
                 cylinder(name + "_p", 0.06, 2.6, (x - 1.2, y + 0.7, 0.3), TIMBER_D, verts=4),
                 lean_to(name + "_a", x - 1.6, x + 1.6, y - 1.4, y + 1.0, 2.9, 2.9, awning or "#C9A65A")], name)


def san_giacomo(name, x, y):
    parts = [box(name + "_b", 14, 15, 9, (x, y, 0), BRICK_V),
             box(name + "_por", 14, 4.2, 5.0, (x, y - 9.6, 0), PLAST_V),
             lean_to(name + "_porr", x - 7.3, x + 7.3, y - 11.9, y - 7.5, 5.0, 5.0, TILE),
             box(name + "_gable", 6, 1.0, 5.0, (x, y - 7.6, 9), BRICK_V),
             disc(name + "_clock", 1.6, x, y - 8.2, 11.2, -90, BLUE, 0.3, 20),
             disc(name + "_clockr", 1.9, x, y - 8.1, 11.2, -90, GOLD, 0.25, 20),
             roof_y(name + "_r", 14, 15, 4, x, y, 9, TILE),
             cylinder(name + "_drum", 3.2, 2.2, (x, y + 1, 11.5), BRICK_V, verts=14),
             dome(name + "_dome", 3.3, (x, y + 1, 13.7), LEAD_V, squash=0.7, segments=14, rings=5)]
    for k in range(5):
        parts.append(column(f"{name}_col{k}", x - 6 + k * 3, y - 11.5, 0, 0.35, 4.6, ISTRIA, True, 8))
    parts.append(box(name + "_bell", 1.2, 0.8, 2.6, (x, y - 7.6, 14.0), BRICK_V))
    return join(parts, name)


def rialto_market(variant="1580"):
    m = Model("rialto-market")
    m.add(0, plate(56, 96, PAVE_V), "ground")
    b = [san_giacomo("sgr", -8, -30)]
    st = []
    colors = ("#7FA05A", "#C9783A", "#B8A048", "#9A5A8A", "#C9C26A", "#6F8F5A")
    if variant == "1580":
        b.append(range_block("fv_w", -22, -2, 12, 72, 13, OCHRE, TILE, 3, ("E", "W"), "round"))
        b.append(arcade_open("fv_warc", 70, 18, 5.0, -15.95, -2, 0, 0, OCHRE, "round", 0.45, 3.0, None, ISTRIA, DARK, True))
        b.append(range_block("fv_n", -5, 39, 22, 12, 13, OCHRE, TILE, 3, ("S", "N"), "round"))
        b.append(range_block("fn", 20, 18, 12, 56, 14, ISTRIA_D, TILE, 3, ("E", "W"), "round"))
        b.append(arcade_open("fn_arc", 54, 18, 5.2, 26.05, 18, 0, 0, ISTRIA_D, "round", 0.45, 3.0, None, ISTRIA, DARK, True))
        b.append(palazzo_water("camerl", 14, 18, 14, 20, -36, 90, ISTRIA_D, "renaissance", 3, LEAD_V))
        pes = [box("pe_roof_base", 18, 10, 0.4, (-4, 31.5, 5.6), TIMBER_D), roof_x("pe_roof", 18, 10, 3.2, -4, 31.5, 6.0, TILE)]
        for kx in range(4):
            for ky in (-1, 1):
                pes.append(column(f"pe_col{kx}{ky}", -12 + kx * 5.4, 31.5 + ky * 4.4, 0, 0.35, 5.6, ISTRIA, True, 8))
        for k in range(4):
            pes.append(box(f"pe_bench{k}", 3.2, 1.4, 0.9, (-11 + k * 4.8, 31.5, 0.3), ISTRIA_D))
        b.append(join(pes, "pescheria"))
        b.append(statue("gobbo", 2, -20, 0.3, 1.8, ISTRIA))
        b.append(column("bando", 2, -18, 0.3, 0.6, 2.6, ROSSO, True, 10))
        for k in range(8):
            st.append(stall(f"erb{k}", 2 + (k % 2) * 5.5, -8 + (k // 2) * 5.2, colors[k % len(colors)], "#E6DCC8" if k % 3 else RED_CLOTH))
    else:
        b.append(palazzo_water("ware1", 12, 26, 10, 21, 20, 90, BRICK_V, "gothic", 2))
        b.append(palazzo_water("ware2", 12, 18, 9, -20, 10, -90, PLAST_V, "gothic", 2))
        b.append(range_block("ware3", -20, 36, 12, 18, 8, BRICK_V, TILE, 2, ("E",), "pointed"))
        lg = [box("loggia_roofb", 14, 7, 0.4, (14, -14, 4.6), TIMBER_D), roof_x("loggia_r", 14, 7, 2.4, 14, -14, 5.0, TILE)]
        for kx in range(4):
            for ky in (-1, 1):
                lg.append(cylinder(f"loggia_p{kx}{ky}", 0.25, 4.6, (8 + kx * 4, -14 + ky * 3, 0), TIMBER_D, verts=6))
        b.append(join(lg, "loggia"))
        for k in range(14):
            st.append(stall(f"st{k}", -8 + (k % 4) * 5.0, -6 + (k // 4) * 6.5, colors[k % len(colors)]))
        for k in range(3):
            st.append(box(f"shed{k}", 6, 4, 3.4, (6 + k * 7, 34, 0), TIMBER_V))
            st.append(roof_x(f"shedr{k}", 6, 4, 1.6, 6 + k * 7, 34, 3.4, TILE))
    m.add(1, join(b, "rm_buildings"), "buildings")
    m.add(2, join(st, "rm_stalls"), "stalls")
    return m


# ---------------------------------------------------------------- the Arsenal
def arsenale(variant="full"):
    m = Model("arsenale")
    full = variant == "full"
    mid = variant in ("full", "1400")
    m.add(0, plate(560, 600, MARSH_V if not full else YARD, 0.3), "ground")
    g = []
    if not full:
        g.append(box("ar_yardV", 166, 176, 0.32, (-193, -208, 0), YARD))
        if mid:
            g.append(box("ar_yardN", 200, 276, 0.32, (-10, -158, 0), YARD))
    m.add(0, join(g, "ar_yards"), "ground") if g else None
    water = [box("ar_entry", 18, 60, 0.4, (-264, -270, 0), WATER_V),
             box("ar_entry2", 20, 24, 0.4, (-257, -240, 0), WATER_V),
             box("ar_dv", 110, 100, 0.4, (-195, -200, 0), WATER_V)]
    if mid:
        water += [box("ar_dn", 180, 190, 0.4, (-20, -135, 0), WATER_V),
                  box("ar_c1", 32, 22, 0.4, (-125, -200, 0), WATER_V)]
    if full:
        water += [box("ar_dnv", 340, 140, 0.4, (-30, 130, 0), WATER_V),
                  box("ar_dg", 140, 200, 0.4, (180, -60, 0), WATER_V),
                  box("ar_c2", 44, 24, 0.4, (90, -100, 0), WATER_V),
                  box("ar_c3", 26, 104, 0.4, (0, 10, 0), WATER_V),
                  box("ar_c4", 24, 104, 0.4, (-100, 250, 0), WATER_V)]
    elif mid:
        water.append(box("ar_lago", 300, 160, 0.33, (-20, 150, 0), "#7E9C96"))
    m.add(0, join(water, "ar_water"), "ground")

    # walls
    if full:
        pts = [(-276, -296), (-272, -296), (276, -296), (276, 296), (-88, 296)]
        pts2 = [(-112, 296), (-276, 296), (-276, -230)]
    elif mid:
        pts = [(-276, -296), (-272, -296), (90, -296), (90, 20), (-120, 20), (-120, -110), (-276, -110), (-276, -230)]
        pts2 = None
    else:
        pts = [(-276, -296), (-272, -296), (-120, -296), (-120, -112), (-276, -112), (-276, -230)]
        pts2 = None
    walls = [wall_run("ar_wall", pts, 10, 2.4, (0, 0, 0), BRICK_V, towers=True, tower_r=4.5, tower_every=110, merlon="box", tower_shape="square")]
    if pts2:
        walls.append(wall_run("ar_wall2", pts2, 10, 2.4, (0, 0, 0), BRICK_V, towers=True, tower_r=4.5, tower_every=110, merlon="box", tower_shape="square"))
    m.add(1, join(walls, "ar_walls"), "walls")

    # water gate and land gate
    gt = []
    for s in (-1, 1):
        tx = -264 + s * 15
        th = 22 if full else 15
        gt.append(box(f"ar_wt{s}", 11, 11, th, (tx, -290, 0), BRICK_V))
        gt.append(merli_ring(f"ar_wtm{s}", 11, 11, th, 1.1, ISTRIA if full else BRICK_V, tx, -290))
        gt.append(openings(f"ar_wtw{s}", 8, 2, 1.2, 3.0, tx, -295.55, th - 6, -90, "round", DARK, 0.3))
        if full:
            gt.append(box(f"ar_wtband{s}", 11.4, 11.4, 0.6, (tx, -290, th - 2.5), ISTRIA))
    gt.append(box("ar_wtbridge", 20, 4, 1.0, (-264, -293, 9), TIMBER_V))
    if full:
        pm = [box("pm_body", 13, 4, 13, (-238, -298, 0), ISTRIA),
              opening("pm_arch", 5.0, 8.6, -238, -300.05, 0, -90, "round", DARK, 0.6),
              pediment("pm_ped", 13.6, 3.2, -238, -300.1, 13, -90, ISTRIA, 0.8),
              box("pm_lionrel", 4.0, 0.3, 2.4, (-238, -300.2, 9.4), GOLD),
              statue("pm_giustina", -238, -299, 16.2, 2.6, ISTRIA)]
        for du in (-4.6, -3.2, 3.2, 4.6):
            pm.append(cylinder(f"pm_col{du}", 0.42, 9.0, (-238 + du, -300.4, 0), "#C9B9A5", verts=10))
        for du in (-9.0, 9.0):
            pm.append(box(f"pm_lped{du}", 2.4, 3.2, 1.6, (-238 + du, -299.2, 0), ISTRIA_D))
            pm.append(box(f"pm_lion{du}", 1.2, 2.6, 1.8, (-238 + du, -299.2, 1.6), ISTRIA))
            pm.append(box(f"pm_lionh{du}", 1.0, 1.0, 1.1, (-238 + du, -300.4, 2.9), ISTRIA))
        gt.append(join(pm, "porta_magna"))
    else:
        gt.append(gatehouse("ar_gate", 12, 8, 10, (-238, -296, 0), "S", BRICK_V, ISTRIA, "roman"))
    m.add(1, join(gt, "ar_gates"), "gates")

    # covered slipways and stores
    sh = []
    for k, x in enumerate((-238, -217, -196, -175, -154)):
        sh.append(squero(f"tv{k}", x, -125, 18, 46, 9, 0, hull=k % 2 == 0, roof=TILE))
        sh[-1] = rot_y_flip(sh[-1], x, -125)
    for k, y in enumerate((-238, -217, -196, -175)):
        sh.append(squero(f"tvw{k}", -262, y + 12, 16, 22, 8, 90, hull=False))
    if mid:
        for k, x in enumerate((-96, -74, -52, -30, 30, 52)):
            sh.append(squero(f"tns{k}", x, -248, 18, 30, 10, 180, hull=k % 2 == 1))
        for k, x in enumerate((-96, -74, -52, 30, 52)):
            sh.append(squero(f"tnn{k}", x, -14, 18, 44, 11, 0, hull=k % 3 == 0))
            sh[-1] = rot_y_flip(sh[-1], x, -14)
        tana_h = 9.5 if full else 7
        sh.append(box("tana", 316, 20, tana_h, (-12, -282, 0), BRICK_V))
        sh.append(roof_x("tana_r", 316, 20, 5, -12, -282, tana_h, TILE))
        sh.append(openings("tana_wn", 310, 52, 1.4, 3.0, -12, -271.95, 3.0, 90, "round", DARK, 0.3))
        sh.append(openings("tana_ws", 310, 52, 1.4, 3.0, -12, -292.05, 3.0, -90, "round", DARK, 0.3))
    if full:
        for k in range(14):
            x = -190 + k * 23
            if abs(x + 100) < 16:
                continue
            sh.append(squero(f"tnv{k}", x, 236, 20, 60, 13, 0, hull=k % 3 == 1))
            sh[-1] = rot_y_flip(sh[-1], x, 236)
        for k, x in enumerate((122, 146, 170, 194, 218, 242)):
            sh.append(squero(f"tg{k}", x, 72, 20, 52, 13, 0, hull=k % 2 == 0))
            sh[-1] = rot_y_flip(sh[-1], x, 72)
        for k, y in enumerate((-140, -110, -80, -50, -20, 10)):
            sh.append(squero(f"tge{k}", 265, y, 18, 22, 10, -90, hull=False))
        sh.append(range_block("ar_store1", 160, -230, 120, 20, 12, BRICK_V, TILE, 2, ("N",), "round"))
        sh.append(range_block("ar_store2", -200, 20, 140, 16, 11, BRICK_V, TILE, 2, ("S",), "round"))
        sh.append(range_block("ar_bucintoro_house", -170, -100, 44, 16, 12, BRICK_V, TILE, 1, ("S",), "round"))
    m.add(2, join(sh, "ar_sheds"), "slipways")

    boats = [galley("ar_g1", 40, -200, -200, 0, 0.35, True), galley("ar_g2", 38, -180, -175, 0, 0.35, False)]
    if mid:
        boats += [galley("ar_g3", 42, -30, -150, 15, 0.35, True), galley("ar_g4", 40, 20, -100, -10, 0.35, False), galley("ar_g5", 40, -60, -90, 0, 0.35, False)]
    if full:
        boats += [galley("ar_g6", 52, -60, 120, 0, 0.35, True, "#5E3E2A", RED_CLOTH), galley("ar_g7", 52, 60, 150, 180, 0.35, False, "#5E3E2A"),
                  galley("ar_g8", 44, 170, -40, 90, 0.35, True), galley("ar_g9", 44, 200, -90, 90, 0.35, False)]
    m.add(3, join(boats, "ar_galleys"), "galleys")
    return m


def rot_y_flip(o, x, y):
    """Turn a slipway built facing -Y so that it opens to the south basin instead of the north (half a turn about its own centre)."""
    o = move(o, -x, -y, 0)
    o = rot(o, 180)
    return move(o, x, y, 0)


# ---------------------------------------------------------------- Fondaco, Ca' d'Oro
def fondaco(variant="1508"):
    m = Model("fondaco")
    new = variant == "1508"
    S, H = 48.0, (20.0 if new else 14.0)
    wall = FRESCO if new else BRICK_V
    m.add(0, plate(48, 48, PAVE_V, 0.25), "ground")
    m.add(0, courtyard_ring("fd_ring", S, S, H, 14, (0, 0, 0), wall, DARK, True), "walls")
    f = []
    storeys = 4 if new else 3
    sh = H / storeys
    f.append(arcade_open("fd_portico", 26, 5, sh * 1.15, 0, -24, 0, -90, ISTRIA, "round", 0.5, 4, None, ISTRIA, DARK, True))
    for face, (fx, fy, deg) in {"S": (0, -24.05, -90), "N": (0, 24.05, 90), "E": (24.05, 0, 0), "W": (-24.05, 0, 180)}.items():
        for s in range(1 if face == "S" else 0, storeys):
            n = 16 if new else 12
            f.append(openings(f"fd_w{face}{s}", S * 0.9, n, 1.1, sh * 0.5, fx, fy, sh * s + sh * 0.25, deg, "round" if new else "pointed", DARK, 0.3))
        f.append(merli(f"fd_m{face}", S, fx, fy, H, deg, 1.0, ISTRIA))
    for s in range(1, storeys):
        for face, (fx, fy, deg) in {"S": (0, -10.05 + 0.1, 90), "N": (0, 10.05 - 0.1, -90), "E": (9.95, 0, 180), "W": (-9.95, 0, 0)}.items():
            f.append(openings(f"fd_cw{face}{s}", 18, 5, 2.2, sh * 0.62, fx, fy, sh * s + sh * 0.1, deg, "round", DARK, 0.25))
    if new:
        for k, (px, py) in enumerate(((-17, -30), (-5, -30), (8, -30), (19, -30))):
            pass
        for k in range(6):
            f.append(on_wall(box(f"fd_fresco{k}", 4.5, 0.15, 2.4, (0, 0, 0), ("#B37A5C", "#C0A07A", "#A8735E")[k % 3]), -20 + k * 8, -24.12, sh * 3 + 0.6, -90))
    m.add(1, join(f, "fd_facades"), "facades")
    r = []
    for face, (cx, cy, w, d) in {"S": (0, -17, 48, 14), "N": (0, 17, 48, 14), "E": (17, 0, 14, 20), "W": (-17, 0, 14, 20)}.items():
        r.append(hip(f"fd_r{face}", w, d, 3.6, cx, cy, H, TILE, 0.7, 0.0))
    for sx in (-1, 1):
        tz = H
        th = 6 if new else 9
        r.append(box(f"fd_turret{sx}", 6, 6, th, (sx * 20.5, -20.5, tz), wall))
        r.append(merli_ring(f"fd_tm{sx}", 6, 6, tz + th, 0.8, ISTRIA, sx * 20.5, -20.5))
        if new:
            r.append(hip(f"fd_tr{sx}", 6, 6, 3, sx * 20.5, -20.5, tz + th, TILE, 0.1))
    for k in range(5):
        r.append(chimney(f"fd_ch{k}", -18 + k * 9, 18, H + 1.5))
    m.add(2, join(r, "fd_roofs"), "roofs")
    return m


def ca_doro():
    m = Model("ca-doro")
    m.add(0, plate(26, 40, PAVE_V, 0.25), "ground")
    body = [box("cd_body", 26, 22, 18, (0, -9, 0), PLAST_V),
            box("cd_back", 11, 18, 12, (-7.5, 11, 0), PLAST_V),
            box("cd_cwall", 15, 0.6, 4.5, (5.5, 19.7, 0), PLAST_V),
            box("cd_cwall2", 0.6, 18, 4.5, (12.7, 11, 0), PLAST_V),
            box("cd_well", 1.6, 1.6, 1.1, (6, 10, 0.25), ROSSO),
            hip("cd_roof", 26, 22, 4.0, 0, -9, 18, TILE),
            roof_y("cd_backr", 11, 18, 3.5, -7.5, 11, 12, TILE),
            chimney("cd_ch1", -9, -2, 20, 0.5, 3.0), chimney("cd_ch2", 8, -4, 20, 0.5, 3.0)]
    m.add(0, join(body, "cd_body"), "walls")
    fy = -20.0
    f = []
    # left: the open loggias; right: the solid wall clad in marble
    lx, lw = -4.75, 16.5
    f.append(arcade_open("cd_water", lw, 5, 6.0, lx, fy, 0, -90, ISTRIA, "pointed", 0.4, 3.5, None, ISTRIA))
    f.append(opening("cd_bigarch", 4.4, 5.8, lx, fy - 0.3, 0, -90, "round", DARK, 0.3))
    for k, (z, h, n) in enumerate(((6.6, 4.6, 6), (12.2, 4.0, 6))):
        f.append(arcade_open(f"cd_log{k}", lw - 1.2, n, h, lx + 0.6, fy, z, -90, ISTRIA, "ogee", 0.22, 2.5, h * 0.55, ISTRIA))
        f.append(quatrefoils(f"cd_qf{k}", lw - 2.0, n, 0.55, lx + 0.6, fy - 0.1, z + h - 0.55, -90, DARK, 0.2))
        f.append(box(f"cd_balc{k}", lw - 0.6, 0.7, 0.8, (lx + 0.3, fy - 0.3, z), ISTRIA))
        f.append(box(f"cd_gilt{k}", lw - 1.2, 0.3, 0.25, (lx + 0.6, fy - 0.35, z + h - 0.1), GOLD))
    f.append(box("cd_marble", 9.0, 0.3, 17.0, (8.5, fy - 0.1, 0.5), "#D8B8A4"))
    for z in (7.2, 12.6):
        f.append(openings(f"cd_rw{z}", 7, 2, 1.3, 3.4, 8.5, fy - 0.3, z, -90, "pointed", DARK, 0.25))
    f.append(opening("cd_rdoor", 2.2, 3.8, 8.5, fy - 0.3, 0.3, -90, "pointed", DARK, 0.25))
    f.append(box("cd_rope", 0.5, 0.6, 18, (12.75, fy + 0.05, 0), ISTRIA))
    f.append(box("cd_rope2", 0.4, 0.6, 18, (4.0, fy + 0.05, 0), ISTRIA))
    f.append(merli("cd_crest", 26, 0, fy - 0.05, 18, -90, 0.75, ISTRIA, 0.25, 0.35))
    for k in range(9):
        f.append(dome(f"cd_ball{k}", 0.22, (-12 + k * 3, fy, 19.2), GOLD, segments=8, rings=4))
    m.add(1, join(f, "cd_facade"), "facade")
    return m


# ---------------------------------------------------------------- brick Gothic friars' churches
def brick_church(name, L, nave_w, nave_h, aisle_w, aisle_h, tr_y, tr_d, tr_w, choir_d, apse_r, color=BRICK_V, roof=TILE, bays=7):
    """A Venetian friars' church facing south: nave and aisles, transept, choir and polygonal apses, lancet windows, tripartite brick front."""
    front = -L / 2
    nave_y1 = tr_y - tr_d / 2
    nave_len = nave_y1 - front
    ncy = (front + nave_y1) / 2
    W = nave_w + 2 * aisle_w
    walls = [box(name + "_nave", nave_w, nave_len, nave_h, (0, ncy, 0), color)]
    roofs = [roof_y(name + "_nr", nave_w, nave_len, nave_w * 0.42, 0, ncy, nave_h, roof, 0.4)]
    for s in (-1, 1):
        ax = s * (nave_w / 2 + aisle_w / 2)
        walls.append(box(f"{name}_aisle{s}", aisle_w, nave_len, aisle_h, (ax, ncy, 0), color))
        roofs.append(lean_to(f"{name}_ar{s}", s * W / 2, s * nave_w / 2, front, nave_y1, aisle_h, aisle_h + 3.2, roof) if s > 0 else
                     lean_to(f"{name}_ar{s}", s * W / 2, s * nave_w / 2, front, nave_y1, aisle_h, aisle_h + 3.2, roof))
        walls.append(openings(f"{name}_aw{s}", nave_len * 0.9, bays, 1.6, aisle_h * 0.55, s * (W / 2 + 0.05), ncy, aisle_h * 0.25, 0 if s > 0 else 180, "pointed", DARK, 0.3))
        walls.append(openings(f"{name}_cw{s}", nave_len * 0.9, bays, 1.4, (nave_h - aisle_h) * 0.5, s * (nave_w / 2 + 0.05), ncy, aisle_h + 3.6, 0 if s > 0 else 180, "round", DARK, 0.3))
        for k in range(bays + 1):
            by = front + 2 + (nave_len - 4) * k / bays
            walls.append(box(f"{name}_bt{s}{k}", 1.2, 1.4, aisle_h * 0.9, (s * (W / 2 + 0.6), by, 0), shade(color, -0.06)))
    walls.append(box(name + "_tr", tr_w, tr_d, nave_h * 0.92, (0, tr_y, 0), color))
    roofs.append(roof_x(name + "_trr", tr_w, tr_d, tr_d * 0.42, 0, tr_y, nave_h * 0.92, roof, 0.4))
    for s in (-1, 1):
        walls.append(opening(f"{name}_trw{s}", 3.0, nave_h * 0.5, s * (tr_w / 2 + 0.05), tr_y, nave_h * 0.25, 0 if s > 0 else 180, "pointed", DARK, 0.3))
        walls.append(disc(f"{name}_tro{s}", 1.6, s * (tr_w / 2 + 0.05), tr_y, nave_h * 0.82, 0 if s > 0 else 180, DARK, 0.3, 14))
    cy0 = tr_y + tr_d / 2
    walls.append(box(name + "_choir", nave_w, choir_d, nave_h * 0.92, (0, cy0 + choir_d / 2, 0), color))
    roofs.append(roof_y(name + "_cr", nave_w, choir_d, nave_w * 0.42, 0, cy0 + choir_d / 2, nave_h * 0.92, roof, 0.3))

    def apse(nm, r, x, y, h, rf=roof):
        pts = [(x + r * math.cos(math.radians(a)), y + r * math.sin(math.radians(a))) for a in range(0, 181, 30)]
        o = [prism(nm + "_b", pts, h, (0, 0, 0), color)]
        for k in range(6):
            a = math.radians(15 + 30 * k)
            o.append(opening(f"{nm}_w{k}", r * 0.32, h * 0.6, x + r * 0.97 * math.cos(a), y + r * 0.97 * math.sin(a), h * 0.2, math.degrees(a), "pointed", DARK, 0.3))
        top = [(x + r * 1.05 * math.cos(math.radians(a)), y + r * 1.05 * math.sin(math.radians(a))) for a in range(0, 181, 30)]
        o.append(prism(nm + "_rb", top, 0.4, (0, 0, h), rf))
        o.append(cylinder(nm + "_cone", r * 1.0, r * 0.7, (x, y, h), rf, verts=12, r_top=0.2))
        return join(o, nm)

    walls.append(apse(name + "_apse", apse_r, 0, cy0 + choir_d, nave_h * 0.88))
    for s in (-1, 1):
        for k, off in enumerate((nave_w / 2 + 3.5, nave_w / 2 + 9.5)):
            if off + 3 < tr_w / 2 + 0.5:
                walls.append(apse(f"{name}_ch{s}{k}", 3.0, s * off, cy0, nave_h * 0.5))
    # tripartite front with pinnacles, portal and round windows
    pts = [(-W / 2, 0), (W / 2, 0), (W / 2, aisle_h + 2), (nave_w / 2, aisle_h + 5.5), (nave_w / 2, nave_h + 1), (0, nave_h + nave_w * 0.45), (-nave_w / 2, nave_h + 1), (-nave_w / 2, aisle_h + 5.5), (-W / 2, aisle_h + 2)]
    fr = [on_wall(multi_slab(name + "_front", [pts], 1.6, color), 0, front - 0.3, 0, -90)]
    fr.append(on_wall(box(name + "_portal", 6.5, 0.8, 10.5, (0, 0, 0), ISTRIA), 0, front - 1.2, 0, -90))
    fr.append(opening(name + "_door", 3.6, 7.5, 0, front - 1.65, 0, -90, "pointed", DARK, 0.3))
    fr.append(opening(name + "_lunette", 5.6, 4.2, 0, front - 1.7, 9.0, -90, "ogee", ISTRIA, 0.3))
    fr.append(disc(name + "_rose", 2.6, 0, front - 1.15, nave_h * 0.78, -90, DARK, 0.3, 18))
    fr.append(disc(name + "_roser", 3.1, 0, front - 1.05, nave_h * 0.78, -90, ISTRIA, 0.25, 18))
    for s in (-1, 1):
        fr.append(disc(f"{name}_sr{s}", 1.4, s * (nave_w / 2 + aisle_w / 2), front - 1.15, aisle_h * 0.65, -90, DARK, 0.3, 14))
        fr.append(on_wall(box(f"{name}_pil{s}", 1.0, 0.5, nave_h + 1, (0, 0, 0), shade(color, -0.07)), s * nave_w / 2, front - 1.2, 0, -90))
        fr.append(pinnacle(f"{name}_fp{s}", s * nave_w / 2, front - 0.3, nave_h + 1, 1.2, 5.5, ISTRIA, ISTRIA, True))
        fr.append(pinnacle(f"{name}_fq{s}", s * W / 2, front - 0.3, aisle_h + 2, 1.0, 4.0, ISTRIA, ISTRIA, False))
    fr.append(pinnacle(name + "_fa", 0, front - 0.3, nave_h + nave_w * 0.45, 1.3, 5.0, ISTRIA, ISTRIA, True))
    return join(walls, name + "_walls"), join(roofs, name + "_roofs"), join(fr, name + "_front")


def zanipolo():
    m = Model("zanipolo")
    m.add(0, plate(46, 101, PAVE_V, 0.25), "ground")
    w, r, f = brick_church("zp", 100, 15, 30, 8, 18, 22, 14, 44, 12, 7.5, BRICK_V, TILE, 7)
    m.add(0, w, "walls")
    m.add(1, join([r, f], "zp_rf"), "roofs")
    m.add(2, classical_dome("zp_dome", 6.4, 0, 22, 30, 4.5, LEAD_V, BRICK_V, 8, 1.15, ISTRIA, False), "dome")
    return m


def frari():
    m = Model("frari")
    m.add(0, plate(48, 102, PAVE_V, 0.25), "ground")
    w, r, f = brick_church("fr", 100, 15, 28, 9, 17, 24, 12, 40, 12, 7.5, "#B66A4C", TILE, 7)
    m.add(0, w, "walls")
    m.add(1, join([r, f], "fr_rf"), "roofs")
    cx, cy = 19.0, 34.0
    tw = [venetian_campanile("fr_camp", 9, cx, cy, 52, "old", "#A85F44")]
    tw.append(cylinder("fr_oct", 4.0, 5.5, (cx, cy, 52 + 6.75 + 0.7 + 0.1), "#A85F44", verts=8))
    m.add(2, join(tw, "fr_tower"), "campanile")
    return m


# ---------------------------------------------------------------- Palladio and Longhena
def san_giorgio(variant="full"):
    if variant == "old":
        return san_giorgio_old()
    m = Model("san-giorgio")
    m.add(0, plate(52, 96, PAVE_L, 0.25), "ground")
    body = "#E9E1D2"
    w = [box("sgm_nave", 16, 50, 24, (0, -21, 0), body)]
    for s in (-1, 1):
        w.append(box(f"sgm_aisle{s}", 9, 50, 14, (s * 12.5, -21, 0), body))
        w.append(openings(f"sgm_aw{s}", 44, 5, 2.0, 5.5, s * 17.05, -21, 5, 0 if s > 0 else 180, "round", DARK, 0.3))
        w.append(opening(f"sgm_therm{s}", 6, 3.5, s * 8.05, -21, 17, 0 if s > 0 else 180, "round", DARK, 0.3))
    w.append(box("sgm_cross", 30, 18, 24, (0, 13, 0), body))
    for s in (-1, 1):
        w.append(cylinder(f"sgm_tapse{s}", 7, 20, (s * 15, 13, 0), body, verts=20))
    w.append(box("sgm_pres", 16, 14, 22, (0, 29, 0), body))
    w.append(box("sgm_monks", 14, 10, 18, (0, 41, 0), body))
    w.append(cylinder("sgm_mapse", 7, 18, (0, 45.5, 0), body, verts=16))
    m.add(0, join(w, "sgm_walls"), "walls")
    r = [roof_y("sgm_nr", 16, 50, 6, 0, -21, 24, LEAD_V, 0.3),
         lean_to("sgm_ar1", 17, 8, -46, 4, 14, 17, LEAD_V), lean_to("sgm_ar2", -17, -8, -46, 4, 14, 17, LEAD_V),
         roof_x("sgm_cr", 30, 18, 6, 0, 13, 24, LEAD_V, 0.3),
         roof_y("sgm_pr", 16, 14, 5.5, 0, 29, 22, LEAD_V, 0.3),
         roof_y("sgm_mr", 14, 10, 4.5, 0, 41, 18, LEAD_V, 0.3),
         dome("sgm_mad", 7, (0, 45.5, 18), LEAD_V, squash=0.6, segments=16, rings=5)]
    for s in (-1, 1):
        r.append(dome(f"sgm_tad{s}", 7, (s * 15, 13, 20), LEAD_V, squash=0.6, segments=16, rings=5))
    if variant == "full":
        fr = [classical_front("sgm_front", 17, 31, 0, -46.05, 0, -90, 4, 0.95, 5.5, ISTRIA, None, True, True)]
        for s in (-1, 1):
            fr.append(on_wall(multi_slab(f"sgm_half{s}", [[(0, 15), (s * 9.5, 15), (s * 9.5, 17.2), (0, 20.5)]], 1.6, ISTRIA), s * 8.5, -46.0, 0, -90))
            fr.append(on_wall(box(f"sgm_sidewall{s}", 9, 0.6, 15, (0, 0, 0), ISTRIA), s * 12.5, -46.4, 0, -90))
            fr.append(statue(f"sgm_niche{s}", s * 4.2, -47.4, 6.5, 2.6, ISTRIA))
            fr.append(opening(f"sgm_nichep{s}", 2.0, 3.8, s * 4.2, -46.5, 6.2, -90, "round", "#C9C2B2", 0.2))
            for k in (-1, 1):
                fr.append(box(f"sgm_spil{s}{k}", 1.0, 0.8, 13.5, (s * (12.5 + k * 3.6), -47.0, 0), ISTRIA))
        m.add(1, join(r + fr, "sgm_roofs"), "roofs")
    else:
        fr = [on_wall(multi_slab("sgm_rough", [[(-17, 0), (17, 0), (17, 14), (8, 17), (8, 24), (0, 30), (-8, 24), (-8, 17), (-17, 14)]], 1.2, BRICK_V), 0, -46.3, 0, -90),
              opening("sgm_rdoor", 4, 8, 0, -46.95, 0, -90, "flat", DARK, 0.3)]
        for k in range(6):
            fr.append(cylinder(f"sgm_scaf{k}", 0.15, 26, (-15 + k * 6, -48, 0), TIMBER_V, verts=4))
        for z in (8, 16, 24):
            fr.append(box(f"sgm_scafb{z}", 32, 0.3, 0.3, (0, -48, z), TIMBER_V))
        m.add(1, join(r + fr, "sgm_roofs"), "roofs")
    d = [classical_dome("sgm_dome", 7.5, 0, 13, 24, 6.0, LEAD_V, ISTRIA, 12, 1.0, ISTRIA, True)]
    if variant == "1580":
        d.append(venetian_campanile("sgm_camp", 7, 14, 40, 38, "old", BRICK_V))
    else:
        d.append(box("sgm_stump", 7, 7, 12, (14, 40, 0), BRICK_V))
        for k in range(4):
            d.append(cylinder(f"sgm_cs{k}", 0.12, 16, (14 + (-3.8 if k < 2 else 3.8), 40 + (-3.8 if k % 2 else 3.8), 0), TIMBER_V, verts=4))
        d.append(box("sgm_crane", 0.3, 0.3, 8, (14, 40, 16), TIMBER_V))
    m.add(2, join(d, "sgm_dome"), "dome")
    return m


def san_giorgio_old():
    m = Model("san-giorgio-old")
    m.add(0, plate(52, 96, "#B9AE8C", 0.25), "ground")
    w = [box("sgo_nave", 12, 54, 16, (-6, -12, 0), BRICK_V)]
    for s in (-1, 1):
        w.append(box(f"sgo_aisle{s}", 6, 54, 9, (-6 + s * 9, -12, 0), BRICK_V))
        w.append(openings(f"sgo_aw{s}", 48, 8, 1.0, 3.0, -6 + s * 12.05, -12, 4, 0 if s > 0 else 180, "round", DARK, 0.2))
    w.append(cylinder("sgo_apse", 6, 14, (-6, 15, 0), BRICK_V, verts=14))
    w.append(box("sgo_porch", 24, 5, 6, (-6, -41.5, 0), PLAST_V))
    w.append(arcade_open("sgo_porcharc", 24, 6, 5.5, -6, -44, 0, -90, PLAST_V, "round", 0.35, 4.0, None, ISTRIA, DARK))
    w.append(disc("sgo_rose", 2.0, -6, -39.1, 12, -90, DARK, 0.3, 14))
    w.append(courtyard_ring("sgo_cloister", 22, 26, 8, 5, (14, 10, 0), PLAST_V, DARK, True))
    m.add(0, join(w, "sgo_walls"), "walls")
    r = [roof_y("sgo_nr", 12, 54, 5, -6, -12, 16, TILE),
         lean_to("sgo_ar1", 6, 0, -39, 15, 9, 11.5, TILE), lean_to("sgo_ar2", -18, -12, -39, 15, 9, 11.5, TILE),
         dome("sgo_ad", 6, (-6, 15, 14), TILE, squash=0.6, segments=14, rings=5),
         lean_to("sgo_porr", -18, 6, -44, -39, 6, 6, TILE)]
    for (cx, cy, ww, dd) in ((14, -3 + 2.5 - 5.5, 22, 5), (14, 23 - 2.5 + 2.5, 22, 5)):
        pass
    r.append(roof_x("sgo_clr1", 22, 5, 2.2, 14, -0.5, 8, TILE))
    r.append(roof_x("sgo_clr2", 22, 5, 2.2, 14, 20.5, 8, TILE))
    r.append(roof_y("sgo_clr3", 5, 16, 2.2, 5.5, 10, 8, TILE))
    r.append(roof_y("sgo_clr4", 5, 16, 2.2, 22.5, 10, 8, TILE))
    m.add(1, join(r, "sgo_roofs"), "roofs")
    m.add(2, venetian_campanile("sgo_camp", 6.5, 16, -26, 34, "old", BRICK_V), "campanile")
    return m


def redentore(variant="full"):
    m = Model("redentore")
    m.add(0, plate(40, 76, PAVE_L, 0.25), "ground")
    body = "#ECE4D6"
    if variant == "1580":
        w = [box("rd_nave", 18, 40, 9, (0, -12, 0), BRICK_V)]
        for s in (-1, 1):
            w.append(box(f"rd_ch{s}", 5, 40, 7, (s * 11.5, -12, 0), BRICK_V))
        w.append(box("rd_cross", 30, 20, 6, (0, 18, 0), BRICK_V))
        w.append(stair("rd_stair", 22, 3, 6, 15, (0, -35, 0), "S", ISTRIA_D))
        m.add(0, join(w, "rd_walls"), "walls")
        sc = []
        for k in range(8):
            for y in (-33, 9):
                sc.append(cylinder(f"rd_sc{k}{y}", 0.15, 16, (-14 + k * 4, y, 0), TIMBER_V, verts=4))
        for z in (5, 10, 15):
            for y in (-33, 9):
                sc.append(box(f"rd_scb{z}{y}", 30, 0.3, 0.3, (0, y, z), TIMBER_V))
        sc.append(box("rd_crane", 1.2, 1.2, 22, (14, 0, 0), TIMBER_V))
        sc.append(box("rd_jib", 14, 0.5, 0.5, (8, 0, 21), TIMBER_V))
        for k in range(5):
            sc.append(box(f"rd_stone{k}", 3, 2, 1.2, (-12 + k * 6, 30, 0.25), ISTRIA))
        m.add(1, join(sc, "rd_scaffold"), "scaffolding")
        return m
    w = [box("rd_nave", 16, 40, 22, (0, -12, 0), body)]
    for s in (-1, 1):
        w.append(box(f"rd_ch{s}", 6, 40, 13, (s * 11, -12, 0), body))
        w.append(openings(f"rd_chw{s}", 36, 3, 3.0, 4.0, s * 14.05, -12, 4, 0 if s > 0 else 180, "round", DARK, 0.3))
        w.append(opening(f"rd_therm{s}", 6, 3.5, s * 8.05, -12, 16, 0 if s > 0 else 180, "round", DARK, 0.3))
    w.append(box("rd_cross", 30, 20, 22, (0, 18, 0), body))
    for s in (-1, 1):
        w.append(cylinder(f"rd_apse{s}", 7, 18, (s * 15, 18, 0), body, verts=20))
    w.append(box("rd_choir", 16, 8, 16, (0, 32, 0), body))
    w.append(cylinder("rd_capse", 7.8, 16, (0, 33, 0), body, verts=18))
    w.append(stair("rd_stair", 22, 3, 6, 15, (0, -35, 0), "S", ISTRIA_D))
    m.add(0, join(w, "rd_walls"), "walls")
    fr = [move(classical_front("rd_front", 16, 30, 0, 0, 0, -90, 4, 0.85, 0.0, ISTRIA, None, True, True, 4.0), 0, -32.05, 3)]
    for s in (-1, 1):
        fr.append(on_wall(multi_slab(f"rd_half{s}", [[(0, 13), (s * 7, 13), (s * 7, 15), (0, 19)]], 1.4, ISTRIA), s * 8, -32.0, 3, -90))
        fr.append(on_wall(box(f"rd_sw{s}", 6, 0.6, 13, (0, 0, 0), ISTRIA), s * 11, -32.4, 3, -90))
    r = [roof_y("rd_nr", 16, 40, 6, 0, -12, 22, LEAD_V, 0.3),
         lean_to("rd_cr1", 14, 8, -32, 8, 13, 15, LEAD_V), lean_to("rd_cr2", -14, -8, -32, 8, 13, 15, LEAD_V),
         roof_x("rd_xr", 30, 20, 5, 0, 18, 22, LEAD_V, 0.3),
         dome("rd_cad", 7.8, (0, 33, 16), LEAD_V, squash=0.55, segments=16, rings=5)]
    for s in (-1, 1):
        r.append(dome(f"rd_ad{s}", 7, (s * 15, 18, 18), LEAD_V, squash=0.55, segments=16, rings=5))
    m.add(1, join(fr + r, "rd_front"), "front")
    d = [classical_dome("rd_dome", 8.0, 0, 18, 22, 7.0, LEAD_V, body, 12, 1.0, ISTRIA, True)]
    for s in (-1, 1):
        x, y = s * 7.5, 29.5
        d.append(cylinder(f"rd_tw{s}", 2.0, 31, (x, y, 0), body, verts=16))
        d.append(openings(f"rd_tww{s}", 2.6, 1, 1.0, 3.0, x, y - 2.0, 25, -90, "round", DARK, 0.2))
        d.append(cylinder(f"rd_twc{s}", 2.3, 0.6, (x, y, 31), ISTRIA, verts=16))
        d.append(cylinder(f"rd_twt{s}", 1.9, 4.5, (x, y, 31.6), LEAD_V, verts=16, r_top=0.15))
        d.append(dome(f"rd_twb{s}", 0.4, (x, y, 36.1), GOLD, segments=8, rings=4))
    m.add(2, join(d, "rd_dome"), "dome")
    return m


def salute():
    m = Model("salute")
    m.add(0, plate(65, 95, PAVE_L, 0.25), "ground")
    cy = -12.0
    R, H = 22.0, 20.0
    oct_pts = [(R * math.cos(math.radians(22.5 + 45 * k)), cy + R * math.sin(math.radians(22.5 + 45 * k))) for k in range(8)]
    w = [stair("sa_steps", 26, 3.2, 7, 12, (0, -40.5, 0), "S", ISTRIA_D),
         box("sa_podium", 50, 8, 0.8, (0, cy - R * 0.92 - 1, 0), ISTRIA_D)]
    w.append(prism("sa_oct", oct_pts, H, (0, 0, 0), ISTRIA))
    # six chapels with their pediments
    for k in range(8):
        a = 45 * k
        if a in (270, 90):
            continue
        rad = math.radians(a)
        fx, fy = (R * 0.924 + 2.0) * math.cos(rad), cy + (R * 0.924 + 2.0) * math.sin(rad)
        ch = box(f"sa_chap{k}", 11, 4.2, 15, (0, 0, 0), ISTRIA)
        w.append(place(ch, a - 90 + 180, fx, fy, 0) if False else on_wall(ch, fx, fy, 0, a))
        ox, oy = (R * 0.924 + 4.15) * math.cos(rad), cy + (R * 0.924 + 4.15) * math.sin(rad)
        w.append(pediment(f"sa_cped{k}", 11.8, 3.0, ox, oy, 15, a, ISTRIA, 0.8))
        w.append(opening(f"sa_cwin{k}", 4.0, 2.4, ox + 0.05 * math.cos(rad), oy + 0.05 * math.sin(rad), 10.5, a, "round", DARK, 0.3))
        for du in (-4.4, 4.4):
            px = ox + du * -math.sin(rad)
            py = oy + du * math.cos(rad)
            w.append(cylinder(f"sa_cc{k}{du}", 0.5, 14.2, (px, py, 0), ISTRIA, verts=10))
            w.append(statue(f"sa_cs{k}{du}", px, py, 18, 1.8, ISTRIA))
    for k in range(8):
        a = math.radians(22.5 + 45 * k)
        px, py = R * math.cos(a), cy + R * math.sin(a)
        for du in (-1.2, 1.2):
            qx, qy = px + du * -math.sin(a), py + du * math.cos(a)
            w.append(cylinder(f"sa_pil{k}{du}", 0.55, H - 1.0, (qx, qy, 0.8), ISTRIA_D, verts=12))
        w.append(statue(f"sa_ost{k}", px, py, H + 0.6, 2.4, ISTRIA))
    bal = []
    for k in range(8):
        a0, a1 = math.radians(22.5 + 45 * k), math.radians(22.5 + 45 * (k + 1))
        for j in range(11):
            t = (j + 0.5) / 11
            bx = R * 0.99 * ((1 - t) * math.cos(a0) + t * math.cos(a1))
            by = cy + R * 0.99 * ((1 - t) * math.sin(a0) + t * math.sin(a1))
            bal.append(cylinder(f"sa_bal{k}_{j}", 0.22, 1.0, (bx, by, H), ISTRIA, verts=6))
    w.append(join(bal, "sa_balusters"))
    w.append(lathe("sa_corn", [(R * 1.0, 0), (R * 1.04, 0.3), (R * 1.04, 1.2), (R * 0.95, 1.4)], (0, cy, H - 1.4), ISTRIA_D, verts=8))
    # triumphal-arch entrance
    ent_y = cy - R * 0.924
    w.append(on_wall(box("sa_entb", 18, 2.4, 22, (0, 0, 0), ISTRIA), 0, ent_y - 1.2, 0, -90))
    w.append(opening("sa_entarch", 7.0, 13.5, 0, ent_y - 2.45, 0.8, -90, "round", DARK, 0.4))
    for du in (-7.2, -4.2, 4.2, 7.2):
        w.append(box(f"sa_entped{du}", 2.2, 2.4, 3.0, (du, ent_y - 3.2, 0.8), ISTRIA))
        w.append(cylinder(f"sa_entc{du}", 0.8, 15.5, (du, ent_y - 3.2, 3.8), ISTRIA, verts=14))
        w.append(statue(f"sa_ents{du}", du, ent_y - 3.0, 22.5, 2.4, ISTRIA))
    w.append(box("sa_entent", 19, 3.2, 2.0, (0, ent_y - 2.6, 19.3), ISTRIA_D))
    w.append(pediment("sa_entped", 10, 3.0, 0, ent_y - 2.7, 21.3, -90, ISTRIA, 1.2))
    m.add(0, join(w, "sa_walls"), "walls")
    # ambulatory roof, volutes, drum, great dome
    up = [lathe("sa_ring", [(R * 0.9, 0), (R * 0.86, 0.6), (14.5, 3.2), (13.0, 3.4)], (0, cy, H), LEAD_V, verts=48)]
    for k in range(16):
        a = math.tau * k / 16
        rr = 15.6
        vx, vy = rr * math.cos(a), cy + rr * math.sin(a)
        for j, (vr, vt, vc, dz, dr) in enumerate(((2.9, 1.3, ISTRIA, 4.6, 0.0), (2.0, 1.6, ISTRIA_D, 4.1, 0.5), (1.1, 1.9, ISTRIA, 3.6, 0.9))):
            v = cylinder(f"sa_vol{k}_{j}", vr, vt, (0, 0, -vt / 2), vc, verts=28)
            apply_rot(v, rx=math.pi / 2)
            v = rot(v, math.degrees(a))
            up.append(move(v, (rr - dr) * math.cos(a), cy + (rr - dr) * math.sin(a), H + dz))
        up.append(statue(f"sa_vst{k}", (rr - 1.2) * math.cos(a), cy + (rr - 1.2) * math.sin(a), H + 7.3, 2.2, ISTRIA))
    m.add(1, join(up, "sa_volutes"), "volutes")
    d = [classical_dome("sa_dome", 13.0, 0, cy, H + 3.2, 10.5, LEAD_V, ISTRIA, 16, 1.12, ISTRIA, True, 72)]
    # sanctuary with its second dome and the two bell towers
    d.append(box("sa_pres", 30, 16, 21, (0, 17, 0), ISTRIA))
    d.append(classical_dome("sa_dome2", 7.0, 0, 17, 21, 4.5, LEAD_V, ISTRIA, 8, 1.0, ISTRIA, False, 40))
    d.append(box("sa_choir", 18, 12, 17, (0, 31, 0), ISTRIA))
    d.append(hip("sa_choirr", 18, 12, 3, 0, 31, 17, LEAD_V))
    for s in (-1, 1):
        x, y = s * 11.5, 36.0
        d.append(box(f"sa_tw{s}", 4.6, 4.6, 32, (x, y, 0), ISTRIA))
        d.append(openings(f"sa_tww{s}", 3.6, 1, 1.4, 3.6, x, y - 2.35, 26, -90, "round", DARK, 0.2))
        d.append(cylinder(f"sa_twl{s}", 2.0, 3.0, (x, y, 32), ISTRIA, verts=8))
        d.append(dome(f"sa_twd{s}", 2.1, (x, y, 35), LEAD_V, squash=1.2, segments=10, rings=5))
        d.append(box(f"sa_twx{s}", 0.2, 0.2, 2.0, (x, y, 37.4), GOLD))
    m.add(2, join(d, "sa_domes"), "domes")
    return m


# ---------------------------------------------------------------- the Ghetto
def ghetto():
    m = Model("ghetto")
    m.add(0, plate(100, 85, WATER_V, 0.2), "water")
    isl = [(-46, -38), (44, -40), (48, 10), (20, 40), (-44, 38)]
    m.add(0, prism("gh_island", isl, 0.5, (0, 0, 0), PAVE_V), "water")
    houses, roofs, wins = [], [], []
    cols = (PLAST_V, OCHRE, "#D9A58A", "#E8D6BC", "#C99070", "#DCC09A")
    k = 0
    n_pts = len(isl)
    cx0 = sum(p[0] for p in isl) / n_pts
    cy0 = sum(p[1] for p in isl) / n_pts
    for i in range(n_pts):
        (ax, ay), (bx, by) = isl[i], isl[(i + 1) % n_pts]
        L = math.hypot(bx - ax, by - ay)
        ang = math.degrees(math.atan2(by - ay, bx - ax))
        nx, ny = -(by - ay) / L, (bx - ax) / L
        if (cx0 - ax) * nx + (cy0 - ay) * ny < 0:
            nx, ny = -nx, -ny
        n = int(L / 7.5)
        for j in range(n):
            if (i == 0 and j == n // 2) or (i == 1 and j == n // 2):
                continue
            t = (j + 0.5) / n
            hw = L / n - 0.4
            depth = 11
            px = ax + (bx - ax) * t + nx * (depth / 2 + 1.0)
            py = ay + (by - ay) * t + ny * (depth / 2 + 1.0)
            h = 17 + ((k * 7) % 5) * 2.2
            col = cols[k % len(cols)]
            hb = box(f"gh_h{k}", hw, depth, h, (0, 0, 0), col)
            houses.append(place(hb, ang, px, py, 0.5))
            roofs.append(place(hip_roof(f"gh_r{k}", depth, hw, 1.8, (0, 0, 0), TILE, ridge=0.5, overhang=0.3), ang + 90, px, py, 0.5 + h))
            storeys = int(h / 2.55)
            polys = []
            for s in range(storeys):
                z = 0.9 + s * 2.55
                for wv in (-hw * 0.28, 0.0, hw * 0.28):
                    polys.append([(wv - 0.42, z), (wv + 0.42, z), (wv + 0.42, z + 1.35), (wv - 0.42, z + 1.35)])
            wo = multi_slab(f"gh_w{k}", polys, 0.2, DARK)
            in_deg = math.degrees(math.atan2(ny, nx))
            wins.append(on_wall(wo, px + nx * (depth / 2 + 0.05), py + ny * (depth / 2 + 0.05), 0.5, in_deg))
            polys2 = [p for idx, p in enumerate(polys) if idx % 6 in (0, 2)]
            wo2 = multi_slab(f"gh_wo{k}", polys2, 0.2, DARK)
            wins.append(on_wall(wo2, px - nx * (depth / 2 + 0.05), py - ny * (depth / 2 + 0.05), 0.5, in_deg + 180))
            if k % 3 == 0:
                roofs.append(chimney(f"gh_ch{k}", px, py, 0.5 + h + 1.0, 0.4, 2.2))
            k += 1
    m.add(1, join(houses + wins, "gh_houses"), "houses")
    extra = []
    for k2, (wx, wy) in enumerate(((-12, -2), (8, 6), (-2, 18))):
        extra.append(cylinder(f"gh_well{k2}", 1.0, 1.0, (wx, wy, 0.5), ISTRIA, verts=12))
        extra.append(cylinder(f"gh_wellc{k2}", 1.15, 0.2, (wx, wy, 1.5), ISTRIA_D, verts=12))
    # gates through the houses, a little bridge outside each
    for (gx, gy, deg) in ((-1, -39, -90), (46, -15, 0)):
        extra.append(opening(f"gh_gate{gx}", 3.0, 4.4, gx, gy, 0.5, deg, "round", DARK, 0.6))
        bx, by = gx + 4.5 * math.cos(math.radians(deg)), gy + 4.5 * math.sin(math.radians(deg))
        extra.append(place(box(f"gh_bridge{gx}", 4.0, 8.0, 0.8, (0, 0, 0), ISTRIA_D), deg + 90, bx, by, 0.6))
        for s in (-1, 1):
            px = gx - s * 2.2 * math.sin(math.radians(deg))
            py = gy + s * 2.2 * math.cos(math.radians(deg))
            extra.append(box(f"gh_gpost{gx}{s}", 0.8, 0.8, 5.2, (px, py, 0.5), ISTRIA))
    # Banco Rosso arcade, synagogue windows and the Scola Canton cupola
    extra.append(arcade_open("gh_banco", 10, 3, 3.6, -20, -27.0, 0.5, 90, ISTRIA, "round", 0.3, 1.5, None, ISTRIA, "#7A2E26", True))
    extra.append(openings("gh_scola", 7.5, 5, 0.9, 2.2, 8.5, -27.15, 18.2, 90, "round", ISTRIA, 0.3))
    extra.append(cylinder("gh_canton", 2.0, 2.2, (22, -36, 21.5), TIMBER_V, verts=8))
    extra.append(dome("gh_cantond", 2.1, (22, -36, 23.7), LEAD_V, segments=8, rings=4))
    m.add(2, join(roofs + extra, "gh_roofs"), "roofs")
    return m


# ---------------------------------------------------------------- San Pietro di Castello
def san_pietro(variant="full"):
    m = Model("san-pietro")
    m.add(0, plate(45, 80, PAVE_V, 0.25), "ground")
    if variant in ("old", "1580"):
        body = BRICK_V
        w = [box("sp_nave", 12, 52, 15, (-3, 8, 0), body)]
        for s in (-1, 1):
            w.append(box(f"sp_aisle{s}", 6, 52, 9, (-3 + s * 9, 8, 0), body))
            w.append(openings(f"sp_aw{s}", 46, 8, 1.0, 3.0, -3 + s * 12.05, 8, 4, 0 if s > 0 else 180, "round", DARK, 0.2))
        w.append(cylinder("sp_apse", 6, 13, (-3, 34, 0), body, verts=14))
        w.append(opening("sp_door", 3.0, 5, -3, -18.05, 0, -90, "round", DARK, 0.3))
        w.append(disc("sp_rose", 1.8, -3, -18.05, 11, -90, DARK, 0.3, 14))
        m.add(0, join(w, "sp_walls"), "walls")
        r = [roof_y("sp_nr", 12, 52, 5, -3, 8, 15, TILE),
             lean_to("sp_ar1", 9, 3, -18, 34, 9, 11.5, TILE), lean_to("sp_ar2", -15, -9, -18, 34, 9, 11.5, TILE),
             dome("sp_ad", 6, (-3, 34, 13), TILE, squash=0.6, segments=14, rings=5)]
        m.add(1, join(r, "sp_roofs"), "roofs")
        if variant == "old":
            m.add(2, venetian_campanile("sp_camp", 6, 15, -30, 30, "old", BRICK_V), "campanile")
        else:
            m.add(2, codussi_campanile(15, -30), "campanile")
        return m
    body = "#E9E1D2"
    w = [box("sp_nave", 18, 48, 20, (0, -4, 0), body)]
    for s in (-1, 1):
        w.append(box(f"sp_aisle{s}", 7, 48, 12, (s * 12.5, -4, 0), body))
        w.append(openings(f"sp_aw{s}", 42, 4, 2.0, 5.0, s * 16.05, -4, 4, 0 if s > 0 else 180, "round", DARK, 0.3))
    w.append(box("sp_tr", 36, 12, 20, (0, 26, 0), body))
    w.append(cylinder("sp_apse", 7, 17, (0, 32, 0), body, verts=16))
    m.add(0, join(w, "sp_walls"), "walls")
    fr = [classical_front("sp_front", 18, 26, 0, -28.05, 0, -90, 4, 0.8, 3.0, ISTRIA, None, True, True)]
    for s in (-1, 1):
        fr.append(on_wall(multi_slab(f"sp_half{s}", [[(0, 12), (s * 7.5, 12), (s * 7.5, 13.6), (0, 16.5)]], 1.4, ISTRIA), s * 9, -28.0, 0, -90))
        fr.append(on_wall(box(f"sp_sw{s}", 7, 0.6, 12, (0, 0, 0), ISTRIA), s * 12.5, -28.4, 0, -90))
    r = [roof_y("sp_nr", 18, 48, 6, 0, -4, 20, LEAD_V, 0.3),
         lean_to("sp_ar1", 16, 9, -28, 20, 12, 14.5, LEAD_V), lean_to("sp_ar2", -16, -9, -28, 20, 12, 14.5, LEAD_V),
         roof_x("sp_trr", 36, 12, 5, 0, 26, 20, LEAD_V, 0.3),
         dome("sp_ad", 7, (0, 32, 17), LEAD_V, squash=0.55, segments=14, rings=5),
         classical_dome("sp_dome", 6.0, 0, 26, 20, 4.0, LEAD_V, body, 8, 0.95, ISTRIA, False)]
    m.add(1, join(fr + r, "sp_front"), "front")
    m.add(2, codussi_campanile(16, -33), "campanile")
    return m


def codussi_campanile(x, y):
    w = 6.5
    parts = [box("cod_shaft", w, w, 30, (x, y, 0), ISTRIA)]
    for f, (nx, ny) in {"S": (0, -1), "N": (0, 1), "E": (1, 0), "W": (-1, 0)}.items():
        deg = {"S": -90, "N": 90, "E": 0, "W": 180}[f]
        for k in (-1, 1):
            px, py = (x + k * w * 0.35, y + ny * (w / 2 + 0.1)) if ny else (x + nx * (w / 2 + 0.1), y + k * w * 0.35)
            parts.append(box(f"cod_pil{f}{k}", 0.6 if ny else 0.3, 0.3 if ny else 0.6, 29, (px, py, 0), ISTRIA_D))
        parts.append(openings(f"cod_bel{f}", w * 0.8, 2, 1.4, 4.2, x + nx * (w / 2 + 0.05), y + ny * (w / 2 + 0.05), 24, deg, "round", DARK, 0.3))
    parts.append(box("cod_corn", w + 0.6, w + 0.6, 0.6, (x, y, 30), ISTRIA_D))
    parts.append(cylinder("cod_oct", w * 0.48, 4.0, (x, y, 30.6), ISTRIA, verts=8))
    parts.append(dome("cod_dome", w * 0.5, (x, y, 34.6), LEAD_V, squash=1.1, segments=12, rings=5))
    parts.append(box("cod_cross", 0.2, 0.2, 1.8, (x, y, 38.1), GOLD))
    return join(parts, "codussi")


BUILDERS = {
    "venice/san-marco": san_marco,
    "venice/san-marco-1204": lambda: san_marco("1204"),
    "venice/san-marco-832": lambda: san_marco("832"),
    "venice/campanile": campanile_sm,
    "venice/campanile-1204": lambda: campanile_sm("old"),
    "venice/doges-palace": doges_palace,
    "venice/doges-palace-1400": lambda: doges_palace("1400"),
    "venice/doges-palace-ziani": lambda: doges_palace("ziani"),
    "venice/doges-castle": lambda: doges_palace("castle"),
    "venice/piazza": piazza,
    "venice/piazza-1580": lambda: piazza("1580"),
    "venice/piazza-1400": lambda: piazza("1400"),
    "venice/procuratie-vecchie": procuratie_vecchie,
    "venice/procuratie-old": lambda: procuratie_vecchie("old"),
    "venice/procuratie-nuove": procuratie_nuove,
    "venice/torre-orologio": torre_orologio,
    "venice/marciana": marciana,
    "venice/marciana-1580": lambda: marciana("1580"),
    "venice/columns": columns_molo,
    "venice/bucintoro": bucintoro,
    "venice/bucintoro-1400": lambda: bucintoro("1400"),
    "venice/rialto-bridge": rialto_bridge,
    "venice/rialto-bridge-wood": lambda: rialto_bridge("wood"),
    "venice/rialto-pontoon": lambda: rialto_bridge("pontoon"),
    "venice/rialto-market": rialto_market,
    "venice/rialto-market-old": lambda: rialto_market("old"),
    "venice/arsenale": arsenale,
    "venice/arsenale-1400": lambda: arsenale("1400"),
    "venice/arsenale-1204": lambda: arsenale("1204"),
    "venice/fondaco": fondaco,
    "venice/fondaco-old": lambda: fondaco("old"),
    "venice/ca-doro": ca_doro,
    "venice/zanipolo": zanipolo,
    "venice/frari": frari,
    "venice/san-giorgio": san_giorgio,
    "venice/san-giorgio-1580": lambda: san_giorgio("1580"),
    "venice/san-giorgio-old": lambda: san_giorgio("old"),
    "venice/redentore": redentore,
    "venice/redentore-1580": lambda: redentore("1580"),
    "venice/salute": salute,
    "venice/ghetto": ghetto,
    "venice/san-pietro": san_pietro,
    "venice/san-pietro-1580": lambda: san_pietro("1580"),
    "venice/san-pietro-old": lambda: san_pietro("old"),
}
