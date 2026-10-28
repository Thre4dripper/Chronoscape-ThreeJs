# Mohenjo-daro: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
# The Citadel mound (the "Mound of the Great Bath") in the west, the Lower Town's grid in the east,
# the Indus flood plain beyond. Positions of excavated areas follow OpenStreetMap and the published plans;
# the river's ancient course is not known and is drawn as a hedged guess.
ALL = ["early-2600", "mature-2500", "late-1900", "kushan-150"]
INDUS = ["early-2600", "mature-2500", "late-1900"]
MATURE_LATE = ["mature-2500", "late-1900"]
EARLY = ["early-2600"]
MATURE = ["mature-2500"]
LATE = ["late-1900"]
KUSHAN = ["kushan-150"]

SOURCES = [
    dict(id="marshall-1931", title="Mohenjo-daro and the Indus Civilization", author="John Marshall (ed.)", year=1931, note="3 vols.; the excavations of 1922–27", url="https://archive.org/details/in.ernet.dli.2015.33006"),
    dict(id="mackay-1938", title="Further Excavations at Mohenjo-daro", author="Ernest J. H. Mackay", year=1938, note="the DK area excavations of 1927–31"),
    dict(id="jansen-1993", title="Mohenjo-daro: Stadt der Brunnen und Kanäle", author="Michael Jansen", year=1993, note="the wells, drains and platforms of the city"),
    dict(id="kenoyer-1998", title="Ancient Cities of the Indus Valley Civilization", author="Jonathan Mark Kenoyer", year=1998),
    dict(id="possehl-2002", title="The Indus Civilization: A Contemporary Perspective", author="Gregory L. Possehl", year=2002),
    dict(id="wheeler-1968", title="The Indus Civilization (3rd ed.)", author="Mortimer Wheeler", year=1968),
    dict(id="wiki-mohenjo-daro", title="Mohenjo-daro", author="Wikipedia", url="https://en.wikipedia.org/wiki/Mohenjo-daro"),
    dict(id="wiki-ivc", title="Indus Valley Civilisation", author="Wikipedia", url="https://en.wikipedia.org/wiki/Indus_Valley_Civilisation"),
    dict(id="wiki-indus", title="Indus River", author="Wikipedia", url="https://en.wikipedia.org/wiki/Indus_River"),
]

CITY = dict(
    name="Mohenjo-daro", subtitle="City of the Indus",
    description="Mohenjo-daro on the Indus flood plain from its founding on brick platforms (c. 2600 BCE) through the mature Harappan city and its decline (c. 1900 BCE) to the Buddhist stupa built on the Citadel mound in Kushan times. The city's ancient name is unknown; Mohenjo-daro, 'mound of the dead', is Sindhi. Positions are projected from real coordinates; the drawing is an illustration, not a survey, and the river's ancient course is a guess.",
    defaultPeriodId="mature-2500",
    world=dict(heightScale=0.9, walls=["#B98763", "#C49470", "#AD7B58", "#C9A07C", "#B58D6A"], roofs=["#BFA684", "#B39A78"]),
    camera=dict(target=(27.3245, 68.1355), distance=34),
)

# north-west corner, south-east corner: the western fields, the Citadel, the Lower Town and the flood plain to the east
FRAME = ((27.3340, 68.1245), (27.3155, 68.1490))

PALETTE = dict(parchment="#E9D5A9", ink="#6C4A30", water="#5F888A", hill="#A28A62", road="#8E6A46")
COMPASS = (27.3322, 68.1265)
CARTOUCHE = (27.3160, 68.1250)

