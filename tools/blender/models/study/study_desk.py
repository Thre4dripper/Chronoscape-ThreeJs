"""
The things every reader keeps on the table: the atlases, rolled maps, a leather map tube, the lamp (a candle, an oil
lamp, a bronze lamp, an andon or a brazier, by the atlas) and the sandglass. Metres, origin where the app puts the
prop's group (on the table top, y = 0), +Z toward the viewer.

Parts the app treats itself: glass (the sandglass bulbs), paper (the andon's panels, they glow when lit), coals
(the brazier's, they burn when lit).
"""
import math

from studykit import MB, StudyProp, arc_pts, rrect

BRASS, BRASS_D, GILT = "#A8823A", "#7A5C28", "#B08C48"
PAPER, PAGES, INK = "#CDBE98", "#B9A880", "#1E1610"
WOOD, WOOD_D, WOOD_L = "#4E3220", "#32200F", "#6A4428"
CLAY, CLAY_D = "#8E5034", "#6A3A24"
LEATHER, LEATHER_D = "#3E2416", "#2A170D"
TAPE = "#7A3220"
WAX = "#E2D8BE"


# ---------------------------------------------------------------- the atlases

def book(mb, w, d, h, c, clasp=False, boss=False):
    """A bound book lying flat, spine toward -x: boards with rounded edges and brass corners, the text block set in,
    a rounded spine with raised bands and gilt rules."""
    b = 0.0045
    # boards
    for s in (-1, 1):
        mb.box(w - 0.009, b, d, (0.0045, s * (h / 2 - b / 2), 0), c, bevel=0.0012, seg=2)
    # text block: in from the head, tail and fore-edge
    mb.box(w - 0.016, h - 2 * b - 0.001, d - 0.007, (0.0035, 0, 0), PAGES)
    # page edges: a few faint lines across the fore-edge
    for k in range(1, 4):
        y = -h / 2 + b + (h - 2 * b) * k / 4
        mb.box(0.0004, 0.0006, d - 0.0076, (w / 2 - 0.0045 + 0.0001, y, 0), PAPER)
    # the spine: half round, raised bands, gilt rules between them
    R = h / 2 - 0.0025
    prof = [(0.0, -d / 2), (R, -d / 2)]
    cols = [c]
    marks = sorted([(z * d, "band") for z in (-0.3, -0.1, 0.1, 0.3)] + [(z * d, "gilt") for z in (-0.42, -0.2, 0.0, 0.2, 0.42)])
    for z, kind in marks:
        if kind == "band":
            seq = [(R, z - 0.0045), (R + 0.0018, z - 0.003), (R + 0.0018, z + 0.003), (R, z + 0.0045)]
            ccol = [c, c, c, c]
        else:
            seq = [(R, z - 0.0009), (R + 0.0004, z - 0.0008), (R + 0.0004, z + 0.0008), (R, z + 0.0009)]
            ccol = [c, GILT, GILT, GILT]
        prof += seq
        cols += ccol
    prof += [(R, d / 2), (0.0, d / 2)]
    cols += [c, c]
    cols = cols[: len(prof) - 1]
    while len(cols) < len(prof) - 1:
        cols.append(c)
    with mb.at((-w / 2 + 0.011, 0, 0), rot=(math.pi / 2, 0, 0), scale=(0.0135 / R, 1, 1)):
        mb.lathe(prof, c, seg=8, arc=(math.pi / 2, 3 * math.pi / 2), colors=cols)
    # brass corners over the fore-edge corners of the upper board
    for sz in (-1, 1):
        tri = [(w / 2 + 0.0008, sz * (d / 2 + 0.0008)), (w / 2 - 0.028, sz * (d / 2 + 0.0008)), (w / 2 + 0.0008, sz * (d / 2 - 0.028))]
        mb.prism(tri, h / 2 - b - 0.0006, h / 2 + 0.0006, BRASS)
    if clasp:
        mb.box(0.034, 0.0012, 0.022, (w / 2 - 0.016, h / 2 + 0.0011, 0), BRASS, bevel=0.0004, seg=1)
        mb.box(0.0016, h + 0.0034, 0.022, (w / 2 + 0.0015, 0, 0), BRASS, bevel=0.0004, seg=1)
        with mb.at((w / 2 - 0.028, h / 2 + 0.0017, 0)):
            mb.lathe([(0, 0), (0.0042, 0), (0.0042, 0.0008), (0.0028, 0.0022), (0, 0.0026)], BRASS_D, seg=10)
    if boss:
        with mb.at((0.01, h / 2, 0)):
            mb.lathe([(0, 0.0002), (0.017, 0.0002), (0.017, 0.0009), (0.012, 0.0018), (0.006, 0.0034), (0, 0.0038)], BRASS, seg=14)


