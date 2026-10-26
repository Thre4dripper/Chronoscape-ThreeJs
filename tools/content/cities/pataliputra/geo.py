# Pataliputra / Patna: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.

MAGADHA, MAURYA, ASHOKA, GUPTA, SURI = "magadha-450", "maurya-300", "ashoka-250", "gupta-400", "sher-shah-1545"
ALL = [MAGADHA, MAURYA, ASHOKA, GUPTA, SURI]
ANCIENT = [MAGADHA, MAURYA, ASHOKA, GUPTA]
MAURYAN = [MAURYA, ASHOKA]
WALLED = [MAURYA, ASHOKA, GUPTA]

CITY = dict(
    name="Pataliputra", subtitle="Patna on the Ganges",
    description="The middle of the long riverside city of Pataliputra, capital of Magadha, the Mauryas and the Guptas, from the fort of Pataligama (5th century BCE) to Sher Shah Suri's refounded Patna (1541): Kumhrar, Bulandi Bagh, Gulzarbagh and Patna City between the Ganges and the old beds of the Son. Megasthenes' city ran on for kilometres beyond both edges. Positions are projected from real coordinates; the ancient plan is a reconstruction and the drawing is an illustration, not a survey.",
    defaultPeriodId=MAURYA,
    world=dict(heightScale=1.0, walls=["#C9A47A", "#B8936A", "#D6BC94", "#A98260", "#CDB48E"], roofs=["#9C7A55", "#B39A5E", "#8C6A4A"]),
    camera=dict(target=(25.5995, 85.1975), distance=40),
)
FRAME = ((25.6300, 85.1700), (25.5760, 85.2445))

PALETTE = dict(parchment="#E7D4AA", ink="#6C4A31", water="#6A8B86", hill="#7A7E5A", road="#8B6A49")
COMPASS = (25.6255, 85.2390)
CARTOUCHE = (25.5768, 85.1712)

SOURCES = [
    dict(id="megasthenes", title="Ancient India as Described by Megasthenes and Arrian", author="J. W. McCrindle (trans.)", year=1877, url="https://en.wikipedia.org/wiki/Indica_(Megasthenes)"),
    dict(id="faxian", title="A Record of Buddhistic Kingdoms (Faxian's Foguoji)", author="Faxian, trans. James Legge", year=1886, url="https://en.wikipedia.org/wiki/Faxian"),
    dict(id="waddell", title="Report on the Excavations at Pataliputra (Patna), the Palibothra of the Greeks", author="L. A. Waddell", year=1903),
    dict(id="spooner", title="Mr. Ratan Tata's Excavations at Pataliputra (Archaeological Survey of India Annual Report 1912–13)", author="D. B. Spooner", year=1915),
    dict(id="altekar-mishra", title="Report on Kumrahar Excavations, 1951–1955", author="A. S. Altekar & Vijayakanta Mishra", year=1959),
    dict(id="thapar-ashoka", title="Aśoka and the Decline of the Mauryas", author="Romila Thapar", year=1961),
    dict(id="arthashastra", title="The Kautilya Arthashastra", author="R. P. Kangle (trans.)", year="1960–65", url="https://en.wikipedia.org/wiki/Arthashastra"),
    dict(id="wiki-pataliputra", title="Pataliputra", author="Wikipedia", url="https://en.wikipedia.org/wiki/Pataliputra"),
    dict(id="wiki-patna", title="Patna", author="Wikipedia", url="https://en.wikipedia.org/wiki/Patna"),
    dict(id="wiki-ganges", title="Ganges", author="Wikipedia", url="https://en.wikipedia.org/wiki/Ganges"),
    dict(id="wiki-son", title="Sone River", author="Wikipedia", url="https://en.wikipedia.org/wiki/Sone_River"),
    dict(id="wiki-punpun", title="Punpun River", author="Wikipedia", url="https://en.wikipedia.org/wiki/Punpun_River"),
]