PERIODS = [
    dict(id="early-2600", label="The city on the platforms", year=-2600, startYear=-2650, endYear=-2501,
         summary="Around 2600 BCE (the date is approximate; the earliest levels lie below the water table and have never been reached) people on the Indus plain began a city on a vast scale: massive platforms of mud brick and packed earth lifted the Citadel and the Lower Town above the floods, and streets were laid out north–south and east–west. Fired brick of standard size, a common script and weights followed.",
         population="unknown; growing fast",
         feel="Brick kilns smoking along the river, gangs carrying baskets of earth up the rising platforms, the flood plain green after the summer inundation.",
         style="courtyard",
         houses=dict(title="The first brick houses", text="Rooms of fired and mud brick round small courts, raised on the platforms above flood level; little is known of these earliest houses, which lie deep under later ones. Wells and drains were part of the city from the start, as far as soundings show."),
         outskirts=dict(title="Fields and brick kilns", text="Wheat and barley sown on the silt as the flood went down, cattle and buffalo grazing, and kilns firing bricks by the hundred thousand for the new city.")),
    dict(id="mature-2500", label="Mature Harappan Mohenjo-daro", year=-2500, startYear=-2500, endYear=-2001,
         summary="The largest city of the Indus civilisation, perhaps 200–250 hectares with its buried suburbs. On the Citadel stood the Great Bath, the Great Hall ('granary'), the 'College' and a pillared hall; in the Lower Town, blocks of fired-brick courtyard houses with wells and bathrooms lined straight streets with covered drains. No palace or great temple has been identified, and who ruled is unknown.",
         population="perhaps 40,000 (estimates range from about 20,000 upward)",
         feel="Water drawn from hundreds of wells, the smell of the drains and of wet brick, potters' wheels and bead drills whirring in the courtyards, ox-carts creaking down First Street.",
         style="courtyard",
         houses=dict(title="Courtyard houses of the Lower Town", text="Houses of fired brick round an open court, one or two storeys, flat roofs of timber and earth. They show blank walls to the main streets, doors on the side lanes, and no windows outside; many had their own well, a brick bathing platform and a drain to the street."),
         outskirts=dict(title="Fields on the flood plain", text="Wheat, barley, sesame, peas and cotton grown on the silt left by the river's flood; buffalo and humped cattle grazing the banks, threshing floors and herders' huts.")),
    dict(id="late-1900", label="Late Harappan decline", year=-1900, startYear=-2000, endYear=-1700,
         summary="From about 1900 BCE the city shrank and decayed. Houses were rebuilt crudely in reused brick, large houses were cut up into small rooms, kilns were set up inside the city and drains went unrepaired. The causes are debated: shifts of the river, floods, a weaker monsoon, the end of the Mesopotamian trade. By about 1700 the city was largely deserted.",
         population="falling; unknown",
         feel="Smoke from kilns in the old streets, cracked drains overflowing, families in subdivided rooms of great houses, silt banked against the walls.",
         style="courtyard",
         houses=dict(title="Patched and divided houses", text="Old courtyard houses rebuilt on their stumps with broken and reused brick, partition walls through the courts, floors raised again and again over rubble. Bathrooms and drains were blocked or abandoned; some houses were left empty among the occupied ones."),
         outskirts=dict(title="Thin fields and abandoned blocks", text="Fields and grazing on the plain, and on the edges of the city, empty houses falling to ruin and filling with wind-blown silt.")),
    dict(id="kushan-150", label="The stupa on the mound", year=150, startYear=100, endYear=400,
         summary="Two thousand years after the city died, Buddhist monks built a stupa and a monastery of mud brick on the highest point of the Citadel mound, probably in the 2nd or 3rd century CE when the Kushan kings ruled much of the north-west (dated by Kushan coins found there). The Bronze Age city lay buried under the mounds, unknown.",
         population="a monastery and a small village; perhaps a few hundred people",
         feel="Chanting and the beat of a drum at dawn on the mound, kites over the river, villagers threshing on ground littered with ancient broken brick.",
         style="courtyard",
         houses=dict(title="The village below the monastery", text="A few mud-brick houses round courts at the foot of the mound, built partly with bricks dug from the ruins, home to farmers and to the people who served the monks."),
         outskirts=dict(title="Fields on the old mounds", text="Fields and grazing over the low mounds of the buried Lower Town; ploughs turn up broken brick and potsherds of a city no one remembers.")),
]

