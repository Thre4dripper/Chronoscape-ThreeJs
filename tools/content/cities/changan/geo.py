# Chang'an / Daxing / Xi'an: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
SUI = ["sui-600"]
TANG = ["early-tang-650", "tang-750", "late-tang-880"]
GRID = SUI + TANG                      # the Sui-Tang walled-ward city
MING = ["ming-1400"]
ALL = GRID + MING

# The Sui-Tang grid after the usual reconstruction (Xu Song, Heng Chye Kiang, the Shaanxi excavation reports)
# laid over the modern map. The frame holds the northern and central city; the far west and south wards are cut.
# North-south lines (longitude): Zhuque Avenue on the axis, the Imperial City's walls, the avenues between ward columns
Z = 108.9350                                    # Zhuque Avenue, 150 m wide
W12, ICW, W34, W45, W_WALL = 108.9277, 108.9197, 108.9076, 108.8957, 108.8838
E12, ICE, E34, E45, E_WALL = 108.9423, 108.9503, 108.9624, 108.9743, 108.9862
# East-west lines (latitude)
N_WALL = 34.2825                                # the city's north wall, the Palace City's north wall
TH = 34.2760                                    # Tonghuamen-Kaiyuanmen avenue
PC_S = 34.2690                                  # the Palace City's south wall and the Hengjie square
R3 = 34.2625
CHUNMING = 34.2560                              # Chunmingmen-Jinguangmen avenue, 120 m
IC_S = 34.2518                                  # the Imperial City's south wall (and the Ming south wall)
A2, A3, A4, A5, A6, A7 = 34.2460, 34.2402, 34.2344, 34.2286, 34.2228, 34.2170
S_WALL = 34.2046
# Ming Xi'an (walls of the 1370s)
MN, MS, MW, ME = 34.2775, 34.2518, 108.9197, 108.9665
MX, MY = 108.9430, 34.2610                       # the crossing of the four main streets
# the frame
WEST, EAST, NORTH, SOUTH = 108.8945, 108.9870, 34.2905, 34.2160


def R(n, s, w, e):
    """A rectangle between two latitudes and two longitudes."""
    return [(n, w), (n, e), (s, e), (s, w)]


CITY = dict(
    name="Chang'an", subtitle="Daxing, the Tang Capital, and Ming Xi'an",
    description="Chang'an from the Sui foundation of Daxing in 582 to the Ming walled city of Xi'an: the Palace and Imperial Cities, the Daming Palace on its plateau, the two markets and the walled wards of the northern and central city down to the Greater Wild Goose Pagoda. The far western, southern and south-eastern wards lie beyond the frame. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="tang-750",
    world=dict(heightScale=1.0, walls=["#DCCDB0", "#D0BF9E", "#C4B28F"], roofs=["#6A6866", "#5F5E5E", "#787068"]),
    camera=dict(target=(34.2560, 108.9420), distance=46),
)
FRAME = ((NORTH, WEST), (SOUTH, EAST))
PALETTE = dict(parchment="#E7D5AE", ink="#5E4434", water="#668A8C", hill="#7A7D58", road="#8C6C4C")
COMPASS = (34.2875, 108.9000)
CARTOUCHE = (34.2172, 108.8960)

