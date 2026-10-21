"""Athens landmark miniatures: the Acropolis temples on their rock, the theatres of the south slope,
the stoas, temples and council buildings of the Agora, Hadrian's Athens and Ottoman Atina.

Conventions as worldkit: metres, origin at the ground centre of the footprint, +X east, +Y north,
+Z up, main front to the south (-Y); the landmark's rotation turns it on the map. The Acropolis
buildings stand on a cut of the rock ROCK_H high so that they read as sitting on the hill.
Helpers build pieces at the origin; bake() applies transforms so every object's origin is the
world origin, turn() rotates about it.
"""
import math, random
import bpy
from chronokit import Model, box, cylinder, dome, join, shade, gable_roof, hip_roof, mesh_from, ellipse_ring, ring_extrude, columns
from worldkit import lathe, prism, frustum, arch_panel, arcade, minaret, shallow_dome, tree
from archkit import copy_at, cyl_x, cyl_y, half_cyl_y, arch_bay, tiled_hip_roof

# ---------------------------------------------------------------- palette
MARB = "#EEE7D6"      # fresh Pentelic marble
MARB_W = "#E2D7C0"    # weathered marble
MARB_S = "#D8CDB6"    # sculpture, a shade darker so it reads
POROS = "#D5C29C"     # limestone (poros)
STUC = "#E6DAC0"      # stuccoed poros
STONE = "#C2B192"     # wall masonry
ROCK = "#AC9E83"      # the Acropolis limestone
ROCK_D = "#978A70"
SCRUB = "#7D8A5A"
OLIVE = "#6B7B50"
TILE_T = "#B4643F"    # terracotta tiles
TILE_M = "#D3CAB6"    # marble tiles
BLUE = "#4F6A8E"      # painted tympana and friezes
BLUE_D = "#36455F"    # triglyphs, mutules
RED = "#A64B3B"
OCHRE = "#C2903F"
GREEN_P = "#5E7D5A"
GILT = "#CFA64E"
BRONZE = "#8E7246"
DARK = "#2E241C"
TIMBER = "#8C6A4A"
EARTH = "#BDA27A"
EARTH_D = "#A88C64"
SAND = "#D8C59C"
GRASS = "#93A27A"
WATER = "#5F878C"
MUDB = "#C49F72"
PLAST = "#E8DDC8"
LEAD = "#7D8590"
ELEUS = "#4C4C54"     # Eleusinian grey-black limestone
CIPOL = "#94A28E"     # green-veined Karystos marble
ROCK_H = 9.0


# ================================================================ basic helpers

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


def beam(name, L, wy, th, theta, c, color):
    """A bar of length L along X, tilted about Y by theta (negative theta rises toward +X), centred at c."""
    o = box(name, L, wy, th, (0, 0, -th / 2), color)
    bake(o)
    o.rotation_euler = (0.0, theta, 0.0)
    bake(o)
    o.location = c
    return bake(o)


def lin(a, b, n):
    return [a] if n == 1 else [a + (b - a) * i / (n - 1) for i in range(n)]


def gable_x(name, w, d, h, loc, color, overhang=0.4):
    """Plain gable roof with its ridge along X (length w), centred at loc."""
    o = gable_roof(name, d, w, h, (0, 0, 0), color, overhang)
    return turn(o, 90, *loc)


def shed(name, w, d, h_low, h_high, loc, color, high_side="N"):
    """A lean-to roof slab: w x d, sloping from h_high on one side down to h_low (heights above loc z)."""
    x, y, z = loc
    hw, hd = w / 2, d / 2
    hi = {"N": lambda X, Y: Y > 0, "S": lambda X, Y: Y < 0, "E": lambda X, Y: X > 0, "W": lambda X, Y: X < 0}[high_side]
    corners = [(-hw, -hd), (hw, -hd), (hw, hd), (-hw, hd)]
    top = [(X, Y, (h_high if hi(X, Y) else h_low)) for X, Y in corners]
    v = [(X, Y, h - 0.25) for X, Y, h in top] + top
    f = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return mesh_from(name, v, f, (x, y, z), color)


# ================================================================ orders

def fluted(name, r0, r1, h, flutes=20, color=MARB, entasis=0.012, depth=0.07, z0=0.0):
    """A shaft whose section alternates arris and flute: reads as fluting once flat-shaded."""
    n = flutes * 2
    rings = [(0.0, r0), (h * 0.4, r0 + (r1 - r0) * 0.4 + r0 * entasis), (h, r1)] if entasis else [(0.0, r0), (h, r1)]
    verts, faces = [], []
    for z, r in rings:
        for i in range(n):
            a = math.tau * i / n
            rr = r if i % 2 == 0 else r * (1 - depth)
            verts.append((rr * math.cos(a), rr * math.sin(a), z0 + z))
    for k in range(len(rings) - 1):
        for i in range(n):
            j = (i + 1) % n
            faces.append((k * n + i, k * n + j, (k + 1) * n + j, (k + 1) * n + i))
    faces.append(tuple(range(n))[::-1])
    faces.append(tuple(range((len(rings) - 1) * n, len(rings) * n)))
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def doric(name, h, r, color=MARB, flutes=20, fluted_shaft=True):
    """Greek Doric column without a base: fluted shaft with entasis, annulets, echinus and abacus."""
    ch = r * 0.95
    sh = h - ch
    shaft = fluted(name + "_s", r, r * 0.8, sh, flutes, color) if fluted_shaft else cylinder(name + "_s", r, sh, (0, 0, 0), color, verts=16, r_top=r * 0.8)
    parts = [shaft,
             cylinder(name + "_ann", r * 0.84, r * 0.09, (0, 0, sh - r * 0.06), shade(color, -0.05), verts=20),
             cylinder(name + "_ech", r * 0.82, ch * 0.5, (0, 0, sh), color, verts=20, r_top=r * 1.28),
             box(name + "_aba", r * 2.6, r * 2.6, ch * 0.5, (0, 0, sh + ch * 0.5), shade(color, 0.03))]
    return J(parts, name)


def ionic(name, h, r, color=MARB, flutes=24, shaft_c=None):
    bh, ch = r * 0.5, r * 0.75
    sh = h - bh - ch
    parts = [cylinder(name + "_b1", r * 1.35, bh * 0.45, (0, 0, 0), color, verts=16),
             cylinder(name + "_b2", r * 1.18, bh * 0.55, (0, 0, bh * 0.45), shade(color, -0.03), verts=16, r_top=r * 1.05),
             fluted(name + "_s", r, r * 0.86, sh, flutes, shaft_c or color, entasis=0, z0=bh)]
    zc = bh + sh
    parts.append(cylinder(name + "_ech", r * 0.9, ch * 0.45, (0, 0, zc), color, verts=16, r_top=r * 1.05))
    parts.append(box(name + "_cush", r * 2.5, r * 1.3, ch * 0.45, (0, 0, zc + ch * 0.3), color))
    for s in (-1, 1):
        parts.append(cyl_y(f"{name}_v{s}", r * 0.42, r * 1.4, (s * r * 1.15, 0, zc + ch * 0.35), shade(color, -0.04), verts=12))
    parts.append(box(name + "_aba", r * 2.4, r * 2.0, ch * 0.2, (0, 0, zc + ch * 0.8), color))
    return J(parts, name)


def corinth(name, h, r, color=MARB, flutes=20, base=True, shaft_c=None, rich=True):
    bh, ch = (r * 0.5 if base else 0.0), r * 2.3
    sh = h - bh - ch
    parts = []
    if base:
        parts += [box(name + "_pl", r * 2.7, r * 2.7, bh * 0.35, (0, 0, 0), shade(color, -0.03)),
                  cylinder(name + "_t", r * 1.25, bh * 0.65, (0, 0, bh * 0.35), color, verts=16, r_top=r * 1.05)]
    parts.append(fluted(name + "_s", r, r * 0.86, sh, flutes, shaft_c or color, entasis=0, z0=bh))
    zc = bh + sh
    parts.append(cylinder(name + "_bell", r * 0.86, ch * 0.82, (0, 0, zc), shade(color, -0.02), verts=16, r_top=r * 1.15))
    for k in range(8):
        a = k * math.pi / 4
        parts.append(box(f"{name}_l{k}", r * 0.55, r * 0.22, ch * 0.4, (math.cos(a) * r * 0.88, math.sin(a) * r * 0.88, zc), shade(color, -0.08), rot_z=a + math.pi / 2))
    if rich:
        for k in range(8):
            a = k * math.pi / 4 + math.pi / 8
            parts.append(box(f"{name}_u{k}", r * 0.5, r * 0.22, ch * 0.34, (math.cos(a) * r * 0.98, math.sin(a) * r * 0.98, zc + ch * 0.3), shade(color, -0.05), rot_z=a + math.pi / 2))
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        parts.append(box(f"{name}_vo{k}", r * 0.45, r * 0.45, ch * 0.25, (math.cos(a) * r * 1.22, math.sin(a) * r * 1.22, zc + ch * 0.6), shade(color, -0.03), rot_z=a))
    parts.append(box(name + "_aba", r * 2.7, r * 2.7, ch * 0.18, (0, 0, zc + ch * 0.82), color))
    return J(parts, name)


def plain_col(name, h, r, color=MARB):
    """A cheap column for distant colonnades: 10-sided tapering shaft and a block capital."""
    return J([cylinder(name + "_s", r, h - r * 0.7, (0, 0, 0), color, verts=10, r_top=r * 0.86),
              box(name + "_k", r * 2.5, r * 2.5, r * 0.7, (0, 0, h - r * 0.7), shade(color, 0.04))], name)


def kore(name, h, color=MARB):
    """A Caryatid: a draped maiden carrying a capital on her head."""
    parts = [box(name + "_pl", h * 0.22, h * 0.22, h * 0.05, (0, 0, 0), shade(color, -0.05)),
             cylinder(name + "_skirt", h * 0.13, h * 0.5, (0, 0, h * 0.05), color, verts=10, r_top=h * 0.09),
             cylinder(name + "_torso", h * 0.09, h * 0.2, (0, 0, h * 0.55), color, verts=10, r_top=h * 0.075),
             cylinder(name + "_neck", h * 0.035, h * 0.06, (0, 0, h * 0.74), color, verts=6),
             dome(name + "_head", h * 0.055, (0, 0, h * 0.79), color, squash=1.4, segments=10, rings=5),
             cylinder(name + "_hair", h * 0.045, h * 0.13, (0, h * 0.035, h * 0.66), shade(color, -0.06), verts=6),
             cylinder(name + "_polos", h * 0.06, h * 0.06, (0, 0, h * 0.85), color, verts=10, r_top=h * 0.1),
             box(name + "_aba", h * 0.24, h * 0.24, h * 0.05, (0, 0, h * 0.91), color)]
    for s in (-1, 1):
        parts.append(box(f"{name}_arm{s}", h * 0.045, h * 0.05, h * 0.27, (s * h * 0.1, 0, h * 0.44), color))
    parts.append(box(name + "_fold", h * 0.05, h * 0.03, h * 0.45, (h * 0.04, -h * 0.12, h * 0.06), shade(color, -0.04)))
    return J(parts, name)


def figure(name, x, y, z, h, color=MARB_S):
    """A standing figure for pediments and acroteria."""
    return J([box(name + "_b", h * 0.3, h * 0.2, h * 0.78, (x, y, z), color),
              cylinder(name + "_h", h * 0.1, h * 0.2, (x, y, z + h * 0.78), color, verts=6)], name)


def reclining(name, x, y, z, L, h, color=MARB_S, flip=1):
    return J([box(name + "_b", L, h * 0.55, h * 0.55, (x, y, z), color),
              box(name + "_t", L * 0.3, h * 0.5, h, (x - flip * L * 0.35, y, z), color)], name)


# ================================================================ temple parts

def crepis(name, w, d, n=3, rise=0.5, tread=0.7, color=MARB, z=0.0, cx=0.0, cy=0.0):
    """Stepped base whose top step is w x d."""
    return J([box(f"{name}{i}", w + 2 * tread * (n - 1 - i), d + 2 * tread * (n - 1 - i), rise, (cx, cy, z + rise * i), shade(color, -0.05 + 0.02 * i)) for i in range(n)], name)


def peri_pts(W, D, nx, ny, inset, cx=0.0, cy=0.0):
    xs = lin(cx - W / 2 + inset, cx + W / 2 - inset, nx)
    ys = lin(cy - D / 2 + inset, cy + D / 2 - inset, ny)
    pts = [(x, ys[0]) for x in xs] + [(x, ys[-1]) for x in xs] + [(xs[0], y) for y in ys[1:-1]] + [(xs[-1], y) for y in ys[1:-1]]
    return pts, xs, ys


def doric_entab(name, W, D, z, ha, hf, hc, nx, ny, color=MARB, tri=BLUE_D, met=None, relief="all", cy=0.0, sides="SNWE", paint=True):
    """Architrave, triglyph-and-metope frieze and geison round a W x D rectangle (outer face of the architrave).
    relief: all | none | front (the south metopes and the four nearest the front on each flank)."""
    met = met or shade(color, -0.03)
    over = hc * 0.7
    parts = [box(name + "_arch", W, D, ha, (0, cy, z), shade(color, -0.02)),
             box(name + "_taenia", W + 0.12, D + 0.12, ha * 0.1, (0, cy, z + ha * 0.9), RED if paint else shade(color, 0.04)),
             box(name + "_frz", W - 0.14, D - 0.14, hf, (0, cy, z + ha), met)]
    tw = hf * 0.62
    zf = z + ha
    rel_c = shade(color, -0.1)
    for side, L, n in (("S", W, nx), ("N", W, nx), ("W", D, ny), ("E", D, ny)):
        if side not in sides:
            continue
        nt = 2 * (n - 1) + 1
        pos = lin(-L / 2 + tw / 2, L / 2 - tw / 2, nt)
        horiz = side in ("S", "N")
        sg = -1 if side in ("S", "W") else 1
        face = (D / 2 if horiz else W / 2) + 0.02
        for k, t in enumerate(pos):
            if horiz:
                parts.append(box(f"{name}_tg{side}{k}", tw, 0.3, hf, (t, cy + sg * face, zf), tri))
            else:
                parts.append(box(f"{name}_tg{side}{k}", 0.3, tw, hf, (sg * face, cy + t, zf), tri))
            if k == nt - 1:
                continue
            want = relief == "all" or (relief == "front" and (side == "S" or (not horiz and k < 4)))
            if not want:
                continue
            mc = (pos[k] + pos[k + 1]) / 2
            mw = (pos[k + 1] - pos[k] - tw) * 0.8
            fh = hf * 0.7
            if horiz:
                parts.append(box(f"{name}_mt{side}{k}", mw, 0.14, hf * 0.78, (mc, cy + sg * (face - 0.03), zf + hf * 0.1), shade(met, -0.04)))
                parts.append(box(f"{name}_ma{side}{k}", mw * 0.28, 0.22, fh, (mc - mw * 0.2, cy + sg * (face + 0.02), zf + hf * 0.14), rel_c))
                parts.append(box(f"{name}_mb{side}{k}", mw * 0.34, 0.22, fh * 0.75, (mc + mw * 0.2, cy + sg * (face + 0.02), zf + hf * 0.14), rel_c))
            else:
                parts.append(box(f"{name}_mt{side}{k}", 0.14, mw, hf * 0.78, (sg * (face - 0.03), cy + mc, zf + hf * 0.1), shade(met, -0.04)))
                parts.append(box(f"{name}_ma{side}{k}", 0.22, mw * 0.28, fh, (sg * (face + 0.02), cy + mc - mw * 0.2, zf + hf * 0.14), rel_c))
                parts.append(box(f"{name}_mb{side}{k}", 0.22, mw * 0.34, fh * 0.75, (sg * (face + 0.02), cy + mc + mw * 0.2, zf + hf * 0.14), rel_c))
    zg = z + ha + hf
    Wg, Dg = W + 2 * over, D + 2 * over
    parts.append(box(name + "_geison", Wg, Dg, hc * 0.6, (0, cy, zg), shade(color, 0.03)))
    for side in "SNWE":
        if side in "SN":
            parts.append(box(f"{name}_mut{side}", Wg, over, 0.12, (0, cy + (-1 if side == "S" else 1) * (D / 2 + over / 2), zg - 0.12), BLUE_D if paint else shade(color, -0.08)))
        else:
            parts.append(box(f"{name}_mut{side}", over, Dg, 0.12, ((-1 if side == "W" else 1) * (W / 2 + over / 2), cy, zg - 0.12), BLUE_D if paint else shade(color, -0.08)))
    if paint:
        parts.append(box(name + "_band", Wg + 0.04, Dg + 0.04, 0.12, (0, cy, zg + hc * 0.6 - 0.14), RED))
    parts.append(box(name + "_sima", Wg - 0.1, Dg - 0.1, hc * 0.4, (0, cy, zg + hc * 0.6), color))
    return J(parts, name)


