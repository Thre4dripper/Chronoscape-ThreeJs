"""Carthage landmark miniatures: the Punic citadel and harbours, the Tophet and the sea wall,
Roman Carthage's baths, theatres, circus and cisterns, the basilica of Damous el Karita, and
the ruins and the village of Sidi Bou Said.

Conventions as worldkit: metres, origin at the ground centre of the footprint, +X east, +Y north,
+Z up, main front to the south (-Y); the landmark's rotation turns it on the map. Repetitive parts
(ship sheds, stelae, houses, rubble) are written straight into one mesh with MB, so that a ring of
135 sheds costs a few operator calls instead of hundreds.
"""
import math, random
import bpy
from chronokit import Model, box, cylinder, dome, join, shade, gable_roof, hip_roof, mesh_from, ring_extrude, ellipse_pts, stadium_pts, stadium_ring, obelisk
from worldkit import lathe, prism, frustum, rot, move, arch_panel, arcade, wall_run, flat_house, tree, shallow_dome
from archkit import column, copy_at, cyl_x, cyl_y, half_cyl_x, half_cyl_y, steps_front, statue, thermal_window, ring_of

# ---------------------------------------------------------------- palette
SAND = "#D8C49C"      # Punic sandstone ashlar (El Haouaria stone)
SAND_D = "#C2AC82"
STUC = "#EDE5D2"      # white lime stucco
STUC_D = "#DACDB2"
ROCK = "#B8A47F"
ROCK_D = "#A08D6C"
EARTH = "#C9B085"
EARTH_D = "#B49A70"
GRASS = "#9CA670"
SCRUB = "#7F8A58"
MARB = "#ECE6D8"
GRAN = "#8E8A86"      # grey granite of the bath columns
CONC = "#D2C3A3"      # Roman concrete and rendered vaults
STONE = "#CDBB98"     # Roman ashlar and rubble walls
TILE = "#B4643F"
WAT = "#5F878C"
PAVE = "#D6C9A8"
TIMB = "#8C6A4A"
REDF = "#A9584A"      # red mortar floors
OCHRE = "#C2903F"
BLUE = "#4F6A8E"
DARK = "#2E241C"
BRONZE = "#7E6E4E"
GILT = "#D4AE55"
OLIVE = "#6B7B50"
REED = "#8F9A5C"
HULL = "#5E4632"
HULL_W = "#4A3A2C"
SAIL = "#E8DFC8"
WHITE = "#F2EEE4"
GREEN_T = "#5F8A5A"


# ---------------------------------------------------------------- basic helpers
def _sel(o):
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o


def bake(o):
    """Apply location, rotation and scale: geometry in world space, origin at the world origin."""
    if o is None:
        return None
    _sel(o)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return o


def turn(o, deg, x=0.0, y=0.0, z=0.0):
    """Rotate about the world Z axis (degrees, counter-clockwise from above), then move."""
    bake(o)
    o.rotation_euler = (0.0, 0.0, math.radians(deg))
    o.location = (x, y, z)
    return bake(o)


def J(parts, name):
    parts = [p for p in parts if p is not None]
    if not parts:
        return None
    return bake(join(parts, name))


def copies(proto, locs, name, rots=None):
    """Linked copies of a piece built at the origin, at each (x, y, z) with an optional Z rotation (radians)."""
    bake(proto)
    objs = [copy_at(proto, loc, rots[i] if rots else 0.0, name=f"{name}{i}") for i, loc in enumerate(locs)]
    bpy.data.objects.remove(proto, do_unlink=True)
    return J(objs, name)


class MB:
    """Mesh builder: many simple solids collected into one mesh (one operator call at the end)."""

    def __init__(self):
        self.v, self.f = [], []

    def prism(self, pts, z0, z1, top=None, bottom=False):
        n, b = len(pts), len(self.v)
        top = top or pts
        self.v += [(x, y, z0) for x, y in pts] + [(x, y, z1) for x, y in top]
        if bottom:
            self.f.append(tuple(range(b + n - 1, b - 1, -1)))
        self.f.append(tuple(range(b + n, b + 2 * n)))
        for i in range(n):
            j = (i + 1) % n
            self.f.append((b + i, b + j, b + n + j, b + n + i))

    def box(self, cx, cy, z0, w, d, h, rot=0.0, taper=1.0):
        c, s = math.cos(rot), math.sin(rot)
        q = [(-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2)]
        pts = [(cx + x * c - y * s, cy + x * s + y * c) for x, y in q]
        top = [(cx + x * taper * c - y * taper * s, cy + x * taper * s + y * taper * c) for x, y in q] if taper != 1.0 else None
        self.prism(pts, z0, z0 + h, top)

    def cyl(self, cx, cy, z0, r, h, n=8, r_top=None):
        rt = r if r_top is None else r_top
        pts = [(cx + r * math.cos(math.tau * i / n), cy + r * math.sin(math.tau * i / n)) for i in range(n)]
        top = [(cx + rt * math.cos(math.tau * i / n), cy + rt * math.sin(math.tau * i / n)) for i in range(n)]
        self.prism(pts, z0, z0 + h, top)

    def raw(self, verts, faces):
        b = len(self.v)
        self.v += list(verts)
        self.f += [tuple(b + i for i in f) for f in faces]

    def build(self, name, color):
        return mesh_from(name, self.v, self.f, (0, 0, 0), color) if self.f else None


def shift(o, x=0.0, y=0.0, z=0.0):
    """Move a (possibly rotated) object: apply its transforms first."""
    bake(o)
    o.location = (x, y, z)
    return bake(o)


def polar(r, a):
    return (r * math.cos(a), r * math.sin(a))


def cavetto(name, w, d, z, h, color, cx=0.0, cy=0.0):
    """The Egyptian gorge cornice of Punic architecture: a roll moulding and a flaring hollow band."""
    return J([box(name + "_torus", w + 0.3, d + 0.3, h * 0.2, (cx, cy, z), shade(color, 0.05)),
              frustum(name + "_gorge", w, d, w + h * 1.3, d + h * 1.3, h * 0.8, (cx, cy, z + h * 0.2), color)], name)


def icol(name, h, r, color=STUC):
    """A cheap Ionic column at the origin: base, tapered 8-sided shaft, volute bar and abacus."""
    return J([box(name + "_b", r * 2.4, r * 2.4, r * 0.5, (0, 0, 0), shade(color, -0.04)),
              cylinder(name + "_s", r, h - r * 1.4, (0, 0, r * 0.5), color, verts=8, r_top=r * 0.86),
              box(name + "_v", r * 3.0, r * 1.4, r * 0.55, (0, 0, h - r * 0.9), shade(color, -0.05)),
              box(name + "_a", r * 2.4, r * 2.4, r * 0.35, (0, 0, h - r * 0.35), color)], name)


def dcol(name, h, r, color=MARB):
    """A cheap Roman column (Tuscan/Corinthian at distance): base, shaft, bell capital, abacus."""
    return J([box(name + "_b", r * 2.5, r * 2.5, r * 0.6, (0, 0, 0), shade(color, -0.05)),
              cylinder(name + "_s", r, h - r * 2.2, (0, 0, r * 0.6), color, verts=8, r_top=r * 0.86),
              cylinder(name + "_c", r * 0.9, r * 1.2, (0, 0, h - r * 1.6), shade(color, -0.04), verts=8, r_top=r * 1.3),
              box(name + "_a", r * 2.7, r * 2.7, r * 0.4, (0, 0, h - r * 0.4), color)], name)


def col_row(name, pts, z, h, r, kind="i", color=STUC, rots=None):
    proto = icol(name + "_p", h, r, color) if kind == "i" else dcol(name + "_p", h, r, color)
    return copies(proto, [(x, y, z) for x, y in pts], name, rots)


def lin(a, b, n):
    return [a] if n == 1 else [a + (b - a) * i / (n - 1) for i in range(n)]


def hill_cap(name, w, d, h, top=0.8, n=36, seed=3, color=ROCK, jitter=0.05, power=2.6):
    """A cut of hill: a rounded rectangle w x d at the base, battered sides, a flat top scaled by `top`."""
    r = random.Random(seed)
    k = 2.0 / power
    base, cap = [], []
    for i in range(n):
        a = math.tau * i / n
        c, s = math.cos(a), math.sin(a)
        x, y = math.copysign(abs(c) ** k, c) * w / 2, math.copysign(abs(s) ** k, s) * d / 2
        j = 1 + r.uniform(-jitter, jitter)
        base.append((x * j, y * j))
        jt = top * (1 + r.uniform(-jitter, jitter) * 0.6)
        cap.append((x * jt, y * jt))
    mb = MB()
    mb.prism(base, 0, h, cap)
    return mb.build(name, color)


def add_hull(mb, L, W, H, cx, cy, z, ang, ram=False):
    """A ship's hull: pointed bow toward +x (before turning by ang), narrower keel, flat deck."""
    half = [(L / 2, 0), (L * 0.36, W * 0.36), (L * 0.12, W / 2), (-L * 0.2, W * 0.48), (-L * 0.4, W * 0.32), (-L / 2, W * 0.08)]
    outline = half + [(x, -y) for x, y in reversed(half[1:])]
    if half[-1][1] > 0:
        outline = half + [(-L / 2, -W * 0.08)] + [(x, -y) for x, y in reversed(half[1:-1])]
    c, s = math.cos(ang), math.sin(ang)
    tr = lambda p, f: (cx + (p[0] * f[0]) * c - (p[1] * f[1]) * s, cy + (p[0] * f[0]) * s + (p[1] * f[1]) * c)
    keel = [tr(p, (0.88, 0.45)) for p in outline]
    deck = [tr(p, (1.0, 1.0)) for p in outline]
    mb.prism(keel, z, z + H, deck)
    if ram:
        bx, by = tr((L / 2 + 1.0, 0), (1, 1))
        mb.box(bx, by, z, 2.4, W * 0.3, H * 0.35, ang)


def ships(name, specs, color=HULL, masts=True):
    """specs: (L, W, cx, cy, z, ang, kind) with kind 'war' (ram, no mast) or 'merchant' (mast and furled sail)."""
    hb, mm = MB(), MB()
    for L, W, cx, cy, z, ang, kind in specs:
        add_hull(hb, L, W, L * 0.075, cx, cy, z, ang, ram=(kind == "war"))
        if masts and kind == "merchant":
            mm.cyl(cx, cy, z + L * 0.07, 0.25, L * 0.55, n=5)
            mm.box(cx, cy, z + L * 0.55, 0.6, W * 1.3, 0.5, ang + math.pi / 2)
    return J([hb.build(name + "_h", color), mm.build(name + "_m", TIMB)], name)


def wedge_roofs(mb, bounds, r_in, r_out, z_e, z_r, outward=True):
    """Gabled roofs over radial bays between consecutive angles in `bounds`, from radius r_in to r_out."""
    for a0, a1 in zip(bounds, bounds[1:]):
        am = (a0 + a1) / 2
        il, ir, ol, orr = polar(r_in, a0), polar(r_in, a1), polar(r_out, a0), polar(r_out, a1)
        ri, ro = polar(r_in, am), polar(r_out, am)
        v = [(*il, z_e), (*ir, z_e), (*ol, z_e), (*orr, z_e), (*ri, z_r), (*ro, z_r)]
        mb.raw(v, [(0, 2, 5, 4), (1, 4, 5, 3), (0, 4, 1), (2, 3, 5)])


def radial_box(mb, a, r0, r1, z0, h, t):
    rm = (r0 + r1) / 2
    x, y = polar(rm, a)
    mb.box(x, y, z0, r1 - r0, t, h, a)


def ramp(mb, a0, a1, r0, z0, r1, z1, inset=0.6):
    """A sloping slipway in the bay between angles a0 and a1, from (r0, z0) to (r1, z1)."""
    da = inset / max(r0, 1)
    p = [polar(r0, a0 + da), polar(r0, a1 - da), polar(r1, a1 - da * r0 / r1), polar(r1, a0 + da * r0 / r1)]
    zb = max(0.0, min(z0, z1) - 0.4)
    v = [(*p[0], zb), (*p[1], zb), (*p[2], zb), (*p[3], zb), (*p[0], z0), (*p[1], z0), (*p[2], z1), (*p[3], z1)]
    mb.raw(v, [(4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)])


def rubble(name, n, w, d, seed=1, color=STONE, size=1.6, cx=0.0, cy=0.0, z=0.0):
    r = random.Random(seed)
    mb = MB()
    for i in range(n):
        x, y = cx + r.uniform(-w / 2, w / 2), cy + r.uniform(-d / 2, d / 2)
        if r.random() < 0.35:
            mb.cyl(x, y, z, size * 0.4, size * r.uniform(0.3, 0.6), n=6)
        else:
            mb.box(x, y, z, size * r.uniform(0.6, 1.5), size * r.uniform(0.5, 1.1), size * r.uniform(0.3, 0.7), r.uniform(0, 3))
    return mb.build(name, color)


