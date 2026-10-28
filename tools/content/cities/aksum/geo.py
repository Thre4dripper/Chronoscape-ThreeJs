# Aksum: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
ALL = ["early-100", "ezana-350", "kaleb-530", "medieval-1500", "gondarine-1665"]
AKSUMITE = ["ezana-350", "kaleb-530"]
LATER = ["medieval-1500", "gondarine-1665"]
FROM_350 = ["ezana-350", "kaleb-530", "medieval-1500", "gondarine-1665"]

SOURCES = [
    dict(id="munro-hay-aksum", title="Aksum: An African Civilisation of Late Antiquity", author="Stuart Munro-Hay", year=1991),
    dict(id="phillipson-ancient-ethiopia", title="Ancient Ethiopia: Aksum, its Antecedents and Successors", author="David W. Phillipson", year=1998),
    dict(id="phillipson-foundations", title="Foundations of an African Civilisation: Aksum and the Northern Horn, 1000 BC – AD 1300", author="David W. Phillipson", year=2012),
    dict(id="periplus", title="Periplus of the Erythraean Sea", author="anonymous Greek merchant", year="mid-1st century CE", note="trans. Lionel Casson (1989)", url="https://en.wikipedia.org/wiki/Periplus_of_the_Erythraean_Sea"),
    dict(id="unesco-aksum", title="Aksum (World Heritage List no. 15)", author="UNESCO World Heritage Centre", year=1980, url="https://whc.unesco.org/en/list/15/"),
    dict(id="wiki-axum", title="Axum", author="Wikipedia", url="https://en.wikipedia.org/wiki/Axum"),
    dict(id="wiki-kingdom-aksum", title="Kingdom of Aksum", author="Wikipedia", url="https://en.wikipedia.org/wiki/Kingdom_of_Aksum"),
    dict(id="wiki-beta-giyorgis", title="Axum (Beta Giyorgis and the pre-Aksumite settlement)", author="Wikipedia", url="https://en.wikipedia.org/wiki/Axum"),
]

CITY = dict(
    name="Aksum", subtitle="City of the Stelae",
    description="Seventeen centuries of Aksum in the highlands of northern Ethiopia: from the early town below the hill of Beta Giyorgis, through the kings who raised the carved granite stelae, struck gold coins and turned Christian, to the sacred town of St Mary of Zion where emperors came to be crowned. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="ezana-350",
    world=dict(heightScale=1.0, walls=["#B9AE9A", "#A89C86", "#C4B8A0", "#9E927E", "#B2A68E"], roofs=["#8E7A60", "#9A8668"]),
    camera=dict(target=(14.1305, 38.7190), distance=30),
)

# north-west corner, south-east corner: Beta Giyorgis and the hill of Abba Liqanos to the north-west, Mai Qoqo and the tombs of Kaleb to the north-east,
# Dungur and the Gudit field to the west, the open plain to the south
FRAME = ((14.1470, 38.7000), (14.1155, 38.7322))

PALETTE = dict(parchment="#E8D6AE", ink="#5E4632", water="#62858A", hill="#7E7A58", road="#8A6A4A")
COMPASS = (14.1180, 38.7300)
CARTOUCHE = (14.1162, 38.7008)

