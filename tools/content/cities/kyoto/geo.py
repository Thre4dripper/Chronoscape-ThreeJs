# Kyoto / Heian-kyō: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
HEIAN = ["heian-800", "fujiwara-1000"]
LATER = ["ashikaga-1400", "edo-1750"]
ALL = HEIAN + LATER

# The Heian grid (ōji = avenues), after the usual reconstruction laid over the modern streets.
# East-west avenues (latitude)
ICHIJO, TSUCHIMIKADO, KONOE, NAKAMIKADO, OIMIKADO, NIJO = 35.0262, 35.0238, 35.0214, 35.0190, 35.0165, 35.0133
SANJO, SHIJO, GOJO, ROKUJO, SHICHIJO, HACHIJO, KUJO = 35.0085, 35.0035, 34.9985, 34.9935, 34.9885, 34.9835, 34.9785
# North-south avenues (longitude)
SUZAKU, MIBU, OMIYA, HORIKAWA, NISHINOTOIN, MUROMACHI, KARASUMA, HIGASHINOTOIN, KYOGOKU = 135.7425, 135.7458, 135.7490, 135.7522, 135.7556, 135.7572, 135.7592, 135.7618, 135.7672
NISHI_OMIYA, NISHI_HORIKAWA, DOSO = 135.7360, 135.7328, 135.7294
WEST = 135.7200          # the frame cuts the far west of the old grid (Nishi-Kyōgoku was at 135.718)
IMADEGAWA = 35.0295


def R(n, s, w, e):
    """A rectangle between two latitudes and two longitudes."""
    return [(n, w), (n, e), (s, e), (s, w)]


CITY = dict(
    name="Kyoto", subtitle="Heian-kyō, the Capital of Peace and Tranquillity",
    description="Kyoto from its founding as Heian-kyō in 794 to the Edo period: the eastern two-thirds of the old Chinese-style grid between the Kamo and the Katsura plain, and the temple slopes of Higashiyama across the Kamo. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="fujiwara-1000",
    world=dict(heightScale=1.0, walls=["#E4D6BC", "#D8C8A8", "#CDBB98"], roofs=["#6C6A68", "#7A6A58"]),
    camera=dict(target=(35.0060, 135.7560), distance=40),
)
FRAME = ((35.0400, 135.7200), (34.9750, 135.7970))
PALETTE = dict(parchment="#E8D8B4", ink="#5E4636", water="#6A8C8E", hill="#76805C", road="#8A6E50")
COMPASS = (35.0370, 135.7930)
CARTOUCHE = (34.9765, 135.7765)

PERIODS = [
    dict(id="heian-800", label="Heian-kyō founded", year=800, startYear=794, endYear=900,
         summary="Emperor Kanmu's new capital, laid out from 794 on the model of Tang Chang'an: a walled-ward grid 4.5 by 5.2 km, the 84 m Suzaku-ōji running from the Rashōmon to the Greater Palace. State halls are red-pillared, white-walled and tiled; houses are timber with bark or board roofs. Two official temples, Tō-ji and Sai-ji, guard the south gate.",
         population="perhaps 100,000 (estimates vary widely)",
         feel="Raw earth walls along half-empty avenues, oxcarts creaking on gravel, new-cut cypress, and frogs in the paddies inside the wards.",
         style="sinic",
         houses=dict(title="Walled wards of the new capital", text="Each ward (bō) of sixteen 120 m blocks (chō) is ringed by earth walls. A high noble holds a whole chō: halls on posts joined by roofed corridors round a pond. A commoner's lot is a thirty-second of a chō: a plank house with a board roof on the street."),
         outskirts=dict(title="Fields inside the grid", text="Much of the grid is still paddy and vegetable plot. The west half, low and wet, fills slowly; its wards are farmland with a few houses behind brushwood fences.")),
    dict(id="fujiwara-1000", label="Heian-kyō of the Fujiwara", year=1000, startYear=901, endYear=1185,
         summary="The age of Michinaga, Murasaki Shikibu and Sei Shōnagon. Power lies in the regents' mansions, not the palace, which burns again and again while emperors live in town houses. The west half (Ukyō) is emptying; the east (Sakyō) crowds and spills past Kyōgoku toward the Kamo. Halls of unpainted cypress with bark roofs; temples red-pillared and tiled.",
         population="perhaps 100,000–150,000",
         feel="Incense and plum blossom behind tall earth walls; outside, ox dung, beggars at temple gates, and at night the twang of the guards' bowstrings warding off spirits.",
         style="sinic",
         houses=dict(title="Shinden mansions and street houses", text="In the east wards a great noble's mansion fills a block: a south-facing main hall (shinden) joined by roofed corridors to side halls, a pond with an island, a fishing pavilion. Between them commoners' row houses of planks, their board roofs weighted with stones, line the streets."),
         outskirts=dict(title="The deserted west", text="West of Suzaku, Yasutane wrote in 982, houses fall down and people leave but no one comes. Abandoned wards turn into paddy and reed marsh; a few great houses survive among them.")),
    dict(id="ashikaga-1400", label="Muromachi Kyoto", year=1400, startYear=1336, endYear=1573,
         summary="The Ashikaga shoguns rule from Kyoto. Yoshimitsu's Flower Palace and his monastery Shōkoku-ji, with a seven-storey pagoda finished in 1399, rise in the north. The old grid has shrunk to two towns, Kamigyō of courtiers and warriors and Shimogyō of merchants, joined by Muromachi-dōri. Sake brewers who lend money are the richest men in town.",
         population="perhaps 100,000–200,000",
         feel="Looms clacking, the sour steam of sake breweries, bells from the Zen monasteries, and in summer the gongs and flutes of the Gion floats.",
         style="japanese",
         houses=dict(title="Machiya of Kamigyō and Shimogyō", text="Narrow houses of timber and clay, shingle roofs held down by stones, a shop in front and an earth-floored passage to a yard and storehouse. The houses on both sides of a street form a chō, which keeps its own gates and, in Shimogyō, its own Gion float."),
         outskirts=dict(title="Fields of the old capital", text="Most of the west of the Heian grid is paddy and villages; the old avenues survive as cart tracks and field banks. Temples and their gate towns stand on their own across the Kamo.")),
    dict(id="edo-1750", label="Edo-period Kyoto", year=1750, startYear=1583, endYear=1867,
         summary="Rebuilt by Hideyoshi in the 1590s with new long blocks, an earth rampart (Odoi) and the temples moved to Teramachi, Kyoto is the city of the emperor, the head temples and the crafts: Nishijin silk, fans, lacquer, dolls and books. The shogun keeps Nijō Castle; Gion's teahouses and the Shijō theatres fill the east bank. Tile roofs spread after each great fire.",
         population="about 350,000",
         feel="The clack of Nishijin looms, shamisen from Gion's upper rooms, the cool of the Kamo riverbed on summer evenings, and the smells of pickles, incense and lamp oil.",
         style="japanese",
         houses=dict(title="Kyō-machiya, the eel's beds", text="Latticed shop fronts five or six metres wide, a low upper storey with clay-barred windows, and an earth passage (tōriniwa) running thirty metres back past the kitchen to a small garden and a white storehouse. Dues were assessed on frontage, the usual explanation for the shape."),
         outskirts=dict(title="Kyoto's vegetable fields", text="Outside the rampart and across the old west, villages grow vegetables for the city: Kujō leeks, Mibu greens, Shōgoin radishes. Carters' and farmers' hamlets line the roads to Fushimi and Tanba.")),
]

