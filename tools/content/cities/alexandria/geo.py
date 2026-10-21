# Alexandria: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
# The strip of land between the Mediterranean and Lake Mareotis, with Pharos island, the
# Heptastadion and the two harbours, from Alexander's foundation to the Ottoman port town.
import math

EARLY = ["ptolemy-280"]
PTOL = ["ptolemy-280", "ptolemaic-200"]
CLASSIC = ["ptolemaic-200", "roman-150ce"]
ANTIQUE = ["ptolemy-280", "ptolemaic-200", "roman-150ce", "late-400"]
LATER_ANT = ["ptolemaic-200", "roman-150ce", "late-400"]
ROMAN = ["roman-150ce", "late-400"]
LATE = ["late-400"]
OTT = ["ottoman-1600"]
ALL = ANTIQUE + OTT

# The ancient city is laid out on a grid turned about 23 degrees anticlockwise: the Canopic Way
# runs east-north-east. UV(u, v) gives (lat, lon) for a point u metres along the Canopic Way
# (east-north-east) and v metres across it (north-north-west) from its crossing with the
# Street of the Sema (the modern crossing of Horreya Road and Nabi Daniel Street).
P0 = (31.1966, 29.9003)
KX, KY = 111320.0 * math.cos(math.radians(31.194)), 110950.0
CA, SA = 0.9205, 0.3907


def UV(u, v):
    e = CA * u - SA * v
    n = SA * u + CA * v
    return (round(P0[0] + n / KY, 5), round(P0[1] + e / KX, 5))


def Q(u0, u1, v0, v1):
    """A block of the turned grid between u0..u1 and v0..v1."""
    return [UV(u0, v0), UV(u1, v0), UV(u1, v1), UV(u0, v1)]


def LINE(pts):
    return [UV(u, v) for u, v in pts]


CITY = dict(
    name="Alexandria", subtitle="Alexandria by Egypt",
    description="Alexandria from Alexander's foundation (331 BCE) to the Ottoman port town of about 1600: the strip of land between the Mediterranean and Lake Mareotis, Pharos island and the Heptastadion with the Great Harbour and the Eunostos, the Royal Quarter on Cape Lochias, the Canopic Way and the Serapeum hill in Rhakotis. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="ptolemaic-200",
    world=dict(heightScale=1.0, walls=["#E4D7BC", "#D9C7A2", "#EADFC8", "#CDB792", "#DCCBA8"], roofs=["#C9B28C", "#B9A27A"]),
    camera=dict(target=(31.2000, 29.8960), distance=40, maxDistance=140),
)
FRAME = ((31.2220, 29.8590), (31.1660, 29.9320))
RESOLUTION = 4096
PALETTE = dict(parchment="#E8D6AE", ink="#6A4A32", water="#5B8A93", hill="#7E7C58", road="#8A6A4A")
COMPASS = (31.2190, 29.9270)
CARTOUCHE = (31.1668, 29.8605)

