# Nara / Heijō-kyō: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
NARA = ["heijo-720", "tempyo-752"]
LATER = ["abandoned-900", "edo-1700"]
ALL = NARA + LATER

# The Heijō grid after the usual reconstruction laid over the modern map (one bō or jō is about 530 m).
# East-west avenues (latitude): Ichijō-kita (the north edge) to Kujō (the south edge)
NORTH, ICHIJO_S, NIJO, SANJO, SHIJO, GOJO = 34.6964, 34.6916, 34.6864, 34.6820, 34.6772, 34.6724
ROKUJO, SHICHIJO, HACHIJO, KUJO = 34.6676, 34.6628, 34.6580, 34.6534
PALACE_S = 34.6869       # the palace's south wall, with the Suzakumon in it
# North-south avenues (longitude)
SUZAKU = 135.7957
W1, W2, W3 = 135.7897, 135.7826, 135.7780           # Nishi-ichibō to Nishi-sanbō (the frame cuts the far west)
E1, E2, E3, E4 = 135.8014, 135.8071, 135.8129, 135.8186   # Higashi-ichibō to Higashi-yonbō (the Kyōgoku)
G5, G6, G7 = 135.8240, 135.8288, 135.8350           # the Gekyō, the outer capital
WEST, SOUTH = 135.7770, 34.6500


def R(n, s, w, e):
    """A rectangle between two latitudes and two longitudes."""
    return [(n, w), (n, e), (s, e), (s, w)]


CITY = dict(
    name="Nara", subtitle="Heijō-kyō, the Capital of the Peaceful Citadel",
    description="Nara from the building of Heijō-kyō in 710 to the temple town of the Edo period: the eastern three-quarters of the Chinese-style grid, the Gekyō annex with Kōfuku-ji and Gangō-ji, and Tōdai-ji and the Kasuga shrine under the Wakakusa and Kasuga hills. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="tempyo-752",
    world=dict(heightScale=1.0, walls=["#E4D6BC", "#D9C9A6", "#CBB894"], roofs=["#6A6866", "#7C6A56"]),
    camera=dict(target=(34.6840, 135.8150), distance=42),
)
FRAME = ((34.7050, WEST), (SOUTH, 135.8580))
PALETTE = dict(parchment="#E8D7B2", ink="#5D4535", water="#668A8B", hill="#74805A", road="#8A6D4E")
COMPASS = (34.7020, 135.8535)
CARTOUCHE = (34.6515, 135.8300)

