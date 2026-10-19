# Tenochtitlan / Mexico City: frame, eras and the geography of the lake city.
# The lake is drawn as one wide winding WATER path per era (concentric loops round the land, generated
# from LAND below), so that it is a single stroke that stops at the shore.

F, I, M, C = "founding-1350", "itzcoatl-1440", "moctezuma-1519", "colonial-1620"
ALL = [F, I, M, C]
AZTEC = [F, I, M]

CITY = dict(
    name="Tenochtitlan", subtitle="The City in the Lake",
    description="The Mexica island city of Tenochtitlan and its twin Tlatelolco in Lake Texcoco, from the first reed huts of the 1320s to Spanish Mexico City on the eve of the great flood of 1629: the causeways, the dike, the aqueduct from Chapultepec and the canals. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId=M,
    world=dict(heightScale=1.0, walls=["#EFE8D8", "#E6D8BC", "#D9C29E", "#B9785A"], roofs=["#CDBB98", "#BFA982"]),
    camera=dict(target=(19.4385, -99.1340), distance=40),
)
FRAME = ((19.467, -99.163), (19.404, -99.092))

PALETTE = dict(parchment="#E6D3AA", ink="#6F4D34", water="#5F8A88", hill="#777D5A", road="#8A6A4A")
COMPASS = (19.4610, -99.1060)
CARTOUCHE = (19.4085, -99.1610)

SOURCES = [
    dict(id="gonzalez-aparicio", title="Plano reconstructivo de la región de Tenochtitlan", author="Luis González Aparicio", year=1973, note="the standard reconstruction map of the island, causeways and lake shore"),
    dict(id="calnek", title="The Internal Structure of Tenochtitlan", author="Edward E. Calnek", year=1976, note="in E. Wolf (ed.), The Valley of Mexico"),
    dict(id="mundy", title="The Death of Aztec Tenochtitlan, the Life of Mexico City", author="Barbara E. Mundy", year=2015),
    dict(id="candiani", title="Dreaming of Dry Land: Environmental Transformation in Colonial Mexico City", author="Vera S. Candiani", year=2014),
    dict(id="smith-aztecs", title="The Aztecs", author="Michael E. Smith", year=2012, note="3rd edition"),
    dict(id="trasmonte-1628", title="Forma y levantado de la ciudad de México", author="Juan Gómez de Trasmonte", year=1628, note="bird's-eye view of the city just before the flood of 1629"),
    dict(id="cortes-letters", title="Letters from Mexico (Second Letter to Charles V, 30 October 1520)", author="Hernán Cortés", year=1520, url="https://en.wikipedia.org/wiki/Hern%C3%A1n_Cort%C3%A9s"),
    dict(id="wiki-tenochtitlan", title="Tenochtitlan", author="Wikipedia", url="https://en.wikipedia.org/wiki/Tenochtitlan"),
    dict(id="wiki-lake-texcoco", title="Lake Texcoco", author="Wikipedia", url="https://en.wikipedia.org/wiki/Lake_Texcoco"),
    dict(id="wiki-chinampa", title="Chinampa", author="Wikipedia", url="https://en.wikipedia.org/wiki/Chinampa"),
    dict(id="wiki-calpolli", title="Calpolli", author="Wikipedia", url="https://en.wikipedia.org/wiki/Calpolli"),
    dict(id="wiki-desague", title="Desagüe", author="Wikipedia", url="https://en.wikipedia.org/wiki/Desag%C3%BCe"),
    dict(id="wiki-calzada-tlalpan", title="Calzada de Tlalpan", author="Wikipedia", url="https://en.wikipedia.org/wiki/Calzada_de_Tlalpan"),
]

PERIODS = [
    dict(id=F, label="Two Island Towns", year=1350, startYear=1325, endYear=1427,
         summary="The Mexica, latecomers to the valley, settle on a marshy islet in Lake Texcoco around 1325; a breakaway group founds Tlatelolco on the next islet north around 1337. Both are tributaries of the Tepanecs of Azcapotzalco. Houses of reed and mud on reclaimed beds, a small earthen temple to Huitzilopochtli and Tlaloc, fishing, fowling and trading in reeds.",
         population="a few thousand; perhaps 10,000–20,000 by 1400",
         feel="Wind in the tule reeds, smoke of cooking fires over the water, the splash of poles as canoes push through the shallows.",
         style="mesoamerican",
         houses=dict(title="Reed and mud houses", text="Single rooms of wattle and daub or adobe on plots raised from the marsh, thatched with tule reed, grouped round a yard with a granary and a sweat bath. Households of one calpolli (clan ward) lived together round their own small temple."),
         outskirts=dict(title="New chinampas", text="Beds of mud and reed matting staked out into the shallows, the first chinampas, each with a hut, a few willows and maize, beans and chillies growing above the waterline.")),
    dict(id=I, label="The Triple Alliance", year=1440, startYear=1428, endYear=1485,
         summary="In 1428 Itzcoatl, with Texcoco and Tlacopan, overthrew Azcapotzalco. Tenochtitlan became an imperial capital: Moctezuma I (1440–69) enlarged the Templo Mayor, built the dike of Nezahualcoyotl after the flood of 1449 and brought fresh water from Chapultepec. Stone and lime replace mud in temples and palaces; in 1473 Tenochtitlan conquered Tlatelolco.",
         population="perhaps 50,000–80,000 with Tlatelolco",
         feel="Lime kilns smoking, gangs of tribute labourers hauling stone and stakes, drums from the rising temple.",
         style="mesoamerican",
         houses=dict(title="Calpolli patio houses", text="Adobe houses with whitewashed lime plaster and flat roofs, several rooms round a shared patio, one patio per extended family. Each plot fronted a street on one side and a canal on the other, with a canoe tied at the back door."),
         outskirts=dict(title="Chinampa homesteads", text="Long narrow garden beds between canals, edged with willows, each farmed by a household living in a small house at its end. The island grew outward bed by bed.")),
    dict(id=M, label="The Island Capital", year=1519, startYear=1486, endYear=1521,
         summary="The capital of an empire of tribute from coast to coast, as Cortés saw it on 8 November 1519: about 13 km² of island laid out on a grid of streets and canals, three causeways to the mainland, the walled Sacred Precinct with the twin-temple pyramid at its heart, palaces of stone and lime, and at Tlatelolco a market of 20,000 to 25,000 people a day.",
         population="about 200,000 with Tlatelolco (estimates range from 60,000 to 300,000)",
         feel="Thousands of canoes, conch trumpets at dawn from the temple tops, copal smoke, the market's roar heard a league away.",
         style="mesoamerican",
         houses=dict(title="Calpolli patio houses", text="Whitewashed one-storey houses of adobe on stone footings with flat roofs, rooms round a patio, each block reached by a street on one side and a canal on the other. Lords' houses had two storeys, gardens and painted walls."),
         outskirts=dict(title="Chinampa homesteads", text="Long beds of rich lake mud between canals, edged with willows, growing maize, beans, chillies, amaranth and flowers for the city, with the farming family's house and granary at the end of each bed.")),
    dict(id=C, label="Viceregal Mexico", year=1620, startYear=1522, endYear=1629,
         summary="Cortés rebuilt the city on the ruins from 1522: a Spanish grid (the traza) round the Plaza Mayor for Spaniards, with Indian barrios round it, San Juan Tenochtitlan and Santiago Tlatelolco. Churches, convents and palaces of grey stone and red tezontle; canals filled in one by one, the lake shrinking, and repeated floods that culminate in the great flood of 1629.",
         population="perhaps 80,000–100,000 (estimates vary)",
         feel="Church bells instead of drums, carriages and mule trains on the causeways, canoes of Indian vendors still crowding the Acequia Real.",
         style="early-modern",
         houses=dict(title="Spanish casas with patios", text="Houses of stone, tezontle and adobe of one or two storeys, flat-roofed with spouts, built round one or two patios with shops (accesorias) to the street, the richer ones with carved stone portals and balconies."),
         outskirts=dict(title="Indian barrios and chinampas", text="The barrios of San Juan and Santiago Tlatelolco: adobe houses round yards along irregular lanes and canals, chapels for each old calpolli, and chinampas still farmed at the edges.")),
]

