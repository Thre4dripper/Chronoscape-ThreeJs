# Timbuktu: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
ALL = ["founding-1100", "mali-1340", "songhai-1450", "askia-1550", "pashalik-1700"]
TOWN = ["mali-1340", "songhai-1450", "askia-1550", "pashalik-1700"]
EARLY_TOWN = ["mali-1340", "songhai-1450"]
LATER = ["askia-1550", "pashalik-1700"]
FROM_1450 = ["songhai-1450", "askia-1550", "pashalik-1700"]

SOURCES = [
    dict(id="sadi-tarikh", title="Ta'rikh al-Sudan", author="Abd al-Rahman al-Sa'di", year="c. 1655", note="trans. John O. Hunwick, Timbuktu and the Songhay Empire (1999)", url="https://en.wikipedia.org/wiki/Tarikh_al-Sudan"),
    dict(id="hunwick-songhay", title="Timbuktu and the Songhay Empire: Al-Sa'di's Ta'rikh al-Sudan down to 1613 and Other Contemporary Documents", author="John O. Hunwick", year=1999),
    dict(id="saad-timbuktu", title="Social History of Timbuktu: The Role of Muslim Scholars and Notables 1400–1900", author="Elias N. Saad", year=1983),
    dict(id="insoll-timbuktu", title="Urbanism, Archaeology and Trade: Further Observations on the Gao Region (Mali); the Timbuktu Rescue Project", author="Timothy Insoll", year="1996–2002", note="excavations and survey round Timbuktu"),
    dict(id="leo-africanus", title="Description of Africa, Book 7 (Timbuktu)", author="Leo Africanus (al-Hasan al-Wazzan)", year="1526, printed 1550", url="https://en.wikipedia.org/wiki/Leo_Africanus"),
    dict(id="unesco-timbuktu", title="Timbuktu (World Heritage List no. 119)", author="UNESCO World Heritage Centre", year=1988, url="https://whc.unesco.org/en/list/119/"),
    dict(id="wiki-timbuktu", title="Timbuktu", author="Wikipedia", url="https://en.wikipedia.org/wiki/Timbuktu"),
    dict(id="wiki-history-timbuktu", title="History of Timbuktu", author="Wikipedia", url="https://en.wikipedia.org/wiki/History_of_Timbuktu"),
    dict(id="wiki-kabara", title="Kabara, Mali", author="Wikipedia", url="https://en.wikipedia.org/wiki/Kabara,_Mali"),
    dict(id="wiki-niger", title="Niger River", author="Wikipedia", url="https://en.wikipedia.org/wiki/Niger_River"),
    dict(id="wiki-pashalik", title="Pashalik of Timbuktu", author="Wikipedia", url="https://en.wikipedia.org/wiki/Pashalik_of_Timbuktu"),
]

CITY = dict(
    name="Timbuktu", subtitle="City of Scholars",
    description="Seven centuries of Timbuktu on the edge of the Sahara: from a Tuareg camp round a well, through Mansa Musa's Djinguereber mosque, the scholars of Sankore and the Songhai Askias, to the Moroccan pashas. The town lies among dunes, joined to the Niger port of Kabara, 8 km to the south, by a road and a seasonal channel. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="songhai-1450",
    world=dict(heightScale=1.0, walls=["#C9A77E", "#BE9C74", "#D2B48C", "#B8946C", "#CFAE84"], roofs=["#BFA07A", "#B5946C"]),
    camera=dict(target=(16.7738, -3.0062), distance=32),
)

# north-west corner, south-east corner: the caravan ground and the dunes to the north, the start of the Kabara road and the flood plain to the south
FRAME = ((16.7890, -3.0240), (16.7560, -2.9870))

PALETTE = dict(parchment="#ECD9AE", ink="#6E4A2E", water="#6A8C86", hill="#B79A66", road="#8E6B46")
COMPASS = (16.7860, -2.9905)
CARTOUCHE = (16.7568, -3.0230)

