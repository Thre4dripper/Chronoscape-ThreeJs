"""Paris landmark miniatures: Roman Lutetia (forum, baths, arena), the Gothic cathedral and palace chapel,
the palace of the Cité, the Louvre in three states, bridges with houses, fortresses, abbeys and squares.

Conventions as worldkit: metres, origin at the ground centre, +X east, +Y north, +Z up, main front to the
south (-Y). Helpers build at the origin and are put in place with place().
"""
import math
import bpy
from chronokit import Model, box, cylinder, dome, join, shade, gable_roof, hip_roof, mesh_from, ellipse_ring, ring_extrude, ellipse_pts, ellipse_disc, columns, mini_temple
from worldkit import *

# ---------------------------------------------------------------- palette
STONE = "#D9CDB0"        # Lutetian limestone, the pale stone of Paris
STONE_D = "#C4B796"
STONE_L = "#E6DDC8"
SLATE_P = "#575C66"      # slate roofs
LEAD_P = "#76808C"       # lead roofs and spires
GLASS = "#3B4A78"        # stained glass
PAVE = "#CDBF9F"
GROUND = "#C9BC94"
GRASS = "#8DA06A"
LEAF = "#6E8A58"
PLAST = "#E4D9C2"        # plastered timber houses
PLAST2 = "#D8C9AA"
TIMBER_D = "#5A4632"
BRICK_P = "#A9573F"
TILE_R = "#B0603F"       # Roman roof tile
WATER_C = "#5F878C"
SAND = "#D8C496"
GILT_P = "#C9A44C"


# ---------------------------------------------------------------- placement helpers
def place(o, ang=0.0, x=0.0, y=0.0, z=0.0):
    """Rotate an object built at the origin about the origin (degrees, counter-clockwise from above), then move it."""
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


def plate(w, d, color=PAVE, h=0.3, x=0, y=0):
    return box("plate", w, d, h, (x, y, 0), color)


def roof_y(name, w, d, h, x=0, y=0, z=0, color=SLATE_P, over=0.4):
    """Gable roof with the ridge along Y (length d)."""
    return place(gable_roof(name, w, d, h, (0, 0, 0), color, overhang=over), 0, x, y, z)


def roof_x(name, w, d, h, x=0, y=0, z=0, color=SLATE_P, over=0.4):
    """Gable roof with the ridge along X (length w)."""
    return place(gable_roof(name, d, w, h, (0, 0, 0), color, overhang=over), 90, x, y, z)


def hip(name, w, d, h, x=0, y=0, z=0, color=SLATE_P, ridge=0.4, over=0.4):
    if w > d:
        return place(hip_roof(name, d, w, h, (0, 0, 0), color, ridge=ridge, overhang=over), 90, x, y, z)
    return place(hip_roof(name, w, d, h, (0, 0, 0), color, ridge=ridge, overhang=over), 0, x, y, z)


def gable_wall(name, w, h, t, x, y, z, normal="S", color=STONE):
    """A stone gable triangle (w wide, h high, t thick) standing on z, facing `normal`."""
    verts = [(-w / 2, -t / 2, 0), (w / 2, -t / 2, 0), (0, -t / 2, h), (-w / 2, t / 2, 0), (w / 2, t / 2, 0), (0, t / 2, h)]
    faces = [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]
    o = mesh_from(name, verts, faces, (0, 0, 0), color)
    return place(o, {"S": 0, "N": 0, "E": 90, "W": 90}[normal], x, y, z)


def panel(name, w, h, x, y, z, normal_deg, color=DARK, pointed=True, depth=0.3):
    """An arched recess on a wall whose outward normal points at normal_deg (0 = +X, 90 = +Y)."""
    o = arch_panel(name, w, h, (0, 0, 0), "S", color, pointed, depth)
    return place(o, normal_deg + 90, x, y, z)


def disc(name, r, x, y, z, normal="S", color=GLASS, t=0.4, verts=24):
    o = cylinder(name, r, t, (0, 0, -t / 2), color, verts=verts)
    if normal in ("S", "N"):
        apply_rot(o, rx=math.pi / 2)
    else:
        apply_rot(o, ry=math.pi / 2)
    return move(o, x, y, z)


def rose(name, r, x, y, z, normal="S", frame=STONE_D):
    off = {"S": (0, -0.25), "N": (0, 0.25), "E": (0.25, 0), "W": (-0.25, 0)}[normal]
    return join([disc(name + "_f", r + 0.6, x, y, z, normal, frame, 0.35),
                 disc(name + "_g", r, x + off[0], y + off[1], z, normal, GLASS, 0.35),
                 disc(name + "_c", r * 0.22, x + off[0] * 2, y + off[1] * 2, z, normal, frame, 0.35, 12)], name)


def strut(name, a, b, t=0.9, depth=1.4, color=STONE_D):
    """A flying buttress: a slab from point a (outer pier top) to point b (wall), depth measured downward."""
    ax, ay, az = a
    bx, by, bz = b
    dx, dy = bx - ax, by - ay
    L = math.hypot(dx, dy) or 1
    px, py = -dy / L * t / 2, dx / L * t / 2
    verts = []
    for s in (-1, 1):
        verts += [(ax + s * px, ay + s * py, az - depth), (bx + s * px, by + s * py, bz - depth * 0.6), (bx + s * px, by + s * py, bz), (ax + s * px, ay + s * py, az)]
    faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    return mesh_from(name, verts, faces, (0, 0, 0), color)


def pinnacle(name, r, h, x, y, z, color=STONE_D):
    o = cylinder(name, r, h, (x, y, z), color, verts=4, r_top=0)
    o.rotation_euler[2] = math.pi / 4
    return o


def cone_tower(name, r, h, x, y, z=0, color=STONE, roof=SLATE_P, cone=1.7, machicolation=True, merlons_top=False, verts=16, finial=True):
    """A round tower with a corbelled parapet and a slate cone (the French castle tower)."""
    parts = [cylinder(name + "_s", r, h, (x, y, z), color, verts=verts)]
    if machicolation:
        parts.append(cylinder(name + "_m", r * 1.12, 1.2, (x, y, z + h - 1.2), shade(color, -0.06), verts=verts))
    if merlons_top:
        n = max(6, int(2 * math.pi * r / 1.8))
        for i in range(n):
            a = math.tau * i / n
            parts.append(box(f"{name}_mm{i}", 0.9, 0.7, 1.1, (x + r * 1.05 * math.cos(a), y + r * 1.05 * math.sin(a), z + h), shade(color, -0.04), rot_z=a))
    if cone:
        parts.append(cylinder(name + "_c", r * 1.15, r * cone, (x, y, z + h), roof, verts=verts, r_top=0))
        if finial:
            parts.append(cylinder(name + "_fi", 0.12, r * 0.5, (x, y, z + h + r * cone * 0.95), LEAD_P, verts=4))
    return join(parts, name)


def windows(name, length, n, x, y, z, normal="S", h=2.4, fill=0.45, color=DARK, pointed=False):
    return arcade(name, length, h, n, (x, y, z), normal, color, pointed, fill, 0.25)


def range_block(name, cx, cy, w, d, h, wall=STONE, roof=SLATE_P, roof_h=None, axis="x", rows=2, color=DARK, dormers=0, faces=("S", "N"), win_n=None):
    """A rectangular range of rooms with a gable roof along its long axis and rows of windows."""
    parts = [box(name + "_b", w, d, h, (cx, cy, 0), wall)]
    rh = roof_h if roof_h is not None else min(w, d) * 0.55
    if axis == "x":
        parts.append(roof_x(name + "_r", w, d, rh, cx, cy, h, roof))
    else:
        parts.append(roof_y(name + "_r", w, d, rh, cx, cy, h, roof))
    L = w if axis == "x" else d
    n = win_n or max(2, int(L / 4.5))
    storey = h / max(1, rows)
    for f in faces:
        fx, fy = {"S": (cx, cy - d / 2 - 0.05), "N": (cx, cy + d / 2 + 0.05), "E": (cx + w / 2 + 0.05, cy), "W": (cx - w / 2 - 0.05, cy)}[f]
        ln = w if f in ("S", "N") else d
        for r in range(rows):
            parts.append(windows(f"{name}_w{f}{r}", ln * 0.9, max(2, int(ln / 4.5)), fx, fy, storey * r + storey * 0.3, f, storey * 0.5, 0.4, color))
        if dormers:
            for i in range(dormers):
                t = -ln / 2 + ln * (i + 0.5) / dormers
                dx, dy = (t, 0) if f in ("S", "N") else (0, t)
                inset = {"S": (0, d * 0.18), "N": (0, -d * 0.18), "E": (-w * 0.18, 0), "W": (w * 0.18, 0)}[f]
                bx, by = fx + dx + inset[0], fy + dy + inset[1]
                parts.append(box(f"{name}_dm{f}{i}", 1.6, 1.6, 2.0, (bx, by, h), wall))
                parts.append(roof_x(f"{name}_dr{f}{i}", 1.8, 1.8, 1.2, bx, by, h + 2.0, roof, 0.1) if f in ("E", "W") else roof_y(f"{name}_dr{f}{i}", 1.8, 1.8, 1.2, bx, by, h + 2.0, roof, 0.1))
    return join(parts, name)


def house(name, x, y, w, d, h, wall=PLAST, roof=SLATE_P, gable_to="y", roof_h=None, timber=True):
    """A narrow town house; gable_to='y' puts the gable end toward ±Y (ridge along Y)."""
    parts = [box(name + "_b", w, d, h, (x, y, 0), wall)]
    rh = roof_h or (w if gable_to == "y" else d) * 0.8
    parts.append(roof_y(name + "_r", w, d, rh, x, y, h, roof, 0.25) if gable_to == "y" else roof_x(name + "_r", w, d, rh, x, y, h, roof, 0.25))
    if timber:
        parts.append(box(name + "_t", w + 0.1, d + 0.1, 0.35, (x, y, h * 0.45), TIMBER_D))
    return join(parts, name)


def tree(name, r, x, y, h=None):
    h = h or r * 1.6
    return join([cylinder(name + "_t", r * 0.15, h * 0.45, (x, y, 0), TIMBER, verts=6),
                 dome(name + "_c", r, (x, y, h * 0.4), LEAF, squash=1.1, segments=10, rings=6)], name)


def water_ring(name, w_out, d_out, band, x=0, y=0, color=WATER_C):
    return join([box(name + "s", w_out, band, 0.35, (x, y - d_out / 2 + band / 2, 0), color),
                 box(name + "n", w_out, band, 0.35, (x, y + d_out / 2 - band / 2, 0), color),
                 box(name + "w", band, d_out - 2 * band, 0.35, (x - w_out / 2 + band / 2, y, 0), color),
                 box(name + "e", band, d_out - 2 * band, 0.35, (x + w_out / 2 - band / 2, y, 0), color)], name)


def curtain(name, pts, h, t, color=STONE, merlon=True):
    return wall_run(name, pts, h, t, (0, 0, 0), color, towers=False, merlon="box" if merlon else None)


# ---------------------------------------------------------------- Gothic church body
def gothic_body(name, y0, y1, nave_w, nave_h, aisles, color=STONE, roof=LEAD_P, bay=7.5, flyers=True, apse=True,
                transept=None, glass=GLASS, round_win=False, buttress=True):
    """Nave (and choir) running along +Y from y0 to y1 (apse centre at y1), with `aisles` = [(width, height), ...]
    outward from the nave. Returns dict of part lists: walls, roofs, buttress."""
    walls, roofs, butt = [], [], []
    L = y1 - y0
    cy = (y0 + y1) / 2
    half = nave_w / 2
    walls.append(box(name + "_nave", nave_w, L, nave_h, (0, cy, 0), color))
    roofs.append(roof_y(name + "_naveroof", nave_w, L, nave_w * 0.78, 0, cy, nave_h, roof, 0.4))
    nb = max(2, int(round(L / bay)))
    edge = half
    outer_h = nave_h
    for k, (aw, ah) in enumerate(aisles):
        for s in (-1, 1):
            xc = s * (edge + aw / 2)
            walls.append(box(f"{name}_ai{k}{s}", aw, L, ah, (xc, cy, 0), shade(color, -0.02 * k)))
            # lean-to roof sloping outward
            hi_x, lo_x = s * edge, s * (edge + aw)
            verts = [(hi_x, y0, ah + aw * 0.35), (lo_x, y0, ah), (lo_x, y1, ah), (hi_x, y1, ah + aw * 0.35),
                     (hi_x, y0, ah), (hi_x, y1, ah)]
            faces = [(0, 1, 2, 3), (4, 1, 0), (5, 3, 2), (4, 5, 2, 1), (0, 3, 5, 4)]
            roofs.append(mesh_from(f"{name}_air{k}{s}", verts, faces, (0, 0, 0), roof))
            if k == len(aisles) - 1:
                for i in range(nb):
                    by = y0 + L * (i + 0.5) / nb
                    walls.append(panel(f"{name}_aw{k}{s}{i}", L / nb * 0.42, ah * 0.6, s * (edge + aw + 0.05), by, ah * 0.18, 0 if s > 0 else 180, glass, not round_win, 0.3))
        edge += aw
        outer_h = ah
    # clerestory windows
    for s in (-1, 1):
        for i in range(nb):
            by = y0 + L * (i + 0.5) / nb
            top_aisle = aisles[0][1] if aisles else 0
            walls.append(panel(f"{name}_cl{s}{i}", L / nb * 0.45, (nave_h - top_aisle) * 0.62, s * (half + 0.05), by, top_aisle + (nave_h - top_aisle) * 0.2, 0 if s > 0 else 180, glass, not round_win, 0.3))
    if buttress and aisles:
        out = edge + 1.0
        for s in (-1, 1):
            for i in range(nb + 1):
                by = y0 + L * i / nb
                if i == 0:
                    by += 1.2
                ph = outer_h + (nave_h - outer_h) * 0.55
                butt.append(box(f"{name}_bp{s}{i}", 2.0, 1.6, ph, (s * out, by, 0), shade(color, -0.07)))
                butt.append(pinnacle(f"{name}_bpin{s}{i}", 1.0, 4.0, s * out, by, ph, shade(color, -0.07)))
                if flyers:
                    butt.append(strut(f"{name}_fl{s}{i}", (s * out, by, ph - 0.3), (s * half, by, nave_h * 0.86), 0.8, 1.5, shade(color, -0.05)))
    if apse:
        r = half
        walls.append(cylinder(name + "_apse", r, nave_h, (0, y1, 0), color, verts=16))
        roofs.append(cylinder(name + "_apser", r + 0.4, nave_w * 0.78, (0, y1, nave_h), roof, verts=16, r_top=0.1))
        e = half
        for k, (aw, ah) in enumerate(aisles):
            e += aw
            walls.append(cylinder(f"{name}_amb{k}", e, ah, (0, y1, 0), shade(color, -0.02 * k), verts=24))
            roofs.append(cylinder(f"{name}_ambr{k}", e + 0.3, aw * 0.35, (0, y1, ah), roof, verts=24, r_top=e - aw))
        for j in range(7):
            a = math.radians(15 + j * 25)
            walls.append(panel(f"{name}_apw{j}", 2.4, nave_h * 0.3, (r + 0.05) * math.cos(a), y1 + (r + 0.05) * math.sin(a), nave_h * 0.6, math.degrees(a), glass, not round_win, 0.3))
            if aisles:
                walls.append(panel(f"{name}_apo{j}", 2.6, aisles[-1][1] * 0.55, (e + 0.05) * math.cos(a), y1 + (e + 0.05) * math.sin(a), aisles[-1][1] * 0.18, math.degrees(a), glass, not round_win, 0.3))
                if buttress:
                    a2 = math.radians(2.5 + j * 25 + 12.5)
                    if a2 < math.pi:
                        px, py = (e + 1.0) * math.cos(a2), y1 + (e + 1.0) * math.sin(a2)
                        ph = outer_h + (nave_h - outer_h) * 0.55
                        b = box(f"{name}_abp{j}", 2.0, 1.6, ph, (0, 0, 0), shade(color, -0.07))
                        butt.append(place(b, math.degrees(a2), px, py, 0))
                        butt.append(pinnacle(f"{name}_abpin{j}", 1.0, 4.0, px, py, ph, shade(color, -0.07)))
                        if flyers:
                            butt.append(strut(f"{name}_afl{j}", (px, py, ph - 0.3), (r * math.cos(a2), y1 + r * math.sin(a2), nave_h * 0.86), 0.8, 1.5, shade(color, -0.05)))
    if transept:
        ty, tw, tdepth = transept       # centre y, total width (x), depth (y)
        walls.append(box(name + "_tr", tw, tdepth, nave_h, (0, ty, 0), color))
        roofs.append(roof_x(name + "_trr", tw, tdepth, tdepth * 0.78, 0, ty, nave_h, roof, 0.4))
        for s in (-1, 1):
            walls.append(gable_wall(f"{name}_trg{s}", tdepth + 0.6, tdepth * 0.8, 1.0, s * (tw / 2 - 0.3), ty, nave_h, "E", color))
            walls.append(rose(f"{name}_trrose{s}", tdepth * 0.3, s * (tw / 2 + 0.05), ty, nave_h * 0.62, "E" if s > 0 else "W"))
            walls.append(panel(f"{name}_trp{s}", tdepth * 0.32, nave_h * 0.32, s * (tw / 2 + 0.05), ty, 0, 0 if s > 0 else 180, DARK, True, 0.5))
            walls.append(pinnacle(f"{name}_trpin{s}", 0.7, 4.0, s * (tw / 2 - 0.3), ty, nave_h + tdepth * 0.8 - 0.5))
    return dict(walls=walls, roofs=roofs, butt=butt)