# ---------------------------------------------------------------- land (used to generate the lake)
# 1350: the outline of the two islets with the reed beds between them; 1440, 1519: the island(s); 1620: the city and the
# drained west and south, with Lake Texcoco to the east.
HULL_1350 = [(19.4570, -99.1435), (19.4572, -99.1335), (19.4525, -99.1298), (19.4465, -99.1300), (19.4420, -99.1278), (19.4385, -99.1238),
             (19.4335, -99.1228), (19.4288, -99.1252), (19.4268, -99.1312), (19.4280, -99.1385), (19.4325, -99.1420), (19.4400, -99.1418),
             (19.4462, -99.1440), (19.4500, -99.1442)]
TEN_1350 = [(19.4412, -99.1385), (19.4410, -99.1300), (19.4380, -99.1252), (19.4335, -99.1240), (19.4295, -99.1262), (19.4278, -99.1315),
            (19.4290, -99.1378), (19.4330, -99.1408), (19.4390, -99.1405)]
TLAT_1350 = [(19.4562, -99.1425), (19.4562, -99.1342), (19.4525, -99.1310), (19.4478, -99.1318), (19.4465, -99.1372), (19.4480, -99.1425)]
LAND_1440 = [(19.4585, -99.1450), (19.4600, -99.1380), (19.4590, -99.1310), (19.4545, -99.1280), (19.4470, -99.1260), (19.4400, -99.1235),
             (19.4330, -99.1225), (19.4265, -99.1245), (19.4225, -99.1300), (19.4220, -99.1380), (19.4255, -99.1450), (19.4320, -99.1490),
             (19.4400, -99.1495), (19.4470, -99.1485), (19.4535, -99.1475)]
LAND_1519 = [(19.4610, -99.1475), (19.4630, -99.1400), (19.4628, -99.1320), (19.4595, -99.1265), (19.4525, -99.1235), (19.4450, -99.1205),
             (19.4380, -99.1180), (19.4300, -99.1172), (19.4230, -99.1190), (19.4180, -99.1240), (19.4152, -99.1320), (19.4160, -99.1410),
             (19.4200, -99.1480), (19.4270, -99.1525), (19.4350, -99.1538), (19.4420, -99.1528), (19.4490, -99.1520), (19.4560, -99.1510)]
LAND_1620 = [(19.4800, -99.1800), (19.4800, -99.1255), (19.4660, -99.1222), (19.4560, -99.1200), (19.4450, -99.1178), (19.4370, -99.1162),
             (19.4290, -99.1158), (19.4210, -99.1172), (19.4120, -99.1195), (19.3900, -99.1225), (19.3900, -99.1800)]
LAND = {F: HULL_1350, I: LAND_1440, M: LAND_1519, C: LAND_1620}

LAKE_NAME = {F: "Lake Texcoco", I: "Lake Texcoco", M: "Lake Texcoco", C: "Lake Texcoco"}
LAKE_BLURB = {
    F: "A shallow, partly saline lake about 2,240 m above sea level, rich in fish, waterfowl, reeds and edible algae. The Mexica islets were barely above its surface.",
    I: "The western bay round the island, called the Lake of Mexico, was kept fresher by springs and, after 1449, by the dike that held back the salt water of eastern Texcoco.",
    M: "Crossed by tens of thousands of canoes carrying people, tribute, food, stone and water. The lake rose in the rainy season and the city lived with the risk of floods.",
    C: "Shrinking: the western lake was silting into marsh and fields, but the eastern lake still rose against the city in wet years, held back by the dike of San Lázaro.",
}

