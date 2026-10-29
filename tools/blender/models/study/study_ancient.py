"""
Writing things of the older and farther worlds: a clay tablet with a cylinder seal and a stylus, an Egyptian scribe's
palette, a reed pen and ink pot, a Roman wax tablet diptych with its stylus, a papyrus roll, a palm-leaf manuscript
between its boards, a Timbuktu manuscript in its leather wallet, a quipu, and a painted screenfold codex.
Metres, origin where the app puts the prop's group.

tex_* parts carry UVs: the app paints them with its own canvas textures (cuneiform, the papyrus text, the codex).
"""
import math

from studykit import MB, StudyProp, rrect
from study_desk import roll

INK, CLAY = "#1E1610", "#8E5034"
WOOD_L, WOOD_D = "#6A4428", "#32200F"
BRASS = "#A8823A"


def _uv_quad(tex, corners, color):
    xs = [p[0] for p in corners]
    zs = [p[2] for p in corners]
    x0, x1, z0, z1 = min(xs), max(xs), min(zs), max(zs)
    uvs = [((p[0] - x0) / (x1 - x0), (p[2] - z0) / (z1 - z0)) for p in corners]
    tex.quad_uv(corners, uvs, color)


def stadium(l, w, n=6):
    """A long rounded outline [(x, z)] along X, counter-clockwise from above."""
    r = w / 2
    out = []
    for i in range(n + 1):
        a = -math.pi / 2 + math.pi * i / n
        out.append((l / 2 - r + r * math.cos(a), r * math.sin(a)))
    for i in range(n + 1):
        a = math.pi / 2 + math.pi * i / n
        out.append((-l / 2 + r + r * math.cos(a), r * math.sin(a)))
    return out


# ---------------------------------------------------------------- clay tablet

def clay_tablet():
    p = StudyProp("clay-tablet", ao=0.02, edge=0.05)
    mb, tex = MB(), MB()
    C = "#9A7A50"
    with mb.at((0, 0.015, 0), rot=(0, 0.3, 0)):
        top = mb.box(0.1, 0.03, 0.14, (0, 0, 0), C, bevel=0.008, seg=3, skip_top=True)
    with tex.at((0, 0.015, 0), rot=(0, 0.3, 0)):
        _uv_quad(tex, top, C)
    # a cylinder seal, its carved bands, and a reed stylus with a wedge tip
    with mb.at((0.09, 0.012, 0.06), rot=(0, -0.4, math.pi / 2)):
        prof = [(0, -0.02), (0.0105, -0.02), (0.012, -0.019), (0.012, -0.012), (0.0108, -0.011), (0.0108, -0.009), (0.012, -0.008), (0.012, 0.004),
                (0.0108, 0.005), (0.0108, 0.007), (0.012, 0.008), (0.012, 0.019), (0.0105, 0.02), (0.003, 0.02), (0.0028, 0.0195), (0, 0.0195)]
        mb.lathe(prof, "#6A6058", seg=16, colors=["#6A6058"] * 13 + ["#2A2420", "#2A2420"])
    mb.tube([(-0.075, 0.0034, 0.095), (0.045, 0.0034, 0.083)], 0.0034, "#B39A62", seg=3, smooth=False)
    p.part("base", mb, angle=50)
    p.part("tex_face", tex)
    return p


# ---------------------------------------------------------------- the scribe's palette

def palette():
    p = StudyProp("palette", ao=0.02, edge=0.05)
    mb = MB()
    with mb.at((0, 0, 0), rot=(0, -0.2, 0)):
        mb.box(0.3, 0.014, 0.06, (0, 0.007, 0), WOOD_L, bevel=0.002, seg=2)
        for x, c in ((-0.12, INK), (-0.09, "#8A2A1A")):
            with mb.at((x, 0.0138, -0.012)):
                mb.lathe([(0.0092, 0), (0.0108, 0.0002), (0.0108, 0.0009), (0.0092, 0.0011)], "#4E3220", seg=16)
                mb.lathe([(0, 0), (0.0094, 0), (0.0094, 0.0006), (0.006, 0.0011), (0, 0.0013)], c, seg=16)
        # the reeds in the slot, held by a slip of wood
        for i, (l, z) in enumerate(((0.2, 0.008), (0.185, 0.0145))):
            with mb.at((0.03 - (0.2 - l) / 2, 0.0168, z), rot=(0, 0, math.pi / 2)):
                mb.lathe([(0, -l / 2), (0.0022, -l / 2 + 0.006), (0.0028, -l / 2 + 0.012), (0.0028, l / 2), (0, l / 2)], "#C2A868", seg=6)
        mb.box(0.014, 0.0045, 0.03, (-0.03, 0.0186, 0.011), "#5A3A24", bevel=0.001, seg=1)
        # a column of signs, the scribe's name
        for k, (dx, dz, w, d) in enumerate(((0.0, 0.0, 0.006, 0.004), (0.0, 0.007, 0.004, 0.003), (0.0, 0.013, 0.007, 0.0025), (0.0, 0.019, 0.003, 0.005))):
            mb.box(w, 0.0008, d, (0.135 + dx, 0.0143, -0.016 + dz), "#2A1C10")
    p.part("base", mb)
    return p