# ---------------------------------------------------------------- the Indus (course hedged)
RIVER_INDUS = [(27.3345, 68.1455), (27.3300, 68.1461), (27.3250, 68.1467), (27.3200, 68.1465), (27.3150, 68.1471)]
RIVER_KUSHAN = [(27.3345, 68.1480), (27.3300, 68.1484), (27.3250, 68.1490), (27.3200, 68.1488), (27.3150, 68.1494)]

WATER = [
    dict(id="indus", name="Indus (ancient course?)", path=RIVER_INDUS, width=280, periods=INDUS,
         blurb="The Indus now flows several kilometres east of the ruins, and it has shifted many times. In Harappan times it probably ran east of the city, perhaps closer than today, and flooded the plain every summer; this course is a guess, not a survey."),
    dict(id="indus", name="Indus", path=RIVER_KUSHAN, width=240, periods=KUSHAN,
         blurb="Where the river ran in Kushan times is not known; it is drawn a little further east than in the Bronze Age, its old bed left as marsh."),
]

HILLS = [
    dict(id="citadel-mound", name="Citadel mound (Mound of the Great Bath)", center=(27.3254, 68.1329), radius=150,
         blurb="The western mound, raised on a platform of mud brick and earth faced with fired brick, about 12 m above the plain. The Great Bath, the Great Hall and the 'College' stood on its northern part."),
    dict(id="l-area-mound", name="Southern Citadel (L area)", center=(27.3232, 68.1329), radius=125, label=False,
         blurb="The southern part of the Citadel mound, separated from the north by a lane or gap, with the Pillared Hall and other large buildings."),
    dict(id="dk-mound", name="DK mound", center=(27.3266, 68.1390), radius=210, periods=KUSHAN,
         blurb="The buried north-eastern part of the Lower Town, a low mound of brick rubble and silt in Kushan times."),
    dict(id="hr-mound", name="HR and VS mounds", center=(27.3225, 68.1372), radius=200, periods=KUSHAN,
         blurb="The buried southern part of the Lower Town."),
]