def spire(name, x, y, z, r, h, lantern=8.0, color=LEAD_P, sides=8):
    parts = [cylinder(name + "_l", r, lantern, (x, y, z), color, verts=sides)]
    for i in range(sides):
        a = math.tau * (i + 0.5) / sides
        parts.append(panel(f"{name}_lw{i}", r * 0.5, lantern * 0.6, x + r * 0.93 * math.cos(a), y + r * 0.93 * math.sin(a), z + lantern * 0.2, math.degrees(a), DARK, True, 0.2))
    parts.append(cylinder(name + "_n", r, h, (x, y, z + lantern), color, verts=sides, r_top=0))
    for i in range(4):
        a = math.tau * (i + 0.5) / 4
        parts.append(pinnacle(f"{name}_p{i}", 0.5, lantern * 0.9, x + r * 1.2 * math.cos(a), y + r * 1.2 * math.sin(a), z, color))
    parts.append(cylinder(name + "_cr", 0.15, 2.0, (x, y, z + lantern + h - 0.2), GILT_P, verts=4))
    return join(parts, name)


# ================================================================= Notre-Dame
def notre_dame(variant="1550"):
    m = Model("notre-dame")
    m.add(0, plate(48, 128, PAVE), "ground")
    b = gothic_body("nd", -52, 40, 13, 33, [(8, 20), (7.5, 12)], STONE, LEAD_P, bay=7.7,
                    transept=(9, 48, 14))
    m.add(0, join(b["walls"], "nd_walls"), "walls")
    m.add(1, join(b["roofs"] + b["butt"], "nd_roofs"), "roofs")
    # west front: block to the gallery, then the two towers
    W, front = 41, -64
    f = [box("ndf_block", W, 12, 43, (0, front + 6, 0), STONE)]
    for xb in (-20.5, -5.2, 5.2, 20.5):
        f.append(box(f"ndf_bt{xb}", 2.4, 1.6, 41, (xb, front - 0.6, 0), shade(STONE, -0.05)))
    f.append(panel("ndf_p0", 7.4, 13.5, 0, front - 0.6, 0, -90, DARK, True, 0.8))
    for s in (-1, 1):
        f.append(panel(f"ndf_p{s}", 6.2, 12, s * 12.8, front - 0.6, 0, -90, DARK, True, 0.8))
        f.append(panel(f"ndf_lw{s}a", 2.3, 8.5, s * 11.2, front - 0.1, 21, -90, GLASS, True, 0.3))
        f.append(panel(f"ndf_lw{s}b", 2.3, 8.5, s * 14.4, front - 0.1, 21, -90, GLASS, True, 0.3))
    f.append(box("ndf_kings", W, 0.6, 0.8, (0, front - 0.3, 15.2), shade(STONE, -0.08)))
    f.append(arcade("ndf_kingsarc", W - 2, 3.4, 28, (0, front - 0.15, 15.9), "S", shade(STONE, -0.35), False, 0.6, 0.3))
    f.append(box("ndf_kings2", W, 0.6, 0.6, (0, front - 0.3, 19.4), shade(STONE, -0.08)))
    f.append(rose("ndf_rose", 4.8, 0, front - 0.1, 26.5, "S"))
    f.append(arcade("ndf_gal", W - 2, 6.2, 16, (0, front - 0.15, 35.5), "S", DARK, True, 0.55, 0.4))
    f.append(box("ndf_galtop", W + 0.6, 12.6, 0.8, (0, front + 6, 42.6), shade(STONE, -0.05)))
    m.add(0, join(f, "nd_front"), "walls")
    t = []
    for s in (-1, 1):
        tx = s * 12.8
        t.append(box(f"ndt_{s}", 15.2, 14.5, 26, (tx, front + 7.25, 43), STONE))
        for xo in (-7.6, 7.6):
            t.append(box(f"ndt_cb{s}{xo}", 1.6, 1.6, 26, (tx + xo, front - 0.2, 43), shade(STONE, -0.05)))
        for k in (-1, 1):
            t.append(panel(f"ndt_bs{s}{k}", 2.6, 16, tx + k * 3.0, front - 0.1, 46.5, -90, DARK, True, 0.4))
            t.append(panel(f"ndt_bn{s}{k}", 2.6, 16, tx + k * 3.0, front + 14.6, 46.5, 90, DARK, True, 0.4))
            t.append(panel(f"ndt_bo{s}{k}", 2.6, 16, tx + s * 7.65, front + 7.25 + k * 3.0, 46.5, 0 if s > 0 else 180, DARK, True, 0.4))
        mm = merlons(f"ndt_m{s}", 15.2, 14.5, 69, 0.55, 0.65, STONE)
        t.append(move(mm, tx, front + 7.25, 0))
        for cx in (-6.9, 6.9):
            for cy in (-6.5, 6.5):
                t.append(pinnacle(f"ndt_pin{s}{cx}{cy}", 0.6, 3.2, tx + cx, front + 7.25 + cy, 69))
    t.append(box("ndt_screen", 10.4, 1.2, 4.5, (0, front + 0.6, 43), STONE))
    t.append(arcade("ndt_screenarc", 10, 3.6, 6, (0, front - 0.05, 43.3), "S", DARK, True, 0.55, 0.3))
    t.append(gable_wall("ndt_naveg", 13.5, 10.0, 1.0, 0, front + 13.5, 43, "S", STONE))
    m.add(2, join(t, "nd_towers"), "towers")
    if variant != "1789":
        m.add(3, spire("nd_spire", 0, 9, 40.5, 2.6, 47, 9.0, LEAD_P), "spire")
    return m


def saint_etienne():
    """The Merovingian cathedral group: Saint-Étienne, the old church of Notre-Dame, the baptistery."""
    m = Model("saint-etienne")
    m.add(0, plate(48, 128, GROUND), "ground")
    b = gothic_body("se", -58, 8, 12, 19, [(6, 12), (6, 8)], STONE_L, TILE_R, bay=6.5, flyers=False, buttress=False, round_win=True)
    m.add(0, join(b["walls"], "se_walls"), "walls")
    m.add(1, join(b["roofs"], "se_roofs"), "roofs")
    nar = [box("se_narthex", 36, 6, 8, (0, -61, 0), STONE_L), roof_x("se_narr", 36, 6, 2.5, 0, -61, 8, TILE_R)]
    nar.append(arcade("se_nara", 30, 5.5, 5, (0, -64.05, 0), "S", DARK, False, 0.6, 0.3))
    nar.append(box("se_belfry", 6, 6, 26, (0, -55, 0), STONE_L))
    nar.append(arcade("se_belfa", 5, 3, 2, (0, -58.05, 20), "S", DARK, False, 0.6, 0.3))
    nar.append(cylinder("se_belfr", 4.6, 4, (0, -55, 26), TILE_R, verts=4, r_top=0))
    m.add(1, join(nar, "se_narthex"), "roofs")
    nd = gothic_body("ond", 26, 54, 10, 14, [(5, 8)], STONE_L, TILE_R, bay=6, flyers=False, buttress=False, round_win=True)
    m.add(2, join(nd["walls"] + nd["roofs"], "old_nd"), "old church")
    m.add(2, join([cylinder("bap", 4.5, 8, (-19, 15, 0), STONE_L, verts=12), cylinder("bapr", 5, 4, (-19, 15, 8), TILE_R, verts=12, r_top=0),
                   house("bishop1", 16, 36, 10, 7, 8, PLAST, TILE_R, "x"), house("bishop2", 16, 22, 8, 6, 7, PLAST2, TILE_R, "x")], "baptistery"), "old church")
    return m


# ================================================================= Sainte-Chapelle
def sainte_chapelle():
    m = Model("sainte-chapelle")
    m.add(0, plate(18, 36, PAVE), "ground")
    y0, y1, w = -12.0, 10.0, 15.0
    lo = [box("sc_lower", w, y1 - y0, 7.0, (0, (y0 + y1) / 2, 0), STONE), cylinder("sc_lowapse", 7.5, 7.0, (0, y1, 0), STONE, verts=10)]
    for s in (-1, 1):
        for i in range(4):
            lo.append(panel(f"sc_lw{s}{i}", 1.6, 3.2, s * (w / 2 + 0.05), y0 + 2.75 + i * 5.5, 2.2, 0 if s > 0 else 180, GLASS, True))
    # porch, two storeys
    lo.append(box("sc_porch", w, 6, 13, (0, -15, 0), STONE))
    lo.append(panel("sc_pd", 4.4, 7.0, 0, -18.05, 0, -90, DARK, True, 0.5))
    lo.append(panel("sc_pu", 4.4, 5.4, 0, -18.05, 7.4, -90, DARK, True, 0.5))
    for s in (-1, 1):
        lo.append(panel(f"sc_ps{s}", 3.0, 5.0, s * (w / 2 + 0.05), -15, 7.4, 0 if s > 0 else 180, DARK, True, 0.4))
    lo.append(merlons("sc_pm", w, 6, 13, 0.45, 0.55, STONE))
    lo[-1] = move(lo[-1], 0, -15, 0)
    m.add(0, join(lo, "sc_lower"), "lower chapel")
    up = [box("sc_upper", w, y1 - y0, 24.0, (0, (y0 + y1) / 2, 7.0), STONE)]
    ap = cylinder("sc_upapse", 7.5, 24.0, (0, y1, 7.0), STONE, verts=10)
    up.append(ap)
    for s in (-1, 1):
        for i in range(4):
            yy = y0 + 2.75 + i * 5.5
            up.append(panel(f"sc_uw{s}{i}", 4.1, 15.5, s * (w / 2 + 0.05), yy, 9.5, 0 if s > 0 else 180, GLASS, True, 0.3))
            up.append(gable_wall(f"sc_wg{s}{i}", 4.8, 4.6, 0.5, s * (w / 2 - 0.1), yy, 30.6, "E", STONE))
            up.append(pinnacle(f"sc_wgp{s}{i}", 0.35, 1.6, s * (w / 2 - 0.1), yy, 35.0))
        for i in range(5):
            yy = y0 + i * 5.5
            up.append(box(f"sc_bt{s}{i}", 2.2, 1.4, 31, (s * (w / 2 + 1.0), yy, 0), shade(STONE, -0.05)))
            up.append(pinnacle(f"sc_btp{s}{i}", 0.9, 5.5, s * (w / 2 + 1.0), yy, 31))
    r = 7.5
    for j in range(5):
        a = math.radians(18 + 36 * j)
        d = r * math.cos(math.radians(18)) + 0.05
        up.append(panel(f"sc_aw{j}", 3.3, 15.5, d * math.cos(a), y1 + d * math.sin(a), 9.5, math.degrees(a), GLASS, True, 0.3))
        up.append(place(gable_wall(f"sc_ag{j}", 3.8, 4.0, 0.5, 0, 0, 0, "S", STONE), math.degrees(a) + 90, (d - 0.15) * math.cos(a), y1 + (d - 0.15) * math.sin(a), 30.6))
    for j in range(1, 5):
        a = math.radians(36 * j)
        px, py = (r + 0.9) * math.cos(a), y1 + (r + 0.9) * math.sin(a)
        up.append(place(box(f"sc_abt{j}", 2.2, 1.4, 31, (0, 0, 0), shade(STONE, -0.05)), math.degrees(a), px, py, 0))
        up.append(pinnacle(f"sc_abtp{j}", 0.9, 5.5, px, py, 31))
    up.append(box("sc_corn", w + 0.8, y1 - y0, 0.8, (0, (y0 + y1) / 2, 30.6), shade(STONE, -0.06)))
    up.append(cylinder("sc_acorn", 7.9, 0.8, (0, y1, 30.6), shade(STONE, -0.06), verts=10))
    up.append(rose("sc_rose", 4.2, 0, y0 - 0.1, 20.5, "S"))
    up.append(panel("sc_upd", 4.0, 6.0, 0, y0 - 0.1, 13.0, -90, DARK, True, 0.3))
    for s in (-1, 1):
        up.append(cylinder(f"sc_tur{s}", 1.7, 37, (s * 7.7, y0 - 0.6, 0), STONE, verts=8))
        up.append(cylinder(f"sc_turc{s}", 1.9, 7.5, (s * 7.7, y0 - 0.6, 37), LEAD_P, verts=8, r_top=0))
        up.append(cylinder(f"sc_turr{s}", 2.0, 0.7, (s * 7.7, y0 - 0.6, 36.3), shade(STONE, -0.06), verts=8))
    m.add(1, join(up, "sc_upper"), "upper chapel")
    rf = [roof_y("sc_roof", w, y1 - y0, 11.5, 0, (y0 + y1) / 2, 31.2, LEAD_P, 0.4)]
    rf.append(cylinder("sc_aroof", 7.9, 11.5, (0, y1, 31.2), LEAD_P, verts=10, r_top=0))
    rf.append(box("sc_crest", 0.25, y1 - y0, 0.5, (0, (y0 + y1) / 2, 42.6), GILT_P))
    rf.append(gable_wall("sc_wgab", w + 0.4, 11.0, 1.2, 0, y0 - 0.2, 31.2, "S", STONE))
    rf.append(rose("sc_rose2", 1.8, 0, y0 - 0.85, 36.0, "S"))
    rf.append(pinnacle("sc_wgabp", 0.7, 3.0, 0, y0 - 0.2, 41.8))
    m.add(2, join(rf, "sc_roof"), "roof")
    m.add(3, spire("sc_spire", 0, 2.0, 39.5, 2.1, 25.0, 10.0, LEAD_P), "spire")
    return m


