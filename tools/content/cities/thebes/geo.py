# Thebes (Waset): the east bank from Karnak to Luxor along the processional way, the Nile, and the west bank
# from Deir el-Bahari and the Valley of the Kings to Medinet Habu and Malkata (see tools/content/cities/FORMAT.md).
ALL = ["middle-kingdom-1950", "hatshepsut-1470", "ramesside-1250", "late-period-600", "roman-200"]
NEW_KINGDOM = ["hatshepsut-1470", "ramesside-1250"]
FROM_1470 = ["hatshepsut-1470", "ramesside-1250", "late-period-600", "roman-200"]
FROM_1250 = ["ramesside-1250", "late-period-600", "roman-200"]
TO_1250 = ["middle-kingdom-1950", "hatshepsut-1470", "ramesside-1250"]
TO_600 = ["middle-kingdom-1950", "hatshepsut-1470", "ramesside-1250", "late-period-600"]
LATE = ["late-period-600", "roman-200"]


def west(pts, dlon):
    """The centre line of a river drawn as a wide stroke whose east edge is the bank line pts."""
    return [(lat, round(lon - dlon, 5)) for lat, lon in pts]


SOURCES = [
    dict(id="kemp-ancient-egypt", title="Ancient Egypt: Anatomy of a Civilization", author="Barry J. Kemp", year=2006, note="2nd edition; chapter on Thebes and the New Kingdom city"),
    dict(id="strudwick-thebes", title="Thebes in Egypt: A Guide to the Tombs and Temples of Ancient Luxor", author="Nigel and Helen Strudwick", year=1999),
    dict(id="weeks-atlas", title="Atlas of the Valley of the Kings / Theban Mapping Project", author="Kent R. Weeks (ed.)", year="2000–", url="https://thebanmappingproject.com/"),
    dict(id="bunbury-river", title="The Nile and Ancient Egypt: Changing Land- and Waterscapes, from the Neolithic to the Roman Era", author="Judith Bunbury", year=2019),
    dict(id="graham-karnak-floodplain", title="Reconstructing Thebes' ancient river: the Karnak floodplain cores", author="Angus Graham, Judith Bunbury et al.", year="2012–2015", note="Theban Harbours and Waterscapes Survey reports, Journal of Egyptian Archaeology"),
    dict(id="kemp-oconnor-birket-habu", title="An Ancient Nile Harbour: University Museum Excavations at the 'Birket Habu'", author="Barry J. Kemp and David O'Connor", year=1974, note="International Journal of Nautical Archaeology 3"),
    dict(id="wiki-thebes", title="Thebes, Egypt", author="Wikipedia", url="https://en.wikipedia.org/wiki/Thebes,_Egypt"),
    dict(id="wiki-theban-necropolis", title="Theban Necropolis", author="Wikipedia", url="https://en.wikipedia.org/wiki/Theban_Necropolis"),
    dict(id="wiki-birket-habu", title="Malkata (Birket Habu)", author="Wikipedia", url="https://en.wikipedia.org/wiki/Malkata"),
    dict(id="wiki-flooding-nile", title="Flooding of the Nile", author="Wikipedia", url="https://en.wikipedia.org/wiki/Flooding_of_the_Nile"),
    dict(id="wiki-avenue-sphinxes", title="Avenue of Sphinxes", author="Wikipedia", url="https://en.wikipedia.org/wiki/Avenue_of_Sphinxes"),
    dict(id="wiki-diospolis", title="Thebes, Egypt: Greek and Roman Diospolis Magna", author="Wikipedia", url="https://en.wikipedia.org/wiki/Thebes,_Egypt#Ptolemaic_and_Roman_periods"),
]

CITY = dict(
    name="Thebes", subtitle="Waset, City of Amun",
    description="Two thousand years of Thebes, from the Middle Kingdom capital round the first temple of Amun to the Roman villages among its ruins: Karnak and Luxor on the east bank joined by the processional way, the Nile, and the temples and tombs of the west bank under the Theban mountain. The river's course is drawn as the usual reconstruction. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="ramesside-1250",
    world=dict(heightScale=0.9, walls=["#D8C4A0", "#CDB48C", "#E2D3B6", "#C4A880", "#D6C09A"], roofs=["#C9B48E", "#BDA47E"]),
    camera=dict(target=(25.7135, 32.6420), distance=46),
)

# north-west corner, south-east corner: Deir el-Bahari and the Valley of the Kings to Karnak's east town, Malkata to south of Luxor
FRAME = ((25.7450, 32.5955), (25.6890, 32.6690))