def trees(name, pts, r=3.0, color=OLIVE, kind="round"):
    return J([tree(f"{name}{i}", r * (0.85 + 0.3 * ((i * 37) % 7) / 7), (x, y, z), color, TIMB, kind) for i, (x, y, z) in enumerate(pts)], name)


def reeds(name, n, rx, ry, seed=2, cx=0.0, cy=0.0, r_min=0.0):
    r = random.Random(seed)
    mb = MB()
    k = 0
    while k < n:
        a, t = r.uniform(0, math.tau), math.sqrt(r.uniform(0, 1))
        if t < r_min:
            continue
        mb.cyl(cx + rx * t * math.cos(a), cy + ry * t * math.sin(a), 0.2, r.uniform(0.8, 1.6), r.uniform(0.8, 1.6), n=5, r_top=0.15)
        k += 1
    return mb.build(name, REED)


def punic_house(mb_w, mb_r, mb_d, cx, cy, z, w, d, h, rot=0.0, court=True, kiosk=True, windows=2):
    """A Punic courtyard house: wings round a court, flat roofs with a parapet, a red-floored court
    with a cistern mouth, a door on the -Y side, a stair head on the roof. mb_w walls, mb_r red floors,
    mb_d dark openings."""
    c, s = math.cos(rot), math.sin(rot)
    P = lambda x, y: (cx + x * c - y * s, cy + x * s + y * c)
    if court and min(w, d) > 9:
        t = min(w, d) * 0.3
        for (x, y, ww, dd) in [(0, -d / 2 + t / 2, w, t), (0, d / 2 - t / 2, w, t), (-w / 2 + t / 2, 0, t, d - 2 * t), (w / 2 - t / 2, 0, t, d - 2 * t)]:
            px, py = P(x, y)
            mb_w.box(px, py, z, ww, dd, h, rot)
            mb_w.box(px, py, z + h, ww + 0.2, dd + 0.2, 0.5, rot)
        px, py = P(0, 0)
        mb_r.box(px, py, z, w - 2 * t, d - 2 * t, 0.15, rot)
        qx, qy = P(w * 0.08, d * 0.05)
        mb_d.cyl(qx, qy, z, 0.45, 0.25, n=6)
    else:
        px, py = P(0, 0)
        mb_w.box(px, py, z, w, d, h, rot)
        mb_w.box(px, py, z + h, w + 0.2, d + 0.2, 0.5, rot)
    if kiosk:
        kx, ky = P(w / 2 - 1.6, d / 2 - 1.6)
        mb_w.box(kx, ky, z + h, 2.4, 2.4, 2.1, rot)
    dx, dy = P(-w * 0.2, -d / 2 - 0.05)
    mb_d.box(dx, dy, z, 1.1, 0.25, 2.1, rot)
    for k in range(windows):
        t = (k + 0.5) / windows - 0.5
        wx, wy = P(t * w * 0.7 + w * 0.08, -d / 2 - 0.05)
        mb_d.box(wx, wy, z + h * 0.62, 0.7, 0.25, 0.9, rot)
        if h > 6.5:
            mb_d.box(wx, wy, z + h * 0.3, 0.6, 0.25, 0.7, rot)


def mb_cavetto(mb, cx, cy, z, w, d, h):
    """A cavetto cornice written into a mesh builder: roll moulding and flaring gorge."""
    mb.box(cx, cy, z, w + 0.3, d + 0.3, h * 0.2)
    mb.prism([(cx - w / 2, cy - d / 2), (cx + w / 2, cy - d / 2), (cx + w / 2, cy + d / 2), (cx - w / 2, cy + d / 2)], z + h * 0.2, z + h,
             [(cx - w / 2 - h * 0.65, cy - d / 2 - h * 0.65), (cx + w / 2 + h * 0.65, cy - d / 2 - h * 0.65), (cx + w / 2 + h * 0.65, cy + d / 2 + h * 0.65), (cx - w / 2 - h * 0.65, cy + d / 2 + h * 0.65)])


# ---------------------------------------------------------------- classical pieces
def portico(name, length, depth, h, col_r=0.5, spacing=4.5, kind="d", color=MARB, roof=TILE):
    """A one-aisle portico along X centred on the origin: back wall at +Y, columns along -Y, a lean-to roof."""
    wh = h + 1.6
    parts = [box(name + "_floor", length, depth, 0.4, (0, 0, 0), shade(color, -0.08)),
             box(name + "_wall", length, 0.9, wh + 0.4, (0, depth / 2 - 0.45, 0), shade(color, -0.04))]
    cy = -depth / 2 + col_r * 1.4
    n = max(2, int(length / spacing) + 1)
    parts.append(col_row(name + "_c", [(x, cy) for x in lin(-length / 2 + col_r * 1.5, length / 2 - col_r * 1.5, n)], 0.4, h, col_r, kind, color))
    parts.append(box(name + "_arch", length, col_r * 2.6, h * 0.12, (0, cy, 0.4 + h), shade(color, 0.03)))
    z1, z2 = 0.4 + h * 1.12, 0.4 + wh + 0.2
    y1, y2 = -depth / 2 - 0.4, depth / 2 + 0.1
    v = [(-length / 2 - 0.3, y1, z1), (length / 2 + 0.3, y1, z1), (length / 2 + 0.3, y2, z2), (-length / 2 - 0.3, y2, z2)]
    v += [(x, y, z + 0.35) for x, y, z in v]
    parts.append(mesh_from(name + "_roof", v, [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)], (0, 0, 0), roof))
    return J(parts, name)


def court(name, w, d, depth, h, col_r=0.5, spacing=4.5, kind="d", color=MARB, roof=TILE, skip=()):
    """Porticoes facing inward round a w x d court centred on the origin."""
    out = []
    if "S" not in skip:
        out.append(turn(portico(name + "_s", w, depth, h, col_r, spacing, kind, color, roof), 180, 0, -d / 2 + depth / 2))
    if "N" not in skip:
        out.append(turn(portico(name + "_n", w, depth, h, col_r, spacing, kind, color, roof), 0, 0, d / 2 - depth / 2))
    if "W" not in skip:
        out.append(turn(portico(name + "_w", d - 2 * depth, depth, h, col_r, spacing, kind, color, roof), 90, -w / 2 + depth / 2, 0))
    if "E" not in skip:
        out.append(turn(portico(name + "_e", d - 2 * depth, depth, h, col_r, spacing, kind, color, roof), -90, w / 2 - depth / 2, 0))
    return J(out, name)


def gable(name, w, d, h, loc, color=TILE, overhang=0.5, along="Y"):
    """Plain gable roof over w x d; ridge along Y (default) or X."""
    if along == "Y":
        o = gable_roof(name, w, d, h, (0, 0, 0), color, overhang)
        return turn(o, 0, *loc)
    o = gable_roof(name, d, w, h, (0, 0, 0), color, overhang)
    return turn(o, 90, *loc)


def roman_temple(name, w, d, podium, col_h, nf, color=MARB, roof=TILE, z=0.0):
    """A prostyle Corinthian temple on a podium, front to -Y, centred on the origin."""
    r = min(w / (nf * 4.4), 1.0)
    cd = d * 0.62
    parts0 = [box(name + "_pod", w, d, podium, (0, 0, z), shade(color, -0.1)),
              box(name + "_podc", w + 0.6, d + 0.6, 0.45, (0, 0, z + podium - 0.45), shade(color, -0.04)),
              steps_front(name + "_st", w * 0.7, podium, max(4, int(podium / 0.35)), -d / 2, z, shade(color, -0.06))]
    zt = z + podium
    fr = [(x, -d / 2 + r * 2) for x in lin(-w / 2 + r * 1.6, w / 2 - r * 1.6, nf)] + [(x, -d / 2 + r * 2 + (d - cd) * 0.45) for x in (-w / 2 + r * 1.6, w / 2 - r * 1.6)]
    parts1 = [col_row(name + "_c", fr, zt, col_h, r, "d", color),
              box(name + "_cella", w - 0.6, cd, col_h, (0, d / 2 - cd / 2, zt), shade(color, -0.04)),
              box(name + "_door", w * 0.22, 0.4, col_h * 0.6, (0, d / 2 - cd - 0.15, zt), DARK)]
    eh = col_h * 0.18
    parts2 = [box(name + "_ent", w + 0.4, d + 0.4, eh, (0, 0, zt + col_h), shade(color, 0.03)),
              box(name + "_frieze", w + 0.1, d + 0.1, eh * 0.4, (0, 0, zt + col_h + eh * 0.3), shade(color, -0.06)),
              gable(name + "_roof", w + 0.4, d + 0.4, w * 0.2, (0, 0, zt + col_h + eh), roof, 0.4),
              mesh_from(name + "_tymp", [(-w / 2, -d / 2 - 0.25, 0), (w / 2, -d / 2 - 0.25, 0), (0, -d / 2 - 0.25, w * 0.19)], [(0, 1, 2)], (0, 0, zt + col_h + eh), shade(color, -0.08)),
              statue(name + "_acro", 0, -d / 2 - 0.3, zt + col_h + eh + w * 0.2, 2.2, GILT)]
    return J(parts0, name + "_0"), J(parts1, name + "_1"), J(parts2, name + "_2")


def cavea_rows(name, cx, cy, r0, r1, z0, z1, rows, arc=math.pi, start=0.0, colors=(MARB, STONE), n=40):
    """Stepped seating as solid rings from the ground, rising from z0 at r0 to z1 at r1."""
    out = []
    for k in range(rows):
        ra, rb = r0 + (r1 - r0) * k / rows, r0 + (r1 - r0) * (k + 1) / rows
        zz = z0 + (z1 - z0) * (k + 1) / rows
        o, _ = ellipse_pts(rb, rb, n, arc, start)
        i, _ = ellipse_pts(ra, ra, n, arc, start)
        out.append(ring_extrude(f"{name}{k}", o, i, zz, (cx, cy, 0), colors[k % len(colors)], closed=abs(arc - math.tau) < 1e-6))
    return J(out, name)


def ell_ring(name, rx0, ry0, rx1, ry1, h, z=0.0, color=STONE, n=48, arc=math.tau, start=0.0):
    o, closed = ellipse_pts(rx1, ry1, n, arc, start)
    i, _ = ellipse_pts(rx0, ry0, n, arc, start)
    return ring_extrude(name, o, i, h, (0, 0, z), color, closed)


def ell_disc(name, rx, ry, h, z=0.0, color=PAVE, n=48):
    pts, _ = ellipse_pts(rx, ry, n)
    mb = MB()
    mb.prism(pts, z, z + h)
    return mb.build(name, color)


# ================================================================ the Byrsa (hero)
BYRSA_H = 9.0


def punic_temple(name, z, color=STUC):
    """The temple of Eshmun as interpreted here: a podium with a cavetto cornice, a hexastyle porch of
    Punic-Ionic columns, a cella, a cavetto-crowned entablature and a low pediment. Front to -Y."""
    W, D, P = 26.0, 38.0, 4.0
    s0 = [box(name + "_pod", W + 6, D + 6, P - 0.8, (0, 0, z), SAND),
          cavetto(name + "_podc", W + 6, D + 6, z + P - 0.8, 0.8, SAND_D),
          steps_front(name + "_st", 14, P, 12, -D / 2 - 3, z, SAND_D, tread=0.5)]
    zt = z + P
    ch = 10.0
    fr = [(x, -D / 2 + 1.2) for x in lin(-W / 2 + 1.4, W / 2 - 1.4, 6)] + [(x, -D / 2 + 6) for x in (-W / 2 + 1.4, W / 2 - 1.4)]
    s1 = [copies(column(name + "_colp", 0, 0, 0, ch, 0.62, "ionic", STUC, flutes=12), [(x, y, zt) for x, y in fr], name + "_cols"),
          box(name + "_cella", W - 2, D - 9, ch, (0, 4.5, zt), color),
          box(name + "_door", 4.0, 0.4, 6.5, (0, -D / 2 + 8.8, zt), DARK),
          box(name + "_band", W - 1.8, D - 8.8, 0.6, (0, 4.5, zt + ch * 0.7), OCHRE)]
    ze = zt + ch
    s2 = [box(name + "_arch", W + 0.4, D + 0.4, 1.0, (0, 0, ze), STUC_D),
          box(name + "_frieze", W + 0.2, D + 0.2, 0.9, (0, 0, ze + 1.0), BLUE),
          cavetto(name + "_cav", W + 0.4, D + 0.4, ze + 1.9, 1.4, STUC),
          gable(name + "_roof", W + 2.2, D + 2.2, 4.2, (0, 0, ze + 3.3), TILE, 0.3),
          mesh_from(name + "_tymp", [(-W / 2 - 0.9, -D / 2 - 1.2, 0), (W / 2 + 0.9, -D / 2 - 1.2, 0), (0, -D / 2 - 1.2, 4.0)], [(0, 1, 2)], (0, 0, ze + 3.3), STUC_D),
          statue(name + "_akro", 0, -D / 2 - 1.3, ze + 7.4, 2.0, GILT),
          box(name + "_disc", 2.4, 0.4, 2.4, (0, -D / 2 - 1.35, ze + 4.6), GILT)]
    return J(s0, name + "0"), J(s1, name + "1"), J(s2, name + "2")