PERIODS = [
    dict(id="sui-600", label="Daxing, the new Sui capital", year=600, startYear=582, endYear=617,
         summary="Emperor Wen of Sui ordered a new capital in 582 on the plain south-east of the worn-out Han city, and Yuwen Kai laid it out in months: a rammed-earth rectangle 9.7 by 8.6 km, the Palace and Imperial Cities at the head of the axis, two markets, 108 walled wards on a grid of avenues. Halls are timber on earth terraces, tiled in grey.",
         population="perhaps 300,000–500,000 (estimates vary widely)",
         feel="Fresh-pounded earth walls along avenues far too wide for their traffic, ox-carts of tiles and timber, and wheat growing inside the southern wards.",
         style="sinic",
         houses=dict(title="Wards of the new capital", text="Each ward (fang) is a rammed-earth rectangle with two or four gates and a cross of lanes inside. Officials and the families moved in from the old Han city build courtyard compounds of rammed earth and timber near the palace; temples are given whole quarters of wards."),
         outskirts=dict(title="Empty wards in the south", text="South of the markets many wards are walled but hardly lived in: wheat, millet and vegetable plots, a few farmhouses and new temples on the low ridges.")),
    dict(id="early-tang-650", label="Chang'an of Taizong and Gaozong", year=650, startYear=618, endYear=712,
         summary="The Tang took the Sui city whole in 617 and renamed it Chang'an. Under Taizong and Gaozong it fills: monks back from India, envoys from Japan, Silla and the Western Regions, the Daming Palace raised on the Longshou plateau (begun 634, built 662–663), and in 652 Xuanzang's brick pagoda at the Ci'en temple.",
         population="perhaps 600,000–800,000",
         feel="Drums at dawn opening the ward gates, camel bells on the Jinguang avenue, chanting from new temples, and dust from the polo grounds.",
         style="sinic",
         houses=dict(title="Courtyard compounds in the wards", text="Behind the ward walls, lanes lead to gated courtyard houses: rammed-earth walls, timber halls under grey tiles, a front court for guests and inner courts for the family. Only officials of the third rank and above may open a gate onto the avenue."),
         outskirts=dict(title="Gardens of the southern wards", text="The southern wards are a patchwork of temple estates, orchards, vegetable gardens and the villas of officials, with fields between their walls.")),
    dict(id="tang-750", label="Chang'an, the Tang capital", year=750, startYear=713, endYear=755,
         summary="The capital of a million under Xuanzong: the court at the Daming and Xingqing palaces, Sogdian, Persian and Uighur merchants in the West Market, Nestorian, Manichaean and Zoroastrian temples beside a hundred Buddhist and Taoist ones, Li Bai and Du Fu in the taverns, candidates for the examinations crowding the inns of Pingkang ward.",
         population="perhaps 800,000–1,000,000 (the usual figure, much debated)",
         feel="Pipa music and grape wine from the foreign taverns, the market's noon drum, peonies sold by the cartload in spring, and eight hundred beats of the dusk drums shutting the ward gates.",
         style="sinic",
         houses=dict(title="Mansions and lanes of the wards", text="The northern wards hold princes' and ministers' mansions with ponds and pavilions, behind gates on the avenues. Lanes inside the ward walls are lined with shops, inns, wine shops and temples; ordinary houses are one-storey courtyards of earth and timber under grey tiles."),
         outskirts=dict(title="The thin southern wards", text="South of the Yanxing-Yanping avenue, a Song writer recalled, 'though some live there, their kitchen smoke does not join': orchards, fields and temple gardens inside the ward walls.")),
    dict(id="late-tang-880", label="Late Tang Chang'an", year=880, startYear=756, endYear=904,
         summary="The An Lushan rebels took the city in 756 and the Tibetans in 763; the court came back each time, weaker. In 845 Wuzong closed all but four Buddhist temples in the capital and banned the foreign religions. Huang Chao's rebels entered in January 881, and in 904 Zhu Wen pulled the city down and floated its timbers to Luoyang.",
         population="perhaps 500,000, falling",
         feel="Burnt beams among the wards, eunuchs' guards on the avenues, night markets that ignore the curfew, and the scent of peonies the rich still buy at fortunes a stem.",
         style="sinic",
         houses=dict(title="Crowded eastern wards", text="Life gathers in the north-east, near the Daming Palace and the East Market: ward walls are breached for shopfronts, houses crowd the lanes, and taverns stay open after the drums. Ruined mansions of the old aristocracy are let out or pulled down."),
         outskirts=dict(title="Fields in the west and south", text="The western and southern wards thin out into fields, ruined temples closed in 845 and vegetable gardens; soldiers camp in deserted compounds.")),
    dict(id="ming-1400", label="Ming Xi'an", year=1400, startYear=1368, endYear=1644,
         summary="After 904 the city shrank to a walled town on the old Imperial City. The Ming renamed it Xi'an in 1369 and in the 1370s raised new walls on the Tang lines to the west and south, extended north and east, with the palace of the Prince of Qin inside. The Bell Tower (1384) and Drum Tower (1380) mark the centre; the Tang sites are fields and mounds.",
         population="perhaps 100,000 (no reliable figure)",
         feel="Garrison drums from the gate towers, camel trains of the Hui merchants, the reek of tanneries and mutton stalls, and wheat fields running to the foot of the old pagodas.",
         style="sinic",
         houses=dict(title="Courtyards of Ming Xi'an", text="Inside the walls, quadrangle houses of grey brick and timber line straight lanes off the four main streets; soldiers of the garrison hold the north-west quarter, the Hui families the lanes round the Great Mosque, merchants the east."),
         outskirts=dict(title="Villages on the Tang wards", text="Outside the walls, villages of loess and brick houses stand among wheat fields on the old wards; the lines of the Tang avenues survive here and there as field roads and village names.")),
]

