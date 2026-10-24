# Kaifeng / Bianzhou / Dongjing (Bianjing): city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
TANG = ["tang-800"]
SONG = ["song-1120"]
JIN = ["jin-1200"]
MING = ["ming-1600"]
QING = ["qing-1700"]
SONGJIN = SONG + JIN
EARLY = TANG + SONG + JIN                 # the city on the Bian, before the Ming
LATE = MING + QING                         # the Ming-Qing walled city
ALL = EARLY + LATE

# The frame holds the Song inner city and palace city, the eastern and southern parts of the outer city, the Bian river
# out to the frame's east edge and the Fan pagoda in the south. The Ming-Qing wall follows the surviving wall (OpenStreetMap);
# the Song inner and outer walls are drawn after the usual archaeological reconstruction and are approximate.
WEST, EAST, NORTH, SOUTH = 114.3070, 114.3880, 34.8240, 34.7640

# the Song inner city (Li Mian's Tang wall of 781, the Song "old city"), approximate
IN_N, IN_S = 34.8150, 34.7838
# the Song outer city (Later Zhou 955, rebuilt 1075-1078), approximate; its north side lies beyond the frame
OUT_W, OUT_E, OUT_S, OUT_N = 114.3100, 114.3845, 34.7680, 34.8330
# the palace city (Danei) of the Song and Jin
PAL_N, PAL_S, PAL_W, PAL_E = 34.8100, 34.8035, 114.3425, 114.3505
# the Imperial Way's line: Xuande gate, Zhou bridge, Zhuque gate, Nanxun gate
XUANDE = (34.8035, 114.3465)
ZHOUQIAO = (34.7912, 114.3459)
ZHUQUE = (34.7838, 114.3444)
NANXUN_OUT = (OUT_S, 114.3438)
NANXUN_MING = (34.7826, 114.3440)


def R(n, s, w, e):
    """A rectangle between two latitudes and two longitudes."""
    return [(n, w), (n, e), (s, e), (s, w)]


# the Ming-Qing wall (the brick wall that still stands, rebuilt after the floods of 1642 and 1841 on the Ming line)
MQ_WALL = [(34.8199, 114.3400), (34.8201, 114.3482), (34.8180, 114.3685), (34.8170, 114.3687), (34.8055, 114.3659), (34.8003, 114.3661),
           (34.7985, 114.3642), (34.7914, 114.3628), (34.7873, 114.3612), (34.7824, 114.3587), (34.7818, 114.3573), (34.7834, 114.3448),
           (34.7826, 114.3440), (34.7842, 114.3396), (34.7862, 114.3263), (34.7873, 114.3259), (34.7952, 114.3270), (34.7997, 114.3275),
           (34.8018, 114.3280), (34.8124, 114.3316), (34.8190, 114.3349), (34.8195, 114.3364)]
MQ_MOAT = [(34.8208, 114.3398), (34.8210, 114.3482), (34.8188, 114.3692), (34.8174, 114.3696), (34.8055, 114.3668), (34.8003, 114.3670),
           (34.7983, 114.3651), (34.7911, 114.3637), (34.7869, 114.3621), (34.7818, 114.3595), (34.7810, 114.3573), (34.7826, 114.3448),
           (34.7818, 114.3438), (34.7834, 114.3392), (34.7855, 114.3255), (34.7873, 114.3250), (34.7952, 114.3261), (34.7997, 114.3266),
           (34.8020, 114.3271), (34.8130, 114.3307), (34.8198, 114.3342), (34.8204, 114.3362), (34.8208, 114.3398)]
# the Song inner wall: on the Ming line in the east, south and west, its north side some 400 m further south
SONG_INNER = [(IN_N, 114.3300), (IN_N, 114.3672), (34.8055, 114.3659), (34.8003, 114.3661), (34.7985, 114.3642), (34.7914, 114.3628),
              (34.7873, 114.3612), (IN_S, 114.3600), (IN_S, 114.3268), (34.7952, 114.3270), (34.8018, 114.3280), (34.8124, 114.3298)]
SONG_INNER_MOAT = [(IN_N + 0.0007, 114.3292), (IN_N + 0.0007, 114.3681), (34.8055, 114.3668), (34.8003, 114.3670), (34.7983, 114.3651),
                   (34.7911, 114.3637), (34.7869, 114.3621), (IN_S - 0.0007, 114.3608), (IN_S - 0.0007, 114.3259), (34.7952, 114.3261),
                   (34.8018, 114.3271), (34.8124, 114.3289), (IN_N + 0.0007, 114.3292)]

CITY = dict(
    name="Kaifeng", subtitle="Bianzhou, Dongjing of the Song, and the City under the Silt",
    description="Kaifeng on the Bian canal from the Tang prefectural town of Bianzhou to the Qing city rebuilt over the silt of 1642: the Song inner city and palace, the Imperial Way, the eastern and southern wards of the outer city, the Bian out toward the Rainbow Bridge, the Iron and Fan pagodas. The Song outer wall's north side and the western suburbs lie beyond the frame. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="song-1120",
    world=dict(heightScale=1.0, walls=["#DCCDB0", "#D2C1A0", "#C6B492"], roofs=["#5E5F62", "#686664", "#57595C"]),
    camera=dict(target=(34.7985, 114.3500), distance=46),
)
FRAME = ((NORTH, WEST), (SOUTH, EAST))
PALETTE = dict(parchment="#E8D6AE", ink="#5C4434", water="#62878A", hill="#7A7D58", road="#8C6C4C")
COMPASS = (34.8212, 114.3858)
CARTOUCHE = (34.7646, 114.3076)