def ionic_entab(name, W, D, z, h, color=MARB, frieze_c=None, figs=True, fig_c=None, dentils=False, cy=0.0, fig_step=0.9):
    """Three-fascia architrave, continuous frieze (with figures) and cornice round a W x D rectangle. Height h."""
    ha, hf, hc = h * 0.36, h * 0.34, h * 0.30
    fc = frieze_c or shade(color, -0.03)
    parts = [box(name + "_f1", W - 0.12, D - 0.12, ha / 3, (0, cy, z), shade(color, -0.03)),
             box(name + "_f2", W - 0.06, D - 0.06, ha / 3, (0, cy, z + ha / 3), shade(color, -0.015)),
             box(name + "_f3", W, D, ha / 3, (0, cy, z + 2 * ha / 3), color),
             box(name + "_fr", W, D, hf, (0, cy, z + ha), fc),
             box(name + "_c1", W + hc * 0.7, D + hc * 0.7, hc * 0.45, (0, cy, z + ha + hf), shade(color, 0.03)),
             box(name + "_c2", W + hc * 1.3, D + hc * 1.3, hc * 0.55, (0, cy, z + ha + hf + hc * 0.45), color)]
    zf = z + ha
    if figs:
        fc2 = fig_c or shade(color, -0.1)
        locs_a, rots_a, locs_b, rots_b = [], [], [], []
        for side, L in (("S", W), ("N", W), ("W", D), ("E", D)):
            n = max(2, int(L / fig_step))
            for k in range(n):
                t = -L / 2 + (k + 0.5) * L / n
                horiz = side in "SN"
                sg = -1 if side in "SW" else 1
                p = (t, cy + sg * (D / 2 + 0.04), zf + hf * 0.12) if horiz else (sg * (W / 2 + 0.04), cy + t, zf + hf * 0.12)
                (locs_a if k % 3 else locs_b).append(p)
                (rots_a if k % 3 else rots_b).append(0.0 if horiz else math.pi / 2)
        parts.append(copies(box(name + "_fa", fig_step * 0.28, 0.1, hf * 0.72, (0, 0, 0), fc2), locs_a, name + "_figa", rots_a))
        parts.append(copies(box(name + "_fb", fig_step * 0.55, 0.1, hf * 0.62, (0, 0, 0), fc2), locs_b, name + "_figb", rots_b))
    if dentils:
        step = max(hc * 0.5, 0.25)
        locs, rots = [], []
        for side, L in (("S", W), ("N", W), ("W", D), ("E", D)):
            n = int(L / step)
            horiz = side in "SN"
            sg = -1 if side in "SW" else 1
            for k in range(n):
                t = -L / 2 + (k + 0.5) * L / n
                locs.append((t, cy + sg * (D / 2 + hc * 0.22), z + ha + hf - hc * 0.28) if horiz else (sg * (W / 2 + hc * 0.22), cy + t, z + ha + hf - hc * 0.28))
                rots.append(0.0 if horiz else math.pi / 2)
        parts.append(copies(box(name + "_dt", step * 0.5, hc * 0.3, hc * 0.28, (0, 0, 0), shade(color, 0.05)), locs, name + "_dent", rots))
    return J(parts, name)


def greek_roof(name, W, D, z, h, roof=TILE_M, frame=MARB, tymp=BLUE, figs=True, fig_c=None, acro=True, acro_c=None, tiles=True, cy=0.0,
               gables=(True, True), tile_step=0.85):
    """Gabled roof, ridge along Y, over W x D (eaves included) at height z, with framed pediments at y = cy -/+ D/2:
    recessed painted tympanum, raking cornices, pedimental figures, acroteria, cover-tile ridges and antefixes."""
    parts = []
    y0, y1 = cy - D / 2, cy + D / 2
    f = [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]
    parts.append(mesh_from(name + "_r", [(-W / 2, y0, 0), (W / 2, y0, 0), (0, y0, h), (-W / 2, y1, 0), (W / 2, y1, 0), (0, y1, h)], f, (0, 0, z), roof))
    a = math.atan2(h, W / 2)
    L = math.hypot(W / 2, h)
    fig_c = fig_c or MARB_S
    acro_c = acro_c or shade(frame, -0.04)
    for gi, (yy, sg) in enumerate(((y0, -1), (y1, 1))):
        if not gables[gi]:
            continue
        tw = W / 2 - 0.7
        th = h * tw / (W / 2) * 0.9
        yo, yi = yy + sg * 0.05, yy - sg * 0.3
        parts.append(mesh_from(f"{name}_ty{gi}", [(-tw, yo, 0.05), (tw, yo, 0.05), (0, yo, th), (-tw, yi, 0.05), (tw, yi, 0.05), (0, yi, th)], f, (0, 0, z), tymp))
        for s in (-1, 1):
            parts.append(beam(f"{name}_rk{gi}{s}", L + 0.3, 0.9, 0.45, s * a, (s * W / 4, yy + sg * 0.35, z + h / 2 + 0.1), shade(frame, 0.03)))
        if figs:
            nf = max(3, int(W / 2.0))
            for k, x in enumerate(lin(-W / 2 + 1.4, W / 2 - 1.4, nf)):
                avail = h * (1 - abs(x) / (W / 2)) - 0.3
                if avail < 0.45:
                    continue
                py = yy + sg * 0.2
                if avail > 1.3 and abs(x) < W * 0.3:
                    parts.append(figure(f"{name}_pf{gi}{k}", x, py, z + 0.05, avail * 0.85, fig_c))
                else:
                    parts.append(reclining(f"{name}_pr{gi}{k}", x, py, z + 0.05, min(2.0, avail * 2.2), avail * 0.8, fig_c, flip=1 if x < 0 else -1))
        if acro:
            ah = max(0.8, h * 0.32)
            parts.append(box(f"{name}_acb{gi}", ah * 0.5, 0.35, ah * 0.25, (0, yy + sg * 0.2, z + h), acro_c))
            parts.append(box(f"{name}_acp{gi}", ah * 0.75, 0.2, ah * 0.75, (0, yy + sg * 0.2, z + h + ah * 0.25), acro_c, rot_z=0))
            for s in (-1, 1):
                parts.append(figure(f"{name}_acn{gi}{s}", s * (W / 2 - 0.4), yy + sg * 0.2, z, ah * 1.1, acro_c))
    if tiles:
        n = max(4, int(D / tile_step))
        locs = [(0, y0 + (k + 0.5) * D / n, 0) for k in range(n)]
        for s in (-1, 1):
            parts.append(copies(beam(f"{name}_tp{s}", L * 0.98, 0.22, 0.17, s * a, (s * W / 4, 0, z + h / 2 + 0.1), shade(roof, 0.08)), locs, f"{name}_tiles{s}"))
            parts.append(copies(box(f"{name}_ap{s}", 0.24, 0.1, 0.42, (s * (W / 2 - 0.02), 0, z - 0.12), shade(frame, -0.06)), locs, f"{name}_antefix{s}"))
    parts.append(box(name + "_ridge", 0.5, D, 0.32, (0, cy, z + h - 0.2), shade(roof, -0.07)))
    return J(parts, name)


def peripteral(m, nm, W, D, nx, ny, col_h, r, z0, nsteps=3, rise=0.5, tread=0.7, color=MARB, cella_c=None, roof_c=TILE_M, tymp=BLUE,
               relief="all", porch="prostyle", porch_n=6, front_porch=True, inner_frieze=True, frieze_c=BLUE, ped_figs=True, flutes=20,
               roof_h=None, roof=True, tiles=True, paint=True, tile_step=0.85):
    """A Doric peripteral temple on its crepis, front to -Y. Adds stages 0 (base), 1 (columns, cella), 2 (entablature), 3 (roof).
    porch: prostyle (columns across the cella front, Parthenon) | antis (two columns between the cella walls, Hephaisteion)."""
    cella_c = cella_c or shade(color, -0.03)
    m.add(0, crepis(nm + "_crepis", W, D, nsteps, rise, tread, color, z0), "base")
    zs = z0 + nsteps * rise
    inset = r * 1.1
    pts, xs, ys = peri_pts(W, D, nx, ny, inset)
    m.add(1, copies(doric(nm + "_col", col_h, r, color, flutes), [(x, y, zs) for x, y in pts], nm + "_peristyle"), "columns")
    sx, sy = xs[1] - xs[0], ys[1] - ys[0]
    cw2 = (W / 2 - inset) - sx * 0.9
    if porch == "prostyle":
        pf, pb = ys[0] + 0.85 * sy, ys[-1] - 0.85 * sy
        wf, wb = pf + 2.2 * r, pb - 2.2 * r
        zc = zs + 0.6
        m.add(1, box(nm + "_cpl", 2 * cw2 + 1.2, pb - pf + 2.6 * r, 0.6, (0, (pf + pb) / 2, zs), shade(color, -0.04)))
        hp = col_h - 0.6
        pxs = lin(-cw2 + r, cw2 - r, porch_n)
        locs = ([(x, pf, zc) for x in pxs] if front_porch else []) + [(x, pb, zc) for x in pxs]
        m.add(1, copies(doric(nm + "_pcol", hp, r * 0.88, color, flutes), locs, nm + "_porches"))
    else:
        pf, pb = ys[0] + 1.6 * sy, ys[-1] - 1.1 * sy
        wf, wb = pf + 1.1 * sy, pb - 0.8 * sy
        zc = zs
        hp = col_h
        locs = ([(x, pf, zc) for x in (-cw2 * 0.4, cw2 * 0.4)] if front_porch else []) + [(x, pb, zc) for x in (-cw2 * 0.4, cw2 * 0.4)]
        m.add(1, copies(doric(nm + "_pcol", hp, r * 0.92, color, flutes), locs, nm + "_porches"))
        for s in (-1, 1):
            m.add(1, box(f"{nm}_antaF{s}", r * 1.6, wf - pf + r, hp, (s * (cw2 - r * 0.8), (pf + wf) / 2 - r / 2, zc), shade(cella_c, 0.02)))
            m.add(1, box(f"{nm}_antaB{s}", r * 1.6, pb - wb + r, hp, (s * (cw2 - r * 0.8), (pb + wb) / 2 + r / 2, zc), shade(cella_c, 0.02)))
    m.add(1, box(nm + "_cella", 2 * cw2, wb - wf, hp, (0, (wf + wb) / 2, zc), cella_c))
    for s, yy in ((-1, wf), (1, wb)):
        m.add(1, box(f"{nm}_door{s}", cw2 * 0.42, 0.3, hp * 0.74, (0, yy + s * 0.14, zc), DARK))
    ztop = zs + col_h
    ha, hf, hc = col_h * 0.13, col_h * 0.13, col_h * 0.055
    # inner frieze round the cella and its porches, seen between the columns
    if inner_frieze:
        y_a, y_b = (pf - r * 1.3, pb + r * 1.3)
        m.add(2, ionic_entab(nm + "_inner", 2 * cw2 + 0.4, y_b - y_a, ztop, ha + hf * 0.9, color, frieze_c, True, MARB_S, cy=(y_a + y_b) / 2, fig_step=1.0), "entablature")
    Wa, Da = W - 0.2 * r, D - 0.2 * r
    m.add(2, doric_entab(nm + "_ent", Wa, Da, ztop, ha, hf, hc, nx, ny, color, BLUE_D if paint else shade(color, -0.15), relief=relief, paint=paint), "entablature")
    zr = ztop + ha + hf + hc
    over = hc * 0.7
    Wr, Dr = Wa + 2 * over, Da + 2 * over
    rh = roof_h or Wr * 0.12
    if roof:
        m.add(3, greek_roof(nm + "_roof", Wr, Dr, zr, rh, roof_c, color, tymp, figs=ped_figs, tiles=tiles, tile_step=tile_step), "roof")
    return dict(zs=zs, zc=zc, zr=zr, rh=rh, xs=xs, ys=ys, cw2=cw2, pf=pf, pb=pb, wf=wf, wb=wb, Wr=Wr, Dr=Dr, ztop=ztop)


# ================================================================ ground and rock

def rock_cap(name, W, D, H, seed=1, top_inset=2.5, color=ROCK, shrubs=6, loc=(0, 0, 0)):
    """A cut of hill: rounded-rectangle base W x D, battered and irregular cliff, flat top inset by top_inset."""
    rnd = random.Random(seed)
    n = 36

    def ring(hw, hd, zf, jit, zj=0.0):
        out = []
        for i in range(n):
            t = math.tau * i / n
            c, s = math.cos(t), math.sin(t)
            x = hw * math.copysign(abs(c) ** 0.35, c)
            y = hd * math.copysign(abs(s) ** 0.35, s)
            k = 1 - rnd.uniform(0, jit)
            out.append((x * k, y * k, zf + rnd.uniform(-zj, zj)))
        return out
    r0 = ring(W / 2, D / 2, 0.0, 0.03)
    r1 = ring(W / 2 - top_inset * 0.45, D / 2 - top_inset * 0.45, H * 0.5, 0.06, H * 0.18)
    r2 = ring(W / 2 - top_inset, D / 2 - top_inset, H, 0.0)
    verts = r0 + r1 + r2
    faces = []
    for k in range(2):
        for i in range(n):
            j = (i + 1) % n
            faces.append((k * n + i, k * n + j, (k + 1) * n + j, (k + 1) * n + i))
    faces.append(tuple(range(n))[::-1])
    faces.append(tuple(range(2 * n, 3 * n)))
    parts = [mesh_from(name + "_m", verts, faces, (0, 0, 0), color)]
    for i in range(0, n, 5):
        x, y, _ = r0[i]
        sz = rnd.uniform(1.0, 2.2)
        parts.append(box(f"{name}_bd{i}", sz * 1.3, sz, sz * 0.7, (x * 0.94, y * 0.94, 0), shade(color, -0.08), rot_z=rnd.random() * 3))
    for i in range(shrubs):
        x, y, z = r1[(i * 7 + 3) % n]
        parts.append(dome(f"{name}_sh{i}", rnd.uniform(0.7, 1.3), (x * 1.02, y * 1.02, z - 0.4), SCRUB, squash=0.8, segments=8, rings=4))
    o = J(parts, name)
    return turn(o, 0, *loc) if loc != (0, 0, 0) else o


