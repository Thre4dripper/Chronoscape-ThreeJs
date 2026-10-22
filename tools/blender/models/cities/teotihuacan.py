"""Teotihuacan landmark miniatures: talud-tablero pyramids and platforms, the Ciudadela and the Feathered Serpent
Pyramid, apartment compounds and barrios (100–650 CE), and the overgrown ruins the Aztecs knew (1500).
Builders face south (-Y); the landmark rotation turns them on the map (15.5 deg for the avenue's grid)."""
import math
import bpy
from chronokit import Model, box, cylinder, dome, join, shade, mesh_from
from worldkit import *

# ---------------------------------------------------------------- palette
STUCCO = "#EDE5D2"        # burnished lime plaster
STUCCO_D = "#DCCFB4"
TRED = "#A8452F"          # Teotihuacan red (hematite)
TRED_D = "#7E3424"
PAVE = "#D9CCB2"          # stucco floors
EARTH = "#B39A74"
ADOBE_C = "#B9926A"
STONE = "#8E857A"         # volcanic stone of the cores
GRASS = "#8E9768"
GRASS_D = "#76804F"
RUBBLE = "#9F927E"
CHAR = "#5A4A3E"
SOOT = "#352C26"
JADE = "#4E8A6E"
BLUE = "#4F7FA6"
OCHRE = "#C9A04A"
SHELL = "#F3EEE2"
ROOM = "#4A3B30"          # shadowed portico
LEAF = "#6F8A5C"
MAGUEY = "#7C9277"
WOOD = "#7A5A3C"
MAT = "#C8AE78"
CLOTH = "#EFE7D6"
WATER_C = "#62878A"


def rnd(i, k=0):
    """A repeatable pseudo-random number in [0, 1)."""
    v = math.sin(i * 12.9898 + k * 78.233) * 43758.5453
    return v - math.floor(v)


# ---------------------------------------------------------------- small helpers

def rz(o, deg):
    """Rotate about the world Z axis."""
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


def balustrade(name, x, wb, y0, y1, z0, z1, color, hb=0.9):
    """A Teotihuacan alfarda: a sloping ramp beside the steps, ending at the top in a small block."""
    parts = [side_prism(name, [(y0, z0), (y0, z0 + hb), (y1, z1 + hb), (y1, z0)], x - wb / 2, x + wb / 2, color),
             box(name + "_cap", wb + 0.2, 1.4, hb * 1.5, (x, y1 - 0.5, z1), shade(color, 0.04))]
    return join(parts, name)


def stairway(name, w, x, pts, color=STUCCO, bal=None, step=0.34, bw=None, noses=True):
    """A stair climbing through landings pts = [(y, z), ...] (y and z increasing), with balustrades on both sides."""
    bal = bal or shade(color, -0.07)
    bw = bw or max(0.9, w * 0.08)
    parts = []
    fixed = [pts[0]]
    for (yb, zb) in pts[1:]:
        ya, za = fixed[-1]
        if zb - za > 0.05 and (yb - ya) > (zb - za) * 1.6:
            fixed.append((yb - (zb - za) * 1.2, za))
        fixed.append((yb, zb))
    pts = fixed
    for i in range(len(pts) - 1):
        (ya, za), (yb, zb) = pts[i], pts[i + 1]
        if zb - za < 0.05:
            parts.append(box(f"{name}_land{i}", w, yb - ya, 0.2, (x, (ya + yb) / 2, za), color))
            continue
        n = max(3, int(round((zb - za) / step)))
        parts.append(flight(f"{name}_f{i}", w, x, ya, yb, za, zb, n, color))
        if noses:
            for k in range(0, n, 1 if n < 80 else 2):
                yy = ya + (yb - ya) * k / n
                zz = za + (zb - za) * (k + 1) / n
                parts.append(box(f"{name}_n{i}_{k}", w, 0.12, 0.06, (x, yy - 0.04, zz - 0.03), shade(color, -0.14)))
        for s in (-1, 1):
            parts.append(balustrade(f"{name}_b{i}{s}", x + s * (w / 2 + bw / 2), bw, ya, yb, za, zb, bal))
    return join(parts, name)


def edge_stair(name, w, H, edge, face, z, overlap=2.5, k=1.15, color=STUCCO):
    """A stair against the edge of a platform of height H: its foot points `face` (S/N/E/W), its top runs `overlap` m into it."""
    o = stairway(name, w, 0, [(overlap - H * k, 0), (overlap, H)], color)
    return place(o, {"S": 0, "N": 180, "E": 90, "W": -90}[face], edge[0], edge[1], z)


def tablero(name, w, d, h, loc, frame=STUCCO, panel=TRED):
    """The tablero: a vertical rectangular frame round a recessed panel, all four sides of a w x d block."""
    x, y, z = loc
    f = min(0.9, h * 0.22)
    r = min(0.45, f * 0.6)
    parts = [box(name + "_core", w - 2 * r, d - 2 * r, h - f, (x, y, z), panel),
             box(name + "_bot", w, d, f, (x, y, z), frame),
             box(name + "_top", w + 0.3, d + 0.3, f * 1.15, (x, y, z + h - f * 1.15), frame)]
    for sx in (-1, 1):
        for sy in (-1, 1):
            parts.append(box(f"{name}_post{sx}{sy}", f, f, h - 2 * f, (x + sx * (w / 2 - f / 2), y + sy * (d / 2 - f / 2), z + f), frame))
    return join(parts, name)


def tt_stack(name, widths, depths, heights, loc=(0, 0, 0), talud=0.4, terrace=1.2, color=STUCCO, panel=TRED, state="main", over=0.35, bands=1):
    """Stacked talud-tablero bodies. widths/depths: base of each body, then the summit (len = n + 1); heights: n bodies.
    Returns (object, tiers) with tiers = [dict(z0, z1, w, d, tw, td)] (tw/td: outer size of the body's tablero)."""
    x, y, z = loc
    parts, info = [], []
    zz = z
    n = len(heights)
    for i in range(n):
        W, D, H = widths[i], depths[i], heights[i]
        if i < n - 1:
            tw, td = widths[i + 1] + 2 * terrace, depths[i + 1] + 2 * terrace
        else:
            tw, td = widths[n], depths[n]
        hal, hab = H * talud, H * (1 - talud)
        if state == "ruin":
            c = GRASS if i % 2 == 0 else shade(GRASS, -0.06)
            parts.append(frustum(f"{name}_m{i}", W, D, tw * 0.95, td * 0.95, H * 0.93, (x, y, zz), c))
            parts.append(frustum(f"{name}_e{i}", W, D, W * 0.96, D * 0.96, H * 0.18, (x, y, zz), shade(EARTH, -0.05)))
            info.append(dict(z0=zz, z1=zz + H * 0.93, w=W, d=D, tw=tw * 0.95, td=td * 0.95))
            zz += H * 0.93
            continue
        col = color if state == "main" else shade(color, -0.12)
        pan = panel if state == "main" else shade(panel, -0.25)
        ax, ay = tw - 2 * over, td - 2 * over
        for b in range(bands):
            f0, f1 = b / bands, (b + 1) / bands
            parts.append(frustum(f"{name}_t{i}_{b}", W + (ax - W) * f0, D + (ay - D) * f0, W + (ax - W) * f1, D + (ay - D) * f1, hal / bands,
                                 (x, y, zz + hal * f0), shade(col, -0.03 - 0.025 * (b % 2))))
        if hab > 0.05:
            parts.append(tablero(f"{name}_tb{i}", tw, td, hab, (x, y, zz + hal), col, pan))
        info.append(dict(z0=zz, z1=zz + H, w=W, d=D, tw=tw, td=td))
        zz += H
    return join(parts, name), info


def platform(name, w, d, h, loc, tiers=2, color=STUCCO, panel=TRED, state="main", step=None, talud=0.4, terrace=None):
    """A rectangular talud-tablero platform of `tiers` bodies receding evenly."""
    step = step if step is not None else min(w, d) * 0.08
    widths = [w - 2 * step * i for i in range(tiers + 1)]
    depths = [d - 2 * step * i for i in range(tiers + 1)]
    widths[-1] = widths[-2] - 2 * step * 0.35
    depths[-1] = depths[-2] - 2 * step * 0.35
    hs = [h / tiers] * tiers
    return tt_stack(name, widths, depths, hs, loc, talud, terrace if terrace is not None else step * 0.65, color, panel, state)


def almenas(name, w, d, z, loc=(0, 0), size=0.9, color=STUCCO, inner=TRED):
    """Roof ornaments: upright plaques along the edges of a flat roof, each with a painted sign."""
    x, y = loc
    parts = []
    gap = size * 0.7
    for side, (length, fixed, horiz) in enumerate([(w, -d / 2, True), (w, d / 2, True), (d, -w / 2, False), (d, w / 2, False)]):
        k = max(2, int(length / (size + gap)))
        for i in range(k):
            t = -length / 2 + (i + 0.5) * length / k
            px, py = (t, fixed) if horiz else (fixed, t)
            bw, bd = (size, 0.25) if horiz else (0.25, size)
            parts.append(box(f"{name}{side}_{i}", bw, bd, size * 1.15, (x + px, y + py, z), color))
            parts.append(box(f"{name}{side}_{i}s", bw * 0.5 + (0.0 if horiz else 0.05), bd * 0.5 + (0.05 if horiz else 0.0), size * 0.45, (x + px, y + py, z + size * 0.4), inner))
    return join(parts, name)


def temple(name, w, d, h, loc, state="main", wall=STUCCO, band=TRED, face="S"):
    """A Teotihuacan temple: talud-tablero socle, a cella with a pillared doorway, a deep painted roof frieze and almenas.
    state 'burned': blackened stumps of walls and fallen debris; 'ruin': a low grassy hump."""
    x, y, z = loc
    if state == "ruin":
        return join([frustum(name + "_hump", w * 1.2, d * 1.2, w * 0.6, d * 0.5, h * 0.4, (x, y, z), GRASS_D)], name)
    parts = []
    sh = h * 0.3
    parts.append(frustum(name + "_tal", w + 1.6, d + 1.6, w + 0.9, d + 0.9, sh * 0.45, (x, y, z), shade(wall, -0.06)))
    parts.append(tablero(name + "_soc", w + 1.2, d + 1.2, sh * 0.55, (x, y, z + sh * 0.45), wall, band if state == "main" else SOOT))
    zc = z + sh
    if state == "burned":
        for i, (bx, by, bw, bd) in enumerate(((0, d / 2 - 0.4, w, 0.8), (-w / 2 + 0.4, 0, 0.8, d), (w / 2 - 0.4, 0, 0.8, d), (-w * 0.33, -d / 2 + 0.4, w * 0.34, 0.8), (w * 0.33, -d / 2 + 0.4, w * 0.34, 0.8))):
            parts.append(box(f"{name}_bw{i}", bw, bd, h * (0.35 + 0.25 * rnd(i, len(name))), (x + bx, y + by, zc), CHAR))
        parts.append(box(name + "_ash", w * 0.8, d * 0.75, 0.3, (x, y, zc), SOOT))
        for i in range(8):
            parts.append(box(f"{name}_deb{i}", 0.8 + rnd(i, 3), 0.6 + rnd(i, 4), 0.4, (x + (rnd(i, 1) - 0.5) * w, y - d / 2 - 1.0 - rnd(i, 2) * 2.5, zc - sh * 0.2 * rnd(i, 5)), CHAR if i % 2 else RUBBLE, rot_z=rnd(i, 6) * 3))
        o = join(parts, name)
        return rz(o, {"S": 0, "N": 180, "E": 90, "W": -90}[face]) if face != "S" else o
    parts.append(box(name + "_w", w, d, h, (x, y, zc), wall))
    parts.append(box(name + "_door", w * 0.5, 0.4, h * 0.74, (x, y - d / 2 - 0.05, zc), ROOM))
    for s in (-1, 1):
        parts.append(box(f"{name}_pil{s}", 0.7, 0.55, h * 0.74, (x + s * w * 0.09, y - d / 2 - 0.2, zc), wall))
    zr = zc + h
    parts.append(box(name + "_slab", w + 0.8, d + 0.8, 0.35, (x, y, zr), shade(wall, -0.05)))
    parts.append(tablero(name + "_frz", w + 0.6, d + 0.6, h * 0.42, (x, y, zr + 0.35), wall, band))
    parts.append(almenas(name + "_alm", w + 0.2, d + 0.2, zr + 0.35 + h * 0.42, (x, y), max(0.6, w * 0.07), wall, band))
    o = join(parts, name)
    if face != "S":
        o = rz(o, {"N": 180, "E": 90, "W": -90}[face])
    return o