PERIODS = [
    dict(id="tang-800", label="Bianzhou on the Grand Canal", year=800, startYear=618, endYear=906,
         summary="A prefectural city where the Tongji canal, the Sui Grand Canal's main stem, met the roads of the plain: grain barges from the Huai and the Yangzi passed through on their way to Luoyang and Chang'an. In 781 the governor Li Mian rebuilt its rammed-earth walls, some 20 li round. The Xuanwu army's headquarters stood where the Song palace would be; Xiangguo temple was named in 712.",
         population="perhaps 100,000 or more (no reliable figure)",
         feel="Barge haulers chanting on the towpath, grain dust at the transfer granaries, and drums from the governor's yamen at dusk.",
         style="sinic",
         houses=dict(title="Wards of a canal town", text="Inside the walls, lanes of rammed-earth courtyard houses under grey tile and thatch, still grouped in walled wards with gates shut at night. Inns, granaries and boatmen's quarters crowd the canal banks."),
         outskirts=dict(title="Fields of the Bian plain", text="Wheat and millet on the flat yellow loam, hamlets of earth houses along the canal and the roads to Zhengzhou and Song, willows on the towpath.")),
    dict(id="song-1120", label="Dongjing, the Northern Song capital", year=1120, startYear=907, endYear=1127,
         summary="Capital of four Five Dynasties houses and, from 960, of the Song: three nested walls, the outer some 29 km round, four canals bringing the grain of the south. Perhaps a million people. The ward walls are gone: shops open onto the streets, markets run all night, and teahouses, taverns and theatres crowd the city of Zhang Zeduan's scroll. Emperor Huizong builds the Genyue garden.",
         population="perhaps 1,000,000 (estimates 0.5–1.5 million)",
         feel="Lanterns over the Ma Xing street night market, the smell of coal smoke and roast mutton, drums from the theatres and boatmen shouting under the Rainbow Bridge.",
         style="sinic",
         houses=dict(title="Shophouses open to the street", text="No ward walls now: narrow two-storey shophouses of timber and plaster stand gable to gable along the streets, with open fronts, awnings, shop signs and tavern flags. Behind them, family courtyards and workshops; tile for the rich, thatch and boards for the poor."),
         outskirts=dict(title="Market gardens and canal hamlets", text="Between the walls and beyond: vegetable plots, orchards, grave mounds and the villas of officials, with hamlets of inns and warehouses on the canals.")),
    dict(id="jin-1200", label="Nanjing (Bianjing) of the Jin", year=1200, startYear=1128, endYear=1233,
         summary="The Jurchens took the city in 1127 and carried off two emperors and the court. Under the Jin it was the 'Southern Capital': Prince Hailing rebuilt the palace in the 1150s, but Song money, scholars and trade had gone south. In 1214 the Jin court fled here from the Mongols, and in 1232–1233 the city was starved and stormed after a long siege.",
         population="perhaps 200,000–400,000, swollen by refugees after 1214",
         feel="Jurchen horsemen in the empty streets of the outer city, weeds in the old theatres, and after 1214 the crush of refugees and soldiers.",
         style="sinic",
         houses=dict(title="Patched houses of the inner city", text="Life withdraws into the inner city: Song shophouses patched and subdivided, Jurchen officials in the old mansions, temples kept up by fewer monks."),
         outskirts=dict(title="The empty outer city", text="Burnt and abandoned blocks between the walls go back to vegetable gardens and fields; soldiers camp in deserted compounds.")),
    dict(id="ming-1600", label="Ming Kaifeng and the Prince of Zhou", year=1600, startYear=1368, endYear=1642,
         summary="The Ming made Kaifeng the capital of Henan and the seat of the Prince of Zhou, whose vast palace covered the old Song-Jin palace site. The walls were rebuilt and faced in brick, the city ringed by Yellow River dykes. Kaifeng was rich: merchants from Shanxi and Huizhou, a Jewish congregation with its synagogue, princely gardens. In 1642 the dykes were cut during Li Zicheng's siege.",
         population="perhaps 300,000–400,000 before 1642",
         feel="Bells from the Zhou palace, silk and medicine shops round the Drum Tower, carts on the brick-paved main streets, and the Yellow River always higher than the roofs.",
         style="sinic",
         houses=dict(title="Courtyard houses of the Ming city", text="Grey-brick quadrangle houses behind blank walls and gate towers line straight lanes off the main streets; princely kinsmen, officials and merchants hold the big compounds, shopkeepers live over their shops on the Drum Tower streets."),
         outskirts=dict(title="Suburbs and dyked fields", text="Outside the gates, suburbs (guan) of inns and carters; beyond, wheat fields on the old Song city, behind the ring dyke against the Yellow River.")),
    dict(id="qing-1700", label="Qing Kaifeng over the silt", year=1700, startYear=1643, endYear=1840,
         summary="The flood of 1642 buried the Ming city under metres of silt and drowned most of its people. The Qing rebuilt the walls on the old line in the 1660s, but the city inside was half empty: lakes in the hollows of the Zhou palace, fields within the walls. In 1692 a pavilion was raised on the palace's old Coal Hill, the later Dragon Pavilion.",
         population="perhaps 50,000–100,000 (no reliable figure)",
         feel="Reed beds and fishing boats in the palace lakes, cattle grazing inside the walls, and the bells of the rebuilt Xiangguo temple.",
         style="sinic",
         houses=dict(title="Rebuilt courtyards on the silt", text="One-storey brick and adobe courtyard houses rebuilt on the silt over the Ming city, thickest along the streets from the Drum Tower to the Song gate and round Xiangguo temple."),
         outskirts=dict(title="Flood-silt fields", text="Inside and outside the walls, fields of sandy flood silt: wheat, peanuts, jujube trees and ponds left in the low ground, where the Ming city lies buried some metres down.")),
]

# ---------------------------------------------------------------- water and hills
BIAN_IN = [(34.7948, WEST), (34.7948, OUT_W), (34.7935, 114.3268), (34.7922, 114.3380), ZHOUQIAO, (34.7898, 114.3490), (34.7883, 114.3540), (34.7857, 114.3604)]
BIAN_OUT = [(34.7857, 114.3604), (34.7848, 114.3680), (34.7845, 114.3740), (34.7860, OUT_E), (34.7855, 114.3868), (34.7850, EAST + 0.002)]

WATER = [
    dict(id="bian", name="Bian river (Tongji canal)", width=38, periods=EARLY, path=BIAN_IN + BIAN_OUT[1:],
         blurb="The Sui Tongji canal of 605, the Grand Canal's main stem, drawing Yellow River water south-east to the Huai. Under the Song some six million shi of grain a year came up it to the capital, past the Zhou bridge and Xiangguo temple."),
    dict(id="bian-ming", name="Old bed of the Bian", width=14, periods=MING,
         path=[(34.7935, 114.3268), (34.7922, 114.3380), ZHOUQIAO, (34.7898, 114.3490), (34.7883, 114.3540), (34.7857, 114.3604)],
         blurb="After the Jin the Bian silted up and was cut off from the Yellow River; inside the Ming city only a drain ran in its bed under the old Zhou bridge."),
    dict(id="cai", name="Cai river (Huimin)", width=24, periods=EARLY,
         path=[(34.7712, WEST), (34.7716, OUT_W), (34.7735, 114.3300), (34.7745, 114.3440), (34.7740, 114.3600), (34.7712, 114.3740), (34.7690, 114.3800), (OUT_S, 114.3815), (SOUTH, 114.3830)],
         blurb="The Huimin or Cai river curved through the southern outer city under thirteen bridges, among them the Longjin bridge on the Imperial Way, carrying boats from the south-west and the Huai."),
    dict(id="wuzhang", name="Wuzhang river (Guangji)", width=20, periods=EARLY,
         path=[(34.8236, WEST), (34.8228, 114.3200), (34.8212, 114.3400), (34.8205, 114.3545), (34.8215, 114.3700), (34.8228, OUT_E), (34.8232, EAST)],
         blurb="The 'Five-zhang' canal (about 15 m wide, as its name says), fed from the Jinshui, carried grain from Shandong into the north of the outer city. Its line here is the usual reconstruction; a modern stream follows it."),
    dict(id="jinshui", name="Jinshui river", width=12, periods=SONGJIN,
         path=[(34.8140, WEST), (34.8140, OUT_W), (34.8128, 114.3298), (34.8112, 114.3380), (34.8100, PAL_W)],
         blurb="The 'Golden Water' canal brought clean water from the hills west of Zhengzhou across the Bian in an aqueduct and into the palace pools; its overflow joined the Wuzhang."),
    dict(id="song-inner-moat", name="Moat of the inner city", width=22, periods=EARLY, path=SONG_INNER_MOAT,
         blurb="The inner city's moat, fed by the canals."),
    dict(id="song-outer-moat-e", name="Moat of the outer city (Hulong river)", width=30, periods=SONGJIN,
         path=[(NORTH + 0.003, OUT_E + 0.0005), (34.7860, OUT_E + 0.0005), (OUT_S - 0.0005, OUT_E + 0.0005), (OUT_S - 0.0005, OUT_W - 0.0005), (NORTH + 0.003, OUT_W - 0.0005)],
         blurb="The Hulong ('Dragon-Guarding') river, the outer city's moat, about ten zhang (some 30 m) wide, lined with willows and elms on both banks; no one was allowed to walk on its banks."),
    dict(id="ming-moat", name="City moat", width=26, periods=LATE, path=MQ_MOAT,
         blurb="The moat round the Ming and Qing walls; in the Qing it was partly a string of ponds."),
    dict(id="yang-lake", name="Yang family lake", width=250, periods=QING, path=[(34.8072, 114.3444), (34.8052, 114.3446)],
         blurb="One of the two lakes south of the Dragon Pavilion, formed after the flood of 1642 in the hollows of the drowned Zhou palace. Its water is said to be clear; tradition gives it to the loyal Yang family of generals."),
    dict(id="pan-lake", name="Pan family lake", width=250, periods=QING, path=[(34.8072, 114.3480), (34.8052, 114.3479)],
         blurb="The eastern lake by the causeway to the Dragon Pavilion, said to be murky, after the treacherous minister Pan Renmei of the operas. Both lakes date from after 1642."),
    dict(id="baogong-lake", name="Baogong lake", width=260, periods=QING, path=[(34.7950, 114.3345), (34.7915, 114.3362), (34.7885, 114.3390)],
         blurb="A lake left in the low south-west of the city by the flood of 1642, later named after the upright Song judge Bao Zheng."),
]

