# Fatehpur Sikri: the sandstone ridge 37 km west of Agra, from Babur's garden at Sikri (1527)
# through Akbar's capital (1571-85) to the half-empty city of Jahangir's day.
# Positions are written in metres east (x) and north (y) of the Anup Talao in the palace, and
# converted to latitude/longitude by L(); the usual site plans are the basis, to roughly 20-50 m.
import math

O_LAT, O_LON = 27.09681, 77.66617   # the Anup Talao (re-anchored on OSM/Wikipedia; was 27.0955, 77.6640, ~260 m off)
KY, KX = 110950.0, 111320.0 * math.cos(math.radians(27.0955))


def L(x, y):
    return (round(O_LAT + y / KY, 6), round(O_LON + x / KX, 6))


def LL(pts):
    return [L(x, y) for x, y in pts]


ALL = ["sikri-1560", "akbar-1585", "abandoned-1610"]
SIKRI = ["sikri-1560"]
AKBAR = ["akbar-1585"]
LATE = ["abandoned-1610"]
CITY_ERAS = ["akbar-1585", "abandoned-1610"]
NOT_AKBAR = ["sikri-1560", "abandoned-1610"]

CITY = dict(
    name="Fatehpur Sikri", subtitle="Akbar's City of Victory",
    description="Three moments on the red sandstone ridge of Sikri, 37 km west of Agra: the Sufi saint's village beside Babur's garden (1560), Akbar's walled capital with its palaces, great mosque and lake (1585), and the emptied city of Jahangir's day (1610). Positions are projected from real coordinates and the usual site plans; the drawing is an illustration, not a survey.",
    defaultPeriodId="akbar-1585",
    world=dict(heightScale=1.0, walls=["#C9946E", "#D8B48E", "#BF7F5E", "#DCC3A0", "#CFA27C"], roofs=["#C49A74", "#B98A66"]),
    camera=dict(target=L(-120, -60), distance=30, maxDistance=120),
)
FRAME = ((27.1160, 77.6320), (27.0740, 77.6880))
RESOLUTION = 4096
PALETTE = dict(parchment="#E9D5AE", ink="#6E4532", water="#6A8C8A", hill="#8C6E52", road="#8C6A48")
COMPASS = L(1980, 1830)
CARTOUCHE = L(-2980, -2170)

PERIODS = [
    dict(id="sikri-1560", label="The village of Sikri", year=1560, startYear=1527, endYear=1570,
         summary="A village of stonecutters under a ridge of red sandstone by a seasonal lake. Babur beat Rana Sanga at nearby Khanwa in 1527, called the place Shukri, 'thanks', and laid out a garden with a step-well. The Chishti Sufi Shaikh Salim lives on the ridge in a hospice among the quarrymen; in 1568 Akbar, still without a son, comes to ask his prayers.",
         population="a few hundred to a few thousand",
         feel="Chisels ringing on the ridge, buffalo wading in the shallows, the drone of zikr from the saint's hospice at dusk.",
         style="courtyard",
         houses=dict(title="Stonecutters' houses of Sikri", text="One-room houses of rubble sandstone and mud round a yard, roofed with flat stone slabs laid on stone beams, a platform by the door for working. Waste chips and half-finished brackets and lintels lie in every lane."),
         outskirts=dict(title="Quarries and fields", text="Quarry cuts in the ridge, millet and wheat fields on the plain, herders' huts and the lake's grassy margin where Babur's garden stands walled.")),
    dict(id="akbar-1585", label="Akbar's city", year=1585, startYear=1571, endYear=1585,
         summary="Akbar's capital from 1571 to 1585, built at speed of the ridge's own red sandstone: a palace of courts and pavilions on the crest, the Jama Masjid round the saint's tomb, the Buland Darwaza, a lake dammed to the north-west and a town of bazaars and nobles' mansions inside walls on three sides. Here Akbar held the Ibadat Khana debates and received the Jesuits.",
         population="perhaps 100,000–200,000 (Ralph Fitch thought it larger than London; estimates vary widely)",
         feel="Kettledrums from the Naubat Khana at the watches of the day, elephants at the Hathi Pol, Persian, Hindi and Portuguese in the same bazaar.",
         style="courtyard",
         houses=dict(title="Mansions and bazaar houses of Fatehpur", text="Nobles' havelis of dressed red sandstone round one or two courts, with pillared verandahs, stone screens and flat terraces; in the bazaar, rows of shops with rooms above, and behind them rubble-and-mud courtyard houses of soldiers, clerks and craftsmen."),
         outskirts=dict(title="Gardens and lakeside", text="Walled gardens and orchards along the lake shore, the karkhanas and stables below the palace, herders' villages and fields beyond the walls.")),
    dict(id="abandoned-1610", label="The emptied city", year=1610, startYear=1586, endYear=1640,
         summary="The court left in 1585 for the north-west and never truly came back. The palaces stand, locked and kept by a few servants; the bazaars thin out and the town shrinks back to a village round the mosque and the saint's tomb, where his descendants still live. Jahangir camps here in 1619 to escape plague in Agra.",
         population="a few thousand",
         feel="Pigeons in the empty halls, pilgrims tying threads at the saint's marble screen, goats grazing in the Diwan-i-Am.",
         style="courtyard",
         houses=dict(title="The village in the city", text="The saint's descendants and the mosque's servants keep the stone houses round the Jama Masjid; elsewhere mansions stand roofless or are lived in by a family in a few rooms, and new mud houses are built of salvaged stone."),
         outskirts=dict(title="Ruins and fields", text="Empty bazaar streets and garden walls going back to fields; the lake shrinking behind its neglected dam.")),
]

