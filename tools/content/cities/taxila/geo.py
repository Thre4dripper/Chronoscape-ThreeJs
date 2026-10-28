# Taxila (Takshashila): the three successive cities of the Taxila valley -- the Bhir Mound, Sirkap on the Hathial spur
# and Sirsukh -- with the Dharmarajika stupa, the Jandial temple, the Kunala stupa and the Mohra Moradu monastery,
# from the Persian satrapy to the ruins Xuanzang saw (see tools/content/cities/FORMAT.md).
ALL = ["achaemenid-450", "maurya-300", "indo-greek-50", "kushan-200", "huna-500"]
BHIR = ["achaemenid-450", "maurya-300"]
SIRKAP = ["indo-greek-50", "kushan-200"]
SIRSUKH = ["kushan-200", "huna-500"]
LATE = ["indo-greek-50", "kushan-200", "huna-500"]
BUDDHIST = ["maurya-300", "indo-greek-50", "kushan-200", "huna-500"]

CITY = dict(
    name="Taxila", subtitle="Takshashila, the gateway city",
    description="The Taxila valley from the Persian satrapy of the 5th century BCE to the ruins Xuanzang found in the 630s CE: the Bhir Mound city by the Tamra Nala, Sirkap, the Greek grid city on the Hathial spur, the Kushan city of Sirsukh to the north-east, and the Buddhist stupas and monasteries round them. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="maurya-300",
    world=dict(heightScale=1.0, walls=["#CDBB9C", "#C2AE8C", "#D6C7AA", "#B9A27F", "#CBB491"], roofs=["#A99070", "#9C8463", "#B39C79"]),
    camera=dict(target=(33.7495, 72.8285), distance=36),
)
FRAME = ((33.7790, 72.8150), (33.7385, 72.8635))
RESOLUTION = 4096
PALETTE = dict(parchment="#E8D6AE", ink="#6B4B33", water="#62878A", hill="#7C7C58", road="#8C6B4A")
COMPASS = (33.7768, 72.8605)
CARTOUCHE = (33.7398, 72.8500)

