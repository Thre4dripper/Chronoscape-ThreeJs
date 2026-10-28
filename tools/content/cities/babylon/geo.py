# Babylon: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
ALL = ["hammurabi-1750", "kassite-1300", "nebuchadnezzar-575", "achaemenid-450", "alexander-323"]
EARLY = ["hammurabi-1750", "kassite-1300"]
NEO = ["nebuchadnezzar-575", "achaemenid-450", "alexander-323"]
NEB_ACH = ["nebuchadnezzar-575", "achaemenid-450"]
FROM_KASSITE = ["kassite-1300", "nebuchadnezzar-575", "achaemenid-450", "alexander-323"]

SOURCES = [
    dict(id="koldewey", title="The Excavations at Babylon", author="Robert Koldewey", year=1914, note="trans. Agnes S. Johns of Das wieder erstehende Babylon (1913)", url="https://archive.org/details/excavationsatbab00kolduoft"),
    dict(id="george-btt", title="Babylonian Topographical Texts", author="A. R. George", year=1992, note="Orientalia Lovaniensia Analecta 40; the Tintir list of quarters, gates, streets and temples"),
    dict(id="pedersen-babylon", title="Babylon: The Great City", author="Olof Pedersén", year=2021),
    dict(id="finkel-seymour", title="Babylon: Myth and Reality", author="I. L. Finkel and M. J. Seymour (eds.)", year=2008, note="British Museum exhibition catalogue"),
    dict(id="van-de-mieroop", title="The Ancient Mesopotamian City", author="Marc Van De Mieroop", year=1997),
    dict(id="herodotus", title="Histories, Book 1 (chapters 178–200, Babylon)", author="Herodotus", year="c. 430 BCE", url="https://en.wikipedia.org/wiki/Histories_(Herodotus)"),
    dict(id="wiki-babylon", title="Babylon", author="Wikipedia", url="https://en.wikipedia.org/wiki/Babylon"),
    dict(id="wiki-euphrates", title="Euphrates", author="Wikipedia", url="https://en.wikipedia.org/wiki/Euphrates"),
]

CITY = dict(
    name="Babylon", subtitle="Bābili, the Gate of the Gods",
    description="Babylon on the Euphrates from Hammurabi's city (c. 1750 BCE) to the death of Alexander in Nebuchadnezzar's palace (323 BCE): the rectangular inner city astride the river, its double walls and moat, the outer wall reaching north to the Summer Palace. The earliest eras lie under the water table and are barely excavated, so they are drawn as hedged reconstructions. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="nebuchadnezzar-575",
    world=dict(heightScale=1.0, walls=["#D9C6A0", "#CDB48A", "#E0D2B4", "#C8AE86", "#D4BE98"], roofs=["#C8B58E", "#BCA57E"]),
    camera=dict(target=(32.5395, 44.4225), distance=38),
)

# north-west corner, south-east corner: Babil and the outer wall in the north, the Borsippa road in the south
FRAME = ((32.5640, 44.3970), (32.5175, 44.4530))

PALETTE = dict(parchment="#E9D6AA", ink="#6A4A2E", water="#5E8A8C", hill="#A08A60", road="#8E6C46")
COMPASS = (32.5605, 44.4495)
CARTOUCHE = (32.5185, 44.3985)