# ---------------------------------------------------------------- water and hills
WATER = [
    dict(id="yongan", name="Yong'an canal", width=10, periods=GRID,
         path=[(SOUTH, 108.9084), (A4, 108.9084), (A2, 108.9084), (CHUNMING, 108.9084), (R3, 108.9084), (N_WALL, 108.9084), (NORTH, 108.9090)],
         blurb="Dug in 582 to bring water of the Jiao river north through the western wards, past the West Market and out under the north wall into the Forbidden Park. Its exact line through the wards is the usual reconstruction."),
    dict(id="qingming", name="Qingming canal", width=8, periods=GRID,
         path=[(SOUTH, 108.9284), (A4, 108.9284), (A2, 108.9284), (IC_S + 0.0004, 108.9284), (PC_S - 0.0012, 108.9286), (PC_S + 0.0010, 108.9290), (34.2770, 108.9300)],
         blurb="A Sui canal from the Jue river, led north through the wards west of Zhuque Avenue into the Imperial City and on to the pools of the palace gardens."),
    dict(id="longshou", name="Longshou canal", width=10, periods=GRID,
         path=[(34.2742, EAST), (34.2742, 108.9790), (34.2740, 108.9650), (34.2735, 108.9520), (34.2735, ICE + 0.0003)],
         blurb="The 'Dragon Head' canal, dug in 583 from the Chan river east of the city, entering by the Tonghua gate and running west to the Palace City; a branch fed the Xingqing pond."),
    dict(id="longshou-xingqing", name="Longshou canal (Xingqing branch)", width=8, periods=["tang-750", "late-tang-880"],
         path=[(34.2742, 108.9790), (34.2690, 108.9790), (34.2640, 108.9792)],
         blurb="The branch that fed the Dragon Pond of the Xingqing Palace."),
    dict(id="longshou-ming", name="Longshou canal", width=10, periods=MING,
         path=[(34.2650, EAST), (34.2650, 108.9700), (34.2650, ME + 0.0006), (34.2652, 108.9600), (34.2700, 108.9560)],
         blurb="Restored in the early Ming to bring Chan river water through the east wall to the city and the moat of the Prince of Qin's palace; the city's wells were brackish."),
    dict(id="ming-moat", name="City moat", width=22, periods=MING,
         path=[(MN + 0.0007, MW - 0.0008), (MN + 0.0007, ME + 0.0008), (MS - 0.0007, ME + 0.0008), (MS - 0.0007, MW - 0.0008), (MN + 0.0007, MW - 0.0008)],
         blurb="The moat round the Ming walls, fed by the canals; drawbridges crossed it in front of the four gates."),
]

HILLS = [
    dict(id="longshou-yuan", name="Longshou plateau", center=(34.2885, 108.9450), radius=300,
         blurb="The 'Dragon Head' plateau, a loess ridge north of the city. Its southern tip carried the Daming Palace, whose Hanyuan Hall stood some 15 m above the wards; the Tang could look down on the whole city from it."),
    dict(id="leyou-yuan", name="Leyou plateau", center=(34.2257, 108.9800), radius=420, periods=GRID,
         blurb="The highest ground inside the walls, in the south-east wards, a park and picnic place where people climbed on the ninth day of the ninth month. Li Shangyin's quatrain on it ends: 'The setting sun is infinitely lovely, only the dusk is near.'"),
    dict(id="leyou-yuan-ming", name="Leyou plateau", center=(34.2257, 108.9800), radius=420, periods=MING,
         blurb="The old pleasure ground of the Tang, now fields and the ruins of the Qinglong temple, where the Japanese monk Kūkai had studied esoteric Buddhism in 805."),
]