PERIODS = [
    dict(id="ptolemy-280", label="The Young Capital", year=-280, startYear=-331, endYear=-247,
         summary="Founded by Alexander in 331 BCE on a limestone ridge between the sea and Lake Mareotis and laid out on a grid by his architect Deinocrates. Ptolemy I made it the capital of his kingdom; under Ptolemy II the Pharos lighthouse is finished, the Heptastadion ties Pharos island to the shore, and the Museum and its Library gather scholars. Limestone, mud brick and stucco.",
         population="perhaps 100,000 or more, growing fast",
         feel="Masons' hammers on the Pharos rock, Macedonian, Greek and Egyptian voices in the new streets, and the smell of lime kilns.",
         style="antique",
         houses=dict(title="Houses of the new grid", text="Houses of mud brick and limestone rubble round small courts, rendered with lime stucco and with flat roofs, filling the blocks of Deinocrates' grid. Greek settlers live near the palaces; Egyptians stay in the old village of Rhakotis by the Serapis shrine."),
         outskirts=dict(title="Lots still empty", text="Many blocks are still open ground or gardens; to the west the dead are buried in rock-cut tombs, and along the lake shore stand reed huts, kilns and vineyards.")),
    dict(id="ptolemaic-200", label="Ptolemaic Capital", year=-200, startYear=-246, endYear=-31,
         summary="The largest Greek city in the world and its intellectual capital: Eratosthenes, Aristophanes of Byzantium and the Library's copyists, the Serapeum of Ptolemy III on the Rhakotis hill, the palaces covering a quarter of the city, and the Sema where Alexander lies. Grain, papyrus, linen and glass go out; incense, ivory and spices come in through the lake harbour.",
         population="perhaps 300,000 free inhabitants by 60 BCE (Diodorus), plus slaves",
         feel="Bright stucco and colonnades, sailors' shouts in a dozen languages, and the lighthouse fire low on the night horizon.",
         style="antique",
         houses=dict(title="Stuccoed courtyard houses", text="Two- and three-storey houses of limestone and mud brick with stuccoed fronts, flat roofs used as terraces, and cisterns below filled from the canal each flood season. Shops open on the colonnaded main streets; the Jews live mainly in the Delta quarter by the palaces."),
         outskirts=dict(title="Gardens and the necropolis", text="West of the walls the necropolis, with gardens, embalming workshops and rock-cut tombs (Strabo); along the lake, vineyards of Mareotic wine and landing stages.")),
    dict(id="roman-150ce", label="Roman Alexandria", year=150, startYear=-30, endYear=296,
         summary="After Cleopatra's death (30 BCE) the city is ruled by a Roman prefect and ships Egypt's grain to Rome. Augustus finishes the Caesareum and sets two obelisks before it; the Library and Museum continue under imperial patronage. The Jewish community is broken in the revolt of 115–117, and Aurelian wrecks the Brucheion in 272.",
         population="perhaps 400,000–500,000; the second city of the empire",
         feel="Grain dust on the quays of the Eunostos, chariot-race factions shouting in the streets, and the smoke of glass furnaces.",
         style="antique",
         houses=dict(title="Apartment houses and courtyard homes", text="Dense blocks of two- to four-storey houses of limestone and fired brick round light wells, shops and workshops below, some rich houses with mosaic floors like the 'Villa of the Birds' at Kom el-Dikka."),
         outskirts=dict(title="Suburbs and tombs", text="Eleusis and Nicopolis to the east with the legion's camp, the necropolis to the west where the catacombs of Kom el-Shoqafa are dug, and market gardens and vineyards along the lake.")),
    dict(id="late-400", label="Christian Alexandria", year=400, startYear=297, endYear=642,
         summary="The see of the patriarch, Christian rival of Rome and Constantinople. The Serapeum is pulled down in 391 and churches rise on old temples; the Brucheion lies in ruin, the tsunami of 365 has wrecked the harbour fronts, and the city's grain now sails to Constantinople. Hypatia teaches mathematics and philosophy until her murder in 415.",
         population="perhaps 200,000",
         feel="Church bells are still rare: wooden semantra, monks' psalms in Coptic and Greek, street fights between factions, and teachers lecturing in the halls of Kom el-Dikka.",
         style="antique",
         houses=dict(title="Houses and workshops of late antiquity", text="Older houses subdivided and rebuilt with reused stone; workshops for glass, bone and metal fill former courtyards, as excavated at Kom el-Dikka. Churches, hospices and monasteries take over whole blocks."),
         outskirts=dict(title="Ruins and monasteries", text="The Brucheion is a field of ruins and gardens; outside the walls lie monasteries, martyrs' shrines and the old necropolis.")),
    dict(id="ottoman-1600", label="Iskandariya under the Ottomans", year=1600, startYear=1477, endYear=1798,
         summary="A shrunken port. The silted Heptastadion has become a broad neck of land where the town of a few thousand now stands, between the Old Port (west, for Muslim ships) and the New Port (east, for Christian ships). Qaitbay's fort of 1477 holds the Pharos site; inside the medieval walls lie ruin mounds, cisterns, palm gardens, Pompey's Pillar and one standing Needle.",
         population="perhaps 5,000–15,000; the French counted about 8,000 in 1798",
         feel="The call to prayer over rubble fields, European factors haggling over pepper and coffee, and dust blowing from the ruin mounds.",
         style="courtyard",
         houses=dict(title="Houses of the neck town", text="Houses of two or three storeys built of stone taken from the ancient ruins, with flat roofs, wooden mashrabiya windows and inner courts, packed in narrow lanes between the two harbours."),
         outskirts=dict(title="The empty walled city", text="Inside the old Arab walls: palm groves, gardens watered from the canal cisterns, ruin mounds like Kom el-Dikka, a few mosques and churches, and the Coptic and Greek quarters.")),
]