PALETTE = dict(parchment="#E9D6AA", ink="#6B4A30", water="#5E8A86", hill="#A88E62", road="#8C6A48")
COMPASS = (25.7420, 32.6660)
CARTOUCHE = (25.6905, 32.5975)

PERIODS = [
    dict(id="middle-kingdom-1950", label="Middle Kingdom Waset", year=-1950, startYear=-2055, endYear=-1550,
         summary="A provincial town of Upper Egypt whose princes, the Mentuhoteps, reunited the country about 2040 BCE. Under the 12th dynasty Senusret I builds the first large stone temple of Amun at Karnak and the White Chapel for his jubilee; the court soon moves north, but Thebes keeps its god. Mud-brick town, limestone temples, Mentuhotep's terraced tomb-temple under the western cliffs.",
         population="perhaps 10,000–20,000",
         feel="Mud and dung smoke at dawn, oxen on the threshing floors, a new white limestone shrine gleaming over the brick roofs, and the cliffs of the west turning pink at sunset.",
         style="courtyard",
         houses=dict(title="Brick houses of Waset", text="Houses of sun-dried Nile mud brick, plastered and whitewashed, a few rooms round a yard with a bread oven and a grain bin; flat roofs of palm logs and reeds where families slept in summer. The town lay on a mound above the flood, round the temple."),
         outskirts=dict(title="Farmsteads and threshing floors", text="Beyond the town, farmsteads of mud brick among palms and fields of emmer and barley, threshing floors, dovecotes and cattle pens, all on the higher ground the flood did not reach.")),
    dict(id="hatshepsut-1470", label="Hatshepsut's Thebes", year=-1470, startYear=-1549, endYear=-1391,
         summary="The religious capital of an empire. After Ahmose drove out the Hyksos, Theban kings pour the spoils of Nubia and Syria into Amun's temple. Hatshepsut (c. 1479–1458) raises obelisks and the Red Chapel at Karnak, builds the eighth pylon and barque shrines along the road to Luxor, and her terraced temple at Deir el-Bahari. The kings are now buried in the Valley of the Kings.",
         population="perhaps 40,000–60,000",
         feel="Gilded obelisk tips flashing over the town, the drums and sistra of the Opet procession, ships from Punt unloading incense trees, sculptors' chisels ringing on the west bank.",
         style="courtyard",
         houses=dict(title="Town houses of Waset", text="Two- and three-storey houses of mud brick packed along lanes: a ground floor for storage, weaving and animals, living rooms above, a stair to the roof and its grain silos. Officials' houses have a columned hall, a garden pool and painted walls."),
         outskirts=dict(title="Estates of Amun", text="Fields, orchards and cattle stations of the temple of Amun, with the farmhouses of its tenants; on the west bank, the camps of quarrymen and the workshops building Hatshepsut's temple.")),
    dict(id="ramesside-1250", label="Thebes of Ramesses II", year=-1250, startYear=-1390, endYear=-1070,
         summary="The Thebes of the great temples: Amenhotep III's colonnades and colossi, and after Akhenaten's heresy the restored cult of Amun, whose temple now owns a vast share of Egypt's land. Ramesses II finishes the Great Hypostyle Hall, adds Luxor's pylon, obelisks and court, and builds the Ramesseum. The kings live in the north; Thebes is the city of the gods and the dead.",
         population="perhaps 50,000–80,000",
         feel="Painted pylons with fluttering pennants on their flagstaffs, incense and roasting meat at the temple gates, ferries crowded with workmen, the clack of looms in the temple workshops.",
         style="courtyard",
         houses=dict(title="Houses of the city of Amun", text="Narrow mud-brick houses of two or three storeys built wall to wall, whitewashed, with small high windows, wooden doors painted red, and roofs crowded with ovens, grain bins and awnings. Priests and scribes live in larger houses with a columned reception room."),
         outskirts=dict(title="Temple estates and villages", text="Villages of farmers who work the temple fields, with threshing floors, palm groves and pigeon towers; on the west bank, the settlements of the mortuary temples' staff along the desert edge.")),
    dict(id="late-period-600", label="Thebes of the God's Wives", year=-600, startYear=-1069, endYear=-333,
         summary="After the New Kingdom, Thebes is ruled by the high priests of Amun, then by the God's Wives of Amun: royal princesses, Kushite and then Saite, who govern the city as the god's consorts. Taharqa builds his kiosk at Karnak; the Assyrians sack Thebes in 664 or 663 BCE. A smaller city of priests and officials, with tombs for the God's Wives at Medinet Habu.",
         population="perhaps 20,000–40,000",
         feel="Bald-headed priests with their temple tallies, Nubian soldiers at the gates, scorched blocks from the Assyrian sack in the rubble, brick tower-tombs of the officials on the west bank.",
         style="courtyard",
         houses=dict(title="Tower houses of the priests", text="Tall narrow houses of mud brick on the old town mounds, built over the rubble of earlier ones and rising higher each rebuilding; priests' houses cluster against the temple enclosures, where the God's Wives and their stewards have their own estates."),
         outskirts=dict(title="Mounds and fields", text="Abandoned quarters of the New Kingdom city turned to rubbish mounds and fields; small hamlets of farmers, and on the west bank the walled town round Medinet Habu.")),
    dict(id="roman-200", label="Roman Diospolis Magna", year=200, startYear=-332, endYear=400,
         summary="Greek Diospolis Magna: after the revolts against the Ptolemies and the sack of 88 BCE, 'Great Thebes' is a scatter of villages among its temples, as Strabo saw it in about 25 BCE. Priests still serve Amun at Karnak; tourists come to hear the singing Colossus of Memnon and visit the royal tombs. Around 300 CE the Romans build a legion camp inside Luxor temple.",
         population="a few thousand in several villages",
         feel="Greek and Demotic in the same lane, tourists scratching their names on the colossus at dawn, priests in linen at Karnak's gates, mud-brick villages piled against the temple walls.",
         style="courtyard",
         houses=dict(title="Village houses among the temples", text="Mud-brick houses of two or three storeys with vaulted rooms and dovecotes on the roofs, built against and even inside the old temples, on the rubble of the pharaonic city; Greek-style columns appear in a few richer houses."),
         outskirts=dict(title="Villages of the Memnonia", text="On the west bank the villages of the 'Memnonia' and Djeme among the ruined temples; on both banks, fields, palm groves and threshing floors where the old city once stood.")),
]

