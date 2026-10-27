# Samarkand: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
ALL = ["sogdian-650", "samanid-950", "timur-1404", "ulughbeg-1440", "shaybanid-1650"]
EARLY = ["sogdian-650", "samanid-950"]
TIMURID_ON = ["timur-1404", "ulughbeg-1440", "shaybanid-1650"]
TIMURID = ["timur-1404", "ulughbeg-1440"]

SOURCES = [
    dict(id="barthold-turkestan", title="Turkestan Down to the Mongol Invasion", author="V. V. Barthold", year=1928, note="2nd English edition; the description of Samarkand from the Arab geographers"),
    dict(id="clavijo", title="Embassy to Tamerlane, 1403–1406", author="Ruy González de Clavijo", year="1406 (trans. Guy Le Strange, 1928)", url="https://en.wikipedia.org/wiki/Ruy_Gonz%C3%A1lez_de_Clavijo"),
    dict(id="istakhri", title="Kitab al-Masalik wa'l-Mamalik", author="al-Istakhri", year="c. 950", url="https://en.wikipedia.org/wiki/Istakhri"),
    dict(id="ibn-hawqal", title="Surat al-Ard", author="Ibn Hawqal", year="c. 977", url="https://en.wikipedia.org/wiki/Ibn_Hawqal"),
    dict(id="golombek-wilber", title="The Timurid Architecture of Iran and Turan", author="Lisa Golombek and Donald Wilber", year=1988),
    dict(id="de-la-vaissiere", title="Sogdian Traders: A History", author="Étienne de la Vaissière", year=2005),
    dict(id="grenet-afrasiab", title="Samarkand / Afrasiab excavations (French–Uzbek archaeological mission reports)", author="Frantz Grenet et al.", year="1989–2020"),
    dict(id="wiki-samarkand", title="Samarkand", author="Wikipedia", url="https://en.wikipedia.org/wiki/Samarkand"),
    dict(id="wiki-history-samarkand", title="Samarkand: History", author="Wikipedia", url="https://en.wikipedia.org/wiki/Samarkand#History"),
    dict(id="wiki-afrasiyab", title="Afrasiyab (Samarkand)", author="Wikipedia", url="https://en.wikipedia.org/wiki/Afrasiyab_(Samarkand)"),
    dict(id="wiki-siab", title="Siab Bazaar", author="Wikipedia", url="https://en.wikipedia.org/wiki/Siyob_Bazaar"),
    dict(id="wiki-zarafshan", title="Zarafshon (river)", author="Wikipedia", url="https://en.wikipedia.org/wiki/Zarafshon_(river)"),
]

CITY = dict(
    name="Samarkand", subtitle="Maracanda, Face of the Earth",
    description="A thousand years of Samarkand between the Siab stream and the Dargom canal: the Sogdian merchant city on the loess plateau of Afrasiyab, the Samanid city of paper and gardens spreading south, and after the Mongol sack of 1220 the new walled city where Timur, Ulugh Beg and the Uzbek khans raised the Registan, Bibi-Khanym and the Gur-e-Amir. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="timur-1404",
    world=dict(heightScale=1.1, walls=["#DCC59E", "#CFB68C", "#E4D3B2", "#C9AC80", "#D6BF96"], roofs=["#C6AA7E", "#B99D72"]),
    camera=dict(target=(39.6560, 66.9780), distance=40),
)

# north-west corner, south-east corner: the Siab north of Afrasiyab to the Dargom, the Ark to the Kohak hill
FRAME = ((39.6840, 66.9430), (39.6300, 67.0120))

PALETTE = dict(parchment="#E8D6AE", ink="#6A4A30", water="#5E8A8C", hill="#A08A5E", road="#8C6A48")
COMPASS = (39.6800, 67.0080)
CARTOUCHE = (39.6320, 66.9450)

