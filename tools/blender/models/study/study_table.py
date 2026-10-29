"""
The writing table the map lies on: a moulded top edge (ovolo over a cove), an apron with a cock-beaded lower edge,
carved drops and spandrel brackets, two drawers a side with batwing brass bail pulls and keyhole escutcheons, turned
baluster legs on bun feet, joined low down by moulded stretchers.

The table's size follows the map, so it is exported as parts the web app places itself: the long straight pieces
(top moulding, apron, stretcher, the core of the top) are scaled along their length only, everything carved or turned
is placed at its true size. The whole table is assembled here at a reference size so the baked occlusion sees the
real neighbours (the apron under the top's overhang, the legs under the apron), and one of each part is exported.
"""
import math

from studykit import MB, StudyProp, arc_pts

TW, TD = 1.72, 1.55               # reference table, metres
INSET_LEG = 0.09                  # leg centre in from the edge
INSET_APRON = 0.075               # apron face in from the edge
FLOOR = -0.785
APRON_TOP, APRON_BOT = -0.0345, -0.132
DRAWER_Y = -0.076
STRETCHER_Y = FLOOR + 0.12

WOOD = "#5A3822"       # figured walnut; the app tints it per atlas (oak, walnut, black lacquer)
WOOD_D = "#3E2616"     # the turned legs and stretchers, a shade darker with handling
BRASS = "#9C7A3C"
BRASS_D = "#6A5226"
KEY = "#120C08"


def _dedupe(pts):
    out = []
    for p in pts:
        if not out or abs(out[-1][0] - p[0]) > 1e-7 or abs(out[-1][1] - p[1]) > 1e-7:
            out.append(p)
    return out


# the top's edge, (outward, y), from under the top to its upper face: a fillet, a cove, a step and an ovolo
TOP_PROFILE = _dedupe([(0.0, -0.034), (0.002, -0.034), (0.002, -0.031)]
                      + arc_pts(0.013, -0.031, 0.011, 180, 90, 6)
                      + [(0.0165, -0.020), (0.0165, -0.0126)]
                      + arc_pts(0.0045, -0.0126, 0.012, 0, 90, 7)
                      + [(0.0, -0.0006)])

# the apron board, (outward from its face, y): the cock bead along its lower edge
APRON_PROFILE = _dedupe([(-0.022, APRON_BOT), (0.0, APRON_BOT), (0.003, APRON_BOT + 0.0006)]
                        + arc_pts(0.0005, APRON_BOT + 0.0075, 0.0068, -68, 90, 6)
                        + [(0.0, APRON_BOT + 0.0143), (0.0, APRON_TOP), (-0.022, APRON_TOP), (-0.022, APRON_BOT)])

# a stretcher's section about its centre line: square below, rounded above
STRETCHER_PROFILE = [(-0.014, -0.017), (0.014, -0.017), (0.014, 0.008), (0.012, 0.0135), (0.0075, 0.0165), (0.0, 0.017),
                     (-0.0075, 0.0165), (-0.012, 0.0135), (-0.014, 0.008), (-0.014, -0.017)]

# the turned leg, (r, y) from the floor: bun foot, collar, a square for the stretchers, ring, baluster, cup, block
LEG_LOW = [(0, 0), (0.026, 0), (0.034, 0.003), (0.041, 0.010), (0.045, 0.020), (0.046, 0.028), (0.044, 0.038), (0.038, 0.047),
           (0.029, 0.054), (0.021, 0.058), (0.019, 0.062), (0.024, 0.066), (0.027, 0.070), (0.027, 0.076), (0.023, 0.080), (0.021, 0.090), (0, 0.090)]
LEG_HIGH = [(0, 0.150), (0.021, 0.150), (0.023, 0.156), (0.030, 0.162), (0.031, 0.168), (0.029, 0.174), (0.021, 0.178), (0.017, 0.188),
            (0.019, 0.205), (0.025, 0.232), (0.033, 0.268), (0.040, 0.305), (0.0435, 0.335), (0.0435, 0.355), (0.041, 0.382), (0.034, 0.415),
            (0.026, 0.448), (0.019, 0.476), (0.016, 0.492), (0.019, 0.500), (0.027, 0.506), (0.030, 0.514), (0.027, 0.522), (0.019, 0.528),
            (0.016, 0.540), (0.019, 0.555), (0.026, 0.575), (0.032, 0.598), (0.035, 0.618), (0.035, 0.630), (0.031, 0.638), (0.026, 0.642),
            (0.025, 0.652), (0, 0.652)]