PERIODS = [
    dict(id="achaemenid-450", label="Takshashila of the satraps", year=-450, startYear=-520, endYear=-327,
         summary="Takshashila on the Bhir Mound, a town of Gandhara, which Darius I made part of the Persian empire about 518 BCE. Rubble-stone houses crowd crooked lanes on a low mound by the Tamra Nala; an older settlement lies on the Hathial ridge nearby. Later Indian tradition makes the town a place where teachers took pupils in grammar, law and medicine; how early that began is uncertain.",
         population="unknown; perhaps a few thousand",
         feel="Smoke from dung fires, bullock carts creaking in from the passes, a teacher's voice reciting verses for his pupils to repeat.",
         style="courtyard",
         houses=dict(title="Rubble houses of the Bhir Mound", text="Small houses of undressed stone set in mud, plastered inside, with flat roofs of timber and clay; rooms round a little yard with a hearth, storage jars and a soak-pit. They lean on one another along lanes that twist with the old property lines."),
         outskirts=dict(title="Fields and cattle pens", text="Wheat and barley fields on the valley floor, cattle pens and threshing floors, a few farmsteads of rubble and mud on the slopes of the Hathial ridge.")),
    dict(id="maurya-300", label="The gateway city", year=-300, startYear=-326, endYear=-181,
         summary="The Bhir Mound city at its largest. In 326 BCE its king Ambhi (Taxiles) welcomed Alexander; within twenty years Chandragupta Maurya held the Punjab and Taxila became the seat of a northern viceroy. Buddhist legend sends the young Ashoka here to put down a revolt. Rubble houses line twisting streets, with wells and soak-pits in the yards; the Dharmarajika stupa is begun, probably under Ashoka.",
         population="unknown; perhaps 10,000–20,000",
         feel="Caravans from Bactria unloading by the gate, horse traders shouting prices, pupils chanting grammar rules under a teacher's roof, kites over the market.",
         style="courtyard",
         houses=dict(title="Houses on the Bhir Mound", text="Houses of rubble stone in mud mortar, often two storeys, the walls once plastered and painted; rooms open onto a small court with a well or soak-pit of stacked pots. Shops of one room face the streets, which bend and narrow at random."),
         outskirts=dict(title="Fields, groves and caravan grounds", text="Irrigated fields and mango groves along the Tamra Nala, open ground where caravans camp, potters' kilns and brick clamps, and the first Buddhist shrine on the rise to the east.")),
    dict(id="indo-greek-50", label="Sirkap, the Greek city", year=-50, startYear=-180, endYear=60,
         summary="Sirkap, the walled city at the foot of the Hathial ridge, laid out on a grid by the Bactrian Greeks after about 180 BCE and held in turn by Indo-Greek, Saka and Parthian kings. A straight main street runs south from the north gate between house blocks, shops and street shrines; a Greek-style temple stands at Jandial outside the gate. Rebuilt after an earthquake about 30 CE.",
         population="unknown; perhaps 20,000–40,000",
         feel="Greek and Prakrit in the main street, the ring of silversmiths' hammers, incense at a stupa between the shops, cavalry clattering out of the north gate.",
         style="courtyard",
         houses=dict(title="House blocks of Sirkap", text="Each block between the lanes holds several houses of rubble and later of diaper masonry, rooms set round open courts, plastered and flat-roofed, some of two storeys; shops line the main street, and small stupas or shrines stand among them."),
         outskirts=dict(title="Gardens outside the walls", text="Orchards and fields along the Tamra Nala, the temple at Jandial in its enclosure, tombs and stupas along the roads, and the old Bhir Mound half deserted across the stream.")),
    dict(id="kushan-200", label="Kushan Sirsukh", year=200, startYear=61, endYear=459,
         summary="The Kushans have built a new city, Sirsukh, with square walls and round bastions on the plain to the north-east; Sirkap thins out. Silk Road wealth goes into Buddhism: the Dharmarajika is enlarged and ringed with chapels, and monasteries such as Mohra Moradu rise on the hillsides, their stupas covered in painted stucco Buddhas. Walls are laid in diaper masonry, large blocks with small stones packed between.",
         population="unknown",
         feel="Monks' bells and chanting from the hills, the scrape of chisels on grey schist, camels and Kushan horsemen in felt boots at the gates of Sirsukh.",
         style="courtyard",
         houses=dict(title="Houses of Sirsukh", text="Courtyard houses of diaper masonry, coursed blocks with small stones packed between, plastered and whitewashed; flat roofs of beams and clay, rooms round a court with a well, kitchens and stores at the back."),
         outskirts=dict(title="Monasteries and fields", text="Monasteries with cells round a court and a stupa beside them on every spur, orchards and fields between, and Sirkap's old blocks slowly emptying behind its wall.")),
    dict(id="huna-500", label="After the Huns", year=500, startYear=460, endYear=660,
         summary="After the Hephthalite (Huna) raids of about 460–470 the monasteries are burned and the cities shrink. Sirsukh survives as a reduced town; Sirkap and the Bhir Mound are mounds of rubble with fields on them. When Xuanzang passed in the 630s he found the land subject to Kashmir, its ruling families extinct, and most of the monasteries ruined, with few monks.",
         population="a few thousand at most",
         feel="Wind over burned courtyards, goats grazing between broken stupas, a handful of monks tending a lamp at a damaged shrine.",
         style="courtyard",
         houses=dict(title="Houses among the ruins", text="Small houses patched together from the stones of older buildings, one storey, with flat roofs of brushwood and mud; animals stabled in the old courts."),
         outskirts=dict(title="Fields over the old cities", text="Ploughed fields and grazing on the mounds of the Bhir and Sirkap, burned monasteries on the hills, a few hamlets by the streams.")),
]