PERIODS = [
    dict(id="sogdian-650", label="Sogdian Samarkand", year=650, startYear=500, endYear=712,
         summary="Maracanda of Alexander's historians, now the chief city of Sogdiana, ruled by its ikhshid kings under loose Turkic and Chinese overlordship. The walled city covers the loess plateau of Afrasiyab: a citadel on the north point, a temple, merchants' houses with painted halls. Sogdian traders run the caravan routes from Iran to China. Mud brick and pakhsa (rammed loess), timber columns, painted plaster.",
         population="perhaps 40,000–50,000",
         feel="Sogdian, Turkic and Chinese in the bazaar, fire altars and painted gods, camels loading silk and musk at the gates, lutes and wine at a merchant's feast.",
         style="courtyard",
         houses=dict(title="Sogdian merchants' houses", text="Two-storey houses of pakhsa and mud brick packed along narrow lanes; the richest had a square reception hall with four wooden columns, benches along the walls, and paintings of gods, heroes and banquets covering every wall."),
         outskirts=dict(title="Vineyards and estates", text="Below the plateau, irrigated vineyards, orchards and the fortified farmhouses (kushk) of landowners, fed by channels from the Zarafshan; villages of craftsmen along the Siab.")),
    dict(id="samanid-950", label="Samanid Samarkand", year=950, startYear=713, endYear=1220,
         summary="Taken by the Arabs in 712, Samarkand becomes a great Islamic city under the Samanids (819–999) and the Karakhanids. Afrasiyab is the walled inner city with four gates and the Friday mosque by the citadel; a vast walled suburb (rabad) of markets and gardens spreads south. The city makes paper, sells it across the caliphate, and drinks from a lead-lined canal. Sacked by the Mongols in 1220.",
         population="perhaps 100,000 or more",
         feel="Water running in lead channels and open ariqs, the thud of paper-mill hammers on the streams, Persian and Arabic in the mosques, slave and silk caravans at the gates.",
         style="courtyard",
         houses=dict(title="Houses of the rabad", text="Single and two-storey courtyard houses of mud brick with flat roofs of beams, reeds and clay; plastered halls carved with stucco; a pool or a channel in the yard. Istakhri says nearly every house had a garden and running water."),
         outskirts=dict(title="Gardens of Sughd", text="Geographers called the valley of Sughd one of the four paradises of the earth: orchards, vineyards, melon fields and summer houses as far as the eye could see from the citadel.")),
    dict(id="timur-1404", label="Timur's capital", year=1404, startYear=1221, endYear=1408,
         summary="Old Afrasiyab, sacked in 1220, lies empty; the city has moved south. Timur (r. 1370–1405) made it his capital, walled it in the 1370s and filled it with the spoils and craftsmen of his conquests. In 1404 Clavijo, envoy of Castile, finds the Bibi-Khanym mosque just built, the Gur-e-Amir ready for Timur's grandson, and the tents and garden palaces of the court outside the walls.",
         population="perhaps 150,000 with the deported craftsmen",
         feel="Scaffolds and elephants at the great mosque, glazed tiles stacked in the lanes, horse meat and melons for the feast, the drums of the court in the meadow of Kan-i Gil.",
         style="courtyard",
         houses=dict(title="Mahallas of Timur's city", text="Mud-brick courtyard houses with flat earth roofs, an ayvan porch on carved wooden columns facing the court, a pool and a vine; each mahalla with its own small mosque and well. Clavijo thought the city a little larger than Seville."),
         outskirts=dict(title="Garden suburbs", text="Outside the walls Clavijo found more houses than within, and the great gardens of Timur and his family, each walled, with a palace, pools and avenues of trees.")),
    dict(id="ulughbeg-1440", label="Ulugh Beg's Samarkand", year=1440, startYear=1409, endYear=1499,
         summary="Timur's grandson Ulugh Beg governs Samarkand from 1409 and makes it a city of science: a madrasa on the Registan (1417–1420), a khanaqah and caravanserai round the square, and the great observatory on the Kohak hill (c. 1428–1429), where his astronomers compile a new star catalogue. He is murdered in 1449; the Timurid princes quarrel over the city.",
         population="perhaps 150,000",
         feel="Students reciting in the madrasa cells, the glint of the meridian arc on Kohak, scholars arguing mathematics in Persian, the din of the Registan market.",
         style="courtyard",
         houses=dict(title="Mahallas round the Registan", text="Dense one- and two-storey courtyard houses of mud brick and timber, flat-roofed, with ayvans and carved doors; workshops of potters, weavers and coppersmiths grouped by trade in their own mahallas and bazaars."),
         outskirts=dict(title="Gardens and shrines", text="Garden palaces kept by the princes, the meadows of the Kohak hill, and the tombs and khanaqahs that grew up along the roads out of the gates.")),
    dict(id="shaybanid-1650", label="Samarkand of the Uzbek khans", year=1650, startYear=1500, endYear=1750,
         summary="The Uzbek Shaybanids take Samarkand in 1500; later Bukhara becomes the capital and Samarkand a provincial seat under its Janid (Ashtarkhanid) khans. The governor Yalangtush Bahadur completes the Registan with the Sher-Dor (1619–1636) and Tilya-Kori (1646–1660) madrasas. The observatory is a ruin, Bibi-Khanym decaying.",
         population="perhaps 50,000–80,000 and falling",
         feel="Tigers and suns blazing on the new portal, gold leaf in the Tilya-Kori mosque, pigeons in the cracked dome of Bibi-Khanym, caravans thinner than before.",
         style="courtyard",
         houses=dict(title="Uzbek mahallas", text="Courtyard houses of mud brick on timber frames, with a men's outer court and a women's inner court, ayvans on carved columns, flat clay roofs where people slept in summer; a guzar square with a mosque, a pool and a teahouse-like gathering place."),
         outskirts=dict(title="Fields and orchards", text="Much of the old walled area and the Timurid gardens returned to orchards, melon fields and cemeteries; villages along the canals.")),
]