# --- LAKE (generated by lakegen.py) ---
LAKE = [
    dict(id="lake-founding-1350", name=LAKE_NAME["founding-1350"], width=1000, periods=["founding-1350"], blurb=LAKE_BLURB["founding-1350"],
         path=[(19.45742, -99.14824), (19.45888, -99.14783), (19.46012, -99.14693), (19.46102, -99.14565), (19.46147, -99.14413), (19.46169, -99.1331), (19.46114, -99.13118), (19.45989, -99.12968), (19.45519, -99.12598), (19.45385, -99.12526), (19.45236, -99.12504), (19.44742, -99.1252), (19.4447, -99.12387), (19.44147, -99.12021), (19.44025, -99.11941), (19.43934, -99.11912), (19.43386, -99.11805), (19.43244, -99.11817), (19.42684, -99.12091), (19.42599, -99.12148), (19.42528, -99.12223), (19.42455, -99.12362), (19.42255, -99.12962), (19.4223, -99.13141), (19.42367, -99.13982), (19.4243, -99.14122), (19.42533, -99.14234), (19.43024, -99.14612), (19.43163, -99.14667), (19.43932, -99.14658), (19.44477, -99.14852), (19.44598, -99.14876), (19.45042, -99.14894), (19.45742, -99.14824), (19.45822, -99.15716), (19.45966, -99.15693), (19.46241, -99.15597), (19.4637, -99.15525), (19.466, -99.15339), (19.46699, -99.15226), (19.46858, -99.1497), (19.46959, -99.14683), (19.46998, -99.14379), (19.47018, -99.13379), (19.46994, -99.1309), (19.46961, -99.1295), (19.46854, -99.12683), (19.46781, -99.1256), (19.46601, -99.12343), (19.46025, -99.1188), (19.45775, -99.11725), (19.45639, -99.11671), (19.45354, -99.11613), (19.44916, -99.11619), (19.44978, -99.11649), (19.44704, -99.11347), (19.44479, -99.1118), (19.44225, -99.11067), (19.43591, -99.10932), (19.43455, -99.10913), (19.4318, -99.1092), (19.42912, -99.10989), (19.42189, -99.11359), (19.41962, -99.1155), (19.41782, -99.11789), (19.41656, -99.12064), (19.41411, -99.12833), (19.41383, -99.13181), (19.41553, -99.14231), (19.41661, -99.14507), (19.41823, -99.14752), (19.41921, -99.1486), (19.426, -99.15387), (19.42861, -99.15509), (19.42999, -99.15546), (19.43283, -99.15571), (19.43804, -99.15557), (19.44207, -99.157), (19.44379, -99.15748), (19.44555, -99.1577), (19.45122, -99.15786), (19.45822, -99.15716), (19.45902, -99.16607), (19.46139, -99.16569), (19.46371, -99.16503), (19.46595, -99.16411), (19.46807, -99.16292), (19.47005, -99.16149), (19.47187, -99.15984), (19.47259, -99.15798), (19.47259, -99.11857), (19.47176, -99.11685), (19.46531, -99.11162), (19.46331, -99.11022), (19.46117, -99.10906), (19.45893, -99.10817), (19.4566, -99.10755), (19.45422, -99.1072), (19.4509, -99.10717), (19.45486, -99.10911), (19.45262, -99.10673), (19.45082, -99.10524), (19.44889, -99.10397), (19.44684, -99.10291), (19.4447, -99.1021), (19.44249, -99.10152), (19.43749, -99.10052), (19.43523, -99.1002), (19.43296, -99.10014), (19.43069, -99.10032), (19.42845, -99.10077), (19.42627, -99.10146), (19.42417, -99.10239), (19.41947, -99.10479), (19.41737, -99.10601), (19.41542, -99.10748), (19.41363, -99.10917), (19.41204, -99.11105), (19.41065, -99.11312), (19.40949, -99.11533), (19.40657, -99.12367), (19.40582, -99.12645), (19.40542, -99.12931), (19.40537, -99.1322), (19.40567, -99.13508), (19.40739, -99.14479), (19.40816, -99.14713), (19.40917, -99.14936), (19.4104, -99.15147), (19.41184, -99.15342), (19.41348, -99.15519), (19.41529, -99.15676), (19.42176, -99.16162), (19.42386, -99.16275), (19.42607, -99.16363), (19.42835, -99.16424), (19.43068, -99.16459), (19.43676, -99.16457), (19.44222, -99.16628), (19.44513, -99.16664), (19.44893, -99.16684), (19.45202, -99.16677), (19.45902, -99.16607), (19.45982, -99.16891), (19.47244, -99.16891), (19.47259, -99.1686), (19.47259, -99.10814), (19.47037, -99.10444), (19.46758, -99.10248), (19.4646, -99.10087), (19.46147, -99.09963), (19.45822, -99.09876), (19.4549, -99.09828), (19.45156, -99.09819), (19.45264, -99.09815), (19.45994, -99.10173), (19.46047, -99.10233), (19.45819, -99.09999), (19.45569, -99.09791), (19.453, -99.09613), (19.45014, -99.09466), (19.44715, -99.09352), (19.44406, -99.09273), (19.43592, -99.09128), (19.43274, -99.09118), (19.42958, -99.09145), (19.42645, -99.09206), (19.42341, -99.09303), (19.41578, -99.09672), (19.41286, -99.09843), (19.41014, -99.10048), (19.40764, -99.10283), (19.40542, -99.10546), (19.40348, -99.10834), (19.40186, -99.11143), (19.40058, -99.11469), (19.39858, -99.12069), (19.39841, -99.12458), (19.39852, -99.14391), (19.39925, -99.14728), (19.40033, -99.15054), (19.40173, -99.15365), (19.40345, -99.15659), (19.40546, -99.15931), (19.40774, -99.16178), (19.41026, -99.16397), (19.41476, -99.16747), (19.41752, -99.16891), (19.45982, -99.16891), (19.46062, -99.16891), (19.47259, -99.16891), (19.47259, -99.09726), (19.47185, -99.09475), (19.46803, -99.09269), (19.46401, -99.09108), (19.45984, -99.08997), (19.45558, -99.08935), (19.45129, -99.08924), (19.45437, -99.08914), (19.46502, -99.09434), (19.46669, -99.09625), (19.46377, -99.09324), (19.46056, -99.09058), (19.4571, -99.0883), (19.45343, -99.08641), (19.4496, -99.08609), (19.42055, -99.08609), (19.4168, -99.08626), (19.4121, -99.08866), (19.40835, -99.09086), (19.40485, -99.09348), (19.40166, -99.0965), (19.3988, -99.09988), (19.39841, -99.10357), (19.39841, -99.16171), (19.39908, -99.1652), (19.40201, -99.16837), (19.40524, -99.16891), (19.46062, -99.16891), (19.46141, -99.16891), (19.47259, -99.16891), (19.47259, -99.08702), (19.47145, -99.08609), (19.45102, -99.08609), (19.45611, -99.08609), (19.4701, -99.08696), (19.47259, -99.09017), (19.46934, -99.0865), (19.46542, -99.08609), (19.40383, -99.08609), (19.39957, -99.08648), (19.39841, -99.09017), (19.39841, -99.16891), (19.46141, -99.16891)]),
    dict(id="lake-itzcoatl-1440", name=LAKE_NAME["itzcoatl-1440"], width=1000, periods=["itzcoatl-1440"], blurb=LAKE_BLURB["itzcoatl-1440"],
         path=[(19.46043, -99.14931), (19.46129, -99.14874), (19.46202, -99.14798), (19.46275, -99.14657), (19.4644, -99.13905), (19.46446, -99.13729), (19.46346, -99.13029), (19.46301, -99.12884), (19.46216, -99.1276), (19.45649, -99.12373), (19.44827, -99.12143), (19.4406, -99.11878), (19.4336, -99.11778), (19.43235, -99.11779), (19.42524, -99.11993), (19.42396, -99.12057), (19.42293, -99.1216), (19.41838, -99.12806), (19.418, -99.12969), (19.4175, -99.13769), (19.41755, -99.13873), (19.41802, -99.14023), (19.42152, -99.14723), (19.42243, -99.14848), (19.4302, -99.15337), (19.43173, -99.15375), (19.4406, -99.15422), (19.4548, -99.15206), (19.46043, -99.14931), (19.46405, -99.1574), (19.46534, -99.15666), (19.46764, -99.15474), (19.46863, -99.15358), (19.47019, -99.15096), (19.47116, -99.14803), (19.47259, -99.14103), (19.47259, -99.13595), (19.47155, -99.12751), (19.47056, -99.12477), (19.46986, -99.12349), (19.4681, -99.12122), (19.46706, -99.12025), (19.46142, -99.1164), (19.45898, -99.11513), (19.45067, -99.11283), (19.44415, -99.1105), (19.44174, -99.10991), (19.43474, -99.10891), (19.43294, -99.10878), (19.43114, -99.10892), (19.42287, -99.11133), (19.42158, -99.11181), (19.41918, -99.11317), (19.41809, -99.11405), (19.41621, -99.11614), (19.41135, -99.12298), (19.41011, -99.12592), (19.40955, -99.1291), (19.40903, -99.13861), (19.40948, -99.1416), (19.41052, -99.14441), (19.41477, -99.15272), (19.41665, -99.15503), (19.41897, -99.15685), (19.42547, -99.16085), (19.42825, -99.16213), (19.43123, -99.16269), (19.43923, -99.16319), (19.44174, -99.16309), (19.45537, -99.16107), (19.45725, -99.16063), (19.45905, -99.1599), (19.46405, -99.1574), (19.46767, -99.16549), (19.46981, -99.16427), (19.47179, -99.16279), (19.47259, -99.16109), (19.47259, -99.11484), (19.47232, -99.11323), (19.46594, -99.10882), (19.46398, -99.10766), (19.4619, -99.10672), (19.45307, -99.10424), (19.44687, -99.10202), (19.44287, -99.10103), (19.43587, -99.10003), (19.4329, -99.09983), (19.42992, -99.10006), (19.427, -99.10073), (19.4205, -99.10273), (19.41837, -99.10352), (19.41633, -99.10454), (19.4144, -99.10578), (19.4126, -99.10723), (19.41096, -99.10887), (19.40549, -99.11618), (19.40407, -99.11839), (19.40291, -99.12076), (19.40202, -99.12326), (19.40141, -99.12586), (19.4011, -99.12851), (19.40057, -99.13901), (19.40081, -99.1415), (19.4013, -99.14394), (19.40205, -99.14632), (19.40303, -99.14859), (19.40777, -99.15776), (19.40922, -99.15976), (19.41087, -99.16159), (19.41271, -99.1632), (19.41471, -99.16459), (19.42121, -99.16859), (19.42345, -99.16891), (19.4597, -99.16891), (19.46267, -99.16799), (19.46767, -99.16549), (19.4713, -99.16891), (19.47259, -99.16891), (19.47259, -99.10425), (19.47046, -99.10125), (19.46772, -99.09963), (19.46483, -99.09832), (19.46182, -99.09733), (19.45546, -99.09564), (19.44958, -99.09354), (19.44401, -99.09216), (19.43701, -99.09116), (19.43285, -99.09087), (19.4287, -99.0912), (19.42464, -99.09213), (19.41814, -99.09413), (19.41516, -99.09523), (19.41231, -99.09666), (19.40962, -99.09839), (19.40711, -99.10041), (19.40482, -99.1027), (19.40278, -99.10523), (19.39878, -99.11073), (19.39841, -99.11381), (19.39841, -99.15278), (19.39904, -99.15978), (19.40076, -99.1628), (19.40279, -99.16559), (19.4051, -99.16814), (19.40766, -99.16891), (19.4713, -99.16891), (19.47259, -99.16891), (19.47259, -99.09368), (19.47146, -99.09159), (19.46775, -99.08991), (19.46389, -99.08865), (19.45786, -99.08704), (19.45229, -99.08609), (19.41577, -99.08609), (19.41195, -99.08695), (19.40829, -99.08877), (19.40484, -99.09099), (19.40163, -99.09359), (19.39869, -99.09652), (19.39841, -99.09977), (19.39841, -99.16891), (19.47259, -99.16891)]),
    dict(id="lake-moctezuma-1519", name=LAKE_NAME["moctezuma-1519"], width=1000, periods=["moctezuma-1519"], blurb=LAKE_BLURB["moctezuma-1519"],
         path=[(19.46349, -99.15147), (19.4643, -99.15074), (19.46516, -99.14933), (19.46734, -99.14129), (19.4675, -99.13987), (19.4673, -99.13187), (19.46703, -99.13037), (19.46661, -99.12945), (19.46298, -99.12347), (19.4617, -99.12234), (19.45419, -99.11909), (19.4466, -99.11605), (19.43944, -99.11349), (19.43842, -99.11326), (19.42992, -99.11244), (19.42193, -99.11437), (19.42085, -99.11482), (19.4199, -99.11554), (19.4149, -99.12054), (19.41398, -99.12185), (19.41073, -99.13138), (19.41151, -99.14145), (19.41172, -99.14249), (19.41614, -99.15046), (19.41681, -99.15136), (19.41766, -99.15207), (19.42466, -99.15657), (19.42632, -99.15721), (19.43496, -99.15856), (19.4496, -99.15672), (19.45759, -99.15546), (19.46349, -99.15147), (19.46817, -99.15894), (19.47051, -99.15684), (19.47149, -99.15558), (19.47232, -99.15422), (19.47259, -99.15276), (19.47259, -99.12465), (19.47046, -99.11915), (19.46842, -99.11653), (19.46718, -99.11544), (19.46438, -99.11379), (19.45738, -99.11079), (19.44959, -99.10767), (19.44215, -99.105), (19.43922, -99.10434), (19.42978, -99.10348), (19.42693, -99.10387), (19.41993, -99.10567), (19.41833, -99.1062), (19.4168, -99.10695), (19.41537, -99.1079), (19.41408, -99.10904), (19.40908, -99.11404), (19.40717, -99.11644), (19.40583, -99.11924), (19.40303, -99.12724), (19.40233, -99.13022), (19.40228, -99.13328), (19.40308, -99.14228), (19.40367, -99.1453), (19.40421, -99.14673), (19.40889, -99.15509), (19.41081, -99.15768), (19.41326, -99.15972), (19.42026, -99.16422), (19.42177, -99.16505), (19.42337, -99.16567), (19.43303, -99.16736), (19.43488, -99.16752), (19.45074, -99.16559), (19.45917, -99.1643), (19.4619, -99.16322), (19.46817, -99.15894), (19.47259, -99.1664), (19.47259, -99.11003), (19.4722, -99.10823), (19.46996, -99.10671), (19.46756, -99.10549), (19.46056, -99.10249), (19.45259, -99.0993), (19.44487, -99.09652), (19.44247, -99.09583), (19.44002, -99.09543), (19.42964, -99.09453), (19.42727, -99.09471), (19.42493, -99.09517), (19.41793, -99.09697), (19.41527, -99.09785), (19.41275, -99.09908), (19.4104, -99.10065), (19.40826, -99.10253), (19.40326, -99.10753), (19.40157, -99.10942), (19.4001, -99.11151), (19.39887, -99.11375), (19.39841, -99.11613), (19.39841, -99.15272), (19.40164, -99.15972), (19.4031, -99.16196), (19.40481, -99.16401), (19.40673, -99.16582), (19.40885, -99.16737), (19.41585, -99.16891), (19.46784, -99.16891), (19.47259, -99.1664), (19.47259, -99.16891), (19.47259, -99.09889), (19.47074, -99.09719), (19.45559, -99.09092), (19.44758, -99.08804), (19.44424, -99.08707), (19.44082, -99.08651), (19.43282, -99.08609), (19.42619, -99.08609), (19.42293, -99.08647), (19.41593, -99.08827), (19.41222, -99.0895), (19.4087, -99.09122), (19.40542, -99.09341), (19.40243, -99.09603), (19.39841, -99.10103), (19.39841, -99.16748), (19.39881, -99.16891), (19.47259, -99.16891), (19.47259, -99.16891), (19.47259, -99.08889), (19.46693, -99.08609), (19.40044, -99.08616), (19.39841, -99.08952), (19.39841, -99.16891), (19.47259, -99.16891)]),
    dict(id="lake-colonial-1620", name=LAKE_NAME["colonial-1620"], width=1000, periods=["colonial-1620"], blurb=LAKE_BLURB["colonial-1620"],
         path=[(19.47259, -99.16891), (19.47259, -99.12085), (19.46692, -99.11754), (19.45684, -99.11532), (19.43784, -99.11152), (19.42921, -99.11104), (19.41994, -99.11257), (19.41118, -99.11481), (19.39841, -99.11778), (19.39841, -99.16891), (19.47259, -99.16891), (19.47259, -99.16891), (19.47259, -99.11211), (19.46883, -99.10881), (19.45841, -99.10652), (19.43941, -99.10272), (19.42961, -99.1021), (19.42688, -99.10227), (19.41795, -99.10387), (19.39841, -99.1089), (19.39841, -99.16891), (19.47259, -99.16891), (19.47259, -99.16891), (19.47259, -99.10337), (19.47067, -99.10007), (19.45999, -99.09772), (19.44099, -99.09392), (19.43801, -99.09355), (19.43001, -99.09315), (19.42775, -99.09317), (19.4255, -99.09343), (19.41596, -99.09516), (19.4081, -99.09717), (19.39841, -99.10001), (19.39841, -99.16891), (19.47259, -99.16891), (19.47259, -99.16891), (19.47251, -99.09133), (19.45056, -99.08673), (19.44256, -99.08609), (19.41611, -99.08609), (19.41397, -99.08646), (19.40655, -99.08835), (19.39841, -99.09113), (19.39841, -99.16891), (19.47259, -99.16891)]),
]
# --- END LAKE ---

