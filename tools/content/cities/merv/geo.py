# Merv: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
import math

ALL = ["achaemenid-500", "sasanian-500", "seljuk-1100", "ruins-1250", "timurid-1450"]
ANCIENT = ["achaemenid-500", "sasanian-500"]
GK_ON = ["sasanian-500", "seljuk-1100", "ruins-1250", "timurid-1450"]
SELJUK = ["seljuk-1100"]
AFTER = ["ruins-1250", "timurid-1450"]
SK_ON = ["seljuk-1100", "ruins-1250", "timurid-1450"]
TIMURID = ["timurid-1450"]

SOURCES = [
    dict(id="herrmann-merv", title="Monuments of Merv: Traditional Buildings of the Karakum", author="Georgina Herrmann", year=1999),
    dict(id="williams-merv", title="Ancient Merv: Queen of Cities (and the reports of the Ancient Merv Project)", author="Tim Williams et al., UCL Institute of Archaeology", year="1992–2016"),
    dict(id="le-strange", title="The Lands of the Eastern Caliphate", author="Guy Le Strange", year=1905, note="chapter on Marv al-Shahijan and its canals"),
    dict(id="barthold-turkestan", title="Turkestan Down to the Mongol Invasion", author="V. V. Barthold", year=1928),
    dict(id="istakhri", title="Kitab al-Masalik wa'l-Mamalik", author="al-Istakhri", year="c. 950", url="https://en.wikipedia.org/wiki/Istakhri"),
    dict(id="yaqut", title="Mu'jam al-Buldan", author="Yaqut al-Hamawi", year="c. 1224", url="https://en.wikipedia.org/wiki/Yaqut_al-Hamawi"),
    dict(id="wiki-merv", title="Merv", author="Wikipedia", url="https://en.wikipedia.org/wiki/Merv"),
    dict(id="wiki-margiana", title="Margiana", author="Wikipedia", url="https://en.wikipedia.org/wiki/Margiana"),
    dict(id="wiki-murghab", title="Marghab River", author="Wikipedia", url="https://en.wikipedia.org/wiki/Marghab_River"),
    dict(id="wiki-siege-1221", title="Siege of Merv (1221)", author="Wikipedia", url="https://en.wikipedia.org/wiki/Siege_of_Merv_(1221)"),
    dict(id="wiki-seljuk", title="Seljuk Empire", author="Wikipedia", url="https://en.wikipedia.org/wiki/Seljuk_Empire"),
    dict(id="wiki-shah-rukh", title="Shah Rukh", author="Wikipedia", url="https://en.wikipedia.org/wiki/Shah_Rukh"),
]

CITY = dict(
    name="Merv", subtitle="Marw al-Shahijan, Queen of the World",
    description="Two thousand years of Merv in the Murghab oasis, where each age built a new walled city beside the last: the round Achaemenid citadel of Erk Kala, the square Hellenistic and Sasanian city of Gyaur Kala, the vast Seljuk city of Sultan Kala round Sanjar's mausoleum, its emptying after the Mongols, and the small Timurid town to the south. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="seljuk-1100",
    world=dict(heightScale=1.1, walls=["#D8BF96", "#CDB088", "#E0CBA6", "#C6A57C", "#D2B890"], roofs=["#C2A47A", "#B5966C"]),
    camera=dict(target=(37.6640, 62.1700), distance=44),
)

# north-west corner, south-east corner: the Hurmuzfarra fields to the Asadi canal, Muhammad ibn Zayd to Abdullah Khan Kala
FRAME = ((37.6860, 62.1400), (37.6340, 62.2130))

PALETTE = dict(parchment="#E9D7AE", ink="#6A4A30", water="#5E8A8C", hill="#A88E62", road="#8C6A48")
COMPASS = (37.6825, 62.2095)
CARTOUCHE = (37.6356, 62.1418)