# ---------------------------------------------------------------- water
SIAB = [(39.6480, 67.0120), (39.6530, 67.0080), (39.6565, 67.0045), (39.6610, 67.0005), (39.6660, 66.9982), (39.6715, 66.9972), (39.6765, 66.9945),
        (39.6795, 66.9880), (39.6805, 66.9790), (39.6800, 66.9690), (39.6812, 66.9580), (39.6828, 66.9480), (39.6840, 66.9430)]
DARGOM = [(39.6318, 67.0120), (39.6322, 67.0000), (39.6330, 66.9880), (39.6338, 66.9760), (39.6345, 66.9640), (39.6352, 66.9530), (39.6360, 66.9430)]

WATER = [
    dict(id="siab", name="Siab (Siyob)", path=SIAB, width=24,
         blurb="The 'Black Water': a spring-fed stream that runs round the east and north foot of Afrasiyab to the Zarafshan. Its ravine protected the old city; its current drove the mills, including, by tradition, Samarkand's paper mills."),
    dict(id="dargom", name="Dargom canal", path=DARGOM, width=30,
         blurb="The great canal taken off the Zarafshan east of the city, which watered the gardens of the south side. Arab geographers knew it as the Barsh or Dargham; its course here is approximate."),
    dict(id="obi-mashhad", name="Obi-Mashhad ravine", path=[(39.6600, 66.9690), (39.6650, 66.9688), (39.6710, 66.9700), (39.6765, 66.9712), (39.6800, 66.9710)], width=10,
         blurb="A stream in a deep loess ravine along the west side of Afrasiyab, running north to the Siab; the old city's western moat."),
    dict(id="ariq-west", name="Ariq of the Ark", path=[(39.6345, 66.9640), (39.6400, 66.9636), (39.6450, 66.9645), (39.6488, 66.9640)], width=5,
         blurb="One of the ariqs (open irrigation channels) led off the Dargom into the city: each mahalla took its turn of water by day and night.", periods=TIMURID_ON),
    dict(id="ariq-centre", name="Ariq of the Registan", path=[(39.6338, 66.9800), (39.6400, 66.9795), (39.6460, 66.9790), (39.6520, 66.9784)], width=5,
         blurb="An ariq running north toward the Registan. One explanation of the name Registan, 'sandy place', is the silt such channels left on the square.", periods=TIMURID_ON),
    dict(id="ariq-east", name="Eastern ariq", path=[(39.6330, 66.9900), (39.6400, 66.9895), (39.6460, 66.9880), (39.6520, 66.9865)], width=5,
         blurb="An irrigation channel feeding the gardens and pools of the east side of the city.", periods=TIMURID_ON),
    dict(id="ariq-rabad", name="Ariqs of the rabad", path=[(39.6338, 66.9790), (39.6420, 66.9790), (39.6500, 66.9800), (39.6560, 66.9795)], width=5,
         blurb="Channels from the Dargom running north through the suburbs; Istakhri says almost every house and garden of Samarkand had running water.", periods=EARLY),
]

AFR = [(39.6628, 66.9745), (39.6668, 66.9716), (39.6715, 66.9732), (39.6752, 66.9788), (39.6772, 66.9845), (39.6762, 66.9905), (39.6722, 66.9945),
       (39.6675, 66.9950), (39.6650, 66.9918), (39.6642, 66.9862), (39.6634, 66.9822)]

HILLS = [
    dict(id="afrasiyab", name="Afrasiyab", center=(39.6698, 66.9840), radius=780,
         blurb="A plateau of loess about 220 hectares, cut off by ravines and the Siab: the site of Samarkand from the 7th century BCE to the Mongol sack of 1220, named in later legend after the Turanian king of the Shahnameh. Abandoned afterwards to graves and fields."),
    dict(id="kohak", name="Kohak (Chupan-ata spur)", center=(39.6745, 67.0055), radius=360,
         blurb="The 'little mountain', a spur of the Chupan-ata hills across the Siab, where Ulugh Beg built his observatory and Timurid princes kept the Bagh-i Maydan garden."),
    dict(id="khizr-hill", name="Hill of Hazrat Khizr", center=(39.6631, 66.9846), radius=70, label=False,
         blurb="A loess knoll by the old south gate of Afrasiyab, crowned by a mosque since early Islamic times."),
]