PERIODS = [
    dict(id=MAGADHA, label="Pataligama, the new capital of Magadha", year=-450, startYear=-490, endYear=-322,
         summary="Ajatashatru's ministers Sunidha and Vassakara fortify the village of Pataligama at the Son–Ganges confluence against the Licchavis across the river (traditionally c. 490 BCE; the date is much disputed). His son Udayin moves the Magadhan capital here from Rajagriha. Under the Shishunagas and the Nandas it grows into a river town of timber, thatch and mud brick inside earth ramparts.",
         population="unknown; a few tens of thousands at most",
         feel="Carpenters' adzes and rammed earth on the new rampart, ferries crossing toward Vaishali, smoke from potters' kilns firing black polished bowls.",
         style="courtyard",
         houses=dict(title="Timber and mud houses of Pataligama", text="Low houses of mud brick and wattle on timber frames, thatched or tiled, round small yards with a well or a soak pit of stacked pottery rings. Lanes are of beaten earth; potters, smiths and boatmen live by their trades."),
         outskirts=dict(title="Rice fields and hamlets", text="Paddy, barley and sugarcane on the flood-silt, mango groves, hamlets of thatched huts on raised ground, cattle pens and threshing floors beside the old channels of the Son.")),
    dict(id=MAURYA, label="Pataliputra · Mauryan capital", year=-300, startYear=-321, endYear=-269,
         summary="Chandragupta Maurya, advised by Kautilya, takes the Nanda throne (c. 321 BCE) and rules most of northern India from here. Megasthenes, envoy of Seleucus, describes a parallelogram about 80 by 15 stadia along the river, ringed by a timber palisade with 570 towers and 64 gates and a broad moat. The palace stands in parks; houses are of timber.",
         population="perhaps 150,000–400,000 (modern guesses; Megasthenes gives no figure)",
         feel="War elephants swaying through the gates, carts of grain at the river stairs, the call of the market inspectors, and incense and dust at the palace audiences.",
         style="courtyard",
         houses=dict(title="Timber houses of the Mauryan city", text="Megasthenes says that cities by rivers were built of wood, because brick would not survive the floods. Houses of two or three storeys of timber and mud on brick footings, with balconies and tiled or thatched roofs, crowd the lanes between the royal roads."),
         outskirts=dict(title="Gardens and suburbs outside the moat", text="Royal parks and pleasure gardens, orchards, workshops and cremation grounds outside the moat, and villages in the rice fields toward the Son and the road to Rajagriha.")),
    dict(id=ASHOKA, label="Ashoka's Pataliputra", year=-250, startYear=-268, endYear=-185,
         summary="Ashoka, crowned c. 268 BCE, turns to the Buddha's teaching after the Kalinga war. Polished sandstone pillars from Chunar are raised across the empire; at Pataliputra the 80-pillared hall at Kumhrar (its date is argued) and stupas rise, and the Third Buddhist Council meets c. 250 BCE. The dynasty weakens after his death (c. 232) and ends in 185 BCE.",
         population="perhaps the largest city in the world at the time (modern estimates, uncertain)",
         feel="The grinding hiss of stone polishers, monks' chanting at the monasteries, edicts read aloud in the squares, and the royal elephants at the river.",
         style="courtyard",
         houses=dict(title="Timber and brick houses of Ashoka's city", text="Still mostly timber on brick footings, but burnt brick now walls the richer houses and the monasteries. Courtyards with wells of terracotta rings, tiled roofs, and verandas on carved posts line the lanes."),
         outskirts=dict(title="Monasteries and groves", text="Monastery compounds with brick cells round courts, stupas among mango groves, the royal parks, and villages of thatched huts along the roads south and east.")),
    dict(id=GUPTA, label="Kusumapura of the Guptas", year=405, startYear=320, endYear=550,
         summary="The Guptas rise in Magadha from c. 320 CE, though their court soon moves among other cities. Faxian, who stays here c. 405–408 to copy the Vinaya, finds a rich city with Ashoka's stone palace 'built by spirits', two great monasteries, wheeled processions of images, and free hospitals. Aryabhata works at Kusumapura (499).",
         population="unknown; still a large city in Faxian's day",
         feel="Bells and drums on the image cars in the spring procession, the smell of medicinal oils at the hospital, Sanskrit verses recited in the school courtyards.",
         style="courtyard",
         houses=dict(title="Brick houses of the Gupta city", text="Houses of burnt brick round courts, plastered and painted, one or two storeys with flat or tiled roofs; timber balconies over the lanes. Terracotta drains and ring-wells serve each block."),
         outskirts=dict(title="Ruined ramparts and monasteries", text="The old timber palisade has rotted into an earth bank; outside it lie monasteries, gardens, tanks and villages, and the silted moat is a chain of ponds.")),
    dict(id=SURI, label="Sher Shah's Patna", year=1545, startYear=1541, endYear=1704,
         summary="Pataliputra had shrunk to villages by Xuanzang's time (c. 637). In 1541 Sher Shah Suri, an Afghan from Bihar who had driven out Humayun, builds a fort on the Ganges and moves the provincial seat here from Bihar Sharif; his mosque follows (c. 1545). Under the Mughals Patna becomes the capital of Bihar Subah, a great river port for saltpetre, cloth and grain.",
         population="perhaps 200,000 by the late 17th century (travellers' guesses)",
         feel="Boats packed along the ghats, saltpetre and indigo bales, the azan from Sher Shah's mosque, and the bazaar of Patna City loud with Persian, Bhojpuri and Bengali.",
         style="courtyard",
         houses=dict(title="Courtyard houses of Patna City", text="Brick and mud houses of one or two storeys round courts, with flat roofs and parapets; merchants' havelis with carved wooden doors and balconies. Ralph Fitch (1586) found most houses of earth and straw, the streets broad."),
         outskirts=dict(title="Villages over the ruins", text="Mud-walled villages, mango groves and fields over the buried city: Kumhrar, Bulandi Bagh and Gulzarbagh are hamlets whose wells and ploughs turn up old bricks and beams.")),
]

