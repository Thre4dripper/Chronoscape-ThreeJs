# Khanbaliq / Dadu / Beijing: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
import math

JIN = ["jin-1200"]
YUAN = ["kublai-1290"]
MING = ["ming-1450"]
QING = ["qing-1750"]
MQ = MING + QING
DADU = YUAN + MQ                     # the walled city laid out in 1267 and its successors
ALL = JIN + DADU

# All positions WGS84 (as on OpenStreetMap). Beijing's central axis runs at about 116.391 E and leans
# some 2 degrees west of north; the Drum and Bell Towers stand a little west of the Tiananmen line.
# The frame holds the middle of Dadu and the Ming Inner City; the Yuan north wall (2.5 km beyond the Ming one)
# and the Altar of Heaven (3 km south) lie outside it.
WEST, EAST, NORTH, SOUTH = 116.3450, 116.4320, 39.9620, 39.8960

# Ming Inner City walls (north wall 1368, south wall moved south 1419), with the cut-off north-west corner
MN, MS, MW, ME = 39.9487, 39.8992, 116.3490, 116.4280
NW_BEVEL_N, NW_BEVEL_W = 116.3575, 39.9425
# Yuan Dadu: east and west walls on the Ming lines, the south wall along today's Chang'an Avenue
YS, YW, YE = 39.9055, 116.3490, 116.4280
# Main streets (longitudes)
XS = 116.3676           # Xidan - Xisi - Xinjiekou
DSM = 116.3740          # Deshengmen Inner Street
ADM = 116.4021          # Andingmen Inner Street
WFJ = 116.4050          # Wangfujing
DS = 116.4110           # Dongdan - Dongsi - Yonghegong street
AX = 116.3908           # the axis at the Forbidden City
# Main streets (latitudes)
CA = 39.9067            # Chang'an Street (Ming)
FCM = 39.9238           # Fuchengmen - Chaoyangmen line
GL = 39.9402            # Gulou East Street - Dongzhimen
XZM = 39.9398           # Xizhimen street
# Imperial City (Ming) and the Yuan Huangcheng
IN, IS, IW, IE = 39.9335, 39.9073, 116.3730, 116.4011
YIN, YIS, YIW, YIE = 39.9320, 39.9080, 116.3730, 116.3985
# Forbidden City and the Yuan palace city
FC_N, FC_S, FC_W, FC_E = 39.92063, 39.91197, 116.38639, 116.39521
YP_N, YP_S, YP_W, YP_E = 39.92380, 39.91520, 116.38617, 116.39483


def R(n, s, w, e):
    """A rectangle between two latitudes and two longitudes."""
    return [(n, w), (n, e), (s, e), (s, w)]


def oval(lat, lon, rx, ry, n=18, wobble=0.06):
    """An irregular oval rx by ry metres round (lat, lon)."""
    kx = 111320.0 * math.cos(math.radians(lat))
    pts = []
    for i in range(n):
        a = math.tau * i / n
        k = 1 + wobble * math.sin(3 * a + 0.7)
        pts.append((round(lat + ry * k * math.sin(a) / 110950.0, 6), round(lon + rx * k * math.cos(a) / kx, 6)))
    return pts


CITY = dict(
    name="Khanbaliq", subtitle="Dadu of the Great Khan, and Beijing",
    description="The centre of the Yuan capital Dadu (Khanbaliq) and of Ming and Qing Beijing, from the Jin emperors' lake palace of the 1170s to Qianlong's city: the palaces round the Taiye lakes, the Forbidden City, the Drum and Bell Towers and the Jishuitan harbour at the end of the Grand Canal. The Yuan north wall and the Altar of Heaven lie beyond the frame. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="kublai-1290",
    world=dict(heightScale=1.0, walls=["#D6CBB6", "#CBBFA8", "#BFB39C"], roofs=["#5E5F62", "#6A6866", "#57595C"]),
    camera=dict(target=(39.9230, 116.3900), distance=46),
)
FRAME = ((NORTH, WEST), (SOUTH, EAST))
PALETTE = dict(parchment="#E8D6AE", ink="#5C4232", water="#62878A", hill="#7A7D58", road="#8C6C4C")
COMPASS = (39.9585, 116.4260)
CARTOUCHE = (39.8968, 116.3460)