PERIODS = [
    dict(id="founding-1100", label="The well of Buktu", year=1100, startYear=1000, endYear=1323,
         summary="According to the 17th-century Ta'rikh al-Sudan, Tuareg herders summered by the Niger and camped here, on the dunes above the flood, round a well kept by an old woman named Buktu: 'Tin Buktu', the place of Buktu. The story is a tradition; archaeology shows older settlement nearby. Leather tents, mat huts and stores of grain and salt.",
         population="a seasonal camp of a few hundred, perhaps",
         feel="Camels grunting at the well at dawn, smoke of thornwood fires, women pounding millet, wind hissing over the dunes.",
         style="sahel",
         houses=dict(title="Tents and mat huts by the well", text="Tuareg tents of tanned goatskin on wooden poles, and domed huts of mats and straw over bent sticks. Goods left in store while the herders moved north to the rains: grain, salt, hides."),
         outskirts=dict(title="Dunes and thorn scrub", text="Fixed dunes held by acacia and cram-cram grass, grazing for goats and camels; to the south the plain the Niger floods each winter.")),
    dict(id="mali-1340", label="Timbuktu of Mali", year=1340, startYear=1324, endYear=1432,
         summary="Timbuktu passes to the empire of Mali around Mansa Musa's return from his pilgrimage of 1324–25. Tradition credits the Andalusian poet Abu Ishaq al-Sahili with the Djinguereber mosque and a royal palace, the Madugu. Salt from the Sahara and gold from the south meet here; merchants from Walata begin to move in. Banco houses, mat huts, the market.",
         population="perhaps 10,000 (no figures survive)",
         feel="Caravans unloading salt slabs in the north, the Friday crowd at the new mosque, Mande, Songhay and Berber spoken in one market.",
         style="sahel",
         houses=dict(title="Banco houses round yards", text="Single-storey houses of banco (sun-dried mud brick) and soft local limestone, flat roofs of palm-rib beams and mats under a layer of earth, a yard behind a plain wall with one door."),
         outskirts=dict(title="Huts on the sand", text="Round the edges, domed mat huts of the herders and servants, goat pens of thorn branches, wells in the hollows between dunes.")),
    dict(id="songhai-1450", label="City of scholars", year=1450, startYear=1433, endYear=1492,
         summary="Mali's hold has failed: in 1433 the Tuareg chief Akil takes the town and leaves it to its own qadis and the Timbuktu-koi, its governor, until Sonni Ali of Songhai storms it in 1468. Scholars teach at Sankore and in their houses; the Sidi Yahya mosque is built in the 1440s; copyists, booksellers and paper from the north feed the manuscript trade.",
         population="perhaps 25,000 (estimates vary widely)",
         feel="Boys chanting the Qur'an from wooden boards, the scratch of reed pens in a scholar's vestibule, salt and gold weighed in the market.",
         style="sahel",
         houses=dict(title="Houses of scholars and merchants", text="Banco houses of one and two storeys round courts, the upper rooms reached by a stair from the vestibule where the master taught. Facades plastered smooth, with pilasters, drain spouts and a single wooden door."),
         outskirts=dict(title="Bella and herders' huts", text="Domed huts of straw mats over bent poles, the homes of the Bella, servile dependants of the Tuareg, and of Fulani and Tuareg herders; pens and wells among the dunes.")),
    dict(id="askia-1550", label="Timbuktu of the Askias", year=1550, startYear=1493, endYear=1590,
         summary="Under the Askia dynasty of Songhai, ruling from Gao, Timbuktu is the empire's city of learning and trade, run by qadis of the Aqit family. Leo Africanus, here around 1510, saw a rich town of scholars and judges where books sold for more than any other goods. Ahmed Baba is born in 1556; the qadi al-Aqib rebuilds the great mosques from 1570.",
         population="perhaps 50,000–80,000 at its height (estimates vary widely)",
         feel="Students from all over West Africa in the mosque courts, gold dust on the scales, the Azalai's camels kneeling in the north, drums on feast days.",
         style="sahel",
         houses=dict(title="Two-storey banco houses", text="Courtyard houses of banco and limestone, many of two storeys, with carved wooden doors studded with iron; Leo Africanus also saw huts of clay-plastered wattle under thatch, so straw and mud stood side by side."),
         outskirts=dict(title="Straw huts on the edges", text="Rings of mat-and-straw huts of the Bella, herders and the poor, camel camps of the caravan men in the north, gardens and pools to the south-west.")),
    dict(id="pashalik-1700", label="The Pashalik", year=1700, startYear=1591, endYear=1800,
         summary="After Morocco's army defeated Songhai at Tondibi in 1591, Timbuktu is ruled by pashas chosen by the soldiers (the Arma) from a kasbah in the town. Ahmed Baba is exiled to Marrakesh in 1594. The Arma marry into the town and become a local caste; trade shifts to the Atlantic coast, Tuareg raids worsen, and the town slowly declines.",
         population="perhaps 25,000 (no reliable figures)",
         feel="Arma musketeers at the kasbah gate, Moroccan-style windows over the lanes, sand drifting against empty houses on the edge of town.",
         style="sahel",
         houses=dict(title="Carved doors and Moroccan windows", text="Two-storey banco houses whose fronts carry the Moroccan touch: carved wooden window frames with grilles on the upper floor and heavy doors decorated with iron studs and plates. Replastered each year after the rains."),
         outskirts=dict(title="Drifting sand and Bella huts", text="Abandoned houses half-buried by sand on the edges, straw huts of the Bella and herders beyond them; the Tuareg camp close to the town again.")),
]