# ---------------------------------------------------------------- reed pen and ink pot

def reed():
    p = StudyProp("reed", ao=0.02, edge=0.05)
    mb = MB()
    pot = [(0, 0), (0.024, 0), (0.028, 0.006), (0.032, 0.020), (0.030, 0.038), (0.018, 0.048), (0.020, 0.0535), (0.0195, 0.055), (0.0142, 0.055),
           (0.0138, 0.050), (0.0136, 0.047), (0, 0.047)]
    mb.lathe(pot, CLAY, seg=20, colors=[CLAY, CLAY, "#7A4430", CLAY, CLAY, CLAY, CLAY, CLAY, "#4A2A18", "#2A1A10", INK])
    for (x, z, a, l) in ((0.08, 0.03, 0.4, 0.2), (0.07, 0.055, 0.25, 0.17)):
        with mb.at((x, 0.0036, z), rot=(0, a, math.pi / 2)):
            mb.lathe([(0, -l / 2), (0.0006, -l / 2 + 0.002), (0.0024, -l / 2 + 0.012), (0.0034, -l / 2 + 0.024), (0.0035, -0.02), (0.0039, -0.019),
                      (0.0035, -0.018), (0.0035, 0.04), (0.0039, 0.041), (0.0035, 0.042), (0.0035, l / 2), (0, l / 2)], "#B39A5C", seg=7,
                     colors=[INK, INK, "#5A4A2E", "#B39A5C", "#9A824A", "#9A824A", "#B39A5C", "#9A824A", "#9A824A", "#B39A5C", "#B39A5C"])
    p.part("base", mb)
    return p


# ---------------------------------------------------------------- wax tablet

def wax_tablet():
    p = StudyProp("wax-tablet", ao=0.02, edge=0.05)
    mb = MB()
    with mb.at((0, 0, 0), rot=(0, -0.25, 0)):
        for s in (-1, 1):
            with mb.at((s * 0.072, 0, 0)):
                mb.prism(rrect(0.14, 0.1, 0.006, 3), 0.0, 0.0065, WOOD_L, bevel=0.0015, seg=1)
                mb.ring_prism(rrect(0.14, 0.1, 0.006, 3), rrect(0.12, 0.08, 0.003, 3), 0.0065, 0.016, WOOD_L)
                mb.prism(rrect(0.1206, 0.0806, 0.003, 3), 0.005, 0.0105, "#3A2A1A")
                if s < 0:
                    # lines scratched in the wax
                    for row in range(6):
                        x = -0.05
                        k = 0
                        while x < 0.045:
                            w = 0.006 + ((row * 7 + k * 3) % 5) * 0.003
                            mb.box(min(w, 0.05 - x), 0.001, 0.0011, (x + w / 2, 0.0108, -0.03 + row * 0.011), "#5E4A34")
                            x += w + 0.004
                            k += 1
        # the leather ties of the hinge
        for z in (-0.025, 0.025):
            mb.tube([(0.006 * math.cos(a), 0.008 + 0.006 * math.sin(a), z) for a in [math.tau * j / 10 for j in range(11)]], 0.0012, "#4A2A16", seg=4)
        # the stylus: a point to write, a flat end to smooth the wax
        with mb.at((0.02, 0.0188, 0.07), rot=(0, 0, -math.pi / 2)):
            mb.lathe([(0, -0.065), (0.0012, -0.06), (0.0024, -0.045), (0.0026, -0.02), (0.0032, -0.018), (0.0026, -0.016), (0.0026, 0.03), (0.0032, 0.032),
                      (0.0026, 0.034), (0.0018, 0.05), (0, 0.052)], BRASS, seg=8)
        mb.box(0.014, 0.0018, 0.009, (0.02 + 0.058, 0.0188, 0.07), BRASS, bevel=0.0006, seg=1)
    p.part("base", mb)
    return p


# ---------------------------------------------------------------- papyrus