LEG_TOP = -0.035 - FLOOR          # the block's top, under the top's core


def leg(mb):
    mb.lathe(LEG_LOW, WOOD_D, seg=16)
    mb.box(0.05, 0.06, 0.05, (0, 0.12, 0), WOOD_D, bevel=0.003, seg=2)
    mb.lathe(LEG_HIGH, WOOD_D, seg=16)
    mb.box(0.075, LEG_TOP - 0.648, 0.075, (0, (LEG_TOP + 0.648) / 2, 0), WOOD, bevel=0.0035, seg=2)


def top_run(mb, length):
    mb.run_x(TOP_PROFILE, -length / 2, length / 2, WOOD)


def apron_run(mb, length):
    mb.run_x(APRON_PROFILE, -length / 2, length / 2, WOOD)


def stretcher(mb, length):
    mb.run_x(STRETCHER_PROFILE, -length / 2, length / 2, WOOD_D)


def _batwing():
    half = [(0.0, 0.0115), (0.007, 0.0118), (0.013, 0.0146), (0.019, 0.0150), (0.0245, 0.0118), (0.0285, 0.0062), (0.0262, 0.0),
            (0.0285, -0.0062), (0.0245, -0.0118), (0.019, -0.0150), (0.013, -0.0146), (0.007, -0.0118), (0.0, -0.0115)]
    return half + [(-x, y) for x, y in reversed(half[1:-1])]


def _escutcheon():
    pts = []
    for i in range(16):
        a = math.tau * i / 16
        r = 0.0105 + 0.0018 * math.cos(4 * a)
        pts.append((r * math.sin(a) * 0.85, r * math.cos(a) * 1.18))
    return pts


def _face_plate(mb, outline_xy, z0, z1, color, bevel=0.0):
    """A flat plate on a drawer's face (the XY plane), from z0 out to z1."""
    with mb.at((0, 0, z0), rot=(math.pi / 2, 0, 0)):
        mb.prism([(x, -y) for x, y in outline_xy], 0.0, z1 - z0, color, bevel=bevel, seg=1)


def drawer(mb):
    """A drawer front, 8 mm proud of the apron (its face at z = +0.008), its thumbnail lip rounded."""
    mb.box(0.28, 0.062, 0.016, (0, 0, 0), WOOD, bevel=0.0045, seg=2)


def drawer_brass(mb):
    F = 0.008
    for sx in (-1, 1):
        cx = sx * 0.078
        with mb.at((cx, 0.002, 0)):
            _face_plate(mb, _batwing(), F + 0.0005, F + 0.0018, BRASS)
            for px in (-0.019, 0.019):
                with mb.at((px, 0.0, F + 0.0018), rot=(math.pi / 2, 0, 0)):
                    mb.lathe([(0.0024, 0), (0.0024, 0.004), (0.0031, 0.0052), (0.0022, 0.0066), (0, 0.0068)], BRASS_D, seg=6)
            path = []
            for i in range(11):
                s = math.pi * i / 10
                path.append((0.019 * math.cos(s), -0.0005 - 0.0135 * math.sin(s), F + 0.0068 - 0.0012 + 0.0026 * math.sin(s)))
            mb.tube(path, 0.0017, BRASS, seg=5)
    _face_plate(mb, _escutcheon(), F + 0.0005, F + 0.0016, BRASS)
    _face_plate(mb, [(0.0028 * math.cos(a), 0.0035 + 0.0028 * math.sin(a)) for a in [math.radians(-60 + 300 * i / 9) for i in range(10)]]
                + [(-0.0016, -0.006), (0.0016, -0.006)], F + 0.0016, F + 0.0020, KEY)


def pendant(mb):
    """The carved drop under the middle of each apron: a lobed tongue with a turned boss."""
    pts = []
    n = 28
    for i in range(n + 1):
        x = -0.09 + 0.18 * i / n
        y = -(0.004 + 0.032 * math.cos(math.pi * x / 0.18) ** 3) - 0.007 * math.sin(math.pi * abs(x) / 0.045) ** 2 * (abs(x) < 0.09)
        pts.append((x, y))
    outline = [(0.09, 0.004), (-0.09, 0.004)] + pts
    _face_plate(mb, outline, -0.020, -0.0025, WOOD)
    with mb.at((0, -0.017, -0.0025), rot=(math.pi / 2, 0, 0)):
        mb.lathe([(0, 0), (0.0085, 0), (0.0085, 0.0015), (0.0065, 0.0035), (0.003, 0.0048), (0, 0.005)], WOOD, seg=14)