# ---------------------------------------------------------------- water and hills
WATER = [
    dict(id="kamo", name="Kamo-gawa", width=80, blurb="The Duck River, the capital's eastern edge. Its wide gravel bed flooded so often that a court office existed only to manage its banks; the cloistered emperor Shirakawa named its waters, the dice and the warrior monks as the three things he could not control.",
         path=[(35.0400, 135.7652), (35.0360, 135.7672), (35.0322, 135.7698), (35.0300, 135.7714), (35.0250, 135.7713), (35.0200, 135.7711), (35.0150, 135.7713), (35.0100, 135.7718), (35.0050, 135.7719), (35.0000, 135.7712), (34.9963, 135.7702), (34.9930, 135.7697), (34.9890, 135.7695), (34.9840, 135.7690), (34.9800, 135.7682), (34.9750, 135.7674)]),
    dict(id="takano", name="Takano-gawa", width=40, blurb="The eastern branch, joining the Kamo at Tadasu-no-mori below the Shimogamo shrine.",
         path=[(35.0400, 135.7790), (35.0365, 135.7765), (35.0330, 135.7738), (35.0302, 135.7716)]),
    dict(id="horikawa", name="Horikawa", width=12, blurb="A canal dug down the middle of an avenue to carry timber and drain the east wards. In the Edo period lumber yards and dyers lined it; Nijō Castle's east wall stood just across the road.",
         path=[(35.0400, 135.7518), (35.0300, 135.7521), (35.0200, 135.7522), (35.0100, 135.7522), (34.9900, 135.7522), (34.9750, 135.7524)]),
    dict(id="kamiya", name="Kamiya-gawa (Nishi-Horikawa)", width=10, blurb="The western canal, flowing down past Kitano. Paper-makers re-pulped old documents in its water, hence the name 'paper-house river'.",
         path=[(35.0400, 135.7335), (35.0300, 135.7328), (35.0150, 135.7328), (35.0000, 135.7330), (34.9750, 135.7334)]),
    dict(id="takase", name="Takase-gawa", width=8, periods=["edo-1750"], blurb="A shallow canal dug in 1611–14 by the merchant Suminokura Ryōi to bring rice, sake and timber up from Fushimi in flat-bottomed boats hauled by men walking the bank.",
         path=[(35.0127, 135.7703), (35.0090, 135.7704), (35.0037, 135.7704), (34.9985, 135.7690), (34.9963, 135.7682), (34.9890, 135.7668), (34.9840, 135.7660), (34.9750, 135.7645)]),
]

HILLS = [
    dict(id="funaoka", name="Funaoka-yama", center=(35.0378, 135.7428), radius=170, blurb="A low hill due north of the palace on the axis of Suzaku-ōji, said to have been the surveyors' mark for the city."),
    dict(id="yoshida", name="Yoshida-yama", center=(35.0268, 135.7865), radius=330, blurb="A wooded hill east of the Kamo, home of the Yoshida shrine (founded 859)."),
    dict(id="awata", name="Awata-yama", center=(35.0160, 135.7950), radius=380, label=False, blurb="The northern Higashiyama, above the Awataguchi road east to Ōtsu and the Tōkaidō."),
    dict(id="kacho", name="Kachō-zan", center=(35.0060, 135.7915), radius=430, blurb="The hill behind Yasaka, Chion-in and Maruyama, part of the Higashiyama, the Eastern Hills."),
    dict(id="otowa", name="Otowa-yama", center=(34.9960, 135.7935), radius=540, blurb="The hill of the Otowa falls, whose spring gave Kiyomizu-dera, 'pure water temple', its name."),
    dict(id="toribe", name="Toribe-yama", center=(34.9880, 135.7895), radius=460, blurb="Toribeno, the slope where the capital cremated and abandoned its dead; for Heian poets the smoke over Toribeno was the image of impermanence."),
]