SOURCES = [
    dict(id="wiki-taxila", title="Taxila", author="Wikipedia", url="https://en.wikipedia.org/wiki/Taxila"),
    dict(id="wiki-bhir", title="Bhir Mound", author="Wikipedia", url="https://en.wikipedia.org/wiki/Bhir_Mound"),
    dict(id="wiki-sirkap", title="Sirkap", author="Wikipedia", url="https://en.wikipedia.org/wiki/Sirkap"),
    dict(id="wiki-sirsukh", title="Sirsukh", author="Wikipedia", url="https://en.wikipedia.org/wiki/Sirsukh"),
    dict(id="wiki-hathial", title="Hathial", author="Wikipedia", url="https://en.wikipedia.org/wiki/Hathial"),
    dict(id="wiki-gandhara", title="Gandhara", author="Wikipedia", url="https://en.wikipedia.org/wiki/Gandhara"),
    dict(id="wiki-uttarapatha", title="Uttarapatha", author="Wikipedia", url="https://en.wikipedia.org/wiki/Uttarapatha"),
    dict(id="wiki-haro", title="Haro River", author="Wikipedia", url="https://en.wikipedia.org/wiki/Haro_River"),
    dict(id="marshall-taxila", title="Taxila: An Illustrated Account of Archaeological Excavations, 3 vols.", author="John Marshall", year=1951),
    dict(id="marshall-guide", title="A Guide to Taxila", author="John Marshall", year="1918, 4th ed. 1960"),
    dict(id="dani-taxila", title="The Historic City of Taxila", author="Ahmad Hasan Dani", year=1986),
    dict(id="allchin", title="The Archaeology of Early Historic South Asia", author="F. R. Allchin", year=1995),
]

# ---------------------------------------------------------------- water
WATER = [
    dict(id="tamra-nala", name="Tamra Nala", width=16,
         path=[(33.7445, 72.8635), (33.7436, 72.8580), (33.7430, 72.8520), (33.7432, 72.8470), (33.7437, 72.8430), (33.7442, 72.8390),
               (33.7438, 72.8345), (33.7428, 72.8305), (33.7428, 72.8270), (33.7438, 72.8250), (33.7462, 72.8244), (33.7500, 72.8247),
               (33.7540, 72.8249), (33.7580, 72.8245), (33.7620, 72.8238), (33.7680, 72.8232), (33.7740, 72.8215), (33.7790, 72.8205)],
         blurb="The Tamra (or Tabra) Nala, a stony stream that floods after the monsoon rains, runs between the Bhir Mound and Sirkap and on north to the Haro river, a few kilometres beyond the edge of this map. Its course here is approximate."),
    dict(id="lundi-nala", name="Lundi Nala", width=9,
         path=[(33.7585, 72.8635), (33.7610, 72.8580), (33.7640, 72.8565), (33.7690, 72.8575), (33.7740, 72.8578), (33.7790, 72.8590)],
         blurb="A smaller stream from the hills to the east, running past the east side of Sirsukh toward the Haro. Name and course follow the usual excavation plans and are approximate."),
]

HILLS = [
    dict(id="hathial", name="Hathial", center=(33.7470, 72.8368), radius=300,
         blurb="A limestone spur running out from the hills to the south-east. Its western end held the oldest settlement in the valley, perhaps from the late 2nd millennium BCE; the Greeks took the ridge into Sirkap's walls as an upper city."),
    dict(id="kunala-ridge", name="Kunala ridge", center=(33.7500, 72.8295), radius=200, label=False,
         blurb="The western tail of the Hathial spur, just south of the lower city of Sirkap, crowned by the Kunala stupa."),
    dict(id="eastern-hills", name="Eastern hills", center=(33.7520, 72.8590), radius=420,
         blurb="Low hills of limestone and scrub between the Taxila valley and the side valleys where the Jaulian and Mohra Moradu monasteries were built."),
    dict(id="mohra-spur", name="Mohra spur", center=(33.7575, 72.8630), radius=220, label=False,
         blurb="The hill slope above the Mohra Moradu valley."),
]