PERIODS = [
    dict(id="hammurabi-1750", label="Hammurabi's Babylon", year=-1750, startYear=-1792, endYear=-1595,
         summary="Babylon of the First Dynasty, a town of the Amorite kings until Hammurabi (1792–1750 BCE) made it the capital of all Mesopotamia. Its streets, the first Esagila of Marduk and its walls lie below today's water table and are almost unexcavated: their size and plan are guessed from Neo-Babylonian layout, a few deep soundings in Merkes and contemporary cities. Mud brick and reed, a little baked brick.",
         population="unknown; perhaps 20,000–50,000",
         feel="Reed mats drying on flat roofs, donkeys at the river landing, the drone of scribes copying Sumerian, beer brewed in every house.",
         style="courtyard",
         houses=dict(title="Old Babylonian courtyard houses", text="Single-storey houses of sun-dried brick round a small court, entered from crooked lanes, with a reception room, a kitchen and family burials under the floors. This picture comes mostly from contemporary Ur and Sippar; at Babylon only the deepest pits in Merkes reach these levels."),
         outskirts=dict(title="Palm groves and canals", text="Date-palm gardens with vegetables in their shade, barley fields watered by small canals, threshing floors and reed huts of herders.")),
    dict(id="kassite-1300", label="Kassite Babylon (Karduniash)", year=-1300, startYear=-1594, endYear=-627,
         summary="After the Hittite raid of 1595 the Kassites ruled Babylonia for four centuries and kept Babylon as their capital; the long centuries after them, of Assyrian overlordship and revolt, are folded into this map. The city's quarters, gates and temples were listed in the Tintir text, perhaps compiled in the 12th century; an earlier Etemenanki probably stood by then. Little of Kassite Babylon is excavated beyond houses in Merkes.",
         population="unknown",
         feel="Chariots and horses, a novelty of the Kassites, in the streets; boundary stones carved with gods' symbols; the river traffic of a kingdom at peace.",
         style="courtyard",
         houses=dict(title="Kassite houses in Merkes", text="Koldewey's deep trenches in Merkes found Kassite-period houses of mud brick on the same lines as later ones: rooms round a court, thick walls, a door to the lane and no windows outside. The picture beyond Merkes is inferred."),
         outskirts=dict(title="Fields of Karduniash", text="Irrigated barley, sesame and palm gardens along canals, estates granted by kings and recorded on carved boundary stones (kudurru).")),
    dict(id="nebuchadnezzar-575", label="Nebuchadnezzar's city", year=-575, startYear=-626, endYear=-539,
         summary="Nabopolassar (626–605) and his son Nebuchadnezzar II (605–562), enriched by conquest from Egypt's border to the Gulf, rebuild Babylon in baked brick and bitumen: the double walls and moat, the Ishtar Gate in blue glaze, the Processional Way, the palaces, Etemenanki and Esagila restored, a bridge on stone piers, and an outer wall enclosing the Summer Palace. Perhaps the largest city in the world.",
         population="perhaps 100,000–200,000",
         feel="Kilns smoking outside the walls, bricks stamped with the king's name, glazed lions shining along the Processional Way, Aramaic, Akkadian and Hebrew in the same streets.",
         style="courtyard",
         houses=dict(title="Houses of Merkes", text="Koldewey's excavated quarter east of the Processional Way: blocks of mud-brick houses round courts, the bigger ones with several courts, walls toothed in shallow steps along irregular lanes, flat roofs of palm beams, mats and earth; doors and drains to the street."),
         outskirts=dict(title="The outer city and the palm groves", text="Between the inner and outer walls, houses thin out into gardens, kilns and estates; beyond them palm groves line the canals.")),
    dict(id="achaemenid-450", label="Babylon under the Persians", year=-450, startYear=-538, endYear=-332,
         summary="Cyrus took Babylon in 539 without a battle; it became a royal residence of the Persian kings, with a columned pavilion added to the Southern Palace. After the revolts of 484 Xerxes punished the city: some walls were breached and Marduk's cult was curbed (how badly is debated). Herodotus' description, perhaps from c. 450, exaggerates its size but shows it still great and crowded.",
         population="perhaps 100,000 or more",
         feel="Persian guards at the palace gate, temple scribes still keeping their archives in Akkadian, merchants' boats from Armenia unloading wine on the quays.",
         style="courtyard",
         houses=dict(title="Houses of three and four storeys?", text="Herodotus says Babylon was full of houses of three and four storeys and straight streets running to the river. Excavated houses are mostly of one storey round courts, but some had upper rooms; his account mixes eyewitness and hearsay."),
         outskirts=dict(title="Gardens and estates", text="Palm groves, fields and the estates of Persian nobles and of business houses like the Murashu of Nippur; canals and kilns between the walls.")),
    dict(id="alexander-323", label="Alexander's Babylon", year=-323, startYear=-331, endYear=-275,
         summary="Alexander entered Babylon in October 331 BCE and planned to make it the capital of his empire. He set men to clear the ruined Etemenanki for rebuilding, a work never finished, and died in Nebuchadnezzar's palace in June 323. Under the Seleucids a Greek theatre rose on the rubble mound of Homera, but the founding of Seleucia on the Tigris drew people away.",
         population="still large; falling after c. 300 BCE",
         feel="Macedonian veterans in the palace courts, Babylonian priests reading omens on the roofs, the dust of brick rubble carted away from the ruined tower.",
         style="courtyard",
         houses=dict(title="Old houses, new neighbours", text="The same mud-brick courtyard houses of Merkes, repaired and rebuilt on their old lines; Greek soldiers and settlers lodged among Babylonians, and a few houses gained Greek-style peristyle courts later."),
         outskirts=dict(title="Fields and the emptying outer city", text="Gardens, fields and dwindling hamlets between the walls; palm groves along the canals as before.")),
]