PERIODS = [
    dict(id="early-100", label="The early town", year=100, startYear=-150, endYear=269,
         summary="An early Aksumite town grows below the hill of Beta Giyorgis, where an older settlement and an elite cemetery stood. Rough, uncarved granite stelae mark the graves of the powerful north of the town. Around the middle of the 1st century the Greek Periplus names 'the metropolis of the Axumites', where ivory from beyond the Nile was brought on its way to the port of Adulis.",
         population="a few thousand, perhaps (no figures survive)",
         feel="Cattle lowing in the valley at dawn, smoke from hearths of acacia wood, the thud of mallets on granite as a new grave marker is dressed.",
         style="courtyard",
         houses=dict(title="Stone houses of the early town", text="Rectangular houses of rubble stone laid in mud, flat roofs of timber and earth, rooms round small yards; the richer ones already on low stone platforms."),
         outskirts=dict(title="Farmsteads and pasture", text="Scattered farmsteads with stone-walled cattle pens, fields of barley, wheat and teff on the plain, grazing on the hill slopes.")),
    dict(id="ezana-350", label="City of the stelae", year=350, startYear=270, endYear=479,
         summary="Aksum rules the northern highlands and the Red Sea trade through Adulis. Kings strike gold coins and raise carved granite stelae over their tombs, the tallest dressed as towers of thirteen storeys. Around the 330s King Ezana turns Christian under the Syrian Frumentius; the crescent and disc on his coins give way to the cross, and tradition places the first church of Mary of Zion here.",
         population="perhaps 20,000 (a guess; no figures survive)",
         feel="Greek, Ge'ez and South Arabian spoken in the market, the ring of the mint's hammers, granite towers casting long shadows over the graves at evening.",
         style="courtyard",
         houses=dict(title="Aksumite stone houses", text="Walls of rubble stone in mud, laid in recessed and projecting bays and tied by timber beams whose square ends stick out of the wall: the 'monkey-head' framing carved on the stelae. Flat roofs, a stair to an upper floor."),
         outskirts=dict(title="Mansions, farms and cemeteries", text="Elite mansions on stepped podiums among smaller houses; beyond them fields of wheat, barley and teff, cattle pens and the stelae of lesser families.")),
    dict(id="kaleb-530", label="Kaleb's Aksum", year=530, startYear=480, endYear=749,
         summary="A Christian kingdom at its height under Kaleb (Ella Asbeha), who sends a fleet across the Red Sea against the Jewish king of Himyar in Yemen around 525. Cosmas Indicopleustes describes a four-towered royal palace. Mansions like Dungur rise in the west; Kaleb and his son Gebre Meskel are traditionally buried on the hill to the north-east. In the 7th century trade falls away and the town slowly shrinks.",
         population="perhaps 20,000 at its height (a guess)",
         feel="Chanting from the cathedral, war elephants and the king's guard on the west road, merchants counting gold and copper coins under the stelae.",
         style="courtyard",
         houses=dict(title="Houses of the Christian city", text="Two-storey houses of stone and timber on stepped bases, the 'monkey-head' beam ends in rows on the walls, doors and windows framed in wood; small crosses carved over the lintels."),
         outskirts=dict(title="Mansions and farmland", text="Walled mansions of the nobles with their courts and servants' ranges, then villages and fields running out to the plain and the quarries of Gobedra.")),
    dict(id="medieval-1500", label="The sacred town", year=1500, startYear=750, endYear=1535,
         summary="The kings have long moved south; Aksum is a small town of priests round the church of Mary of Zion, rebuilt at some time in the Middle Ages and visited by a few emperors to be crowned. Francisco Alvares, here in the 1520s, saw a five-aisled painted church inside two walled enclosures, stelae, thrones and good houses. In 1535 the army of Ahmad Gragn burned the church.",
         population="perhaps 2,000–5,000 (a guess)",
         feel="Bells of stone and drums at the church gate, incense at dawn, the long chant of the priests, pilgrims sleeping in the churchyard.",
         style="kraal",
         houses=dict(title="Round huts round the church", text="Round houses of stone and wattle under conical thatched roofs, set in fenced compounds of the clergy and their families; some older stone houses still in use near the church."),
         outskirts=dict(title="Villages and fields", text="Small hamlets of round huts among the broken stelae and the mounds of the old mansions; terraced fields and pasture on the slopes.")),
    dict(id="gondarine-1665", label="Town of priests", year=1665, startYear=1536, endYear=1800,
         summary="After the wars, Aksum's church is rebuilt in a modest form, then replaced by Emperor Fasilides around 1665 with the battlemented church that still stands, on the old Aksumite podium. The court is at Gondar; Aksum is a holy town of priests, monks and church schools, with the right of sanctuary and the coronation stones where emperors were anointed.",
         population="a few thousand, many of them clergy (a guess)",
         feel="The chant of Yared's hymns before dawn, white-robed priests under juniper trees, pilgrims in the churchyard for the feast of Zion.",
         style="courtyard",
         houses=dict(title="Stone hidmo houses", text="Flat-roofed Tigrayan stone houses (hidmo) with thick walls of unmortared stone, timber posts inside and an earthen roof; round thatched huts in the yards. Clergy households cluster round the church."),
         outskirts=dict(title="Hamlets among the ruins", text="Farmsteads and round huts among the fallen stelae and ruined palaces, threshing floors and ox-ploughed fields of teff and barley.")),
]