# ---------------------------------------------------------------- roads
BHIR_STREETS = [
    dict(id="bhir-first-street", name="First Street", width=8, style="major", labelled=True, periods=BHIR,
         path=[(33.7480, 72.8199), (33.7466, 72.8197), (33.7452, 72.8199), (33.7438, 72.8197), (33.7424, 72.8200), (33.7408, 72.8198)],
         blurb="The main street of the Bhir Mound as Marshall named it, running roughly north–south and bending as it goes; shops of one or two rooms opened onto it."),
    dict(id="bhir-second-street", name="Second Street", width=6, style="minor", periods=BHIR,
         path=[(33.7476, 72.8217), (33.7462, 72.8215), (33.7448, 72.8218), (33.7434, 72.8216), (33.7420, 72.8219), (33.7410, 72.8222)],
         blurb="A parallel street to the east, narrower and more crooked; the lanes between the two were often blocked by later houses."),
    dict(id="bhir-north-lane", name="Lane of the wells", width=5, style="minor", periods=BHIR,
         path=[(33.7451, 72.8178), (33.7449, 72.8190), (33.7451, 72.8205), (33.7448, 72.8222), (33.7450, 72.8234)],
         blurb="A twisting cross-lane; the soak-wells of stacked pottery rings that drained the houses were dug along lanes like this."),
    dict(id="bhir-south-lane", name="South lane", width=5, style="minor", periods=["maurya-300"],
         path=[(33.7428, 72.8180), (33.7430, 72.8192), (33.7427, 72.8208), (33.7429, 72.8222), (33.7426, 72.8233)],
         blurb="A lane through the southern quarter, built over as the town grew south in the Mauryan period."),
]

LANES = [33.7611, 33.7598, 33.7584, 33.7570, 33.7556, 33.7542, 33.7524]
SIRKAP_LANES = [dict(id=f"sirkap-lane-{i}", name=f"Sirkap cross-lane {i}", width=5, style="minor", periods=SIRKAP,
                     path=[(LANES[i], 72.8265), (LANES[i], 72.8299), (LANES[i], 72.8335)],
                     blurb="One of the narrow side streets that cross the main street at right angles, dividing Sirkap into regular blocks in the Hippodamian manner.")
                for i in range(1, 6)]