# ---------------------------------------------------------------- water

GANGA = [(25.6226, 85.1650), (25.6213, 85.1850), (25.6191, 85.2000), (25.6156, 85.2150), (25.6111, 85.2300), (25.6071, 85.2450), (25.6060, 85.2500)]

SON_OLD = [(25.5845, 85.1650), (25.5822, 85.1760), (25.5812, 85.1900), (25.5806, 85.2050), (25.5810, 85.2200), (25.5820, 85.2350), (25.5835, 85.2500)]

MOAT_S = [(25.5855, 85.1650), (25.5856, 85.1850), (25.5853, 85.2000), (25.5856, 85.2250), (25.5860, 85.2500)]

WATER = [
    dict(id="ganga", name="Ganges (Ganga)", path=GANGA, width=1800,
         blurb="The Ganges here is broad and braided, more than a kilometre wide in the monsoon, with shifting sandbanks (diara). Across it lay the Licchavi country of Vaishali and the mouth of the Gandak. The city's ghats, boatyards and harbour lined this bank; Megasthenes calls the river the greatest in India."),
    dict(id="son-old", name="Old bed of the Son (Erannoboas)", path=SON_OLD, width=220, periods=[MAGADHA, MAURYA, ASHOKA],
         blurb="Megasthenes places the city where the Erannoboas, the Son, meets the Ganges. The Son has since moved west to join the Ganges near Maner; the line drawn here follows one reconstruction of an old bed south of the city, and is uncertain."),
    dict(id="son-silted", name="Silting channel of the Son", path=SON_OLD, width=110, periods=[GUPTA],
         blurb="By Gupta times the Son's old channel south of the city was probably shrinking as the river shifted west; its course and date are uncertain."),
    dict(id="punpun-nala", name="Punpun backwater (later the Badshahi Nala)", path=SON_OLD, width=45, periods=[SURI],
         blurb="By the 16th century the old Son bed south of the city was a seasonal drain and backwater, fed in the rains by the Punpun; the Mughals called its line the Badshahi Nala."),
    dict(id="moat-south", name="The moat", path=MOAT_S, width=90, periods=MAURYAN,
         blurb="Megasthenes (in Arrian) says a ditch ran outside the palisade, 600 feet wide and 30 cubits deep, for defence and to take the city's sewage. Its line here is a reconstruction; the width is drawn smaller than his figure."),
]