# ---------------------------------------------------------------- water: the Mai Shum reservoir and the seasonal streams
MAI_HEJJA_N = [(14.1470, 38.7216), (14.1440, 38.7213), (14.1410, 38.7212), (14.1380, 38.7213), (14.1360, 38.7214), (14.1347, 38.7215)]
MAI_HEJJA_S = [(14.1337, 38.7214), (14.1325, 38.7213), (14.1312, 38.7213), (14.1295, 38.7215), (14.1270, 38.7218), (14.1240, 38.7224), (14.1200, 38.7231), (14.1155, 38.7236)]
WEST_STREAM = [(14.1395, 38.7082), (14.1360, 38.7090), (14.1325, 38.7096), (14.1290, 38.7101), (14.1255, 38.7109), (14.1215, 38.7116), (14.1155, 38.7124)]

WATER = [
    dict(id="mai-hejja", name="Mai Hejja (upper course)", path=MAI_HEJJA_N, width=8,
         blurb="A seasonal stream coming down between the hills of Beta Giyorgis and Mai Qoqo. It runs only in the rains of June to September; the rest of the year it is a stony bed, with water to be dug for in the sand."),
    dict(id="mai-hejja-south", name="Mai Hejja (through the town)", path=MAI_HEJJA_S, width=8,
         blurb="Below the reservoir the stream runs south past the stelae field and through the town to the plain. The name used here follows the archaeologists' maps; its ancient name is not known."),
    dict(id="mai-shum", name="Mai Shum", path=[(14.13405, 38.72140), (14.13435, 38.72165)], width=30, periods=FROM_350,
         blurb="The reservoir at the foot of Mai Qoqo, called the Queen of Sheba's Bath. It is cut into the rock where the valley opens, and may go back to Aksumite times; it was recut and enlarged later and is still used for water and for the Timkat baptism."),
    dict(id="mai-shum-spring", name="The spring pool", path=[(14.13412, 38.72148), (14.13428, 38.72160)], width=16, periods=["early-100"],
         blurb="A pool where the stream leaves the hills, the town's surest water in the dry months. Whether it was already dammed and cut into a reservoir is not known."),
    dict(id="west-stream", name="Stream below Beta Giyorgis", path=WEST_STREAM, width=6,
         blurb="A seasonal stream from the western slopes of Beta Giyorgis, crossing the Gondar road between the town and Dungur; dry outside the summer rains."),
]

HILLS = [
    dict(id="beta-giyorgis", name="Beta Giyorgis", center=(14.1405, 38.7135), radius=650,
         blurb="The flat-topped hill north-west of the town, over 2,200 m high. A settlement and an elite cemetery stood on its top centuries before the Aksumite kingdom (excavated by Rodolfo Fattovich); the church of St George that gives it its name came much later."),
    dict(id="abba-liqanos", name="Abba Liqanos", center=(14.1425, 38.7055), radius=360,
         blurb="A hilltop west of Beta Giyorgis crowned by the monastery of Abba Liqanos, by tradition one of the Nine Saints, monks from the Roman world who came to Aksum around 500."),
    dict(id="mai-qoqo", name="Mai Qoqo", center=(14.1345, 38.7282), radius=420,
         blurb="The hill east of the stream, at whose western foot lies the Mai Shum reservoir. On its slopes and on the spur to the north lie Aksumite tombs, among them those traditionally of Kaleb and Gebre Meskel."),
    dict(id="tombs-ridge", name="Ridge of the royal tombs", center=(14.1440, 38.7300), radius=320, label=False,
         blurb="A spur north of Mai Qoqo, with a wide view over the town and the plain, where the tombs attributed to Kaleb and Gebre Meskel were dug."),
]