ROADS = BHIR_STREETS + SIRKAP_LANES + [
    dict(id="uttarapatha-west", name="Road to Pushkalavati and Bactria", width=12, style="major", labelled=True, periods=ALL,
         path=[(33.7535, 72.8150), (33.7515, 72.8162), (33.7495, 72.8175), (33.7480, 72.8190)],
         blurb="The great northern road, the Uttarapatha, came in from the west: over the Indus at Udabhandapura to Pushkalavati and on through the passes to Bactria. Caravans of horses, wool and lapis came down it."),
    dict(id="uttarapatha-east", name="Road to the Ganges plain", width=12, style="major", labelled=True, periods=ALL,
         path=[(33.7409, 72.8210), (33.7414, 72.8240), (33.7418, 72.8268), (33.7408, 72.8310), (33.7398, 72.8360), (33.7393, 72.8405), (33.7386, 72.8445)],
         blurb="The Uttarapatha went on south-east through the Margalla pass toward Mathura and the Ganges cities; Pataliputra, the Mauryan capital, lay some 1,500 km away."),
    dict(id="kashmir-road", name="Road north to the Haro and Kashmir", width=8, style="minor", periods=BHIR,
         path=[(33.7480, 72.8192), (33.7520, 72.8188), (33.7580, 72.8185), (33.7650, 72.8180), (33.7720, 72.8175), (33.7790, 72.8172)],
         blurb="A track north across the valley to the fords of the Haro and on toward Urasa (Hazara) and Kashmir."),
    dict(id="sirkap-main-street", name="Main street of Sirkap", width=10, style="major", labelled=True, periods=SIRKAP,
         path=[(33.7611, 72.8300), (33.7590, 72.8300), (33.7565, 72.8300), (33.7545, 72.8300), (33.7526, 72.8300)],
         blurb="A straight street about 700 m long from the north gate toward the palace and the Hathial ridge, lined with shops and with small shrines and stupas set in among the house blocks."),
    dict(id="sirkap-west-road", name="Road west from the north gate", width=10, style="major", periods=LATE,
         path=[(33.7613, 72.8300), (33.7622, 72.8270), (33.7616, 72.8238), (33.7590, 72.8205), (33.7560, 72.8178), (33.7535, 72.8150)],
         blurb="Outside the north gate the western road turned across the Tamra Nala to join the old highway to the Indus."),
    dict(id="jandial-road", name="Road north past Jandial", width=9, style="minor", periods=LATE,
         path=[(33.7613, 72.8300), (33.7630, 72.8302), (33.7650, 72.8306), (33.7680, 72.8315), (33.7730, 72.8325), (33.7790, 72.8335)],
         blurb="From the north gate the road ran north past the temple at Jandial toward the Haro and the hill country beyond."),
    dict(id="dharmarajika-road", name="Road to the Dharmarajika", width=7, style="minor", periods=LATE,
         path=[(33.7556, 72.8337), (33.7552, 72.8380), (33.7535, 72.8410), (33.7500, 72.8422), (33.7476, 72.8430), (33.7460, 72.8433)],
         blurb="A path from Sirkap round the north and east of the Hathial ridge to the great stupa, walked by pilgrims and by monks going to and from the town."),
    dict(id="sirkap-sirsukh-road", name="Road from Sirkap to Sirsukh", width=9, style="minor", periods=SIRSUKH,
         path=[(33.7630, 72.8302), (33.7642, 72.8345), (33.7652, 72.8400), (33.7660, 72.8450), (33.7665, 72.8480)],
         blurb="The road from the old city to the new Kushan one, about 2 km."),
    dict(id="sirsukh-ns", name="Sirsukh, north–south street", width=10, style="major", periods=SIRSUKH,
         path=[(33.7665, 72.8480), (33.7700, 72.8480), (33.7740, 72.8480), (33.7775, 72.8480)],
         blurb="Sirsukh's interior is barely excavated; a main street between the gates is assumed, not known."),
    dict(id="sirsukh-ew", name="Sirsukh, east–west street", width=8, style="minor", periods=SIRSUKH,
         path=[(33.7722, 72.8410), (33.7722, 72.8450), (33.7722, 72.8510), (33.7722, 72.8550)],
         blurb="A cross street between the east and west gates; its line, like the rest of the plan, is conjectural."),
    dict(id="sirsukh-west-road", name="Road west from Sirsukh", width=7, style="minor", periods=SIRSUKH,
         path=[(33.7722, 72.8410), (33.7712, 72.8380), (33.7700, 72.8345), (33.7690, 72.8318)],
         blurb="A road from Sirsukh's west gate to the old northern road past Jandial."),
    dict(id="monastery-road", name="Road to Mohra Moradu and Jaulian", width=7, style="minor", periods=SIRSUKH,
         path=[(33.7722, 72.8550), (33.7700, 72.8562), (33.7660, 72.8585), (33.7630, 72.8600), (33.7622, 72.8635)],
         blurb="The way east into the hills to the monasteries of Mohra Moradu and, a little farther, Jaulian, where monks lived from the 2nd to the 5th century."),
]

# ---------------------------------------------------------------- walls and gates
SIRKAP_WALL = [(33.7612, 72.8262), (33.7612, 72.8338), (33.7560, 72.8340), (33.7530, 72.8345), (33.7510, 72.8375), (33.7488, 72.8392),
               (33.7468, 72.8382), (33.7462, 72.8352), (33.7490, 72.8325), (33.7520, 72.8300), (33.7522, 72.8262)]