def byrsa():
    m = Model("byrsa")
    m.add(0, hill_cap("hill", 230, 170, BYRSA_H, top=0.8, seed=11, color=ROCK), "hill")
    m.add(0, hill_cap("summit", 182, 134, 0.3, top=0.99, seed=12, color=EARTH, jitter=0.02), "hill")
    zt = BYRSA_H + 0.3
    # citadel walls along the top edge, square towers with cavetto crowns, a gate where the great stair arrives
    ring = [(-12, -62), (-78, -62), (-88, -50), (-88, 50), (-78, 62), (78, 62), (88, 50), (88, -50), (78, -62), (12, -62)]
    m.add(0, wall_run("walls", ring, 7.0, 3.0, (0, 0, BYRSA_H), SAND, towers=False))
    tw, tc = MB(), MB()
    tpts = [(-30, -62), (-55, -62), (-80, -60), (-88, -28), (-88, 0), (-88, 28), (-80, 60), (-50, 62), (-20, 62), (20, 62), (50, 62), (80, 60),
            (88, 28), (88, 0), (88, -28), (80, -60), (55, -62), (30, -62)]
    for x, y in tpts:
        tw.box(x, y, BYRSA_H, 7, 7, 10.5)
        mb_cavetto(tc, x, y, BYRSA_H + 10.5, 7, 7, 1.0)
    m.add(0, tw.build("towers", SAND_D))
    m.add(0, tc.build("tower_crowns", SAND))
    m.add(0, J([box("gate_t" + str(s), 8, 8, 11, (s * 15, -62, BYRSA_H), SAND_D) for s in (-1, 1)] +
               [box("gate_lintel", 24, 6, 2.2, (0, -62, BYRSA_H + 7.6), SAND_D), cavetto("gate_cav", 24, 6, BYRSA_H + 9.8, 1.0, SAND),
                box("gate_way", 0.4, 0.4, 0.1, (0, -62, BYRSA_H), DARK)], "gate"))
    # the stair of sixty steps up the south face, with terraced gardens either side
    m.add(1, steps_front("stair", 14, BYRSA_H, 60, -64, 0, STUC, tread=0.38), "temple")
    m.add(1, J([box(f"stair_wall{s}", 1.2, 24, 2.2, (s * 7.6, -76, 0), SAND) for s in (-1, 1)], "stair_walls"))
    # sacred court with porticoes round the temple of Eshmun
    m.add(1, box("court", 72, 70, 0.3, (0, 6, zt), PAVE))
    t0, t1, t2 = punic_temple("eshmun", zt + 0.3)
    m.add(1, t0)
    m.add(1, t1)
    m.add(1, J([box(f"temenos{k}", *dims, (x, y, zt), STUC_D) for k, (x, y, dims) in enumerate([(0, 41, (72, 1.2, 5.5)), (-36, 6, (1.2, 70, 5.5)), (36, 6, (1.2, 70, 5.5)), (-22, -29, (28, 1.2, 5.5)), (22, -29, (28, 1.2, 5.5))])], "temenos"))
    pts = [(x, 37.5) for x in lin(-32, 32, 12)] + [(sx * 32.5, y) for sx in (-1, 1) for y in lin(-24, 32, 10)]
    m.add(1, col_row("temenos_cols", pts, zt + 0.3, 4.6, 0.32, "i", STUC))
    m.add(1, J([box("altar", 6, 4, 1.8, (0, -22, zt), SAND), box("altar_top", 6.6, 4.6, 0.4, (0, -22, zt + 1.8), SAND_D),
                box("propylon_l", 4, 4, 7, (-6.5, -29, zt), STUC), box("propylon_r", 4, 4, 7, (6.5, -29, zt), STUC),
                box("propylon_t", 17, 4.6, 1.4, (0, -29, zt + 7), STUC_D), cavetto("propylon_cav", 17, 4.6, zt + 8.4, 1.0, STUC)], "altar"))
    # houses and stores of the citadel, packed between the sacred court and the walls
    mw, mr, md = MB(), MB(), MB()
    r = random.Random(5)
    cells = []
    for gx in lin(-78, 78, 11):
        for gy in lin(-52, 52, 8):
            if abs(gx) < 44 and -36 < gy < 48:
                continue
            if abs(gx) < 12 and gy < -30:
                continue
            cells.append((gx + r.uniform(-1, 1), gy + r.uniform(-1, 1)))
    for (x, y) in cells:
        w, d = r.uniform(11.5, 13.5), r.uniform(11, 13)
        punic_house(mw, mr, md, x, y, zt, w, d, r.choice([6.0, 7.5, 9.0, 10.5]), court=r.random() < 0.7, kiosk=r.random() < 0.6)
    m.add(2, mw.build("houses", STUC), "houses")
    m.add(2, mr.build("floors", REDF))
    m.add(2, md.build("openings", DARK))
    m.add(2, t2)
    pc = MB()
    for x0, y0, x1, y1 in ((-33.5, 39.5, 33.5, 39.5), (-34.0, -28, -34.0, 39.5), (34.0, -28, 34.0, 39.5)):
        L = math.hypot(x1 - x0, y1 - y0)
        pc.box((x0 + x1) / 2, (y0 + y1) / 2, zt + 4.9, L if y0 == y1 else 4.0, 4.0 if y0 == y1 else L, 0.5)
    m.add(2, pc.build("portico_roofs", TILE))
    m.add(2, trees("trees", [(-22, -16, zt), (22, -16, zt), (-26, 28, zt), (26, 28, zt), (-14, 30, zt), (14, 30, zt),
                             (-80, -78, 0), (90, -70, 0), (-104, 30, 0), (104, 20, 0), (-60, -80, 0), (62, -80, 0)], 3.2))
    return m


def byrsa_forum():
    m = Model("byrsa-forum")
    H = BYRSA_H + 2
    m.add(0, hill_cap("hill", 230, 170, 3.0, top=0.97, seed=11, color=ROCK, jitter=0.02), "terrace")
    m.add(0, box("platform", 210, 150, H, (0, 0, 0), STONE))
    mb = MB()
    for x in lin(-100, 100, 15):
        mb.box(x, -76.5, 0, 4, 3, H - 1.5)
        mb.box(x, 76.5, 0, 4, 3, H - 1.5)
    for y in lin(-66, 66, 9):
        mb.box(-106.5, y, 0, 3, 4, H - 1.5)
        mb.box(106.5, y, 0, 3, 4, H - 1.5)
    m.add(0, mb.build("buttresses", shade(STONE, -0.05)))
    m.add(0, arcade("south_arches", 180, 6, 14, (0, -75.2, 1.0), "S", DARK, pointed=False))
    m.add(0, steps_front("stairs", 30, H, 30, -75, 0, shade(STONE, 0.04), tread=0.5))
    m.add(1, box("forum_floor", 120, 96, 0.3, (-10, -8, H), PAVE), "forum")
    m.add(1, turn(court("forum_porticoes", 120, 96, 7, 7.0, 0.42, 5.0, "d", MARB, TILE, skip=("N",)), 0, -10, -8, H))
    # capitolium at the north end of the forum, facing south
    t0, t1, t2 = roman_temple("capitol", 26, 40, 4.5, 13.0, 6)
    m.add(1, turn(t0, 0, -10, 46, H))
    m.add(1, turn(t1, 0, -10, 46, H))
    # judicial basilica along the east side
    m.add(1, box("basilica", 34, 130, 16, (82, 0, H), shade(MARB, -0.06)))
    m.add(1, box("basilica_aisles", 44, 136, 10, (82, 0, H), shade(STONE, 0.04)))
    m.add(1, arcade("basilica_w", 120, 7, 16, (60, 0, H), "W", DARK, pointed=False))
    # offices and a small temple to the west
    m.add(1, box("curia", 18, 26, 12, (-88, 30, H), MARB))
    m.add(1, box("offices", 18, 60, 9, (-88, -20, H), STONE))
    m.add(2, turn(t2, 0, -10, 46, H), "roofs")
    m.add(2, gable("basilica_roof", 34, 130, 6, (82, 0, H + 16), TILE, 0.4))
    m.add(2, gable("aisle_roof", 44, 136, 2.0, (82, 0, H + 10), shade(TILE, 0.06), 0.2))
    m.add(2, gable("curia_roof", 18, 26, 4, (-88, 30, H + 12), TILE))
    m.add(2, box("offices_roof", 19, 61, 0.6, (-88, -20, H + 9), shade(TILE, -0.05)))
    m.add(2, J([statue(f"st{k}", x, y, H + 0.3, 3.2, BRONZE) for k, (x, y) in enumerate([(-30, -20), (10, -20), (-30, 10), (10, 10), (-10, -40)])], "statues"))
    m.add(2, J([box("arch", 14, 5, 10, (-10, -58, H), MARB), box("arch_att", 15, 5.6, 2.4, (-10, -58, H + 10), shade(MARB, -0.05)),
                box("arch_open", 5, 6, 7, (-10, -58, H), DARK)], "arch"))
    return m


def byrsa_ruins():
    m = Model("byrsa-ruins")
    m.add(0, hill_cap("hill", 230, 170, BYRSA_H, top=0.78, seed=13, color=ROCK, jitter=0.08), "hill")
    m.add(0, hill_cap("grass", 176, 128, 0.4, top=0.96, seed=14, color=GRASS, jitter=0.06))
    # stumps of the Roman retaining walls and buttresses, broken at random heights
    r = random.Random(4)
    mb = MB()
    for k in range(34):
        side = k % 4
        t = r.uniform(-0.45, 0.45)
        x, y = [(t * 200, -78), (t * 200, 78), (-104, t * 140), (104, t * 140)][side]
        mb.box(x, y, 0, r.uniform(6, 16) if side < 2 else 3.0, 3.0 if side < 2 else r.uniform(6, 16), r.uniform(2.5, 8.5))
    m.add(0, mb.build("wall_stumps", STONE))
    m.add(1, rubble("rubble", 160, 160, 110, seed=7, color=STONE, size=2.0, z=BYRSA_H + 0.3), "ruins")
    m.add(1, rubble("marble", 40, 120, 80, seed=8, color=MARB, size=1.4, z=BYRSA_H + 0.3))
    m.add(1, col_row("standing", [(-30, 20), (-24, 20), (12, -10)], BYRSA_H + 0.3, 9.0, 0.5, "d", MARB))
    m.add(1, J([cyl_x(f"drum{k}", 0.5, 3.0, (x, y, BYRSA_H + 0.8), MARB, verts=8) for k, (x, y) in enumerate([(-18, 16), (-8, 26), (30, -20), (40, 12)])], "drums"))
    # lime kiln, a goat fold and a few olives
    m.add(2, J([cylinder("kiln", 4.0, 4.5, (40, 30, BYRSA_H + 0.3), STONE, verts=12, r_top=3.2), cylinder("kiln_mouth", 2.6, 0.3, (40, 30, BYRSA_H + 4.8), DARK, verts=10)], "kiln"), "life")
    fold = [(-60, -30), (-40, -30), (-40, -14), (-60, -14), (-60, -26)]
    m.add(2, wall_run("fold", fold, 1.2, 0.7, (0, 0, BYRSA_H + 0.3), STONE, towers=False, merlon=None))
    m.add(2, trees("olives", [(-70, 20, BYRSA_H), (-55, 40, BYRSA_H), (60, -40, BYRSA_H), (75, 30, BYRSA_H), (-95, -60, 0), (100, -60, 0)], 3.4))
    return m


# ================================================================ the circular naval harbour (hero)
R_W, R_S0, R_S1, R_OUT = 113.0, 116.0, 156.0, 164.0
ENT = math.radians(-58)           # direction of the channel from the merchant harbour (model coordinates)
GAP = math.radians(5.5)


def _ring_arc(name, r0, r1, h, z, color, n=120):
    o, _ = ellipse_pts(r1, r1, n, math.tau - 2 * GAP, ENT + GAP)
    i, _ = ellipse_pts(r0, r0, n, math.tau - 2 * GAP, ENT + GAP)
    return ring_extrude(name, o, i, h, (0, 0, z), color, closed=False)


def _channel(m, stage, color=WAT):
    c, s = math.cos(ENT), math.sin(ENT)
    m.add(stage, J([box("channel", 62, 22, 0.32, ((R_W + 30) * c, (R_W + 30) * s, 0.2), color, rot_z=ENT)], "channel"))


