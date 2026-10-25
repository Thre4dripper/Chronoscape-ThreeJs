"""Taxila landmark miniatures: the Dharmarajika stupa, Sirkap's wall, gate, shrines, palace and house blocks,
the Greek-plan temple at Jandial, the Kunala stupa, the Bhir Mound houses, Sirsukh's Kushan wall and the
Mohra Moradu monastery.

Conventions as worldkit: metres, origin at the ground centre of the footprint, +X east, +Y north, +Z up,
main front to the south (-Y); the landmark's rotation turns it on the map. Helpers build pieces in world
space; bake() applies transforms, turn() rotates about the world origin. Gandharan stupas get a square
base with pilasters, a drum, a hemispherical dome, a harmika and a tall mast of umbrellas; Kushan walls
are drawn in diaper masonry as alternating bands of two stone colours. Ruined variants are made by
leaving out roofs and umbrellas and then squashing everything above an uneven cut line (ruinify).
"""
import math, random
import bpy
from chronokit import Model, box, cylinder, dome, join, shade, gable_roof, mesh_from
from worldkit import lathe, prism, frustum, arch_panel, stair, tree, wall_run, rot, move
from archkit import column, copy_at, half_cyl_y, entablature, pediment

# ---------------------------------------------------------------- palette
RUBBLE = "#BBA987"     # undressed stone in mud (Bhir Mound, early Sirkap)
RUBBLE_D = "#A8956F"
DIAPER_A = "#B6A27F"   # diaper masonry: big blocks
DIAPER_B = "#CDBE9C"   # ... and the small packing stones
KANJUR = "#D8C8A0"     # soft limestone (kanjur), stuccoed
STUCCO = "#EAE2CF"     # lime stucco
STUCCO_W = "#F0EADC"
PLAST = "#E2D5BA"      # mud plaster
MUD = "#B89A74"
ROOF = "#A48C6C"       # flat roofs of beams and clay
TIMBER = "#8C6A4A"
TILE = "#B06844"
DARK = "#2E241C"
GILT = "#CFA64E"
RED = "#A64B3B"
BLUE = "#4F6A8E"
GROUND = "#BDA582"
PAVE = "#C9B794"
ROCK = "#A39478"
ROCK_D = "#8E8068"
GRASS = "#93A27A"
WATER = "#5F878C"
ASH = "#5E554C"
SCHIST = "#7F857A"


# ================================================================ basic helpers

def _sel(o):
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o


def bake(o):
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


def hemi(name, r, loc, color, rise=0.95, verts=20, rings=6):
    """A dome (anda) as a solid of revolution."""
    prof = [(r, 0)] + [(r * math.cos(a), r * rise * math.sin(a)) for a in [math.pi / 2 * i / rings for i in range(1, rings + 1)]]
    prof[-1] = (0.0, prof[-1][1])
    return lathe(name, prof, loc, color, verts=verts)


def banded(name, w, d, h, loc, c1=DIAPER_A, c2=DIAPER_B, band=1.3, rot_z=0.0):
    """A block of diaper masonry: courses of large stones and bands of small packing stones in two colours."""
    x, y, z = loc
    n = max(1, int(round(h / band)))
    hh = h / n
    return J([box(f"{name}{i}", w + (0.04 if i % 2 else 0), d + (0.04 if i % 2 else 0), hh, (x, y, z + i * hh), c1 if i % 2 == 0 else c2, rot_z) for i in range(n)], name)


def banded_cyl(name, r, h, loc, c1=DIAPER_A, c2=DIAPER_B, band=1.3, verts=16):
    x, y, z = loc
    n = max(1, int(round(h / band)))
    hh = h / n
    return J([cylinder(f"{name}{i}", r + (0.03 if i % 2 else 0), hh, (x, y, z + i * hh), c1 if i % 2 == 0 else c2, verts=verts) for i in range(n)], name)


def ring_pts(r, n, start=0.0):
    return [(r * math.cos(start + math.tau * i / n), r * math.sin(start + math.tau * i / n)) for i in range(n)]


def pilasters_sq(name, w, d, z, h, color, every=1.6, pw=0.35, proj=0.18, cap=True):
    """Flat pilasters with capitals round a w x d block (base at z), one every `every` metres."""
    out = []
    for side, (L, fixed, horiz) in enumerate([(w, -d / 2, True), (w, d / 2, True), (d, -w / 2, False), (d, w / 2, False)]):
        n = max(2, int(L / every))
        for i in range(n + 1):
            t = -L / 2 + L * i / n
            if horiz:
                px, py, pw_, pd_ = t, fixed + (proj / 2 if fixed > 0 else -proj / 2), pw, proj
            else:
                px, py, pw_, pd_ = fixed + (proj / 2 if fixed > 0 else -proj / 2), t, proj, pw
            out.append(box(f"{name}{side}_{i}", pw_, pd_, h, (px, py, z), color))
            if cap:
                out.append(box(f"{name}{side}_{i}c", pw_ * 1.6, pd_ * 1.6, h * 0.12, (px, py, z + h * 0.88), shade(color, 0.05)))
    return J(out, name)


def pilasters_round(name, r, z, h, n, color, pw=0.4, proj=0.18, loc=(0, 0)):
    out = []
    for i in range(n):
        a = math.tau * i / n
        out.append(box(f"{name}{i}", proj, pw, h, (loc[0] + (r + proj / 2) * math.cos(a), loc[1] + (r + proj / 2) * math.sin(a), z), color, rot_z=a))
    return J(out, name)


def umbrellas(name, x, y, z, n, r0, step, color=STUCCO, mast=TIMBER, r1=None):
    """The chattravali: a mast with n umbrellas, the lowest of radius r0 shrinking upward."""
    r1 = r1 if r1 is not None else r0 * 0.35
    parts = [cylinder(name + "_mast", r0 * 0.06 + 0.05, step * (n + 0.8), (x, y, z), mast, verts=6)]
    for i in range(n):
        r = r0 + (r1 - r0) * (i / max(1, n - 1))
        parts.append(cylinder(f"{name}_u{i}", r, max(0.12, step * 0.16), (x, y, z + step * (i + 0.6)), color, verts=14, r_top=r * 0.82))
    return J(parts, name)


def harmika(name, x, y, z, s, color=STUCCO):
    """The railed box on top of the dome, crowned by inverted steps."""
    parts = [box(name + "_b", s, s, s * 0.7, (x, y, z), color)]
    for i in range(3):
        parts.append(box(f"{name}_s{i}", s * (1.05 + i * 0.12), s * (1.05 + i * 0.12), s * 0.12, (x, y, z + s * 0.7 + i * s * 0.12), shade(color, -0.04)))
    return J(parts, name), z + s * 0.7 + 3 * s * 0.12


def seated_buddha(name, x, y, z, h, color=STUCCO_W, face=0.0):
    """A tiny seated figure with a halo, for niches (h = seated height)."""
    parts = [box(name + "_lap", h * 0.7, h * 0.4, h * 0.22, (x, y, z), color, rot_z=face),
             box(name + "_body", h * 0.42, h * 0.3, h * 0.45, (x, y, z + h * 0.22), color, rot_z=face),
             dome(name + "_head", h * 0.14, (x, y, z + h * 0.67), color, squash=1.0, segments=8, rings=4)]
    return J(parts, name)


def gstupa(name, base_w, loc=(0, 0, 0), tiers=1, tier_h=None, drum_r=None, drum_h=None, dome_r=None, umb=5, color=STUCCO, base_color=None,
           stair_face="S", pil=True, niches=0, verts=24, rail=False, top=True, fig_color=None):
    """A Gandharan stupa: square base of one or more moulded tiers with pilasters and a stair, one or two
    drums, a hemispherical dome, harmika and a mast of umbrellas. Returns (object, top z)."""
    x, y, z0 = loc
    bc = base_color or color
    th = tier_h or base_w * 0.18
    parts = []
    z = z0
    w = base_w
    for t in range(tiers):
        parts.append(box(f"{name}_t{t}", w, w, th, (x, y, z), bc))
        parts.append(box(f"{name}_t{t}m", w + 0.3, w + 0.3, th * 0.1, (x, y, z), shade(bc, -0.06)))
        parts.append(box(f"{name}_t{t}c", w + 0.4, w + 0.4, th * 0.1, (x, y, z + th * 0.9), shade(bc, 0.04)))
        if pil:
            p = pilasters_sq(f"{name}_p{t}", w, w, z + th * 0.1, th * 0.8, shade(bc, 0.03), every=max(1.2, w / 9))
            parts.append(move(p, x, y, 0))
        if niches and t == 0:
            for side, face in enumerate(("S", "N", "E", "W")):
                L = w * 0.8
                for k in range(niches):
                    u = -L / 2 + L * (k + 0.5) / niches
                    nx, ny, fa = {"S": (x + u, y - w / 2 - 0.02, 0), "N": (x + u, y + w / 2 + 0.02, math.pi), "E": (x + w / 2 + 0.02, y + u, math.pi / 2), "W": (x - w / 2 - 0.02, y + u, -math.pi / 2)}[face]
                    if face == stair_face and abs(u) < w * 0.16:
                        continue
                    nh = th * 0.62
                    parts.append(arch_panel(f"{name}_n{side}_{k}", L / niches * 0.62, nh, (nx, ny, z + th * 0.16), face, DARK, False, 0.2))
                    off = {"S": (0, -0.12), "N": (0, 0.12), "E": (0.12, 0), "W": (-0.12, 0)}[face]
                    parts.append(seated_buddha(f"{name}_b{side}_{k}", nx + off[0], ny + off[1], z + th * 0.16, nh * 0.62, fig_color or STUCCO_W, fa))
        if stair_face and t == 0:
            run = th * tiers * 1.0
            sw = w * 0.22
            if stair_face == "S":
                sl = (x, y - w / 2 - run / 2, 0)
            elif stair_face == "N":
                sl = (x, y + w / 2 + run / 2, 0)
            elif stair_face == "E":
                sl = (x + w / 2 + run / 2, y, 0)
            else:
                sl = (x - w / 2 - run / 2, y, 0)
            s = stair(f"{name}_st", sw, th * tiers, run, max(4, int(th * tiers / 0.3)), (0, 0, z0), stair_face, shade(bc, -0.05))
            parts.append(move(s, sl[0], sl[1], 0))
        z += th
        w *= 0.8
    dr = drum_r or w * 0.45
    dh = drum_h or dr * 0.55
    parts.append(cylinder(name + "_drum", dr, dh, (x, y, z), color, verts=verts))
    parts.append(cylinder(name + "_drumc", dr + 0.18, dh * 0.08, (x, y, z + dh * 0.92), shade(color, 0.04), verts=verts))
    if pil and dr > 1.5:
        parts.append(pilasters_round(name + "_dp", dr, z, dh * 0.92, max(8, int(dr * 2.2)), shade(color, 0.03), pw=min(0.5, dr * 0.12), proj=0.15, loc=(x, y)))
    if niches and dr > 2:
        n = max(6, int(dr * 1.6))
        for i in range(n):
            a = math.tau * (i + 0.5) / n
            nx, ny = x + (dr + 0.05) * math.cos(a), y + (dr + 0.05) * math.sin(a)
            parts.append(box(f"{name}_dn{i}", 0.2, dr * 0.5, dh * 0.6, (nx, ny, z + dh * 0.15), DARK, rot_z=a))
            parts.append(seated_buddha(f"{name}_db{i}", x + (dr + 0.18) * math.cos(a), y + (dr + 0.18) * math.sin(a), z + dh * 0.15, dh * 0.42, fig_color or STUCCO_W, a + math.pi / 2))
    z += dh
    rr = dome_r or dr * 0.96
    parts.append(hemi(name + "_anda", rr, (x, y, z), color, rise=0.95, verts=verts, rings=7 if verts >= 20 else 4))
    z += rr * 0.95
    if top:
        h, z = harmika(name + "_h", x, y, z - rr * 0.04, rr * 0.36, shade(color, -0.04))
        parts.append(h)
        if umb:
            parts.append(umbrellas(name + "_umb", x, y, z, umb, rr * 0.55, rr * 0.32))
            z += rr * 0.32 * (umb + 0.8)
    if rail:
        parts.append(lathe(name + "_rail", [(dr * 1.35, 0), (dr * 1.35, 1.1), (dr * 1.3, 1.1), (dr * 1.3, 0)], (x, y, z0), TIMBER, verts=verts * 2, cap_top=False, cap_bottom=False))
    return J(parts, name), z