PERIODS = [
    dict(id="achaemenid-500", label="Margu, satrapy of Margiana", year=-500, startYear=-550, endYear=-330,
         summary="Margu, the Margiana of the Greeks, is a province of the Persian Empire, named in Darius' inscription at Behistun. Its stronghold is Erk Kala, a round citadel of mud brick on a high rampart above the irrigated delta of the Murghab, where the oasis river fans out into canals before dying in the Karakum sands. Around it lie farmsteads, fields and vineyards.",
         population="unknown; a few thousand in and around the citadel",
         feel="Donkeys on the rampart ramp, the creak of water-lifts on the canals, Persian officials counting barley tax in the citadel yard, desert wind carrying sand over the fields.",
         style="courtyard",
         houses=dict(title="Houses inside Erk Kala", text="Small mud-brick houses round yards, packed inside the citadel rampart and roofed with poplar beams, reed mats and clay; storerooms for grain and a hearth in every house."),
         outskirts=dict(title="Farmsteads of the delta", text="Scattered farmsteads with thick mud walls, each by its own canal: wheat, barley, millet and vines, flocks driven to the desert edge in spring.")),
    dict(id="sasanian-500", label="Marw of the Sasanians", year=500, startYear=-329, endYear=1036,
         summary="Refounded about 280 BCE by Antiochus I as Antiochia Margiana, the city is now Gyaur Kala, a walled square nearly two kilometres a side with Erk Kala as its citadel. Under the Sasanians it is a frontier capital and mint. Fire temples, a Buddhist stupa and monastery and the churches of a Christian metropolitan stand inside one wall: a city of many faiths. Mud brick and pakhsa.",
         population="unknown; perhaps a few tens of thousands",
         feel="Hymns in Syriac from the church, chanting at the Buddhist monastery, the smoke of the sacred fire, Sogdian, Persian and Bactrian spoken at the caravan gates.",
         style="courtyard",
         houses=dict(title="Houses of Gyaur Kala", text="Mud-brick and pakhsa courtyard houses along a grid of lanes between the two main streets, flat roofs of beams and clay, workshops of potters, glass- and metalworkers in their own quarters."),
         outskirts=dict(title="Koshks and villages", text="Outside the walls the estates of the landed gentry (dihqans), each a fortified koshk with corrugated walls, among canals, orchards and the villages of the oasis.")),
    dict(id="seljuk-1100", label="Seljuk metropolis", year=1100, startYear=1037, endYear=1220,
         summary="Taken by the Seljuk Turks in 1037, Merv (Marw al-Shahijan) is the capital of Khurasan and from 1118 of Sultan Sanjar's empire. The city has moved west of the old walls to Sultan Kala, walled by the Seljuks, with the Shahriyar Ark, the Friday mosque, libraries Yaqut would praise and markets of silk and cotton. Perhaps the largest city in the world about 1150, though estimates differ.",
         population="perhaps 150,000–200,000 (estimates vary widely)",
         feel="The call to prayer from a dozen minarets, bales of cotton cloth under the bazaar domes, Turkic horsemen at the Ark gate, scholars arguing in the library reading rooms.",
         style="courtyard",
         houses=dict(title="Courtyard houses of Sultan Kala", text="Mud-brick courtyard houses with flat earth roofs and a domed room or two of fired brick for the well-off; a pool or a channel from the canal in the yard; lanes of workshops grouped by trade near the markets."),
         outskirts=dict(title="Koshks, ice houses and melon fields", text="The oasis round the walls: walled gardens and the corrugated koshks of the gentry, conical ice houses (yakhdan) by the canals, orchards and the famous melon fields.")),
    dict(id="ruins-1250", label="After the Mongols", year=1250, startYear=1221, endYear=1408,
         summary="In February 1221 the Mongol army of Tolui, son of Chinggis Khan, took Merv, drove the people onto the plain and killed most of them; the dams of the Murghab were later broken. Sultan Kala stands empty, its walls slumping, the Ark gutted. Only the mausoleum of Sanjar still raises its dome over the ruins. A small population lingers under the Ilkhans.",
         population="a few thousand at most",
         feel="Wind through empty gates, jackals in the bazaar, a few families farming among the mounds, travellers stopping to pray at Sanjar's tomb.",
         style="courtyard",
         houses=dict(title="Squatters in the ruins", text="A few houses patched together from fallen brick in the corners of old courtyards, roofed with reeds; most of the city a field of melted mud walls."),
         outskirts=dict(title="Fields gone to desert", text="With the canals neglected the oasis shrinks: tamarisk and sand over old fields, a few villages where water still runs.")),
    dict(id="timurid-1450", label="Shah Rukh's Merv", year=1450, startYear=1409, endYear=1510,
         summary="Timur's son Shah Rukh orders Merv rebuilt, by the usual account in 1409: the Murghab dam is restored, the canals cleaned, and a new, smaller walled town laid out south of the old cities, later called Abdullah Khan Kala. The old cities to the north are fields, brick quarries and shrines, among them the Askhab mausolea given new Timurid iwans.",
         population="perhaps 10,000–20,000",
         feel="Masons cutting new brick from old walls, water running again in the Majan, Turkmen herders selling sheep at the gate, pilgrims at the Companions' tombs.",
         style="courtyard",
         houses=dict(title="Houses of the new town", text="Mud-brick courtyard houses inside the Timurid walls, an ayvan porch on wooden posts facing the yard, flat roofs where families slept in summer; small mosques and a bazaar on the cross streets."),
         outskirts=dict(title="Fields among the ruins", text="Irrigated fields and melon beds laid out between the walls of the old cities; shepherds' pens in the empty gates of Sultan Kala.")),
]