def cothon(variant="punic"):
    m = Model("cothon")
    m.add(0, cylinder("ground", R_OUT + 1.5, 0.3, (0, 0, 0), EARTH, verts=72), "basin")
    m.add(0, cylinder("water", R_W + 2, 0.3, (0, 0, 0.22), WAT, verts=72))
    _channel(m, 0)
    m.add(0, _ring_arc("outer_wall", R_OUT - 2.5, R_OUT, 11.0, 0.3, SAND))
    m.add(0, _ring_arc("back_wall", R_S1, R_S1 + 1.6, 8.5, 0.3, SAND_D))
    m.add(0, _ring_arc("lane", R_S1 + 1.6, R_OUT - 2.5, 0.3, 0.3, PAVE))
    for sgn in (-1, 1):
        a = ENT + sgn * (GAP + 0.012)
        x, y = polar(R_OUT - 3, a)
        m.add(0, J([box(f"gate_tower{sgn}", 11, 11, 14, (x, y, 0.3), SAND, rot_z=a), cavetto(f"gate_cav{sgn}", 11, 11, 14.3, 1.0, SAND_D, x, y)], f"gate{sgn}"))
    # the island
    m.add(0, cylinder("island", 55, 0.9, (0, 0, 0.3), PAVE, verts=48))
    m.add(0, cylinder("island_quay", 56.5, 0.5, (0, 0, 0.2), SAND_D, verts=48))

    # ---- ring of ship sheds: partition walls, slipways, columns, gabled roofs with stores above
    N = 135
    bounds = [ENT + GAP + (math.tau - 2 * GAP) * k / N for k in range(N + 1)]
    walls, ramps, roofs = MB(), MB(), MB()
    for a in bounds:
        radial_box(walls, a, R_S0 - 1.0, R_S1, 0.3, 7.2, 0.9)
    for a0, a1 in zip(bounds, bounds[1:]):
        ramp(ramps, a0, a1, R_W - 6, 0.35, R_S1 - 0.5, 2.3, 0.5)
    wedge_roofs(roofs, bounds, R_S0 - 2.4, R_S1 + 0.6, 7.5, 10.4)
    m.add(1, walls.build("shed_walls", SAND), "sheds")
    m.add(1, ramps.build("slipways", TIMB))
    m.add(1, col_row("shed_cols", [polar(R_S0 - 1.4, a) for a in bounds], 0.3, 6.2, 0.36, "i", STUC))
    m.add(1, _ring_arc("architrave", R_S0 - 2.1, R_S0 - 0.6, 1.0, 6.5, STUC_D))
    m.add(1, _ring_arc("store_front", R_S0 - 1.8, R_S0 - 1.0, 0.9, 6.5 + 1.0, STUC))
    # island sheds facing outward, and the admiral's tower
    NI = 30
    ib = [math.tau * k / NI + 0.05 for k in range(NI + 1)]
    iw, ir, iro = MB(), MB(), MB()
    for a in ib[:-1]:
        radial_box(iw, a, 21, 53.5, 1.2, 6.0, 0.8)
    for a0, a1 in zip(ib, ib[1:]):
        ramp(ir, a0, a1, 21.5, 2.2, 58, 0.35, 0.4)
    wedge_roofs(iro, ib, 21.5, 55.5, 6.6, 8.8)
    m.add(1, iw.build("island_walls", SAND))
    m.add(1, ir.build("island_slips", TIMB))
    m.add(1, col_row("island_cols", [polar(54.5, a) for a in ib[:-1]], 1.2, 5.4, 0.34, "i", STUC))
    tz = 1.2
    m.add(1, J([box("adm_base", 20, 20, 3.5, (0, 0, tz), SAND), cavetto("adm_base_cav", 20, 20, tz + 3.5, 0.7, SAND_D),
                steps_front("adm_steps", 6, 4.2, 10, -10, tz, SAND_D, tread=0.5),
                box("adm_tower", 12, 12, 16, (0, 0, tz + 4.2), STUC),
                box("adm_door", 2.2, 0.3, 3.4, (0, -6.1, tz + 4.2), DARK)] +
               [box(f"adm_win{k}", 1.2, 0.3, 2.2, (x, -6.1, tz + 11), DARK) for k, x in enumerate((-3, 3))], "admiral"))
    m.add(2, roofs.build("shed_roofs", TILE), "roofs")
    m.add(2, iro.build("island_roofs", shade(TILE, 0.05)))
    zl = tz + 20.2
    m.add(2, J([box("adm_floor", 14, 14, 0.6, (0, 0, zl), STUC_D)] +
               [col_row("adm_loggia", [(x, y) for x in lin(-6, 6, 4) for y in (-6, 6)] + [(x, y) for x in (-6, 6) for y in (-2, 2)], zl + 0.6, 4.6, 0.32, "i", STUC)] +
               [cavetto("adm_cav", 14, 14, zl + 5.2, 1.2, STUC), box("adm_roof", 15.5, 15.5, 0.6, (0, 0, zl + 6.4), STUC_D),
                statue("trumpeter", 0, -6.5, zl + 0.6, 1.8, BRONZE)], "loggia"))
    # warships hauled up in some sheds, a few afloat in the basin
    r = random.Random(9)
    specs = []
    for k in r.sample(range(N), 22):
        am = (bounds[k] + bounds[k + 1]) / 2
        x, y = polar((R_S0 + R_S1) / 2 - 3, am)
        specs.append((34, 4.4, x, y, 1.6, am + math.pi, "war"))
    for k in r.sample(range(NI), 6):
        am = (ib[k] + ib[k + 1]) / 2
        x, y = polar(38, am)
        specs.append((30, 4.0, x, y, 1.8, am, "war"))
    for (rr, a, d) in [(88, 0.6, 1.2), (84, 2.4, 2.0), (90, 3.6, 0.3), (86, ENT + 0.35, ENT + math.pi / 2)]:
        x, y = polar(rr, a)
        specs.append((36, 4.8, x, y, 0.45, d, "war"))
    m.add(2, ships("warships", specs, HULL_W, masts=False))
    return m


def cothon_roman():
    m = Model("cothon-roman")
    m.add(0, cylinder("ground", R_OUT + 1.5, 0.3, (0, 0, 0), EARTH, verts=72), "basin")
    m.add(0, cylinder("water", R_W + 2, 0.3, (0, 0, 0.22), WAT, verts=72))
    _channel(m, 0)
    m.add(0, _ring_arc("quay", R_W, R_OUT, 1.3, 0.3, STONE))
    m.add(0, cylinder("island", 55, 1.4, (0, 0, 0.3), STONE, verts=6))
    # colonnade round the basin, warehouses behind it
    N = 88
    bounds = [ENT + GAP + (math.tau - 2 * GAP) * k / N for k in range(N + 1)]
    m.add(1, col_row("ring_cols", [polar(R_W + 3, a) for a in bounds], 1.6, 6.0, 0.4, "d", MARB), "porticoes")
    m.add(1, _ring_arc("ring_ent", R_W + 2.2, R_W + 3.8, 1.0, 7.6, shade(MARB, -0.04)))
    m.add(1, _ring_arc("stores", R_W + 9, R_OUT - 4, 7.0, 1.6, STONE))
    doors = MB()
    for a in bounds[1:-1:2]:
        x, y = polar(R_W + 8.9, a)
        doors.box(x, y, 1.6, 2.2, 0.4, 3.2, a + math.pi / 2)
    m.add(1, doors.build("store_doors", DARK))
    # island: hexagonal court with a portico round a small temple
    hexp = [polar(46, math.tau * k / 6) for k in range(6)]
    pts = []
    for (x0, y0), (x1, y1) in zip(hexp, hexp[1:] + hexp[:1]):
        pts += [(x0 + (x1 - x0) * t / 6, y0 + (y1 - y0) * t / 6) for t in range(6)]
    m.add(1, col_row("hex_cols", pts, 1.7, 5.5, 0.36, "d", MARB))
    t0, t1, t2 = roman_temple("island_temple", 14, 22, 2.5, 8.0, 4)
    for o in (t0, t1):
        m.add(1, turn(o, 0, 0, 0, 1.7))
    m.add(2, turn(t2, 0, 0, 0, 1.7), "roofs")
    m.add(2, _ring_arc("ring_roof", R_W + 1.6, R_W + 8.6, 0.5, 8.6, TILE))
    m.add(2, _ring_arc("store_roof", R_W + 8.6, R_OUT - 3.6, 0.6, 8.6, shade(TILE, -0.06)))
    hr = MB()
    for (x0, y0), (x1, y1) in zip(hexp, hexp[1:] + hexp[:1]):
        mx, my, a = (x0 + x1) / 2, (y0 + y1) / 2, math.atan2(y1 - y0, x1 - x0)
        hr.box(mx * 0.98, my * 0.98, 7.2, 46.5, 5.0, 0.5, a)
    m.add(2, hr.build("hex_roof", TILE))
    specs = [(28, 7, *polar(84, a), 0.45, a + math.pi / 2, "merchant") for a in (0.3, 1.5, 2.6, 3.7, 4.6)]
    m.add(2, ships("merchantmen", specs, HULL))
    return m


def cothon_silted():
    m = Model("cothon-silted")
    m.add(0, cylinder("ground", R_OUT + 1.5, 0.3, (0, 0, 0), EARTH, verts=64), "lagoon")
    m.add(0, cylinder("marsh", R_W + 14, 0.25, (0, 0, 0.2), GRASS, verts=48))
    m.add(0, cylinder("pool", 96, 0.25, (0, 0, 0.3), WAT, verts=48))
    m.add(0, hill_cap("island", 100, 96, 2.2, top=0.6, seed=21, color=EARTH_D, jitter=0.1))
    # the bank: low mounds where the sheds stood, with a few stumps of walls
    m.add(1, ell_ring("bank", R_W + 12, R_W + 12, R_OUT - 2, R_OUT - 2, 2.0, 0.3, EARTH_D, n=60), "ruins")
    r = random.Random(3)
    mb = MB()
    for k in range(44):
        a = r.uniform(0, math.tau)
        x, y = polar(r.uniform(R_W + 16, R_OUT - 6), a)
        mb.box(x, y, 1.8, r.uniform(2, 6), 1.0, r.uniform(0.8, 2.8), a)
    for k in range(10):
        a = r.uniform(0, math.tau)
        x, y = polar(r.uniform(5, 30), a)
        mb.box(x, y, 2.0, r.uniform(2, 5), 1.0, r.uniform(1, 3), a)
    m.add(1, mb.build("stumps", STONE))
    m.add(1, reeds("reeds", 260, R_W + 12, R_W + 12, r_min=0.84))
    m.add(1, reeds("island_reeds", 60, 52, 50, seed=7, r_min=0.8))
    m.add(2, trees("figs", [(0, 6, 2.2), (-12, -8, 1.6), (130, 40, 2.3), (-120, 70, 2.3)], 3.4, OLIVE), "life")
    m.add(2, J([flat_house("hut", 6, 5, 3, (128, -40, 2.3), WHITE, door_face="W")], "hut"))
    m.add(2, ships("boats", [(7, 2.2, 70, 50, 0.5, 0.8, "boat"), (6, 2.0, -60, -66, 0.5, 2.0, "boat")], HULL, masts=False))
    return m


# ================================================================ the merchant harbour
HB_W, HB_D = 240.0, 330.0


