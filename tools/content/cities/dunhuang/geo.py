# Dunhuang / Shazhou: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
HAN = ["han-100"]
WEI = ["northern-wei-500"]
TANG = ["tang-800"]
GUIYI = ["guiyi-950"]
MING = ["ming-1500"]
LIVED = HAN + WEI + TANG + GUIYI          # the oasis town before its desertion
MEDIEVAL = WEI + TANG + GUIYI
TG = TANG + GUIYI
ALL = LIVED + MING

# The frame: the old town on the west bank of the Dang, the oasis round it and, 5 km south, the Crescent Moon Spring
# in the Mingsha dunes. The Mogao caves (25 km south-east) are drawn out of place at the south-east edge.
NORTH, SOUTH, WEST, EAST = 40.152, 40.085, 94.634, 94.722
# Shazhou old town: the usual reading of the surviving stretches (west bank of the Dang; the east side was washed out by the river
# in the Qing). Its exact trace is uncertain; this is a rectangle of about 720 x 1,170 m.
TW, TE, TS, TN = 94.6445, 94.6535, 40.1325, 40.1430
MX, MY = 94.6490, 40.1378                 # the main streets' crossing; south and north gates on MX, west and east gates on MY
SPRING = (40.0886, 94.6716)               # Crescent Moon Spring (Yueyaquan)


def R(n, s, w, e):
    """A rectangle between two latitudes and two longitudes."""
    return [(n, w), (n, e), (s, e), (s, w)]


def _crescent():
    """The spring's centre line: a shallow arc about 220 m long, convex to the north, as metres turned into lat/lon."""
    lat0, lon0 = SPRING
    pts = []
    for i in range(9):
        x = -105 + 210 * i / 8
        y = 22 - 38 * (x / 105) ** 2
        pts.append((round(lat0 + y / 110950, 6), round(lon0 + x / 85160, 6)))
    return pts


CITY = dict(
    name="Dunhuang", subtitle="Shazhou, Oasis of the Caves",
    description="The oasis of Dunhuang from the Han commandery of 111 BCE to its desertion behind the Ming frontier: the walled town of Shazhou on the west bank of the Dang river, its canals and farms, the Sogdian quarter east of the river and, 5 km south, the Crescent Moon Spring in the Mingsha dunes. The Mogao caves, 25 km south-east, are drawn out of place at the frame's edge. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="tang-800",
    world=dict(heightScale=1.0, walls=["#D8C49C", "#CDB78E", "#C4AC82", "#DCCBA8"], roofs=["#B9A27C", "#AE966F", "#6E6A66"]),
    camera=dict(target=(40.1300, 94.6560), distance=44),
)
FRAME = ((NORTH, WEST), (SOUTH, EAST))
PALETTE = dict(parchment="#EAD8B0", ink="#6A4A32", water="#5F8A8C", hill="#B89A66", road="#8C6C4A")
COMPASS = (40.1490, 94.7175)
CARTOUCHE = (40.0862, 94.6350)