# ---------------------------------------------------------------- water (the Murghab's canals run south to north through the oasis)
MAJAN = [(37.6340, 62.1668), (37.6400, 62.1669), (37.6460, 62.1671), (37.6519, 62.1672), (37.6600, 62.1675), (37.6680, 62.1680), (37.6771, 62.1685), (37.6860, 62.1690)]
RAZIK = [(37.6340, 62.1812), (37.6420, 62.1810), (37.6500, 62.1809), (37.6580, 62.1809), (37.6660, 62.1810), (37.6740, 62.1812), (37.6860, 62.1818)]
HURMUZ = [(37.6340, 62.1500), (37.6420, 62.1496), (37.6500, 62.1492), (37.6580, 62.1490), (37.6680, 62.1488), (37.6780, 62.1490), (37.6860, 62.1494)]
ASADI = [(37.6340, 62.2070), (37.6450, 62.2068), (37.6560, 62.2066), (37.6660, 62.2066), (37.6760, 62.2070), (37.6860, 62.2076)]

WATER = [
    dict(id="majan", name="Nahr Majan (Majan canal)", path=MAJAN, width=14, periods=["sasanian-500", "seljuk-1100", "timurid-1450"],
         blurb="The canal of the new city: Abu Muslim built his palace and mosque on its banks in 748, and it ran through the markets of Sultan Kala past the Friday mosque. Its line here is approximate."),
    dict(id="majan-dry", name="Majan canal (silted)", path=MAJAN, width=8, periods=["ruins-1250"],
         blurb="After 1221 the dams were broken and the canals left uncleaned; the Majan carries a trickle in spring floods."),
    dict(id="razik", name="Nahr Razik (Razik canal)", path=RAZIK, width=12,
         blurb="One of the four great canals taken off the Murghab, running north along the west side of the old city. Geographers name four: the Hurmuzfarra, Majan, Razik and Asadi; their courses here are schematic."),
    dict(id="hurmuzfarra", name="Nahr Hurmuzfarra", path=HURMUZ, width=12,
         blurb="The westernmost of Merv's four canals, watering the estates and koshks west of the city. Its Persian name recalls a Sasanian founder."),
    dict(id="asadi", name="Nahr Asadi", path=ASADI, width=10, periods=["sasanian-500", "seljuk-1100", "timurid-1450"],
         blurb="The eastern canal, watering the fields beyond the old city. Its name may come from Asad ibn Abdallah, Umayyad governor of Khurasan."),
    dict(id="erk-canal", name="Old canal of Margu", path=[(37.6340, 62.1940), (37.6450, 62.1945), (37.6560, 62.1952), (37.6650, 62.1955)], width=8, periods=["achaemenid-500"],
         blurb="An irrigation channel bringing Murghab water north to the fields below the citadel; the Achaemenid canal system is known only in outline."),
]

ERK_C, ERK_R = (37.6712, 62.1928), 260.0


def _circle(c, r, n=20):
    return [(round(c[0] + r / 111000.0 * math.sin(math.tau * i / n), 5), round(c[1] + r / 88100.0 * math.cos(math.tau * i / n), 5)) for i in range(n)]


ERK = _circle(ERK_C, ERK_R)
# Gyaur Kala: left open at the north where Erk Kala forms the wall
GK = [(37.6712, 62.1898), (37.6714, 62.1822), (37.6630, 62.1824), (37.6545, 62.1825), (37.6543, 62.1930), (37.6545, 62.2032), (37.6630, 62.2035), (37.6712, 62.2033), (37.6712, 62.1958)]
GK_POLY = GK + [(37.6735, 62.1928)]
SK = [(37.6520, 62.1575), (37.6518, 62.1700), (37.6525, 62.1795), (37.6600, 62.1797), (37.6690, 62.1798), (37.6768, 62.1792), (37.6772, 62.1700), (37.6768, 62.1610),
      (37.6720, 62.1560), (37.6640, 62.1553), (37.6560, 62.1560)]
AKK = [(37.6410, 62.1700), (37.6408, 62.1772), (37.6472, 62.1775), (37.6474, 62.1698)]

HILLS = [
    dict(id="erk-mound", name="Mound of Erk Kala", center=ERK_C, radius=290, label=False,
         blurb="The citadel stands on a rampart and mound of mud brick that grew with every rebuilding; today it rises some 30 metres above the plain."),
    dict(id="karakum-edge", name="Edge of the Karakum", center=(37.6830, 62.2040), radius=260, periods=AFTER,
         blurb="Where the canals failed after 1221 the dunes of the Black Sand desert crept in over the northern fields."),
]