def commercial_harbour():
    m = Model("commercial-harbour")
    m.add(0, box("ground", 300, 400, 0.3, (0, 0, 0), EARTH), "basin")
    m.add(0, box("water", HB_W, HB_D, 0.3, (0, 0, 0.22), WAT))
    # quays round the basin
    qz, qh = 0.3, 1.2
    mb = MB()
    for (x, y, w, d) in [(0, -HB_D / 2 - 6, HB_W + 24, 12), (0, HB_D / 2 + 6, HB_W + 24, 12), (-HB_W / 2 - 6, 0, 12, HB_D), (HB_W / 2 - 4 + 10, 20, 12, HB_D - 40)]:
        mb.box(x, y, qz, w, d, qh)
    m.add(0, mb.build("quays", SAND_D))
    # the channel to the sea at the south-east corner, closed by a chain between two towers
    m.add(0, box("channel", 22, 70, 0.32, (HB_W / 2 + 6, -HB_D / 2 + 10, 0.2), WAT))
    m.add(1, J([box(f"chain_tower{s}", 9, 9, 13, (HB_W / 2 + 6 + s * 16, -HB_D / 2 - 20, 0.3), SAND) for s in (-1, 1)] +
               [cavetto(f"chain_cav{s}", 9, 9, 13.3, 0.8, SAND_D, HB_W / 2 + 6 + s * 16, -HB_D / 2 - 20) for s in (-1, 1)] +
               [box("chain", 24, 0.5, 0.5, (HB_W / 2 + 6, -HB_D / 2 - 20, 1.0), BRONZE)], "towers"), "stores")
    # warehouses along the long sides
    sw, sd = MB(), MB()
    for side in (-1, 1):
        x = side * (HB_W / 2 + 21)
        for k, y in enumerate(lin(-135, 160, 9) if side < 0 else lin(-100, 160, 8)):
            sw.box(x, y, qz, 16, 30, 7.0)
            for dy in (-8, 0, 8):
                sd.box(x - side * 8.05, y + dy, qz, 0.3, 2.6, 3.4)
    m.add(1, sw.build("warehouses", STUC))
    for side in (-1, 1):
        ys = lin(-150, 175, 34) if side < 0 else lin(-112, 175, 30)
        m.add(1, col_row(f"quay_cols{side}", [(side * (HB_W / 2 + 11.5), y) for y in ys], qz, 5.0, 0.3, "i", STUC))
        m.add(2, box(f"quay_portico_roof{side}", 4.0, ys[-1] - ys[0] + 4, 0.4, (side * (HB_W / 2 + 11.5), (ys[0] + ys[-1]) / 2, qz + 5.0), TILE))
    m.add(1, sd.build("doors", DARK))
    # the double wall at the north end with the gate to the naval harbour
    m.add(1, J([box("nwall_a", 76, 3, 9, (-113, HB_D / 2 + 18, 0.3), SAND), box("nwall_b", 196, 3, 9, (52, HB_D / 2 + 18, 0.3), SAND),
                box("nwall_c", 76, 3, 9, (-113, HB_D / 2 + 24, 0.3), SAND_D), box("nwall_d", 196, 3, 9, (52, HB_D / 2 + 24, 0.3), SAND_D),
                box("ngate_a", 9, 15, 12, (-71, HB_D / 2 + 21, 0.3), SAND_D), box("ngate_b", 9, 15, 12, (-49, HB_D / 2 + 21, 0.3), SAND_D),
                box("ngate_w", 14, 32, 0.32, (-60, HB_D / 2 + 16, 0.2), WAT)], "north_wall"))
    rr, ro = MB(), MB()
    for side in (-1, 1):
        x = side * (HB_W / 2 + 21)
        for y in (lin(-135, 160, 9) if side < 0 else lin(-100, 160, 8)):
            rr.box(x, y, qz + 7.0, 16.6, 30.6, 0.5)
            rr.box(x, y, qz + 7.5, 15.6, 29.6, 0.6)
    m.add(2, rr.build("roofs", STUC_D), "ships")
    r = random.Random(2)
    specs = [(26, 7.5, -HB_W / 2 + 6, y, 0.45, math.pi / 2, "merchant") for y in (-110, -60, 20, 90)]
    specs += [(24, 7.0, HB_W / 2 - 6, y, 0.45, -math.pi / 2, "merchant") for y in (-40, 60, 130)]
    specs += [(28, 8.0, x, y, 0.45, r.uniform(0, 3), "merchant") for x, y in [(-30, -40), (40, 60), (10, 130)]]
    m.add(2, ships("ships", specs, HULL))
    mb = MB()
    for k in range(90):
        x, y = r.uniform(-HB_W / 2 - 9, -HB_W / 2 - 2), r.uniform(-150, 150)
        mb.box(x, y, qz + qh, 1.2, 1.2, 1.0)
        x, y = r.uniform(HB_W / 2 + 0, HB_W / 2 + 10), r.uniform(-100, 150)
        mb.cyl(x, y, qz + qh, 0.5, 1.1, n=6)
    m.add(2, mb.build("cargo", OCHRE))
    return m


def harbour_silted():
    m = Model("harbour-silted")
    m.add(0, box("ground", 300, 400, 0.3, (0, 0, 0), EARTH), "lagoon")
    m.add(0, box("marsh", 250, 340, 0.25, (0, 0, 0.2), GRASS))
    m.add(0, ell_disc("pool", 70, 140, 0.25, 0.3, WAT, n=36))
    m.add(1, reeds("reeds", 420, 118, 168, seed=4, r_min=0.5), "ruins")
    m.add(1, rubble("quay_stones", 60, 250, 350, seed=5, color=SAND_D, size=2.4))
    m.add(2, trees("tamarisks", [(-120, 120, 0.3), (110, -150, 0.3), (130, 40, 0.3), (-130, -60, 0.3)], 3.0, OLIVE), "life")
    m.add(2, ships("boats", [(7, 2.2, 20, 40, 0.5, 1.2, "boat"), (6, 2.0, -30, -80, 0.5, 2.6, "boat")], HULL, masts=False))
    return m


# ================================================================ the Tophet
def tophet():
    m = Model("tophet")
    m.add(0, box("ground", 70, 90, 0.3, (0, 0, 0), EARTH), "precinct")
    # terraces of successive levels of urns
    m.add(0, box("terrace_old", 60, 34, 0.9, (0, 20, 0.3), EARTH_D))
    m.add(0, box("terrace_mid", 60, 26, 0.6, (0, -9, 0.3), shade(EARTH, -0.04)))
    wall = [(-33, -36), (-33, 43), (33, 43), (33, -36), (8, -36)]
    m.add(0, wall_run("enclosure", wall, 1.8, 0.8, (0, 0, 0.3), SAND, towers=False, merlon=None))
    m.add(0, wall_run("enclosure2", [(-4, -36), (-33, -36)], 1.8, 0.8, (0, 0, 0.3), SAND, towers=False, merlon=None))
    r = random.Random(17)
    stel, urns, pale = MB(), MB(), MB()
    zones = [(-27, 27, 6, 34, 1.2), (-27, 27, -20, 2, 0.9), (-27, 27, -32, -24, 0.3)]
    for k in range(300):
        x0, x1, y0, y1, z = zones[k % 3]
        x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        if abs(x) < 5 and y < -14:
            continue
        h = r.uniform(1.0, 2.2)
        w = r.uniform(0.45, 0.7)
        a = r.uniform(-0.25, 0.25)
        c, s = math.cos(a), math.sin(a)
        # a thin slab with a pointed top
        prof = [(-w / 2, 0), (w / 2, 0), (w / 2, h * 0.8), (0, h), (-w / 2, h * 0.8)]
        t = 0.16
        v = [(x + px * c - (-t / 2) * s, y + px * s + (-t / 2) * c, z + pz) for px, pz in prof] + [(x + px * c - (t / 2) * s, y + px * s + (t / 2) * c, z + pz) for px, pz in prof]
        (pale if r.random() < 0.35 else stel).raw(v, [(0, 1, 2, 3, 4), (9, 8, 7, 6, 5), (0, 5, 6, 1), (1, 6, 7, 2), (2, 7, 8, 3), (3, 8, 9, 4), (4, 9, 5, 0)])
        if r.random() < 0.5:
            urns.cyl(x + r.uniform(-0.8, 0.8), y + r.uniform(0.4, 1.0), z, 0.28, 0.5, n=6, r_top=0.18)
    m.add(1, stel.build("stelae", SAND), "stelae")
    m.add(1, pale.build("stelae_lime", STUC))
    m.add(1, urns.build("urns", OCHRE))
    # a small shrine (the so-called chapel) and a sacred tree
    m.add(2, J([box("shrine", 6, 6, 4.2, (-18, -26, 0.3), STUC), cavetto("shrine_cav", 6, 6, 4.5, 0.9, STUC_D, -18, -26),
                box("shrine_door", 1.6, 0.3, 2.6, (-18, -29.05, 0.3), DARK), box("altar", 2.4, 1.6, 1.1, (-18, -32, 0.3), SAND_D)], "shrine"), "shrine")
    m.add(2, trees("trees", [(24, -28, 0.3), (-26, 38, 1.2)], 3.0))
    return m


# ================================================================ the Punic sea wall
def sea_wall():
    m = Model("sea-wall")
    m.add(0, box("ground", 30, 240, 0.3, (0, 0, 0), EARTH), "wall")
    m.add(0, box("beach", 8, 240, 0.25, (11, 0, 0.05), "#DCCBA2"))
    L = 240
    m.add(0, J([box("wall_s", 5.5, L / 2 - 9, 11, (-1.5, -L / 4 - 4.5, 0.3), SAND), box("wall_n", 5.5, L / 2 - 9, 11, (-1.5, L / 4 + 4.5, 0.3), SAND)], "curtain"))
    mb = MB()
    for y in (-108, -72, -36, 36, 72, 108):
        mb.box(3.5, y, 0.3, 9, 10, 14)
    m.add(1, mb.build("towers", SAND_D), "towers")
    m.add(1, J([box(f"gate_t{s}", 10, 9, 15, (2.0, s * 9.5, 0.3), SAND_D) for s in (-1, 1)] +
               [box("gate_lintel", 9, 10, 3.0, (-1.0, 0, 9.3), SAND), box("gate_opening", 0.4, 6, 7.5, (6.6, 0, 0.3), DARK),
                box("gate_way", 6, 10, 0.4, (-1.0, 0, 0.3), PAVE)], "gate"))
    m.add(1, J([cavetto(f"cav{y}", 9, 10, 14.3, 1.0, SAND, 3.5, y) for y in (-108, -72, -36, 36, 72, 108)] +
               [cavetto(f"gcav{s}", 10, 9, 15.3, 1.0, SAND, 2.0, s * 9.5) for s in (-1, 1)], "cornices"))
    mm = MB()
    for y in lin(-116, 116, 60):
        if abs(y) > 15:
            mm.box(-1.5, y, 11.3, 4.8, 1.2, 1.3)
    m.add(2, mm.build("merlons", SAND_D), "houses")
    # the houses of the seaside quarter behind the wall
    mw, mr, md = MB(), MB(), MB()
    r = random.Random(8)
    for k, y in enumerate(lin(-108, 108, 9)):
        if abs(y) < 14:
            continue
        punic_house(mw, mr, md, -10.5, y, 0.3, 8.5, r.uniform(16, 22), r.choice([6.0, 7.5, 9.0]), 0.0, court=False)
    m.add(2, mw.build("houses", STUC))
    m.add(2, md.build("openings", DARK))
    m.add(2, box("street", 4, 240, 0.32, (-5.0, 0, 0.0), PAVE))
    sl = MB()
    for y in (-108, -72, -36, 36, 72, 108):
        for dy in (-2.5, 2.5):
            sl.box(8.05, y + dy, 6.0, 0.3, 0.8, 2.0)
        for dx, dy in ((-3, -4), (3, -4), (-3, 4), (3, 4)):
            sl.box(3.5 + dx, y + dy, 15.3, 1.6, 1.6, 1.4)
    m.add(2, sl.build("slits_merlons", SAND_D))
    m.add(2, ships("boats", [(9, 2.6, 12, y, 0.3, math.pi / 2 + 0.2, "boat") for y in (-90, -50, 60, 95)], HULL, masts=False))
    return m


# ================================================================ the Hannibal quarter
def hannibal_quarter():
    m = Model("hannibal-quarter")
    # the slope rises toward +Y (up to the Byrsa summit): three terraces
    m.add(0, box("t0", 120, 80, 0.3, (0, 0, 0), EARTH), "terraces")
    m.add(0, box("t1", 120, 52, 1.8, (0, 14, 0.3), EARTH_D))
    m.add(0, box("t2", 120, 26, 1.8, (0, 27, 2.1), shade(EARTH_D, -0.04)))
    # stepped streets between the blocks
    m.add(0, J([turn(box(f"street_flat{x}", 5.5, 80, 0.12, (0, 0, 0.3), PAVE), 0, x, 0, 0) for x in (-21, 21)] +
               [turn(steps_front(f"st{x}_{y}", 5.5, 1.8, 7, y, z, PAVE, tread=1.6), 0, x, 0, 0) for x in (-21, 21) for y, z in ((-12, 0.3), (14, 2.1))], "stairs"))
    mw, mr, md = MB(), MB(), MB()
    r = random.Random(12)
    zs = {-1: 0.3, 0: 2.1, 1: 3.9}
    for bx in (-42, 0, 42):
        for row, y in ((-1, -28), (0, 0), (1, 27)):
            for k, xo in enumerate((-8.5, 8.5)):
                w, d = 16.0, r.uniform(18, 24)
                punic_house(mw, mr, md, bx + xo, y, zs[row], w, d, r.choice([6.5, 7.0, 8.0]), 0.0, court=True)
    m.add(1, mw.build("houses", STUC), "houses")
    m.add(1, mr.build("floors", REDF))
    m.add(1, md.build("openings", DARK))
    # roof terraces: stairs heads, awnings, a few pots and a fig tree
    m.add(2, trees("figs", [(-21, -36, 0.3), (21, 8, 2.1), (55, -36, 0.3)], 2.6))
    return m


# ================================================================ the Juno hill necropolis
def juno_necropolis():
    m = Model("juno-necropolis")
    m.add(0, hill_cap("hill", 80, 60, 4.0, top=0.7, seed=31, color=ROCK, jitter=0.06), "hill")
    m.add(0, hill_cap("grass", 54, 40, 0.3, top=0.95, seed=32, color=GRASS, jitter=0.04))
    r = random.Random(33)
    sh, sl, mk = MB(), MB(), MB()
    pts = [(x, y) for x in lin(-23, 23, 8) for y in lin(-15, 15, 5)]
    for k, (x, y) in enumerate(pts):
        x += r.uniform(-1.5, 1.5)
        y += r.uniform(-1.5, 1.5)
        if r.random() < 0.5:
            sh.box(x, y, 4.0, 2.4, 3.6, 0.35)          # open shaft
            sl.box(x + 2.6, y, 4.0, 1.0, 3.8, 0.6)      # cover slabs set aside
        else:
            sl.box(x, y, 4.0, 3.0, 4.2, 0.5)            # sealed shaft
        if r.random() < 0.6:
            mk.box(x - 1.8, y + 2.2, 4.0, 0.7, 0.4, r.uniform(1.0, 1.8))
    m.add(1, sh.build("shafts", DARK), "tombs")
    m.add(1, sl.build("slabs", SAND_D))
    m.add(1, mk.build("markers", SAND))
    m.add(2, J([box("chapel", 5, 5, 3.6, (0, 22, 3.5), STUC), cavetto("chapel_cav", 5, 5, 7.1, 0.8, STUC_D, 0, 22), box("chapel_door", 1.4, 0.3, 2.2, (0, 19.45, 3.5), DARK)], "chapel"), "chapel")
    m.add(2, trees("olives", [(-30, 20, 1.0), (30, -18, 1.0), (32, 16, 1.0), (-34, -12, 0.5)], 3.0))
    m.add(2, reeds("scrub", 70, 38, 28, seed=34, r_min=0.75))
    m.add(2, rubble("stones", 60, 60, 40, seed=35, color=SAND_D, size=0.9, z=4.0))
    return m