def rock_arc(name, cx, cy, r0, r1, a0, a1, h, n=26, seed=5, color=ROCK):
    """A curved cliff (the Acropolis face behind the theatre): inner face at r0 leaning back, ragged top."""
    rnd = random.Random(seed)
    verts, faces = [], []
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        c, s = math.cos(a), math.sin(a)
        ht = (h + rnd.uniform(-3, 3)) * (0.35 + 0.65 * math.sin(math.pi * i / n))
        ri, ro = r0 + rnd.uniform(-0.5, 0.8), r1 + rnd.uniform(-1.0, 1.5)
        rt = ri + 2.5
        verts += [(cx + ri * c, cy + ri * s, 0), (cx + rt * c, cy + rt * s, ht), (cx + ro * c, cy + ro * s, ht), (cx + ro * c, cy + ro * s, 0)]
    for i in range(n):
        a, b = 4 * i, 4 * (i + 1)
        for k in range(4):
            k2 = (k + 1) % 4
            faces.append((a + k, b + k, b + k2, a + k2))
    faces.append((0, 1, 2, 3))
    faces.append((4 * n + 3, 4 * n + 2, 4 * n + 1, 4 * n))
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def sloped_fan(name, R, cy, zc, zr, a0=0.0, a1=math.pi, n=28, color=EARTH):
    """A half-disc of ground whose top slopes from zc at its centre (on the chord) to zr at the rim."""
    angs = lin(a0, a1, n)
    top = [(0.0, cy, zc)] + [(R * math.cos(a), cy + R * math.sin(a), zr) for a in angs]
    bot = [(x, y, 0.0) for x, y, _ in top]
    m = len(top)
    verts = top + bot
    faces = [(0, i, i + 1) for i in range(1, m - 1)] + [(m, m + i + 1, m + i) for i in range(1, m - 1)]
    faces += [(i, m + i, m + i + 1, i + 1) for i in range(1, m - 1)]
    faces += [(0, m, m + 1, 1), (m - 1, 2 * m - 1, m, 0)]
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def cavea(name, cx, cy, r0, r1, z0, z1, rows, arc_deg, start_deg, colors, diaz=(), n=40):
    """Stepped seating rings (solid to the ground) between radii r0 and r1, rising z0 -> z1. Returns (lower, upper) halves."""
    arc, st = math.radians(arc_deg), math.radians(start_deg)
    dr, dz = (r1 - r0) / rows, (z1 - z0) / rows
    lo, hi = [], []
    z = z0
    for k in range(rows):
        ra, rb = r0 + dr * k, r0 + dr * (k + 1)
        if k in diaz:
            col = shade(colors[0], 0.06)
        else:
            z += dz
            col = colors[k % len(colors)]
        (lo if k < rows // 2 else hi).append(ellipse_ring(f"{name}{k}", rb, rb, ra / rb, z, (cx, cy, 0), col, n=n, arc=arc, start=st))
    return J(lo, name + "_lo"), J(hi, name + "_hi"), z


def radial_stairs(name, cx, cy, r0, r1, z0, z1, angles_deg, color, width=0.9):
    L = math.hypot(r1 - r0, z1 - z0)
    th = -math.atan2(z1 - z0, r1 - r0)
    out = []
    for i, a in enumerate(angles_deg):
        o = beam(f"{name}{i}", L, width, 0.3, th, ((r0 + r1) / 2, 0, (z0 + z1) / 2 + 0.2), color)
        out.append(turn(o, a, cx, cy, 0))
    return J(out, name)


def u_pts(x_open, xc, r, n=20):
    pts = [(x_open, -r), (xc, -r)]
    for i in range(1, n):
        a = -math.pi / 2 + math.pi * i / n
        pts.append((xc + r * math.cos(a), r * math.sin(a)))
    return pts + [(xc, r), (x_open, r)]


def court_house(name, w, d, depth, h, loc=(0, 0, 0), wall=MUDB, roof=TILE_T, court=SAND):
    """Rooms on four sides of an open court with lean-to tiled roofs sloping inward."""
    x, y, z = loc
    parts = [box(name + "_court", w - 2 * depth, d - 2 * depth, 0.2, (x, y, z), court)]
    for side in "SNWE":
        if side in "SN":
            sg = -1 if side == "S" else 1
            parts.append(box(f"{name}_{side}", w, depth, h, (x, y + sg * (d / 2 - depth / 2), z), wall))
            parts.append(shed(f"{name}_r{side}", w + 0.6, depth + 0.6, 0.0, 1.0, (x, y + sg * (d / 2 - depth / 2), z + h), roof, "N" if side == "N" else "S"))
        else:
            sg = -1 if side == "W" else 1
            parts.append(box(f"{name}_{side}", depth, d - 2 * depth, h, (x + sg * (w / 2 - depth / 2), y, z), wall))
            parts.append(shed(f"{name}_r{side}", depth + 0.6, d - 2 * depth, 0.0, 1.0, (x + sg * (w / 2 - depth / 2), y, z + h), roof, "E" if side == "E" else "W"))
    parts.append(box(name + "_door", 1.4, 0.3, 2.2, (x, y - d / 2 - 0.1, z), DARK))
    return J(parts, name)


def small_temple(name, W, D, col_h, nfront=4, order="doric", color=MARB, roof_c=TILE_T, kind="prostyle", z0=0.0, steps=2, figs=False):
    """A small temple facing -Y: prostyle (columns across the front), amphiprostyle (front and back) or in antis."""
    parts = [crepis(name + "_cr", W, D, steps, 0.3, 0.45, color, z0)]
    zs = z0 + steps * 0.3
    r = min(W / (nfront * 4.2), 0.6)
    xs = lin(-W / 2 + r * 1.3, W / 2 - r * 1.3, nfront)
    mk = {"doric": lambda: doric(name + "_c", col_h, r, color), "ionic": lambda: ionic(name + "_c", col_h, r * 0.8, color),
          "corinthian": lambda: corinth(name + "_c", col_h, r * 0.85, color, rich=False)}[order]
    yf = -D / 2 + r * 1.3
    locs = [(x, yf, zs) for x in xs]
    if kind == "amphiprostyle":
        locs += [(x, D / 2 - r * 1.3, zs) for x in xs]
    if kind == "antis":
        locs = [(x, yf, zs) for x in xs[1:-1]]
    parts.append(copies(mk(), locs, name + "_cols"))
    depth_porch = r * 2.8 if kind != "antis" else 0.0
    cy0 = -D / 2 + depth_porch
    cy1 = D / 2 - (r * 2.8 if kind == "amphiprostyle" else 0.0)
    parts.append(box(name + "_cella", W - r * 0.6, cy1 - cy0, col_h, (0, (cy0 + cy1) / 2, zs), shade(color, -0.03)))
    parts.append(box(name + "_door", W * 0.22, 0.3, col_h * 0.65, (0, cy0 - 0.1, zs), DARK))
    eh = col_h * 0.26
    parts.append(ionic_entab(name + "_ent", W, D, zs + col_h, eh, color, figs=False) if order != "doric" else
                 doric_entab(name + "_ent", W, D, zs + col_h, eh * 0.4, eh * 0.4, eh * 0.2, nfront, max(3, int(nfront * D / W)), color, relief="none"))
    parts.append(greek_roof(name + "_roof", W + 0.6, D + 0.6, zs + col_h + eh, W * 0.16, roof_c, color, BLUE, figs=figs, tile_step=0.7))
    return J(parts, name)


# ================================================================ the Acropolis

def parthenon(variant="430"):
    m = Model("parthenon" if variant == "430" else "parthenon-mosque")
    W, D = 30.88, 69.5
    m.add(0, rock_cap("rock", 40, 80, ROCK_H, seed=3, top_inset=2.6), "rock")
    mosque = variant == "mosque"
    t = peripteral(m, "pt", W, D, 8, 17, 10.43, 0.95, ROCK_H, nsteps=3, rise=0.52, tread=0.72, color=MARB, roof_c=TILE_M,
                   porch="prostyle", porch_n=6, front_porch=not mosque, inner_frieze=True, frieze_c=BLUE, tile_step=0.8)
    zs = t["zs"]
    # the gold-and-ivory goddess glimpsed through the east door, and the altar of Athena east of the temple
    if not mosque:
        m.add(1, box("door_glow", 3.2, 0.2, 6.0, (0, t["wf"] - 0.32, t["zc"] + 0.8), GILT))
        m.add(1, box("altar", 4.0, 2.2, 1.2, (0, -D / 2 - 4.5, ROCK_H), MARB_W))
    else:
        # Christian apse in the east porch, kept by the mosque; Ottoman minaret in the south-west corner
        m.add(1, cylinder("apse", 4.2, 9.0, (0, t["wf"], t["zc"]), PLAST, verts=24), "columns")
        m.add(1, box("pronaos_wall", 2 * t["cw2"], 0.8, 7.5, (0, t["pf"], t["zc"]), PLAST))
        m.add(1, box("mihrab_door", 2.2, 0.3, 3.5, (-5, t["pf"] - 0.4, t["zc"]), DARK))
        m.add(3, minaret("minaret", 1.25, 27.0, (-t["cw2"] + 1.6, t["wb"] - 2.2, zs), PLAST, MARB, balconies=1, cap="cone", sides=16, taper=0.82), "roof")
        for i, (x, y) in enumerate([(13.5, -38.0), (-14.5, -37.5), (15.5, 37.5)]):
            m.add(0, box(f"house{i}", 6.0, 5.0, 3.6, (x, y, ROCK_H), PLAST))
            m.add(0, hip_roof(f"house{i}_r", 6.0, 5.0, 1.4, (x, y, ROCK_H + 3.6), TILE_T, ridge=0.4, overhang=0.3))
    return m


def erechtheion():
    m = Model("erechtheion")
    zl, zh = ROCK_H - 3.0, ROCK_H
    # two-level rock: low ground to the north and west, high ground to the east and south
    m.add(0, rock_cap("rock", 30, 42, zl, seed=7, top_inset=1.8), "rock")
    hi = J([box("hi_core", 18.0, 25.0, 3.0, (-5.0, -8.0, zl), ROCK),
            box("hi_east", 26.0, 8.0, 3.0, (-1.0, -17.0, zl), ROCK)], "rock_hi")
    m.add(0, hi)
    yo = -2.0
    y0, y1 = yo - 11.75, yo + 11.75
    # main block from the low ground up
    zt = zh + 6.6
    m.add(1, box("cella", 11.6, 23.5, zt - zl, (0, yo, zl), MARB), "walls")
    m.add(1, box("west_podium", 11.9, 0.3, 4.0, (0, y1 + 0.15, zl), shade(MARB, -0.05)))
    m.add(1, copies(ionic("wcol", zt - (zl + 4.0), 0.3, MARB), [(x, y1 + 0.25, zl + 4.0) for x in (-3.6, -1.2, 1.2, 3.6)], "west_halfcols"))
    for i, x in enumerate((-2.4, 0.0, 2.4)):
        m.add(1, box(f"wwin{i}", 1.2, 0.3, 2.4, (x, y1 + 0.2, zl + 6.0), DARK))
    # east porch: six Ionic columns on the high ground
    m.add(1, crepis("east_steps", 12.4, 3.0, 3, 0.25, 0.35, MARB, zh - 0.75, cy=y0 - 1.4))
    m.add(1, copies(ionic("ecol", 6.6, 0.345, MARB), [(x, y0 - 2.3, zh) for x in lin(-5.4, 5.4, 6)], "east_porch"))
    m.add(1, box("east_door", 2.2, 0.3, 4.6, (0, y0 - 0.12, zh), DARK))
    # north porch on the low ground: four columns in front, one behind each corner, taller
    nx0, nx1 = 5.8, 12.1
    ny0, ny1 = 0.0, 10.4
    m.add(1, crepis("north_steps", nx1 - nx0 + 0.8, ny1 - ny0 + 0.6, 3, 0.22, 0.35, MARB, zl, cx=(nx0 + nx1) / 2 + 0.3, cy=(ny0 + ny1) / 2))
    npts = [(nx1 - 0.5, y) for y in lin(ny0 + 0.55, ny1 - 0.55, 4)] + [(nx0 + 3.1, ny0 + 0.55), (nx0 + 3.1, ny1 - 0.55)]
    m.add(1, copies(ionic("ncol", 7.6, 0.41, MARB), [(x, y, zl + 0.66) for x, y in npts], "north_porch"))
    m.add(1, box("north_door", 0.3, 2.4, 4.9, (nx0 + 0.12, (ny0 + ny1) / 2, zl + 0.66), DARK))
    # Caryatid porch on its parapet, on the high ground, south side near the west end
    kx0 = -5.8 - 3.6
    m.add(1, box("kore_parapet", 3.8, 5.8, 1.8, (kx0 + 1.8, 4.2, zh), MARB))
    kpts = [(kx0 + 0.45, y) for y in lin(1.85, 6.55, 4)] + [(kx0 + 2.3, 1.85), (kx0 + 2.3, 6.55)]
    m.add(1, copies(kore("kore", 2.3, MARB), [(x, y, zh + 1.8) for x, y in kpts], "caryatids"))
    m.add(2, ionic_entab("kore_ent", 4.0, 5.9, zh + 1.8 + 2.25, 0.95, MARB, figs=False, dentils=True, cy=4.2), "entablature")
    m.add(2, box("kore_roof", 4.2, 6.1, 0.3, (kx0 + 1.9, 4.2, zh + 1.8 + 3.2), MARB_W))
    # entablatures: dark Eleusinian frieze with white figures; north porch roof turned to face north
    ey0, ey1 = y0 - 2.9, y1 + 0.2
    m.add(2, ionic_entab("ent", 12.4, ey1 - ey0, zt, 1.9, MARB, ELEUS, True, MARB, cy=(ey0 + ey1) / 2, fig_step=0.8))
    nz = zl + 0.66 + 7.6
    nent = ionic_entab("n_ent", ny1 - ny0 + 0.2, nx1 - nx0 + 0.6, 0, 1.9, MARB, ELEUS, True, MARB, fig_step=0.8)
    m.add(2, turn(nent, 90, (nx0 + nx1) / 2 + 0.3, (ny0 + ny1) / 2, nz))
    m.add(3, greek_roof("roof", 13.2, ey1 - ey0 + 0.6, zt + 1.9, 2.0, TILE_M, MARB, BLUE, figs=False, cy=(ey0 + ey1) / 2, tile_step=0.7), "roof")
    nroof = greek_roof("n_roof", ny1 - ny0 + 0.9, nx1 - nx0 + 1.4, 0, 1.6, TILE_M, MARB, BLUE, figs=False, gables=(True, False), tile_step=0.7)
    m.add(3, turn(nroof, 90, (nx0 + nx1) / 2 + 0.6, (ny0 + ny1) / 2, nz + 1.9))
    # the Pandroseion: walled court west of the temple with Athena's olive
    py0, py1 = y1 + 0.3, 19.6
    pw = [box("pan_w", 0.6, py1 - py0, 2.4, (-8.5, (py0 + py1) / 2, zl), STONE), box("pan_e", 0.6, py1 - py0, 2.4, (9.5, (py0 + py1) / 2, zl), STONE),
          box("pan_n", 18.6, 0.6, 2.4, (0.5, py1, zl), STONE), box("pan_floor", 17.4, py1 - py0, 0.15, (0.5, (py0 + py1) / 2, zl), shade(ROCK, 0.1))]
    m.add(1, J(pw, "pandroseion"))
    m.add(3, tree("olive", 2.2, (-2.5, 15.0, zl), OLIVE, TIMBER))
    m.add(1, small_temple("kekropeion", 3.2, 4.4, 2.6, 2, "ionic", MARB, TILE_M, "prostyle", zl, steps=1))
    return m


def propylaia(variant="430"):
    ruined = variant == "1680"
    m = Model("propylaia" if not ruined else "propylaia-1680")
    zw = ROCK_H - 1.6     # floor of the west hall
    zp = ROCK_H - 2.2     # platform of the wings and the head of the ramp
    m.add(0, rock_cap("rock", 60, 40, ROCK_H, seed=11, top_inset=2.2, loc=(0, 8, 0)), "rock")
    m.add(0, rock_cap("rock_n", 22, 20, zp, seed=12, top_inset=1.5, loc=(-19, -18, 0)))
    m.add(0, rock_cap("rock_s", 16, 16, zp, seed=13, top_inset=1.2, loc=(17, -17, 0)))
    # the ramp
    rv = [(-7, -28, 0.4), (7, -28, 0.4), (7, -12, zp), (-7, -12, zp), (-7, -28, 0), (7, -28, 0), (7, -12, 0), (-7, -12, 0)]
    m.add(0, mesh_from("ramp", rv, [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)], (0, 0, 0), shade(POROS, 0.05)))
    m.add(0, box("west_platform", 20.0, 12.0, 0.6, (0, -7.0, zp), MARB_W))
    xs = [-8.3, -5.5, -2.7, 2.7, 5.5, 8.3]
    # west porch and hall
    keep_w = range(6) if not ruined else (0, 1, 4, 5)
    m.add(1, copies(doric("wcol", 8.8, 0.78, MARB), [(xs[i], -11.4, zw) for i in keep_w], "west_porch"), "columns")
    ion_pts = [(s * 3.0, y) for s in (-1, 1) for y in (-8.8, -6.0, -3.2)]
    if ruined:
        ion_pts = ion_pts[:2] + ion_pts[3:4]
    m.add(1, copies(ionic("icol", 10.2, 0.52, MARB), [(x, y, zw) for x, y in ion_pts], "ionic_passage"))
    for s in (-1, 1):
        m.add(1, box(f"hall_wall{s}", 1.1, 9.6, 8.8 if not ruined else 5.5, (s * 9.1, -6.9, zw), MARB))
    gate = [box("gate_wall", 18.2, 1.2, 11.0 if not ruined else 7.0, (0, -1.4, zw), MARB)]
    for x, w, h in ((0, 4.2, 7.4), (-4.6, 3.0, 5.5), (4.6, 3.0, 5.5), (-7.6, 1.5, 3.2), (7.6, 1.5, 3.2)):
        gate.append(box(f"door{x}", w, 1.3, min(h, 6.8) if ruined else h, (x, -1.4, zw + 0.0), DARK))
    m.add(1, J(gate, "gate_wall"))
    m.add(1, crepis("gate_steps", 18.2, 1.0, 4, 0.4, 0.3, MARB, zw, cy=-0.4))
    # east porch on the summit
    keep_e = range(6) if not ruined else (0, 1, 2, 5)
    m.add(1, copies(doric("ecol", 8.5, 0.78, MARB), [(xs[i], 5.0, ROCK_H) for i in keep_e], "east_porch"))
    for s in (-1, 1):
        m.add(1, box(f"east_wall{s}", 1.1, 6.5, 8.5 if not ruined else 6.0, (s * 9.1, 1.9, ROCK_H), MARB))
    if not ruined:
        m.add(2, doric_entab("w_ent", 18.6, 10.6, zw + 8.8, 1.15, 1.15, 0.5, 6, 3, MARB, relief="none", cy=-6.8), "entablature")
        m.add(2, doric_entab("e_ent", 18.6, 8.2, ROCK_H + 8.5, 1.15, 1.15, 0.5, 6, 3, MARB, relief="none", cy=1.6))
        m.add(3, greek_roof("w_roof", 19.8, 11.8, zw + 8.8 + 2.8, 2.6, TILE_M, MARB, BLUE, figs=False, cy=-6.8, gables=(True, False)), "roof")
        m.add(3, greek_roof("e_roof", 19.8, 9.4, ROCK_H + 8.5 + 2.8, 2.6, TILE_M, MARB, BLUE, figs=False, cy=1.6, gables=(False, True)))
    else:
        m.add(2, box("w_arch_frag", 7.0, 1.2, 1.15, (-6.9, -11.4, zw + 8.8), MARB_W), "entablature")
        m.add(2, box("e_arch_frag", 8.0, 1.2, 1.15, (-5.5, 5.0, ROCK_H + 8.5), MARB_W))
        rnd = random.Random(9)
        m.add(2, J([box(f"rub{i}", rnd.uniform(1, 2.5), rnd.uniform(0.8, 1.6), rnd.uniform(0.6, 1.2), (rnd.uniform(-7, 7), rnd.uniform(-10, 4), zw + 0.4), MARB_W, rot_z=rnd.random() * 3) for i in range(12)], "rubble"))
    # wings: the Pinakotheke (north, -X) and the south wing (+X), their small Doric porches facing the ramp
    nw = [box("pin_hall", 10.0, 13.0, 7.0, (-19.0, -18.0, zp), MARB)]
    for i, y in enumerate((-20.5, -15.5)):
        nw.append(box(f"pin_win{i}", 0.3, 1.2, 1.8, (-13.9, y, zp + 2.6), DARK))
    nw.append(box("pin_door", 0.3, 1.8, 3.4, (-13.9, -18.0, zp), DARK))
    m.add(1, J(nw, "pinakotheke"))
    m.add(1, copies(doric("pcol", 5.85, 0.52, MARB), [(-10.9, y, zp) for y in (-22.0, -18.0, -14.0)], "pin_porch"))
    m.add(1, box("pin_anta", 3.8, 0.9, 5.85, (-12.0, -24.5, zp), MARB))
    sw = [box("sw_hall", 4.5, 9.0, 6.5, (15.5, -16.0, zp), MARB), box("sw_pier", 1.2, 1.2, 5.85, (12.0, -20.4, zp), MARB)]
    m.add(1, J(sw, "south_wing"))
    m.add(1, copies(doric("scol", 5.85, 0.52, MARB), [(10.9, y, zp) for y in (-17.2, -13.6)], "sw_porch"))
    if not ruined:
        m.add(3, tiled_hip_roof("pin_roof", 14.0, 13.6, 2.2, (-17.5, -18.0, zp + 6.6), TILE_M))
        m.add(3, tiled_hip_roof("sw_roof", 7.8, 9.6, 1.8, (14.2, -16.0, zp + 6.3), TILE_M))
        m.add(1, box("agrippa_base", 3.8, 5.0, 12.0, (-12.6, -27.0, 1.0), ROCK_D))   # pedestal for a bronze chariot (later the Monument of Agrippa)
    else:
        # the Florentine dukes' crenellated upper storey on the north wing, the Frankish tower on the south wing
        m.add(3, box("palace_storey", 10.0, 13.0, 4.0, (-19.0, -18.0, zp + 7.0), STONE), "towers")
        m.add(3, J([box(f"pm{i}", 1.0, 0.8, 1.0, (-24.0 + i * 1.7, -24.6, zp + 11.0), STONE) for i in range(7)], "palace_merlons"))
        m.add(3, hip_roof("palace_roof", 10.0, 9.0, 1.6, (-19.0, -16.0, zp + 11.0), TILE_T, ridge=0.4, overhang=0.3))
        m.add(3, box("frankish_tower", 8.0, 7.6, 26.0, (16.0, -16.0, zp), STONE))
        m.add(3, J([box(f"fm{i}{s}", 1.2, 1.0, 1.4, (12.6 + i * 2.25, -16.0 + s * 3.4, zp + 26.0), STONE) for i in range(4) for s in (-1, 1)], "tower_merlons"))
        for i, z in enumerate((zp + 8, zp + 15, zp + 21)):
            m.add(3, box(f"slit{i}", 0.5, 0.3, 1.6, (16.0, -19.9, z), DARK))
        m.add(1, J([box("batt_wall", 22.0, 2.2, 3.5, (0, -26.0, 0), STONE), box("batt_gate", 3.4, 2.4, 2.8, (0, -26.0, 0), DARK)], "ottoman_battery"))
    return m