def rubble(name, n, cx, cy, rx, ry, z, seed=0, colors=(RUBBLE, STONE, STUCCO_D), size=1.0):
    parts = []
    for i in range(n):
        s = size * (0.5 + rnd(i, seed) * 0.9)
        parts.append(box(f"{name}{i}", s * 1.3, s, s * 0.6, (cx + (rnd(i, seed + 1) - 0.5) * 2 * rx, cy + (rnd(i, seed + 2) - 0.5) * 2 * ry, z),
                         colors[i % len(colors)], rot_z=rnd(i, seed + 3) * 3.1))
    return join(parts, name)


def maguey(name, loc, s=1.0):
    x, y, z = loc
    p = [cylinder(name + "_c", 0.9 * s, 1.1 * s, (x, y, z), MAGUEY, verts=5, r_top=0.05)]
    for i in range(4):
        a = i * math.pi / 2 + 0.4
        p.append(box(f"{name}_l{i}", 1.5 * s, 0.25 * s, 0.18 * s, (x + math.cos(a) * 0.7 * s, y + math.sin(a) * 0.7 * s, z + 0.3 * s), shade(MAGUEY, 0.06), rot_z=a))
    return join(p, name)


def scrub(name, n, cx, cy, rx, ry, z, seed=0, trees=0.3):
    """Bushes, trees and maguey over a ruin."""
    parts = []
    for i in range(n):
        px, py = cx + (rnd(i, seed) - 0.5) * 2 * rx, cy + (rnd(i, seed + 7) - 0.5) * 2 * ry
        r = rnd(i, seed + 3)
        if r < trees:
            parts.append(tree(f"{name}t{i}", 2.0 + rnd(i, seed + 5) * 1.6, (px, py, z), LEAF if i % 2 else "#7E9460"))
        elif r < 0.65:
            parts.append(maguey(f"{name}m{i}", (px, py, z), 0.8 + rnd(i, seed + 4) * 0.5))
        else:
            parts.append(cylinder(f"{name}b{i}", 1.0 + rnd(i, seed + 4), 1.2, (px, py, z), GRASS_D, verts=6, r_top=0.4))
    return join(parts, name)


def maize_plot(name, w, d, loc, rows=6, per=12):
    x, y, z = loc
    p = [box(name + "_bed", w, d, 0.25, (x, y, z), "#7A6446")]
    for r in range(rows):
        for k in range(per):
            px = x - w / 2 + w * (k + 0.5) / per
            py = y - d / 2 + d * (r + 0.5) / rows
            p.append(cylinder(f"{name}_m{r}_{k}", 0.32, 1.7, (px, py, z + 0.25), "#7FA05A" if (r + k) % 3 else "#A9B65A", verts=4, r_top=0.05))
    return join(p, name)


def figure(name, loc, color="#E6DCC6", load=None):
    x, y, z = loc
    p = [cylinder(name + "_b", 0.26, 1.1, (x, y, z), color, verts=6),
         dome(name + "_h", 0.21, (x, y, z + 1.25), "#7A5236", segments=6, rings=3)]
    if load:
        p.append(box(name + "_l", 0.7, 0.55, 0.6, (x, y + 0.4, z + 0.75), load))
    return join(p, name)


# ---------------------------------------------------------------- apartment compounds