# ---------------------------------------------------------------- water
# The sea is drawn as wide ribbons kept just off the shore; the two harbours are filled with
# shorter ribbons. Pharos is the gap between them, outlined as an island. In 1600 the
# Heptastadion has silted into a neck of land, so the harbour ribbons stop short of it.
WATER = [
    dict(id="open-sea", name="The Sea", width=3280,
         path=[(31.22900, 29.85400), (31.23100, 29.88000), (31.23300, 29.94000)]),
    dict(id="sea", name="The Sea", width=1100,
         path=[(31.20856, 29.84933), (31.21013, 29.85370), (31.21216, 29.85792), (31.21476, 29.86292), (31.21718, 29.86796), (31.21927, 29.87206), (31.22095, 29.87499), (31.22238, 29.87718), (31.22462, 29.88092), (31.22637, 29.89076), (31.22637, 29.90213), (31.22307, 29.91269), (31.22099, 29.91772), (31.22170, 29.91713), (31.22145, 29.91247), (31.22249, 29.91570), (31.22451, 29.92178), (31.22671, 29.92891), (31.22852, 29.93692)],
         blurb="The Mediterranean. The coast of Egypt is low and featureless and the approach to Alexandria is strewn with reefs: hence the lighthouse, seen far out to sea."),
    dict(id="sea-west", name="The Sea", width=1180,
         path=[(31.20400, 29.85400), (31.20750, 29.86000)]),
    dict(id="east-coast", name="The Sea", width=840, periods=ANTIQUE,
         path=[(31.21509, 29.90387), (31.21784, 29.90718), (31.21565, 29.91249), (31.21472, 29.91326), (31.21477, 29.91412), (31.21617, 29.91851), (31.21818, 29.92453), (31.22025, 29.93125), (31.22199, 29.93893)]),
    dict(id="pharos-waters", name="Waters of Pharos", width=840, periods=ANTIQUE,
         path=[(31.20017, 29.85063), (31.20632, 29.86189), (31.20892, 29.86689), (31.21132, 29.87190), (31.21355, 29.87626), (31.21544, 29.87956), (31.21691, 29.88182), (31.21947, 29.88609), (31.21551, 29.89137), (31.21123, 29.89094), (31.20824, 29.88969), (31.20517, 29.88805), (31.20178, 29.88585), (31.20053, 29.88116), (31.19961, 29.87705), (31.19851, 29.87204), (31.19742, 29.86711), (31.19612, 29.86188), (31.20017, 29.85063)]),
    dict(id="eunostos-shore", name="Eunostos", width=840, periods=ANTIQUE,
         path=[(31.17993, 29.84871), (31.18231, 29.85728), (31.18462, 29.86189), (31.18758, 29.86781), (31.19084, 29.87375), (31.19358, 29.87882), (31.19596, 29.88358), (31.19828, 29.88683), (31.19899, 29.88785)]),
    dict(id="eunostos", name="Eunostos (Harbour of Good Return)", width=1360, periods=ANTIQUE,
         path=[(31.19250, 29.85400), (31.19350, 29.86200), (31.19550, 29.87100), (31.19750, 29.87800)],
         blurb="The western harbour, west of the Heptastadion, open to the sea between Pharos and the mainland. Inside it lay the Kibotos ('the Box'), a dug basin joined by canal to Lake Mareotis; the grain ships for Rome loaded here."),
    dict(id="eunostos-in", name="Eunostos", width=1240, periods=ANTIQUE,
         path=[(31.19750, 29.87800), (31.19950, 29.88400)]),
    dict(id="great-harbour-shore", name="Great Harbour", width=840, periods=ANTIQUE,
         path=[(31.19932, 29.88839), (31.20024, 29.89024), (31.20204, 29.89324), (31.20357, 29.89630), (31.20476, 29.89844), (31.20653, 29.90028), (31.20871, 29.90151), (31.21128, 29.90220), (31.21433, 29.90296), (31.21609, 29.90507)]),
    dict(id="great-harbour", name="Great Harbour (Megas Limen)", width=1130, periods=ANTIQUE,
         path=[(31.20250, 29.89150), (31.20600, 29.89400), (31.20900, 29.89750), (31.21400, 29.89900)],
         blurb="The eastern harbour, between the Heptastadion, Pharos and Cape Lochias, entered by a narrow channel past the lighthouse rock. Its south shore held the royal docks, the Poseidion, the Timonium, the Emporion and the warehouses."),
    dict(id="harbour-mouth", name="Harbour mouth", width=1580, periods=ANTIQUE,
         path=[(31.21400, 29.89900), (31.21850, 29.89750)]),
    dict(id="coast-1600", name="The Sea", width=840, periods=OTT,
         path=[(31.17993, 29.84871), (31.18231, 29.85728), (31.18462, 29.86189), (31.18758, 29.86781), (31.19084, 29.87375), (31.19358, 29.87882), (31.19563, 29.88291), (31.19401, 29.88183), (31.19678, 29.87887), (31.19952, 29.87679), (31.19951, 29.87661), (31.19851, 29.87204), (31.19742, 29.86711), (31.19612, 29.86188), (31.20017, 29.85063), (31.20632, 29.86189), (31.20892, 29.86689), (31.21132, 29.87190), (31.21355, 29.87626), (31.21544, 29.87956), (31.21691, 29.88182), (31.21947, 29.88609), (31.21551, 29.89137), (31.21165, 29.89098), (31.20931, 29.89069), (31.20890, 29.89164), (31.20547, 29.89506), (31.20311, 29.89790), (31.20463, 29.89600), (31.20293, 29.89514), (31.20476, 29.89844), (31.20653, 29.90028), (31.20871, 29.90151), (31.21128, 29.90220), (31.21433, 29.90296), (31.21784, 29.90718), (31.21565, 29.91249), (31.21472, 29.91326), (31.21477, 29.91412), (31.21617, 29.91851), (31.21818, 29.92453), (31.22025, 29.93125), (31.22199, 29.93893)]),
    dict(id="western-harbour", name="Old Port (Western Harbour)", width=1350, periods=OTT,
         path=[(31.19250, 29.85400), (31.19350, 29.86200), (31.19500, 29.87000), (31.19650, 29.87600)],
         blurb="The old Eunostos. Under the Mamluks and Ottomans it was reserved to Muslim ships; Christian merchantmen had to use the shallower, rockier New Port."),
    dict(id="new-port", name="New Port (Eastern Harbour)", width=1400, periods=OTT,
         path=[(31.20750, 29.89750), (31.21000, 29.89850), (31.21400, 29.89900)],
         blurb="The ancient Great Harbour, half silted, where Venetian, French and English ships anchored under the guns of Qaitbay's fort."),
    dict(id="mareotis", name="Lake Mareotis", width=2810,
         path=[(31.16200, 29.85000), (31.16400, 29.90000), (31.16800, 29.94000)],
         blurb="A large shallow lake south of the city, fed by Nile canals. Strabo thought its harbour busier than the sea harbours: Egyptian grain, papyrus and the Mareotic wine of its shores came in here."),
    dict(id="mareotis-shore", name="Lake Mareotis", width=620,
         path=[(31.17180, 29.85013), (31.17250, 29.87019), (31.17351, 29.88527), (31.17431, 29.89533), (31.17531, 29.90536), (31.17632, 29.91545), (31.17782, 29.92545), (31.17931, 29.94036)]),
    dict(id="royal-harbour", name="Royal harbour", width=300, periods=ANTIQUE,
         path=[(31.2060, 29.9022), (31.2108, 29.9040)],
         blurb="A closed harbour for the kings' own ships on the west side of Cape Lochias, with the island of Antirhodos and its small palace off it."),
    dict(id="lake-harbour", name="Lake harbour", width=260, periods=ANTIQUE,
         path=[(31.1755, 29.9095), (31.1812, 29.9085)],
         blurb="The quays on Lake Mareotis where the Nile boats unloaded."),
    dict(id="canal", name="Canal of Schedia", width=34,
         path=[(31.1890, 29.9400), (31.1860, 29.9250), (31.1830, 29.9120), (31.1812, 29.9085), (31.1803, 29.9000), (31.1806, 29.8930), (31.1825, 29.8870), (31.1855, 29.8820), (31.1885, 29.8800)],
         blurb="The canal from the Canopic branch of the Nile at Schedia, bringing fresh water and river boats along the south of the city to the Kibotos in the western harbour. It filled the city's cisterns at every flood; Muhammad Ali's Mahmudiya canal (1820) follows much of its line."),
    dict(id="kibotos", name="Kibotos", width=170, periods=ANTIQUE,
         path=[(31.1880, 29.8792), (31.1905, 29.8810)]),
]
PHAROS = [(31.2008, 29.8590), (31.2032, 29.8640), (31.2058, 29.8690), (31.2082, 29.8740), (31.2105, 29.8785), (31.2125, 29.8820), (31.2140, 29.8843), (31.2149, 29.8858), (31.2140, 29.8870), (31.2120, 29.8868), (31.2096, 29.8858), (31.2068, 29.8843), (31.2048, 29.8830), (31.2040, 29.8800), (31.2031, 29.8760), (31.2020, 29.8710), (31.2009, 29.8660), (31.1999, 29.8620)]
# in 1600 Pharos is joined to the mainland by the silted neck: one outline from the neck's west root round the island and back down its east side
NECK_1600 = [(31.1945, 29.8870), (31.1990, 29.8822), (31.2032, 29.8790)] + PHAROS[14:] + PHAROS[:10] + [(31.2072, 29.8862), (31.2060, 29.8890), (31.2030, 29.8920), (31.2005, 29.8950), (31.1985, 29.8975), (31.1972, 29.8925)]
ISLANDS = [
    dict(name="Pharos", polygon=PHAROS, periods=ANTIQUE),
    dict(name="Antirhodos", periods=CLASSIC, polygon=[(31.2072, 29.9008), (31.2082, 29.9012), (31.2084, 29.9024), (31.2074, 29.9026), (31.2068, 29.9016)]),
    dict(name="Pharos and the neck", polygon=NECK_1600, periods=OTT),
]