# ---------------------------------------------------------------- the lake
# Akbar's south-east shore, along the foot of the ridge, south-west to north-east
SHORE = [(-2528, -444), (-1685, -78), (-892, 189), (-198, 422), (248, 588), (644, 943)]


def off(pts, d):
    """Offset a shore line by d metres to the north-west (into the lake)."""
    return [(x - 0.45 * d, y + 0.89 * d) for x, y in pts]


WATER = [
    dict(id="lake-1560", name="Lake of Sikri", path=LL([(-3300, 50)] + off(SHORE, 760)[:5]), width=900, periods=SIKRI,
         blurb="A natural lake, shallow and seasonal, filled by the monsoon streams off the hills to the west. Babur admired it in 1527 and had a pavilion built by its edge."),
    dict(id="lake", name="The great lake", path=LL([(-3300, 50)] + off(SHORE, 700)), width=1400, periods=AKBAR,
         blurb="Akbar dammed the lake to supply the new city, making a sheet of water perhaps 10 km long and 3 km wide on the city's open side. It watered gardens and, by wheels and channels up the ridge, the palace, and served as a pleasure lake. Now dry."),
    dict(id="lake-arm", name="The great lake", path=LL([(-560, 1000), (-760, 1700), (-900, 2400)]), width=1000, periods=AKBAR),
    dict(id="lake-1610", name="The lake", path=LL([(-3300, 50)] + off(SHORE, 800)[:5] + [(140, 1400)]), width=1100, periods=LATE,
         blurb="With no one to keep the dam and the channels, the lake shrank back towards its old shallows; how much water stood here in Jahangir's day is not clearly recorded."),
]

ISLANDS = []

HILLS = [
    dict(id="sikri-ridge", name="Sikri ridge", center=L(-350, -220), radius=340,
         blurb="A long ridge of red sandstone, some 3 km long and rising perhaps 30–40 m above the plain, the last outlier of the Vindhyan hills. The city's palaces, mosque and houses were all cut from it."),
    dict(id="ridge-2", name="Sikri ridge", center=L(-650, -330), radius=320, label=False),
    dict(id="ridge-3", name="Sikri ridge", center=L(-1000, -440), radius=290, label=False),
    dict(id="ridge-4", name="Sikri ridge", center=L(-60, -80), radius=330, label=False),
    dict(id="ridge-5", name="Sikri ridge", center=L(300, 60), radius=300, label=False),
    dict(id="ridge-6", name="Sikri ridge", center=L(650, 220), radius=260, label=False),
]