# ---------------------------------------------------------------- the Euphrates (Purattu; the Arahtu channel at Babylon)
RIVER = [(32.5650, 44.4248), (32.5600, 44.4230), (32.5550, 44.4207), (32.5500, 44.4186), (32.5460, 44.4171), (32.5420, 44.4161),
         (32.5380, 44.4164), (32.5343, 44.4170), (32.5300, 44.4168), (32.5250, 44.4156), (32.5200, 44.4140), (32.5160, 44.4125)]

RIVER_BLURB = "The Euphrates (Akkadian Purattu; the channel at Babylon was called the Arahtu) then ran through the middle of the city, splitting it in two and feeding the moats and canals. Nabopolassar and Nebuchadnezzar lined it with baked-brick quays. It later shifted west of the ruins; its earliest course is unknown."

WATER = [
    dict(id="euphrates", name="Purattu (Euphrates), the Arahtu", path=RIVER, width=150, blurb=RIVER_BLURB),
    dict(id="moat-east", name="Moat of the eastern city", path=[(32.5443, 44.4246), (32.5443, 44.4356), (32.5283, 44.4356), (32.5283, 44.4172)], width=55, periods=NEO,
         blurb="Nabopolassar and Nebuchadnezzar ringed the double inner wall with a moat fed from the Euphrates, its banks faced with baked brick set in bitumen. Its width is estimated at 50–80 metres."),
    dict(id="moat-west", name="Moat of the western city", path=[(32.5443, 44.4156), (32.5443, 44.4066), (32.5283, 44.4066), (32.5283, 44.4150)], width=50, periods=NEO,
         blurb="The moat continued round the western half of the city; its line here is drawn from the excavated wall trace and is approximate."),
    dict(id="libil-hegalla", name="Libil-ḫegalla, the eastern canal", path=[(32.5505, 44.4190), (32.5482, 44.4248), (32.5458, 44.4278), (32.5430, 44.4281), (32.5380, 44.4281), (32.5330, 44.4281), (32.5283, 44.4281)],
         width=24, periods=NEO,
         blurb="'May it bring abundance': the canal of the eastern city, which Nabopolassar and Nebuchadnezzar say they re-dug and lined with baked brick. It ran from the Euphrates north of the city through the eastern quarters; its exact course is not known."),
    dict(id="libil-hegalla", name="Eastern canal (Libil-ḫegalla?)", path=[(32.5505, 44.4190), (32.5482, 44.4248), (32.5458, 44.4278), (32.5430, 44.4281), (32.5380, 44.4281), (32.5330, 44.4281), (32.5283, 44.4281)],
         width=20, periods=EARLY,
         blurb="Babylon's eastern canal is named in texts long before Nebuchadnezzar; that it already ran on this line in the second millennium is a guess."),
    dict(id="moat-outer", name="Moat of the outer wall", path=[(32.5622, 44.4236), (32.5622, 44.4288), (32.5552, 44.4458), (32.5297, 44.4436), (32.5232, 44.4302), (32.5207, 44.4155)], width=45, periods=NEO,
         blurb="Nebuchadnezzar's outer wall had its own moat, fed from the river at both ends, so that the eastern suburbs could be flooded against an attacker."),
]

HILLS = [
    dict(id="homera", name="Homera (the rubble of Etemenanki)", center=(32.5422, 44.4310), radius=80, periods=["alexander-323"],
         blurb="A mound of broken baked brick in the north-east of the city. Strabo and Arrian say Alexander had the ruined tower's debris cleared; the rubble seems to have been dumped here, and the Greek theatre was later built against it."),
]