# ---------------------------------------------------------------- roads
_GRID_ROADS = [
    dict(id="zhuque", name="Zhuque Avenue", path=[(IC_S - 0.0004, Z), (SOUTH, Z)], width=150, style="major", labelled=True,
         blurb="The Avenue of the Vermilion Bird, 150 m wide from ditch to ditch, from the Imperial City's Zhuque gate 5 km to the Mingde gate. No house opened onto it: only the walls and gates of the wards, locust trees and drainage ditches. It divided the city into the eastern Wannian and western Chang'an counties."),
    dict(id="chengtianmen-street", name="Chengtianmen Street", path=[(PC_S, Z), (IC_S, Z)], width=110, style="major",
         blurb="The axis through the Imperial City from the Zhuque gate to the Chengtian gate, lined with the offices of government."),
    dict(id="hengjie", name="Hengjie (the Transverse Street)", path=[(PC_S - 0.0009, ICW), (PC_S - 0.0009, ICE)], width=200, style="major", labelled=True,
         blurb="A square-cum-street some 220 m wide between the Palace City's south wall and the Imperial City, where the court assembled, amnesties were proclaimed from the Chengtian gate and troops paraded."),
    dict(id="chunming", name="Chunmingmen Avenue", path=[(CHUNMING, ICE), (CHUNMING, EAST)], width=120, style="major", labelled=True,
         blurb="The great east-west avenue, 120 m wide, from the Imperial City to the Chunming gate in the east wall, the road to Luoyang. The East Market and Xingqing Palace opened onto it."),
    dict(id="jinguang", name="Jinguangmen Avenue", path=[(CHUNMING, WEST), (CHUNMING, ICW)], width=120, style="major", labelled=True,
         blurb="The west half of the great cross-avenue, ending at the Jinguang gate, where the Silk Road left the city for Liangzhou, Dunhuang and Samarkand."),
    dict(id="tonghua-e", name="Tonghuamen Avenue", path=[(TH, ICE + 0.0007), (TH, EAST)], width=50),
    dict(id="kaiyuan-w", name="Kaiyuanmen Avenue", path=[(TH, WEST), (TH, ICW - 0.0007)], width=50),
    dict(id="pcs-e", name="Avenue east of the Hengjie", path=[(PC_S, ICE + 0.0007), (PC_S, EAST)], width=40),
    dict(id="pcs-w", name="Avenue west of the Hengjie", path=[(PC_S, WEST), (PC_S, ICW - 0.0007)], width=40),
    dict(id="r3-e", name="Avenue by the Yanxi gate", path=[(R3, ICE + 0.0007), (R3, E45)], width=40),
    dict(id="r3-w", name="Avenue by the Anfu gate", path=[(R3, WEST), (R3, ICW - 0.0007)], width=40),
    dict(id="ics-street", name="Avenue before the Imperial City", path=[(IC_S - 0.0004, W34), (IC_S - 0.0004, E34)], width=47,
         blurb="The street along the south wall of the Imperial City, joining the three south gates."),
    dict(id="ics-street-e", name="Avenue south of Chongren", path=[(IC_S, E45), (IC_S, EAST)], width=40),
    dict(id="a2", name="Fourth avenue south", path=[(A2, WEST), (A2, EAST)], width=40),
    dict(id="a3", name="Fifth avenue south", path=[(A3, WEST), (A3, EAST)], width=40),
    dict(id="a4", name="Sixth avenue south", path=[(A4, WEST), (A4, EAST)], width=40),
    dict(id="a5", name="Seventh avenue south", path=[(A5, WEST), (A5, EAST)], width=40),
    dict(id="yanxing", name="Yanxingmen-Yanping Avenue", path=[(A6, WEST), (A6, EAST)], width=55, labelled=True,
         blurb="The southern of the three great cross-avenues, from the Yanxing gate in the east wall to the Yanping gate in the west."),
    dict(id="hanguang", name="Hanguangmen Street", path=[(IC_S - 0.0004, W12), (SOUTH, W12)], width=45, labelled=True,
         blurb="The avenue south from the Hanguang gate, the west gate of the Imperial City's south wall."),
    dict(id="anshang", name="Anshangmen Street", path=[(IC_S - 0.0004, E12), (SOUTH, E12)], width=45, labelled=True,
         blurb="The avenue south from the Anshang gate toward the Qixia gate in the south wall; the Ming South Street later followed its line."),
    dict(id="icw-street", name="Avenue west of the Imperial City", path=[(N_WALL, ICW - 0.0007), (IC_S, ICW - 0.0007), (IC_S - 0.0004, ICW), (SOUTH, ICW)], width=40),
    dict(id="ice-street", name="Avenue east of the Imperial City", path=[(N_WALL, ICE + 0.0007), (IC_S, ICE + 0.0007), (IC_S - 0.0004, ICE), (SOUTH, ICE)], width=40),
    dict(id="w34", name="Avenue by the West Market", path=[(N_WALL, W34), (SOUTH, W34)], width=40),
    dict(id="danfeng", name="Danfeng Street", path=[(N_WALL, E34), (CHUNMING, E34)], width=120, labelled=True, periods=TANG,
         blurb="The broad street (some 120-180 m) running south from the Danfeng gate of the Daming Palace, the court's way down into the city."),
    dict(id="e34-sui", name="Avenue by the East Market", path=[(N_WALL, E34), (CHUNMING, E34)], width=40, periods=SUI),
    dict(id="e34", name="Avenue by the East Market", path=[(CHUNMING, E34), (SOUTH, E34)], width=40),
    dict(id="e45", name="Avenue east of the Market", path=[(N_WALL, E45), (SOUTH, E45)], width=40),
]
ROADS = [dict(r, periods=r.get("periods", GRID)) for r in _GRID_ROADS] + [
    dict(id="ming-west-street", name="West Street", path=[(MY - 0.0005, MW), (MY, MX)], width=22, style="major", labelled=True, periods=MING,
         blurb="From the Anding gate to the crossing; the Bell Tower of 1384 stood on it near Guangji Street until it was moved east to the crossing in 1582."),
    dict(id="ming-east-street", name="East Street", path=[(MY, MX), (MY, ME)], width=22, style="major", labelled=True, periods=MING,
         blurb="From the crossing to the Changle gate, the road to Lintong and the east."),
    dict(id="ming-north-street", name="North Street", path=[(MN, MX), (MY, MX)], width=20, style="major", labelled=True, periods=MING),
    dict(id="ming-south-street", name="South Street", path=[(MY, MX), (MS, MX)], width=20, style="major", labelled=True, periods=MING,
         blurb="On the line of the Tang Anshangmen street, from the crossing to the Yongning (South) gate."),
    dict(id="ming-guangji", name="Guangji Street", path=[(34.2700, 108.9370), (MS, 108.9370)], width=10, periods=MING),
    dict(id="ming-west-road", name="Road to Xianyang", path=[(MY - 0.0005, MW - 0.0012), (34.2590, 108.9100), (34.2575, WEST)], width=12, labelled=True, periods=MING,
         blurb="West from the Anding gate across the old wards toward Xianyang and the Gansu corridor: the old Silk Road, now walked by Hui and Central Asian caravans."),
    dict(id="ming-east-road", name="Road to Lintong", path=[(MY, ME + 0.0012), (34.2612, 108.9760), (34.2615, EAST)], width=12, labelled=True, periods=MING),
    dict(id="ming-north-road", name="Road to the Wei crossing", path=[(MN + 0.0012, MX), (34.2850, 108.9440), (NORTH, 108.9445)], width=10, periods=MING),
    dict(id="ming-ciensi-road", name="Road to Ci'en temple", path=[(MS - 0.0012, MX), (34.2440, 108.9450), (34.2330, 108.9520), (34.2240, 108.9575), (34.2210, 108.9590)], width=8, labelled=True, periods=MING,
         blurb="A country road south from the Yongning gate to the Ci'en temple and its pagoda, past villages on the old wards."),
    dict(id="ming-jianfu-road", name="Road to Jianfu temple", path=[(MS - 0.0012, 108.9400), (34.2450, 108.9390), (34.2405, 108.9388)], width=6, style="minor", periods=MING),
]