WATER = LAKE + [
    dict(id="tlatelolco-channel", name="Channel between Tenochtitlan and Tlatelolco", width=45, periods=[I],
         path=[(19.4448, -99.1520), (19.4440, -99.1450), (19.4434, -99.1380), (19.4430, -99.1320), (19.4428, -99.1250), (19.4428, -99.1210)],
         blurb="The water between the two island cities, narrowing as both built chinampas toward each other. Tlatelolco kept its own ruler and market until 1473."),
    dict(id="tezontlalli-canal", name="Canal of Tlatelolco", width=16, periods=[M],
         path=[(19.4440, -99.1565), (19.4432, -99.1500), (19.4428, -99.1420), (19.4425, -99.1350), (19.4422, -99.1280), (19.4420, -99.1210), (19.4420, -99.1160)],
         blurb="The canal along the old boundary between Tenochtitlan and Tlatelolco, crossing the island from lake to lake."),
    dict(id="north-canal-1620", name="Acequia de Tezontlale", width=12, periods=[C],
         path=[(19.4425, -99.1440), (19.4425, -99.1350), (19.4422, -99.1280), (19.4420, -99.1210), (19.4418, -99.1150)],
         blurb="What was left of the old canal between the city and Tlatelolco, carrying canoes from the eastern lake to the northern barrios. Its western half had been filled in."),
    dict(id="acequia-real-1440", name="Great canal", width=16, periods=[I],
         path=[(19.4305, -99.1210), (19.4308, -99.1300), (19.4312, -99.1370), (19.4318, -99.1450), (19.4322, -99.1510)],
         blurb="The main east-west canal of Tenochtitlan, south of the temple precinct and the ruler's palace, used by canoes bringing goods from the eastern lake."),
    dict(id="acequia-real", name="Great canal (later the Acequia Real)", width=16, periods=[M],
         path=[(19.4300, -99.1150), (19.4305, -99.1230), (19.4310, -99.1300), (19.4312, -99.1370), (19.4315, -99.1450), (19.4320, -99.1555)],
         blurb="The main east-west canal, running past the south side of Moctezuma's palace. Cortés counted canals like this crossed by bridges of long, strong beams that could be raised."),
    dict(id="acequia-real-1620", name="Acequia Real", width=12, periods=[C],
         path=[(19.4300, -99.1140), (19.4305, -99.1230), (19.4310, -99.1300), (19.4312, -99.1370), (19.4315, -99.1430)],
         blurb="The royal canal along the south side of the viceregal palace: Indian canoes unloaded maize, fruit, flowers and firewood at its landings beside the Plaza Mayor."),
    dict(id="toltec-canal", name="Toltec canal (Toltecaacalopan)", width=16, periods=[M],
         path=[(19.4428, -99.1470), (19.4390, -99.1470), (19.4350, -99.1468), (19.4314, -99.1466)],
         blurb="A north-south canal on the west side of the city, crossed by the Tlacopan causeway. Its gap was the deadliest of the Noche Triste in 1520."),
    dict(id="viga-canal", name="Canal to Xochimilco and Chalco", width=16, periods=[M],
         path=[(19.4305, -99.1268), (19.4250, -99.1265), (19.4200, -99.1262), (19.4140, -99.1258)],
         blurb="The canal south through the chinampa wards toward the southern lakes, carrying maize, vegetables and flowers into the city."),
    dict(id="viga-canal-1620", name="Canal de la Viga", width=14, periods=[C],
         path=[(19.4305, -99.1268), (19.4250, -99.1265), (19.4200, -99.1262), (19.4120, -99.1258), (19.4000, -99.1255)],
         blurb="The canal from Chalco and Xochimilco: every morning hundreds of canoes brought vegetables, flowers and fodder to the Roldán landing."),
    dict(id="moyotlan-canal", name="Moyotlan canal", width=12, periods=[M],
         path=[(19.4313, -99.1402), (19.4250, -99.1405), (19.4180, -99.1410)],
         blurb="A canal through the south-western ward of Moyotlan, one of many lined with house plots and chinampas."),
]