HILLS = [
    dict(id="genyue-hill", name="Wansui Mountain (Genyue)", center=(34.8110, 114.3590), radius=150, periods=SONG,
         blurb="The 'Mountain of Ten Thousand Years' raised by Huizong's builders from 1117 in the north-east of the inner city, with rocks shipped from Lake Tai on the 'Flower and Rock Convoys'. The usual figure for its height is about 90 chi, some 28 m."),
    dict(id="fantai", name="Fan terrace", center=(34.7706, 114.3588), radius=90,
         blurb="A low mound in the south-east, named after the Fan family who lived round it; the Tianqing temple and its pagoda stood on it."),
    dict(id="coal-hill", name="Coal Hill of the Zhou palace", center=(34.8098, 114.3466), radius=80, periods=LATE,
         blurb="The artificial hill at the back of the Zhou prince's palace. It stood above the silt of 1642, and the Qing built a pavilion on it in 1692, the later Dragon Pavilion."),
]

# ---------------------------------------------------------------- roads
ROADS = [
    # ---- the Song and Jin capital
    dict(id="yujie", name="Imperial Way (Yujie)", path=[XUANDE, ZHOUQIAO, ZHUQUE, (34.7745, 114.3440), NANXUN_OUT, (SOUTH, 114.3436)], width=40, style="major", labelled=True, periods=SONGJIN,
         blurb="The ceremonial avenue south from the palace's Xuande gate, 'some two hundred paces wide' near the palace, with brick-lined channels planted with lotus, peach and plum, and red and black lacquered fences keeping commoners off the emperor's lane in the middle."),
    dict(id="palace-front", name="Street before the palace", path=[(34.8020, 114.3280), (34.8028, 114.3400), (34.8028, 114.3620), (34.8007, 114.3661), (34.8030, 114.3690), (34.8030, OUT_E), (34.8032, EAST)], width=26, style="major", labelled=True, periods=SONGJIN,
         blurb="The east-west street before the Xuande gate, from the Liang gate in the west to the old Cao gate and on to the New Cao gate of the outer city; east of the palace it ran past the Pan Tower and the Sangjia entertainment quarter."),
    dict(id="maxing", name="Ma Xing Street", path=[(34.8028, 114.3545), (IN_N, 114.3545), (NORTH, 114.3545)], width=20, labelled=True, periods=SONGJIN,
         blurb="The 'Horse Traders' Street' north from the Pan Tower crossroads to the New Fengqiu gate, the liveliest night market of the capital: Cai Tao wrote that its lamp-oil smoke kept the mosquitoes away."),
    dict(id="east-street", name="Street of the Old Song Gate", path=[(34.7915, 114.3466), (34.7907, 114.3488), (34.7898, 114.3560), (34.7876, 114.3613), (34.7880, 114.3740), (34.7895, OUT_E), (34.7895, EAST)], width=22, style="major", labelled=True, periods=SONGJIN,
         blurb="From the Zhou bridge past Xiangguo temple to the old Song gate (Lizhe) of the inner city and on to the New Song gate of the outer city, the road to Song prefecture and the east. The scroll's city gate may be one of the gates on it."),
    dict(id="west-street", name="Street to the New Zheng Gate", path=[(34.7920, 114.3452), (34.7945, 114.3300), (34.7965, OUT_W), (34.7965, WEST)], width=20, labelled=True, periods=SONGJIN,
         blurb="West along the north bank of the Bian to the old Zheng gate and the New Zheng gate (Shuntian) of the outer city, outside which lay the Jinming pond of the imperial boating festivals."),
    dict(id="liang-road", name="Road from the Liang Gate", path=[(34.8020, 114.3280), (34.8020, OUT_W), (34.8020, WEST)], width=16, periods=SONGJIN),
    dict(id="baokang", name="Baokang Gate Street", path=[(34.7905, 114.3540), (IN_S, 114.3540), (34.7755, 114.3545), (OUT_S, 114.3560), (SOUTH, 114.3565)], width=16, labelled=True, periods=SONGJIN,
         blurb="South from the Bian through the Baokang gate toward the Chen prefecture gate; the Fan terrace and the Tianqing temple lay just to the east."),
    dict(id="fengqiu-west", name="Street west of the palace", path=[(34.8028, 114.3400), (IN_N, 114.3400), (NORTH, 114.3400)], width=16, periods=SONGJIN),
    dict(id="outer-east-n", name="Road in the east outer city", path=[(34.8030, 114.3760), (34.7895, 114.3760)], width=12, periods=SONGJIN),
    # ---- Tang Bianzhou
    dict(id="tang-axis", name="Street before the governor's yamen", path=[(34.8035, 114.3465), ZHOUQIAO, ZHUQUE, (34.7745, 114.3440), (SOUTH, 114.3436)], width=24, style="major", labelled=True, periods=TANG,
         blurb="The street south from the gate of the Xuanwu military governor's compound across the Zhou bridge to the south gate, the line the Song would widen into the Imperial Way."),
    dict(id="tang-ew", name="East-west street", path=[(34.8020, WEST), (34.8020, 114.3280), (34.8028, 114.3465), (34.8028, 114.3620), (34.8007, 114.3661), (34.8015, EAST)], width=18, labelled=True, periods=TANG),
    dict(id="tang-canal-road", name="Canal street", path=[(34.7965, WEST), (34.7945, 114.3300), (34.7920, 114.3452), (34.7907, 114.3488), (34.7898, 114.3560), (34.7876, 114.3613), (34.7880, 114.3740), (34.7880, EAST)], width=14, labelled=True, periods=TANG,
         blurb="The towpath and street along the Bian, through the west and east gates: the road of the barge haulers and the grain convoys."),
    dict(id="tang-north", name="North street", path=[(34.8028, 114.3545), (IN_N, 114.3545), (NORTH, 114.3545)], width=12, periods=TANG),
    # ---- the Ming and Qing city
    dict(id="ming-axis", name="Street before the Zhou palace", path=[(34.8030, 114.3465), ZHOUQIAO, NANXUN_MING], width=22, style="major", labelled=True, periods=MING,
         blurb="The old Imperial Way, now the street from the Zhou palace's south gate to the Nanxun gate, lined with the offices of the province and the shops of the Drum Tower quarter."),
    dict(id="qing-axis", name="South Gate Street", path=[(34.8088, 114.3463), (34.8030, 114.3463), ZHOUQIAO, NANXUN_MING], width=18, style="major", labelled=True, periods=QING,
         blurb="From the Dragon Pavilion along the causeway between the two lakes and south on the line of the Song Imperial Way to the South gate; the modern Zhongshan Road."),
    dict(id="mq-ew", name="Daliang Gate - Cao Gate street", path=[(34.8018, 114.3280), (34.8020, 114.3400), (34.8018, 114.3530), (34.8007, 114.3661)], width=20, style="major", labelled=True, periods=LATE,
         blurb="The main east-west street, from the Daliang gate in the west to the Renhe (Cao) gate in the east."),
    dict(id="mq-songmen", name="Song Gate Street", path=[(34.7947, 114.3500), (34.7930, 114.3520), (34.7876, 114.3613)], width=16, labelled=True, periods=LATE,
         blurb="From the Drum Tower south-east to the Lijing gate, still called the Song gate after its Song predecessor."),
    dict(id="mq-gulou", name="Drum Tower Street", path=[(34.7947, 114.3462), (34.7947, 114.3500), (34.8018, 114.3500)], width=14, labelled=True, periods=LATE),
    dict(id="mq-north", name="North Gate Street", path=[(34.8192, 114.3573), (34.8120, 114.3560), (34.8018, 114.3560)], width=14, labelled=True, periods=LATE),
    dict(id="mq-west", name="Street by the Yanqing temple", path=[(34.8018, 114.3380), (34.7900, 114.3380), (34.7852, 114.3381)], width=10, periods=LATE),
    dict(id="mq-east-road", name="Road east from the Cao gate", path=[(34.8007, 114.3670), (34.8015, 114.3760), (34.8015, EAST)], width=10, periods=LATE),
    dict(id="mq-song-road", name="Road east from the Song gate", path=[(34.7876, 114.3622), (34.7872, 114.3740), (34.7880, EAST)], width=10, periods=LATE),
    dict(id="mq-south-road", name="Road to the Fan pagoda", path=[(34.7820, 114.3440), (34.7760, 114.3500), (34.7730, 114.3560)], width=8, periods=LATE),
    dict(id="mq-west-road", name="Road west from the Daliang gate", path=[(34.8018, 114.3270), (34.8010, WEST)], width=10, periods=LATE),
    dict(id="mq-north-road", name="Road to the Yellow River", path=[(34.8205, 114.3573), (NORTH, 114.3580)], width=10, periods=LATE),
]