PERIODS = [
    dict(id="heijo-720", label="Heijō-kyō, the new capital", year=720, startYear=710, endYear=739,
         summary="Empress Genmei moved the court here from Fujiwara-kyō in 710. The grid copies Tang Chang'an: 4.3 by 4.8 km of walled wards, the 74 m Suzaku-ōji, the palace at its head with the First Daigokuden. Yakushi-ji, Daian-ji and Gangō-ji are being moved in from Asuka; the Fujiwara build Kōfuku-ji on the eastern rise.",
         population="perhaps 50,000–100,000 (estimates vary widely)",
         feel="Fresh-sawn cypress and wet plaster, red columns among half-empty wards, oxcarts of roof tiles from the kilns of Nara-yama, and wooden tags clacking in the clerks' hands.",
         style="sinic",
         houses=dict(title="Ward lots of the new capital", text="Ranks were paid in land: a prince or minister held a whole 120 m block (chō) of halls on earth-fast posts round a gravel court; a lower official a half or a quarter. A commoner's lot was a sixteenth or a thirty-second of a chō: a board-roofed hut, a well and a vegetable patch."),
         outskirts=dict(title="Fields inside the grid", text="The southern and western wards fill slowly. Many blocks are still paddy and dry fields worked by the families who live on them, behind brushwood fences.")),
    dict(id="tempyo-752", label="Nara of the Great Buddha", year=752, startYear=740, endYear=784,
         summary="The Tenpyō age of Emperor Shōmu. After epidemic, rebellion and five years of wandering capitals (740–745) the court is back, and the state pours its copper and gold into Tōdai-ji: the 15 m bronze Buddha, the largest wooden hall in the world, twin pagodas near 100 m. The city fills to the Kyōgoku and the Gekyō is crowded with monks and craftsmen.",
         population="perhaps 100,000",
         feel="The ring of hammers at the temple workshops, chanting from a dozen great temples, incense and smoke from the foundry, and imported musk and aloeswood in the markets.",
         style="sinic",
         houses=dict(title="Ward houses of Tenpyō Nara", text="Nobles' compounds take one or more chō behind tiled earth walls; some main halls now have tiled roofs and painted columns, as the court ordered in 724. Officials' and craftsmen's lots are small yards of board-roofed huts, storehouses on stilts and wells lined with timber."),
         outskirts=dict(title="The southern wards", text="South of Rokujō the grid thins into fields, the two markets, potters' and dyers' yards and the farms that pay their rice tax to the capital.")),
    dict(id="abandoned-900", label="Nanto, the southern capital", year=900, startYear=785, endYear=1180,
         summary="The court left for Nagaoka in 784 and Heian-kyō in 794. Within a generation the palace site was paddy; the avenues became field banks. The great temples stayed with their estates, monks and lawsuits, and Nara, 'the southern capital' (Nanto), shrank to a temple town between Kōfuku-ji, Tōdai-ji and the Kasuga shrine.",
         population="a few thousand to perhaps 10,000",
         feel="Frogs in the paddies over the old palace, temple bells across empty wards, deer on the Kasuga meadows, and the chant of monks on the long road to the Fujiwara shrine.",
         style="japanese",
         houses=dict(title="The temple town", text="Houses of temple servants, carpenters and tile-makers in board and plaster cluster at the gates of Kōfuku-ji, Tōdai-ji and Gangō-ji, along the old Sanjō avenue. Each belongs to a temple or shrine and pays dues to it."),
         outskirts=dict(title="Villages in the old grid", text="Farm hamlets with thatched roofs stand among paddies laid out on the old ward lines; the jōri field grid keeps the capital's geometry for a thousand years.")),
    dict(id="edo-1700", label="Edo-period Nara", year=1700, startYear=1567, endYear=1867,
         summary="After the Daibutsuden burned in 1567 the Buddha sat in the open for over a century; the monk Kōkei raised money to recast its head (1692) and rebuild the hall, finished in 1709. Nara is a shogunal town of some 35,000 under a magistrate: pilgrims' inns, sake, Nara-zuke pickles, bleached hemp cloth (Nara-sarashi) and sumi ink.",
         population="about 35,000",
         feel="Deer nosing at pilgrims' rice crackers, the sour steam of breweries, lamp-soot and glue from the ink makers, and the great temple bell of Tōdai-ji at dusk.",
         style="japanese",
         houses=dict(title="Machiya of Naramachi", text="Narrow two-storey town houses of timber and clay, latticed shop fronts, tiled roofs and a long earth-floored passage to a yard, well and storehouse. Many stand on the old precinct of Gangō-ji, whose courts were built over from the 15th century."),
         outskirts=dict(title="Villages of the Yamato plain", text="Villages of thatched farmhouses with walled yards, rice and cotton fields on the old jōri grid, and the hamlets that grow up round Yakushi-ji, Tōshōdai-ji and Saidai-ji.")),
]

# ---------------------------------------------------------------- water and hills
WATER = [
    dict(id="saho", name="Saho-gawa", width=22, blurb="The river of Saho-hime, goddess of spring. It comes down from the Kasuga hills north of Tōdai-ji and crosses the city diagonally to the south-west; the Rajōmon's foundations were found partly under its later bed.",
         path=[(34.6985, 135.8580), (34.6968, 135.8500), (34.6955, 135.8420), (34.6948, 135.8340), (34.6930, 135.8260), (34.6895, 135.8200), (34.6845, 135.8160), (34.6780, 135.8115), (34.6710, 135.8065), (34.6640, 135.8025), (34.6570, 135.7990), (34.6530, 135.7968), (SOUTH, 135.7940)]),
    dict(id="akishino", name="Akishino-gawa", width=16, blurb="The stream from the Akishino hills, which ran past Saidai-ji and down the west side of the palace through the Ukyō. In the capital years it was probably straightened as a canal serving the West Market.",
         path=[(34.7050, 135.7862), (34.6990, 135.7868), (34.6930, 135.7870), (34.6860, 135.7878), (34.6780, 135.7880), (34.6700, 135.7880), (34.6620, 135.7880), (34.6560, 135.7890), (SOUTH, 135.7905)]),
    dict(id="sarusawa", name="Sarusawa-ike", width=72, periods=["tempyo-752"] + LATER, blurb="The pond below Kōfuku-ji, dug in 749 for the rite of releasing living creatures (hōjō-e). In legend a court lady drowned herself in it when the emperor's favour waned.",
         path=[(34.6812, 135.8310), (34.6812, 135.8322)]),
]