MARSH = [
    dict(name="Ukyō marsh", polygon=[(34.9960, WEST), (34.9960, 135.7290), (34.9880, 135.7310), (34.9830, 135.7290), (34.9830, WEST)], periods=["heian-800", "fujiwara-1000", "ashikaga-1400"]),
    dict(name="Wet fields by the Kamiya", polygon=[(35.0080, 135.7240), (35.0070, 135.7310), (35.0010, 135.7315), (35.0000, 135.7250)], periods=["fujiwara-1000", "ashikaga-1400"]),
]

# ---------------------------------------------------------------- roads
_HEIAN_ROADS = [
    dict(id="suzaku", name="Suzaku-ōji", path=[(NIJO + 0.0001, SUZAKU), (KUJO + 0.0003, SUZAKU)], width=84, style="major", labelled=True,
         blurb="The 84 m central avenue from the Suzakumon to the Rashōmon, lined with willows and the earth walls of the wards. Nobody lived on it; by 1000 it was grazed by oxen and horses."),
    dict(id="ichijo", name="Ichijō-ōji", path=[(ICHIJO, 135.7300), (ICHIJO, KYOGOKU)], width=30, labelled=True),
    dict(id="tsuchimikado", name="Tsuchimikado-ōji", path=[(TSUCHIMIKADO, OMIYA), (TSUCHIMIKADO, KYOGOKU)], width=30),
    dict(id="konoe", name="Konoe-ōji", path=[(KONOE, OMIYA), (KONOE, KYOGOKU)], width=30),
    dict(id="nakamikado", name="Nakamikado-ōji", path=[(NAKAMIKADO, OMIYA), (NAKAMIKADO, KYOGOKU)], width=30),
    dict(id="oimikado", name="Ōimikado-ōji", path=[(OIMIKADO, OMIYA), (OIMIKADO, KYOGOKU)], width=30),
    dict(id="oimikado-w", name="Ōimikado-ōji (west)", path=[(OIMIKADO, WEST), (OIMIKADO, NISHI_OMIYA)], width=30),
    dict(id="nijo", name="Nijō-ōji", path=[(NIJO, WEST), (NIJO, KYOGOKU)], width=51, labelled=True,
         blurb="At 51 m the widest cross-avenue, running along the palace's south wall in front of the Suzakumon."),
    dict(id="sanjo", name="Sanjō-ōji", path=[(SANJO, WEST), (SANJO, KYOGOKU)], width=24, labelled=True),
    dict(id="shijo", name="Shijō-ōji", path=[(SHIJO, WEST), (SHIJO, KYOGOKU)], width=24, labelled=True),
    dict(id="gojo", name="Gojō-ōji", path=[(GOJO, WEST), (GOJO, KYOGOKU)], width=24, labelled=True),
    dict(id="rokujo", name="Rokujō-ōji", path=[(ROKUJO, WEST), (ROKUJO, KYOGOKU)], width=24),
    dict(id="shichijo", name="Shichijō-ōji", path=[(SHICHIJO, WEST), (SHICHIJO, KYOGOKU)], width=24, labelled=True),
    dict(id="hachijo", name="Hachijō-ōji", path=[(HACHIJO, WEST), (HACHIJO, KYOGOKU)], width=24),
    dict(id="kujo", name="Kujō-ōji", path=[(KUJO, WEST), (KUJO, KYOGOKU)], width=29, labelled=True),
    dict(id="omiya", name="Ōmiya-ōji", path=[(ICHIJO, OMIYA), (KUJO, OMIYA)], width=36, labelled=True),
    dict(id="nishi-omiya", name="Nishi-Ōmiya-ōji", path=[(ICHIJO, NISHI_OMIYA), (KUJO, NISHI_OMIYA)], width=36),
    dict(id="mibu", name="Mibu-ōji", path=[(NIJO, MIBU), (KUJO, MIBU)], width=30, style="minor"),
    dict(id="nishinotoin", name="Nishi-no-tōin-ōji", path=[(ICHIJO, NISHINOTOIN), (KUJO, NISHINOTOIN)], width=24),
    dict(id="higashinotoin", name="Higashi-no-tōin-ōji", path=[(ICHIJO, HIGASHINOTOIN), (KUJO, HIGASHINOTOIN)], width=24),
    dict(id="kyogoku", name="Higashi-Kyōgoku-ōji", path=[(ICHIJO, KYOGOKU), (KUJO, KYOGOKU)], width=30, labelled=True,
         blurb="The city's eastern edge avenue. Beyond it lay the Kamo flood plain, where Michinaga built Hōjō-ji in the 1020s."),
    dict(id="toba", name="Toba no tsukurimichi", path=[(KUJO, SUZAKU), (34.9750, 135.7432)], width=20, style="minor",
         blurb="The 'built road' south from the Rashōmon to the river port of Toba, where goods from the provinces landed."),
]
ROADS = [dict(r, periods=HEIAN) for r in _HEIAN_ROADS] + [
    dict(id="awata-road", name="Awataguchi road", path=[(SANJO, KYOGOKU), (35.0090, 135.7760), (35.0098, 135.7830), (35.0105, 135.7900), (35.0110, 135.7970)], width=10, style="minor", periods=["fujiwara-1000", "ashikaga-1400"],
         blurb="The road east over the hills to Ōtsu and the provinces of the east."),
    dict(id="kiyomizu-michi", name="Kiyomizu road", path=[(GOJO, KYOGOKU), (34.9985, 135.7760), (34.9975, 135.7800), (34.9958, 135.7830)], width=8, style="minor", periods=["fujiwara-1000", "ashikaga-1400"],
         blurb="The pilgrims' road from Gojō over the Kamo to Kiyomizu-dera."),
    # Muromachi
    dict(id="imadegawa-1400", name="Imadegawa", path=[(IMADEGAWA, 135.7400), (IMADEGAWA, 135.7700)], width=12, labelled=True, periods=["ashikaga-1400"]),
    dict(id="ichijo-1400", name="Ichijō", path=[(ICHIJO, 135.7350), (ICHIJO, KYOGOKU)], width=10, periods=["ashikaga-1400"]),
    dict(id="nijo-1400", name="Nijō", path=[(NIJO, OMIYA), (NIJO, KYOGOKU)], width=12, labelled=True, periods=["ashikaga-1400"]),
    dict(id="sanjo-1400", name="Sanjō", path=[(SANJO, 135.7380), (SANJO, KYOGOKU), (SANJO, 135.7705)], width=12, labelled=True, periods=["ashikaga-1400"]),
    dict(id="shijo-1400", name="Shijō", path=[(SHIJO, OMIYA), (SHIJO, 135.7708)], width=12, labelled=True, periods=["ashikaga-1400"]),
    dict(id="gojo-1400", name="Gojō", path=[(GOJO, OMIYA), (GOJO, 135.7695)], width=12, labelled=True, periods=["ashikaga-1400"]),
    dict(id="shichijo-1400", name="Shichijō", path=[(SHICHIJO, 135.7380), (SHICHIJO, KYOGOKU)], width=10, periods=["ashikaga-1400"]),
    dict(id="kujo-1400", name="Kujō", path=[(KUJO, 135.7380), (KUJO, 135.7600)], width=8, style="minor", periods=["ashikaga-1400"]),
    dict(id="muromachi-1400", name="Muromachi-kōji", path=[(35.0330, MUROMACHI), (GOJO, MUROMACHI)], width=10, labelled=True, periods=["ashikaga-1400"],
         blurb="The spine joining Kamigyō and Shimogyō, with the shogun's Flower Palace at its north end; it gave the shogunate and the age their name."),
    dict(id="karasuma-1400", name="Karasuma-kōji", path=[(IMADEGAWA, KARASUMA), (SHICHIJO, KARASUMA)], width=10, periods=["ashikaga-1400"]),
    dict(id="omiya-1400", name="Ōmiya", path=[(35.0330, OMIYA), (KUJO, OMIYA)], width=10, periods=["ashikaga-1400"]),
    dict(id="horikawa-1400", name="Horikawa", path=[(35.0330, 135.7530), (KUJO, 135.7530)], width=8, style="minor", periods=["ashikaga-1400"]),
    dict(id="kyogoku-1400", name="Kyōgoku", path=[(35.0300, KYOGOKU), (SHICHIJO, KYOGOKU)], width=10, periods=["ashikaga-1400"]),
    dict(id="suzaku-1400", name="Suzaku track", path=[(NIJO, SUZAKU), (KUJO, SUZAKU)], width=8, style="minor", periods=["ashikaga-1400"],
         blurb="What was left of the great Suzaku-ōji: a cart track between fields called Suzaku-no, 'Suzaku moor'."),
    dict(id="gion-1400", name="Gion road", path=[(SHIJO, 135.7726), (35.0036, 135.7775)], width=8, style="minor", periods=["ashikaga-1400"]),
    dict(id="fushimi-1400", name="Fushimi road", path=[(GOJO, 135.7712), (34.9900, 135.7708), (34.9800, 135.7715), (34.9750, 135.7720)], width=8, style="minor", periods=["ashikaga-1400"]),
    # Edo
    dict(id="imadegawa", name="Imadegawa-dōri", path=[(IMADEGAWA, 135.7360), (IMADEGAWA, 135.7700)], width=12, labelled=True, periods=["edo-1750"]),
    dict(id="marutamachi", name="Marutamachi-dōri", path=[(OIMIKADO, 135.7400), (OIMIKADO, 135.7700)], width=10, periods=["edo-1750"]),
    dict(id="nijo-1750", name="Nijō-dōri", path=[(NIJO, 135.7530), (NIJO, 135.7700)], width=10, periods=["edo-1750"]),
    dict(id="sanjo-1750", name="Sanjō-dōri", path=[(SANJO, 135.7380), (35.0088, 135.7650), (35.0091, 135.7700), (35.0092, 135.7740), (35.0098, 135.7830), (35.0105, 135.7900), (35.0110, 135.7970)], width=12, labelled=True, periods=["edo-1750"],
         blurb="The last stretch of the Tōkaidō from Edo: travellers came down from Keage and over the Sanjō bridge into the city, where the inns clustered."),
    dict(id="shijo-1750", name="Shijō-dōri", path=[(SHIJO, 135.7380), (SHIJO, 135.7702), (SHIJO, 135.7740), (35.0036, 135.7775)], width=12, labelled=True, periods=["edo-1750"]),
    dict(id="gojo-1750", name="Gojō-dōri", path=[(34.9963, 135.7400), (34.9963, 135.7690), (34.9963, 135.7740), (34.9958, 135.7830)], width=12, labelled=True, periods=["edo-1750"],
         blurb="Hideyoshi's Gojō: the old Rokujō-bōmon street, made the Gojō road when he moved the bridge here in 1589 to serve his Great Buddha."),
    dict(id="matsubara-1750", name="Matsubara-dōri", path=[(GOJO, 135.7480), (GOJO, 135.7690), (34.9985, 135.7745), (34.9980, 135.7790)], width=8, style="minor", periods=["edo-1750"]),
    dict(id="shichijo-1750", name="Shichijō-dōri", path=[(SHICHIJO, 135.7400), (SHICHIJO, 135.7700), (34.9893, 135.7740)], width=10, labelled=True, periods=["edo-1750"]),
    dict(id="senbon-1750", name="Senbon-dōri", path=[(35.0360, SUZAKU), (KUJO, SUZAKU)], width=8, style="minor", periods=["edo-1750"],
         blurb="A lane on the line of the old Suzaku-ōji, named for the thousand stupas (senbon) set up at the cremation ground of Rendaino to the north."),
    dict(id="horikawa-1750", name="Horikawa-dōri", path=[(35.0360, 135.7530), (KUJO, 135.7530)], width=10, periods=["edo-1750"]),
    dict(id="karasuma-1750", name="Karasuma-dōri", path=[(35.0330, KARASUMA), (KUJO, KARASUMA)], width=10, labelled=True, periods=["edo-1750"]),
    dict(id="muromachi-1750", name="Muromachi-dōri", path=[(35.0330, MUROMACHI), (34.9963, MUROMACHI)], width=8, periods=["edo-1750"]),
    dict(id="teramachi", name="Teramachi-dōri", path=[(35.0310, KYOGOKU), (34.9963, KYOGOKU)], width=8, labelled=True, periods=["edo-1750"],
         blurb="Hideyoshi gathered some eighty temples along the old Kyōgoku line in 1590, a 'temple town' on the city's east side."),
    dict(id="omiya-1750", name="Ōmiya-dōri", path=[(SANJO, OMIYA), (KUJO, OMIYA)], width=8, style="minor", periods=["edo-1750"]),
    dict(id="yamato-oji", name="Yamato-ōji", path=[(35.0092, 135.7740), (SHIJO, 135.7742), (34.9963, 135.7735), (34.9930, 135.7710), (34.9850, 135.7708), (34.9750, 135.7712)], width=10, periods=["edo-1750"],
         blurb="The road south along the east bank to Fushimi and Nara."),
    dict(id="kiyomizu-zaka", name="Gojō-zaka and Kiyomizu-zaka", path=[(34.9963, 135.7740), (34.9960, 135.7790), (34.9955, 135.7828)], width=6, style="minor", periods=["edo-1750"]),
    dict(id="sannei-zaka", name="Sannen-zaka", path=[(35.0010, 135.7805), (34.9985, 135.7802), (34.9962, 135.7826)], width=5, style="minor", periods=["edo-1750"]),
]