def votive(name, s, loc, color=STUCCO, umb=3):
    """A small votive stupa (s = side of its square base)."""
    o, _ = gstupa(name, s, loc, tiers=1, tier_h=s * 0.45, drum_r=s * 0.36, drum_h=s * 0.25, umb=umb, color=color, stair_face=None, pil=False, verts=12)
    return o


def ruinify(objs, cut=3.0, keep=0.3, seed=1.0, floor=0.0):
    """Squash everything above an uneven cut line: walls become broken stumps, domes low mounds."""
    for o in objs:
        if o is None:
            continue
        bake(o)
        for v in o.data.vertices:
            x, y, z = v.co
            n = 0.5 + 0.5 * math.sin(x * 0.41 + seed) * math.cos(y * 0.33 - seed * 1.7)
            c = max(floor, cut * (0.5 + 0.9 * n))
            if z > c:
                v.co.z = c + (z - c) * keep
        o.data.update()
    return objs


def flat_room(name, w, d, h, loc, color=PLAST, roof=ROOF, door=None, parapet=True, rot_z=0.0):
    """A flat-roofed room or house of rubble and plaster; door = face letter for a dark doorway."""
    x, y, z = loc
    parts = [box(name + "_b", w, d, h, (x, y, z), color, rot_z)]
    if parapet:
        parts.append(box(name + "_r", w - 0.3, d - 0.3, 0.12, (x, y, z + h), roof, rot_z))
        parts.append(box(name + "_p", w + 0.1, d + 0.1, 0.45, (x, y, z + h), shade(color, -0.05), rot_z))
        parts.append(box(name + "_pi", w - 0.5, d - 0.5, 0.5, (x, y, z + h + 0.02), roof, rot_z))
    if door:
        dw, dh = min(1.2, min(w, d) * 0.3), min(2.2, h * 0.6)
        ox, oy = {"S": (0, -d / 2 - 0.05), "N": (0, d / 2 + 0.05), "E": (w / 2 + 0.05, 0), "W": (-w / 2 - 0.05, 0)}[door]
        bw, bd = (dw, 0.2) if door in ("S", "N") else (0.2, dw)
        c, s = math.cos(rot_z), math.sin(rot_z)
        parts.append(box(name + "_d", bw, bd, dh, (x + ox * c - oy * s, y + ox * s + oy * c, z), DARK, rot_z))
    return J(parts, name)


def court_house(name, w, d, h, loc, color=PLAST, depth=None, door="S", storey2=False, rng=None):
    """Rooms on four sides of an open court, flat roofs with parapets; an optional upper room."""
    x, y, z = loc
    dp = depth or min(w, d) * 0.3
    parts = [flat_room(name + "_s", w, dp, h, (x, y - d / 2 + dp / 2, z), color, door=door if door == "S" else None),
             flat_room(name + "_n", w, dp, h, (x, y + d / 2 - dp / 2, z), color, door=door if door == "N" else None),
             flat_room(name + "_w", dp, d - 2 * dp, h * 0.92, (x - w / 2 + dp / 2, y, z), shade(color, -0.03), door=door if door == "W" else None),
             flat_room(name + "_e", dp, d - 2 * dp, h * 0.92, (x + w / 2 - dp / 2, y, z), shade(color, -0.03), door=door if door == "E" else None),
             box(name + "_court", w - 2 * dp, d - 2 * dp, 0.08, (x, y - 0, z), PAVE)]
    # doors from the court into the rooms
    for i, (ox, oy, bw, bd) in enumerate([(0, -d / 2 + dp + 0.05, 1.0, 0.15), (0, d / 2 - dp - 0.05, 1.0, 0.15), (-w / 2 + dp + 0.05, 0, 0.15, 1.0), (w / 2 - dp - 0.05, 0, 0.15, 1.0)]):
        parts.append(box(f"{name}_cd{i}", bw, bd, min(2.0, h * 0.55), (x + ox, y + oy, z), DARK))
    if storey2:
        parts.append(flat_room(name + "_up", w * 0.45, dp, h * 0.8, (x - w * 0.2, y + d / 2 - dp / 2, z + h + 0.12), shade(color, 0.03)))
    return J(parts, name)


def monastery(name, w, d, h, loc, color=DIAPER_A, color2=DIAPER_B, cells_per_side=None, storeys=1, tank=True, roofed=True, door="S"):
    """A sangharama: cells round a square court with a pillared verandah, flat roofs, a tank in the court."""
    x, y, z = loc
    dp = min(w, d) * 0.2
    parts = []
    for k, (cw, cd, cx, cy) in enumerate([(w, dp, x, y - d / 2 + dp / 2), (w, dp, x, y + d / 2 - dp / 2), (dp, d - 2 * dp, x - w / 2 + dp / 2, y), (dp, d - 2 * dp, x + w / 2 - dp / 2, y)]):
        parts.append(banded(f"{name}_r{k}", cw, cd, h, (cx, cy, z), color, color2, band=h / 4))
        if storeys > 1:
            parts.append(banded(f"{name}_u{k}", cw - 0.6 if cw > cd else cw, cd if cw > cd else cd - 0.6, h * 0.85, (cx, cy, z + h), color, color2, band=h / 3))
        if roofed:
            ztop = z + h * (1 + 0.85 * (storeys - 1))
            parts.append(box(f"{name}_rf{k}", cw + 0.3, cd + 0.3, 0.35, (cx, cy, ztop), ROOF))
            parts.append(box(f"{name}_pp{k}", cw + 0.4, cd + 0.4, 0.5, (cx, cy, ztop + 0.35), shade(ROOF, -0.08)))
            parts.append(box(f"{name}_pi{k}", max(0.1, cw - 0.6), max(0.1, cd - 0.6), 0.55, (cx, cy, ztop + 0.36), ROOF))
    # verandah posts and cell doors round the court
    iw, idp = w - 2 * dp, d - 2 * dp
    n = cells_per_side or max(3, int(iw / 3.2))
    for side, (L, fixed, horiz, sgn) in enumerate([(iw, -idp / 2, True, 1), (iw, idp / 2, True, -1), (idp, -iw / 2, False, 1), (idp, iw / 2, False, -1)]):
        for i in range(n):
            t = -L / 2 + L * (i + 0.5) / n
            if horiz:
                parts.append(box(f"{name}_cd{side}_{i}", min(1.0, L / n * 0.4), 0.2, min(2.0, h * 0.5), (x + t, y + fixed - sgn * 0.05, z), DARK))
                parts.append(box(f"{name}_vp{side}_{i}", 0.35, 0.35, h * 0.9, (x + t + L / n / 2, y + fixed + sgn * 1.6, z), TIMBER))
            else:
                parts.append(box(f"{name}_cd{side}_{i}", 0.2, min(1.0, L / n * 0.4), min(2.0, h * 0.5), (x + fixed - sgn * 0.05, y + t, z), DARK))
                parts.append(box(f"{name}_vp{side}_{i}", 0.35, 0.35, h * 0.9, (x + fixed + sgn * 1.6, y + t + L / n / 2, z), TIMBER))
    if roofed:
        # verandah roof: a lean-to slab round the inner court
        for k, (vw, vd, vx, vy) in enumerate([(iw, 1.9, x, y - idp / 2 + 0.95), (iw, 1.9, x, y + idp / 2 - 0.95), (1.9, idp - 3.8, x - iw / 2 + 0.95, y), (1.9, idp - 3.8, x + iw / 2 - 0.95, y)]):
            parts.append(box(f"{name}_vr{k}", vw, vd, 0.25, (vx, vy, z + h * 0.9), ROOF))
    parts.append(box(name + "_court", iw, idp, 0.1, (x, y, z), PAVE))
    if tank:
        parts.append(box(name + "_tank", iw * 0.3, idp * 0.3, 0.3, (x, y, z), shade(PAVE, -0.1)))
        parts.append(box(name + "_water", iw * 0.26, idp * 0.26, 0.32, (x, y, z), WATER))
    # entrance
    ox, oy, fw, fd = {"S": (0, -d / 2 - 0.05, 2.2, 0.3), "N": (0, d / 2 + 0.05, 2.2, 0.3), "E": (w / 2 + 0.05, 0, 0.3, 2.2), "W": (-w / 2 - 0.05, 0, 0.3, 2.2)}[door]
    parts.append(box(name + "_gate", fw, fd, min(3.2, h * 0.75), (x + ox, y + oy, z), DARK))
    return J(parts, name)