WALLS = [
    dict(id="tang-wall", name="Outer wall (guocheng)", closed=True, periods=GRID,
         path=[(N_WALL, W_WALL), (N_WALL, E_WALL), (S_WALL, E_WALL), (S_WALL, W_WALL)],
         blurb="The rammed-earth outer wall of 582, about 36.7 km round and only some 5 m high, with three gates on each side but the north. It was a boundary and a customs line more than a fortification."),
    dict(id="palace-wall", name="Palace City wall", closed=True, periods=GRID,
         path=[(N_WALL, ICW), (N_WALL, ICE), (PC_S, ICE), (PC_S, ICW)],
         blurb="The Palace City, 2.8 by 1.5 km: the Taiji Palace in the middle, the Eastern Palace of the crown prince and the Yeting of the palace women on either side, walled in rammed earth about 10 m high."),
    dict(id="imperial-wall", name="Imperial City wall", periods=GRID,
         path=[(PC_S - 0.0018, ICW), (IC_S, ICW), (IC_S, ICE), (PC_S - 0.0018, ICE)],
         blurb="The Imperial City (Huangcheng), 2.8 by 1.8 km, walled on three sides and open to the Hengjie on the north: ministries, courts, the ancestral temple and the altars of soil and grain, with no private houses. An innovation of the Sui."),
    dict(id="daming-wall", name="Daming Palace wall", periods=TANG,
         path=[(34.3030, 108.9534), (N_WALL, 108.9534), (N_WALL, 108.9714), (34.3030, 108.9650)],
         blurb="The Daming Palace's walls, laid out in 662 as a trapezoid about 7.6 km round on the Longshou plateau, outside the city's north-east wall. The north and its Taiye pond lie beyond the frame."),
    dict(id="xingqing-wall", name="Xingqing Palace wall", closed=True, periods=["tang-750", "late-tang-880"],
         path=[(34.2675, E45 + 0.0007), (34.2675, E_WALL - 0.0007), (CHUNMING + 0.0006, E_WALL - 0.0007), (CHUNMING + 0.0006, E45 + 0.0007)],
         blurb="Xuanzong's palace, built from 714 on his princely mansion in the Longqing ward and half the ward north of it."),
    dict(id="jiacheng", name="Jiacheng (covered way)", periods=["tang-750", "late-tang-880"],
         path=[(N_WALL, E_WALL - 0.0007), (34.2675, E_WALL - 0.0007), (CHUNMING + 0.0006, E_WALL - 0.0007), (SOUTH, E_WALL - 0.0007)],
         blurb="A walled passage along the east wall, built in the 720s and 730s, by which the emperor could ride unseen from the Daming Palace to the Xingqing Palace and on to the Furong garden at the Qujiang pond."),
    dict(id="ming-wall", name="Ming city wall", closed=True, periods=MING,
         path=[(MN, MW), (MN, ME), (MS, ME), (MS, MW)],
         blurb="Raised in 1370-1378 over the Tang Imperial City's west and south walls and extended north and east: 13.7 km round, 12 m high, with corner towers and barbicans at the four gates. Its rammed earth was faced with brick in 1568; it still stands."),
]

GATES = [
    dict(id="xuanwumen", name="Xuanwu gate", position=(N_WALL, Z), periods=GRID),
    dict(id="hanguangmen", name="Hanguang gate", position=(IC_S, W12), periods=GRID),
    dict(id="anshangmen", name="Anshang gate", position=(IC_S, E12), periods=GRID),
    dict(id="jingfengmen", name="Jingfeng gate", position=(CHUNMING, ICE), periods=GRID),
    dict(id="shunyimen", name="Shunyi gate", position=(CHUNMING, ICW), periods=GRID),
    dict(id="yanximen", name="Yanxi gate", position=(R3, ICE), periods=GRID),
    dict(id="anfumen", name="Anfu gate", position=(R3, ICW), periods=GRID),
    dict(id="chunmingmen", name="Chunming gate", position=(CHUNMING, E_WALL), periods=GRID),
    dict(id="tonghuamen", name="Tonghua gate", position=(TH, E_WALL), periods=GRID),
    dict(id="yanxingmen", name="Yanxing gate", position=(A6, E_WALL), periods=GRID),
    dict(id="changlemen", name="Changle gate (East Gate)", position=(MY, ME), periods=MING),
    dict(id="andingmen", name="Anding gate (West Gate)", position=(MY - 0.0005, MW), periods=MING),
    dict(id="anyuanmen", name="Anyuan gate (North Gate)", position=(MN, MX), periods=MING),
]