PERIODS = [
    dict(id="jin-1200", label="Jin Zhongdu and the Daning Palace", year=1200, startYear=1153, endYear=1263,
         summary="In 1153 the Jurchen Jin moved their capital to Yanjing and renamed it Zhongdu; its walls lay south-west of this map. North-east of them, round lakes fed by the Gaoliang river, Emperor Shizong built the Daning detached palace in 1179, with Qionghua island heaped up in the lake and crowned by a hall. The rest is villages, temples and fields.",
         population="Zhongdu perhaps several hundred thousand; this area a few villages",
         feel="Reed-cutters and fishermen on the lakes, the emperor's summer escort raising dust on the road from Zhongdu, millet drying on village threshing floors.",
         style="sinic",
         houses=dict(title="Villages north-east of Zhongdu", text="Farm compounds of pounded earth and grey brick round a yard with a well, a millet store and a pig pen; a village temple, a wine shop and a smithy on the road to the capital."),
         outskirts=dict(title="Millet and sorghum fields", text="Open fields of millet, sorghum and wheat, vegetable plots by the lakes, graves among the trees, and the parks and hunting grounds of the Daning palace.")),
    dict(id="kublai-1290", label="Khanbaliq, the Yuan capital", year=1290, startYear=1264, endYear=1367,
         summary="Kublai Khan had Liu Bingzhong lay out a new capital beside the Jin lakes from 1267: a rammed-earth rectangle of about 28.6 km round with eleven gates, a grid of avenues and lanes, the palace on the Taiye lake, the Drum and Bell Towers at the centre and, from 1293, Grand Canal grain barges in Jishuitan. The Mongols called it Khanbaliq, 'city of the khan'.",
         population="perhaps 500,000 to 900,000 (estimates vary widely)",
         feel="Camel bells and Mongol horsemen, Persian, Uyghur and Italian voices in the Xiejie market, coal smoke, and the drum beating the night watches from the tower.",
         style="sinic",
         houses=dict(title="Hutongs of Dadu", text="Between the avenues run east-west lanes (hutong) some 70-80 m apart. In 1285 plots of 8 mu (about half a hectare) were granted first to the rich and to officials; courtyard houses of grey brick and timber filled them, while ordinary families built smaller courts of rammed earth."),
         outskirts=dict(title="Empty wards and gardens", text="Much of the walled area, the north above all, was never fully built: vegetable gardens, orchards and fields between scattered compounds, temples, felt tents and horse lines.")),
    dict(id="ming-1450", label="Ming Beijing after Yongle", year=1450, startYear=1368, endYear=1643,
         summary="Xu Da took Dadu in 1368 and moved its north wall 2.5 km south. The Yongle emperor made Beijing the capital, formally in 1421: the Forbidden City (1406-1420) on the old palace site, Jingshan heaped up from the moat spoil, a larger Imperial City, the south wall moved south (1419), and in 1436-1439 the gates rebuilt with barbicans and arrow towers.",
         population="perhaps 600,000 to 900,000",
         feel="Eunuchs' sedan chairs in the lanes outside the Imperial City, clerks hurrying to the ministries at dawn, soldiers on the new brick walls, and the yellow roofs glimpsed over red walls.",
         style="sinic",
         houses=dict(title="Siheyuan of the Inner City", text="Courtyard houses of grey brick under grey tile, gated on the hutong: an entrance court behind a screen wall, the main hall facing south for the elders, side halls for sons and their wives, a back row for women and servants. Princes and eunuchs build bigger mansions with gardens."),
         outskirts=dict(title="Gardens inside the walls", text="Vegetable gardens, temple grounds, garrison yards and empty lots fill the far corners of the Inner City, especially round the Jishuitan lakes and in the north-east.")),
    dict(id="qing-1750", label="Qianlong's Beijing", year=1750, startYear=1644, endYear=1911,
         summary="The Manchus entered in June 1644 and gave the Inner City to the Eight Banners, moving most Han Chinese to the Outer City. They kept and rebuilt the Ming palaces: Tiananmen and the White Dagoba on Qionghua island in 1651, the Hall of Supreme Harmony in 1695-1697. Under Qianlong came the Yonghegong lamasery (1744), the brick Bell Tower (1745-1747) and the Jingshan pavilions (1751).",
         population="perhaps 700,000 to 1,000,000",
         feel="Bannermen with caged larks in the tea houses, Tibetan lamas in maroon at the Yonghegong, camel trains of coal from the Western Hills, and the noon gun of the Drum Tower.",
         style="sinic",
         houses=dict(title="Banner courtyards", text="Each banner holds a sector of the Inner City; its families live in rows of siheyuan of grey brick round one, two or three courts, with jujube and pomegranate trees, goldfish jars and a screen wall inside the gate. Princes' mansions (wangfu) take whole blocks."),
         outskirts=dict(title="Banner barracks and gardens", text="Soldiers' rows, granaries, temple gardens and vegetable plots in the corners of the city, and lotus ponds round Shichahai.")),
]