ROADS = [
    # ---- Afrasiyab: the inner city's cross streets and the roads out of its gates
    dict(id="afr-ns", name="Street of the Kesh gate", path=[(39.6636, 66.9828), (39.6670, 66.9832), (39.6705, 66.9838), (39.6735, 66.9845)], width=12, style="major", labelled=True,
         blurb="From the citadel south to the Kesh gate (Bab al-Kish), the way to the rabad and to Kesh (Shahrisabz). The modern road through Afrasiyab runs close to it.", periods=EARLY),
    dict(id="afr-ew", name="Street of the China gate", path=[(39.6668, 66.9725), (39.6680, 66.9790), (39.6690, 66.9838), (39.6695, 66.9890), (39.6690, 66.9945)], width=10, style="major",
         blurb="Across the inner city from the Nawbahar gate in the west to the China gate (Bab al-Sin) in the east.", periods=EARLY),
    dict(id="kesh-road", name="Road to Kesh", path=[(39.6634, 66.9824), (39.6600, 66.9805), (39.6560, 66.9790), (39.6500, 66.9785), (39.6420, 66.9780), (39.6300, 66.9775)], width=12, style="major", labelled=True,
         blurb="South through the rabad and across the Dargom toward Kesh and the passes to Bactria: the main street of the suburbs.", periods=EARLY),
    dict(id="bukhara-road-early", name="Road to Bukhara", path=[(39.6668, 66.9722), (39.6660, 66.9620), (39.6650, 66.9520), (39.6640, 66.9430)], width=12, style="major", labelled=True,
         blurb="West down the Zarafshan valley to Bukhara: the caravan route to Merv and Iran.", periods=EARLY),
    dict(id="china-road", name="Road to Ustrushana and China", path=[(39.6690, 66.9948), (39.6700, 67.0030), (39.6720, 67.0120)], width=10, style="major",
         blurb="East up the valley toward Panjikant, Ustrushana and the passes to Ferghana and China.", periods=EARLY),
    dict(id="rabad-west", name="Street of the rabad", path=[(39.6560, 66.9790), (39.6540, 66.9700), (39.6520, 66.9600), (39.6500, 66.9500)], width=8, style="minor", periods=EARLY,
         blurb="A street of the outer city running west among the gardens."),
    # ---- the Timurid city: streets meeting at the Registan
    dict(id="timur-street", name="Timur's bazaar street", path=[(39.6558, 66.9768), (39.6578, 66.9786), (39.6598, 66.9812), (39.6612, 66.9812), (39.6618, 66.9808)], width=14, style="major", labelled=True,
         blurb="From the Registan to the Iron Gate past Bibi-Khanym. In 1404 Timur had it cut through the houses and lined with shops under a vaulted roof in some twenty days, working by night and day (Clavijo).", periods=TIMURID_ON),
    dict(id="shah-i-zinda-road", name="Road to Shah-i-Zinda", path=[(39.6618, 66.9808), (39.6621, 66.9835), (39.6619, 66.9866)], width=8, style="minor", periods=TIMURID_ON,
         blurb="From the Iron Gate along the foot of Afrasiyab to the street of tombs."),
    dict(id="kohak-road", name="Road to Kohak", path=[(39.6620, 66.9866), (39.6650, 66.9960), (39.6690, 66.9985), (39.6735, 67.0035)], width=8, style="minor", periods=["ulughbeg-1440", "shaybanid-1650"],
         blurb="Out past Shah-i-Zinda and across the Siab to the observatory hill and the Bagh-i Maydan."),
    dict(id="karizgah-street", name="Street of the Karizgah gate", path=[(39.6538, 66.9764), (39.6500, 66.9768), (39.6460, 66.9770), (39.6419, 66.9772)], width=12, style="major", labelled=True,
         blurb="South from the Registan to the Karizgah gate and on to Kesh, Timur's birthplace.", periods=TIMURID_ON),
    dict(id="kesh-road-late", name="Road to Shahrisabz", path=[(39.6419, 66.9772), (39.6360, 66.9770), (39.6300, 66.9768)], width=10, style="major", periods=TIMURID_ON,
         blurb="Across the Dargom toward Kesh, which Timur renamed Shahr-i Sabz, the Green City."),
    dict(id="chorsu-street", name="Street of the Chorsu", path=[(39.6546, 66.9744), (39.6537, 66.9734), (39.6530, 66.9690), (39.6520, 66.9640)], width=10, style="major",
         blurb="West from the Registan through the Chorsu crossing to the gate of the Ark.", periods=TIMURID_ON),
    dict(id="bukhara-street", name="Street of the Bukhara gate", path=[(39.6537, 66.9734), (39.6555, 66.9690), (39.6572, 66.9630)], width=10, style="major", periods=TIMURID_ON,
         blurb="From the Chorsu north-west to the Bukhara gate."),
    dict(id="bukhara-road", name="Road to Bukhara", path=[(39.6572, 66.9626), (39.6590, 66.9540), (39.6610, 66.9430)], width=12, style="major", labelled=True, periods=TIMURID_ON,
         blurb="The caravan road west to Bukhara, 250 km down the Zarafshan."),
    dict(id="shaykhzada-street", name="Street of the Shaykhzada gate", path=[(39.6556, 66.9752), (39.6580, 66.9722), (39.6604, 66.9690)], width=8, style="minor", periods=TIMURID_ON,
         blurb="North-west from the Registan to the Shaykhzada gate; gate names after Sharaf al-Din Yazdi and Clavijo, positions approximate."),
    dict(id="firuza-street", name="Street of the Firuza gate", path=[(39.6550, 66.9774), (39.6553, 66.9830), (39.6555, 66.9880), (39.6557, 66.9924)], width=10, style="major", periods=TIMURID_ON,
         blurb="East from the Registan to the Turquoise gate (Firuza) and the roads to the garden palaces."),
    dict(id="firuza-road", name="Road to the gardens", path=[(39.6557, 66.9928), (39.6560, 67.0040), (39.6560, 67.0120)], width=10, style="minor", periods=TIMURID_ON,
         blurb="Out to the garden palaces and the meadow of Kan-i Gil on the Siab, where Timur pitched his tents."),
    dict(id="sozangaran-street", name="Street of the Sozangaran gate", path=[(39.6542, 66.9772), (39.6510, 66.9830), (39.6472, 66.9898)], width=8, style="minor", periods=TIMURID_ON,
         blurb="South-east to the gate of the needle-makers (Sozangaran)."),
    dict(id="sozangaran-road", name="Road south-east", path=[(39.6470, 66.9905), (39.6420, 67.0000), (39.6380, 67.0120)], width=8, style="minor", periods=TIMURID_ON,
         blurb="Toward the villages up the Dargom and the road to Panjikant."),
]