def bracket(mb, side):
    """A spandrel bracket in the corner between a leg block (at x = 0) and the apron's lower edge (y = 0),
    reaching toward -x * side."""
    pts = [(0.0, 0.004), (0.0, -0.05)]
    for i in range(9):
        t = math.radians(90 - 90 * i / 8)
        pts.append((-0.062 + 0.062 * math.sin(t), -0.05 + 0.05 * math.cos(t)))
    pts.append((-0.062, 0.004))
    pts = [(x * side, y) for x, y in pts]
    _face_plate(mb, pts, -0.018, -0.0015, WOOD)


PARTS = ["top_run", "top_corner", "core", "apron_run", "leg", "stretcher", "drawer", "drawer_brass", "pendant", "bracket_r", "bracket_l"]


def build():
    p = StudyProp("table", ao=0.09, edge=0.05, ground=False)
    hx, hz = TW / 2, TD / 2
    lx, lz = hx - INSET_LEG, hz - INSET_LEG
    az = hz - INSET_APRON
    sides = [  # (rotation about y, half length along the side, distance out to the edge): front, right, back, left
        (0.0, hx, hz), (math.pi / 2, hz, hx), (math.pi, hx, hz), (-math.pi / 2, hz, hx)]

    def ex(name, pos, fn, angle=48.0):
        mb = MB()
        with mb.at(pos):
            fn(mb)
        p.part(name, mb, pos, angle)

    # ---- the exported parts, drawn in table coordinates and kept relative to their pivots
    ex("top_run", (0, 0, hz), lambda m: top_run(m, TW))
    ex("top_corner", (hx, 0, hz), lambda m: m.corner(TOP_PROFILE, WOOD))
    ex("core", (0, 0, 0), lambda m: m.box(TW, 0.032, TD, (0, -0.0175, 0), WOOD))
    ex("apron_run", (0, 0, az), lambda m: apron_run(m, TW - 2 * INSET_LEG))
    ex("leg", (lx, FLOOR, lz), leg)
    ex("stretcher", (0, STRETCHER_Y, lz), lambda m: stretcher(m, 2 * lx))
    ex("drawer", (TW * 0.2, DRAWER_Y, az), drawer)
    ex("drawer_brass", (TW * 0.2, DRAWER_Y, az), drawer_brass, angle=60)
    ex("pendant", (0, APRON_BOT, az), pendant)
    ex("bracket_r", (lx - 0.0375, APRON_BOT, az), lambda m: bracket(m, 1))
    ex("bracket_l", (-(lx - 0.0375), APRON_BOT, az), lambda m: bracket(m, -1))

    # ---- the rest of the table, only to shade the occlusion
    c = MB()
    for k, (ry, half, out) in enumerate(sides):
        with c.at(rot=(0, ry, 0)):
            if k:
                with c.at((0, 0, out)):
                    top_run(c, 2 * half)
                with c.at((0, 0, out - INSET_APRON)):
                    apron_run(c, 2 * (half - INSET_LEG))
                with c.at((0, STRETCHER_Y, out - INSET_LEG)):
                    stretcher(c, 2 * (half - INSET_LEG))
                with c.at((0, APRON_BOT, out - INSET_APRON)):
                    pendant(c)
                with c.at((half, 0, out)):
                    c.corner(TOP_PROFILE, WOOD)
            for s in (-1, 1):
                if k == 0 and s == 1:
                    continue
                with c.at((s * (half - INSET_LEG - 0.0375), APRON_BOT, out - INSET_APRON)):
                    bracket(c, s)
            if k in (0, 2):
                for s in (-1, 1):
                    if k == 0 and s == 1:
                        continue
                    with c.at((s * TW * 0.2, DRAWER_Y, out - INSET_APRON)):
                        drawer(c)
                        drawer_brass(c)
    for sx, sz in ((-1, 1), (1, -1), (-1, -1)):
        with c.at((sx * lx, FLOOR, sz * lz)):
            leg(c)
    c.box(4.0, 0.01, 4.0, (0, FLOOR - 0.005, 0), "#20160E")   # the floor
    p.ctx(c)
    return p


BUILDERS = {"study/table": build}