# ---------------------------------------------------------------- streets: straight, at right angles
FIRST_ST = 68.1376
EAST_ST = 27.3262
ROADS = [
    dict(id="first-street", name="First Street (Main Street)", path=[(27.3292, FIRST_ST), (27.3262, FIRST_ST), (27.3243, FIRST_ST), (27.3224, FIRST_ST), (27.3196, FIRST_ST)],
         width=10, style="major", labelled=True, periods=INDUS,
         blurb="The excavators' First Street, the main north–south street of the Lower Town, about 10 m wide and running straight for over 800 m, with covered brick drains along its sides. Its ancient name is unknown."),
    dict(id="east-street", name="East Street", path=[(27.3262, 68.1352), (27.3262, FIRST_ST), (27.3262, 68.1399), (27.3262, 68.1436)],
         width=9, style="major", labelled=True, periods=INDUS,
         blurb="The main east–west street of the Lower Town, crossing First Street at right angles in the DK area. Its drains ran east toward the flood plain."),
    dict(id="second-street", name="Street east of First Street", path=[(27.3290, 68.1399), (27.3262, 68.1399), (27.3243, 68.1399), (27.3200, 68.1399)],
         width=7, style="minor", periods=INDUS,
         blurb="A lesser north–south street parallel to First Street; the grid of the eastern Lower Town is known only in part."),
    dict(id="central-cross", name="Cross street in the DK area", path=[(27.3243, 68.1352), (27.3243, FIRST_ST), (27.3243, 68.1420)],
         width=7, style="minor", periods=INDUS,
         blurb="An east–west street dividing the blocks of the Lower Town; the lines of the lesser streets are partly reconstructed."),
    dict(id="south-cross", name="Cross street between HR and VS", path=[(27.3224, 68.1352), (27.3224, FIRST_ST), (27.3224, 68.1420)],
         width=7, style="minor", periods=INDUS,
         blurb="An east–west street in the south of the Lower Town, between the HR and VS areas."),
    dict(id="deadman-lane", name="Deadman Lane", path=[(27.3236, 68.1356), (27.3236, 68.1372)], width=6, style="minor", periods=INDUS,
         blurb="A narrow lane in the HR area, named by the excavators for skeletons found there; they once fed the story of a massacre at the city's end, now rejected."),
    dict(id="gap-path", name="Path between Citadel and Lower Town", path=[(27.3292, 68.1348), (27.3260, 68.1348), (27.3230, 68.1348), (27.3196, 68.1348)],
         width=8, style="minor", periods=INDUS,
         blurb="The low ground between the Citadel and the Lower Town, perhaps an open space or a channel; its use is unknown."),
    dict(id="citadel-lane", name="Lane across the Citadel", path=[(27.3240, 68.1316), (27.3240, 68.1343)], width=8, style="minor", periods=INDUS,
         blurb="A broad lane or gap dividing the Citadel's northern mound, with the Great Bath, from its southern part, the L area."),
    dict(id="landing-road", name="Road to the river landing", path=[(27.3262, 68.1436), (27.3262, 68.1452)], width=8, style="minor", periods=INDUS,
         blurb="East Street ran on toward the river; where boats landed is not known."),
    dict(id="north-road", name="Road north", path=[(27.3292, FIRST_ST), (27.3315, 68.1374), (27.3342, 68.1370)], width=8, style="major", periods=INDUS,
         blurb="First Street continued north out of the city toward the fields and the villages upriver."),
    dict(id="south-road", name="Road south", path=[(27.3196, FIRST_ST), (27.3175, 68.1378), (27.3153, 68.1380)], width=8, style="major", periods=INDUS,
         blurb="South along the plain, the direction of the river traffic toward the sea, some 300 km away, and the Gulf trade."),
    dict(id="west-track", name="Track to the western fields", path=[(27.3248, 68.1312), (27.3250, 68.1280), (27.3255, 68.1243)], width=6, style="minor", periods=INDUS,
         blurb="A track from the Citadel's west side across the fields."),
    # ---- Kushan
    dict(id="stupa-path", name="Path up the stupa mound", path=[(27.3232, 68.1356), (27.3240, 68.1346), (27.3250, 68.1340)], width=6, style="minor", periods=KUSHAN,
         blurb="From the village at the foot of the mound up to the monastery and the stupa."),
    dict(id="mound-track", name="Track across the mounds", path=[(27.3232, 68.1356), (27.3240, 68.1380), (27.3262, 68.1420), (27.3270, 68.1470)], width=6, style="minor", periods=KUSHAN,
         blurb="A village track across the low mounds of the buried city toward the river."),
    dict(id="kushan-north-road", name="Road north", path=[(27.3232, 68.1356), (27.3290, 68.1360), (27.3342, 68.1362)], width=6, style="minor", periods=KUSHAN,
         blurb="A country road along the plain."),
]

CITADEL = [(27.3268, 68.1314), (27.3268, 68.1344), (27.3222, 68.1344), (27.3222, 68.1314)]

WALLS = [
    dict(id="citadel-wall", name="Citadel platform wall", path=CITADEL, closed=True, periods=INDUS,
         blurb="The Citadel stood on a platform of mud brick and earth with a revetment of brick and, at least in places, solid towers. Whether it was a defence against enemies or against floods, or both, is debated; its full line is only partly excavated."),
]

GATES = []
BRIDGES = []

# ---------------------------------------------------------------- built-up areas
def rect(n, w, s, e):
    return [(n, w), (n, e), (s, e), (s, w)]