# ---------------------------------------------------------------- roads
AGRA_GATE, AJMERI_GATE = (1090, 388), (-2181, -832)
DELHI_GATE, LAL_GATE, BIR_GATE, CHANDAR_GATE = (734, 832), (892, 632), (991, -333), (595, -721)
GWALIOR_GATE, TEHRA_GATE, CHOR_GATE = (-198, -1110), (-793, -1254), (-1685, -1076)

ROADS = [
    # Akbar's city (and its emptied streets after him)
    dict(id="bazaar", name="Bazaar of the Agra Gate", path=LL([AGRA_GATE, (700, 230), (330, 60), (250, 40), (170, 25)]), width=24, style="major", labelled=True, periods=CITY_ERAS,
         blurb="The main street of the city, from the Agra Gate up the ridge to the Naubat Khana and the Diwan-i-Am, lined with shops; Monserrate and Fitch both describe a long, busy bazaar."),
    dict(id="ridge-road", name="Road along the ridge", path=LL([(250, 40), (160, -60), (0, -85), (-110, -95), (-220, -110), (-292, -200), (-300, -232)]), width=12, periods=CITY_ERAS,
         blurb="From the palace gate along the crest past the harem palaces to the Badshahi Darwaza, the emperor's own gate into the Jama Masjid."),
    dict(id="lower-road", name="Lower town road", path=LL([BIR_GATE, (600, -450), (200, -560), (-200, -640), (-600, -760), (-1100, -900), CHOR_GATE]), width=12, style="major", periods=CITY_ERAS,
         blurb="Along the foot of the ridge on its south-eastern side, through the lower town of shops and houses below the Buland Darwaza."),
    dict(id="darwaza-road", name="Road from the Buland Darwaza", path=LL([(-368, -350), (-360, -450), (-330, -640), (-260, -900), GWALIOR_GATE]), width=10, periods=CITY_ERAS),
    dict(id="ajmer-street", name="Ajmeri Gate road", path=LL([AJMERI_GATE, (-1700, -640), (-1200, -500), (-800, -380), (-480, -322)]), width=12, periods=CITY_ERAS),
    dict(id="lake-road", name="Lakeside road", path=LL([(-200, 128), (-195, 200), (-175, 240), (20, 240), (200, 230), (450, 330), DELHI_GATE]), width=10, periods=CITY_ERAS,
         blurb="Down from the Hathi Pol past the Hiran Minar and the caravanserai, along the lake shore to the Delhi Gate."),
    dict(id="agra-road", name="Road to Agra", path=LL([AGRA_GATE, (1500, 520), (2500, 820)]), width=16, style="major", labelled=True, periods=CITY_ERAS,
         blurb="The imperial road to Agra, 37 km east, along which Akbar moved his court and treasury; under him it was marked by kos minars, the Mughal milestones."),
    dict(id="mathura-road", name="Road to Mathura and Delhi", path=LL([DELHI_GATE, (950, 1050), (1350, 1500), (1700, 2400)]), width=12, style="major", labelled=True, periods=CITY_ERAS),
    dict(id="ajmer-road", name="Road to Ajmer", path=LL([AJMERI_GATE, (-2600, -1000), (-3300, -1250)]), width=12, style="major", labelled=True, periods=CITY_ERAS,
         blurb="West towards Ajmer and the shrine of Muinuddin Chishti, to which Akbar went on foot in 1570 to give thanks for his son."),
    dict(id="gwalior-road", name="Road to Gwalior", path=LL([GWALIOR_GATE, (-180, -1400), (-150, -2450)]), width=10, style="major", periods=CITY_ERAS),
    dict(id="bayana-road", name="Road to Bayana", path=LL([TEHRA_GATE, (-900, -1600), (-1150, -2450)]), width=8, periods=CITY_ERAS),
    dict(id="bir-road", name="Road from the Bir Gate", path=LL([BIR_GATE, (1500, -450), (2450, -650)]), width=8, periods=CITY_ERAS),
    dict(id="chandar-road", name="Road from the Chandar Gate", path=LL([CHANDAR_GATE, (800, -1100), (1100, -1700)]), width=6, periods=CITY_ERAS),
    dict(id="lal-road", name="Lal Gate lane", path=LL([LAL_GATE, (800, 560), (650, 420)]), width=6, periods=AKBAR),
    # the village of Sikri
    dict(id="sikri-agra-road", name="Road to Agra", path=LL([(2500, 820), (1500, 500), (900, 220), (400, -120), (0, -200), (-280, -300)]), width=10, style="major", labelled=True, periods=SIKRI,
         blurb="The old road from Agra to Bayana and Rajputana ran past the ridge; Babur's army came this way to Khanwa in 1527."),
    dict(id="sikri-west-road", name="Road to Khanwa and Bayana", path=LL([(-480, -330), (-1200, -560), (-2200, -880), (-3300, -1250)]), width=8, periods=SIKRI),
    dict(id="sikri-garden-lane", name="Lane to Babur's garden", path=LL([(-500, -310), (-800, -250), (-1150, -110)]), width=5, periods=SIKRI),
    dict(id="sikri-south-lane", name="Track to Gwalior", path=LL([(-300, -420), (-250, -900), (-180, -1400), (-150, -2450)]), width=6, periods=SIKRI),
]