HILLS = [
    dict(id="wakakusa", name="Wakakusa-yama", center=(34.6890, 135.8520), radius=420, blurb="A grassy hill of three swelling tiers, 342 m high, east of Tōdai-ji. Its grass has been burned off in winter since at least the 18th century; the 'mountain burning' is said to have begun as a way of settling a quarrel over the boundary between Tōdai-ji and Kōfuku-ji."),
    dict(id="kasugayama", name="Kasuga-yama and Mikasa", center=(34.6795, 135.8555), radius=600, blurb="The sacred mountain of the Kasuga shrine, whose god is said to have come down to Mikasa-yama riding a white deer. Hunting and tree-felling on it were banned in 841; its forest has stood ever since."),
    dict(id="narayama", name="Nara-yama", center=(34.7040, 135.8220), radius=450, blurb="The low hills along the capital's north, crossed by the Narazaka road to Yamashiro. Tile kilns for the palace and the temples were dug into their slopes."),
    dict(id="ichiniwa", name="Ichiniwa tumulus", center=(34.6977, 135.7903), radius=80, label=False, blurb="A 5th-century keyhole tomb at the palace's north-west corner, its front half levelled to make room for the palace; the rest is honoured as the tomb of Emperor Heizei."),
    dict(id="uwanabe", name="Uwanabe tumulus", center=(34.7020, 135.8082), radius=130, blurb="One of the great keyhole tombs of the Saki group north of the palace, 255 m long, built in the 5th century and already ancient when the capital was laid out."),
    dict(id="konabe", name="Konabe tumulus", center=(34.7048, 135.8032), radius=105, label=False, blurb="A 204 m keyhole tomb of the Saki group, ringed by its moat."),
]