ROADS = [
    # ---- Neo-Babylonian and later
    dict(id="processional-way", name="Ay-ibur-šabû, the Processional Way", path=[(32.5555, 44.4226), (32.5500, 44.4224), (32.5455, 44.4223), (32.5436, 44.4222), (32.5412, 44.4223), (32.5398, 44.4236),
                                                                               (32.5385, 44.4237), (32.5346, 44.4237), (32.5343, 44.4210), (32.5343, 44.4181)],
         width=20, style="major", labelled=True, periods=NEO,
         blurb="'May the arrogant not prevail', the usual translation of its name: the sacred road of Marduk from the Akitu house north of the city through the Ishtar Gate, south past the palace and the ziggurat, then west between Etemenanki and Esagila to the bridge. Nebuchadnezzar raised and paved it."),
    dict(id="west-street", name="Street of Adad (to the Adad Gate)", path=[(32.5343, 44.4159), (32.5343, 44.4120), (32.5343, 44.4076)], width=12, style="major", periods=NEO,
         blurb="From the bridge across the western city to its west gate. Street names are known from the Tintir list; which street ran where is approximate."),
    dict(id="borsippa-road", name="Road to Borsippa", path=[(32.5343, 44.4076), (32.5300, 44.4040), (32.5240, 44.4012), (32.5178, 44.3990)], width=12, style="major", labelled=True, periods=NEO,
         blurb="South-west to Borsippa, the city of Nabu, Marduk's son, about 17 km away. At the New Year Nabu's statue came up this road by boat and on foot to visit his father."),
    dict(id="marduk-street", name="Street of Marduk", path=[(32.5395, 44.4345), (32.5395, 44.4285), (32.5395, 44.4240)], width=12, style="major", labelled=True, periods=NEO,
         blurb="From the Marduk Gate in the east wall into the heart of the city. The eastern quarters were cut by streets running roughly at right angles, as Herodotus noticed."),
    dict(id="zababa-street", name="Street of Zababa", path=[(32.5335, 44.4345), (32.5335, 44.4285), (32.5335, 44.4240)], width=10, style="minor", periods=NEO,
         blurb="From the Zababa Gate toward Esagila; named, like the gate, for the war god of Kish."),
    dict(id="enlil-street", name="Street of the Enlil Gate", path=[(32.5292, 44.4255), (32.5320, 44.4255), (32.5338, 44.4248)], width=10, style="minor", periods=NEO,
         blurb="North from the south gate through Šuanna to Esagila's forecourt."),
    dict(id="merkes-street", name="Street through Merkes", path=[(32.5434, 44.4257), (32.5398, 44.4257)], width=8, style="minor", periods=NEO,
         blurb="One of the excavated lanes of Merkes, a few metres wide, between blocks of courtyard houses."),
    dict(id="shamash-street", name="Street of Šamaš", path=[(32.5390, 44.4076), (32.5390, 44.4150)], width=9, style="minor", periods=NEO,
         blurb="From the Šamaš Gate east to the river quays of the western city."),
    dict(id="kish-road", name="Road to Kish", path=[(32.5395, 44.4357), (32.5405, 44.4400), (32.5410, 44.4435), (32.5425, 44.4528)], width=12, style="major", labelled=True, periods=NEO,
         blurb="East through the outer wall to Kish, about 15 km away, and on to the Tigris and Elam."),
    dict(id="sippar-road", name="Road to Kutha and Sippar", path=[(32.5436, 44.4305), (32.5500, 44.4320), (32.5570, 44.4345), (32.5638, 44.4370)], width=10, style="major", periods=NEO,
         blurb="North from the Sin Gate toward Kutha and Sippar, the city of the sun god."),
    dict(id="babil-road", name="Road to the Summer Palace", path=[(32.5555, 44.4226), (32.5578, 44.4240), (32.5586, 44.4250)], width=10, style="minor", periods=NEO,
         blurb="The road along the river to the palace at the northern tip of the outer city."),
    dict(id="south-road", name="Road to Dilbat and Nippur", path=[(32.5292, 44.4255), (32.5240, 44.4262), (32.5178, 44.4270)], width=10, style="major", periods=NEO,
         blurb="South from the Enlil Gate to Dilbat and on to Nippur, the old holy city of Enlil."),
    # ---- the second millennium (hedged)
    dict(id="early-sacred-way", name="Sacred way to Esagila", path=[(32.5480, 44.4222), (32.5440, 44.4222), (32.5410, 44.4228), (32.5380, 44.4234), (32.5345, 44.4232)], width=12, style="major", labelled=True, periods=EARLY,
         blurb="A processional road to Marduk's temple surely existed before Nebuchadnezzar, but its course and gates are not known; it is drawn on the line of the later Processional Way."),
    dict(id="early-kish-road", name="Road to Kish", path=[(32.5380, 44.4240), (32.5385, 44.4320), (32.5400, 44.4420), (32.5425, 44.4528)], width=9, style="major", periods=EARLY,
         blurb="Kish, an older royal city than Babylon, lay 15 km east."),
    dict(id="early-borsippa-road", name="Road to Borsippa", path=[(32.5343, 44.4140), (32.5300, 44.4060), (32.5240, 44.4012), (32.5178, 44.3990)], width=9, style="major", periods=EARLY,
         blurb="Hammurabi rebuilt Ezida, Nabu's temple at Borsippa; the road left the west bank toward it."),
    dict(id="early-sippar-road", name="Road to Sippar", path=[(32.5420, 44.4250), (32.5500, 44.4300), (32.5638, 44.4370)], width=9, style="major", periods=EARLY,
         blurb="North to Sippar, where the stele of Hammurabi's laws may first have stood in the temple of Šamaš."),
    dict(id="early-river-lane", name="Lane to the landing", path=[(32.5360, 44.4232), (32.5352, 44.4200), (32.5345, 44.4181)], width=8, style="minor", periods=EARLY,
         blurb="From the temple quarter down to the river landing, where a ferry crossed to the west bank."),
]