# ---------------------------------------------------------------- the Nile: east bank line, river drawn as a wide stroke west of it
BANK = [(25.6880, 32.6322), (25.6950, 32.6344), (25.6995, 32.6362), (25.7040, 32.6390), (25.7090, 32.6428), (25.7140, 32.6470), (25.7200, 32.6522),
        (25.7250, 32.6560), (25.7310, 32.6598), (25.7380, 32.6632), (25.7460, 32.6668)]

NILE_BLURB = "The river (Iteru) rose from July to September and covered the fields of both banks, leaving the towns and temples on their mounds. Coring shows that in pharaonic times the channel ran further east, close to Karnak's quay, and has since drifted west; the course drawn is the usual reconstruction."

WATER = [
    dict(id="nile", name="The Nile (Iteru)", path=west(BANK, 0.0032), width=560, blurb=NILE_BLURB),
    dict(id="karnak-canal", name="Canal of Karnak", path=[(25.7203, 32.6508), (25.7200, 32.6545)], width=44, periods=FROM_1470,
         blurb="A canal joined the river to the harbour basin in front of Amun's temple, so that the god's barque, and the ships bringing stone, grain and tribute, could moor at the temple gate. Its line and date are known only in part from excavation and cores."),
    dict(id="birket-habu", name="Birket Habu", path=[(25.7055, 32.6040), (25.7044, 32.6150), (25.7036, 32.6250)], width=380, periods=["ramesside-1250"],
         blurb="A harbour basin over two kilometres long dug for Amenhotep III's palace at Malkata, probably for his jubilee festivals about 1360 BCE; the spoil heaps still ring it. By Ramesses II's time the palace was empty and the basin was silting up."),
]

ISLANDS = []

