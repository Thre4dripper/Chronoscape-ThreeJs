"""The imperial fora, rebuilt as proper ensembles that match their content footprints.
Local frame: +Y is the far (temple / basilica) end, -Y the entrance. Metres."""
import math
from chronokit import *

MARBLE, PLAZA, SAND = "marble", "plaza", "#C8A574"


def lean_to(name, x_in, x_out, y0, y1, h_in, h_out, z=0.0, color="terracotta"):
    """Single-pitch portico roof sloping down toward the open plaza (x_in)."""
    v = [(x_in, y0, z + h_in), (x_out, y0, z + h_out), (x_out, y1, z + h_out), (x_in, y1, z + h_in),
         (x_in, y0, z + h_in - 0.5), (x_out, y0, z + h_out - 0.5), (x_out, y1, z + h_out - 0.5), (x_in, y1, z + h_in - 0.5)]
    f = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    return mesh_from(name, v, f, (0, 0, 0), color)


def portico(m, name, x_in, x_out, y0, y1, col_h=11.0, stage=1, roof=True, cols=True, base_z=0.4):
    """A colonnaded portico running along y: back wall at x_out, columns at x_in."""
    s = 1 if x_out > x_in else -1
    m.add(stage, box(f"{name}_wall", 1.6, y1 - y0, col_h + 3, (x_out - s * 0.8, (y0 + y1) / 2, base_z), MARBLE))
    m.add(stage, box(f"{name}_floor", abs(x_out - x_in), y1 - y0, 0.6, ((x_in + x_out) / 2, (y0 + y1) / 2, base_z), shade(MARBLE, -0.06)))
    if cols:
        n = max(2, int((y1 - y0) / 4.6))
        pts = [(x_in, y0 + 2 + (y1 - y0 - 4) * i / (n - 1)) for i in range(n)]
        m.add(stage, columns(f"{name}_cols", pts, 0.65, col_h, (0, 0, base_z + 0.6), MARBLE))
        m.add(stage, box(f"{name}_ent", 1.6, y1 - y0, 1.2, (x_in, (y0 + y1) / 2, base_z + 0.6 + col_h + 0.3), shade(MARBLE, 0.05)))
    if roof:
        m.add(2, lean_to(f"{name}_roof", x_in - s * 1.2, x_out, y0, y1, col_h + 2.4, col_h + 4.2, base_z, shade("terracotta", -0.08)))


def exedra(m, name, cx, cy, r, side, h=13.0, stage=1):
    """Semicircular hall opening onto the portico, bulging outward on `side` (+1 east, -1 west)."""
    start = -math.pi / 2 if side > 0 else math.pi / 2
    m.add(stage, ellipse_ring(f"{name}_wall", r, r, (r - 1.6) / r, h, (cx, cy, 0.4), MARBLE, arc=math.pi, start=start))
    m.add(stage, ellipse_ring(f"{name}_floor", r - 1.6, r - 1.6, 0.02, 0.6, (cx, cy, 0.4), shade(MARBLE, -0.06), arc=math.pi, start=start))
    m.add(2, ellipse_ring(f"{name}_roof", r + 0.6, r + 0.6, 0.55, 1.0, (cx, cy, 0.4 + h), shade("terracotta", -0.08), arc=math.pi, start=start))


def equestrian(m, x, y, stage=2, quadriga=False):
    m.add(stage, box("statue_base", 4, 7 if not quadriga else 9, 3, (x, y, 0.4), MARBLE))
    if quadriga:
        for i in range(4):
            m.add(stage, box(f"horse{i}", 0.8, 2.4, 1.6, (x - 1.5 + i, y - 1.5, 3.4), "bronze"))
        m.add(stage, box("chariot", 2.4, 1.6, 1.4, (x, y + 1.6, 3.4), "bronze"))
    else:
        m.add(stage, box("horse", 1.2, 3.6, 2.2, (x, y, 3.4), "bronze"))
        m.add(stage, cylinder("rider", 0.5, 1.6, (x, y + 0.2, 5.6), "bronze", verts=8))


