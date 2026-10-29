"""
Instruments and writing things from the map's own world: an astrolabe (its rete turns), a pair of dividers (its legs
open), ink and a quill with a pounce pot, a reading glass, an inkstone with its ink stick and water dropper, a brush on
a mountain-shaped rest, a name seal and its paste box. Metres, origin where the app puts the prop's group.

Parts the app treats itself: anim_* (animated about their pivots), glass (the lens), tex_face (the astrolabe's
engraved plate, painted by the app).
"""
import math

from studykit import MB, StudyProp, rrect

BRASS, BRASS_D, GOLD, STEEL = "#A8823A", "#7A5C28", "#B8934A", "#8A8A86"
INK, PEWTER = "#1E1610", "#5C5850"
POR, BLUE = "#BDB8AA", "#34506E"   # porcelain, its cobalt bands
WOOD_D, WOOD_L = "#32200F", "#6A4428"


def disc_uv(mb, r, y, color, seg=40):
    """A flat disc facing up with planar UVs (0..1 across its diameter)."""
    c = mb.vert((0, y, 0), (0.5, 0.5))
    ring = [mb.vert((r * math.cos(a), y, r * math.sin(a)), (0.5 + 0.5 * math.cos(a), 0.5 + 0.5 * math.sin(a))) for a in [math.tau * j / seg for j in range(seg)]]
    for j in range(seg):
        mb.face((c, ring[j], ring[(j + 1) % seg]), color, (0, 1, 0), False)


def circle(r, n=32, cx=0.0, cz=0.0):
    return [(cx + r * math.cos(math.tau * j / n), cz + r * math.sin(math.tau * j / n)) for j in range(n)]


# ---------------------------------------------------------------- astrolabe

def astrolabe():
    p = StudyProp("astrolabe", ao=0.02, edge=0.05)
    mb = MB()
    # the mater, its raised limb round the engraved plate
    mb.lathe([(0, 0), (0.0885, 0), (0.0905, 0.0015), (0.0905, 0.0085), (0.0912, 0.0102), (0.0906, 0.0119), (0.0888, 0.0127), (0.0870, 0.0121),
              (0.0864, 0.0104), (0.0862, 0.0100)], BRASS_D, seg=48)
    # the throne, pierced and lobed, with its shackle and ring
    thr = [(-0.024, -0.086), (-0.022, -0.096), (-0.016, -0.100), (-0.019, -0.106), (-0.012, -0.110), (-0.006, -0.108), (-0.004, -0.114), (0.0, -0.117),
           (0.004, -0.114), (0.006, -0.108), (0.012, -0.110), (0.019, -0.106), (0.016, -0.100), (0.022, -0.096), (0.024, -0.086)]
    mb.prism(thr, 0.0015, 0.0098, BRASS, bevel=0.0008, seg=1)
    with mb.at((0, 0.0097, -0.098)):
        mb.lathe([(0, 0), (0.0045, 0), (0.0045, 0.0008), (0.003, 0.0016), (0, 0.0018)], BRASS_D, seg=10)
    mb.tube([(0.0055 * math.cos(a), 0.0058, -0.1215 + 0.0055 * math.sin(a)) for a in [math.tau * j / 12 for j in range(13)]], 0.0016, BRASS, seg=5)
    mb.tube([(0.0125 * math.cos(a), 0.0026, -0.139 + 0.0125 * math.sin(a)) for a in [math.tau * j / 18 for j in range(19)]], 0.0024, BRASS, seg=6)
    # the rule across the front, pointed at both ends, and the pin with its wedge
    rule = [(-0.084, 0), (-0.06, -0.0045), (-0.012, -0.005), (-0.008, -0.008), (0.008, -0.008), (0.012, -0.005), (0.06, -0.0045), (0.084, 0),
            (0.06, 0.0045), (0.012, 0.005), (0.008, 0.008), (-0.008, 0.008), (-0.012, 0.005), (-0.06, 0.0045)]
    with mb.at((0, 0, 0), rot=(0, 0.7, 0)):
        mb.prism(rule, 0.0168, 0.0182, BRASS, bevel=0.0004, seg=1)
        with mb.at((0, 0.0095, 0)):
            mb.lathe([(0.0024, 0), (0.0024, 0.0098), (0.0036, 0.0104), (0.0034, 0.0112), (0, 0.0116)], BRASS_D, seg=10)
        mb.box(0.012, 0.0022, 0.0016, (0.0, 0.0198, 0), BRASS_D)
    p.part("base", mb, angle=40)
    face = MB()
    disc_uv(face, 0.0866, 0.0100, "#C49A50")
    p.part("tex_face", face)
    # the rete: the star map that turns over the plate
    rt = MB()
    y0, y1, yb = 0.0106, 0.0120, 0.0114
    rt.ring_prism(circle(0.0752, 48), circle(0.0722, 48), y0, y1, GOLD)
    rt.ring_prism(circle(0.0505, 40, 0, 0.018), circle(0.0475, 40, 0, 0.018), y0, y1, GOLD)
    for a in (0, math.pi / 2):
        with rt.at(rot=(0, a, 0)):
            rt.box(0.145, yb - y0, 0.0032, (0, (y0 + yb) / 2, 0), GOLD)
    # star pointers: little flames reaching in from the rings
    for k, a in enumerate([0.4, 1.3, 2.1, 2.9, 3.7, 4.6, 5.5, 0.9, 3.3]):
        r0 = 0.072 if k < 7 else 0.048
        with rt.at((0, 0, 0.018 if k >= 7 else 0), rot=(0, -a, 0)):
            leaf = [(r0 + 0.001, -0.0035), (r0 - 0.008, -0.0028), (r0 - 0.016, -0.0004), (r0 - 0.019, 0.0), (r0 - 0.016, 0.0010), (r0 - 0.009, 0.0032), (r0 + 0.001, 0.0035)]
            rt.prism(leaf, y0, yb, GOLD)
    p.part("anim_rete", rt, (0, 0.0135, 0), angle=40)
    return p