# ---------------------------------------------------------------- roads
_NARA_ROADS = [
    dict(id="suzaku", name="Suzaku-ōji", path=[(NIJO - 0.0002, SUZAKU), (KUJO + 0.0002, SUZAKU)], width=74, style="major", labelled=True,
         blurb="The central avenue, about 74 m wide and 3.7 km long, from the Suzakumon of the palace to the Rajōmon. Willows lined its ditches, and the earth walls of the wards closed it on both sides: it was a stage for embassies, not a street to live on."),
    dict(id="nijo", name="Nijō-ōji", path=[(NIJO, WEST), (NIJO, G7)], width=37, labelled=True,
         blurb="The cross-avenue along the palace's south wall, running east into the Gekyō toward Tōdai-ji."),
    dict(id="ichijo-s-w", name="Ichijō-minami-ōji", path=[(ICHIJO_S, WEST), (ICHIJO_S, 135.7895)], width=24),
    dict(id="ichijo-s-e", name="Ichijō-minami-ōji", path=[(ICHIJO_S, 135.8042), (ICHIJO_S, G7)], width=24),
    dict(id="ichijo-n-w", name="Ichijō-kita-ōji", path=[(NORTH, WEST), (NORTH, 135.7895)], width=24),
    dict(id="ichijo-n-e", name="Ichijō-kita-ōji", path=[(NORTH, 135.8016), (NORTH, G7)], width=24),
    dict(id="sanjo", name="Sanjō-ōji", path=[(SANJO, WEST), (SANJO, G7)], width=24, labelled=True,
         blurb="The third avenue, which ran east past Kōfuku-ji's south gate toward the Kasuga plain; it survives as Nara's Sanjō-dōri."),
    dict(id="shijo", name="Shijō-ōji", path=[(SHIJO, WEST), (SHIJO, G6)], width=24),
    dict(id="gojo", name="Gojō-ōji", path=[(GOJO, WEST), (GOJO, G7)], width=24, labelled=True),
    dict(id="rokujo", name="Rokujō-ōji", path=[(ROKUJO, WEST), (ROKUJO, E4)], width=24),
    dict(id="shichijo", name="Shichijō-ōji", path=[(SHICHIJO, WEST), (SHICHIJO, E4)], width=24, labelled=True),
    dict(id="hachijo", name="Hachijō-ōji", path=[(HACHIJO, WEST), (HACHIJO, E4)], width=24),
    dict(id="kujo", name="Kujō-ōji", path=[(KUJO, WEST), (KUJO, E4)], width=24, labelled=True),
    dict(id="nishi-ichibo", name="Nishi-ichibō-ōji", path=[(NIJO, W1), (KUJO, W1)], width=24),
    dict(id="nishi-nibo", name="Nishi-nibō-ōji", path=[(NORTH, W2), (KUJO, W2)], width=24),
    dict(id="nishi-sanbo", name="Nishi-sanbō-ōji", path=[(NORTH, W3), (KUJO, W3)], width=20),
    dict(id="higashi-ichibo", name="Higashi-ichibō-ōji", path=[(NIJO, E1), (KUJO, E1)], width=24),
    dict(id="higashi-nibo", name="Higashi-nibō-ōji", path=[(NORTH, E2), (KUJO, E2)], width=24),
    dict(id="higashi-sanbo", name="Higashi-sanbō-ōji", path=[(NORTH, E3), (KUJO, E3)], width=24),
    dict(id="kyogoku", name="Higashi-Kyōgoku-ōji", path=[(NORTH, E4), (KUJO, E4)], width=30, labelled=True,
         blurb="The east edge of the main grid, the fourth avenue east of Suzaku. Beyond it the Gekyō climbed toward the hills."),
    dict(id="gekyo-5", name="Higashi-gobō-ōji", path=[(NORTH, G5), (GOJO, G5)], width=20),
    dict(id="gekyo-6", name="Higashi-rokubō-ōji", path=[(NORTH, G6), (GOJO, G6)], width=20),
    dict(id="gekyo-7", name="Higashi-shichibō-ōji", path=[(NORTH, G7), (GOJO, G7)], width=20, labelled=True,
         blurb="The east edge of the Gekyō, outside the west gates of Tōdai-ji."),
    dict(id="shimotsu-michi", name="Shimotsu-michi", path=[(KUJO - 0.0007, SUZAKU), (SOUTH, SUZAKU)], width=12, style="minor", labelled=True,
         blurb="The Lower Road, one of three straight roads across the Nara basin; the capital's Suzaku-ōji was laid out on its line."),
    dict(id="nakatsu-michi", name="Nakatsu-michi", path=[(KUJO, E4), (SOUTH, E4)], width=12, style="minor",
         blurb="The Middle Road south to Asuka, on the line of the Kyōgoku."),
    dict(id="narazaka", name="Narazaka road", path=[(NORTH, 135.8320), (34.7000, 135.8318), (34.7050, 135.8315)], width=10, style="minor",
         blurb="The road north over the Nara hills to the Kizu river and Yamashiro."),
]
ROADS = [dict(r, periods=NARA) for r in _NARA_ROADS] + [
    # abandoned-900: the grid fades to field banks
    dict(id="sanjo-900", name="Sanjō road", path=[(SANJO, E4), (SANJO, G7), (34.6818, 135.8400), (34.6815, 135.8466)], width=12, labelled=True, periods=LATER,
         blurb="The old Sanjō avenue, the spine of the temple town, running on past Kōfuku-ji to the Kasuga shrine as its approach."),
    dict(id="shichibo-900", name="Higashi-shichibō road", path=[(NORTH, G7), (GOJO, G7)], width=8, style="minor", periods=["abandoned-900"]),
    dict(id="suzaku-900", name="Suzaku track", path=[(NIJO, SUZAKU), (KUJO, SUZAKU), (SOUTH, SUZAKU)], width=8, style="minor", periods=["abandoned-900"],
         blurb="What was left of the great avenue: a cart track between paddies on the line of the old Shimotsu-michi."),
    dict(id="nakatsu-900", name="Nakatsu-michi", path=[(NORTH, E4), (SOUTH, E4)], width=10, periods=["abandoned-900"]),
    dict(id="ichijo-900", name="Ichijō road to Saidai-ji", path=[(ICHIJO_S, G7), (ICHIJO_S, 135.8040), (34.6925, 135.7830)], width=8, style="minor", periods=LATER,
         blurb="The road west from the temple town past Hokke-ji and across the site of the old palace to Saidai-ji."),
    dict(id="nishinokyo-900", name="Road to Yakushi-ji", path=[(34.6925, 135.7880), (34.6820, 135.7890), (34.6700, 135.7890), (34.6640, 135.7895)], width=8, style="minor", periods=["abandoned-900"],
         blurb="A track down the west bank of the Akishino to Tōshōdai-ji and Yakushi-ji in their villages of Nishinokyō, 'the west capital'."),
    dict(id="narazaka-900", name="Narazaka road", path=[(34.6900, 135.8290), (NORTH, 135.8300), (34.7050, 135.8315)], width=8, style="minor", periods=["abandoned-900"]),
    # edo-1700
    dict(id="kyo-kaido", name="Kyō-kaidō", path=[(34.7050, 135.8310), (34.6990, 135.8300), (34.6950, 135.8290), (SANJO, 135.8290)], width=10, labelled=True, periods=["edo-1700"],
         blurb="The Kyoto road, north over Narazaka. Its last stretch through Kitamachi was lined with inns and the shops that sold Nara fans and ink to travellers."),
    dict(id="kami-kaido", name="Kami-kaidō", path=[(SANJO, 135.8290), (34.6760, 135.8292), (34.6700, 135.8296), (SOUTH, 135.8300)], width=10, labelled=True, periods=["edo-1700"],
         blurb="The Upper Road south along the hills toward Tenri, Sakurai and the Ise pilgrimage road: the old Kamitsu-michi."),
    dict(id="koriyama-kaido", name="Kōriyama road", path=[(34.6760, 135.8292), (34.6700, 135.8200), (34.6600, 135.8050), (34.6540, 135.7960), (SOUTH, 135.7900)], width=8, periods=["edo-1700"],
         blurb="The road south-west to the castle town of Kōriyama and on to Osaka."),
    dict(id="todaiji-approach", name="Tōdai-ji approach", path=[(SANJO, 135.8398), (34.6843, 135.8398)], width=10, style="minor", periods=["edo-1700"]),
    dict(id="tegai", name="Tegai road", path=[(34.6890, 135.8290), (34.6890, 135.8378)], width=8, style="minor", periods=["edo-1700"],
         blurb="The road to Tōdai-ji's west gate, the Tegaimon, through the gate town of Tegai."),
    dict(id="shimomikado", name="Shimomikado", path=[(34.6800, 135.8200), (34.6800, 135.8290)], width=6, style="minor", periods=["edo-1700"]),
    dict(id="moto-koshi", name="Naramachi lane", path=[(34.6745, 135.8200), (34.6745, 135.8292)], width=6, style="minor", periods=["edo-1700"]),
]