PERIODS = [
    dict(id="han-100", label="The Han commandery of Dunhuang", year=-100, startYear=-111, endYear=280,
         summary="The Han took the Hexi corridor from the Xiongnu and set up the commandery of Dunhuang about 111 BCE (some historians argue for a few decades later), carrying the wall and its beacon line west to the Yumen and Yang passes, 70-90 km beyond the frame. The town on the west bank of the Dang is a garrison and supply base: rammed-earth walls, granaries, the governor's office, soldier-farmers digging canals.",
         population="about 38,000 in the whole commandery (census of 2 CE); a few thousand in the town",
         feel="Pounded earth and camel dung, the drum of the commandery office, convict labourers digging ditches, and columns of smoke from the beacons on the desert edge.",
         style="sinic",
         houses=dict(title="Rammed-earth houses of the garrison town", text="Single-storey houses of rammed earth and sun-dried brick round small yards, roofed flat with poplar poles, reed mats and mud; the barracks, granaries and stables of the garrison along the walls."),
         outskirts=dict(title="Fields of the military colonies", text="Wheat and millet fields laid out by the soldier-farmers (tuntian), fed by new canals from the Dang; farmsteads among poplars and willows, and the gravel desert straight beyond the last ditch.")),
    dict(id="northern-wei-500", label="Buddhist Dunhuang", year=500, startYear=281, endYear=617,
         summary="After the Han the oasis passes between the Liang kingdoms of the north-west, the Northern Wei (from 439-442) and their successors. Buddhism comes with monks and merchants on the road: Dharmaraksha, 'the bodhisattva of Dunhuang', translates sutras in the 3rd century, and from 366, by tradition, monks cut meditation caves into the Mogao cliff 25 km south-east. Monasteries rise among the town's earth houses.",
         population="perhaps 10,000-20,000 in the oasis (no reliable figure)",
         feel="Bells and chanting from the monasteries, Sogdian voices at the market, and the dry wind off the dunes sifting sand into every courtyard.",
         style="sinic",
         houses=dict(title="Courtyard houses of the oasis town", text="One-storey houses of rammed earth and mud brick round courtyards, flat roofs of poplar beams and reed matting. The great local clans, the Suo, Zhang, Yin and Linghu, build larger compounds with gate halls and timber porches."),
         outskirts=dict(title="Canal hamlets", text="Hamlets strung along the canals among fields of wheat, millet and hemp, rows of poplars and elms against the wind, orchards of apricots and jujubes.")),
    dict(id="tang-800", label="Shazhou under Tibetan rule", year=800, startYear=618, endYear=847,
         summary="Tang Shazhou is a frontier prefecture with a Sogdian colony east of the walls. In 786, after a long siege, it surrenders to the Tibetan Empire, which rules until 848: Chinese clerks serve Tibetan officials and the monasteries prosper. The Mogao caves are at their height, with the Great Buddhas of 35 and 26 m in their timber façades, and the monasteries copy sutras by the thousand.",
         population="about 16,000 in the prefecture by the census of the 740s; fewer under Tibetan rule",
         feel="Tibetan and Chinese spoken in the yamen, chanting from more than a dozen monasteries, camel bells at the east gate, and the smell of ink and lamp oil in the scriptoria.",
         style="sinic",
         houses=dict(title="Courtyard houses of Shazhou", text="Inside the rammed-earth walls, one-storey courtyard houses of earth and timber with flat mud roofs; grey-tiled halls only for officials and monasteries. Contracts in the library cave sell houses room by room and divide them between brothers."),
         outskirts=dict(title="Farms of the townships", text="Farmsteads of the oasis townships strung along the canals: walled yards, poplars and elms, wheat, millet, hemp and beans, orchards and melon beds, watered in turn by the canal officers' rota.")),
    dict(id="guiyi-950", label="The Guiyi Circuit of the Cao family", year=950, startYear=848, endYear=1036,
         summary="In 848 Zhang Yichao drives out the Tibetans and offers Shazhou to the Tang, who make it the Guiyi ('Return to Allegiance') Circuit. From 914 the Cao family rule it as a little kingdom, marrying into the Uighur and Khotanese royal houses and cutting great family caves at Mogao. About 1000 a side chamber, Cave 17, is sealed full of manuscripts; in 1036 the Tanguts of Xixia take the oasis.",
         population="perhaps 20,000-30,000 in the oasis (estimates from the household registers vary)",
         feel="Uighur, Khotanese and Chinese envoys at the Cao court, feasts of the lay Buddhist societies in the lanes, and lamps carried out to every cave on the eighth day of the twelfth month.",
         style="sinic",
         houses=dict(title="Courtyard houses of the Guiyi town", text="One-storey courtyard houses of rammed earth and mud brick, flat-roofed: a hall, side rooms and a kitchen round a yard, often a mill or a stable. The deeds in the library cave sell them room by room, measured to the foot."),
         outskirts=dict(title="Farms and monastery estates", text="Farmsteads along the canals, monastery estates worked by dependent households, and on the desert edge the felt tents of Uighur and Tibetan herders.")),
    dict(id="ming-1500", label="Beyond the Jiayu Pass", year=1500, startYear=1037, endYear=1724,
         summary="The Tanguts hold Dunhuang from 1036, the Mongols from 1227. The Ming fix their frontier at the Jiayu Pass, some 380 km east, and leave the oasis to loose guard commands under Mongol chiefs (Shazhou guard from 1404; the Handong left guard from 1479). Farmers drift away; by the 1520s the Ming have withdrawn behind the pass. The old town is a ruin and the caves are visited by few.",
         population="a few hundred households of herders and farmers (a guess)",
         feel="Wind over the broken walls, sheep and goats bleating in the old streets, dung fires before felt tents, and sand drifting against every doorway.",
         style="sinic",
         houses=dict(title="Huts in the ruins", text="A few farmhouses of mud brick and rammed earth patched against the old walls, roofed with poplar poles and reeds; many families live in felt tents for part of the year."),
         outskirts=dict(title="Silted canals and pasture", text="Only a few canals are kept open; old fields turn to tamarisk scrub, reed beds and grazing for sheep, goats and camels.")),
]