INNER_EAST = [(32.5436, 44.4186), (32.5436, 44.4345), (32.5292, 44.4345), (32.5292, 44.4180), (32.5408, 44.4180), (32.5410, 44.4186)]
INNER_WEST = [(32.5436, 44.4152), (32.5436, 44.4075), (32.5292, 44.4075), (32.5292, 44.4150)]

WALLS = [
    dict(id="inner-wall-east", name="Imgur-Enlil and Nemetti-Enlil (eastern city)", path=INNER_EAST, closed=True, periods=NEO,
         blurb="The double inner wall: Imgur-Enlil, the main wall about 6.5 m thick, and Nemetti-Enlil, the outer wall about 3.7 m thick, with a military road between and towers every 20 m or so, rebuilt in baked brick by Nabopolassar and Nebuchadnezzar. Gate positions other than the Ishtar Gate are approximate."),
    dict(id="inner-wall-west", name="Imgur-Enlil and Nemetti-Enlil (western city)", path=INNER_WEST, closed=True, periods=NEO,
         blurb="The western half of the double wall, with the Šamaš, Adad and Lugalirra gates in the Tintir list; its line is known from Koldewey's soundings and the mounds."),
    dict(id="outer-wall", name="Outer wall of Nebuchadnezzar", path=[(32.5615, 44.4236), (32.5615, 44.4285), (32.5545, 44.4448), (32.5300, 44.4425), (32.5240, 44.4300), (32.5215, 44.4162)],
         closed=False, periods=NEO,
         blurb="A triple rampart of baked and mud brick built by Nebuchadnezzar from the Summer Palace in the north round the east of the city to the river in the south, enclosing the outer city, with a moat. The line drawn is simplified; part lies beyond the map."),
    dict(id="inner-wall-east", name="Imgur-Enlil (earlier phase, eastern city)", path=INNER_EAST, closed=True, periods=["kassite-1300"],
         blurb="The Tintir list, probably of the 12th century, already names the city's eight gates and quarters, so the inner city's lines may be this old; how much of the wall then stood on this trace is not known."),
    dict(id="inner-wall-west", name="Imgur-Enlil (earlier phase, western city)", path=INNER_WEST, closed=True, periods=["kassite-1300"],
         blurb="The western circuit in the Kassite period: a guess on the later line."),
    dict(id="old-wall", name="Wall of Sumu-la-El and Hammurabi (conjectural)", path=[(32.5428, 44.4186), (32.5428, 44.4300), (32.5300, 44.4300), (32.5300, 44.4180), (32.5408, 44.4180)],
         closed=True, periods=["hammurabi-1750"],
         blurb="Year names record that Sumu-la-El (c. 1880–1845) built the 'great wall of Babylon' and that Hammurabi repaired it. Its line is unknown; drawn here as a smaller circuit round the east-bank temple quarter."),
    dict(id="temenos-wall", name="Wall of the Etemenanki precinct", path=[(32.5382, 44.4190), (32.5382, 44.4232), (32.5348, 44.4232), (32.5348, 44.4190)], closed=True, periods=NEO,
         blurb="The ziggurat stood in a walled court about 400 m square, lined with rooms and store chambers and entered by a dozen gates; it is drawn smaller here."),
]