ISLANDS = [
    dict(name="Diara sandbank", polygon=[(25.6185, 85.1760), (25.6215, 85.1740), (25.6232, 85.1820), (25.6222, 85.1960), (25.6200, 85.1990), (25.6188, 85.1880)]),
    dict(name="Diara sandbank", polygon=[(25.6118, 85.2190), (25.6140, 85.2170), (25.6150, 85.2260), (25.6125, 85.2370), (25.6105, 85.2385), (25.6108, 85.2290)]),
]

# ---------------------------------------------------------------- walls, gates, roads

PAL_N = [(25.6075, 85.1700), (25.6062, 85.1850), (25.6050, 85.2000), (25.6040, 85.2150), (25.6005, 85.2320), (25.5980, 85.2445)]
PAL_S = [(25.5870, 85.1700), (25.5866, 85.1850), (25.5864, 85.2000), (25.5867, 85.2250), (25.5872, 85.2445)]
UDAYIN = [(25.6052, 85.1880), (25.6040, 85.2150), (25.5990, 85.2215), (25.5925, 85.2180), (25.5918, 85.1990), (25.5945, 85.1880), (25.6052, 85.1880)]
SURI_FORT = [(25.5986, 85.2349), (25.5986, 85.2381), (25.5964, 85.2381), (25.5964, 85.2349), (25.5986, 85.2349)]

WALLS = [
    dict(id="udayin-rampart", name="Rampart of the early city", path=UDAYIN, closed=True, periods=[MAGADHA],
         blurb="An earth rampart with a timber stockade round the first capital, grown from Ajatashatru's fort at Pataligama. Nothing of it has been securely identified; its line here is a guess sized to a town of the Nanda age."),
    dict(id="palisade-north", name="Timber palisade (river side)", path=PAL_N, periods=MAURYAN,
         blurb="Megasthenes: a wooden wall pierced with loopholes for archers, with 570 towers and 64 gates. Lines of sal posts found at Bulandi Bagh and elsewhere since 1903 are taken to be part of it; whether they belong to the outer circuit or an inner line is debated."),
    dict(id="palisade-south", name="Timber palisade (land side)", path=PAL_S, periods=MAURYAN,
         blurb="The palisade on the landward side, with the moat outside. Its trace is a reconstruction: Megasthenes' parallelogram ran some 14 km along the river, far beyond both edges of this map."),
    dict(id="rampart-north", name="Old rampart (river side)", path=PAL_N, periods=[GUPTA],
         blurb="By Faxian's time the Mauryan timber had long rotted or burned; an earth bank and brick repairs probably marked the old line. What defences the Gupta city had is not known."),
    dict(id="rampart-south", name="Old rampart (land side)", path=PAL_S, periods=[GUPTA],
         blurb="The landward line of the old city, an earth bank above the silting moat (reconstruction)."),
    dict(id="sher-shah-fort", name="Sher Shah's fort", path=SURI_FORT, closed=True, periods=[SURI],
         blurb="The fort Sher Shah built on the Ganges in 1541, when he judged Patna the place for a great city. Its walls stood into the 19th century; the Qila House (Jalan Museum) stands on part of the site. The outline here is schematic."),
]

GATES = [
    dict(id="gate-rajagriha", name="South gate (road to Rajagriha)", position=(25.5864, 85.2050), periods=WALLED),
    dict(id="gate-sw", name="South-west gate", position=(25.5867, 85.1780), periods=WALLED),
    dict(id="gate-se", name="South-east gate", position=(25.5867, 85.2350), periods=WALLED),
    dict(id="gate-river-w", name="River gate", position=(25.6057, 85.1920), periods=WALLED),
    dict(id="gate-harbour", name="Harbour gate", position=(25.6048, 85.2050), periods=WALLED),
    dict(id="gate-river-e", name="River gate", position=(25.6040, 85.2200), periods=WALLED),
    dict(id="gate-pataligama", name="Gotama's Gate", position=(25.6045, 85.2050), periods=[MAGADHA]),
    dict(id="gate-udayin-s", name="South gate", position=(25.5921, 85.2050), periods=[MAGADHA]),
    dict(id="fort-gate", name="Fort gate", position=(25.5964, 85.2365), periods=[SURI]),
]

