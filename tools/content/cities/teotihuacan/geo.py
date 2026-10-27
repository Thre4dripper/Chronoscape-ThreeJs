# Teotihuacan: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
import math

T, M, X, C, A = "tzacualli-100", "miccaotli-250", "xolalpan-450", "collapse-650", "aztec-1500"
ALL = [T, M, X, C, A]
CLASSIC = [M, X, C]

# The city is laid out on a grid turned 15.5 degrees east of north, the line of the Avenue of the Dead.
# G(u, v) gives (lat, lon) for a point u metres along the avenue (north positive) and v metres across it
# (east positive) from the centre of the Pyramid of the Moon, which stands on the avenue's axis.
P0 = (19.6996, -98.8440)
_A = math.radians(15.5)
KY, KX = 110850.0, 111320.0 * math.cos(math.radians(19.70))


def G(u, v):
    n = u * math.cos(_A) - v * math.sin(_A)
    e = u * math.sin(_A) + v * math.cos(_A)
    return (round(P0[0] + n / KY, 6), round(P0[1] + e / KX, 6))


FRAME = ((19.7065, -98.8735), (19.6700, -98.8265))
_PAD = 0.0004


def _clip(poly):
    """Clip a polygon to the frame (less a small margin): Sutherland-Hodgman against the four edges."""
    (n, w), (s, e) = FRAME
    n, s, w, e = n - _PAD, s + _PAD, w + _PAD, e - _PAD
    edges = [(lambda p: p[0] <= n, lambda a, b: (n, a[1] + (b[1] - a[1]) * (n - a[0]) / (b[0] - a[0]))),
             (lambda p: p[0] >= s, lambda a, b: (s, a[1] + (b[1] - a[1]) * (s - a[0]) / (b[0] - a[0]))),
             (lambda p: p[1] >= w, lambda a, b: (a[0] + (b[0] - a[0]) * (w - a[1]) / (b[1] - a[1]), w)),
             (lambda p: p[1] <= e, lambda a, b: (a[0] + (b[0] - a[0]) * (e - a[1]) / (b[1] - a[1]), e))]
    out = list(poly)
    for inside, cut in edges:
        src, out = out, []
        for i, cur in enumerate(src):
            prev = src[i - 1]
            if inside(cur):
                if not inside(prev):
                    out.append(cut(prev, cur))
                out.append(cur)
            elif inside(prev):
                out.append(cut(prev, cur))
        if not out:
            return []
    return [(round(a, 6), round(b, 6)) for a, b in out]


def R(u0, u1, v0, v1):
    """A rectangle of the turned grid between u0..u1 and v0..v1, clipped to the frame."""
    return _clip([G(u0, v0), G(u0, v1), G(u1, v1), G(u1, v0)])


def L(*uv):
    return [G(u, v) for u, v in uv]


CITY = dict(
    name="Teotihuacan", subtitle="City of the Gods",
    description="The planned city of Teotihuacan in the north-east of the Basin of Mexico, from the first decades of the Pyramid of the Sun to the overgrown mounds the Aztecs visited as the place where the gods were born: the Avenue of the Dead, the pyramids, the Ciudadela and the apartment compounds of the grid. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId=X,
    world=dict(heightScale=1.0, walls=["#EDE4D0", "#E4D7BC", "#D9C7A6", "#C9A58A"], roofs=["#CDBB98", "#C2AE8A"]),
    camera=dict(target=G(-1000, 80), distance=42),
)

PALETTE = dict(parchment="#E6D3AA", ink="#6F4D34", water="#62878A", hill="#7A7A58", road="#8A6A4A")
COMPASS = (19.7035, -98.8300)
CARTOUCHE = (19.6712, -98.8405)