BLOCKS = [
    # ---- the Citadel (large buildings; houses fill the gaps between the landmarks)
    dict(name="Northern Citadel", polygon=rect(27.3266, 68.1316, 27.3243, 68.1342), density="dense", periods=MATURE_LATE),
    dict(name="L area", polygon=rect(27.3237, 68.1316, 27.3224, 68.1342), density="dense", periods=MATURE_LATE),
    dict(name="Citadel under construction", polygon=rect(27.3266, 68.1316, 27.3243, 68.1342), density="loose", periods=EARLY),
    # ---- the Lower Town, mature: blocks between First Street, the second street and the cross streets
    dict(name="DK-G (north)", polygon=rect(27.3288, FIRST_ST + 0.00008, 27.3265, 68.1396), density="dense", periods=MATURE),
    dict(name="DK-G (north-east)", polygon=rect(27.3288, 68.1402, 27.3265, 68.1420), density="dense", periods=MATURE),
    dict(name="North-western block", polygon=rect(27.3288, 68.1352, 27.3265, FIRST_ST - 0.00008), density="dense", periods=MATURE),
    dict(name="DK-B and DK-C", polygon=rect(27.3259, FIRST_ST + 0.00008, 27.3246, 68.1396), density="dense", periods=MATURE),
    dict(name="DK area (east)", polygon=rect(27.3259, 68.1402, 27.3246, 68.1420), density="dense", periods=MATURE),
    dict(name="West of First Street", polygon=rect(27.3259, 68.1352, 27.3246, FIRST_ST - 0.00008), density="dense", periods=MATURE),
    dict(name="HR area", polygon=rect(27.3240, 68.1352, 27.3227, FIRST_ST - 0.00008), density="dense", periods=MATURE),
    dict(name="Central blocks", polygon=rect(27.3240, FIRST_ST + 0.00008, 27.3227, 68.1396), density="dense", periods=MATURE),
    dict(name="Eastern blocks", polygon=rect(27.3240, 68.1402, 27.3227, 68.1420), density="dense", periods=MATURE),
    dict(name="VS area", polygon=rect(27.3221, 68.1352, 27.3198, FIRST_ST - 0.00008), density="dense", periods=MATURE),
    dict(name="Southern blocks", polygon=rect(27.3221, FIRST_ST + 0.00008, 27.3198, 68.1396), density="dense", periods=MATURE),
    dict(name="Moneer area", polygon=rect(27.3221, 68.1402, 27.3198, 68.1420), density="dense", periods=MATURE),
    # ---- suburbs, buried under the alluvium (extent hedged)
    dict(name="Eastern suburbs (buried)", polygon=rect(27.3288, 68.1424, 27.3198, 68.1436), density="loose", periods=MATURE),
    dict(name="Southern suburbs (buried)", polygon=rect(27.3192, 68.1352, 27.3178, 68.1436), density="loose", periods=MATURE),
    dict(name="Northern suburbs (buried)", polygon=rect(27.3306, 68.1352, 27.3295, 68.1420), density="loose", periods=MATURE),
    # ---- the early city: the central Lower Town on its platforms
    dict(name="DK area (early)", polygon=rect(27.3285, FIRST_ST + 0.00008, 27.3265, 68.1396), density="dense", periods=EARLY),
    dict(name="West of First Street (early)", polygon=rect(27.3259, 68.1352, 27.3246, FIRST_ST - 0.00008), density="dense", periods=EARLY),
    dict(name="DK-B and DK-C (early)", polygon=rect(27.3259, FIRST_ST + 0.00008, 27.3246, 68.1396), density="dense", periods=EARLY),
    dict(name="HR area (early)", polygon=rect(27.3240, 68.1352, 27.3227, FIRST_ST - 0.00008), density="dense", periods=EARLY),
    dict(name="Central blocks (early)", polygon=rect(27.3240, FIRST_ST + 0.00008, 27.3227, 68.1396), density="loose", periods=EARLY),
    dict(name="VS area (early)", polygon=rect(27.3221, 68.1352, 27.3205, FIRST_ST - 0.00008), density="loose", periods=EARLY),
    dict(name="Eastern edge (early)", polygon=rect(27.3259, 68.1402, 27.3227, 68.1416), density="loose", periods=EARLY),
    # ---- the late city: still dense in parts, thinning at the edges
    dict(name="DK-G (late)", polygon=rect(27.3288, FIRST_ST + 0.00008, 27.3265, 68.1396), density="dense", periods=LATE),
    dict(name="DK-G east (late)", polygon=rect(27.3288, 68.1402, 27.3265, 68.1420), density="loose", periods=LATE),
    dict(name="North-western block (late)", polygon=rect(27.3288, 68.1352, 27.3265, FIRST_ST - 0.00008), density="loose", periods=LATE),
    dict(name="DK-B and DK-C (late)", polygon=rect(27.3259, FIRST_ST + 0.00008, 27.3246, 68.1396), density="dense", periods=LATE),
    dict(name="DK area east (late)", polygon=rect(27.3259, 68.1402, 27.3246, 68.1420), density="loose", periods=LATE),
    dict(name="West of First Street (late)", polygon=rect(27.3259, 68.1352, 27.3246, FIRST_ST - 0.00008), density="dense", periods=LATE),
    dict(name="HR area (late)", polygon=rect(27.3240, 68.1352, 27.3227, FIRST_ST - 0.00008), density="dense", periods=LATE),
    dict(name="Central blocks (late)", polygon=rect(27.3240, FIRST_ST + 0.00008, 27.3227, 68.1396), density="dense", periods=LATE),
    dict(name="Eastern blocks (late)", polygon=rect(27.3240, 68.1402, 27.3227, 68.1420), density="loose", periods=LATE),
    dict(name="VS area (late)", polygon=rect(27.3221, 68.1352, 27.3198, FIRST_ST - 0.00008), density="dense", periods=LATE),
    dict(name="Southern blocks (late)", polygon=rect(27.3221, FIRST_ST + 0.00008, 27.3198, 68.1396), density="loose", periods=LATE),
    dict(name="Moneer area (late)", polygon=rect(27.3221, 68.1402, 27.3198, 68.1420), density="loose", periods=LATE),
    # ---- Kushan: a village at the foot of the stupa mound
    dict(name="Village below the monastery", polygon=rect(27.3238, 68.1347, 27.3222, 68.1362), density="loose", periods=KUSHAN),
    dict(name="Monastery dependencies", polygon=rect(27.3266, 68.1316, 27.3258, 68.1328), density="loose", periods=KUSHAN),
]