# 1350: the reed beds between and round the two islets (the islets cut out as holes, keyhole style)
MARSH = [
    dict(name="Tule reed beds", periods=[F],
         polygon=HULL_1350 + [HULL_1350[0]] + TEN_1350[::-1] + [TEN_1350[-1], HULL_1350[0]] + TLAT_1350[::-1] + [TLAT_1350[-1]]),
    dict(name="Lagoon of Mexico, silting", periods=[C],
         polygon=[(19.4520, -99.1700), (19.4520, -99.1560), (19.4460, -99.1545), (19.4400, -99.1560), (19.4330, -99.1560), (19.4250, -99.1545), (19.4180, -99.1560), (19.4180, -99.1700)]),
    dict(name="Salt marsh north of Tlatelolco", periods=[C],
         polygon=[(19.4700, -99.1520), (19.4700, -99.1300), (19.4655, -99.1305), (19.4640, -99.1420), (19.4630, -99.1520)]),
    dict(name="Eastern shore marsh", periods=[C],
         polygon=[(19.4660, -99.1260), (19.4560, -99.1235), (19.4450, -99.1215), (19.4450, -99.1200), (19.4560, -99.1210), (19.4660, -99.1235)]),
]

TLACOPAN = [(19.4359, -99.1336), (19.4360, -99.1380), (19.4366, -99.1430), (19.4372, -99.1470), (19.4380, -99.1510), (19.4390, -99.1545),
            (19.4405, -99.1590), (19.4418, -99.1640), (19.4425, -99.1690)]
TLACOPAN_C = [(19.4362, -99.1345), (19.4366, -99.1430), (19.4372, -99.1470), (19.4380, -99.1510), (19.4390, -99.1545), (19.4405, -99.1590), (19.4418, -99.1640), (19.4425, -99.1690)]
IZTAPALAPA_N = [(19.43357, -99.1330), (19.4300, -99.1331), (19.4250, -99.1334), (19.4200, -99.1337), (19.4160, -99.1340), (19.4121, -99.1345)]
IZTAPALAPA_S = [(19.4115, -99.1345), (19.4060, -99.1350), (19.4000, -99.1352)]
COYOACAN = [(19.4117, -99.1348), (19.4085, -99.1400), (19.4040, -99.1460), (19.4010, -99.1500)]
TEPEYAC = [(19.43628, -99.1330), (19.4420, -99.1328), (19.4480, -99.1320), (19.4540, -99.1305), (19.4600, -99.1285), (19.4630, -99.1273), (19.4680, -99.1250), (19.4720, -99.1230)]
DIKE = [(19.4720, -99.0955), (19.4550, -99.0965), (19.4400, -99.0975), (19.4250, -99.0990), (19.4100, -99.1010), (19.4000, -99.1020)]