WALLS = [
    dict(id="palace-wall", name="Palace wall (Ōgaki)", closed=True, periods=NARA,
         path=[(NORTH, 135.7900), (NORTH, 135.8011), (34.6940, 135.8011), (34.6940, 135.8038), (PALACE_S, 135.8038), (PALACE_S, 135.7900)],
         blurb="The tiled earth wall, about 5 m high, round the palace: a square of about 1 km with an annex 250 m wide on the east. Probably twelve gates opened in it, three on each side."),
    dict(id="rajo", name="Rajō (south wall)", periods=NARA, path=[(KUJO - 0.0005, 135.7905), (KUJO - 0.0005, 135.8010)],
         blurb="Heijō-kyō had no city wall in the Chinese sense: only a short wall and moat flanked the Rajōmon, for the show of a walled capital."),
]

GATES = [
    dict(id="wakainukaimon", name="Wakainukaimon", position=(PALACE_S, 135.7930), periods=NARA),
    dict(id="mibumon", name="Mibumon", position=(PALACE_S, 135.8000), periods=NARA),
]

BRIDGES = [
    dict(id="saho-bridge", name="Saho-gawa bridge", path=[(34.6945, 135.8290), (34.6928, 135.8290)], build="timber", arches=3, periods=["edo-1700"],
         blurb="The Kyō-kaidō's bridge over the Saho at the north end of Kitamachi."),
    dict(id="sanjo-saho", name="Sanjō bridge over the Saho", path=[(SANJO, 135.8135), (SANJO, 135.8152)], build="timber", arches=3, periods=NARA),
]