GARDENS = [
    dict(name="Wheat and barley fields (west)", polygon=[(27.3335, 68.1252), (27.3335, 68.1305), (27.3275, 68.1305), (27.3275, 68.1252)], kind="orchard"),
    dict(name="Fields on the flood plain (south-west)", polygon=[(27.3215, 68.1252), (27.3215, 68.1305), (27.3160, 68.1305), (27.3160, 68.1252)], kind="orchard"),
    dict(name="Cotton and sesame fields (north)", polygon=[(27.3335, 68.1310), (27.3335, 68.1365), (27.3312, 68.1365), (27.3312, 68.1310)], kind="orchard"),
    dict(name="Fields south of the city", polygon=[(27.3172, 68.1310), (27.3172, 68.1370), (27.3160, 68.1370), (27.3160, 68.1310)], kind="orchard"),
    dict(name="Fields on the old mounds", polygon=[(27.3288, 68.1365), (27.3288, 68.1430), (27.3200, 68.1430), (27.3200, 68.1365)], kind="orchard", periods=KUSHAN),
    dict(name="Fields north of the mound", polygon=[(27.3305, 68.1310), (27.3305, 68.1355), (27.3275, 68.1355), (27.3275, 68.1310)], kind="orchard", periods=KUSHAN),
]

MARSH = [
    dict(name="Flood basin (north-east)", polygon=[(27.3338, 68.1400), (27.3338, 68.1446), (27.3310, 68.1448), (27.3308, 68.1410)]),
    dict(name="Flood basin (south-east)", polygon=[(27.3188, 68.1440), (27.3188, 68.1452), (27.3158, 68.1456), (27.3158, 68.1400), (27.3170, 68.1400)]),
    dict(name="Back-swamp west of the Citadel", polygon=[(27.3268, 68.1258), (27.3268, 68.1300), (27.3222, 68.1300), (27.3222, 68.1258)]),
    dict(name="The river's old bed", polygon=[(27.3330, 68.1448), (27.3330, 68.1468), (27.3170, 68.1470), (27.3170, 68.1450)], periods=KUSHAN),
]