# ---------------------------------------------------------------- water
WATER = [
    # the lakes north of the palace: one large Jishuitan (Haizi) under the Jin and Yuan, three lakes after the Ming walls
    dict(id="haizi-jin", name="Lakes of the Gaoliang river", width=380, periods=JIN,
         path=[(39.9345, 116.3875), (39.9390, 116.3830), (39.9430, 116.3760), (39.9465, 116.3700), (39.9490, 116.3660)],
         blurb="A chain of shallow lakes and reed beds where the Gaoliang river spread out north-east of Zhongdu. Kublai's planners would put the centre of their new city on its eastern shore."),
    dict(id="jishuitan-yuan", name="Jishuitan (the Haizi)", width=380, periods=YUAN,
         path=[(39.9345, 116.3875), (39.9390, 116.3830), (39.9430, 116.3760), (39.9465, 116.3700), (39.9490, 116.3660)],
         blurb="'The Sea', the great lake inside Dadu, fed by springs led from the Western Hills by Guo Shoujing. From 1293 it was the terminus of the Grand Canal: the Yuan history says its surface was 'covered with boats'."),
    dict(id="qianhai", name="Qianhai (Front Lake)", width=170, periods=MQ,
         path=[(39.9342, 116.3878), (39.9372, 116.3862), (39.9390, 116.3850)],
         blurb="The southern of the three lakes of Shichahai, all that the Ming walls left of the Yuan Jishuitan. Lotus grows in summer; in winter people skate and sled on it."),
    dict(id="houhai", name="Houhai (Rear Lake)", width=200, periods=MQ,
         path=[(39.9395, 116.3838), (39.9415, 116.3790), (39.9435, 116.3745)],
         blurb="The middle lake, joined to Qianhai under the Yinding bridge. Princes' mansions and temples line its banks; the Ten Temples (Shicha) gave the lakes their name."),
    dict(id="xihai", name="Xihai (Jishuitan)", width=170, periods=MQ,
         path=[(39.9445, 116.3725), (39.9465, 116.3708)],
         blurb="The western lake, which kept the old name Jishuitan, 'pool of gathered water'. Water from the Western Hills enters here through a sluice under the north wall."),
    # the Taiye lakes
    dict(id="beihai", name="Taiye lake: Beihai", width=470, periods=ALL,
         path=[(39.9293, 116.3812), (39.9265, 116.3816), (39.9250, 116.3822)],
         blurb="The northern basin of the Taiye ('Great Liquid') lake round Qionghua island. The Jin dug it out for the Daning palace; Kublai built his palace on its east bank; the Ming and Qing kept it as the Western Park (Xiyuan)."),
    dict(id="beihai-south", name="Taiye lake", width=180, periods=ALL,
         path=[(39.9240, 116.3822), (39.9214, 116.3820)]),
    dict(id="beihai-bay", name="Taiye lake", width=90, periods=ALL,
         path=[(39.9245, 116.3835), (39.9230, 116.3846)]),
    dict(id="zhonghai", name="Taiye lake: Zhonghai", width=210, periods=ALL,
         path=[(39.9212, 116.3818), (39.9175, 116.3812), (39.9135, 116.3812), (39.9112, 116.3818)],
         blurb="The middle basin, west of the palace. In the Yuan it was the southern end of the Taiye lake; the Ming called it the Middle Sea when they dug the Southern Sea below it."),
    dict(id="nanhai", name="Nanhai (Southern Sea)", width=260, periods=MQ,
         path=[(39.9105, 116.3825), (39.9090, 116.3842)],
         blurb="Dug in the early Ming to complete the three seas of the Western Park, round the Yingtai island where the Qing emperors later held audiences and fished."),
    # canals and the palace water supply
    dict(id="qianhai-beihai", name="Channel into the Taiye lake", width=25, periods=MQ,
         path=[(39.9342, 116.3878), (39.9318, 116.3855), (39.9300, 116.3840)],
         blurb="The Ming fed the palace lakes from Shichahai through a channel under the Imperial City wall."),
    dict(id="jinshui-yuan", name="Jinshui river (palace water)", width=10, periods=YUAN,
         path=[(39.9405, WEST), (39.9400, 116.3500), (39.9330, 116.3640), (39.9300, 116.3730), (39.9282, 116.3792)],
         blurb="The Yuan led clean water from the Yuquan spring to the Taiye lake in a channel of its own, kept apart from the canal water and carried over crossing streams in troughs. Its course through the city follows the usual reconstruction."),
    dict(id="tonghui-yuan", name="Tonghui canal", width=24, periods=YUAN,
         path=[(39.9348, 116.3878), (39.9352, 116.3903), (39.9350, 116.3940), (39.9338, 116.3978), (39.9318, 116.3994), (39.9200, 116.3995), (39.9080, 116.3995), (YS - 0.0008, 116.3995), (39.9010, 116.4100), (SOUTH, 116.4230)],
         blurb="Guo Shoujing's canal of 1292-1293, the last stage of the Grand Canal: from Jishuitan under the Wanning bridge, along the east wall of the Imperial City and out by the Wenming gate to Tongzhou, with lock gates to lift the barges. Kublai named it 'Tonghui', 'Free-flowing Benefit'."),
    dict(id="yuhe", name="Yuhe (Jade River)", width=14, periods=MQ,
         path=[(39.9348, 116.3878), (39.9352, 116.3903), (39.9350, 116.3940), (39.9338, 116.3978), (39.9318, 116.3994), (39.9200, 116.3995), (39.9073, 116.3995), (MS + 0.0003, 116.3998)],
         blurb="The old Tonghui canal through the city. Once the Ming Imperial City wall enclosed it, boats could no longer pass; it became a drain from Shichahai to the south moat, and the grain barges stopped at Dongbianmen."),
    dict(id="gaoliang", name="Gaoliang river", width=26, periods=JIN + YUAN,
         path=[(39.9512, WEST), (39.9505, 116.3550), (39.9497, 116.3610), (39.9490, 116.3660)],
         blurb="The river from the springs at the foot of the Western Hills that fed the lakes. The Yuan diverted more spring water into it to keep the canal full."),
    dict(id="gaoliang-mq", name="Gaoliang river", width=26, periods=MQ,
         path=[(39.9512, WEST), (39.9505, 116.3550), (39.9497, 116.3590)]),
    dict(id="sluice-mq", name="Inflow to Jishuitan", width=16, periods=MQ,
         path=[(MN + 0.0011, 116.3702), (39.9470, 116.3706)]),
    # moats
    dict(id="yuan-moat", name="Moat of Dadu", width=30, periods=YUAN,
         path=[(NORTH, YW - 0.0010), (YS - 0.0008, YW - 0.0010), (YS - 0.0008, YE + 0.0010), (NORTH, YE + 0.0010)],
         blurb="The moat outside the rammed-earth walls, crossed by bridges at the gates."),
    dict(id="ming-moat", name="City moat (Huchenghe)", width=36, periods=MQ,
         path=[(MN + 0.0011, NW_BEVEL_N), (MN + 0.0011, ME + 0.0011), (MS - 0.0009, ME + 0.0011), (MS - 0.0009, MW - 0.0011), (NW_BEVEL_W, MW - 0.0011), (MN + 0.0011, NW_BEVEL_N)],
         blurb="The moat round the Ming walls, fed by the Gaoliang river at the north-west corner and draining east into the Tonghui river at Dongbianmen."),
    dict(id="tonghui-mq", name="Tonghui river (to Tongzhou)", width=30, periods=MQ,
         path=[(MS - 0.0009, ME + 0.0011), (39.8975, EAST)]),
    dict(id="tongzi-he", name="Tongzi river (palace moat)", width=52, periods=MQ,
         path=[(39.91228, 116.3899), (39.91228, 116.38585), (39.92105, 116.38585), (39.92105, 116.39575), (39.91228, 116.39575), (39.91228, 116.3917)],
         blurb="The moat of the Forbidden City, 52 m wide, dug in the 1410s; its spoil went into Jingshan. Its water came from the Taiye lake."),
]

ISLANDS = [
    dict(name="Qionghua island", polygon=oval(39.9253, 116.3828, 135, 135, 20, 0.05)),
    dict(name="Yingtai", polygon=oval(39.9089, 116.3842, 55, 45, 12, 0.08), periods=MQ),
]

HILLS = []