HILLS = [
    dict(id="theban-mountain", name="The Theban Mountain (Ta Dehent)", center=(25.7320, 32.5985), radius=380,
         blurb="The limestone massif of the west bank, crowned to the west by the pyramid-shaped peak of el-Qurn, 'the Peak', sacred to the snake goddess Meretseger, 'she who loves silence'. Its valleys hold the royal tombs; its foothills, thousands of tombs of officials."),
    dict(id="deir-el-bahari-cliffs", name="Cliffs of Deir el-Bahari", center=(25.7365, 32.6020), radius=170, label=False,
         blurb="The sheer amphitheatre of limestone cliffs that frames the temples of Mentuhotep II and Hatshepsut; Hathor, as a cow, was believed to emerge from the mountain here."),
    dict(id="ridge-valley", name="Ridge between Deir el-Bahari and the Valley of the Kings", center=(25.7400, 32.6030), radius=110, label=False,
         blurb="A narrow limestone ridge: the royal tombs lie only a few hundred metres behind Hatshepsut's temple, reached on foot over the top by the workmen's path."),
    dict(id="dra-abu-el-naga", name="Dra Abu el-Naga", center=(25.7430, 32.6110), radius=280,
         blurb="Foothills at the north end of the necropolis, where the kings of the 17th dynasty were buried under small brick pyramids and New Kingdom officials cut their tomb chapels."),
    dict(id="qurnet-murai", name="Qurnet Murai", center=(25.7248, 32.6045), radius=170,
         blurb="A low hill between Deir el-Medina and the plain, with tombs of New Kingdom officials, among them Amenhotep Huy, viceroy of Kush under Tutankhamun."),
    dict(id="valley-hills", name="Hills of the royal valleys", center=(25.7440, 32.5990), radius=200, label=False,
         blurb="The desert hills round the Valley of the Kings, cut by flash-flood gullies that sometimes filled the tombs with debris."),
    dict(id="southern-hills", name="Desert hills of the south-west", center=(25.7130, 32.5975), radius=260, label=False,
         blurb="Low desert hills behind Medinet Habu and Malkata, with the Valley of the Queens in a wadi to the west."),
]

AVENUE = [(25.7006, 32.6398), (25.7050, 32.6443), (25.7095, 32.6489), (25.7135, 32.6530), (25.71637, 32.65586)]
RIVER_ROAD = [(25.6890, 32.6332), (25.6950, 32.6353), (25.6995, 32.6371), (25.7040, 32.6399), (25.7090, 32.6437), (25.7140, 32.6479), (25.7200, 32.6531),
              (25.7250, 32.6569), (25.7310, 32.6607), (25.7380, 32.6641), (25.7450, 32.6676)]