def nike():
    m = Model("nike")
    zb = ROCK_H - 1.0
    m.add(0, rock_cap("rock", 14, 20, 3.0, seed=21, top_inset=0.6), "bastion")
    bast = [box("pyrgos", 12.8, 18.8, zb - 3.0, (0, 0, 3.0), POROS)]
    for k in range(1, int((zb - 3.0) / 0.9)):
        bast.append(box(f"course{k}", 12.9, 18.9, 0.06, (0, 0, 3.0 + k * 0.9), shade(POROS, -0.1)))
    m.add(0, J(bast, "pyrgos"))
    par = [box("par_w", 0.35, 18.0, 1.05, (-6.2, 0.4, zb), MARB), box("par_s", 12.6, 0.35, 1.05, (0, -9.2, zb), MARB),
           box("par_n", 12.6, 0.35, 1.05, (0, 9.2, zb), MARB)]
    for i, y in enumerate(lin(-8, 8, 9)):
        par.append(box(f"nk{i}", 0.12, 1.0, 0.8, (-6.42, y, zb + 0.12), MARB_S))
    m.add(1, J(par, "parapet"), "temple")
    zs = zb + 0.75
    m.add(1, crepis("crepis", 5.4, 8.2, 3, 0.25, 0.32, MARB, zb, cy=-1.0))
    m.add(1, copies(ionic("col", 4.1, 0.26, MARB), [(x, y, zs) for x in lin(-2.25, 2.25, 4) for y in (-1.0 - 3.45, -1.0 + 3.45)], "cols"))
    m.add(1, box("cella", 4.6, 4.0, 4.1, (0, -0.6, zs), shade(MARB, -0.03)))
    m.add(1, box("door", 1.4, 0.3, 2.9, (0, -2.65, zs), DARK))
    m.add(2, ionic_entab("ent", 5.3, 8.1, zs + 4.1, 1.05, MARB, BLUE, True, MARB, cy=-1.0, fig_step=0.5), "roof")
    m.add(2, greek_roof("roof", 6.0, 8.8, zs + 5.15, 1.05, TILE_M, MARB, BLUE, figs=True, cy=-1.0, tile_step=0.5, acro_c=GILT))
    m.add(2, box("altar", 2.2, 1.1, 0.9, (0, -8.0, zb), MARB_W))
    return m


def promachos():
    m = Model("promachos")
    m.add(0, rock_cap("rock", 12, 12, ROCK_H, seed=31, top_inset=1.4), "base")
    z = ROCK_H
    m.add(0, box("base1", 5.6, 5.6, 0.6, (0, 0, z), MARB_W))
    m.add(0, box("base2", 4.6, 4.6, 1.5, (0, 0, z + 0.6), MARB))
    m.add(0, box("base3", 4.9, 4.9, 0.25, (0, 0, z + 2.1), MARB_W))
    z += 2.35
    B = "#9A7A4C"
    body = [cylinder("peplos", 0.95, 4.3, (0, 0, z), B, verts=16, r_top=0.62),
            box("overfold", 1.3, 0.95, 0.9, (0, 0, z + 3.0), shade(B, 0.05)),
            cylinder("torso", 0.62, 1.8, (0, 0, z + 4.3), B, verts=16, r_top=0.55),
            box("aegis", 1.2, 0.85, 0.9, (0, -0.1, z + 5.1), shade(B, 0.08)),
            cylinder("neck", 0.22, 0.35, (0, 0, z + 6.1), B, verts=8),
            dome("head", 0.42, (0, 0, z + 6.45), B, squash=1.25, segments=12, rings=6),
            cylinder("helmet", 0.46, 0.35, (0, 0, z + 6.6), shade(B, -0.05), verts=12, r_top=0.4),
            box("crest", 0.16, 1.3, 0.75, (0, 0.05, z + 6.85), GILT),
            box("visor", 0.7, 0.3, 0.12, (0, -0.42, z + 6.75), shade(B, -0.05)),
            box("arm_r", 0.32, 0.32, 1.9, (0.8, -0.25, z + 4.1), B),
            box("arm_l", 0.3, 0.3, 1.8, (-0.8, 0.0, z + 4.0), B),
            cylinder("spear", 0.08, 11.0, (1.0, -0.45, z), B, verts=6),
            cylinder("spear_tip", 0.13, 0.9, (1.0, -0.45, z + 11.0), GILT, verts=6, r_top=0.0),
            cyl_x("shield", 1.55, 0.18, (-1.25, 0.15, z + 1.7), shade(B, 0.04), verts=24),
            cyl_x("boss", 0.4, 0.3, (-1.37, 0.15, z + 1.7), GILT, verts=12)]
    m.add(1, J(body, "athena"), "statue")
    return m


def old_temple(variant="intact"):
    ruin = variant == "ruin"
    m = Model("old-temple" if not ruin else "old-temple-ruin")
    m.add(0, rock_cap("rock", 28, 50, ROCK_H, seed=41, top_inset=2.0), "rock")
    W, D = 21.3, 43.4
    if not ruin:
        peripteral(m, "ot", W, D, 6, 12, 7.8, 0.82, ROCK_H, nsteps=2, rise=0.45, tread=0.6, color=STUC, cella_c=shade(STUC, -0.04), roof_c=TILE_T,
                   relief="none", porch="antis", inner_frieze=False, ped_figs=True, tile_step=0.75)
        return m
    burnt = shade(STUC, -0.22)
    m.add(0, crepis("crepis", W, D, 2, 0.45, 0.6, shade(STUC, -0.1), ROCK_H), "base")
    zs = ROCK_H + 0.9
    pts, xs, ys = peri_pts(W, D, 6, 12, 0.9)
    rnd = random.Random(5)
    stumps = []
    for i, (x, y) in enumerate(pts):
        if y > D / 2 - 9:
            continue
        if rnd.random() < 0.35:
            continue
        h = rnd.uniform(0.6, 4.5)
        stumps.append(cylinder(f"stump{i}", 0.8, h, (x, y, zs), burnt if rnd.random() < 0.5 else shade(STUC, -0.08), verts=12, r_top=0.76))
    m.add(1, J(stumps, "stumps"), "ruins")
    m.add(1, J([box(f"cw{s}", 0.9, 22.0, rnd.uniform(1.0, 2.2), (s * 6.0, -4.0, zs), burnt) for s in (-1, 1)], "cella_walls"))
    drums = []
    for i in range(10):
        d = cyl_x(f"drum{i}", 0.78, 1.1, (rnd.uniform(-9, 9), rnd.uniform(-20, 5), zs + 0.78), shade(STUC, -0.12), verts=12)
        drums.append(d)
    m.add(1, J(drums, "drums"))
    # the western rooms, patched up and roofed as a treasury (one reading of the evidence)
    m.add(2, box("opisthodomos", 13.0, 12.5, 6.0, (0, D / 2 - 8.5, zs), STUC), "treasury")
    m.add(2, box("opd_door", 2.0, 0.3, 3.2, (0, D / 2 - 14.85, zs), DARK))
    m.add(2, tiled_hip_roof("opd_roof", 13.6, 13.1, 2.2, (0, D / 2 - 8.5, zs + 6.0), TILE_T))
    m.add(2, J([cylinder(f"wcol{i}", 0.8, 6.8, (x, D / 2 - 1.8, zs), STUC, verts=16, r_top=0.66) for i, x in enumerate(xs[1:-1])], "west_cols"))
    return m


# ================================================================ the south slope

def theatre_dionysus(variant="hell"):
    m = Model({"hell": "theatre-dionysus", "430": "theatre-dionysus-430", "roman": "theatre-dionysus-roman"}[variant])
    oy = -10.0
    early = variant == "430"
    m.add(0, box("ground", 110, 92, 0.3, (0, 0, 0), EARTH), "cavea")
    m.add(0, rock_arc("cliff", 0, oy, 47.5, 55.5, math.radians(18), math.radians(162), 34.0, seed=3))
    r_orch = 9.8 if not early else 12.0
    if early:
        lo, hi, ztop = cavea("seats", 0, oy, 13.0, 41.0, 0.4, 15.0, 18, 180, 0, [EARTH, EARTH_D, TIMBER], n=36)
        m.add(1, lo, "seats")
        m.add(1, hi)
        m.add(0, cylinder("orchestra", r_orch, 0.5, (0, oy, 0), SAND, verts=40))
        m.add(0, box("terrace_wall", 30.0, 1.2, 2.2, (0, oy - r_orch - 0.6, 0), STONE))
        m.add(2, box("skene", 22.0, 5.0, 5.0, (0, oy - r_orch - 6.5, 0), TIMBER), "stage")
        for i, x in enumerate((-6, 0, 6)):
            m.add(2, box(f"skene_door{i}", 1.6, 0.3, 2.8, (x, oy - r_orch - 3.95, 0), DARK))
        m.add(2, gable_x("skene_roof", 22.0, 5.0, 1.2, (0, oy - r_orch - 6.5, 5.0), TILE_T))
        m.add(2, turn(small_temple("old_temple_dion", 8.0, 13.0, 4.5, 2, "doric", POROS, TILE_T, "antis"), 90, -14.0, -40.0, 0))
        return m
    lo, hi, ztop = cavea("seats", 0, oy, 11.0, 47.0, 0.45, 25.0, 34, 200, -10, [MARB_W, shade(MARB_W, -0.05)], diaz=(14, 25), n=44)
    m.add(1, lo, "seats")
    m.add(1, hi)
    m.add(1, radial_stairs("stairs", 0, oy, 11.0, 47.0, 0.45, ztop, [-10 + 200 * j / 13 for j in range(14)], shade(MARB_W, -0.14)))
    m.add(1, ellipse_ring("prohedria", 10.9, 10.9, 0.9, 1.1, (0, oy, 0), MARB, n=44, arc=math.radians(200), start=math.radians(-10)))
    throne_locs, throne_rots = [], []
    for j in range(30):
        a = math.radians(-6 + 192 * j / 29)
        throne_locs.append((10.4 * math.cos(a), oy + 10.4 * math.sin(a), 0.4))
        throne_rots.append(a + math.pi / 2)
    m.add(1, copies(J([box("th_seat", 0.75, 0.65, 0.9, (0, 0, 0), MARB), box("th_back", 0.75, 0.15, 1.5, (0, 0.3, 0), MARB)], "throne"), throne_locs, "thrones", throne_rots))
    roman = variant == "roman"
    if roman:
        rings = [ellipse_ring(f"pave{k}", r_orch * (k + 1) / 5, r_orch * (k + 1) / 5, (k / (k + 1)) if k else 0.02, 0.5, (0, oy, 0), MARB if k % 2 else "#B9A48A", n=40) for k in range(5)]
        m.add(0, J(rings, "orchestra"))
        m.add(1, ellipse_ring("barrier", r_orch + 0.3, r_orch + 0.3, 0.97, 1.6, (0, oy, 0), MARB_W, n=44, arc=math.radians(200), start=math.radians(-10)))
    else:
        m.add(0, cylinder("orchestra", r_orch, 0.5, (0, oy, 0), SAND, verts=40))
        m.add(0, cylinder("thymele", 0.8, 1.1, (0, oy, 0.5), MARB, verts=12))
    # stage building with paraskenia; Hellenistic proskenion or Roman pulpitum and scaenae frons
    ys0 = oy - r_orch - 5.5           # front face of the skene wall
    m.add(2, box("skene", 46.0, 6.0, 9.0, (0, ys0 - 3.0, 0), MARB_W), "stage")
    m.add(2, hip_roof("skene_roof", 46.0, 6.0, 1.6, (0, ys0 - 3.0, 9.0), TILE_T, ridge=0.8, overhang=0.4))
    for s in (-1, 1):
        m.add(2, box(f"parask{s}", 6.5, 5.0, 7.0, (s * 19.75, ys0 + 2.5, 0), MARB_W))
        m.add(2, copies(doric(f"pcol{s}", 4.6, 0.32, MARB), [(s * 19.75 + dx, ys0 + 5.25, 0.3) for dx in (-2.2, 0, 2.2)], f"pcols{s}"))
    if not roman:
        m.add(2, copies(doric("prcol", 3.0, 0.24, MARB), [(x, ys0 + 4.6, 0) for x in lin(-15.5, 15.5, 14)], "proskenion"))
        m.add(2, box("logeion", 33.0, 5.0, 0.4, (0, ys0 + 2.5, 3.0), TIMBER))
        for i, x in enumerate((-9, 0, 9)):
            m.add(2, box(f"thyroma{i}", 5.0, 0.3, 4.0, (x, ys0 + 0.1, 4.0), DARK))
    else:
        m.add(2, box("pulpitum", 33.0, 6.5, 1.5, (0, ys0 + 3.25, 0), MARB))
        m.add(2, J([box(f"relief{i}", 2.4, 0.2, 1.0, (x, ys0 + 6.55, 0.25), MARB_S) for i, x in enumerate(lin(-14, 14, 9))], "pulpitum_reliefs"))
        for t, z in enumerate((1.5, 5.4)):
            m.add(2, copies(corinth(f"frons{t}", 3.6, 0.22, MARB, rich=False), [(x, ys0 + 0.6, z) for x in lin(-16, 16, 12)], f"frons{t}"))
            m.add(2, box(f"frons_ent{t}", 34.0, 1.2, 0.35, (0, ys0 + 0.6, z + 3.6), MARB))
    # stoa of Dionysus behind the stage, facing the sanctuary; the 4th-century temple
    sy = ys0 - 6.0 - 3.5
    m.add(3, box("stoa_back", 62.0, 1.0, 6.5, (0, sy + 3.0, 0), MARB_W), "sanctuary")
    m.add(3, copies(doric("scol", 5.6, 0.36, MARB), [(x, sy - 3.0, 0) for x in lin(-30, 30, 20)], "stoa_cols"))
    m.add(3, shed("stoa_roof", 63.0, 7.6, 5.8, 7.2, (0, sy, 0), TILE_T, "N"))
    m.add(3, turn(small_temple("temple_dion", 8.0, 14.0, 5.0, 4, "doric", MARB_W, TILE_T, "prostyle"), 90, -20.0, sy - 9.5, 0))
    # Thrasyllos' choregic monument in the cave above the theatre
    tz = 25.5
    m.add(3, box("thr_cave", 7.0, 2.0, 5.0, (0, oy + 49.5, tz), DARK))
    m.add(3, J([box("thr_pier", 0.9, 0.9, 4.4, (x, oy + 48.4, tz), MARB) for x in (-3.0, 0.0, 3.0)] +
               [box("thr_ent", 7.6, 1.2, 1.0, (0, oy + 48.4, tz + 4.4), MARB), cylinder("thr_tripod", 0.5, 1.2, (0, oy + 48.4, tz + 5.4), BRONZE, verts=8, r_top=0.8)], "thrasyllos"))
    return m