SOURCES = [
    dict(id="millon-1973", title="Urbanization at Teotihuacan, Mexico, vol. 1: The Teotihuacan Map", author="René Millon, R. Bruce Drewitt and George L. Cowgill", year=1973, note="the survey map of the whole city on which every later plan is based"),
    dict(id="cowgill-2015", title="Ancient Teotihuacan: Early Urbanism in Central Mexico", author="George L. Cowgill", year=2015),
    dict(id="sugiyama-2005", title="Human Sacrifice, Militarism, and Rulership: Materialization of State Ideology at the Feathered Serpent Pyramid, Teotihuacan", author="Saburo Sugiyama", year=2005),
    dict(id="manzanilla", title="Teotihuacan, ciudad excepcional de Mesoamérica", author="Linda R. Manzanilla", year=2017),
    dict(id="sanders-1979", title="The Basin of Mexico: Ecological Processes in the Evolution of a Civilization", author="William T. Sanders, Jeffrey R. Parsons and Robert S. Santley", year=1979),
    dict(id="wiki-teotihuacan", title="Teotihuacan", author="Wikipedia", url="https://en.wikipedia.org/wiki/Teotihuacan"),
    dict(id="wiki-avenue", title="Teotihuacan (the Avenue of the Dead)", author="Wikipedia", url="https://en.wikipedia.org/wiki/Teotihuacan"),
    dict(id="wiki-cerro-gordo", title="Cerro Gordo (Mexico State)", author="Wikipedia", url="https://en.wikipedia.org/wiki/Teotihuacan#Geography"),
]

PERIODS = [
    dict(id=T, label="The Early City", year=100, startYear=1, endYear=149,
         summary="People from across the Basin of Mexico gather in the Teotihuacan valley, round its springs and the obsidian of the hills. By 100 CE the settlement may already spread over many square kilometres, though thinly. Work has begun on the Pyramid of the Sun over a cave; the Moon pyramid is still a small platform. Houses are of adobe, wattle and thatch.",
         population="perhaps 60,000–80,000 (Millon's estimate; others are lower)",
         feel="Dust from basket-loads of rubble tipped into the rising pyramid, smoke of cooking fires over thatch, the click of obsidian knapping in every yard.",
         style="mesoamerican",
         houses=dict(title="Adobe and wattle houses", text="Groups of small rooms of adobe or wattle and daub on stone footings, thatched or flat-roofed, round an open yard with hearths and storage pits. The stone apartment compounds of later centuries do not exist yet."),
         outskirts=dict(title="Hamlets and fields", text="Scattered houses among maize fields on the valley floor, with terraces on the slopes of Cerro Gordo and canals led off the springs to the south-west.")),
    dict(id=M, label="The City Laid Out", year=250, startYear=150, endYear=349,
         summary="The Sun pyramid is finished and the Moon enlarged; in the Ciudadela the Feathered Serpent Pyramid is dedicated over some 200 sacrificial burials. The whole city is set out on one grid turned 15.5° east of north, the rivers straightened to fit it, and from about 225 the people move into walled stone apartment compounds.",
         population="perhaps 80,000–100,000",
         feel="Lime kilns smoking, gangs carrying volcanic stone along the new avenue, drums at dusk from the Ciudadela.",
         style="mesoamerican",
         houses=dict(title="The first apartment compounds", text="Walled one-storey compounds of stone and rubble faced with lime plaster, 50–60 m a side, with many rooms round several open patios. Each housed some 60 to 100 people, probably related families sharing a craft."),
         outskirts=dict(title="Adobe houses and fields", text="Older adobe houses not yet rebuilt in stone, with maize, beans and squash on the edge of the grid and irrigated plots by the springs.")),
    dict(id=X, label="City of the Gods", year=450, startYear=350, endYear=549,
         summary="The largest city in the Americas: 100,000 or more people in some 2,000 apartment compounds over about 20 km². Merchants, Zapotec settlers from Oaxaca and families from the Gulf coast live in their own barrios; walls are painted with gods, priests and jaguars; Teotihuacan goods and style reach the Maya cities.",
         population="100,000–125,000 (the usual estimate)",
         feel="Copal smoke from patio altars, the red of painted walls in the sun, porters with loads of obsidian and Thin Orange bowls on the avenue.",
         style="mesoamerican",
         houses=dict(title="Apartment compounds", text="Large walled one-storey compounds of many rooms round patios, 50–60 m a side, with flat roofs, red-painted walls and a small temple on the main patio. Rich compounds such as Tetitla or Atetelco were painted inside with murals."),
         outskirts=dict(title="Edge of the city", text="Smaller compounds and adobe houses among fields of maize, beans and amaranth, and on the valley floor the canals and plots watered by the springs.")),
    dict(id=C, label="After the Fire", year=650, startYear=550, endYear=749,
         summary="Some time between about 550 and 650 the temples and palaces along the Avenue of the Dead were burned, their sculptures smashed and thrown down: a deliberate destruction, probably an uprising within the city. The centre was not rebuilt. People drifted away; newcomers with Coyotlatelco pottery settled in parts of the ruins.",
         population="perhaps 20,000–40,000 and falling (very uncertain)",
         feel="Blackened walls along the avenue, weeds in the plazas, the smell of old ash after rain.",
         style="mesoamerican",
         houses=dict(title="Compounds half abandoned", text="Some apartment compounds still lived in, rooms walled off and patios turned into yards; others empty, their roofs fallen. Newcomers built small houses inside the old walls."),
         outskirts=dict(title="Farms in the ruins", text="Maize plots planted over fallen compounds, and hamlets of the Coyotlatelco newcomers on the valley edges.")),
    dict(id=A, label="Where the Gods Were Born", year=1500, startYear=1350, endYear=1521,
         summary="Teotihuacan has been a ruin for eight centuries. The Aztecs believed the gods had gathered here to create the Fifth Sun and that the mounds were the tombs of ancient lords. A small Acolhua town lies to the south-west; pilgrims, priests and, later sources say, the emperor himself come to the pyramids.",
         population="a few thousand in the town and hamlets (archaeological guess)",
         feel="Wind over grassy mounds, maize stalks rattling between the old walls, a thread of copal smoke on the Sun pyramid's top.",
         style="mesoamerican",
         houses=dict(title="Village among the ruins", text="Small houses of adobe and reused stone round yards with a granary and a sweat bath, built on and between the overgrown compounds, many stones taken from the old walls."),
         outskirts=dict(title="Fields among the mounds", text="Maize, beans and maguey planted over the buried city; farmers turn up figurines and obsidian with every hoe stroke.")),
]