# ---------------------------------------------------------------- water: the seasonal channel from the Kabara side, the pools, the flood plain
CHANNEL = [(16.7560, -3.0140), (16.7585, -3.0128), (16.7610, -3.0116), (16.7632, -3.0107), (16.7650, -3.0100)]

WATER = [
    dict(id="kabara-channel", name="The channel to Kabara", path=CHANNEL, width=26, periods=["mali-1340", "songhai-1450", "askia-1550"],
         blurb="A seasonal creek from the Niger's flood plain toward the town. Leo Africanus wrote that when the Niger rose its water was brought into Timbuktu through channels; in high-flood months small boats could come up close to the town. Dry for half the year."),
    dict(id="kabara-channel", name="The channel to Kabara", path=CHANNEL, width=16, periods=["founding-1100", "pashalik-1700"],
         blurb="A seasonal creek from the Niger's flood plain toward the town, wet only in the months of high water (December to February) and often silted; after 1600 it was neglected and the sand pushed in."),
    dict(id="south-pool", name="The flood pool south of the town", path=[(16.7651, -3.0108), (16.7660, -3.0090)], width=80,
         blurb="A pond left by the flood at the head of the channel, where boats unloaded in good years and the town drew water, washed and watered animals; the place where gardens were dug."),
    dict(id="badjinde-channel", name="Channel into Badjindé", path=[(16.7660, -3.0090), (16.7670, -3.0066), (16.7686, -3.0046), (16.7703, -3.0034)], width=12, periods=EARLY_TOWN,
         blurb="A branch of the flood channel reaching the low ground in the middle of the town in good flood years. The quarter of Badjindé is usually said to take its name from the pool it filled; the course drawn here is an interpretation."),
    dict(id="badjinde-pool", name="The pool of Badjindé", path=[(16.7703, -3.0037), (16.7710, -3.0029)], width=44, periods=EARLY_TOWN,
         blurb="Seasonal water in the hollow of Badjindé, the town's low point; later filled and built over as the channel silted."),
]

MARSH = [
    dict(name="The flood plain toward Kabara", polygon=[(16.7622, -3.0238), (16.7628, -3.0180), (16.7618, -3.0130), (16.7604, -3.0060), (16.7600, -2.9990), (16.7590, -2.9930),
                                                        (16.7575, -2.9875), (16.7560, -2.9872), (16.7560, -3.0238)]),
]