GATES = [
    dict(id="sin-gate", name="Sin Gate", position=(32.5436, 44.4305), periods=NEO),
    dict(id="marduk-gate", name="Marduk Gate", position=(32.5395, 44.4345), periods=NEO),
    dict(id="zababa-gate", name="Zababa Gate", position=(32.5335, 44.4345), periods=NEO),
    dict(id="enlil-gate", name="Enlil Gate", position=(32.5292, 44.4255), periods=NEO),
    dict(id="urash-gate", name="Uraš Gate", position=(32.5292, 44.4112), periods=NEO),
    dict(id="shamash-gate", name="Šamaš Gate", position=(32.5390, 44.4075), periods=NEO),
    dict(id="adad-gate", name="Adad Gate", position=(32.5343, 44.4075), periods=NEO),
    dict(id="lugalirra-gate", name="Lugalirra Gate", position=(32.5436, 44.4110), periods=NEO),
]

BRIDGES = [
    dict(id="euphrates-bridge", name="Bridge over the Euphrates", path=[(32.5343, 44.4181), (32.5343, 44.4159)], build="stone", arches=8, landmarkId="euphrates-bridge", periods=NEO,
         blurb="The bridge joining the two halves of the city, on boat-shaped piers of baked brick and stone; Herodotus says its timber deck was taken up at night against thieves."),
]