def scroll():
    p = StudyProp("scroll", ao=0.02, edge=0.06)
    mb, tex = MB(), MB()
    sheet = "#CDB47C"
    with mb.at((0, 0, 0), rot=(0, 0.15, 0)):
        for s, r in ((-1, 0.024), (1, 0.018)):
            with mb.at((s * 0.13, r, 0), rot=(0, math.pi / 2, 0)):
                roll(mb, r, 0.1, sheet, turns=3.0, start=-1.2 if s < 0 else 1.3, ties=None)
        top = mb.box(0.26, 0.0012, 0.094, (0, 0.0009, 0), sheet, skip_top=True)
    with tex.at((0, 0, 0), rot=(0, 0.15, 0)):
        _uv_quad(tex, top, sheet)
    p.part("base", mb, angle=60)
    p.part("tex_sheet", tex)
    return p


# ---------------------------------------------------------------- palm leaf and Timbuktu

def palm_leaf():
    p = StudyProp("palm-leaf", ao=0.02, edge=0.06)
    mb = MB()
    with mb.at((0, 0, 0), rot=(0, 0.2, 0)):
        mb.prism(stadium(0.27, 0.052), 0.0, 0.009, WOOD_L, bevel=0.0015, seg=1)
        y = 0.0092
        cols = ["#C9B27A", "#BFA66E", "#CDB880", "#C4AC74"]
        for i in range(10):
            dx = ((i * 37) % 7 - 3) * 0.0006
            dz = ((i * 53) % 5 - 2) * 0.0005
            with mb.at((dx, 0, dz)):
                mb.prism(stadium(0.258 - (i % 3) * 0.002, 0.046), y, y + 0.0014, cols[i % 4])
            y += 0.0015
        mb.prism(stadium(0.27, 0.052), y + 0.0001, y + 0.0091, WOOD_L, bevel=0.0015, seg=1)
        yt = y + 0.0091
        mb.ring_prism(stadium(0.262, 0.044), stadium(0.252, 0.034), yt - 0.0002, yt + 0.0006, "#7A3020")
        # the cord through the leaves, wound round the bundle, with its bone toggle
        for x in (-0.07, 0.07):
            h0, h1 = -0.0006, yt + 0.0012
            path = []
            for k in range(17):
                a = math.tau * k / 16
                path.append((x + 0.0012 * k / 16, (h0 + h1) / 2 + (h1 - h0) / 2 * 1.04 * math.sin(a), 0.0272 * math.cos(a)))
            mb.tube(path, 0.0013, "#7A3020", seg=5)
        mb.ellipsoid((0.0, yt + 0.003, 0.0), 0.009, 0.0026, 0.0034, "#D8CCB0", seg=10, rings=5)
        mb.tube([(-0.07, yt + 0.0014, 0.0), (-0.035, yt + 0.0022, 0.002), (-0.006, yt + 0.003, 0.0)], 0.0012, "#7A3020", seg=5)
    p.part("base", mb)
    return p


def manuscript():
    p = StudyProp("manuscript", ao=0.02, edge=0.05)
    mb = MB()
    L, LD, T = "#6A3E22", "#4A2A16", "#8A5A30"
    with mb.at((0, 0, 0), rot=(0, 0.2, 0)):
        mb.box(0.17, 0.022, 0.125, (0, 0.011, 0), L, bevel=0.004, seg=2)
        # loose leaves fanned out of the wallet, a few lines of script on the top one
        for i, (dx, a) in enumerate(((0.024, 0.04), (0.03, 0.11), (0.036, -0.03))):
            y = 0.0223 + i * 0.0009
            with mb.at((dx, 0, 0.004), rot=(0, a, 0)):
                mb.box(0.13, 0.0007, 0.1, (0, y + 0.00035, 0), "#D4C49C" if i != 1 else "#CDBB92")
                if i == 2:
                    for row in range(9):
                        x = -0.045
                        k = 0
                        while x < 0.055:
                            w = 0.008 + ((row * 5 + k * 7) % 6) * 0.004
                            w = min(w, 0.058 - x)
                            mb.box(w, 0.0006, 0.0014, (x + w / 2, y + 0.001, -0.04 + row * 0.0095), "#2A1C12")
                            x += w + 0.003
                            k += 1
        # the flap, tooled
        flap = [(-0.086, -0.0628), (0.0, -0.0628), (0.03, 0.0), (0.0, 0.0628), (-0.086, 0.0628)]
        mb.prism(flap, 0.0222, 0.0256, LD, bevel=0.0008, seg=1)
        inner = [(-0.078, -0.054), (-0.004, -0.054), (0.02, 0.0), (-0.004, 0.054), (-0.078, 0.054)]
        inner2 = [(-0.074, -0.05), (-0.006, -0.05), (0.0152, 0.0), (-0.006, 0.05), (-0.074, 0.05)]
        mb.ring_prism(inner, inner2, 0.0252, 0.0262, T)
        with mb.at((-0.03, 0.0255, 0)):
            mb.lathe([(0, 0), (0.011, 0), (0.011, 0.0006), (0.007, 0.0012), (0, 0.0014)], T, seg=12)
    p.part("base", mb)
    return p