ROADS = [
    # 1350: paths on the islets
    dict(id="islet-path", name="Path to the temple", path=[(19.4300, -99.1330), (19.4340, -99.1328), (19.4400, -99.1325)], width=6, style="minor", periods=[F]),
    dict(id="islet-path-ew", name="Path across the islet", path=[(19.4345, -99.1395), (19.4347, -99.1330), (19.4345, -99.1260)], width=6, style="minor", periods=[F]),
    dict(id="tlatelolco-path", name="Path of Tlatelolco", path=[(19.4475, -99.1360), (19.4515, -99.1360), (19.4555, -99.1365)], width=6, style="minor", periods=[F]),
    # the causeways
    dict(id="tlacopan-causeway", name="Causeway of Tlacopan", path=TLACOPAN, width=10, style="major", labelled=True, periods=[I, M],
         blurb="The western causeway to Tlacopan, the shortest to the mainland, with gaps bridged by removable beams. The aqueduct from Chapultepec ran beside it into the city."),
    dict(id="iztapalapa-causeway-1440", name="Causeway of Iztapalapa", path=IZTAPALAPA_N, width=12, style="major", labelled=True, periods=[I]),
    dict(id="iztapalapa-causeway", name="Causeway of Iztapalapa", path=[(19.43174, -99.1331)] + IZTAPALAPA_N[1:], width=12, style="major", labelled=True, periods=[M],
         blurb="The great southern causeway, 'as straight as a rule' and wide enough for eight horsemen abreast, wrote Bernal Díaz. Cortés entered the city along it on 8 November 1519."),
    dict(id="iztapalapa-causeway-s", name="Causeway of Iztapalapa", path=IZTAPALAPA_S, width=12, style="major", periods=[I, M]),
    dict(id="coyoacan-causeway", name="Causeway of Coyoacán", path=COYOACAN, width=9, style="major", periods=[I, M],
         blurb="The branch to Coyoacán, joining the Iztapalapa causeway at the fort of Xoloc."),
    dict(id="tepeyac-causeway", name="Causeway of Tepeyac", path=TEPEYAC, width=10, style="major", labelled=True, periods=[I, M],
         blurb="The northern causeway past Tlatelolco to the hill of Tepeyac and its shrine of the goddess Tonantzin."),
    dict(id="dike", name="Dike of Nezahualcoyotl", path=DIKE, width=20, style="minor", labelled=True, periods=[I, M],
         blurb="A dike about 16 km long of stakes, stone and earth, built in 1449 to separate the fresh western lake from the salt eastern lake and protect the city from floods."),
    # streets of the island
    dict(id="east-street", name="Street to the Texcoco landing", path=[(19.4347, -99.13069), (19.4345, -99.1250), (19.4342, -99.1185)], width=8, style="minor", periods=[M]),
    dict(id="east-street-1440", name="Street to the Texcoco landing", path=[(19.4347, -99.1300), (19.4345, -99.1250), (19.4344, -99.1232)], width=8, style="minor", periods=[I]),
    dict(id="tlatelolco-street", name="Street of Tlatelolco", path=[(19.4515, -99.1405), (19.4515, -99.1460), (19.4520, -99.1505)], width=7, style="minor", periods=[M]),
    dict(id="tlatelolco-market-street", name="Market street", path=[(19.4497, -99.1320), (19.4497, -99.1265), (19.4500, -99.1240)], width=7, style="minor", periods=[M]),
    dict(id="moyotlan-street", name="Street of Moyotlan", path=[(19.4357, -99.1352), (19.4300, -99.1355), (19.4230, -99.1360), (19.4175, -99.1362)], width=7, style="minor", periods=[M]),
    # 1620: calzadas and the streets of the traza
    dict(id="calzada-tacuba", name="Calzada de Tacuba", path=TLACOPAN_C, width=12, style="major", labelled=True, periods=[C],
         blurb="The old Tlacopan causeway, now a paved road with the aqueduct alongside, lined with houses as far as San Cosme."),
    dict(id="calzada-san-antonio", name="Calzada de San Antonio Abad", path=[(19.43174, -99.1331), (19.4300, -99.1331), (19.4250, -99.1334), (19.4200, -99.1337), (19.4160, -99.1340), (19.4115, -99.1345), (19.4060, -99.1350), (19.4000, -99.1352)],
         width=12, style="major", labelled=True, periods=[C], blurb="The old Iztapalapa causeway, the road south to Coyoacán and Iztapalapa past the hermitage of San Antonio Abad."),
    dict(id="calzada-guadalupe", name="Calzada de Guadalupe", path=[(19.4400, -99.1328), (19.4480, -99.1320), (19.4540, -99.1305), (19.4600, -99.1285), (19.4630, -99.1273), (19.4680, -99.1250), (19.4720, -99.1230)],
         width=10, style="major", labelled=True, periods=[C], blurb="The old Tepeyac causeway, the pilgrims' road to the shrine of Our Lady of Guadalupe."),
    dict(id="calle-tacuba", name="Calle de Tacuba", path=[(19.4362, -99.1345), (19.4362, -99.1265)], width=10, style="minor", periods=[C]),
    dict(id="calle-san-francisco", name="Calle de San Francisco", path=[(19.4340, -99.1418), (19.4341, -99.1346)], width=10, style="minor", periods=[C]),
    dict(id="calle-donceles", name="Calle de los Donceles", path=[(19.4375, -99.1418), (19.4375, -99.1265)], width=9, style="minor", periods=[C]),
    dict(id="calle-santo-domingo", name="Calle de Santo Domingo", path=[(19.4400, -99.1355), (19.4400, -99.1265)], width=9, style="minor", periods=[C]),
    dict(id="calle-del-reloj", name="Calle del Reloj", path=[(19.4440, -99.1300), (19.4365, -99.1300)], width=9, style="minor", periods=[C]),
    dict(id="calle-santo-domingo-ns", name="Calle de la Encarnación", path=[(19.4420, -99.1348), (19.4352, -99.1348)], width=9, style="minor", periods=[C]),
    dict(id="calle-san-agustin", name="Calle de San Agustín", path=[(19.4290, -99.1418), (19.4295, -99.1345)], width=9, style="minor", periods=[C]),
    dict(id="calle-mesones", name="Calle de Mesones", path=[(19.4278, -99.1418), (19.4280, -99.1268)], width=9, style="minor", periods=[C]),
    dict(id="calle-san-juan", name="Calle de San Juan de Letrán", path=[(19.4400, -99.1422), (19.4270, -99.1422)], width=10, style="minor", periods=[C]),
    dict(id="calle-santisima", name="Calle de la Santísima", path=[(19.4400, -99.1268), (19.4290, -99.1268)], width=9, style="minor", periods=[C]),
    dict(id="san-lazaro-dike", name="Albarradón de San Lázaro", path=[(19.4720, -99.1236), (19.4660, -99.1220), (19.4560, -99.1198), (19.4450, -99.1176), (19.4370, -99.1160), (19.4290, -99.1156), (19.4210, -99.1170), (19.4120, -99.1193), (19.4000, -99.1210)],
         width=14, style="minor", labelled=True, periods=[C], blurb="The dike built in 1555–56 after a flood, closer to the city than Nezahualcoyotl's, guarding its eastern edge against Lake Texcoco."),
]

# the Sacred Precinct of Tenochtitlan (1519 extent) and of Tlatelolco
PRECINCT = [(19.43628, -99.13345), (19.43628, -99.13069), (19.43357, -99.13069), (19.43357, -99.13345)]
WALLS = []
GATES = []

BRIDGES = [
    dict(id="toltec-bridge", name="Bridge of the Toltec canal", path=[(19.43715, -99.14640), (19.43728, -99.14740)], build="timber", arches=1, landmarkId="toltec-canal-bridge", periods=[M]),
    dict(id="tlacopan-gap-1", name="Bridge in the Tlacopan causeway", path=[(19.43968, -99.15660), (19.43978, -99.15695)], build="timber", arches=1, periods=[M],
         blurb="One of the gaps in the causeway, spanned by removable beams so that the city could cut itself off."),
    dict(id="tlacopan-gap-2", name="Bridge in the Tlacopan causeway", path=[(19.44090, -99.16040), (19.44098, -99.16075)], build="timber", arches=1, periods=[I, M]),
    dict(id="iztapalapa-gap-1", name="Bridge in the Iztapalapa causeway", path=[(19.41410, -99.13423), (19.41380, -99.13427)], build="timber", arches=1, periods=[M]),
    dict(id="iztapalapa-gap-2", name="Bridge in the Iztapalapa causeway", path=[(19.40720, -99.13490), (19.40690, -99.13492)], build="timber", arches=1, periods=[I, M]),
    dict(id="tepeyac-gap", name="Bridge in the Tepeyac causeway", path=[(19.46520, -99.12625), (19.46548, -99.12612)], build="timber", arches=1, periods=[M]),
    dict(id="acequia-bridge", name="Bridge over the great canal", path=[(19.43125, -99.1331), (19.43075, -99.1331)], build="timber", arches=1, periods=[M]),
    dict(id="tlatelolco-canal-bridge", name="Bridge over the canal of Tlatelolco", path=[(19.44275, -99.13280), (19.44225, -99.13282)], build="timber", arches=1, periods=[M]),
    dict(id="acequia-bridge-1620", name="Puente del Palacio over the Acequia Real", path=[(19.43125, -99.1331), (19.43075, -99.1331)], build="stone", arches=1, periods=[C]),
]