BLOCKS = [
    # ---- the second millennium: a smaller east-bank city round Esagila (conjectural)
    dict(name="Old Babylonian quarter (Merkes, deep levels)", polygon=[(32.5424, 44.4240), (32.5424, 44.4296), (32.5390, 44.4296), (32.5390, 44.4240)], density="dense", periods=["hammurabi-1750"]),
    dict(name="Quarter round Esagila", polygon=[(32.5385, 44.4185), (32.5385, 44.4296), (32.5350, 44.4296), (32.5350, 44.4238), (32.5340, 44.4238), (32.5340, 44.4185)], density="dense", periods=["hammurabi-1750"]),
    dict(name="Southern quarter", polygon=[(32.5326, 44.4185), (32.5326, 44.4296), (32.5304, 44.4296), (32.5304, 44.4185)], density="loose", periods=["hammurabi-1750"]),
    dict(name="North of the temples", polygon=[(32.5424, 44.4186), (32.5424, 44.4232), (32.5390, 44.4232), (32.5390, 44.4186)], density="dense", periods=["hammurabi-1750"]),
    dict(name="West-bank hamlets", polygon=[(32.5410, 44.4090), (32.5410, 44.4148), (32.5320, 44.4148), (32.5320, 44.4090)], density="loose", periods=["hammurabi-1750"]),
    # ---- Kassite: the inner city of the Tintir list, less densely built
    dict(name="Ka-dingirra", polygon=[(32.5432, 44.4186), (32.5432, 44.4276), (32.5398, 44.4276), (32.5398, 44.4186)], density="dense", periods=["kassite-1300"]),
    dict(name="Eridu", polygon=[(32.5392, 44.4186), (32.5392, 44.4276), (32.5340, 44.4276), (32.5340, 44.4186)], density="dense", periods=["kassite-1300"]),
    dict(name="Šuanna", polygon=[(32.5328, 44.4184), (32.5328, 44.4276), (32.5296, 44.4276), (32.5296, 44.4184)], density="dense", periods=["kassite-1300"]),
    dict(name="Eastern quarters", polygon=[(32.5432, 44.4286), (32.5432, 44.4340), (32.5296, 44.4340), (32.5296, 44.4286)], density="loose", periods=["kassite-1300"]),
    dict(name="Kumar", polygon=[(32.5432, 44.4080), (32.5432, 44.4148), (32.5392, 44.4148), (32.5392, 44.4080)], density="dense", periods=["kassite-1300"]),
    dict(name="Tuba", polygon=[(32.5387, 44.4080), (32.5387, 44.4148), (32.5296, 44.4148), (32.5296, 44.4080)], density="loose", periods=["kassite-1300"]),
    # ---- the inner city, 575-323
    dict(name="Merkes (Ka-dingirra)", polygon=[(32.5432, 44.4243), (32.5432, 44.4276), (32.5398, 44.4276), (32.5398, 44.4243)], density="dense", periods=NEO),
    dict(name="South of the palace", polygon=[(32.5407, 44.4183), (32.5407, 44.4231), (32.5386, 44.4231), (32.5386, 44.4183)], density="dense", periods=NEO),
    dict(name="New City (Ālu-eššu)", polygon=[(32.5432, 44.4286), (32.5432, 44.4340), (32.5398, 44.4340), (32.5398, 44.4286)], density="dense", periods=NEB_ACH),
    dict(name="New City (Ālu-eššu)", polygon=[(32.5408, 44.4286), (32.5408, 44.4340), (32.5398, 44.4340), (32.5398, 44.4286)], density="loose", periods=["alexander-323"]),
    dict(name="Eridu", polygon=[(32.5391, 44.4243), (32.5391, 44.4276), (32.5339, 44.4276), (32.5339, 44.4243)], density="dense", periods=NEO),
    dict(name="TE.E", polygon=[(32.5391, 44.4286), (32.5391, 44.4340), (32.5339, 44.4340), (32.5339, 44.4286)], density="dense", periods=NEO),
    dict(name="Šuanna", polygon=[(32.5326, 44.4183), (32.5326, 44.4276), (32.5296, 44.4276), (32.5296, 44.4183)], density="dense", periods=NEO),
    dict(name="Kullab", polygon=[(32.5331, 44.4286), (32.5331, 44.4340), (32.5296, 44.4340), (32.5296, 44.4286)], density="dense", periods=NEO),
    dict(name="Kumar", polygon=[(32.5432, 44.4080), (32.5432, 44.4148), (32.5394, 44.4148), (32.5394, 44.4080)], density="dense", periods=NEO),
    dict(name="Tuba", polygon=[(32.5386, 44.4080), (32.5386, 44.4148), (32.5347, 44.4148), (32.5347, 44.4080)], density="dense", periods=NEO),
    dict(name="Tuba (south)", polygon=[(32.5339, 44.4080), (32.5339, 44.4148), (32.5296, 44.4148), (32.5296, 44.4080)], density="dense", periods=NEB_ACH),
    dict(name="Tuba (south)", polygon=[(32.5339, 44.4080), (32.5339, 44.4148), (32.5296, 44.4148), (32.5296, 44.4080)], density="loose", periods=["alexander-323"]),
    # ---- the outer city between the walls
    dict(name="Outer city, north-east", polygon=[(32.5560, 44.4300), (32.5530, 44.4405), (32.5455, 44.4415), (32.5455, 44.4310)], density="loose", periods=NEO),
    dict(name="Outer city, east", polygon=[(32.5428, 44.4372), (32.5428, 44.4420), (32.5312, 44.4410), (32.5312, 44.4372)], density="loose", periods=NEO),
    dict(name="Outer city, south", polygon=[(32.5274, 44.4192), (32.5274, 44.4360), (32.5258, 44.4320), (32.5236, 44.4200)], density="loose", periods=NEO),
    # ---- villages across the river and outside the walls
    dict(name="Villages of the west bank", polygon=[(32.5268, 44.4045), (32.5268, 44.4110), (32.5225, 44.4110), (32.5225, 44.4045)], density="loose"),
    dict(name="Hamlets by the Kish road", polygon=[(32.5455, 44.4462), (32.5455, 44.4520), (32.5418, 44.4520), (32.5418, 44.4462)], density="loose"),
]

GARDENS = [
    dict(name="Palm groves of the west bank", polygon=[(32.5610, 44.3985), (32.5610, 44.4150), (32.5470, 44.4140), (32.5470, 44.3985)], kind="orchard"),
    dict(name="Palm groves toward Borsippa", polygon=[(32.5268, 44.3985), (32.5268, 44.4030), (32.5190, 44.4060), (32.5190, 44.3985)], kind="orchard"),
    dict(name="Gardens of the outer city", polygon=[(32.5545, 44.4235), (32.5545, 44.4290), (32.5480, 44.4300), (32.5470, 44.4250)], kind="orchard", periods=NEO),
    dict(name="Palm gardens east of the city", polygon=[(32.5560, 44.4270), (32.5560, 44.4430), (32.5310, 44.4430), (32.5310, 44.4360)], kind="orchard", periods=EARLY),
    dict(name="Palm gardens north of the city", polygon=[(32.5600, 44.4232), (32.5600, 44.4262), (32.5450, 44.4262), (32.5450, 44.4232)], kind="orchard", periods=EARLY),
    dict(name="Fields beyond the outer wall", polygon=[(32.5580, 44.4470), (32.5580, 44.4525), (32.5470, 44.4525), (32.5470, 44.4475)], kind="orchard"),
    dict(name="Fields to the south", polygon=[(32.5215, 44.4290), (32.5215, 44.4450), (32.5185, 44.4450), (32.5185, 44.4290)], kind="orchard"),
]