# ---------------------------------------------------------------- water and hills
SAN_JUAN = L((-1180, 2300), (-1350, 1700), (-1500, 1150), (-1650, 700), (-1650, 250), (-1650, -250), (-1650, -700), (-1720, -1150), (-1860, -1700), (-2000, -2300), (-2150, -3000))
SAN_JUAN_EARLY = L((-1180, 2300), (-1350, 1700), (-1500, 1150), (-1600, 800), (-1700, 420), (-1640, 120), (-1700, -200), (-1620, -600), (-1720, -1150), (-1860, -1700), (-2000, -2300), (-2150, -3000))
SAN_LORENZO = L((-2350, 2100), (-2500, 1400), (-2600, 800), (-2600, 200), (-2600, -500), (-2700, -1200), (-2850, -1900), (-3050, -2600))

WATER = [
    dict(id="san-juan-early", name="Río San Juan", path=SAN_JUAN_EARLY, width=14, periods=[T],
         blurb="A seasonal river running south-west through the valley to Lake Texcoco, dry for half the year and in spate in the summer rains. Here still in its natural bed."),
    dict(id="san-juan", name="Río San Juan", path=SAN_JUAN, width=16, periods=CLASSIC + [A],
         blurb="The builders of the grid diverted the river into straight channels that follow the city's orientation, so that it crosses the Avenue of the Dead at right angles between the Street of the Dead complex and the Ciudadela. Its canalised bed is still visible."),
    dict(id="san-lorenzo", name="Río San Lorenzo", path=SAN_LORENZO, width=10,
         blurb="A smaller stream crossing the southern part of the city, also bent to the grid in its central course (the usual reading of the survey)."),
]

HILLS = [
    dict(id="cerro-gordo", name="Cerro Gordo", center=(19.7062, -98.8395), radius=520,
         blurb="The extinct volcano north of the city, about 3,050 m high. Seen down the Avenue of the Dead it rises directly behind the Pyramid of the Moon, whose outline seems to echo it; springs and caves on its slopes were probably sacred."),
    dict(id="cerro-colorado", name="Cerro Colorado", center=(19.6745, -98.8305), radius=380, label=True,
         blurb="Low volcanic hills on the south-east edge of the valley, quarried for the red tezontle and stone of the city's rubble cores (the hill's identification here is approximate)."),
]

MARSH = [
    dict(name="Springs of the valley floor", polygon=R(-2350, -2900, -2550, -1750),
         blurb="Dozens of springs rose on the valley floor south-west of the city; their water was led along canals to irrigated fields, perhaps the basis of the city's food."),
]