ROADS = [
    dict(id="processional-way", name="Processional way of Amun", path=AVENUE, width=22, style="major", labelled=True, periods=NEW_KINGDOM,
         blurb="The road between Karnak and Luxor, about two and a half kilometres, along which Amun's barque was carried at the Opet festival. Hatshepsut lined it with six barque shrines where the bearers rested. Its earlier course is known only in part."),
    dict(id="processional-way", name="Processional way of Amun", path=AVENUE, width=22, style="major", labelled=True, periods=["late-period-600"],
         blurb="The old processional road between the temples. Nectanebo I (380–362 BCE) will rebuild it as a paved avenue lined with some 1,300 sphinxes; in 600 BCE it is still the New Kingdom road, with older sphinxes at both ends."),
    dict(id="avenue-of-sphinxes", name="Avenue of Sphinxes", path=AVENUE, width=24, style="major", labelled=True, periods=["roman-200"],
         blurb="Nectanebo I's paved dromos, lined on both sides with human-headed sphinxes a few metres apart, from Luxor temple to the gate of the Khonsu temple at Karnak, about 2.7 km. Roman Thebans built houses and workshops over parts of it."),
    dict(id="mut-avenue", name="Avenue of rams to Mut", path=[(25.71597, 32.65676), (25.71329, 32.65532)], width=18, style="major", periods=FROM_1470,
         blurb="From Karnak's southern pylons to the gate of Mut's precinct: the road of Amun's visits to his consort. Ram-headed sphinxes, recut by later kings, line it."),
    dict(id="river-road", name="Road along the river", path=RIVER_ROAD, width=10, style="major",
         blurb="The bank road of the east side, past the landing places, granaries and markets, from Luxor north to Karnak's quay and on toward Medamud and Koptos."),
    dict(id="medamud-road", name="Road to Medamud", path=[(25.72149, 32.66027), (25.7300, 32.6635), (25.7380, 32.6662), (25.7450, 32.6688)], width=9, style="minor", periods=FROM_1250,
         blurb="North from the gate of Montu's precinct toward Medamud, Montu's other temple 8 km away, along a sphinx-lined road near the temple."),
    dict(id="road-of-the-west", name="Road of the West", path=[(25.7195, 32.6460), (25.7200, 32.6350), (25.7210, 32.6230), (25.7208, 32.6125)], width=10, style="major", labelled=True,
         blurb="From the west-bank ferry landing across the fields to the desert edge and the temples of the dead. Funerals crossed the river by boat and went on by this road, the mourners wailing behind the sledge."),
    dict(id="desert-edge-road", name="Road along the desert edge", path=[(25.7365, 32.6175), (25.7310, 32.6200), (25.7275, 32.6140), (25.7235, 32.6125), (25.7210, 32.6120), (25.7195, 32.6070), (25.71901, 32.6030)],
         width=9, style="minor", periods=FROM_1250,
         blurb="The road linking the 'Houses of Millions of Years', the kings' mortuary temples, along the edge of the cultivation, patrolled by the police of the necropolis."),
    dict(id="valley-festival-road", name="Road of the Valley Festival", path=[(25.73361, 32.61719), (25.7305, 32.6240), (25.7310, 32.6330), (25.7315, 32.6450), (25.7318, 32.6522)],
         width=10, style="minor", periods=FROM_1470,
         blurb="From the river landing to the valley temple of Deir el-Bahari: the route of Amun's barque at the Beautiful Festival of the Valley, when Thebans visited the tombs of their families."),
    dict(id="valley-festival-road", name="Road to Mentuhotep's valley temple", path=[(25.73272, 32.61671), (25.7305, 32.6240), (25.7310, 32.6330), (25.7315, 32.6450), (25.7318, 32.6522)],
         width=10, style="minor", periods=["middle-kingdom-1950"],
         blurb="From the river to the valley temple of Mentuhotep II, the start of the Valley Festival, already celebrated in the Middle Kingdom."),
    dict(id="hatshepsut-causeway", name="Causeway of Hatshepsut", path=[(25.73757, 32.60823), (25.73361, 32.61719)], width=30, style="major", periods=FROM_1470,
         blurb="A walled causeway about a kilometre long from the valley temple to Djeser-djeseru, lined with sandstone sphinxes of the queen, with a barque station halfway."),
    dict(id="mentuhotep-causeway", name="Causeway of Mentuhotep II", path=[(25.73668, 32.60775), (25.73272, 32.61671)], width=30, style="major", periods=["middle-kingdom-1950"],
         blurb="The open causeway, over a kilometre long, from Mentuhotep II's valley temple up to his terraced tomb-temple, lined by statues of the king."),
    dict(id="seti-road", name="Road to the temple of Seti I", path=[(25.73287, 32.62839), (25.7312, 32.6335)], width=8, style="minor", periods=FROM_1250,
         blurb="From the front of Seti I's temple down to the valley road and the river."),
    dict(id="workmens-path", name="Workmen's path to the Valley of the Kings", path=[(25.7292, 32.6012), (25.7330, 32.6025), (25.7375, 32.6031), (25.7400, 32.6012)], width=5, style="minor", periods=NEW_KINGDOM,
         blurb="The path over the mountain from Deir el-Medina to the royal tombs, about an hour's climb. Workmen spent the week in stone huts at the pass and came home for their days off."),
    dict(id="deir-el-medina-path", name="Path from Deir el-Medina to the plain", path=[(25.7276, 32.6020), (25.7266, 32.6060), (25.7258, 32.6088)], width=6, style="minor", periods=NEW_KINGDOM,
         blurb="The workmen's road down to the temples and their storehouses, where they collected grain rations, fish and firewood."),
    dict(id="malkata-road", name="Road to Malkata", path=[(25.71901, 32.6030), (25.7110, 32.6025), (25.7080, 32.6020)], width=9, style="minor", periods=["ramesside-1250"],
         blurb="From the desert-edge road south to the deserted palace of Amenhotep III."),
]

WALLS = []
GATES = []
BRIDGES = []
AQUEDUCTS = []

# ---------------------------------------------------------------- built-up areas
B_QUAY = [(25.7215, 32.6538), (25.7250, 32.6568), (25.7235, 32.6592), (25.7212, 32.6575)]
B_NORTH = [(25.7235, 32.6612), (25.7270, 32.6622), (25.7262, 32.6662), (25.7228, 32.6652)]
B_EAST = [(25.7186, 32.6648), (25.7212, 32.6660), (25.7195, 32.6685), (25.7160, 32.6680)]
B_PRECINCTS = [(25.7140, 32.6605), (25.7140, 32.6645), (25.7100, 32.6640), (25.7105, 32.6600)]
B_SOUTH_MUT = [(25.7090, 32.6550), (25.7090, 32.6620), (25.7052, 32.6610), (25.7056, 32.6545)]
B_RIVERSIDE = [(25.7160, 32.6505), (25.7192, 32.6538), (25.7168, 32.6544), (25.7145, 32.6510)]
B_WEST_AV = [(25.7040, 32.6402), (25.7128, 32.6475), (25.7128, 32.6514), (25.7040, 32.6430)]
B_EAST_AV = [(25.7020, 32.6420), (25.7098, 32.6500), (25.7085, 32.6540), (25.7005, 32.6460)]
B_LUXOR = [(25.6976, 32.6400), (25.7004, 32.6413), (25.6995, 32.6450), (25.6960, 32.6436)]
B_LUXOR_S = [(25.6930, 32.6362), (25.6968, 32.6380), (25.6960, 32.6420), (25.6922, 32.6402)]
B_LUXOR_N = [(25.7012, 32.6385), (25.7036, 32.6400), (25.7030, 32.6418), (25.7012, 32.6408)]
B_FERRY_W = [(25.7175, 32.6420), (25.7210, 32.6420), (25.7210, 32.6448), (25.7175, 32.6440)]
B_RAMESSEUM = [(25.7274, 32.6132), (25.7296, 32.6150), (25.7282, 32.6176), (25.7260, 32.6152)]
B_QURNA = [(25.7340, 32.6296), (25.7356, 32.6296), (25.7356, 32.6330), (25.7334, 32.6330)]
B_HABU = [(25.7172, 32.6040), (25.7180, 32.6070), (25.7160, 32.6076), (25.7150, 32.6046)]
B_VALLEY_TEMPLE = [(25.7348, 32.6182), (25.7366, 32.6196), (25.7354, 32.6216), (25.7336, 32.6200)]
B_MEMNONIA = [(25.7228, 32.6135), (25.7245, 32.6150), (25.7232, 32.6172), (25.7215, 32.6155)]