def crane(name, x, y, h=16):
    """A treadwheel crane: A-frame, jib and wheel."""
    parts = [box(f"{name}_leg1", 0.5, 0.5, h, (x - 1.5, y, 0.4), "timber"), box(f"{name}_leg2", 0.5, 0.5, h, (x + 1.5, y, 0.4), "timber"),
             box(f"{name}_jib", 0.4, 9, 0.4, (x, y + 4, h), "timber")]
    w = cylinder(f"{name}_wheel", 2.4, 0.6, (0, 0, 0), "timber", verts=12)
    w.rotation_euler = (0, math.pi / 2, 0)
    bpy.ops.object.select_all(action="DESELECT"); w.select_set(True); bpy.context.view_layer.objects.active = w
    bpy.ops.object.transform_apply(rotation=True)
    w.location = (x, y - 2, 2.8)
    bpy.ops.object.transform_apply(location=True)
    return join(parts + [w], name)


def scaffold(name, x0, x1, y0, y1, h):
    poles = []
    for x in (x0, x1):
        for k in range(int((y1 - y0) / 4) + 1):
            poles.append(box(f"{name}_p{x:.0f}{k}", 0.3, 0.3, h, (x, y0 + k * 4, 0.4), "timber"))
    for y in (y0, y1):
        for k in range(int((x1 - x0) / 4) + 1):
            poles.append(box(f"{name}_q{y:.0f}{k}", 0.3, 0.3, h, (x0 + k * 4, y, 0.4), "timber"))
    for z in range(4, int(h), 4):
        poles.append(box(f"{name}_d{z}a", x1 - x0, 0.25, 0.25, ((x0 + x1) / 2, y0, z), "timber"))
        poles.append(box(f"{name}_d{z}b", 0.25, y1 - y0, 0.25, (x0, (y0 + y1) / 2, z), "timber"))
    return join(poles, name)