def odeon_pericles():
    m = Model("odeon-pericles")
    m.add(0, box("ground", 64, 70, 0.3, (0, 0, 0), EARTH), "walls")
    hy0, hy1 = -28.0, 34.4
    W = 62.4
    m.add(0, box("hall", W, hy1 - hy0, 7.5, (0, (hy0 + hy1) / 2, 0.3), STUC))
    m.add(0, J([box(f"pil{i}{s}", 0.8, 0.4, 7.5, (s * (W / 2 + 0.1), y, 0.3), shade(STUC, 0.04)) for i, y in enumerate(lin(hy0 + 2, hy1 - 2, 12)) for s in (-1, 1)], "pilasters"))
    m.add(0, J([box(f"win{i}", 1.6, 0.3, 1.2, (x, hy0 - 0.1, 5.4), DARK) for i, x in enumerate(lin(-26, 26, 10))], "windows"))
    # the porch on the south
    m.add(1, crepis("porch_steps", 56.0, 6.6, 2, 0.3, 0.4, POROS, 0.0, cy=hy0 - 3.3), "porch")
    m.add(1, copies(doric("pcol", 6.5, 0.48, POROS), [(x, hy0 - 5.9, 0.6) for x in lin(-26, 26, 12)], "porch_cols"))
    m.add(1, doric_entab("porch_ent", 55.0, 6.6, 7.1, 0.8, 0.8, 0.35, 12, 2, POROS, relief="none", cy=hy0 - 3.0, sides="S"))
    m.add(1, shed("porch_roof", 56.6, 7.4, 9.1, 9.9, (0, hy0 - 3.2, 0), TILE_T, "N"))
    # the tent roof: a tiled pyramid with a lantern
    zr = 7.8
    H = 15.0
    D = hy1 - hy0
    cy = (hy0 + hy1) / 2
    parts = [hip_roof("roof", W, D, H, (0, cy, zr), TILE_T, ridge=0.0, overhang=0.8)]
    n = 14
    for k in range(1, n):
        f = k / n
        parts.append(box(f"course{k}", (W + 1.6) * (1 - f), (D + 1.6) * (1 - f), 0.18, (0, cy, zr + H * f - 0.1), shade(TILE_T, 0.08 if k % 2 else -0.04)))
    m.add(2, J(parts, "tent_roof"), "roof")
    m.add(2, box("lantern", 4.0, 4.0, 2.2, (0, cy, zr + H - 1.4), STUC))
    m.add(2, J([box(f"lw{i}", 0.6, 4.1, 1.2, (-1.2 + i * 1.2, cy, zr + H - 0.6), DARK) for i in range(3)], "lantern_open"))
    m.add(2, hip_roof("lantern_roof", 4.4, 4.4, 1.6, (0, cy, zr + H + 0.8), TILE_T, ridge=0.0, overhang=0.3))
    return m


def odeon_herodes():
    m = Model("odeon-herodes")
    cy = -10.0
    m.add(0, box("ground", 88, 60, 0.3, (0, 0, 0), EARTH), "cavea")
    m.add(0, ellipse_ring("outer_wall", 39.5, 39.5, 37.0 / 39.5, 25.0, (0, cy, 0), STONE, n=40, arc=math.pi, start=0))
    lo, hi, ztop = cavea("seats", 0, cy, 10.5, 37.0, 0.5, 23.0, 32, 180, 0, [MARB_W, shade(MARB_W, -0.05)], diaz=(20,), n=40)
    m.add(1, lo, "seats")
    m.add(1, hi)
    m.add(1, radial_stairs("stairs", 0, cy, 10.5, 37.0, 0.5, ztop, [180 * j / 9 for j in range(10)], shade(MARB_W, -0.15)))
    pave = [ellipse_ring(f"pave{k}", 10.0 * (k + 1) / 4, 10.0 * (k + 1) / 4, (k / (k + 1)) if k else 0.02, 0.45, (0, cy, 0), "#3E3B3A" if k % 2 else MARB, n=32, arc=math.pi, start=0) for k in range(4)]
    m.add(0, J(pave, "orchestra"))
    # outer arches on the curved wall
    locs, rots = [], []
    for t, z in enumerate((4.0, 13.0)):
        for j in range(12):
            a = math.pi * (j + 0.5) / 12
            locs.append((39.6 * math.cos(a), cy + 39.6 * math.sin(a), z))
            rots.append(a + math.pi / 2)
    m.add(1, copies(box("oarch", 2.4, 0.4, 5.5, (0, 0, 0), DARK), locs, "outer_arches", rots))
    # stage, scaenae frons, foyer and the arcaded south facade
    m.add(2, box("stage", 72.0, 7.0, 1.4, (0, -13.5, 0), MARB), "stage")
    m.add(2, box("frons", 72.0, 3.0, 26.0, (0, -18.5, 0), STONE))
    for t, z in enumerate((1.4, 9.4, 17.4)):
        m.add(2, J([box(f"niche{t}{i}", 2.4, 0.3, 5.0, (x, -16.95, z + 0.8), DARK) for i, x in enumerate(lin(-30, 30, 9))], f"niches{t}"))
        m.add(2, copies(plain_col(f"fc{t}", 6.6, 0.32, MARB), [(x, -16.4, z) for x in lin(-32, 32, 17)], f"frons_cols{t}"))
        m.add(2, box(f"frons_ent{t}", 70.0, 1.0, 0.6, (0, -16.4, z + 6.6), MARB))
    m.add(2, box("foyer", 80.0, 7.0, 18.0, (0, -23.5, 0), STONE))
    m.add(2, box("facade", 82.0, 3.0, 28.0, (0, -28.5, 0), STONE))
    for t, (z, h, n) in enumerate(((0.3, 8.0, 9), (10.0, 6.5, 9), (18.5, 5.5, 9))):
        m.add(2, arcade(f"facade_arches{t}", 76.0, h, n, (0, -30.05, z), "S", DARK, pointed=False, fill=0.62))
    for s in (-1, 1):
        m.add(2, box(f"stair_tower{s}", 8.0, 22.0, 22.0, (s * 40.0, -19.0, 0), STONE))
        m.add(2, box(f"tower_cap{s}", 8.6, 22.6, 0.6, (s * 40.0, -19.0, 22.0), shade(STONE, 0.06)))
    m.add(2, box("facade_cornice", 82.6, 3.6, 0.7, (0, -28.5, 28.0), shade(STONE, 0.06)))
    return m


# ================================================================ the Agora

def stoa_poikile():
    m = Model("stoa-poikile")
    L, Dp = 38.0, 12.6
    m.add(0, box("ground", 42, 16, 0.2, (0, 0, 0), SAND), "base")
    m.add(0, crepis("crepis", L, Dp, 2, 0.35, 0.45, POROS, 0.2))
    z = 0.9
    m.add(1, copies(doric("col", 5.8, 0.42, MARB_W), [(x, -Dp / 2 + 0.6, z) for x in lin(-L / 2 + 0.6, L / 2 - 0.6, 15)], "outer"), "columns")
    m.add(1, copies(ionic("icol", 7.2, 0.34, MARB_W), [(x, 0.4, z) for x in lin(-15, 15, 7)], "inner"))
    m.add(1, box("back", L, 0.9, 7.6, (0, Dp / 2 - 0.45, z), STUC))
    for s in (-1, 1):
        m.add(1, box(f"end{s}", 0.9, Dp - 1.0, 7.0, (s * (L / 2 - 0.45), 0.5, z), STUC))
    for i, (x, c) in enumerate(zip(lin(-13.5, 13.5, 4), (RED, BLUE, OCHRE, GREEN_P))):
        m.add(1, box(f"painting{i}", 7.2, 0.12, 2.6, (x, Dp / 2 - 0.95, z + 1.6), c))
        m.add(1, box(f"frame{i}", 7.6, 0.08, 3.0, (x, Dp / 2 - 0.92, z + 1.4), shade(TIMBER, -0.1)))
    # spoils: bronze shields hung on the back wall
    m.add(1, J([cyl_y(f"shield{i}", 0.45, 0.12, (x, Dp / 2 - 1.0, z + 4.9), BRONZE, verts=12) for i, x in enumerate(lin(-16, 16, 9))], "shields"))
    m.add(2, doric_entab("ent", L - 0.1, Dp, z + 5.8, 0.75, 0.75, 0.32, 15, 5, MARB_W, relief="none"), "roof")
    roof = greek_roof("roof", Dp + 1.0, L + 1.0, 0, 2.2, TILE_T, MARB_W, BLUE, figs=False, tile_step=0.8)
    m.add(2, turn(roof, 90, 0, 0, z + 5.8 + 1.82))
    return m


def stoa_attalos():
    m = Model("stoa-attalos")
    L = 107.0
    yf, yb = -8.0, 10.6
    m.add(0, box("terrace", 116, 22, 0.6, (0, 0, 0), SAND), "base")
    m.add(0, crepis("crepis", L + 2.0, yb - yf + 2.0, 2, 0.3, 0.4, MARB_W, 0.6, cy=(yf + yb) / 2))
    z = 1.2
    m.add(1, copies(doric("col", 5.0, 0.4, MARB, flutes=20), [(x, yf, z) for x in lin(-L / 2 + 0.6, L / 2 - 0.6, 45)], "lower_outer"), "ground floor")
    m.add(1, copies(ionic("icol", 6.0, 0.33, MARB), [(x, -0.6, z) for x in lin(-50, 50, 22)], "lower_inner"))
    m.add(1, box("shopfront", L, 0.8, 11.6, (0, 5.0, z), MARB_W))
    m.add(1, J([box(f"shop{i}{t}", 1.4, 0.3, 2.6 if t == 0 else 2.0, (x, 4.55, z + (0 if t == 0 else 6.8)), DARK) for i, x in enumerate(lin(-50, 50, 21)) for t in (0, 1)], "shop_doors"))
    m.add(1, box("shops", L, yb - 5.4, 11.6, (0, (5.4 + yb) / 2, z), shade(MARB_W, -0.03)))
    for s in (-1, 1):
        m.add(1, box(f"end{s}", 1.0, yb - yf + 0.4, 11.6, (s * (L / 2 + 0.5), (yf + yb) / 2, z), MARB_W))
    m.add(1, J([box(f"bwin{i}", 0.9, 0.3, 1.2, (x, yb + 0.1, z + 8.4), DARK) for i, x in enumerate(lin(-50, 50, 21))], "back_windows"))
    m.add(2, doric_entab("lent", L + 0.6, 1.4, z + 5.0, 0.55, 0.55, 0.25, 45, 2, MARB, relief="none", cy=yf, sides="S"), "upper floor")
    m.add(2, box("upper_floor", L, 13.0, 0.4, (0, -1.6, z + 6.0), MARB_W))
    zu = z + 6.4
    m.add(2, copies(ionic("ucol", 4.4, 0.3, MARB), [(x, yf, zu) for x in lin(-L / 2 + 0.6, L / 2 - 0.6, 45)], "upper_outer"))
    m.add(2, box("balustrade", L - 0.6, 0.25, 1.05, (0, yf, zu), MARB_W))
    m.add(2, copies(plain_col("uicol", 5.2, 0.28, MARB), [(x, -0.6, zu) for x in lin(-50, 50, 22)], "upper_inner"))
    m.add(3, ionic_entab("uent", L + 0.8, yb - yf + 0.8, zu + 4.4, 1.1, MARB, figs=False, dentils=False, cy=(yf + yb) / 2), "roof")
    roof = greek_roof("roof", yb - yf + 2.2, L + 2.6, 0, 2.6, TILE_T, MARB, MARB_W, figs=False, acro=False, tile_step=0.95)
    m.add(3, turn(roof, 90, 0, (yf + yb) / 2, zu + 5.5))
    for s in (-1, 1):
        m.add(1, crepis(f"end_stair{s}", 4.0, 7.0, 6, 0.6, 0.35, MARB_W, 0.6, cx=s * (L / 2 + 2.5), cy=yb - 4.0))
    return m


def hephaisteion(variant="temple"):
    church = variant == "church"
    m = Model("hephaisteion" if not church else "hephaisteion-church")
    W, D = 13.71, 31.77
    m.add(0, rock_cap("kolonos", 24, 44, 2.6, seed=51, top_inset=1.6, color="#B4A685", shrubs=10), "hill")
    rnd = random.Random(52)
    m.add(0, J([dome(f"bush{i}", rnd.uniform(0.5, 0.8), (s * (W / 2 + 2.3), y, 2.6), SCRUB, squash=1.1, segments=8, rings=4) for i, y in enumerate(lin(-16, 16, 9)) for s in (-1, 1)], "garden"))
    t = peripteral(m, "hp", W, D, 6, 13, 5.71, 0.5, 2.6, nsteps=3, rise=0.33, tread=0.4, color=MARB, roof_c=TILE_T, relief="front",
                   porch="antis", front_porch=not church, inner_frieze=True, frieze_c=BLUE, roof=not church, tile_step=0.6)
    m.add(1, box("altar", 2.4, 1.6, 1.0, (0, -D / 2 - 3.6, 2.6), MARB_W))
    if church:
        # Byzantine conversion: a barrel vault over the cella, an apse in the east porch, the pteron re-roofed
        zr = t["zr"]
        m.add(1, cylinder("apse", 2.4, 5.0, (0, t["wf"], t["zc"]), PLAST, verts=20), "columns")
        m.add(3, half_cyl_y("vault", 3.9, t["wb"] - t["wf"] + 2.0, (0, (t["wf"] + t["wb"]) / 2, zr - 0.6), "#CBBFA6", verts=20), "roof")
        g = greek_roof("gables", t["Wr"], t["Dr"], zr, t["rh"], "#BCA98A", MARB, BLUE, figs=True, tiles=False)
        m.add(3, g)
        m.add(3, box("cross_door", 1.2, 0.3, 2.4, (0, t["wb"] + 0.2, t["zc"]), DARK))
    return m


def bouleuterion(variant="hell"):
    m = Model({"hell": "bouleuterion", "430": "bouleuterion-430", "f": "building-f"}[variant])
    m.add(0, box("ground", 60, 36, 0.2, (0, 0, 0), SAND), "ground")
    if variant == "f":
        m.add(1, court_house("building_f", 26.0, 24.0, 5.5, 3.6, (-9.0, 2.0, 0.2), MUDB, TILE_T), "house")
        m.add(1, court_house("building_c", 12.0, 10.0, 3.5, 3.0, (14.0, -4.0, 0.2), MUDB, TILE_T))
        m.add(1, box("well", 1.2, 1.2, 0.8, (-9.0, 2.0, 0.2), STONE))
        m.add(1, J([box(f"stone{i}", 0.4, 0.4, 1.1, (x, -15.0, 0.2), MARB_W) for i, x in enumerate((-20.0, 8.0))], "boundary"))
        m.add(1, tree("plane", 2.6, (12.0, 10.0, 0.2), "#6F8A5C", TIMBER))
        return m
    # the Tholos: a round hall with a conical tiled roof, at the south end
    tx = -20.5
    th = [cylinder("tholos_wall", 9.15, 4.6, (tx, 0, 0.2), STUC, verts=36), cylinder("tholos_eave", 9.7, 0.4, (tx, 0, 4.8), shade(STUC, 0.05), verts=36),
          cylinder("tholos_roof", 9.9, 4.2, (tx, 0, 5.2), TILE_T, verts=36, r_top=0.9), cylinder("tholos_lantern", 1.0, 0.9, (tx, 0, 9.4), STUC, verts=12),
          box("tholos_door", 1.6, 0.3, 2.6, (tx, -9.2, 0.2), DARK)]
    ribs = []
    for i in range(24):
        a = math.tau * i / 24
        rb = beam(f"rib{i}", 9.2, 0.18, 0.15, -math.atan2(4.2, 9.0), (5.0, 0, 5.2 + 2.1 + 0.1), shade(TILE_T, 0.1))
        ribs.append(turn(rb, math.degrees(a), tx, 0, 0))
    m.add(1, J(th + ribs, "tholos"), "buildings")
    if variant == "430":
        ob = [box("old_bouleuterion", 23.0, 23.0, 7.0, (6.0, 2.0, 0.2), STUC), box("ob_door", 2.0, 0.3, 3.0, (6.0, -9.6, 0.2), DARK)]
        m.add(1, J(ob, "old_bouleuterion"))
        m.add(2, tiled_hip_roof("ob_roof", 23.8, 23.8, 4.0, (6.0, 2.0, 7.2), TILE_T), "roofs")
        m.add(1, small_temple("propylon", 4.0, 4.0, 3.6, 2, "doric", POROS, TILE_T, "antis"))
        m.add(1, J([box(f"stone{i}", 0.4, 0.4, 1.1, (x, -15.0, 0.2), MARB_W) for i, x in enumerate((-28.0, 22.0))], "boundary"))
        m.add(1, J([box("archives", 9.0, 7.0, 4.0, (24.0, 8.0, 0.2), STUC)], "archives"))
        m.add(2, tiled_hip_roof("arch_roof", 9.6, 7.6, 1.6, (24.0, 8.0, 4.2), TILE_T))
        return m
    # New Bouleuterion behind, with its porch; the Metroon's long Ionic front facing the square
    nb = [box("new_bouleuterion", 22.0, 17.0, 9.0, (8.0, 8.5, 0.2), STUC)]
    m.add(1, J(nb, "new_bouleuterion"))
    m.add(2, tiled_hip_roof("nb_roof", 22.8, 17.8, 3.4, (8.0, 8.5, 9.2), TILE_T), "roofs")
    m.add(1, box("metroon", 38.0, 10.0, 7.0, (11.0, -8.0, 0.2), STUC))
    m.add(1, J([box(f"mdoor{i}", 1.6, 0.3, 3.0, (x, -13.05, 0.6), DARK) for i, x in enumerate((-2.0, 7.0, 16.0, 25.0))], "metroon_doors"))
    m.add(1, crepis("m_steps", 39.0, 4.0, 2, 0.2, 0.3, MARB_W, 0.2, cx=11.0, cy=-15.0))
    m.add(1, copies(ionic("mcol", 6.0, 0.33, MARB), [(x, -16.3, 0.6) for x in lin(-6.5, 28.5, 14)], "metroon_cols"))
    m.add(2, ionic_entab("m_ent", 38.6, 15.0, 6.6, 0.9, MARB, figs=False, cy=-10.4), "roofs")
    mroof = greek_roof("m_roof", 16.0, 39.6, 0, 2.2, TILE_T, MARB, BLUE, figs=False, tile_step=0.9)
    m.add(2, turn(mroof, 90, 11.0, -10.4, 7.5))
    m.add(1, copies(plain_col("tpc", 3.2, 0.25, MARB), [(tx + dx, -9.9, 0.2) for dx in (-1.6, 1.6)], "tholos_porch"))
    m.add(1, box("tholos_porch_roof", 4.6, 2.0, 0.4, (tx, -9.9, 3.4), TILE_T))
    return m