# ---------------------------------------------------------------- roads
ROADS = [
    # the Jin countryside
    dict(id="zhongdu-road", name="Road to Zhongdu", width=12, style="major", labelled=True, periods=JIN,
         path=[(39.9222, 116.3880), (39.9100, 116.3870), (39.9000, 116.3790), (SOUTH, 116.3720)],
         blurb="The road from the Daning palace south-west to the north-east gates of Zhongdu, about 3 km away."),
    dict(id="jin-north-road", name="Road north to Changping", width=8, labelled=True, periods=JIN,
         path=[(39.9225, 116.3885), (39.9330, 116.3900), (39.9450, 116.3930), (NORTH, 116.3960)]),
    dict(id="jin-east-road", name="Road east to the Wenyu river", width=8, periods=JIN,
         path=[(39.9225, 116.3885), (39.9235, 116.4100), (39.9255, EAST)]),
    # Dadu and Beijing
    dict(id="qianbulang-yuan", name="Qianbulang (the Thousand-Step Corridor)", width=40, style="major", labelled=True, periods=YUAN,
         path=[(YS, 116.3912), (YIS, 116.3911), (YP_S - 0.0002, 116.3908)],
         blurb="The ceremonial way from the Lizheng gate in the city wall through the Lingxing gate of the Imperial City to the palace's Chongtian gate, flanked by covered galleries; the Ming repeated it in front of Tiananmen."),
    dict(id="haizi-street", name="Street of the Haizi bridge", width=25, style="major", labelled=True, periods=YUAN,
         path=[(YIN, 116.3903), (39.9352, 116.3903), (39.9398, 116.3898)],
         blurb="The axis north of the palace to the Central Pavilion (Zhongxin ge), which marked the middle of the city, and the Drum Tower beside it."),
    dict(id="dianmen-outer", name="Di'anmen Outer Street", width=25, style="major", labelled=True, periods=MQ,
         path=[(IN + 0.0002, 116.3901), (39.9352, 116.3902), (39.9394, 116.3897)],
         blurb="The axis street from the Imperial City's north gate over the Wanning bridge to the Drum Tower, lined with shops, tea houses and the 'tobacco-pipe' lane to the lakes."),
    dict(id="xiejie-yuan", name="Xiejie (Slanting Street)", width=20, style="major", labelled=True, periods=YUAN,
         path=[(39.9440, 116.3790), (39.9425, 116.3835), (39.9405, 116.3858)],
         blurb="The diagonal street along the north-east shore of Jishuitan, the busiest market of Dadu: silks, furs, pearls, horses and camels, near the harbour and the Drum Tower."),
    dict(id="gulou-west", name="Gulou West Street", width=20, labelled=True, periods=MQ,
         path=[(39.9455, DSM), (39.9440, 116.3790), (39.9425, 116.3840), (39.9402, 116.3888)],
         blurb="The old Xiejie, the one diagonal street of the grid, following the shore of the Yuan harbour."),
    dict(id="chongren-street", name="Street to the Chongren gate", width=24, periods=YUAN,
         path=[(39.9402, 116.3872), (39.9403, DS), (39.9405, YE)]),
    dict(id="gulou-east", name="Gulou East Street", width=24, labelled=True, periods=MQ,
         path=[(39.9402, 116.3902), (39.9403, DS), (39.9405, ME)],
         blurb="East from the Drum Tower to the Dongzhimen gate, where carts of timber and bricks from the Grand Canal came into the city."),
    dict(id="xizhimen-street", name="Xizhimen Street", width=22, periods=DADU,
         path=[(39.9398, MW), (39.9405, XS)],
         blurb="From the west gate (Heyimen under the Yuan, Xizhimen under the Ming), by which carts of spring water from the Jade Spring hill came in for the palace."),
    dict(id="xisi-yuan", name="Shuncheng gate street", width=26, style="major", labelled=True, periods=YUAN,
         path=[(YS, 116.3685), (39.9067, XS), (FCM, XS), (39.9405, XS), (39.9430, XS)]),
    dict(id="xisi", name="Xidan - Xisi Street", width=26, style="major", labelled=True, periods=MQ,
         path=[(MS, 116.3685), (39.9067, XS), (FCM, XS), (39.9405, XS), (39.9480, XS)],
         blurb="The main north-south street of the west city, from the Xuanwu gate through the crossings of Xidan and Xisi, each marked by memorial arches (pailou), to Xinjiekou."),
    dict(id="dongsi-yuan", name="Wenming gate street", width=26, style="major", labelled=True, periods=YUAN,
         path=[(YS, DS), (FCM, DS), (39.9403, DS), (NORTH, DS)]),
    dict(id="dongsi", name="Dongdan - Dongsi Street", width=26, style="major", labelled=True, periods=MQ,
         path=[(MS, DS), (39.9067, DS), (FCM, DS), (39.9403, DS), (MN - 0.0003, DS)],
         blurb="The main north-south street of the east city, from the Chongwen gate past the arches of Dongdan and Dongsi to the Yonghegong."),
    dict(id="andingmen-inner", name="Andingmen Inner Street", width=22, labelled=True, periods=MQ,
         path=[(IN + 0.0003, ADM), (GL, ADM), (MN, ADM)]),
    dict(id="anzhen-yuan", name="Anzhen gate street", width=22, periods=YUAN,
         path=[(YIN + 0.0003, ADM), (GL, ADM), (NORTH, ADM)]),
    dict(id="deshengmen-inner", name="Deshengmen Inner Street", width=20, periods=MQ,
         path=[(MN, DSM), (39.9455, DSM)]),
    dict(id="fuchengmen-street", name="Fuchengmen Inner Street", width=22, labelled=True, periods=DADU,
         path=[(FCM, MW), (FCM, XS), (39.9238, IW)],
         blurb="The road from the west gate (Pingzemen under the Yuan, Fuchengmen under the Ming), the coal road from the Western Hills; it passes the Miaoying White Dagoba and the Guangji temple."),
    dict(id="chaoyangmen-street", name="Chaoyangmen Inner Street", width=22, labelled=True, periods=DADU,
         path=[(FCM, YIE + 0.0003), (FCM, DS), (FCM, ME)],
         blurb="From the east gate (Qihuamen under the Yuan, Chaoyangmen under the Ming) where the grain from the canal granaries came in."),
    dict(id="changan-west", name="West Chang'an Street", width=26, labelled=True, periods=MQ,
         path=[(CA, XS), (CA, 116.3848)]),
    dict(id="changan-east", name="East Chang'an Street", width=26, labelled=True, periods=MQ,
         path=[(CA, 116.3977), (CA, DS)]),
    dict(id="tianjie", name="Tianjie (the Imperial Way)", width=40, style="major", labelled=True, periods=MQ,
         path=[(39.9012, 116.3915), (39.9069, 116.3913)],
         blurb="The T-shaped walled square in front of Tiananmen, with the Thousand-Step Corridor of offices along its sides; edicts were lowered from the gate to officials kneeling here."),
    dict(id="qianmen-street", name="Qianmen Street", width=26, style="major", periods=MQ,
         path=[(MS - 0.0006, 116.3916), (SOUTH, 116.3918)]),
    dict(id="wangfujing", name="Wangfujing (Street of the Princes' Mansions)", width=20, labelled=True, periods=MQ,
         path=[(CA, WFJ), (FCM, WFJ)],
         blurb="Named after the ten princes' mansions built along it under Yongle."),
    dict(id="donganmen-street", name="Dong'anmen Street", width=18, periods=MQ,
         path=[(39.9150, IE + 0.0003), (39.9150, WFJ)]),
    dict(id="dianmen-east", name="Di'anmen East Street", width=18, periods=MQ,
         path=[(IN + 0.0005, 116.3908), (IN + 0.0005, IE + 0.0004)]),
    dict(id="guozijian-street", name="Chengxian Street (Guozijian Street)", width=12, labelled=True, periods=MQ,
         path=[(39.9446, ADM), (39.9446, DS)],
         blurb="The quiet lane of the Temple of Confucius and the Imperial Academy, spanned by memorial arches; officials had to dismount at its ends."),
]