# ================================================================ the Antonine Baths (hero)
BZ = 8.0     # height of the basement: the main floor stands on it


def antonine_baths():
    m = Model("antonine-baths")
    m.add(0, box("terrace", 204, 10, 1.0, (0, -50, 0), PAVE), "basement")
    m.add(0, box("basement", 196, 92, BZ, (0, 0, 0), STONE))
    m.add(0, arcade("bas_s", 186, 5.5, 28, (0, -46.05, 0.6), "S", DARK, pointed=False))
    m.add(0, arcade("bas_n", 186, 5.5, 28, (0, 46.05, 0.6), "N", DARK, pointed=False))
    m.add(0, arcade("bas_w", 84, 5.5, 12, (-98.05, 0, 0.6), "W", DARK, pointed=False))
    m.add(0, arcade("bas_e", 84, 5.5, 12, (98.05, 0, 0.6), "E", DARK, pointed=False))
    m.add(0, box("floor", 194, 90, 0.4, (0, 0, BZ), PAVE))
    z = BZ + 0.4
    # ---- stage 1: walls of the halls
    s1 = []
    # frigidarium: the great cold hall in the middle, under three cross vaults
    s1 += [box("frig", 58, 28, 21, (0, 4, z), CONC),
           box("frig_band", 58.6, 28.6, 0.8, (0, 4, z + 12), shade(CONC, -0.05))]
    for s in (-1, 1):
        s1 += [box(f"pool{s}", 16, 22, 15, (s * 37, 4, z), shade(CONC, 0.03))]
    # caldarium facing the sea, with tepidaria and sudatoria either side
    cal = cylinder("cald", 15, 19, (0, -31, z), CONC, verts=8)
    cal.rotation_euler[2] = math.pi / 8
    s1 += [bake(cal)]
    for s in (-1, 1):
        s1 += [box(f"tep{s}", 18, 18, 15, (s * 25, -30, z), CONC)]
        sud = cylinder(f"sud{s}", 8.5, 13, (s * 45, -33, z), CONC, verts=8)
        sud.rotation_euler[2] = math.pi / 8
        s1 += [bake(sud)]
    # halls and the open-air swimming pool on the landward side
    s1 += [box("natatio_rim", 48, 18, 1.0, (0, 33, z), MARB), box("natatio", 44, 14, 0.3, (0, 33, z + 0.75), WAT)]
    for s in (-1, 1):
        s1 += [box(f"hall{s}", 30, 22, 15, (s * 42, 32, z), CONC)]
    m.add(1, J(s1, "halls"), "halls")
    # windows and doors
    mb = MB()
    for x in (-18.5, 0, 18.5):
        for yy in (-10.05, 18.05):
            mb.box(x, yy, z + 3, 4.5, 0.4, 7.5)
    for s in (-1, 1):
        for x in (-6, 0, 6):
            mb.box(s * 25 + x, -39.05, z + 2.5, 2.8, 0.4, 6.5)
        for y in (26, 38):
            mb.box(s * 42 + s * 15.05, y, z + 2.5, 0.4, 3.0, 6.5)
    for k in range(5):
        a = -math.pi / 2 + (k - 2) * math.pi / 4
        x, y = 13.9 * math.cos(a), -31 + 13.9 * math.sin(a)
        mb.box(x, y, z + 4, 3.6, 0.6, 9, a + math.pi / 2)
    m.add(1, mb.build("openings", DARK))
    # palaestrae at both ends
    for s in (-1, 1):
        m.add(1, box(f"pal_floor{s}", 36, 84, 0.3, (s * 77, 0, z), shade(PAVE, 0.03)))
        m.add(1, turn(court(f"palaestra{s}", 36, 84, 6, 6.5, 0.4, 5.2, "d", MARB, TILE), 0, s * 77, 0, z))
    # the entrance portico on the landward side, colonnades round the swimming pool, stairs up from the sea terrace
    m.add(1, copies(column("pc", 0, 0, 0, 9.0, 0.5, "corinthian", MARB, flutes=10), [(x, 44.2, z) for x in lin(-54, 54, 19)], "entrance_portico"))
    m.add(1, copies(column("nc", 0, 0, 0, 5.5, 0.32, "corinthian", MARB, flutes=10), [(x, y, z + 1.0) for x in lin(-22, 22, 7) for y in (25.0, 41.0)], "natatio_cols"))
    for s in (-1, 1):
        m.add(1, turn(steps_front(f"sea_stair{s}", 7, BZ, 14, 0, 0, shade(STONE, 0.05), tread=0.55), 0, s * 52, -46.0, 0))
    # ---- stage 2: vaults, domes, roofs and windows in the lunettes
    VT = "#B98063"     # tiles over the vaults
    s2 = [half_cyl_x("frig_vault", 14.2, 58.6, (0, 4, z + 21), VT, verts=16),
          box("frig_cornice", 59.4, 29.4, 0.9, (0, 4, z + 20.4), shade(CONC, 0.06))]
    for x in (-19, 0, 19):
        s2.append(half_cyl_y(f"frig_cross{x}", 9.6, 28.8, (x, 4, z + 21), shade(VT, -0.04), verts=14))
    for x in (-19, 0, 19):
        for yy, rz in ((-10.1, 0.0), (18.1, math.pi)):
            s2.append(thermal_window(f"therm{x}_{yy}", 7.2, 0.8, (x, yy, z + 21.3), DARK, CONC, rz))
    for s in (-1, 1):
        s2 += [half_cyl_y(f"pool_vault{s}", 8.2, 22.4, (s * 37, 4, z + 15), VT, verts=12),
               half_cyl_x(f"tep_vault{s}", 9.2, 18.4, (s * 25, -30, z + 15), VT, verts=12),
               dome(f"sud_dome{s}", 8.8, (s * 45, -33, z + 13), shade(CONC, 0.06), squash=0.7, segments=16, rings=6),
               half_cyl_x(f"hall_vault{s}", 11.2, 30.4, (s * 42, 32, z + 15), VT, verts=12),
               box(f"hall_cornice{s}", 30.8, 22.8, 0.7, (s * 42, 32, z + 14.5), shade(CONC, 0.06)),
               box(f"tep_cornice{s}", 18.8, 18.8, 0.7, (s * 25, -30, z + 14.5), shade(CONC, 0.06)),
               thermal_window(f"tep_therm{s}", 6.0, 0.8, (s * 25, -39.1, z + 15.2), DARK, CONC, 0.0),
               thermal_window(f"hall_therm{s}", 7.2, 0.8, (s * 57.1, 32, z + 15.2), DARK, CONC, math.pi / 2 * s),
               box(f"portico_roof{s}", 54, 5.4, 0.6, (s * 27, 43.2, z + 10.2), TILE)]
    s2 += [dome("cald_dome", 15.6, (0, -31, z + 19), shade(CONC, 0.07), squash=0.62, segments=24, rings=8),
           cylinder("cald_drum", 15.4, 1.0, (0, -31, z + 18.5), shade(CONC, 0.03), verts=24),
           cylinder("cald_oculus", 2.2, 0.6, (0, -31, z + 19 + 15.6 * 0.62 - 0.3), DARK, verts=10)]
    s2 += [statue(f"statue{k}", x, -44.0, BZ + 0.4, 3.0, BRONZE) for k, x in enumerate((-60, -20, 20, 60))]
    s2 += [statue(f"nstatue{k}", x, 33, z + 1.0, 2.4, MARB) for k, x in enumerate((-26, 26))]
    m.add(2, J(s2, "vaults"), "vaults")
    return m


def antonine_baths_ruin():
    m = Model("antonine-baths-ruin")
    m.add(0, box("sand", 204, 110, 0.4, (0, 0, 0), "#DCCBA2"), "basement")
    # the vaulted basement, broken off at uneven heights, its rooms open to the sky
    r = random.Random(41)
    mb = MB()
    for x in lin(-96, 96, 17):
        mb.box(x, 0, 0, 2.0, 90, r.uniform(3.5, 7.5))
    for y in lin(-44, 44, 5):
        mb.box(0, y, 0, 194, 2.0, r.uniform(3.0, 6.5))
    m.add(0, mb.build("walls", STONE))
    m.add(1, J([half_cyl_x(f"vault{k}", 5.5, r.uniform(10, 24), (x, y, 5.5), shade(STONE, -0.04), verts=10) for k, (x, y) in enumerate([(-60, -22), (-30, 22), (36, -22), (66, 22), (6, 0)])], "vaults"), "vaults")
    m.add(1, rubble("blocks", 140, 190, 100, seed=42, color=STONE, size=2.4))
    m.add(2, J([cyl_x(f"col{k}", 0.75, 11, (x, y, 0.75), GRAN, verts=10) for k, (x, y) in enumerate([(-10, 6), (14, -4), (-24, 20)])], "fallen_columns"), "columns")
    m.add(2, rubble("marble", 50, 120, 60, seed=43, color=MARB, size=1.4))
    m.add(2, J([box(f"dune{k}", w, d, h, (x, y, 0), "#D8C79E") for k, (x, y, w, d, h) in enumerate([(-80, -40, 40, 20, 2.2), (60, -46, 60, 14, 1.8)])], "dunes"))
    return m


# ================================================================ entertainment
def amphitheatre():
    m = Model("amphitheatre")
    AX, AY, OX, OY = 32.5, 18.5, 60.0, 47.0
    m.add(0, ell_disc("arena", AX, AY, 0.4, 0.0, "#D9C6A0"), "arena")
    m.add(0, ell_ring("podium", AX, AY, AX + 1.5, AY + 1.5, 4.0, 0.0, MARB, n=48))
    rows = 12
    seats = []
    for k in range(rows):
        t0, t1 = k / rows, (k + 1) / rows
        rx0, ry0 = AX + 1.5 + (OX - 3 - AX - 1.5) * t0, AY + 1.5 + (OY - 3 - AY - 1.5) * t0
        rx1, ry1 = AX + 1.5 + (OX - 3 - AX - 1.5) * t1, AY + 1.5 + (OY - 3 - AY - 1.5) * t1
        seats.append(ell_ring(f"row{k}", rx0, ry0, rx1, ry1, 4.5 + 1.45 * (k + 1), 0.0, MARB if k % 2 else STONE, n=48))
    m.add(1, J(seats, "cavea"), "cavea")
    m.add(1, ell_ring("facade", OX - 3, OY - 3, OX, OY, 24, 0.0, STONE, n=56), "facade")
    for tier, z in enumerate((1.0, 8.6, 16.2)):
        m.add(2, ring_of(lambda: arch_panel("p", 3.0, 5.6, (0, 0, 0), "S", DARK, pointed=False, depth=0.4), 44, OX + 0.05, OY + 0.05, z, f"arches{tier}"), "arcades")
    m.add(2, ell_ring("cornice1", OX, OY, OX + 0.6, OY + 0.6, 0.6, 7.8, shade(STONE, 0.05), n=56))
    m.add(2, ell_ring("cornice2", OX, OY, OX + 0.6, OY + 0.6, 0.6, 15.4, shade(STONE, 0.05), n=56))
    m.add(2, ell_ring("attic", OX - 0.2, OY - 0.2, OX + 0.4, OY + 0.4, 1.6, 23.2, shade(STONE, 0.07), n=56))
    return m


def amphitheatre_ruin():
    m = Model("amphitheatre-ruin")
    AX, AY, OX, OY = 32.5, 18.5, 60.0, 47.0
    m.add(0, ell_disc("arena", AX, AY, 0.3, 0.0, EARTH), "arena")
    m.add(0, ell_ring("podium", AX, AY, AX + 1.5, AY + 1.5, 3.0, 0.0, STONE, n=48))
    m.add(0, ell_disc("cellar", 12, 2.5, 0.35, 0.05, DARK, n=16))
    m.add(1, ell_ring("mound", AX + 1.5, AY + 1.5, OX - 6, OY - 6, 4.5, 0.0, GRASS, n=48), "mound")
    r = random.Random(51)
    mb = MB()
    for k in range(56):
        a = math.tau * k / 56
        if r.random() < 0.45:
            continue
        x, y = (OX - 2) * math.cos(a), (OY - 2) * math.sin(a)
        mb.box(x, y, 0, 3.6, 2.5, r.uniform(2.0, 7.5), a + math.pi / 2)
    m.add(1, mb.build("piers", STONE))
    m.add(2, rubble("stones", 80, 120, 94, seed=52, color=STONE, size=1.8), "ruins")
    return m