BLOCKS = [
    # ---- Middle Kingdom: the town round the first temple of Amun
    dict(name="Waset", polygon=B_PRECINCTS, density="dense", periods=["middle-kingdom-1950"]),
    dict(name="Eastern town", polygon=B_EAST, density="dense", periods=["middle-kingdom-1950"]),
    dict(name="Quay hamlet", polygon=B_QUAY, density="loose", periods=["middle-kingdom-1950"]),
    dict(name="Farms south of the town", polygon=B_SOUTH_MUT, density="loose", periods=["middle-kingdom-1950"]),
    dict(name="Village of the southern sanctuary", polygon=B_LUXOR, density="loose", periods=["middle-kingdom-1950"]),
    dict(name="Priests of Mentuhotep's temple", polygon=B_VALLEY_TEMPLE, density="loose", periods=["middle-kingdom-1950"]),
    # ---- Hatshepsut's Thebes
    dict(name="Quarter of the quay", polygon=B_QUAY, density="dense", periods=["hatshepsut-1470"]),
    dict(name="North of the precinct", polygon=B_NORTH, density="loose", periods=["hatshepsut-1470"]),
    dict(name="Eastern town", polygon=B_EAST, density="dense", periods=["hatshepsut-1470"]),
    dict(name="Between the precincts", polygon=B_PRECINCTS, density="dense", periods=["hatshepsut-1470"]),
    dict(name="South of Mut", polygon=B_SOUTH_MUT, density="loose", periods=["hatshepsut-1470"]),
    dict(name="Riverside", polygon=B_RIVERSIDE, density="dense", periods=["hatshepsut-1470"]),
    dict(name="West of the processional way", polygon=B_WEST_AV, density="loose", periods=["hatshepsut-1470"]),
    dict(name="East of the processional way", polygon=B_EAST_AV, density="loose", periods=["hatshepsut-1470"]),
    dict(name="Southern Ipet", polygon=B_LUXOR, density="dense", periods=["hatshepsut-1470"]),
    dict(name="South of Luxor", polygon=B_LUXOR_S, density="loose", periods=["hatshepsut-1470"]),
    dict(name="West-bank landing", polygon=B_FERRY_W, density="loose", periods=["hatshepsut-1470"]),
    dict(name="Builders of Djeser-djeseru", polygon=B_VALLEY_TEMPLE, density="loose", periods=["hatshepsut-1470"]),
    # ---- Ramesside Thebes
    dict(name="Quarter of the quay", polygon=B_QUAY, density="dense", periods=["ramesside-1250"]),
    dict(name="North of the precinct", polygon=B_NORTH, density="dense", periods=["ramesside-1250"]),
    dict(name="Eastern town", polygon=B_EAST, density="dense", periods=["ramesside-1250"]),
    dict(name="Between the precincts", polygon=B_PRECINCTS, density="dense", periods=["ramesside-1250"]),
    dict(name="South of Mut", polygon=B_SOUTH_MUT, density="loose", periods=["ramesside-1250"]),
    dict(name="Riverside", polygon=B_RIVERSIDE, density="dense", periods=["ramesside-1250"]),
    dict(name="West of the processional way", polygon=B_WEST_AV, density="dense", periods=["ramesside-1250"]),
    dict(name="East of the processional way", polygon=B_EAST_AV, density="dense", periods=["ramesside-1250"]),
    dict(name="Southern Ipet", polygon=B_LUXOR, density="dense", periods=["ramesside-1250"]),
    dict(name="South of Luxor", polygon=B_LUXOR_S, density="loose", periods=["ramesside-1250"]),
    dict(name="Luxor landing", polygon=B_LUXOR_N, density="dense", periods=["ramesside-1250"]),
    dict(name="West-bank landing", polygon=B_FERRY_W, density="loose", periods=["ramesside-1250"]),
    dict(name="Staff of the Ramesseum", polygon=B_RAMESSEUM, density="loose", periods=["ramesside-1250"]),
    dict(name="Qurna", polygon=B_QURNA, density="loose", periods=["ramesside-1250"]),
    dict(name="Village by the temple of Amun at Djeme", polygon=B_HABU, density="loose", periods=["ramesside-1250"]),
    dict(name="Valley temple village", polygon=B_VALLEY_TEMPLE, density="loose", periods=["ramesside-1250"]),
    # ---- Late Period: a smaller city after the Assyrian sack
    dict(name="Quarter of the quay", polygon=B_QUAY, density="dense", periods=["late-period-600"]),
    dict(name="North of the precinct", polygon=B_NORTH, density="loose", periods=["late-period-600"]),
    dict(name="Eastern town", polygon=B_EAST, density="dense", periods=["late-period-600"]),
    dict(name="Between the precincts", polygon=B_PRECINCTS, density="dense", periods=["late-period-600"]),
    dict(name="Riverside", polygon=B_RIVERSIDE, density="dense", periods=["late-period-600"]),
    dict(name="West of the processional way", polygon=B_WEST_AV, density="loose", periods=["late-period-600"]),
    dict(name="Southern Ipet", polygon=B_LUXOR, density="dense", periods=["late-period-600"]),
    dict(name="West-bank landing", polygon=B_FERRY_W, density="loose", periods=["late-period-600"]),
    dict(name="Djeme", polygon=B_HABU, density="dense", periods=["late-period-600"]),
    dict(name="Qurna", polygon=B_QURNA, density="loose", periods=["late-period-600"]),
    # ---- Roman: villages among the ruins
    dict(name="Village of Karnak", polygon=B_EAST, density="dense", periods=["roman-200"]),
    dict(name="Village between the precincts", polygon=B_PRECINCTS, density="loose", periods=["roman-200"]),
    dict(name="Quay village", polygon=B_QUAY, density="loose", periods=["roman-200"]),
    dict(name="Village of Luxor", polygon=B_LUXOR, density="dense", periods=["roman-200"]),
    dict(name="Luxor landing", polygon=B_LUXOR_N, density="dense", periods=["roman-200"]),
    dict(name="Outside Djeme", polygon=B_HABU, density="loose", periods=["roman-200"]),
    dict(name="Memnonia", polygon=B_MEMNONIA, density="loose", periods=["roman-200"]),
    dict(name="West-bank landing", polygon=B_FERRY_W, density="loose", periods=["roman-200"]),
]