WALLS = [
    dict(id="yuan-wall", name="Walls of Dadu", periods=YUAN,
         path=[(NORTH, YW), (YS, YW), (YS, YE), (NORTH, YE)],
         blurb="Rammed earth, about 28.6 km round (7.6 by 6.7 km), with eleven gates; begun 1267. In the rains the walls were protected with reed matting. The north wall, 2.5 km beyond the frame, still stands as a long earth mound."),
    dict(id="yuan-imperial", name="Huangcheng (Imperial City) wall", closed=True, periods=YUAN,
         path=R(YIN, YIS, YIW, YIE),
         blurb="The Yuan imperial city (also called the Xiaocheng), about 20 li round, enclosing the Taiye lake with the emperor's palace on the east bank and the palaces of the crown prince and the empress dowager on the west."),
    dict(id="ming-wall", name="Inner City wall (Neicheng)", closed=True, periods=MQ,
         path=[(MN, NW_BEVEL_N), (MN, ME), (MS, ME), (MS, MW), (NW_BEVEL_W, MW)],
         blurb="Xu Da's north wall of 1368 and Yongle's south wall of 1419 joined to the old Yuan east and west walls: about 24 km round, faced with brick from 1445, 12 m high, with nine gates, barbicans and arrow towers. The north-west corner is cut off by the lakes."),
    dict(id="ming-imperial", name="Imperial City wall (Huangcheng)", closed=True, periods=MQ,
         path=R(IN, IS, IW, IE),
         blurb="Yongle's Imperial City, some 11 km round, red-plastered under yellow tiles: the lakes of the Western Park, Jingshan, temples, storehouses and the offices and workshops of the eunuch directorates. Its four gates were Tiananmen, Di'anmen, Dong'anmen and Xi'anmen."),
    dict(id="tianjie-wall", name="Walls of the Imperial Way", periods=MQ,
         path=[(IS, 116.3975), (39.9062, 116.3975), (39.9062, 116.3935), (39.9010, 116.3935), (39.9010, 116.3895), (39.9062, 116.3895), (39.9062, 116.3850), (IS, 116.3850)],
         blurb="The red walls of the T-shaped square in front of Tiananmen, closed by the Damingmen on the south and the Chang'an Left and Right gates on the east and west."),
]

GATES = [
    dict(id="lizhengmen", name="Lizheng gate", position=(YS, 116.3912), periods=YUAN),
    dict(id="wenmingmen", name="Wenming gate", position=(YS, DS), periods=YUAN),
    dict(id="shunchengmen", name="Shuncheng gate", position=(YS, 116.3685), periods=YUAN),
    dict(id="qihuamen", name="Qihua gate", position=(FCM, YE), periods=YUAN),
    dict(id="chongrenmen", name="Chongren gate", position=(39.9405, YE), periods=YUAN),
    dict(id="pingzemen", name="Pingze gate", position=(FCM, YW), periods=YUAN),
    dict(id="heyimen", name="Heyi gate", position=(39.9398, YW), periods=YUAN),
    dict(id="lingxingmen", name="Lingxing gate", position=(YIS, 116.3911), periods=YUAN),
    dict(id="houzaimen", name="Houzai gate", position=(YIN, 116.3903), periods=YUAN),
    dict(id="dongzhimen", name="Dongzhimen", position=(39.9405, ME), periods=MQ),
    dict(id="chaoyangmen", name="Chaoyangmen", position=(FCM, ME), periods=MQ),
    dict(id="chongwenmen", name="Chongwenmen", position=(MS, DS), periods=MQ),
    dict(id="zhengyangmen", name="Zhengyangmen (Qianmen)", position=(MS, 116.3915), periods=MQ),
    dict(id="xuanwumen", name="Xuanwumen", position=(MS, 116.3685), periods=MQ),
    dict(id="fuchengmen", name="Fuchengmen", position=(FCM, MW), periods=MQ),
    dict(id="xizhimen", name="Xizhimen", position=(39.9398, MW), periods=MQ),
    dict(id="xianmen", name="Xi'anmen", position=(39.9238, IW), periods=MQ),
    dict(id="donganmen", name="Dong'anmen", position=(39.9150, IE), periods=MQ),
    dict(id="damingmen", name="Damingmen", position=(39.9010, 116.3915), periods=MING),
    dict(id="daqingmen", name="Daqingmen", position=(39.9010, 116.3915), periods=QING),
]