# ---------------------------------------------------------------- the walled wards
# Ward columns (west to east) and rows (north to south), between the avenues.
COLS = dict(W4=(W45, W34), W3=(W34, ICW), W2=(ICW, W12), W1=(W12, Z), E1=(Z, E12), E2=(E12, ICE), E3=(ICE, E34), E4=(E34, E45), E5=(E45, E_WALL))
OUTER = ["W4", "W3", "E3", "E4", "E5"]
INNER = ["W2", "W1", "E1", "E2"]
NORTH_ROWS = [(N_WALL, TH), (TH, PC_S), (PC_S, R3), (R3, CHUNMING)]          # beside the Palace and Imperial Cities (outer columns only)
SOUTH_ROWS = [(CHUNMING, IC_S), (IC_S, A2), (A2, A3), (A3, A4), (A4, A5), (A5, A6), (A6, A7)]
MARKETS = {("W4", 0), ("W4", 1), ("E4", 0), ("E4", 1)}                     # the two markets fill two wards each
XINGQING = {("E5", "n3"), ("E5", "n2")}
LEYOU = {("E5", 5)}                                                         # the Leyouyuan park

# Ward names after Xu Song's list (columns 1-3 east of Zhuque and a few others); the rest go unnamed on the map.
NAMES = {
    ("E1", 1): "Xingdao ward", ("E1", 2): "Kaihua ward", ("E1", 3): "Anren ward", ("E1", 4): "Guangfu ward", ("E1", 5): "Jingshan ward", ("E1", 6): "Lanling ward",
    ("E2", 1): "Wuben ward", ("E2", 2): "Chongyi ward", ("E2", 3): "Changxing ward", ("E2", 4): "Yongle ward", ("E2", 5): "Jing'an ward", ("E2", 6): "Anshan ward",
    ("E3", 0): "Pingkang ward", ("E3", 1): "Xuanyang ward", ("E3", 2): "Qinren ward", ("E3", 3): "Yongning ward", ("E3", 4): "Yongchong ward", ("E3", 5): "Zhaoguo ward", ("E3", 6): "Jinchang ward",
    ("E3", "n3"): "Chongren ward", ("E3", "n2"): "Yongxing ward", ("E3", "n1"): "Guangzhai ward", ("E3", "n0"): "Yishan ward",
    ("E5", "n3"): "Longqing ward", ("W3", "n3"): "Yining ward", ("W2", 3): "Yankang ward", ("W1", 5): "Chongye ward", ("W3", "n1"): "Fuxing ward",
}


def ward(col, row, density, era):
    """One ward between its avenues; row is an index into SOUTH_ROWS or 'n0'..'n3' for NORTH_ROWS."""
    w, e = COLS[col]
    n, s = NORTH_ROWS[int(row[1])] if isinstance(row, str) else SOUTH_ROWS[row]
    return dict(name=NAMES.get((col, row), "Ward"), polygon=R(n, s, w, e), density=density, periods=[era])


def wards(era, dense_to, loose_to, west_dense_to=None, west_loose_to=None, skip=()):
    """Every ward in the frame for one era: dense down to row dense_to, loose to loose_to, none beyond (fields).
    The west_* limits, when given, apply to the columns west of Zhuque Avenue."""
    out = []
    for col in OUTER + INNER:
        west = col.startswith("W")
        dt = west_dense_to if (west and west_dense_to is not None) else dense_to
        lt = west_loose_to if (west and west_loose_to is not None) else loose_to
        if col in OUTER:
            for i in range(4):
                if (col, f"n{i}") not in skip:
                    out.append(ward(col, f"n{i}", "dense" if dt >= 0 else "loose", era))
        for i in range(len(SOUTH_ROWS)):
            if (col in INNER and i == 0) or (col, i) in MARKETS or (col, i) in skip:
                continue                      # the Imperial City, the markets, palaces and parks
            if i <= dt:
                out.append(ward(col, i, "dense", era))
            elif i <= lt:
                out.append(ward(col, i, "loose", era))
    return out


_PALACE_BLOCKS = [
    dict(name="Offices of the Imperial City, west", polygon=R(PC_S - 0.0020, IC_S + 0.0003, ICW + 0.0003, Z - 0.0008), density="dense"),
    dict(name="Offices of the Imperial City, east", polygon=R(PC_S - 0.0020, IC_S + 0.0003, Z + 0.0008, ICE - 0.0003), density="dense"),
    dict(name="Eastern Palace (Donggong)", polygon=R(N_WALL - 0.0003, PC_S + 0.0003, 108.9415, ICE - 0.0003), density="loose"),
    dict(name="Yeting Palace", polygon=R(N_WALL - 0.0003, PC_S + 0.0003, ICW + 0.0003, 108.9272), density="loose"),
    dict(name="Inner halls of the Taiji Palace", polygon=R(N_WALL - 0.0004, 34.2772, 108.9285, 108.9412), density="loose"),
]