GARDENS = [
    dict(name="Palm groves of the west", polygon=[(25.7240, 32.6200), (25.7275, 32.6230), (25.7255, 32.6300), (25.7220, 32.6270)], kind="orchard"),
    dict(name="Palm groves by the landing", polygon=[(25.7140, 32.6300), (25.7180, 32.6330), (25.7165, 32.6400), (25.7120, 32.6370)], kind="orchard"),
    dict(name="Gardens of Amun", polygon=[(25.7050, 32.6560), (25.7080, 32.6600), (25.7060, 32.6650), (25.7030, 32.6610)], kind="orchard"),
    dict(name="Vineyard of the west", polygon=[(25.7270, 32.6330), (25.7300, 32.6345), (25.7290, 32.6400), (25.7262, 32.6385)], kind="vineyard", periods=FROM_1470),
    dict(name="Palms of Luxor", polygon=[(25.6935, 32.6440), (25.6975, 32.6465), (25.6960, 32.6510), (25.6920, 32.6485)], kind="orchard"),
    dict(name="Palm groves of Qurna", polygon=[(25.7360, 32.6380), (25.7395, 32.6400), (25.7380, 32.6470), (25.7345, 32.6450)], kind="orchard"),
    dict(name="Palm groves of the southern plain", polygon=[(25.7080, 32.6280), (25.7115, 32.6300), (25.7100, 32.6360), (25.7068, 32.6340)], kind="orchard"),
    dict(name="Orchards by the river", polygon=[(25.7240, 32.6380), (25.7275, 32.6400), (25.7262, 32.6460), (25.7230, 32.6440)], kind="orchard"),
    dict(name="Vineyards of the estate of Amun", polygon=[(25.6935, 32.6530), (25.6970, 32.6550), (25.6955, 32.6600), (25.6920, 32.6580)], kind="vineyard", periods=["hatshepsut-1470", "ramesside-1250", "late-period-600"]),
    dict(name="Gardens north of Karnak", polygon=[(25.7300, 32.6640), (25.7340, 32.6655), (25.7330, 32.6685), (25.7292, 32.6672)], kind="orchard"),
]