def atlases():
    p = StudyProp("atlases", ao=0.03, edge=0.07)
    mb = MB()
    books = [dict(w=0.27, d=0.2, h=0.05, c="#3F5238", r=0.08, clasp=True),
             dict(w=0.24, d=0.18, h=0.04, c="#5E2A1E", r=-0.12),
             dict(w=0.21, d=0.155, h=0.045, c="#2E3A50", r=0.2, boss=True)]
    y = 0.0
    for bk in books:
        yy = y + bk["h"] / 2 + 0.0005
        y += bk["h"] + 0.001
        with mb.at((0, yy, 0), rot=(0, bk["r"], 0)):
            book(mb, bk["w"], bk["d"], bk["h"], bk["c"], bk.get("clasp", False), bk.get("boss", False))
    p.part("base", mb)
    return p


# ---------------------------------------------------------------- rolled maps

def roll(mb, r, length, color, turns=3.0, start=0.0, ties=TAPE):
    """A rolled sheet along X: a real spiral of paper (you see it at the ends), tied with tape."""
    t = 0.0008
    r_in = r * 0.28
    n = int(turns * 15)
    outer, inner = [], []
    for i in range(n + 1):
        th = turns * math.tau * i / n
        rr = r_in + (r - r_in) * i / n
        a = start - th
        outer.append((rr * math.cos(a), rr * math.sin(a)))
        inner.append(((rr - t) * math.cos(a), (rr - t) * math.sin(a)))
    sec = outer + list(reversed(inner))
    # (u, v): u along -z, v along +y for a path along +x
    mb.sweep(sec, [(-length / 2, 0, 0), (length / 2, 0, 0)], color, caps=True, smooth=True, cap_color=color)
    # tapes round the outer turn, stepping down over the sheet's free edge
    per = 15
    loop = []
    for i in range(n - per, n + 1):
        th = turns * math.tau * i / n
        rr = r_in + (r - r_in) * i / n + 0.0009
        a = start - th
        loop.append((rr * math.cos(a), rr * math.sin(a)))
    loop.append(loop[0])
    for k in ((-0.22, 0.22) if ties else ()):
        path = [(k * length, v, -u) for u, v in loop]
        mb.sweep([(-0.0007, -0.006), (0.0007, -0.006), (0.0007, 0.006), (-0.0007, 0.006)], path, ties, caps=True, smooth=True, up=(1, 0, 0))


def rolled_maps():
    p = StudyProp("rolled-maps", ao=0.03, edge=0.2)
    mb = MB()
    # two rolls side by side, just apart, and a third resting in the groove between them (1 mm clear of both);
    # all parallel, so the gaps hold along their whole length
    rolls = [(-0.1, -0.032, 0.42, 0.028, 0.03, "#BDAE88", 0.0, 0.3), (0.04, 0.042, 0.36, 0.024, 0.03, "#B5A47E", 0.0, 2.0), (-0.04, 0.0094, 0.38, 0.022, 0.03, "#C0B08A", 0.0361, 4.1)]
    for x, z, l, r, a, c, y, st in rolls:
        with mb.at((x, y + r, z), rot=(0, a, 0)):
            roll(mb, r, l, c, start=st)
    p.part("base", mb, angle=60)
    return p


# ---------------------------------------------------------------- the map tube