BLOCKS = (
    [dict(b, periods=GRID) for b in _PALACE_BLOCKS]
    + wards("sui-600", 2, 4)
    + wards("early-tang-650", 3, 6)
    + wards("tang-750", 4, 5, skip=XINGQING | LEYOU)
    + wards("late-tang-880", 3, 5, west_dense_to=1, west_loose_to=1, skip=XINGQING | LEYOU)
    + [
        # Ming Xi'an: four quarters inside the walls, the suburbs at the gates, villages on the old wards
        dict(name="North-west quarter (the garrison)", polygon=R(MN - 0.0003, MY + 0.0003, MW + 0.0003, MX - 0.0003), density="dense", periods=MING),
        dict(name="South-west quarter", polygon=R(MY - 0.0005, MS + 0.0003, MW + 0.0003, MX - 0.0003), density="dense", periods=MING),
        dict(name="South-east quarter", polygon=R(MY - 0.0003, MS + 0.0003, MX + 0.0003, ME - 0.0003), density="dense", periods=MING),
        dict(name="North-east quarter", polygon=R(MN - 0.0003, MY + 0.0003, MX + 0.0003, ME - 0.0003), density="dense", periods=MING),
        dict(name="East suburb (Dongguan)", polygon=R(34.2650, 34.2575, ME + 0.0014, 108.9770), density="dense", periods=MING),
        dict(name="South suburb", polygon=R(MS - 0.0016, 34.2470, 108.9395, 108.9470), density="loose", periods=MING),
        dict(name="West suburb", polygon=R(34.2632, 34.2585, 108.9120, MW - 0.0016), density="loose", periods=MING),
        dict(name="North suburb", polygon=R(34.2815, MN + 0.0016, 108.9405, 108.9460), density="loose", periods=MING),
        dict(name="Village at the Ci'en temple", polygon=R(34.2235, 34.2212, 108.9555, 108.9630), density="loose", periods=MING),
        dict(name="Village at the Jianfu temple", polygon=R(34.2425, 34.2405, 108.9360, 108.9415), density="loose", periods=MING),
        dict(name="Villages on the Daming terrace", polygon=R(34.2850, 34.2832, 108.9480, 108.9560), density="loose", periods=MING),
        dict(name="Hamlet in the old West Market", polygon=R(34.2530, 34.2495, 108.8990, 108.9060), density="loose", periods=MING),
        dict(name="Hamlet in the old East Market", polygon=R(34.2510, 34.2480, 108.9660, 108.9720), density="loose", periods=MING),
        dict(name="Villages of the Leyou plateau", polygon=R(34.2315, 34.2290, 108.9730, 108.9800), density="loose", periods=MING),
    ]
)

GARDENS = [
    dict(name="Fields in the southern wards", polygon=R(A5, SOUTH, WEST, EAST), kind="orchard", periods=SUI),
    dict(name="Orchards of the southern wards", polygon=R(A6, SOUTH, WEST, EAST), kind="orchard", periods=["tang-750", "late-tang-880"]),
    dict(name="Fields in the western wards", polygon=R(A2, A6, WEST, Z - 0.0009), kind="orchard", periods=["late-tang-880"]),
    dict(name="West garden of the Taiji Palace", polygon=R(34.2768, PC_S + 0.0004, 108.9280, 108.9325), kind="park", periods=GRID),
    dict(name="East garden of the Taiji Palace", polygon=R(34.2768, PC_S + 0.0004, 108.9375, 108.9412), kind="park", periods=GRID),
    dict(name="Grounds of the Daming Palace", polygon=R(NORTH, N_WALL + 0.0004, 108.9538, 108.9705), kind="park", periods=TANG),
    dict(name="Forbidden Park (Jinyuan)", polygon=R(NORTH, N_WALL + 0.0006, WEST, 108.9410), kind="park", periods=GRID),
    dict(name="Leyouyuan", polygon=R(A5, A6, E45, E_WALL), kind="park", periods=["tang-750", "late-tang-880"]),
    # Ming: fields over the Tang city, leaving room for the villages
    dict(name="Fields on the old Daming Palace", polygon=R(NORTH, 34.2805, 108.9570, EAST), kind="orchard", periods=MING),
    dict(name="Fields north of the walls", polygon=R(NORTH, MN + 0.0020, WEST, 108.9390), kind="orchard", periods=MING),
    dict(name="Fields on the western wards", polygon=R(MN, 34.2545, WEST, 108.9110), kind="orchard", periods=MING),
    dict(name="Fields on the eastern wards", polygon=R(34.2790, 34.2665, ME + 0.0020, EAST), kind="orchard", periods=MING),
    dict(name="Fields on the south-western wards", polygon=R(34.2460, 34.2240, WEST, 108.9350), kind="orchard", periods=MING),
    dict(name="Fields on the southern wards", polygon=R(34.2400, 34.2240, 108.9420, 108.9700), kind="orchard", periods=MING),
    dict(name="Fields on the south-eastern wards", polygon=R(34.2460, 34.2330, 108.9720, EAST), kind="orchard", periods=MING),
    dict(name="Fields by the Ci'en temple", polygon=R(34.2240, SOUTH, WEST, 108.9540), kind="orchard", periods=MING),
    dict(name="Fields east of the Ci'en temple", polygon=R(34.2205, SOUTH, 108.9640, EAST), kind="orchard", periods=MING),
]