WALLS = [
    dict(id="song-outer-wall", name="Outer wall (Waicheng, the 'New City')", periods=SONGJIN,
         path=[(NORTH + 0.004, OUT_E), (OUT_S, OUT_E), (OUT_S, OUT_W), (NORTH + 0.004, OUT_W)],
         blurb="Begun in 955 by Emperor Shizong of the Later Zhou and rebuilt higher in 1075–1078: about 29 km round, rammed earth, with barbicans, 'horse-face' bastions every hundred paces and water gates where the canals entered. Its line here is the usual reconstruction; the north side lies beyond the frame."),
    dict(id="song-inner-wall", name="Inner wall (Licheng, the 'Old City')", closed=True, periods=EARLY, path=SONG_INNER,
         blurb="The wall of Bianzhou, rebuilt by the governor Li Mian in 781 at about 20 li round, which became the Song inner city. The Ming wall follows it in the east, south and west; its north side is the usual reconstruction."),
    dict(id="palace-wall", name="Palace city wall (Danei)", closed=True, periods=SONGJIN, path=R(PAL_N, PAL_S, PAL_W, PAL_E),
         blurb="The palace city, about 5 li round, grown from the Tang governor's compound: red-plastered walls with corner towers and the Xuande, Donghua, Xihua and Gongchen gates. The palace lay under the later Zhou palace and the lakes."),
    dict(id="mq-wall", name="City wall", closed=True, periods=LATE, path=MQ_WALL,
         blurb="Rebuilt in 1368–1378 on the Jin wall, which had extended the Song inner city to the north, and faced in brick. Buried and breached in 1642, rebuilt in the 1660s and again after the flood of 1841; the brick wall still stands, about 14 km round."),
    dict(id="zhou-outer-wall", name="Outer wall of the Zhou palace", closed=True, periods=MING, path=R(34.8135, 34.8032, 114.3398, 114.3532),
         blurb="The 'screen wall' (xiaoqiang) round the Prince of Zhou's palace and its gardens, said to be some 9 li round; its exact line is not known."),
    dict(id="zhou-inner-wall", name="Inner wall of the Zhou palace", closed=True, periods=MING, path=R(34.8108, 34.8048, 114.3436, 114.3496),
         blurb="The 'forbidden city' of the princely palace, with its own moat."),
    dict(id="ring-dyke", name="Ring dyke (on the old outer wall)", periods=LATE,
         path=[(NORTH + 0.004, OUT_E), (OUT_S, OUT_E), (OUT_S, OUT_W), (NORTH + 0.004, OUT_W)],
         blurb="The ruined Song outer wall survived as an earth bank, probably kept up as a dyke round the city against the Yellow River floods, which came ever closer as the river bed rose."),
]