WALLS = [
    dict(id="daidairi-wall", name="Wall of the Daidairi", closed=True, periods=HEIAN,
         path=[(ICHIJO - 0.0003, NISHI_OMIYA + 0.0003), (ICHIJO - 0.0003, OMIYA - 0.0003), (NIJO + 0.0003, OMIYA - 0.0003), (NIJO + 0.0003, NISHI_OMIYA + 0.0003)],
         blurb="The tiled earth wall of the Greater Palace, about 1.2 by 1.4 km, pierced by fourteen gates. Inside: the State Halls, the emperor's residence, and the offices of the eight ministries."),
    dict(id="rajo", name="Rajō (south wall)", periods=["heian-800"], path=[(KUJO - 0.0003, 135.7380), (KUJO - 0.0003, 135.7470)],
         blurb="Heian-kyō had no real city wall: only a short earth wall and ditch flanked the Rashōmon, for show."),
    dict(id="odoi", name="Odoi rampart", periods=["edo-1750"],
         path=[(35.0400, 135.7368), (35.0300, 135.7362), (35.0200, 135.7348), (35.0100, 135.7352), (35.0000, 135.7375), (34.9900, 135.7390), (34.9800, 135.7425), (34.9785, 135.7520), (34.9790, 135.7600), (34.9805, 135.7660), (34.9880, 135.7680), (34.9960, 135.7690), (35.0080, 135.7700), (35.0200, 135.7698), (35.0300, 135.7700), (35.0400, 135.7640)],
         blurb="Hideyoshi's earth rampart and moat of 1591, 22.5 km round, enclosing the city as 'Rakuchū'. By 1750 long stretches had been levelled or planted with bamboo; the seven entrances (nanakuchi) kept their names."),
]