ROADS = [
    # ---- Margu and Gyaur Kala
    dict(id="erk-road", name="Road to the citadel", path=[(37.6340, 62.1925), (37.6450, 62.1926), (37.6560, 62.1927), (37.6688, 62.1928)], width=10, style="major", labelled=True, periods=["achaemenid-500"],
         blurb="The track up from the southern fields and the road to Aria (Herat) to the gate of Erk Kala."),
    dict(id="erk-west", name="Road to Hyrcania", path=[(37.6712, 62.1897), (37.6700, 62.1750), (37.6690, 62.1600), (37.6680, 62.1400)], width=8, style="minor", periods=["achaemenid-500"],
         blurb="West across the oasis toward Parthia and Hyrcania by the Caspian."),
    dict(id="gk-ns", name="North–south street of Gyaur Kala", path=[(37.6545, 62.1930), (37.6600, 62.1929), (37.6629, 62.1928), (37.6688, 62.1928)], width=14, style="major", labelled=True, periods=GK_ON[:2],
         blurb="From the south gate to the foot of the citadel. The Hellenistic city was laid out round two main streets crossing at right angles, a plan still visible from the air."),
    dict(id="gk-ew", name="East–west street of Gyaur Kala", path=[(37.6629, 62.1824), (37.6629, 62.1880), (37.6629, 62.1928), (37.6629, 62.1980), (37.6629, 62.2035)], width=14, style="major", periods=GK_ON[:2],
         blurb="Across the city from the west gate to the east gate and the road to the Oxus."),
    dict(id="herat-road-gk", name="Road to Herat", path=[(37.6543, 62.1930), (37.6480, 62.1925), (37.6400, 62.1910), (37.6340, 62.1900)], width=12, style="major", labelled=True, periods=["sasanian-500"],
         blurb="South up the Murghab valley to Herat and on to Sistan and India."),
    dict(id="amul-road", name="Road to Amul and Bukhara", path=[(37.6629, 62.2035), (37.6680, 62.2080), (37.6760, 62.2130)], width=12, style="major", labelled=True, periods=["sasanian-500", "seljuk-1100"],
         blurb="North-east across the Karakum to Amul on the Oxus, then Bukhara and Samarkand: the Silk Road eastward."),
    dict(id="nishapur-road-early", name="Road to Nishapur", path=[(37.6629, 62.1824), (37.6625, 62.1700), (37.6620, 62.1550), (37.6610, 62.1400)], width=12, style="major", labelled=True, periods=["sasanian-500"],
         blurb="West to Sarakhs, Nishapur and Ctesiphon: the Great Khurasan Road."),
    # ---- Sultan Kala
    dict(id="sk-ns", name="Street of the Majan", path=[(37.6519, 62.1640), (37.6560, 62.1642), (37.6600, 62.1646), (37.6625, 62.1655), (37.6680, 62.1660), (37.6770, 62.1660)], width=14, style="major", labelled=True, periods=SELJUK,
         blurb="The main street of Sultan Kala from the south gate past the Friday mosque and Sanjar's mausoleum to the north gate, running beside the Majan canal."),
    dict(id="sk-ew", name="Street of the Shahristan gate", path=[(37.6632, 62.1554), (37.6632, 62.1600), (37.6631, 62.1650), (37.6640, 62.1700), (37.6650, 62.1796)], width=14, style="major", periods=SELJUK,
         blurb="Across Sultan Kala from the west gate to the east gate facing the old city (the shahristan); street names after the geographers, positions schematic."),
    dict(id="sk-old-link", name="Road to the old city", path=[(37.6650, 62.1796), (37.6640, 62.1812), (37.6629, 62.1824)], width=10, style="minor", periods=SELJUK,
         blurb="Over the Razik canal to the west gate of Gyaur Kala, by now a half-deserted quarter of potters and brick kilns."),
    dict(id="gk-ew-late", name="Lane through the old city", path=[(37.6629, 62.1824), (37.6629, 62.1928), (37.6629, 62.2035)], width=8, style="minor", periods=SELJUK,
         blurb="The old main street of Gyaur Kala, still the road east to Amul and Bukhara."),
    dict(id="nishapur-road", name="Road to Nishapur", path=[(37.6632, 62.1554), (37.6628, 62.1500), (37.6620, 62.1400)], width=12, style="major", labelled=True, periods=SELJUK,
         blurb="West to Sarakhs and Nishapur on the Khurasan Road; caravans from Iraq and Iran came in here."),
    dict(id="herat-road", name="Road to Herat", path=[(37.6519, 62.1640), (37.6460, 62.1645), (37.6400, 62.1650), (37.6340, 62.1652)], width=12, style="major", labelled=True, periods=SELJUK,
         blurb="South from the main gate up the Murghab valley to Herat."),
    dict(id="north-road", name="Road to Khwarazm", path=[(37.6770, 62.1660), (37.6810, 62.1662), (37.6860, 62.1665)], width=10, style="major", periods=SELJUK,
         blurb="North out of the city toward Khwarazm across the desert."),
    # ---- the Timurid town
    dict(id="akk-ns", name="Bazaar street of the new town", path=[(37.6408, 62.1736), (37.6441, 62.1736), (37.6473, 62.1736)], width=10, style="major", labelled=True, periods=TIMURID,
         blurb="The main street of Shah Rukh's town, from the south gate to the north gate."),
    dict(id="akk-ew", name="Cross street", path=[(37.6441, 62.1699), (37.6441, 62.1736), (37.6440, 62.1774)], width=8, style="minor", periods=TIMURID,
         blurb="The east–west street crossing at the bazaar."),
    dict(id="akk-north", name="Road to the old cities", path=[(37.6473, 62.1736), (37.6520, 62.1720), (37.6600, 62.1700), (37.6680, 62.1700)], width=8, style="minor", periods=TIMURID,
         blurb="North through the ruins of Sultan Kala, past fields laid out inside its walls."),
    dict(id="akk-herat", name="Road to Herat", path=[(37.6408, 62.1736), (37.6370, 62.1735), (37.6340, 62.1734)], width=10, style="major", labelled=True, periods=TIMURID,
         blurb="South to Herat, Shah Rukh's capital."),
    dict(id="akk-west", name="Road to Mashhad", path=[(37.6441, 62.1699), (37.6460, 62.1600), (37.6500, 62.1500), (37.6540, 62.1400)], width=8, style="minor", periods=TIMURID,
         blurb="West to Sarakhs and Mashhad, where Shah Rukh's wife Gawhar Shad had built her great mosque."),
    dict(id="ruin-track", name="Track through the ruins", path=[(37.6519, 62.1640), (37.6600, 62.1646), (37.6625, 62.1655), (37.6680, 62.1660), (37.6770, 62.1660)], width=6, style="minor", periods=["ruins-1250"],
         blurb="A path among the mounds where the main street of Sultan Kala had been, used by herders and pilgrims to Sanjar's tomb."),
]