# ---------------------------------------------------------------- roads
AV_N, AV_S = -255, -3250
ROADS = [
    dict(id="avenue-early", name="The ceremonial way", path=L((AV_N, 0), (-1600, 0)), width=18, style="major", labelled=True, periods=[T],
         blurb="A processional way probably already ran south from the Moon towards the new Sun pyramid; whether it was paved in this form is not known."),
    dict(id="avenue-of-the-dead", name="Avenue of the Dead", path=L((AV_N, 0), (-1100, 0), (-1960, 0), (AV_S, 0)), width=40, style="major", labelled=True, periods=CLASSIC,
         blurb="The city's spine, some 40 m wide and more than 4 km long, running from the Moon plaza past the Sun pyramid to the Ciudadela and beyond, 15.5° east of north. North of the river it climbs in a series of sunken plazas closed by cross-walls. Its Nahuatl name, Miccaotli, is Aztec."),
    dict(id="miccaotli", name="Miccaotli", path=L((AV_N, 0), (-1100, 0), (-1960, 0), (-2500, 0)), width=10, style="minor", labelled=True, periods=[A],
         blurb="'Road of the dead': the Aztecs took the mounds lining the old avenue for the tombs of ancient lords. A path runs along it between the fields."),
    dict(id="east-avenue", name="East Avenue", path=L((-1960, 440), (-1960, 1100), (-1960, 2150)), width=24, style="major", labelled=True, periods=CLASSIC,
         blurb="Millon's survey traced avenues running east and west from the Ciudadela and the Great Compound, dividing the city into quarters with the Avenue of the Dead. Their existence is debated: they may be lines of compounds rather than streets."),
    dict(id="west-avenue", name="West Avenue", path=L((-1960, -440), (-1960, -1300), (-1960, -3100)), width=24, style="major", labelled=True, periods=CLASSIC,
         blurb="The western arm of the cross: the line ran toward the Oaxaca barrio and the springs. Debated, like the East Avenue."),
    dict(id="street-w650", name="Street", path=L((150, -650), (-1640, -650), (-1660, -650), (-3000, -650)), width=8, style="minor", periods=CLASSIC),
    dict(id="street-e650", name="Street", path=L((150, 650), (-1640, 650), (-1660, 650), (-3000, 650)), width=8, style="minor", periods=CLASSIC),
    dict(id="street-w1300", name="Street", path=L((-200, -1300), (-1640, -1300), (-2650, -1300)), width=7, style="minor", periods=[X]),
    dict(id="street-e1300", name="Street", path=L((-300, 1300), (-1500, 1300), (-2650, 1300)), width=7, style="minor", periods=[X]),
    dict(id="cross-450", name="Street", path=L((-450, -2900), (-450, -20)), width=8, style="minor", periods=CLASSIC),
    dict(id="cross-450e", name="Street", path=L((-450, 20), (-450, 1900)), width=8, style="minor", periods=CLASSIC),
    dict(id="cross-1100", name="Street", path=L((-1100, -2900), (-1100, -70)), width=8, style="minor", periods=CLASSIC),
    dict(id="cross-1100e", name="Street", path=L((-1100, 70), (-1100, 2100)), width=8, style="minor", periods=CLASSIC),
    dict(id="road-otumba", name="Road to Otumba", path=L((-1100, 2100), (-900, 2600)), width=8, style="minor", labelled=True, periods=[X, C],
         blurb="Toward the grey obsidian of Otumba in the hills to the east; the prized green obsidian came from farther north, near Pachuca."),
    dict(id="path-oztoyahualco", name="Path to Oztoyahualco", path=L((AV_N - 40, -60), (-150, -600), (0, -1300), (100, -2000)), width=6, style="minor", periods=[T]),
    dict(id="path-springs", name="Path to the springs", path=L((-1600, -60), (-1900, -900), (-2300, -1700)), width=6, style="minor", periods=[T]),
    dict(id="road-acolman", name="Road to Acolman and Texcoco", path=L((-2500, -60), (-2620, -900), (-2700, -1700), (-2900, -2700)), width=8, style="minor", labelled=True, periods=[A],
         blurb="The road from the Aztec-period town south-west along the valley to Acolman and on to Texcoco, the capital of the Acolhua to whom Teotihuacan was subject."),
    dict(id="path-pyramids", name="Path to the pyramids", path=L((-2700, -1600), (-2200, -900), (-1600, -60)), width=6, style="minor", periods=[A]),
]

BRIDGES = [
    dict(id="san-juan-crossing", name="Crossing of the Río San Juan", path=L((-1620, 0), (-1680, 0)), build="stone", arches=1, landmarkId="san-juan-crossing", periods=CLASSIC,
         blurb="Where the canalised river passes under or through the avenue; how the crossing was built is not known."),
]