GATES = [
    dict(id="suzakumon-g", name="Suzakumon", position=(NIJO + 0.0004, SUZAKU), periods=HEIAN),
    dict(id="yomeimon", name="Yōmeimon", position=(KONOE, OMIYA - 0.0003), periods=HEIAN),
    dict(id="taikenmon", name="Taikenmon", position=(OIMIKADO, OMIYA - 0.0003), periods=HEIAN),
    dict(id="ikanmon", name="Ikanmon", position=(OIMIKADO + 0.0012, OMIYA - 0.0003), periods=HEIAN),
    dict(id="awataguchi", name="Awataguchi", position=(35.0092, 135.7745), periods=["edo-1750"]),
    dict(id="oharaguchi", name="Ōharaguchi", position=(35.0300, 135.7700), periods=["edo-1750"]),
    dict(id="tanbaguchi", name="Tanbaguchi", position=(34.9890, 135.7390), periods=["edo-1750"]),
    dict(id="tojiguchi", name="Tōjiguchi", position=(34.9786, 135.7520), periods=["edo-1750"]),
]

BRIDGES = [
    dict(id="gojo-1400-bridge", name="Gojō bridge", path=[(GOJO, 135.7700), (GOJO, 135.7722)], build="timber", arches=6, periods=["ashikaga-1400"],
         blurb="The Kiyomizu pilgrims' bridge at the old Gojō, rebuilt by subscription (kanjin) monks; in legend Benkei met the boy Yoshitsune here."),
    dict(id="shijo-1400-bridge", name="Shijō bridge (Gion bridge)", path=[(SHIJO, 135.7708), (SHIJO, 135.7730)], build="timber", arches=6, periods=["ashikaga-1400"],
         blurb="A timber bridge kept up by the Gion shrine's subscriptions, carrying the festival across the Kamo."),
    dict(id="sanjo-ohashi", name="Sanjō Ōhashi", path=[(35.0091, 135.7707), (35.0092, 135.7730)], build="timber", arches=8, landmarkId="sanjo-bridge", periods=["edo-1750"],
         blurb="The bridge at the end of the Tōkaidō, on stone piers since 1590."),
    dict(id="gojo-ohashi", name="Gojō Ōhashi", path=[(34.9963, 135.7690), (34.9963, 135.7714)], build="timber", arches=8, landmarkId="gojo-bridge", periods=["edo-1750"],
         blurb="Hideyoshi's Gojō bridge of 1589, leading to the Great Buddha of Hōkō-ji."),
    dict(id="shijo-1750-bridge", name="Shijō bridge", path=[(SHIJO, 135.7707), (SHIJO, 135.7731)], build="timber", arches=6, periods=["edo-1750"]),
]

