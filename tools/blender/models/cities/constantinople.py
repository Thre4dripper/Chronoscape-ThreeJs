"""Constantinople landmark miniatures: Byzantine churches and palaces, the walls, Ottoman mosques and Topkapı."""
import math
import bpy
from chronokit import Model, box, cylinder, dome, join, shade, gable_roof, hip_roof, steps, columns, mesh_from, ring_extrude, ellipse_ring, stadium_ring, stadium_pts, obelisk
from worldkit import *

# ---------------------------------------------------------------- palette
BRICK_B = "#AE6A4E"       # Byzantine brick
STONE_B = "#D3C3A1"       # limestone bands and ashlar
WALL_STONE = "#C9B894"    # land-wall limestone
HS_WALL = "#D6AE88"       # Hagia Sophia's ochre render
OTT_STONE = "#DDD4C2"     # Ottoman cut limestone
PAVE = "#CDBF9F"
SAND_C = "#D6C49A"
GRASS = "#8E9D69"
PORPHYRY = "#7A3A3E"
BRONZE_ROOF = "#9C8150"
TILE_B = "#AE6342"
CYPRESS = "#4F6B45"


# ---------------------------------------------------------------- parts
def plate(name, w, d, color=PAVE, h=0.4):
    return box(name, w, d, h, (0, 0, 0), color)


def half_dome(name, r, loc=(0, 0, 0), face="N", color=LEAD, rise=1.0, seg=12, rings=5):
    """A quarter sphere (semi-dome, apse conch) open toward the building, its curve facing `face`."""
    verts, faces = [], []
    n = seg + 1
    for i in range(rings):
        phi = (math.pi / 2) * i / rings
        for j in range(n):
            az = -math.pi / 2 + math.pi * j / seg
            verts.append((r * math.cos(phi) * math.sin(az), r * math.cos(phi) * math.cos(az), r * rise * math.sin(phi)))
    apex = len(verts)
    verts.append((0, 0, r * rise))
    for i in range(rings - 1):
        for j in range(seg):
            a = i * n + j
            faces.append((a, a + 1, a + n + 1, a + n))
    top = (rings - 1) * n
    for j in range(seg):
        faces.append((top + j, top + j + 1, apex))
    back = [i * n for i in range(rings)] + [apex] + [i * n + seg for i in range(rings - 1, -1, -1)]
    faces.append(tuple(back))
    faces.append(tuple(range(n)))
    o = mesh_from(name, verts, faces, (0, 0, 0), color)
    o = rot(o, {"N": 0, "S": 180, "E": -90, "W": 90}[face])
    return move(o, *loc)


def half_cylinder(name, r, h, loc=(0, 0, 0), face="N", color=BRICK_B, seg=10):
    """An apse wall: half a cylinder bulging toward `face`."""
    pts = [(r * math.sin(-math.pi / 2 + math.pi * j / seg), r * math.cos(-math.pi / 2 + math.pi * j / seg)) for j in range(seg + 1)]
    o = prism(name, pts[::-1], h, (0, 0, 0), color)
    o = rot(o, {"N": 0, "S": 180, "E": -90, "W": 90}[face])
    return move(o, *loc)


def apse(name, r, h, loc, face="N", color=BRICK_B, roof=LEAD):
    x, y, z = loc
    return join([half_cylinder(name + "_w", r, h, (x, y, z), face, color), half_dome(name + "_c", r * 1.04, (x, y, z + h), face, roof, rise=0.55, seg=10, rings=4)], name)


def barrel(name, w, length, loc=(0, 0, 0), axis="Y", color=LEAD, seg=8, rise=0.8):
    """A half-cylinder vault roof of span w running along `axis`."""
    pts = [(w / 2 * math.cos(math.pi * i / seg), w / 2 * math.sin(math.pi * i / seg) * rise) for i in range(seg + 1)]
    verts = [(px, -length / 2, pz) for px, pz in pts] + [(px, length / 2, pz) for px, pz in pts]
    n = len(pts)
    faces = [tuple(range(n)), tuple(range(2 * n - 1, n - 1, -1))] + [(i, i + 1, n + i + 1, n + i) for i in range(n - 1)] + [(0, n, 2 * n - 1, n - 1)]
    o = mesh_from(name, verts, faces, (0, 0, 0), color)
    if axis == "X":
        o = rot(o, 90)
    return move(o, *loc)


def ring_panels(name, r, n, w, h, loc, color=DARK, offset=0.0):
    """Dark window panels set tangentially round a drum of radius r."""
    x, y, z = loc
    out = []
    for i in range(n):
        a = math.tau * (i + offset) / n
        out.append(box(f"{name}{i}", w, 0.3, h, (x + (r + 0.05) * math.cos(a), y + (r + 0.05) * math.sin(a), z), color, rot_z=a + math.pi / 2))
    return join(out, name)


def ring_boxes(name, r, n, w, d, h, loc, color, offset=0.5):
    x, y, z = loc
    out = []
    for i in range(n):
        a = math.tau * (i + offset) / n
        out.append(box(f"{name}{i}", w, d, h, (x + r * math.cos(a), y + r * math.sin(a), z), color, rot_z=a + math.pi / 2))
    return join(out, name)


def byz_dome(name, r, loc, drum_h=None, sides=12, wall=BRICK_B, roof=LEAD, rise=0.75):
    """A Middle Byzantine dome: a tall polygonal drum with arched windows and a lead dome with a scalloped eave."""
    x, y, z = loc
    dh = drum_h if drum_h is not None else r * 1.2
    parts = [cylinder(name + "_drum", r, dh, (x, y, z), wall, verts=sides)]
    for i in range(sides):
        a = math.tau * (i + 0.5) / sides
        parts.append(arch_panel(f"{name}_w{i}", r * 0.38, dh * 0.62, (0, 0, 0), "S", DARK, False, 0.25))
        parts[-1] = rot(parts[-1], math.degrees(a) + 90)
        parts[-1] = move(parts[-1], x + r * math.cos(a) * 0.97, y + r * math.sin(a) * 0.97, z + dh * 0.18)
    parts.append(cylinder(name + "_eave", r * 1.06, r * 0.08, (x, y, z + dh), roof, verts=sides))
    parts.append(shallow_dome(name + "_d", r * 1.02, (x, y, z + dh + r * 0.08), roof, rise=rise))
    parts.append(cylinder(name + "_cross", r * 0.04, r * 0.4, (x, y, z + dh + r * 0.08 + r * 1.02 * rise - 0.1), GILT, verts=4))
    return join(parts, name)


def cross_in_square(name, w, d, h, loc=(0, 0, 0), wall=BRICK_B, roof=LEAD, dome_r=None, drum_h=None, narthex=True, side_domes=False):
    """A Middle Byzantine church facing west (entrance -Y, apse +Y): a square naos with a raised cross of barrel
    roofs, a domed drum over the crossing, three apses and a narthex."""
    x, y, z = loc
    r = dome_r or w * 0.2
    arm = w * 0.36
    parts = [box(name + "_core", w, d, h * 0.72, (x, y, z), wall)]
    parts.append(box(name + "_armx", w, arm, h, (x, y, z), wall))
    parts.append(box(name + "_army", arm, d, h, (x, y, z), wall))
    parts.append(barrel(name + "_bx", arm * 1.06, w + 0.4, (x, y, z + h), "X", roof))
    parts.append(barrel(name + "_by", arm * 1.06, d + 0.4, (x, y, z + h), "Y", roof))
    for sx in (-1, 1):
        for sy in (-1, 1):
            parts.append(box(f"{name}_cr{sx}{sy}", (w - arm) / 2 + 0.2, (d - arm) / 2 + 0.2, 0.5, (x + sx * (arm / 2 + (w - arm) / 4), y + sy * (arm / 2 + (d - arm) / 4), z + h * 0.72), roof))
            if side_domes:
                parts.append(shallow_dome(f"{name}_sd{sx}{sy}", r * 0.45, (x + sx * w * 0.32, y + sy * d * 0.32, z + h * 0.72 + 0.5), roof, rise=0.6))
    parts.append(byz_dome(name + "_dome", r, (x, y, z + h + arm * 0.35), drum_h, wall=wall, roof=roof))
    parts.append(apse(name + "_apse", arm * 0.45, h * 0.75, (x, y + d / 2, z), "N", wall, roof))
    for s in (-1, 1):
        parts.append(apse(f"{name}_pas{s}", arm * 0.3, h * 0.5, (x + s * w * 0.34, y + d / 2, z), "N", wall, roof))
    for s in (-1, 1):
        parts.append(arcade(f"{name}_win{s}", arm * 0.7, h * 0.3, 3, (x + s * (w / 2 + 0.05), y, z + h * 0.48), "E" if s > 0 else "W", DARK, False, 0.6))
    parts.append(arch_panel(name + "_wwin", arm * 0.5, h * 0.3, (x, y - d / 2 - 0.05, z + h * 0.5), "S", DARK, False))
    if narthex:
        nd = d * 0.22
        parts.append(box(name + "_nar", w, nd, h * 0.6, (x, y - d / 2 - nd / 2, z), wall))
        parts.append(box(name + "_narr", w + 0.4, nd + 0.4, 0.5, (x, y - d / 2 - nd / 2, z + h * 0.6), roof))
        parts.append(arcade(name + "_nara", w * 0.8, h * 0.4, 3, (x, y - d / 2 - nd - 0.05, z), "S", DARK, False, 0.55))
    return join(parts, name)


def basilica(name, L, W, h, loc=(0, 0, 0), wall=BRICK_B, roof=TILE_B, atrium=0.0):
    """An Early Christian basilica facing west (-Y): a tall nave with a clerestory, lower aisles, an apse, an atrium in front."""
    x, y, z = loc
    nave_w, aisle_w = W * 0.46, W * 0.27
    parts = [box(name + "_nave", nave_w, L, h, (x, y, z), wall), gable_roof(name + "_nroof", nave_w, L, nave_w * 0.32, (x, y, z + h), roof, overhang=0.4)]
    for s in (-1, 1):
        ax = x + s * (nave_w / 2 + aisle_w / 2)
        parts.append(box(f"{name}_aisle{s}", aisle_w, L, h * 0.58, (ax, y, z), wall))
        parts.append(box(f"{name}_aroof{s}", aisle_w + 0.4, L + 0.4, 0.5, (ax, y, z + h * 0.58), roof))
        parts.append(arcade(f"{name}_clere{s}", L * 0.86, h * 0.26, max(4, int(L / 5)), (x + s * (nave_w / 2 + 0.05), y, z + h * 0.64), "E" if s > 0 else "W", DARK, False, 0.5))
        parts.append(arcade(f"{name}_aw{s}", L * 0.86, h * 0.26, max(4, int(L / 5)), (x + s * (W / 2 + 0.05), y, z + h * 0.15), "E" if s > 0 else "W", DARK, False, 0.4))
    parts.append(apse(name + "_apse", nave_w * 0.48, h * 0.75, (x, y + L / 2, z), "N", wall, roof))
    parts.append(arcade(name + "_front", nave_w * 0.8, h * 0.3, 3, (x, y - L / 2 - 0.05, z), "S", DARK, False, 0.6))
    if atrium:
        parts.append(courtyard_ring(name + "_atr", W, atrium, h * 0.4, 4.0, (x, y - L / 2 - atrium / 2, z), wall, DARK))
    return join(parts, name)


def ottoman_minaret(name, r, h, loc=(0, 0, 0), balconies=2, color=OTT_STONE, cap=LEAD):
    """A pencil minaret: square base, 16-sided shaft, corbelled balconies (serefe) and a tall lead cone with a gilt finial."""
    x, y, z = loc
    base_h = h * 0.1
    parts = [box(name + "_base", r * 2.5, r * 2.5, base_h, (x, y, z), color)]
    parts.append(cylinder(name + "_tr", r * 1.25, base_h * 0.4, (x, y, z + base_h), color, verts=16, r_top=r))
    shaft0 = z + base_h * 1.4
    top = z + h
    parts.append(cylinder(name + "_shaft", r, top - shaft0, (x, y, shaft0), color, verts=16, r_top=r * 0.88))
    for i in range(balconies):
        t = shaft0 + (top - shaft0) * (0.55 + 0.38 * i / max(1, balconies - 1) if balconies > 1 else 0.82)
        parts.append(cylinder(f"{name}_cor{i}", r * 0.95, r * 0.6, (x, y, t - r * 0.6), color, verts=16, r_top=r * 1.5))
        parts.append(cylinder(f"{name}_bal{i}", r * 1.55, r * 0.55, (x, y, t), shade(color, -0.06), verts=16))
    parts.append(cylinder(name + "_cap", r * 1.02, r * 5.2, (x, y, top), cap, verts=16, r_top=0.0))
    parts.append(cylinder(name + "_alem", r * 0.08, r * 1.2, (x, y, top + r * 5.0), GILT, verts=6))
    return join(parts, name)


def lead_dome(name, r, loc, drum_h=0.0, wall=OTT_STONE, roof=LEAD, rise=0.62, windows=0, finial=True):
    """An Ottoman dome: an optional drum ringed by windows, a lead-sheeted dome and a gilt alem."""
    x, y, z = loc
    parts = []
    if drum_h:
        parts.append(cylinder(name + "_drum", r * 1.02, drum_h, (x, y, z), wall, verts=max(16, windows or 16)))
        if windows:
            parts.append(ring_panels(name + "_win", r * 1.02, windows, r * 2 * math.pi / windows * 0.45, drum_h * 0.6, (x, y, z + drum_h * 0.2)))
    parts.append(shallow_dome(name + "_d", r, (x, y, z + drum_h), roof, rise=rise))
    if finial:
        parts.append(cylinder(name + "_alem", max(0.12, r * 0.04), r * 0.3, (x, y, z + drum_h + r * rise - 0.05), GILT, verts=6))
    return join(parts, name)


def domed_portico(name, length, depth, h, n, loc, face="S", color=OTT_STONE, roof=LEAD):
    """A row of n domed bays on columns (a mosque portico or a court arcade), open toward `face`."""
    x, y, z = loc
    parts = [box(name + "_b", length, depth, h, (0, 0, 0), color)]
    parts.append(arcade(name + "_a", length * 0.96, h * 0.82, n, (0, -depth / 2 - 0.05, 0), "S", DARK, True, 0.78, 0.5))
    bay = length / n
    for i in range(n):
        parts.append(dome(f"{name}_d{i}", min(bay, depth) * 0.42, (-length / 2 + bay * (i + 0.5), 0, h), roof, squash=0.75, segments=10, rings=4))
    o = join(parts, name)
    o = rot(o, {"S": 0, "N": 180, "E": 90, "W": -90}[face])
    return move(o, x, y, z)