# ---------------------------------------------------------------- built-up blocks
# u bands (along the avenue) and v bands (across it), kept clear of the avenue, the streets and the rivers
U = [(250, -440), (-460, -1090), (-1110, -1630), (-1675, -1945), (-1975, -2585), (-2620, -3260)]
VW2, VW1, VE1, VE2 = (-3200, -662), (-638, -32), (32, 638), (662, 2300)


def B(name, ui, vb, density="dense", periods=None):
    u0, u1 = U[ui]
    return dict(name=name, density=density, periods=periods, polygon=R(u0, u1, vb[0], vb[1]))


BLOCKS = [
    # 100: a scattered early city
    dict(name="Oztoyahualco", density="dense", periods=[T], polygon=R(150, -420, -1500, -700)),
    dict(name="Oztoyahualco fields", density="loose", periods=[T], polygon=R(150, -700, -2600, -1520)),
    dict(name="Houses round the Moon", density="loose", periods=[T], polygon=R(-120, -440, -620, -40)),
    dict(name="Builders' camps", density="loose", periods=[T], polygon=R(-460, -1100, 340, 900)),
    dict(name="West of the way", density="loose", periods=[T], polygon=R(-500, -1300, -900, -40)),
    dict(name="By the river", density="loose", periods=[T], polygon=R(-1300, -1580, -700, 400)),
    dict(name="Hamlets by the springs", density="loose", periods=[T], polygon=R(-1950, -2300, -1700, -900)),
    # 250: the grid filling up
    B("Oztoyahualco", 0, VW2, "dense", [M]),
    B("Moon quarter, west", 0, VW1, "dense", [M]),
    B("Moon quarter, east", 0, VE1, "dense", [M]),
    B("North-east", 0, VE2, "loose", [M]),
    B("West of the Sun", 1, VW1, "dense", [M]),
    B("Sun quarter", 1, VE1, "dense", [M]),
    B("Western city", 1, VW2, "dense", [M]),
    B("Tepantitla quarter", 1, VE2, "loose", [M]),
    B("Street of the Dead, west", 2, VW1, "dense", [M]),
    B("Street of the Dead, east", 2, VE1, "dense", [M]),
    B("Tetitla quarter, far west", 2, VW2, "loose", [M]),
    B("Eastern city", 2, VE2, "loose", [M]),
    B("River quarter, west", 3, VW1, "dense", [M]),
    B("River quarter, east", 3, VE1, "dense", [M]),
    B("Tlailotlacan", 3, VW2, "loose", [M]),
    B("South-west", 4, VW1, "loose", [M]),
    B("South-east", 4, VE1, "loose", [M]),
    # 450: the city at its height
    B("Oztoyahualco", 0, VW2, "dense", [X]),
    B("Moon quarter, west", 0, VW1, "dense", [X]),
    B("Moon quarter, east", 0, VE1, "dense", [X]),
    B("North-east", 0, VE2, "dense", [X]),
    B("West of the Sun", 1, VW1, "dense", [X]),
    B("Sun quarter", 1, VE1, "dense", [X]),
    B("Tetitla and Atetelco", 1, VW2, "dense", [X]),
    B("Tepantitla quarter", 1, VE2, "dense", [X]),
    B("Street of the Dead, west", 2, VW1, "dense", [X]),
    B("Street of the Dead, east", 2, VE1, "dense", [X]),
    B("Western city", 2, VW2, "dense", [X]),
    B("Merchants' barrio", 2, VE2, "dense", [X]),
    B("River quarter, west", 3, VW1, "dense", [X]),
    B("River quarter, east", 3, VE1, "dense", [X]),
    B("Tlailotlacan", 3, VW2, "dense", [X]),
    B("East of the river", 3, VE2, "loose", [X]),
    B("La Ventilla", 4, VW1, "dense", [X]),
    B("Behind the Ciudadela", 4, VE1, "dense", [X]),
    B("South-western city", 4, VW2, "loose", [X]),
    B("South-eastern city", 4, VE2, "loose", [X]),
    B("Tlajinga, west", 5, VW1, "dense", [X]),
    B("Tlajinga, east", 5, VE1, "loose", [X]),
    # 650: the dwindling city
    B("Oztoyahualco", 0, VW2, "loose", [C]),
    B("Moon quarter", 0, VW1, "loose", [C]),
    B("West of the Sun", 1, VW1, "loose", [C]),
    B("Tetitla and Atetelco", 1, VW2, "dense", [C]),
    B("Tepantitla quarter", 1, VE2, "loose", [C]),
    B("Western city", 2, VW2, "dense", [C]),
    B("Merchants' barrio", 2, VE2, "loose", [C]),
    B("River quarter, west", 3, VW1, "loose", [C]),
    B("Tlailotlacan", 3, VW2, "loose", [C]),
    B("La Ventilla", 4, VW1, "loose", [C]),
    B("Behind the Ciudadela", 4, VE1, "loose", [C]),
    B("Tlajinga", 5, VW1, "loose", [C]),
    # 1500: a town and hamlets among the mounds
    dict(name="Teotihuacan, the Aztec-period town", density="dense", periods=[A], polygon=R(-2650, -3000, -1900, -1150)),
    dict(name="Edge of the town", density="loose", periods=[A], polygon=R(-2300, -2620, -1600, -700)),
    dict(name="Hamlet by the Sun pyramid", density="loose", periods=[A], polygon=R(-480, -900, 420, 900)),
    dict(name="Hamlet west of the avenue", density="loose", periods=[A], polygon=R(-1150, -1600, -900, -300)),
    dict(name="Hamlet behind the Ciudadela", density="loose", periods=[A], polygon=R(-2000, -2350, 480, 1000)),
]