ROADS = [
    dict(id="west-road", name="Road west to Gobedra and the Takkaze", path=[(14.1312, 38.7178), (14.1300, 38.7176), (14.1290, 38.7165), (14.1275, 38.7150), (14.1271, 38.7120), (14.1266, 38.7090), (14.12625, 38.7065), (14.1259, 38.7030), (14.1255, 38.7000)],
         width=12, style="major", labelled=True, periods=FROM_350,
         blurb="West past the great mansions and the stelae field of Gudit to the granite quarries of Gobedra, about 4 km out, and on to the Takkaze river and the west. In later centuries the route to Gondar."),
    dict(id="west-track", name="Track west to Gobedra", path=[(14.1312, 38.7178), (14.1300, 38.7176), (14.1290, 38.7165), (14.1275, 38.7150), (14.1271, 38.7120), (14.1266, 38.7090), (14.12625, 38.7065), (14.1259, 38.7030), (14.1255, 38.7000)],
         width=7, style="minor", periods=["early-100"],
         blurb="A track west along the foot of the hills to the outcrops of Gobedra, where granite for the first stelae was split."),
    dict(id="stelae-street", name="Street of the stelae", path=[(14.1312, 38.7160), (14.1312, 38.7190), (14.1312, 38.7215), (14.1310, 38.7245)],
         width=14, style="major", labelled=True, periods=FROM_350,
         blurb="The east–west way between the royal stelae field and the cathedral precinct: the town's ceremonial heart, where processions passed and, in later centuries, the coronation road ran."),
    dict(id="east-road", name="Road east to Yeha and Adulis", path=[(14.1310, 38.7245), (14.1305, 38.7270), (14.1295, 38.7300), (14.1288, 38.7322)],
         width=12, style="major", labelled=True, periods=FROM_350,
         blurb="East toward Adwa and Yeha, then north-east over the plateau and down the escarpment to Adulis on the Red Sea, a journey the Periplus reckons at about eight days. Ivory, gold and incense went out this way; glass, wine, cloth and iron came in."),
    dict(id="east-track", name="Track east", path=[(14.1312, 38.7215), (14.1310, 38.7245), (14.1305, 38.7270), (14.1295, 38.7300), (14.1288, 38.7322)],
         width=7, style="minor", periods=["early-100"],
         blurb="The track east toward Yeha, the older centre of the highlands, and the coast."),
    dict(id="south-road", name="Road south to the plain", path=[(14.1312, 38.7205), (14.1300, 38.7206), (14.1270, 38.7207), (14.1240, 38.7204), (14.1200, 38.7199), (14.1155, 38.7195)],
         width=10, style="major", labelled=False, periods=FROM_350,
         blurb="South out of the town into the farmland of the plain, toward the villages and the roads to the south."),
    dict(id="tombs-road", name="Road of the royal tombs", path=[(14.1312, 38.7225), (14.1330, 38.7224), (14.1348, 38.7223), (14.1365, 38.7226), (14.1378, 38.7233), (14.1395, 38.7250), (14.1408, 38.7270), (14.1416, 38.7285)],
         width=8, style="minor", labelled=True, periods=["kaleb-530", "medieval-1500", "gondarine-1665"],
         blurb="Up the valley past the Mai Shum reservoir and the stone of Ezana to the tombs on the ridge north-east of the town."),
    dict(id="mai-shum-path", name="Path to Mai Shum", path=[(14.1312, 38.7225), (14.1330, 38.7224), (14.1348, 38.7223), (14.1365, 38.7226), (14.1378, 38.7233)],
         width=6, style="minor", periods=["early-100", "ezana-350"],
         blurb="The path from the town up to the pool at the mouth of the valley, walked every day by women and girls with water jars."),
    dict(id="beta-giyorgis-path", name="Path up Beta Giyorgis", path=[(14.1312, 38.7160), (14.1340, 38.7150), (14.1365, 38.7142), (14.1386, 38.7132)],
         width=6, style="minor",
         blurb="The climb to the top of Beta Giyorgis, where the old hilltop settlement and its cemetery lay."),
    dict(id="lower-street", name="Lane of the mansions", path=[(14.1290, 38.7165), (14.1268, 38.7175), (14.1262, 38.7200), (14.1270, 38.7207)],
         width=6, style="minor", periods=AKSUMITE,
         blurb="A lane through the southern quarter of stone houses and mansions."),
]