# ---------------------------------------------------------------- dividers

def _divider_leg(mb, y):
    """One leg along +x from the hinge: a brass arm with a turned swelling, and a steel point."""
    pts = [(0.006, -0.006), (0.03, -0.0052), (0.045, -0.0062), (0.055, -0.0062), (0.07, -0.0044), (0.112, -0.0034), (0.114, 0.0),
           (0.112, 0.0034), (0.07, 0.0044), (0.055, 0.0062), (0.045, 0.0062), (0.03, 0.0052), (0.006, 0.006)]
    mb.prism(pts, y - 0.00175, y + 0.00175, BRASS, bevel=0.0006, seg=1)
    with mb.at((0.111, y, 0), rot=(0, 0, -math.pi / 2)):
        mb.lathe([(0, 0), (0.0032, 0), (0.0035, 0.005), (0.0029, 0.009), (0.0008, 0.060), (0, 0.066)], STEEL, seg=10)


def dividers():
    p = StudyProp("dividers", ao=0.015, edge=0.05)
    mb = MB()
    # the joint: a turned disc round both legs, a screw head, and a handle to hold it by
    mb.lathe([(0, -0.0038), (0.0125, -0.0038), (0.0135, -0.0028), (0.0135, 0.0062), (0.0125, 0.0072), (0, 0.0072)], BRASS, seg=24)
    with mb.at((0, 0.0072, 0)):
        mb.lathe([(0, 0), (0.0062, 0), (0.0058, 0.0012), (0.0035, 0.0021), (0, 0.0024)], BRASS_D, seg=14)
    mb.box(0.009, 0.0008, 0.0012, (0, 0.0095, 0), "#3A2A14")
    with mb.at((-0.012, 0.0017, 0), rot=(0, 0, math.pi / 2)):
        mb.lathe([(0, 0), (0.004, 0.0), (0.0045, 0.003), (0.003, 0.007), (0.0042, 0.012), (0.0050, 0.016), (0.0038, 0.021), (0.0018, 0.024), (0, 0.0245)], BRASS, seg=12)
    p.part("base", mb)
    for name, y in (("anim_leg_a", -0.0005), ("anim_leg_b", 0.0035)):
        lg = MB()
        _divider_leg(lg, y)
        p.part(name, lg, (0, y, 0))
    return p


# ---------------------------------------------------------------- ink and a quill