MARSH = [
    dict(name="Papyrus thickets", polygon=[(25.7392, 32.6560), (25.7440, 32.6584), (25.7432, 32.6600), (25.7386, 32.6578)]),
    dict(name="Flood basin of the south-west", polygon=[(25.6920, 32.6150), (25.6980, 32.6180), (25.6962, 32.6260), (25.6906, 32.6230)]),
    dict(name="Silted Birket Habu", polygon=[(25.7068, 32.6050), (25.7056, 32.6240), (25.7020, 32.6240), (25.7032, 32.6050)], periods=LATE),
]

DISTRICTS = [
    dict(id="ipet-isut", name="Ipet-isut (Karnak)", polygon=[(25.7225, 32.6545), (25.7225, 32.6665), (25.7095, 32.6665), (25.7095, 32.6525)],
         description="'The most select of places': the temple city of Amun-Ra with the precincts of Montu and Mut, its estates, workshops, granaries and priests' houses, and the old town of Waset round it."),
    dict(id="ipet-resyt", name="Ipet-resyt (Luxor)", polygon=[(25.7040, 32.6370), (25.7040, 32.6430), (25.6920, 32.6440), (25.6920, 32.6350)], periods=FROM_1470,
         description="'The southern sanctuary': the temple where Amun of Karnak came each year at the Opet festival, and the quarter round it. In Roman times a legion camp, later the village of Luxor (al-Uqsur, 'the castles')."),
    dict(id="waset", name="Waset", polygon=[(25.7130, 32.6455), (25.7130, 32.6530), (25.7010, 32.6470), (25.7010, 32.6395)], periods=FROM_1470,
         description="The town along the processional way between the two temples: houses, markets and workshops of the city of Amun, whose full extent is still unknown under modern Luxor."),
    dict(id="west-of-thebes", name="The West of Thebes", polygon=[(25.7420, 32.5980), (25.7420, 32.6200), (25.7160, 32.6200), (25.7160, 32.5980)],
         description="The city of the dead: royal tombs in the valleys, officials' tombs in the foothills, the kings' mortuary temples along the desert edge, and the villages of those who built and served them."),
    dict(id="memnonia", name="Memnonia", polygon=[(25.7300, 32.6000), (25.7300, 32.6180), (25.7160, 32.6180), (25.7160, 32.6000)], periods=["roman-200"],
         description="The Greek name of the west bank, after the 'Memnon' the tourists heard singing; the town of Djeme inside Medinet Habu was its centre."),
]

LABELS = [
    dict(text="Iteru", position=(25.7060, 32.6345), size="lg", rotation=-55, periods=TO_600),
    dict(text="Nile", position=(25.7060, 32.6345), size="lg", rotation=-55, periods=["roman-200"]),
    dict(text="Waset", position=(25.7070, 32.6490), size="lg", periods=["hatshepsut-1470", "ramesside-1250", "late-period-600"]),
    dict(text="Waset", position=(25.7118, 32.6625), size="lg", periods=["middle-kingdom-1950"]),
    dict(text="Diospolis Magna", position=(25.7070, 32.6490), size="lg", periods=["roman-200"]),
    dict(text="Ipet-isut", position=(25.7232, 32.6640), size="md"),
    dict(text="Ipet-resyt", position=(25.6960, 32.6400), size="md", periods=FROM_1470),
    dict(text="The West", position=(25.7240, 32.6260), size="lg", periods=TO_600),
    dict(text="Memnonia", position=(25.7240, 32.6260), size="lg", periods=["roman-200"]),
    dict(text="Djeser-djeseru", position=(25.7340, 32.6110), size="sm", periods=FROM_1470),
    dict(text="Set Maat", position=(25.7300, 32.5990), size="sm", periods=NEW_KINGDOM),
    dict(text="Djeme", position=(25.7155, 32.6060), size="sm", periods=LATE),
    dict(text="Birket Habu", position=(25.7015, 32.6150), size="sm", periods=["ramesside-1250"]),
    dict(text="el-Qurn", position=(25.7300, 32.5965), size="sm", periods=["middle-kingdom-1950", "late-period-600", "roman-200"]),
]