# ---------------------------------------------------------------- built-up areas
BLOCKS = [
    # heijo-720
    dict(name="Sakyō, north wards", polygon=R(NORTH, NIJO, 135.8042, E4), density="dense", periods=["heijo-720"]),
    dict(name="Sakyō, Nijō to Gojō", polygon=R(NIJO, GOJO, SUZAKU, E4), density="dense", periods=["heijo-720"]),
    dict(name="Sakyō, south wards", polygon=R(GOJO, KUJO, SUZAKU, E4), density="loose", periods=["heijo-720"]),
    dict(name="Ukyō, Nijō to Shijō", polygon=R(NIJO, SHIJO, W2, SUZAKU), density="dense", periods=["heijo-720"]),
    dict(name="Ukyō, south and west wards", polygon=R(SHIJO, KUJO, WEST, SUZAKU), density="loose", periods=["heijo-720"]),
    dict(name="Ukyō, north wards", polygon=R(NORTH, NIJO, WEST, 135.7895), density="loose", periods=["heijo-720"]),
    dict(name="Gekyō, north", polygon=R(NORTH, SANJO, E4, G7), density="loose", periods=["heijo-720"]),
    dict(name="Gekyō, round Kōfuku-ji", polygon=R(SANJO, GOJO, E4, G7), density="dense", periods=["heijo-720"]),
    # tempyo-752
    dict(name="Sakyō, north wards", polygon=R(NORTH, NIJO, 135.8042, E4), density="dense", periods=["tempyo-752"]),
    dict(name="Sakyō, Nijō to Rokujō", polygon=R(NIJO, ROKUJO, SUZAKU, E4), density="dense", periods=["tempyo-752"]),
    dict(name="Sakyō, south wards", polygon=R(ROKUJO, KUJO, SUZAKU, E4), density="loose", periods=["tempyo-752"]),
    dict(name="Ukyō, Nijō to Shijō", polygon=R(NIJO, SHIJO, WEST, SUZAKU), density="dense", periods=["tempyo-752"]),
    dict(name="Ukyō, south wards", polygon=R(SHIJO, KUJO, WEST, SUZAKU), density="loose", periods=["tempyo-752"]),
    dict(name="Ukyō, north wards", polygon=R(NORTH, NIJO, WEST, 135.7895), density="loose", periods=["tempyo-752"]),
    dict(name="Gekyō", polygon=R(NORTH, GOJO, E4, G7), density="dense", periods=["tempyo-752"]),
    dict(name="Tōdai-ji workshops", polygon=R(34.6910, 34.6870, G7 + 0.0002, 135.8380), density="loose", periods=["tempyo-752"]),
    # abandoned-900
    dict(name="Nara, the temple town", polygon=R(34.6900, 34.6740, G5, G7), density="dense", periods=["abandoned-900"]),
    dict(name="Tegai, at Tōdai-ji's west gate", polygon=R(34.6910, 34.6870, G7 + 0.0002, 135.8380), density="loose", periods=["abandoned-900"]),
    dict(name="Kitamachi", polygon=R(34.6935, 34.6900, G5, G7), density="loose", periods=["abandoned-900"]),
    dict(name="Hokke-ji village", polygon=R(34.6955, 34.6920, 135.8050, 135.8125), density="loose", periods=["abandoned-900"]),
    dict(name="Saidai-ji village", polygon=R(34.6915, 34.6885, 135.7780, 135.7860), density="loose", periods=["abandoned-900"]),
    dict(name="Nishinokyō villages", polygon=R(34.6740, 34.6650, 135.7790, 135.7832), density="loose", periods=["abandoned-900"]),
    dict(name="Daian-ji village", polygon=R(34.6720, 34.6690, 135.8000, 135.8100), density="loose", periods=["abandoned-900"]),
    dict(name="Kujō village", polygon=R(34.6575, 34.6545, 135.7975, 135.8060), density="loose", periods=["abandoned-900"]),
    # edo-1700
    dict(name="Naramachi", polygon=R(34.6815, 34.6725, 135.8200, 135.8345), density="dense", periods=["edo-1700"]),
    dict(name="Kitamachi", polygon=R(34.6950, 34.6825, 135.8240, 135.8345), density="dense", periods=["edo-1700"]),
    dict(name="Sanjō-dōri", polygon=R(34.6838, 34.6805, 135.8130, 135.8240), density="dense", periods=["edo-1700"]),
    dict(name="Tegai and Zōshi", polygon=R(34.6915, 34.6852, 135.8345, 135.8382), density="dense", periods=["edo-1700"]),
    dict(name="Takabatake", polygon=R(34.6800, 34.6750, 135.8345, 135.8440), density="dense", periods=["edo-1700"]),
    dict(name="Hokke-ji village", polygon=R(34.6955, 34.6920, 135.8050, 135.8125), density="loose", periods=["edo-1700"]),
    dict(name="Saidai-ji village", polygon=R(34.6915, 34.6880, 135.7780, 135.7860), density="loose", periods=["edo-1700"]),
    dict(name="Nishinokyō village", polygon=R(34.6740, 34.6650, 135.7790, 135.7832), density="loose", periods=["edo-1700"]),
    dict(name="Daian-ji village", polygon=R(34.6720, 34.6690, 135.8000, 135.8100), density="loose", periods=["edo-1700"]),
    dict(name="Kizuji villages", polygon=R(34.6720, 34.6640, 135.8150, 135.8260), density="loose", periods=["edo-1700"]),
    dict(name="Kujō village", polygon=R(34.6575, 34.6545, 135.7975, 135.8060), density="loose", periods=["edo-1700"]),
]