def ground(name, w, d, color=GROUND, h=0.3):
    return box(name, w, d, h, (0, 0, 0), color)


# ================================================================ the Dharmarajika stupa

def dharmarajika(variant="kushan"):
    """Footprint 140 x 170: the great stupa south of centre, its ring of votive stupas and chapels, a monastery to the north."""
    m = Model("dharmarajika-" + variant)
    SX, SY = 0.0, -35.0
    m.add(0, ground("ground", 140, 170, GROUND), "terrace")
    if variant == "early" or variant == "ig":
        m.add(0, cylinder("pave", 22, 0.35, (SX, SY, 0), PAVE, verts=40))
        o, _ = gstupa("stupa", 0, (SX, SY, 0.35), tiers=0, drum_r=12.5, drum_h=1.6, dome_r=12.0, umb=1, color=PLAST, stair_face=None, pil=False, verts=32, rail=True)
        m.add(1, o, "stupa")
        if variant == "ig":
            for i, (px, py) in enumerate(ring_pts(19, 12, 0.2)):
                if abs(px) < 3 or abs(py) < 3:
                    continue
                m.add(2, votive(f"v{i}", 2.6, (SX + px, SY + py, 0.35), STUCCO, umb=2), "votives")
            for i, (px, py) in enumerate([(-24, 0), (24, 0), (0, 24)]):
                m.add(2, flat_room(f"ch{i}", 5.5, 5, 4, (SX + px, SY + py, 0), DIAPER_B, door={0: "E", 1: "W", 2: "S"}[i]))
            m.add(2, monastery("vihara", 40, 34, 4.2, (0, 40, 0), RUBBLE, PLAST, roofed=True), "monastery")
        else:
            m.add(2, J([flat_room(f"hut{i}", 5, 4, 3, (x, 30 + (i % 2) * 6, 0), MUD, door="S") for i, x in enumerate((-10, -3, 4, 11))], "huts"), "monks")
        for i, (tx, ty) in enumerate([(-45, 50), (40, 60), (-50, -70), (50, -75), (55, 20)]):
            m.add(2, tree(f"tree{i}", 3.2, (tx, ty, 0), "#6F8A5C"))
        return m

    ruined = variant == "ruin"
    # paved court and its ring of chapels
    m.add(0, cylinder("court", 48, 0.3, (SX, SY, 0), PAVE, verts=48), "court")
    # the great stupa: round terrace with four stairs, drum with pilasters, dome, harmika, umbrellas
    TR, TH = 24.0, 3.4
    parts = [banded_cyl("terrace", TR, TH, (SX, SY, 0.3), KANJUR, shade(KANJUR, -0.06), band=0.85, verts=40),
             cylinder("terrace_cap", TR + 0.5, 0.35, (SX, SY, 0.3 + TH), shade(KANJUR, 0.05), verts=40),
             pilasters_round("terrace_pil", TR, 0.6, TH - 0.5, 44, shade(KANJUR, 0.06), pw=0.55, proj=0.2, loc=(SX, SY))]
    for face, (ox, oy) in {"S": (0, -TR - 3.5), "N": (0, TR + 3.5), "E": (TR + 3.5, 0), "W": (-TR - 3.5, 0)}.items():
        s = stair("st" + face, 5.0, TH + 0.3, 7.0, 10, (0, 0, 0.3), face, shade(KANJUR, -0.05))
        parts.append(move(s, SX + ox, SY + oy, 0))
    z = 0.3 + TH + 0.35
    DR, DH = 18.5, 5.5
    parts += [cylinder("drum", DR, DH, (SX, SY, z), STUCCO, verts=40),
              pilasters_round("drum_pil", DR, z + 0.3, DH - 0.8, 36, shade(STUCCO, -0.04), pw=0.6, proj=0.22, loc=(SX, SY)),
              cylinder("drum_c", DR + 0.5, 0.45, (SX, SY, z + DH - 0.45), shade(STUCCO, 0.03), verts=40),
              cylinder("drum_b", DR + 0.4, 0.4, (SX, SY, z), shade(STUCCO, -0.06), verts=40)]
    z += DH
    if ruined:
        parts.append(hemi("anda", 17.5, (SX, SY, z), shade(KANJUR, -0.1), rise=0.62, verts=32, rings=7))
        # the great cut made by treasure hunters, a dark scar in the dome
        parts.append(box("scar", 4, 18, 6, (SX, SY - 9, z + 4), ASH))
        stupa = J(parts, "great_stupa")
        ruinify([stupa], cut=9.0, keep=0.6, seed=2.0)
        m.add(1, stupa, "great stupa")
    else:
        parts.append(hemi("anda", 17.5, (SX, SY, z), STUCCO_W, rise=0.9, verts=40, rings=9))
        z += 17.5 * 0.9
        h, z2 = harmika("harmika", SX, SY, z - 0.6, 6.0, shade(STUCCO, -0.03))
        parts.append(h)
        parts.append(umbrellas("chattra", SX, SY, z2, 7, 6.0, 1.7, color=shade(STUCCO, -0.05), r1=1.8))
        parts.append(cylinder("finial", 0.25, 1.5, (SX, SY, z2 + 1.7 * 7.8), GILT, verts=6))
        m.add(1, J(parts, "great_stupa"), "great stupa")

    # votive stupas on the circuit, chapels round the court
    vs = []
    proto = votive("vproto", 3.2, (0, 0, 0.3), STUCCO, umb=0 if ruined else 3)
    for i, (px, py) in enumerate(ring_pts(31, 28, 0.06)):
        if min(abs(px), abs(py)) < 4.5:
            continue
        vs.append(copy_at(proto, (SX + px, SY + py, 0), name=f"vs{i}"))
    for i, (px, py) in enumerate(ring_pts(36.5, 18, 0.2)):
        if min(abs(px), abs(py)) < 4.5:
            continue
        vs.append(copy_at(proto, (SX + px, SY + py, 0), name=f"vt{i}"))
    bpy.data.objects.remove(proto, do_unlink=True)
    chapels = []
    n = 26
    for i in range(n):
        a = math.tau * (i + 0.5) / n
        cx, cy = SX + 43 * math.cos(a), SY + 43 * math.sin(a)
        if min(abs(cx - SX), abs(cy - SY)) < 6:
            continue
        rz = a + math.pi / 2
        c = [banded(f"ch{i}", 7.5, 5.5, 4.5, (cx, cy, 0), DIAPER_A, DIAPER_B, band=0.9, rot_z=rz)]
        dx, dy = -math.cos(a) * 2.8, -math.sin(a) * 2.8
        c.append(box(f"ch{i}_door", 1.6, 0.3, 2.6, (cx + dx, cy + dy, 0), DARK, rot_z=rz))
        if not ruined:
            c.append(box(f"ch{i}_roof", 8.1, 6.1, 0.4, (cx, cy, 4.5), ROOF, rot_z=rz))
            c.append(box(f"ch{i}_fig", 0.9, 0.5, 1.4, (cx + dx * 0.55, cy + dy * 0.55, 0.6), STUCCO_W, rot_z=rz))
        chapels.append(J(c, f"chapel{i}"))
    if ruined:
        ruinify(vs, cut=1.3, keep=0.25, seed=0.7)
        ruinify(chapels, cut=2.0, keep=0.3, seed=1.3)
    m.add(2, J(vs, "votives"), "votive stupas")
    m.add(2, J(chapels, "chapels"), "chapels")
    # monastery courts to the north
    mon = [monastery("vihara", 62, 52, 5.0, (-12, 56, 0), DIAPER_A, DIAPER_B, storeys=1 if ruined else 2, roofed=not ruined),
           monastery("vihara2", 36, 40, 4.5, (40, 52, 0), DIAPER_A, DIAPER_B, storeys=1, roofed=not ruined, tank=False, door="W")]
    if ruined:
        ruinify(mon, cut=2.2, keep=0.3, seed=0.4)
        for i, (ax, ay) in enumerate([(-20, 50), (-5, 62), (35, 48), (-30, -20), (25, -60)]):
            mon.append(box(f"ash{i}", 6, 4, 0.36, (ax, ay, 0), ASH))
    m.add(2, J(mon, "monastery"), "monastery")
    trees = [tree(f"tree{i}", 3.2, (tx, ty, 0), "#6F8A5C") for i, (tx, ty) in enumerate([(-62, -75), (60, -78), (62, 10), (-62, 15), (-60, -40), (64, -30)])]
    m.add(3, J(trees, "trees"), "trees")
    return m


# ================================================================ Sirkap