# ================================================================= Palais de la Cité
def palais_cite(variant="1550"):
    m = Model("palais-cite")
    m.add(0, plate(150, 70, PAVE), "ground")
    if variant in ("1000", "1250"):
        m.add(0, curtain("pal_wall", [(-72, -33), (70, -33), (70, 33), (-72, 33), (-72, -33)], 7, 2.2, STONE), "walls")
        for i, (tx, ty) in enumerate([(-72, -33), (70, -33), (70, 33), (-72, 33), (0, -33), (0, 33)]):
            m.add(0, cylinder(f"pal_wt{i}", 3.2, 10, (tx, ty, 0), shade(STONE, -0.04), verts=12), "walls")
        keep = [box("pal_keep", 13, 13, 24, (28, 10, 0), STONE), hip("pal_keepr", 14, 14, 6, 28, 10, 24, SLATE_P, 0.1)]
        keep.append(windows("pal_keepw", 10, 3, 28, 3.45, 16, "S", 2.4, 0.4))
        m.add(2, join(keep, "pal_keep"), "keep")
        hall = [range_block("pal_hall", -12, 2, 44, 15, 12, STONE, SLATE_P, 9, "x", 2),
                range_block("pal_chap", 20, -17, 20, 8, 10, STONE, SLATE_P, 6, "x", 1),
                range_block("pal_lodge", 48, 10, 12, 30, 9, STONE, SLATE_P, 6, "y", 2)]
        hall.append(cylinder("pal_chapapse", 4, 10, (30, -17, 0), STONE, verts=12))
        hall.append(cylinder("pal_chapapr", 4.2, 4, (30, -17, 10), SLATE_P, verts=12, r_top=0))
        if variant == "1250":
            hall.append(range_block("pal_quai", -20, -25, 60, 12, 11, STONE, SLATE_P, 7, "x", 2))
            hall.append(cone_tower("pal_bonbec", 5.5, 17, -60, -27, 0, STONE, SLATE_P, 1.6))
            hall.append(range_block("pal_merc", 2, 24, 50, 10, 10, STONE, SLATE_P, 6, "x", 2))
        m.add(1, join(hall, "pal_halls"), "halls")
        m.add(1, join([tree(f"pal_tr{i}", 3.2, -66 + (i % 3) * 5, -18 + (i // 3) * 9) for i in range(9)], "pal_garden"), "halls")
        return m
    # Philip the Fair's palace (1300s) as it stood through the 16th–18th centuries
    q = [range_block("pal_quai", -2, -27, 116, 15, 13, STONE, SLATE_P, 8, "x", 2, dormers=0)]
    q.append(cone_tower("pal_bonbec", 5.6, 19, -63, -29, 0, STONE, SLATE_P, 1.6, merlons_top=False))
    q.append(cone_tower("pal_argent", 6.8, 24, -9, -30, 0, STONE, SLATE_P, 1.7))
    q.append(cone_tower("pal_cesar", 6.8, 24, 9, -30, 0, STONE, SLATE_P, 1.7))
    q.append(panel("pal_gate", 3.5, 6, 0, -34.6, 0, -90, DARK, True, 0.5))
    clock = [box("pal_horloge", 10, 10, 34, (66, -28, 0), STONE), hip("pal_horlr", 10.5, 10.5, 9, 66, -28, 34, SLATE_P, 0.05)]
    clock.append(box("pal_clock", 4.6, 0.4, 4.6, (66, -33.2, 15), GLAZE_BLUE))
    clock.append(disc("pal_clockd", 1.8, 66, -33.5, 17.3, "S", GILT_P, 0.2))
    clock.append(box("pal_clock2", 0.4, 4.6, 4.6, (71.2, -28, 15), GLAZE_BLUE))
    clock.append(cylinder("pal_bell", 1.4, 4, (66, -28, 43), LEAD_P, verts=8, r_top=0))
    clock.append(merlons("pal_horm", 10, 10, 34, 0.5, 0.6, STONE))
    clock[-1] = move(clock[-1], 66, -28, 0)
    q += clock
    m.add(0, join(q, "pal_quai"), "conciergerie")
    salle = [box("pal_salle", 70, 27, 15, (-6, -5, 0), STONE),
             roof_x("pal_salr1", 70, 13.5, 9, -6, -11.75, 15, SLATE_P, 0.3), roof_x("pal_salr2", 70, 13.5, 9, -6, 1.75, 15, SLATE_P, 0.3)]
    for s in (-1, 1):
        salle.append(gable_wall(f"pal_salg{s}a", 13.8, 9, 0.8, -6 + s * 34.8, -11.75, 15, "E", STONE))
        salle.append(gable_wall(f"pal_salg{s}b", 13.8, 9, 0.8, -6 + s * 34.8, 1.75, 15, "E", STONE))
    salle.append(windows("pal_salw", 64, 10, -6, 8.55, 5, "N", 6, 0.45, GLASS, True))
    m.add(1, join(salle, "pal_salle"), "great hall")
    rest = [range_block("pal_east", 52, 3, 14, 48, 14, STONE, SLATE_P, 8, "y", 2, faces=("E", "W")),
            range_block("pal_south", -8, 27, 92, 12, 12, STONE, SLATE_P, 7, "x", 2)]
    if variant == "1550":
        rest.append(box("pal_keep", 12, 12, 30, (30, 20, 0), STONE))
        rest.append(hip("pal_keepr", 12.5, 12.5, 8, 30, 20, 30, SLATE_P, 0.05))
        for cx in (-6, 6):
            for cy in (-6, 6):
                rest.append(cylinder(f"pal_kt{cx}{cy}", 1.6, 33, (30 + cx, 20 + cy, 0), STONE, verts=10))
                rest.append(cylinder(f"pal_ktc{cx}{cy}", 1.8, 4, (30 + cx, 20 + cy, 33), SLATE_P, verts=10, r_top=0))
    rest += [tree(f"pal_tr{i}", 3.0, -70 + (i % 2) * 5, -15 + (i // 2) * 8) for i in range(6)]
    m.add(1, join(rest, "pal_ranges"), "great hall")
    return m


# ================================================================= the Louvre
LX, LY = -35.0, -33.0     # the medieval castle sits in the south-west quarter of the Cour Carrée


def louvre_castle(grosse_tour=True, lescot=False, charles_v=False):
    parts_w, parts_t, parts_k = [], [], []
    W, D, H = 72, 78, 12
    x0, x1, y0, y1 = LX - W / 2, LX + W / 2, LY - D / 2, LY + D / 2
    parts_w.append(water_ring("lv_moat", W + 16, D + 16, 7, LX, LY))
    if lescot:
        pts = [(LX - 6, y0), (x1, y0), (x1, y1), (x0, y1), (x0, LY + 4)]
    else:
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    parts_w.append(curtain("lv_curtain", pts, H, 3.0, STONE))
    towers = [(x1, y0), (x1, y1), (x0, y1), (LX - 5, y0), (LX + 5, y0), (x1, LY - 5), (x1, LY + 5), (LX, y1)]
    if not lescot:
        towers += [(x0, y0), (x0, LY)]
    th = 20 if charles_v else 18
    for i, (tx, ty) in enumerate(towers):
        parts_t.append(cone_tower(f"lv_t{i}", 5.0, th, tx, ty, 0, STONE, SLATE_P, 2.0 if charles_v else 1.6))
    parts_w.append(panel("lv_gate", 3.6, 7, LX, y0 - 1.6, 0, -90, DARK, True, 0.6))
    parts_w.append(panel("lv_gatee", 3.6, 7, x1 + 1.6, LY, 0, 0, DARK, True, 0.6))
    # ranges inside the curtain
    parts_w.append(range_block("lv_rs", LX + (6 if lescot else 0), y0 + 7, W - 10 - (12 if lescot else 0), 9, 13, STONE, SLATE_P, 7 if charles_v else 5, "x", 2, faces=("N",)))
    parts_w.append(range_block("lv_rn", LX, y1 - 7, W - 10, 9, 13, STONE, SLATE_P, 7 if charles_v else 5, "x", 2, faces=("S",)))
    if charles_v:
        parts_w.append(range_block("lv_re", x1 - 7, LY, 9, D - 26, 14, STONE, SLATE_P, 7, "y", 3, dormers=4, faces=("W",)))
        parts_t.append(cone_tower("lv_vis", 3.2, 24, LX + 10, y1 - 13, 0, STONE, SLATE_P, 2.2, machicolation=False))
    if not lescot:
        parts_w.append(range_block("lv_rw", x0 + 7, LY, 9, D - 26, 13, STONE, SLATE_P, 7 if charles_v else 5, "y", 2, faces=("E",)))
    if grosse_tour:
        parts_w.append(ellipse_ring("lv_gtmoat", 13, 13, 0.72, 0.35, (LX, LY, 0), WATER_C, n=32))
        parts_k.append(cone_tower("lv_grosse", 7.5, 30, LX, LY, 0, STONE, SLATE_P, 1.7))
        parts_k.append(panel("lv_gtdoor", 1.8, 3.5, LX, LY - 7.55, 4, -90, DARK, True, 0.3))
        for k in range(3):
            parts_k.append(panel(f"lv_gtw{k}", 1.0, 2.2, LX + 7.55 * math.cos(math.radians(-60 + 60 * k)), LY + 7.55 * math.sin(math.radians(-60 + 60 * k)), 14 + 4 * k, -60 + 60 * k, DARK, False, 0.3))
    if lescot:
        ly = y0 + 24
        lw = [box("lv_lescot", 14, 48, 18, (x0 + 7, ly, 0), STONE_L)]
        lw.append(roof_y("lv_lescotr", 14, 48, 7, x0 + 7, ly, 18, SLATE_P, 0.3))
        for r, (z, hh) in enumerate([(1.5, 5.0), (7.5, 5.0), (13.5, 3.2)]):
            lw.append(windows(f"lv_lescotw{r}", 44, 9, x0 + 14.05, ly, z, "E", hh, 0.5, DARK, False))
            lw.append(windows(f"lv_lescotww{r}", 44, 9, x0 - 0.05, ly, z, "W", hh, 0.5, DARK, False))
        for yy in (-17, 0, 17):
            lw.append(box(f"lv_avant{yy}", 1.2, 7, 19.5, (x0 + 14.4, ly + yy, 0), STONE))
            lw.append(gable_wall(f"lv_avg{yy}", 7.4, 3.2, 1.2, x0 + 14.4, ly + yy, 19.5, "E", STONE))
        lw.append(box("lv_pavroi", 18, 18, 24, (x0 + 2, y0 + 2, 0), STONE_L))
        lw.append(hip("lv_pavroir", 18.5, 18.5, 10, x0 + 2, y0 + 2, 24, SLATE_P, 0.1))
        lw.append(windows("lv_pavroiw", 16, 4, x0 + 2, y0 - 7.05, 6, "S", 4, 0.4))
        lw.append(windows("lv_pavroiw2", 16, 4, x0 + 2, y0 - 7.05, 14, "S", 4, 0.4))
        parts_k += lw
        # scaffolding where the old west wing is coming down
        parts_k += [cylinder(f"lv_scaf{i}", 0.2, 16, (x0 + 4 + (i % 2) * 6, LY + 8 + (i // 2) * 7, 0), TIMBER_D, verts=4) for i in range(6)]
    return parts_w, parts_t, parts_k


def louvre(variant="1250"):
    m = Model("louvre-" + variant)
    m.add(0, plate(165, 165, GROUND), "ground")
    if variant in ("1250", "1550"):
        w, t, k = louvre_castle(grosse_tour=(variant == "1250"), lescot=(variant == "1550"), charles_v=(variant == "1550"))
        m.add(0, join(w, "lv_walls"), "walls")
        m.add(1, join(t, "lv_towers"), "towers")
        m.add(2, join(k, "lv_keep"), "keep")
        out = [house("lv_shed1", 40, 45, 26, 9, 6, PLAST2, SLATE_P, "x"), house("lv_shed2", 55, 18, 9, 24, 6, PLAST2, SLATE_P, "y"),
               house("lv_shed3", 25, 62, 18, 8, 5, PLAST2, SLATE_P, "x")]
        out += [tree(f"lv_tr{i}", 3.4, 10 + (i % 4) * 14, 20 + (i // 4) * 14) for i in range(8)]
        if variant == "1550":
            out += [box(f"lv_garden{i}", 22, 18, 0.4, (45 + (i % 2) * 24, -55 + (i // 2) * 21, 0), GRASS) for i in range(4)]
        m.add(1, join(out, "lv_outer"), "towers")
        return m
    # 1789: the Cour Carrée
    R, dep, H = 80.0, 24.0, 22.0
    w = []
    for s in (-1, 1):
        w.append(box(f"cc_ns{s}", 2 * R, dep, H, (0, s * (R - dep / 2), 0), STONE_L))
        w.append(box(f"cc_ew{s}", dep, 2 * R - 2 * dep, H, (s * (R - dep / 2), 0, 0), STONE_L))
    for f, (fx, fy) in (("S", (0, -R - 0.05)), ("N", (0, R + 0.05)), ("W", (-R - 0.05, 0))):
        for r, z in enumerate((2.0, 9.0, 15.5)):
            w.append(windows(f"cc_w{f}{r}", 2 * R - 8, 32, fx, fy, z, f, 4.2, 0.45, DARK, r == 0))
    for f, (fx, fy) in (("S", (0, -R + dep + 0.05)), ("N", (0, R - dep - 0.05)), ("W", (-R + dep + 0.05, 0)), ("E", (R - dep - 0.05, 0))):
        for r, z in enumerate((2.0, 9.0, 15.5)):
            w.append(windows(f"cc_i{f}{r}", 2 * R - 2 * dep - 6, 22, fx, fy, z, {"S": "N", "N": "S", "W": "E", "E": "W"}[f], 4.0, 0.45, DARK, r == 0))
    w.append(box("cc_court", 2 * R - 2 * dep, 2 * R - 2 * dep, 0.4, (0, 0, 0), PAVE))
    m.add(0, join(w, "cc_wings"), "wings")
    top = []
    for s in (-1, 1):
        top.append(box(f"cc_bal{s}", 2 * R + 0.6, 1.0, 1.4, (0, s * R, H), STONE))
        top.append(box(f"cc_bale{s}", 1.0, 2 * R, 1.4, (s * R, 0, H), STONE))
        top.append(box(f"cc_flat{s}", 2 * R - 2, dep - 2, 0.6, (0, s * (R - dep / 2), H), shade(LEAD_P, 0.2)))
        top.append(box(f"cc_flate{s}", dep - 2, 2 * R - 2 * dep, 0.6, (s * (R - dep / 2), 0, H), shade(LEAD_P, 0.2)))
    # roofed Lescot and Lemercier wings on the west side, the Pavillon de l'Horloge with its square dome
    top.append(hip("cc_wroof", dep, 2 * R - 10, 8, -R + dep / 2, 0, H + 1.4, SLATE_P, 0.85, 0.2))
    hz = [box("cc_horloge", 26, 30, 32, (-R + dep / 2, 0, 0), STONE_L)]
    hz.append(frustum("cc_hdome", 22, 26, 10, 12, 12, (-R + dep / 2, 0, 32), SLATE_P))
    hz.append(box("cc_hlant", 4, 4, 4, (-R + dep / 2, 0, 44), LEAD_P))
    hz.append(windows("cc_hw", 20, 3, -R - 1.05 + 0, 0, 23, "W", 6, 0.5, DARK, True))
    hz[-1] = move(hz[-1], 0, 0, 0)
    for s in (-1, 1):
        top.append(box(f"cc_pav{s}", 30, 28, 28, (0, s * (R - 12), 0), STONE_L))
        top.append(hip(f"cc_pavr{s}", 30, 28, 8, 0, s * (R - 12), 28, SLATE_P, 0.4))
    # Perrault's colonnade on the east front
    col = [box("cc_podium", 3.0, 2 * R - 10, 9.0, (R + 0.6, 0, 0), STONE)]
    cpos = []
    y = -R + 8
    while y < R - 7:
        if abs(y) > 12:
            cpos += [(R + 1.4, y - 0.9), (R + 1.4, y + 0.9)]
        y += 6.5
    col.append(columns("cc_cols", cpos, 0.55, 11.0, (0, 0, 9.0), STONE_L))
    col.append(box("cc_entab", 2.6, 2 * R - 10, 2.0, (R + 1.4, 0, 20.0), STONE_L))
    col.append(box("cc_cpav", 4.0, 22, 22, (R + 1.0, 0, 0), STONE_L))
    col.append(gable_wall("cc_ped", 22, 4.5, 1.2, R + 2.4, 0, 22, "E", STONE_L))
    m.add(1, join(top + hz + col, "cc_top"), "pavilions")
    return m


def tuileries():
    m = Model("tuileries")
    m.add(0, plate(36, 270, PAVE), "ground")
    w = [range_block("tu_s", 0, -63, 24, 76, 18, STONE_L, SLATE_P, 9, "y", 3, dormers=6, faces=("E", "W")),
         range_block("tu_n", 0, 63, 24, 76, 18, STONE_L, SLATE_P, 9, "y", 3, dormers=6, faces=("E", "W"))]
    m.add(0, join(w, "tu_wings"), "wings")
    p = []
    for yy, hh, rh in ((-120, 26, 12), (120, 26, 12), (-20, 22, 9), (20, 22, 9)):
        dd = 30 if abs(yy) > 100 else 12
        p.append(box(f"tu_pav{yy}", 34 if abs(yy) > 100 else 28, dd, hh, (0, yy, 0), STONE_L))
        p.append(hip(f"tu_pavr{yy}", 34 if abs(yy) > 100 else 28, dd, rh, 0, yy, hh, SLATE_P, 0.3))
        for f, sx in (("W", -1), ("E", 1)):
            p.append(windows(f"tu_pw{yy}{f}", dd - 4, max(2, int(dd / 5)), sx * ((34 if abs(yy) > 100 else 28) / 2 + 0.05), yy, hh * 0.35, f, hh * 0.25, 0.45))
    c = [box("tu_central", 32, 26, 26, (0, 0, 0), STONE_L), frustum("tu_dome", 26, 22, 12, 10, 14, (0, 0, 26), SLATE_P),
         box("tu_lant", 4, 4, 5, (0, 0, 40), LEAD_P), columns("tu_ccols", [(-16.8, y) for y in (-8, -4, 4, 8)] + [(16.8, y) for y in (-8, -4, 4, 8)], 0.6, 9, (0, 0, 0), STONE),
         panel("tu_cdoor", 4, 8, -16.05, 0, 0, 180, DARK, False, 0.4), panel("tu_cdoor2", 4, 8, 16.05, 0, 0, 0, DARK, False, 0.4)]
    m.add(1, join(p + c, "tu_pavilions"), "pavilions")
    return m


def grande_galerie():
    m = Model("grande-galerie")
    m.add(0, plate(250, 26, PAVE), "ground")
    g = [box("gg_body", 250, 20, 18, (0, 0, 0), STONE_L)]
    g.append(roof_x("gg_roof", 250, 20, 8, 0, 0, 18, SLATE_P, 0.4))
    for f, fy in (("S", -10.05), ("N", 10.05)):
        g.append(windows(f"gg_ground{f}", 240, 40, 0, fy, 1.0, f, 5.5, 0.5, DARK, True))
        g.append(windows(f"gg_upper{f}", 240, 40, 0, fy, 10.0, f, 5.5, 0.4, DARK, False))
    for i in range(20):
        x = -118 + i * 12.4
        g.append(box(f"gg_dorm{i}", 2.4, 2.0, 3.0, (x, -7.5, 18), STONE_L))
        g.append(gable_wall(f"gg_dormg{i}", 3.0, 2.0, 2.2, x, -7.5, 21, "S", STONE_L) if i % 2 else cylinder(f"gg_dormc{i}", 1.5, 1.5, (x, -7.5, 21), STONE_L, verts=8, r_top=0.2))
    m.add(0, join(g, "gg_gallery"), "gallery")
    m.add(1, join([box("gg_cornice", 251, 21, 0.8, (0, 0, 17.2), STONE)], "gg_cornice"), "roof")
    return m


# ================================================================= fortresses
def grand_chatelet():
    m = Model("grand-chatelet")
    m.add(0, plate(50, 40, PAVE), "ground")
    w = [box("gc_body", 40, 30, 14, (0, 2, 0), STONE), roof_x("gc_roof", 40, 30, 9, 0, 2, 14, SLATE_P)]
    w.append(box("gc_court", 20, 14, 0.5, (0, 4, 14.0), PAVE))
    w.append(panel("gc_pass", 5.0, 8.0, 0, -13.1, 0, -90, DARK, True, 0.6))
    w.append(panel("gc_passn", 5.0, 8.0, 0, 17.05, 0, 90, DARK, True, 0.6))
    w.append(windows("gc_w", 34, 7, 0, 17.05, 9, "N", 2.4, 0.35))
    m.add(0, join(w, "gc_body"), "walls")
    t = [cone_tower("gc_t1", 5.5, 22, -6.5, -14, 0, STONE, SLATE_P, 1.8), cone_tower("gc_t2", 5.5, 22, 6.5, -14, 0, STONE, SLATE_P, 1.8),
         cone_tower("gc_t3", 4.0, 18, -20, 14, 0, STONE, SLATE_P, 1.8), cone_tower("gc_t4", 4.0, 18, 20, 14, 0, STONE, SLATE_P, 1.8),
         cone_tower("gc_t5", 3.5, 17, -20, -10, 0, STONE, SLATE_P, 1.8)]
    t.append(box("gc_keep", 10, 10, 26, (14, 0, 0), STONE))
    t.append(hip("gc_keepr", 10.5, 10.5, 7, 14, 0, 26, SLATE_P, 0.1))
    t.append(box("gc_clock", 3.0, 0.3, 3.0, (14, -5.2, 17), GLAZE_BLUE))
    m.add(1, join(t, "gc_towers"), "towers")
    return m


def bastille():
    m = Model("bastille")
    m.add(0, plate(37, 68, GROUND), "ground")
    H = 22
    w = [box("ba_body", 26, 58, H, (0, 0, 0), STONE_D)]
    w.append(box("ba_court1", 18, 20, 0.5, (0, -14, H - 14), PAVE))
    w.append(merlons("ba_mer", 26, 58, H, 0.8, 0.9, STONE_D))
    w.append(panel("ba_gate", 3.2, 6, 0, -29.1, 0, -90, DARK, True, 0.5))
    w.append(windows("ba_wW", 50, 8, -13.05, 0, 9, "W", 1.6, 0.2))
    w.append(windows("ba_wE", 50, 8, 13.05, 0, 9, "E", 1.6, 0.2))
    w.append(box("ba_cross", 26, 8, H - 4, (0, 4, 0), shade(STONE_D, 0.05)))
    w.append(roof_x("ba_crossr", 24, 8, 3, 0, 4, H - 4, SLATE_P, 0.2))
    m.add(0, join(w, "ba_walls"), "walls")
    t = []
    for i, (tx, ty) in enumerate([(sx, sy) for sx in (-13, 13) for sy in (-29, -9.7, 9.7, 29)]):
        t.append(cylinder(f"ba_t{i}", 4.6, H + 1.5, (tx, ty, 0), STONE_D, verts=16))
        n = 10
        for k in range(n):
            a = math.tau * k / n
            t.append(box(f"ba_tm{i}_{k}", 1.0, 0.8, 1.1, (tx + 4.4 * math.cos(a), ty + 4.4 * math.sin(a), H + 1.5), STONE_D, rot_z=a))
        if i in (0, 3, 5):
            t.append(cylinder(f"ba_tc{i}", 2.2, 3.0, (tx, ty, H + 1.5), STONE_D, verts=10))
            t.append(cylinder(f"ba_tcr{i}", 2.5, 3.0, (tx, ty, H + 4.5), SLATE_P, verts=10, r_top=0))
    m.add(1, join(t, "ba_towers"), "towers")
    return m


def temple():
    m = Model("temple")
    m.add(0, plate(110, 110, GROUND), "ground")
    m.add(0, curtain("tp_wall", [(54, -54), (-54, -54), (-54, 54), (54, 54)], 8, 2.0, STONE), "walls")
    for i, (tx, ty) in enumerate([(54, -54), (-54, -54), (-54, 54), (0, -54), (-54, 0), (54, 54)]):
        m.add(0, cone_tower(f"tp_wt{i}", 3.0, 11, tx, ty, 0, STONE, SLATE_P, 1.6, machicolation=False), "walls")
    m.add(0, panel("tp_gate", 4, 6, 0, -55.2, 0, -90, DARK, True, 0.6), "walls")
    keep = [box("tp_keep", 14, 14, 40, (8, 12, 0), STONE)]
    for cx in (-7, 7):
        for cy in (-7, 7):
            keep.append(cylinder(f"tp_kt{cx}{cy}", 2.6, 44, (8 + cx, 12 + cy, 0), STONE, verts=12))
            keep.append(cylinder(f"tp_ktc{cx}{cy}", 2.9, 7, (8 + cx, 12 + cy, 44), SLATE_P, verts=12, r_top=0))
    keep.append(hip("tp_keepr", 14.5, 14.5, 9, 8, 12, 40, SLATE_P, 0.05))
    keep.append(merlons("tp_km", 14, 14, 40, 0.6, 0.7, STONE))
    keep[-1] = move(keep[-1], 8, 12, 0)
    for f, (fx, fy) in (("S", (8, 4.95)), ("E", (15.05, 12)), ("W", (0.95, 12))):
        for z in (12, 22, 31):
            keep.append(panel(f"tp_kw{f}{z}", 1.2, 2.6, fx, fy, z, {"S": -90, "E": 0, "W": 180}[f], DARK, True, 0.3))
    small = [box("tp_petite", 10, 8, 26, (8, 23, 0), STONE), hip("tp_petiter", 10.4, 8.4, 6, 8, 23, 26, SLATE_P, 0.2)]
    for cx in (-5, 5):
        small.append(cylinder(f"tp_pt{cx}", 1.8, 29, (8 + cx, 27, 0), STONE, verts=10))
        small.append(cylinder(f"tp_ptc{cx}", 2.0, 5, (8 + cx, 27, 29), SLATE_P, verts=10, r_top=0))
    m.add(2, join(keep + small, "tp_keep"), "keep")
    ch = [cylinder("tp_rot", 10, 13, (-22, -14, 0), STONE, verts=20), cylinder("tp_rotr", 10.5, 7, (-22, -14, 13), SLATE_P, verts=20, r_top=1.5),
          box("tp_choir", 24, 12, 13, (-1, -14, 0), STONE), roof_x("tp_choirr", 24, 12, 7, -1, -14, 13, SLATE_P), cylinder("tp_chap", 6, 13, (11, -14, 0), STONE, verts=12)]
    ch.append(windows("tp_rotw", 14, 5, -22, -24.05, 6, "S", 4, 0.4, GLASS, True))
    ch.append(campanile("tp_bell", 4, 20, (-8, -22, 0), STONE, "spire", SLATE_P))
    ch.append(range_block("tp_house", -30, 30, 40, 10, 10, STONE, SLATE_P, 6, "x", 2))
    ch += [tree(f"tp_tr{i}", 3.5, 25 + (i % 3) * 9, -30 + (i // 3) * 12) for i in range(9)]
    m.add(1, join(ch, "tp_church"), "church")
    return m


# ================================================================= abbeys and churches
def saint_germain():
    m = Model("saint-germain")
    m.add(0, plate(30, 85, PAVE), "ground")
    nave = gothic_body("sg_n", -33, 10, 10, 18, [(5.5, 9)], STONE, SLATE_P, bay=6.0, flyers=False, apse=False, round_win=True, buttress=False)
    choir = gothic_body("sg_c", 10, 30, 10, 20, [(5.5, 9), (2.5, 6)], STONE, SLATE_P, bay=5.5, flyers=True)
    m.add(0, join(nave["walls"] + choir["walls"], "sg_walls"), "walls")
    m.add(1, join(nave["roofs"] + choir["roofs"] + choir["butt"], "sg_roofs"), "roofs")
    tw = [box("sg_tower", 9, 9, 30, (0, -37, 0), STONE)]
    for f, (fx, fy, d) in (("S", (0, -41.55, -90)), ("E", (4.55, -37, 0)), ("W", (-4.55, -37, 180))):
        tw.append(panel(f"sg_tw{f}a", 1.5, 3.6, fx + (0.0 if f != "S" else -1.6), fy + (-1.2 if f != "S" else 0), 24, d, DARK, False, 0.3))
        tw.append(panel(f"sg_tw{f}b", 1.5, 3.6, fx + (0.0 if f != "S" else 1.6), fy + (1.2 if f != "S" else 0), 24, d, DARK, False, 0.3))
    tw.append(panel("sg_door", 3.0, 5.5, 0, -41.6, 0, -90, DARK, False, 0.5))
    tw.append(cylinder("sg_spire", 6.6, 16, (0, -37, 30), SLATE_P, verts=8, r_top=0))
    for s in (-1, 1):
        tw.append(box(f"sg_ct{s}", 5, 5, 27, (s * 7.5, 8, 0), STONE))
        tw.append(cylinder(f"sg_ctc{s}", 3.6, 5, (s * 7.5, 8, 27), SLATE_P, verts=4, r_top=0))
        tw.append(panel(f"sg_ctw{s}", 1.3, 3, s * 7.5, 5.45, 21, -90, DARK, False, 0.3))
    m.add(2, join(tw, "sg_towers"), "towers")
    return m


def sainte_genevieve_abbey():
    m = Model("sainte-genevieve")
    m.add(0, plate(84, 110, GROUND), "ground")
    b = gothic_body("sgv", -45, 30, 10, 20, [(6, 10)], STONE, SLATE_P, bay=6.5, flyers=False, transept=(10, 34, 10))
    b2 = [panel("sgv_door", 3.5, 6, 0, -45.1, 0, -90, DARK, True, 0.5), gable_wall("sgv_wg", 10.4, 7.8, 0.8, 0, -45.2, 20, "S", STONE),
          rose("sgv_rose", 2.6, 0, -45.3, 14, "S")]
    m.add(0, join(b["walls"] + b2, "sgv_walls"), "walls")
    m.add(1, join(b["roofs"] + b["butt"], "sgv_roofs"), "roofs")
    tw = [box("sgv_tower", 8, 8, 34, (13, 18, 0), STONE)]
    for f, d in (("S", -90), ("E", 0), ("N", 90), ("W", 180)):
        a = math.radians(d)
        tw.append(panel(f"sgv_tw{f}", 2.2, 6, 13 + 4.05 * math.cos(a), 18 + 4.05 * math.sin(a), 25, d, DARK, True, 0.3))
    tw.append(merlons("sgv_tm", 8, 8, 34, 0.5, 0.6, STONE))
    tw[-1] = move(tw[-1], 13, 18, 0)
    tw.append(cylinder("sgv_tsp", 5.6, 10, (13, 18, 34), SLATE_P, verts=4, r_top=0))
    tw[-1].rotation_euler[2] = math.pi / 4
    m.add(2, join(tw, "sgv_tower"), "tower")
    cl = []
    cx, cy = -27, 5
    for nm, x, y, w, d, ax in (("s", cx, cy - 16, 30, 7, "x"), ("n", cx, cy + 16, 30, 7, "x"), ("w", cx - 16, cy, 7, 39, "y")):
        cl.append(range_block("sgv_cl" + nm, x, y, w, d, 11, STONE, SLATE_P, 5, ax, 2))
    cl.append(box("sgv_garth", 22, 22, 0.4, (cx, cy, 0), GRASS))
    cl.append(range_block("sgv_abbot", -24, 40, 34, 10, 12, STONE, SLATE_P, 6, "x", 2, dormers=4))
    cl += [tree(f"sgv_tr{i}", 3.2, -35 + (i % 4) * 9, -40 + (i // 4) * 9) for i in range(8)]
    m.add(1, join(cl, "sgv_cloister"), "roofs")
    return m


def pantheon():
    m = Model("pantheon")
    m.add(0, plate(84, 110, PAVE), "ground")
    PS = "#E2D8C2"
    cy, H = 8.0, 25.0
    body = [box("pa_arm_y", 36, 84, H, (0, cy, 0), PS), box("pa_arm_x", 84, 36, H, (0, cy, 0), PS)]
    for s in (-1, 1):
        body.append(box(f"pa_cb{s}", 84, 36.6, 1.6, (0, cy, H), STONE))
        body.append(box(f"pa_cbb{s}", 36.6, 84, 1.6, (0, cy, H), STONE))
        body.append(windows(f"pa_wx{s}", 30, 4, s * 42.05, cy, 10, "E" if s > 0 else "W", 6, 0.35, DARK, True))
        body.append(windows(f"pa_wy{s}", 30, 4, 0, cy + s * 42.05, 10, "N" if s > 0 else "S", 6, 0.35, DARK, True))
    body.append(box("pa_roof", 34, 82, 0.8, (0, cy, H + 1.6), shade(LEAD_P, 0.25)))
    body.append(box("pa_roofx", 82, 34, 0.8, (0, cy, H + 1.6), shade(LEAD_P, 0.25)))
    m.add(0, join(body, "pa_body"), "walls")
    por = [box("pa_stylo", 44, 20, 1.6, (0, cy - 52, 0), STONE)]
    cpos = [(-18 + 7.2 * i, cy - 59) for i in range(6)] + [(-18 + 7.2 * i, cy - 52.5) for i in (0, 5)] + [(-18, cy - 46), (18, cy - 46)]
    por.append(columns("pa_cols", cpos, 1.0, 19.0, (0, 0, 1.6), PS))
    por.append(box("pa_entab", 42, 16, 3.2, (0, cy - 52.5, 20.6), PS))
    por.append(gable_wall("pa_ped", 43, 7.5, 16, 0, cy - 52.5, 23.8, "S", PS))
    por.append(roof_y("pa_pedr", 43, 16, 7.5, 0, cy - 52.5, 23.8, shade(LEAD_P, 0.25), 0.3))
    por.append(panel("pa_door", 5, 10, 0, cy - 42.05, 1.6, -90, DARK, False, 0.5))
    for i in range(3):
        por.append(box(f"pa_step{i}", 46 + 2 * i, 2.0, 0.55, (0, cy - 62.5 - i * 1.6 + 1.6, 0), STONE))
    m.add(1, join(por, "pa_portico"), "portico")
    dz = H + 2.4
    d = [cylinder("pa_drumbase", 19, 4, (0, cy, dz), PS, verts=40)]
    cols = [(17.5 * math.cos(math.tau * i / 32), cy + 17.5 * math.sin(math.tau * i / 32)) for i in range(32)]
    d.append(columns("pa_peri", cols, 0.65, 13.0, (0, 0, dz + 4), PS))
    d.append(cylinder("pa_drum", 14.5, 15.5, (0, cy, dz + 4), PS, verts=40))
    d.append(cylinder("pa_attic", 18.6, 2.6, (0, cy, dz + 17), PS, verts=40))
    d.append(cylinder("pa_attic2", 15.2, 4.0, (0, cy, dz + 19.6), PS, verts=40))
    d.append(dome("pa_dome", 14.5, (0, cy, dz + 23.4), shade(LEAD_P, 0.15), squash=1.05, segments=32, rings=14))
    d.append(cylinder("pa_lant", 2.6, 6, (0, cy, dz + 37.5), PS, verts=12))
    d.append(dome("pa_lantd", 2.8, (0, cy, dz + 43.5), shade(LEAD_P, 0.15), squash=1.3, segments=12, rings=6))
    d.append(cylinder("pa_cross", 0.25, 3.5, (0, cy, dz + 47), GILT_P, verts=4))
    m.add(2, join(d, "pa_dome"), "dome")
    return m


def sorbonne(variant="1789"):
    m = Model("sorbonne-" + variant)
    m.add(0, plate(70, 90, PAVE), "ground")
    if variant == "1550":
        r = [range_block("so_n", 0, 36, 60, 10, 11, STONE, SLATE_P, 6, "x", 2, dormers=6),
             range_block("so_e", 26, 6, 10, 50, 11, STONE, SLATE_P, 6, "y", 2, faces=("E", "W")),
             range_block("so_w", -26, 6, 10, 50, 11, PLAST, SLATE_P, 6, "y", 2, faces=("E", "W")),
             house("so_h1", -20, -32, 12, 10, 9, PLAST, SLATE_P, "y"), house("so_h2", 22, -32, 14, 10, 10, PLAST2, SLATE_P, "y")]
        m.add(0, join(r, "so_ranges"), "college")
        ch = gothic_body("so_ch", -20, 2, 9, 14, [], STONE, SLATE_P, bay=5.5, flyers=False, buttress=False)
        chw = [place(join(ch["walls"] + ch["roofs"], "so_chapel"), -90, 0, -22, 0)]
        chw.append(cylinder("so_flech", 0.9, 9, (0, -22, 20), LEAD_P, verts=6, r_top=0))
        m.add(1, join(chw, "so_chapel"), "chapel")
        return m
    r = [range_block("so_n", 0, 37, 66, 14, 16, STONE_L, SLATE_P, 8, "x", 3, dormers=8),
         range_block("so_e", 27, 4, 12, 52, 16, STONE_L, SLATE_P, 8, "y", 3, faces=("E", "W"), dormers=5),
         range_block("so_w", -27, 4, 12, 52, 16, STONE_L, SLATE_P, 8, "y", 3, faces=("E", "W"), dormers=5)]
    m.add(0, join(r, "so_ranges"), "college")
    # Lemercier's chapel along the south side, facade to the west, dome over the crossing
    ch = [box("so_cnave", 52, 16, 22, (-4, -32, 0), STONE_L), roof_x("so_cnr", 52, 16, 6, -4, -32, 22, SLATE_P),
          box("so_ctr", 16, 26, 22, (2, -32, 0), STONE_L), roof_y("so_ctrr", 16, 26, 6, 2, -32, 22, SLATE_P)]
    fx = -30.0
    ch.append(box("so_cfront", 1.6, 18, 28, (fx, -32, 0), STONE_L))
    ch.append(columns("so_ccol", [(fx - 1.2, -32 + d) for d in (-7, -3, 3, 7)], 0.5, 10, (0, 0, 0), STONE))
    ch.append(columns("so_ccol2", [(fx - 1.2, -32 + d) for d in (-4, 4)], 0.45, 9, (0, 0, 11), STONE))
    ch.append(gable_wall("so_cped", 10, 3.5, 1.4, fx - 0.6, -32, 28, "E", STONE_L))
    ch.append(panel("so_cdoor", 3, 6, fx - 0.85, -32, 0, 180, DARK, False, 0.4))
    ch.append(cylinder("so_drum", 6.5, 9, (2, -32, 22), STONE_L, verts=24))
    ch.append(windows("so_drumw", 8, 3, 2, -38.55, 24, "S", 4, 0.4, DARK, True))
    ch.append(dome("so_dome", 6.5, (2, -32, 31), SLATE_P, squash=1.5, segments=24, rings=10))
    ch.append(cylinder("so_lant", 1.4, 4.5, (2, -32, 40.5), STONE_L, verts=8))
    ch.append(cylinder("so_lantc", 1.6, 2.5, (2, -32, 45), LEAD_P, verts=8, r_top=0))
    m.add(1, join(ch, "so_chapel"), "chapel")
    return m


def hotel_de_ville(variant="1789"):
    m = Model("hotel-de-ville-" + variant)
    m.add(0, plate(80, 45, PAVE), "ground")
    H = 16
    new = []
    xs = (-40, 40) if variant == "1789" else (0, 40)
    w = xs[1] - xs[0]
    cx = (xs[0] + xs[1]) / 2
    new.append(box("hv_front", w, 14, H, (cx, -15.5, 0), STONE_L))
    new.append(box("hv_back", w, 10, H, (cx, 17.5, 0), STONE_L))
    new.append(box("hv_side", 10, 20, H, (xs[1] - 5, 1, 0), STONE_L))
    if variant == "1789":
        new.append(box("hv_side2", 10, 20, H, (xs[0] + 5, 1, 0), STONE_L))
    for r, z in enumerate((1.5, 7.5)):
        new.append(windows(f"hv_fw{r}", w - 4, int(w / 4), cx, -22.55, z, "S", 4.5, 0.42, DARK, r == 0))
    m.add(0, join(new, "hv_walls"), "walls")
    rf = [roof_x("hv_froof", w, 14, 10, cx, -15.5, H, SLATE_P), roof_x("hv_broof", w, 10, 8, cx, 17.5, H, SLATE_P)]
    nd = int(w / 6)
    for i in range(nd):
        x = xs[0] + 3 + i * (w - 6) / max(1, nd - 1)
        rf.append(box(f"hv_dorm{i}", 2.2, 1.6, 3.2, (x, -21.0, H), STONE_L))
        rf.append(gable_wall(f"hv_dormg{i}", 2.8, 2.2, 1.6, x, -21.0, H + 3.2, "S", STONE_L))
    for px in ((xs[0] + 5, xs[1] - 5) if variant == "1789" else (xs[1] - 5,)):
        rf.append(box(f"hv_pav{px}", 12, 45, H + 4, (px, 0, 0), STONE_L))
        rf.append(hip(f"hv_pavr{px}", 12.4, 45, 10, px, 0, H + 4, SLATE_P, 0.6))
        rf.append(windows(f"hv_pavw{px}", 10, 2, px, -22.55, 13.5, "S", 4.5, 0.4))
    if variant == "1789":
        bel = [box("hv_entry", 14, 2, 22, (0, -23, 0), STONE_L), panel("hv_door", 4, 7, 0, -24.05, 0, -90, DARK, False, 0.5),
               box("hv_camp", 6, 6, 10, (0, -16, H + 6), STONE_L), disc("hv_clock", 1.6, 0, -19.1, H + 10, "S", GLAZE_BLUE, 0.3),
               cylinder("hv_campd", 3.6, 5, (0, -16, H + 16), SLATE_P, verts=8, r_top=0.6), cylinder("hv_campf", 0.6, 3, (0, -16, H + 21), GILT_P, verts=6, r_top=0)]
        m.add(2, join(bel, "hv_belfry"), "belfry")
    else:
        old = [box("hv_old", 34, 18, 12, (-21, -10, 0), PLAST2), roof_y("hv_oldr", 34, 18, 9, -21, -10, 12, SLATE_P)]
        old.append(columns("hv_piliers", [(-36 + 5 * i, -19.6) for i in range(7)], 0.6, 4.5, (0, 0, 0), STONE))
        old.append(box("hv_oldarc", 34, 0.4, 4.5, (-21, -18.95, 0), DARK))
        old.append(windows("hv_oldw", 30, 6, -21, -19.05, 7, "S", 2.6, 0.45))
        old += [cylinder(f"hv_scaf{i}", 0.18, 20, (-1.5 + (i % 2) * 3, -23 + (i // 2) * 9, 0), TIMBER_D, verts=4) for i in range(8)]
        old.append(box("hv_scafp", 3.5, 30, 0.3, (0, -9, 12), TIMBER_D))
        old.append(box("hv_crane", 0.6, 0.6, 14, (8, 0, H + 1), TIMBER_D))
        old.append(box("hv_cranej", 12, 0.5, 0.5, (4, 0, H + 14), TIMBER_D))
        m.add(2, join(old, "hv_old"), "old house")
    m.add(1, join(rf, "hv_roofs"), "roofs")
    return m


# ================================================================= bridges
def stone_bridge(name, length, width, n_arches, deck_z, color=STONE, parapet=True, demilunes=False):
    """A masonry bridge along Y: a solid body with dark arch openings on both faces, cutwaters at the piers."""
    parts = [box(name + "_body", width, length, deck_z, (0, 0, 0), color)]
    span = length / n_arches
    for s in (-1, 1):
        for i in range(n_arches):
            y = -length / 2 + span * (i + 0.5)
            parts.append(panel(f"{name}_ar{s}{i}", min(span * 0.74, deck_z * 0.78 * 1.8), deck_z * 0.78, s * (width / 2 + 0.05), y, 0, 0 if s > 0 else 180, "#3C4648", False, 0.3))
        for i in range(1, n_arches):
            y = -length / 2 + span * i
            cw = prism(f"{name}_cw{s}{i}", [(0, -1.6), (s * 3.0, 0), (0, 1.6)] if s > 0 else [(0, 1.6), (s * 3.0, 0), (0, -1.6)], deck_z * 0.55, (s * width / 2, y, 0), shade(color, -0.06))
            parts.append(cw)
            if demilunes:
                parts.append(cylinder(f"{name}_dl{s}{i}", 3.2, deck_z + 1.2, (s * (width / 2 + 0.6), y, 0), color, verts=16))
    if parapet:
        for s in (-1, 1):
            parts.append(box(f"{name}_par{s}", 0.7, length, 1.1, (s * (width / 2 - 0.35), 0, deck_z), shade(color, 0.05)))
    parts.append(box(name + "_road", width - 1.4, length, 0.15, (0, 0, deck_z), PAVE))
    return join(parts, name)


def bridge_houses(name, length, deck_z, x_rows, depth, n, h_range=(11, 14), walls=(PLAST, PLAST2, "#E8D2B8"), roof=SLATE_P, uniform=False):
    out = []
    w = length / n
    for r, xr in enumerate(x_rows):
        for i in range(n):
            y = -length / 2 + w * (i + 0.5)
            h = h_range[0] if uniform else h_range[0] + ((i * 7 + r * 3) % 4) / 3 * (h_range[1] - h_range[0])
            col = walls[(i + r) % len(walls)]
            hs = house(f"{name}{r}_{i}", xr, y, depth, w * 0.97, h, col, roof, "x", w * 0.75 if uniform else None, timber=not uniform)
            out.append(move(hs, 0, 0, deck_z))
    return join(out, name)


def pont_notre_dame(houses=True):
    m = Model("pont-notre-dame")
    m.add(0, stone_bridge("pnd", 106, 22, 5, 9.0, STONE), "arches")
    if houses:
        m.add(1, bridge_houses("pnd_h", 96, 9.0, (-7.5, 7.5), 7, 30, (12, 12), (BRICK_P, STONE_L), SLATE_P, uniform=True), "houses")
        m.add(1, join([box(f"pnd_band{s}", 0.3, 96, 0.5, (s * 11.05, 0, 9 + 4.2), STONE_L) for s in (-1, 1)], "pnd_bands"), "houses")
    else:
        pump = [box("pnd_pump", 9, 10, 9, (-15.5, 40, 0), PLAST2), roof_y("pnd_pumpr", 9, 10, 4, -15.5, 40, 9, SLATE_P)]
        pump.append(disc("pnd_wheel", 3.5, -15.5, 33.5, 3.5, "S", TIMBER_D, 0.8, 12))
        pump.append(cylinder("pnd_pumpt", 1.2, 6, (-15.5, 40, 13), LEAD_P, verts=8, r_top=0))
        m.add(1, join(pump, "pnd_pump"), "pump")
    return m


def pont_au_change(stone=False):
    m = Model("pont-au-change")
    if stone:
        m.add(0, stone_bridge("pac", 110, 30, 7, 9.0, STONE), "arches")
        return m
    deck_z = 7.0
    piles = []
    span = 110 / 6
    for i in range(7):
        y = -55 + span * i
        for k in range(6):
            piles.append(cylinder(f"pac_pile{i}_{k}", 0.35, deck_z, (-13 + k * 5.2, y, 0), TIMBER_D, verts=6))
        piles.append(box(f"pac_cap{i}", 28, 1.2, 0.8, (0, y, deck_z - 0.8), TIMBER_D))
    piles.append(box("pac_deck", 28, 110, 1.0, (0, 0, deck_z - 0.2), TIMBER))
    for j, y in enumerate((-30, 12)):
        piles.append(house(f"pac_mill{j}", -18, y, 7, 6, 4, TIMBER, SLATE_P, "y", 2.5, False))
        piles[-1] = move(piles[-1], 0, 0, deck_z - 3)
        piles.append(disc(f"pac_wheel{j}", 3.0, -18, y - 3.6, 3.1, "S", TIMBER_D, 0.6, 12))
    m.add(0, join(piles, "pac_piers"), "piers")
    m.add(1, bridge_houses("pac_h", 104, deck_z, (-9.5, 9.5), 8, 22, (9, 13), (PLAST, PLAST2, "#E8D2B8"), SLATE_P), "houses")
    return m


def pont_neuf():
    m = Model("pont-neuf")
    south = place(stone_bridge("pn_s", 80, 20, 5, 10.0, STONE, True, True), 0, 0, -120, 0)
    north = place(stone_bridge("pn_n", 150, 20, 7, 10.0, STONE, True, True), 0, 0, 90, 0)
    mid = [box("pn_mid", 20, 95, 10.0, (0, -32.5, 0), STONE), box("pn_midroad", 18.6, 95, 0.15, (0, -32.5, 10.0), PAVE)]
    for s in (-1, 1):
        mid.append(box(f"pn_midpar{s}", 0.7, 95, 1.1, (s * 9.65, -32.5, 10.0), shade(STONE, 0.05)))
    m.add(0, join([south, north] + mid, "pn_arches"), "arches")
    st = [cylinder("pn_terre", 8.0, 10.0, (-9, -40, 0), STONE, verts=20), box("pn_ped", 3, 6, 4.5, (-11, -40, 10), STONE_L),
          box("pn_horse", 1.6, 4.2, 2.2, (-11, -40, 15.2), BRONZE), box("pn_horseleg", 1.4, 3.4, 0.7, (-11, -40, 14.5), BRONZE),
          box("pn_rider", 0.9, 0.9, 2.0, (-11, -40.2, 17.3), BRONZE), cylinder("pn_head", 0.55, 0.9, (-11, -38.0, 17.0), BRONZE, verts=8)]
    sam = [box("pn_sam", 9, 10, 12, (-15, 140, 0), PLAST2), hip("pn_samr", 9.4, 10.4, 4, -15, 140, 12, SLATE_P, 0.3),
           box("pn_samt", 3, 3, 5, (-15, 140, 16), STONE_L), cylinder("pn_samc", 2.0, 3.5, (-15, 140, 21), LEAD_P, verts=8, r_top=0),
           disc("pn_samclock", 1.4, -15, 134.9, 8, "S", GLAZE_BLUE, 0.3), panel("pn_samarch", 4, 6, -15, 134.95, 0.5, -90, DARK, False, 0.3)]
    m.add(1, join(st + sam, "pn_statue"), "statue")
    return m


def saint_jacques(variant="1550"):
    m = Model("saint-jacques-" + variant)
    m.add(0, plate(22, 55, PAVE), "ground")
    if variant == "1250":
        b = gothic_body("sjo", -18, 18, 9, 14, [(3.5, 8)], STONE, SLATE_P, bay=6, flyers=False)
        m.add(0, join(b["walls"], "sjo_walls"), "walls")
        m.add(1, join(b["roofs"] + b["butt"] + [gable_wall("sjo_wg", 9.4, 7, 0.8, 0, -18.2, 14, "S", STONE), panel("sjo_door", 2.6, 4.5, 0, -18.1, 0, -90, DARK, True, 0.4)], "sjo_roofs"), "roofs")
        m.add(2, campanile("sjo_bell", 4.5, 20, (-6.5, -21, 0), STONE, "spire", SLATE_P), "belfry")
        return m
    b = gothic_body("sjn", -17, 18, 9, 18, [(4.5, 10)], STONE, SLATE_P, bay=5.5, flyers=True)
    m.add(0, join(b["walls"] + [gable_wall("sjn_wg", 9.4, 7, 0.8, 4.5, -17.2, 18, "S", STONE)], "sjn_walls"), "walls")
    m.add(1, join(b["roofs"] + b["butt"], "sjn_roofs"), "roofs")
    tx, ty, s = -4.0, -22.0, 10.0
    t = [box("sjt_shaft", s, s, 50, (tx, ty, 0), STONE_L)]
    for cx in (-1, 1):
        for cy in (-1, 1):
            t.append(box(f"sjt_cb{cx}{cy}", 1.6, 1.6, 50, (tx + cx * (s / 2 - 0.2), ty + cy * (s / 2 - 0.2), 0), STONE))
            t.append(pinnacle(f"sjt_cp{cx}{cy}", 1.2, 7.0, tx + cx * (s / 2 - 0.2), ty + cy * (s / 2 - 0.2), 52))
    for f, d in (("S", -90), ("E", 0), ("N", 90), ("W", 180)):
        a = math.radians(d)
        for z, hh in ((14, 9), (31, 13)):
            t.append(panel(f"sjt_w{f}{z}", 3.2, hh, tx + (s / 2 + 0.05) * math.cos(a), ty + (s / 2 + 0.05) * math.sin(a), z, d, DARK, True, 0.3))
    t.append(box("sjt_balu", s + 1.2, s + 1.2, 2.0, (tx, ty, 50), STONE))
    t.append(merlons("sjt_m", s + 1.0, s + 1.0, 52, 0.5, 0.5, STONE))
    t[-1] = move(t[-1], tx, ty, 0)
    t.append(cylinder("sjt_stair", 1.6, 55, (tx + s / 2, ty + s / 2, 0), STONE_L, verts=8))
    t.append(cylinder("sjt_statue", 0.6, 3.5, (tx, ty, 52), STONE_L, verts=8))
    m.add(2, join(t, "sjt_tower"), "tower")
    return m


# ================================================================= markets and cemeteries
def open_hall(name, x, y, w, d, h, roof_h, roof=SLATE_P, post_every=5.0, axis="x"):
    parts = [box(name + "_in", w - 1.2, d - 1.2, h - 0.5, (x, y, 0), "#4A3F33")]
    L, D = (w, d) if axis == "x" else (d, w)
    n = int(L / post_every)
    for i in range(n + 1):
        t = -L / 2 + L * i / n
        for s in (-1, 1):
            px, py = (x + t, y + s * D / 2) if axis == "x" else (x + s * D / 2, y + t)
            parts.append(box(f"{name}_p{i}{s}", 0.7, 0.7, h, (px, py, 0), TIMBER))
    parts.append(box(name + "_plate", w, d, 0.6, (x, y, h - 0.6), TIMBER_D))
    parts.append(roof_x(name + "_r", w, d, roof_h, x, y, h, roof, 0.8) if axis == "x" else roof_y(name + "_r", w, d, roof_h, x, y, h, roof, 0.8))
    return join(parts, name)


def stall(name, x, y, color):
    return join([box(name + "_t", 3, 2, 1.0, (x, y, 0), TIMBER), box(name + "_a", 3.4, 2.6, 0.2, (x, y - 0.3, 2.2), color),
                 box(name + "_p", 0.15, 0.15, 2.2, (x - 1.5, y - 1.3, 0), TIMBER_D), box(name + "_p2", 0.15, 0.15, 2.2, (x + 1.5, y - 1.3, 0), TIMBER_D)], name)


def pillory(name, x, y):
    return join([cylinder(name + "_b", 3.0, 6.0, (x, y, 0), STONE, verts=8), cylinder(name + "_g", 3.2, 2.6, (x, y, 6.0), "#4A3F33", verts=8),
                 cylinder(name + "_r", 3.6, 4.0, (x, y, 8.6), SLATE_P, verts=8, r_top=0)], name)


def les_halles():
    m = Model("les-halles")
    m.add(0, plate(110, 70, PAVE), "ground")
    m.add(0, curtain("ha_wall", [(-54, -34), (54, -34), (54, 34), (-54, 34), (-54, -34)], 4, 1.2, STONE, merlon=False), "walls")
    m.add(1, join([open_hall("ha_h1", -8, 16, 86, 15, 7, 9), open_hall("ha_h2", -8, -4, 86, 15, 7, 9),
                   open_hall("ha_h3", 38, -22, 22, 12, 6, 7, axis="x")], "ha_halls"), "halls")
    cols = ["#A65238", "#C9A24A", "#5F7A8A", "#8A5A7A", "#7D9A6C"]
    st = [stall(f"ha_st{i}", -44 + (i % 10) * 7.5, -24 + (i // 10) * 5, cols[i % 5]) for i in range(20)]
    st.append(pillory("ha_pil", 44, 26))
    st.append(cylinder("ha_cross", 0.4, 7, (-46, 28, 0), STONE, verts=6))
    m.add(2, join(st, "ha_stalls"), "stalls")
    return m


def charnel(name, x, y, length, axis, inward):
    """An arcaded charnel gallery with a bone loft under a steep roof; `inward` = face of the arcade."""
    if axis == "x":
        parts = [box(name + "_b", length, 5, 7, (x, y, 0), STONE), roof_x(name + "_r", length, 5, 3.5, x, y, 7, SLATE_P, 0.3)]
        fy = y + (2.55 if inward == "N" else -2.55)
        parts.append(arcade(name + "_a", length - 2, 4.2, max(3, int(length / 3.5)), (x, fy, 0), inward, DARK, True, 0.65, 0.3))
    else:
        parts = [box(name + "_b", 5, length, 7, (x, y, 0), STONE), roof_y(name + "_r", 5, length, 3.5, x, y, 7, SLATE_P, 0.3)]
        fx = x + (2.55 if inward == "E" else -2.55)
        parts.append(arcade(name + "_a", length - 2, 4.2, max(3, int(length / 3.5)), (fx, y, 0), inward, DARK, True, 0.65, 0.3))
    return join(parts, name)


def innocents(variant="1550"):
    m = Model("innocents-" + variant)
    if variant == "1789":
        m.add(0, plate(100, 55, PAVE), "ground")
        f = [box("in_basin", 16, 16, 1.6, (0, 0, 0), STONE), box("in_basin2", 12, 12, 2.4, (0, 0, 1.6), STONE_L),
             box("in_fount", 8.5, 8.5, 9, (0, 0, 4.0), STONE_L)]
        for d in (-90, 0, 90, 180):
            a = math.radians(d)
            f.append(panel(f"in_fa{d}", 4.2, 6.5, 4.3 * math.cos(a), 4.3 * math.sin(a), 4.2, d, DARK, False, 0.3))
        f.append(box("in_fattic", 9.2, 9.2, 1.4, (0, 0, 13), STONE_L))
        f.append(dome("in_fdome", 4.6, (0, 0, 14.4), LEAD_P, squash=0.8, segments=16, rings=8))
        m.add(1, join(f, "in_fountain"), "fountain")
        cols = ["#A65238", "#C9A24A", "#5F7A8A", "#B04A3A", "#7D9A6C"]
        st = [stall(f"in_st{i}", -42 + (i % 12) * 7.5, (-20 if i < 12 else 20) + (0 if i < 12 else 0), cols[i % 5]) for i in range(24)]
        st += [join([cylinder(f"in_um{i}_p", 0.1, 2.6, (-30 + (i % 6) * 12, (-8 if i < 6 else 8), 0), TIMBER_D, verts=4),
                     cylinder(f"in_um{i}_c", 2.2, 0.8, (-30 + (i % 6) * 12, (-8 if i < 6 else 8), 2.6), "#B4432F" if i % 2 else "#C9A24A", verts=8, r_top=0)], f"in_um{i}") for i in range(12)]
        m.add(2, join(st, "in_market"), "market")
        return m
    m.add(0, plate(100, 55, "#B7AC86"), "ground")
    m.add(0, curtain("in_wall", [(-49, -26.5), (49, -26.5), (49, 26.5), (-49, 26.5), (-49, -26.5)], 4.5, 1.2, STONE, merlon=False), "walls")
    ch = gothic_body("in_ch", -10, 8, 8, 13, [], STONE, SLATE_P, bay=5, flyers=False, buttress=False)
    church = place(join(ch["walls"] + ch["roofs"], "in_church"), -90, 34, 19, 0)
    m.add(1, join([church, campanile("in_bell", 3.5, 20, (24, 19, 0), STONE, "spire", SLATE_P)], "in_church"), "church")
    lan = [cylinder("in_lantern", 0.9, 13, (-8, 4, 0), STONE, verts=8), cylinder("in_lant2", 1.2, 2.0, (-8, 4, 13), DARK, verts=8),
           cylinder("in_lantc", 1.3, 2.5, (-8, 4, 15), SLATE_P, verts=8, r_top=0), box("in_pulpit", 3, 3, 3, (6, -6, 0), STONE)]
    lan += [join([box(f"in_cr{i}", 0.3, 0.3, 1.8, (-35 + (i * 13) % 60, -15 + (i * 7) % 26, 0), STONE_D),
                  box(f"in_crb{i}", 1.1, 0.3, 0.3, (-35 + (i * 13) % 60, -15 + (i * 7) % 26, 1.2), STONE_D)], f"in_cross{i}") for i in range(14)]
    if variant == "1550":
        gal = [charnel("in_chS", 0, -23.5, 90, "x", "N"), charnel("in_chN", -12, 23.5, 66, "x", "S"), charnel("in_chW", -46, 0, 42, "y", "E")]
        f = [box("in_fount", 9, 5, 10, (45, -22, 0), STONE_L), hip("in_founr", 9.4, 5.4, 3, 45, -22, 10, LEAD_P, 0.2)]
        f.append(panel("in_fa1", 3.2, 6.5, 43, -24.55, 1.0, -90, DARK, False, 0.3))
        f.append(panel("in_fa2", 3.2, 6.5, 47, -24.55, 1.0, -90, DARK, False, 0.3))
        f.append(panel("in_fa3", 3.0, 6.5, 49.55, -22, 1.0, 0, DARK, False, 0.3))
        m.add(2, join(gal + f, "in_charnels"), "charnels")
    m.add(2, join(lan, "in_lantern"), "charnels")
    return m


# ================================================================= Roman Lutetia and Cluny
def roman_stripes(name, w, d, h, x, y, color=STONE_L, band=BRICK_P, every=2.4):
    parts = [box(name, w, d, h, (x, y, 0), color)]
    z = every
    while z < h - 0.5:
        parts.append(box(f"{name}_br{z:.0f}", w + 0.1, d + 0.1, 0.35, (x, y, z), band))
        z += every
    return join(parts, name)


def cluny_baths():
    m = Model("cluny-baths")
    m.add(0, plate(90, 70, PAVE), "ground")
    b = [roman_stripes("cb_frig", 22, 13, 15, 0, 14), roman_stripes("cb_tep", 18, 20, 12, -21, 14), roman_stripes("cb_cal", 20, 22, 13, 21, 14)]
    b.append(cylinder("cb_calap1", 5, 11, (31, 14, 0), STONE_L, verts=16))
    b.append(cylinder("cb_calap2", 4, 10, (21, 25, 0), STONE_L, verts=16))
    b.append(roman_stripes("cb_back", 70, 8, 9, 0, 29))
    for s in (-1, 1):
        b.append(panel(f"cb_win{s}", 4, 6, s * 6, 7.45, 6, -90, DARK, False, 0.3))
    m.add(0, join(b, "cb_halls"), "halls")
    r = [roof_x("cb_frigr", 22, 13, 5, 0, 14, 15, TILE_R), roof_y("cb_tepr", 18, 20, 5, -21, 14, 12, TILE_R), roof_y("cb_calr", 20, 22, 5, 21, 14, 13, TILE_R),
         cylinder("cb_ap1r", 5.2, 3, (31, 14, 11), TILE_R, verts=16, r_top=1), cylinder("cb_ap2r", 4.2, 3, (21, 25, 10), TILE_R, verts=16, r_top=1),
         roof_x("cb_backr", 70, 8, 3, 0, 29, 9, TILE_R)]
    m.add(1, join(r, "cb_roofs"), "roofs")
    p = [box("cb_pal", 60, 22, 0.4, (0, -14, 0), SAND)]
    pts = [(-30 + i * 4, -25) for i in range(16)] + [(-30 + i * 4, -3) for i in range(16)] + [(-31, -22 + i * 4) for i in range(5)] + [(31, -22 + i * 4) for i in range(5)]
    p.append(columns("cb_cols", pts, 0.4, 4.5, (0, 0, 0), STONE_L))
    for s in (-1, 1):
        p.append(roof_x(f"cb_portr{s}", 64, 3.5, 1.2, 0, -14 + s * 11, 4.8, TILE_R, 0.2))
    p.append(box("cb_shops", 84, 6, 4, (0, -32, 0), STONE_L))
    p.append(roof_x("cb_shopsr", 84, 6, 1.6, 0, -32, 4, TILE_R, 0.2))
    p.append(arcade("cb_shopa", 80, 3, 16, (0, -35.05, 0), "S", DARK, False, 0.6, 0.3))
    m.add(2, join(p, "cb_palaestra"), "palaestra")
    return m


def frigidarium(name, x, y, roofed=True, garden=False):
    parts = [roman_stripes(name + "_w", 22, 13, 14, x, y)]
    if roofed:
        parts.append(apply_rot(cylinder(name + "_v", 6.5, 22, (0, 0, -11), STONE_L, verts=16), ry=math.pi / 2))
        parts[-1] = move(parts[-1], x, y, 14 - 3.5)
        parts.append(box(name + "_vtop", 22, 13, 0.6, (x, y, 14), GRASS if garden else STONE_D))
    parts.append(panel(name + "_arch", 6, 9, x, y - 6.55, 0, -90, DARK, False, 0.3))
    return join(parts, name)


def cluny_ruins():
    m = Model("cluny-ruins")
    m.add(0, plate(90, 70, GROUND), "ground")
    m.add(0, frigidarium("cr_frig", 0, 14), "frigidarium")
    ruins = []
    for i, (x, y, w, d, h) in enumerate([(-21, 14, 18, 1.5, 7), (-30, 14, 1.5, 20, 5), (21, 4, 20, 1.5, 6), (31, 14, 1.5, 22, 9), (12, 25, 1.5, 6, 4),
                                         (-10, 29, 40, 1.5, 3), (-25, -3, 1.5, 12, 2), (20, -25, 30, 1.5, 2.5)]):
        ruins.append(roman_stripes(f"cr_r{i}", w, d, h, x, y))
    ruins += [tree(f"cr_tr{i}", 3.0, -35 + (i % 5) * 16, -20 + (i // 5) * 36) for i in range(8)]
    ruins += [box(f"cr_vine{i}", 22, 0.8, 1.2, (-15, -20 + i * 3, 0), LEAF) for i in range(4)]
    ruins.append(house("cr_hut", 30, -12, 8, 6, 5, PLAST2, THATCH, "x"))
    m.add(1, join(ruins, "cr_ruins"), "ruins")
    return m


def hotel_de_cluny():
    m = Model("hotel-de-cluny")
    m.add(0, plate(90, 70, PAVE), "ground")
    m.add(0, frigidarium("hc_frig", -30, 12, True, True), "frigidarium")
    h = [range_block("hc_main", 12, 18, 40, 11, 13, STONE_L, SLATE_P, 9, "x", 2, dormers=5, faces=("S",)),
         range_block("hc_east", 28, -2, 9, 30, 11, STONE_L, SLATE_P, 7, "y", 2, dormers=3, faces=("W",)),
         range_block("hc_west", -5, -2, 8, 24, 9, STONE_L, SLATE_P, 6, "y", 2, faces=("E",))]
    h.append(curtain("hc_cwall", [(-9, -18), (32, -18)], 6, 1.2, STONE_L))
    h.append(panel("hc_gate", 3.4, 5, 12, -18.7, 0, -90, DARK, True, 0.5))
    h.append(cone_tower("hc_stair", 3.0, 17, 12, 12.2, 0, STONE_L, SLATE_P, 2.0, machicolation=False))
    h.append(box("hc_chapel", 7, 7, 9, (36, 8, 0), STONE_L))
    h.append(cylinder("hc_oriel", 2.2, 4, (39.5, 8, 5), STONE_L, verts=6))
    h.append(cylinder("hc_orielr", 2.4, 3, (39.5, 8, 9), SLATE_P, verts=6, r_top=0))
    m.add(1, join(h, "hc_hotel"), "hôtel")
    m.add(2, join([tree(f"hc_tr{i}", 3.2, 20 + (i % 3) * 8, -30 + (i // 3) * 7) for i in range(6)] + [box("hc_lawn", 30, 14, 0.4, (25, -28, 0), GRASS)], "hc_garden"), "garden")
    return m


def arena():
    m = Model("arena")
    m.add(0, join([ellipse_disc("ar_base", 65, 50, 0.3, (0, 0, 0), GROUND, 48), ellipse_disc("ar_floor", 27, 24, 0.5, (0, 0, 0), SAND, 40)], "ar_ground"), "ground")
    tiers = []
    rx0, ry0 = 27, 24
    n = 6
    for i in range(n):
        a0 = rx0 + (63 - rx0) * i / n
        a1 = rx0 + (63 - rx0) * (i + 1) / n
        b0 = ry0 + (48 - ry0) * i / n
        b1 = ry0 + (48 - ry0) * (i + 1) / n
        outer, _ = ellipse_pts(a1, b1, 40, math.radians(260), math.radians(50))
        inner, _ = ellipse_pts(a0, b0, 40, math.radians(260), math.radians(50))
        tiers.append(ring_extrude(f"ar_tier{i}", outer, inner, 1.6 + i * 1.7, (0, 0, 0), STONE if i % 2 else STONE_L, closed=False))
    outer, _ = ellipse_pts(64, 49, 40, math.radians(260), math.radians(50))
    inner, _ = ellipse_pts(61, 46, 40, math.radians(260), math.radians(50))
    tiers.append(ring_extrude("ar_wall", outer, inner, 12.5, (0, 0, 0), STONE_D, closed=False))
    m.add(1, join(tiers, "ar_cavea"), "cavea")
    st = [box("ar_stage", 10, 40, 1.6, (34, 0, 0), STONE_L), box("ar_scaena", 5, 44, 12, (42, 0, 0), STONE_L)]
    for i in range(9):
        st.append(panel(f"ar_niche{i}", 2.6, 6, 39.45, -18 + i * 4.5, 2.5, 180, DARK, False, 0.3))
    st.append(roof_y("ar_scaenar", 5, 44, 2, 42, 0, 12, TILE_R, 0.3))
    for s in (-1, 1):
        st.append(panel(f"ar_vom{s}", 3.5, 4.5, 0, s * 24.5, 0, 90 if s > 0 else -90, DARK, False, 0.6))
    m.add(2, join(st, "ar_stage"), "stage")
    return m


def forum():
    m = Model("forum")
    m.add(0, plate(175, 90, PAVE), "ground")
    base, body, roof = mini_temple("fo_temple", 16, 26, 3.0, 11, 6, 0, (0, 0, 0), STONE_L, TILE_R)
    t = place(join([base, body, roof], "fo_temple"), 90, -62, 0, 0)    # facing east into the square
    court = []
    for s in (-1, 1):
        court.append(columns(f"fo_tc{s}", [(-84 + i * 4, s * 38) for i in range(11)], 0.45, 5.5, (0, 0, 0), STONE_L))
        court.append(box(f"fo_tcw{s}", 44, 3, 6.5, (-62, s * 41, 0), STONE_L))
        court.append(roof_x(f"fo_tcr{s}", 44, 6, 1.6, -62, s * 39.5, 6.0, TILE_R, 0.2))
    court.append(box("fo_tcwb", 3, 85, 6.5, (-86, 0, 0), STONE_L))
    m.add(1, join([t] + court, "fo_temple"), "temple")
    sq = []
    for s in (-1, 1):
        sq.append(columns(f"fo_c{s}", [(-34 + i * 4, s * 30) for i in range(23)], 0.45, 6.0, (0, 0, 0), STONE_L))
        sq.append(box(f"fo_shops{s}", 92, 10, 6.5, (12, s * 38, 0), STONE_L))
        sq.append(roof_x(f"fo_shopr{s}", 92, 18, 2.5, 12, s * 36, 6.5, TILE_R, 0.2))
        sq.append(arcade(f"fo_sha{s}", 88, 3.5, 18, (12, s * 32.95, 0), "N" if s < 0 else "S", DARK, False, 0.6, 0.3))
    sq.append(box("fo_altar", 4, 3, 1.5, (-20, 0, 0), STONE))
    sq.append(box("fo_statue", 1.6, 1.6, 4.5, (10, 0, 0), STONE_L))
    m.add(0, join(sq, "fo_square"), "square")
    bas = [box("fo_bas", 22, 76, 15, (74, 0, 0), STONE_L), roof_y("fo_basr", 22, 76, 5.5, 74, 0, 15, TILE_R, 0.4)]
    bas.append(columns("fo_basc", [(62.2, -34 + i * 4.25) for i in range(17)], 0.6, 8.0, (0, 0, 0), STONE_L))
    bas.append(windows("fo_basw", 70, 12, 62.95, 0, 9.5, "W", 3.5, 0.45, DARK, False))
    m.add(2, join(bas, "fo_basilica"), "basilica")
    return m


# ================================================================= Saint-Eustache, Place Royale, walls
def saint_eustache(variant="1789"):
    m = Model("saint-eustache-" + variant)
    m.add(0, plate(44, 105, PAVE), "ground")
    if variant == "1550":
        b = gothic_body("seu", 10, 30, 12, 33, [(7, 22), (6, 13)], STONE_L, SLATE_P, bay=6.5, flyers=False)
        w = b["walls"]
        m.add(0, join(w, "seu_walls"), "choir rising")
        sc = [cylinder(f"seu_sc{i}", 0.2, 36, (-8 + (i % 3) * 8, 6 + (i // 3) * 8, 0), TIMBER_D, verts=4) for i in range(9)]
        sc += [box(f"seu_scp{z}", 18, 20, 0.25, (0, 14, z), TIMBER_D) for z in (12, 24, 33)]
        sc.append(join([cylinder("seu_wheel", 2.5, 1.2, (0, 0, -0.6), TIMBER, verts=12)], "seu_wheel"))
        apply_rot(sc[-1], rx=math.pi / 2)
        sc[-1] = move(sc[-1], 12, -6, 2.5)
        sc.append(box("seu_mast", 0.6, 0.6, 30, (14, -6, 0), TIMBER_D))
        sc.append(box("seu_jib", 0.5, 14, 0.5, (14, 0, 30), TIMBER_D))
        sc += [house(f"seu_old{i}", -10 + i * 9, -30, 8, 18, 10, PLAST, SLATE_P, "y") for i in range(2)]
        sc.append(join([box("seu_oldch", 12, 30, 12, (6, -28, 0), STONE), roof_y("seu_oldchr", 12, 30, 7, 6, -28, 12, SLATE_P)], "seu_oldch"))
        m.add(1, join(sc, "seu_site"), "scaffolds")
        return m
    b = gothic_body("seu", -40, 30, 12, 33, [(7, 22), (6, 13)], STONE_L, SLATE_P, bay=6.5, flyers=True, transept=(-2, 44, 12))
    m.add(0, join(b["walls"], "seu_walls"), "walls")
    m.add(1, join(b["roofs"] + b["butt"], "seu_roofs"), "roofs")
    fr = [box("seu_front", 38, 8, 26, (0, -45, 0), STONE_L)]
    fr.append(columns("seu_fc1", [(x, -49.6) for x in (-8, -4, 4, 8)], 0.7, 11, (0, 0, 0), STONE_L))
    fr.append(columns("seu_fc2", [(x, -49.6) for x in (-6, -2, 2, 6)], 0.6, 9, (0, 0, 12), STONE_L))
    fr.append(box("seu_fent", 20, 2, 1.4, (0, -49.4, 11), STONE_L))
    fr.append(gable_wall("seu_fped", 16, 4, 1.6, 0, -49.0, 26, "S", STONE_L))
    fr.append(panel("seu_door", 4.5, 8, 0, -49.1, 0, -90, DARK, False, 0.5))
    fr.append(box("seu_ntower", 10, 8, 40, (-14, -45, 0), STONE_L))
    fr.append(frustum("seu_ntop", 9, 7, 6, 4, 6, (-14, -45, 40), STONE_L))
    fr.append(dome("seu_ntd", 2.4, (-14, -45, 46), LEAD_P, squash=1.4, segments=12, rings=6))
    fr.append(box("seu_stower", 10, 8, 30, (14, -45, 0), STONE_L))
    fr.append(panel("seu_nb", 3, 7, -14, -49.05, 28, -90, DARK, False, 0.3))
    m.add(2, join(fr, "seu_front"), "front")
    return m


def place_royale():
    m = Model("place-royale")
    m.add(0, plate(140, 140, PAVE), "ground")
    R, dep, H = 69.0, 13.0, 13.0
    houses = []
    n = 9
    for side in range(4):
        for i in range(n):
            t = -R + dep + (2 * R - 2 * dep) * (i + 0.5) / n
            if side == 0:
                x, y, ax = t, -R + dep / 2, "x"
            elif side == 1:
                x, y, ax = t, R - dep / 2, "x"
            elif side == 2:
                x, y, ax = -R + dep / 2, t, "y"
            else:
                x, y, ax = R - dep / 2, t, "y"
            if side < 2 and i == n // 2:
                continue
            w = (2 * R - 2 * dep) / n
            bw, bd = (w * 0.99, dep) if ax == "x" else (dep, w * 0.99)
            hs = [box(f"pr_h{side}_{i}", bw, bd, H, (x, y, 0), BRICK_P)]
            hs.append(box(f"pr_q{side}_{i}", bw + 0.1, bd + 0.1, 4.2, (x, y, 0), STONE_L))
            hs.append(box(f"pr_c{side}_{i}", bw + 0.15, bd + 0.15, 0.5, (x, y, 8.2), STONE_L))
            hs.append(hip(f"pr_r{side}_{i}", bw, bd, 7, x, y, H, SLATE_P, 0.35, 0.2))
            houses.append(join(hs, f"pr_house{side}_{i}"))
    for c, (cx, cy) in enumerate([(-R + dep / 2, -R + dep / 2), (R - dep / 2, -R + dep / 2), (R - dep / 2, R - dep / 2), (-R + dep / 2, R - dep / 2)]):
        houses.append(join([box(f"pr_cor{c}", dep, dep, H, (cx, cy, 0), BRICK_P), box(f"pr_corq{c}", dep + 0.1, dep + 0.1, 4.2, (cx, cy, 0), STONE_L),
                            hip(f"pr_corr{c}", dep, dep, 7, cx, cy, H, SLATE_P, 0.1, 0.2)], f"pr_corner{c}"))
    arc = []
    inner = R - dep
    for f, (fx, fy) in (("N", (0, -inner - 0.05)), ("S", (0, inner + 0.05)), ("E", (-inner - 0.05, 0)), ("W", (inner + 0.05, 0))):
        arc.append(arcade(f"pr_arc{f}", 2 * inner - 4, 3.8, 36, (fx, fy, 0), f, DARK, False, 0.7, 0.3))
        arc.append(windows(f"pr_win{f}", 2 * inner - 4, 36, fx, fy, 5.5, f, 2.2, 0.4))
    for f, (fx, fy) in (("S", (0, -R - 0.05)), ("N", (0, R + 0.05)), ("W", (-R - 0.05, 0)), ("E", (R + 0.05, 0))):
        for z in (5.0, 9.0):
            arc.append(windows(f"pr_ow{f}{z:.0f}", 2 * R - 6, 40, fx, fy, z, f, 2.2, 0.4))
    m.add(0, join(houses + arc, "pr_houses"), "houses")
    pav = []
    for s, nm in ((-1, "roi"), (1, "reine")):
        y = s * (R - dep / 2)
        pav += [box(f"pr_{nm}", 16, dep + 2, 20, (0, y, 0), BRICK_P), box(f"pr_{nm}q", 16.1, dep + 2.1, 4.5, (0, y, 0), STONE_L),
                hip(f"pr_{nm}r", 16.4, dep + 2.4, 11, 0, y, 20, SLATE_P, 0.2, 0.3),
                panel(f"pr_{nm}arch", 5, 4.4, 0, y + s * (dep / 2 + 1.05), 0, 90 if s > 0 else -90, DARK, False, 0.4),
                panel(f"pr_{nm}archi", 5, 4.4, 0, y - s * (dep / 2 + 1.05), 0, -90 if s > 0 else 90, DARK, False, 0.4)]
    m.add(1, join(pav, "pr_pavilions"), "pavilions")
    g = [box("pr_lawn", 96, 96, 0.4, (0, 0, 0), GRASS)]
    g.append(water_ring("pr_rail", 98, 98, 0.5, 0, 0, DARK))
    g[-1].scale[2] = 4.0
    for i in range(24):
        a = math.tau * i / 24
        g.append(tree(f"pr_tr{i}", 2.6, 40 * math.cos(a), 40 * math.sin(a)))
    g += [box("pr_ped", 3, 6, 3.5, (0, 0, 0), STONE_L), box("pr_horse", 1.5, 4, 2, (0, 0, 4.2), BRONZE), box("pr_legs", 1.3, 3.2, 0.7, (0, 0, 3.5), BRONZE),
          box("pr_rider", 0.9, 0.9, 1.9, (0, 0.2, 6.2), BRONZE)]
    m.add(2, join(g, "pr_garden"), "garden")
    return m


def tour_de_nesle():
    m = Model("tour-de-nesle")
    m.add(0, plate(26, 26, GROUND), "ground")
    m.add(0, curtain("tn_wall", [(0, -2), (0, -13)], 8, 2.5, STONE), "wall")
    t = [cone_tower("tn_tower", 5.2, 25, 0, 2, 0, STONE, SLATE_P, 1.5, machicolation=True, merlons_top=False),
         cone_tower("tn_stair", 2.2, 31, 4.6, -1.5, 0, STONE, SLATE_P, 2.4, machicolation=False)]
    for z in (6, 12, 18):
        t.append(panel(f"tn_w{z}", 0.9, 2.0, 0, 2 - 5.25, z, -90, DARK, True, 0.3))
    m.add(1, join(t, "tn_tower"), "tower")
    return m


def philippe_wall():
    m = Model("philippe-wall")
    m.add(0, plate(20, 110, GROUND), "ground")
    m.add(0, curtain("pw_wall", [(0, -55), (0, 55)], 8, 3.0, STONE), "wall")
    m.add(0, box("pw_walk", 1.6, 110, 0.4, (1.8, 0, 7.6), STONE_D), "wall")
    t = []
    for i, y in enumerate((-22, 34)):
        t.append(cylinder(f"pw_t{i}", 3.8, 11, (-1.2, y, 0), STONE, verts=16))
        n = 9
        for k in range(n):
            a = math.pi / 2 + math.pi * k / (n - 1)
            t.append(box(f"pw_tm{i}{k}", 0.9, 0.7, 1.1, (-1.2 + 3.6 * math.cos(a), y + 3.6 * math.sin(a), 11), STONE, rot_z=a))
        t.append(panel(f"pw_tw{i}", 0.6, 1.8, -5.05, y, 5, 180, DARK, False, 0.3))
    t += [house(f"pw_hut{i}", 6.5, -40 + i * 26, 6, 9, 6, PLAST, SLATE_P, "y") for i in range(3)]
    m.add(1, join(t, "pw_towers"), "towers")
    return m


BUILDERS = {
    "paris/notre-dame": notre_dame,
    "paris/notre-dame-1789": lambda: notre_dame("1789"),
    "paris/saint-etienne": saint_etienne,
    "paris/sainte-chapelle": sainte_chapelle,
    "paris/palais-cite": palais_cite,
    "paris/palais-cite-1250": lambda: palais_cite("1250"),
    "paris/palais-cite-capetian": lambda: palais_cite("1000"),
    "paris/louvre-fortress": lambda: louvre("1250"),
    "paris/louvre-1550": lambda: louvre("1550"),
    "paris/louvre-1789": lambda: louvre("1789"),
    "paris/tuileries": tuileries,
    "paris/grande-galerie": grande_galerie,
    "paris/grand-chatelet": grand_chatelet,
    "paris/bastille": bastille,
    "paris/temple": temple,
    "paris/saint-germain": saint_germain,
    "paris/sainte-genevieve-abbey": sainte_genevieve_abbey,
    "paris/pantheon": pantheon,
    "paris/sorbonne-college": lambda: sorbonne("1550"),
    "paris/sorbonne": sorbonne,
    "paris/hotel-de-ville": hotel_de_ville,
    "paris/hotel-de-ville-1550": lambda: hotel_de_ville("1550"),
    "paris/pont-notre-dame": pont_notre_dame,
    "paris/pont-notre-dame-1789": lambda: pont_notre_dame(False),
    "paris/pont-au-change": pont_au_change,
    "paris/pont-au-change-1789": lambda: pont_au_change(True),
    "paris/pont-neuf": pont_neuf,
    "paris/saint-jacques": saint_jacques,
    "paris/saint-jacques-old": lambda: saint_jacques("1250"),
    "paris/les-halles": les_halles,
    "paris/innocents-1250": lambda: innocents("1250"),
    "paris/innocents": innocents,
    "paris/innocents-1789": lambda: innocents("1789"),
    "paris/cluny-baths": cluny_baths,
    "paris/cluny-ruins": cluny_ruins,
    "paris/hotel-de-cluny": hotel_de_cluny,
    "paris/arena": arena,
    "paris/forum": forum,
    "paris/saint-eustache-1550": lambda: saint_eustache("1550"),
    "paris/saint-eustache": saint_eustache,
    "paris/place-royale": place_royale,
    "paris/tour-de-nesle": tour_de_nesle,
    "paris/philippe-wall": philippe_wall,
}