def altar_twelve():
    m = Model("altar-twelve")
    m.add(0, box("pave", 10.0, 10.0, 0.25, (0, 0, 0), MARB_W), "enclosure")
    posts, panels = [], []
    side = 9.4
    for s in "SNWE":
        for k, t in enumerate(lin(-side / 2, side / 2, 7)):
            if s == "W" and k in (3,):
                continue
            x, y = {"S": (t, -side / 2), "N": (t, side / 2), "W": (-side / 2, t), "E": (side / 2, t)}[s]
            posts.append(box(f"post{s}{k}", 0.35, 0.35, 1.3, (x, y, 0.25), MARB))
        for k in range(6):
            t = -side / 2 + (k + 0.5) * side / 6
            if s == "W" and k in (2, 3):
                continue
            x, y = {"S": (t, -side / 2), "N": (t, side / 2), "W": (-side / 2, t), "E": (side / 2, t)}[s]
            w, d = ((side / 6 - 0.35), 0.16) if s in "SN" else (0.16, (side / 6 - 0.35))
            panels.append(box(f"panel{s}{k}", w, d, 0.95, (x, y, 0.25), shade(MARB, -0.06)))
    m.add(1, J(posts + panels, "parapet"), "parapet")
    m.add(1, crepis("altar_steps", 2.2, 2.2, 2, 0.2, 0.25, MARB_W, 0.25))
    m.add(1, J([box("altar", 1.8, 1.8, 1.0, (0, 0, 0.65), MARB), box("altar_top", 2.0, 2.0, 0.15, (0, 0, 1.65), shade(MARB, 0.04)),
                box("hearth", 1.0, 1.0, 0.12, (0, 0, 1.8), DARK)], "altar"))
    return m


def pnyx(variant="iii"):
    early = variant == "430"
    m = Model("pnyx" if not early else "pnyx-430")
    cyb = -28.0
    R = 54.0
    if early:
        m.add(0, rock_cap("hilltop", 110, 14, 9.0, seed=61, top_inset=2.0, loc=(0, -33.0, 0)), "hill")
        m.add(0, sloped_fan("slope", R, cyb, 9.0, 2.0, n=30, color=GRASS), "hill")
        m.add(1, ellipse_ring("lower_wall", R + 1.0, R + 1.0, R / (R + 1.0), 2.6, (0, cyb, 0), STONE, n=40, arc=math.radians(120), start=math.radians(30)), "assembly")
        m.add(1, J([box("bema1", 4.0, 3.0, 2.8, (0, cyb + R - 4.5, 0), ROCK), box("bema_step", 4.0, 1.2, 1.2, (0, cyb + R - 6.6, 0), ROCK)], "bema"))
        rnd = random.Random(62)
        m.add(1, J([box(f"rock{i}", rnd.uniform(1, 2.5), rnd.uniform(1, 2.5), rnd.uniform(0.4, 1.0), (rnd.uniform(-35, 35), cyb + rnd.uniform(6, 40), 0), ROCK_D, rot_z=rnd.random() * 3) for i in range(14)], "outcrops"))
        return m
    m.add(0, rock_cap("scarp", 110, 14, 8.0, seed=63, top_inset=0.6, loc=(0, -33.0, 0)), "hill")
    m.add(0, sloped_fan("auditorium", R, cyb, 3.0, 8.4, n=30, color=GRASS), "hill")
    m.add(1, ellipse_ring("retaining_wall", R + 2.6, R + 2.6, R / (R + 2.6), 9.6, (0, cyb, 0), STONE, n=48, arc=math.pi, start=0), "walls")
    m.add(1, J([ellipse_ring(f"course{k}", R + 2.68, R + 2.68, (R + 2.5) / (R + 2.68), 0.14, (0, cyb, 1.4 * (k + 1)), shade(STONE, -0.1), n=48, arc=math.pi, start=0) for k in range(6)], "courses"))
    # the rock-cut bema with its side stairs, against the scarp
    bema = [box("bema_t1", 10.0, 4.6, 1.2, (0, cyb + 2.3, 3.0), ROCK), box("bema_t2", 6.4, 3.4, 1.2, (0, cyb + 1.7, 4.2), ROCK),
            box("bema_cube", 2.8, 2.8, 1.6, (0, cyb + 1.4, 5.4), shade(ROCK, 0.05))]
    for s in (-1, 1):
        for k in range(4):
            bema.append(box(f"bst{s}{k}", 1.4, 1.2, 0.6 * (k + 1), (s * (6.0 + 1.4 * (3 - k)), cyb + 1.0, 3.0), ROCK))
    m.add(1, J(bema, "bema"))
    # above the scarp: the altar of Zeus Agoraios and the foundations of two unfinished stoas
    m.add(2, J([box("stoa_f1", 92.0, 1.4, 0.7, (0, -36.0, 8.0), STONE), box("stoa_f2", 92.0, 1.4, 0.7, (0, -38.8, 8.0), STONE),
                box("altar", 3.2, 2.4, 1.2, (0, -31.5, 8.0), MARB_W)], "terrace"), "terrace")
    return m


# ================================================================ the south-east

def olympieion(variant="complete"):
    names = {"complete": "olympieion", "platform": "olympieion-platform", "antiochus": "olympieion-antiochus", "ruin": "olympieion-ruin"}
    m = Model(names[variant])
    W, D = 41.1, 107.75
    m.add(0, box("precinct", 56, 120, 0.4, (0, 0, 0), SAND if variant != "ruin" else GRASS), "platform")
    pts_x = lin(-W / 2 + 1.3, W / 2 - 1.3, 8)
    pts_y = lin(-D / 2 + 1.3, D / 2 - 1.3, 20)
    allpts = [(x, y) for y in pts_y[:3] + pts_y[-3:] for x in pts_x] + [(x, y) for y in pts_y[3:-3] for x in (pts_x[0], pts_x[1], pts_x[-2], pts_x[-1])]
    if variant == "platform":
        # the tyrants' foundation in limestone, part-built, with Doric drums stacked and lying about
        m.add(0, box("found", W + 3.0, D + 3.0, 1.2, (0, 0, 0.4), POROS))
        m.add(0, box("found2", W + 1.0, D - 30.0, 0.8, (0, -14.0, 1.6), shade(POROS, 0.04)))
        rnd = random.Random(71)
        stacks = [cylinder(f"drum_st{i}", 1.2, rnd.uniform(1.0, 4.5), (x, pts_y[0], 2.4), POROS, verts=16, r_top=1.15) for i, x in enumerate(pts_x[1:6])]
        m.add(1, J(stacks, "drum_stacks"), "drums")
        lying = [cyl_x(f"drum_l{i}", 1.2, 1.4, (rnd.uniform(-24, 24), rnd.uniform(-50, 50), 1.6), shade(POROS, -0.05), verts=14) for i in range(16)]
        m.add(1, J(lying, "drums_lying"))
        m.add(1, J([box(f"block{i}", rnd.uniform(1.5, 3), rnd.uniform(1, 2), 0.8, (rnd.uniform(-26, 26), rnd.uniform(-55, 55), 0.4), shade(POROS, -0.08), rot_z=rnd.random() * 3) for i in range(14)], "blocks"))
        return m
    if variant == "ruin":
        m.add(0, crepis("crepis", W, D, 2, 0.6, 0.8, shade(MARB_W, -0.05), 0.4), "platform")
        m.add(0, box("silt", W + 6.0, D + 6.0, 0.9, (0, 0, 0.4), shade(GRASS, -0.05)))
        zs = 1.6
        se = [(x, y) for y in pts_y[:3] for x in pts_x[:4]] + [(pts_x[0], pts_y[3])]
        sw = [(pts_x[0], pts_y[-1]), (pts_x[1], pts_y[-1]), (pts_x[0], pts_y[-2]), (pts_x[1], pts_y[-2])]
        m.add(1, copies(corinth("col", 17.25, 0.85, MARB_W, rich=False), [(x, y, zs) for x, y in se + sw], "standing"), "columns")
        arch = [box("arch_x0", pts_x[3] - pts_x[0] + 2.2, 1.6, 1.4, ((pts_x[0] + pts_x[3]) / 2, y, zs + 17.25), MARB_W) for y in pts_y[:3]]
        arch += [box("arch_y0", 1.6, pts_y[2] - pts_y[0] + 2.2, 1.4, (x, (pts_y[0] + pts_y[2]) / 2, zs + 17.25 + 1.4), MARB_W) for x in pts_x[:4]]
        m.add(2, J(arch, "architraves"), "architraves")
        rnd = random.Random(73)
        m.add(2, J([cyl_x(f"fallen{i}", 0.85, rnd.uniform(1.5, 3.0), (rnd.uniform(-18, 18), rnd.uniform(-10, 45), 1.3 + 0.85), MARB_W, verts=14) for i in range(12)], "fallen"))
        m.add(2, J([tree(f"t{i}", rnd.uniform(1.5, 2.4), (rnd.uniform(-25, 25), rnd.uniform(-55, 55), 0.4), OLIVE) for i in range(7)], "trees"))
        return m
    m.add(0, crepis("crepis", W, D, 3, 0.6, 0.8, MARB_W, 0.4))
    zs = 2.2
    rich = variant == "complete"
    m.add(1, copies(corinth("col", 17.25, 0.85, MARB, rich=False), [(x, y, zs) for x, y in allpts], "columns"), "columns")
    ch = 17.25 if rich else 9.0
    m.add(1, box("cella", 22.0, pts_y[-4] - pts_y[3], ch, (0, (pts_y[3] + pts_y[-4]) / 2, zs), shade(MARB, -0.03)))
    m.add(1, box("door", 5.0, 0.3, 10.0 if rich else 8.5, (0, pts_y[3] - 0.15, zs), DARK if rich else shade(MARB, -0.1)))
    zt = zs + 17.25
    if variant == "antiochus":
        m.add(2, J([box("arch_e", W - 1.0, 1.8, 1.5, (0, pts_y[0], zt), MARB), box("arch_w", W - 1.0, 1.8, 1.5, (0, pts_y[1], zt), MARB)], "architraves"), "architraves")
        m.add(2, J([box(f"scaff{i}", 0.25, 0.25, 19.0, (pts_x[0] - 1.6, y, 0.4), TIMBER) for i, y in enumerate(lin(-20, 40, 8))], "scaffold"))
        return m
    # entablature: three-fascia architrave, frieze, cornice with a modillion band; tiled roof with pediments
    Wa, Da = W - 0.6, D - 0.6
    m.add(2, ionic_entab("ent", Wa, Da, zt, 3.8, MARB, figs=False), "entablature")
    m.add(2, box("modillions", Wa + 1.6, Da + 1.6, 0.25, (0, 0, zt + 3.8 * 0.70 + 0.05), shade(MARB, -0.12)))
    m.add(3, greek_roof("roof", Wa + 2.4, Da + 2.4, zt + 3.8, 5.6, TILE_T, MARB, shade(MARB, -0.08), figs=True, fig_c=MARB_S, tile_step=1.0), "roof")
    m.add(3, J([figure(f"hadrian{i}", x, -D / 2 - 5.0, 0.4, 3.2, BRONZE) for i, x in enumerate(lin(-16, 16, 6))], "statues"))
    return m


def hadrians_arch():
    m = Model("hadrians-arch")
    w, t = 13.5, 2.3
    m.add(0, box("plinth", w + 0.6, t + 0.8, 0.5, (0, 0, 0), MARB_W), "arch")
    body = arch_bay("arch", w, 10.2, t, 3.05, 6.0, MARB, keystone=True)
    m.add(0, turn(body, 0, 0, 0, 0.5))
    pil = []
    for sd in (-1, 1):
        for x in (-w / 2 + 0.5, -4.0, 4.0, w / 2 - 0.5):
            pil.append(box(f"pil{sd}{x}", 0.9, 0.3, 9.0, (x, sd * (t / 2 + 0.1), 0.5), shade(MARB, 0.03)))
    m.add(0, J(pil, "pilasters"))
    locs = [(x, sd * (t / 2 + 1.0), 0.5) for sd in (-1, 1) for x in (-4.9, 4.9)]
    m.add(1, copies(J([box("ped", 1.5, 1.5, 1.6, (0, 0, 0), MARB_W), turn(corinth("c", 8.6, 0.45, MARB, rich=True), 0, 0, 0, 1.6)], "colped"), locs, "free_columns"), "columns")
    m.add(1, J([box(f"ent_break{i}", 1.5, 1.2, 1.2, (x, y, 10.7), MARB) for i, (x, y, _) in enumerate(locs)], "breaks"))
    m.add(1, ionic_entab("ent", w, t, 10.7, 1.4, MARB, figs=False, dentils=True))
    m.add(1, J([box(f"inscr{sd}", 7.0, 0.1, 0.25, (0, sd * (t / 2 + 0.36), 11.05), DARK) for sd in (-1, 1)], "inscriptions"))
    # upper storey: an open screen of Corinthian columns with a pediment over the middle bay
    zu = 12.1
    m.add(2, box("attic_base", 10.6, 2.0, 0.6, (0, 0, zu), MARB_W), "attic")
    for s in (-1, 1):
        m.add(2, box(f"attic_pier{s}", 1.2, 1.6, 4.8, (s * 4.6, 0, zu + 0.6), MARB))
    m.add(2, box("attic_screen", 3.6, 0.6, 4.8, (0, 0, zu + 0.6), shade(MARB, -0.05)))
    m.add(2, copies(corinth("uc", 4.6, 0.26, MARB, rich=False), [(x, y, zu + 0.6) for y in (-1.15, 1.15) for x in (-2.4, 2.4)], "upper_cols"))
    m.add(2, box("upper_ent", 10.6, 2.6, 0.7, (0, 0, zu + 5.2), MARB))
    ped = greek_roof("ped", 5.8, 3.0, zu + 5.9, 1.4, MARB_W, MARB, shade(MARB, -0.08), figs=False, tiles=False, acro=True)
    m.add(2, ped)
    return m


def lysicrates():
    m = Model("lysicrates")
    m.add(0, box("pave", 5.6, 5.6, 0.2, (0, 0, 0), SAND), "base")
    LS = "#C9B58C"
    m.add(0, J([box("base_mould", 3.3, 3.3, 0.3, (0, 0, 0.2), LS), box("base", 2.9, 2.9, 3.8, (0, 0, 0.5), LS),
                box("base_crown", 3.3, 3.3, 0.35, (0, 0, 4.3), shade(LS, 0.05))], "base"))
    z = 4.65
    m.add(1, cylinder("plinth", 1.35, 0.45, (0, 0, z), MARB_W, verts=24), "monument")
    z += 0.45
    m.add(1, cylinder("drum", 0.98, 3.5, (0, 0, z), MARB, verts=24))
    locs, rots = [], []
    for k in range(6):
        a = math.tau * k / 6 + math.pi / 6
        locs.append((1.05 * math.cos(a), 1.05 * math.sin(a), z))
        rots.append(a)
    m.add(1, copies(corinth("c", 3.5, 0.17, MARB, base=True, rich=True), locs, "cols", rots))
    m.add(1, J([box(f"tripod_rel{k}", 0.35, 0.12, 0.6, (1.0 * math.cos(math.tau * k / 6), 1.0 * math.sin(math.tau * k / 6), z + 2.7), MARB_S, rot_z=math.tau * k / 6 + math.pi / 2) for k in range(6)], "reliefs"))
    z += 3.5
    m.add(2, J([cylinder("arch", 1.2, 0.28, (0, 0, z), MARB, verts=24), cylinder("frieze", 1.17, 0.3, (0, 0, z + 0.28), MARB_S, verts=24),
                cylinder("cornice", 1.32, 0.2, (0, 0, z + 0.58), MARB, verts=24), cylinder("roof", 1.32, 0.55, (0, 0, z + 0.78), MARB_W, verts=24, r_top=0.45)], "roof"), "roof")
    zt = z + 1.33
    m.add(2, lathe("finial", [(0.45, 0), (0.55, 0.25), (0.3, 0.5), (0.42, 0.75), (0.2, 1.05), (0.25, 1.2), (0.0, 1.25)], (0, 0, zt), MARB, verts=12))
    zt += 1.25
    legs = []
    for k in range(3):
        a = math.tau * k / 3
        o = beam(f"leg{k}", 1.7, 0.1, 0.1, -math.radians(70), (0.25, 0, 0.8), BRONZE)
        legs.append(turn(o, math.degrees(a), 0, 0, zt))
    legs.append(cylinder("bowl", 0.2, 0.5, (0, 0, zt + 1.0), BRONZE, verts=12, r_top=0.58))
    legs.append(cylinder("rim", 0.58, 0.12, (0, 0, zt + 1.5), BRONZE, verts=12))
    m.add(2, J(legs, "tripod"))
    return m