# ---------------------------------------------------------------- walls and gates
WALL = [(-2528, -444), AJMERI_GATE, CHOR_GATE, (-1190, -1220), TEHRA_GATE, GWALIOR_GATE, (198, -943), CHANDAR_GATE, BIR_GATE, (1309, 111), AGRA_GATE, LAL_GATE, DELHI_GATE, (644, 943)]

WALLS = [
    dict(id="city-wall", name="City wall", path=LL(WALL), closed=False, periods=AKBAR,
         blurb="A rubble wall faced with sandstone, with round bastions and battlements, enclosing the city on three sides; the lake closed the fourth. Its length is given variously, from about 6 km to six or seven miles (some 11 km); this trace follows the usual site plan and is simplified."),
    dict(id="city-wall-1610", name="City wall", path=LL(WALL), closed=False, periods=LATE,
         blurb="Still standing, but with the court gone its gates were no longer manned as before."),
]

GATES = [
    dict(id="chor-gate", name="Chor Gate", position=L(*CHOR_GATE), periods=CITY_ERAS),
    dict(id="tehra-gate", name="Tehra Gate", position=L(*TEHRA_GATE), periods=CITY_ERAS),
    dict(id="gwalior-gate", name="Gwalior Gate", position=L(*GWALIOR_GATE), periods=CITY_ERAS),
    dict(id="chandar-gate", name="Chandar Gate", position=L(*CHANDAR_GATE), periods=CITY_ERAS),
    dict(id="bir-gate", name="Bir (Suraj) Gate", position=L(*BIR_GATE), periods=CITY_ERAS),
    dict(id="lal-gate", name="Lal Gate", position=L(*LAL_GATE), periods=CITY_ERAS),
    dict(id="delhi-gate", name="Delhi Gate", position=L(*DELHI_GATE), periods=CITY_ERAS),
]

BRIDGES = []
AQUEDUCTS = [
    dict(name="Water-lift from the lake to the palace", path=LL([(-310, 330), (-295, 165), (-270, 110), (-240, 80), (-200, 72), (-150, 45), (-90, 5)]), periods=AKBAR),
]

# ---------------------------------------------------------------- built-up areas
BAZAAR_N = [(1000, 430), (700, 282), (400, 125), (380, 230), (650, 420), (880, 600)]
BAZAAR_S = [(1060, 330), (720, 190), (390, 20), (430, -110), (780, 30), (1010, 150)]
TOWN_E = [(450, -160), (820, -20), (1100, 40), (1150, -80), (930, -300), (600, -420), (300, -330)]
TOWN_S = [(930, -390), (600, -495), (200, -605), (-200, -685), (-280, -700), (-190, -960), (-100, -1015), (200, -890), (540, -690), (900, -420)]
STONECUTTERS = [(-400, -370), (-390, -640), (-600, -720), (-1000, -830), (-1100, -560), (-800, -420), (-500, -350)]
SHAIKHS = [(-470, -140), (-310, -135), (-320, -20), (-420, 40), (-560, -40)]