BRIDGES = [
    dict(id="wanning-b", name="Wanning bridge", path=[(39.9348, 116.3903), (39.9356, 116.3902)], build="stone", arches=1, landmarkId="wanning-bridge", periods=DADU,
         blurb="The bridge that carries the axis over the outflow of Jishuitan, 'the bridge of ten thousand tranquillities'."),
    dict(id="yinding", name="Yinding bridge", path=[(39.9396, 116.3849), (39.9389, 116.3839)], build="stone", arches=1, periods=MQ,
         blurb="The small 'silver ingot' bridge at the neck between Qianhai and Houhai, famous for its view of the Western Hills."),
    dict(id="yuan-wood-bridge", name="Timber bridge to Yingzhou", path=[(39.9211, 116.3802), (39.9211, 116.3836)], build="timber", arches=10, periods=YUAN,
         blurb="The Yuan timber bridge from the Round City across the lake to the palaces on the west bank, with a drawbridge in the middle."),
    dict(id="jinao-yudong", name="Jin'ao Yudong bridge", path=[(39.9211, 116.3802), (39.9211, 116.3836)], build="stone", arches=9, periods=MQ,
         blurb="The Ming marble bridge between Beihai and Zhonghai, named after the gold turtle and jade rainbow arches at its two ends."),
    dict(id="yongan", name="Yong'an bridge", path=[(39.9241, 116.3838), (39.9226, 116.3852)], build="stone", arches=3, periods=DADU,
         blurb="The bridge from the Round City to Qionghua island, with a decorated arch at each end."),
]

AQUEDUCTS = []

# ---------------------------------------------------------------- built-up areas
_YUAN_BLOCKS = [
    dict(name="Wards of the Pingze gate", polygon=R(FCM - 0.0003, YS + 0.0004, YW + 0.0004, XS - 0.0003), density="dense"),
    dict(name="Wards of the Shuncheng gate", polygon=R(FCM - 0.0003, YS + 0.0004, XS + 0.0003, YIW - 0.0004), density="dense"),
    dict(name="Wards of the Heyi gate", polygon=R(XZM - 0.0003, FCM + 0.0003, YW + 0.0004, XS - 0.0003), density="dense"),
    dict(name="Wards west of the Imperial City", polygon=R(YIN, FCM + 0.0003, XS + 0.0003, YIW - 0.0004), density="dense"),
    dict(name="North-west wards by the Haizi", polygon=R(39.9500, XZM + 0.0003, YW + 0.0004, XS - 0.0003), density="loose"),
    dict(name="Market quarter of the Xiejie", polygon=R(39.9460, YIN + 0.0004, 116.3780, 116.3960), density="dense"),
    dict(name="Wards of the Chongren gate", polygon=R(39.9487, GL + 0.0003, 116.3960, DS - 0.0003), density="dense"),
    dict(name="North-east wards", polygon=R(39.9487, GL + 0.0003, DS + 0.0003, YE - 0.0004), density="loose"),
    dict(name="Wards east of the palace", polygon=R(GL - 0.0003, FCM + 0.0003, YIE + 0.0004, DS - 0.0003), density="dense"),
    dict(name="Wards of the Qihua gate", polygon=R(GL - 0.0003, FCM + 0.0003, DS + 0.0003, YE - 0.0004), density="dense"),
    dict(name="Wards of the Wenming gate", polygon=R(FCM - 0.0003, YS + 0.0004, YIE + 0.0004, DS - 0.0003), density="dense"),
    dict(name="South-east wards", polygon=R(FCM - 0.0003, YS + 0.0004, DS + 0.0003, YE - 0.0004), density="dense"),
    dict(name="Thinly built northern wards", polygon=R(NORTH - 0.0005, 39.9500, 116.3800, DS - 0.0003), density="loose"),
    dict(name="Palaces of the west bank (Longfu and Xingsheng)", polygon=R(YIN - 0.0003, YIS + 0.0003, YIW + 0.0003, 116.3790), density="loose"),
    dict(name="Suburbs toward Zhongdu", polygon=R(YS - 0.0016, SOUTH, YW, YE), density="loose"),
]

_MQ_BLOCKS = [
    ("Xuanwumen Inner quarter", R(CA - 0.0003, MS + 0.0004, MW + 0.0004, XS - 0.0003), "dense", "dense"),
    ("Xidan quarter and the western ministries", [(CA - 0.0003, XS + 0.0003), (CA - 0.0003, 116.3846), (39.9058, 116.3846), (39.9058, 116.3890), (MS + 0.0004, 116.3890), (MS + 0.0004, XS + 0.0003)], "dense", "dense"),
    ("Ministries east of the Imperial Way", [(CA - 0.0003, 116.3980), (CA - 0.0003, DS - 0.0003), (MS + 0.0004, DS - 0.0003), (MS + 0.0004, 116.3940), (39.9058, 116.3940), (39.9058, 116.3980)], "dense", "dense"),
    ("Chongwenmen Inner quarter", R(CA - 0.0003, MS + 0.0004, DS + 0.0003, ME - 0.0004), "dense", "dense"),
    ("Xisi south", R(FCM - 0.0003, CA + 0.0003, MW + 0.0004, XS - 0.0003), "dense", "dense"),
    ("Xidan north", R(FCM - 0.0003, CA + 0.0003, XS + 0.0003, IW - 0.0004), "dense", "dense"),
    ("Fuchengmen quarter", R(XZM - 0.0003, FCM + 0.0003, MW + 0.0004, XS - 0.0003), "dense", "dense"),
    ("Xisi north", R(IN, FCM + 0.0003, XS + 0.0003, IW - 0.0004), "dense", "dense"),
    ("Xinjiekou", [(MN - 0.0004, NW_BEVEL_N + 0.0004), (MN - 0.0004, XS - 0.0003), (XZM + 0.0003, XS - 0.0003), (XZM + 0.0003, MW + 0.0004), (NW_BEVEL_W - 0.0003, MW + 0.0004)], "loose", "dense"),
    ("Banks of Xihai and Houhai", R(MN - 0.0004, IN + 0.0004, XS + 0.0003, DSM - 0.0003), "loose", "dense"),
    ("North of the Bell Tower", R(MN - 0.0004, GL + 0.0003, DSM + 0.0003, ADM - 0.0003), "dense", "dense"),
    ("Shichahai and the Drum Tower", R(GL - 0.0003, IN + 0.0006, 116.3800, ADM - 0.0003), "dense", "dense"),
    ("Andingmen quarter", R(MN - 0.0004, GL + 0.0003, ADM + 0.0003, DS - 0.0003), "loose", "dense"),
    ("Dongzhimen quarter", R(MN - 0.0004, GL + 0.0003, DS + 0.0003, ME - 0.0004), "loose", "dense"),
    ("Jiaodaokou", R(GL - 0.0003, FCM + 0.0003, ADM + 0.0003, DS - 0.0003), "dense", "dense"),
    ("Imperial City's north-east corner", R(GL - 0.0003, FCM + 0.0003, IE + 0.0004, ADM - 0.0003), "dense", "dense"),
    ("Dongsi quarter", R(GL - 0.0003, FCM + 0.0003, DS + 0.0003, ME - 0.0004), "dense", "dense"),
    ("Princes' mansions of Wangfujing", R(FCM - 0.0003, CA + 0.0003, IE + 0.0004, WFJ - 0.0002), "dense", "dense"),
    ("Dongdan north", R(FCM - 0.0003, CA + 0.0003, WFJ + 0.0002, DS - 0.0003), "dense", "dense"),
    ("Chaoyangmen quarter", R(FCM - 0.0003, CA + 0.0003, DS + 0.0003, ME - 0.0004), "dense", "dense"),
    ("Storehouses and directorates of the Imperial City", R(IN - 0.0004, 39.9245, 116.3935, IE - 0.0003), "dense", "dense"),
    ("South-east Imperial City (Nanchizi)", R(39.9230, IS + 0.0004, 116.3962, IE - 0.0003), "loose", "dense"),
    ("Xishiku: west bank of the Western Park", R(IN - 0.0004, IS + 0.0004, IW + 0.0003, 116.3790), "dense", "dense"),
    ("Qianmen suburb", R(MS - 0.0013, SOUTH, 116.3800, 116.4050), "loose", "dense"),
]