WALLS = [
    dict(id="afrasiyab-walls", name="Walls of Afrasiyab", path=AFR, closed=True, periods=EARLY,
         blurb="Several lines of pakhsa and mud-brick ramparts round the plateau, rebuilt from the 6th century BCE to the 12th century CE; four gates in Arab times: Nawbahar (west), Bukhara (north), China (east) and Kesh (south)."),
    dict(id="afrasiyab-ruin", name="Ramparts of Afrasiyab (ruined)", path=AFR, closed=True, periods=TIMURID_ON,
         blurb="Breached by the Mongols in 1220 and never rebuilt: eroded loess ramparts round an empty plateau of mounds, potsherds and graves."),
    dict(id="rabad-wall", name="Wall of the rabad", path=[(39.6634, 66.9745), (39.6600, 66.9560), (39.6500, 66.9500), (39.6400, 66.9560), (39.6355, 66.9700), (39.6352, 66.9860),
                                                            (39.6420, 66.9990), (39.6530, 67.0040), (39.6620, 66.9985), (39.6650, 66.9918)],
         periods=["samanid-950"],
         blurb="The outer wall round the suburbs, with many gates, described by Istakhri and Ibn Hawqal; its line is drawn here schematically. Beyond it a still longer wall enclosed the gardens and villages."),
    dict(id="timur-walls", name="Walls of Timur's city", path=[(39.6532, 66.9625), (39.6560, 66.9618), (39.6585, 66.9640), (39.6605, 66.9690), (39.6613, 66.9750), (39.6618, 66.9805),
                                                                (39.6612, 66.9850), (39.6590, 66.9895), (39.6556, 66.9928), (39.6515, 66.9930), (39.6472, 66.9905), (39.6440, 66.9860),
                                                                (39.6420, 66.9800), (39.6418, 66.9740), (39.6430, 66.9690), (39.6455, 66.9650), (39.6485, 66.9628), (39.6503, 66.9625)],
         periods=TIMURID_ON,
         blurb="Mud-brick walls with a moat, built round the new city in the 1370s and joined to the Ark on the west. Six gates: Ahanin (Iron), Firuza, Sozangaran, Karizgah, Bukhara and Shaykhzada; their positions here follow the usual reconstruction."),
]

GATES = [
    dict(id="bab-al-kish", name="Bab al-Kish (Kesh gate)", position=(39.6634, 66.9824), periods=EARLY),
    dict(id="bab-nawbahar", name="Bab Nawbahar", position=(39.6668, 66.9719), periods=EARLY),
    dict(id="bab-bukhara-afr", name="Bab Bukhara", position=(39.6752, 66.9788), periods=EARLY),
    dict(id="bab-al-sin", name="Bab al-Sin (China gate)", position=(39.6688, 66.9948), periods=EARLY),
    dict(id="ahanin", name="Darvaza-i Ahanin (Iron Gate)", position=(39.6618, 66.9807), periods=TIMURID_ON),
    dict(id="firuza", name="Firuza gate", position=(39.6557, 66.9926), periods=TIMURID_ON),
    dict(id="sozangaran", name="Sozangaran gate", position=(39.6472, 66.9903), periods=TIMURID_ON),
    dict(id="karizgah", name="Karizgah gate", position=(39.6419, 66.9772), periods=TIMURID_ON),
    dict(id="bukhara-gate", name="Bukhara gate", position=(39.6573, 66.9628), periods=TIMURID_ON),
    dict(id="shaykhzada", name="Shaykhzada gate", position=(39.6604, 66.9690), periods=TIMURID_ON),
]