# ---------------------------------------------------------------- built-up areas
BLOCKS = [
    # heian-800: the new grid, filling from the north-east
    dict(name="Sakyō, north wards", polygon=R(ICHIJO, NIJO, OMIYA, KYOGOKU), density="dense", periods=["heian-800"]),
    dict(name="Sakyō, Nijō to Shijō", polygon=R(NIJO, SHIJO, SUZAKU, KYOGOKU), density="dense", periods=["heian-800"]),
    dict(name="Sakyō, Shijō to Shichijō", polygon=R(SHIJO, SHICHIJO, SUZAKU, KYOGOKU), density="loose", periods=["heian-800"]),
    dict(name="Sakyō, south wards", polygon=R(SHICHIJO, KUJO, SUZAKU, KYOGOKU), density="loose", periods=["heian-800"]),
    dict(name="Ukyō, Nijō to Shijō", polygon=R(NIJO, SHIJO, WEST, SUZAKU), density="loose", periods=["heian-800"]),
    dict(name="Ukyō, south wards", polygon=R(SHIJO, KUJO, WEST, SUZAKU), density="loose", periods=["heian-800"]),
    dict(name="Ukyō, north wards", polygon=R(ICHIJO, NIJO, WEST, NISHI_OMIYA), density="loose", periods=["heian-800"]),
    dict(name="Offices of the eight ministries", polygon=R(ICHIJO - 0.0005, NIJO + 0.0005, NISHI_OMIYA + 0.0005, OMIYA - 0.0005), density="loose", periods=HEIAN),
    dict(name="Yasaka village", polygon=R(35.0015, 34.9965, 135.7745, 135.7815), density="loose", periods=["heian-800"]),
    # fujiwara-1000: the east crowds, the west empties
    dict(name="Sakyō, Ichijō to Nijō", polygon=R(ICHIJO, NIJO, OMIYA, KYOGOKU), density="dense", periods=["fujiwara-1000"]),
    dict(name="Sakyō, Nijō to Gojō", polygon=R(NIJO, GOJO, SUZAKU, KYOGOKU), density="dense", periods=["fujiwara-1000"]),
    dict(name="Sakyō, Gojō to Shichijō", polygon=R(GOJO, SHICHIJO, SUZAKU, KYOGOKU), density="dense", periods=["fujiwara-1000"]),
    dict(name="Sakyō, south wards", polygon=R(SHICHIJO, KUJO, SUZAKU, KYOGOKU), density="loose", periods=["fujiwara-1000"]),
    dict(name="Beyond Kyōgoku", polygon=R(ICHIJO, GOJO, KYOGOKU + 0.0004, 135.7695), density="loose", periods=["fujiwara-1000"]),
    dict(name="Ukyō, north", polygon=R(ICHIJO, NIJO, WEST, NISHI_OMIYA), density="loose", periods=["fujiwara-1000"]),
    dict(name="Ukyō, Nijō to Gojō", polygon=R(NIJO, GOJO, DOSO, SUZAKU), density="loose", periods=["fujiwara-1000"]),
    dict(name="Ukyō, Shichijō and the market", polygon=R(ROKUJO, KUJO, DOSO, SUZAKU), density="loose", periods=["fujiwara-1000"]),
    dict(name="Gion and Yasaka", polygon=R(35.0060, 34.9975, 135.7735, 135.7800), density="loose", periods=["fujiwara-1000"]),
    dict(name="Rokuhara", polygon=R(34.9975, 34.9915, 135.7715, 135.7775), density="loose", periods=["fujiwara-1000"]),
    dict(name="Kiyomizu-zaka", polygon=R(34.9985, 34.9962, 135.7800, 135.7832), density="loose", periods=["fujiwara-1000"]),
    # ashikaga-1400: two towns, Kamigyō and Shimogyō
    dict(name="Kamigyō, north of Imadegawa", polygon=R(35.0345, IMADEGAWA, 135.7420, 135.7575), density="dense", periods=["ashikaga-1400"]),
    dict(name="Kamigyō", polygon=R(IMADEGAWA, NIJO, OMIYA, KYOGOKU), density="dense", periods=["ashikaga-1400"]),
    dict(name="Kitano gate town", polygon=R(35.0320, 35.0270, 135.7340, 135.7410), density="loose", periods=["ashikaga-1400"]),
    dict(name="Between the two towns", polygon=R(NIJO, SANJO, HORIKAWA, KYOGOKU), density="loose", periods=["ashikaga-1400"]),
    dict(name="Shimogyō", polygon=R(SANJO, GOJO, HORIKAWA, KYOGOKU + 0.0002), density="dense", periods=["ashikaga-1400"]),
    dict(name="Shimogyō, south", polygon=R(GOJO, SHICHIJO, HORIKAWA, KYOGOKU), density="loose", periods=["ashikaga-1400"]),
    dict(name="Mibu and Ōmiya farms", polygon=R(NIJO, SHICHIJO, MIBU, HORIKAWA), density="loose", periods=["ashikaga-1400"]),
    dict(name="Tō-ji gate town", polygon=R(SHICHIJO, 34.9822, MIBU, NISHINOTOIN), density="loose", periods=["ashikaga-1400"]),
    dict(name="Gion gate town", polygon=R(35.0055, 35.0000, 135.7730, 135.7790), density="dense", periods=["ashikaga-1400"]),
    dict(name="Kiyomizu-zaka", polygon=R(34.9985, 34.9962, 135.7798, 135.7832), density="dense", periods=["ashikaga-1400"]),
    dict(name="Rokuhara", polygon=R(34.9975, 34.9915, 135.7712, 135.7775), density="loose", periods=["ashikaga-1400"]),
    # edo-1750: Hideyoshi's city
    dict(name="Nishijin", polygon=R(35.0345, 35.0240, 135.7385, OMIYA), density="dense", periods=["edo-1750"]),
    dict(name="Kamigyō, north", polygon=R(35.0360, IMADEGAWA, OMIYA, 135.7700), density="dense", periods=["edo-1750"]),
    dict(name="Kamigyō", polygon=R(IMADEGAWA, NIJO, OMIYA, KYOGOKU), density="dense", periods=["edo-1750"]),
    dict(name="Teramachi and Kawaramachi", polygon=R(35.0280, 34.9965, KYOGOKU + 0.0003, 135.7698), density="dense", periods=["edo-1750"]),
    dict(name="Central wards", polygon=R(NIJO, SHIJO, OMIYA - 0.0010, KYOGOKU), density="dense", periods=["edo-1750"]),
    dict(name="Shimogyō", polygon=R(SHIJO, SHICHIJO, OMIYA, KYOGOKU), density="dense", periods=["edo-1750"]),
    dict(name="Shimogyō, south", polygon=R(SHICHIJO, 34.9810, OMIYA, 135.7660), density="loose", periods=["edo-1750"]),
    dict(name="Senbon and Mibu", polygon=R(35.0240, SHICHIJO, 135.7385, OMIYA - 0.0010), density="loose", periods=["edo-1750"]),
    dict(name="Shimabara and the west", polygon=R(SHICHIJO, 34.9820, 135.7395, OMIYA), density="loose", periods=["edo-1750"]),
    dict(name="Gion", polygon=R(35.0085, 34.9998, 135.7728, 135.7805), density="dense", periods=["edo-1750"]),
    dict(name="Higashiyama slopes", polygon=R(34.9998, 34.9940, 135.7718, 135.7840), density="dense", periods=["edo-1750"]),
    dict(name="Awataguchi", polygon=R(35.0125, 35.0085, 135.7730, 135.7860), density="dense", periods=["edo-1750"]),
    dict(name="Okazaki villages", polygon=R(35.0230, 35.0125, 135.7730, 135.7850), density="loose", periods=["edo-1750"]),
    dict(name="Shichijō east", polygon=R(34.9940, 34.9850, 135.7705, 135.7790), density="loose", periods=["edo-1750"]),
]