GATES = [
    # Song inner city
    dict(id="zhuque-gate", name="Zhuque gate", position=ZHUQUE, periods=SONGJIN),
    dict(id="baokang-gate", name="Baokang gate", position=(IN_S, 114.3540), periods=SONGJIN),
    dict(id="xin-gate", name="Xin gate", position=(IN_S, 114.3360), periods=SONGJIN),
    dict(id="lizhe-gate", name="Lizhe gate (old Song gate)", position=(34.7876, 114.3613), periods=SONGJIN),
    dict(id="wangchun-gate", name="Wangchun gate (old Cao gate)", position=(34.8007, 114.3661), periods=SONGJIN),
    dict(id="changhe-gate", name="Changhe gate (Liang gate)", position=(34.8020, 114.3280), periods=SONGJIN),
    dict(id="jinglong-gate", name="Jinglong gate (old Fengqiu gate)", position=(IN_N, 114.3545), periods=SONGJIN),
    # Song outer city
    dict(id="xinsong-gate", name="New Song gate (Chaoyang)", position=(34.7895, OUT_E), periods=SONGJIN),
    dict(id="east-water-gate", name="East water gate", position=(34.7860, OUT_E), periods=SONGJIN),
    dict(id="xincao-gate", name="New Cao gate (Hanhui)", position=(34.8030, OUT_E), periods=SONGJIN),
    dict(id="nanxun-gate", name="Nanxun gate", position=NANXUN_OUT, periods=SONGJIN),
    dict(id="chenzhou-gate", name="Chen prefecture gate (Xuanhua)", position=(OUT_S, 114.3560), periods=SONGJIN),
    dict(id="dailou-gate", name="Dailou gate (Anshang)", position=(OUT_S, 114.3250), periods=SONGJIN),
    dict(id="xinzheng-gate", name="New Zheng gate (Shuntian)", position=(34.7965, OUT_W), periods=SONGJIN),
    dict(id="west-water-gate", name="West water gate", position=(34.7948, OUT_W), periods=SONGJIN),
    dict(id="wansheng-gate", name="Wansheng gate", position=(34.8020, OUT_W), periods=SONGJIN),
    # Tang Bianzhou
    dict(id="tang-south-gate", name="South gate", position=ZHUQUE, periods=TANG),
    dict(id="tang-east-gate", name="East gate", position=(34.7876, 114.3613), periods=TANG),
    dict(id="tang-west-gate", name="West gate", position=(34.8020, 114.3280), periods=TANG),
    dict(id="tang-north-gate", name="North gate", position=(IN_N, 114.3545), periods=TANG),
    # Ming and Qing
    dict(id="daliang-gate", name="Daliang gate (West gate)", position=(34.8018, 114.3280), periods=LATE),
    dict(id="anyuan-gate", name="Anyuan gate (North gate)", position=(34.8192, 114.3573), periods=LATE),
    dict(id="renhe-gate", name="Renhe gate (Cao gate)", position=(34.8007, 114.3661), periods=LATE),
    dict(id="lijing-gate", name="Lijing gate (Song gate)", position=(34.7876, 114.3613), periods=LATE),
    dict(id="nanxun-ming", name="Nanxun gate (South gate)", position=NANXUN_MING, periods=LATE),
]

BRIDGES = [
    dict(id="zhouqiao-bridge", name="Zhou bridge", path=[(34.7918, 114.3460), (34.7906, 114.3458)], build="stone", arches=3, landmarkId="zhouqiao", periods=EARLY,
         blurb="The bridge of the prefecture (zhou), officially the Tianhan bridge, where the Imperial Way crossed the Bian."),
    dict(id="xiangguo-bridge", name="Xiangguo temple bridge", path=[(34.7905, 114.3500), (34.7892, 114.3498)], build="stone", arches=1, periods=SONGJIN,
         blurb="The bridge by Xiangguo temple, a low flat bridge like the Zhou bridge, so low that only flat-roofed boats could pass under it."),
    dict(id="rainbow-bridge-b", name="Rainbow Bridge (Hongqiao)", path=[(34.7862, 114.3868), (34.7848, 114.3868)], build="timber", arches=1, landmarkId="rainbow-bridge", periods=SONG,
         blurb="A pierless timber arch over the Bian east of the city, the centrepiece of Zhang Zeduan's scroll."),
    dict(id="shang-tu-bridge", name="Shangtu bridge", path=[(34.7858, 114.3780), (34.7840, 114.3780)], build="timber", arches=1, periods=SONGJIN,
         blurb="Another of the arched 'flying bridges' over the Bian inside the outer city, beside the grain wharves."),
    dict(id="longjin-bridge", name="Longjin bridge", path=[(34.7752, 114.3440), (34.7738, 114.3440)], build="stone", arches=3, periods=SONGJIN,
         blurb="The bridge of the Imperial Way over the Cai river, between the Zhuque and Nanxun gates."),
    dict(id="tang-east-bridge", name="Canal bridge", path=[(34.7858, 114.3780), (34.7840, 114.3780)], build="stone", arches=3, periods=TANG),
]

# ---------------------------------------------------------------- built-up areas
# inner-city pieces shared by the Tang, Song and Jin eras (between the Bian, the Imperial Way and the main streets)
_INNER_SW = R(34.7905, IN_S + 0.0005, 114.3285, 114.3445)
_INNER_SE = [(34.7895, 114.3475), (34.7877, 114.3532), (IN_S + 0.0005, 114.3532), (IN_S + 0.0005, 114.3475)]
_INNER_SE2 = [(34.7872, 114.3548), (34.7863, 114.3570), (IN_S + 0.0005, 114.3585), (IN_S + 0.0005, 114.3548)]
_INNER_W = [(34.8012, 114.3292), (34.8012, 114.3448), (34.7930, 114.3448), (34.7953, 114.3292)]
_INNER_E = [(34.8012, 114.3478), (34.8012, 114.3640), (34.7985, 114.3632), (34.7914, 114.3618), (34.7886, 114.3606), (34.7903, 114.3560), (34.7920, 114.3478)]
_INNER_NW_S = [(34.8115, 114.3310), (34.8100, 114.3392), (34.8037, 114.3392), (34.8037, 114.3310)]
_INNER_NW_N = [(IN_N - 0.0006, 114.3310), (IN_N - 0.0006, 114.3392), (34.8122, 114.3392), (34.8138, 114.3310)]
_INNER_NE = R(IN_N - 0.0006, 34.8037, 114.3510, 114.3538)
_INNER_NE2 = R(34.8088, 34.8037, 114.3553, 114.3650)
_INNER_N = R(IN_N - 0.0006, PAL_N + 0.0005, 114.3425, 114.3505)
# Ming-Qing pieces (between the Ming main streets)
_MQ_SWA = R(34.7915, 34.7868, 114.3292, 114.3372)
_MQ_SWB = R(34.7905, 34.7850, 114.3390, 114.3436)
_MQ_WA = R(34.8008, 34.7940, 114.3292, 114.3372)
_MQ_WB = R(34.8008, 34.7930, 114.3390, 114.3448)
_MQ_DT1 = R(34.8008, 34.7955, 114.3472, 114.3492)
_MQ_DT2 = [(34.8008, 114.3508), (34.8008, 114.3552), (34.7920, 114.3552), (34.7937, 114.3520), (34.7952, 114.3508)]
_MQ_DT3 = [(34.8000, 114.3568), (34.8000, 114.3640), (34.7985, 114.3634), (34.7914, 114.3620), (34.7890, 114.3606), (34.7910, 114.3568)]
_MQ_DT4 = [(34.7940, 114.3470), (34.7928, 114.3515), (34.7889, 114.3580), (34.7870, 114.3580), (34.7887, 114.3540), (34.7902, 114.3490), (34.7911, 114.3470)]
_MQ_DT5 = [(34.7900, 114.3462), (34.7890, 114.3490), (34.7875, 114.3540), (34.7852, 114.3590), (34.7836, 114.3578), (34.7840, 114.3460)]
_MQ_NW = [(34.8180, 114.3375), (34.8122, 114.3330), (34.8030, 114.3300), (34.8030, 114.3388), (34.8180, 114.3388)]
_MQ_NEA = R(34.8175, 34.8028, 114.3540, 114.3552)
_MQ_NEB = [(34.8175, 114.3578), (34.8175, 114.3665), (34.8055, 114.3652), (34.8028, 114.3652), (34.8028, 114.3570)]