# ---------------------------------------------------------------- water and hills
DANG = [(40.0985, WEST), (40.1050, 94.6400), (40.1130, 94.6470), (40.1210, 94.6530), (40.1290, 94.6558), (40.1378, 94.6565), (40.1460, 94.6575), (NORTH, 94.6590)]

WATER = [
    dict(id="dang", name="Dang river (Danghe)", path=DANG, width=70,
         blurb="The Dang (in Tang texts the Ganquan, 'Sweet Spring', river) comes out of the Qilian mountains to the south-west and runs north past the town to the Shule river. All the oasis lives on it: its water is taken off at weirs above the town into a fan of canals. Summer floods later washed away the old town's east side."),
    dict(id="mengshou", name="Mengshou canal", width=8, periods=LIVED,
         path=[(40.1163, 94.6490), (40.1172, 94.6455), (40.1205, 94.6410), (40.1260, 94.6378), (40.1380, 94.6375), (40.1460, 94.6374), (NORTH, 94.6372)],
         blurb="One of the canals named in the Tang gazetteer of Shazhou found at Dunhuang (Pelliot 2005), called after Meng Shou, an official said to have dug it. Its line here, west of the town, is a guess."),
    dict(id="yangkai", name="Yangkai canal", width=8, periods=LIVED,
         path=[(40.1225, 94.6542), (40.1260, 94.6700), (40.1330, 94.6800), (40.1450, 94.6900), (NORTH, 94.6950)],
         blurb="A canal of the Tang gazetteer, here led north-east across the oasis east of the river. Canal officers (qutou) organised the farmers on each canal to clean it and to take their turn at the water."),
    dict(id="duxiang", name="Duxiang canal", width=8, periods=LIVED,
         path=[(40.1180, 94.6510), (40.1150, 94.6650), (40.1150, 94.6900), (40.1180, 94.7100), (40.1250, EAST)],
         blurb="The 'canal of the town townships', after the Tang gazetteer, here running east along the foot of the dunes. Its course is a guess; the manuscripts list scores of smaller branch canals and ditches."),
    dict(id="beifu", name="Beifu canal", width=7, periods=LIVED,
         path=[(40.1440, 94.6576), (40.1480, 94.6700), (NORTH, 94.6790)],
         blurb="'The north office canal' of the Tang gazetteer, watering the fields north of the town; its line is a guess."),
    dict(id="ming-ditch", name="Irrigation ditch", width=6, periods=MING,
         path=[(40.1163, 94.6490), (40.1172, 94.6455), (40.1205, 94.6410), (40.1260, 94.6378), (40.1380, 94.6375)],
         blurb="One of the few channels still kept open by the farmers who remained."),
    dict(id="yueyaquan", name="Crescent Moon Spring (Yueyaquan)", width=42, path=_crescent(),
         blurb="A crescent pool about 220 m long in a hollow among the dunes, fed by groundwater and never filled by the drifting sand: Tang texts call it the 'Sand Well' (Shajing). It has shrunk badly in the last century and is now topped up artificially."),
]