DISTRICTS = [
    dict(id="citadel", name="The Citadel (SD area)", polygon=CITADEL, periods=INDUS,
         description="The raised western mound with the city's great public buildings: the Great Bath, the Great Hall, the 'College' and, in the southern L area, the Pillared Hall. Who used them, priests, rulers or councils, is unknown."),
    dict(id="dk-area", name="DK area", polygon=rect(27.3290, FIRST_ST - 0.0001, 27.3244, 68.1422), periods=INDUS,
         description="The north-eastern Lower Town, dug by K. N. Dikshit and Ernest Mackay in the 1920s: First Street, East Street, dense blocks of houses, wells and workshops. The 'Priest-King' was found here."),
    dict(id="hr-area", name="HR area", polygon=rect(27.3242, 68.1350, 27.3226, FIRST_ST - 0.00005), periods=INDUS,
         description="Named after H. Hargreaves, who excavated it: large houses, the narrow Deadman Lane and the find-spot of the bronze 'Dancing Girl'."),
    dict(id="vs-area", name="VS area", polygon=rect(27.3223, 68.1350, 27.3196, FIRST_ST - 0.00005), periods=INDUS,
         description="Named after M. S. Vats: houses, workshops and many wells in the south-west of the Lower Town."),
    dict(id="moneer-area", name="Moneer area", polygon=rect(27.3223, 68.1398, 27.3196, 68.1422), periods=INDUS,
         description="The south-eastern Lower Town, where later surveys found much evidence of crafts: shell working, beads, pottery and stone tools."),
]

LABELS = [
    dict(text="Indus", position=(27.3290, 68.1463), size="lg", rotation=-84, periods=INDUS),
    dict(text="Indus", position=(27.3215, 68.1485), size="md", rotation=-84, periods=KUSHAN),
    dict(text="Citadel", position=(27.3272, 68.1306), size="md", periods=INDUS),
    dict(text="Lower Town", position=(27.3300, 68.1388), size="lg", periods=MATURE_LATE),
    dict(text="Lower Town", position=(27.3293, 68.1388), size="md", periods=EARLY),
    dict(text="DK", position=(27.3276, 68.1410), size="sm", periods=INDUS),
    dict(text="HR", position=(27.3233, 68.1358), size="sm", periods=INDUS),
    dict(text="VS", position=(27.3204, 68.1356), size="sm", periods=INDUS),
    dict(text="Moneer", position=(27.3203, 68.1412), size="sm", periods=INDUS),
    dict(text="Flood plain", position=(27.3170, 68.1430), size="sm"),
    dict(text="Stupa mound", position=(27.3273, 68.1330), size="md", periods=KUSHAN),
    dict(text="Mounds of the buried city", position=(27.3245, 68.1398), size="sm", periods=KUSHAN),
    dict(text="to the sea", position=(27.3163, 68.1388), size="sm", rotation=-85, periods=INDUS),
]