SIRSUKH_WALL = [(33.7775, 72.8410), (33.7775, 72.8550), (33.7665, 72.8550), (33.7665, 72.8410)]
WALLS = [
    dict(id="sirkap-wall", name="Wall of Sirkap", closed=True, periods=LATE, path=SIRKAP_WALL,
         blurb="A stone wall about 6 m thick with rectangular bastions, enclosing the lower city on the plain and climbing over the Hathial spur to take in an upper city; Marshall measured the circuit at nearly 5.6 km. In the 5th century CE it stands abandoned."),
    dict(id="sirsukh-wall", name="Wall of Sirsukh", closed=True, periods=SIRSUKH, path=SIRSUKH_WALL,
         blurb="The Kushan city wall, a rough rectangle about 1.4 by 1.2 km, faced in diaper masonry with semicircular bastions every 27 m or so and loopholes in the lower storey. Parts of the south and east walls were excavated in 1915."),
]

GATES = [
    dict(id="sirkap-north-gate", name="North Gate of Sirkap", position=(33.7612, 72.8300), periods=LATE),
    dict(id="sirkap-east-gate", name="East gate (conjectural)", position=(33.7557, 72.8339), periods=SIRKAP),
    dict(id="sirsukh-south-gate", name="South gate", position=(33.7665, 72.8480), periods=SIRSUKH),
    dict(id="sirsukh-north-gate", name="North gate", position=(33.7775, 72.8480), periods=SIRSUKH),
    dict(id="sirsukh-west-gate", name="West gate", position=(33.7722, 72.8410), periods=SIRSUKH),
    dict(id="sirsukh-east-gate", name="East gate", position=(33.7722, 72.8550), periods=SIRSUKH),
]

BRIDGES = [
    dict(id="tamra-bridge-west", name="Crossing of the Tamra Nala", path=[(33.7619, 72.8249), (33.7614, 72.8228)], build="timber", arches=2, periods=LATE,
         blurb="A wooden bridge, or in the dry season simply a ford, where the western road crossed the stream below Sirkap."),
    dict(id="tamra-bridge-stupa", name="Ford below the Dharmarajika", path=[(33.7445, 72.8433), (33.7429, 72.8430)], build="timber", arches=1, periods=LATE,
         blurb="A ford of the Tamra Nala just below the rise of the great stupa, for those coming up from the south road."),
]

AQUEDUCTS = []

# ---------------------------------------------------------------- built-up blocks
def _rect(n, s, w, e):
    return [(n, w), (n, e), (s, e), (s, w)]


# the Bhir Mound: three crooked columns between First and Second Streets, three rows between the lanes
BHIR_COLS = [(72.8180, 72.8194), (72.8203, 72.8213), (72.8221, 72.8233)]
BHIR_ROWS = [(33.7477, 33.7454), (33.7446, 33.7432), (33.7425, 33.7415)]
BHIR_BLOCKS = []
for r, (n, s) in enumerate(BHIR_ROWS):
    for c, (w, e) in enumerate(BHIR_COLS):
        BHIR_BLOCKS.append(dict(name="Bhir Mound", density="dense",
                                periods=(BHIR if r < 2 else ["maurya-300"]),
                                polygon=[(n, w + 0.0001 * (c % 2)), (n - 0.0002 * (r % 2), e), (s, e - 0.0001 * ((r + c) % 2)), (s + 0.0001, w)]))

# Sirkap: two rows of blocks between the main street and the walls, cut by the cross-lanes
SIRKAP_BLOCKS = []
for i in range(6):
    n, s = LANES[i] - 0.00008, LANES[i + 1] + 0.00008
    for side, (w, e) in (("west", (72.8266, 72.8295)), ("east", (72.8305, 72.8334))):
        SIRKAP_BLOCKS.append(dict(name=f"Sirkap, block {'ABCDEFG'[i]} {side}", density="dense", periods=["indo-greek-50"], polygon=_rect(n, s, w, e)))
        if i < 4:
            SIRKAP_BLOCKS.append(dict(name=f"Sirkap, block {'ABCDEFG'[i]} {side}", density="loose", periods=["kushan-200"], polygon=_rect(n, s, w, e)))