GARDENS = [
    dict(name="Tōin garden", polygon=R(34.6905, 34.6878, 135.8016, 135.8036), kind="park", periods=["tempyo-752"]),
    dict(name="Paddies on the palace site", polygon=R(34.6958, 34.6874, 135.7905, 135.8034), kind="orchard", periods=LATER),
    dict(name="Fields of the old Sakyō", polygon=R(34.6850, 34.6550, 135.7965, 135.8005), kind="orchard", periods=LATER),
    dict(name="Fields of the old Ukyō", polygon=R(34.6850, 34.6550, 135.7900, 135.7948), kind="orchard", periods=LATER),
    dict(name="Kasuga-no meadows", polygon=R(34.6840, 34.6800, 135.8360, 135.8470), kind="park", periods=LATER),
]

DISTRICTS = [
    dict(id="heijo-kyu", name="Heijō-kyū (the palace)", polygon=[(NORTH, 135.7900), (NORTH, 135.8011), (34.6940, 135.8011), (34.6940, 135.8038), (PALACE_S, 135.8038), (PALACE_S, 135.7900)], periods=NARA,
         description="The walled palace: the Daigokuden and the State Halls in two parallel courts, the emperor's residence (Dairi), the eight ministries and their offices, kitchens, stores and the Tōin garden on the east. Perhaps 10,000 officials, guards and servants worked inside."),
    dict(id="sakyo", name="Sakyō (Left Capital)", polygon=R(NIJO, KUJO, SUZAKU, E4), periods=NARA,
         description="The eastern half, 'left' as the emperor looks south: higher ground, the mansions of princes and Fujiwara ministers, Daian-ji and the East Market."),
    dict(id="ukyo", name="Ukyō (Right Capital)", polygon=R(NIJO, KUJO, WEST, SUZAKU), periods=NARA,
         description="The western half, with Yakushi-ji, later Tōshōdai-ji and Saidai-ji, and the West Market. The frame cuts its westernmost wards."),
    dict(id="gekyo", name="Gekyō (Outer Capital)", polygon=R(NORTH, GOJO, E4, G7), periods=NARA,
         description="The annex of three bō on the east, an irregular extension up the slope toward the hills, with Kōfuku-ji and Gangō-ji. Unlike Chang'an's grid, Heijō's bulged here, probably to take in the Fujiwara temple."),
    dict(id="nanto", name="Nanto (the Southern Capital)", polygon=R(34.6935, 34.6740, G5, 135.8470), periods=["abandoned-900"],
         description="Nara after the court left: the temple town of the Gekyō, ruled in practice by Kōfuku-ji and its warrior monks, and the precincts of Tōdai-ji and the Kasuga shrine."),
    dict(id="naramachi", name="Naramachi", polygon=R(34.6815, 34.6725, 135.8200, 135.8345), periods=["edo-1700"],
         description="The merchant town built over the old courts of Gangō-ji, south of Sarusawa pond: sake brewers, ink makers, bleachers of hemp cloth and the shops of the pilgrim trade."),
]