# ---------------------------------------------------------------- quipu

def quipu():
    p = StudyProp("quipu", ao=0.015, edge=0.06)
    mb = MB()
    cols = ["#B39A62", "#7A3220", "#3C5A4A", "#D8CCB0", "#5A4A32"]
    main = [(-0.135 + 0.27 * i / 12, 0.0036, 0.004 * math.sin(i * 0.9)) for i in range(13)]
    mb.tube(main, 0.0034, "#A8905A", seg=6)
    for s in (-1, 1):
        x = s * 0.135
        with mb.at((x, 0.0036, 0), rot=(0, 0, -s * math.pi / 2)):
            mb.lathe([(0, -0.001), (0.0036, 0), (0.0046, 0.008), (0.003, 0.014), (0, 0.016)], "#A8905A", seg=6)
    for i in range(10):
        x0 = -0.11 + i * 0.024
        a = (i - 4.5) * 0.06
        l = 0.1 + ((i * 37) % 5) * 0.012
        c = cols[i % 5]
        path = []
        for k in range(9):
            t = k / 8
            d = l * t
            wob = 0.003 * math.sin(t * 5 + i)
            path.append((x0 + math.sin(a) * d + wob * math.cos(a), 0.0017 + 0.0016 * (1 - t) ** 3, 0.004 + math.cos(a) * d))
        mb.tube(path, 0.0016, c, seg=5)
        for kk, f in enumerate([0.3, 0.55, 0.8][: 1 + (i % 3)]):
            d = l * f
            px = x0 + math.sin(a) * d + 0.003 * math.sin(f * 5 + i) * math.cos(a)
            pz = 0.004 + math.cos(a) * d
            long = (i + kk) % 4 == 0
            with mb.at((px, 0.0019, pz), rot=(0, a, 0)):
                mb.ellipsoid((0, 0, 0), 0.0032, 0.0026, 0.0068 if long else 0.0036, c, seg=8, rings=4)
        if i in (2, 5, 8):
            # a subsidiary cord tied onto the pendant
            d0 = l * 0.45
            bx, bz = x0 + math.sin(a) * d0, 0.004 + math.cos(a) * d0
            sub = [(bx + 0.012 * t + 0.003 * math.sin(t * 4), 0.0015, bz + 0.045 * t) for t in [k / 6 for k in range(7)]]
            mb.tube(sub, 0.0012, cols[(i + 2) % 5], seg=4)
    p.part("base", mb, angle=60)
    return p


# ---------------------------------------------------------------- codex

def codex():
    p = StudyProp("codex", ao=0.02, edge=0.05)
    mb, tex = MB(), MB()
    G = "#D2C3A0"
    xs = [-0.12 + 0.06 * k for k in range(5)]
    ys = [0.0035 if k % 2 == 0 else 0.0095 for k in range(5)]
    t = 0.0016
    for i in range(4):
        x0, x1, y0, y1 = xs[i], xs[i + 1], ys[i], ys[i + 1]
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        ang = math.atan2(y1 - y0, x1 - x0)
        ln = math.hypot(x1 - x0, y1 - y0) + 0.0012
        with mb.at((0, 0, 0), rot=(0, -0.2, 0)):
            with mb.at((cx, cy, 0), rot=(0, 0, ang)):
                top = mb.box(ln, t, 0.09, (0, 0, 0), G, skip_top=True)
        with tex.at((0, 0, 0), rot=(0, -0.2, 0)):
            with tex.at((cx, cy, 0), rot=(0, 0, ang)):
                xs_ = [q[0] for q in top]
                zs_ = [q[2] for q in top]
                ax, bx, az, bz = min(xs_), max(xs_), min(zs_), max(zs_)
                uvs = [((i + (q[0] - ax) / (bx - ax)) / 4, (q[2] - az) / (bz - az)) for q in top]
                tex.quad_uv(top, uvs, G)
    p.part("base", mb)
    p.part("tex_panels", tex)
    return p


BUILDERS = {
    "study/clay-tablet": clay_tablet, "study/palette": palette, "study/reed": reed, "study/wax-tablet": wax_tablet,
    "study/scroll": scroll, "study/palm-leaf": palm_leaf, "study/manuscript": manuscript, "study/quipu": quipu, "study/codex": codex,
}