def _vane(mb, s0, s1, wide, narrow, n=10):
    """A feather's vane along +y from s0 to s1: wider on +x, a thin curved blade with two faces."""
    rows = []
    for i in range(n + 1):
        t = i / n
        s = s0 + (s1 - s0) * t
        env = math.sin(math.pi * min(1.0, t * 1.15)) ** 0.6 if t < 0.97 else 0.15
        w1, w0 = wide * env, narrow * env
        row = []
        for x in (-w0, -w0 * 0.5, 0.0, w1 * 0.35, w1 * 0.7, w1):
            bend = -0.0025 * (x / max(wide, 1e-6)) ** 2 * 3
            row.append((x, s - 0.012 * (x / wide) * (abs(x) > 0) , bend))
        rows.append(row)
    top = [[mb.vert((x, y, z + 0.00035)) for x, y, z in row] for row in rows]
    bot = [[mb.vert((x, y, z - 0.00035)) for x, y, z in row] for row in rows]
    m = len(rows[0])
    for i in range(n):
        for j in range(m - 1):
            mb.face((top[i][j], top[i][j + 1], top[i + 1][j + 1], top[i + 1][j]), "#E4D9C2", (0, 0, 1), True)
            mb.face((bot[i][j], bot[i][j + 1], bot[i + 1][j + 1], bot[i + 1][j]), "#D6CAB2", (0, 0, -1), True)
    for i in range(n):
        for j in (0, m - 1):
            mb.face((top[i][j], top[i + 1][j], bot[i + 1][j], bot[i][j]), "#D6CAB2", (-1 if j == 0 else 1, 0, 0), True)


def quill():
    p = StudyProp("quill", ao=0.03, edge=0.04)
    mb = MB()
    well = [(0, 0), (0.045, 0), (0.047, 0.003), (0.047, 0.007), (0.044, 0.009), (0.042, 0.012), (0.040, 0.016), (0.039, 0.036), (0.036, 0.042),
            (0.030, 0.047), (0.022, 0.050), (0.017, 0.053), (0.017, 0.060), (0.0188, 0.0614), (0.018, 0.063), (0.0125, 0.063), (0.012, 0.060),
            (0.012, 0.0495), (0, 0.0495)]
    mb.lathe(well, PEWTER, seg=24, colors=[PEWTER] * 16 + ["#2A2620", INK])
    # the quill, standing in the ink, leaning out
    with mb.at((0, 0.045, 0), rot=(0.18, 0.4, -0.5)):
        mb.tube([(0, 0.0, 0), (0.0, 0.08, 0), (0.002, 0.16, 0), (0.006, 0.23, 0), (0.011, 0.27, 0)], 0.0019, "#DDD2BC", seg=6, scales=[1.0, 0.95, 0.8, 0.6, 0.35])
        with mb.at((0.0012, 0.0, 0.0)):
            _vane(mb, 0.085, 0.268, 0.017, 0.006)
    # a pounce pot, its dished top pierced for sprinkling sand
    with mb.at((0.075, 0, 0.03)):
        pot = [(0, 0), (0.020, 0), (0.022, 0.004), (0.0215, 0.008), (0.017, 0.014), (0.0155, 0.022), (0.0165, 0.030), (0.020, 0.036), (0.0225, 0.039),
               (0.021, 0.041), (0.017, 0.0398), (0.008, 0.0378), (0, 0.0372)]
        mb.lathe(pot, PEWTER, seg=20)
        for k, (r, a) in enumerate([(0.0, 0.0)] + [(0.008, math.tau * j / 6) for j in range(6)]):
            y = 0.0372 + (0.0006 if r else 0.0) + 0.0002
            with mb.at((r * math.cos(a), y, r * math.sin(a))):
                mb.lathe([(0, 0), (0.0011, 0), (0, 0.0003)], INK, seg=6)
    p.part("base", mb)
    return p


# ---------------------------------------------------------------- a reading glass