HILLS = [
    dict(id="serapeum-hill", name="Serapeum hill", center=UV(-830, -1330), radius=230, label=False, blurb="The rocky hill of Rhakotis, the highest natural ground of the city, crowned by the Serapeum."),
    dict(id="kom-el-dikka-mound", name="Kom el-Dikka", center=UV(251, -360), radius=200, periods=OTT, blurb="'Mound of rubble': medieval and later dumps over the Roman theatre and baths, used as a lookout by the French in 1798 and only cleared from 1960."),
    dict(id="kom-el-nadura", name="Kom el-Nadura", center=UV(-640, 230), radius=120, periods=OTT, blurb="'Lookout mound', a ruin heap by the Old Port from which ships were sighted."),
]

# ---------------------------------------------------------------- streets
SUN_U, MOON_U = 2700, -1850
ROADS = [
    dict(id="canopic-way", name="Canopic Way (Plateia)", path=LINE([(MOON_U, 0), (-900, 0), (0, 0), (1200, 0), (SUN_U, 0)]), width=30, style="major", labelled=True, periods=ANTIQUE,
         blurb="The main east-west avenue, about 30 m wide and lined with colonnades from the Gate of the Sun to the Gate of the Moon (Achilles Tatius). Its line is followed today by Horreya Road."),
    dict(id="canopus-road", name="Road to Eleusis and Canopus", path=LINE([(SUN_U, 0), (3150, 0), (3500, 40)]), width=14, style="major", periods=ANTIQUE),
    dict(id="soma-street", name="Street of the Sema", path=LINE([(0, -1830), (0, 0), (0, 455)]), width=24, style="major", labelled=True, periods=ANTIQUE,
         blurb="The main north-south street from the Great Harbour past the Sema to the lake harbour, crossing the Canopic Way at the heart of the city (the line of Nabi Daniel Street)."),
    dict(id="serapeum-street", name="Street of the Serapeum", path=LINE([(-850, 0), (-850, -1285)]), width=14, labelled=True, periods=LATER_ANT),
    dict(id="rhakotis-street", name="Street of Rhakotis", path=LINE([(-1500, 140), (-1500, -1150)]), width=10, periods=ANTIQUE),
    dict(id="lochias-street", name="Street of Lochias", path=LINE([(1150, -1550), (1150, 0), (1150, 960)]), width=14, labelled=True, periods=ANTIQUE,
         blurb="Into the Royal Quarter and out toward the palaces on Cape Lochias."),
    dict(id="delta-street", name="Street of the Delta", path=LINE([(2000, -1550), (2000, 0), (2000, 900)]), width=10, periods=ANTIQUE),
    dict(id="harbour-street", name="Harbour street", path=LINE([(-300, 280), (1150, 280), (2600, 280)]), width=12, periods=ANTIQUE),
    dict(id="l-south", name="Street L2", path=LINE([(-1650, -550), (2700, -550)]), width=10, periods=ANTIQUE),
    dict(id="l-south2", name="Street L3", path=LINE([(-1450, -1060), (2700, -1060)]), width=10, periods=LATER_ANT),
    dict(id="necropolis-road", name="Road to the Necropolis", path=LINE([(MOON_U, 0), (-2150, -60), (-2600, -150), (-3300, -300), (-4200, -560)]), width=12, labelled=True, periods=ANTIQUE,
         blurb="West from the Gate of the Moon past the Kibotos to the necropolis, 'the city of the dead', with its gardens and embalming houses."),
    dict(id="pharos-road", name="Pharos road", path=[(31.2048, 29.8830), (31.2075, 29.8840), (31.2100, 29.8846), (31.2128, 29.8848)], width=10, periods=ANTIQUE),
    dict(id="pharos-village-road", name="Pharos village street", path=[(31.2048, 29.8830), (31.2040, 29.8770), (31.2028, 29.8700), (31.2015, 29.8640)], width=8, periods=ANTIQUE),
    # Ottoman: the neck town and tracks across the walled ruin-field
    dict(id="neck-street", name="Main street of the neck", path=[(31.1985, 29.8930), (31.2010, 29.8885), (31.2040, 29.8845), (31.2075, 29.8845), (31.2125, 29.8850)], width=10, style="major", labelled=True, periods=OTT,
         blurb="From the Sea Gate of the walled city across the neck to the Ras el-Tin end and Qaitbay's fort: the town's bazaars, khans and mosques line it."),
    dict(id="rosetta-road", name="Road to Bab Rashid", path=LINE([(-700, 300), (-500, 100), (0, 0), (800, -40), (1480, -100), (2200, -150), (3500, -150)]), width=10, style="major", labelled=True, periods=OTT,
         blurb="Across the empty walled city along the old Canopic Way to the Rosetta Gate and the road to Rashid on the Nile."),
    dict(id="sidra-road", name="Road to Bab Sidra", path=LINE([(-500, 100), (-700, -500), (-880, -1000), (-950, -1200)]), width=8, periods=OTT,
         blurb="South past the Attarine mosque to the gate by Pompey's Pillar and the canal."),
    dict(id="old-port-road", name="Road to the Old Port", path=[(31.1985, 29.8930), (31.1962, 29.8900), (31.1950, 29.8875)], width=8, periods=OTT),
]