WALLS = [
    dict(id="erk-walls", name="Walls of Erk Kala", path=ERK, closed=True, periods=ANCIENT,
         blurb="A ring of mud-brick walls on a rampart about 20 hectares round, raised in the Achaemenid period and rebuilt many times; the citadel of every city of Merv until the Seljuks."),
    dict(id="erk-ruin", name="Rampart of Erk Kala", path=ERK, closed=True, periods=SK_ON,
         blurb="The old citadel's rampart, abandoned as the city moved west: a ring of eroded earth inside the old city's north wall."),
    dict(id="gk-walls", name="Walls of Gyaur Kala", path=GK, closed=False, periods=["sasanian-500"],
         blurb="The square walls of Antiochia Margiana, thickened by the Parthians and Sasanians into a massive mud-brick rampart with towers, a gallery for archers and four gates in the middle of the sides."),
    dict(id="gk-walls-seljuk", name="Walls of the shahristan (Gyaur Kala)", path=GK, closed=False, periods=SELJUK,
         blurb="Still standing round the old city, now an inner suburb of potters and craftsmen; the Seljuks kept them in repair as a second line of defence."),
    dict(id="gk-ruin", name="Ruined walls of Gyaur Kala", path=GK, closed=False, periods=AFTER,
         blurb="Slumped ramparts, their towers rounded into mounds by wind and rain."),
    dict(id="sk-walls", name="Walls of Sultan Kala", path=SK, closed=True, periods=SELJUK,
         blurb="Built by Malik Shah about 1080 and strengthened by Sanjar: a high wall of mud brick and pakhsa with half-round towers every 15–30 metres, a lower outer wall and a ditch. Their trace here is simplified."),
    dict(id="sk-ruin", name="Ruined walls of Sultan Kala", path=SK, closed=True, periods=AFTER,
         blurb="Breached by the Mongols in 1221 and never repaired; the ramparts still stand many metres high today."),
    dict(id="akk-walls", name="Walls of Abdullah Khan Kala", path=AKK, closed=True, periods=TIMURID,
         blurb="The walls of the Timurid town, a rough square of about 600 metres with corner towers and gates on the axes; the later name comes from a 16th-century Uzbek ruler."),
]