def theatre():
    m = Model("theatre")
    CY, R0, R1 = -12.0, 11.0, 49.0
    m.add(0, box("ground", 104, 26, 0.3, (0, -24.5, 0), PAVE), "cavea")
    m.add(0, cavea_rows("cavea", 0, CY, R0, R1 - 2.5, 0.5, 15.0, 16, colors=(MARB, shade(MARB, -0.06))))
    m.add(0, cylinder("orchestra", R0, 0.35, (0, CY, 0), "#C9B8A0", verts=24))
    o, _ = ellipse_pts(R1, R1, 40, math.pi, 0.0)
    i, _ = ellipse_pts(R1 - 2.5, R1 - 2.5, 40, math.pi, 0.0)
    m.add(1, ring_extrude("outer", o, i, 17.5, (0, CY, 0), STONE, closed=False), "stage")
    m.add(1, shift(ring_of(lambda: arch_panel("p", 2.8, 5.0, (0, 0, 0), "S", DARK, pointed=False, depth=0.4), 30, R1 + 0.05, R1 + 0.05, 1.0, "arches",
                           skip=lambda i, a: math.sin(a) < 0.05), 0, CY, 0))
    m.add(1, box("pulpitum", 66, 6, 1.6, (0, CY - 3, 0.3), STONE))
    m.add(1, box("scaena", 72, 5, 19, (0, CY - 8.5, 0.3), STONE))
    m.add(1, box("postscaenium", 76, 10, 13, (0, CY - 16, 0.3), shade(STONE, -0.05)))
    for s in (-1, 1):
        m.add(1, box(f"parascenium{s}", 14, 18, 15, (s * 44, CY - 9, 0.3), shade(STONE, -0.03)))
    m.add(2, col_row("frons_cols1", [(x, CY - 5.6) for x in lin(-32, 32, 14)], 1.9, 7.6, 0.42, "d", MARB), "frons")
    m.add(2, col_row("frons_cols2", [(x, CY - 5.6) for x in lin(-32, 32, 14)], 10.1, 6.4, 0.36, "d", "#C9A9A0"))
    m.add(2, J([box(f"ent{k}", 70, 1.8, 0.7, (0, CY - 5.6, zz), MARB) for k, zz in enumerate((9.4, 16.4))] +
               [box(f"door{k}", 4 if k == 1 else 3, 0.3, 6, (x, CY - 6.05, 1.9), DARK) for k, x in enumerate((-16, 0, 16))], "frons_ent"))
    m.add(2, box("stage_roof", 72, 9, 0.6, (0, CY - 10, 19.3), TILE))
    return m


def odeon():
    m = Model("odeon")
    CY, R = -10.0, 46.0
    m.add(0, box("ground", 95, 80, 0.3, (0, 0, 0), PAVE), "walls")
    o, _ = ellipse_pts(R + 1.2, R + 1.2, 36, math.pi, 0.0)
    i, _ = ellipse_pts(R - 1.2, R - 1.2, 36, math.pi, 0.0)
    m.add(0, ring_extrude("curve", o, i, 20.0, (0, CY, 0.3), STONE, closed=False))
    m.add(0, box("facade", 95, 5, 22, (0, -37.5, 0.3), STONE))
    for s in (-1, 1):
        m.add(0, box(f"side{s}", 2.4, 30, 20, (s * (R + 0.0), -24, 0.3), STONE))
    m.add(1, shift(ring_of(lambda: arch_panel("p", 2.6, 4.5, (0, 0, 0), "S", DARK, pointed=False, depth=0.4), 26, R + 1.25, R + 1.25, 12.0, "windows",
                           skip=lambda i, a: math.sin(a) < 0.08), 0, CY, 0), "windows")
    m.add(1, shift(ring_of(lambda: arch_panel("q", 3.0, 6.0, (0, 0, 0), "S", DARK, pointed=False, depth=0.4), 26, R + 1.25, R + 1.25, 1.2, "doors",
                           skip=lambda i, a: math.sin(a) < 0.08), 0, CY, 0))
    m.add(1, arcade("facade_doors", 70, 7.5, 7, (0, -40.05, 0.3), "S", DARK, pointed=False))
    m.add(1, col_row("facade_cols", [(x, -41.2) for x in lin(-40, 40, 9)], 0.3, 10, 0.55, "d", MARB))
    m.add(1, box("facade_ent", 86, 2.6, 1.2, (0, -41.2, 10.3), MARB))
    # the timber roof: half a low cone over the curve, a lean-to over the stage
    n = 18
    zr, za = 20.3, 30.0
    rim = [(R + 1.8) * math.cos(math.pi * k / n) for k in range(n + 1)]
    v = [((R + 1.8) * math.cos(math.pi * k / n), CY + (R + 1.8) * math.sin(math.pi * k / n), zr) for k in range(n + 1)] + [(0, CY, za)]
    f = [(k, k + 1, n + 1) for k in range(n)]
    v2 = [(-R - 1.8, CY, zr), (R + 1.8, CY, zr), (R + 1.8, -40.5, zr + 2.0), (-R - 1.8, -40.5, zr + 2.0), (0, CY, za)]
    roof = MB()
    roof.raw(v, f)
    roof.raw([(-R - 1.8, CY, zr), (R + 1.8, CY, zr), (R + 1.8, -40.5, zr + 2.0), (-R - 1.8, -40.5, zr + 2.0), (R + 1.8, CY, za - 1.0), (-R - 1.8, CY, za - 1.0)],
             [(3, 2, 4, 5), (0, 3, 5), (1, 4, 2)])
    m.add(2, roof.build("roof", TILE), "roof")
    m.add(2, mesh_from("roof_back", [(-R - 1.8, CY + 0.05, zr), (R + 1.8, CY + 0.05, zr), (0, CY + 0.05, za)], [(0, 1, 2)], (0, 0, 0), STONE))
    m.add(2, J([statue(f"fst{k}", x, -41.0, 11.5, 2.6, MARB) for k, x in enumerate(lin(-35, 35, 8))], "facade_statues"))
    bt = MB()
    for k in range(13):
        a = math.pi * (k + 0.5) / 13
        x, y = (R + 2.2) * math.cos(a), CY + (R + 2.2) * math.sin(a)
        bt.box(x, y, 0.3, 2.0, 2.4, 14.0, a, taper=0.8)
    m.add(1, bt.build("buttresses", shade(STONE, -0.05)))
    return m


def circus():
    m = Model("circus")
    L, W = 520.0, 90.0
    pts = stadium_pts(L - 20, W - 20)
    mb = MB()
    mb.prism(pts, 0, 0.3)
    m.add(0, mb.build("arena", "#D9C6A0"), "arena")
    for k in range(6):
        ll, ww = L - 20 + 2 * (k + 1) * 1.65, W - 20 + 2 * (k + 1) * 1.65
        m.add(1 if k else 0, stadium_ring(f"stand{k}", ll, ww, 1.7, 1.4 + 1.35 * (k + 1), (0, 0, 0), MARB if k % 2 else STONE))
    m.add(1, stadium_ring("outer", L, W, 1.4, 11.0, (0, 0, 0), STONE), "stands")
    for tier, zz in enumerate((0.8, 6.0)):
        for sgn in (-1, 1):
            m.add(1, arcade(f"arc{tier}_{sgn}", L - 60, 4.2, 70, (-15, sgn * (W / 2 + 0.05), zz), "S" if sgn < 0 else "N", DARK, pointed=False, depth=0.4))
    # the spina with basins, an obelisk and the turning posts
    sp = -10.0
    m.add(1, box("spina", 300, 7, 1.6, (sp, 0, 0.3), STONE))
    m.add(1, J([box(f"basin{k}", 50, 4.6, 0.3, (sp - 105 + k * 70, 0, 1.75), WAT) for k in range(4)], "basins"))
    m.add(2, J([obelisk("obelisk", 2.4, 22, (sp, 0, 1.9), "#9C5B4C")], "obelisk"), "spina")
    for s in (-1, 1):
        m.add(2, J([cylinder(f"meta{s}_{k}", 1.0, 6.5, (sp + s * 156, (k - 1) * 2.4, 0.3), GILT, verts=8, r_top=0.15) for k in range(3)] +
                   [cylinder(f"meta_base{s}", 4.2, 1.8, (sp + s * 156, 0, 0.3), MARB, verts=12)], f"meta{s}"))
    m.add(2, J([statue(f"spina_st{k}", sp + x, 0, 1.9, 3.0, BRONZE) for k, x in enumerate((-120, -60, 60, 120))], "spina_statues"))
    # the starting gates at the flat (west) end
    m.add(2, box("carceres", 8, W - 6, 8.5, (-L / 2 + 7, 0, 0.3), STONE))
    m.add(2, arcade("gates", W - 16, 6.0, 12, (-L / 2 + 11.05, 0, 0.3), "E", DARK, pointed=False))
    for s in (-1, 1):
        m.add(2, box(f"tower{s}", 12, 12, 14, (-L / 2 + 7, s * (W / 2 - 5), 0.3), shade(STONE, -0.04)))
    m.add(2, arch_panel("porta_triumphalis", 6, 9, (L / 2 - 0.5, 0, 0.3), "E", DARK, pointed=False, depth=1.0))
    return m


# ================================================================ water supply
def la_malga(ruined=False):
    m = Model("la-malga-ruin" if ruined else "la-malga")
    m.add(0, box("ground", 130, 105, 0.3, (0, 0, 0), EARTH), "walls")
    N, CW, WT, LEN = 15, 7.3, 1.25, 96.0
    W = N * CW + (N + 1) * WT
    x0 = -W / 2
    y0 = -52.5 + LEN / 2
    walls = MB()
    r = random.Random(61)
    broken = {2, 5, 6, 11} if ruined else set()
    for k in range(N + 1):
        x = x0 + k * (CW + WT) + WT / 2
        h = 6.5 if not ruined else (r.uniform(3.0, 6.5) if (k in broken or k - 1 in broken) else 6.5)
        walls.box(x, y0, 0.3, WT, LEN, h)
    walls.box(0, y0 - LEN / 2 - 0.6, 0.3, W, 1.2, 6.5)
    m.add(0, walls.build("walls", STONE))
    # the distribution gallery across the heads of the tanks
    m.add(0, box("gallery", W, 6, 7.5, (0, 49, 0.3), shade(STONE, -0.04)))
    vaults = []
    for k in range(N):
        if k in broken:
            continue
        x = x0 + WT + k * (CW + WT) + CW / 2
        vaults.append(half_cyl_y(f"vault{k}", CW / 2 + WT / 2, LEN, (x, y0, 6.8), CONC, verts=12))
    m.add(1, J(vaults, "vaults"), "vaults")
    m.add(1, half_cyl_x("gallery_vault", 3.2, W, (0, 49, 7.8), CONC, verts=10))
    # the aqueduct arriving on arches from the west
    bt = MB()
    for y in lin(-48, 40, 12):
        bt.box(-W / 2 - 1.0, y, 0.3, 2.0, 2.4, 5.5, taper=0.8)
        bt.box(W / 2 + 1.0, y, 0.3, 2.0, 2.4, 5.5, taper=0.8)
    m.add(0, bt.build("buttresses", shade(STONE, -0.05)))
    m.add(1, J([box("aq_channel", 3.0, 3.0, 2.2, (-W / 2 - 1.5, 49, 8.0), STONE), box("aq_pier", 3.0, 3.2, 8.0, (-W / 2 - 1.5, 49, 0.3), STONE)], "aqueduct"))
    # inspection shafts on the vaults
    sh = MB()
    for k in range(N):
        if k in broken:
            continue
        x = x0 + WT + k * (CW + WT) + CW / 2
        for y in (-40, -20, 0, 20, 38):
            sh.box(x, y, 6.8 + CW / 2 + 0.3, 1.4, 1.4, 1.2)
            sh.box(x, y, 6.8 + CW / 2 + 1.5, 1.8, 1.8, 0.3)
    m.add(2, sh.build("shafts", STONE), "shafts")
    if ruined:
        mw, mr, md = MB(), MB(), MB()
        for k, (x, y) in enumerate([(-40, -45), (-20, -48), (22, -46), (44, -44)]):
            punic_house(mw, mr, md, x, y, 0.3, 8, 6, 3.2, court=False)
        m.add(2, mw.build("village", WHITE))
        m.add(2, md.build("village_doors", DARK))
        m.add(2, trees("figs", [(-55, -40, 0.3), (0, -46, 0.3), (58, -36, 0.3)], 2.6))
        m.add(2, rubble("fallen", 50, 120, 90, seed=62, color=CONC, size=1.8, z=0.3))
    return m