def cells(name, length, depth, h, n, loc, axis="X", color=OTT_STONE, roof=LEAD, chimneys=True):
    """A range of domed cells (medrese rooms, hospital wards, han rooms) with chimneys."""
    x, y, z = loc
    parts = [box(name + "_b", length, depth, h, (0, 0, 0), color)]
    bay = length / n
    for i in range(n):
        cx = -length / 2 + bay * (i + 0.5)
        parts.append(dome(f"{name}_d{i}", min(bay, depth) * 0.4, (cx, 0, h), roof, squash=0.7, segments=8, rings=3))
        if chimneys and i % 2 == 0:
            parts.append(cylinder(f"{name}_ch{i}", 0.35, 1.8, (cx + bay * 0.45, depth * 0.3, h), color, verts=6, r_top=0.25))
    o = join(parts, name)
    if axis == "Y":
        o = rot(o, 90)
    return move(o, x, y, z)


def tree_row(name, pts, r=2.2, kind="cypress", color=None):
    out = []
    for i, (x, y) in enumerate(pts):
        out.append(tree(f"{name}{i}", r, (x, y, 0.4), color or (CYPRESS if kind == "cypress" else "#6F8A5C"), kind=kind))
    return join(out, name)


def houses(name, spots, color=STONE_B, roof=TILE_B, h=7.0):
    """A few town houses with hipped tile roofs: spots = [(x, y, w, d), ...]."""
    out = []
    for i, (x, y, w, d) in enumerate(spots):
        hh = h * (0.8 + 0.4 * ((i * 37) % 10) / 10)
        out.append(box(f"{name}_b{i}", w, d, hh, (x, y, 0.4), shade(color, -0.05 * (i % 3))))
        out.append(hip_roof(f"{name}_r{i}", w, d, min(w, d) * 0.35, (x, y, 0.4 + hh), roof, ridge=0.4, overhang=0.4))
    return join(out, name)


def banded_wall(name, length, t, h, loc, color=WALL_STONE, band=BRICK_B, bands=3, along="X"):
    """A straight wall of limestone with courses of brick, the Byzantine banded masonry."""
    x, y, z = loc
    w, d = (length, t) if along == "X" else (t, length)
    parts = [box(name + "_w", w, d, h, (x, y, z), color)]
    for i in range(bands):
        bz = z + h * (i + 1) / (bands + 1)
        parts.append(box(f"{name}_band{i}", w + (0.1 if along == "Y" else 0), d + (0.1 if along == "X" else 0), h * 0.06, (x, y, bz), band))
    return join(parts, name)


def battlements(name, length, t, z, loc_xy, along="X", color=WALL_STONE, size=1.1, gap=1.1):
    x, y = loc_xy
    out = []
    n = max(1, int(length / (size + gap)))
    for i in range(n):
        u = -length / 2 + (i + 0.5) * length / n
        out.append(box(f"{name}{i}", size if along == "X" else t, t if along == "X" else size, size * 1.2, (x + (u if along == "X" else 0), y + (u if along == "Y" else 0), z), color))
    return join(out, name)