BLOCKS = [
    # ---- the early town, c. 100
    dict(name="Houses at the foot of Beta Giyorgis", polygon=[(14.1316, 38.7163), (14.1336, 38.7156), (14.1340, 38.7180), (14.1318, 38.7184)], density="loose", periods=["early-100"]),
    dict(name="The early town", polygon=[(14.1308, 38.7168), (14.1308, 38.7205), (14.1288, 38.7205), (14.1288, 38.7170)], density="loose", periods=["early-100"]),
    dict(name="Slopes of Beta Giyorgis", polygon=[(14.1372, 38.7100), (14.1380, 38.7140), (14.1405, 38.7150), (14.1412, 38.7105)], density="loose", periods=["early-100"]),
    dict(name="Farmsteads by the spring", polygon=[(14.1318, 38.7228), (14.1334, 38.7230), (14.1332, 38.7246), (14.1318, 38.7246)], density="loose", periods=["early-100"]),
    # ---- the Aksumite city, 350 and 530
    dict(name="Round the cathedral", polygon=[(14.1308, 38.7181), (14.1308, 38.7202), (14.1272, 38.7203), (14.1272, 38.7182)], density="dense", periods=AKSUMITE),
    dict(name="Between road and stream", polygon=[(14.1307, 38.7208), (14.1307, 38.7211), (14.1262, 38.7217), (14.1262, 38.7209)], density="dense", periods=AKSUMITE),
    dict(name="East of the stream", polygon=[(14.1307, 38.7220), (14.1306, 38.7246), (14.1284, 38.7254), (14.1262, 38.7246), (14.1262, 38.7226)], density="dense", periods=AKSUMITE),
    dict(name="West town", polygon=[(14.1305, 38.7140), (14.1306, 38.7172), (14.1292, 38.7163), (14.1278, 38.7150), (14.1276, 38.7118), (14.1292, 38.7112)], density="loose", periods=AKSUMITE),
    dict(name="South of the west road", polygon=[(14.1266, 38.7112), (14.1268, 38.7148), (14.1262, 38.7172), (14.1240, 38.7174), (14.1240, 38.7114)], density="loose", periods=AKSUMITE),
    dict(name="Below the stelae", polygon=[(14.1316, 38.7164), (14.1335, 38.7158), (14.1336, 38.7176), (14.1316, 38.7177)], density="loose", periods=AKSUMITE),
    dict(name="Under Mai Qoqo", polygon=[(14.1316, 38.7229), (14.1334, 38.7231), (14.1331, 38.7250), (14.1315, 38.7251)], density="loose", periods=AKSUMITE),
    dict(name="Toward the plain", polygon=[(14.1258, 38.7182), (14.1258, 38.7202), (14.1228, 38.7201), (14.1228, 38.7183)], density="loose", periods=AKSUMITE),
    dict(name="East of the south road", polygon=[(14.1258, 38.7210), (14.1258, 38.7220), (14.1230, 38.7225), (14.1228, 38.7209)], density="loose", periods=AKSUMITE),
    dict(name="Mansions of the west", polygon=[(14.1275, 38.7072), (14.1292, 38.7075), (14.1294, 38.7095), (14.1272, 38.7096)], density="loose", periods=["kaleb-530"]),
    dict(name="Houses round Dungur", polygon=[(14.1274, 38.7020), (14.1290, 38.7022), (14.1290, 38.7058), (14.1274, 38.7057)], density="loose", periods=["kaleb-530"]),
    dict(name="East town", polygon=[(14.1302, 38.7256), (14.1300, 38.7272), (14.1284, 38.7272), (14.1284, 38.7258)], density="loose", periods=["kaleb-530"]),
    # ---- the sacred town, 1500
    dict(name="Clergy compounds round Mary of Zion", polygon=[(14.1308, 38.7170), (14.1308, 38.7203), (14.1276, 38.7203), (14.1276, 38.7172)], density="dense", periods=["medieval-1500"]),
    dict(name="Huts east of the stream", polygon=[(14.1306, 38.7220), (14.1305, 38.7240), (14.1280, 38.7242), (14.1280, 38.7222)], density="loose", periods=["medieval-1500"]),
    dict(name="Huts under the stelae", polygon=[(14.1316, 38.7164), (14.1335, 38.7158), (14.1336, 38.7176), (14.1316, 38.7177)], density="loose", periods=["medieval-1500"]),
    dict(name="Hamlet on the west road", polygon=[(14.1283, 38.7125), (14.1300, 38.7130), (14.1302, 38.7160), (14.1288, 38.7158)], density="loose", periods=["medieval-1500"]),
    dict(name="Huts toward the plain", polygon=[(14.1270, 38.7182), (14.1270, 38.7203), (14.1245, 38.7202), (14.1245, 38.7184)], density="loose", periods=["medieval-1500"]),
    # ---- the town of priests, 1665
    dict(name="Clergy houses round the church", polygon=[(14.1308, 38.7170), (14.1308, 38.7203), (14.1275, 38.7203), (14.1275, 38.7172)], density="dense", periods=["gondarine-1665"]),
    dict(name="East of the stream", polygon=[(14.1306, 38.7220), (14.1305, 38.7242), (14.1278, 38.7246), (14.1270, 38.7222)], density="dense", periods=["gondarine-1665"]),
    dict(name="Under the stelae", polygon=[(14.1316, 38.7164), (14.1335, 38.7158), (14.1336, 38.7176), (14.1316, 38.7177)], density="loose", periods=["gondarine-1665"]),
    dict(name="West houses", polygon=[(14.1283, 38.7125), (14.1300, 38.7130), (14.1302, 38.7160), (14.1288, 38.7158)], density="loose", periods=["gondarine-1665"]),
    dict(name="South town", polygon=[(14.1268, 38.7182), (14.1268, 38.7203), (14.1240, 38.7202), (14.1240, 38.7184)], density="loose", periods=["gondarine-1665"]),
    dict(name="Under Mai Qoqo", polygon=[(14.1316, 38.7229), (14.1334, 38.7231), (14.1331, 38.7248), (14.1315, 38.7249)], density="loose", periods=["gondarine-1665"]),
]