def map_case():
    p = StudyProp("map-case", ao=0.03, edge=0.2)
    mb = MB()
    B, L, LD = BRASS, LEATHER, LEATHER_D
    seq = [((0, -0.2565), B), ((0.012, -0.2562), B), ((0.024, -0.2548), B), ((0.032, -0.252), B), ((0.0365, -0.247), B), ((0.0372, -0.243), B),
           ((0.0366, -0.239), B), ((0.0364, -0.236), B), ((0.0364, -0.226), B), ((0.0374, -0.2245), B), ((0.0374, -0.2215), B), ((0.0362, -0.2205), L),
           ((0.034, -0.22), L), ((0.034, -0.108), LD), ((0.0356, -0.1072), LD), ((0.0356, -0.0928), LD), ((0.034, -0.092), L),
           ((0.034, 0.092), LD), ((0.0356, 0.0928), LD), ((0.0356, 0.1072), LD), ((0.034, 0.108), L), ((0.034, 0.205), B),
           ((0.0373, 0.2056), B), ((0.0378, 0.208), B), ((0.0378, 0.212), B), ((0.0372, 0.214), B), ((0.0372, 0.236), B), ((0.0377, 0.238), B),
           ((0.0377, 0.242), B), ((0.0368, 0.245), B), ((0.030, 0.251), B), ((0.018, 0.2545), B), ((0.0085, 0.2556), BRASS_D), ((0.0062, 0.258), BRASS_D),
           ((0.0052, 0.2625), BRASS_D), ((0.0034, 0.2655), BRASS_D), ((0, 0.2662), B)]
    prof = [q for q, _ in seq]
    cols = [c for _, c in seq][:-1]
    with mb.at((0, 0.034, 0), rot=(0, 0, -math.pi / 2)):
        mb.lathe(prof, L, seg=18, colors=cols)
    # stitching down the seam of the leather, on top
    for k in range(-9, 10):
        x = k * 0.0105
        if abs(abs(x) - 0.1) < 0.012:
            continue
        mb.box(0.005, 0.0008, 0.0012, (x, 0.068 + 0.0001, 0.0), "#5A3A22")
    # two D-rings on their staples, for the strap
    for x in (-0.15, 0.15):
        mb.box(0.012, 0.0016, 0.008, (x, 0.0682, 0), BRASS_D, bevel=0.0005, seg=1)
        path = [(x + 0.009 * math.cos(math.radians(a)), 0.0688 + 0.0085 * math.sin(math.radians(a)) * 0.9 + 0.0, 0.0) for a in range(-10, 200, 15)]
        mb.tube(path, 0.0013, BRASS, seg=5)
    p.part("base", mb)
    return p


# ---------------------------------------------------------------- the lamps

def lamp_candle():
    p = StudyProp("lamp-candle", ao=0.04, edge=0.03)
    mb = MB()
    stick = [(0, 0), (0.056, 0), (0.060, 0.003), (0.060, 0.007), (0.055, 0.010), (0.050, 0.012), (0.042, 0.018), (0.030, 0.026), (0.020, 0.032),
             (0.016, 0.036), (0.0175, 0.040), (0.021, 0.043), (0.021, 0.047), (0.016, 0.050), (0.0105, 0.056), (0.0095, 0.066), (0.014, 0.072),
             (0.0165, 0.078), (0.014, 0.084), (0.0095, 0.090), (0.009, 0.100), (0.012, 0.104), (0.016, 0.107), (0.030, 0.111), (0.037, 0.114),
             (0.038, 0.118), (0.036, 0.1205), (0.032, 0.1195), (0.018, 0.1195), (0.0165, 0.121), (0.0155, 0.134), (0.0168, 0.136), (0.0168, 0.139),
             (0.0142, 0.1395), (0.0138, 0.1375), (0, 0.1375)]
    mb.lathe(stick, BRASS, seg=20)
    # the candle, its top melted into a cup
    mb.lathe([(0, 0.137), (0.0134, 0.137), (0.0134, 0.249), (0.0131, 0.2535), (0.0117, 0.2556), (0.0095, 0.2538), (0.005, 0.2518), (0, 0.2512)], WAX, seg=18)
    for a, l, y in ((0.3, 1.0, 0.238), (2.4, 0.7, 0.244), (4.2, 1.3, 0.232)):
        mb.ellipsoid((math.cos(a) * 0.0132, y, math.sin(a) * 0.0132), 0.0034, 0.011 * l, 0.0034, "#EFE7D0", seg=8, rings=6)
    mb.ellipsoid((0.022, 0.1196, 0.006), 0.007, 0.0012, 0.005, "#EFE7D0", seg=10, rings=4)
    mb.tube([(0, 0.251, 0), (0.0002, 0.256, 0), (0.0012, 0.2605, 0), (0.0022, 0.263, 0)], 0.0007, INK, seg=4)
    # the thumb ring on the base
    path = [(0.064 + 0.011 * math.cos(math.radians(a)), 0.012 + 0.011 * math.sin(math.radians(a)), 0) for a in range(-170, 175, 20)]
    mb.tube(path, 0.0026, BRASS, seg=6)
    p.part("base", mb)
    return p