BLOCKS = [
    # ---- Song: the inner city
    dict(name="Inner city south of the Bian (west)", polygon=_INNER_SW, density="dense", periods=SONG),
    dict(name="Inner city south of the Bian (east)", polygon=_INNER_SE, density="dense", periods=SONG),
    dict(name="Inner city south of the Bian (by the Baokang gate)", polygon=_INNER_SE2, density="dense", periods=SONG),
    dict(name="Inner city west of the Imperial Way", polygon=_INNER_W, density="dense", periods=SONG),
    dict(name="Xiangguo temple quarter", polygon=_INNER_E, density="dense", periods=SONG),
    dict(name="North-west inner city", polygon=_INNER_NW_S, density="dense", periods=SONG),
    dict(name="North-west inner city (by the wall)", polygon=_INNER_NW_N, density="dense", periods=SONG),
    dict(name="Ma Xing Street quarter", polygon=_INNER_NE, density="dense", periods=SONG),
    dict(name="Pan Tower quarter", polygon=_INNER_NE2, density="dense", periods=SONG),
    dict(name="Behind the palace", polygon=_INNER_N, density="loose", periods=SONG),
    # ---- Song: the outer city
    dict(name="West outer city (north)", polygon=R(34.8122, 34.8030, 114.3115, 114.3255), density="dense", periods=SONG),
    dict(name="West outer city (by the Bian)", polygon=R(34.7928, 34.7780, 114.3115, 114.3255), density="dense", periods=SONG),
    dict(name="South outer city (west)", polygon=R(34.7822, 34.7756, 114.3268, 114.3428), density="dense", periods=SONG),
    dict(name="South outer city (east)", polygon=R(34.7822, 34.7756, 114.3455, 114.3532), density="dense", periods=SONG),
    dict(name="South outer city (by the Baokang street)", polygon=R(34.7822, 34.7752, 114.3555, 114.3640), density="dense", periods=SONG),
    dict(name="Beyond the Cai (west)", polygon=R(34.7722, 34.7690, 114.3310, 114.3428), density="loose", periods=SONG),
    dict(name="Beyond the Cai (east)", polygon=R(34.7728, 34.7690, 114.3455, 114.3550), density="loose", periods=SONG),
    dict(name="East outer city (north)", polygon=R(34.8140, 34.8040, 114.3700, 114.3835), density="dense", periods=SONG),
    dict(name="East outer city (Old Song gate)", polygon=R(34.8020, 34.7905, 114.3690, 114.3752), density="dense", periods=SONG),
    dict(name="East outer city (New Song gate)", polygon=R(34.8020, 34.7905, 114.3768, 114.3835), density="dense", periods=SONG),
    dict(name="South-east outer city", polygon=R(34.7832, 34.7748, 114.3655, 114.3835), density="dense", periods=SONG),
    dict(name="North outer city", polygon=R(34.8198, 34.8166, 114.3115, 114.3392), density="dense", periods=SONG),
    dict(name="North outer city (by Ma Xing Street)", polygon=R(34.8198, 34.8166, 114.3408, 114.3535), density="dense", periods=SONG),
    dict(name="Kaibao temple quarter", polygon=R(34.8198, 34.8180, 114.3555, 114.3640), density="dense", periods=SONG),
    dict(name="North-east outer city", polygon=R(34.8198, 34.8158, 114.3700, 114.3835), density="dense", periods=SONG),
    dict(name="Inns outside the east gates", polygon=R(34.7925, 34.7905, 114.3858, 114.3878), density="loose", periods=SONG),
    dict(name="Villages outside the west wall", polygon=R(34.8100, 34.8030, 114.3074, 114.3090), density="loose", periods=SONG),

    # ---- Tang Bianzhou: dense round the yamen and along the canal, thinner toward the walls; canal hamlets outside
    dict(name="Wards by the canal (west)", polygon=_INNER_SW, density="dense", periods=TANG),
    dict(name="Wards by the canal (east)", polygon=_INNER_SE, density="dense", periods=TANG),
    dict(name="Wards by the canal (south-east)", polygon=_INNER_SE2, density="dense", periods=TANG),
    dict(name="Wards west of the yamen street", polygon=_INNER_W, density="dense", periods=TANG),
    dict(name="Wards round Xiangguo temple", polygon=_INNER_E, density="dense", periods=TANG),
    dict(name="North-west wards", polygon=_INNER_NW_S, density="loose", periods=TANG),
    dict(name="North-east wards", polygon=_INNER_NE2, density="loose", periods=TANG),
    dict(name="Canal hamlet outside the east gate", polygon=R(34.7908, 34.7886, 114.3640, 114.3760), density="loose", periods=TANG),
    dict(name="Canal hamlet outside the west gate", polygon=R(34.7990, 34.7972, 114.3150, 114.3250), density="loose", periods=TANG),
    dict(name="Hamlet by the Fan terrace", polygon=R(34.7735, 34.7718, 114.3540, 114.3600), density="loose", periods=TANG),

    # ---- Jin: the inner city still lived in, the outer city thinning
    dict(name="Inner city south of the Bian (west)", polygon=_INNER_SW, density="dense", periods=JIN),
    dict(name="Inner city south of the Bian (east)", polygon=_INNER_SE, density="dense", periods=JIN),
    dict(name="Inner city south of the Bian (by the Baokang gate)", polygon=_INNER_SE2, density="dense", periods=JIN),
    dict(name="Inner city west of the Imperial Way", polygon=_INNER_W, density="dense", periods=JIN),
    dict(name="Xiangguo temple quarter", polygon=_INNER_E, density="dense", periods=JIN),
    dict(name="North-west inner city", polygon=_INNER_NW_S, density="loose", periods=JIN),
    dict(name="Ma Xing Street quarter", polygon=_INNER_NE, density="loose", periods=JIN),
    dict(name="Pan Tower quarter", polygon=_INNER_NE2, density="loose", periods=JIN),
    dict(name="South outer city", polygon=R(34.7822, 34.7756, 114.3268, 114.3428), density="loose", periods=JIN),
    dict(name="South outer city (east)", polygon=R(34.7822, 34.7756, 114.3455, 114.3532), density="loose", periods=JIN),
    dict(name="East outer city", polygon=R(34.8020, 34.7905, 114.3690, 114.3752), density="loose", periods=JIN),
    dict(name="East outer city (New Song gate)", polygon=R(34.8020, 34.7905, 114.3768, 114.3835), density="loose", periods=JIN),
    dict(name="West outer city", polygon=R(34.7928, 34.7840, 114.3115, 114.3255), density="loose", periods=JIN),
    dict(name="Kaibao temple quarter", polygon=R(34.8198, 34.8180, 114.3555, 114.3640), density="loose", periods=JIN),

    # ---- Ming Kaifeng inside its brick wall, with suburbs at the gates
    dict(name="South-west quarter", polygon=_MQ_SWA, density="dense", periods=MING),
    dict(name="South-west quarter (by the South gate)", polygon=_MQ_SWB, density="dense", periods=MING),
    dict(name="West quarter", polygon=_MQ_WA, density="dense", periods=MING),
    dict(name="West quarter (by the main street)", polygon=_MQ_WB, density="dense", periods=MING),
    dict(name="Drum Tower quarter (west)", polygon=_MQ_DT1, density="dense", periods=MING),
    dict(name="Drum Tower quarter", polygon=_MQ_DT2, density="dense", periods=MING),
    dict(name="East quarter", polygon=_MQ_DT3, density="dense", periods=MING),
    dict(name="Xiangguo temple quarter", polygon=_MQ_DT4, density="dense", periods=MING),
    dict(name="South-east quarter", polygon=_MQ_DT5, density="dense", periods=MING),
    dict(name="North-west quarter", polygon=_MQ_NW, density="dense", periods=MING),
    dict(name="North-east quarter (by the North Gate street)", polygon=_MQ_NEA, density="dense", periods=MING),
    dict(name="North-east quarter", polygon=_MQ_NEB, density="dense", periods=MING),
    dict(name="Lanes north of the Zhou palace", polygon=R(34.8186, 34.8145, 114.3400, 114.3535), density="dense", periods=MING),
    dict(name="East suburb (Song gate)", polygon=R(34.7905, 34.7882, 114.3645, 114.3760), density="dense", periods=MING),
    dict(name="East suburb (south of the road)", polygon=R(34.7864, 34.7838, 114.3640, 114.3740), density="loose", periods=MING),
    dict(name="East suburb (Cao gate)", polygon=R(34.8045, 34.8022, 114.3685, 114.3760), density="loose", periods=MING),
    dict(name="East suburb (south of the Cao gate road)", polygon=R(34.8000, 34.7975, 114.3685, 114.3760), density="loose", periods=MING),
    dict(name="South suburb", polygon=R(34.7808, 34.7780, 114.3380, 114.3432), density="loose", periods=MING),
    dict(name="West suburb", polygon=R(34.8045, 34.8022, 114.3170, 114.3245), density="loose", periods=MING),
    dict(name="West suburb (south of the road)", polygon=R(34.8002, 34.7975, 114.3170, 114.3245), density="loose", periods=MING),
    dict(name="North suburb", polygon=R(34.8238, 34.8218, 114.3530, 114.3568), density="loose", periods=MING),
    dict(name="North suburb (east)", polygon=R(34.8238, 34.8218, 114.3588, 114.3640), density="loose", periods=MING),
    dict(name="Village by the Fan pagoda", polygon=R(34.7728, 34.7716, 114.3540, 114.3620), density="loose", periods=MING),

    # ---- Qing: rebuilt along the main streets, much of the walled area empty
    dict(name="Drum Tower quarter (west)", polygon=_MQ_DT1, density="dense", periods=QING),
    dict(name="Drum Tower quarter", polygon=_MQ_DT2, density="dense", periods=QING),
    dict(name="East quarter", polygon=_MQ_DT3, density="dense", periods=QING),
    dict(name="Xiangguo temple lanes", polygon=[(34.7938, 114.3470), (34.7925, 114.3505), (34.7905, 114.3540), (34.7875, 114.3540), (34.7875, 114.3470)], density="dense", periods=QING),
    dict(name="West of the Drum Tower", polygon=R(34.8008, 34.7966, 114.3400, 114.3448), density="dense", periods=QING),
    dict(name="Lanes south of the lakes", polygon=R(34.8012, 34.7966, 114.3292, 114.3372), density="loose", periods=QING),
    dict(name="North-east lanes", polygon=R(34.8090, 34.8030, 114.3568, 114.3640), density="loose", periods=QING),
    dict(name="North lanes", polygon=R(34.8180, 34.8130, 114.3578, 114.3640), density="loose", periods=QING),
    dict(name="East suburb (Song gate)", polygon=R(34.7900, 34.7882, 114.3640, 114.3720), density="loose", periods=QING),
    dict(name="West suburb", polygon=R(34.8045, 34.8024, 114.3190, 114.3245), density="loose", periods=QING),
]