ROADS = [
    # the ancient royal road and its cross-streets
    dict(id="royal-road", name="Rajapatha (the royal road)", path=[(25.5962, 85.1700), (25.5960, 85.1850), (25.5958, 85.2000), (25.5955, 85.2150), (25.5952, 85.2300), (25.5950, 85.2445)], width=28, style="major", labelled=True, periods=WALLED,
         blurb="The main street along the length of the city. Megasthenes describes a royal road running north-west to the frontier, with a pillar every ten stadia; inside the walls it is the axis of the city. Its line here is a reconstruction."),
    dict(id="street-kumhrar", name="Street of the palace", path=[(25.6066, 85.1780), (25.6000, 85.1780), (25.5960, 85.1780), (25.5867, 85.1780)], width=16, style="minor", labelled=False, periods=WALLED),
    dict(id="street-bulandi", name="River street", path=[(25.6057, 85.1920), (25.5960, 85.1920), (25.5866, 85.1920)], width=14, style="minor", periods=WALLED),
    dict(id="street-harbour", name="Street of the harbour", path=[(25.6085, 85.2050), (25.6048, 85.2050), (25.5958, 85.2050), (25.5864, 85.2050)], width=20, style="major", labelled=False, periods=WALLED),
    dict(id="street-east", name="East street", path=[(25.6040, 85.2200), (25.5954, 85.2200), (25.5867, 85.2200)], width=14, style="minor", periods=WALLED),
    dict(id="street-se", name="South-east street", path=[(25.6005, 85.2350), (25.5951, 85.2350), (25.5867, 85.2350)], width=12, style="minor", periods=WALLED),
    dict(id="road-rajagriha", name="Road to Rajagriha and Gaya", path=[(25.5864, 85.2050), (25.5820, 85.2055), (25.5790, 85.2060), (25.5760, 85.2070)], width=18, style="major", labelled=True, periods=ANCIENT,
         blurb="South across the Son's old bed to Rajagriha, the older Magadhan capital in its ring of hills, and to Bodh Gaya. A ford or ferry crossed the channel; the line is schematic."),
    dict(id="road-champa", name="Road east to Champa", path=[(25.5950, 85.2445), (25.5945, 85.2500)], width=16, style="major", periods=WALLED),
    # the early town
    dict(id="pataligama-street", name="Main street of Pataligama", path=[(25.5935, 85.1880), (25.5962, 85.1960), (25.5965, 85.2050), (25.5975, 85.2150), (25.5990, 85.2215)], width=12, style="major", labelled=False, periods=[MAGADHA]),
    dict(id="pataligama-ford", name="Lane to Gotama's Ford", path=[(25.6085, 85.2050), (25.6045, 85.2050), (25.5965, 85.2050), (25.5921, 85.2050)], width=10, style="minor", periods=[MAGADHA],
         blurb="The Buddhist texts say the gate by which the Buddha left the new fort was named Gotama's Gate, and the ferry place where he crossed the Ganges Gotama's Ford."),
    # Sher Shah's Patna
    dict(id="river-road", name="Highway along the Ganges", path=[(25.6012, 85.1700), (25.6000, 85.1900), (25.5985, 85.2050), (25.5965, 85.2150), (25.5952, 85.2250), (25.5946, 85.2350), (25.5944, 85.2445)], width=18, style="major", labelled=True, periods=[SURI],
         blurb="The road along the south bank, west to Danapur and the Son ferries and east through Patna City toward Bengal; the later Ashok Rajpath follows much of it."),
    dict(id="chowk-road", name="Road to Gaya from the Chowk", path=[(25.5946, 85.2290), (25.5900, 85.2280), (25.5840, 85.2270), (25.5760, 85.2255)], width=12, style="minor", labelled=True, periods=[SURI]),
    dict(id="gulzarbagh-lane", name="Lane to the landing", path=[(25.5985, 85.2050), (25.6060, 85.2050), (25.6085, 85.2050)], width=8, style="minor", periods=[SURI]),
    dict(id="kumhrar-lane", name="Village lane to Kumhrar", path=[(25.6000, 85.1900), (25.5960, 85.1890), (25.5900, 85.1870), (25.5840, 85.1860)], width=6, style="minor", periods=[SURI]),
]