LABELS = [
    dict(text="Saho-gawa", position=(34.6740, 135.8105), size="md", rotation=-55),
    dict(text="Akishino-gawa", position=(34.6820, 135.7872), size="sm", rotation=-88),
    dict(text="Heijō-kyō", position=(34.6600, 135.7960), size="lg", periods=["heijo-720"]),
    dict(text="Nara", position=(34.6600, 135.7960), size="lg", periods=["tempyo-752"]),
    dict(text="Sakyō", position=(34.6690, 135.8130), size="lg", periods=NARA),
    dict(text="Ukyō", position=(34.6730, 135.7800), size="lg", periods=NARA),
    dict(text="Gekyō", position=(34.6935, 135.8265), size="md", periods=NARA),
    dict(text="Heijō-kyū", position=(34.6955, 135.7925), size="md", periods=NARA),
    dict(text="Nanto", position=(34.6760, 135.8380), size="lg", periods=["abandoned-900"]),
    dict(text="Nara", position=(34.6760, 135.8390), size="lg", periods=["edo-1700"]),
    dict(text="Naramachi", position=(34.6735, 135.8240), size="sm", periods=["edo-1700"]),
    dict(text="Nishinokyō", position=(34.6630, 135.7810), size="sm", periods=LATER),
    dict(text="Kasuga-no", position=(34.6822, 135.8430), size="sm", periods=LATER),
    dict(text="Yamato plain", position=(34.6560, 135.8100), size="md", periods=LATER),
]

SOURCES = [
    dict(id="wiki-heijo-kyo", title="Heijō-kyō", author="Wikipedia", url="https://en.wikipedia.org/wiki/Heij%C5%8D-ky%C5%8D"),
    dict(id="wiki-nara-history", title="History of Nara", author="Wikipedia", url="https://en.wikipedia.org/wiki/Nara,_Nara#History"),
    dict(id="wiki-saho", title="Saho River", author="Wikipedia", url="https://en.wikipedia.org/wiki/Saho_River"),
    dict(id="wiki-wakakusa", title="Mount Wakakusa", author="Wikipedia", url="https://en.wikipedia.org/wiki/Mount_Wakakusa"),
    dict(id="wiki-kasugayama", title="Kasugayama Primeval Forest", author="Wikipedia", url="https://en.wikipedia.org/wiki/Kasugayama_Primeval_Forest"),
    dict(id="wiki-saki-tumuli", title="Saki Tumulus Cluster", author="Wikipedia", url="https://en.wikipedia.org/wiki/Saki_Tumulus_Cluster"),
    dict(id="farris-sacred", title="Sacred Texts and Buried Treasures: Issues in the Historical Archaeology of Ancient Japan", author="William Wayne Farris", year=1998),
    dict(id="tsuboi-tanaka", title="The Historic City of Nara: An Archaeological Approach", author="Tsuboi Kiyotari and Tanaka Migaku", year=1991),
    dict(id="nabunken", title="Excavation reports of the Heijō Palace site", author="Nara National Research Institute for Cultural Properties (Nabunken)", url="https://www.nabunken.go.jp/"),
    dict(id="cambridge-1", title="The Cambridge History of Japan, vol. 1: Ancient Japan", author="Delmer M. Brown (ed.)", year=1993),
]