HILLS = [
    dict(id="north-dunes", name="Dunes of Abaradjou", center=(16.7858, -3.0160), radius=430,
         blurb="Fixed dunes on the Sahara side, where the caravans from Arawan and Taoudenni came down to the town. Sand blows off them into the northern lanes every dry season."),
    dict(id="north-east-dunes", name="North-eastern dunes", center=(16.7850, -2.9945), radius=480, label=False,
         blurb="Long dune ridges running east–west, held by thorn trees and grass; herders' camps and wells in the hollows between them."),
    dict(id="west-dunes", name="Western dunes", center=(16.7765, -3.0205), radius=360,
         blurb="Dunes on the road west to Goundam and the lakes; cemeteries lie at their foot, outside the town."),
    dict(id="south-west-dune", name="Dune of the Kabara road", center=(16.7670, -3.0195), radius=330, label=False,
         blurb="A sand ridge above the flood plain on the south-west; the old track to the river ran along the higher ground to keep its feet dry in the flood."),
    dict(id="east-dunes", name="Eastern dunes", center=(16.7690, -2.9915), radius=360, label=False,
         blurb="Dunes toward the road east along the river to Bamba and Gao."),
    dict(id="south-east-dune", name="Sand ridge of the east road", center=(16.7628, -2.9960), radius=250, label=False,
         blurb="A low ridge between the flood plain and the town, grazed by goats and crossed by the track to the river villages."),
]

ROADS = [
    dict(id="kabara-road", name="Road to Kabara", path=[(16.7560, -3.0090), (16.7600, -3.0083), (16.7650, -3.0074), (16.7690, -3.0066), (16.7734, -3.0062)], width=14, style="major", labelled=True,
         blurb="The 8 km track to Kabara, Timbuktu's port on the Niger, where boats from Djenné and Gao unloaded grain, gold, kola and slaves. Donkeys and porters carried everything up; Tuareg raiders made the stretch through the dunes notorious.",
         periods=TOWN),
    dict(id="kabara-track", name="Track to the river", path=[(16.7560, -3.0090), (16.7600, -3.0083), (16.7650, -3.0074), (16.7700, -3.0068), (16.7745, -3.0066)], width=8, style="minor",
         blurb="A herders' track from the well down to the flood plain and the river, where the Tuareg summered with their herds.", periods=["founding-1100"]),
    dict(id="great-street", name="The street of the market", path=[(16.7734, -3.0062), (16.7760, -3.0061), (16.7792, -3.0060)], width=10, style="major", labelled=True,
         blurb="The town's spine from the market north past the Sidi Yahya quarter to Abaradjou, where the Saharan caravans unloaded: the Kabara road and the caravan road meeting in the middle of town.",
         periods=TOWN),
    dict(id="arawan-road", name="Caravan road to Arawan and Taoudenni", path=[(16.7792, -3.0060), (16.7830, -3.0058), (16.7860, -3.0055), (16.7890, -3.0052)], width=14, style="major", labelled=True,
         blurb="The track north into the Sahara: 250 km to the wells of Arawan, then twenty days more to the salt mines of Taghaza (until about 1585) and Taoudenni. The Azalai, the great salt caravan, came down it in winter.",
         periods=TOWN),
    dict(id="arawan-track", name="Track to Arawan", path=[(16.7765, -3.0066), (16.7830, -3.0060), (16.7890, -3.0052)], width=8, style="minor",
         blurb="The Tuareg herders' route north to the rainy-season pastures round Arawan.", periods=["founding-1100"]),
    dict(id="goundam-road", name="Road west to Goundam", path=[(16.7734, -3.0062), (16.7734, -3.0090), (16.7734, -3.0130), (16.7722, -3.0160), (16.7700, -3.0200), (16.7680, -3.0240)], width=12, style="major", labelled=True,
         blurb="West out of the Djinguereber quarter toward Goundam, the lakes and the Massina, skirting the western dunes.", periods=TOWN),
    dict(id="gao-road", name="Road east to Bamba and Gao", path=[(16.7734, -3.0062), (16.7734, -3.0030), (16.7732, -3.0000), (16.7724, -2.9960), (16.7705, -2.9870)], width=12, style="major", labelled=True,
         blurb="East along the river toward Bamba and Gao, the Songhai capital, 400 km away: the road of the Askias' governors and messengers.", periods=TOWN),
    dict(id="sankore-lane", name="Lane to Sankore", path=[(16.7764, -3.0061), (16.7766, -3.0048), (16.7764, -3.0028), (16.7760, -3.0010)], width=6, style="minor",
         blurb="The lane from the market street to the Sankore mosque and the scholars' houses of the northern quarter.", periods=FROM_1450),
    dict(id="djinguereber-lane", name="Lane of the Djinguereber", path=[(16.7734, -3.0090), (16.7722, -3.0090), (16.7716, -3.0085)], width=6, style="minor",
         blurb="The lane from the west road down to the great mosque's north door, crowded on Fridays.", periods=TOWN),
    dict(id="badjinde-lane", name="Lane of Badjindé", path=[(16.7734, -3.0030), (16.7715, -3.0018), (16.7695, -3.0012)], width=6, style="minor",
         blurb="Down from the east road into Badjindé and Bella Farandja.", periods=TOWN),
    dict(id="kasbah-lane", name="Lane to the Kasbah", path=[(16.7690, -3.0066), (16.7688, -3.0090)], width=6, style="minor",
         blurb="From the Kabara road to the gate of the Moroccans' kasbah.", periods=["pashalik-1700"]),
]