MARSH = [
    dict(name="Reed beds", polygon=[(32.5215, 44.4120), (32.5215, 44.4150), (32.5185, 44.4140), (32.5185, 44.4110)]),
]

DISTRICTS = [
    dict(id="ka-dingirra", name="Ka-dingirra", polygon=[(32.5436, 44.4182), (32.5436, 44.4280), (32.5398, 44.4280), (32.5398, 44.4182)], periods=FROM_KASSITE,
         description="'Gate of the gods', the quarter by the Ishtar Gate with the Southern Palace and, east of the Processional Way, the houses of Merkes. Quarter names are from the Tintir list; their boundaries are approximate."),
    dict(id="eridu", name="Eridu", polygon=[(32.5396, 44.4182), (32.5396, 44.4280), (32.5328, 44.4280), (32.5328, 44.4182)], periods=FROM_KASSITE,
         description="The holy heart of Babylon, named after the ancient southern city of Ea: Esagila, Etemenanki and a cluster of smaller temples."),
    dict(id="shuanna", name="Šuanna", polygon=[(32.5328, 44.4182), (32.5328, 44.4280), (32.5292, 44.4280), (32.5292, 44.4182)], periods=FROM_KASSITE,
         description="The southern quarter of the eastern city, an old name sometimes used for Babylon itself; temples of Adad and others stood here."),
    dict(id="new-city", name="New City (Ālu-eššu)", polygon=[(32.5436, 44.4280), (32.5436, 44.4345), (32.5395, 44.4345), (32.5395, 44.4280)], periods=FROM_KASSITE,
         description="The north-eastern quarter of the eastern city. In Seleucid times the Greek theatre and later a gymnasium stood at its southern edge on the Homera mound."),
    dict(id="tee", name="TE.E", polygon=[(32.5395, 44.4280), (32.5395, 44.4345), (32.5335, 44.4345), (32.5335, 44.4280)], periods=FROM_KASSITE,
         description="A quarter of the eastern city whose name is written only in Sumerian signs; its reading and exact extent are uncertain."),
    dict(id="kullab", name="Kullab", polygon=[(32.5335, 44.4280), (32.5335, 44.4345), (32.5292, 44.4345), (32.5292, 44.4280)], periods=FROM_KASSITE,
         description="The south-eastern quarter, with the temple of Ninurta near the Zababa and Enlil gates; named after the quarter of Uruk."),
    dict(id="kumar", name="Kumar", polygon=[(32.5436, 44.4075), (32.5436, 44.4152), (32.5365, 44.4152), (32.5365, 44.4075)], periods=FROM_KASSITE,
         description="The northern quarter of the western city across the river; texts place a temple of Ninurta's wife and dwelling quarters here."),
    dict(id="tuba", name="Tuba", polygon=[(32.5365, 44.4075), (32.5365, 44.4152), (32.5292, 44.4152), (32.5292, 44.4075)], periods=FROM_KASSITE,
         description="The southern quarter of the western city, reached from Esagila by the bridge; little excavated, as the river has since shifted over part of it."),
]

LABELS = [
    dict(text="Purattu", position=(32.5575, 44.4210), size="lg", rotation=-70),
    dict(text="Purattu", position=(32.5232, 44.4146), size="md", rotation=-72),
    dict(text="Bābili", position=(32.5268, 44.4385), size="lg", periods=NEO),
    dict(text="Bābili", position=(32.5440, 44.4380), size="lg", periods=EARLY),
    dict(text="Libil-ḫegalla", position=(32.5478, 44.4258), size="sm", rotation=-35, periods=NEO),
    dict(text="to Kish", position=(32.5432, 44.4495), size="sm", rotation=-10),
    dict(text="to Borsippa", position=(32.5210, 44.4005), size="sm", rotation=60),
    dict(text="to Kutha and Sippar", position=(32.5612, 44.4385), size="sm", rotation=-70),
    dict(text="Homera", position=(32.5428, 44.4322), size="sm", periods=["alexander-323"]),
    dict(text="Palm groves", position=(32.5560, 44.4060), size="sm"),
]