GARDENS = [
    dict(name="Imperial pastures", polygon=R(35.0360, 35.0300, 135.7300, 135.7380), kind="park", periods=HEIAN),
    dict(name="Fields of Suzaku-no", polygon=R(NIJO - 0.0005, SHIJO + 0.0005, 135.7300, MIBU - 0.0004), kind="orchard", periods=["ashikaga-1400"]),
    dict(name="Ukyō fields", polygon=R(SHIJO - 0.0005, KUJO + 0.0005, 135.7320, MIBU - 0.0006), kind="orchard", periods=["ashikaga-1400"]),
    dict(name="Maruyama", polygon=R(35.0060, 35.0040, 135.7800, 135.7840), kind="park", periods=["edo-1750"]),
    dict(name="Shōgoin radish fields", polygon=R(35.0230, 35.0160, 135.7740, 135.7820), kind="orchard", periods=["ashikaga-1400"]),
    dict(name="Kujō leek fields", polygon=R(34.9810, 34.9760, 135.7550, 135.7640), kind="orchard", periods=["edo-1750"]),
]

DISTRICTS = [
    dict(id="daidairi", name="Daidairi (Greater Palace)", polygon=R(ICHIJO, NIJO, NISHI_OMIYA, OMIYA), periods=HEIAN,
         description="The walled precinct of the state: the State Halls (Chōdō-in) with the Daigokuden, the Hall of Abundant Pleasures (Burakuin), the emperor's residence (Dairi) and dozens of ministry compounds. Abandoned after the fires of 1177 and 1227; its site became the fields of Uchino."),
    dict(id="sakyo", name="Sakyō (Left Capital)", polygon=R(NIJO, KUJO, SUZAKU, KYOGOKU), periods=HEIAN,
         description="The eastern half, 'left' as the emperor looks south. Higher and drier, it became the real city, where nobles built their mansions and the East Market thrived."),
    dict(id="ukyo", name="Ukyō (Right Capital)", polygon=R(NIJO, KUJO, WEST, SUZAKU), periods=HEIAN,
         description="The western half, low and marshy toward the Katsura. Settled slowly and abandoned early: by 982 it was 'almost a wilderness'."),
    dict(id="kamigyo", name="Kamigyō (Upper Town)", polygon=R(35.0345, NIJO, OMIYA, KYOGOKU), periods=LATER,
         description="The northern town of courtiers, the shogun's palace, Zen monasteries and, after the Ōnin War, the Nishijin weavers."),
    dict(id="shimogyo", name="Shimogyō (Lower Town)", polygon=R(SANJO, SHICHIJO, HORIKAWA, KYOGOKU), periods=LATER,
         description="The merchants' town around Shijō and Muromachi: sake brewers, moneylenders, cloth dealers, and the neighbourhoods that build the Gion floats."),
    dict(id="gion", name="Gion", polygon=R(35.0080, 34.9998, 135.7725, 135.7800), periods=["fujiwara-1000", "ashikaga-1400", "edo-1750"],
         description="The gate town of the Gion shrine. In the Edo period its teahouses (chaya) made it the city's pleasure quarter, licensed in 1712."),
    dict(id="nishijin", name="Nishijin", polygon=R(35.0345, 35.0240, 135.7385, OMIYA), periods=["edo-1750"],
         description="'West Camp': named for the Western Army's headquarters in the Ōnin War, then home of the silk weavers who returned after it. Several thousand looms in the eighteenth century."),
]