# ---------------------------------------------------------------- built-up areas

def _q(s, n, w, e):
    return [(n, w), (n, e), (s, e), (s, w)]

# Mauryan city: cells between the royal road (25.596) and the cross-streets (85.178, 85.192, 85.205, 85.220, 85.235)
NW1 = [(25.6070, 85.1705), (25.6066, 85.1772), (25.5967, 85.1772), (25.5967, 85.1705)]
NW2 = _q(25.5967, 25.6050, 85.1890, 85.1912)
NW3 = [(25.6045, 85.1928), (25.6040, 85.2042), (25.5966, 85.2042), (25.5966, 85.1928)]
NW4 = [(25.6040, 85.2058), (25.6034, 85.2192), (25.5962, 85.2192), (25.5962, 85.2058)]
NW5 = [(25.6030, 85.2208), (25.6006, 85.2342), (25.5958, 85.2342), (25.5958, 85.2208)]
NW6 = [(25.6000, 85.2358), (25.5982, 85.2440), (25.5956, 85.2440), (25.5956, 85.2358)]
SW1 = _q(25.5875, 25.5952, 85.1705, 85.1772)
SW2 = _q(25.5875, 25.5952, 85.1788, 85.1912)
SW3 = _q(25.5875, 25.5952, 85.1928, 85.2042)
SW4 = _q(25.5874, 25.5950, 85.2058, 85.2192)
SW5 = _q(25.5876, 25.5946, 85.2208, 85.2342)
SW6 = _q(25.5878, 25.5942, 85.2358, 85.2440)
PALACE_Q = _q(25.5967, 25.6060, 85.1788, 85.1885)