GATES = [
    dict(id="gk-west-gate", name="West gate", position=(37.6629, 62.1824), periods=GK_ON[:2]),
    dict(id="gk-east-gate", name="East gate (gate of Amul)", position=(37.6630, 62.2035), periods=GK_ON[:2]),
    dict(id="sk-west-gate", name="Gate of Nishapur", position=(37.6632, 62.1555), periods=SELJUK),
    dict(id="sk-north-gate", name="North gate", position=(37.6770, 62.1660), periods=SELJUK),
    dict(id="sk-east-gate", name="Gate of the Shahristan", position=(37.6650, 62.1796), periods=SELJUK),
    dict(id="akk-south-gate", name="Herat gate", position=(37.6408, 62.1736), periods=TIMURID),
    dict(id="akk-west-gate", name="West gate", position=(37.6441, 62.1699), periods=TIMURID),
]

BRIDGES = [
    dict(id="razik-bridge", name="Bridge over the Razik", path=[(37.6629, 62.1803), (37.6629, 62.1818)], build="stone", arches=2, periods=["sasanian-500"],
         blurb="Where the road west left the old city by its west gate and crossed the Razik canal."),
    dict(id="razik-bridge-seljuk", name="Bridge over the Razik", path=[(37.6643, 62.1803), (37.6638, 62.1818)], build="stone", arches=2, periods=SELJUK,
         blurb="The crossing between the new city and the old, of fired brick."),
    dict(id="majan-bridge", name="Bridge of the Majan", path=[(37.6638, 62.1665), (37.6640, 62.1680)], build="stone", arches=2, periods=SELJUK,
         blurb="The main cross street bridging the Majan canal in the heart of Sultan Kala."),
    dict(id="asadi-bridge", name="Bridge over the Asadi", path=[(37.6668, 62.2058), (37.6676, 62.2075)], build="timber", arches=2, periods=["sasanian-500", "seljuk-1100"],
         blurb="A timber bridge on the road to Amul and the desert crossing."),
]