def lens():
    p = StudyProp("lens", ao=0.02, edge=0.05, ground=True)
    mb = MB()
    rim = [(0.0418, -0.003), (0.047, -0.0045), (0.0498, -0.003), (0.0506, 0.0), (0.0498, 0.003), (0.047, 0.0045), (0.0418, 0.003), (0.0415, 0.0), (0.0418, -0.003)]
    mb.lathe(rim, BRASS, seg=40)
    with mb.at((0.049, 0.0016, 0), rot=(0, 0, -math.pi / 2)):
        mb.lathe([(0, 0), (0.0062, 0), (0.0068, 0.003), (0.0060, 0.006), (0.0060, 0.012), (0.0074, 0.0135), (0.0074, 0.017), (0, 0.017)], BRASS, seg=12)
        with mb.at((0, 0.017, 0)):
            mb.lathe([(0, 0), (0.0066, 0), (0.0076, 0.003), (0.0086, 0.013), (0.0072, 0.027), (0.0082, 0.046), (0.0094, 0.066), (0.0088, 0.080), (0.0066, 0.088),
                      (0.003, 0.092), (0, 0.0925)], WOOD_D, seg=12)
    # the group sits 8 mm up: drop the lens and handle onto the table
    p.part("base", mb)
    g = MB()
    g.lathe([(0, -0.0026), (0.02, -0.0022), (0.035, -0.0012), (0.0425, -0.0003), (0.0425, 0.0003), (0.035, 0.0012), (0.02, 0.0022), (0, 0.0026)], "#DFE6E2", seg=32)
    p.part("glass", g)
    return p


# ---------------------------------------------------------------- inkstone

def inkstone():
    p = StudyProp("inkstone", ao=0.02, edge=0.03)
    mb = MB()
    S, SD = "#3A3A3E", "#2E2E32"
    mb.ring_prism(rrect(0.12, 0.18, 0.012, 3), rrect(0.10, 0.16, 0.008, 3), 0.0, 0.0225, S)
    mb.ring_prism(rrect(0.116, 0.176, 0.010, 3), rrect(0.10, 0.16, 0.008, 3), 0.0225, 0.0245, S)

    def h(x, z):
        # the grinding ground, faintly dished, running down into the well at the head
        g = 0.0165 - 0.0012 * (1 - (x / 0.05) ** 2) * (1 - (z / 0.08) ** 2)
        dw = ((x / 0.042) ** 2 + ((z + 0.058) / 0.022) ** 2)
        if dw < 1:
            g -= 0.0085 * (1 - dw) ** 0.7
        return g

    mb.grid(-0.051, 0.051, -0.081, 0.081, 12, 20, h, lambda x, z, y: SD if y < 0.0155 else S)
    # the pool of ink standing in the well, its edge where it meets the sloping stone
    with mb.at((0, 0.0125, -0.058), scale=(0.039, 1, 0.0205)):
        mb.lathe([(1.0, 0), (0, 0)], "#0A0A0C", seg=28)
    # the ink stick, resting on the ground with its gilt label
    with mb.at((0.012, 0.0, 0.035), rot=(0, 0.3, 0)):
        mb.box(0.022, 0.012, 0.08, (0, 0.0215, 0), "#16161A", bevel=0.0015, seg=1)
        mb.box(0.011, 0.0006, 0.042, (0, 0.0277, 0.004), "#A8863A")
    # the water dropper
    with mb.at((0.11, 0, -0.04)):
        mb.lathe([(0, 0), (0.012, 0.0008), (0.020, 0.006), (0.024, 0.014), (0.022, 0.022), (0.014, 0.028), (0.006, 0.0305), (0.0042, 0.032), (0.0042, 0.0365),
                  (0.0022, 0.0368), (0, 0.0368)], "#6E8A8A", seg=18)
    p.part("base", mb, angle=40)
    return p


# ---------------------------------------------------------------- brush and rest