BLOCKS = [
    # early town
    dict(name="Pataligama by the river", polygon=_q(25.5975, 25.6035, 85.1900, 85.2040), density="dense", periods=[MAGADHA]),
    dict(name="Potters' and smiths' quarter", polygon=_q(25.5975, 25.6025, 85.2060, 85.2120), density="dense", periods=[MAGADHA]),
    dict(name="Lanes of the early city", polygon=_q(25.5930, 25.5955, 85.1950, 85.2040), density="dense", periods=[MAGADHA]),
    dict(name="Lanes of the early city", polygon=_q(25.5932, 25.5985, 85.2060, 85.2170), density="loose", periods=[MAGADHA]),
    dict(name="Hamlet west of the rampart", polygon=_q(25.5960, 25.6020, 85.1760, 85.1860), density="loose", periods=[MAGADHA]),
    dict(name="Hamlet east of the rampart", polygon=_q(25.5950, 25.6000, 85.2260, 85.2350), density="loose", periods=[MAGADHA]),
    # the Mauryan and Gupta city
    dict(name="West quarter", polygon=NW1, density="dense", periods=WALLED),
    dict(name="Lanes by the palace", polygon=NW2, density="loose", periods=WALLED),
    dict(name="Courtiers' houses", polygon=_q(25.5967, 25.6015, 85.1788, 85.1830), density="loose", periods=WALLED),
    dict(name="Bulandi Bagh quarter", polygon=NW3, density="dense", periods=WALLED),
    dict(name="Harbour quarter", polygon=NW4, density="dense", periods=WALLED),
    dict(name="East river quarter", polygon=NW5, density="dense", periods=WALLED),
    dict(name="East end", polygon=NW6, density="dense", periods=MAURYAN),
    dict(name="East end", polygon=NW6, density="loose", periods=[GUPTA]),
    dict(name="South-west quarter", polygon=SW1, density="dense", periods=MAURYAN),
    dict(name="South-west quarter", polygon=SW1, density="loose", periods=[GUPTA]),
    dict(name="Quarter south of the palace", polygon=SW2, density="dense", periods=WALLED),
    dict(name="Quarter of the stupa", polygon=SW3, density="loose", periods=[ASHOKA, GUPTA]),
    dict(name="Quarter of the wells", polygon=SW3, density="dense", periods=[MAURYA]),
    dict(name="South gate quarter", polygon=SW4, density="loose", periods=[ASHOKA, GUPTA]),
    dict(name="South gate quarter", polygon=SW4, density="dense", periods=[MAURYA]),
    dict(name="South-east quarter", polygon=SW5, density="dense", periods=WALLED),
    dict(name="South-east quarter", polygon=SW6, density="dense", periods=MAURYAN),
    dict(name="South-east quarter", polygon=SW6, density="loose", periods=[GUPTA]),
    dict(name="Villages beyond the Son", polygon=_q(25.5764, 25.5795, 85.1800, 85.2000), density="loose", periods=ANCIENT),
    dict(name="Villages beyond the Son", polygon=_q(25.5764, 25.5795, 85.2120, 85.2350), density="loose", periods=ANCIENT),
    # Sher Shah's Patna
    dict(name="Patna City, west of the Chowk", polygon=[(25.5992, 85.2170), (25.5975, 85.2280), (25.5958, 85.2280), (25.5962, 85.2170)], density="dense", periods=[SURI]),
    dict(name="Patna City, west of the Chowk", polygon=_q(25.5900, 25.5942, 85.2160, 85.2272), density="dense", periods=[SURI]),
    dict(name="Patna City by Harmandir", polygon=[(25.5978, 85.2296), (25.5975, 85.2340), (25.5953, 85.2340), (25.5955, 85.2296)], density="dense", periods=[SURI]),
    dict(name="Patna City, east", polygon=_q(25.5885, 25.5940, 85.2290, 85.2370), density="dense", periods=[SURI]),
    dict(name="Patna City, east", polygon=_q(25.5885, 25.5918, 85.2395, 85.2440), density="dense", periods=[SURI]),
    dict(name="Mughal suburb by the river", polygon=[(25.6010, 85.2390), (25.5990, 85.2440), (25.5952, 85.2440), (25.5955, 85.2390)], density="loose", periods=[SURI]),
    dict(name="Gulzarbagh", polygon=_q(25.5990, 25.6040, 85.2010, 85.2130), density="loose", periods=[SURI]),
    dict(name="Mahendru and the ghats", polygon=_q(25.5975, 25.6045, 85.2140, 85.2160), density="loose", periods=[SURI]),
    dict(name="Village of Kumhrar", polygon=_q(25.5930, 25.5975, 85.1800, 85.1870), density="loose", periods=[SURI]),
    dict(name="Bulandi Bagh hamlet", polygon=_q(25.6005, 25.6040, 85.1920, 85.1990), density="loose", periods=[SURI]),
    dict(name="Village by the old wells", polygon=_q(25.5900, 25.5955, 85.1960, 85.2040), density="loose", periods=[SURI]),
    dict(name="Hamlets on the river road", polygon=_q(25.6015, 25.6060, 85.1720, 85.1840), density="loose", periods=[SURI]),
]

GARDENS = [
    dict(name="Royal park", polygon=_q(25.6045, 25.6060, 85.1790, 85.1885), kind="park", periods=MAURYAN),
    dict(name="Palace grove", polygon=_q(25.5967, 25.6008, 85.1855, 85.1885), kind="orchard", periods=WALLED),
    dict(name="Mango groves outside the rampart", polygon=_q(25.5880, 25.5940, 85.1720, 85.1860), kind="orchard", periods=[MAGADHA]),
    dict(name="Fields south of the early city", polygon=_q(25.5865, 25.5910, 85.1900, 85.2300), kind="orchard", periods=[MAGADHA]),
    dict(name="Rice fields beyond the Son", polygon=_q(25.5764, 25.5795, 85.1710, 85.1790), kind="orchard", periods=ANCIENT),
    dict(name="Rice fields beyond the Son", polygon=_q(25.5764, 25.5795, 85.2010, 85.2110), kind="orchard", periods=ANCIENT),
    dict(name="Mango groves over the old city", polygon=_q(25.5880, 25.5960, 85.1720, 85.1790), kind="orchard", periods=[SURI]),
    dict(name="Fields over the old city", polygon=_q(25.5880, 25.5925, 85.1880, 85.1950), kind="orchard", periods=[SURI]),
    dict(name="Fields over the old city", polygon=_q(25.5880, 25.5935, 85.2050, 85.2150), kind="orchard", periods=[SURI]),
    dict(name="Fields toward the Punpun", polygon=_q(25.5764, 25.5800, 85.1720, 85.2200), kind="orchard", periods=[SURI]),
    dict(name="Fields toward the Punpun", polygon=_q(25.5830, 25.5870, 85.1720, 85.2200), kind="orchard", periods=[SURI]),
]