GARDENS = [
    dict(name="Genyue garden", polygon=R(34.8132, 34.8090, 114.3562, 114.3622), kind="park", periods=SONG),
    dict(name="Rear garden of the palace", polygon=R(PAL_N - 0.0003, 34.8086, PAL_W + 0.0004, PAL_E - 0.0004), kind="park", periods=SONGJIN),
    dict(name="Gardens of the governor's compound", polygon=R(34.8095, 34.8040, 114.3430, 114.3500), kind="park", periods=TANG),
    dict(name="Fields inside the north wall", polygon=R(IN_N - 0.0006, 34.8100, 114.3310, 114.3640), kind="orchard", periods=TANG),
    dict(name="Fields east of the city", polygon=R(34.8230, 34.7920, 114.3700, EAST), kind="orchard", periods=TANG),
    dict(name="Fields south of the city", polygon=R(34.7830, 34.7740, WEST, EAST), kind="orchard", periods=TANG),
    dict(name="Fields by the Fan terrace (west)", polygon=R(34.7740, 34.7714, WEST, 114.3530), kind="orchard", periods=TANG),
    dict(name="Fields by the Fan terrace (east)", polygon=R(34.7740, 34.7714, 114.3610, EAST), kind="orchard", periods=TANG),
    dict(name="Fields far south", polygon=R(34.7690, SOUTH, WEST, EAST), kind="orchard", periods=TANG),
    dict(name="Fields west of the city (north)", polygon=R(34.8230, 34.7992, WEST, 114.3240), kind="orchard", periods=TANG),
    dict(name="Fields west of the city (south)", polygon=R(34.7940, 34.7860, WEST, 114.3240), kind="orchard", periods=TANG),
    dict(name="Fields north of the city", polygon=R(NORTH, 34.8172, 114.3250, 114.3700), kind="orchard", periods=TANG),
    dict(name="Gardens beyond the Cai", polygon=R(34.7728, OUT_S + 0.0004, 114.3610, 114.3835), kind="orchard", periods=SONG),
    dict(name="Fields beyond the south wall", polygon=R(OUT_S - 0.0012, SOUTH, WEST, EAST), kind="orchard", periods=SONGJIN),
    dict(name="Fields beyond the east wall", polygon=R(34.8230, 34.7940, OUT_E + 0.0010, EAST), kind="orchard", periods=SONGJIN),
    dict(name="Fields in the north outer city", polygon=R(34.8198, 34.8162, 114.3115, 114.3535), kind="orchard", periods=JIN),
    dict(name="Fields in the south outer city", polygon=R(34.7728, OUT_S + 0.0004, 114.3115, 114.3570), kind="orchard", periods=JIN),
    dict(name="Fields in the south outer city (east)", polygon=R(34.7728, OUT_S + 0.0004, 114.3610, 114.3835), kind="orchard", periods=JIN),
    dict(name="Fields in the east outer city", polygon=R(34.8198, 34.8040, 114.3700, 114.3835), kind="orchard", periods=JIN),
    dict(name="Gardens of the Zhou palace", polygon=R(34.8130, 34.8112, 114.3402, 114.3528), kind="park", periods=MING),
    dict(name="Fields outside the walls (south)", polygon=R(34.7770, 34.7735, WEST, EAST), kind="orchard", periods=LATE),
    dict(name="Fields round the Fan pagoda (west)", polygon=R(34.7735, 34.7712, WEST, 114.3530), kind="orchard", periods=LATE),
    dict(name="Fields round the Fan pagoda (east)", polygon=R(34.7735, 34.7712, 114.3630, EAST), kind="orchard", periods=LATE),
    dict(name="Fields far south (west)", polygon=R(34.7712, SOUTH, WEST, 114.3570), kind="orchard", periods=LATE),
    dict(name="Fields far south (east)", polygon=R(34.7712, SOUTH, 114.3605, EAST), kind="orchard", periods=LATE),
    dict(name="Fields outside the walls (east)", polygon=R(34.8230, 34.7790, 114.3770, EAST), kind="orchard", periods=LATE),
    dict(name="Fields outside the walls (west)", polygon=R(34.8230, 34.7790, WEST, 114.3160), kind="orchard", periods=LATE),
    dict(name="Fields outside the walls (north)", polygon=R(NORTH, 34.8218, 114.3160, 114.3525), kind="orchard", periods=LATE),
    dict(name="Fields inside the walls (north-west)", polygon=[(34.8180, 114.3375), (34.8122, 114.3330), (34.8030, 114.3300), (34.8030, 114.3420), (34.8180, 114.3420)], kind="orchard", periods=QING),
    dict(name="Fields inside the walls (south-west)", polygon=[(34.7860, 114.3290), (34.7845, 114.3400), (34.7840, 114.3420), (34.7865, 114.3420), (34.7866, 114.3290)], kind="orchard", periods=QING),
    dict(name="Fields inside the walls (south-east)", polygon=R(34.7870, 34.7836, 114.3470, 114.3580), kind="orchard", periods=QING),
    dict(name="Fields inside the walls (north-east)", polygon=R(34.8125, 34.8095, 114.3578, 114.3660), kind="orchard", periods=QING),
    dict(name="Fields on the Zhou palace", polygon=R(34.8140, 34.8105, 114.3425, 114.3530), kind="orchard", periods=QING),
]