DISTRICTS = [
    dict(id="ceremonial-centre", name="Avenue of the Dead", periods=CLASSIC, polygon=R(-120, -2200, -480, 480),
         description="The ceremonial and political heart: the two great pyramids, some 75 temples on platforms lining the avenue, palaces and the Ciudadela. Few ordinary people lived here."),
    dict(id="oztoyahualco", name="Oztoyahualco", periods=[T, M, X], polygon=R(250, -460, -2600, -680),
         description="The north-western quarter, among the oldest parts of the city; excavated compounds here (15B:N6W3) show family shrines, kitchens and burials under the floors."),
    dict(id="tlailotlacan", name="Tlailotlacan (Oaxaca barrio)", periods=[M, X], polygon=R(-1300, -1700, -2700, -2100),
         description="A barrio of Zapotec families from the Valley of Oaxaca who kept their own pottery, funerary urns and tombs for some four centuries while living in Teotihuacan-style compounds."),
    dict(id="merchants-barrio", name="Merchants' barrio", periods=[M, X], polygon=R(-700, -1100, 1450, 1950),
         description="A barrio on the eastern edge with Gulf-coast and Maya pottery and round adobe buildings unlike the rest of the city, probably the home of traders from the lowlands."),
    dict(id="tlajinga", name="Tlajinga", periods=[X, C], polygon=R(-2620, -3260, -640, 640),
         description="The southern end of the city along the avenue, a district of potters and lapidaries in modest compounds."),
    dict(id="ruins", name="The ruins of the old city", periods=[A], polygon=R(-120, -2200, -480, 480),
         description="Overgrown mounds along the old avenue, mined for stone and planted with maize; the Aztecs gave the pyramids the names of the Sun and Moon that they still bear."),
]

LABELS = [
    dict(text="TEOTIHUACAN", position=G(-1350, -1150), size="lg", rotation=-74.5, periods=[M, X, C]),
    dict(text="Teotihuacan", position=G(-900, -1000), size="md", rotation=-74.5, periods=[T]),
    dict(text="Teotihuacan (ruins)", position=G(-1350, -1150), size="md", rotation=-74.5, periods=[A]),
    dict(text="Teotihuacan (town)", position=G(-3100, -1500), size="sm", periods=[A]),
    dict(text="Miccaotli", position=G(-2250, -60), size="sm", rotation=-74.5, periods=[A]),
    dict(text="Río San Juan", position=G(-1610, -1600), size="sm", rotation=-14, periods=ALL),
    dict(text="Río San Lorenzo", position=G(-2560, 1300), size="sm", rotation=-14, periods=ALL),
    dict(text="Tlailotlacan", position=G(-1250, -2400), size="sm", periods=[M, X]),
    dict(text="Merchants' barrio", position=G(-650, 1700), size="sm", periods=[M, X]),
    dict(text="Oztoyahualco", position=G(220, -1600), size="sm", periods=[T, M, X]),
    dict(text="Tlajinga", position=G(-3000, 330), size="sm", periods=[X, C]),
    dict(text="to Otumba", position=G(-880, 2450), size="sm", rotation=-60, periods=[X, C]),
    dict(text="to Acolman", position=G(-3050, -2500), size="sm", rotation=-60, periods=[A]),
    dict(text="springs", position=G(-2750, -2300), size="sm", periods=ALL),
]