HILLS = [
    dict(id="mingsha", name="Mingsha Shan (Singing Sand Mountain)", center=(40.0960, 94.6620), radius=300,
         blurb="Dunes of fine sand rising 100 m and more above the oasis, stretching 40 km east to the Mogao cliff. In dry weather a sliding slope booms and hums; Tang and Five Dynasties texts already tell of the sand that 'roars like thunder', and townspeople climbed them at the Dragon Boat festival."),
    dict(id="dune-1", name="Mingsha dunes", center=(40.0935, 94.6455), radius=380, label=False),
    dict(id="dune-2", name="Mingsha dunes", center=(40.0890, 94.6545), radius=380, label=False),
    dict(id="dune-3", name="Mingsha dunes", center=(40.0990, 94.6535), radius=330, label=False),
    dict(id="dune-4", name="Mingsha dunes", center=(40.0870, 94.6625), radius=300, label=False),
    dict(id="dune-5", name="Mingsha dunes", center=(40.0950, 94.6805), radius=340, label=False),
    dict(id="dune-6", name="Mingsha dunes", center=(40.0870, 94.6835), radius=300, label=False),
    dict(id="dune-7", name="Mingsha dunes", center=(40.1015, 94.6830), radius=340, label=False),
    dict(id="dune-8", name="Mingsha dunes", center=(40.0905, 94.6935), radius=380, label=False),
    dict(id="dune-9", name="Mingsha dunes", center=(40.1000, 94.6965), radius=330, label=False),
    dict(id="dune-10", name="Mingsha dunes", center=(40.0880, 94.7040), radius=320, label=False),
    dict(id="dune-11", name="Mingsha dunes", center=(40.0975, 94.7200), radius=290, label=False),
    dict(id="dune-12", name="Mingsha dunes", center=(40.1060, 94.7185), radius=250, label=False),
    dict(id="dune-13", name="Mingsha dunes", center=(40.1065, 94.6530), radius=270, label=False),
    dict(id="dune-15", name="Mingsha dunes", center=(40.0870, 94.6475), radius=260, label=False),
]

# ---------------------------------------------------------------- roads
EAST_GATE_ROAD = [(MY, TE), (MY, 94.6559)]
EAST_ROAD = [(MY, 94.6571), (MY, 94.6640), (40.1385, 94.6900), (40.1395, EAST)]
SPRING_ROAD = [(MY, 94.6620), (40.1300, 94.6633), (40.1200, 94.6650), (40.1050, 94.6690), (40.0912, 94.6714)]
MOGAO_ROAD = [(40.1300, 94.6633), (40.1200, 94.6850), (40.1050, 94.7080), (40.0918, 94.7158)]

ROADS = [
    dict(id="south-street", name="South Street", path=[(TS, MX), (MY, MX)], width=14, style="major", labelled=True, periods=LIVED,
         blurb="The street from the south gate to the crossing in the middle of the town. The Tang town's street plan is not known; the cross of main streets is the usual pattern of a prefectural town."),
    dict(id="north-street", name="North Street", path=[(MY, MX), (TN, MX)], width=14, style="major", periods=LIVED),
    dict(id="west-street", name="West Street", path=[(MY, TW), (MY, MX)], width=12, style="major", periods=LIVED),
    dict(id="east-street", name="East Street", path=[(MY, MX), (MY, TE)], width=12, style="major", labelled=True, periods=LIVED,
         blurb="From the crossing to the east gate and the bridge over the Dang, the way to the Sogdian quarter, the caravan market and the road to China."),
    dict(id="lane-s", name="Lane", path=[(40.1350, MX), (40.1350, TE)], width=6, style="minor", periods=MEDIEVAL),
    dict(id="bridge-approach", name="Bridge approach", path=EAST_GATE_ROAD, width=12, periods=LIVED),
    dict(id="east-road", name="Road to Guazhou and Chang'an", path=EAST_ROAD, width=14, style="major", labelled=True, periods=LIVED,
         blurb="The Silk Road east: to Guazhou, through the Hexi corridor to Liangzhou and on to Chang'an, some 1,800 km away. Caravans of silk went west along it; horses, jade, glass and silver came east."),
    dict(id="spring-road", name="Road to the Sand Well", path=SPRING_ROAD, width=8, labelled=True, periods=ALL,
         blurb="South across the oasis to the dunes and the Crescent Moon Spring, 5 km from the town: a pleasure outing on festival days."),
    dict(id="mogao-road", name="Road to the Mogao caves", path=MOGAO_ROAD, width=8, labelled=True, periods=WEI + TANG + GUIYI,
         blurb="South-east along the foot of the dunes and across the gravel desert to the Mogao cliff, 25 km from the town: a day's walk for pilgrims, monks and painters. On this map it ends at the cliff drawn out of place at the frame's edge."),
    dict(id="yang-road", name="Road to the Yang Pass", path=[(MY, TW), (40.1350, 94.6405), (40.1290, WEST)], width=10, labelled=True, periods=LIVED,
         blurb="South-west to the Yang Pass, about 70 km away, and the southern road along the Kunlun to Khotan."),
    dict(id="yumen-road", name="Road to the Yumen Pass", path=[(TN, MX), (40.1480, 94.6440), (NORTH, 94.6405)], width=10, labelled=True, periods=LIVED,
         blurb="North-west to the Yumen ('Jade Gate') Pass, some 80-90 km away, and the northern road by Loulan or, later, by Hami and Turfan."),
    dict(id="han-fort-road", name="Track to the fort", path=[(MY, 94.6640), (40.1450, 94.6648), (40.1475, 94.6650)], width=6, style="minor", periods=HAN + WEI),
    dict(id="ming-track-n", name="Track", path=[(40.1380, 94.6440), (40.1480, 94.6440), (NORTH, 94.6405)], width=6, style="minor", periods=MING),
    dict(id="ming-track-e", name="Track to the ford", path=[(MY, TE), (MY, 94.6640), (40.1385, 94.6900)], width=6, style="minor", periods=MING),
]