BLOCKS = BHIR_BLOCKS + SIRKAP_BLOCKS + [
    dict(name="Hathial village", density="loose", periods=["achaemenid-450"],
         polygon=[(33.7518, 72.8318), (33.7516, 72.8345), (33.7503, 72.8350), (33.7500, 72.8322)]),
    dict(name="Bhir Mound, west suburb", density="loose", periods=["maurya-300"],
         polygon=[(33.7470, 72.8160), (33.7468, 72.8174), (33.7440, 72.8175), (33.7438, 72.8160)]),
    dict(name="Caravan ground and potters", density="loose", periods=["maurya-300"],
         polygon=[(33.7408, 72.8228), (33.7410, 72.8250), (33.7400, 72.8262), (33.7395, 72.8232)]),
    dict(name="Bhir Mound, last houses", density="loose", periods=["indo-greek-50"],
         polygon=[(33.7476, 72.8181), (33.7476, 72.8212), (33.7456, 72.8212), (33.7456, 72.8181)]),
    dict(name="Outside the north gate", density="loose", periods=["indo-greek-50"],
         polygon=[(33.7638, 72.8310), (33.7638, 72.8336), (33.7618, 72.8336), (33.7618, 72.8310)]),
    dict(name="Sirsukh, north-west quarter", density="dense", periods=["kushan-200"], polygon=_rect(33.7770, 33.7727, 72.8416, 72.8475)),
    dict(name="Sirsukh, north-east quarter", density="dense", periods=["kushan-200"], polygon=_rect(33.7770, 33.7727, 72.8485, 72.8545)),
    dict(name="Sirsukh, south-west quarter", density="dense", periods=["kushan-200"], polygon=_rect(33.7717, 33.7672, 72.8416, 72.8475)),
    dict(name="Sirsukh, south-east quarter", density="dense", periods=["kushan-200"], polygon=_rect(33.7717, 33.7672, 72.8485, 72.8545)),
    dict(name="Sirsukh, what is left", density="loose", periods=["huna-500"], polygon=_rect(33.7745, 33.7727, 72.8440, 72.8475)),
    dict(name="Sirsukh, what is left", density="loose", periods=["huna-500"], polygon=_rect(33.7717, 33.7690, 72.8485, 72.8520)),
    dict(name="Monks' village by the Dharmarajika", density="loose", periods=["kushan-200"],
         polygon=[(33.7473, 72.8400), (33.7473, 72.8422), (33.7464, 72.8422), (33.7464, 72.8400)]),
    dict(name="Hamlet by the Tamra Nala", density="loose", periods=["huna-500"],
         polygon=[(33.7470, 72.8228), (33.7470, 72.8236), (33.7452, 72.8236), (33.7452, 72.8226)]),
]

GARDENS = [
    dict(name="Fields of the valley", kind="orchard", periods=ALL,
         polygon=[(33.7700, 72.8235), (33.7700, 72.8300), (33.7655, 72.8295), (33.7655, 72.8245)]),
    dict(name="Fields north of the Bhir Mound", kind="orchard", periods=BHIR,
         polygon=[(33.7560, 72.8200), (33.7560, 72.8235), (33.7500, 72.8237), (33.7495, 72.8200)]),
    dict(name="Fields over the Bhir Mound", kind="orchard", periods=["kushan-200", "huna-500"],
         polygon=[(33.7472, 72.8185), (33.7472, 72.8215), (33.7440, 72.8215), (33.7440, 72.8185)]),
    dict(name="Mango groves", kind="orchard", periods=ALL,
         polygon=[(33.7470, 72.8440), (33.7470, 72.8500), (33.7445, 72.8500), (33.7445, 72.8445)]),
    dict(name="Fields of the plain", kind="orchard", periods=ALL,
         polygon=[(33.7640, 72.8400), (33.7640, 72.8460), (33.7600, 72.8460), (33.7600, 72.8400)]),
    dict(name="Monastery grove", kind="park", periods=["kushan-200"],
         polygon=[(33.7600, 72.8580), (33.7598, 72.8595), (33.7588, 72.8596), (33.7590, 72.8580)]),
    dict(name="Fields over Sirkap", kind="orchard", periods=["huna-500"],
         polygon=[(33.7595, 72.8268), (33.7595, 72.8332), (33.7545, 72.8332), (33.7545, 72.8268)]),
]