def ottoman_tomb(name, r, h, loc, color=OTT_STONE, roof=LEAD, portico=True):
    x, y, z = loc
    pts = [(r * math.cos(math.pi / 8 + i * math.pi / 4), r * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
    parts = [prism(name + "_body", pts, h, (x, y, z), color)]
    parts.append(ring_panels(name + "_win", r * 0.92, 8, r * 0.35, h * 0.35, (x, y, z + h * 0.2), DARK, offset=0.0))
    parts.append(cylinder(name + "_c", r * 1.08, 0.6, (x, y, z + h), shade(color, -0.05), verts=8))
    parts.append(lead_dome(name + "_d", r * 0.92, (x, y, z + h + 0.6), r * 0.3, color, roof, rise=0.7))
    if portico:
        parts.append(box(name + "_por", r * 1.4, r * 0.7, h * 0.7, (x, y - r - r * 0.3, z), color))
        parts.append(box(name + "_porr", r * 1.5, r * 0.8, 0.4, (x, y - r - r * 0.3, z + h * 0.7), roof))
    return join(parts, name)


def pyramid_cap(name, half, h, loc, color=LEAD):
    """A four-sided pointed roof over a square tower of half-width `half`."""
    o = cylinder(name, half * 1.5, h, (0, 0, 0), color, verts=4, r_top=0.15)
    o = rot(o, 45)
    return move(o, *loc)


def boat(name, length, loc, color=TIMBER, sail=True, angle=0):
    x, y, z = loc
    L, B = length, length * 0.28
    pts = [(-L / 2, 0), (-L * 0.3, -B / 2), (L * 0.3, -B / 2), (L / 2, 0), (L * 0.3, B / 2), (-L * 0.3, B / 2)]
    parts = [prism(name + "_hull", pts, L * 0.12, (0, 0, 0), color)]
    if sail:
        parts.append(cylinder(name + "_mast", L * 0.02, L * 0.6, (0, 0, L * 0.12), TIMBER, verts=4))
        parts.append(box(name + "_sail", L * 0.02, L * 0.4, L * 0.35, (0, 0, L * 0.25), "#EFE6D2"))
    o = join(parts, name)
    o = rot(o, angle)
    return move(o, x, y, z)


# ---------------------------------------------------------------- Hagia Sophia
def hagia_sophia(variant="562"):
    """Justinian's Great Church (entrance west = -Y, apse east = +Y). variant: 562 | 1150 (buttressed) | 1560 (mosque)."""
    m = Model("hagia-sophia")
    wall = HS_WALL if variant != "562" else shade(HS_WALL, 0.08)
    m.add(0, plate("ground", 96, 110, PAVE), "body")
    # aisles and galleries, narthexes, apse
    m.add(0, box("aisles", 70, 68, 23, (0, -2, 0), wall))
    m.add(0, box("aisle_roof", 71, 69, 0.8, (0, -2, 23), LEAD))
    m.add(0, box("narthex", 62, 9, 19, (0, -40.5, 0), wall))
    m.add(0, box("narthex_roof", 63, 10, 0.8, (0, -40.5, 19), LEAD))
    m.add(0, box("exonarthex", 62, 7, 11, (0, -48.5, 0), shade(wall, -0.04)))
    m.add(0, box("exonarthex_roof", 63, 8, 0.6, (0, -48.5, 11), LEAD))
    m.add(0, arcade("exo_doors", 56, 7, 9, (0, -52.05, 0), "S", DARK, False, 0.5))
    m.add(0, arcade("nar_win", 56, 5, 9, (0, -45.05, 12), "S", DARK, False, 0.45))
    for s, f in ((1, "E"), (-1, "W")):
        m.add(0, arcade(f"gal_low{f}", 60, 7, 12, (s * 35.05, -2, 2.5), f, DARK, False, 0.5))
        m.add(0, arcade(f"gal_up{f}", 60, 6, 12, (s * 35.05, -2, 13), f, DARK, False, 0.5))
    m.add(0, apse("apse", 9, 25, (0, 32, 0), "N", wall, LEAD))
    m.add(0, arcade("apse_win", 8, 6, 3, (0, 41.1, 9), "N", DARK, False, 0.5))
    # the great piers and the north and south buttress towers
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(1, box(f"buttress{sx}{sy}", 10, 13, 29, (sx * 39, sy * 15.5, 0), shade(wall, -0.07)), "core")
            m.add(1, move(frustum(f"buttress_r{sx}{sy}", 10.6, 13.6, 3, 13.6, 5, (0, 0, 0), LEAD), sx * 39, sy * 15.5, 29))
    # the square that carries the dome, with the tympanum walls north and south (+-X)
    m.add(1, box("dome_base", 34, 34, 40, (0, 0, 0), wall))
    for s, f in ((1, "E"), (-1, "W")):
        m.add(1, arcade(f"tymp_low{f}", 26, 6, 7, (s * 17.05, 0, 25), f, DARK, False, 0.55))
        m.add(1, arcade(f"tymp_up{f}", 20, 5, 5, (s * 17.05, 0, 32.5), f, DARK, True, 0.55))
    # semi-domes east and west over half-drums, with the four exedrae
    for s, f in ((-1, "S"), (1, "N")):
        m.add(1, half_cylinder(f"semi_wall{f}", 16, 31, (0, s * 17, 0), f, wall, seg=12))
        m.add(1, half_dome(f"semi{f}", 16.3, (0, s * 17, 31), f, LEAD, rise=0.56, seg=14, rings=6))
        for sx in (-1, 1):
            m.add(1, half_cylinder(f"exw{f}{sx}", 7, 24, (sx * 10.5, s * 26, 0), f, wall, seg=8))
            m.add(1, half_dome(f"exd{f}{sx}", 7.2, (sx * 10.5, s * 26, 24), f, LEAD, rise=0.6, seg=10, rings=4))
        # five windows along the foot of each semi-dome
        for k in range(5):
            a = math.pi * (k + 0.5) / 5
            px, py = 16.05 * math.cos(a), s * (17 + 16.05 * math.sin(a))
            m.add(1, box(f"semiw{f}{k}", 1.4, 0.3, 2.6, (px, py, 31.3), DARK, rot_z=math.atan2(s * math.sin(a), math.cos(a)) + math.pi / 2))
    # the dome: forty ribs and forty windows round its foot (the 562 dome is raised about 6 m)
    dz = 40.0
    m.add(2, cylinder("drum", 16.6, 3.6, (0, 0, dz), wall, verts=40), "dome")
    m.add(2, ring_boxes("ribs", 16.9, 40, 1.0, 1.4, 3.6, (0, 0, dz), shade(wall, -0.05), offset=0.0))
    m.add(2, ring_panels("windows", 16.6, 40, 1.15, 2.6, (0, 0, dz + 0.5), DARK, offset=0.5))
    m.add(2, shallow_dome("dome", 16.8, (0, 0, dz + 3.6), LEAD, rise=0.6 if variant != "337" else 0.5))
    m.add(2, cylinder("crown", 0.6, 2.4, (0, 0, dz + 3.6 + 16.8 * 0.6 - 0.2), GILT if variant == "1560" else LEAD, verts=8))
    if variant in ("1150", "1560"):
        # flying buttresses added after earthquakes (989, 1317): the great sloping masses on the west and north
        for sx in (-1, 1):
            fb = frustum(f"wfly{sx}", 6, 10, 5, 3, 22, (0, 0, 0), shade(wall, -0.1))
            m.add(3, move(fb, sx * 22, -50, 0), "buttresses")
            for sy in (-1, 1):
                fb = frustum(f"sfly{sx}{sy}", 12, 7, 2.5, 6, 26, (0, 0, 0), shade(wall, -0.1))
                m.add(3, move(fb, sx * 41.5, sy * 30, 0))
        m.add(3, move(frustum("eastfly", 14, 8, 10, 2.5, 20, (0, 0, 0), shade(wall, -0.1)), 0, 44.5, 0))
    if variant == "1560":
        # Mehmed II's brick minaret (south-east) and Bayezid II's stone minaret (north-east)
        m.add(3, ottoman_minaret("min_brick", 2.0, 52, (40, 46, 0), 1, "#A9654A", LEAD))
        m.add(3, ottoman_minaret("min_stone", 1.7, 56, (-40, 46, 0), 1, OTT_STONE, LEAD))
        m.add(3, cylinder("crescent", 0.5, 3.5, (0, 0, dz + 3.6 + 16.8 * 0.6 + 2.0), GILT, verts=6))
    return m


def hagia_sophia_basilica():
    """The first Great Church (dedicated 360): a five-aisled timber-roofed basilica, after the usual reconstruction."""
    m = Model("hagia-sophia-basilica")
    m.add(0, plate("ground", 96, 110, PAVE), "ground")
    m.add(1, basilica("church", 60, 44, 20, (0, 14, 0.4), shade(BRICK_B, 0.1), TILE_B), "church")
    m.add(1, courtyard_ring("atrium", 44, 30, 7, 5, (0, -31, 0.4), shade(STONE_B, 0.05), DARK))
    m.add(2, box("propylon", 20, 5, 11, (0, -48.5, 0.4), STONE_B), "porch")
    m.add(2, columns("propcol", [(-8 + 4 * i, 0) for i in range(5)], 0.7, 9, (0, -52.5, 0.4), MARBLE))
    m.add(2, gable_roof("propr", 20, 7, 3, (0, -49.5, 11.4), TILE_B, 0.3))
    return m


# ---------------------------------------------------------------- Hagia Irene
def hagia_irene():
    m = Model("hagia-irene")
    brick = "#A8664C"
    m.add(0, plate("ground", 36, 86, PAVE), "body")
    m.add(0, courtyard_ring("atrium", 32, 24, 7, 4, (0, -29, 0.4), brick, DARK))
    m.add(0, box("narthex", 32, 6, 12, (0, -14, 0.4), brick))
    m.add(0, box("nave", 32, 44, 15, (0, 11, 0.4), brick))
    m.add(0, box("nave_roof", 32.6, 44.6, 0.6, (0, 11, 15.4), LEAD))
    for s, f in ((1, "E"), (-1, "W")):
        m.add(0, arcade(f"low{f}", 40, 5, 8, (s * 16.05, 11, 2), f, DARK, False, 0.45))
        m.add(0, arcade(f"up{f}", 40, 4, 8, (s * 16.05, 11, 9), f, DARK, False, 0.45))
    m.add(1, box("crossarm", 22, 16, 21, (0, 15, 0.4), brick), "domes")
    m.add(1, byz_dome("dome", 8, (0, 15, 21.4), drum_h=4.5, sides=20, wall=brick, roof=LEAD, rise=0.55))
    m.add(1, shallow_dome("west_dome", 7.5, (0, -1.5, 15.9), LEAD, rise=0.38))
    m.add(1, apse("apse", 6.5, 15, (0, 33, 0.4), "N", brick, LEAD))
    return m


def hagia_irene_basilica():
    m = Model("hagia-irene-basilica")
    m.add(0, plate("ground", 36, 86, PAVE), "ground")
    m.add(1, basilica("church", 50, 30, 15, (0, 10, 0.4), shade(BRICK_B, 0.08), TILE_B, atrium=22), "church")
    return m


# ---------------------------------------------------------------- Hippodrome
def hippodrome(variant="562"):
    """The circus, built along Y with the curved sphendone at -Y and the starting gates (carceres) at +Y; the kathisma on +X."""
    m = Model("hippodrome")
    L, W = 450, 130
    m.add(0, plate("ground", W, L, SAND_C), "seating")
    ruin = variant == "ruin"
    stone = shade(STONE_B, 0.05)
    if not ruin:
        for k, (t, h) in enumerate(((30, 4.5), (22, 9), (14, 13.5), (5, 17))):
            # seating in a U open at the starting gates (+Y): outer and inner outlines share the flat end
            outer = stadium_pts(L - 16, W)
            inner = [(x - t / 2, y) for x, y in stadium_pts(L - 16 - t, W - 2 * t)]
            r = ring_extrude(f"tier{k}", outer, inner, h, (0, 0, 0), stone if k % 2 == 0 else shade(stone, -0.06), closed=False)
            m.add(0, move(rot(r, -90), 0, -8, 0))
        for s in (-1, 1):
            m.add(1, box(f"gate_tower{s}", 12, 16, 19, (s * 59, L / 2 - 9, 0), shade(stone, 0.04)))
            m.add(1, merlons(f"gate_tm{s}", 12, 16, 19, 0.9, 0.9, stone))
            m.stages[1][-1] = move(m.stages[1][-1], s * 59, L / 2 - 9, 0)
        for s, f in ((1, "E"), (-1, "W")):
            m.add(0, arcade(f"outer{f}", 360, 11, 34, (s * 65.05, 35, 0.4), f, DARK, False, 0.6))
        # carceres with the bronze horses
        m.add(1, box("carceres", W - 6, 14, 13, (0, L / 2 - 8, 0), stone), "gates")
        m.add(1, arcade("gates", W - 20, 9, 12, (0, L / 2 - 15.05, 0.4), "S", DARK, False, 0.75))
        m.add(1, box("horses_base", 10, 4, 2.5, (0, L / 2 - 8, 13), MARBLE))
        for i in range(4):
            m.add(1, box(f"horse{i}", 1.2, 3.4, 2.2, (-3.3 + 2.2 * i, L / 2 - 8, 15.5), GILT if variant != "337" else BRONZE))
        # kathisma, the imperial box on the palace side
        m.add(1, box("kathisma", 22, 34, 22, (W / 2 - 13, 20, 0), shade(stone, 0.06)))
        m.add(1, arcade("kath_loggia", 30, 7, 5, (W / 2 - 24.05, 20, 13), "W", DARK, True, 0.7))
        m.add(1, hip_roof("kath_roof", 22, 34, 5, (W / 2 - 13, 20, 22), LEAD, ridge=0.5, overhang=0.5))
    else:
        # At Meydani: the seats robbed for stone; the sphendone's vaulted substructure still stands at the south
        r = stadium_ring("ruin_ring", L, W, 6, 3.0, (0, 0, 0), shade(stone, -0.12))
        m.add(0, rot(r, -90))
        sph = ellipse_ring("sphendone", W / 2, W / 2, 0.82, 16, (0, 0, 0), shade(stone, -0.08), n=40, arc=math.pi, start=math.pi)
        m.add(0, move(sph, 0, -L / 2 + W / 2, 0))
        for i in range(10):
            a = math.pi + math.pi * (i + 0.5) / 10
            m.add(0, box(f"sph_arch{i}", 4.5, 0.4, 9, (W / 2 * math.cos(a) * 1.002, -L / 2 + W / 2 + W / 2 * math.sin(a) * 1.002, 0.4), DARK, rot_z=a + math.pi / 2))
        m.add(1, houses("west_houses", [(-56, 60, 14, 10), (-56, 90, 12, 12), (-57, 125, 12, 9), (-55, -10, 12, 14), (52, 160, 14, 10), (55, 120, 10, 12)], STONE_B, TILE_B, 7), "houses")
        m.add(1, tree_row("trees", [(-40, 150), (-30, 175), (35, 150), (40, -80), (-42, -60), (20, 190)], 2.4, "round"))
    # the spina with its monuments
    m.add(2, box("spina", 5, 230, 1.6, (0, 5, 0.4), MARBLE), "monuments")
    if variant != "337":
        m.add(2, box("theod_base", 5, 5, 6, (0, 32, 2.0), MARBLE))
        m.add(2, obelisk("theod_obelisk", 2.3, 18.5, (0, 32, 8.0), "#B8897A"))
    m.add(2, cylinder("serpent", 0.55, 7.5, (0, 0, 2.0), BRONZE, verts=8))
    for i in range(3):
        a = math.tau * i / 3
        m.add(2, box(f"head{i}", 1.6, 0.6, 0.6, (0.8 * math.cos(a), 0.8 * math.sin(a), 9.2), BRONZE, rot_z=a))
    if variant != "337":
        m.add(2, obelisk("walled_obelisk", 3.4, 29, (0, -42, 2.0), BRONZE if variant == "562" or variant == "1150" else shade(STONE_B, -0.1)))
    if not ruin:
        for s in (-1, 1):
            for k in (-1, 0, 1):
                m.add(2, cylinder(f"meta{s}{k}", 0.9, 5, (k * 1.6, 5 + s * 117, 2.0), GILT if variant != "337" else BRONZE, verts=8, r_top=0.1))
        for i, yy in enumerate((-90, -70, 60, 80, 100)):
            m.add(2, cylinder(f"statcol{i}", 0.7, 9, (0, yy, 2.0), MARBLE, verts=8))
            m.add(2, box(f"statue{i}", 1.4, 1.4, 2.4, (0, yy, 11.0), BRONZE))
    return m


# ---------------------------------------------------------------- Great Palace and Chalke
def great_palace(variant="whole"):
    """The palace on terraces stepping down from the Hippodrome (-X) toward the sea (+X)."""
    m = Model("great-palace")
    ruin = variant == "ruin"
    wall = STONE_B if not ruin else shade(STONE_B, -0.12)
    m.add(0, plate("ground", 230, 210, GRASS if ruin else PAVE), "terraces")
    # terraces: upper (12 m) and middle (6 m) platforms with arched substructures facing the sea
    m.add(0, box("upper", 100, 210, 12, (-65, 0, 0), shade(wall, -0.05)))
    m.add(0, box("middle", 70, 190, 6, (20, -5, 0), shade(wall, -0.08)))
    m.add(0, arcade("upper_sub", 190, 9, 19, (-14.95, 0, 0.5), "E", DARK, False, 0.6))
    m.add(0, arcade("middle_sub", 170, 4.5, 17, (55.05, -5, 0.5), "E", DARK, False, 0.6))
    # Peristyle court (the mosaic court) and its apsed hall
    roof = LEAD if not ruin else None
    m.add(1, courtyard_ring("peristyle", 64, 54, 7 if not ruin else 3.5, 6, (-70, 50, 12), shade(MARBLE, -0.05), DARK), "halls")
    m.add(1, box("apse_hall", 26, 22, 14 if not ruin else 6, (-70, 89, 12), wall))
    if not ruin:
        m.add(1, gable_roof("apse_hall_r", 26, 22, 6, (-70, 89, 26), TILE_B, 0.4))
    # Daphne and the Triklinos of the Nineteen Couches
    m.add(1, box("daphne", 62, 20, 15 if not ruin else 6, (-72, -35, 12), wall))
    m.add(1, box("nineteen", 20, 50, 16 if not ruin else 5, (-30, -10, 12), wall))
    if not ruin:
        m.add(1, hip_roof("daphne_r", 62, 20, 6, (-72, -35, 27), TILE_B, ridge=0.6, overhang=0.6))
        m.add(1, hip_roof("nineteen_r", 20, 50, 6, (-30, -10, 28), LEAD, ridge=0.6, overhang=0.6))
        m.add(1, arcade("daphne_a", 56, 6, 10, (-72, -45.05, 12.5), "S", DARK, True, 0.6))
    # Chrysotriklinos: an octagonal domed throne hall with eight apses
    oct_pts = [(15 * math.cos(math.pi / 8 + i * math.pi / 4), 15 * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
    m.add(1, prism("chryso", oct_pts, 15 if not ruin else 7, (15, 40, 6), wall))
    for i in range(8):
        a = math.pi / 4 * i
        m.add(1, cylinder(f"chryso_apse{i}", 4.2, 9 if not ruin else 5, (15 + 14.2 * math.cos(a), 40 + 14.2 * math.sin(a), 6), wall, verts=10))
    if not ruin:
        m.add(2, lead_dome("chryso_dome", 13, (15, 40, 21), 2.5, wall, LEAD, rise=0.6, windows=16, finial=False), "domes")
    # palace church (Pharos) and the lighthouse tower by the sea
    if not ruin:
        m.add(2, cross_in_square("pharos", 14, 18, 11, (35, -60, 6), shade(BRICK_B, 0.05), LEAD, dome_r=3.2))
        m.add(2, cross_in_square("nea", 22, 26, 13, (-70, -80, 12), shade(BRICK_B, 0.05), LEAD, dome_r=4.2, side_domes=True))
    else:
        m.add(2, box("nea_ruin", 22, 26, 5, (-70, -80, 12), BRICK_B), "ruins")
        m.add(2, box("pharos_ruin", 14, 18, 4, (35, -60, 6), BRICK_B))
    m.add(2, box("tower", 8, 8, 24 if not ruin else 12, (100, 80, 0), wall))
    # more halls on the middle terrace, a gallery along the upper terrace edge, the wall toward the sea
    extra = [(25, 75, 30, 20, 12), (-2, -78, 22, 30, 10), (35, 5, 24, 18, 9), (-95, 10, 26, 30, 13), (-45, 70, 22, 18, 11)]
    for k, (x, y, w, d, h) in enumerate(extra):
        z0 = 12 if x < -15 else 6
        m.add(2, box(f"hall{k}", w, d, h if not ruin else h * 0.4, (x, y, z0), shade(wall, -0.04 * (k % 2))))
        if not ruin:
            m.add(2, hip_roof(f"hall_r{k}", w, d, min(w, d) * 0.3, (x, y, z0 + h), TILE_B if k % 2 else LEAD, ridge=0.5, overhang=0.5))
    if not ruin:
        m.add(2, box("gallery", 6, 170, 7, (-19, 0, 12), shade(MARBLE, -0.08)))
        m.add(2, arcade("gallery_a", 160, 5.5, 26, (-15.95, 0, 12), "E", DARK, False, 0.7))
        m.add(2, box("gallery_r", 7, 171, 0.5, (-19, 0, 19), TILE_B))
        for k in range(4):
            m.add(2, lead_dome(f"bath_d{k}", 3.2, (29 + (k % 2) * 12 - 6, 5 + (k // 2) * 8 - 4, 15), 0, wall, LEAD, finial=False))
    m.add(2, wall_run("seaward", [(112, -100), (112, 100)], 8, 2.5, (0, 0, 0), wall, towers=True, tower_every=50, tower_shape="square"))
    # lower terrace: the polo ground and gardens
    m.add(2, box("tzykanisterion", 50, 80, 0.3, (85, -40, 0.4), SAND_C))
    m.add(2, tree_row("garden", [(80, 30), (88, 45), (75, 55), (95, 15), (70, 95), (100, 100), (-20, 85), (-30, 70)], 2.6, "round"))
    if ruin:
        m.add(2, tree_row("wild", [(-60, 0), (-40, 20), (10, 0), (25, -20), (-90, 70), (-100, -60)], 2.8, "round"))
    return scale_xy(m, 220 / 230.5, 200 / 210)


def scale_xy(m, sx, sy):
    """Shrink every part of a model in plan about the origin (to fit a footprint)."""
    for objs in m.stages.values():
        for o in objs:
            o.scale = (sx, sy, 1.0)
            bpy.ops.object.select_all(action="DESELECT")
            o.select_set(True)
            bpy.context.view_layer.objects.active = o
            bpy.ops.object.transform_apply(scale=True)
    return m


def chalke():
    """The Chalke, the bronze-roofed vestibule of the palace on the Augusteion (front = -Y)."""
    m = Model("chalke")
    m.add(0, plate("ground", 45, 35, PAVE), "hall")
    m.add(0, box("hall", 28, 22, 14, (0, 2, 0.4), STONE_B))
    m.add(0, arcade("front", 22, 10, 3, (0, -9.05, 0.4), "S", DARK, False, 0.75))
    m.add(0, box("doors", 5, 0.4, 7, (0, -9.2, 0.4), BRONZE))
    m.add(0, box("icon", 2.4, 0.4, 2.8, (0, -9.3, 9.0), GILT))
    for s in (-1, 1):
        m.add(0, banded_wall(f"palace_wall{s}", 9, 3, 9, (s * 18.5, 6, 0.4), STONE_B, BRICK_B, 2))
    m.add(1, box("roof", 29, 23, 0.8, (0, 2, 14.4), BRONZE_ROOF), "dome")
    m.add(1, cylinder("drum", 8.2, 2.2, (0, 2, 15.2), STONE_B, verts=16))
    m.add(1, shallow_dome("dome", 8.4, (0, 2, 17.4), BRONZE_ROOF, rise=0.55, finial=True))
    m.add(2, columns("porch", [(-9, 0), (-3, 0), (3, 0), (9, 0)], 0.7, 8, (0, -13, 0.4), MARBLE), "porch")
    m.add(2, box("porch_roof", 22, 6, 0.8, (0, -12, 8.4), BRONZE_ROOF))
    return m


# ---------------------------------------------------------------- Basilica Cistern and the Stoa Basilica
def basilica_cistern():
    """The cistern cut open: 336 columns in 12 rows of 28 standing in water, brick vaults over the north half."""
    m = Model("basilica-cistern")
    W, D, H = 65, 138, 9.0
    m.add(0, plate("ground", W, D, PAVE), "walls")
    m.add(0, box("water", W - 6, D - 6, 0.5, (0, 0, 0.4), WATER))
    for s in (-1, 1):
        m.add(0, box(f"wx{s}", 3, D, H, (s * (W / 2 - 1.5), 0, 0), BRICK_B))
        m.add(0, box(f"wy{s}", W, 3, H, (0, s * (D / 2 - 1.5), 0), BRICK_B))
    pos = []
    for i in range(12):
        for j in range(28):
            pos.append((-W / 2 + 3 + (W - 6) * (i + 0.5) / 12, -D / 2 + 3 + (D - 6) * (j + 0.5) / 28))
    m.add(1, columns("columns", pos, 0.42, H - 1.2, (0, 0, 0.9), shade(MARBLE, -0.1), capital=True, verts=6), "columns")
    for i in range(12):
        x = -W / 2 + 3 + (W - 6) * (i + 0.5) / 12
        m.add(1, box(f"rib{i}", 0.6, (D - 6) * 0.55, 0.7, (x, -(D - 6) * 0.225, H - 0.4), shade(BRICK_B, 0.1)))
    m.add(2, box("vault", W - 6, (D - 6) * 0.45, 0.8, (0, (D - 6) * 0.275, H - 0.3), BRICK_B), "vaults")
    for i in range(12):
        for j in range(13):
            x = -W / 2 + 3 + (W - 6) * (i + 0.5) / 12
            y = (D - 6) * 0.05 + (D - 6) * 0.45 * (j + 0.5) / 13
            m.add(2, dome(f"v{i}_{j}", 2.1, (x, y, H + 0.5), shade(BRICK_B, 0.08), squash=0.5, segments=6, rings=2))
    m.add(2, box("entrance", 8, 8, 5, (-W / 2 + 6, -D / 2 + 6, 0.4), STONE_B))
    m.add(2, hip_roof("entrance_r", 8, 8, 2.5, (-W / 2 + 6, -D / 2 + 6, 5.4), TILE_B, ridge=0.2, overhang=0.4))
    return m


def stoa_basilica():
    """The Basilica (Stoa Basilike) before the cistern: a colonnaded court of law courts and bookshops."""
    m = Model("stoa-basilica")
    W, D = 65, 138
    m.add(0, plate("ground", W, D, PAVE), "court")
    m.add(0, courtyard_ring("stoa", W - 2, D - 2, 9, 8, (0, 0, 0.4), STONE_B, DARK))
    m.add(1, box("roof_ring", W - 1, D - 1, 0.5, (0, 0, 9.4), TILE_B), "colonnade")
    m.add(1, box("court", W - 18, D - 18, 0.3, (0, 0, 0.4), shade(MARBLE, -0.05)))
    m.add(1, columns("inner", peristyle_pts(W - 20, D - 20, 9, 19), 0.5, 7, (0, 0, 0.4), MARBLE))
    m.add(2, box("hall", 40, 18, 15, (0, D / 2 - 18, 0.4), STONE_B), "hall")
    m.add(2, move(rot(gable_roof("hall_r", 18, 40, 5, (0, 0, 0), TILE_B, 0.4), 90), 0, D / 2 - 18, 15.4))
    m.add(2, cylinder("statue_col", 0.8, 8, (0, -20, 0.7), MARBLE, verts=8))
    m.add(2, box("statue", 1.4, 1.4, 2.6, (0, -20, 8.7), BRONZE))
    return m


def peristyle_pts(w, d, nx, ny):
    pts = []
    for i in range(nx):
        x = -w / 2 + w * i / (nx - 1)
        pts += [(x, -d / 2), (x, d / 2)]
    for j in range(1, ny - 1):
        y = -d / 2 + d * j / (ny - 1)
        pts += [(-w / 2, y), (w / 2, y)]
    return pts


# ---------------------------------------------------------------- Forum and Column of Constantine
def porphyry_column(name, loc=(0, 0, 0), top="statue", hoops=False):
    """Constantine's column: a marble pedestal on steps, seven porphyry drums bound with wreaths, and its crown."""
    x, y, z = loc
    parts = [box(name + f"_st{i}", 13 - i * 1.6, 13 - i * 1.6, 0.6, (x, y, z + i * 0.6), shade(MARBLE, -0.05)) for i in range(3)]
    parts.append(box(name + "_ped", 8, 8, 7, (x, y, z + 1.8), MARBLE))
    parts.append(box(name + "_pedc", 8.8, 8.8, 0.8, (x, y, z + 8.8), MARBLE))
    zz = z + 9.6
    parts.append(cylinder(name + "_base", 2.2, 1.2, (x, y, zz), MARBLE, verts=16))
    zz += 1.2
    for i in range(7):
        parts.append(cylinder(f"{name}_drum{i}", 1.6, 4.0, (x, y, zz), PORPHYRY, verts=16))
        zz += 4.0
        parts.append(cylinder(f"{name}_ring{i}", 1.75, 0.5, (x, y, zz - 0.25), "#4A4440" if hoops else GILT, verts=16))
    parts.append(box(name + "_cap", 3.8, 3.8, 1.5, (x, y, zz), MARBLE))
    zz += 1.5
    if top == "statue":
        parts.append(cylinder(name + "_body", 0.7, 3.8, (x, y, zz), GILT, verts=8, r_top=0.55))
        parts.append(dome(name + "_head", 0.55, (x, y, zz + 4.2), GILT, segments=8, rings=4))
        for i in range(7):
            a = math.pi * (0.15 + 0.7 * i / 6)
            parts.append(box(f"{name}_ray{i}", 0.12, 0.12, 0.9, (x + 0.55 * math.cos(a), y, zz + 4.2 + 0.55 * math.sin(a)), GILT))
        parts.append(cylinder(name + "_spear", 0.08, 5.5, (x + 0.8, y, zz), GILT, verts=4))
        parts.append(dome(name + "_globe", 0.4, (x - 0.9, y, zz + 2.6), GILT, segments=8, rings=4))
    elif top == "cross":
        parts.append(box(name + "_cv", 0.5, 0.5, 4.5, (x, y, zz), GILT))
        parts.append(box(name + "_ch", 2.6, 0.5, 0.5, (x, y, zz + 3.0), GILT))
    else:
        parts.append(box(name + "_cap2", 2.6, 2.6, 1.2, (x, y, zz), shade(MARBLE, -0.1)))
    return join(parts, name)


def forum_of_constantine(variant="337"):
    m = Model("forum-of-constantine")
    m.add(0, plate("ground", 140, 120, shade(MARBLE, -0.08)), "colonnades")
    m.add(0, ellipse_disc_paving())
    ring = ellipse_ring("portico", 66, 56, 0.86, 13, (0, 0, 0.4), STONE_B, n=56)
    m.add(0, ring)
    m.add(0, ellipse_ring("portico_roof", 67, 57, 0.84, 0.6, (0, 0, 13.4), TILE_B, n=56))
    for lvl, zz in ((0, 1.0), (1, 7.4)):
        for i in range(40):
            a = math.tau * (i + 0.5) / 40
            if abs(math.cos(a)) > 0.97:
                continue
            m.add(0, box(f"bay{lvl}_{i}", 3.6, 0.3, 4.6, (66 * 0.86 * math.cos(a) * 0.995, 56 * 0.86 * math.sin(a) * 0.995, zz), DARK, rot_z=math.atan2(56 * math.cos(a), -66 * math.sin(a))))
    # the two arches on the Mese, east and west
    for s in (-1, 1):
        g = box(f"arch{s}", 9, 16, 17, (s * 62, 0, 0.4), MARBLE)
        m.add(1, g, "arches")
        m.add(1, arch_panel(f"archo{s}", 6, 11, (s * 66.6, 0, 0.4), "E" if s > 0 else "W", DARK, False, 0.4))
        m.add(1, arch_panel(f"archi{s}", 6, 11, (s * 57.4, 0, 0.4), "W" if s > 0 else "E", DARK, False, 0.4))
    # the Senate house on the north side
    m.add(1, box("senate", 30, 18, 15, (0, 34, 0.4), MARBLE))
    m.add(1, gable_roof("senate_r", 30, 18, 5, (0, 34, 15.4), TILE_B, 0.4))
    m.add(1, columns("senate_porch", [(-9 + 4.5 * i, 0) for i in range(5)], 0.8, 11, (0, 22.5, 0.4), PORPHYRY))
    m.add(1, box("senate_pr", 22, 5, 1.2, (0, 23, 11.4), MARBLE))
    # statues on columns round the forum
    for i, (sx, sy) in enumerate(((-30, -20), (30, -20), (-30, 18), (30, 18))):
        m.add(1, cylinder(f"scol{i}", 0.7, 7, (sx, sy, 0.4), MARBLE, verts=8))
        m.add(1, box(f"sst{i}", 1.3, 1.3, 2.2, (sx, sy, 7.4), BRONZE))
    m.add(2, porphyry_column("column", (0, 0, 0.4), "statue" if variant == "337" else "cross"), "column")
    return m


def ellipse_disc_paving():
    return ellipse_ring("paving", 57, 48, 0.0001, 0.3, (0, 0, 0.4), shade(MARBLE, -0.02), n=48)


def column_of_constantine(variant="1560"):
    m = Model("column-of-constantine")
    m.add(0, plate("ground", 140, 120, PAVE), "ground")
    if variant == "1560":
        m.add(1, houses("around", [(-50, 40, 14, 10), (-30, 45, 12, 10), (40, 40, 16, 10), (52, -38, 12, 12), (-52, -40, 14, 10), (30, -45, 14, 9)], STONE_B, TILE_B, 7), "houses")
    else:
        m.add(1, ellipse_ring("ruin", 66, 56, 0.92, 3, (0, 0, 0.4), shade(STONE_B, -0.15), n=40, arc=math.pi * 1.1, start=0.2), "ruins")
        m.add(1, tree_row("trees", [(-40, -30), (35, 30), (-20, 40)], 2.4, "round"))
    m.add(2, porphyry_column("column", (0, 0, 0.4), "cross" if variant == "1453" else "none", hoops=variant == "1560"), "column")
    return m


# ---------------------------------------------------------------- Forum of Theodosius
def spiral_column(name, h, r, loc, color=MARBLE, band=None, statue=True):
    x, y, z = loc
    parts = [box(name + "_ped", r * 3.6, r * 3.6, 6, (x, y, z), color)]
    parts.append(cylinder(name + "_shaft", r, h, (x, y, z + 6), color, verts=16))
    turns, n = 9, 150
    for i in range(n):
        t = i / n
        a = math.tau * turns * t
        parts.append(box(f"{name}_sp{i}", 0.9, 0.25, 0.7, (x + (r + 0.05) * math.cos(a), y + (r + 0.05) * math.sin(a), z + 6.5 + t * (h - 1.5)), band or shade(color, -0.18), rot_z=a + math.pi / 2))
    parts.append(box(name + "_cap", r * 2.5, r * 2.5, 1.2, (x, y, z + 6 + h), color))
    if statue:
        parts.append(cylinder(name + "_st", 0.6, 3.6, (x, y, z + 7.2 + h), GILT, verts=8))
    return join(parts, name)


def forum_of_theodosius():
    m = Model("forum-of-theodosius")
    m.add(0, plate("ground", 150, 110, shade(MARBLE, -0.08)), "colonnades")
    m.add(0, courtyard_ring("stoas", 116, 78, 10, 7, (5, -4, 0.4), STONE_B, DARK))
    m.add(0, box("stoa_roof", 117, 79, 0.5, (5, -4, 10.4), TILE_B))
    m.add(0, box("court", 100, 62, 0.25, (5, -4, 0.4), shade(MARBLE, -0.02)))
    # the basilica of Theodosius north of the forum
    m.add(1, box("basilica", 80, 14, 15, (5, 45, 0.4), STONE_B), "arch")
    m.add(1, gable_roof("basilica_r", 14, 80, 5, (0, 0, 0), TILE_B, 0.4))
    m.stages[1][-1] = move(rot(m.stages[1][-1], 90), 5, 45, 15.4)
    # the triumphal arch on the Mese, west side: three openings framed by 'tree-trunk' columns
    ax = -66
    m.add(1, box("arch", 9, 34, 19, (ax, -4, 0.4), MARBLE))
    for k, (dy, ww, hh) in enumerate(((0, 7, 13), (-11, 4, 8), (11, 4, 8))):
        m.add(1, arch_panel(f"aw{k}", ww, hh, (ax - 4.55, -4 + dy, 0.4), "W", DARK, False, 0.4))
        m.add(1, arch_panel(f"ae{k}", ww, hh, (ax + 4.55, -4 + dy, 0.4), "E", DARK, False, 0.4))
    for dy in (-15.5, -6, 6, 15.5):
        m.add(1, cylinder(f"tcol{dy}", 0.9, 14, (ax - 5.6, -4 + dy, 0.4), "#C9BEB0", verts=10))
        for k in range(5):
            m.add(1, box(f"knot{dy}_{k}", 0.6, 0.6, 0.6, (ax - 5.6 - 0.9 * math.cos(k), -4 + dy + 0.9 * math.sin(k), 2.0 + 2.4 * k), shade("#C9BEB0", -0.15)))
    # the Column of Theodosius with its spiral of reliefs
    m.add(2, spiral_column("column", 33, 2.0, (8, -6, 0.4)), "column")
    m.add(2, cylinder("statue_cav", 0.4, 0.1, (8, -6, 44), GILT, verts=4))
    return m


# ---------------------------------------------------------------- Aqueduct of Valens
def aqueduct_of_valens():
    """The arcade across the valley between the fourth and third hills (along X), two tiers where it is highest."""
    m = Model("aqueduct-of-valens")
    L, top = 900, 26.0
    m.add(0, plate("ground", L, 14, GRASS), "hills")

    def ground(x):  # the hills at either end and the valley floor between
        u = x / (L / 2)
        return max(0.0, 12.5 * (abs(u) ** 2.2) - 0.5) + 0.4

    # earth of the two hills under the ends
    prof = [(-L / 2, 0)] + [(x, ground(x)) for x in range(-450, 451, 30)] + [(L / 2, 0)]
    pts = [(px, pz) for px, pz in prof]
    verts = [(px, -7, pz) for px, pz in pts] + [(px, 7, pz) for px, pz in pts]
    n = len(pts)
    faces = [tuple(range(n)), tuple(range(2 * n - 1, n - 1, -1))] + [(i, i + 1, n + i + 1, n + i) for i in range(n - 1)] + [(n - 1, 0, n, 2 * n - 1)]
    m.add(0, mesh_from("hill", verts, faces, (0, 0, 0), shade(GRASS, -0.05)))
    bays = 84
    bay = L / bays
    for i in range(bays):
        x = -L / 2 + bay * (i + 0.5)
        g = ground(x)
        hh = top - g
        if hh < 3:
            continue
        m.add(1, box(f"bay{i}", bay + 0.05, 7.5 if hh > 14 else 6.0, hh, (x, 0, g), STONE_B), "arcades")
        if hh > 14:
            low = hh * 0.56
            for s, f in ((-1, "S"), (1, "N")):
                m.add(1, arch_panel(f"la{i}{f}", bay * 0.62, low - 1.5, (x, s * 3.8, g), f, DARK, False, 0.3))
                m.add(1, arch_panel(f"ua{i}{f}", bay * 0.55, hh - low - 3.0, (x, s * 3.8, g + low + 0.6), f, DARK, False, 0.3))
            m.add(1, box(f"band{i}", bay + 0.05, 7.8, 0.6, (x, 0, g + low), BRICK_B))
        else:
            for s, f in ((-1, "S"), (1, "N")):
                m.add(1, arch_panel(f"ua{i}{f}", bay * 0.58, hh - 2.6, (x, s * 3.05, g), f, DARK, False, 0.3))
    m.add(2, box("channel", L - 40, 4.5, 1.6, (0, 0, top), shade(STONE_B, -0.1)), "channel")
    m.add(2, box("channel_cap", L - 40, 3.0, 0.4, (0, 0, top + 1.6), BRICK_B))
    return m


# ---------------------------------------------------------------- Theodosian Land Walls
def theodosian_walls(variant="intact"):
    """A 360 m stretch of the triple defence: moat, outer wall, inner wall (outside = -Y)."""
    m = Model("theodosian-walls")
    L = 360
    m.add(0, plate("ground", L, 72, GRASS), "moat")
    m.add(0, box("moat", L, 11, 0.5, (0, -26.5, 0.1), WATER))
    m.add(0, box("counterscarp", L, 1.2, 1.4, (0, -32.6, 0.4), shade(WALL_STONE, -0.1)))
    m.add(0, box("scarp", L, 1.5, 2.6, (0, -20.4, 0.4), WALL_STONE))
    m.add(0, battlements("scarp_m", L, 1.3, 3.0, (0, -20.4), "X", WALL_STONE, 0.9, 1.3))
    m.add(0, box("peribolos", L, 7, 0.3, (0, -16, 0.4), shade(GRASS, 0.1)))
    breach = variant == "1453"
    bx0, bx1 = -75, -25

    def gap(x):
        return breach and bx0 < x < bx1

    # outer wall (8.5 m) with towers between the inner towers
    for seg_x0, seg_x1 in (((-L / 2, bx0), (bx1, L / 2)) if breach else ((-L / 2, L / 2),)):
        ln = seg_x1 - seg_x0
        cx = (seg_x0 + seg_x1) / 2
        m.add(1, banded_wall(f"outer{cx}", ln, 2.2, 8.5, (cx, -12, 0.4), WALL_STONE, BRICK_B, 2), "outer wall")
        m.add(1, battlements(f"outer_m{cx}", ln, 1.8, 8.9, (cx, -12), "X", WALL_STONE))
    for i, x in enumerate(range(-150, 151, 60)):
        if gap(x):
            continue
        if i % 2 == 0:
            m.add(1, box(f"otow{i}", 9, 7, 12, (x, -14.5, 0.4), shade(WALL_STONE, -0.04)))
        else:
            m.add(1, cylinder(f"otow{i}", 4.6, 12, (x, -15, 0.4), shade(WALL_STONE, -0.04), verts=12))
            m.add(1, box(f"otowb{i}", 9.2, 3, 12, (x, -12.5, 0.4), shade(WALL_STONE, -0.04)))
        m.add(1, battlements(f"otm{i}", 8, 6, 12.4, (x, -14.5), "X", WALL_STONE, 0.9, 1.0))
    # inner wall (12 m, 5 m thick) with great towers every 60 m and a gate in the middle
    for seg_x0, seg_x1 in (((-L / 2, bx0), (bx1, -9), (9, L / 2)) if breach else ((-L / 2, -9), (9, L / 2))):
        ln = seg_x1 - seg_x0
        cx = (seg_x0 + seg_x1) / 2
        m.add(2, banded_wall(f"inner{cx}", ln, 5, 12, (cx, 9, 0.4), WALL_STONE, BRICK_B, 4), "inner wall")
        m.add(2, battlements(f"inner_m{cx}", ln, 1.2, 12.4, (cx, 6.9), "X", WALL_STONE))
    for i, x in enumerate(range(-180, 181, 60)):
        if x == 0 or abs(x) == 180 or gap(x):
            continue
        tz = 0.4
        if i % 2 == 0:
            m.add(2, banded_wall(f"itow{i}", 11, 11, 20, (x, 4, tz), shade(WALL_STONE, -0.03), BRICK_B, 5))
            m.add(2, merlons(f"itm{i}", 11, 11, 20.4, 1.0, 1.0, WALL_STONE))
            m.stages[2][-1] = move(m.stages[2][-1], x, 4, 0)
        else:
            m.add(2, cylinder(f"itow{i}", 6.3, 20, (x, 4, tz), shade(WALL_STONE, -0.03), verts=8))
            m.add(2, ring_boxes(f"itm{i}", 5.8, 8, 1.2, 1.0, 1.3, (x, 4, 20.4), WALL_STONE))
        m.add(2, arcade(f"itw{i}", 6, 2.2, 2, (x, -1.55, 13), "S", DARK, False, 0.5))
    # the gate: two towers and an arched passage, with a gate in the outer wall and a bridge over the moat
    for s in (-1, 1):
        m.add(2, box(f"gtow{s}", 10, 12, 20, (s * 11, 4, 0.4), shade(WALL_STONE, 0.04)))
        m.add(2, merlons(f"gtm{s}", 10, 12, 20.4, 1.0, 1.0, WALL_STONE))
        m.stages[2][-1] = move(m.stages[2][-1], s * 11, 4, 0)
    m.add(2, box("gate", 12, 7, 14, (0, 8.5, 0.4), shade(WALL_STONE, 0.04)))
    m.add(2, arch_panel("gate_arch", 5, 8.5, (0, 4.9, 0.4), "S", DARK, False, 0.5))
    m.add(2, arch_panel("ogate", 4, 6, (0, -13.2, 0.4), "S", DARK, False, 0.4))
    m.add(2, box("bridge", 5, 13, 1.2, (0, -26.5, 0.4), TIMBER))
    # inside: the road behind the wall and a few houses
    m.add(3, houses("houses", [(-140, 27, 14, 9), (-110, 28, 10, 8), (60, 27, 12, 9), (100, 28, 14, 8), (150, 27, 10, 10), (20, 30, 10, 8)], STONE_B, TILE_B, 6.5), "town")
    m.add(3, tree_row("trees", [(-160, 30), (-80, 30), (40, 31), (130, 31), (-40, 32)], 2.3, "round"))
    if breach:
        # the breach of 1453: rubble, a stockade of timber, earth-filled barrels; an Ottoman bombard beyond the moat
        for k, x in enumerate(range(bx0 + 3, bx1, 7)):
            m.add(3, frustum(f"rubble{k}", 8, 9, 3, 3, 3.5 + (k % 3), (0, 0, 0), shade(WALL_STONE, -0.12)))
            m.stages[3][-1] = move(m.stages[3][-1], x, 6 - (k % 2) * 10, 0.4)
        for k in range(int((bx1 - bx0) / 1.6)):
            m.add(3, cylinder(f"stake{k}", 0.35, 6 + (k % 3) * 0.6, (bx0 + 0.8 + k * 1.6, -12, 0.4), TIMBER, verts=5))
        for k in range(6):
            m.add(3, cylinder(f"barrel{k}", 0.8, 1.6, (bx0 + 5 + k * 7.5, -10.5, 0.4), shade(TIMBER, -0.1), verts=8))
        for k in range(9):
            m.add(3, box(f"mantlet{k}", 4.5, 0.5, 2.6, (-120 + k * 28, -34.6, 0.4), shade(THATCH, -0.2)))
        for k in range(3):
            m.add(3, box(f"stone_ball{k}", 1.0, 1.0, 1.0, (-62 + k * 9, -17, 0.7), GRANITE))
    return m


# ---------------------------------------------------------------- Golden Gate and Yedikule
def golden_gate(variant="byz"):
    """The land wall with the Golden Gate (wall line at y = -45, outside = -Y); variant yedikule adds the Ottoman fortress."""
    m = Model("golden-gate" if variant == "byz" else "yedikule")
    m.add(0, plate("ground", 190, 170, GRASS), "walls")
    m.add(0, box("moat", 190, 12, 0.5, (0, -76, 0.1), WATER))
    m.add(0, box("road", 8, 120, 0.3, (0, -10, 0.4), SAND_C))
    m.add(0, banded_wall("outer", 190, 2.2, 8.5, (0, -62, 0.4), WALL_STONE, BRICK_B, 2))
    m.add(0, battlements("outer_m", 190, 1.8, 8.9, (0, -62), "X", WALL_STONE))
    m.add(0, box("bridge", 6, 13, 1.2, (0, -76, 0.4), TIMBER))
    # the outer gate (propylaeum) of marble
    m.add(1, box("propylon", 24, 7, 12, (0, -62, 0.4), MARBLE), "golden gate")
    m.add(1, arch_panel("prop_arch", 6, 9, (0, -65.6, 0.4), "S", DARK, False, 0.4))
    # inner wall with the two marble pylons and the triple arch
    for x0, x1 in ((-95, -25), (25, 95)):
        m.add(1, banded_wall(f"inner{x0}", x1 - x0, 5, 12, ((x0 + x1) / 2, -45, 0.4), WALL_STONE, BRICK_B, 4))
        m.add(1, battlements(f"inner_m{x0}", x1 - x0, 1.2, 12.4, ((x0 + x1) / 2, -47.1), "X", WALL_STONE))
    for s in (-1, 1):
        m.add(1, box(f"pylon{s}", 15, 15, 22, (s * 18, -45, 0.4), MARBLE))
        m.add(1, cornice(f"pyl_c{s}", 15, 15, 22.4, 0.6, 0.4, shade(MARBLE, -0.05)))
        m.stages[1][-1] = move(m.stages[1][-1], s * 18, -45, 0)
        m.add(1, box(f"wtow{s}", 11, 11, 20, (s * 70, -45, 0.4), shade(WALL_STONE, -0.03)))
    m.add(1, box("triple", 21, 7, 17, (0, -45, 0.4), MARBLE))
    for k, (dx, ww, hh) in enumerate(((0, 7, 13), (-7.5, 3, 7.5), (7.5, 3, 7.5))):
        m.add(1, arch_panel(f"gw{k}", ww, hh, (dx, -48.6, 0.4), "S", DARK, False, 0.4))
        m.add(1, arch_panel(f"gi{k}", ww, hh, (dx, -41.4, 0.4), "N", DARK, False, 0.4))
    m.add(1, box("doors", 6.2, 0.5, 9.5, (0, -46, 0.4), GILT if variant == "byz" else BRONZE))
    if variant == "byz":
        m.add(1, box("quadriga_base", 9, 4, 1.5, (0, -45, 17.4), MARBLE))
        for i in range(4):
            m.add(1, box(f"elephant{i}", 1.5, 3, 2.2, (-3 + 2 * i, -45, 18.9), GILT))
        m.add(2, houses("houses", [(-55, 10, 14, 10), (-30, 40, 12, 10), (40, 15, 12, 12), (60, 55, 14, 9), (-60, 60, 12, 9)], STONE_B, TILE_B, 6.5), "town")
        m.add(2, tree_row("trees", [(-20, 20), (25, 45), (-75, 30), (75, -20), (10, 70), (-40, -20)], 2.4, "round"))
        for s in (-1, 1):
            m.add(2, merlons(f"wtm{s}", 11, 11, 20.4, 1.0, 1.0, WALL_STONE))
            m.stages[2][-1] = move(m.stages[2][-1], s * 70, -45, 0)
    else:
        # Mehmed II's Yedikule: three new round towers and curtain walls closing a pentagon behind the land wall
        pent = [(-70, -45), (-85, 35), (0, 72), (85, 35), (70, -45)]
        m.add(2, wall_run("curtain", pent, 14, 5, (0, 0, 0.4), WALL_STONE, towers=False, merlon="box"), "fortress")
        for i, (x, y) in enumerate(pent[1:4]):
            m.add(2, cylinder(f"rtow{i}", 9.5, 27, (x, y, 0.4), shade(WALL_STONE, -0.02), verts=16))
            m.add(2, cylinder(f"rcap{i}", 10.3, 12, (x, y, 27.4), LEAD, verts=16, r_top=0.3))
        for s in (-1, 1):
            m.add(2, pyramid_cap(f"pcap{s}", 7.5, 9, (s * 18, -45, 23.0)))
            m.add(2, pyramid_cap(f"wcap{s}", 5.5, 8, (s * 70, -45, 20.4)))
        m.add(3, box("mosque", 12, 12, 8, (0, 15, 0.4), OTT_STONE), "mosque")
        m.add(3, lead_dome("mosque_d", 5.5, (0, 15, 8.4), 1.0, OTT_STONE, LEAD))
        m.add(3, ottoman_minaret("minaret", 1.1, 22, (8, 9, 0.4), 1))
        m.add(3, cells("barracks", 60, 7, 5, 8, (0, 50, 0.4), "X", OTT_STONE, LEAD, False))
        m.add(3, tree_row("trees", [(-30, 0), (30, 0), (-45, 30), (45, 30)], 2.2, "cypress"))
    return m


# ---------------------------------------------------------------- Sea walls
def sea_walls():
    """A stretch of the Marmara sea wall (sea = -Y): beach, wall with towers, a sea gate and a landing stage."""
    m = Model("sea-walls")
    L = 300
    m.add(0, plate("ground", L, 40, SAND_C), "shore")
    m.add(0, box("sea", L, 7, 0.6, (0, -16.5, 0.0), WATER))
    m.add(0, box("lane", L, 5, 0.3, (0, 1, 0.4), shade(SAND_C, -0.08)))
    m.add(1, banded_wall("wall", L, 3, 11, (0, -6.5, 0.4), WALL_STONE, BRICK_B, 3), "wall")
    m.add(1, battlements("wall_m", L, 1.2, 11.4, (0, -7.4), "X", WALL_STONE))
    for i, x in enumerate(range(-125, 126, 50)):
        m.add(1, banded_wall(f"tower{i}", 9, 8, 16, (x, -8, 0.4), shade(WALL_STONE, -0.03), BRICK_B, 4))
        m.add(1, merlons(f"tm{i}", 9, 8, 16.4, 1.0, 1.0, WALL_STONE))
        m.stages[1][-1] = move(m.stages[1][-1], x, -8, 0)
    m.add(1, box("gate_frame", 8, 0.6, 7.5, (0, -8.3, 0.4), MARBLE))
    m.add(1, arch_panel("gate", 4, 6, (0, -8.7, 0.4), "S", DARK, False, 0.4))
    m.add(2, box("jetty", 4, 10, 0.8, (0, -15, 0.2), TIMBER), "harbour")
    m.add(2, boat("boat1", 14, (12, -16.5, 0.5), TIMBER, True, 5))
    m.add(2, boat("boat2", 10, (-60, -17, 0.5), shade(TIMBER, -0.1), True, -10))
    m.add(2, houses("houses", [(-120, 11, 12, 9), (-95, 12, 10, 10), (-40, 11, 14, 9), (30, 12, 12, 10), (60, 11, 10, 9), (110, 12, 14, 10)], STONE_B, TILE_B, 7))
    m.add(2, cross_in_square("church", 12, 14, 9, (-70, 11, 0.4), BRICK_B, LEAD, dome_r=2.6, narthex=False))
    return m


# ---------------------------------------------------------------- Holy Apostles and the Fatih Mosque
def holy_apostles(variant="562"):
    m = Model("holy-apostles")
    m.add(0, plate("ground", 200, 200, PAVE), "precinct")
    m.add(0, courtyard_ring("precinct", 170, 170, 6, 5, (0, 0, 0.4), STONE_B, DARK))
    if variant == "337":
        # Constantine's mausoleum: a domed rotunda among memorials of the apostles
        m.add(1, cylinder("rotunda", 17, 18, (0, 0, 0.4), shade(BRICK_B, 0.1), verts=32), "mausoleum")
        m.add(1, ring_panels("niches", 17, 12, 3, 9, (0, 0, 2), DARK))
        m.add(1, ring_panels("upper", 17, 16, 1.6, 3.5, (0, 0, 12.5), DARK, 0.5))
        m.add(2, shallow_dome("dome", 17.5, (0, 0, 18.4), LEAD, rise=0.6, finial=True), "dome")
        m.add(2, box("porch", 14, 10, 10, (0, -21, 0.4), shade(BRICK_B, 0.1)))
        m.add(2, gable_roof("porch_r", 14, 10, 3, (0, -21, 10.4), TILE_B, 0.4))
        m.add(2, tree_row("cypress", [(-50, -50), (50, -50), (-50, 50), (50, 50), (0, 60)], 2.2))
        return m
    # Justinian's church (536-550): a cross of five domes; built facing west then turned to the city's grid
    wall = shade(BRICK_B, 0.04)
    parts = [box("armNS", 30, 86, 20, (0, 0, 0.4), wall), box("armEW", 76, 30, 20, (0, -6, 0.4), wall)]
    for i, (x, y) in enumerate(((0, -6), (0, -31), (0, 22), (-23, -6), (23, -6))):
        parts.append(byz_dome(f"dome{i}", 9 if i == 0 else 8, (x, y, 20.4), drum_h=4.5 if i == 0 else 3.0, sides=16, wall=wall, roof=LEAD, rise=0.6))
    parts.append(apse("apse", 8, 15, (0, 43, 0.4), "N", wall, LEAD))
    parts.append(box("narthex", 34, 8, 13, (0, -47, 0.4), wall))
    parts.append(box("narthex_r", 34.5, 8.5, 0.6, (0, -47, 13.4), LEAD))
    parts.append(arcade("narthex_a", 30, 8, 5, (0, -51.05, 0.4), "S", DARK, False, 0.6))
    for s, f in ((1, "E"), (-1, "W")):
        parts.append(arcade(f"armw{f}", 26, 6, 4, (s * 38.05, -6, 8), f, DARK, False, 0.5))
    parts.append(cylinder("constantine_mausoleum", 12, 15, (26, 34, 0.4), wall, verts=24))
    parts.append(shallow_dome("mausoleum_d", 12.3, (26, 34, 15.4), LEAD, rise=0.55))
    church = join(parts, "church")
    church = rot(church, 61)
    m.add(1, church, "church")
    m.add(2, tree_row("cypress", [(-60, -60), (60, -60), (-65, 55), (62, 60), (-70, 0), (70, 0)], 2.2), "garden")
    return m


def fatih_mosque():
    """Mehmed II's mosque complex (1463-1470) built over the Holy Apostles: qibla = +Y, court -Y, medreses each side."""
    m = Model("fatih-mosque")
    m.add(0, plate("ground", 200, 200, PAVE), "court")
    m.add(0, domed_portico("court_s", 62, 7, 7, 9, (0, -51.5, 0.4), "N"))
    for s, f in ((-1, "E"), (1, "W")):
        m.add(0, domed_portico(f"court_{f}", 41, 7, 7, 6, (s * 27.5, -27.5, 0.4), f))
    m.add(0, box("court_pave", 48, 40, 0.3, (0, -27, 0.4), shade(MARBLE, -0.05)))
    m.add(0, cylinder("sadirvan", 3.2, 3, (0, -27, 0.4), MARBLE, verts=8))
    m.add(0, dome("sadirvan_d", 3.4, (0, -27, 3.4), LEAD, squash=0.7, segments=10, rings=4))
    m.add(0, domed_portico("son_cemaat", 62, 8, 9, 5, (0, -4, 0.4), "S"))
    # prayer hall: central dome with a semi-dome to the qibla, side domes
    m.add(1, box("hall", 62, 52, 20, (0, 26, 0.4), OTT_STONE), "hall")
    m.add(1, arcade("hall_w1", 48, 6, 6, (31.05, 26, 3), "E", DARK, True, 0.45))
    m.add(1, arcade("hall_w2", 48, 6, 6, (-31.05, 26, 3), "W", DARK, True, 0.45))
    m.add(1, box("dome_base", 30, 30, 26, (0, 22, 0.4), OTT_STONE))
    m.add(2, lead_dome("dome", 13, (0, 22, 26.4), 3.5, OTT_STONE, LEAD, rise=0.62, windows=20), "domes")
    m.add(2, half_dome("semi", 13, (0, 37, 20.4), "N", LEAD, rise=0.7, seg=12, rings=5))
    for s in (-1, 1):
        for k, yy in enumerate((8, 22, 38)):
            m.add(2, lead_dome(f"side{s}{k}", 5.5, (s * 22, yy, 20.4), 0, OTT_STONE, LEAD, rise=0.55))
    for s in (-1, 1):
        m.add(2, ottoman_minaret(f"min{s}", 1.8, 56, (s * 33, 0, 0.4), 2))
    # Mehmed's tomb behind the qibla wall, and the eight medreses of the Sahn-i Seman
    m.add(3, ottoman_tomb("tomb", 8, 12, (0, 72, 0.4)), "kulliye")
    for s in (-1, 1):
        for k, yy in enumerate((-72, -28, 16, 60)):
            m.add(3, courtyard_ring(f"med{s}{k}", 34, 38, 6, 6, (s * 80, yy, 0.4), OTT_STONE, DARK))
            for j in range(4):
                m.add(3, dome(f"medd{s}{k}{j}", 3.0, (s * 80 + (j - 1.5) * 8, yy + 16, 6.4), LEAD, squash=0.7, segments=8, rings=3))
                m.add(3, dome(f"meds{s}{k}{j}", 3.0, (s * 80 + (j - 1.5) * 8, yy - 16, 6.4), LEAD, squash=0.7, segments=8, rings=3))
    m.add(3, tree_row("cypress", [(-20, 60), (20, 60), (-14, 84), (14, 84), (0, 95)], 2.2))
    return m


# ---------------------------------------------------------------- Pantokrator, Chora, Little Hagia Sophia
def pantokrator(variant="1150"):
    """Three linked churches of John II's monastery (west = -Y; the south church at +X)."""
    m = Model("pantokrator")
    m.add(0, plate("ground", 75, 60, PAVE), "churches")
    m.add(1, cross_in_square("south", 22, 26, 15, (17, 2, 0.4), BRICK_B, LEAD, dome_r=5.0, drum_h=6.5, narthex=False), "churches")
    m.add(1, cross_in_square("north", 18, 24, 13, (-16, 3, 0.4), BRICK_B, LEAD, dome_r=4.3, drum_h=5.5, narthex=False))
    m.add(1, box("chapel", 12, 26, 13, (0.5, 2, 0.4), shade(BRICK_B, 0.04)))
    m.add(1, barrel("chapel_r", 12.4, 26.4, (0.5, 2, 13.4), "Y", LEAD))
    m.add(2, byz_dome("chapel_d1", 3.3, (0.5, -4, 15.5), 4.0, wall=BRICK_B, roof=LEAD), "domes")
    m.add(2, byz_dome("chapel_d2", 3.3, (0.5, 8, 15.5), 4.0, wall=BRICK_B, roof=LEAD))
    m.add(2, box("narthex", 56, 7, 10, (1, -14.5, 0.4), BRICK_B))
    m.add(2, box("narthex_r", 56.5, 7.5, 0.6, (1, -14.5, 10.4), LEAD))
    m.add(2, arcade("narthex_a", 50, 6, 9, (1, -18.05, 0.4), "S", DARK, False, 0.55))
    m.add(2, apse("chapel_apse", 4, 9, (0.5, 15, 0.4), "N", BRICK_B, LEAD))
    if variant == "1560":
        m.add(3, ottoman_minaret("minaret", 1.3, 26, (30, -19, 0.4), 1, "#B88A6E", LEAD), "minaret")
    else:
        m.add(3, courtyard_ring("cells", 72, 8, 6, 6, (0, 26, 0.4), STONE_B, DARK), "monastery")
    return m


def chora(variant="1150"):
    """St Saviour in Chora (west = -Y; the parekklesion on the south, +X)."""
    m = Model("chora")
    m.add(0, plate("ground", 45, 40, PAVE), "church")
    m.add(1, cross_in_square("naos", 15, 16, 12, (-2, 5, 0.4), BRICK_B, LEAD, dome_r=4.0, drum_h=5.0, narthex=False), "naos")
    m.add(1, box("inner_narthex", 19, 6, 9, (-2, -6, 0.4), BRICK_B))
    m.add(1, box("inner_nr", 19.5, 6.5, 0.5, (-2, -6, 9.4), LEAD))
    if variant in ("1453", "1560"):
        m.add(2, box("outer_narthex", 27, 5, 8, (2, -11.5, 0.4), shade(BRICK_B, 0.05)), "Metochites")
        m.add(2, box("outer_nr", 27.5, 5.5, 0.5, (2, -11.5, 8.4), LEAD))
        m.add(2, arcade("outer_a", 24, 5.5, 6, (2, -14.05, 0.4), "S", DARK, False, 0.6))
        for k, x in enumerate((-6, 6)):
            m.add(2, byz_dome(f"nd{k}", 2.0, (x, -6, 9.9), 2.0, sides=10, wall=BRICK_B, roof=LEAD))
        m.add(2, box("parekklesion", 8, 26, 10, (11.5, 1, 0.4), shade(BRICK_B, 0.05)))
        m.add(2, barrel("par_r", 8.4, 26.4, (11.5, 1, 10.4), "Y", LEAD))
        m.add(2, byz_dome("par_d", 2.6, (11.5, 4, 12.3), 2.8, sides=12, wall=BRICK_B, roof=LEAD))
        m.add(2, apse("par_apse", 3.2, 7, (11.5, 14, 0.4), "N", BRICK_B, LEAD))
    if variant == "1560":
        m.add(3, ottoman_minaret("minaret", 1.0, 20, (16.5, -13, 0.4), 1, "#B88A6E", LEAD), "minaret")
    return m


def little_hagia_sophia(variant="562"):
    """Sts Sergius and Bacchus (west = -Y): an octagon under a melon dome in a square shell, narthex west, apse east."""
    m = Model("little-hagia-sophia")
    brick = "#B07052"
    m.add(0, plate("ground", 50, 70, PAVE), "church")
    m.add(0, box("shell", 30, 30, 13, (0, 14, 0.4), brick))
    m.add(0, box("shell_r", 30.6, 30.6, 0.5, (0, 14, 13.4), LEAD))
    m.add(0, box("narthex", 30, 6, 10, (0, -4, 0.4), brick))
    m.add(0, box("narthex_r", 30.6, 6.6, 0.5, (0, -4, 10.4), LEAD))
    m.add(0, apse("apse", 5.5, 12, (0, 29, 0.4), "N", brick, LEAD))
    for s, f in ((1, "E"), (-1, "W")):
        m.add(0, arcade(f"win{f}", 24, 5, 5, (s * 15.05, 14, 5), f, DARK, False, 0.5))
    oct_pts = [(10.5 * math.cos(math.pi / 8 + i * math.pi / 4), 10.5 * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
    m.add(1, prism("octagon", oct_pts, 5, (0, 14, 13.9), brick), "dome")
    m.add(1, ring_panels("oct_win", 9.8, 8, 3.2, 3, (0, 14, 14.6), DARK, offset=0.0))
    d = shallow_dome("dome", 10.3, (0, 14, 18.9), LEAD, rise=0.5)
    for v in d.data.vertices:
        dx, dy = v.co.x, v.co.y - 14
        rr = math.hypot(dx, dy)
        if rr > 1e-3:
            k = 1 + 0.05 * math.cos(math.atan2(dy, dx) * 16)
            v.co.x, v.co.y = dx * k, 14 + dy * k
    m.add(1, d)
    if variant == "1560":
        m.add(2, domed_portico("portico", 30, 6, 7, 5, (0, -10, 0.4), "S"), "medrese")
        m.add(2, cells("cells_w", 22, 6, 5, 5, (-18, -24, 0.4), "Y", OTT_STONE, LEAD))
        m.add(2, cells("cells_s", 36, 6, 5, 6, (0, -32, 0.4), "X", OTT_STONE, LEAD))
        m.add(2, ottoman_minaret("minaret", 1.2, 26, (17, -9, 0.4), 1))
        m.add(2, tree_row("trees", [(14, -22), (-6, -22)], 2.0))
    else:
        m.add(2, courtyard_ring("atrium", 30, 22, 6, 4, (0, -18, 0.4), shade(brick, 0.08), DARK), "atrium")
    return m


# ---------------------------------------------------------------- Blachernae, Kastellion, Galata Tower, Boukoleon
def blachernae():
    """The Komnenian palace on a terrace inside the land walls (the walls along -X, the city to +X)."""
    m = Model("blachernae")
    m.add(0, plate("ground", 150, 130, GRASS), "terrace")
    m.add(0, banded_wall("landwall", 130, 5, 13, (-68, 0, 0.4), WALL_STONE, BRICK_B, 4, "Y"))
    m.add(0, battlements("landwall_m", 130, 1.2, 13.4, (-70.1, 0), "Y", WALL_STONE))
    for i, y in enumerate((-55, -15, 25, 58)):
        m.add(0, box(f"lt{i}", 12, 11, 21, (-68.5, y, 0.4), shade(WALL_STONE, -0.03)))
        m.add(0, merlons(f"ltm{i}", 12, 11, 21.4, 1.0, 1.0, WALL_STONE))
        m.stages[0][-1] = move(m.stages[0][-1], -68.5, y, 0)
    # the terrace on tall arched substructures (like the Anemas vaults)
    m.add(0, box("terrace", 60, 110, 12, (-35, 0, 0.4), shade(WALL_STONE, -0.06)))
    m.add(0, arcade("terrace_a", 100, 9, 12, (-4.95, 0, 0.4), "E", DARK, False, 0.6))
    # the palace: a three-storey hall of brick and stone with balconies toward the city
    m.add(1, banded_wall("palace", 50, 22, 18, (-35, 20, 12.4), shade(STONE_B, 0.02), BRICK_B, 5), "palace")
    for k, zz in enumerate((14.5, 20.5, 26.5)):
        m.add(1, arcade(f"pw{k}", 20, 4, 5, (-9.95, 20, zz), "E", DARK, True, 0.55))
        m.add(1, arcade(f"ps{k}", 44, 4, 9, (-35, 8.95, zz), "S", DARK, True, 0.55))
    m.add(1, box("balcony", 2.5, 18, 0.6, (-22.6, 20, 20.3), TIMBER))
    m.add(1, hip_roof("palace_r", 50, 22, 6, (-35, 20, 30.4), TILE_B, ridge=0.6, overhang=0.6))
    m.add(1, banded_wall("hall", 36, 18, 14, (-38, -30, 12.4), shade(STONE_B, 0.02), BRICK_B, 4))
    m.add(1, gable_roof("hall_r", 18, 36, 5, (0, 0, 0), TILE_B, 0.5))
    m.stages[1][-1] = move(rot(m.stages[1][-1], 90), -38, -30, 26.4)
    m.add(1, arcade("hall_w", 30, 5, 6, (-38, -39.05, 17), "S", DARK, True, 0.55))
    # palace church and the gardens toward the city
    m.add(2, cross_in_square("church", 16, 18, 12, (30, 30, 0.4), BRICK_B, LEAD, dome_r=3.6), "church")
    m.add(2, tree_row("garden", [(20, -10), (35, -20), (50, -5), (45, -40), (15, -45), (60, 20), (60, 55)], 2.5, "round"))
    m.add(2, box("stair", 8, 14, 12, (-1, -10, 0.4), shade(WALL_STONE, -0.06)))
    return m


def kastellion():
    """The Kastellion of Galata, the tower that held the chain across the Golden Horn (the Horn is -Y)."""
    m = Model("kastellion")
    m.add(0, plate("ground", 40, 40, SAND_C), "bailey")
    m.add(0, box("water", 40, 9, 0.5, (0, -15.5, 0.0), WATER))
    m.add(0, wall_run("bailey", [(-17, -10), (17, -10), (17, 17), (-17, 17), (-17, -10)], 7, 2, (0, 0, 0.4), WALL_STONE, towers=False))
    m.add(1, banded_wall("keep", 13, 13, 24, (0, 4, 0.4), WALL_STONE, BRICK_B, 5), "keep")
    m.add(1, merlons("keep_m", 13, 13, 24.4, 1.0, 1.0, WALL_STONE))
    m.stages[1][-1] = move(m.stages[1][-1], 0, 4, 0)
    m.add(1, arcade("keep_w", 9, 2.5, 3, (0, -2.55, 15), "S", DARK, False, 0.4))
    m.add(2, cylinder("windlass", 1.6, 4, (0, -8, 0.4), TIMBER, verts=10), "chain")
    for i in range(10):
        m.add(2, box(f"link{i}", 0.6 if i % 2 else 0.25, 1.4, 0.6 if i % 2 == 0 else 0.25, (0, -10.5 - i * 1.0, 0.6), "#4A4440"))
    for i in range(3):
        m.add(2, box(f"float{i}", 2.5, 1.2, 0.6, (0, -13 - i * 2.4, 0.4), TIMBER))
    return m


def galata_tower():
    m = Model("galata-tower")
    stone = "#C9B897"
    m.add(0, plate("ground", 30, 30, PAVE), "tower")
    m.add(0, banded_wall("wall", 30, 3, 9, (0, -3, 0.4), WALL_STONE, BRICK_B, 2))
    m.add(0, battlements("wall_m", 30, 2.6, 9.4, (0, -3), "X", WALL_STONE))
    m.add(1, cylinder("shaft", 8.4, 44, (0, 0, 0.4), stone, verts=24, r_top=8.0), "shaft")
    for k, zz in enumerate((10, 19, 28, 37)):
        m.add(1, ring_panels(f"win{k}", 8.1 if zz > 20 else 8.3, 6, 0.9, 1.8, (0, 0, zz), DARK, offset=k * 0.5))
    m.add(2, cylinder("corbels", 8.0, 1.6, (0, 0, 44.4), stone, verts=24, r_top=9.2), "top")
    m.add(2, cylinder("gallery", 9.2, 1.2, (0, 0, 46.0), shade(stone, -0.05), verts=24))
    m.add(2, cylinder("upper", 7.6, 6, (0, 0, 47.2), stone, verts=24))
    m.add(2, ring_panels("upper_win", 7.6, 12, 1.6, 4.0, (0, 0, 47.8), DARK))
    m.add(2, cylinder("cap", 8.3, 15, (0, 0, 53.2), LEAD, verts=24, r_top=0.2))
    m.add(2, cylinder("finial", 0.2, 2.5, (0, 0, 68.0), GILT, verts=6))
    return m


def boukoleon():
    """The Boukoleon, the seaside palace on the sea wall (sea = -Y): the facade with three great marble-framed windows."""
    m = Model("boukoleon")
    m.add(0, plate("ground", 110, 45, PAVE), "sea wall")
    m.add(0, box("sea", 110, 4.5, 0.6, (0, -20.25, 0.0), WATER))
    m.add(0, box("quay", 50, 4, 1.2, (-20, -16.5, 0.4), shade(WALL_STONE, -0.08)))
    m.add(0, banded_wall("seawall", 110, 3.5, 9, (0, -12.8, 0.4), WALL_STONE, BRICK_B, 3))
    m.add(1, banded_wall("facade", 62, 3, 9, (-12, -12.8, 9.4), shade(MARBLE, -0.12), BRICK_B, 2), "palace")
    for k, x in enumerate((-30, -12, 6)):
        m.add(1, box(f"frame{k}", 7.5, 0.5, 7.0, (x, -14.5, 10.4), MARBLE))
        m.add(1, box(f"win{k}", 5.5, 0.5, 5.6, (x, -14.75, 10.9), DARK))
    m.add(1, box("loggia", 24, 8, 6, (32, -8, 9.4), STONE_B))
    m.add(1, arcade("loggia_a", 22, 5, 5, (32, -12.05, 9.4), "S", DARK, False, 0.75))
    m.add(1, box("palace", 62, 20, 18, (-12, 0, 0.4), STONE_B))
    m.add(1, hip_roof("palace_r", 62, 20, 6, (-12, 0, 18.4), TILE_B, ridge=0.6, overhang=0.6))
    m.add(1, hip_roof("loggia_r", 24, 8, 2.5, (32, -8, 15.4), TILE_B, ridge=0.6, overhang=0.4))
    m.add(2, box("tower", 10, 10, 22, (45, 8, 0.4), WALL_STONE), "tower")
    m.add(2, merlons("tower_m", 10, 10, 22.4, 1.0, 1.0, WALL_STONE))
    m.stages[2][-1] = move(m.stages[2][-1], 45, 8, 0)
    for s in (-1, 1):
        m.add(2, box(f"lion{s}", 3.2, 1.6, 2.0, (-20 + s * 6, -16.8, 1.6), MARBLE))
    m.add(2, boat("dromon", 15, (20, -19.8, 0.5), TIMBER_RED, True, 0))
    return m


# ---------------------------------------------------------------- Topkapi Palace
def topkapi():
    """Mehmed II's New Palace (1459-1478): Gate of Salutation at -Y, the courts running north-east to the point."""
    m = Model("topkapi")
    S = OTT_STONE
    m.add(0, plate("ground", 200, 360, GRASS), "walls")
    m.add(0, wall_run("enclosure", [(-98, -178), (98, -178), (98, 178), (-98, 178), (-98, -178)], 10, 2.5, (0, 0, 0.4), S, towers=False))
    for i, (x, y) in enumerate(((-95.5, -175.5), (95.5, -175.5), (95.5, 60), (-95.5, 60), (95.5, 175.5), (-95.5, 175.5))):
        m.add(0, cylinder(f"ctow{i}", 4.5, 13, (x, y, 0.4), S, verts=12))
    m.add(0, box("court2", 150, 125, 0.3, (0, -112, 0.4), shade(GRASS, 0.08)))
    m.add(0, box("court3", 130, 95, 0.3, (5, 10, 0.4), shade(PAVE, 0.05)))
    # Gate of Salutation with its two pointed towers, and the wall between the second and third courts
    m.add(1, box("salutation", 26, 14, 12, (0, -170, 0.4), S), "gates")
    m.add(1, arch_panel("salutation_a", 6, 8, (0, -177.1, 0.4), "S", DARK, True, 0.4))
    for sx in (-1, 1):
        m.add(1, cylinder(f"st{sx}", 4.6, 18, (sx * 11, -172, 0.4), S, verts=8))
        m.add(1, cylinder(f"stc{sx}", 5.0, 11, (sx * 11, -172, 18.4), LEAD, verts=8, r_top=0.1))
    m.add(1, box("inner_wall", 150, 3, 8, (0, -46, 0.4), S))
    m.add(1, box("felicity", 22, 10, 9, (0, -48, 0.4), S))
    m.add(1, hip_roof("felicity_r", 30, 16, 3.5, (0, -50, 9.4), LEAD, ridge=0.6, overhang=1.5))
    m.add(1, columns("felicity_c", [(-12 + 4 * i, 0) for i in range(7)], 0.5, 8, (0, -55, 0.4), MARBLE))
    # second court: porticoes all round, the kitchens with their chimneys, the Divan and the Tower of Justice
    m.add(2, domed_portico("p2w", 110, 7, 6, 14, (-71, -112, 0.4), "E"), "second court")
    m.add(2, domed_portico("p2s", 120, 7, 6, 14, (0, -162, 0.4), "N"))
    m.add(2, domed_portico("p2e", 110, 7, 6, 14, (62, -112, 0.4), "W"))
    m.add(2, cells("kitchens", 116, 22, 9, 10, (82, -112, 0.4), "Y", S, LEAD, False))
    for k in range(10):
        m.add(2, cylinder(f"chimney{k}", 2.0, 6, (84, -162 + k * 11.2, 13.0), S, verts=8, r_top=1.0))
        m.add(2, cylinder(f"chimney_cap{k}", 1.2, 1.2, (84, -162 + k * 11.2, 19.0), LEAD, verts=8, r_top=0.2))
    m.add(2, box("divan", 28, 18, 9, (-50, -60, 0.4), S))
    for k in range(3):
        m.add(2, lead_dome(f"divan_d{k}", 3.8, (-59 + k * 9, -60, 9.4), 0.8, S, LEAD))
    m.add(2, box("divan_eave", 34, 24, 0.5, (-50, -60, 8.4), LEAD))
    m.add(2, box("justice", 8, 8, 30, (-66, -42, 0.4), S))
    m.add(2, arcade("justice_w", 7, 3, 2, (-66, -46.05, 22), "S", DARK, True, 0.6))
    m.add(2, pyramid_cap("justice_cap", 4.2, 9, (-66, -42, 30.4)))
    m.add(2, tree_row("cypress2", [(-40, -140), (-25, -128), (25, -128), (40, -140), (-40, -92), (40, -92), (-10, -80), (10, -80), (0, -105)], 2.4))
    # the harem: a dense cluster of domed rooms and courts behind the Divan
    harem = [(-80, -25, 30, 24, 10), (-56, -22, 18, 16, 12), (-80, 5, 30, 26, 11), (-57, 8, 16, 22, 9), (-80, 38, 30, 28, 12),
             (-56, 42, 18, 20, 10), (-78, 70, 32, 22, 9), (-52, 72, 20, 18, 11)]
    for k, (x, y, w, d, h) in enumerate(harem):
        m.add(2, box(f"harem{k}", w, d, h, (x, y, 0.4), shade(S, -0.03 * (k % 3))))
        m.add(2, box(f"harem_r{k}", w + 0.6, d + 0.6, 0.4, (x, y, h + 0.4), LEAD))
        m.add(2, lead_dome(f"harem_d{k}", min(w, d) * 0.22, (x, y, h + 0.8), 0.5, S, LEAD))
    # third court: the Audience Chamber, the treasury, the privy rooms and the palace school round the sides
    m.add(3, box("arz", 20, 16, 7, (0, -32, 0.4), S), "third court")
    m.add(3, hip_roof("arz_r", 30, 26, 4, (0, -32, 7.4), LEAD, ridge=0.5, overhang=1.0))
    m.add(3, columns("arz_c", [(-12 + 4 * i, -12) for i in range(7)] + [(-12 + 4 * i, 12) for i in range(7)], 0.4, 6.5, (0, -32, 0.4), MARBLE, capital=False, verts=6))
    m.add(3, cells("school_e", 90, 14, 9, 9, (66, 10, 0.4), "Y", S, LEAD, True))
    m.add(3, domed_portico("p3e", 90, 6, 6, 11, (55, 10, 0.4), "W"))
    m.add(3, cells("school_w", 60, 14, 9, 6, (-30, 25, 0.4), "Y", S, LEAD, True))
    m.add(3, cells("treasury", 40, 18, 10, 4, (40, 66, 0.4), "X", S, LEAD, False))
    m.add(3, domed_portico("treasury_p", 40, 5, 7, 6, (40, 54.5, 0.4), "S"))
    m.add(3, cells("privy", 44, 18, 10, 4, (-22, 66, 0.4), "X", S, LEAD, False))
    # fourth court: terraced gardens down to the point, with a kiosk
    m.add(3, box("terrace4", 180, 4, 4, (0, 88, 0.4), shade(S, -0.08)))
    m.add(3, tree_row("garden4", [(-60, 110), (-30, 130), (0, 105), (30, 140), (60, 115), (75, 155), (-75, 150), (10, 160), (-45, 165), (45, 100)], 2.8, "round"))
    m.add(3, tree_row("cypress4", [(-20, 100), (20, 100), (-50, 125), (50, 130)], 2.2))
    m.add(3, box("kiosk", 14, 14, 6, (40, 150, 0.4), S))
    m.add(3, hip_roof("kiosk_r", 14, 14, 3, (40, 150, 6.4), LEAD, ridge=0.1, overhang=1.4))
    m.add(3, lead_dome("kiosk_d", 3.5, (40, 150, 9.0), 0, S, LEAD))
    return m


# ---------------------------------------------------------------- Suleymaniye
def suleymaniye():
    """Sinan's mosque for Suleyman (1550-1557): qibla = +Y; court -Y with four minarets; tombs behind; medreses each side."""
    m = Model("suleymaniye")
    S = OTT_STONE
    m.add(0, plate("ground", 230, 250, PAVE), "precinct")
    m.add(0, wall_run("precinct", [(-112, -122), (112, -122), (112, 122), (-112, 122), (-112, -122)], 4.5, 1.6, (0, 0, 0.4), S, towers=False, merlon=None))
    m.add(0, box("garden", 70, 44, 0.3, (0, 95, 0.4), GRASS))
    # medreses and hospital ranges along the sides of the precinct
    for s in (-1, 1):
        for k, yy in enumerate((-80, -20, 40)):
            m.add(0, courtyard_ring(f"med{s}{k}", 36, 50, 6.5, 6, (s * 88, yy, 0.4), S, DARK))
            for j in range(5):
                m.add(0, dome(f"medd{s}{k}{j}", 2.8, (s * 88 - s * 15, yy - 20 + j * 10, 6.9), LEAD, squash=0.7, segments=8, rings=3))
    # the court: domed porticoes round a fountain, entrance portal on the far side
    cy, cw, cd = -40, 58, 48
    m.add(1, domed_portico("court_n", cw, 7, 8, 7, (0, cy - cd / 2 + 3.5, 0.4), "N"), "court")
    for s, f in ((-1, "E"), (1, "W")):
        m.add(1, domed_portico(f"court_{f}", cd - 7, 7, 8, 5, (s * (cw / 2 - 3.5), cy + 3.5, 0.4), f))
    m.add(1, box("court_pave", cw - 14, cd - 10, 0.3, (0, cy + 1, 0.4), shade(MARBLE, -0.03)))
    m.add(1, box("sadirvan", 6, 6, 3.5, (0, cy + 2, 0.4), MARBLE))
    m.add(1, iwan("portal", 10, 14, 4, (0, cy - cd / 2 + 1, 0.4), "S", S, MARBLE))
    m.add(1, domed_portico("son_cemaat", cw, 9, 11, 5, (0, -10.5, 0.4), "S"))
    # prayer hall 59 x 58 m: four piers, a 26.5 m dome on pendentives, semi-domes to front and back (qibla axis)
    hy = 24
    m.add(2, box("hall", 58, 58, 22, (0, hy, 0.4), S), "hall")
    m.add(2, box("hall_r", 58.6, 58.6, 0.6, (0, hy, 22.4), LEAD))
    for s, f in ((1, "E"), (-1, "W")):
        m.add(2, arcade(f"hall_w1{f}", 50, 6, 7, (s * 29.05, hy, 3), f, DARK, True, 0.45))
        m.add(2, arcade(f"hall_w2{f}", 50, 4.5, 9, (s * 29.05, hy, 12.5), f, DARK, True, 0.45))
        # the galleries under the side tympana, each covered by five domes
        for k in range(5):
            m.add(2, lead_dome(f"side{f}{k}", 4.6 if k % 2 == 0 else 3.6, (s * 21.5, hy - 20 + k * 10, 22.4 + 0.6), 0.6, S, LEAD, rise=0.6))
        # tympanum wall with windows and buttress turrets
        m.add(2, box(f"tymp{f}", 3, 28, 16, (s * 13.5, hy, 22.4), S))
        m.add(2, arcade(f"tymp_w{f}", 24, 5, 6, (s * 15.05, hy, 27), f, DARK, True, 0.5))
    m.add(2, box("dome_base", 30, 30, 37, (0, hy, 0.4), S))
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(2, box(f"weight{sx}{sy}", 6, 6, 42, (sx * 15.5, hy + sy * 15.5, 0.4), S))
            m.add(2, lead_dome(f"weight_d{sx}{sy}", 2.6, (sx * 15.5, hy + sy * 15.5, 42.4), 1.8, S, LEAD, rise=0.8))
    for s, f in ((-1, "S"), (1, "N")):
        m.add(2, half_cylinder(f"semi_wall{f}", 13.3, 30, (0, hy + s * 15, 0.4), f, S, seg=12))
        m.add(2, half_dome(f"semi{f}", 13.6, (0, hy + s * 15, 30.4), f, LEAD, rise=0.75, seg=14, rings=6))
    m.add(3, cylinder("drum", 14.0, 4.2, (0, hy, 37.4), S, verts=32), "dome")
    m.add(3, ring_panels("dome_win", 14.0, 32, 1.1, 2.8, (0, hy, 38.0), DARK, 0.5))
    m.add(3, ring_boxes("dome_ribs", 14.4, 32, 0.9, 1.0, 4.2, (0, hy, 37.4), shade(S, -0.05), 0.0))
    m.add(3, lead_dome("dome", 13.9, (0, hy, 41.6), 0, S, LEAD, rise=0.66))
    # four minarets at the corners of the court: the two by the mosque taller, with three balconies
    for s in (-1, 1):
        m.add(3, ottoman_minaret(f"min_tall{s}", 2.0, 66, (s * (cw / 2 + 1.5), -13, 0.4), 3))
        m.add(3, ottoman_minaret(f"min_low{s}", 1.7, 50, (s * (cw / 2 + 1.5), cy - cd / 2 - 1, 0.4), 2))
    # the tombs of Suleyman and Hurrem in the garden behind the qibla wall
    m.add(4, ottoman_tomb("suleyman_tomb", 9, 12, (6, 96, 0.4)), "tombs")
    m.add(4, ottoman_tomb("hurrem_tomb", 5.5, 9, (-24, 98, 0.4), portico=False))
    m.add(4, tree_row("cypress", [(-40, 80), (-34, 110), (30, 112), (40, 82), (-8, 112), (22, 78), (-60, -110), (60, -110)], 2.3))
    return m


# ---------------------------------------------------------------- Grand Bazaar and Rustem Pasha
def grand_bazaar():
    """The covered market: the Cevahir Bedesten (15 domes) and the Sandal Bedesten (20 domes) among streets of shops."""
    m = Model("grand-bazaar")
    m.add(0, plate("ground", 230, 170, shade(PAVE, -0.05)), "shops")
    # streets of shops: long vaulted ranges separated by lanes, with cross lanes every so often
    k = 0
    for y in (-70, -48, -26, 26, 48, 70):
        for x0, x1 in ((-110, -66), (-60, -14), (-8, 40), (46, 110)):
            ln = x1 - x0
            m.add(0, box(f"shop{k}", ln, 13, 6.0, ((x0 + x1) / 2, y, 0.4), shade(STONE_B, -0.04 * (k % 3))))
            m.add(0, barrel(f"shopr{k}", 13.4, ln + 0.4, ((x0 + x1) / 2, y, 6.4), "X", LEAD, rise=0.35))
            for j in range(int(ln / 9)):
                m.add(0, dome(f"shopd{k}_{j}", 1.6, ((x0 + x1) / 2 - ln / 2 + 4.5 + j * 9, y, 8.5), LEAD, squash=0.6, segments=8, rings=3))
            k += 1
    # the domed street between the two bedestens
    m.add(0, cells("arasta", 38, 12, 6, 5, (12, 0, 0.4), "X", STONE_B, LEAD, False))
    # the Cevahir (old) Bedesten of Mehmed II
    bx, by = -30, 0
    m.add(1, box("bedesten", 45, 30, 11, (bx, by, 0.4), STONE_B), "bedestens")
    for i in range(5):
        for j in range(3):
            m.add(1, lead_dome(f"bd{i}{j}", 3.9, (bx - 18 + i * 9, by - 9.5 + j * 9.5, 11.4), 0.8, STONE_B, LEAD, rise=0.6, finial=False))
    for s, f in ((-1, "S"), (1, "N")):
        m.add(1, arch_panel(f"bgate{f}", 4, 7, (bx, by + s * 15.05, 0.4), f, DARK, True, 0.4))
    for s, f in ((-1, "W"), (1, "E")):
        m.add(1, arch_panel(f"bgate{f}", 4, 7, (bx + s * 22.55, by, 0.4), f, DARK, True, 0.4))
    # the Sandal Bedesten
    sx, sy = 52, -1
    m.add(1, box("sandal", 40, 32, 10, (sx, sy, 0.4), shade(STONE_B, 0.04)))
    for i in range(5):
        for j in range(4):
            m.add(1, lead_dome(f"sd{i}{j}", 3.3, (sx - 16 + i * 8, sy - 12 + j * 8, 10.4), 0.6, STONE_B, LEAD, rise=0.6, finial=False))
    # hans at either end of the middle band, and a small mosque
    m.add(2, courtyard_ring("han_w", 44, 30, 9, 7, (-86, 0, 0.4), STONE_B, DARK), "hans")
    for j in range(5):
        m.add(2, dome(f"hanw_d{j}", 2.6, (-104 + j * 9, 11.5, 9.4), LEAD, squash=0.7, segments=8, rings=3))
        m.add(2, dome(f"hanw_s{j}", 2.6, (-104 + j * 9, -11.5, 9.4), LEAD, squash=0.7, segments=8, rings=3))
    m.add(2, courtyard_ring("han_e", 22, 30, 9, 6, (98, 0, 0.4), STONE_B, DARK))
    m.add(2, box("mescid", 10, 10, 8, (80, -6, 0.4), OTT_STONE))
    m.add(2, lead_dome("mescid_d", 4.4, (80, -6, 8.4), 0.8))
    m.add(2, ottoman_minaret("mescid_m", 0.9, 22, (79, 8, 0.4), 1))
    return m


def rustem_pasha():
    """Sinan's mosque for the grand vizier Rustem Pasha, raised on a platform over vaulted shops (qibla = +Y)."""
    m = Model("rustem-pasha")
    S = OTT_STONE
    m.add(0, plate("ground", 60, 50, PAVE), "platform")
    m.add(0, box("platform", 56, 46, 5, (0, 0, 0.4), shade(S, -0.08)))
    for s, f in ((-1, "S"), (1, "N")):
        m.add(0, arcade(f"shops{f}", 52, 3.8, 10, (0, s * 23.05, 0.4), f, DARK, True, 0.7))
    for s, f in ((1, "E"), (-1, "W")):
        m.add(0, arcade(f"shops{f}", 42, 3.8, 8, (s * 28.05, 0, 0.4), f, DARK, True, 0.7))
    m.add(0, stair("stair", 6, 5, 7, 8, (-14, -21.5, 0.4), "S", shade(S, -0.08)))
    m.add(1, box("hall", 30, 26, 13, (0, 7, 5.4), S), "mosque")
    m.add(1, arcade("hall_w", 26, 5, 5, (15.05, 7, 8), "E", DARK, True, 0.5))
    m.add(1, arcade("hall_w2", 26, 5, 5, (-15.05, 7, 8), "W", DARK, True, 0.5))
    m.add(1, domed_portico("portico", 30, 6, 8, 5, (0, -9, 5.4), "S"))
    m.add(1, box("portico_outer", 32, 4, 5, (0, -14, 5.4), shade(S, -0.03)))
    m.add(1, box("portico_outer_r", 32.5, 4.5, 0.5, (0, -14, 10.4), LEAD))
    for sx in (-1, 1):
        for sy in (-1, 1):
            m.add(2, half_dome(f"exedra{sx}{sy}", 4.6, (sx * 9.5, 7 + sy * 9, 18.4), "N" if sy > 0 else "S", LEAD, rise=0.65, seg=8, rings=4), "dome")
    oct_pts = [(9 * math.cos(math.pi / 8 + i * math.pi / 4), 9 * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
    m.add(2, prism("octagon", oct_pts, 4, (0, 7, 18.4), S))
    m.add(2, ring_panels("oct_w", 8.4, 8, 2.2, 2.4, (0, 7, 18.9), DARK))
    m.add(2, lead_dome("dome", 7.8, (0, 7, 22.4), 1.2, S, LEAD, rise=0.65, windows=16))
    m.add(3, ottoman_minaret("minaret", 1.3, 38, (17.5, -10, 5.4), 1), "minaret")
    return m


# ---------------------------------------------------------------- registry
BUILDERS = {
    "constantinople/hagia-sophia": lambda: hagia_sophia("562"),
    "constantinople/hagia-sophia-1150": lambda: hagia_sophia("1150"),
    "constantinople/hagia-sophia-mosque": lambda: hagia_sophia("1560"),
    "constantinople/hagia-sophia-basilica": hagia_sophia_basilica,
    "constantinople/hagia-irene": hagia_irene,
    "constantinople/hagia-irene-basilica": hagia_irene_basilica,
    "constantinople/hippodrome": lambda: hippodrome("562"),
    "constantinople/hippodrome-337": lambda: hippodrome("337"),
    "constantinople/hippodrome-ruin": lambda: hippodrome("ruin"),
    "constantinople/great-palace": great_palace,
    "constantinople/great-palace-ruin": lambda: great_palace("ruin"),
    "constantinople/chalke": chalke,
    "constantinople/basilica-cistern": basilica_cistern,
    "constantinople/stoa-basilica": stoa_basilica,
    "constantinople/forum-of-constantine": lambda: forum_of_constantine("337"),
    "constantinople/forum-of-constantine-1150": lambda: forum_of_constantine("1150"),
    "constantinople/column-of-constantine": lambda: column_of_constantine("1560"),
    "constantinople/column-of-constantine-1453": lambda: column_of_constantine("1453"),
    "constantinople/forum-of-theodosius": forum_of_theodosius,
    "constantinople/aqueduct-of-valens": aqueduct_of_valens,
    "constantinople/theodosian-walls": theodosian_walls,
    "constantinople/theodosian-walls-1453": lambda: theodosian_walls("1453"),
    "constantinople/golden-gate": golden_gate,
    "constantinople/yedikule": lambda: golden_gate("yedikule"),
    "constantinople/sea-walls": sea_walls,
    "constantinople/holy-apostles-337": lambda: holy_apostles("337"),
    "constantinople/holy-apostles": holy_apostles,
    "constantinople/fatih-mosque": fatih_mosque,
    "constantinople/pantokrator": pantokrator,
    "constantinople/pantokrator-mosque": lambda: pantokrator("1560"),
    "constantinople/chora": chora,
    "constantinople/chora-1453": lambda: chora("1453"),
    "constantinople/chora-mosque": lambda: chora("1560"),
    "constantinople/little-hagia-sophia": little_hagia_sophia,
    "constantinople/little-hagia-sophia-mosque": lambda: little_hagia_sophia("1560"),
    "constantinople/blachernae": blachernae,
    "constantinople/kastellion": kastellion,
    "constantinople/galata-tower": galata_tower,
    "constantinople/boukoleon": boukoleon,
    "constantinople/topkapi": topkapi,
    "constantinople/suleymaniye": suleymaniye,
    "constantinople/grand-bazaar": grand_bazaar,
    "constantinople/rustem-pasha": rustem_pasha,
}