WALLS = [
    dict(id="town-wall", name="Town wall of Dunhuang", closed=True, periods=HAN + WEI, path=R(TN, TS, TW, TE),
         blurb="Where the Han commandery town stood is debated; it was probably at or near the later Shazhou on the west bank of the Dang, and the map draws it on that circuit. Rammed earth, laid in layers between board shutters."),
    dict(id="shazhou-wall", name="Shazhou town wall", closed=True, periods=TG, path=R(TN, TS, TW, TE),
         blurb="The Tang walls of Shazhou, rammed earth some 10 m high, with corner towers, bastions and four gates; an inner citadel (zicheng) held the governor's offices. Stretches of the west wall and the south-west corner still stand on the west bank of the Dang."),
    dict(id="shazhou-ruin", name="Ruined walls of Shazhou", closed=False, periods=MING, path=[(TN, TE), (TN, TW), (TS, TW), (TS, TE)],
         blurb="The walls stand broken and empty, the east side already gnawed by the river. The Qing built a new Dunhuang town on the east bank in the 1720s."),
]

GATES = [
    dict(id="south-gate", name="South gate", position=(TS, MX), periods=LIVED),
    dict(id="north-gate", name="North gate", position=(TN, MX), periods=LIVED),
    dict(id="west-gate", name="West gate", position=(MY, TW), periods=LIVED),
    dict(id="east-gate", name="East gate", position=(MY, TE), periods=LIVED),
]

BRIDGES = [
    dict(id="dang-bridge-b", name="Bridge over the Dang", path=[(MY, 94.65595), (MY, 94.65705)], build="timber", arches=5, landmarkId="dang-bridge", periods=LIVED,
         blurb="A timber bridge on trestles joined the town to the east bank, the Sogdian quarter and the road to China."),
]

# ---------------------------------------------------------------- built-up areas
Q_NW = R(40.1427, MY + 0.0003, TW + 0.0003, MX - 0.0003)
Q_NE = R(40.1427, MY + 0.0003, MX + 0.0003, TE - 0.0003)
Q_SW = R(MY - 0.0003, TS + 0.0003, TW + 0.0003, MX - 0.0003)
Q_SE = R(MY - 0.0003, TS + 0.0003, MX + 0.0003, TE - 0.0003)

VILLAGES = [
    dict(name="Village on the Beifu canal", polygon=R(40.1478, 40.1460, 94.6700, 94.6740), density="loose"),
    dict(name="Village on the Yangkai canal", polygon=R(40.1310, 40.1292, 94.6880, 94.6930), density="loose"),
    dict(name="Village in the east fields", polygon=R(40.1455, 40.1437, 94.7000, 94.7050), density="loose"),
    dict(name="Village south of the town", polygon=R(40.1215, 40.1196, 94.6415, 94.6455), density="loose"),
    dict(name="Village on the Duxiang canal", polygon=R(40.1175, 40.1160, 94.6780, 94.6830), density="loose"),
    dict(name="Hamlet at the dunes", polygon=R(40.1132, 40.1115, 94.7000, 94.7045), density="loose"),
]