# ---------------------------------------------------------------- walls and gates
ANCIENT_WALL = LINE([(3050, 905), (SUN_U, 600), (SUN_U, 0), (SUN_U, -1550), (0, -1550), (-600, -1480), (-1150, -1480), (-1700, -700), (MOON_U, 0), (-1980, 110)])
ARAB_WALL = LINE([(1260, 1080), (1480, -100), (1300, -1000), (-650, -1150), (-1300, -880), (-1350, -200), (-1150, 260)])
WALLS = [
    dict(id="ancient-walls", name="City walls", path=ANCIENT_WALL, periods=ANTIQUE,
         blurb="The Hellenistic walls on the land side, about 15 km round with the sea fronts. Their trace is known only in part (Mahmoud el-Falaki's survey of 1866); this line is the usual reconstruction, with the Gates of the Sun and the Moon at the two ends of the Canopic Way."),
    dict(id="arab-walls", name="Arab walls", path=ARAB_WALL, periods=OTT,
         blurb="The walls of the medieval city, built under the Tulunids in the 9th century and rebuilt by the Mamluks, enclosing a much smaller area than the ancient walls. By 1600 they guard mostly ruins and gardens; the living town lies outside on the neck."),
]
GATES = [
    dict(id="moon-gate", name="Gate of the Moon", position=UV(MOON_U, 0), periods=ANTIQUE),
    dict(id="sun-gate", name="Gate of the Sun", position=UV(SUN_U, 0), periods=ANTIQUE),
    dict(id="bab-al-bahr", name="Bab al-Bahr (Sea Gate)", position=(31.1985, 29.8930), periods=OTT),
    dict(id="bab-sidra", name="Bab Sidra", position=UV(-1000, -1065), periods=OTT),
]
BRIDGES = [
    dict(id="heptastadion-b", name="Heptastadion", path=[(31.1962, 29.8905), (31.2048, 29.8828)], build="stone", arches=2, landmarkId="heptastadion", periods=ANTIQUE,
         blurb="The 'seven-stade' causeway, about 1.2 km long, joining Pharos to the mainland and dividing the two harbours, with two bridged openings for ships to pass between them."),
]
AQUEDUCTS = []