BLOCKS = [
    # Akbar's city
    dict(name="Bazaar, north side", polygon=LL(BAZAAR_N), density="dense", periods=AKBAR),
    dict(name="Bazaar, south side", polygon=LL(BAZAAR_S), density="dense", periods=AKBAR),
    dict(name="Nobles' mansions on the ridge", polygon=LL(TOWN_E), density="loose", periods=AKBAR),
    dict(name="Lower town", polygon=LL(TOWN_S), density="dense", periods=AKBAR),
    dict(name="Sikri: the stonecutters' quarter", polygon=LL(STONECUTTERS), density="dense", periods=AKBAR),
    dict(name="Shaikhs' quarter north of the mosque", polygon=LL(SHAIKHS), density="dense", periods=AKBAR),
    dict(name="Tehra Gate quarter", polygon=LL([(-650, -820), (-1100, -950), (-1500, -1070), (-1180, -1190), (-800, -1215)]), density="loose", periods=AKBAR),
    dict(name="Ajmeri Gate quarter", polygon=LL([(-1250, -560), (-1700, -700), (-2050, -850), (-1750, -1000), (-1200, -880)]), density="loose", periods=AKBAR),
    dict(name="Nobles' gardens by the lake", polygon=LL([(-1350, -380), (-900, -270), (-560, -270), (-600, -130), (-1000, -130), (-1300, -210)]), density="loose", periods=AKBAR),
    dict(name="Palace servants' quarter", polygon=LL([(-300, -60), (-238, -60), (-236, 20), (-280, 95), (-330, 80), (-305, 0)]), density="dense", periods=AKBAR),
    dict(name="Karkhanas and stables", polygon=LL([(150, 105), (330, 140), (420, 250), (230, 210)]), density="loose", periods=AKBAR),
    # the emptied city
    dict(name="Sikri: the stonecutters' quarter", polygon=LL(STONECUTTERS), density="loose", periods=LATE),
    dict(name="Shaikhs' quarter north of the mosque", polygon=LL(SHAIKHS), density="dense", periods=LATE),
    dict(name="What is left of the bazaar", polygon=LL(BAZAAR_S), density="loose", periods=LATE),
    dict(name="Lower town below the Buland Darwaza", polygon=LL([(-200, -685), (-280, -700), (-190, -960), (-100, -1015), (100, -900), (100, -650)]), density="loose", periods=LATE),
    # the village of Sikri
    dict(name="Sikri", polygon=LL([(-500, -340), (-280, -320), (-260, -150), (-450, -120), (-560, -220)]), density="loose", periods=SIKRI),
    dict(name="Stonecutters' hamlet", polygon=LL([(-560, -390), (-380, -390), (-370, -560), (-600, -560)]), density="dense", periods=SIKRI),
    dict(name="Hamlet below the ridge", polygon=LL([(150, -480), (380, -440), (400, -600), (170, -640)]), density="loose", periods=SIKRI),
    dict(name="Herders by the lake", polygon=LL([(-1700, -260), (-1450, -200), (-1450, -330), (-1700, -380)]), density="loose", periods=SIKRI),
]

GARDENS = [
    dict(name="Orchards by the lake", polygon=LL([(-1080, -20), (-1080, 60), (-700, 190), (-450, 250), (-450, 130), (-800, 30)]), kind="orchard", periods=AKBAR),
    dict(name="Garden of the harem", polygon=LL([(-185, 0), (-120, 0), (-120, 28), (-185, 28)]), kind="park", periods=CITY_ERAS),
    dict(name="Gardens below the Hiran Minar", polygon=LL([(-470, 210), (-330, 260), (-330, 360), (-480, 330)]), kind="park", periods=AKBAR),
    dict(name="Orchard inside the Bir Gate", polygon=LL([(1150, -160), (1220, -40), (1180, 60), (1120, -60)]), kind="orchard", periods=AKBAR),
    dict(name="Fields by the Agra road", polygon=LL([(1500, 600), (2300, 860), (2300, 1200), (1600, 1000)]), kind="vineyard", periods=ALL),
    dict(name="Fields south of the walls", polygon=LL([(-700, -1500), (-260, -1440), (-240, -2000), (-600, -2000)]), kind="vineyard", periods=ALL),
    dict(name="Fields by the Gwalior road", polygon=LL([(-90, -1420), (300, -1350), (400, -1900), (-70, -1980)]), kind="vineyard", periods=ALL),
    dict(name="Fields of Sikri", polygon=LL([(-200, -800), (300, -700), (500, -1100), (-150, -1200)]), kind="vineyard", periods=SIKRI),
]