# ================================================================ late antique
def damous_el_karita():
    m = Model("damous-el-karita")
    m.add(0, box("ground", 150, 70, 0.3, (0, 0, 0), PAVE), "walls")
    # nine-aisled basilica, entrance at -X (west), apse at +X
    bx0, bx1 = -45.0, 20.0
    BL, BW = bx1 - bx0, 45.0
    cx = (bx0 + bx1) / 2
    nave_w, a_w = 9.0, 4.5
    s0 = [box("aisles_out", BL, BW, 7.5, (cx, 0, 0.3), STONE),
          box("aisles_in", BL, nave_w + 4 * a_w, 10.5, (cx, 0, 0.3), shade(STONE, 0.03)),
          box("nave", BL, nave_w, 15.0, (cx, 0, 0.3), shade(STONE, 0.06))]
    m.add(0, J(s0, "basilica"))
    o, _ = ellipse_pts(6.0, 6.0, 12, math.pi, -math.pi / 2)
    mb = MB()
    mb.prism([(x + bx1, y) for x, y in o], 0.3, 11.0)
    m.add(0, mb.build("apse", STONE))
    # atrium in front, the hemicycle and the rotunda beyond the apse
    m.add(0, box("atrium_floor", 28, 44, 0.3, (-61, 0, 0.3), shade(PAVE, 0.04)))
    hem = MB()
    o, _ = ellipse_pts(24, 24, 24, math.pi, -math.pi / 2)
    i, _ = ellipse_pts(21, 21, 24, math.pi, -math.pi / 2)
    m.add(0, ring_extrude("hemicycle_wall", [(x + 32, y) for x, y in o], [(x + 32, y) for x, y in i], 5.0, (0, 0, 0.3), STONE, closed=False))
    m.add(0, box("hemicycle_floor", 18, 40, 0.25, (40, 0, 0.3), shade(PAVE, 0.04)))
    m.add(1, turn(court("atrium", 28, 44, 4.5, 5.0, 0.35, 4.2, "d", MARB, TILE, skip=("E",)), 0, -61, 0, 0.3), "porticoes")
    hc = [(32 + 18 * math.cos(a), 18 * math.sin(a)) for a in lin(-math.pi / 2 + 0.1, math.pi / 2 - 0.1, 15)]
    m.add(1, col_row("hemicycle_cols", hc, 0.3, 4.8, 0.32, "d", MARB))
    m.add(1, J([cylinder("rotunda", 9, 6.0, (65, 0, 0.3), STONE, verts=16), cylinder("rot_door", 2.0, 0.4, (56, 0, 0.3), DARK, verts=6)], "rotunda"))
    win = MB()
    for x in lin(bx0 + 4, bx1 - 4, 9):
        for s in (-1, 1):
            win.box(x, s * (nave_w / 2 + 0.05), 11.0, 1.3, 0.3, 2.6)
            win.box(x, s * (BW / 2 + 0.05), 2.0, 1.2, 0.3, 3.0)
    win.box(bx0 - 0.05, 0, 0.3, 0.3, 4.0, 6.0)
    for s in (-1, 1):
        win.box(bx0 - 0.05, s * 13, 0.3, 0.3, 2.6, 4.5)
    m.add(1, win.build("windows", DARK))
    # roofs
    s2 = [gable("nave_roof", BL, nave_w, 3.6, (cx, 0, 15.3), TILE, 0.3, along="X")]
    for s in (-1, 1):
        y_in, y_mid, y_out = s * nave_w / 2, s * (nave_w / 2 + 2 * a_w), s * BW / 2
        for (ya, yb, za, zb, nm) in ((y_in, y_mid, 10.8, 9.8, "in"), (y_mid, y_out, 7.8, 6.8, "out")):
            v = [(bx0 - 0.3, ya, za), (bx1 + 0.3, ya, za), (bx1 + 0.3, yb + s * 0.4, zb), (bx0 - 0.3, yb + s * 0.4, zb)]
            v += [(x, y, zz + 0.35) for x, y, zz in v]
            s2.append(mesh_from(f"aisle_roof_{nm}{s}", v, [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)], (0, 0, 0), shade(TILE, -0.04 if nm == "out" else 0.0)))
    s2 += [dome("apse_roof", 6.2, (bx1, 0, 11.0), TILE, squash=0.6, segments=16, rings=6),
           dome("rot_dome", 9.4, (65, 0, 6.3), shade(TILE, 0.04), squash=0.55, segments=20, rings=6),
           box("cross_v", 0.4, 0.4, 2.6, (bx0 + 0.6, 0, 18.9), BRONZE), box("cross_h", 0.4, 1.6, 0.4, (bx0 + 0.6, 0, 20.3), BRONZE)]
    m.add(2, J(s2, "roofs"), "roofs")
    m.add(2, trees("cypresses", [(-74, 28, 0.3), (-74, -28, 0.3), (62, 26, 0.3), (62, -26, 0.3)], 1.4, "#5E7A50", "cypress"))
    # graves crowding round the martyrs' church: tomb slabs and mensae
    gr = MB()
    r = random.Random(81)
    for k in range(110):
        x, y = r.uniform(-74, 74), r.choice((-1, 1)) * r.uniform(24.5, 34)
        if 30 < x < 74 and abs(y) < 26:
            continue
        gr.box(x, y, 0.3, 2.2, 1.0, r.uniform(0.3, 0.8), r.uniform(-0.1, 0.1))
    m.add(2, gr.build("graves", STUC_D))
    bt = MB()
    for x in lin(bx0 + 3, bx1 - 3, 8):
        for sg in (-1, 1):
            bt.box(x, sg * (BW / 2 + 0.7), 0.3, 1.4, 1.4, 6.0, taper=0.85)
    m.add(1, bt.build("buttresses", shade(STONE, -0.05)))
    return m


def villa_aviary():
    m = Model("villa-aviary")
    m.add(0, box("terrace", 50, 45, 1.2, (0, 0, 0), STONE), "walls")
    m.add(0, box("garden", 18, 14, 0.3, (0, 2, 1.2), GRASS))
    m.add(0, box("mosaic", 24, 20, 0.12, (0, 2, 1.15), "#C79A6A"))
    rooms = MB()
    for (x, y, w, d, h) in [(0, 16.5, 46, 11, 6.5), (-19.5, -1, 9, 26, 5.5), (19.5, -1, 9, 26, 5.5), (-12, -17, 20, 9, 5.0), (12, -17, 20, 9, 5.0)]:
        rooms.box(x, y, 1.2, w, d, h)
    m.add(0, rooms.build("rooms", STUC))
    pts = [(x, y) for x in lin(-11, 11, 5) for y in (-7, 11)] + [(x, y) for x in (-11, 11) for y in lin(-2.5, 6.5, 3)]
    m.add(1, col_row("peristyle", pts, 1.2, 3.8, 0.24, "d", MARB), "peristyle")
    m.add(1, J([box("tri_door", 4.0, 0.3, 3.2, (0, 10.9, 1.2), DARK), box("front_door", 2.0, 0.3, 2.8, (0, -21.6, 1.2), DARK)], "doors"))
    m.add(1, trees("garden_trees", [(-5, 2, 1.5), (5, 2, 1.5)], 1.6, "#6F8A5C"))
    m.add(1, box("fountain", 3, 3, 0.6, (0, 2, 1.5), WAT))
    roofs = [hip_roof("tri_roof", 46, 11, 3.0, (0, 16.5, 7.7), TILE, ridge=0.6, overhang=0.5)]
    for s in (-1, 1):
        roofs.append(hip_roof(f"wing_roof{s}", 9, 26, 2.4, (s * 19.5, -1, 6.7), TILE, ridge=0.6, overhang=0.4))
        roofs.append(hip_roof(f"front_roof{s}", 20, 9, 2.2, (s * 12, -17, 6.2), TILE, ridge=0.5, overhang=0.4))
    roofs.append(box("portico_roof_n", 26, 3.4, 0.4, (0, 10.6, 5.0), shade(TILE, 0.05)))
    roofs.append(box("portico_roof_s", 26, 3.4, 0.4, (0, -6.6, 5.0), shade(TILE, 0.05)))
    m.add(2, J(roofs, "roofs"), "roofs")
    # the aviary mosaic: birds among scrolls, as coloured panels round the garden
    mo = MB()
    r = random.Random(91)
    for k in range(60):
        a = math.tau * k / 60
        x, y = 10.5 * math.cos(a), 2 + 8.5 * math.sin(a)
        mo.box(x, y, 1.27, 0.8, 0.8, 0.05, a)
    m.add(1, mo.build("mosaic_birds", "#7A8C5A"))
    m.add(1, reeds("shrubs", 24, 8, 6, seed=92, cx=0, cy=2))
    m.add(2, J([box("bath", 8, 8, 4.5, (-19.5, -18.5, 1.2), STUC), dome("bath_dome", 4.2, (-19.5, -18.5, 5.7), shade(STUC, -0.04), squash=0.6, segments=14, rings=5)], "bath"))
    m.add(2, J([box(f"win{k}", 1.0, 0.3, 1.6, (x, -21.6, 3.0), DARK) for k, x in enumerate((-16, -8, 8, 16))], "windows"))
    return m


# ================================================================ after 698
def sidi_bou_said():
    m = Model("sidi-bou-said")
    m.add(0, hill_cap("hill", 90, 70, 6.0, top=0.82, seed=71, color=ROCK, jitter=0.05), "village")
    zt = 6.0
    # zawiya: a court with the saint's domed tomb and a square minaret
    m.add(1, box("zaw_court", 22, 18, 0.3, (6, 6, zt), WHITE), "zawiya")
    m.add(1, wall_run("zaw_wall", [(-5, -3), (-5, 15), (17, 15), (17, -3), (9, -3)], 3.2, 0.7, (0, 0, zt), WHITE, towers=False, merlon=None))
    m.add(1, J([box("tomb", 9, 9, 6, (11, 9, zt), WHITE), box("tomb_door", 1.6, 0.3, 2.6, (11, 4.45, zt), DARK)], "tomb"))
    m.add(1, J([box("minaret", 4, 4, 15, (-2, 12, zt), WHITE), box("min_band", 4.6, 4.6, 0.5, (-2, 12, zt + 12.5), GREEN_T),
                box("min_lantern", 2.6, 2.6, 2.6, (-2, 12, zt + 15), WHITE), box("min_win", 1.0, 0.3, 1.6, (-2, 9.95, zt + 10), DARK)], "minaret"))
    m.add(2, J([dome("tomb_dome", 4.4, (11, 9, zt + 6), WHITE, squash=1.05, segments=16, rings=7),
                cylinder("tomb_drum", 4.6, 0.6, (11, 9, zt + 5.6), WHITE, verts=16),
                cylinder("min_cap", 2.0, 2.0, (-2, 12, zt + 17.6), GREEN_T, verts=4, r_top=0.0)], "domes"), "domes")
    # whitewashed houses on the slope
    mw, mr, md = MB(), MB(), MB()
    r = random.Random(72)
    for (x, y) in [(-30, -20), (-18, -22), (-34, 2), (-22, 16), (-36, 18), (28, -18), (16, -24), (34, -4), (30, 14), (24, 24), (-10, -26), (2, -26), (-14, 26),
                   (-24, -6), (-12, -12), (24, 4), (36, -24), (-4, 26), (8, 24), (-38, -12), (14, -14), (-26, 28)]:
        w, d = r.uniform(8, 12), r.uniform(8, 11)
        zz = zt if abs(x) < 33 and abs(y) < 25 else zt - 1.2
        punic_house(mw, mr, md, x, y, zz, w, d, r.choice([3.5, 4.2, 5.0]), court=w > 10)
    m.add(1, mw.build("houses", WHITE))
    m.add(1, mr.build("courts", "#D9CDB6"))
    m.add(1, md.build("doors", DARK))
    m.add(2, trees("trees", [(-6, -12, zt), (20, -8, zt), (-26, 8, zt), (36, 26, zt - 1)], 2.2, "#6F8A5C"))
    return m


BUILDERS = {
    "carthage/byrsa": byrsa,
    "carthage/byrsa-forum": byrsa_forum,
    "carthage/byrsa-ruins": byrsa_ruins,
    "carthage/cothon": cothon,
    "carthage/cothon-roman": cothon_roman,
    "carthage/cothon-silted": cothon_silted,
    "carthage/commercial-harbour": commercial_harbour,
    "carthage/harbour-silted": harbour_silted,
    "carthage/tophet": tophet,
    "carthage/sea-wall": sea_wall,
    "carthage/hannibal-quarter": hannibal_quarter,
    "carthage/juno-necropolis": juno_necropolis,
    "carthage/antonine-baths": antonine_baths,
    "carthage/antonine-baths-ruin": antonine_baths_ruin,
    "carthage/amphitheatre": amphitheatre,
    "carthage/amphitheatre-ruin": amphitheatre_ruin,
    "carthage/theatre": theatre,
    "carthage/odeon": odeon,
    "carthage/circus": circus,
    "carthage/la-malga": la_malga,
    "carthage/la-malga-ruin": lambda: la_malga(True),
    "carthage/damous-el-karita": damous_el_karita,
    "carthage/villa-aviary": villa_aviary,
    "carthage/sidi-bou-said": sidi_bou_said,
}