def stone_stack(name, x, y, n=6):
    return join([box(f"{name}_{i}", 3.0, 1.6, 1.2, (x + (i % 3) * 3.3, y + (i // 3) * 2.0, 0.4), MARBLE) for i in range(n)], name)


# ---------------------------------------------------------------- Forum of Trajan
def forum_of_trajan(construction=False):
    m = Model("forum-of-trajan" + ("-construction" if construction else ""))
    W, D = 185, 300
    px, py0, py1 = 59, -150, -40        # plaza half-width and y extent
    m.add(0, box("plaza", px * 2, py1 - py0, 0.4, (0, (py0 + py1) / 2, 0), SAND if construction else PLAZA), "plaza")
    m.add(0, box("precinct", W, D, 0.2, (0, 0, 0), shade(PLAZA, -0.05)))
    # porticoes along both long sides, exedrae behind them
    for s in (-1, 1):
        if construction and s > 0:
            m.add(1, box("portico_e_footing", 15, py1 - py0, 1.2, (s * (px + 7.5), (py0 + py1) / 2, 0.4), MARBLE), "porticoes")
        else:
            portico(m, f"portico{s}", s * px, s * (px + 15), py0, py1, cols=True, roof=not construction)
        exedra(m, f"exedra{s}", s * (px + 15), (py0 + py1) / 2, 22, s, h=13 if not construction or s < 0 else 6)
    # entrance at the south: a triple gateway with a central arch
    m.add(1, box("gate_l", 40, 6, 14, (-36, py0 - 3, 0.4), MARBLE))
    m.add(1, box("gate_r", 40, 6, 14, (36, py0 - 3, 0.4), MARBLE))
    if not construction:
        m.add(1, box("gate_arch_top", 32, 6, 6, (0, py0 - 3, 12.4), MARBLE))
        m.add(2, box("gate_attic", 32, 6, 3, (0, py0 - 3, 18.4), shade(MARBLE, 0.05)))
        m.add(2, box("gate_quadriga", 6, 3, 3, (0, py0 - 3, 21.4), "bronze"))
        equestrian(m, 0, (py0 + py1) / 2)
    # Basilica Ulpia: across the north end of the plaza, with apses at both ends
    by0, by1 = py1, py1 + 60
    bl = 170
    if construction:
        m.add(1, box("basilica_walls_n", bl, 2, 9, (0, by1 - 1, 0.4), "brick"), "basilica")
        m.add(1, box("basilica_walls_s", bl, 2, 6, (0, by0 + 1, 0.4), "brick"))
        m.add(1, columns("basilica_cols_built", [(-60 + 12 * i, by0 + 12) for i in range(6)], 0.9, 12, (0, 0, 0.4), MARBLE))
        m.add(2, scaffold("basilica_scaffold", -10, 70, by0 + 6, by1 - 6, 18), "site")
        m.add(2, crane("crane1", -30, by0 + 30, 22))
        m.add(2, crane("crane2", 45, by0 + 22, 18))
    else:
        m.add(1, box("basilica_floor", bl, by1 - by0, 1.2, (0, (by0 + by1) / 2, 0.4), shade(MARBLE, -0.05)), "basilica")
        m.add(1, columns("basilica_cols", peristyle(bl - 12, by1 - by0 - 10, 18, 5), 1.0, 14, (0, (by0 + by1) / 2, 1.6), MARBLE))
        m.add(1, box("basilica_clerestory", bl - 30, by1 - by0 - 26, 22, (0, (by0 + by1) / 2, 1.6), shade(MARBLE, -0.03)))
        m.add(2, hip_roof("basilica_roof", bl - 30, by1 - by0 - 26, 7, (0, (by0 + by1) / 2, 23.6), "terracotta", ridge=0.85))
        m.add(2, box("basilica_aisle_roof", bl, by1 - by0, 0.8, (0, (by0 + by1) / 2, 15.6), shade("terracotta", -0.1)))
    for s in (-1, 1):
        m.add(1, ellipse_ring(f"apse{s}", 24, 24, 0.9, 12 if not construction else 5, (s * bl / 2, (by0 + by1) / 2, 0.4), shade(MARBLE, -0.04), arc=math.pi, start=(-math.pi / 2 if s > 0 else math.pi / 2)))
    # the Column between two libraries
    cy = by1 + 18
    m.add(1, box("column_court", 50, 30, 0.6, (0, cy, 0.4), PLAZA))
    for s in (-1, 1):
        m.add(1, box(f"library{s}", 18, 26, 16 if not construction else 7, (s * 34, cy, 0.4), "brick"))
        if not construction:
            m.add(2, hip_roof(f"library_roof{s}", 18, 26, 4, (s * 34, cy, 16.4), "terracotta"))
    if construction:
        m.add(2, box("column_base", 6, 6, 5.4, (0, cy, 0.4), MARBLE))
        m.add(2, crane("crane3", 9, cy, 30))
    else:
        m.add(2, box("column_base", 6, 6, 5.4, (0, cy, 0.4), MARBLE), "column")
        m.add(2, cylinder("column_shaft", 1.85, 30, (0, cy, 5.8), MARBLE, verts=16))
        m.add(2, box("column_capital", 4.2, 4.2, 1.5, (0, cy, 35.8), MARBLE))
        m.add(2, cylinder("column_statue", 0.8, 4, (0, cy, 37.3), "bronze", verts=8))
    # a colonnaded court beyond (later the Temple of Trajan stood here)
    m.add(1, box("north_court", 120, 70, 0.4, (0, cy + 52, 0), shade(PLAZA, -0.03)))
    # Trajan's Markets: three stepped terraces wrapped around the east exedra, cut into the Quirinal
    ex, ey = px + 15, (py0 + py1) / 2
    tiers = [(30, 38, 11), (38, 46, 18), (46, 54, 25)] if not construction else [(30, 38, 11), (38, 46, 7)]
    for i, (r0, r1, h) in enumerate(tiers):
        m.add(1, ellipse_ring(f"markets{i}", r1, r1, r0 / r1, h, (ex, ey, 0.4), "brick", arc=math.pi, start=-math.pi / 2), "markets")
        if not construction or i == 0:
            m.add(2, ellipse_ring(f"markets_roof{i}", r1 + 0.4, r1 + 0.4, (r0 + 0.5) / (r1 + 0.4), 0.8, (ex, ey, 0.4 + h), shade("terracotta", -0.05), arc=math.pi, start=-math.pi / 2))
    if construction:
        # the cut face of the hill and the spoil being carted away
        m.add(2, box("hill_cut", 30, 120, 22, (ex + 70, ey + 20, 0.4), "#9C8A6A"), "earthworks")
        m.add(2, box("hill_step", 18, 120, 12, (ex + 52, ey + 20, 0.4), "#A9967A"))
        m.add(2, stone_stack("stones1", -40, -120))
        m.add(2, stone_stack("stones2", 20, -70))
        m.add(2, crane("crane4", -20, -100, 14))
    return m


# ---------------------------------------------------------------- Forum of Augustus
def forum_of_augustus():
    m = Model("forum-of-augustus")
    W, D = 125, 118
    px, py0, py1 = 28, -59, 30
    m.add(0, box("plaza", px * 2, py1 - py0, 0.4, (0, (py0 + py1) / 2, 0), PLAZA), "plaza")
    for s in (-1, 1):
        portico(m, f"portico{s}", s * px, s * (px + 12), py0, py1 + 12)
        exedra(m, f"exedra{s}", s * (px + 12), -5, 20, s, h=14)
    # the firewall against the Subura
    m.add(1, box("firewall", W, 3, 33, (0, D / 2 - 2, 0.4), "#9C8A72"))
    # Temple of Mars Ultor at the far end, on a high podium
    b, body, roof = mini_temple("mars", 36, 46, 3.5, 17, 8, 0, (0, 24, 0.4), MARBLE)
    m.add(1, b); m.add(1, body); m.add(2, roof)
    equestrian(m, 0, -20, quadriga=True)
    m.add(1, box("entrance", 30, 4, 12, (0, py0 - 2, 0.4), MARBLE))
    return m


# ---------------------------------------------------------------- Forum of Caesar
def forum_of_caesar(construction=False):
    m = Model("forum-of-caesar" + ("-construction" if construction else ""))
    W, D = 75, 160
    px, py0, py1 = 24, -80, 50
    m.add(0, box("plaza", px * 2, py1 - py0, 0.4, (0, (py0 + py1) / 2, 0), SAND if construction else PLAZA), "plaza")
    for s in (-1, 1):
        if construction and s < 0:
            m.add(1, box("portico_w_footing", 12, py1 - py0, 1.0, (s * (px + 6), (py0 + py1) / 2, 0.4), MARBLE), "porticoes")
        else:
            portico(m, f"portico{s}", s * px, s * (px + 12), py0, py1 + 20, roof=not construction)
    # tabernae (shops) behind the west portico, opening onto the Clivus Argentarius
    shops = [box(f"taberna{i}", 6, 7.2, 7, (-(px + 15.5), py0 + 4 + i * 8, 0.4), "brick") for i in range(15)]
    m.add(1, join(shops, "tabernae"), "shops")
    m.add(2, box("tabernae_roof", 7, 125, 0.8, (-(px + 15.5), py0 + 60, 7.4), shade("terracotta", -0.08)))
    # Temple of Venus Genetrix at the far end
    if construction:
        m.add(1, box("temple_podium", 30, 42, 5, (0, 58, 0.4), shade("limestone", -0.08)), "temple")
        m.add(2, scaffold("temple_scaffold", -15, 15, 40, 76, 16), "site")
        m.add(2, crane("crane", 22, 50, 20))
        m.add(2, stone_stack("stones", -18, -40))
    else:
        b, body, roof = mini_temple("venus", 30, 42, 5, 15, 8, 0, (0, 58, 0.4), MARBLE)
        m.add(1, b); m.add(1, body); m.add(2, roof)
        equestrian(m, 0, -10)
    return m


BUILDERS = {
    "rome/forum-of-trajan": lambda: forum_of_trajan(False),
    "rome/forum-of-trajan-construction": lambda: forum_of_trajan(True),
    "rome/forum-of-augustus": forum_of_augustus,
    "rome/forum-of-caesar": lambda: forum_of_caesar(False),
    "rome/forum-of-caesar-construction": lambda: forum_of_caesar(True),
}