BLOCKS = [
    # ---- Margu: houses below the citadel and villages
    dict(name="Settlement below the citadel", polygon=[(37.6600, 62.1880), (37.6680, 62.1870), (37.6682, 62.1918), (37.6600, 62.1918)], density="loose", periods=["achaemenid-500"]),
    dict(name="Settlement east of the road", polygon=[(37.6610, 62.1936), (37.6682, 62.1938), (37.6680, 62.1990), (37.6610, 62.1990)], density="loose", periods=["achaemenid-500"]),
    dict(name="Village by the old canal", polygon=[(37.6480, 62.1955), (37.6530, 62.1958), (37.6530, 62.2000), (37.6480, 62.2000)], density="loose", periods=["achaemenid-500"]),
    # ---- Gyaur Kala in Sasanian times: four quarters between the cross streets
    dict(name="South-west quarter", polygon=[(37.6550, 62.1830), (37.6622, 62.1830), (37.6622, 62.1920), (37.6550, 62.1920)], density="dense", periods=["sasanian-500"]),
    dict(name="South-east quarter", polygon=[(37.6550, 62.1936), (37.6550, 62.1992), (37.6576, 62.1992), (37.6576, 62.2026), (37.6622, 62.2026), (37.6622, 62.1936)], density="dense", periods=["sasanian-500"]),
    dict(name="North-west quarter", polygon=[(37.6636, 62.1830), (37.6706, 62.1830), (37.6706, 62.1888), (37.6682, 62.1904), (37.6636, 62.1920)], density="dense", periods=["sasanian-500"]),
    dict(name="North-east quarter", polygon=[(37.6636, 62.1936), (37.6682, 62.1952), (37.6706, 62.1968), (37.6706, 62.2026), (37.6636, 62.2026)], density="dense", periods=["sasanian-500"]),
    dict(name="Suburb on the Majan", polygon=[(37.6600, 62.1690), (37.6660, 62.1690), (37.6660, 62.1790), (37.6600, 62.1790)], density="loose", periods=["sasanian-500"]),
    dict(name="Suburb at the east gate", polygon=[(37.6600, 62.2045), (37.6660, 62.2045), (37.6660, 62.2060), (37.6600, 62.2060)], density="loose", periods=["sasanian-500"]),
    # ---- Sultan Kala
    dict(name="Quarter of the Nishapur gate", polygon=[(37.6528, 62.1580), (37.6624, 62.1565), (37.6624, 62.1634), (37.6528, 62.1632)], density="dense", periods=SELJUK),
    dict(name="Quarter south of the bazaar", polygon=[(37.6528, 62.1680), (37.6624, 62.1682), (37.6630, 62.1788), (37.6532, 62.1788)], density="dense", periods=SELJUK),
    dict(name="Quarter of the north-west", polygon=[(37.6655, 62.1566), (37.6716, 62.1566), (37.6716, 62.1650), (37.6655, 62.1650)], density="dense", periods=SELJUK),
    dict(name="Quarter by the north gate", polygon=[(37.6722, 62.1580), (37.6762, 62.1620), (37.6762, 62.1652), (37.6722, 62.1652)], density="dense", periods=SELJUK),
    dict(name="Quarter below the Ark", polygon=[(37.6655, 62.1685), (37.6690, 62.1688), (37.6690, 62.1788), (37.6662, 62.1788)], density="dense", periods=SELJUK),
    dict(name="Garden palaces by the Ark", polygon=[(37.6696, 62.1688), (37.6762, 62.1690), (37.6762, 62.1716), (37.6696, 62.1716)], density="loose", periods=SELJUK),
    dict(name="Potters of the old city", polygon=[(37.6555, 62.1832), (37.6620, 62.1832), (37.6620, 62.1905), (37.6555, 62.1905)], density="loose", periods=SELJUK),
    dict(name="Old city: north-east", polygon=[(37.6640, 62.1940), (37.6700, 62.1975), (37.6700, 62.2025), (37.6640, 62.2025)], density="loose", periods=SELJUK),
    dict(name="Suburb outside the Nishapur gate", polygon=[(37.6600, 62.1505), (37.6660, 62.1505), (37.6660, 62.1545), (37.6600, 62.1545)], density="loose", periods=SELJUK),
    dict(name="Suburb outside the south gate", polygon=[(37.6440, 62.1652), (37.6505, 62.1652), (37.6505, 62.1664), (37.6440, 62.1664)], density="loose", periods=SELJUK),
    dict(name="Northern suburb", polygon=[(37.6780, 62.1668), (37.6840, 62.1668), (37.6840, 62.1682), (37.6780, 62.1682)], density="loose", periods=SELJUK),
    # ---- after 1221
    dict(name="Squatters by the mausoleum", polygon=[(37.6600, 62.1600), (37.6625, 62.1600), (37.6625, 62.1630), (37.6600, 62.1630)], density="loose", periods=["ruins-1250"]),
    dict(name="Hamlet in the old city", polygon=[(37.6580, 62.1840), (37.6610, 62.1840), (37.6610, 62.1880), (37.6580, 62.1880)], density="loose", periods=["ruins-1250"]),
    # ---- the Timurid town
    dict(name="North-west mahalla", polygon=[(37.6447, 62.1704), (37.6468, 62.1704), (37.6468, 62.1731), (37.6447, 62.1731)], density="dense", periods=TIMURID),
    dict(name="North-east mahalla", polygon=[(37.6447, 62.1741), (37.6468, 62.1741), (37.6468, 62.1770), (37.6447, 62.1770)], density="dense", periods=TIMURID),
    dict(name="South-west mahalla", polygon=[(37.6414, 62.1705), (37.6436, 62.1705), (37.6436, 62.1731), (37.6414, 62.1731)], density="dense", periods=TIMURID),
    dict(name="South-east mahalla", polygon=[(37.6414, 62.1741), (37.6436, 62.1741), (37.6436, 62.1768), (37.6414, 62.1768)], density="dense", periods=TIMURID),
    dict(name="Suburb north of the gate", polygon=[(37.6490, 62.1726), (37.6515, 62.1728), (37.6512, 62.1760), (37.6490, 62.1760)], density="loose", periods=TIMURID),
]