def sirkap_wall(ruined=False):
    """Footprint 220 x 50: the north wall of Sirkap with square bastions and the north gate. Built with the
    outer face to the south (-Y); the landmark is turned 180 degrees so that it faces north."""
    m = Model("sirkap-wall")
    m.add(0, ground("ground", 220, 50, GROUND), "ground")
    WY, T, H = -8.0, 6.0, 8.5
    wall = []
    for i, (x0, x1) in enumerate([(-110, -9), (9, 110)]):
        L = x1 - x0
        wall.append(banded(f"wall{i}", L, T, H, ((x0 + x1) / 2, WY, 0), RUBBLE, shade(RUBBLE, 0.07), band=0.6))
        wall.append(box(f"walk{i}", L, T - 1.2, 0.2, ((x0 + x1) / 2, WY, H), shade(RUBBLE, -0.05)))
    bast = []
    for i, bx in enumerate((-104, -78, -52, -27, 27, 52, 78, 104)):
        bast.append(banded(f"bast{i}", 11, 9, H + 1.8, (bx, WY - T / 2 - 3.2, 0), RUBBLE, shade(RUBBLE, 0.07), band=0.6))
        bast.append(box(f"bplinth{i}", 12, 10, 1.0, (bx, WY - T / 2 - 3.2, 0), shade(RUBBLE, -0.08)))
    gate = [banded("towerW", 12, 15, H + 4.5, (-11, WY - 2, 0), RUBBLE, shade(RUBBLE, 0.07), band=1.25),
            banded("towerE", 12, 15, H + 4.5, (11, WY - 2, 0), RUBBLE, shade(RUBBLE, 0.07), band=1.25),
            box("passage_floor", 10, 20, 0.15, (0, WY - 1, 0), PAVE)]
    if not ruined:
        gate += [box("lintel", 10.2, 15, 6.0, (0, WY - 2, H - 1.5), shade(RUBBLE, -0.04)),
                 box("gatehouse", 34, 15, 3.2, (0, WY - 2, H + 4.5), PLAST),
                 box("gh_roof", 34.6, 15.6, 0.4, (0, WY - 2, H + 7.7), ROOF),
                 box("gate_doorS", 6.5, 0.4, 6.2, (0, WY - 9.6, 0), DARK),
                 box("gate_doorN", 6.5, 0.4, 6.2, (0, WY + 5.6, 0), DARK)]
        for s in (-1, 1):
            for k in range(3):
                gate.append(box(f"gh_win{s}{k}", 1.0, 0.2, 1.4, (s * (5 + k * 4.5), WY - 9.6, H + 5.5), DARK))
        # battlements with loopholes: stepped merlons along the parapet and on the bastions
        mer = []
        for i, (x0, x1) in enumerate([(-110, -9), (9, 110)]):
            n = int((x1 - x0) / 2.4)
            for k in range(n):
                mx = x0 + (k + 0.5) * (x1 - x0) / n
                mer.append(box(f"m{i}_{k}", 1.3, 0.9, 1.3, (mx, WY - T / 2 + 0.45, H), RUBBLE))
                mer.append(box(f"m{i}_{k}t", 0.7, 0.9, 0.5, (mx, WY - T / 2 + 0.45, H + 1.3), RUBBLE))
        for i, bx in enumerate((-104, -78, -52, -27, 27, 52, 78, 104)):
            for k in range(4):
                mer.append(box(f"bm{i}_{k}", 1.4, 1.0, 1.3, (bx - 4 + k * 2.7, WY - T / 2 - 7.3, H + 1.8), RUBBLE))
            for s in (-1, 1):
                mer.append(box(f"bm{i}_s{s}", 1.0, 1.4, 1.3, (bx + s * 5.0, WY - T / 2 - 4.5, H + 1.8), RUBBLE))
            mer.append(box(f"bl{i}", 0.3, 0.2, 1.4, (bx, WY - T / 2 - 7.75, 4.5), DARK))
        for i, (x0, x1) in enumerate([(-110, -9), (9, 110)]):
            for k in range(int((x1 - x0) / 6)):
                lx = x0 + (k + 0.5) * (x1 - x0) / int((x1 - x0) / 6)
                if any(abs(lx - bx) < 6.5 for bx in (-104, -78, -52, -27, 27, 52, 78, 104)) or abs(lx) < 18:
                    continue
                mer.append(box(f"loop{i}_{k}", 0.3, 0.2, 1.5, (lx, WY - T / 2 - 0.08, 4.8), DARK))
        for k in range(14):
            mx = -16.2 + k * 2.5
            mer.append(box(f"ghm{k}", 1.2, 0.9, 1.1, (mx, WY - 9.2, H + 8.1), PLAST))
            mer.append(box(f"ghn{k}", 1.2, 0.9, 1.1, (mx, WY + 5.2, H + 8.1), PLAST))
        for s in (-1, 1):
            for k in range(5):
                mer.append(box(f"ghs{s}{k}", 0.9, 1.2, 1.1, (s * 16.6, WY - 8 + k * 3.0, H + 8.1), PLAST))
        gate.append(J(mer, "battlements"))
    else:
        for k in range(14):
            gate.append(dome(f"rubble{k}", 4.5, (-100 + k * 15.5, WY - 5 + (k % 3) * 2, 0), shade(RUBBLE, -0.08), squash=0.35, segments=10, rings=5))
    walls = wall + bast + gate
    if ruined:
        ruinify(walls, cut=3.0, keep=0.25, seed=1.1)
    m.add(1, J(wall + bast, "wall"), "wall and bastions")
    m.add(2, J(gate, "gate"), "north gate")
    # inside: the head of the main street with shops and houses, and the lane behind the wall
    town = [box("street", 9, 22, 0.12, (0, 14, 0), PAVE), box("wall_lane", 216, 4, 0.1, (0, 0.5, 0), shade(PAVE, -0.05))]
    rng = random.Random(4)
    for s in (-1, 1):
        x = 6.5
        while x < 95:
            w = min(rng.uniform(9, 15), 108 - x)
            if not ruined:
                if x < 40:
                    for k in range(int(w // 4.5)):
                        town.append(flat_room(f"shop{s}_{int(x)}_{k}", 4.2, 5, 3.6, (s * (x + 2.2 + k * 4.5), 6.0, 0), PLAST, door="S"))
                    town.append(court_house(f"house{s}_{int(x)}", w, 12, rng.uniform(4.0, 5.6), (s * (x + w / 2), 17.5, 0), PLAST if rng.random() < 0.6 else RUBBLE, door="S", storey2=rng.random() < 0.4))
                else:
                    town.append(court_house(f"house{s}_{int(x)}", w, 19, rng.uniform(4.0, 5.4), (s * (x + w / 2), 12.0, 0), PLAST if rng.random() < 0.5 else RUBBLE, door="S", storey2=rng.random() < 0.3))
            else:
                town.append(box(f"found{s}_{int(x)}", w - 1, 16, 0.9, (s * (x + w / 2), 13, 0), RUBBLE_D))
            x += w + 1.5
    if not ruined:
        town.append(box("road_out", 9, 7, 0.12, (0, -21.5, 0), PAVE))
        town.append(votive("roadside_stupa", 3.2, (-12, -21.5, 0), STUCCO))
        town.append(votive("roadside_stupa2", 2.6, (12, -21.8, 0), STUCCO))
        for s_ in (-1, 1):
            town.append(flat_room(f"guard{s_}", 5, 4, 3.4, (s_ * 9.5, 1.0, 0), RUBBLE, door="E" if s_ < 0 else "W"))
            for k in range(6):
                town.append(box(f"cartrut{s_}{k}", 0.3, 0.6, 0.15, (s_ * 1.6, -24.5 + k * 1.0, 0.12), shade(PAVE, -0.12)))
        for k, tx in enumerate((-40, -66, 40, 66, 92, -92, -20, 20)):
            town.append(tree(f"tree{k}", 2.6, (tx, -22.0, 0), "#6F8A5C"))
    m.add(3, J(town, "town"), "main street")
    return m


def niche_greek(name, x, y, z, w, h, color):
    """A niche framed as a Greek temple front: dark recess, two half-columns, a pediment."""
    t = 0.12
    parts = [box(name + "_r", w * 0.7, 0.1, h * 0.7, (x, y - 0.03, z + h * 0.05), DARK)]
    for s in (-1, 1):
        parts.append(box(f"{name}_c{s}", w * 0.1, t, h * 0.75, (x + s * w * 0.4, y - t / 2, z), shade(color, 0.05)))
    parts.append(box(name + "_ent", w, t, h * 0.08, (x, y - t / 2, z + h * 0.75), shade(color, 0.05)))
    v = [(-w / 2, 0, 0), (w / 2, 0, 0), (0, 0, h * 0.2), (-w / 2, -t, 0), (w / 2, -t, 0), (0, -t, h * 0.2)]
    parts.append(mesh_from(name + "_ped", v, [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)], (x, y, z + h * 0.83), shade(color, 0.05)))
    return J(parts, name), z + h * 1.03


def niche_ogee(name, x, y, z, w, h, color):
    """A niche under an ogee (chaitya) arch."""
    parts = [arch_panel(name + "_r", w * 0.7, h * 0.85, (x, y - 0.03, z + h * 0.05), "S", DARK, True, 0.1),
             arch_panel(name + "_f", w * 0.95, h, (x, y - 0.08, z), "S", shade(color, 0.05), True, 0.06)]
    return J(parts, name), z + h * 1.0


def niche_torana(name, x, y, z, w, h, color):
    """A niche framed as an early Indian torana: two posts and three crossbars with projecting ends."""
    parts = [box(name + "_r", w * 0.6, 0.1, h * 0.65, (x, y - 0.03, z + h * 0.05), DARK)]
    for s in (-1, 1):
        parts.append(box(f"{name}_p{s}", w * 0.1, 0.14, h * 0.95, (x + s * w * 0.36, y - 0.07, z), shade(color, 0.05)))
    for k in range(3):
        parts.append(box(f"{name}_b{k}", w * (1.05 - k * 0.04), 0.14, h * 0.06, (x, y - 0.07, z + h * (0.7 + k * 0.11)), shade(color, 0.05)))
    return J(parts, name), z + h * 1.0


def bird(name, x, y, z, s, double=False, color=GILT):
    """A perched bird with spread wings; double=True gives the two-headed eagle."""
    parts = [box(name + "_body", s * 0.35, s * 0.3, s * 0.55, (x, y, z), color),
             box(name + "_wings", s * 1.3, s * 0.12, s * 0.35, (x, y, z + s * 0.25), color)]
    for k, hx in enumerate((-0.18, 0.18) if double else (0.0,)):
        parts.append(box(f"{name}_neck{k}", s * 0.12, s * 0.12, s * 0.25, (x + hx * s, y, z + s * 0.55), color))
        parts.append(box(f"{name}_head{k}", s * 0.2, s * 0.22, s * 0.16, (x + hx * s * 1.4, y - s * 0.03, z + s * 0.78), color))
    return J(parts, name)


def eagle_shrine():
    """Footprint 14 x 14: the stupa of the double-headed eagle in its small court, front (stair) to the south."""
    m = Model("eagle-shrine")
    m.add(0, ground("court", 14, 14, PAVE, 0.15), "court")
    cw = [box("cw_n", 14, 0.5, 1.4, (0, 6.75, 0), RUBBLE), box("cw_w", 0.5, 13, 1.4, (-6.75, 0.25, 0), RUBBLE), box("cw_e", 0.5, 13, 1.4, (6.75, 0.25, 0), RUBBLE),
          box("cw_sw", 4.5, 0.5, 1.4, (-4.75, -6.75, 0), RUBBLE), box("cw_se", 4.5, 0.5, 1.4, (4.75, -6.75, 0), RUBBLE)]
    m.add(0, J(cw, "court_wall"))
    BW, BD, BH, BY = 8.0, 6.8, 2.6, 1.2
    base = [box("base", BW, BD, BH, (0, BY, 0.15), KANJUR),
            box("base_m", BW + 0.3, BD + 0.3, 0.25, (0, BY, 0.15), shade(KANJUR, -0.06)),
            box("base_c", BW + 0.4, BD + 0.4, 0.3, (0, BY, 0.15 + BH - 0.3), shade(KANJUR, 0.05))]
    fy = BY - BD / 2
    # front: Corinthian pilasters with the three kinds of niche between them, on either side of the stair
    xs = [-3.95, -2.85, -1.75, -0.65, 0.65, 1.75, 2.85, 3.95]
    for i, px in enumerate(xs):
        base.append(box(f"pil{i}", 0.22, 0.16, BH - 0.6, (px, fy - 0.08, 0.4), shade(KANJUR, 0.04)))
        base.append(box(f"pilc{i}", 0.34, 0.24, 0.28, (px, fy - 0.1, 0.15 + BH - 0.58), shade(KANJUR, 0.08)))
    makers = [niche_greek, niche_ogee, niche_torana]
    for s in (-1, 1):
        for k, mk in enumerate(makers):
            cx = s * (3.4 - k * 1.1)
            o, top = mk(f"niche{s}{k}", cx, fy, 0.55, 0.8, 1.35, KANJUR)
            base.append(o)
            base.append(bird(f"bird{s}{k}", cx, fy - 0.12, top, 0.45, double=(k == 2), color=GILT if k == 2 else shade(KANJUR, -0.12)))
    # sides and back: plain pilasters
    for i in range(5):
        for s in (-1, 1):
            base.append(box(f"spil{s}{i}", 0.16, 0.22, BH - 0.6, (s * (BW / 2 + 0.08), BY - BD / 2 + 0.6 + i * (BD - 1.2) / 4, 0.4), shade(KANJUR, 0.04)))
        base.append(box(f"bpil{i}", 0.22, 0.16, BH - 0.6, (-BW / 2 + 0.6 + i * (BW - 1.2) / 4, BY + BD / 2 + 0.08, 0.4), shade(KANJUR, 0.04)))
    s = stair("stair", 1.2, BH, 2.4, 9, (0, 0, 0.15), "S", shade(KANJUR, -0.05))
    base.append(move(s, 0, fy - 1.2, 0))
    m.add(1, J(base, "base"), "base")
    z = 0.15 + BH
    top = [cylinder("drum", 2.7, 1.6, (0, BY, z), STUCCO, verts=24),
           pilasters_round("drum_pil", 2.7, z + 0.1, 1.4, 12, shade(STUCCO, -0.05), pw=0.25, proj=0.1, loc=(0, BY)),
           cylinder("drum_c", 2.85, 0.15, (0, BY, z + 1.45), shade(STUCCO, 0.04), verts=24),
           hemi("anda", 2.6, (0, BY, z + 1.6), STUCCO_W, 0.95, 24, 7)]
    h, z2 = harmika("harmika", 0, BY, z + 1.6 + 2.4, 1.0, STUCCO)
    top += [h, umbrellas("umb", 0, BY, z2, 3, 1.3, 0.75)]
    m.add(2, J(top, "dome"), "dome and umbrellas")
    return m


def apsidal_temple():
    """Footprint 40 x 70: the walled court with its steps and the apsidal temple (apse to the north)."""
    m = Model("apsidal-temple")
    m.add(0, ground("court", 40, 70, PAVE, 0.4), "court")
    cw = [banded("cw_w", 1.2, 70, 3.2, (-19.4, 0, 0), RUBBLE, shade(RUBBLE, 0.07), 1.1), banded("cw_e", 1.2, 70, 3.2, (19.4, 0, 0), RUBBLE, shade(RUBBLE, 0.07), 1.1),
          banded("cw_n", 40, 1.2, 3.2, (0, 34.4, 0), RUBBLE, shade(RUBBLE, 0.07), 1.1),
          banded("cw_sw", 15, 1.2, 3.2, (-12.5, -34.4, 0), RUBBLE, shade(RUBBLE, 0.07), 1.1), banded("cw_se", 15, 1.2, 3.2, (12.5, -34.4, 0), RUBBLE, shade(RUBBLE, 0.07), 1.1),
          box("gate_l", 1.4, 1.6, 4.4, (-5.3, -34.4, 0), KANJUR), box("gate_r", 1.4, 1.6, 4.4, (5.3, -34.4, 0), KANJUR)]
    s = stair("steps", 9.0, 0.4, 2.0, 3, (0, 0, 0), "S", shade(PAVE, -0.05))
    cw.append(move(s, 0, -36.0 + 1.0, 0))
    cw.append(box("path", 6, 30, 0.08, (0, -19, 0.4), shade(PAVE, -0.08)))
    m.add(0, J(cw, "court_walls"))
    # the temple: plinth, porch, nave, apse; barrel roof and half dome (porch front at y=-3, apse centre at y=24)
    PZ = 0.4 + 1.6
    t = [box("plinth", 18, 32, 1.6, (0, 10, 0.4), KANJUR), box("plinth_c", 18.4, 32.4, 0.25, (0, 10, 0.4 + 1.35), shade(KANJUR, 0.05)),
         cylinder("plinth_apse", 7.8, 1.6, (0, 24, 0.4), KANJUR, verts=28)]
    st = stair("tstair", 6, 1.6, 2.6, 6, (0, 0, 0.4), "S", shade(KANJUR, -0.05))
    t.append(move(st, 0, -6.0 - 1.3, 0))
    NW, NL, NH = 13.0, 24.0, 7.0
    t += [banded("nave", NW, NL, NH, (0, 12, PZ), PLAST, shade(PLAST, -0.05), 1.75),
          cylinder("apse", NW / 2, NH, (0, 24, PZ), PLAST, verts=28),
          box("porch_l", 1.6, 3.0, NH, (-NW / 2 + 0.8, -1.5, PZ), shade(PLAST, -0.04)),
          box("porch_r", 1.6, 3.0, NH, (NW / 2 - 0.8, -1.5, PZ), shade(PLAST, -0.04)),
          box("door", 2.6, 0.3, 4.0, (0, -0.1, PZ), DARK)]
    t += [column(f"pc{i}", x, -2.5, PZ, NH - 0.3, 0.38, "tuscan", KANJUR, 12) for i, x in enumerate((-2.6, 2.6))]
    roof = []
    v = half_cyl_y("vault", NW / 2 + 0.4, NL + 3.0, (0, 0, 0), ROOF, verts=20)
    roof.append(move(v, 0, 10.5, PZ + NH))
    roof.append(dome("apse_dome", NW / 2 + 0.4, (0, 24, PZ + NH), ROOF, squash=1.0, segments=20, rings=8))
    # the chaitya window: a horseshoe arch on the front gable
    roof.append(arch_panel("chaitya_f", 7.0, 7.4, (0, -3.05, PZ + NH - 1.4), "S", TIMBER, False, 0.25))
    roof.append(arch_panel("chaitya", 5.5, 6.5, (0, -3.2, PZ + NH - 1.2), "S", DARK, False, 0.3))
    roof.append(cylinder("finial", 0.3, 1.6, (0, 10, PZ + NH + NW / 2 + 0.2), GILT, verts=6))
    m.add(1, J(t, "temple"), "temple")
    m.add(2, J(roof, "roof"), "roof")
    vs = [votive(f"v{i}", 2.4, (x, y, 0.4), STUCCO) for i, (x, y) in enumerate([(-11, -26), (11, -26), (-11, -15), (11, -15), (-13, 29), (13, 29)])]
    vs += [flat_room(f"room{i}", 5, 6, 3.4, (sx * 15.8, y, 0.4), PLAST, door="E" if sx < 0 else "W") for i, (sx, y) in enumerate([(-1, 4), (1, 4), (-1, 14), (1, 14)])]
    m.add(3, J(vs, "court_shrines"), "court shrines")
    return m


def sirkap_block():
    """Footprint 40 x 60: a Sirkap block; the shop front on the south (turned east onto the main street on the map)."""
    m = Model("sirkap-block")
    m.add(0, ground("ground", 40, 60, GROUND), "ground")
    rng = random.Random(11)
    p = [box("lane_w", 3.5, 60, 0.1, (-18.2, 0, 0.3), PAVE), box("lane_e", 3.5, 60, 0.1, (18.2, 0, 0.3), PAVE), box("front", 40, 3.0, 0.1, (0, -28.5, 0.3), PAVE)]
    m.add(0, J(p, "lanes"))
    shops = []
    for k in range(7):
        x = -14.4 + k * 4.8
        shops.append(flat_room(f"shop{k}", 4.6, 6, 3.8, (x, -24, 0.3), PLAST if k % 2 else shade(PLAST, -0.05), door="S"))
        shops.append(box(f"awning{k}", 4.4, 1.4, 0.12, (x, -27.7, 2.9), TIMBER))
    m.add(1, J(shops, "shops"), "shops")
    houses = [court_house("h1", 16, 16, 5.2, (-8.2, -11, 0.3), PLAST, door="W", storey2=True),
              court_house("h2", 16, 18, 4.6, (8.2, -10, 0.3), RUBBLE, door="E"),
              court_house("h3", 20, 18, 5.0, (-6.2, 9, 0.3), DIAPER_B, door="W", storey2=True),
              court_house("h4", 32, 9, 4.2, (0, 24.5, 0.3), PLAST, door="N")]
    m.add(2, J(houses, "houses"), "houses")
    shrine = [box("shrine_court", 10, 16, 0.15, (11, 8, 0.3), PAVE), box("shrine_wall", 10, 0.6, 1.4, (11, 16.2, 0.3), RUBBLE),
              box("shrine_wall2", 0.6, 16, 1.4, (16.3, 8, 0.3), RUBBLE)]
    o, _ = gstupa("block_stupa", 4.2, (11, 9, 0.45), tiers=1, tier_h=1.4, umb=3, color=STUCCO, base_color=KANJUR, stair_face="W", verts=16)
    shrine.append(o)
    shrine.append(tree("pipal", 2.0, (12, 2.5, 0.3), "#6F8A5C"))
    m.add(3, J(shrine, "stupa court"), "stupa court")
    return m


def sirkap_palace():
    """Footprint 110 x 90: courts round an audience hall; the gate on the west, toward the main street."""
    m = Model("sirkap-palace")
    m.add(0, ground("ground", 110, 90, GROUND), "ground")
    outer = wall_run("enclosure", [(-54, -44), (54, -44), (54, 44), (-54, 44), (-54, -44)], 4.0, 1.4, color=RUBBLE, towers=False, merlon=None)
    m.add(0, outer, "enclosure")
    courts = [monastery("audience", 50, 44, 5.5, (-26, -18, 0), RUBBLE, shade(RUBBLE, 0.07), roofed=True, tank=False, door="W"),
              monastery("private", 46, 44, 5.0, (28, -18, 0), PLAST, shade(PLAST, -0.05), roofed=True, tank=True, door="W"),
              court_house("offices", 40, 34, 4.6, (-30, 24, 0), RUBBLE, door="S"),
              court_house("stores", 44, 34, 4.2, (26, 24, 0), shade(RUBBLE, 0.04), door="S", storey2=True)]
    m.add(1, J(courts, "courts"), "courts")
    hall = [box("hall", 26, 10, 8.0, (-26, 1, 0), PLAST), box("hall_roof", 27, 11, 0.5, (-26, 1, 8.0), ROOF),
            box("hall_par", 27.4, 11.4, 0.6, (-26, 1, 8.5), shade(ROOF, -0.1)), box("hall_door", 3.0, 0.3, 4.5, (-26, -4.1, 0), DARK)]
    hall += [column(f"hc{i}", -26 - 10 + i * 4, -6.0, 0, 6.0, 0.4, "ionic", KANJUR, 12) for i in range(6)]
    hall += [box("porch_roof", 24, 3.6, 0.5, (-26, -5.6, 6.0), ROOF)]
    gate = [banded("gate", 6, 12, 7.5, (-52, -18, 0), RUBBLE, shade(RUBBLE, 0.07), 1.25), box("gate_door", 0.4, 3.4, 4.5, (-55.0, -18, 0), DARK)]
    m.add(2, J(hall + gate, "hall"), "audience hall")
    return m


def hathial():
    """Footprint 110 x 80: a walled post on the rocky crest of the Hathial ridge (interpretation)."""
    m = Model("hathial")
    rock = [frustum("rock", 110, 80, 92, 62, 3.5, (0, 0, 0), ROCK), frustum("crest", 80, 56, 72, 50, 2.5, (3, 2, 3.5), ROCK_D)]
    rng = random.Random(3)
    for i in range(12):
        a = rng.uniform(0, math.tau)
        rock.append(dome(f"boulder{i}", rng.uniform(2, 4.5), (math.cos(a) * rng.uniform(40, 48), math.sin(a) * rng.uniform(28, 34), 0), ROCK_D, squash=0.6, segments=8, rings=4))
    m.add(0, J(rock, "rock"), "ridge")
    pts = [(-30, -20), (36, -20), (36, 24), (-30, 24), (-30, -20)]
    w = wall_run("wall", pts, 5.0, 2.2, (0, 0, 6.0), RUBBLE, towers=True, tower_r=3.0, tower_every=22, merlon="box", tower_shape="square")
    m.add(1, w, "walls")
    b = [flat_room("barrack1", 40, 7, 4.2, (2, 16, 6.0), RUBBLE, door="S"), flat_room("barrack2", 7, 26, 4.2, (-23, 0, 6.0), RUBBLE, door="E"),
         flat_room("store", 16, 9, 4.0, (22, -12, 6.0), PLAST, door="N"),
         banded("keep", 10, 10, 13, (12, 6, 6.0), RUBBLE, shade(RUBBLE, 0.07), 1.3), box("keep_roof", 10.6, 10.6, 0.5, (12, 6, 19.0), ROOF),
         box("gate", 5, 3, 0.1, (-30, 2, 6.0), DARK), box("gate_door", 0.4, 3, 3.4, (-31.2, 2, 6.0), DARK)]
    for k in range(4):
        b.append(box(f"keep_slit{k}", 0.3, 0.2, 1.4, (8 + k * 2.6, 0.9, 13), DARK))
    m.add(2, J(b, "buildings"), "citadel")
    path = [box(f"path{i}", 3, 6, 0.2, (-40 + i * 3, -30 + i * 4.5, i * 0.9), shade(ROCK, 0.08)) for i in range(5)]
    m.add(2, J(path, "path"))
    return m


# ================================================================ Jandial

def jandial(ruined=False):
    """Footprint 28 x 50: the Greek-plan temple at Jandial, front to the south. Plinth, outer wall with windows,
    Ionic columns in antis at front and back, pronaos, naos, a solid block with a (conjectural) tower, tiled roof."""
    m = Model("jandial")
    m.add(0, ground("ground", 34, 56, GROUND), "ground")
    # the temenos: a low wall with piers round the paved court, open at the front
    tem = [box("court", 33, 55, 0.12, (0, 0, 0.3), PAVE)]
    for nm, (w, d, x, y) in {"n": (32.4, 0.7, 0, 27.2), "w": (0.7, 54.4, -16.2, 0), "e": (0.7, 54.4, 16.2, 0),
                             "sw": (11, 0.7, -10.7, -27.2), "se": (11, 0.7, 10.7, -27.2)}.items():
        tem.append(box("tw_" + nm, w, d, 1.1, (x, y, 0), shade(KANJUR, -0.08)))
        tem.append(box("tc_" + nm, w + 0.2, d + 0.2, 0.15, (x, y, 1.1), shade(KANJUR, 0.02)))
        L = max(w, d)
        for k in range(int(L / 3) + 1):
            t = -L / 2 + k * L / int(L / 3)
            px, py = (x + t, y) if w > d else (x, y + t)
            tem.append(box(f"tp_{nm}{k}", 0.9, 0.9, 1.5, (px, py, 0), shade(KANJUR, -0.04)))
    for k, (tx, ty) in enumerate([(-15, 24), (15, 24), (-15, -10), (15, -10)]):
        tem.append(tree(f"tree{k}", 1.4, (tx, ty, 0.3), "#6F8A5C", kind="cypress"))
    m.add(0, J(tem, "temenos"))
    PZ = 1.9
    plinth = [banded("plinth", 26, 46, PZ - 0.25, (0, 1.5, 0), KANJUR, shade(KANJUR, -0.05), band=0.4), box("plinth_m", 26.4, 46.4, 0.35, (0, 1.5, 0), shade(KANJUR, -0.07)),
              box("plinth_c", 26.5, 46.5, 0.25, (0, 1.5, PZ - 0.25), shade(KANJUR, 0.05))]
    st = stair("steps", 13, PZ, 3.4, 8, (0, 0, 0), "S", shade(KANJUR, -0.04))
    plinth.append(move(st, 0, -21.5 - 1.7, 0))
    m.add(0, J(plinth, "plinth"), "plinth")
    H = 7.2
    x0, x1, y0, y1 = -12.2, 12.2, -21.0, 23.8
    walls = [banded("side_w", 1.2, y1 - y0, H, (-12.2 + 0.6, (y0 + y1) / 2, PZ), KANJUR, shade(KANJUR, -0.05), 1.2),
             banded("side_e", 1.2, y1 - y0, H, (12.2 - 0.6, (y0 + y1) / 2, PZ), KANJUR, shade(KANJUR, -0.05), 1.2)]
    for s in (-1, 1):
        for yy, nm in ((y0 + 0.6, "f"), (y1 - 0.6, "b")):
            walls.append(banded(f"anta_{nm}{s}", 5.6, 1.2, H, (s * 9.4, yy, PZ), KANJUR, shade(KANJUR, -0.05), 1.2))
        for k in range(7):
            yy = y0 + 4 + k * (y1 - y0 - 8) / 6
            walls.append(box(f"win{s}{k}", 0.25, 1.3, 2.2, (s * 12.25, yy, PZ + 3.4), DARK))
    # inner temple: pronaos walls, naos, solid tower block, back porch
    walls += [banded("in_w", 1.0, 30, H, (-7.0, 1.5, PZ), PLAST, shade(PLAST, -0.05), 1.2), banded("in_e", 1.0, 30, H, (7.0, 1.5, PZ), PLAST, shade(PLAST, -0.05), 1.2),
              box("naos_front", 13, 1.0, H, (0, -6.5, PZ), PLAST), box("naos_door", 3.0, 0.3, 4.6, (0, -7.05, PZ), DARK),
              box("naos_floor", 13, 12, 0.1, (0, 0, PZ), PAVE)]
    TB = 10.0
    walls.append(banded("tower_base", 13, 8.5, H, (0, 10.3, PZ), DIAPER_A, DIAPER_B, 1.2))
    cols = []
    for i, x in enumerate((-3.4, 3.4)):
        cols.append(column(f"cf{i}", x, y0 + 0.6, PZ, H, 0.5, "ionic", KANJUR, 32))
        cols.append(column(f"cb{i}", x, y1 - 0.6, PZ, H, 0.5, "ionic", KANJUR, 32))
        cols.append(column(f"pf{i}", x, -14.0, PZ, H, 0.48, "ionic", KANJUR, 32))
        cols.append(column(f"pb{i}", x, 17.6, PZ, H, 0.48, "ionic", KANJUR, 32))
    for s in (-1, 1):
        for k in range(7):
            yy = y0 + 4 + k * (y1 - y0 - 8) / 6
            cols.append(box(f"sill{s}{k}", 0.35, 1.7, 0.2, (s * 12.3, yy, PZ + 3.2), shade(KANJUR, 0.06)))
            cols.append(box(f"lint{s}{k}", 0.35, 1.7, 0.25, (s * 12.3, yy, PZ + 5.6), shade(KANJUR, 0.06)))
            for b in range(3):
                cols.append(box(f"grille{s}{k}{b}", 0.12, 0.1, 2.2, (s * 12.36, yy - 0.4 + b * 0.4, PZ + 3.4), shade(KANJUR, -0.1)))
    temple = J(walls + cols, "temple")
    if ruined:
        ruinify([temple], cut=PZ + 2.5, keep=0.3, seed=0.9, floor=PZ)
    m.add(1, temple, "walls and columns")
    top = []
    if not ruined:
        top.append(entablature("ent", -12.2, 12.2, -21.0, 23.8, PZ + H, 1.5, KANJUR, dentils=True))
        top.append(pediment("roof", 25.6, 46.0, PZ + H + 1.5, 3.6, -22.2, KANJUR, TILE, ridges=True, statues=False))
        # back gable: a second plain pediment face
        tz = PZ + H + 1.5
        for s in (-1, 1):
            for k in range(24):
                yy = -22.6 + k * 47.0 / 23
                top.append(box(f"antefix{s}{k}", 0.25, 0.5, 0.55, (s * 13.25, yy, tz - 0.05), shade(KANJUR, 0.04)))
        for k in range(3):
            top.append(box(f"acro{k}", 0.8, 0.5, 1.1, ((k - 1) * 12.6, -22.6, tz + (3.6 if k == 1 else 0.1)), shade(KANJUR, 0.04)))
        top.append(move(pilasters_sq("tower_pil", 9.0, 7.0, tz + 0.3, 9.8, shade(KANJUR, 0.03), every=1.5, pw=0.4, proj=0.2), 0, 10.3, 0))
        top += [banded("tower", 9.0, 7.0, 10.5, (0, 10.3, tz), DIAPER_A, DIAPER_B, 1.3),
                box("tower_c", 9.8, 7.8, 0.5, (0, 10.3, tz + 10.5), shade(KANJUR, 0.05)),
                box("tower_t", 7.0, 5.0, 1.4, (0, 10.3, tz + 11.0), KANJUR),
                box("tower_t2", 4.0, 3.0, 1.0, (0, 10.3, tz + 12.4), KANJUR)]
        for s in (-1, 1):
            for k in range(2):
                top.append(box(f"tw_win{s}{k}", 0.25, 1.2, 1.8, (s * 4.55, 9.3 + k * 2.2, tz + 6.0), DARK))
        top.append(box("tw_winS", 1.2, 0.25, 1.8, (0, 6.75, tz + 6.0), DARK))
        m.add(2, J(top, "roof"), "roof and tower")
    else:
        rng = random.Random(5)
        for k in range(10):
            x, y = rng.uniform(-11, 11), rng.uniform(-20, 22)
            top.append(box(f"drum{k}", 2.2, 1.0, 1.0, (x, y, PZ), KANJUR, rot_z=rng.uniform(0, 3)))
        m.add(2, J(top, "debris"), "fallen columns")
    return m


# ================================================================ Kunala, Bhir, Sirsukh, Mohra Moradu

def kunala(ruined=False):
    """Footprint 46 x 64: the stupa on three terraces on the ridge, a small monastery to the north."""
    m = Model("kunala")
    m.add(0, J([frustum("ridge", 46, 64, 40, 58, 1.5, (0, 0, 0), ROCK), box("pave", 32, 34, 0.2, (0, -13, 1.5), PAVE)], "ridge"), "ridge")
    o, ztop = gstupa("stupa", 22, (0, -12, 1.7), tiers=3, tier_h=2.5, drum_r=5.6, drum_h=3.4, dome_r=5.4, umb=0 if ruined else 6,
                     color=STUCCO, base_color=KANJUR, stair_face="S", top=not ruined, verts=28)
    if ruined:
        ruinify([o], cut=8.0, keep=0.35, seed=0.3, floor=1.7)
    m.add(1, o, "stupa")
    mon = monastery("vihara", 34, 22, 4.0, (0, 19, 1.5), DIAPER_A, DIAPER_B, roofed=not ruined, tank=False, door="S")
    if ruined:
        ruinify([mon], cut=3.2, keep=0.3, seed=1.7, floor=1.5)
    m.add(2, mon, "monastery")
    vs = [votive(f"v{i}", 2.4, (x, y, 1.7), STUCCO, umb=0 if ruined else 2) for i, (x, y) in enumerate([(-13, -27), (13, -27), (-15, 0), (15, 0)])]
    if ruined:
        ruinify(vs, cut=2.5, keep=0.3)
    m.add(2, J(vs, "votives"))
    return m


def bhir_quarter():
    """Footprint 90 x 80: a stretch of First Street on the Bhir Mound with the irregular rubble houses on either side."""
    m = Model("bhir-quarter")
    m.add(0, ground("ground", 90, 80, shade(GROUND, -0.03)), "ground")
    street = [(-4, -38.4), (-2, -22), (-5, -4), (-1, 14), (-3, 38.4)]
    st = []
    for i, ((ax, ay), (bx, by)) in enumerate(zip(street, street[1:])):
        L = math.hypot(bx - ax, by - ay)
        st.append(box(f"st{i}", 6.5, L + 3, 0.1, ((ax + bx) / 2, (ay + by) / 2, 0.3), PAVE, rot_z=-math.atan2(bx - ax, by - ay)))
    lane = [(-4, 4), (-20, 2), (-32, 7), (-43.4, 5)]
    for i, ((ax, ay), (bx, by)) in enumerate(zip(lane, lane[1:])):
        L = math.hypot(bx - ax, by - ay)
        st.append(box(f"ln{i}", L + 2, 3.5, 0.1, ((ax + bx) / 2, (ay + by) / 2, 0.3), PAVE, rot_z=math.atan2(by - ay, bx - ax)))
    m.add(0, J(st, "streets"))

    def street_x(y):
        for (ax, ay), (bx, by) in zip(street, street[1:]):
            if ay <= y <= by:
                return ax + (bx - ax) * (y - ay) / (by - ay)
        return street[-1][0]

    rng = random.Random(21)
    houses, yards = [], []
    for side in (-1, 1):
        y = -38.0
        while y < 37:
            d = rng.uniform(8, 13)
            if side < 0 and y < 8 and y + d > 1:      # leave the cross-lane open
                y = 8.0
                continue
            yc = min(y + d / 2, 38 - d / 2)
            sx = street_x(yc) + side * 3.6
            depth = 44 - abs(sx) if side < 0 else 44 - abs(sx)
            w_front = rng.uniform(8, 14)
            # front range (shops), back rooms, a yard between
            x_front = sx + side * w_front / 2
            hh = rng.uniform(3.6, 6.4)
            col = rng.choice([RUBBLE, RUBBLE, PLAST, shade(RUBBLE, -0.05), MUD])
            houses.append(flat_room(f"f{side}_{int(y)}", w_front, d - 1.2, hh, (x_front, yc, 0.3), col, door="E" if side < 0 else "W"))
            xb = sx + side * (w_front + rng.uniform(4, 7))
            wb = min(rng.uniform(8, 16), depth - abs(xb - sx) - 1)
            if wb > 4:
                houses.append(flat_room(f"b{side}_{int(y)}", wb, d - 1.2, hh * rng.uniform(0.8, 1.15), (xb + side * wb / 2, yc, 0.3), shade(col, 0.03), door="N" if rng.random() < 0.5 else "S"))
                yx = (sx + side * w_front + xb) / 2
                yw = abs(xb - (sx + side * w_front))
                yards.append(box(f"yard{side}_{int(y)}", yw, d - 2, 0.12, (yx, yc, 0.3), PAVE))
                yards.append(box(f"wallY{side}_{int(y)}", yw, 0.6, 2.0, (yx, yc - d / 2 + 0.9, 0.3), shade(col, -0.05)))
                if rng.random() < 0.6:
                    yards.append(cylinder(f"soak{side}_{int(y)}", 0.6, 0.5, (yx, yc + 1.0, 0.3), shade(MUD, -0.1), verts=10))
                    yards.append(cylinder(f"soakw{side}_{int(y)}", 0.4, 0.52, (yx, yc + 1.0, 0.3), DARK, verts=10))
                if rng.random() < 0.5:
                    yards.append(cylinder(f"jar{side}_{int(y)}", 0.45, 0.9, (yx - side * 1.5, yc - 1.5, 0.3), "#A8643F", verts=8, r_top=0.3))
            y += d
    m.add(1, J(houses, "houses"), "houses")
    m.add(2, J(yards, "yards"), "yards and soak-wells")
    well = [cylinder("well", 1.4, 0.9, (-12, 5.5, 0.3), RUBBLE, verts=14), cylinder("well_w", 1.0, 0.92, (-12, 5.5, 0.3), WATER, verts=14),
            box("well_post1", 0.2, 0.2, 2.4, (-13.3, 5.5, 0.3), TIMBER), box("well_post2", 0.2, 0.2, 2.4, (-10.7, 5.5, 0.3), TIMBER),
            box("well_beam", 2.8, 0.2, 0.2, (-12, 5.5, 2.6), TIMBER), tree("neem", 2.8, (-24, 3.5, 0.3), "#6F8A5C")]
    m.add(2, J(well, "well"), "well")
    return m


def sirsukh_wall():
    """Footprint 260 x 44: the south wall of Sirsukh in diaper masonry with semicircular bastions, outer face to the south."""
    m = Model("sirsukh-wall")
    m.add(0, ground("ground", 260, 44, GROUND), "ground")
    WY, T, H = -6.0, 6.0, 9.0
    wall = [frustum("plinth", 260, T + 2.4, 260, T, 1.8, (0, WY, 0), shade(DIAPER_A, -0.06))]
    wall.append(banded("wall", 260, T, H - 1.8, (0, WY, 1.8), DIAPER_A, DIAPER_B, band=1.15))
    bast = []
    xs = [-121.5 + k * 27 for k in range(10)]
    for i, bx in enumerate(xs):
        bast.append(lathe(f"bplinth{i}", [(7.4, 0), (6.6, 1.8)], (bx, WY - T / 2, 0), shade(DIAPER_A, -0.06), verts=20))
        bast.append(banded_cyl(f"bast{i}", 6.6, H + 1.4 - 1.8, (bx, WY - T / 2, 1.8), DIAPER_A, DIAPER_B, band=1.15, verts=20))
        for k in range(5):
            a = math.pi + math.pi * (k + 0.5) / 5
            bast.append(box(f"slit{i}_{k}", 0.25, 0.3, 1.6, (bx + 6.65 * math.cos(a), WY - T / 2 + 6.65 * math.sin(a), 3.4), DARK, rot_z=a + math.pi / 2))
    mer = []
    n = int(260 / 2.5)
    for k in range(n):
        mx = -130 + (k + 0.5) * 260 / n
        if any(abs(mx - bx) < 6.8 for bx in xs):
            continue
        mer.append(box(f"m{k}", 1.3, 1.0, 1.3, (mx, WY - T / 2 + 0.5, H), DIAPER_B))
        if k % 3 == 1:
            mer.append(box(f"ls{k}", 0.25, 0.3, 1.4, (mx + 1.25, WY - T / 2 - 0.05, 4.5), DARK))
    for i, bx in enumerate(xs):
        for k in range(9):
            a = math.pi + math.pi * k / 8
            mer.append(box(f"bm{i}_{k}", 1.3, 0.9, 1.3, (bx + 6.0 * math.cos(a), WY - T / 2 + 6.0 * math.sin(a), H + 1.4), DIAPER_B, rot_z=a + math.pi / 2))
        mer.append(box(f"bfloor{i}", 9, 4, 0.2, (bx, WY - T / 2 - 2.5, H + 1.4), shade(DIAPER_A, -0.05)))
    m.add(1, J(wall, "wall"), "wall")
    m.add(2, J(bast + mer, "bastions"), "bastions and battlements")
    town = [box("intervallum", 258, 5, 0.1, (0, 2.5, 0), PAVE)]
    for k in range(6):
        sx = -110 + k * 40
        town.append(stair(f"ramp{k}", 2.2, H, 9, 14, (0, 0, 0), "E", shade(DIAPER_A, -0.03)))
        town[-1] = move(town[-1], sx + 4.5, WY + T / 2 + 1.2, 0)
    rng = random.Random(8)
    x = -126
    while x < 112:
        w = min(rng.uniform(12, 20), 128 - x)
        town.append(court_house(f"h{int(x)}", w, 15, rng.uniform(4.2, 5.8), (x + w / 2, 13.0, 0), rng.choice([PLAST, DIAPER_B, STUCCO]), door="S", storey2=rng.random() < 0.3))
        x += w + rng.uniform(2.5, 5)
    m.add(3, J(town, "town"), "houses inside")
    return m


def mohra_moradu(ruined=False):
    """Footprint 70 x 100: the stupa court to the south, the monastery square to the north, an assembly hall to the east."""
    m = Model("mohra-moradu")
    m.add(0, J([frustum("terrace", 70, 100, 66, 96, 1.2, (0, 0, 0), shade(GROUND, -0.05)), box("stupa_court", 46, 40, 0.15, (-4, -27, 1.2), PAVE)], "terrace"), "terrace")
    cw = [banded("cw_s1", 18, 1.2, 3.0, (-18, -46.4, 1.2), DIAPER_A, DIAPER_B, 1.0), banded("cw_s2", 18, 1.2, 3.0, (10, -46.4, 1.2), DIAPER_A, DIAPER_B, 1.0),
          banded("cw_w", 1.2, 40, 3.0, (-26.4, -27, 1.2), DIAPER_A, DIAPER_B, 1.0), banded("cw_e", 1.2, 40, 3.0, (18.4, -27, 1.2), DIAPER_A, DIAPER_B, 1.0)]
    st = stair("entry", 8, 1.2, 3, 4, (0, 0, 0), "S", shade(DIAPER_A, -0.05))
    cw.append(move(st, -4, -48.5, 0))
    m.add(0, J(cw, "court_wall"))
    o, _ = gstupa("stupa", 14.5, (-4, -26, 1.35), tiers=2, tier_h=2.6, drum_r=4.6, drum_h=3.0, dome_r=4.5, umb=0 if ruined else 7, color=STUCCO, base_color=STUCCO,
                  stair_face="S", niches=6, top=not ruined, verts=24, fig_color=STUCCO_W)
    # paint: a red band and gilded halo line on the base, as traces at Mohra Moradu suggest
    band = box("paint", 14.9, 14.9, 0.25, (-4, -26, 1.35 + 2.0), RED)
    if ruined:
        ruinify([o], cut=7.5, keep=0.35, seed=0.8, floor=1.35)
    m.add(1, J([o, band], "stupa"), "main stupa")
    vs = [votive(f"v{i}", 3.0, (x, y, 1.35), STUCCO, umb=0 if ruined else 3) for i, (x, y) in enumerate([(-20, -38), (12, -38), (-20, -14), (12, -14), (-20, -26), (12, -26)])]
    if ruined:
        ruinify(vs, cut=2.0, keep=0.3)
    m.add(2, J(vs, "votives"), "votive stupas")
    mon = [monastery("vihara", 44, 44, 4.6, (-6, 24, 1.2), DIAPER_A, DIAPER_B, cells_per_side=7, storeys=1 if ruined else 2, roofed=not ruined, tank=True, door="S"),
           banded("hall", 14, 20, 5.0, (25, 28, 1.2), DIAPER_A, DIAPER_B, 1.25), banded("kitchen", 14, 12, 4.2, (25, 10, 1.2), DIAPER_A, DIAPER_B, 1.05)]
    if not ruined:
        mon += [box("hall_roof", 14.6, 20.6, 0.4, (25, 28, 6.2), ROOF), box("kit_roof", 14.6, 12.6, 0.4, (25, 10, 5.4), ROOF),
                box("hall_door", 0.3, 2.0, 2.8, (17.9, 28, 1.2), DARK), cylinder("chimney", 0.6, 1.6, (28, 12, 5.4), shade(ROOF, -0.1), verts=8)]
        trees = [tree(f"t{i}", 3.0, (x, y, 1.2), "#6F8A5C") for i, (x, y) in enumerate([(26, -40), (28, -10), (-30, 0), (-30, 45)])]
        mon += trees
    else:
        ruinify(mon, cut=2.4, keep=0.3, seed=1.9, floor=1.2)
        for i, (x, y) in enumerate([(-10, 22), (2, 30), (-16, 12), (24, 26), (-6, -20)]):
            mon.append(box(f"ash{i}", 5, 4, 0.12, (x, y, 1.3), ASH))
    m.add(3, J(mon, "monastery"), "monastery")
    return m


BUILDERS = {
    "taxila/dharmarajika": lambda: dharmarajika("kushan"),
    "taxila/dharmarajika-early": lambda: dharmarajika("early"),
    "taxila/dharmarajika-ig": lambda: dharmarajika("ig"),
    "taxila/dharmarajika-ruin": lambda: dharmarajika("ruin"),
    "taxila/sirkap-wall": lambda: sirkap_wall(False),
    "taxila/sirkap-wall-ruin": lambda: sirkap_wall(True),
    "taxila/eagle-shrine": eagle_shrine,
    "taxila/apsidal-temple": apsidal_temple,
    "taxila/sirkap-block": sirkap_block,
    "taxila/sirkap-palace": sirkap_palace,
    "taxila/hathial": hathial,
    "taxila/jandial": lambda: jandial(False),
    "taxila/jandial-ruin": lambda: jandial(True),
    "taxila/kunala": lambda: kunala(False),
    "taxila/kunala-ruin": lambda: kunala(True),
    "taxila/bhir-quarter": bhir_quarter,
    "taxila/sirsukh-wall": sirsukh_wall,
    "taxila/mohra-moradu": lambda: mohra_moradu(False),
    "taxila/mohra-moradu-ruin": lambda: mohra_moradu(True),
}