# ---------------------------------------------------------------- built-up areas
# shore-bounded blocks: points along the coast (see the water ribbons) close the polygons
N_RHAK = LINE([(-1830, 25), (-880, 25), (-880, 230), (-1300, 150), (-1830, 90)])
N_CENTRE = LINE([(-820, 25), (-30, 25), (-30, 255), (-500, 255), (-820, 260)])
N_CAES = LINE([(-300, 305), (-30, 305), (-30, 380), (-300, 360)])
N_BRUCH = LINE([(30, 25), (1120, 25), (1120, 255), (30, 255)])
N_BRUCH2 = LINE([(230, 305), (1120, 305), (1120, 800), (900, 760), (650, 560), (230, 470)])
N_DELTA = LINE([(1180, 25), (1970, 25), (1970, 255), (1180, 255)])
N_DELTA2 = LINE([(1180, 305), (1970, 305), (1970, 820), (1580, 900), (1180, 900)])
N_EAST = LINE([(2030, 25), (2680, 25), (2680, 255), (2030, 255)])
N_EAST2 = LINE([(2030, 305), (2680, 305), (2680, 780), (2030, 800)])
S1_W = Q(-1680, -1520, -530, -25)
S1_RW = Q(-1480, -870, -530, -25)
S1_C = Q(-830, -20, -530, -25)
S1_E = Q(20, 1130, -530, -25)
S1_F = Q(1170, 1980, -530, -25)
S1_G = Q(2020, 2680, -530, -25)
S2_W = Q(-1480, -870, -1040, -570)
S2_C = Q(-830, -20, -1040, -570)
S2_E = Q(20, 1130, -1040, -570)
S2_F = Q(1170, 1980, -1040, -570)
S2_G = Q(2020, 2680, -1040, -570)
S3_W = Q(-1150, -940, -1440, -1080)
S3_C = Q(-720, -20, -1440, -1080)
S3_E = Q(20, 1130, -1530, -1080)
S3_F = Q(1170, 1980, -1530, -1080)
S3_G = Q(2020, 2680, -1530, -1080)
PHAROS_VILLAGE = [(31.2018, 29.8650), (31.2045, 29.8662), (31.2068, 29.8715), (31.2088, 29.8762), (31.2082, 29.8790), (31.2052, 29.8790), (31.2038, 29.8745), (31.2026, 29.8700)]
LAKE_SHORE = LINE([(-600, -1610), (2600, -1640), (2600, -1880), (1700, -1900), (300, -1760), (-500, -1640)])
NECROPOLIS_GARDENS = [(31.1795, 29.8640), (31.1820, 29.8680), (31.1845, 29.8720), (31.1840, 29.8770), (31.1810, 29.8790), (31.1780, 29.8740), (31.1770, 29.8680), (31.1775, 29.8640)]
NECK_TOWN = [(31.1960, 29.8905), (31.1995, 29.8850), (31.2033, 29.8812), (31.2050, 29.8840), (31.2062, 29.8862), (31.2035, 29.8900), (31.2005, 29.8935), (31.1985, 29.8945)]
NECK_NORTH = [(31.2070, 29.8780), (31.2100, 29.8800), (31.2122, 29.8830), (31.2115, 29.8850), (31.2085, 29.8850), (31.2062, 29.8830)]