BLOCKS = [
    # ---- the camp, c. 1100
    dict(name="Huts round the well", polygon=[(16.7748, -3.0072), (16.7762, -3.0072), (16.7762, -3.0050), (16.7748, -3.0050)], density="loose", periods=["founding-1100"]),
    dict(name="Stores of the herders", polygon=[(16.7735, -3.0060), (16.7746, -3.0060), (16.7746, -3.0040), (16.7735, -3.0040)], density="loose", periods=["founding-1100"]),
    # ---- Mali, 1340
    dict(name="Djinguereber", polygon=[(16.7698, -3.0128), (16.7730, -3.0128), (16.7730, -3.0068), (16.7700, -3.0068)], density="dense", periods=["mali-1340"]),
    dict(name="Round the market", polygon=[(16.7716, -3.0057), (16.7731, -3.0057), (16.7731, -3.0024), (16.7716, -3.0024)], density="dense", periods=["mali-1340"]),
    dict(name="Badjindé", polygon=[(16.7690, -3.0058), (16.7712, -3.0058), (16.7712, -3.0040), (16.7690, -3.0052)], density="loose", periods=["mali-1340"]),
    dict(name="Sareikeina", polygon=[(16.7739, -3.0105), (16.7768, -3.0105), (16.7768, -3.0066), (16.7739, -3.0066)], density="loose", periods=["mali-1340"]),
    dict(name="Sankoré", polygon=[(16.7739, -3.0056), (16.7782, -3.0056), (16.7782, -3.0022), (16.7739, -3.0022)], density="loose", periods=["mali-1340"]),
    # ---- the town of 1450
    dict(name="Djinguereber", polygon=[(16.7694, -3.0134), (16.7730, -3.0134), (16.7730, -3.0068), (16.7696, -3.0068)], density="dense", periods=["songhai-1450"]),
    dict(name="Badjindé", polygon=[(16.7712, -3.0057), (16.7731, -3.0057), (16.7731, -3.0016), (16.7716, -3.0016)], density="dense", periods=["songhai-1450"]),
    dict(name="Badjindé south", polygon=[(16.7690, -3.0058), (16.7712, -3.0058), (16.7712, -3.0044), (16.7690, -3.0056)], density="dense", periods=["songhai-1450"]),
    dict(name="Sareikeina", polygon=[(16.7739, -3.0118), (16.7780, -3.0118), (16.7780, -3.0066), (16.7739, -3.0066)], density="dense", periods=["songhai-1450"]),
    dict(name="Sankoré", polygon=[(16.7739, -3.0056), (16.7790, -3.0056), (16.7790, -3.0012), (16.7739, -3.0012)], density="dense", periods=["songhai-1450"]),
    dict(name="Bella Farandja", polygon=[(16.7680, -3.0040), (16.7712, -3.0026), (16.7731, -3.0010), (16.7731, -2.9990), (16.7690, -2.9998)], density="loose", periods=["songhai-1450"]),
    dict(name="Abaradjou", polygon=[(16.7795, -3.0110), (16.7815, -3.0110), (16.7815, -3.0066), (16.7795, -3.0066)], density="loose", periods=["songhai-1450"]),
    # ---- the Askias' city, 1550: the largest extent
    dict(name="Djinguereber", polygon=[(16.7690, -3.0140), (16.7730, -3.0140), (16.7730, -3.0068), (16.7693, -3.0068)], density="dense", periods=["askia-1550"]),
    dict(name="Badjindé", polygon=[(16.7698, -3.0057), (16.7731, -3.0057), (16.7731, -3.0014), (16.7698, -3.0018)], density="dense", periods=["askia-1550"]),
    dict(name="Sareikeina", polygon=[(16.7739, -3.0135), (16.7790, -3.0135), (16.7790, -3.0066), (16.7739, -3.0066)], density="dense", periods=["askia-1550"]),
    dict(name="Sankoré", polygon=[(16.7739, -3.0056), (16.7798, -3.0056), (16.7798, -3.0004), (16.7739, -3.0004)], density="dense", periods=["askia-1550"]),
    dict(name="Bella Farandja", polygon=[(16.7676, -3.0058), (16.7695, -3.0058), (16.7697, -3.0012), (16.7731, -3.0008), (16.7731, -2.9978), (16.7680, -2.9985)], density="loose", periods=["askia-1550"]),
    dict(name="Abaradjou", polygon=[(16.7797, -3.0130), (16.7825, -3.0130), (16.7825, -3.0066), (16.7797, -3.0066)], density="loose", periods=["askia-1550"]),
    dict(name="Huts beyond Sankoré", polygon=[(16.7739, -2.9998), (16.7795, -2.9998), (16.7790, -2.9972), (16.7745, -2.9972)], density="loose", periods=["askia-1550"]),
    dict(name="Western huts", polygon=[(16.7700, -3.0172), (16.7728, -3.0160), (16.7728, -3.0145), (16.7692, -3.0145)], density="loose", periods=["askia-1550"]),
    # ---- the Pashalik, 1700: the same town, thinning at the edges
    dict(name="Djinguereber", polygon=[(16.7693, -3.0136), (16.7730, -3.0136), (16.7730, -3.0068), (16.7695, -3.0068)], density="dense", periods=["pashalik-1700"]),
    dict(name="Badjindé", polygon=[(16.7698, -3.0057), (16.7731, -3.0057), (16.7731, -3.0016), (16.7698, -3.0020)], density="dense", periods=["pashalik-1700"]),
    dict(name="Sareikeina", polygon=[(16.7739, -3.0118), (16.7782, -3.0118), (16.7782, -3.0066), (16.7739, -3.0066)], density="dense", periods=["pashalik-1700"]),
    dict(name="Sareikeina, the sanded edge", polygon=[(16.7739, -3.0132), (16.7788, -3.0132), (16.7788, -3.0121), (16.7739, -3.0121)], density="loose", periods=["pashalik-1700"]),
    dict(name="Sankoré", polygon=[(16.7739, -3.0056), (16.7792, -3.0056), (16.7792, -3.0008), (16.7739, -3.0008)], density="dense", periods=["pashalik-1700"]),
    dict(name="Bella Farandja", polygon=[(16.7692, -3.0040), (16.7697, -3.0014), (16.7731, -3.0010), (16.7731, -2.9982), (16.7688, -2.9990)], density="loose", periods=["pashalik-1700"]),
    dict(name="Abaradjou", polygon=[(16.7797, -3.0112), (16.7818, -3.0112), (16.7818, -3.0066), (16.7797, -3.0066)], density="loose", periods=["pashalik-1700"]),
]