AQUEDUCTS = [
    dict(name="Aqueduct of Chapultepec", periods=[I, M],
         path=[(19.4240, -99.1660), (19.4320, -99.1620), (19.43835, -99.15760), (19.43875, -99.15450), (19.43775, -99.15100), (19.43745, -99.14850)]),
    dict(name="Aqueduct of Chapultepec (Santa Fe line)", periods=[C],
         path=[(19.4240, -99.1660), (19.4320, -99.1620), (19.43835, -99.15760), (19.43875, -99.15450), (19.43775, -99.15100), (19.43745, -99.14850), (19.43625, -99.14400)]),
]

BLOCKS = [
    # 1350: the two settlements
    dict(name="Tenochtitlan, first houses", density="loose", periods=[F],
         polygon=[(19.4388, -99.1368), (19.4388, -99.1300), (19.4362, -99.1280), (19.4322, -99.1282), (19.4312, -99.1330), (19.4330, -99.1372)]),
    dict(name="Tlatelolco, first houses", density="loose", periods=[F],
         polygon=[(19.4545, -99.1405), (19.4545, -99.1352), (19.4520, -99.1338), (19.4492, -99.1345), (19.4490, -99.1400)]),
    # 1440: Tenochtitlan
    dict(name="Cuepopan", density="dense", periods=[I], polygon=[(19.4415, -99.1460), (19.4415, -99.1342), (19.4368, -99.1342), (19.4374, -99.1460)]),
    dict(name="Atzacoalco", density="dense", periods=[I], polygon=[(19.4415, -99.1320), (19.4410, -99.1250), (19.4352, -99.1240), (19.4352, -99.1296), (19.4364, -99.1296), (19.4364, -99.1320)]),
    dict(name="Teopan", density="dense", periods=[I], polygon=[(19.4338, -99.1296), (19.4340, -99.1240), (19.4315, -99.1240), (19.4315, -99.1296)]),
    dict(name="Moyotlan", density="dense", periods=[I], polygon=[(19.4357, -99.1470), (19.4357, -99.1340), (19.4322, -99.1340), (19.4326, -99.1470)]),
    dict(name="Southern wards", density="loose", periods=[I], polygon=[(19.4300, -99.1440), (19.4300, -99.1342), (19.4235, -99.1342), (19.4245, -99.1420)]),
    dict(name="South-eastern chinampas", density="loose", periods=[I], polygon=[(19.4300, -99.1322), (19.4300, -99.1255), (19.4260, -99.1262), (19.4235, -99.1318)]),
    dict(name="Tlatelolco", density="dense", periods=[I], polygon=[(19.4560, -99.1440), (19.4565, -99.1340), (19.4500, -99.1325), (19.4455, -99.1340), (19.4455, -99.1440)]),
    dict(name="Tlatelolco chinampas", density="loose", periods=[I], polygon=[(19.4545, -99.1312), (19.4540, -99.1290), (19.4470, -99.1272), (19.4455, -99.1310)]),
    # 1519: Tenochtitlan
    dict(name="Cuepopan", density="dense", periods=[M], polygon=[(19.4417, -99.1462), (19.4417, -99.1340), (19.4368, -99.1340), (19.4377, -99.1462)]),
    dict(name="Cuepopan chinampas", density="loose", periods=[M], polygon=[(19.4417, -99.1520), (19.4417, -99.1478), (19.4382, -99.1478), (19.4388, -99.1520)]),
    dict(name="Atzacoalco", density="dense", periods=[M], polygon=[(19.4417, -99.1321), (19.4417, -99.1240), (19.4352, -99.1240), (19.4352, -99.13035), (19.4367, -99.13035), (19.4367, -99.1321)]),
    dict(name="Atzacoalco chinampas", density="loose", periods=[M], polygon=[(19.4417, -99.1235), (19.4417, -99.1205), (19.4352, -99.1192), (19.4352, -99.1235)]),
    dict(name="Teopan", density="dense", periods=[M], polygon=[(19.4339, -99.12985), (19.4339, -99.1195), (19.4317, -99.1192), (19.4317, -99.12985)]),
    dict(name="Teopan south", density="dense", periods=[M], polygon=[(19.4302, -99.1325), (19.4302, -99.1275), (19.4240, -99.1273), (19.4240, -99.1325)]),
    dict(name="Zoquiapan chinampas", density="loose", periods=[M], polygon=[(19.4300, -99.1258), (19.4298, -99.1190), (19.4235, -99.1200), (19.4200, -99.1245), (19.4200, -99.1257)]),
    dict(name="Teopan chinampas", density="loose", periods=[M], polygon=[(19.4235, -99.1325), (19.4235, -99.1273), (19.4185, -99.1272), (19.4170, -99.1325)]),
    dict(name="Moyotlan", density="dense", periods=[M], polygon=[(19.4355, -99.1462), (19.4355, -99.1354), (19.4320, -99.1354), (19.4321, -99.1462)]),
    dict(name="Cuepopan south", density="dense", periods=[M], polygon=[(19.4356, -99.1352), (19.4356, -99.1337), (19.4349, -99.1337), (19.4349, -99.1352)]),
    dict(name="Moyotlan south", density="dense", periods=[M], polygon=[(19.4303, -99.1395), (19.4303, -99.1338), (19.4235, -99.1340), (19.4235, -99.1395)]),
    dict(name="Moyotlan chinampas", density="loose", periods=[M], polygon=[(19.4303, -99.1462), (19.4303, -99.1410), (19.4180, -99.1416), (19.4195, -99.1462)]),
    dict(name="Moyotlan west chinampas", density="loose", periods=[M], polygon=[(19.4372, -99.1520), (19.4372, -99.1478), (19.4310, -99.1476), (19.4232, -99.1474), (19.4275, -99.1515)]),
    # 1519: Tlatelolco
    dict(name="Tlatelolco west", density="dense", periods=[M], polygon=[(19.4560, -99.1490), (19.4560, -99.1412), (19.4436, -99.1412), (19.4440, -99.1490)]),
    dict(name="Tlatelolco south", density="dense", periods=[M], polygon=[(19.4492, -99.1405), (19.4492, -99.1350), (19.4436, -99.1350), (19.4436, -99.1405)]),
    dict(name="Tlatelolco east", density="dense", periods=[M], polygon=[(19.4555, -99.1292), (19.4555, -99.1258), (19.4436, -99.1236), (19.4436, -99.1318), (19.4500, -99.1311)]),
    dict(name="Tlatelolco north", density="dense", periods=[M], polygon=[(19.4605, -99.1440), (19.4610, -99.1320), (19.4538, -99.1320), (19.4538, -99.1440)]),
    dict(name="Market quarter", density="dense", periods=[M], polygon=[(19.4472, -99.1348), (19.4472, -99.1330), (19.4436, -99.1330), (19.4436, -99.1348)]),
    dict(name="Tlatelolco chinampas", density="loose", periods=[M], polygon=[(19.4612, -99.1490), (19.4615, -99.1448), (19.4565, -99.1448), (19.4565, -99.1490)]),
    # 1620: the traza and the barrios
    dict(name="Traza, north-west", density="dense", periods=[C], polygon=[(19.4398, -99.1418), (19.4398, -99.1352), (19.4366, -99.1352), (19.4366, -99.1418)]),
    dict(name="Traza, north", density="dense", periods=[C], polygon=[(19.4398, -99.1344), (19.4398, -99.1272), (19.4379, -99.1272), (19.4379, -99.1344)]),
    dict(name="Traza, west", density="dense", periods=[C], polygon=[(19.4358, -99.1418), (19.4358, -99.1352), (19.4345, -99.1352), (19.4345, -99.1418)]),
    dict(name="Traza, south-west", density="dense", periods=[C], polygon=[(19.4336, -99.1400), (19.4336, -99.1345), (19.4299, -99.1345), (19.4299, -99.1400)]),
    dict(name="Traza, old precinct", density="dense", periods=[C], polygon=[(19.4372, -99.1345), (19.4372, -99.1298), (19.4338, -99.1298), (19.4338, -99.1325), (19.4352, -99.1325), (19.4352, -99.1345)]),
    dict(name="Empedradillo", density="dense", periods=[C], polygon=[(19.4352, -99.1352), (19.4352, -99.1338), (19.4337, -99.1338), (19.4337, -99.1352)]),
    dict(name="Traza, east", density="dense", periods=[C], polygon=[(19.4372, -99.1296), (19.4372, -99.1272), (19.4295, -99.1272), (19.4295, -99.1296)]),
    dict(name="Traza, south", density="dense", periods=[C], polygon=[(19.4292, -99.1418), (19.4292, -99.1272), (19.4282, -99.1272), (19.4283, -99.1418)]),
    dict(name="San Juan Moyotlan", density="loose", periods=[C], polygon=[(19.4400, -99.1500), (19.4398, -99.1428), (19.4275, -99.1428), (19.4210, -99.1430), (19.4230, -99.1500)]),
    dict(name="San Pablo Teopan", density="loose", periods=[C], polygon=[(19.4275, -99.1410), (19.4275, -99.1272), (19.4200, -99.1272), (19.4190, -99.1410)]),
    dict(name="San Pablo east", density="loose", periods=[C], polygon=[(19.4300, -99.1258), (19.4300, -99.1180), (19.4220, -99.1190), (19.4210, -99.1258)]),
    dict(name="San Sebastián Atzacoalco", density="loose", periods=[C], polygon=[(19.4415, -99.1262), (19.4410, -99.1185), (19.4320, -99.1178), (19.4318, -99.1262)]),
    dict(name="Santa María Cuepopan", density="loose", periods=[C], polygon=[(19.4418, -99.1500), (19.4418, -99.1355), (19.4405, -99.1355), (19.4405, -99.1500)]),
    dict(name="Santiago Tlatelolco", density="loose", periods=[C], polygon=[(19.4580, -99.1460), (19.4580, -99.1335), (19.4432, -99.1335), (19.4432, -99.1460)]),
    dict(name="Tlatelolco east", density="loose", periods=[C], polygon=[(19.4560, -99.1315), (19.4550, -99.1250), (19.4432, -99.1230), (19.4432, -99.1315)]),
]