BLOCKS = [
    # the young capital: centre and Rhakotis built, the east half still filling in
    dict(name="Rhakotis", polygon=N_RHAK, density="dense", periods=ANTIQUE),
    dict(name="Rhakotis", polygon=S1_RW, density="dense", periods=ANTIQUE),
    dict(name="Rhakotis", polygon=S1_W, density="dense", periods=ANTIQUE),
    dict(name="Rhakotis", polygon=S2_W, density="loose", periods=EARLY),
    dict(name="Rhakotis", polygon=S2_W, density="dense", periods=LATER_ANT),
    dict(name="Below the Serapeum", polygon=S3_W, density="loose", periods=ANTIQUE),
    dict(name="Harbour quarter", polygon=N_CENTRE, density="dense", periods=ANTIQUE),
    dict(name="By the Poseidion", polygon=N_CAES, density="dense", periods=ANTIQUE),
    dict(name="Brucheion", polygon=N_BRUCH, density="dense", periods=["ptolemy-280", "ptolemaic-200", "roman-150ce"]),
    dict(name="Brucheion ruins", polygon=N_BRUCH, density="loose", periods=LATE),
    dict(name="Brucheion", polygon=N_BRUCH2, density="loose", periods=PTOL + ["roman-150ce"]),
    dict(name="Delta", polygon=N_DELTA, density="loose", periods=EARLY),
    dict(name="Delta (Jewish quarter)", polygon=N_DELTA, density="dense", periods=CLASSIC),
    dict(name="Delta", polygon=N_DELTA, density="loose", periods=LATE),
    dict(name="Delta (Jewish quarter)", polygon=N_DELTA2, density="dense", periods=CLASSIC),
    dict(name="Delta", polygon=N_DELTA2, density="loose", periods=LATE),
    dict(name="Eastern quarter", polygon=N_EAST, density="dense", periods=LATER_ANT),
    dict(name="Eastern quarter", polygon=N_EAST2, density="loose", periods=LATER_ANT),
    dict(name="City centre", polygon=S1_C, density="dense", periods=ANTIQUE),
    dict(name="City centre", polygon=S1_E, density="dense", periods=ANTIQUE),
    dict(name="Beta", polygon=S1_F, density="loose", periods=EARLY),
    dict(name="Beta", polygon=S1_F, density="dense", periods=LATER_ANT),
    dict(name="Gamma", polygon=S1_G, density="dense", periods=LATER_ANT),
    dict(name="Neapolis", polygon=S2_C, density="loose", periods=EARLY),
    dict(name="Neapolis", polygon=S2_C, density="dense", periods=LATER_ANT),
    dict(name="Neapolis", polygon=S2_E, density="dense", periods=LATER_ANT),
    dict(name="Epsilon", polygon=S2_F, density="dense", periods=LATER_ANT),
    dict(name="Epsilon", polygon=S2_G, density="loose", periods=LATER_ANT),
    dict(name="South quarter", polygon=S3_C, density="dense", periods=LATER_ANT),
    dict(name="South quarter", polygon=S3_E, density="loose", periods=LATER_ANT),
    dict(name="South quarter", polygon=S3_F, density="loose", periods=LATER_ANT),
    dict(name="South-east quarter", polygon=S3_G, density="loose", periods=LATER_ANT),
    dict(name="Pharos village", polygon=PHAROS_VILLAGE, density="loose", periods=ANTIQUE),
    dict(name="Lake quays", polygon=LAKE_SHORE, density="loose", periods=LATER_ANT),
    # the Ottoman town on the neck; a few clusters inside the walls
    dict(name="The neck town (Turkish town)", polygon=NECK_TOWN, density="dense", periods=OTT),
    dict(name="Ras el-Tin end", polygon=NECK_NORTH, density="loose", periods=OTT),
    dict(name="Attarine", polygon=Q(-1100, -560, -400, 180), density="loose", periods=OTT),
    dict(name="Coptic and Greek quarter", polygon=Q(-280, 380, -100, 200), density="loose", periods=OTT),
]
GARDENS = [
    dict(name="Royal gardens", polygon=LINE([(1180, 960), (1120, 820), (1450, 820), (1560, 960)]), kind="park", periods=PTOL + ["roman-150ce"]),
    dict(name="Gardens of the necropolis", polygon=NECROPOLIS_GARDENS, kind="orchard", periods=ANTIQUE),
    dict(name="Vineyards by the lake", polygon=LINE([(-1300, -1700), (-700, -1700), (-700, -1950), (-1300, -1900)]), kind="vineyard", periods=CLASSIC),
    dict(name="Monastery gardens", polygon=Q(2030, 2680, -1530, -1080), kind="orchard", periods=LATE),
    dict(name="Palm gardens in the walls", polygon=Q(-1100, 1250, -1000, -450), kind="orchard", periods=OTT),
    dict(name="Palm gardens in the walls", polygon=Q(450, 1250, -400, 600), kind="orchard", periods=OTT),
    dict(name="Gardens by the canal", polygon=LINE([(-600, -1610), (1600, -1640), (1600, -1880), (300, -1760), (-500, -1640)]), kind="orchard", periods=OTT),
]
MARSH = [
    dict(name="Lake shallows", polygon=LINE([(1700, -2050), (3100, -2350), (3100, -2600), (1700, -2350)]), periods=ALL),
]
DISTRICTS = [
    dict(id="brucheion", name="Brucheion (Royal Quarter)", polygon=LINE([(30, 25), (1150, 25), (1150, 960), (650, 560), (30, 470)]), periods=ANTIQUE,
         description="The royal quarter, a quarter or even a third of the city by Strabo's account: palaces, the Museum and Library, gardens, the Sema and the royal harbour. Ruined in the fighting of 272 under Aurelian and never rebuilt."),
    dict(id="rhakotis", name="Rhakotis", polygon=LINE([(-1830, 25), (-880, 25), (-880, -1480), (-1150, -1480), (-1700, -700)]), periods=ANTIQUE,
         description="The Egyptian village that was here before Alexander, and afterwards the native quarter of the city round the Serapis sanctuary on its hill."),
    dict(id="delta", name="Delta", polygon=LINE([(1180, 25), (1970, 25), (1970, 820), (1580, 900), (1180, 900)]), periods=CLASSIC,
         description="One of the city's five lettered districts, east of the palaces, where most of Alexandria's Jews lived (Philo, Josephus). Two of the five districts were called 'Jewish' in Philo's day."),
    dict(id="neck-town", name="Turkish town", polygon=NECK_TOWN, periods=OTT,
         description="The living town of the 16th–18th centuries, built on the silt that had buried the Heptastadion, with its khans, mosques, the European consuls' fondachi and the customs house."),
]
LABELS = [
    dict(text="THALASSA", position=(31.2190, 29.8990), size="lg", rotation=-5, periods=PTOL),
    dict(text="MARE NOSTRUM", position=(31.2190, 29.8990), size="lg", rotation=-5, periods=ROMAN),
    dict(text="BAHR AL-RUM", position=(31.2190, 29.8990), size="lg", rotation=-5, periods=OTT),
    dict(text="LIMNE MAREOTIS", position=(31.1690, 29.8980), size="lg", rotation=-2, periods=PTOL),
    dict(text="LACUS MAREOTIS", position=(31.1690, 29.8980), size="lg", rotation=-2, periods=ROMAN),
    dict(text="BUHAYRAT MARYUT", position=(31.1690, 29.8980), size="lg", rotation=-2, periods=OTT),
    dict(text="Megas Limen", position=(31.2085, 29.8960), size="md", rotation=-10, periods=ANTIQUE),
    dict(text="Eunostos", position=(31.1935, 29.8680), size="md", rotation=-20, periods=ANTIQUE),
    dict(text="Old Port", position=(31.1935, 29.8680), size="md", rotation=-20, periods=OTT),
    dict(text="New Port", position=(31.2085, 29.8975), size="md", rotation=-10, periods=OTT),
    dict(text="Pharos", position=(31.2060, 29.8700), size="md", rotation=-30, periods=ANTIQUE),
    dict(text="Ras el-Tin", position=(31.2045, 29.8680), size="sm", rotation=-30, periods=OTT),
    dict(text="Rhakotis", position=UV(-1300, -300), size="md", rotation=-23, periods=ANTIQUE),
    dict(text="Brucheion", position=UV(700, 420), size="md", rotation=-23, periods=PTOL + ["roman-150ce"]),
    dict(text="Delta", position=UV(1600, 500), size="sm", rotation=-23, periods=CLASSIC),
    dict(text="Lochias", position=(31.2122, 29.9078), size="sm", rotation=-70, periods=ANTIQUE),
    dict(text="Necropolis", position=(31.1835, 29.8690), size="sm", rotation=-25, periods=ANTIQUE),
    dict(text="Eleusis", position=UV(3350, -350), size="sm", rotation=-23, periods=LATER_ANT),
]