BLOCKS = (
    [dict(name="North-west quarter", polygon=Q_NW, density="dense", periods=HAN),
     dict(name="North-east quarter", polygon=Q_NE, density="dense", periods=HAN),
     dict(name="South-west quarter", polygon=Q_SW, density="loose", periods=HAN),
     dict(name="South-east quarter", polygon=Q_SE, density="loose", periods=HAN)]
    + [dict(name="North-west quarter", polygon=Q_NW, density="dense", periods=MEDIEVAL),
       dict(name="North-east quarter", polygon=Q_NE, density="dense", periods=MEDIEVAL),
       dict(name="South-west quarter", polygon=Q_SW, density="dense", periods=MEDIEVAL),
       dict(name="South-east quarter", polygon=Q_SE, density="dense", periods=TG),
       dict(name="South-east quarter", polygon=Q_SE, density="loose", periods=WEI)]
    + [dict(name="Congjiao township (the Sogdian colony)", polygon=R(40.1418, 40.1384, 94.6630, 94.6730), density="dense", periods=TANG),
       dict(name="East bank quarter", polygon=R(40.1418, 40.1384, 94.6630, 94.6730), density="dense", periods=GUIYI),
       dict(name="Inns by the bridge", polygon=R(40.1372, 40.1338, 94.6578, 94.6613), density="dense", periods=TG),
       dict(name="East bank houses", polygon=R(40.1372, 40.1338, 94.6636, 94.6700), density="loose", periods=TG),
       dict(name="East bank hamlet", polygon=R(40.1418, 40.1390, 94.6630, 94.6690), density="loose", periods=WEI),
       dict(name="West suburb", polygon=R(40.1425, 40.1388, 94.6395, 94.6438), density="loose", periods=MEDIEVAL),
       dict(name="North suburb", polygon=R(40.1475, 40.1438, 94.6497, 94.6545), density="loose", periods=TG)]
    + [dict(v, periods=LIVED) for v in VILLAGES]
    + [dict(name="Squatters in the old north-east quarter", polygon=R(40.1420, 40.1395, 94.6500, 94.6528), density="loose", periods=MING),
       dict(name="Farm on the west canal", polygon=R(40.1300, 40.1285, 94.6385, 94.6420), density="loose", periods=MING)]
)

FIELDS_W = [(40.1310, 94.6360), (40.1310, 94.6438), (40.1215, 94.6495), (40.1150, 94.6452), (40.1150, 94.6360)]
FIELDS_NW = R(40.1425, 40.1318, 94.6350, 94.6438)
FIELDS_N = R(NORTH - 0.0005, 40.1442, 94.6600, 94.7150)
FIELDS_E = R(40.1425, 40.1200, 94.6720, 94.7180)
FIELDS_SE = R(40.1325, 40.1090, 94.6645, 94.6895)
FIELDS_SE2 = R(40.1195, 40.1105, 94.6905, 94.7140)
FIELDS_RIVER = [(40.1195, 94.6560), (40.1290, 94.6588), (40.1290, 94.6620), (40.1100, 94.6620), (40.1100, 94.6575)]

GARDENS = (
    [dict(name=n, polygon=p, kind="orchard", periods=LIVED) for n, p in (
        ("Fields of the west canal", FIELDS_W), ("Fields west of the town", FIELDS_NW), ("Fields north of the town", FIELDS_N),
        ("Fields of the east canals", FIELDS_E), ("Fields under the dunes", FIELDS_SE), ("Fields on the Duxiang canal", FIELDS_SE2),
        ("Fields by the river", FIELDS_RIVER))]
    + [dict(name="Orchards by the town", polygon=R(40.1475, 40.1440, 94.6420, 94.6488), kind="orchard", periods=MEDIEVAL),
       dict(name="Fields kept on the west canal", polygon=FIELDS_W, kind="orchard", periods=MING),
       dict(name="Fields kept north of the ruins", polygon=R(40.1500, 40.1442, 94.6600, 94.6760), kind="orchard", periods=MING)]
)