DISTRICTS = [
    dict(id="palace-city", name="Palace City (Gongcheng)", polygon=R(N_WALL, PC_S, ICW, ICE), periods=GRID,
         description="The walled palace at the head of the axis: the Daxing (from Tang times Taiji) Palace of the emperor in the middle, the crown prince's Eastern Palace to the east, the Yeting of the palace women and workshops to the west. The court lived here until the Daming Palace was finished in 663."),
    dict(id="imperial-city", name="Imperial City (Huangcheng)", polygon=R(PC_S, IC_S, ICW, ICE), periods=GRID,
         description="The government quarter, a Sui innovation: ministries, courts, the guards' offices, the imperial ancestral temple and the altar of soil and grain, along seven east-west and five north-south streets. No one lived here but officials on duty."),
    dict(id="daming-palace", name="Daming Palace", polygon=R(NORTH, N_WALL, 108.9534, 108.9714), periods=TANG,
         description="The 'Palace of Great Brilliance', the main seat of the Tang court from 663: front halls stepped up the plateau from the Danfeng gate, the inner palace round the Taiye pond to the north."),
    dict(id="wannian", name="Wannian county (the east)", polygon=R(PC_S, SOUTH, ICE, EAST), periods=TANG,
         description="East of Zhuque Avenue the wards belonged to Wannian county (Daxing county under the Sui): higher ground, nearer the Daming Palace, with the mansions of the great, the East Market and the pleasure quarter of Pingkang."),
    dict(id="changan-county", name="Chang'an county (the west)", polygon=R(PC_S, SOUTH, WEST, ICW), periods=TANG,
         description="West of the axis, Chang'an county: the West Market and its foreign merchants, Sogdian, Persian and Turkic communities, Zoroastrian and Nestorian temples, and more commoners' wards."),
    dict(id="pingkang", name="Pingkang ward", polygon=R(CHUNMING, IC_S, ICE, E34), periods=["tang-750", "late-tang-880"],
         description="The ward between the Imperial City and the East Market, close to the examination offices: lodgings of candidates and provincial liaison offices, and in its north-east lanes the 'Northern Quarter' of courtesans described by Sun Qi in 884."),
    dict(id="ming-xian", name="Xi'an walled city", polygon=R(MN, MS, MW, ME), periods=MING,
         description="The Ming city of the 1370s: four main streets from four gates, the Prince of Qin's palace in the north-east, the garrison in the north-west, the Hui lanes round the Great Mosque near the Drum Tower."),
]

LABELS = [
    dict(text="Daxing", position=(34.2395, 108.9720), size="lg", periods=SUI),
    dict(text="Chang'an", position=(34.2395, 108.9720), size="lg", periods=TANG),
    dict(text="Xi'an", position=(34.2740, 108.9300), size="lg", periods=MING),
    dict(text="Zhuque Avenue", position=(34.2310, Z), size="md", rotation=-90, periods=GRID),
    dict(text="Palace City", position=(34.2805, 108.9250), size="md", periods=GRID),
    dict(text="Imperial City", position=(34.2655, 108.9250), size="md", periods=GRID),
    dict(text="Daming Palace", position=(34.2898, 108.9690), size="md", periods=TANG),
    dict(text="Jiedong (east of the street)", position=(34.2325, 108.9560), size="sm", periods=TANG),
    dict(text="Jiexi (west of the street)", position=(34.2325, 108.9130), size="sm", periods=TANG),
    dict(text="Forbidden Park", position=(34.2880, 108.9100), size="sm", periods=GRID),
    dict(text="Fields of the old Tang city", position=(34.2300, 108.9200), size="md", periods=MING),
    dict(text="Ruins of the Daming Palace", position=(34.2895, 108.9690), size="sm", periods=MING),
]

SOURCES = [
    dict(id="wiki-changan", title="Chang'an", author="Wikipedia", url="https://en.wikipedia.org/wiki/Chang%27an"),
    dict(id="wiki-xian", title="Xi'an", author="Wikipedia", url="https://en.wikipedia.org/wiki/Xi%27an"),
    dict(id="wiki-fortifications-xian", title="Fortifications of Xi'an", author="Wikipedia", url="https://en.wikipedia.org/wiki/Fortifications_of_Xi%27an"),
    dict(id="wiki-yuwen-kai", title="Yuwen Kai", author="Wikipedia", url="https://en.wikipedia.org/wiki/Yuwen_Kai"),
    dict(id="xiong", title="Sui-Tang Chang'an: A Study in the Urban History of Medieval China", author="Victor Cunrui Xiong", year=2000),
    dict(id="heng", title="Cities of Aristocrats and Bureaucrats: The Development of Medieval Chinese Cityscapes", author="Heng Chye Kiang", year=1999),
    dict(id="steinhardt", title="Chinese Imperial City Planning", author="Nancy Shatzman Steinhardt", year=1990),
    dict(id="xu-song", title="Tang liangjing chengfang kao (Study of the Wards of the Two Tang Capitals)", author="Xu Song", year=1810),
]