BRIDGES = [
    dict(id="dargom-bridge", name="Bridge over the Dargom", path=[(39.6345, 66.9774), (39.6328, 66.9774)], build="stone", arches=3, periods=EARLY,
         blurb="Where the road to Kesh crossed the great canal south of the city."),
    dict(id="dargom-bridge-late", name="Bridge over the Dargom", path=[(39.6347, 66.9769), (39.6326, 66.9768)], build="stone", arches=3, periods=TIMURID_ON,
         blurb="The crossing of the Dargom on the road to Shahrisabz."),
    dict(id="siab-bridge-gardens", name="Bridge over the Siab", path=[(39.6560, 67.0035), (39.6560, 67.0062)], build="timber", arches=2, periods=TIMURID_ON,
         blurb="A crossing of the Siab on the way to the meadows and garden palaces east of the city."),
    dict(id="siab-bridge-kohak", name="Bridge to Kohak", path=[(39.6678, 66.9968), (39.6694, 66.9990)], build="timber", arches=2, periods=["ulughbeg-1440", "shaybanid-1650"],
         blurb="The crossing of the Siab below the observatory hill."),
    dict(id="china-bridge", name="Bridge at the China gate", path=[(39.6696, 66.9962), (39.6699, 66.9992)], build="timber", arches=2, periods=EARLY,
         blurb="Where the road east crossed the Siab below the China gate."),
]

AQUEDUCTS = [
    dict(name="Juy-i Arziz (the Lead Canal)", path=[(39.6560, 66.9798), (39.6590, 66.9810), (39.6615, 66.9820), (39.6634, 66.9826)], periods=["samanid-950"]),
]