MARSH = [
    dict(name="Lake margin", polygon=LL(SHORE + list(reversed(off(SHORE, 330)))), periods=SIKRI),
    dict(name="Drying lake margin", polygon=LL(SHORE + list(reversed(off(SHORE, 230)))), periods=LATE),
]

DISTRICTS = [
    dict(id="daulat-khana", name="Daulat Khana (the palace)", polygon=LL([(-250, -95), (170, -95), (170, 180), (-250, 180)]), periods=CITY_ERAS,
         description="The imperial palace on the crest of the ridge: courts of audience, the emperor's own quarters round the Anup Talao, the harem palaces, offices, treasury and workshops, all of red sandstone and laid out on a strict grid."),
    dict(id="sikri", name="Sikri", polygon=LL([(-620, -420), (-250, -420), (-250, -100), (-620, -100)]), periods=ALL,
         description="The old village on the ridge where Shaikh Salim Chishti lived; under Akbar the quarter of the great mosque, the saint's family and the stonecutters, and afterwards the village again."),
    dict(id="bazaar", name="The bazaar", polygon=LL([(1080, 460), (330, 150), (330, -30), (1080, 280)]), periods=AKBAR,
         description="The commercial street from the Agra Gate to the palace: cloth, grain and jewel merchants, cookshops, money-changers and the imperial mint nearby."),
    dict(id="lower-town", name="Lower town", polygon=LL([(950, -380), (-300, -690), (-200, -1050), (540, -700)]), periods=AKBAR,
         description="Houses of soldiers, clerks and craftsmen on the plain between the ridge and the south wall."),
]

LABELS = [
    dict(text="Fatehpur", position=L(450, -760), size="lg", periods=CITY_ERAS),
    dict(text="Sikri", position=L(-470, -470), size="lg", periods=SIKRI),
    dict(text="Sikri", position=L(-700, -560), size="md", periods=CITY_ERAS),
    dict(text="The Lake", position=L(-1500, 900), size="lg", rotation=-24, periods=AKBAR),
    dict(text="The Lake", position=L(-1700, 800), size="md", rotation=-24, periods=NOT_AKBAR),
    dict(text="Sikri ridge", position=L(-850, -250), size="md", rotation=-22, periods=ALL),
    dict(text="to Agra", position=L(2100, 620), size="sm", periods=ALL),
]

SOURCES = [
    dict(id="rizvi-flynn", title="Fathpur-Sikri", author="S. A. A. Rizvi & V. J. A. Flynn", year=1975),
    dict(id="brand-lowry", title="Fatehpur-Sikri: A Sourcebook", author="Michael Brand & Glenn D. Lowry (eds.)", year=1985),
    dict(id="petruccioli", title="Fathpur Sikri: la città del sole e delle acque", author="Attilio Petruccioli", year=1988),
    dict(id="smith-fs", title="The Moghul Architecture of Fathpur-Sikri", author="Edmund W. Smith (Archaeological Survey of India)", year="1894–98", url="https://archive.org/details/moghularchitect01smit"),
    dict(id="koch", title="Mughal Architecture: An Outline of its History and Development, 1526–1858", author="Ebba Koch", year=1991),
    dict(id="wiki-fatehpur-sikri", title="Fatehpur Sikri", author="Wikipedia", url="https://en.wikipedia.org/wiki/Fatehpur_Sikri"),
]