MARSH = [
    dict(name="Reed beds by the river", polygon=R(NORTH - 0.0003, 40.1470, 94.6545, 94.6620)),
    dict(name="Tamarisk scrub on the old fields", polygon=R(40.1420, 40.1200, 94.6720, 94.7180), periods=MING),
    dict(name="Tamarisk scrub under the dunes", polygon=R(40.1325, 40.1090, 94.6645, 94.6895), periods=MING),
]

DISTRICTS = [
    dict(id="town", name="Dunhuang town", polygon=R(TN, TS, TW, TE), periods=HAN + WEI,
         description="The walled seat of the commandery of Dunhuang: the governor's office, granaries and barracks, and later the first monasteries, behind rammed-earth walls on the west bank of the Dang."),
    dict(id="shazhou", name="Shazhou", polygon=R(TN, TS, TW, TE), periods=TG,
         description="The walled town of Shazhou, seat of the prefecture and later of the Guiyi Circuit: the yamen in its inner citadel, monasteries, courtyard houses and lanes. Most of the oasis people lived outside it on their farms."),
    dict(id="congjiao", name="Congjiao township", polygon=R(40.1418, 40.1338, 94.6578, 94.6730), periods=TANG,
         description="A township of about 300 Sogdian households, registered in the 750s, a short way east of the town round the Xian (Zoroastrian) shrine of 'An city'. After the Tibetan conquest the families scattered among the other townships and turned Buddhist."),
    dict(id="oasis", name="The oasis", polygon=R(NORTH, 40.1090, WEST, EAST), periods=ALL,
         description="Fields, orchards, poplar rows and farmsteads along the canals of the Dang: a green island about 20 km across between the gravel desert and the Mingsha dunes."),
]

LABELS = [
    dict(text="Dunhuang", position=(40.1460, 94.6830), size="lg", periods=HAN + WEI),
    dict(text="Shazhou", position=(40.1460, 94.6830), size="lg", periods=TG),
    dict(text="Ruins of Shazhou", position=(40.1460, 94.6830), size="lg", periods=MING),
    dict(text="Dang He", position=(40.1240, 94.6528), size="md", rotation=-65),
    dict(text="Mingsha Shan", position=(40.0930, 94.6880), size="lg"),
    dict(text="Crescent Moon Spring", position=(40.0868, 94.6716), size="sm"),
    dict(text="Toward the Mogao Caves (25 km)", position=(40.0868, 94.7110), size="sm", periods=WEI + TANG + GUIYI + MING),
    dict(text="Oasis fields", position=(40.1300, 94.7040), size="md", periods=LIVED),
    dict(text="Congjiao (Sogdians)", position=(40.1430, 94.6690), size="sm", periods=TANG),
    dict(text="Gobi", position=(40.1505, 94.6380), size="sm"),
]

SOURCES = [
    dict(id="wiki-dunhuang", title="Dunhuang", author="Wikipedia", url="https://en.wikipedia.org/wiki/Dunhuang"),
    dict(id="wiki-hexi", title="Hexi Corridor", author="Wikipedia", url="https://en.wikipedia.org/wiki/Hexi_Corridor"),
    dict(id="wiki-shazhou", title="Shazhou", author="Wikipedia", url="https://en.wikipedia.org/wiki/Shazhou"),
    dict(id="wiki-crescent-lake", title="Crescent Lake (Dunhuang)", author="Wikipedia", url="https://en.wikipedia.org/wiki/Crescent_Lake_(Dunhuang)"),
    dict(id="wiki-singing-sand", title="Singing sand", author="Wikipedia", url="https://en.wikipedia.org/wiki/Singing_sand"),
    dict(id="wiki-guiyi", title="Guiyi Circuit", author="Wikipedia", url="https://en.wikipedia.org/wiki/Guiyi_Circuit"),
    dict(id="hansen", title="The Silk Road: A New History", author="Valerie Hansen", year=2012),
    dict(id="whitfield", title="Life Along the Silk Road", author="Susan Whitfield", year=1999),
    dict(id="rong-xinjiang", title="Eighteen Lectures on Dunhuang", author="Rong Xinjiang (trans. Imre Galambos)", year=2013),
    dict(id="shazhou-tujing", title="Shazhou dudufu tujing (Gazetteer of the Shazhou Area Command, Pelliot chinois 2005)", author="anonymous, Tang"),
]