def brush():
    p = StudyProp("brush", ao=0.02, edge=0.04)
    mb = MB()
    pts = []
    for i in range(41):
        z = -0.07 + 0.14 * i / 40
        # three peaks between two valleys, falling to the ends
        hz = abs(z)
        y = 0.0
        if hz < 0.03:
            y = 0.012 + 0.028 * (1 + math.cos(math.pi * hz / 0.03)) / 2
        elif hz < 0.07:
            y = 0.012 + 0.018 * (1 - math.cos(math.pi * (hz - 0.03) / 0.02)) / 2 if hz < 0.05 else 0.03 * (1 + math.cos(math.pi * (hz - 0.05) / 0.02)) / 2
        pts.append((max(y, 0.0), z))
    outline = [(0.0, -0.07)] + pts[1:-1] + [(0.0, 0.07)]
    with mb.at((0.07, 0, 0), rot=(0, 0, math.pi / 2)):
        mb.prism(outline, 0.0, 0.02, "#3A4A3E", smooth=True, bevel=0.0018, seg=2)
    # the brush across a valley: lacquered cap, bamboo with its nodes, the ferrule, the inked hair
    cap, bam, node, fer, hair = "#2A1810", "#B39A62", "#9A8250", "#5A3A24", INK
    prof = [((0, 0), cap), ((0.0060, 0.0005), cap), ((0.0066, 0.003), cap), ((0.0066, 0.012), cap), ((0.0057, 0.0135), bam), ((0.0055, 0.05), node),
            ((0.0061, 0.052), node), ((0.0055, 0.054), bam), ((0.0054, 0.11), node), ((0.0059, 0.112), node), ((0.0054, 0.114), bam), ((0.0053, 0.188), fer),
            ((0.0062, 0.190), fer), ((0.0062, 0.198), hair), ((0.0058, 0.200), hair), ((0.0066, 0.210), hair), ((0.0055, 0.222), hair), ((0.003, 0.234), hair),
            ((0, 0.242), hair)]
    with mb.at((0.06, 0.0175, 0.03), rot=(0, 0, 0.1)):
        with mb.at((0.046, 0, 0), rot=(0, 0, math.pi / 2)):
            mb.lathe([q for q, _ in prof], bam, seg=12, colors=[c for _, c in prof][1:])
        mb.tube([(0.046 + 0.0055 + 0.0055 * math.cos(a), 0.0055 * math.sin(a), 0) for a in [math.tau * j / 12 for j in range(13)]], 0.0009, "#7A3220", seg=4)
    p.part("base", mb, angle=50)
    return p


# ---------------------------------------------------------------- seal and paste

def seal():
    p = StudyProp("seal", ao=0.025, edge=0.03)
    mb = MB()
    st, std = "#A8946A", "#8E7A52"
    mb.box(0.032, 0.05, 0.032, (0, 0.025, 0), st, bevel=0.0022, seg=2)
    # a crouching lion on the top
    mb.ellipsoid((0, 0.056, 0.003), 0.012, 0.0085, 0.0145, st, seg=12, rings=7)
    mb.ellipsoid((0, 0.0645, -0.0105), 0.0082, 0.0078, 0.0078, st, seg=10, rings=6)
    for a in range(5):
        ang = -1.0 + a * 0.5
        mb.ellipsoid((0.0072 * math.sin(ang), 0.0675 + 0.002 * math.cos(ang), -0.0078 + 0.003 * math.cos(ang)), 0.0034, 0.0034, 0.0034, std, seg=8, rings=4)
    for sx in (-1, 1):
        mb.ellipsoid((sx * 0.0085, 0.052, -0.0095), 0.0035, 0.004, 0.0055, st, seg=8, rings=4)
        mb.ellipsoid((sx * 0.0085, 0.052, 0.0135), 0.0035, 0.004, 0.006, st, seg=8, rings=4)
    mb.ellipsoid((0, 0.0628, -0.018), 0.004, 0.0035, 0.003, std, seg=8, rings=4)
    mb.tube([(0, 0.056, 0.017), (0.004, 0.062, 0.019), (0.007, 0.066, 0.014), (0.004, 0.067, 0.010)], 0.0016, std, seg=5)
    # the paste box, open, its lid beside it
    with mb.at((0.072, 0, 0)):
        prof = [((0, 0), POR), ((0.030, 0), POR), ((0.033, 0.002), POR), ((0.0335, 0.006), BLUE), ((0.0335, 0.010), POR),
                ((0.0335, 0.014), POR), ((0.031, 0.016), POR), ((0.0295, 0.016), POR), ((0.0292, 0.0128), POR),
                ((0.020, 0.0143), "#9A2E28"), ((0, 0.0151), "#9A2E28")]
        mb.lathe([q for q, _ in prof], POR, seg=24, colors=[c for _, c in prof][1:])
    with mb.at((0.074, 0, 0.076)):
        lid = [((0, 0), POR), ((0.0345, 0), POR), ((0.0345, 0.006), BLUE), ((0.0335, 0.009), POR), ((0.030, 0.0135), POR),
               ((0.018, 0.0165), BLUE), ((0.008, 0.0172), POR), ((0, 0.0174), POR)]
        mb.lathe([q for q, _ in lid], POR, seg=24, colors=[c for _, c in lid][1:])
    p.part("base", mb)
    return p


BUILDERS = {
    "study/astrolabe": astrolabe, "study/dividers": dividers, "study/quill": quill, "study/lens": lens,
    "study/inkstone": inkstone, "study/brush": brush, "study/seal": seal,
}