SOURCES = [
    dict(id="wiki-alexandria", title="Alexandria", author="Wikipedia", url="https://en.wikipedia.org/wiki/Alexandria"),
    dict(id="wiki-ancient-alexandria", title="History of Alexandria", author="Wikipedia", url="https://en.wikipedia.org/wiki/History_of_Alexandria"),
    dict(id="wiki-mareotis", title="Lake Mariout", author="Wikipedia", url="https://en.wikipedia.org/wiki/Lake_Mariout"),
    dict(id="strabo-17", title="Geography, Book 17 (description of Alexandria, 17.1.6–10)", author="Strabo", year="c. 20 CE", url="https://en.wikipedia.org/wiki/Geographica"),
    dict(id="fraser", title="Ptolemaic Alexandria", author="P. M. Fraser", year=1972),
    dict(id="mckenzie", title="The Architecture of Alexandria and Egypt, c. 300 BC to AD 700", author="Judith McKenzie", year=2007),
    dict(id="haas", title="Alexandria in Late Antiquity: Topography and Social Conflict", author="Christopher Haas", year=1997),
    dict(id="goiran", title="Palaeoenvironmental reconstruction of the ancient harbors of Alexandria (Heptastadion)", author="J.-P. Goiran et al.", year=2005),
    dict(id="el-falaki", title="Mémoire sur l'antique Alexandrie", author="Mahmoud Bey el-Falaki", year=1872),
]