BLOCKS = (
    [dict(b, periods=YUAN) for b in _YUAN_BLOCKS]
    + [dict(name=n, polygon=p, density=dm, periods=MING) for n, p, dm, dq in _MQ_BLOCKS]
    + [dict(name=n, polygon=p, density=dq, periods=QING) for n, p, dm, dq in _MQ_BLOCKS]
    + [
        dict(name="Xiliu village", polygon=R(39.9268, 39.9244, 116.3620, 116.3685), density="loose", periods=JIN),
        dict(name="Fishing village on the lakes", polygon=R(39.9448, 39.9420, 116.3830, 116.3885), density="loose", periods=JIN),
        dict(name="Hamlet east of the Daning palace", polygon=R(39.9182, 39.9160, 116.3950, 116.4005), density="loose", periods=JIN),
        dict(name="Village on the Zhongdu road", polygon=R(39.9032, 39.9005, 116.3765, 116.3825), density="loose", periods=JIN),
        dict(name="Eastern hamlet", polygon=R(39.9302, 39.9283, 116.4120, 116.4175), density="loose", periods=JIN),
        dict(name="Service quarter of the Daning palace", polygon=R(39.9212, 39.9185, 116.3870, 116.3925), density="loose", periods=JIN),
    ]
)

GARDENS = [
    # Jin: fields round the palace and the villages
    dict(name="Fields north of the lakes", polygon=R(NORTH, 39.9500, WEST, EAST), kind="orchard", periods=JIN),
    dict(name="Fields east of the lakes", polygon=R(39.9500, 39.9310, 116.3905, EAST), kind="orchard", periods=JIN),
    dict(name="Fields east of the palace", polygon=R(39.9278, 39.9192, 116.3935, EAST), kind="orchard", periods=JIN),
    dict(name="Fields toward Zhongdu", polygon=R(39.9150, SOUTH, 116.3880, EAST), kind="orchard", periods=JIN),
    dict(name="Fields by the Gaoliang river", polygon=R(39.9500, 39.9272, WEST, 116.3740), kind="orchard", periods=JIN),
    dict(name="Fields west of the palace", polygon=R(39.9240, SOUTH, WEST, 116.3740), kind="orchard", periods=JIN),
    dict(name="Gardens of the Daning palace", polygon=R(39.9310, 39.9200, 116.3745, 116.3790), kind="park", periods=JIN),
    # Yuan
    dict(name="Yuyuan, the imperial garden", polygon=R(YIN - 0.0004, YP_N + 0.0003, 116.3860, 116.3960), kind="park", periods=YUAN),
    dict(name="Fields in the northern wards", polygon=R(NORTH - 0.0005, 39.9520, YW + 0.0004, 116.3760), kind="orchard", periods=YUAN),
    dict(name="Fields in the north-east wards", polygon=R(NORTH - 0.0005, 39.9490, DS + 0.0004, YE - 0.0004), kind="orchard", periods=YUAN),
    dict(name="Fields outside the west wall", polygon=R(NORTH, SOUTH, WEST, YW - 0.0020), kind="orchard", periods=DADU),
    dict(name="Fields outside the east wall", polygon=R(NORTH, SOUTH, YE + 0.0020, EAST), kind="orchard", periods=DADU),
    # Ming and Qing
    dict(name="Fields north of the walls", polygon=R(NORTH, MN + 0.0020, YW - 0.0020, YE + 0.0020), kind="orchard", periods=MQ),
    dict(name="Western Park (Xiyuan)", polygon=R(39.9318, 39.9100, 116.3792, 116.3860), kind="park", periods=MQ),
]

MARSH = [
    dict(name="Reed beds of the Gaoliang", polygon=R(39.9530, 39.9505, 116.3560, 116.3680), periods=JIN + YUAN),
]