BLOCKS = [
    # ---- Afrasiyab, the inner city (650, 950); the citadel in the north point is left clear
    dict(name="West quarter of Afrasiyab", polygon=[(39.6640, 66.9752), (39.6675, 66.9730), (39.6676, 66.9785), (39.6672, 66.9824), (39.6642, 66.9822)], density="dense", periods=EARLY),
    dict(name="Quarter of the Kesh gate", polygon=[(39.6645, 66.9838), (39.6684, 66.9838), (39.6688, 66.9890), (39.6660, 66.9915), (39.6650, 66.9870)], density="dense", periods=EARLY),
    dict(name="North-west quarter", polygon=[(39.6686, 66.9735), (39.6714, 66.9742), (39.6738, 66.9790), (39.6710, 66.9830), (39.6688, 66.9800)], density="dense", periods=EARLY),
    dict(name="Quarter of the China gate", polygon=[(39.6700, 66.9848), (39.6718, 66.9850), (39.6745, 66.9895), (39.6718, 66.9935), (39.6700, 66.9930)], density="dense", periods=EARLY),
    # ---- the suburbs south of Afrasiyab
    dict(name="Suburb by the Kesh gate", polygon=[(39.6580, 66.9730), (39.6620, 66.9740), (39.6624, 66.9795), (39.6570, 66.9782)], density="dense", periods=["sogdian-650"]),
    dict(name="Craftsmen by the Siab", polygon=[(39.6600, 66.9840), (39.6635, 66.9880), (39.6625, 66.9950), (39.6590, 66.9900)], density="loose", periods=["sogdian-650"]),
    dict(name="Rabad: Ghatfar", polygon=[(39.6570, 66.9700), (39.6624, 66.9742), (39.6625, 66.9792), (39.6565, 66.9782)], density="dense", periods=["samanid-950"]),
    dict(name="Rabad: Ras al-Taq", polygon=[(39.6566, 66.9806), (39.6624, 66.9832), (39.6632, 66.9900), (39.6590, 66.9940), (39.6560, 66.9880)], density="dense", periods=["samanid-950"]),
    dict(name="Rabad: south-west", polygon=[(39.6460, 66.9640), (39.6530, 66.9620), (39.6550, 66.9690), (39.6555, 66.9775), (39.6470, 66.9772)], density="dense", periods=["samanid-950"]),
    dict(name="Rabad: south-east", polygon=[(39.6470, 66.9800), (39.6550, 66.9800), (39.6550, 66.9930), (39.6470, 66.9940)], density="dense", periods=["samanid-950"]),
    dict(name="Rabad: Asfizar", polygon=[(39.6390, 66.9620), (39.6455, 66.9600), (39.6460, 66.9770), (39.6380, 66.9770)], density="loose", periods=["samanid-950"]),
    dict(name="Rabad: Warsnin", polygon=[(39.6380, 66.9800), (39.6460, 66.9800), (39.6465, 66.9960), (39.6420, 66.9970), (39.6385, 66.9880)], density="loose", periods=["samanid-950"]),
    dict(name="Rabad: Matarid", polygon=[(39.6530, 66.9530), (39.6600, 66.9580), (39.6625, 66.9720), (39.6560, 66.9690), (39.6510, 66.9600)], density="loose", periods=["samanid-950"]),
    # ---- Timurid, Ulugh Beg and Uzbek city inside the walls (quarters between the main streets)
    dict(name="Mahallas of the Ark", polygon=[(39.6505, 66.9645), (39.6520, 66.9650), (39.6527, 66.9725), (39.6505, 66.9745), (39.6490, 66.9710)], density="dense", periods=TIMURID_ON),
    dict(name="Mahallas north of the Chorsu", polygon=[(39.6538, 66.9650), (39.6560, 66.9640), (39.6548, 66.9700), (39.6536, 66.9722)], density="dense", periods=TIMURID_ON),
    dict(name="Shaykhzada mahallas", polygon=[(39.6568, 66.9650), (39.6590, 66.9665), (39.6602, 66.9700), (39.6575, 66.9730), (39.6555, 66.9718)], density="dense", periods=TIMURID_ON),
    dict(name="Mahallas below Bibi-Khanym", polygon=[(39.6578, 66.9736), (39.6612, 66.9745), (39.6614, 66.9762), (39.6580, 66.9772), (39.6566, 66.9762)], density="dense", periods=TIMURID_ON),
    dict(name="Mahallas of the Firuza street", polygon=[(39.6560, 66.9800), (39.6580, 66.9815), (39.6605, 66.9840), (39.6595, 66.9890), (39.6562, 66.9910)], density="dense", periods=TIMURID_ON),
    dict(name="Mahallas south of the Firuza street", polygon=[(39.6520, 66.9840), (39.6547, 66.9800), (39.6547, 66.9915), (39.6515, 66.9918), (39.6490, 66.9890)], density="dense", periods=TIMURID_ON),
    dict(name="Mahallas of the Karizgah street", polygon=[(39.6440, 66.9780), (39.6530, 66.9780), (39.6500, 66.9835), (39.6460, 66.9880), (39.6436, 66.9830)], density="dense", periods=TIMURID_ON),
    dict(name="Mahallas of the Gur-e-Amir", polygon=[(39.6440, 66.9705), (39.6460, 66.9665), (39.6480, 66.9650), (39.6525, 66.9760), (39.6440, 66.9760)], density="dense", periods=TIMURID_ON),
    dict(name="Suburb outside the Bukhara gate", polygon=[(39.6575, 66.9545), (39.6610, 66.9560), (39.6600, 66.9615), (39.6575, 66.9610)], density="loose", periods=TIMURID_ON),
    dict(name="Suburb outside the Karizgah gate", polygon=[(39.6360, 66.9700), (39.6410, 66.9700), (39.6412, 66.9762), (39.6360, 66.9762)], density="loose", periods=TIMURID_ON),
    dict(name="Suburb outside the Karizgah gate", polygon=[(39.6360, 66.9782), (39.6412, 66.9782), (39.6420, 66.9860), (39.6370, 66.9860)], density="loose", periods=TIMURID_ON),
    dict(name="Suburb outside the Firuza gate", polygon=[(39.6530, 66.9940), (39.6575, 66.9935), (39.6580, 66.9990), (39.6535, 66.9990)], density="loose", periods=TIMURID_ON),
]