MARSH = []

DISTRICTS = [
    dict(id="bhir-mound", name="Bhir Mound", periods=BHIR,
         polygon=[(33.7480, 72.8176), (33.7480, 72.8236), (33.7408, 72.8236), (33.7408, 72.8176)],
         description="The oldest city on the valley floor, from about the 6th century BCE: a mound of rubble houses on irregular streets, the Takshashila of the Persian satraps, of Alexander and of the Mauryan viceroys."),
    dict(id="sirkap", name="Sirkap", periods=SIRKAP,
         polygon=[(33.7612, 72.8262), (33.7612, 72.8338), (33.7522, 72.8340), (33.7522, 72.8262)],
         description="The Indo-Greek city founded in the 2nd century BCE, its lower town on a grid of blocks along one main street, its upper town on the Hathial ridge; home to Greek, Saka and Parthian kings until the Kushans moved the city."),
    dict(id="sirkap-upper", name="Upper city (Hathial)", periods=SIRKAP,
         polygon=[(33.7522, 72.8340), (33.7510, 72.8375), (33.7488, 72.8392), (33.7468, 72.8382), (33.7462, 72.8352), (33.7490, 72.8325), (33.7520, 72.8300)],
         description="The part of Sirkap on the ridge, inside the walls but thinly built: a citadel and perhaps barracks and stores. Little has been excavated."),
    dict(id="sirsukh", name="Sirsukh", periods=SIRSUKH,
         polygon=[(33.7775, 72.8410), (33.7775, 72.8550), (33.7665, 72.8550), (33.7665, 72.8410)],
         description="The Kushan city on the plain, square-walled with round bastions, built probably in the late 1st or 2nd century CE. Its interior is almost unexcavated; modern villages and fields cover it."),
    dict(id="dharmarajika-precinct", name="Dharmarajika precinct", periods=BUDDHIST,
         polygon=[(33.7462, 72.8410), (33.7462, 72.8436), (33.7444, 72.8436), (33.7444, 72.8410)],
         description="The sacred ground of the great stupa on the rise east of the Tamra Nala, with its chapels, votive stupas and monastery."),
]

LABELS = [
    dict(text="Takshashila", position=(33.7488, 72.8205), size="lg", periods=BHIR),
    dict(text="Bhir Mound", position=(33.7488, 72.8205), size="md", periods=["indo-greek-50", "kushan-200", "huna-500"]),
    dict(text="Sirkap", position=(33.7625, 72.8270), size="lg", periods=SIRKAP),
    dict(text="Sirkap (ruins)", position=(33.7625, 72.8270), size="md", periods=["huna-500"]),
    dict(text="Sirsukh", position=(33.7783, 72.8440), size="lg", periods=SIRSUKH),
    dict(text="Tamra Nala", position=(33.7520, 72.8238), size="sm", rotation=-88),
    dict(text="Lundi Nala", position=(33.7710, 72.8585), size="sm", rotation=-85),
    dict(text="Hathial", position=(33.7452, 72.8372), size="md"),
    dict(text="to Pushkalavati and Bactria", position=(33.7540, 72.8158), size="sm", rotation=-35),
    dict(text="to Mathura and the Ganges", position=(33.7392, 72.8350), size="sm", rotation=8),
    dict(text="to Jaulian", position=(33.7632, 72.8610), size="sm", periods=SIRSUKH),
    dict(text="to the Haro river", position=(33.7780, 72.8250), size="sm"),
]