GARDENS = [
    dict(name="Garden of Moctezuma's palace", kind="park", periods=[M], polygon=[(19.4312, -99.1298), (19.4312, -99.1280), (19.4305, -99.1280), (19.4305, -99.1298)]),
    dict(name="Alameda", kind="park", periods=[C], polygon=[(19.4362, -99.1475), (19.4362, -99.1432), (19.4343, -99.1432), (19.4343, -99.1475)]),
]

DISTRICTS = [
    dict(id="sacred-precinct", name="Sacred Precinct", periods=[M], polygon=PRECINCT,
         description="The walled heart of the city and of the Mexica world: the Templo Mayor, temples of other gods, priests' schools, the skull rack, the ballcourt and the warriors' halls. The four quarters of the city met at its gates."),
    dict(id="moyotlan", name="Moyotlan", periods=[I, M], polygon=[(19.4357, -99.1530), (19.4357, -99.1336), (19.4160, -99.1336), (19.4160, -99.1480), (19.4270, -99.1530)],
         description="The south-western of the four quarters (campan), 'place of mosquitoes', later the Indian parish of San Juan."),
    dict(id="teopan", name="Teopan (Zoquiapan)", periods=[I, M], polygon=[(19.4345, -99.1328), (19.4345, -99.1175), (19.4230, -99.1185), (19.4160, -99.1270), (19.4160, -99.1328)],
         description="The south-eastern quarter, 'place of the god', with Moctezuma's palace on its edge and chinampa wards to the south; later San Pablo."),
    dict(id="atzacoalco", name="Atzacoalco", periods=[I, M], polygon=[(19.4420, -99.1328), (19.4420, -99.1200), (19.4350, -99.1185), (19.4350, -99.1328)],
         description="The north-eastern quarter, facing the eastern lake and the canoe landings from Texcoco; later San Sebastián."),
    dict(id="cuepopan", name="Cuepopan", periods=[I, M], polygon=[(19.4420, -99.1530), (19.4420, -99.1336), (19.4362, -99.1336), (19.4362, -99.1530)],
         description="The north-western quarter, 'where the flowers open', on the Tlacopan causeway; later Santa María la Redonda."),
    dict(id="tlatelolco", name="Tlatelolco", periods=[F, I, M], polygon=[(19.4625, -99.1500), (19.4625, -99.1260), (19.4432, -99.1215), (19.4432, -99.1500)],
         description="The twin city on the northern island, founded about 1337, independent until Tenochtitlan's conquest of 1473 and always the home of the great market and the long-distance merchants (pochteca)."),
    dict(id="traza", name="The traza", periods=[C], polygon=[(19.4400, -99.1422), (19.4400, -99.1268), (19.4278, -99.1268), (19.4278, -99.1422)],
         description="The Spanish city: a grid of straight streets laid out by Alonso García Bravo in the 1520s round the Plaza Mayor, reserved in principle for Spanish residents."),
    dict(id="san-juan", name="San Juan Tenochtitlan", periods=[C], polygon=[(19.4400, -99.1530), (19.4400, -99.1425), (19.4180, -99.1425), (19.4180, -99.1530)],
         description="The Indian parcialidad that kept the old name of Tenochtitlan, with its own governor and the market of San Juan."),
    dict(id="santiago-tlatelolco", name="Santiago Tlatelolco", periods=[C], polygon=[(19.4625, -99.1500), (19.4625, -99.1260), (19.4430, -99.1220), (19.4430, -99.1500)],
         description="The second Indian parcialidad, round the Franciscan church of Santiago and the Colegio de Santa Cruz."),
]

LABELS = [
    dict(text="LAGO DE TEXCOCO", position=(19.4300, -99.1060), size="lg", rotation=-80, periods=ALL),
    dict(text="Laguna de México", position=(19.4560, -99.1570), size="md", rotation=-70, periods=[I, M]),
    dict(text="TENOCHTITLAN", position=(19.4395, -99.1395), size="lg", periods=[I, M]),
    dict(text="Tenochtitlan", position=(19.4352, -99.1365), size="md", periods=[F]),
    dict(text="TLATELOLCO", position=(19.4575, -99.1395), size="md", periods=[I, M]),
    dict(text="Tlatelolco", position=(19.4555, -99.1390), size="sm", periods=[F]),
    dict(text="MÉXICO", position=(19.4395, -99.1395), size="lg", periods=[C]),
    dict(text="Santiago Tlatelolco", position=(19.4570, -99.1400), size="md", periods=[C]),
    dict(text="to Tlacopan", position=(19.4440, -99.1610), size="sm", rotation=-18, periods=[I, M, C]),
    dict(text="to Tepeyac", position=(19.4655, -99.1235), size="sm", rotation=-60, periods=[I, M, C]),
    dict(text="to Iztapalapa and Coyoacán", position=(19.4080, -99.1310), size="sm", rotation=-88, periods=[I, M, C]),
    dict(text="to Chapultepec", position=(19.4270, -99.1600), size="sm", rotation=-30, periods=[I, M, C]),
    dict(text="Albarradón", position=(19.4500, -99.0990), size="sm", rotation=-86, periods=[I, M]),
    dict(text="Xoloc", position=(19.4118, -99.1310), size="sm", periods=[M]),
]