LABELS = [
    dict(text="Kamo-gawa", position=(35.0190, 135.7728), size="md", rotation=-88),
    dict(text="Higashiyama", position=(35.0020, 135.7905), size="lg", rotation=-80),
    dict(text="Heian-kyō", position=(34.9905, 135.7450), size="lg", periods=["heian-800"]),
    dict(text="Sakyō", position=(34.9960, 135.7600), size="lg", periods=HEIAN),
    dict(text="Ukyō", position=(34.9960, 135.7280), size="lg", periods=HEIAN),
    dict(text="Daidairi", position=(35.0250, 135.7395), size="md", periods=HEIAN),
    dict(text="Kamigyō", position=(35.0230, 135.7530), size="lg", periods=LATER),
    dict(text="Shimogyō", position=(35.0010, 135.7620), size="lg", periods=LATER),
    dict(text="Nishijin", position=(35.0300, 135.7430), size="md", periods=["edo-1750"]),
    dict(text="Gion", position=(35.0050, 135.7760), size="md", periods=["fujiwara-1000", "ashikaga-1400", "edo-1750"]),
    dict(text="Rakuchū", position=(35.0110, 135.7600), size="sm", periods=["edo-1750"]),
    dict(text="Rokuhara", position=(34.9945, 135.7745), size="sm", periods=["fujiwara-1000", "ashikaga-1400"]),
    dict(text="Suzaku-no (fields)", position=(35.0055, 135.7385), size="sm", periods=["ashikaga-1400"]),
]

SOURCES = [
    dict(id="wiki-heian-kyo", title="Heian-kyō", author="Wikipedia", url="https://en.wikipedia.org/wiki/Heian-ky%C5%8D"),
    dict(id="wiki-kyoto-history", title="History of Kyoto", author="Wikipedia", url="https://en.wikipedia.org/wiki/History_of_Kyoto"),
    dict(id="wiki-kamo-river", title="Kamo River", author="Wikipedia", url="https://en.wikipedia.org/wiki/Kamo_River"),
    dict(id="wiki-takase", title="Takase River", author="Wikipedia", url="https://en.wikipedia.org/wiki/Takase_River"),
    dict(id="wiki-odoi", title="Odoi", author="Wikipedia", url="https://en.wikipedia.org/wiki/Odoi"),
    dict(id="stavros", title="Kyoto: An Urban History of Japan's Premodern Capital", author="Matthew Stavros", year=2014),
    dict(id="ponsonby-fane", title="Kyoto: The Old Capital of Japan, 794–1869", author="Richard Ponsonby-Fane", year=1956),
    dict(id="mccullough", title="The Capital and Its Society (Cambridge History of Japan, vol. 2: Heian Japan)", author="William H. McCullough", year=1999),
    dict(id="fieve-waley", title="Japanese Capitals in Historical Perspective: Place, Power and Memory in Kyoto, Edo and Tokyo", author="Nicolas Fiévé and Paul Waley (eds.)", year=2003),
    dict(id="berry", title="The Culture of Civil War in Kyoto", author="Mary Elizabeth Berry", year=1994),
    dict(id="chiteiki", title="Chiteiki (Record of the Pond Pavilion)", author="Yoshishige no Yasutane", year=982, url="https://en.wikipedia.org/wiki/Yoshishige_no_Yasutane"),
]