def compound(name, nx, ny, patios, loc=(0, 0, 0), c=3.6, wall_h=3.3, color=STUCCO, state="main", mural=TRED, temple_patios=(0,),
             mural_patios=None, alleys=(), door="S"):
    """A walled one-storey apartment compound on a grid of c-metre cells: flat-roofed rooms round open patios
    (cell rectangles (i0, j0, i1, j1), end-exclusive), porticoes on low talud-tablero steps, a temple platform and
    altar in the main patio. Returns one object."""
    x0, y0, z0 = loc
    W, D = nx * c, ny * c
    mural_patios = temple_patios if mural_patios is None else mural_patios
    holes = list(patios) + list(alleys)
    parts = [frustum(name + "_pl", W + 1.4, D + 1.4, W + 0.2, D + 0.2, 0.9, (x0, y0, z0), shade(color, -0.09))]
    zf = z0 + 0.9

    def blocked(i, j):
        return any(a <= i < c_ and b <= j < d_ for a, b, c_, d_ in holes)

    for j in range(ny):
        i = 0
        while i < nx:
            if blocked(i, j):
                i += 1
                continue
            k = i
            while k < nx and not blocked(k, j):
                k += 1
            hh = wall_h + (0.35 if ((j // 3) + (i // 4)) % 2 else 0.0)
            col = color
            if state == "burned":
                q = rnd(i * 31 + j, len(name))
                if q < 0.4:
                    hh, col = wall_h * (0.35 + q), CHAR
            parts.append(box(f"{name}_r{j}_{i}", (k - i) * c, c, hh, (x0 - W / 2 + (i + k) / 2 * c, y0 - D / 2 + (j + 0.5) * c, zf), col))
            i = k
    for ai, (i0, j0, i1, j1) in enumerate(alleys):
        parts.append(box(f"{name}_al{ai}", (i1 - i0) * c, (j1 - j0) * c, 0.12, (x0 - W / 2 + (i0 + i1) / 2 * c, y0 - D / 2 + (j0 + j1) / 2 * c, zf), shade(PAVE, -0.1)))
    for pi, (i0, j0, i1, j1) in enumerate(patios):
        px, py = x0 - W / 2 + (i0 + i1) / 2 * c, y0 - D / 2 + (j0 + j1) / 2 * c
        pw, pd = (i1 - i0) * c, (j1 - j0) * c
        parts.append(box(f"{name}_pf{pi}", pw, pd, 0.12, (px, py, zf), PAVE))
        painted = pi in mural_patios and state != "burned"
        rec = shade(mural, -0.32) if painted else ROOM
        for side, (length, ox, oy, horiz, inward) in enumerate([(pw, 0, pd / 2, True, -1), (pw, 0, -pd / 2, True, 1),
                                                              (pd, pw / 2, 0, False, -1), (pd, -pw / 2, 0, False, 1)]):
            if pi in temple_patios and side == 0 and state != "burned":
                continue
            L = length * 0.84
            ex, ey = px + ox, py + oy
            # the portico: a low talud step painted red, pillars, a shaded back wall with murals
            sx, sy = (L, 1.9) if horiz else (1.9, L)
            ix, iy = (0, inward * 0.95) if horiz else (inward * 0.95, 0)
            parts.append(box(f"{name}_ps{pi}{side}", sx, sy, 0.55, (ex + ix, ey + iy, zf), mural if painted else shade(color, -0.12)))
            bx, by = (L, 0.4) if horiz else (0.4, L)
            parts.append(box(f"{name}_pr{pi}{side}", bx, by, wall_h * 0.72, (ex + ix * 0.15, ey + iy * 0.15, zf + 0.55), rec))
            n = max(2, int(L / 3.0))
            for q in range(n):
                t = -L / 2 + L * (q + 0.5) / n
                qx, qy = (ex + t, ey + iy * 1.55) if horiz else (ex + ix * 1.55, ey + t)
                parts.append(box(f"{name}_pp{pi}{side}{q}", 0.7, 0.7, wall_h * 0.78 - 0.55, (qx, qy, zf + 0.55), color))
            lx, ly = (L, 2.0) if horiz else (2.0, L)
            parts.append(box(f"{name}_pl{pi}{side}", lx, ly, 0.45, (ex + ix, ey + iy, zf + wall_h * 0.78), shade(color, -0.04)))
        if pi in temple_patios:
            tw = pw * 0.42
            ty = py + pd / 2 - 2.6
            if state == "burned":
                parts.append(box(f"{name}_tp{pi}", tw, 4.6, 1.2, (px, ty, zf), CHAR))
            else:
                ob, _ = platform(f"{name}_tp{pi}", tw, 4.8, 2.0, (px, ty, zf), 1, color, mural, state, 0.4)
                parts.append(ob)
                parts.append(flight(f"{name}_ts{pi}", tw * 0.4, px, ty - 3.6, ty - 2.3, zf, zf + 2.0, 5, color))
                parts.append(temple(f"{name}_tt{pi}", tw * 0.55, 2.4, 1.8, (px, ty + 0.4, zf + 2.0), state, color, mural))
            ob, _ = platform(f"{name}_alt{pi}", 1.8, 1.8, 1.0, (px, py - 0.5, zf), 1, color, mural, state, 0.15)
            parts.append(ob)
    if state == "main":
        for pi, (i0, j0, i1, j1) in enumerate(patios):
            px, py = x0 - W / 2 + (i0 + i1) / 2 * c, y0 - D / 2 + (j0 + j1) / 2 * c
            pw, pd = (i1 - i0) * c, (j1 - j0) * c
            for sx in (-1, 1):
                for sy in (-1, 1):
                    parts.append(brazier(f"{name}_bz{pi}{sx}{sy}", (px + sx * (pw / 2 - 2.6), py + sy * (pd / 2 - 2.6), zf + 0.12), 0.45, False))
            for q in range(2):
                parts.append(figure(f"{name}_fg{pi}{q}", (px - 1.5 + q * 2.4, py - pd * 0.18, zf + 0.12), (CLOTH, TRED, OCHRE)[(pi + q) % 3], MAT if q else None))
            parts.append(maguey(f"{name}_mg{pi}", (px + pw * 0.22, py + pd * 0.12, zf + 0.12), 0.5))
    # parapet rim round the roofs and the street door
    for k, (bw, bd, bx, by) in enumerate(((W, 0.5, 0, -D / 2 + 0.25), (W, 0.5, 0, D / 2 - 0.25), (0.5, D, -W / 2 + 0.25, 0), (0.5, D, W / 2 - 0.25, 0))):
        parts.append(box(f"{name}_rim{k}", bw, bd, 0.35, (x0 + bx, y0 + by, zf + wall_h), shade(color, -0.06)))
    dx, dy = {"S": (0, -D / 2), "N": (0, D / 2), "E": (W / 2, 0), "W": (-W / 2, 0)}[door]
    parts.append(box(name + "_door", 2.0 if door in "SN" else 0.4, 0.4 if door in "SN" else 2.0, 2.4, (x0 + dx * 1.01, y0 + dy * 1.01, zf), DARK))
    return join(parts, name)


def banner(name, loc, h=4.5, color=TRED):
    x, y, z = loc
    return join([box(name + "_ft", 0.8, 0.8, 0.4, (x, y, z), STUCCO_D), cylinder(name + "_p", 0.1, h, (x, y, z + 0.4), WOOD, verts=4),
                 box(name + "_c", 0.1, 1.6, 1.3, (x, y + 0.8, z + h - 1.0), color)], name)


def brazier(name, loc, r=0.7, lit=True):
    x, y, z = loc
    p = [cylinder(name + "_f", r * 0.5, r * 0.7, (x, y, z), TRED_D, verts=8, r_top=r * 0.7),
         cylinder(name + "_b", r * 0.7, r * 0.9, (x, y, z + r * 0.7), STUCCO_D, verts=10, r_top=r)]
    if lit:
        p.append(cylinder(name + "_fl", r * 0.55, r * 0.9, (x, y, z + r * 1.6), "#E08A3A", verts=6, r_top=0.05))
    return join(p, name)


def dress(m, name, info, yc, stair_half, stage=2, state="main", per_side=3):
    """Braziers on the terrace corners and along the sides, banners at the corners of each body."""
    for i, t in enumerate(info):
        hw, hd, z = t["tw"] / 2 - 1.3, t["td"] / 2 - 1.3, t["z1"]
        for sx in (-1, 1):
            for sy in (-1, 1):
                if state == "main":
                    m.add(stage, banner(f"{name}_bn{i}{sx}{sy}", (sx * hw, yc + sy * hd, z), 3.5 + 0.2 * i, TRED if (i + sx) % 2 else OCHRE))
                else:
                    m.add(stage, box(f"{name}_sb{i}{sx}{sy}", 1.2, 1.2, 0.4, (sx * hw, yc + sy * hd, z), CHAR))
        for q in range(per_side):
            t_ = -0.5 + (q + 0.5) / per_side
            for (px, py) in ((t_ * 2 * hw, yc + hd), (-hw, yc + t_ * 2 * hd), (hw, yc + t_ * 2 * hd), (t_ * 2 * hw, yc - hd)):
                if abs(px) < stair_half + 2 and py < yc:
                    continue
                m.add(stage, brazier(f"{name}_bz{i}_{q}_{px:.0f}_{py:.0f}", (px, py, z), 0.6, state == "main"))


def procession(m, name, pts, n, stage=2, colors=(CLOTH, TRED, OCHRE, JADE)):
    """Figures climbing a stair in pairs along the landings pts."""
    segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    L = sum(abs(b[1] - a[1]) + abs(b[0] - a[0]) for a, b in segs)
    for k in range(n):
        d = L * (k + 0.5) / n
        for (ya, za), (yb, zb) in segs:
            seg = abs(yb - ya) + abs(zb - za)
            if d <= seg:
                t = d / seg if seg else 0
                for s in (-1, 1):
                    m.add(stage, figure(f"{name}{k}{s}", (s * 1.2, ya + (yb - ya) * t, za + (zb - za) * t + 0.15), colors[(k + s) % len(colors)]))
                break
            d -= seg


# ---------------------------------------------------------------- the Pyramid of the Sun

SUN_W = [225, 182, 145, 110, 78, 54]
SUN_H = [19.0, 16.0, 13.0, 10.0, 7.0]


def sun_steps(info, yc, adosada_top):
    """Landings of the Sun's stair: from the adosada top up through each body's tablero front edge."""
    pts = []
    ya, za = adosada_top
    pts.append((ya, za))
    for t in info:
        if t["z1"] <= za + 0.5:
            continue
        pts.append((yc - t["td"] / 2 + 0.6, t["z1"]))
    return pts


def pyramid_of_the_sun(state="main"):
    m = Model("pyramid-of-the-sun-" + state)
    yc = 25.0
    ground = {"main": PAVE, "burned": shade(PAVE, -0.08), "ruin": shade(GRASS, 0.05), "building": EARTH}[state]
    m.add(0, box("ground", 240, 290, 0.3, (0, 0, 0), ground), "ground")
    z0 = 0.3
    if state == "building":
        return sun_building(m, yc, z0)
    col = STUCCO
    # the enclosing platform round three sides, low and stuccoed
    if state != "ruin":
        for i, (bw, bd, bx, by) in enumerate(((5, 270, -117.5, 0), (5, 270, 117.5, 0), (240, 5, 0, 142.5))):
            m.add(0, frustum(f"encl{i}", bw, bd, bw * 0.6, bd - 1, 2.6, (bx, by, z0), shade(STUCCO_D, -0.05 if state == "main" else -0.15)))
    body, info = tt_stack("sun", SUN_W, SUN_W, SUN_H, (0, yc, z0), 0.74, 4.0, col, TRED, state, 0.35, 1 if state == "ruin" else 4)
    m.add(1, body, "pyramid")
    ztop = z0 + sum(SUN_H) * (0.93 if state == "ruin" else 1.0)
    yfront = yc - SUN_W[0] / 2
    # the adosada: a three-bodied platform against the west (front) face
    ad, adi = platform("adosada", 104, 36, 14.0, (0, yfront - 12, z0), 3, col, TRED, state, 3.2, 0.5)
    m.add(1, ad)
    ad_top_y = yfront - 12 - adi[-1]["td"] / 2
    ad_z = adi[-1]["z1"]
    if state == "ruin":
        # a worn path instead of the stair, scrub and stones, a little Aztec shrine on the summit
        m.add(1, side_prism("path", [(yfront - 32, z0), (yfront - 32, z0 + 0.4), (yc - SUN_W[-1] / 2, ztop + 0.3), (yc - SUN_W[-1] / 2, ztop - 1.0)], -1.6, 1.6, "#C9B48E"))
        for k, (sx, sy, rx, ry) in enumerate(((0, yc - 124, 108, 6), (0, yc + 112, 108, 2), (-113, yc, 2, 108), (113, yc, 2, 108))):
            m.add(2, scrub(f"scrub{k}", 18, sx, sy, rx, ry, z0, 3 + k, 0.3), "growth")
        for k, t in enumerate(info):
            hw = t["tw"] / 2
            for q in range(10):
                a = q / 10 * math.tau + k
                px, py = math.cos(a) * hw * 0.98, yc + math.sin(a) * hw * 0.98
                m.add(2, maguey(f"mg{k}_{q}", (max(-hw, min(hw, px)), max(yc - hw, min(yc + hw, py)), t["z1"] - 0.3), 0.9))
        m.add(2, rubble("stones", 60, 0, yfront - 20, 60, 12, z0, 11, size=1.4))
        m.add(2, box("shrine_b", 4, 3.5, 0.6, (0, yc, ztop), STONE))
        m.add(2, box("shrine_w", 3.2, 2.6, 2.0, (0, yc + 0.2, ztop + 0.6), ADOBE_C))
        m.add(2, cylinder("shrine_r", 2.8, 2.2, (0, yc + 0.2, ztop + 2.6), THATCH, verts=4, r_top=0.2))
        m.add(2, cylinder("censer", 0.45, 0.8, (0, yc - 3.0, ztop), TRED_D, verts=10, r_top=0.6))
        m.add(2, cylinder("smoke", 0.5, 3.0, (0, yc - 3.0, ztop + 0.8), "#D8D2C8", verts=6, r_top=0.15))
        return m
    # the adosada's stair from the plaza, then the main stair through the five bodies
    sw = 30.0
    m.add(2, stairway("ad_stair", sw, 0, [(ad_top_y - 16, z0), (ad_top_y + 0.6, ad_z)], col), "stairs")
    pts = [(ad_top_y + 0.6, ad_z), (yfront + 0.5, ad_z)] + sun_steps(info, yc, (yfront + 0.5, ad_z))[1:]
    m.add(2, stairway("stair", sw * 0.8, 0, pts, col, step=0.3))
    dress(m, "sun", info, yc, sw * 0.4 + 2, 2, state, 6)
    # the summit temple and braziers
    st = "burned" if state == "burned" else "main"
    m.add(2, temple("temple", 30, 20, 7.0, (0, yc + 4, ztop), st, STUCCO, TRED), "temple")
    for s in (-1, 1):
        m.add(2, cylinder(f"braz{s}", 0.8, 1.4, (s * 16, yc - 18, ztop), TRED_D, verts=10, r_top=1.1))
    if state == "main":
        procession(m, "pr", [(ad_top_y - 16, z0)] + pts, 40)
        for q in range(60):
            m.add(2, figure(f"crowd{q}", (-50 + rnd(q, 1) * 100, yfront - 50 + rnd(q, 2) * 14, z0), (CLOTH, TRED, OCHRE)[q % 3]))
        m.add(2, box("cave", 5, 0.8, 2.4, (0, ad_top_y - 16.4, z0), DARK))
    if state == "burned":
        m.add(2, rubble("debris", 70, 0, yfront - 30, 40, 10, z0, 5, (CHAR, RUBBLE, STUCCO_D, SOOT), 1.3))
        m.add(2, rubble("debris2", 30, 0, yc, 26, 20, ztop, 9, (CHAR, SOOT, RUBBLE), 1.0))
        for k in range(6):
            m.add(2, box(f"soot{k}", 4 + rnd(k, 2) * 5, 0.3, 6 + rnd(k, 3) * 6, (-30 + k * 12, yc - SUN_W[3] / 2 - 2 + k * 0.1, z0 + 34 + rnd(k, 4) * 8), SOOT))
    return m


def sun_building(m, yc, z0):
    """c. 100: the pyramid's core rising in cells of adobe, earth ramps, workers with baskets, a cave mouth at its foot."""
    hs = [19.0, 16.0, 7.0]
    ws = [225, 182, 150, 132]
    body, info = tt_stack("core", ws, ws, hs, (0, yc, z0), 1.0, 4.0, ADOBE_C, ADOBE_C, "main", 0.0)
    m.add(1, body, "core")
    ztop = z0 + sum(hs)
    # adobe cell walls on the working surface
    for i in range(-5, 6):
        m.add(1, box(f"cellx{i}", 0.9, 128, 1.2, (i * 12, yc, ztop), shade(ADOBE_C, -0.12)))
        m.add(1, box(f"celly{i}", 128, 0.9, 1.2, (0, yc + i * 12, ztop), shade(ADOBE_C, -0.12)))
    for i in range(30):
        m.add(1, box(f"fill{i}", 10, 10, 0.9 + rnd(i, 1) * 0.8, (-55 + (i % 6) * 22, yc - 50 + (i // 6) * 24, ztop), EARTH if i % 2 else STONE))
    # earth ramps up the sides
    yfront = yc - 112.5
    for s, (x0, x1) in ((-1, (-112, -86)), (1, (86, 112))):
        m.add(1, side_prism(f"ramp{s}", [(yfront - 52, z0), (yc - 80, z0 + 19), (yc - 76, z0 + 19), (yc - 76, z0)], s * 92 - 6, s * 92 + 6, EARTH), None)
    m.add(1, side_prism("ramp_c", [(yc - 91, z0 + 19), (yc - 78, z0 + 35), (yc - 73, z0 + 35), (yc - 73, z0 + 19)], -6, 6, EARTH))
    # workers carrying baskets, piles of stone and earth, the cave mouth
    k = 0
    for s in (-1, 1):
        for q in range(9):
            t = q / 9
            m.add(2, figure(f"w{k}", (s * 92 + (rnd(k, 2) - 0.5) * 6, yfront - 52 + t * 44, z0 + 19 * t), "#E6DCC6", MAT), "workers")
            k += 1
    for q in range(60):
        m.add(2, figure(f"wt{q}", (-60 + rnd(q, 4) * 120, yc - 60 + rnd(q, 5) * 120, ztop), "#D9CCB4", MAT if q % 2 else None))
    for q in range(30):
        m.add(2, figure(f"wg{q}", (-80 + rnd(q, 7) * 160, yfront - 48 + rnd(q, 8) * 24, z0), "#E6DCC6", MAT if q % 3 else None))
    for q in range(10):
        m.add(2, frustum(f"pile{q}", 9, 7, 3, 2, 3.5, (-100 + q * 22, yfront - 22 - rnd(q, 3) * 18, z0), EARTH if q % 2 else STONE))
    m.add(2, box("cave", 7, 1.2, 3.0, (0, yfront - 0.3, z0), DARK))
    for q in range(14):
        hx, hy = -108 + q * 16.6, yfront - 52 + (q % 2) * 4
        if abs(abs(hx) - 92) < 9:
            continue
        m.add(2, box(f"hut{q}", 6, 4.5, 2.4, (hx, hy, z0), "#CDB892"))
        m.add(2, cylinder(f"hutr{q}", 4.2, 2.4, (hx, hy, z0 + 2.4), THATCH, verts=4, r_top=0.2))
    return m


# ---------------------------------------------------------------- the Pyramid of the Moon

def pyramid_of_the_moon(state="main"):
    m = Model("pyramid-of-the-moon-" + state)
    ground = {"main": PAVE, "burned": shade(PAVE, -0.08), "ruin": shade(GRASS, 0.05), "early": EARTH}[state]
    m.add(0, box("ground", 150, 160, 0.3, (0, 0, 0), ground), "ground")
    z0 = 0.3
    col = STUCCO
    if state == "early":
        # Buildings 2–3: a small talud-tablero platform with a temple, a stuccoed court, houses of the early city
        m.add(0, box("court", 70, 64, 0.15, (0, 4, z0), PAVE))
        body, info = tt_stack("b3", [40, 33, 27, 22], [40, 33, 27, 22], [5.0, 4.5, 4.0], (0, 14, z0 + 0.15), 0.45, 1.2, col, TRED, "main")
        m.add(1, body, "platform")
        zt = info[-1]["z1"]
        m.add(1, stairway("st", 9, 0, [(-12, z0 + 0.15), (14 - 11 + 0.5, zt)], col))
        m.add(2, temple("temple", 12, 8, 3.6, (0, 16, zt), "main", STUCCO, TRED), "temple")
        alt, _ = platform("altar", 6, 6, 1.4, (0, -22, z0 + 0.15), 1, col, TRED, "main", 0.4)
        m.add(2, alt)
        for i, (hx, hy) in enumerate(((-55, -55), (-58, -20), (-56, 20), (-50, 55), (55, -50), (58, -15), (56, 25), (48, 60), (-20, -66), (22, -66), (0, 70))):
            m.add(2, box(f"h{i}", 8, 6, 2.6, (hx, hy, z0), "#CDB892"))
            r = cylinder(f"hr{i}", 5.4, 2.4, (hx, hy, z0 + 2.6), THATCH, verts=4, r_top=0.25)
            r.rotation_euler[2] = math.pi / 4
            m.add(2, r)
        m.add(2, scrub("tr", 14, 0, 0, 68, 72, z0, 21, 0.9))
        for q in range(24):
            m.add(2, figure(f"f{q}", (-30 + rnd(q, 1) * 60, -30 + rnd(q, 2) * 20, z0 + 0.15), (CLOTH, TRED, OCHRE)[q % 3], MAT if q % 4 == 0 else None))
        for q in range(8):
            m.add(2, brazier(f"bz{q}", (-30 + q * 8.5, -4, z0 + 0.15), 0.5))
        return m
    W = [147, 116, 88, 62, 42]
    Dd = [125, 98, 74, 52, 34]
    H = [13.0, 11.0, 10.0, 9.0]
    yc = 17.0
    body, info = tt_stack("moon", W, Dd, H, (0, yc, z0), 0.62, 3.0, col, TRED, state, 0.35, 1 if state == "ruin" else 3)
    m.add(1, body, "pyramid")
    ztop = z0 + (sum(H) * (0.93 if state == "ruin" else 1.0))
    # the adosada: five talud-tablero bodies against the south face
    aw = [96, 88, 80, 72, 64, 58]
    ad_d = [44, 40, 36, 32, 28, 25]
    ah = [4.2, 4.2, 4.2, 4.2, 4.2]
    ayc = yc - Dd[0] / 2 - 4
    ad, adi = tt_stack("adosada", aw, ad_d, ah, (0, ayc, z0), 0.4, 2.0, col, TRED, state)
    m.add(1, ad)
    ad_front = ayc - adi[-1]["td"] / 2
    ad_z = adi[-1]["z1"]
    if state == "ruin":
        m.add(1, side_prism("path", [(-76, z0), (-76, z0 + 0.4), (yc - W[-1] / 2 * 0.8, ztop + 0.3), (yc - W[-1] / 2 * 0.8, ztop - 1)], -1.4, 1.4, "#C9B48E"))
        m.add(2, scrub("scrub", 24, 0, -74, 66, 2, z0, 5, 0.3), "growth")
        for k, sx in enumerate((-69, 69)):
            m.add(2, scrub(f"scrubs{k}", 10, sx, 0, 2, 70, z0, 9 + k, 0.3))
        for k, t in enumerate(info):
            for q in range(8):
                a = q / 8 * math.tau + k * 0.7
                m.add(2, maguey(f"mg{k}_{q}", (math.cos(a) * t["tw"] * 0.47, yc + math.sin(a) * t["td"] * 0.47, t["z1"] - 0.3), 0.8))
        m.add(2, rubble("stones", 40, 0, ad_front - 6, 40, 5, z0, 4, size=1.2))
        return m
    sw = 16.0
    m.add(2, stairway("ad_stair", sw, 0, [(-79, z0), (ad_front + 0.5, ad_z)], col), "stairs")
    pts = [(ad_front + 0.5, ad_z)]
    for t in info:
        if t["z1"] > ad_z + 0.5:
            pts.append((yc - t["td"] / 2 + 0.5, t["z1"]))
    m.add(2, stairway("stair", sw * 0.75, 0, pts, col, step=0.3))
    dress(m, "moon", info, yc, sw * 0.4 + 1, 2, state, 5)
    dress(m, "ados", adi, ayc, sw * 0.5 + 1, 2, state, 2)
    if state == "main":
        procession(m, "pr", [(-79, z0), (ad_front + 0.5, ad_z)] + pts[1:], 30)
        for q in range(36):
            m.add(2, figure(f"crowd{q}", (-60 + rnd(q, 1) * 120, -78 + rnd(q, 2) * 4, z0), (CLOTH, TRED, OCHRE)[q % 3]))
    st = "burned" if state == "burned" else "main"
    m.add(2, temple("temple", 20, 13, 5.5, (0, yc + 4, ztop), st, STUCCO, TRED), "temple")
    m.add(2, temple("ad_temple", 14, 7, 3.4, (0, ayc + 2, ad_z), st, STUCCO, TRED))
    for s in (-1, 1):
        m.add(2, cylinder(f"braz{s}", 0.7, 1.2, (s * 13, yc - 10, ztop), TRED_D, verts=10, r_top=1.0))
        m.add(2, cylinder(f"abraz{s}", 0.6, 1.0, (s * 22, ad_front + 3, ad_z), TRED_D, verts=10, r_top=0.9))
    if state == "burned":
        m.add(2, rubble("debris", 50, 0, -74, 45, 4, z0, 6, (CHAR, RUBBLE, STUCCO_D, SOOT), 1.2))
        m.add(2, rubble("debris2", 20, 0, yc, 16, 12, ztop, 8, (CHAR, SOOT, RUBBLE), 0.9))
    return m


# ---------------------------------------------------------------- the Plaza of the Moon

def platform_temple(m, name, w, d, h, loc, face, state, tiers=3, stage=1, temple_h=None):
    """A temple-platform of the plaza type: talud-tablero bodies, a stair on its `face`, a temple on top facing the same way."""
    x, y, z = loc
    deg = {"S": 0, "N": 180, "E": 90, "W": -90}[face]
    # build facing south at the origin, then turn and place
    pw, pd = (w, d) if face in "SN" else (d, w)
    body, info = platform(name, pw, pd, h, (0, 0, 0), tiers, STUCCO, TRED, state, min(pw, pd) * 0.07)
    parts = [body]
    zt = info[-1]["z1"]
    if state != "ruin":
        parts.append(stairway(name + "_st", pw * 0.32, 0, [(-pd / 2 - h * 0.85, 0), (-info[-1]["td"] / 2 + 0.4, zt)], STUCCO))
        th = temple_h or max(2.6, h * 0.45)
        parts.append(temple(name + "_tm", info[-1]["tw"] * 0.6, info[-1]["td"] * 0.5, th, (0, info[-1]["td"] * 0.08, zt), state, STUCCO, TRED))
    else:
        parts.append(scrub(name + "_sc", 5, 0, 0, pw * 0.35, pd * 0.35, zt - 0.3, len(name), 0.4))
    o = join(parts, name)
    m.add(stage, place(o, deg, x, y, z))


def moon_plaza(state="main"):
    m = Model("moon-plaza-" + state)
    ground = {"main": PAVE, "burned": shade(PAVE, -0.1), "ruin": shade(GRASS, 0.07)}[state]
    m.add(0, box("ground", 210, 170, 0.3, (0, 0, 0), ground), "plaza")
    z0 = 0.3
    if state != "ruin":
        m.add(0, box("floor", 140, 150, 0.12, (0, 5, z0), shade(PAVE, 0.04)))
    # the central altar platform and the compartmented structure beside it
    alt, ai = platform("altar", 20, 20, 4.0, (0, 0, z0), 2, STUCCO, TRED, state, 1.2)
    m.add(1, alt, "platforms")
    if state != "ruin":
        for f, (dx, dy, face) in enumerate(((0, -10, "S"), (0, 10, "N"), (-10, 0, "W"), (10, 0, "E"))):
            o = stairway(f"alt_st{f}", 5, 0, [(-13.0, 0), (-7.0, 4.0)], STUCCO)
            m.add(1, place(o, {"S": 0, "N": 180, "E": 90, "W": -90}[face], 0, 0, z0))
        cs, _ = platform("comp", 16, 16, 2.0, (0, -32, z0), 1, STUCCO, TRED, state, 0.6)
        m.add(1, cs)
        for k in (-1, 0, 1):
            m.add(1, box(f"compx{k}", 13, 0.8, 1.6, (0, -32 + k * 4.5, z0 + 2.0), STUCCO_D))
            m.add(1, box(f"compy{k}", 0.8, 13, 1.6, (k * 4.5, -32, z0 + 2.0), STUCCO_D))
    # temple platforms round the plaza: four on each side facing in, two flanking the avenue's mouth
    for s, face in ((-1, "E"), (1, "W")):
        for i, py in enumerate((-58, -18, 22, 60)):
            platform_temple(m, f"pt{s}{i}", 28, 30, 9.0 if i in (1, 2) else 7.5, (s * 88, py, z0), face, state, 3, 1)
    for s in (-1, 1):
        platform_temple(m, f"ps{s}", 22, 18, 6.0, (s * 46, -72, z0), "N", state, 2, 2)
    for s in (-1, 1):
        platform_temple(m, f"pn{s}", 24, 20, 7.0, (s * 52, 70, z0), "S", state, 2, 2)
    if state == "burned":
        m.add(2, rubble("debris", 80, 0, 0, 70, 70, z0, 3, (CHAR, RUBBLE, STUCCO_D, SOOT), 1.0), "debris")
    if state == "ruin":
        m.add(2, scrub("scrub", 50, 0, 0, 95, 80, z0, 12, 0.3), "growth")
        m.add(2, rubble("stones", 40, 0, 0, 80, 70, z0, 13, size=0.9))
    else:
        for i in range(10):
            m.add(2, cylinder(f"braz{i}", 0.6, 1.1, (-54 + i * 12, 28, z0), TRED_D, verts=8, r_top=0.85), "braziers")
    return m


# ---------------------------------------------------------------- the Palace of Quetzalpapalotl

def bird_pillar(name, loc, h, state="main"):
    """A square pillar carved on its faces with a frontal or profile bird, eyes once inlaid with obsidian."""
    x, y, z = loc
    col = STUCCO_D if state == "main" else CHAR
    p = [box(name + "_b", 0.6 * 2.6, 0.6 * 2.6, 0.5, (x, y, z), shade(col, -0.05)),
         box(name + "_s", 1.5, 1.5, h - 0.5, (x, y, z + 0.5), col)]
    if state == "main":
        for f, (dx, dy, bw, bd) in enumerate(((0, -0.78, 1.0, 0.12), (0, 0.78, 1.0, 0.12), (-0.78, 0, 0.12, 1.0), (0.78, 0, 0.12, 1.0))):
            p.append(box(f"{name}_r{f}", bw, bd, h * 0.55, (x + dx, y + dy, z + h * 0.2), "#C9BBA0"))
            ex, ey = (x + dx * 1.08 + (0.2 if dy else 0), y + dy * 1.08 + (0.2 if dx else 0))
            p.append(box(f"{name}_e{f}", 0.16, 0.16, 0.16, (ex, ey, z + h * 0.6), DARK))
    return join(p, name)


def palace_of_quetzalpapalotl(state="main"):
    m = Model("palace-of-quetzalpapalotl-" + state)
    m.add(0, box("ground", 60, 70, 0.3, (0, 0, 0), PAVE), "ground")
    z0 = 0.3
    col = STUCCO
    base, bi = platform("base", 56, 64, 1.6, (0, 0, z0), 1, col, TRED, state, 0.6)
    m.add(0, base)
    zf = bi[-1]["z1"]
    PW, PD = 26.0, 26.0
    py = -4.0
    wall_h = 4.8
    m.add(0, box("patio", PW, PD, 0.12, (0, py, zf), shade(PAVE, -0.04)))
    # rooms round the patio (three sides) and the entrance portico to the north
    rooms = [(-27, -31, -13, 31), (13, -31, 27, 31), (-13, -31, 13, -17), (-13, 9, 13, 31)]
    for i, (a, b, c_, d_) in enumerate(rooms):
        w, d = c_ - a, d_ - b
        cx, cy = (a + c_) / 2, (b + d_) / 2
        hh = wall_h
        if state == "burned":
            m.add(1, box(f"room{i}", w, d, hh * 0.55, (cx, cy, zf), CHAR), "rooms")
            m.add(1, rubble(f"rb{i}", 10, cx, cy, w * 0.4, d * 0.4, zf + hh * 0.55, i, (CHAR, SOOT, RUBBLE), 0.9))
        else:
            m.add(1, box(f"room{i}", w, d, hh, (cx, cy, zf), col), "rooms")
            m.add(2, tablero(f"frz{i}", w + 0.4, d + 0.4, 1.3, (cx, cy, zf + hh), col, TRED), "roof")
            pass
    if state == "main":
        m.add(2, almenas("alm_out", 54.4, 62.4, zf + wall_h + 1.3, (0, 0), 0.9, col, TRED))
    # the dark porticoes behind the pillars, red dado
    for side, (L, ox, oy, horiz) in enumerate(((PW, 0, PD / 2, True), (PW, 0, -PD / 2, True), (PD, -PW / 2, 0, False), (PD, PW / 2, 0, False))):
        ex, ey = ox, py + oy
        bx, by = (L * 0.9, 0.4) if horiz else (0.4, L * 0.9)
        m.add(1, box(f"por{side}", bx, by, wall_h * 0.8, (ex, ey, zf), ROOM if state == "main" else SOOT))
        dx, dy = (L * 0.9, 0.5) if horiz else (0.5, L * 0.9)
        m.add(1, box(f"dado{side}", dx, dy, 0.8, (ex + (0 if horiz else (0.25 if ox < 0 else -0.25)), ey + ((0.25 if oy < 0 else -0.25) if horiz else 0), zf), TRED if state == "main" else CHAR))
    # the carved pillars, four to a side, and the portico roof over them
    n = 4
    for side in range(4):
        for q in range(n):
            t = -PW / 2 + 3 + (PW - 6) * q / (n - 1)
            if side == 0:
                px, pyy = t, py + PD / 2 - 3.2
            elif side == 1:
                px, pyy = t, py - PD / 2 + 3.2
            elif side == 2:
                px, pyy = -PW / 2 + 3.2, py + t
            else:
                px, pyy = PW / 2 - 3.2, py + t
            if side >= 2 and q in (0, n - 1):
                continue
            m.add(1, bird_pillar(f"pil{side}{q}", (px, pyy, zf), wall_h * 0.85, state))
    if state == "main":
        for side, (bw, bd, bx, by) in enumerate(((PW, 4.0, 0, py + PD / 2 - 2), (PW, 4.0, 0, py - PD / 2 + 2), (4.0, PD - 8, -PW / 2 + 2, py), (4.0, PD - 8, PW / 2 - 2, py))):
            m.add(2, box(f"proof{side}", bw, bd, 0.5, (bx, by, zf + wall_h * 0.85), shade(col, -0.04)))
            m.add(2, box(f"pfrz{side}", bw, bd, 0.9, (bx, by, zf + wall_h * 0.85 + 0.5), TRED))
    # the stair up from the plaza on the north side
    m.add(1, place(stairway("nstair", 14, 0, [(-34.6, z0), (-31.6, zf)], col), 180))
    if state == "burned":
        m.add(2, rubble("debris", 140, 0, py, 11, 11, zf, 2, (CHAR, SOOT, RUBBLE, STUCCO_D), 0.9), "debris")
        m.add(2, rubble("almenas_fallen", 100, 0, 0, 29, 33, z0, 6, (STUCCO_D, TRED_D, RUBBLE), 0.7))
        for k in range(16):
            m.add(2, box(f"beam{k}", 5 + rnd(k, 1) * 3, 0.4, 0.4, (-20 + rnd(k, 2) * 40, -26 + rnd(k, 3) * 52, zf + 2.6), SOOT, rot_z=rnd(k, 4) * 3))
    return m


# ---------------------------------------------------------------- the Plaza of the Columns

def plaza_of_the_columns(state="main"):
    m = Model("plaza-of-the-columns-" + state)
    ground = PAVE if state == "main" else shade(PAVE, -0.1)
    m.add(0, box("ground", 220, 170, 0.3, (0, 0, 0), ground), "plaza")
    z0 = 0.3
    # the main pyramid at the back (west), facing the plaza and the avenue (east = -Y)
    platform_temple(m, "main", 64, 44, 16.0, (0, 56, z0), "S", state, 4, 1, 5.0)
    # long platforms on the north and south sides, each with two temples
    for s in (-1, 1):
        body, info = platform(f"side{s}", 34, 104, 7.0, (s * 80, -6, z0), 2, STUCCO, TRED, state, 1.6)
        m.add(1, body)
        zt = info[-1]["z1"]
        for q, py in enumerate((-30, 18)):
            m.add(1, edge_stair(f"sst{s}{q}", 8, zt - z0, (s * 63, py), "E" if s < 0 else "W", z0, 2.4))
            o = temple(f"stm{s}{q}", 14, 9, 4.0, (0, 0, 0), state, STUCCO, TRED)
            m.add(2, place(o, 90 if s < 0 else -90, s * 82, py, zt))
    # residences behind the side platforms and the main pyramid
    for s in (-1, 1):
        m.add(2, compound(f"res{s}", 9, 8, [(2, 2, 6, 6)], (s * 82, 66, z0), 3.4, 3.2, STUCCO, "burned" if state == "burned" else "main", TRED, (0,), (0,)))
    # a low wall closing the plaza toward the avenue, with a central stair
    for s in (-1, 1):
        m.add(1, frustum(f"fw{s}", 70, 4, 68, 2.6, 2.4, (s * 46, -78, z0), STUCCO_D))
    m.add(1, stairway("fst", 18, 0, [(-84, z0), (-80, z0 + 2.4), (-76, z0 + 2.4), (-72, z0)], STUCCO))
    if state == "burned":
        m.add(2, rubble("debris", 60, 0, 0, 90, 60, z0, 7, (CHAR, RUBBLE, STUCCO_D, SOOT), 1.1), "debris")
    else:
        for q in range(6):
            m.add(2, cylinder(f"braz{q}", 0.6, 1.0, (-25 + q * 10, 20, z0), TRED_D, verts=8, r_top=0.8))
    return m


# ---------------------------------------------------------------- the avenue: sunken plazas

def avenue_of_the_dead(state="main"):
    m = Model("avenue-of-the-dead-" + state)
    ruin = state == "ruin"
    m.add(0, box("ground", 130, 440, 0.3, (0, 0, 0), GRASS if ruin else shade(PAVE, -0.05)), "avenue")
    z0 = 0.3
    walls = [-150.0, -50.0, 50.0, 150.0]
    rise = 1.4
    bounds = [-220.0] + walls + [220.0]
    for k in range(5):
        y0, y1 = bounds[k], bounds[k + 1]
        zf = z0 + rise * k
        m.add(0, box(f"floor{k}", 40, y1 - y0, zf - z0 + 0.15, (0, (y0 + y1) / 2, z0), "#C9B48E" if ruin else PAVE))
    for k, wy in enumerate(walls):
        zs, zn = z0 + rise * k, z0 + rise * (k + 1)
        h = 3.6 + rise
        if ruin:
            m.add(1, frustum(f"cw{k}", 44, 12, 40, 5, h * 0.7, (0, wy, z0), GRASS_D), "walls")
            continue
        body, info = tt_stack(f"cw{k}", [44, 40], [10, 7], [h], (0, wy, z0), 0.45, 0.0, STUCCO, TRED, state)
        m.add(1, body, "walls")
        top = z0 + h
        m.add(1, stairway(f"cws{k}", 16, 0, [(wy - 5 - (top - zs) * 0.9, zs), (wy - 3.0, top)], STUCCO))
        o = stairway(f"cwn{k}", 16, 0, [(-5 - (top - zn) * 0.9, 0), (-3.0, top - zn)], STUCCO)
        m.add(1, place(o, 180, 0, wy, zn))
    # platforms along both sides, stairs to the avenue, small temples (three-temple groups)
    for s in (-1, 1):
        for i, py in enumerate((-190, -110, -20, 75, 170)):
            d = 56 if i % 2 == 0 else 46
            h = 7.5 if i % 2 == 0 else 6.0
            face = "E" if s < 0 else "W"
            platform_temple(m, f"pl{s}{i}", 40, d, h, (s * 44, py, z0), face, state, 3, 1 if i % 2 == 0 else 2)
    if state == "burned":
        m.add(2, rubble("debris", 120, 0, 0, 22, 200, z0 + 1, 4, (CHAR, RUBBLE, STUCCO_D, SOOT), 1.1), "debris")
        for k in range(6):
            m.add(2, box(f"sculp{k}", 1.4, 2.6, 1.0, (-12 + rnd(k, 3) * 24, -180 + k * 70, z0 + 1.4 * (k * 70 // 100)), "#8E8676", rot_z=k))
    elif ruin:
        m.add(2, box("path", 3.0, 440, 0.12, (0, 0, z0 + 0.15), "#CDB994"), "growth")
        m.add(2, scrub("scrub", 70, 0, 0, 54, 205, z0, 17, 0.3))
        for k in range(8):
            m.add(2, maize_plot(f"mz{k}", 9, 14, (-58 + 116 * (k % 2), -200 + k * 55, z0), 4, 5))
    else:
        for k in range(12):
            m.add(2, figure(f"pr{k}", (-8 + (k % 4) * 5, -200 + k * 34, z0 + 1.4 * min(4, int((-200 + k * 34 + 220) // 100))), CLOTH if k % 3 else TRED), "people")
    return m


# ---------------------------------------------------------------- the San Juan crossing

def san_juan_crossing():
    m = Model("san-juan-crossing")
    # the channel between two raised banks
    m.add(0, box("bankn", 120, 37, 1.6, (0, 26.5, 0), shade(PAVE, -0.06)), "banks")
    m.add(0, box("banks", 120, 37, 1.6, (0, -26.5, 0), shade(PAVE, -0.06)))
    m.add(0, box("water", 120, 16, 0.6, (0, 0, 0), WATER_C))
    for s in (-1, 1):
        m.add(1, box(f"lining{s}", 120, 1.0, 2.0, (0, s * 8.5, 0), STONE), "channel")
        for q in range(20):
            m.add(1, box(f"blk{s}{q}", 5.6, 1.1, 0.5, (-57 + q * 6, s * 8.5, 0.6 + (q % 2) * 0.6), shade(STONE, 0.08 * (q % 2))))
    # the avenue's paving to the edge and a crossing of stone slabs on piers
    for s in (-1, 1):
        m.add(1, box(f"pave{s}", 40, 36, 0.2, (0, s * 27, 1.6), PAVE))
        m.add(1, box(f"edge{s}", 40, 1.2, 0.5, (0, s * 9.6, 1.6), STONE))
    for q in range(-4, 5):
        m.add(1, box(f"pier{q}", 1.6, 16, 1.4, (q * 4.6, 0, 0), STONE))
    m.add(2, box("slabs", 40, 18.5, 0.5, (0, 0, 1.6), "#A79C8C"), "crossing")
    for q in range(-8, 9):
        m.add(2, box(f"jt{q}", 0.12, 18.5, 0.04, (q * 2.4, 0, 2.1), shade(STONE, -0.2)))
    # platforms on the banks, facing the avenue
    for sx in (-1, 1):
        for sy in (-1, 1):
            platform_temple(m, f"bp{sx}{sy}", 30, 26, 5.5, (sx * 44, sy * 30, 1.6), "E" if sx < 0 else "W", "main", 2, 2)
    # willows and reeds on the water's edge, a few people
    for q in range(10):
        m.add(2, cylinder(f"reed{q}", 0.8, 1.4, (-55 + q * 12 + (q % 3), (-1) ** q * 6.5, 0.6), "#8E9A5C", verts=5, r_top=0.1))
    for q in range(4):
        m.add(2, tree(f"wil{q}", 2.6, ((-56, -30, 30, 56)[q], 13 * (-1) ** q, 1.6), "#7E9460"))
    for q in range(6):
        m.add(2, figure(f"f{q}", (-10 + q * 4, -2 + (q % 2) * 4, 2.1), CLOTH, MAT if q % 2 else None))
    return m


# ---------------------------------------------------------------- the Feathered Serpent Pyramid

FS_W = [65.0, 59.6, 54.2, 48.8, 43.4, 38.0, 34.0]
FS_H = [3.35] * 6


def fs_head(name, loc, deg, s=1.0):
    """The feathered serpent's head, tenoned into the tablero: head, open jaws, fangs, eyes, and its collar of feathers."""
    x, y, z = loc
    p = [box(name + "_h", 1.3 * s, 1.6 * s, 1.0 * s, (0, -0.8 * s, 0), STUCCO_D),
         box(name + "_sn", 1.1 * s, 0.7 * s, 0.45 * s, (0, -1.9 * s, 0.5 * s), STUCCO_D),
         box(name + "_jaw", 1.0 * s, 0.6 * s, 0.3 * s, (0, -1.8 * s, 0.0), shade(STUCCO_D, -0.15)),
         box(name + "_ey", 1.36 * s, 0.25 * s, 0.25 * s, (0, -1.3 * s, 0.7 * s), DARK),
         box(name + "_fg", 0.8 * s, 0.15 * s, 0.3 * s, (0, -2.2 * s, 0.1 * s), SHELL)]
    c = cylinder(name + "_col", 1.25 * s, 0.35 * s, (0, -0.15 * s, 0.5 * s), JADE, verts=10)
    c.rotation_euler[0] = math.pi / 2
    bpy.ops.object.select_all(action="DESELECT")
    c.select_set(True)
    bpy.context.view_layer.objects.active = c
    bpy.ops.object.transform_apply(rotation=True)
    p.append(c)
    o = join(p, name)
    return place(o, deg, x, y, z)


def fs_headdress(name, loc, deg, s=1.0):
    """The headdress head (Cipactli or war serpent): a block with two goggle rings and a top knot."""
    x, y, z = loc
    p = [box(name + "_b", 1.5 * s, 1.0 * s, 1.3 * s, (0, -0.5 * s, 0), STUCCO_D),
         box(name + "_k", 0.9 * s, 0.6 * s, 0.4 * s, (0, -0.5 * s, 1.3 * s), OCHRE),
         box(name + "_m", 1.1 * s, 0.2 * s, 0.25 * s, (0, -1.05 * s, 0.2 * s), SHELL)]
    for k in (-1, 1):
        c = cylinder(f"{name}_r{k}", 0.3 * s, 0.2 * s, (k * 0.38 * s, -1.0 * s, 0.85 * s), BLUE, verts=8)
        c.rotation_euler[0] = math.pi / 2
        bpy.ops.object.select_all(action="DESELECT")
        c.select_set(True)
        bpy.context.view_layer.objects.active = c
        bpy.ops.object.transform_apply(rotation=True)
        p.append(c)
    o = join(p, name)
    return place(o, deg, x, y, z)


def serpent_relief(name, L, loc, deg, h, color=JADE):
    """An undulating serpent body carved along a tablero or talud face, with shells beside it."""
    x, y, z = loc
    parts = []
    n = max(4, int(L / 2.2))
    for k in range(n):
        t = (k + 0.5) / n
        px = -L / 2 + L * t
        pz = h * (0.5 + 0.28 * math.sin(t * L * 0.45))
        parts.append(box(f"{name}{k}", L / n * 1.05, 0.25, h * 0.22, (px, -0.1, pz - h * 0.11), color if k % 2 else shade(color, 0.12)))
        if k % 3 == 1:
            parts.append(box(f"{name}s{k}", 0.5, 0.2, 0.4, (px, -0.12, h * 0.1), SHELL))
    o = join(parts, name)
    return place(o, deg, x, y, z)


def temple_of_the_feathered_serpent(state="main"):
    m = Model("temple-of-the-feathered-serpent-" + state)
    ruin = state == "ruin"
    m.add(0, box("ground", 80, 100, 0.3, (0, 0, 0), shade(GRASS, 0.05) if ruin else PAVE), "ground")
    z0 = 0.3
    yc = 15.0
    adosada = state in ("adosada", "burned", "ruin")
    pst = "ruin" if ruin else ("burned" if state == "burned" else "main")
    body, info = tt_stack("fs", FS_W, FS_W, FS_H, (0, yc, z0), 0.32, 0.6, STUCCO_D, "#B65A3E", "main" if state in ("main", "adosada") else pst)
    m.add(1, body, "pyramid")
    ztop = info[-1]["z1"]
    if not ruin:
        # heads on every tablero, in pairs (serpent, headdress), and serpent bodies in relief between them
        cnt = 0
        for i, t in enumerate(info):
            tw = t["tw"]
            hab = FS_H[i] * 0.68
            zt = t["z1"] - hab * 0.62
            for f, (deg, axis) in enumerate(((0, "S"), (180, "N"), (90, "E"), (-90, "W"))):
                if adosada and axis == "S" and zt < z0 + 14:
                    continue
                n = max(2, int(tw / 5.6))
                for q in range(n):
                    tt = -tw / 2 + tw * (q + 0.5) / n
                    if axis == "S" and abs(tt) < 9:
                        continue
                    if axis == "S":
                        px, py = tt, yc - tw / 2
                    elif axis == "N":
                        px, py = -tt, yc + tw / 2
                    elif axis == "E":
                        px, py = tw / 2, yc + tt
                    else:
                        px, py = -tw / 2, yc - tt
                    s = 0.62 if i < 5 else 0.5
                    if q % 2 == 0:
                        m.add(1, fs_head(f"hd{i}{f}{q}", (px, py, zt), deg, s))
                    else:
                        m.add(1, fs_headdress(f"hh{i}{f}{q}", (px, py, zt - 0.1), deg, s))
                    cnt += 1
                # serpent bodies along the tablero face
                if not (adosada and axis == "S" and zt < z0 + 14):
                    off = tw / 2 + 0.1
                    loc = {"S": (0, yc - off, t["z1"] - hab), "N": (0, yc + off, t["z1"] - hab), "E": (off, yc, t["z1"] - hab), "W": (-off, yc, t["z1"] - hab)}[axis]
                    rdeg = {"S": 0, "N": 180, "E": 90, "W": -90}[axis]
                    if axis == "S":
                        for sgn in (-1, 1):
                            Lh = tw / 2 - 9
                            o = serpent_relief(f"sr{i}{f}{sgn}", Lh, (sgn * (9 + Lh / 2), yc - off, t["z1"] - hab), 0, hab, JADE)
                            m.add(1, o)
                    else:
                        m.add(1, serpent_relief(f"sr{i}{f}", tw * 0.94, loc, rdeg, hab, JADE))
    if state == "main":
        # the front stair with serpent heads on its balustrades, and the temple on top
        yf = yc - FS_W[0] / 2
        pts = [(yf - 12.0, z0), (yc - FS_W[-1] / 2 + 0.5, ztop)]
        m.add(2, stairway("stair", 13, 0, pts, STUCCO, STUCCO_D, 0.3, 1.6), "stair")
        for i, t in enumerate(info):
            fy = pts[0][0] + (pts[1][0] - pts[0][0]) * (t["z0"] - z0) / (ztop - z0)
            for sgn in (-1, 1):
                m.add(2, fs_head(f"bh{i}{sgn}", (sgn * 7.3, fy - 0.6, t["z0"] + 0.9), 0, 0.55))
        m.add(2, temple("temple", 20, 14, 5.0, (0, yc + 2, ztop), "main", STUCCO, TRED), "temple")
        return m
    if ruin:
        m.add(1, frustum("ad_mound", 72, 34, 50, 20, 11.0, (0, yc - FS_W[0] / 2 - 12, z0), GRASS_D))
        m.add(2, scrub("scrub", 70, 0, 0, 36, 45, z0, 8, 0.25), "growth")
        m.add(2, rubble("stones", 60, 0, -35, 30, 8, z0, 9, size=1.0))
        m.add(2, rubble("stones2", 40, 0, 15, 34, 34, z0, 19, size=0.8))
        for k, (hx, hy, dg) in enumerate(((-20, -40, 20), (14, -44, -60), (30, 40, 150))):
            m.add(2, fs_head(f"fallen{k}", (hx, hy, z0), dg, 0.6))
        # one or two heads showing through the turf at the back
        m.add(2, fs_head("hd_out", (-12, yc + FS_W[1] / 2 + 0.5, z0 + 5.5), 180, 0.6))
        return m
    # the adosada of c. 350: four plain talud-tablero bodies against the front, a stair and a temple
    ad_w, ad_d = [72, 66, 60, 54, 50], [36, 32, 28, 24, 21]
    ayc = yc - FS_W[0] / 2 - 8
    ad, adi = tt_stack("adosada", ad_w, ad_d, [3.3] * 4, (0, ayc, z0), 0.36, 2.0, STUCCO if state == "adosada" else shade(STUCCO, -0.12), TRED if state == "adosada" else shade(TRED, -0.25))
    m.add(1, ad)
    az = adi[-1]["z1"]
    afront = ayc - adi[-1]["td"] / 2
    m.add(2, stairway("ad_stair", 14, 0, [(-49.0, z0), (afront + 0.5, az)], STUCCO), "stair")
    st = "main" if state == "adosada" else "burned"
    m.add(2, temple("ad_temple", 18, 9, 4.2, (0, ayc + 2, az), st, STUCCO, TRED), "temple")
    # the pyramid's own summit temple was destroyed: only its low base remains
    m.add(2, box("old_base", 22, 16, 0.6, (0, yc + 2, ztop), shade(STUCCO_D, -0.1)))
    m.add(2, rubble("old_debris", 14, 0, yc + 2, 9, 6, ztop + 0.6, 3, (STONE, STUCCO_D, RUBBLE), 0.8))
    if state == "burned":
        m.add(2, rubble("debris", 30, 0, -46, 30, 3, z0, 4, (CHAR, RUBBLE, SOOT), 1.0))
    return m


# ---------------------------------------------------------------- the Ciudadela

def ciudadela(state="main"):
    m = Model("ciudadela-" + state)
    ruin = state == "ruin"
    m.add(0, box("ground", 400, 400, 0.3, (0, 0, 0), shade(GRASS, 0.06) if ruin else PAVE), "ground")
    z0 = 0.3
    H = 7.0
    pst = "ruin" if ruin else state
    # the four enclosing platforms: front (west, -Y) and back (east), north and south sides (here -X / +X)
    plats = [("front", 400, 70, 0, -165), ("back", 400, 70, 0, 165), ("side_a", 80, 260, -160, 0), ("side_b", 80, 260, 160, 0)]
    for nm, w, d, x, y in plats:
        body, info = platform(nm, w, d, H, (x, y, z0), 2, STUCCO, TRED, pst, 2.0)
        m.add(0, body, "platforms")
    zt = z0 + H * (0.93 if ruin else 1.0)
    # the great stair from the avenue up the front platform
    if not ruin:
        m.add(1, stairway("front_st", 70, 0, [(-199.8, z0), (-191.5, zt)], STUCCO), "stairs")
        # inner stairs down into the plaza, one in front of each pyramid
    # fifteen pyramids: four on the front and each side, three on the back
    pyr = [(-120, -165, "S"), (-40, -165, "S"), (40, -165, "S"), (120, -165, "S"),
           (-160, -90, "W"), (-160, -30, "W"), (-160, 30, "W"), (-160, 90, "W"),
           (160, -90, "E"), (160, -30, "E"), (160, 30, "E"), (160, 90, "E"),
           (-110, 165, "N"), (0, 165, "N"), (110, 165, "N")]
    inward = {"S": "N", "N": "S", "W": "E", "E": "W"}
    for i, (px, py, side) in enumerate(pyr):
        platform_temple(m, f"py{i}", 30, 30, 11.0, (px, py, zt), inward[side], pst, 3, 1)
        if not ruin:
            # a stair from the platform top down to the plaza in front of the pyramid
            edge = {"S": (px, -130), "N": (px, 130), "W": (-120, py), "E": (120, py)}[side]
            m.add(1, edge_stair(f"inst{i}", 18, zt - z0, edge, inward[side], z0, 3.0))
    # the plaza: altar platform; residential compounds flanking the Feathered Serpent Pyramid (left empty at x=0, y=25..125)
    alt, _ = platform("altar", 16, 16, 3.0, (0, -40, z0), 2, STUCCO, TRED, pst, 1.0)
    m.add(1, alt)
    if ruin:
        for s in (-1, 1):
            m.add(1, frustum(f"cmp{s}", 60, 92, 48, 80, 2.4, (s * 74, 72, z0), GRASS_D))
        m.add(2, scrub("scrub", 90, 0, 0, 180, 180, z0, 14, 0.3), "growth")
        for k in range(10):
            if k == 7:
                continue
            m.add(2, maize_plot(f"mz{k}", 24, 18, (-90 + (k % 5) * 45, -100 + (k // 5) * 60, z0), 4, 8))
        return m
    for s in (-1, 1):
        m.add(2, compound(f"cmp{s}", 17, 26, [(2, 3, 8, 11), (10, 3, 15, 11), (2, 15, 8, 23), (10, 15, 15, 23)], (s * 74, 72, z0),
                          3.6, 3.6, STUCCO, "burned" if state == "burned" else "main", TRED, (0,), (0, 1)), "compounds")
    if state == "burned":
        m.add(2, rubble("debris", 90, 0, -60, 110, 60, z0, 8, (CHAR, RUBBLE, STUCCO_D, SOOT), 1.2))
    else:
        for k in range(16):
            m.add(2, figure(f"f{k}", (-60 + (k % 8) * 16, -80 + (k // 8) * 20, z0), CLOTH if k % 3 else TRED), "people")
    return m


# ---------------------------------------------------------------- the Great Compound

def stall(name, loc, goods, awning=True):
    x, y, z = loc
    p = [box(name + "_m", 2.8, 2.2, 0.1, (x, y, z), MAT), box(name + "_g", 2.0, 1.2, 0.45, (x, y - 0.1, z + 0.1), goods)]
    if awning:
        p += [box(name + "_p", 0.15, 0.15, 2.4, (x, y + 0.95, z), WOOD), box(name + "_a", 3.0, 2.5, 0.12, (x, y + 0.1, z + 2.35), CLOTH)]
    return join(p, name)


def great_compound():
    m = Model("great-compound")
    m.add(0, box("ground", 380, 370, 0.3, (0, 0, 0), PAVE), "plaza")
    z0 = 0.3
    # two great wings (north and south of the plaza, here at -X / +X), with buildings on top
    for s in (-1, 1):
        body, info = platform(f"wing{s}", 110, 330, 6.5, (s * 133, 10, z0), 2, STUCCO, TRED, "main", 2.4)
        m.add(0, body, "platforms")
        zt = info[-1]["z1"]
        m.add(1, compound(f"bld{s}", 26, 78, [(5, 6, 12, 16), (14, 6, 21, 16), (5, 30, 21, 46), (5, 60, 12, 70), (14, 60, 21, 70)], (s * 133, 10, zt),
                          3.6, 3.4, STUCCO, "main", TRED, (2,), (2,)), "buildings")
        for q, py in enumerate((-110, -30, 50, 130)):
            m.add(1, edge_stair(f"wst{s}{q}", 14, zt - z0, (s * 78, py), "E" if s < 0 else "W", z0, 2.6))
    # the back (west, +Y) platform closing the plaza
    body, info = platform("back", 156, 34, 5.0, (0, 166, z0), 2, STUCCO, TRED, "main", 1.6)
    m.add(0, body)
    m.add(1, stairway("bst", 30, 0, [(149 - 5.5, z0), (149 + 0.4, info[-1]["z1"])], STUCCO))
    platform_temple(m, "btm", 26, 18, 5.0, (0, 168, info[-1]["z1"]), "S", "main", 2, 2)
    # the plaza: rows of market mats and awnings, porters
    goods = [OCHRE, "#5B4B3E", JADE, "#C9763E", SHELL, "#7FA05A", TRED, "#2E241C"]
    k = 0
    for row in range(9):
        for col in range(9):
            x = -56 + col * 14
            y = -140 + row * 30
            if abs(x) < 10 and -40 < y < 0:
                continue
            m.add(2, stall(f"st{k}", (x + (row % 2) * 4, y, z0), goods[(row * 3 + col) % len(goods)], (row + col) % 3 != 0), "market")
            k += 1
    for q in range(24):
        m.add(2, figure(f"p{q}", (-60 + rnd(q, 1) * 120, -150 + rnd(q, 2) * 260, z0), CLOTH if q % 3 else "#C9763E", MAT if q % 2 else None))
    alt, _ = platform("altar", 12, 12, 2.5, (0, -20, z0), 2, STUCCO, TRED, "main", 0.8)
    m.add(2, alt)
    return m


# ---------------------------------------------------------------- Xalla

def xalla(state="main"):
    m = Model("xalla-" + state)
    m.add(0, box("ground", 130, 120, 0.3, (0, 0, 0), PAVE if state == "main" else shade(PAVE, -0.1)), "ground")
    z0 = 0.3
    burned = state == "burned"
    # enclosing wall
    for k, (bw, bd, bx, by) in enumerate(((128, 2, 0, -59), (128, 2, 0, 59), (2, 120, -64, 0), (2, 120, 64, 0))):
        m.add(0, frustum(f"wall{k}", bw, bd, bw - 0.6 if bw > 2 else 1.2, bd - 0.6 if bd > 2 else 1.2, 3.6, (bx, by, z0), STUCCO_D if not burned else shade(STUCCO_D, -0.15)), "wall")
    m.add(0, box("gate", 6, 2.4, 2.8, (0, -58.8, z0), DARK))
    # four great buildings on platforms round the plaza, facing in
    blds = [(0, 38, 64, 22, "S"), (0, -36, 56, 20, "N"), (-42, 0, 22, 50, "E"), (42, 0, 22, 50, "W")]
    for i, (bx, by, bw, bd, face) in enumerate(blds):
        body, info = platform(f"pl{i}", bw, bd, 3.6, (bx, by, z0), 2, STUCCO, TRED, state, 1.0)
        m.add(1, body, "platforms")
        zt = info[-1]["z1"]
        tw, td = info[-1]["tw"], info[-1]["td"]
        hall_w, hall_d = (tw - 3, td * 0.55) if face in "SN" else (tw * 0.55, td - 3)
        sx, sy = {"S": (0, 1), "N": (0, -1), "E": (-1, 0), "W": (1, 0)}[face]
        hx, hy = bx + sx * (tw - hall_w) / 2 * 0.9, by + sy * (td - hall_d) / 2 * 0.9
        if burned:
            m.add(2, box(f"hall{i}", hall_w, hall_d, 1.8, (hx, hy, zt), CHAR), "halls")
            m.add(2, rubble(f"rb{i}", 14, hx, hy, hall_w * 0.4, hall_d * 0.4, zt + 1.8, i, (CHAR, SOOT, RUBBLE), 0.8))
        else:
            m.add(2, box(f"hall{i}", hall_w, hall_d, 4.6, (hx, hy, zt), STUCCO), "halls")
            m.add(2, tablero(f"hfrz{i}", hall_w + 0.4, hall_d + 0.4, 1.4, (hx, hy, zt + 4.6), STUCCO, TRED))
            m.add(2, almenas(f"halm{i}", hall_w, hall_d, zt + 6.0, (hx, hy), 0.9, STUCCO, TRED))
            # portico toward the plaza: dark recess and pillars
            L = hall_w if face in "SN" else hall_d
            fx, fy = hx - sx * hall_w / 2, hy - sy * hall_d / 2
            pb = (L * 0.8, 0.4) if face in "SN" else (0.4, L * 0.8)
            m.add(2, box(f"por{i}", pb[0], pb[1], 3.4, (fx - sx * 0.1, fy - sy * 0.1, zt), ROOM))
            n = max(3, int(L / 4))
            for q in range(n):
                t = -L * 0.4 + L * 0.8 * q / (n - 1)
                qx, qy = (fx + t, fy - sy * 0.8) if face in "SN" else (fx - sx * 0.8, fy + t)
                m.add(2, box(f"pil{i}{q}", 0.9, 0.9, 4.6, (qx, qy, zt), STUCCO))
        edge = {"S": (bx, by - bd / 2), "N": (bx, by + bd / 2), "E": (bx + bw / 2, by), "W": (bx - bw / 2, by)}[face]
        m.add(1, edge_stair(f"st{i}", 12, 3.6, edge, face, z0, 1.6))
    # the central temple
    platform_temple(m, "ctemple", 15, 15, 6.0, (0, 0, z0), "S", "burned" if burned else "main", 3, 2)
    if burned:
        m.add(2, rubble("debris", 40, 0, 0, 30, 25, z0, 5, (CHAR, RUBBLE, "#8E8676", SOOT), 1.0))
    else:
        for q in range(8):
            m.add(2, figure(f"f{q}", (-20 + q * 6, -14 + (q % 2) * 3, z0), CLOTH if q % 2 else TRED))
    return m


# ---------------------------------------------------------------- the mural compounds

def tetitla():
    m = Model("tetitla")
    m.add(0, box("ground", 64, 64, 0.3, (0, 0, 0), shade(PAVE, -0.04)), "ground")
    m.add(1, compound("c", 17, 17, [(6, 6, 11, 11), (1, 1, 5, 5), (12, 1, 16, 5), (1, 12, 5, 16), (12, 12, 16, 16)], (0, 0, 0.3), 3.6, 3.3, STUCCO,
                      "main", TRED, (0,), (0, 1, 2, 3, 4), [(5, 8, 6, 9), (11, 8, 12, 9)]), "compound")
    for q in range(4):
        m.add(2, figure(f"f{q}", (-3 + q * 2, -1.5, 1.2), CLOTH if q % 2 else TRED), "people")
    return m


def atetelco():
    m = Model("atetelco")
    m.add(0, box("ground", 64, 64, 0.3, (0, 0, 0), shade(PAVE, -0.04)), "ground")
    # the White Patio has temple platforms on three sides: model it with the compound and two extra platforms
    m.add(1, compound("c", 17, 17, [(4, 8, 11, 15), (12, 2, 16, 7), (2, 1, 7, 5), (12, 10, 16, 15)], (0, 0, 0.3), 3.6, 3.3, STUCCO,
                      "main", TRED, (0,), (0, 1, 3)), "compound")
    zf = 1.2
    px, py = -30.6 + 7.5 * 3.6, -30.6 + 11.5 * 3.6
    for s, face in ((-1, "E"), (1, "W")):
        o, _ = platform(f"wp{s}", 4.6, 9.0, 2.0, (px + s * 8.6, py, zf), 1, STUCCO, TRED, "main", 0.4)
        m.add(2, o, "temples")
        m.add(2, temple(f"wt{s}", 2.4, 5.0, 1.8, (px + s * 9.0, py, zf + 2.0), "main", STUCCO, TRED))
    return m


def tepantitla():
    m = Model("tepantitla")
    m.add(0, box("ground", 60, 60, 0.3, (0, 0, 0), shade(PAVE, -0.04)), "ground")
    m.add(1, compound("c", 16, 16, [(5, 5, 11, 11), (1, 1, 4, 4), (12, 12, 15, 15), (1, 12, 4, 15), (12, 1, 15, 4)], (0, 0, 0.3), 3.6, 3.3, STUCCO,
                      "main", TRED, (), (0, 1)), "compound")
    # the Tlalocan portico: a strip of blue-green water and figures under the red frame
    zf = 1.2
    px, py, pw = 0.0, 0.0, 6 * 3.6
    m.add(2, box("mural_w", pw * 0.8, 0.3, 0.9, (px, py + pw / 2 - 1.2, zf + 0.6), "#4C8A8A"), "murals")
    for q in range(24):
        m.add(2, box(f"mfig{q}", 0.35, 0.32, 0.5, (px - pw * 0.36 + (q % 12) * pw * 0.065, py + pw / 2 - 1.25, zf + 1.6 + (q // 12) * 0.7), OCHRE if q % 2 else SHELL))
    m.add(2, box("mountain", 1.6, 0.3, 1.6, (px, py + pw / 2 - 1.3, zf + 0.7), OCHRE))
    for q in range(10):
        m.add(2, figure(f"f{q}", (-7 + q * 1.6, -3 + (q % 2) * 2.5, zf), CLOTH if q % 2 else OCHRE), "people")
    return m


# ---------------------------------------------------------------- the barrios

def oaxaca_barrio():
    m = Model("oaxaca-barrio")
    m.add(0, box("ground", 120, 120, 0.3, (0, 0, 0), EARTH), "ground")
    z0 = 0.3
    m.add(1, compound("main", 17, 16, [(6, 5, 12, 11), (1, 1, 5, 5), (13, 11, 16, 15)], (-22, 14, z0), 3.6, 3.2, STUCCO,
                      "main", TRED, (0,), (0,)), "compounds")
    m.add(1, compound("small", 9, 8, [(3, 2, 6, 6)], (34, -36, z0), 3.4, 3.0, STUCCO_D, "main", TRED, (), ()))
    # the Zapotec tomb entered by a stair from the main patio: an opening, a carved stone jamb and lintel
    tx, ty, zf = -22 - 30.6 + 9 * 3.6 + 4.0, 14 - 28.8 + 8 * 3.6 - 5.0, z0 + 1.02
    m.add(2, box("tomb_pit", 2.6, 3.4, 0.1, (tx, ty, zf), DARK), "tomb")
    for s in (-1, 1):
        m.add(2, box(f"jamb{s}", 0.5, 0.6, 1.6, (tx + s * 1.5, ty + 1.9, zf), "#9C9283"))
        m.add(2, box(f"glyph{s}", 0.1, 0.4, 1.0, (tx + s * 1.5 - s * 0.3, ty + 1.9, zf + 0.3), TRED_D))
    m.add(2, box("lintel", 3.8, 0.7, 0.5, (tx, ty + 1.9, zf + 1.6), "#9C9283"))
    m.add(2, box("urn_b", 0.6, 0.6, 0.7, (tx - 2.6, ty + 1.2, zf), "#8F8A82"))
    m.add(2, box("urn_h", 0.9, 0.3, 0.6, (tx - 2.6, ty + 1.2, zf + 0.7), "#8F8A82"))
    # a carved stela in the open ground, fields and adobe outbuildings
    m.add(2, box("stela_b", 2.2, 1.6, 0.4, (30, 30, z0), "#9C9283"))
    m.add(2, box("stela", 1.4, 0.6, 3.8, (30, 30, z0 + 0.4), "#A9A196"))
    for q in range(3):
        m.add(2, box(f"stg{q}", 0.9, 0.1, 0.7, (30, 29.65, z0 + 1.2 + q * 0.9), TRED_D))
    for i, (px, py, w, d) in enumerate(((30, 2, 26, 18), (2, -42, 26, 22), (-38, -42, 26, 22), (44, 50, 14, 14))):
        m.add(2, maize_plot(f"plot{i}", w, d, (px, py, z0), 5, 10), "fields")
    for i, (hx, hy) in enumerate(((-50, -22), (12, 46), (52, 8))):
        m.add(2, box(f"hut{i}", 7, 5, 2.5, (hx, hy, z0), ADOBE_C))
        m.add(2, box(f"hutr{i}", 7.6, 5.6, 0.3, (hx, hy, z0 + 2.5), shade(ADOBE_C, -0.1)))
    for q in range(6):
        m.add(2, figure(f"f{q}", (tx - 3 + q * 1.4, ty - 2.5, zf), "#D8CDB6" if q % 2 else "#8E8A84"), "people")
    return m


def round_house(name, r, loc, wall=ADOBE_C):
    x, y, z = loc
    p = [cylinder(name + "_b", r * 1.08, 0.5, (x, y, z), shade(wall, -0.1), verts=16),
         cylinder(name + "_w", r, 2.6, (x, y, z + 0.5), wall, verts=16),
         box(name + "_d", 1.2, 0.4, 1.9, (x, y - r, z + 0.5), DARK),
         cylinder(name + "_r", r * 1.25, r * 1.1, (x, y, z + 3.1), THATCH, verts=16, r_top=0.15)]
    return join(p, name)


def merchants_barrio():
    m = Model("merchants-barrio")
    m.add(0, box("ground", 140, 120, 0.3, (0, 0, 0), EARTH), "ground")
    z0 = 0.3
    m.add(1, compound("cmp", 14, 14, [(5, 5, 10, 10), (1, 1, 4, 4)], (-38, 18, z0), 3.6, 3.2, STUCCO, "main", TRED, (0,), (0,)), "compounds")
    for i, (hx, hy, r) in enumerate(((22, 30, 5.0), (40, 18, 4.2), (30, 2, 4.6), (52, 40, 3.8), (12, -20, 4.4), (36, -30, 5.0), (56, -10, 3.8), (-14, -36, 4.0))):
        m.add(1, round_house(f"rh{i}", r, (hx, hy, z0)))
    m.add(2, box("yard", 16, 26, 0.12, (0, 6, z0), shade(EARTH, 0.1)), "goods")
    for q in range(14):
        c = [CLOTH, OCHRE, "#C9763E", SHELL, JADE][q % 5]
        if q % 3 == 0:
            m.add(2, cylinder(f"jar{q}", 0.45, 0.9, (-6 + (q % 7) * 2, -4 + (q // 7) * 8, z0 + 0.12), "#B36B45", verts=10, r_top=0.25))
        else:
            m.add(2, box(f"bale{q}", 1.4, 1.0, 0.8, (-6 + (q % 7) * 2, -4 + (q // 7) * 8, z0 + 0.12), c))
    for i, (px, py, w, d) in enumerate(((-40, -40, 30, 24), (-62, -20, 10, 12), (58, 52, 18, 12))):
        m.add(2, maize_plot(f"plot{i}", w, d, (px, py, z0), 5, 10), "fields")
    for q in range(8):
        m.add(2, figure(f"p{q}", (-6 + q * 5, -8 + (q % 3) * 6, z0), CLOTH if q % 2 else "#C9763E", MAT if q % 2 else None), "people")
    return m


BUILDERS = {
    "teotihuacan/pyramid-of-the-sun": lambda: pyramid_of_the_sun("main"),
    "teotihuacan/pyramid-of-the-sun-100": lambda: pyramid_of_the_sun("building"),
    "teotihuacan/pyramid-of-the-sun-650": lambda: pyramid_of_the_sun("burned"),
    "teotihuacan/pyramid-of-the-sun-1500": lambda: pyramid_of_the_sun("ruin"),
    "teotihuacan/pyramid-of-the-moon": lambda: pyramid_of_the_moon("main"),
    "teotihuacan/pyramid-of-the-moon-100": lambda: pyramid_of_the_moon("early"),
    "teotihuacan/pyramid-of-the-moon-650": lambda: pyramid_of_the_moon("burned"),
    "teotihuacan/pyramid-of-the-moon-1500": lambda: pyramid_of_the_moon("ruin"),
    "teotihuacan/moon-plaza": lambda: moon_plaza("main"),
    "teotihuacan/moon-plaza-650": lambda: moon_plaza("burned"),
    "teotihuacan/moon-plaza-1500": lambda: moon_plaza("ruin"),
    "teotihuacan/palace-of-quetzalpapalotl": lambda: palace_of_quetzalpapalotl("main"),
    "teotihuacan/palace-of-quetzalpapalotl-650": lambda: palace_of_quetzalpapalotl("burned"),
    "teotihuacan/plaza-of-the-columns": lambda: plaza_of_the_columns("main"),
    "teotihuacan/plaza-of-the-columns-650": lambda: plaza_of_the_columns("burned"),
    "teotihuacan/xalla": lambda: xalla("main"),
    "teotihuacan/xalla-650": lambda: xalla("burned"),
    "teotihuacan/tepantitla": tepantitla,
    "teotihuacan/tetitla": tetitla,
    "teotihuacan/atetelco": atetelco,
    "teotihuacan/avenue-of-the-dead": lambda: avenue_of_the_dead("main"),
    "teotihuacan/avenue-of-the-dead-650": lambda: avenue_of_the_dead("burned"),
    "teotihuacan/avenue-of-the-dead-1500": lambda: avenue_of_the_dead("ruin"),
    "teotihuacan/san-juan-crossing": san_juan_crossing,
    "teotihuacan/ciudadela": lambda: ciudadela("main"),
    "teotihuacan/ciudadela-650": lambda: ciudadela("burned"),
    "teotihuacan/ciudadela-1500": lambda: ciudadela("ruin"),
    "teotihuacan/temple-of-the-feathered-serpent": lambda: temple_of_the_feathered_serpent("main"),
    "teotihuacan/temple-of-the-feathered-serpent-adosada": lambda: temple_of_the_feathered_serpent("adosada"),
    "teotihuacan/temple-of-the-feathered-serpent-650": lambda: temple_of_the_feathered_serpent("burned"),
    "teotihuacan/temple-of-the-feathered-serpent-1500": lambda: temple_of_the_feathered_serpent("ruin"),
    "teotihuacan/great-compound": great_compound,
    "teotihuacan/oaxaca-barrio": oaxaca_barrio,
    "teotihuacan/merchants-barrio": merchants_barrio,
}