GARDENS = [
    dict(name="Trees of the church precinct", polygon=[(14.1290, 38.7176), (14.1290, 38.7181), (14.1278, 38.7181), (14.1278, 38.7176)], kind="park", periods=LATER),
    dict(name="Olive and juniper grove", polygon=[(14.1345, 38.7175), (14.1360, 38.7170), (14.1362, 38.7195), (14.1347, 38.7198)], kind="park", periods=LATER),
]

DISTRICTS = [
    dict(id="stelae-field", name="The royal stelae field", polygon=[(14.1316, 38.7178), (14.1345, 38.7178), (14.1345, 38.7210), (14.1316, 38.7210)], periods=ALL,
         description="The main cemetery of Aksum's rulers at the foot of Beta Giyorgis: rough stones of the early graves, then the carved stelae of the 3rd and 4th centuries over great underground tombs. The archaeologists' Northern Stelae Park."),
    dict(id="zion-precinct", name="Precinct of Mary of Zion", polygon=[(14.1275, 38.7180), (14.1310, 38.7180), (14.1310, 38.7203), (14.1275, 38.7203)], periods=FROM_350,
         description="The cathedral and its enclosures: in Alvares' day a great walled circuit holding the church, the houses of its clergy, canons and monks. Boundaries approximate."),
    dict(id="west-mansions", name="The western mansions", polygon=[(14.1250, 38.7015), (14.1300, 38.7015), (14.1300, 38.7160), (14.1250, 38.7160)], periods=AKSUMITE,
         description="The western side of the Aksumite city along the road to Gobedra, with great mansions on stepped podiums: Ta'akha Maryam, and later Dungur, beside the stelae field of Gudit."),
    dict(id="mai-shum-valley", name="The valley of Mai Shum", polygon=[(14.1335, 38.7210), (14.1395, 38.7210), (14.1395, 38.7245), (14.1335, 38.7245)], periods=ALL,
         description="The mouth of the Mai Hejja valley between the two hills, with the town's reservoir and, beyond it, the road to the royal tombs."),
]

LABELS = [
    dict(text="Aksum", position=(14.1258, 38.7240), size="lg", periods=ALL),
    dict(text="Beta Giyorgis", position=(14.1430, 38.7150), size="md"),
    dict(text="Mai Qoqo", position=(14.1340, 38.7300), size="md"),
    dict(text="Abba Liqanos", position=(14.1452, 38.7045), size="sm"),
    dict(text="Mai Shum", position=(14.1352, 38.7198), size="sm", periods=FROM_350),
    dict(text="stelae field", position=(14.1340, 38.7188), size="sm"),
    dict(text="Dungur", position=(14.1280, 38.7045), size="sm", periods=["kaleb-530", "medieval-1500", "gondarine-1665"]),
    dict(text="Gudit field", position=(14.1245, 38.7080), size="sm", periods=FROM_350),
    dict(text="to Gobedra and the west", position=(14.1240, 38.7030), size="sm"),
    dict(text="to Yeha and Adulis", position=(14.1278, 38.7298), size="sm"),
    dict(text="the plain", position=(14.1185, 38.7160), size="md"),
    dict(text="tombs of Kaleb", position=(14.1455, 38.7285), size="sm", periods=["kaleb-530", "medieval-1500", "gondarine-1665"]),
]