GARDENS = [
    dict(name="Fields of the Hurmuzfarra", polygon=[(37.6400, 62.1405), (37.6800, 62.1405), (37.6800, 62.1478), (37.6400, 62.1478)], kind="orchard"),
    dict(name="Fields beyond the Asadi", polygon=[(37.6380, 62.2082), (37.6780, 62.2082), (37.6780, 62.2125), (37.6380, 62.2125)], kind="orchard", periods=["achaemenid-500", "sasanian-500", "seljuk-1100", "timurid-1450"]),
    dict(name="Vineyards of the oasis", polygon=[(37.6560, 62.1580), (37.6680, 62.1580), (37.6680, 62.1660), (37.6560, 62.1660)], kind="vineyard", periods=ANCIENT),
    dict(name="Fields of the Majan", polygon=[(37.6520, 62.1685), (37.6590, 62.1685), (37.6590, 62.1790), (37.6520, 62.1790)], kind="orchard", periods=ANCIENT),
    dict(name="Melon fields", polygon=[(37.6380, 62.1510), (37.6468, 62.1510), (37.6468, 62.1640), (37.6380, 62.1640)], kind="orchard", periods=["achaemenid-500", "sasanian-500", "seljuk-1100", "timurid-1450"]),
    dict(name="Orchards south of the old city", polygon=[(37.6380, 62.1830), (37.6520, 62.1830), (37.6520, 62.1910), (37.6380, 62.1910)], kind="orchard", periods=["sasanian-500", "seljuk-1100", "timurid-1450"]),
    dict(name="Gardens of the Seljuk gentry", polygon=[(37.6680, 62.1500), (37.6760, 62.1500), (37.6760, 62.1545), (37.6680, 62.1545)], kind="park", periods=SELJUK),
    dict(name="Gardens north of the Ark", polygon=[(37.6780, 62.1700), (37.6840, 62.1700), (37.6840, 62.1800), (37.6780, 62.1800)], kind="orchard", periods=SELJUK),
    dict(name="Fields inside Sultan Kala", polygon=[(37.6530, 62.1580), (37.6600, 62.1580), (37.6600, 62.1630), (37.6530, 62.1630)], kind="orchard", periods=TIMURID),
    dict(name="Melon beds by the Majan", polygon=[(37.6530, 62.1680), (37.6620, 62.1680), (37.6620, 62.1780), (37.6530, 62.1780)], kind="orchard", periods=TIMURID),
    dict(name="Gardens of the new town", polygon=[(37.6370, 62.1690), (37.6400, 62.1690), (37.6400, 62.1790), (37.6370, 62.1790)], kind="park", periods=TIMURID),
    dict(name="Fields north of the citadel", polygon=[(37.6760, 62.1830), (37.6840, 62.1830), (37.6840, 62.2000), (37.6760, 62.2000)], kind="orchard", periods=ANCIENT + ["seljuk-1100", "timurid-1450"]),
]

MARSH = [
    dict(name="Tamarisk scrub", polygon=[(37.6790, 62.1710), (37.6840, 62.1710), (37.6840, 62.1800), (37.6790, 62.1800)], periods=["ruins-1250"]),
]

DISTRICTS = [
    dict(id="erk-kala", name="Erk Kala", polygon=ERK, periods=["achaemenid-500"],
         description="The round citadel of Margu: governor's residence, granaries and soldiers' houses behind a high rampart."),
    dict(id="gyaur-kala", name="Gyaur Kala (Antiochia Margiana)", polygon=GK_POLY, periods=["sasanian-500"],
         description="The square city of the Seleucids, Parthians and Sasanians, with Erk Kala as its citadel: houses, workshops, temples, a stupa and churches along a grid of streets."),
    dict(id="shahristan", name="The shahristan (Gyaur Kala)", polygon=GK_POLY, periods=SELJUK,
         description="The old walled city, emptying as people moved west to the Majan; kilns, workshops and a few mosques remain."),
    dict(id="sultan-kala", name="Sultan Kala", polygon=SK, periods=SELJUK,
         description="The Seljuk city west of the old one: the Shahriyar Ark, the Friday mosque and Sanjar's mausoleum, markets, libraries and dense courtyard houses along the Majan canal."),
    dict(id="sultan-kala-ruins", name="Ruins of Sultan Kala", polygon=SK, periods=AFTER,
         description="The great Seljuk city after 1221: empty courtyards, slumped walls and the lone dome of Sanjar's mausoleum."),
    dict(id="abdullah-khan-kala", name="Abdullah Khan Kala", polygon=AKK, periods=TIMURID,
         description="Shah Rukh's new town south of the old cities, walled and laid out on two cross streets."),
]

LABELS = [
    dict(text="Margu", position=(37.6600, 62.1760), size="lg", periods=["achaemenid-500"]),
    dict(text="Marw", position=(37.6500, 62.1990), size="lg", periods=["sasanian-500"]),
    dict(text="Marw al-Shahijan", position=(37.6500, 62.1560), size="lg", periods=SELJUK),
    dict(text="Sultan Kala", position=(37.6700, 62.1600), size="md", periods=SK_ON),
    dict(text="Gyaur Kala", position=(37.6590, 62.1960), size="md", periods=GK_ON),
    dict(text="Erk Kala", position=(37.6752, 62.1928), size="sm"),
    dict(text="Abdullah Khan Kala", position=(37.6385, 62.1736), size="sm", periods=TIMURID),
    dict(text="Majan", position=(37.6720, 62.1676), size="sm", rotation=-88, periods=["sasanian-500", "seljuk-1100", "timurid-1450"]),
    dict(text="Razik", position=(37.6480, 62.1804), size="sm", rotation=-88),
    dict(text="Hurmuzfarra", position=(37.6720, 62.1484), size="sm", rotation=-88),
    dict(text="Murghab oasis", position=(37.6810, 62.1900), size="md"),
    dict(text="Karakum", position=(37.6800, 62.2050), size="sm", periods=AFTER),
]