GARDENS = [
    dict(name="Vineyards of Sughd", polygon=[(39.6440, 66.9440), (39.6560, 66.9440), (39.6560, 66.9560), (39.6440, 66.9560)], kind="vineyard", periods=EARLY),
    dict(name="Orchards of the rabad", polygon=[(39.6380, 66.9480), (39.6440, 66.9450), (39.6450, 66.9600), (39.6380, 66.9600)], kind="orchard", periods=EARLY),
    dict(name="Gardens along the Dargom", polygon=[(39.6365, 66.9880), (39.6420, 66.9990), (39.6400, 67.0110), (39.6340, 67.0110), (39.6342, 66.9900)], kind="orchard"),
    dict(name="Melon fields", polygon=[(39.6365, 66.9450), (39.6420, 66.9450), (39.6420, 66.9560), (39.6365, 66.9560)], kind="orchard", periods=TIMURID_ON),
    dict(name="Bagh-i Shamal (the North Garden)", polygon=[(39.6610, 66.9500), (39.6680, 66.9500), (39.6690, 66.9600), (39.6620, 66.9610)], kind="park", periods=TIMURID),
    dict(name="Orchards west of the city", polygon=[(39.6440, 66.9450), (39.6560, 66.9450), (39.6560, 66.9580), (39.6440, 66.9580)], kind="orchard", periods=TIMURID_ON),
    dict(name="Bagh-i Maydan", polygon=[(39.6770, 67.0000), (39.6820, 67.0010), (39.6820, 67.0110), (39.6780, 67.0100)], kind="park", periods=["ulughbeg-1440"]),
    dict(name="Garden lands east of the Siab", polygon=[(39.6590, 67.0050), (39.6660, 67.0020), (39.6700, 67.0110), (39.6600, 67.0110)], kind="orchard"),
    dict(name="Fields on Afrasiyab", polygon=[(39.6680, 66.9760), (39.6735, 66.9790), (39.6740, 66.9880), (39.6690, 66.9900), (39.6665, 66.9840)], kind="orchard", periods=TIMURID_ON),
    dict(name="Orchards by the Siab", polygon=[(39.6770, 66.9600), (39.6800, 66.9600), (39.6800, 66.9680), (39.6770, 66.9680)], kind="orchard"),
]

DISTRICTS = [
    dict(id="afrasiyab", name="Afrasiyab (the shahristan)", polygon=AFR, periods=EARLY,
         description="The walled inner city on its loess plateau: citadel, palace, temple and later the Friday mosque, and merchants' quarters along the four streets from the gates."),
    dict(id="afrasiyab-ruins", name="Afrasiyab (ruins)", polygon=AFR, periods=TIMURID_ON,
         description="The old city, deserted after the Mongol sack of 1220: mounds of melted mud brick, a few graves and the shrines on its southern slope."),
    dict(id="rabad", name="The rabad", polygon=[(39.6634, 66.9745), (39.6600, 66.9560), (39.6500, 66.9500), (39.6400, 66.9560), (39.6355, 66.9700), (39.6352, 66.9860), (39.6420, 66.9990), (39.6530, 67.0040), (39.6620, 66.9985), (39.6650, 66.9918)],
         periods=["samanid-950"], description="The outer city south of Afrasiyab: markets, caravanserais, mosques, gardens and workshops, and the residence of the Samanid governors."),
    dict(id="timur-city", name="Timur's city", polygon=[(39.6532, 66.9625), (39.6585, 66.9640), (39.6613, 66.9750), (39.6612, 66.9850), (39.6556, 66.9928), (39.6472, 66.9905), (39.6420, 66.9800), (39.6430, 66.9690), (39.6503, 66.9625)],
         periods=TIMURID_ON, description="The walled city of the 1370s, roughly today's old town: mahallas of courtyard houses round the Registan, with the Ark on the west and Bibi-Khanym by the north gate."),
    dict(id="shah-i-zinda-district", name="Shah-i-Zinda", polygon=[(39.6612, 66.9858), (39.6635, 66.9862), (39.6648, 66.9900), (39.6625, 66.9905)], periods=TIMURID_ON,
         description="The necropolis of the 'Living King', Qutham (Kusam) ibn Abbas, on the southern slope of Afrasiyab, where Timur's family and amirs built their tombs."),
    dict(id="kohak-district", name="Kohak", polygon=[(39.6715, 67.0010), (39.6780, 67.0010), (39.6780, 67.0110), (39.6715, 67.0110)], periods=["ulughbeg-1440", "shaybanid-1650"],
         description="The hill of the observatory and the Bagh-i Maydan garden north-east of the city."),
]

LABELS = [
    dict(text="Afrasiyab", position=(39.6720, 66.9860), size="lg"),
    dict(text="Siab", position=(39.6790, 66.9940), size="sm", rotation=-50),
    dict(text="Dargom", position=(39.6328, 66.9920), size="md"),
    dict(text="Samarqand", position=(39.6600, 66.9610), size="lg", periods=EARLY),
    dict(text="Rabad", position=(39.6480, 66.9860), size="md", periods=["samanid-950"]),
    dict(text="Samarqand", position=(39.6450, 66.9620), size="lg", periods=TIMURID_ON),
    dict(text="Kohak", position=(39.6720, 67.0080), size="md"),
    dict(text="Shah-i Zinda", position=(39.6648, 66.9905), size="sm", periods=TIMURID_ON),
    dict(text="Registan", position=(39.6530, 66.9790), size="sm", periods=TIMURID_ON),
    dict(text="Kan-i Gil", position=(39.6620, 67.0080), size="sm", periods=TIMURID),
    dict(text="Sughd", position=(39.6400, 66.9500), size="md", periods=EARLY),
]