DISTRICTS = [
    dict(id="daning-palace", name="Daning palace", polygon=R(39.9310, 39.9180, 116.3745, 116.3930), periods=JIN,
         description="The Jin emperors' detached palace of 1179 (later called Wanning and Shou'an): halls on the lake shore and on the heaped-up Qionghua island, where Shizong and Zhangzong spent their summers away from Zhongdu."),
    dict(id="dadu", name="Dadu (Khanbaliq)", polygon=R(NORTH, YS, YW, YE), periods=YUAN,
         description="The 'Great Capital', laid out from 1267 on a plan going back to the Rites of Zhou: the palace in front, markets behind, the ancestral temple on the east and the altars of soil and grain on the west. Mongol, Chinese, Central Asian and Tibetan quarters mixed in its fifty wards."),
    dict(id="yuan-imperial-city", name="Huangcheng (the Imperial City)", polygon=R(YIN, YIS, YIW, YIE), periods=YUAN,
         description="The enclosure round the Taiye lake: the Great Within (Danei) on the east bank, the Longfu palace of the crown prince and the Xingsheng palace of the empress dowager on the west, gardens, stables and tents between."),
    dict(id="danei", name="The Great Within (Danei)", polygon=R(YP_N, YP_S, YP_W, YP_E), periods=YUAN,
         description="The palace city, about 740 by 950 m: the Daming Hall for the great audiences at the front, the Yanchun Pavilion behind, corner towers on its walls. Its exact site is debated; it lay roughly where the Forbidden City now stands, a little to the north."),
    dict(id="xiejie-market", name="The Bell and Drum Tower market", polygon=R(39.9440, 39.9365, 116.3800, 116.3960), periods=YUAN,
         description="The commercial heart of Dadu round the harbour: the Xiejie, the rice, silk, fur and pearl markets, the camel and horse markets, wine shops and the theatres of the zaju playwrights."),
    dict(id="zijincheng", name="Zijincheng (the Forbidden City)", polygon=R(FC_N, FC_S, FC_W, FC_E), periods=MQ,
         description="The 'Purple Forbidden City', the emperor's palace from 1420 to 1912: the outer court of the three great halls for state ceremonies and the inner court of the emperor's and empresses' residences behind the Gate of Heavenly Purity."),
    dict(id="ming-imperial-city", name="Huangcheng (the Imperial City)", polygon=R(IN, IS, IW, IE), periods=MQ,
         description="The walled enclosure round the Forbidden City: the Western Park and its three lakes, Jingshan, the Ancestral Temple and the Altar of Soil and Grain, and the storehouses, kitchens and workshops of the twenty-four eunuch directorates."),
    dict(id="inner-city", name="Inner City (Neicheng)", polygon=R(MN, MS, MW, ME), periods=MING,
         description="The walled city of 1368-1420 round the Imperial City, divided into wards (fang) under five city police districts; ministries line the Imperial Way, markets cluster at the Bell and Drum Towers, Xisi and Dongsi."),
    dict(id="banner-city", name="The Tartar City (Inner City)", polygon=R(MN, MS, MW, ME), periods=QING,
         description="From 1648 the Inner City was reserved for the Eight Banners, each with its sector: the two Yellow Banners in the north, the Whites in the east, the Reds in the west and the Blues in the south. Han Chinese merchants and officials lived in the Outer City to the south."),
]

LABELS = [
    dict(text="Zhongdu lies to the south-west", position=(39.8985, 116.3560), size="sm", periods=JIN),
    dict(text="Daning Palace", position=(39.9290, 116.3700), size="md", periods=JIN),
    dict(text="Khanbaliq", position=(39.9560, 116.4000), size="lg", periods=YUAN),
    dict(text="Dadu", position=(39.9535, 116.4000), size="md", periods=YUAN),
    dict(text="Beijing", position=(39.9555, 116.4000), size="lg", periods=MQ),
    dict(text="Taiye lake", position=(39.9180, 116.3790), size="sm", rotation=-80, periods=ALL),
    dict(text="Jishuitan", position=(39.9445, 116.3740), size="md", rotation=-35, periods=JIN + YUAN),
    dict(text="Shichahai", position=(39.9420, 116.3770), size="sm", rotation=-30, periods=MQ),
    dict(text="The Great Within", position=(39.9248, 116.3955), size="sm", periods=YUAN),
    dict(text="Imperial City", position=(39.9310, 116.3770), size="sm", periods=DADU),
    dict(text="Western Park", position=(39.9150, 116.3760), size="sm", rotation=-90, periods=MQ),
    dict(text="Inner City", position=(39.9010, 116.3600), size="md", periods=MQ),
    dict(text="Yuan north wall 2.5 km north", position=(39.9600, 116.3700), size="sm", periods=YUAN),
    dict(text="Outer City and Altar of Heaven to the south", position=(39.8968, 116.4060), size="sm", periods=QING),
]

SOURCES = [
    dict(id="wiki-khanbaliq", title="Khanbaliq", author="Wikipedia", url="https://en.wikipedia.org/wiki/Khanbaliq"),
    dict(id="wiki-zhongdu", title="Zhongdu", author="Wikipedia", url="https://en.wikipedia.org/wiki/Zhongdu"),
    dict(id="wiki-beijing-history", title="History of Beijing", author="Wikipedia", url="https://en.wikipedia.org/wiki/History_of_Beijing"),
    dict(id="wiki-fortifications-beijing", title="Fortifications of Beijing", author="Wikipedia", url="https://en.wikipedia.org/wiki/Fortifications_of_Beijing"),
    dict(id="wiki-imperial-city", title="Imperial City, Beijing", author="Wikipedia", url="https://en.wikipedia.org/wiki/Imperial_City,_Beijing"),
    dict(id="wiki-shichahai", title="Shichahai", author="Wikipedia", url="https://en.wikipedia.org/wiki/Shichahai"),
    dict(id="wiki-hutong", title="Hutong", author="Wikipedia", url="https://en.wikipedia.org/wiki/Hutong"),
    dict(id="wiki-eight-banners", title="Eight Banners", author="Wikipedia", url="https://en.wikipedia.org/wiki/Eight_Banners"),
    dict(id="steinhardt", title="Chinese Imperial City Planning", author="Nancy Shatzman Steinhardt", year=1990),
    dict(id="hou-renzhi", title="Historical Atlas of Beijing (Beijing lishi ditu ji)", author="Hou Renzhi (ed.)", year=1988),
    dict(id="naquin", title="Peking: Temples and City Life, 1400-1900", author="Susan Naquin", year=2000),
]