def lamp_oil():
    p = StudyProp("lamp-oil", ao=0.03, edge=0.03)
    mb = MB()
    C = CLAY
    body = [(0, 0), (0.022, 0), (0.024, 0.002), (0.023, 0.005), (0.034, 0.009), (0.044, 0.016), (0.047, 0.022), (0.045, 0.028), (0.040, 0.032),
            (0.0385, 0.0345), (0.036, 0.0352), (0.034, 0.0335), (0.020, 0.031), (0.012, 0.030), (0.0065, 0.0298), (0.0055, 0.028), (0.0052, 0.024), (0, 0.024)]
    cols = [C] * 15 + [INK, INK]
    mb.lathe(body, C, seg=24, colors=cols)
    # the nozzle, and the wick hole at its tip
    sec = [(0.0125 * math.cos(math.tau * j / 12), 0.0085 * math.sin(math.tau * j / 12)) for j in range(12)]
    mb.sweep(sec, [(0.028, 0.022, 0), (0.048, 0.025, 0), (0.064, 0.0285, 0), (0.076, 0.031, 0)], C, caps=False, scales=[1.0, 0.86, 0.76, 0.72])
    mb.ellipsoid((0.076, 0.031, 0), 0.0098, 0.0062, 0.009, C, seg=12, rings=6)
    with mb.at((0.075, 0.0368, 0)):
        mb.lathe([(0, 0), (0.0042, 0), (0.0036, 0.0006), (0, 0.0007)], INK, seg=10)
    mb.tube([(0.075, 0.036, 0), (0.0752, 0.041, 0), (0.0758, 0.0455, 0)], 0.0011, "#2A2018", seg=4)
    # the ring handle at the back
    path = [(-0.054 + 0.014 * math.cos(math.radians(a)), 0.03 + 0.012 * math.sin(math.radians(a)), 0) for a in range(-40, 230, 18)]
    mb.tube(path, 0.0038, C, seg=6)
    p.part("base", mb)
    return p


def lamp_bronze():
    p = StudyProp("lamp-bronze", ao=0.04, edge=0.03)
    mb = MB()
    BZ, BZD = "#5A5A3E", "#46462E"
    prof = [(0, 0), (0.060, 0), (0.062, 0.004), (0.058, 0.008), (0.050, 0.011), (0.044, 0.014), (0.030, 0.020), (0.020, 0.026), (0.014, 0.032),
            (0.012, 0.040), (0.0105, 0.060), (0.016, 0.066), (0.022, 0.070), (0.024, 0.074), (0.016, 0.078), (0.010, 0.084), (0.010, 0.096),
            (0.0165, 0.099), (0.0172, 0.103), (0.0165, 0.107), (0.010, 0.110), (0.010, 0.140), (0.014, 0.146), (0.010, 0.152), (0.010, 0.160),
            (0.016, 0.166), (0.040, 0.176), (0.054, 0.184), (0.056, 0.190), (0.052, 0.1925), (0.048, 0.189), (0.020, 0.1832), (0, 0.1825)]
    cols = [BZ] * 4 + [BZD, BZD] + [BZ] * 10 + [BZD] * 4 + [BZ] * 12
    mb.lathe(prof, BZ, seg=24, colors=cols[: len(prof) - 1])
    with mb.at((0, 0.186, 0)):
        mb.lathe([(0, 0), (0.0335, 0), (0, 0.0001)], "#1A1408", seg=20)
    mb.tube([(0, 0.186, 0), (0.0006, 0.192, 0), (0.0012, 0.197, 0)], 0.0012, "#2A2018", seg=4)
    p.part("base", mb)
    return p


def lamp_andon():
    p = StudyProp("lamp-andon", ao=0.04, edge=0.03)
    mb = MB()
    W = WOOD_D
    mb.box(0.13, 0.012, 0.13, (0, 0.009, 0), W, bevel=0.002, seg=2)
    for sx in (-1, 1):
        for sz in (-1, 1):
            mb.box(0.016, 0.004, 0.016, (sx * 0.052, 0.002, sz * 0.052), W)
            mb.box(0.01, 0.255, 0.01, (sx * 0.052, 0.015 + 0.1275, sz * 0.052), W, bevel=0.0012, seg=1)
    outer, inner = rrect(0.118, 0.118, 0.004, 1), rrect(0.096, 0.096, 0.002, 1)
    for y in (0.026, 0.240):
        mb.ring_prism(outer, inner, y, y + 0.01, W)
    # the paper's lattice, just proud of it
    for s in (-1, 1):
        for y in (0.098, 0.172):
            mb.box(0.1, 0.004, 0.003, (0, y, s * 0.0516), W)
            mb.box(0.003, 0.004, 0.1, (s * 0.0516, y, 0), W)
        mb.box(0.003, 0.2, 0.0024, (0, 0.137, s * 0.0513), W)
        mb.box(0.0024, 0.2, 0.003, (s * 0.0513, 0.137, 0), W)
    # the carrying bar
    for s in (-1, 1):
        mb.box(0.008, 0.05, 0.008, (s * 0.053, 0.275, 0), W, bevel=0.001, seg=1)
    mb.box(0.12, 0.009, 0.012, (0, 0.302, 0), W, bevel=0.0015, seg=2)
    p.part("base", mb)
    pp = MB()
    pp.box(0.1, 0.2, 0.1, (0, 0.137, 0), "#C8BB9A")
    p.part("paper", pp)
    return p