def stadium(variant="roman"):
    lyc = variant == "lycurgan"
    m = Model("stadium" if not lyc else "stadium-lycurgan")
    # built along X (open end at -X, sphendone at +X), turned at the end so the open end faces -Y
    Ltot, Wtot = 260.0, 90.0
    x_open, r_in = -118.0, 16.7
    xc = Ltot / 2 - 44.0
    objs = {0: [], 1: [], 2: [], 3: []}
    objs[0].append(box("ground", Ltot, Wtot, 0.3, (0, 0, 0), GRASS))
    track = mesh_from("track", [(x, y, 0.35) for x, y in u_pts(x_open, xc, r_in, 24)], [tuple(range(len(u_pts(x_open, xc, r_in, 24))))], (0, 0, 0), SAND)
    objs[0].append(track)
    rows, step, rise = (34, 0.8, 0.4) if not lyc else (12, 2.27, 1.13)
    z = 0.3
    for k in range(rows):
        ra, rb = r_in + step * k, r_in + step * (k + 1)
        z += rise
        if lyc:
            col = MARB_W if k < 2 else (GRASS if k % 2 else shade(GRASS, -0.05))
        else:
            col = MARB if k % 2 else shade(MARB, -0.04)
        o = ring_extrude(f"row{k}", u_pts(x_open + 2.0, xc, rb, 24), u_pts(x_open + 2.0, xc, ra, 24), z, (0, 0, 0), col, closed=False)
        objs[1 if k < rows // 2 else 2].append(o)
    if not lyc:
        # stairways up the banks and a parapet along the top
        L = math.hypot(step * rows, rise * rows)
        th = -math.atan2(rise * rows, step * rows)
        for i, x in enumerate(lin(x_open + 12.0, xc, 9)):
            for s in (-1, 1):
                o = beam(f"st{i}{s}", L, 0.9, 0.3, th, (r_in + step * rows / 2, 0, 0.3 + rise * rows / 2 + 0.2), shade(MARB, -0.12))
                objs[2].append(turn(o, 90 * s, x, 0, 0))
        for j in range(1, 8):
            a = -math.pi / 2 + math.pi * j / 8
            o = beam(f"sst{j}", L, 0.9, 0.3, th, (r_in + step * rows / 2, 0, 0.3 + rise * rows / 2 + 0.2), shade(MARB, -0.12))
            objs[2].append(turn(o, math.degrees(a), xc, 0, 0))
        ro = r_in + step * rows
        objs[3].append(ring_extrude("parapet", u_pts(x_open + 2.0, xc, ro + 0.5, 24), u_pts(x_open + 2.0, xc, ro, 24), z + 1.1, (0, 0, 0), MARB_W, closed=False))
        # propylon at the open end and the double herms at the turning posts
        prop = small_temple("propylon", 12.0, 5.0, 6.0, 4, "doric", MARB, TILE_M, "prostyle")
        objs[3].append(turn(prop, -90, x_open - 4.0, 0, 0))
        for i, x in enumerate((x_open + 8.0, xc - 4.0)):
            for s in (-1, 1):
                objs[3].append(J([box(f"herm{i}{s}", 0.6, 0.6, 2.4, (x, s * 1.5, 0.35), MARB), box(f"hermh{i}{s}", 0.5, 0.5, 0.6, (x, s * 1.5, 2.75), MARB_S)], f"herm{i}{s}"))
    else:
        objs[3].append(J([box(f"post{i}", 0.5, 0.5, 1.6, (x, 0, 0.35), POROS) for i, x in enumerate((x_open + 8.0, xc - 4.0))], "turning_posts"))
    labels = {0: "ground", 1: "seats", 2: "upper seats", 3: "propylon"}
    for st in range(4):
        o = J(objs[st], f"stage{st}")
        if o is not None:
            m.add(st, turn(o, 90), labels[st])
    return m


# ================================================================ Roman Athens

def roman_agora():
    m = Model("roman-agora")
    yW, yE = -43.0, 49.0           # west and east walls (the gate projects west of yW)
    xS, xN = -41.0, 41.0
    L, Wd = yE - yW, xN - xS
    cy = (yW + yE) / 2
    m.add(0, box("court", Wd, L, 0.3, (0, cy, 0), "#E4DCCB"), "court")
    m.add(0, J([box(f"pv{i}", Wd - 16.0, 0.12, 0.05, (0, y, 0.3), shade("#E4DCCB", -0.08)) for i, y in enumerate(lin(yW + 9, yE - 9, 12))], "paving"))
    walls = [box("wall_w", Wd, 1.2, 7.5, (0, yW + 0.6, 0), STONE), box("wall_e", Wd, 1.2, 7.5, (0, yE - 0.6, 0), STONE),
             box("wall_s", 1.2, L, 7.5, (xS + 0.6, cy, 0), STONE), box("wall_n", 1.2, L, 7.5, (xN - 0.6, cy, 0), STONE)]
    m.add(0, J(walls, "walls"))
    # shops along the south side opening into the colonnade
    m.add(0, J([box(f"shop{i}", 0.3, 1.8, 2.8, (xS + 7.4, y, 0.3), DARK) for i, y in enumerate(lin(yW + 10, yE - 10, 14))], "shop_doors"))
    m.add(0, box("shop_range", 6.2, L - 2.4, 6.0, (xS + 4.3, cy, 0), STONE))
    # Ionic colonnades round the court
    off = 8.0
    pts = [(x, yW + off) for x in lin(xS + off, xN - off, 16)] + [(x, yE - off) for x in lin(xS + off, xN - off, 16)]
    pts += [(xS + off, y) for y in lin(yW + off, yE - off, 21)[1:-1]] + [(xN - off, y) for y in lin(yW + off, yE - off, 21)[1:-1]]
    m.add(1, copies(ionic("col", 6.4, 0.32, MARB), [(x, y, 0.3) for x, y in pts], "colonnades"), "colonnades")
    roofs = [shed("roof_w", Wd, off + 0.6, 6.7, 8.2, (0, yW + off / 2, 0), TILE_T, "S"), shed("roof_e", Wd, off + 0.6, 6.7, 8.2, (0, yE - off / 2, 0), TILE_T, "N"),
             shed("roof_s", off + 0.6, L - 2 * off, 6.7, 8.2, (xS + off / 2, cy, 0), TILE_T, "W"), shed("roof_n", off + 0.6, L - 2 * off, 6.7, 8.2, (xN - off / 2, cy, 0), TILE_T, "E")]
    m.add(2, J(roofs, "stoa_roofs"), "roofs")
    # the Gate of Athena Archegetis
    gy = yW - 3.0
    gate = [crepis("g_steps", 12.0, 5.6, 3, 0.35, 0.4, MARB_W, 0.0, cy=gy)]
    gate.append(copies(doric("gcol", 8.0, 0.6, MARB), [(x, gy - 2.0, 1.05) for x in (-4.5, -1.5, 1.5, 4.5)], "gate_cols"))
    gate += [box(f"g_anta{s}", 1.0, 3.8, 8.0, (s * 5.4, gy + 0.9, 1.05), MARB) for s in (-1, 1)]
    gate.append(box("g_door", 3.0, 0.4, 6.0, (0, yW + 0.05, 0.3), DARK))
    gate.append(doric_entab("g_ent", 11.6, 5.4, 9.05, 0.9, 0.9, 0.4, 4, 3, MARB, relief="none", cy=gy))
    gate.append(greek_roof("g_roof", 12.4, 6.2, 11.25, 1.7, TILE_T, MARB, BLUE, figs=False, cy=gy, gables=(True, False)))
    gate.append(figure("lucius", 0, gy - 2.9, 12.95, 2.0, BRONZE))
    gate.append(box("oil_law", 1.2, 0.15, 2.2, (5.4, gy - 1.05, 2.0), shade(MARB, -0.12)))
    m.add(3, J(gate, "gate_archegetis"), "gates")
    east = [copies(ionic("ecol", 6.2, 0.34, MARB), [(x, yE + 0.6, 0.3) for x in (-4.5, -1.5, 1.5, 4.5)], "east_cols"),
            box("e_door", 3.0, 0.4, 5.0, (0, yE - 0.1, 0.3), DARK), box("e_ent", 11.0, 2.4, 1.0, (0, yE + 0.6, 6.5), MARB)]
    m.add(3, J(east, "east_propylon"))
    m.add(3, J([figure(f"statue{i}", x, cy + 6.0, 0.3, 2.4, MARB_S) for i, x in enumerate((-12, 12))], "statues"))
    m.add(3, box("fountain", 3.0, 3.0, 0.8, (0, cy, 0.3), WATER))
    return m


def tower_of_winds():
    m = Model("tower-of-winds")
    R = 4.18
    oct_pts = lambda r: [(r * math.cos(math.pi / 8 + k * math.pi / 4), r * math.sin(math.pi / 8 + k * math.pi / 4)) for k in range(8)]
    m.add(0, J([prism(f"step{k}", oct_pts(R + 0.75 - 0.25 * k), 0.3, (0, 0, 0.3 * k), shade(MARB_W, -0.04 + 0.02 * k)) for k in range(3)], "steps"), "tower")
    z = 0.9
    m.add(0, prism("body", oct_pts(R), 9.6, (0, 0, z), MARB))
    figs = []
    for k in range(8):
        a = k * math.pi / 4 + math.pi / 2
        rr = R * math.cos(math.pi / 8)
        figs.append(box(f"wind{k}", 2.3, 0.25, 1.2, (rr * math.cos(a) * 1.01, rr * math.sin(a) * 1.01, z + 8.0), MARB_S, rot_z=a + math.pi / 2))
        figs.append(box(f"dial{k}", 1.5, 0.12, 1.5, (rr * math.cos(a) * 1.005, rr * math.sin(a) * 1.005, z + 5.2), shade(MARB, -0.06), rot_z=a + math.pi / 2))
    m.add(0, J(figs, "winds"))
    m.add(0, prism("frieze_band", oct_pts(R + 0.12), 0.25, (0, 0, z + 7.75), shade(MARB, 0.03)))
    m.add(2, prism("cornice", oct_pts(R + 0.45), 0.45, (0, 0, z + 9.6), MARB), "roof")
    roof = mesh_from("roof", [(x, y, 0) for x, y in oct_pts(R + 0.35)] + [(0, 0, 2.6)], [(k, (k + 1) % 8, 8) for k in range(8)] + [tuple(range(8))[::-1]], (0, 0, z + 10.05), MARB_W)
    m.add(2, roof)
    zt = z + 12.65
    m.add(2, J([cylinder("cap", 0.45, 0.6, (0, 0, zt - 0.1), MARB, verts=8), cylinder("rod", 0.05, 1.0, (0, 0, zt + 0.5), BRONZE, verts=6),
                box("triton", 0.3, 1.1, 0.5, (0, 0, zt + 1.4), BRONZE), box("wand", 0.08, 1.6, 0.08, (0, 0.5, zt + 1.6), BRONZE)], "triton"))
    # the two porches (north-east and north-west) and the round cistern on the south
    for i, deg in enumerate((135, 225)):
        p = [crepis(f"pst{i}", 4.4, 2.4, 2, 0.25, 0.3, MARB_W, 0.0, cy=-R - 1.0)]
        p.append(copies(corinth(f"pc{i}", 4.6, 0.22, MARB, rich=False), [(x, -R - 1.9, 0.5) for x in (-1.6, 1.6)], f"pcols{i}"))
        p.append(box(f"pdoor{i}", 1.4, 0.3, 3.2, (0, -R * math.cos(math.pi / 8) - 0.1, z), DARK))
        p.append(box(f"pent{i}", 4.4, 2.6, 0.6, (0, -R - 1.0, 5.1), MARB))
        p.append(greek_roof(f"proof{i}", 4.6, 2.8, 5.7, 0.9, MARB_W, MARB, shade(MARB, -0.06), figs=False, tiles=False, cy=-R - 1.0, gables=(True, False)))
        m.add(1, turn(J(p, f"porch{i}"), deg), "porches")
    m.add(1, cylinder("cistern", 2.0, 6.5, (0, -R - 1.2, 0), MARB_W, verts=20))
    m.add(1, cylinder("cistern_roof", 2.15, 0.9, (0, -R - 1.2, 6.5), MARB_W, verts=20, r_top=0.6))
    return m


def hadrians_library(variant="intact"):
    ruin = variant == "ruin"
    m = Model("hadrians-library" if not ruin else "hadrians-library-ruin")
    xS, xN = -41.0, 41.0      # builder x: -X is north, +X south once turned to face west
    yW, yE = -55.0, 61.0
    cy = (yW + yE) / 2
    m.add(0, box("court", 82, 116, 0.3, (0, cy, 0), GRASS if not ruin else SAND), "court")
    WC = "#D9CBAF"
    hw = 12.0 if not ruin else 5.0
    walls = [box("wall_e", 82, 1.6, hw, (0, yE - 0.8, 0), WC), box("wall_n", 1.6, 116, hw, (xS + 0.8, cy, 0), WC), box("wall_s", 1.6, 116, hw if not ruin else 3.0, (xN - 0.8, cy, 0), WC)]
    walls += [box("wall_w_n", 33.5, 1.6, 12.0, (xS + 16.75, yW + 0.8, 0), WC), box("wall_w_s", 33.5, 1.6, 12.0 if not ruin else 4.0, (xN - 16.75, yW + 0.8, 0), WC)]
    m.add(0, J(walls, "walls"))
    # west facade: green Karystos columns standing before the wall, with the entablature breaking forward over them
    sides = (-1, 1) if not ruin else (-1,)
    for s in sides:
        xs7 = lin(s * 11.0, s * 37.5, 7)
        m.add(1, copies(corinth(f"fc{s}", 9.6, 0.5, MARB, rich=True, shaft_c=CIPOL), [(x, yW - 1.3, 0.3) for x in xs7], f"facade_cols{s}"), "facade")
        m.add(1, J([box(f"fped{s}{i}", 1.4, 1.4, 0.3, (x, yW - 1.3, 0.0), MARB_W) for i, x in enumerate(xs7)], f"fpeds{s}"))
        m.add(2, box(f"fent{s}", 28.0, 3.2, 1.6, (s * 24.25, yW - 0.6, 9.9), MARB), "entablature")
    m.add(0, box("steps", 82, 3.0, 0.3, (0, yW - 1.5, 0), MARB_W))
    if not ruin:
        prop = [crepis("p_steps", 14.0, 6.0, 3, 0.3, 0.35, MARB_W, 0.0, cy=yW - 3.0)]
        prop.append(copies(corinth("pc", 10.5, 0.55, MARB, rich=True), [(x, yW - 5.2, 0.9) for x in (-5.2, -1.75, 1.75, 5.2)], "propylon_cols"))
        prop.append(box("p_door", 4.0, 0.4, 7.5, (0, yW - 0.1, 0.3), DARK))
        prop.append(ionic_entab("p_ent", 13.4, 6.2, 11.4, 1.6, MARB, figs=False, dentils=True, cy=yW - 3.0))
        prop.append(greek_roof("p_roof", 14.2, 7.0, 13.0, 2.2, TILE_T, MARB, BLUE, figs=True, cy=yW - 3.0, gables=(True, False), tile_step=0.8))
        m.add(1, J(prop, "propylon"))
        # inner court: a peristyle of a hundred columns round a long pool
        off = 9.0
        pts = [(x, yW + off) for x in lin(xS + off, xN - off, 16)] + [(x, yE - 20.0) for x in lin(xS + off, xN - off, 16)]
        pts += [(s, y) for s in (xS + off, xN - off) for y in lin(yW + off, yE - 20.0, 22)[1:-1]]
        m.add(1, copies(plain_col("pc_in", 7.0, 0.32, "#D8CDBA"), [(x, y, 0.3) for x, y in pts], "peristyle"))
        roofs = [shed("pr_w", 82 - 3.2, off + 0.6, 7.0, 9.0, (0, yW + off / 2 + 0.8, 0), TILE_T, "S"),
                 shed("pr_n", off + 0.6, yE - 20.0 - yW - off, 7.0, 9.0, (xS + off / 2 + 0.8, (yW + off + yE - 20.0) / 2, 0), TILE_T, "W"),
                 shed("pr_s", off + 0.6, yE - 20.0 - yW - off, 7.0, 9.0, (xN - off / 2 - 0.8, (yW + off + yE - 20.0) / 2, 0), TILE_T, "E")]
        m.add(2, J(roofs, "peristyle_roofs"))
        m.add(1, box("pool", 14.0, 52.0, 0.5, (0, -2.0, 0.0), WATER))
        m.add(1, box("pool_rim", 15.0, 53.0, 0.4, (0, -2.0, 0.0), MARB_W))
        # the library range on the east: book hall in the middle, reading rooms and lecture halls to the sides
        ly0 = yE - 19.0
        m.add(1, box("east_range", 79.0, 18.0, 11.0, (0, ly0 + 9.0, 0), WC))
        m.add(1, box("book_hall", 22.0, 18.5, 16.5, (0, ly0 + 9.0, 0), shade(WC, 0.04)))
        m.add(1, J([box(f"niche{i}", 1.2, 0.3, 3.0, (x, ly0 - 0.1, 4.0 + 5.0 * t), DARK) for i, x in enumerate(lin(-8.5, 8.5, 6)) for t in (0, 1)], "book_niches"))
        m.add(1, copies(corinth("bc", 9.0, 0.45, MARB, rich=False), [(x, ly0 - 2.2, 0.3) for x in (-7.5, -2.5, 2.5, 7.5)], "hall_porch"))
        m.add(2, greek_roof("hall_roof", 23.6, 21.0, 16.5, 3.0, TILE_T, WC, BLUE, figs=False, cy=ly0 + 8.0, tile_step=0.9))
        m.add(2, J([gable_x(f"wing_roof{s}", 28.0, 18.6, 2.4, (s * 25.5, ly0 + 9.0, 11.0), TILE_T) for s in (-1, 1)], "wing_roofs"))
        m.add(2, J([tree(f"t{i}", 1.6, (x, y, 0.3), "#6F8A5C") for i, (x, y) in enumerate([(-16, -30), (16, -30), (-16, 20), (16, 20), (-16, -5), (16, -5)])], "garden_trees"))
    else:
        # Ottoman court: the church of the Megali Panagia, the voivode's house and shops
        ch = [box("church", 12.0, 22.0, 8.0, (0, 5.0, 0.3), STONE), half_cyl_y("ch_vault", 5.8, 22.4, (0, 5.0, 8.3), TILE_T, verts=16),
              cylinder("ch_apse", 3.2, 7.0, (0, 16.0, 0.3), STONE, verts=16), cylinder("drum", 2.6, 2.6, (0, 4.0, 11.5), STONE, verts=12),
              dome("dome", 2.7, (0, 4.0, 14.1), TILE_T, squash=0.7, segments=12, rings=5)]
        m.add(1, J(ch, "megali_panagia"), "court")
        m.add(1, box("voivode", 26.0, 12.0, 7.5, (22.0, 40.0, 0.3), PLAST))
        m.add(1, box("balcony", 18.0, 1.6, 0.4, (22.0, 33.4, 4.0), TIMBER))
        m.add(2, hip_roof("voivode_roof", 26.0, 12.0, 2.6, (22.0, 40.0, 7.8), TILE_T, ridge=0.5, overhang=0.6), "roofs")
        for i, y in enumerate(lin(-40, 40, 9)):
            m.add(1, box(f"shop{i}", 6.0, 7.5, 3.2, (xS + 4.6, y, 0.3), PLAST))
            m.add(2, shed(f"shop_r{i}", 6.6, 8.0, 3.5, 4.4, (xS + 4.6, y, 0), TILE_T, "W"))
        m.add(2, J([tree(f"t{i}", 2.4, (x, y, 0.3), "#6F8A5C") for i, (x, y) in enumerate([(14, -25), (-16, 28), (20, 10)])], "planes"))
    return m


def dipylon(variant="hell"):
    early = variant == "430"
    m = Model("dipylon" if not early else "dipylon-430")
    m.add(0, box("ground", 90, 60, 0.3, (0, 0, 0), EARTH), "ground")
    SOC, MB = "#B8A788", "#C49A6C"
    # the city wall along y = 0: stone socle, mud-brick upper wall; gaps for the gates
    runs = [(-45.0, -36.0), (-14.0, 15.0), (25.0, 45.0)]
    w = []
    for i, (a, b) in enumerate(runs):
        w += [box(f"socle{i}", b - a, 3.0, 3.2, ((a + b) / 2, 0, 0.3), SOC), box(f"brick{i}", b - a, 2.6, 4.6, ((a + b) / 2, 0, 3.5), MB),
              box(f"coping{i}", b - a, 3.0, 0.4, ((a + b) / 2, 0, 8.1), shade(SOC, 0.05))]
    m.add(1, J(w, "wall"), "walls")
    # the Dipylon: a long court open to the outside, towers at the four corners, the double gate at its inner end
    gx = -25.0
    court = [box("court_w", 3.0, 22.0, 8.0, (gx - 11.0, -11.0, 0.3), SOC), box("court_e", 3.0, 22.0, 8.0, (gx + 11.0, -11.0, 0.3), SOC),
             box("court_wb", 3.0, 22.0, 1.2, (gx - 11.0, -11.0, 8.3), MB), box("court_eb", 3.0, 22.0, 1.2, (gx + 11.0, -11.0, 8.3), MB)]
    for x, y in ((gx - 12.0, -22.0), (gx + 12.0, -22.0), (gx - 12.0, 1.0), (gx + 12.0, 1.0)):
        court.append(box(f"tower{x}{y}", 7.0, 7.0, 11.0, (x, y, 0.3), SOC))
        court.append(box(f"towerb{x}{y}", 7.0, 7.0, 2.0, (x, y, 11.3), MB))
    court += [box("gate_wall", 19.0, 3.0, 8.0, (gx, 0, 0.3), SOC), box("pier", 2.0, 3.2, 8.0, (gx, 0, 0.3), SOC)]
    court += [box(f"gate_open{s}", 5.0, 3.2, 5.5, (gx + s * 4.0, 0, 0.3), DARK) for s in (-1, 1)]
    court.append(box("court_pave", 19.0, 22.0, 0.15, (gx, -11.0, 0.3), shade(EARTH, 0.08)))
    m.add(1, J(court, "dipylon"))
    m.add(0, box("dromos", 14.0, 8.0, 0.1, (gx, -26.0, 0.3), shade(EARTH, 0.1)))
    # the Sacred Gate with the stone channel of the Eridanos beside the road
    sx = 20.0
    sg = [box("sg_tw", 6.0, 8.0, 10.0, (sx - 6.5, -1.5, 0.3), SOC), box("sg_te", 6.0, 8.0, 10.0, (sx + 6.5, -1.5, 0.3), SOC),
          box("sg_twb", 6.0, 8.0, 1.5, (sx - 6.5, -1.5, 10.3), MB), box("sg_teb", 6.0, 8.0, 1.5, (sx + 6.5, -1.5, 10.3), MB),
          box("road", 3.6, 60.0, 0.12, (sx - 1.8, 0, 0.3), shade(EARTH, 0.1)), box("channel_l", 0.8, 60.0, 1.2, (sx + 0.3, 0, 0.3), STONE),
          box("channel_r", 0.8, 60.0, 1.2, (sx + 3.5, 0, 0.3), STONE), box("eridanos", 2.4, 60.0, 0.5, (sx + 1.9, 0, 0.3), WATER)]
    m.add(1, J(sg, "sacred_gate"))
    # graves outside: stelai, naiskoi, marble vases, the bull of Dionysios of Kollytos, a mound
    rnd = random.Random(81)
    graves = []
    for i in range(12):
        x, y = rnd.uniform(-2, 40), rnd.uniform(-27, -8)
        if abs(x - sx) < 4.5:
            x += 9
        kind = i % 4
        if kind == 0:
            graves.append(box(f"stele{i}", 0.9, 0.25, 2.0, (x, y, 0.3), MARB))
        elif kind == 1:
            graves.append(J([box(f"nb{i}", 2.6, 1.4, 0.5, (x, y, 0.3), MARB_W), box(f"nl{i}", 0.3, 1.2, 2.0, (x - 1.1, y, 0.8), MARB), box(f"nr{i}", 0.3, 1.2, 2.0, (x + 1.1, y, 0.8), MARB),
                                box(f"nt{i}", 2.6, 1.4, 0.4, (x, y, 2.8), MARB), box(f"nf{i}", 1.4, 0.3, 1.4, (x, y + 0.3, 0.8), MARB_S)], f"naiskos{i}"))
        elif kind == 2:
            graves.append(lathe(f"lek{i}", [(0.25, 0), (0.4, 0.3), (0.42, 1.0), (0.15, 1.2), (0.1, 1.5), (0.18, 1.6), (0.0, 1.65)], (x, y, 0.3), MARB, verts=10))
        else:
            graves.append(J([box(f"pl{i}", 3.0, 2.0, 0.8, (x, y, 0.3), STONE)], f"plot{i}"))
    graves.append(J([box("bull_base", 1.6, 3.2, 2.6, (8.0, -20.0, 0.3), MARB_W), box("bull", 1.0, 2.4, 1.2, (8.0, -20.0, 2.9), MARB), box("bull_head", 0.8, 0.6, 0.6, (8.0, -21.4, 3.5), MARB)], "bull"))
    graves.append(dome("tumulus", 4.0, (38.0, -22.0, 0.3), shade(GRASS, -0.05), squash=0.45, segments=16, rings=6))
    m.add(2, J(graves, "graves"), "graves")
    if not early:
        # the Pompeion: a colonnaded court with dining rooms where the Panathenaic procession was marshalled
        px, py = -3.0, 16.0
        pw, pd = 28.0, 20.0
        pom = [box("pom_wall_n", pw, 1.0, 6.0, (px, py + pd / 2, 0.3), STUC), box("pom_wall_s", pw, 1.0, 6.0, (px, py - pd / 2, 0.3), STUC),
               box("pom_wall_w", 1.0, pd, 6.0, (px - pw / 2, py, 0.3), STUC), box("pom_wall_e", 1.0, pd, 6.0, (px + pw / 2, py, 0.3), STUC),
               box("pom_rooms", pw - 2.0, 6.0, 5.0, (px, py + pd / 2 - 3.5, 0.3), STUC)]
        pom.append(copies(plain_col("pomc", 4.6, 0.3, MARB_W), [(x, py - pd / 2 + 3.0, 0.3) for x in lin(px - 11, px + 11, 9)] + [(x, py + 2.5, 0.3) for x in lin(px - 11, px + 11, 9)], "pom_cols"))
        pom.append(shed("pom_roof_s", pw, 4.6, 4.9, 6.4, (px, py - pd / 2 + 2.6, 0), TILE_T, "S"))
        pom.append(shed("pom_roof_n", pw, 8.0, 5.2, 6.8, (px, py + pd / 2 - 4.2, 0), TILE_T, "N"))
        pom.append(small_temple("pom_propylon", 5.0, 4.0, 4.0, 2, "ionic", MARB, TILE_T, "antis"))
        m.add(3, J(pom[:-1], "pompeion"), "pompeion")
        m.add(3, turn(pom[-1], 180, px + pw / 2 + 3.2, py, 0.3))
    else:
        m.add(3, J([box(f"tent{i}", 3.0, 2.4, 1.6, (x, y, 0.3), "#D9C9A6") for i, (x, y) in enumerate([(-38, -18), (-4, -16), (30, -10), (-8, -24)])], "refugee_shelters"), "refugees")
    return m


# ================================================================ Ottoman Atina

def fethiye():
    m = Model("fethiye")
    m.add(0, box("terrace", 24, 26, 0.4, (0, 0, 0), SAND), "hall")
    hy = 3.0
    WH = "#E4D9C3"
    hall = [box("hall", 15.0, 15.0, 9.0, (0, hy, 0.4), WH)]
    for k in range(1, 4):
        hall.append(box(f"band{k}", 15.08, 15.08, 0.12, (0, hy, 0.4 + k * 2.3), "#B5714F"))
    for f, (dx, dy) in (("S", (0, -7.5)), ("N", (0, 7.5)), ("E", (7.5, 0)), ("W", (-7.5, 0))):
        for t, z in enumerate((2.2, 6.0)):
            for k in (-1, 0, 1) if t == 0 else (-1, 1):
                along = k * 4.0
                loc = (dx + (along if f in "SN" else 0), hy + dy + (along if f in "EW" else 0), 0.4 + z)
                hall.append(arch_panel(f"win{f}{t}{k}", 1.2, 2.0, loc, f, DARK, pointed=False, depth=0.25))
    m.add(0, J(hall, "prayer_hall"))
    m.add(1, prism("drum", [(6.6 * math.cos(math.pi / 8 + k * math.pi / 4), 6.6 * math.sin(math.pi / 8 + k * math.pi / 4)) for k in range(8)], 2.4, (0, hy, 9.4), WH), "dome")
    m.add(1, J([box(f"sq{s}{t}", 2.4, 2.4, 2.0, (s * 6.3, hy + t * 6.3, 9.4), WH, rot_z=math.pi / 4) for s in (-1, 1) for t in (-1, 1)], "corners"))
    m.add(1, shallow_dome("dome", 6.3, (0, hy, 11.8), LEAD, rise=0.72, finial=True))
    # portico of four reused ancient columns with three small domes
    py = hy - 7.5 - 2.8
    por = [box("por_floor", 15.0, 5.6, 0.5, (0, py, 0.4), MARB_W)]
    por.append(copies(J([cylinder("pc_s", 0.32, 4.4, (0, 0, 0), MARB_W, verts=12, r_top=0.28), box("pc_k", 0.8, 0.8, 0.5, (0, 0, 4.4), MARB)], "pcol"), [(x, py - 2.4, 0.9) for x in (-6.8, -2.3, 2.3, 6.8)], "por_cols"))
    por.append(box("por_beam", 15.0, 5.4, 0.9, (0, py, 5.8), WH))
    for i, x in enumerate((-4.6, 0.0, 4.6)):
        por.append(shallow_dome(f"pdome{i}", 2.1, (x, py, 6.7), LEAD, rise=0.65, finial=False))
    por.append(box("door", 2.0, 0.3, 3.6, (0, hy - 7.6, 0.4), DARK))
    m.add(2, J(por, "portico"), "portico")
    m.add(2, minaret("minaret", 1.15, 25.0, (9.4, hy - 6.2, 0.4), WH, MARB, balconies=1, cap="cone", sides=12, taper=0.85))
    m.add(2, box("fountain", 2.2, 2.2, 1.0, (-7.0, py - 6.5, 0.4), MARB_W))
    m.add(2, tree("plane", 2.6, (8.0, py - 7.0, 0.4), "#6F8A5C", TIMBER))
    return m


# ================================================================ registry

BUILDERS = {
    "athens/parthenon": lambda: parthenon("430"),
    "athens/parthenon-mosque": lambda: parthenon("mosque"),
    "athens/erechtheion": erechtheion,
    "athens/propylaia": lambda: propylaia("430"),
    "athens/propylaia-1680": lambda: propylaia("1680"),
    "athens/nike": nike,
    "athens/promachos": promachos,
    "athens/old-temple": lambda: old_temple("intact"),
    "athens/old-temple-ruin": lambda: old_temple("ruin"),
    "athens/theatre-dionysus": lambda: theatre_dionysus("hell"),
    "athens/theatre-dionysus-430": lambda: theatre_dionysus("430"),
    "athens/theatre-dionysus-roman": lambda: theatre_dionysus("roman"),
    "athens/odeon-pericles": odeon_pericles,
    "athens/odeon-herodes": odeon_herodes,
    "athens/stoa-poikile": stoa_poikile,
    "athens/stoa-attalos": stoa_attalos,
    "athens/hephaisteion": lambda: hephaisteion("temple"),
    "athens/hephaisteion-church": lambda: hephaisteion("church"),
    "athens/bouleuterion": lambda: bouleuterion("hell"),
    "athens/bouleuterion-430": lambda: bouleuterion("430"),
    "athens/building-f": lambda: bouleuterion("f"),
    "athens/altar-twelve": altar_twelve,
    "athens/pnyx": lambda: pnyx("iii"),
    "athens/pnyx-430": lambda: pnyx("430"),
    "athens/olympieion": lambda: olympieion("complete"),
    "athens/olympieion-platform": lambda: olympieion("platform"),
    "athens/olympieion-antiochus": lambda: olympieion("antiochus"),
    "athens/olympieion-ruin": lambda: olympieion("ruin"),
    "athens/hadrians-arch": hadrians_arch,
    "athens/lysicrates": lysicrates,
    "athens/stadium": lambda: stadium("roman"),
    "athens/stadium-lycurgan": lambda: stadium("lycurgan"),
    "athens/roman-agora": roman_agora,
    "athens/tower-of-winds": tower_of_winds,
    "athens/hadrians-library": lambda: hadrians_library("intact"),
    "athens/hadrians-library-ruin": lambda: hadrians_library("ruin"),
    "athens/dipylon": lambda: dipylon("hell"),
    "athens/dipylon-430": lambda: dipylon("430"),
    "athens/fethiye": fethiye,
}