GARDENS = [
    dict(name="Gardens by the pool", polygon=[(16.7650, -3.0142), (16.7668, -3.0138), (16.7668, -3.0118), (16.7648, -3.0118)], kind="orchard", periods=TOWN),
    dict(name="Flood fields (bourgou and rice)", polygon=[(16.7608, -3.0220), (16.7618, -3.0170), (16.7600, -3.0150), (16.7575, -3.0160), (16.7570, -3.0215)], kind="orchard", periods=["mali-1340", "songhai-1450", "askia-1550"]),
]

DISTRICTS = [
    dict(id="djinguereber-quarter", name="Djinguereber", polygon=[(16.7688, -3.0145), (16.7731, -3.0145), (16.7731, -3.0068), (16.7690, -3.0068)], periods=TOWN,
         description="The south-western quarter round the great mosque, the oldest part of the walled-in town; in Mali's time the seat of the governors, after 1591 the quarter of the Moroccan Arma round their kasbah. Boundaries approximate."),
    dict(id="sareikeina", name="Sareikeina", polygon=[(16.7738, -3.0140), (16.7792, -3.0140), (16.7792, -3.0066), (16.7738, -3.0066)], periods=TOWN,
         description="The western and central quarter behind the Sidi Yahya mosque, of merchants' and scholars' houses. The names and limits of Timbuktu's quarters shifted over time; this layout follows the usual modern one."),
    dict(id="sankore-quarter", name="Sankoré", polygon=[(16.7738, -3.0057), (16.7800, -3.0057), (16.7800, -3.0002), (16.7738, -3.0002)], periods=TOWN,
         description="The northern quarter of the Sankore mosque, home of the great scholarly families (the Aqit among them) and of the Saharan merchants nearest the caravan ground."),
    dict(id="badjinde", name="Badjindé", polygon=[(16.7695, -3.0058), (16.7732, -3.0058), (16.7732, -3.0012), (16.7697, -3.0016)], periods=TOWN,
         description="The low middle of the town round the market, named, it is usually said, after the pool the flood filled here."),
    dict(id="bella-farandja", name="Bella Farandja", polygon=[(16.7674, -3.0060), (16.7695, -3.0060), (16.7697, -3.0012), (16.7732, -3.0006), (16.7732, -2.9975), (16.7678, -2.9983)], periods=FROM_1450,
         description="The south-eastern edge of straw and mat huts, long associated with the Bella, the servile dependants of the Tuareg, and with newcomers from the river."),
    dict(id="abaradjou", name="Abaradjou", polygon=[(16.7796, -3.0130), (16.7830, -3.0130), (16.7830, -3.0000), (16.7796, -3.0000)], periods=TOWN,
         description="The northern edge where the Saharan caravans arrived: camel grounds, salt stores and the camps of the Tuareg and Arab caravan men."),
]