MARSH = [
    dict(name="Silted moat", polygon=_q(25.5849, 25.5861, 85.1710, 85.2440), periods=[GUPTA]),
    dict(name="Low ground of the old moat", polygon=_q(25.5850, 25.5862, 85.1710, 85.2150), periods=[SURI]),
    dict(name="Jheels on the old Son bed", polygon=_q(25.5824, 25.5836, 85.1720, 85.2000), periods=[GUPTA, SURI]),
    dict(name="Waterlogged ground by the Son", polygon=_q(25.5828, 25.5845, 85.2100, 85.2440), periods=[MAGADHA]),
    dict(name="Riverside flats", polygon=[(25.6100, 85.1710), (25.6098, 85.1800), (25.6088, 85.1800), (25.6090, 85.1710)]),
]

DISTRICTS = [
    dict(id="pataligama", name="Pataligama", polygon=UDAYIN[:-1], periods=[MAGADHA],
         description="The fortified village at the confluence that Ajatashatru's ministers built against the Licchavis, and the capital it became under Udayin, the Shishunagas and the Nandas."),
    dict(id="royal-quarter", name="The royal quarter (Kumhrar)", polygon=PALACE_Q, periods=WALLED,
         description="Where the Mauryan palace and the pillared hall stood among parks and fishponds, by the usual reading of the Kumhrar excavations. In Faxian's day the old palace still stood and a monastery hospital worked nearby."),
    dict(id="bulandi-bagh", name="Bulandi Bagh", polygon=NW3, periods=WALLED,
         description="The quarter by the river where Waddell (1903) and Spooner (1912–15) found long rows of sal-wood posts: the timber palisade of the Mauryan city, preserved in wet clay."),
    dict(id="patna-city", name="Patna City", polygon=[(25.5992, 85.2160), (25.5980, 85.2445), (25.5885, 85.2445), (25.5885, 85.2160)], periods=[SURI],
         description="Sher Shah's new town round his fort on the river, which the Mughals made the capital of Bihar: the Chowk, the bazaars, mosques, the Harmandir and the merchants' ghats."),
]

LABELS = [
    dict(text="Ganga", position=(25.6235, 85.2080), size="lg", rotation=8),
    dict(text="Diara", position=(25.6210, 85.1860), size="sm", rotation=4),
    dict(text="Son (old bed)", position=(25.5794, 85.1830), size="sm", rotation=2, periods=[MAGADHA, MAURYA, ASHOKA]),
    dict(text="Badshahi Nala", position=(25.5797, 85.2150), size="sm", periods=[SURI]),
    dict(text="To Vaishali, across the river", position=(25.6170, 85.2380), size="sm", rotation=10),
    dict(text="To Rajagriha and Gaya", position=(25.5778, 85.2120), size="sm", periods=ANCIENT),
    dict(text="To Gaya", position=(25.5778, 85.2290), size="sm", periods=[SURI]),
    dict(text="Royal road west, to Taxila", position=(25.5970, 85.1740), size="sm", periods=MAURYAN),
    dict(text="To Champa", position=(25.5935, 85.2410), size="sm", periods=WALLED),
    dict(text="Pataligama", position=(25.5985, 85.2080), size="md", periods=[MAGADHA]),
    dict(text="Palibothra", position=(25.5905, 85.1980), size="lg", periods=[MAURYA]),
    dict(text="Pataliputra", position=(25.5905, 85.1980), size="lg", periods=[ASHOKA]),
    dict(text="Kusumapura", position=(25.5905, 85.1980), size="lg", periods=[GUPTA]),
    dict(text="Kumhrar", position=(25.5948, 85.1835), size="sm", periods=[SURI]),
    dict(text="Gulzarbagh", position=(25.6045, 85.2090), size="sm", periods=[SURI]),
    dict(text="Patna", position=(25.5900, 85.2310), size="lg", periods=[SURI]),
]