MARSH = [
    dict(name="Reed beds of the drowned palace", polygon=R(34.8040, 34.8028, 114.3420, 114.3500), periods=QING),
    dict(name="Waterlogged ground by Baogong lake", polygon=R(34.7975, 34.7958, 114.3300, 114.3360), periods=QING),
]

DISTRICTS = [
    dict(id="danei", name="Palace city (Danei)", polygon=R(PAL_N, PAL_S, PAL_W, PAL_E), periods=SONGJIN,
         description="The Song emperors' palace, grown from the Tang governor's compound and the Later Liang and Later Zhou palaces: the Daqing hall for great audiences, the Wende and Chuigong halls for daily business, the inner palace and gardens behind."),
    dict(id="licheng", name="Inner city (Licheng)", polygon=SONG_INNER, periods=SONGJIN,
         description="The 'old city' of the Tang, packed with government offices, the mansions of the great, the great temples and the busiest streets: the Imperial Way, the Pan Tower and Ma Xing streets, the Zhou bridge night market."),
    dict(id="waicheng-east", name="Outer city: the eastern wards", polygon=R(34.8200, 34.7700, 114.3680, OUT_E), periods=SONGJIN,
         description="Between the two walls on the east, where the Bian came in from the Huai: granaries, wharves, boatmen's inns, warehouses and the markets that grew up round the water gates."),
    dict(id="bianzhou", name="Bianzhou", polygon=SONG_INNER, periods=TANG,
         description="The prefectural city of Bianzhou, seat from 781 of the Xuanwu military governor: a walled town at the crossing of the Tongji canal and the roads across the plain."),
    dict(id="zhou-palace-d", name="Palace of the Prince of Zhou", polygon=R(34.8135, 34.8032, 114.3398, 114.3532), periods=MING,
         description="The palace of Zhu Su, fifth son of the Hongwu emperor, made Prince of Zhou in 1370 and settled in Kaifeng in 1378, and of his descendants for 260 years: walled courts on the old Song-Jin palace site, gardens, and a hill behind."),
    dict(id="kaifeng-qing", name="Walled city of Kaifeng", polygon=MQ_WALL, periods=QING,
         description="The Qing provincial capital rebuilt on the silt: yamens, temples, guild halls and markets along a few streets; lakes, ponds and fields fill much of the area inside the walls."),
]

LABELS = [
    dict(text="Bianzhou", position=(34.8180, 114.3200), size="lg", periods=TANG),
    dict(text="Dongjing", position=(34.7712, 114.3180), size="lg", periods=SONG),
    dict(text="Nanjing (Bianjing)", position=(34.7712, 114.3200), size="lg", periods=JIN),
    dict(text="Kaifeng", position=(34.7700, 114.3220), size="lg", periods=LATE),
    dict(text="Bian river", position=(34.7838, 114.3780), size="md", rotation=2, periods=EARLY),
    dict(text="Cai river", position=(34.7726, 114.3360), size="sm", rotation=-3, periods=EARLY),
    dict(text="Wuzhang river", position=(34.8222, 114.3300), size="sm", rotation=4, periods=EARLY),
    dict(text="Imperial Way", position=(34.7960, 114.3448), size="sm", rotation=-88, periods=SONGJIN),
    dict(text="Inner city", position=(34.8125, 114.3350), size="md", periods=SONGJIN),
    dict(text="Outer city", position=(34.8100, 114.3760), size="md", periods=SONGJIN),
    dict(text="Palace", position=(34.8092, 114.3465), size="sm", periods=SONGJIN),
    dict(text="Zhou palace", position=(34.8125, 114.3465), size="sm", periods=MING),
    dict(text="Yang lake", position=(34.8052, 114.3420), size="sm", periods=QING),
    dict(text="Pan lake", position=(34.8052, 114.3505), size="sm", periods=QING),
    dict(text="Baogong lake", position=(34.7905, 114.3330), size="sm", periods=QING),
    dict(text="Ring dyke", position=(34.7672, 114.3300), size="sm", periods=LATE),
]

SOURCES = [
    dict(id="wiki-kaifeng", title="Kaifeng", author="Wikipedia", url="https://en.wikipedia.org/wiki/Kaifeng"),
    dict(id="wiki-bianjing", title="Bianjing", author="Wikipedia", url="https://en.wikipedia.org/wiki/Bianjing"),
    dict(id="wiki-bian-river", title="Bian River", author="Wikipedia", url="https://en.wikipedia.org/wiki/Bian_River"),
    dict(id="wiki-grand-canal", title="Grand Canal (China)", author="Wikipedia", url="https://en.wikipedia.org/wiki/Grand_Canal_(China)"),
    dict(id="wiki-1642-flood", title="1642 Yellow River flood", author="Wikipedia", url="https://en.wikipedia.org/wiki/1642_Yellow_River_flood"),
    dict(id="dongjing-menghualu", title="Dongjing meng Hua lu (The Eastern Capital: A Dream of Splendour)", author="Meng Yuanlao", year=1147),
    dict(id="west-dongjing", title="The Interplay of Commerce and Culture in Song Kaifeng (on the Dongjing meng Hua lu)", author="Stephen H. West"),
    dict(id="heng", title="Cities of Aristocrats and Bureaucrats: The Development of Medieval Chinese Cityscapes", author="Heng Chye Kiang", year=1999),
    dict(id="steinhardt", title="Chinese Imperial City Planning", author="Nancy Shatzman Steinhardt", year=1990),
    dict(id="qiu-gang", title="Kaifeng Song cheng kaogu (archaeology of the Song city of Kaifeng)", author="Qiu Gang et al., Kaifeng Song City Archaeological Team"),
    dict(id="osm", title="OpenStreetMap: Kaifeng city wall and lakes", author="OpenStreetMap contributors", url="https://www.openstreetmap.org/"),
]