LABELS = [
    dict(text="Tin Buktu", position=(16.7782, -3.0095), size="lg", periods=["founding-1100"]),
    dict(text="Tunbuktu", position=(16.7820, -3.0175), size="lg", periods=TOWN),
    dict(text="Sahra", position=(16.7875, -3.0110), size="lg"),
    dict(text="Djinguereber", position=(16.7695, -3.0128), size="sm", periods=TOWN),
    dict(text="Sareikeina", position=(16.7785, -3.0100), size="sm", periods=TOWN),
    dict(text="Sankoré", position=(16.7793, -3.0020), size="sm", periods=TOWN),
    dict(text="Badjindé", position=(16.7718, -3.0022), size="sm", periods=TOWN),
    dict(text="Bella Farandja", position=(16.7684, -3.0002), size="sm", periods=FROM_1450),
    dict(text="Abaradjou", position=(16.7822, -3.0095), size="sm", periods=TOWN),
    dict(text="to Kabara and the Niger", position=(16.7578, -3.0050), size="md"),
    dict(text="to Arawan and Taoudenni", position=(16.7878, -3.0025), size="sm", rotation=-80),
    dict(text="to Gao", position=(16.7712, -2.9895), size="sm"),
    dict(text="to Goundam", position=(16.7698, -3.0225), size="sm"),
    dict(text="flood plain", position=(16.7590, -3.0185), size="sm"),
]