def lamp_brazier():
    p = StudyProp("lamp-brazier", ao=0.03, edge=0.03)
    mb = MB()
    C, CD = CLAY, CLAY_D
    bowl = [(0, 0.03), (0.036, 0.03), (0.046, 0.036), (0.054, 0.046), (0.059, 0.052), (0.0625, 0.060), (0.066, 0.070), (0.0695, 0.075), (0.069, 0.079),
            (0.065, 0.080), (0.0615, 0.0775), (0.054, 0.068), (0.040, 0.059), (0, 0.055)]
    cols = [C, C, C, CD, CD, C, C, C, C, C, C, "#3A2418", "#2A1A12"]
    mb.lathe(bowl, C, seg=24, colors=cols)
    # incised chevrons round the band
    for i in range(12):
        a = math.tau * i / 12
        with mb.at((0, 0, 0), rot=(0, -a, 0)):
            mb.box(0.002, 0.0025, 0.009, (0.0605, 0.056, 0), "#5A2E1A")
    for i in range(3):
        a = math.tau * i / 3 + 0.5
        c, s = math.cos(a), math.sin(a)
        mb.tube([(0.032 * c, 0.034, 0.032 * s), (0.040 * c, 0.016, 0.040 * s), (0.046 * c, 0.0, 0.046 * s)], 0.0095, C, seg=8, scales=[1.0, 0.95, 1.1])
    p.part("base", mb)
    cc = MB()
    for i, (x, z, r) in enumerate([(0.0, 0.0, 0.014), (0.022, 0.008, 0.012), (-0.02, 0.012, 0.012), (0.006, -0.024, 0.011), (-0.016, -0.016, 0.011), (0.026, -0.014, 0.01), (-0.004, 0.026, 0.01)]):
        cc.ellipsoid((x, 0.061 + r * 0.25, z), r, r * 0.7, r * 0.9, "#2A2420", seg=6, rings=3)
    p.part("coals", cc, angle=10)
    return p


# ---------------------------------------------------------------- the sandglass

def sandglass():
    p = StudyProp("sandglass", ao=0.03, edge=0.03)
    mb = MB()
    plate = [(0, 0), (0.050, 0), (0.053, 0.0025), (0.053, 0.0055), (0.0505, 0.0075), (0.0475, 0.0095), (0.0475, 0.0115), (0.043, 0.014), (0, 0.014)]
    mb.lathe(plate, WOOD_L, seg=20)
    with mb.at((0, 0.184, 0), rot=(math.pi, 0, 0)):
        mb.lathe(plate, WOOD_L, seg=20)
    half = [(0.0052, 0.014), (0.0064, 0.020), (0.0064, 0.025), (0.0040, 0.031), (0.0052, 0.046), (0.0072, 0.064), (0.0060, 0.077), (0.0042, 0.084),
            (0.0062, 0.0905)]
    post = half + [(r, 0.184 - y) for r, y in reversed(half)]
    for i in range(3):
        a = math.tau * i / 3
        with mb.at((math.cos(a) * 0.042, 0, math.sin(a) * 0.042)):
            mb.lathe(post, WOOD_L, seg=8)
    # (the sand is drawn in the app, so it can run down after each turn)
    p.part("base", mb)
    g = MB()
    g.lathe([(0, 0.0141), (0.012, 0.0148), (0.026, 0.021), (0.033, 0.030), (0.0352, 0.045), (0.034, 0.060), (0.027, 0.074), (0.016, 0.084), (0.0055, 0.0905),
             (0.0048, 0.092), (0.0055, 0.0935), (0.016, 0.100), (0.027, 0.110), (0.034, 0.124), (0.0352, 0.139), (0.033, 0.154), (0.026, 0.163),
             (0.012, 0.1692), (0, 0.1699)], "#DFE6E2", seg=20)
    p.part("glass", g)
    return p


BUILDERS = {
    "study/atlases": atlases, "study/rolled-maps": rolled_maps, "study/map-case": map_case,
    "study/lamp-candle": lamp_candle, "study/lamp-oil": lamp_oil, "study/lamp-bronze": lamp_bronze,
    "study/lamp-andon": lamp_andon, "study/lamp-brazier": lamp_brazier, "study/sandglass": sandglass,
}
