# Carthage: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
# The peninsula between the Gulf of Tunis and the Lake of Tunis: the Byrsa hill in the middle, the two
# Punic harbours and the Tophet at Salammbo to the south, the Megara suburb and the cliff of Sidi Bou Said
# to the north, from the Punic city of the 5th century BCE to the deserted site of about 1600.
import math

P400 = ["punic-400"]
P150 = ["punic-150"]
PUNIC = ["punic-400", "punic-150"]
ROMAN = ["roman-200"]
LATE = ["vandal-480"]
ROM_LATE = ["roman-200", "vandal-480"]
RUINS = ["ruins-1600"]
LATER = ["punic-150", "roman-200", "vandal-480", "ruins-1600"]
ANTIQUE = PUNIC + ROM_LATE
ALL = ANTIQUE + RUINS

# The Roman street grid (and, roughly, the late Punic grid of the coastal plain before it) is turned
# about 30 degrees from north, parallel to the shore. UV(u, v) gives (lat, lon) for a point u metres
# along the decumani (east-south-east, toward the sea) and v metres along the cardines
# (north-north-east) from the centre of the Byrsa summit.
P0 = (36.8528, 10.3237)
KX, KY = 111320.0 * math.cos(math.radians(36.853)), 110950.0
CA, SA = math.cos(math.radians(30)), 0.5


def UV(u, v):
    e = CA * u + SA * v
    n = -SA * u + CA * v
    return (round(P0[0] + n / KY, 5), round(P0[1] + e / KX, 5))


def TOUV(p):
    e, n = (p[1] - P0[1]) * KX, (p[0] - P0[0]) * KY
    return (CA * e - SA * n, SA * e + CA * n)


def Q(u0, u1, v0, v1):
    """A block of the grid between u0..u1 and v0..v1."""
    return [UV(u0, v0), UV(u1, v0), UV(u1, v1), UV(u0, v1)]


def LINE(pts):
    return [UV(u, v) for u, v in pts]


def OFF(pts, d):
    """The polyline moved d metres to the right of its direction of travel (negative: to the left)."""
    out = []
    for i, (lat, lon) in enumerate(pts):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
        de, dn = (b[1] - a[1]) * KX, (b[0] - a[0]) * KY
        L = math.hypot(de, dn) or 1.0
        out.append((round(lat - de / L * d / KY, 5), round(lon + dn / L * d / KX, 5)))
    return out


# the shore of the Gulf of Tunis, south (the Taenia at Le Kram) to north (round the cape of Sidi Bou Said)
SHORE = [(36.8250, 10.3110), (36.8290, 10.3158), (36.8330, 10.3200), (36.8365, 10.3236), (36.8395, 10.3260), (36.8420, 10.3277),
         (36.8450, 10.3293), (36.8485, 10.3318), (36.8515, 10.3343), (36.8545, 10.3368), (36.8570, 10.3393), (36.8603, 10.3402),
         (36.8638, 10.3392), (36.8656, 10.3415), (36.8664, 10.3462), (36.8678, 10.3508), (36.8698, 10.3540), (36.8724, 10.3553),
         (36.8748, 10.3536), (36.8772, 10.3500), (36.8800, 10.3450)]
# the north shore of the Lake of Tunis, east (the Taenia) to west
SHORE_SMOOTH = [(36.8200, 10.3060), (36.8395, 10.3260), (36.8545, 10.3368), (36.8603, 10.3402), (36.8700, 10.3545), (36.8800, 10.3450), (36.8850, 10.3380)]
LAKE_SHORE = [(36.8235, 10.3085), (36.8290, 10.3112), (36.8335, 10.3092), (36.8372, 10.3063), (36.8402, 10.3028), (36.8422, 10.2985), (36.8440, 10.2930)]
SH_UV = sorted((TOUV(p)[1], TOUV(p)[0]) for p in SHORE[2:11])


def SHU(v, inset=60):
    """u of the shore at grid row v (between the harbours and the Antonine Baths), less an inset."""
    for (v0, u0), (v1, u1) in zip(SH_UV, SH_UV[1:]):
        if v0 <= v <= v1:
            return u0 + (u1 - u0) * (v - v0) / (v1 - v0) - inset
    return (SH_UV[0][1] if v < SH_UV[0][0] else SH_UV[-1][1]) - inset


def QS(u0, v0, v1, inset=60):
    """A grid block from u0 east to the shore."""
    return [UV(u0, v0), UV(SHU(v0, inset), v0), UV(SHU(v1, inset), v1), UV(u0, v1)]


# centres of the two harbours (grid coordinates as in landmarks.py)
ROUND_UV, RECT_UV = (457, -594), (679, -985)
ROUND_C, RECT_C = UV(*ROUND_UV), UV(*RECT_UV)

CITY = dict(
    name="Carthage", subtitle="Qart-hadasht, the New City",
    description="Carthage from the Punic city of the 5th century BCE to the deserted site of about 1600: the peninsula between the Gulf of Tunis and the Lake of Tunis, with the Byrsa hill, the rectangular and circular harbours and the Tophet at Salammbo, the Megara suburb and the cliff of Sidi Bou Said, and Roman Carthage laid out over the ruins. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="punic-150",
    world=dict(heightScale=1.0, walls=["#ECE3CF", "#E0D2B4", "#E8DCC2", "#D3C19E", "#F0E9DA"], roofs=["#CDBB96", "#BFAA82"]),
    camera=dict(target=(36.8500, 10.3262), distance=40, maxDistance=140),
)
FRAME = ((36.8760, 10.3020), (36.8310, 10.3580))
RESOLUTION = 4096
PALETTE = dict(parchment="#E9D7AE", ink="#6A4A32", water="#5A8A92", hill="#7E7C58", road="#8A6A4A")
COMPASS = (36.8360, 10.3520)
CARTOUCHE = (36.8318, 10.3028)

PERIODS = [
    dict(id="punic-400", label="Punic Carthage", year=-400, startYear=-550, endYear=-265,
         summary="The Phoenician colony of Tyre, founded by tradition in 814 BCE, is now the head of an empire of trading posts from Sardinia to Spain, ruled by suffetes, a council and the people's assembly. The citadel and temple of Eshmun crown the Byrsa; the city spreads over the plain to the sea wall, with the Tophet and an older harbour at Salammbo. Sandstone, mud brick, white stucco.",
         population="perhaps 100,000–200,000; ancient figures are guesses",
         feel="Phoenician, Libyan and Greek in the streets, purple vats stinking by the shore, and incense and drums at the sanctuaries.",
         style="courtyard",
         houses=dict(title="Punic houses", text="Houses of two or more storeys round a central court with a cistern beneath, walls of rubble and mud brick on sandstone footings, white stucco, flat roofs, floors of red mortar studded with white stone chips (pavimentum punicum), and a narrow corridor from the street."),
         outskirts=dict(title="Megara: gardens and estates", text="North of the city, inside the walls, the Megara: market gardens, orchards and vineyards cut by hedges and irrigation channels, with country houses of the rich. Tombs on the hills of Juno and Byrsa's flanks.")),
    dict(id="punic-150", label="The Punic city, 150 BCE", year=-150, startYear=-264, endYear=-146,
         summary="Beaten twice by Rome and stripped of its empire, Carthage is still rich: it paid off its war debt early, and Hannibal as suffete (196) reformed its finances. The circular naval harbour, probably dug in these decades, holds its 220 ship sheds; new houses climb the Byrsa slope. In 149 Rome declares war, and in 146 the city is taken street by street and burned.",
         population="perhaps 150,000–250,000; Strabo's 700,000 is not believed",
         feel="Shipwrights' mallets in the closed harbour, merchants' scales in the agora, and from 149 the thud of Roman rams against the walls.",
         style="courtyard",
         houses=dict(title="Houses of the Byrsa slope", text="On the Byrsa the 'Hannibal quarter': houses on a regular plan, each with a court, a basin, a bottle-shaped cistern and a stair to an upper floor; rubble and mud-brick walls, white stucco, red mortar floors with white chips. Appian's six-storey houses lined the streets to the citadel."),
         outskirts=dict(title="Megara", text="Inside the long land walls, the Megara: kitchen gardens and orchards watered by channels, olive and fig trees, villas of the great families, and the tombs of Sainte-Monique on the coast hills.")),
    dict(id="roman-200", label="Colonia Iulia Concordia Carthago", year=200, startYear=-145, endYear=395,
         summary="After a century as a cursed ruin, Carthage is refounded by Augustus (29 BCE) as a Roman colony on a grid over the levelled Byrsa. By 200 CE it is the second city of the Latin West and capital of Africa Proconsularis: grain and oil sail to Rome, the Antonine Baths stand on the shore, and the Zaghouan aqueduct fills the cisterns of La Malga.",
         population="perhaps 100,000 or more",
         feel="Latin and Punic in the forum, racing factions shouting in the circus, the smell of garum and oil on the quays, and Christian meetings in private houses.",
         style="antique",
         houses=dict(title="Houses of the Roman grid", text="Long narrow insulae of 120 by 480 Roman feet, filled with peristyle houses with mosaic floors for the rich, and shops and workshops with flats above for the rest; walls of rubble and reused Punic stone, tiled roofs, cisterns under the courts."),
         outskirts=dict(title="Villas and cemeteries", text="Suburban villas with mosaics of hunts and estates, market gardens, kilns and the cemeteries of the officials and of the Christians along the roads out of the city.")),
    dict(id="vandal-480", label="Vandal and Byzantine Carthage", year=480, startYear=396, endYear=698,
         summary="The great Christian city of Augustine's councils, walled in 425 under Theodosius II. In 439 the Vandal king Gaiseric takes it and makes it his capital; Arian churches, palace life and the circus go on. Belisarius retakes it for Byzantium in 533, rebuilding walls and churches like Damous el Karita. In 698 the Arab army of Hassan ibn al-Nu'man takes it and abandons it for Tunis.",
         population="perhaps 50,000–100,000, falling",
         feel="Church bells are not yet rung: psalms in the basilicas, Gothic and Latin in the streets, and dust from earthquake and siege repairs.",
         style="antique",
         houses=dict(title="Late antique houses", text="The Roman insulae subdivided: courts filled with workshops and rooms, porticoes walled up, rich houses with apses and new mosaics for the Vandal and Roman nobility, and burials appearing inside the walls by the 6th century."),
         outskirts=dict(title="Monasteries and estates", text="Martyrs' basilicas and monasteries outside the wall of 425, villas with gardens and hunting grounds, and fields creeping back into the abandoned edges of the grid.")),
    dict(id="ruins-1600", label="The ruins of Carthage", year=1600, startYear=699, endYear=1880,
         summary="After 698 Tunis, across the lake, becomes the capital and Carthage a quarry: its marble and columns go to the mosques of Tunis and Kairouan and as far as Pisa and Genoa. Louis IX of France dies in his camp here in 1270. By 1600: barley and olives over the grid, the hamlet of La Malga in the cisterns, and Sidi Bou Said on its cliff.",
         population="a few hundred villagers, herdsmen and fishermen",
         feel="Wind in the barley over buried mosaics, the cries of stone-robbers' mules, and the call to prayer from Sidi Bou Said.",
         style="courtyard",
         houses=dict(title="Village houses", text="Low whitewashed houses of rubble and reused Roman stone round small courts, flat-roofed, with a cistern; at La Malga some families live inside the vaulted Roman cisterns themselves."),
         outskirts=dict(title="Fields among the ruins", text="Barley fields, olive groves and prickly-pear hedges over the ruin mounds; lime kilns burning marble, and goats on the Byrsa.")),
]

# ---------------------------------------------------------------- water
# The gulf is a narrow ribbon along the shore plus a wide one further out. The harbours: the
# rectangular commercial harbour with its channel to the sea, and the circular naval harbour (the
# Cothon) with its island, filled as a ring of water round the island. In 1600 both are reduced to
# silted lagoons. The Lake of Tunis is a wide ribbon off its north shore.
WATER = [
    dict(id="gulf", name="Gulf of Tunis", width=700, path=OFF(SHORE, 350),
         blurb="The Gulf of Tunis, open to the north-east. Carthage was a harbour city first: its ships traded to Spain, Sardinia, Sicily, Etruria and the Levant, and later Rome's grain fleets sailed from here to Ostia."),
    dict(id="gulf-open", name="Gulf of Tunis", width=1700, path=OFF(SHORE_SMOOTH, 1350)),
    dict(id="gulf-far", name="Gulf of Tunis", width=3000, path=OFF(SHORE_SMOOTH, 3500)),
    dict(id="lake", name="Lake of Tunis", width=2400, path=OFF(LAKE_SHORE, -1200),
         blurb="A shallow lagoon between Carthage and Tunis (Tunes), closed from the gulf by the sand spit the ancients called the Taenia, 'the ribbon', with a narrow mouth at La Goulette. Its fish and shallows fed the city; Scipio's army camped on its shore in 147 BCE."),
] + [
    dict(id=f"commercial-harbour-{k}", name="Commercial harbour", width=64, periods=ANTIQUE, path=[UV(679 + du, -1118), UV(679 + du, -852)],
         blurb="The rectangular merchant harbour, about 330 by 250 m here (450 by 350 m in some reconstructions), entered from the sea by a channel some 20 m wide that could be closed with iron chains (Appian). Quays and warehouses lined it; ships passed through it into the closed naval harbour.")
    for k, du in enumerate((-93, -31, 31, 93))
] + [
    dict(id="harbour-mouth", name="Harbour entrance", width=40, periods=ANTIQUE,
         path=[UV(770, -1130), UV(860, -1230), UV(990, -1310)]),
    dict(id="harbour-link", name="Channel to the naval harbour", width=26, periods=LATER,
         path=[UV(610, -840), UV(495, -690)]),
    dict(id="cothon", name="Circular naval harbour (Cothon)", width=64, periods=LATER,
         path=[(ROUND_C[0] + 84 * math.sin(math.tau * i / 24) / KY, ROUND_C[1] + 84 * math.cos(math.tau * i / 24) / KX) for i in range(25)],
         blurb="The naval harbour, a round basin about 325 m across with an island in the middle, ringed by ship sheds: Appian counts 220 berths, each fronted by two Ionic columns, with the admiral's tower on the island. Excavation (Hurst) dates it in this form to the 2nd century BCE."),
    dict(id="commercial-harbour-1600", name="Silted lagoon", width=160, periods=RUINS,
         path=[UV(690, -1120), UV(680, -860)]),
    dict(id="cothon-1600", name="Silted round lagoon", width=40, periods=RUINS,
         path=[(ROUND_C[0] + 78 * math.sin(math.tau * i / 24) / KY, ROUND_C[1] + 78 * math.cos(math.tau * i / 24) / KX) for i in range(25)]),
]
ISLANDS = [
    dict(name="Admiralty island", periods=LATER,
         polygon=[(ROUND_C[0] + 54 * math.sin(math.tau * i / 20) / KY, ROUND_C[1] + 54 * math.cos(math.tau * i / 20) / KX) for i in range(20)]),
]

HILLS = [
    dict(id="byrsa-hill", name="Byrsa", center=(36.8526, 10.3236), radius=260,
         blurb="The citadel hill, about 60 m high. Its name was explained by the Greeks with the tale of Dido's ox-hide (byrsa), cut into strips to enclose the land she had bought; the word may come from a Phoenician word for 'fortress'."),
    dict(id="juno-hill", name="Juno hill", center=(36.8556, 10.3270), radius=150,
         blurb="A low hill north-east of the Byrsa, named by modern excavators after a supposed temple of Juno Caelestis; its slopes held Punic tombs of the 7th–6th centuries BCE."),
    dict(id="odeon-hill", name="Odeon hill", center=(36.8598, 10.3290), radius=150, label=False,
         blurb="The hill of the Roman odeon and theatre; Punic tombs lie beneath."),
    dict(id="bordj-djedid", name="Bordj Djedid", center=(36.8590, 10.3378), radius=120,
         blurb="The coastal hill north of the Antonine Baths, with the Punic necropolis of Sainte-Monique and, in Roman times, great cisterns feeding the baths."),
    dict(id="sidi-bou-said-hill", name="Jebel Manar", center=(36.8705, 10.3480), radius=380,
         blurb="The cliff at the end of the peninsula, about 130 m high. Its ancient name is uncertain; the Arabs called it Jebel Manar, 'hill of the beacon', for the fire lit there to guide ships."),
    dict(id="koudiat-zateur", name="Koudiat Zateur", center=(36.8645, 10.3215), radius=140, label=False,
         blurb="A low rise in the Megara, with tombs and later villas."),
]

# ---------------------------------------------------------------- streets
DEC = [-852, -568, -284, 0, 284, 568, 852, 1136]
CAR = [-564, -282, 0, 282, 564]
ROADS = [
    # Punic Carthage
    dict(id="three-streets", name="The three streets to the Byrsa", path=[(36.8478, 10.3266), (36.8494, 10.3256), (36.8508, 10.3247), (36.8516, 10.3240)], width=10, style="major", labelled=True, periods=PUNIC,
         blurb="Appian (Punica 128) tells of three streets climbing from the agora to the Byrsa, lined with houses six storeys high, where the Romans fought for six days in 146 BCE, crossing from roof to roof on planks."),
    dict(id="three-streets-2", name="Street to the Byrsa", path=[(36.8478, 10.3266), (36.8488, 10.3245), (36.8505, 10.3232)], width=8, periods=PUNIC),
    dict(id="three-streets-3", name="Street to the Byrsa", path=[(36.8478, 10.3266), (36.8500, 10.3266), (36.8517, 10.3254)], width=8, periods=PUNIC),
    dict(id="sea-street", name="Sea-wall street", path=[(36.8440, 10.3268), (36.8470, 10.3285), (36.8500, 10.3307), (36.8530, 10.3333), (36.8560, 10.3360), (36.8590, 10.3376)], width=8, labelled=True, periods=PUNIC,
         blurb="The street running behind the sea wall through the seaside quarter (the 'Magon quarter' of the German excavators), where houses were rebuilt on the same plots from the 5th century to 146 BCE."),
    dict(id="harbour-street", name="Harbour street", path=LINE([(470, -1020), (280, -820), (270, -460), (420, -360), (501, -352)]), width=10, style="major", periods=PUNIC),
    dict(id="punic-street-1", name="Street of the lower city", path=LINE([(300, -560), (300, 820)]), width=8, periods=PUNIC),
    dict(id="punic-street-2", name="Street of the lower city", path=LINE([(600, -420), (600, 820)]), width=8, periods=PUNIC),
    dict(id="punic-cross-1", name="Street to the sea", path=LINE([(140, -200), (SHU(-200, 40), -200)]), width=7, periods=PUNIC),
    dict(id="punic-cross-2", name="Street to the sea", path=LINE([(140, 200), (SHU(200, 40), 200)]), width=7, periods=PUNIC),
    dict(id="punic-cross-3", name="Street to the sea", path=LINE([(140, 520), (SHU(520, 40), 520)]), width=7, periods=PUNIC),
    dict(id="megara-road", name="Road to Megara", path=[(36.8540, 10.3246), (36.8580, 10.3248), (36.8630, 10.3258), (36.8680, 10.3268), (36.8720, 10.3262), (36.8760, 10.3250)], width=9, labelled=True, periods=PUNIC,
         blurb="North out of the city into the garden suburb of Megara, which lay inside the outer walls."),
    dict(id="cape-road", name="Road to the cape", path=[(36.8630, 10.3258), (36.8650, 10.3330), (36.8675, 10.3400), (36.8700, 10.3460)], width=7, periods=PUNIC),
    dict(id="utica-road", name="Road to Utica", path=[(36.8540, 10.3222), (36.8575, 10.3170), (36.8615, 10.3110), (36.8660, 10.3050), (36.8690, 10.3020)], width=10, style="major", labelled=True, periods=ANTIQUE,
         blurb="North-west across the isthmus to Utica, the older Phoenician city at the mouth of the Medjerda; Roman Carthage's road to Hippo and Numidia."),
    dict(id="tunes-road", name="Road to Tunes", path=[(36.8518, 10.3218), (36.8530, 10.3150), (36.8530, 10.3095), (36.8505, 10.3050), (36.8470, 10.3020)], width=10, style="major", labelled=True, periods=ANTIQUE,
         blurb="West along the lake shore to Tunes (Tunis), 15 km away, and the interior: the road of the grain and oil of the Medjerda valley."),
    dict(id="taenia-road", name="Road along the Taenia", path=[(36.8410, 10.3225), (36.8375, 10.3205), (36.8335, 10.3170), (36.8300, 10.3140)], width=8, periods=ANTIQUE),
    # Roman Carthage: the grid. The decumanus maximus runs from the forum on the Byrsa to the sea,
    # the cardo maximus along the line of the hill.
    dict(id="decumanus-maximus", name="Decumanus maximus", path=LINE([(-1000, 0), (-560, 0), (-120, 0)]), width=14, style="major", labelled=True, periods=ROM_LATE),
    dict(id="decumanus-maximus-e", name="Decumanus maximus", path=LINE([(120, 0), (500, 0), (SHU(0, 30), 0)]), width=14, style="major", periods=ROM_LATE,
         blurb="The main east-west street of the Roman grid, from the forum on the Byrsa down to the sea; westward it ran on to the amphitheatre."),
    dict(id="cardo-maximus", name="Cardo maximus", path=LINE([(0, -1000), (0, -560), (0, -110)]), width=14, style="major", labelled=True, periods=ROM_LATE,
         blurb="The main north-south street, crossing the forum on the Byrsa; south it reached the harbours, north the road to the cape and the villas of the coast."),
    dict(id="cardo-maximus-n", name="Cardo maximus", path=LINE([(0, 110), (0, 600), (0, 1400), (0, 1900)]), width=14, style="major", periods=ROM_LATE),
] + [
    dict(id=f"decumanus-{i}", name="Decumanus", path=LINE([(-700, v), (SHU(v, 30), v)]), width=8, periods=ROM_LATE)
    for i, v in enumerate(DEC) if v != 0
] + [
    dict(id=f"cardo-{i}", name="Cardo", path=LINE([(u, -980), (u, 1300)]), width=8, periods=ROM_LATE)
    for i, u in enumerate(CAR) if u not in (0, 564)
] + [
    dict(id="cardo-coast", name="Cardo by the sea", path=LINE([(564, -720), (564, 600)]), width=8, periods=ROM_LATE),
    # after 698: tracks across the fields
    dict(id="track-marsa", name="Track from Tunis to La Marsa", path=[(36.8445, 10.3020), (36.8500, 10.3110), (36.8560, 10.3170), (36.8605, 10.3195), (36.8660, 10.3225), (36.8720, 10.3245), (36.8760, 10.3250)], width=7, style="major", labelled=True, periods=RUINS,
         blurb="The track from Tunis round the lake to La Marsa, where the Hafsid sultans had their summer gardens, passing the hamlet of La Malga."),
    dict(id="track-sidi", name="Track to Sidi Bou Said", path=[(36.8660, 10.3225), (36.8668, 10.3310), (36.8685, 10.3400), (36.8705, 10.3462)], width=6, periods=RUINS),
    dict(id="track-byrsa", name="Track to the shore", path=[(36.8605, 10.3195), (36.8560, 10.3230), (36.8520, 10.3260), (36.8480, 10.3240), (36.8440, 10.3215), (36.8400, 10.3200), (36.8340, 10.3170)], width=5, periods=RUINS),
]

# ---------------------------------------------------------------- walls and gates
BYRSA_WALL = [(36.8546, 10.3218), (36.8549, 10.3245), (36.8538, 10.3262), (36.8516, 10.3262), (36.8505, 10.3245), (36.8507, 10.3220), (36.8525, 10.3208)]
SEA_WALL = OFF(SHORE[3:16], -45)
# the circuit of 425, known only in stretches: south by the harbours, round the circus and La Malga, north past Damous el Karita to the sea
THEODOSIAN = [UV(900, -1250), UV(500, -1250), UV(150, -1150), UV(-300, -1000), UV(-700, -900), UV(-980, -700), UV(-1000, -300), UV(-1000, 100), UV(-900, 520), UV(-640, 820), UV(-300, 1150), UV(100, 1400), UV(450, 1680)]
WALLS = [
    dict(id="land-wall", name="Land walls across the isthmus", path=[(36.8760, 10.3040), (36.8650, 10.3030), (36.8540, 10.3028), (36.8440, 10.3033)], periods=PUNIC,
         blurb="Appian describes a triple line across the isthmus, 30 cubits high, with stalls for 300 elephants and 4,000 horses and barracks for 20,000 foot in its thickness. Its trace has never been found; it is drawn here at the edge of the map, probably too far east."),
    dict(id="sea-wall", name="Sea wall", path=SEA_WALL, periods=PUNIC,
         blurb="A single wall along the shore. A stretch of it, of large sandstone blocks with towers and a gate, was excavated in the seaside quarter north of the harbours; it was rebuilt and thickened in the 4th–3rd centuries BCE."),
    dict(id="byrsa-wall", name="Walls of the Byrsa", path=BYRSA_WALL, closed=True, periods=PUNIC,
         blurb="The citadel's own circuit, about two stades round in Orosius' figure, where the last defenders held out in 146 BCE."),
    dict(id="theodosian-wall", name="Wall of Theodosius II", path=THEODOSIAN, periods=LATE,
         blurb="Built in 425 against the Vandal threat, after the Roman city had stood unwalled for 450 years; restored by Justinian after 533. Its line is known from short stretches only and is drawn here in outline."),
]
GATES = []
BRIDGES = []
AQUEDUCTS = [
    dict(name="Aqueduct from Zaghouan", path=[(36.8540, 10.3020), (36.8555, 10.3080), (36.8572, 10.3130), (36.8588, 10.3176)], periods=ROM_LATE),
]

# ---------------------------------------------------------------- built-up areas
# Punic: the seaside quarter and the plain between the Byrsa and the sea; the Byrsa slopes; Megara.
# The lower city between the Byrsa and the sea is laid out in grid cells between the Punic streets
# (u = 300, 600; v = -200, 200, 520); the agora is left open north-east of the round harbour.
PU_U = [(140, 292), (308, 592), (608, None)]
PU_V = [(-420, -208), (-192, 192), (208, 512), (528, 820)]


def PCELL(u0, u1, v0, v1):
    return Q(u0, u1, v0, v1) if u1 is not None else QS(u0, v0, v1, 60)


MEGARA_1 = [(36.8600, 10.3220), (36.8650, 10.3230), (36.8660, 10.3300), (36.8630, 10.3330), (36.8610, 10.3280)]
MEGARA_2 = [(36.8665, 10.3250), (36.8730, 10.3240), (36.8745, 10.3330), (36.8700, 10.3380), (36.8672, 10.3320)]
MEGARA_3 = [(36.8580, 10.3110), (36.8640, 10.3100), (36.8655, 10.3190), (36.8600, 10.3200), (36.8565, 10.3160)]
MEGARA_4 = [(36.8680, 10.3060), (36.8740, 10.3060), (36.8750, 10.3200), (36.8690, 10.3215), (36.8670, 10.3140)]

BLOCKS = [
    dict(name="Lower city" if v0 < 500 else "Dermech", polygon=PCELL(u0, u1, v0, v1),
         density="dense" if (v0 < 500 or p == "punic-150") else "loose", periods=[p])
    for p in PUNIC for (u0, u1) in PU_U for (v0, v1) in PU_V
    if not (u0 == 308 and v0 == -420)
] + [
    dict(name="Agora quarter", polygon=Q(160, 292, -560, -436), density="dense", periods=PUNIC),
    dict(name="Byrsa south slope", polygon=Q(-200, 125, -480, -110), density="dense", periods=P150),
    dict(name="Metal-workers on the Byrsa slope", polygon=Q(-200, 125, -480, -110), density="loose", periods=P400),
    dict(name="Byrsa west slope", polygon=Q(-330, -135, -200, 200), density="loose", periods=PUNIC),
    dict(name="Byrsa north slope", polygon=Q(-150, 125, 105, 330), density="dense", periods=P150),
    dict(name="Byrsa north slope", polygon=Q(-150, 125, 105, 330), density="loose", periods=P400),
    dict(name="West of the harbours", polygon=Q(-150, 270, -1000, -520), density="dense", periods=PUNIC),
    dict(name="Megara", polygon=MEGARA_1, density="loose", periods=PUNIC),
    dict(name="Megara", polygon=MEGARA_2, density="loose", periods=PUNIC),
    dict(name="Megara", polygon=MEGARA_3, density="loose", periods=P150),
    dict(name="Megara", polygon=MEGARA_4, density="loose", periods=P150),
    # Roman and late antique: the cells of the grid between the streets drawn above
] + [
    dict(name="Insulae of the colony", polygon=Q(u0 + 8, u1 - 8, v0 + 8, v1 - 8), density="dense", periods=ROM_LATE)
    for (u0, u1) in [(-564, -282), (-282, 0), (0, 282), (282, 564)]
    for (v0, v1) in [(-852, -568), (-568, -284), (-284, 0), (0, 284), (284, 568), (568, 852), (852, 1136)]
    if not (u0 == -564 and v0 >= 568)
] + [
    dict(name="Insulae by the sea", polygon=QS(572, v0 + 8, v1 - 8, 70), density="dense", periods=ROM_LATE)
    for (v0, v1) in [(-568, -284), (-284, 0), (0, 284), (284, 568)]
] + [
    dict(name="Harbour quarter", polygon=Q(-282 + 8, 282 - 8, -1000, -860), density="dense", periods=ROM_LATE),
    dict(name="West quarter", polygon=Q(-700, -572, -560, 560), density="loose", periods=ROMAN),
    dict(name="Northern villas", polygon=Q(-280, 560, 1144, 1420), density="loose", periods=ROM_LATE),
    dict(name="Northern villas", polygon=Q(-560, -290, 860, 1140), density="loose", periods=ROM_LATE),
    # after 698: villages
    dict(name="La Malga", polygon=[(36.8600, 10.3165), (36.8610, 10.3195), (36.8598, 10.3210), (36.8588, 10.3200), (36.8590, 10.3170)], density="loose", periods=RUINS),
    dict(name="Douar Chott", polygon=[(36.8460, 10.3075), (36.8475, 10.3100), (36.8462, 10.3118), (36.8448, 10.3095)], density="loose", periods=RUINS),
    dict(name="Sidi Bou Said", polygon=[(36.8695, 10.3448), (36.8718, 10.3452), (36.8725, 10.3485), (36.8708, 10.3500), (36.8692, 10.3478)], density="dense", periods=RUINS),
    dict(name="La Marsa gardens", polygon=[(36.8735, 10.3220), (36.8760, 10.3215), (36.8760, 10.3300), (36.8740, 10.3300)], density="loose", periods=RUINS),
]
GARDENS = [
    dict(name="Gardens of Megara", polygon=[(36.8620, 10.3120), (36.8700, 10.3120), (36.8720, 10.3200), (36.8660, 10.3210)], kind="orchard", periods=PUNIC),
    dict(name="Vines of Megara", polygon=[(36.8680, 10.3330), (36.8720, 10.3300), (36.8690, 10.3420), (36.8665, 10.3400)], kind="vineyard", periods=PUNIC),
    dict(name="Olive groves", polygon=[(36.8600, 10.3040), (36.8680, 10.3040), (36.8670, 10.3110), (36.8605, 10.3110)], kind="orchard", periods=ALL),
    dict(name="Suburban gardens", polygon=[(36.8650, 10.3120), (36.8720, 10.3120), (36.8740, 10.3220), (36.8670, 10.3220)], kind="orchard", periods=ROM_LATE),
    dict(name="Fields over the grid", polygon=Q(-560, 560, -860, -300), kind="vineyard", periods=RUINS),
    dict(name="Olives over the grid", polygon=Q(-560, 500, 300, 1100), kind="orchard", periods=RUINS),
    dict(name="Gardens of La Marsa", polygon=[(36.8705, 10.3120), (36.8760, 10.3120), (36.8760, 10.3210), (36.8720, 10.3215)], kind="orchard", periods=RUINS),
]
MARSH = [
    dict(name="Lake shallows", polygon=[(36.8395, 10.3030), (36.8420, 10.3060), (36.8400, 10.3100), (36.8370, 10.3080)], periods=ALL),
    dict(name="Silted harbours", polygon=Q(560, 800, -1150, -560), periods=RUINS),
]
DISTRICTS = [
    dict(id="byrsa", name="Byrsa", polygon=BYRSA_WALL, periods=PUNIC,
         description="The citadel: the temple of Eshmun on the summit, reached by a stair of sixty steps, and the last refuge of the city in 146 BCE."),
    dict(id="seaside", name="Seaside quarter", polygon=Q(140, 880, -420, 820), periods=PUNIC,
         description="The dense lower city between the Byrsa and the sea wall, with the agora near the harbours, merchants' houses, dye works and potters' kilns."),
    dict(id="megara", name="Megara", polygon=[(36.8590, 10.3060), (36.8760, 10.3060), (36.8760, 10.3330), (36.8690, 10.3420), (36.8610, 10.3330)], periods=PUNIC,
         description="The great suburb inside the outer walls, of gardens and orchards 'full of every kind of fruit' (Diodorus, of Agathocles' soldiers), with villas, water channels and hedges."),
    dict(id="ports", name="Ports", polygon=Q(380, 900, -1260, -480), periods=ANTIQUE,
         description="The two harbours at Salammbo, the merchant harbour and the closed naval harbour behind it, and the Tophet on their western side; in Roman times the quays of the grain fleet."),
    dict(id="forum", name="Forum of the colony", polygon=Q(-140, 140, -110, 110), periods=ROMAN,
         description="The Byrsa summit, cut down and built up into a terrace of about 3 ha under Augustus, carrying the forum, the capitol, the basilica and the proconsul's offices."),
]
LABELS = [
    dict(text="GULF OF TUNIS", position=(36.8480, 10.3480), size="lg", rotation=-60, periods=PUNIC + RUINS),
    dict(text="MARE INTERNUM", position=(36.8480, 10.3480), size="lg", rotation=-60, periods=ROM_LATE),
    dict(text="LAKE OF TUNIS", position=(36.8350, 10.3040), size="md", rotation=-40, periods=ANTIQUE),
    dict(text="AL-BUHAYRA", position=(36.8350, 10.3040), size="md", rotation=-40, periods=RUINS),
    dict(text="Byrsa", position=(36.8552, 10.3218), size="md", rotation=0, periods=ALL),
    dict(text="Megara", position=(36.8690, 10.3170), size="md", rotation=0, periods=PUNIC),
    dict(text="Taenia", position=(36.8320, 10.3165), size="sm", rotation=-50, periods=ANTIQUE),
    dict(text="Cothon", position=(36.8478, 10.3225), size="sm", rotation=0, periods=P150),
    dict(text="Salammbo", position=(36.8400, 10.3205), size="sm", rotation=0, periods=RUINS),
    dict(text="La Malga", position=(36.8615, 10.3175), size="sm", rotation=0, periods=RUINS),
    dict(text="Douar Chott", position=(36.8452, 10.3060), size="sm", rotation=0, periods=RUINS),
    dict(text="Sidi Bou Said", position=(36.8735, 10.3470), size="sm", rotation=0, periods=RUINS),
    dict(text="La Marsa", position=(36.8752, 10.3260), size="sm", rotation=0, periods=RUINS),
    dict(text="to Utica", position=(36.8700, 10.3045), size="sm", rotation=-50, periods=ANTIQUE),
    dict(text="to Tunes", position=(36.8490, 10.3045), size="sm", rotation=-30, periods=ANTIQUE),
    dict(text="to Tunis, 15 km", position=(36.8380, 10.3070), size="sm", rotation=-40, periods=RUINS),
    dict(text="to the Sebkha of Ariana", position=(36.8745, 10.3110), size="sm", rotation=0, periods=ALL),
]

SOURCES = [
    dict(id="wiki-carthage", title="Carthage", author="Wikipedia", url="https://en.wikipedia.org/wiki/Carthage"),
    dict(id="wiki-ancient-carthage", title="Ancient Carthage", author="Wikipedia", url="https://en.wikipedia.org/wiki/Ancient_Carthage"),
    dict(id="wiki-roman-carthage", title="Roman Carthage", author="Wikipedia", url="https://en.wikipedia.org/wiki/Roman_Carthage"),
    dict(id="wiki-archaeological-site", title="Archaeological site of Carthage", author="Wikipedia", url="https://en.wikipedia.org/wiki/Archaeological_site_of_Carthage"),
    dict(id="wiki-lake-tunis", title="Lake of Tunis", author="Wikipedia", url="https://en.wikipedia.org/wiki/Lake_of_Tunis"),
    dict(id="appian", title="Roman History, Book 8: The Punic Wars (Punica) 95–135", author="Appian", year="2nd century CE", url="https://en.wikipedia.org/wiki/Appian"),
    dict(id="lancel", title="Carthage: A History", author="Serge Lancel", year=1995),
    dict(id="hurst", title="The Sanctuary of Tanit at Carthage in the Roman Period; Excavations at Carthage: The British Mission II (the circular harbour)", author="Henry Hurst", year="1994–1999"),
    dict(id="miles", title="Carthage Must Be Destroyed", author="Richard Miles", year=2010),
    dict(id="rakob", title="Karthago I–III: Die deutschen Ausgrabungen in Karthago", author="Friedrich Rakob (ed.)", year="1991–1999"),
    dict(id="ennabli", title="Pour sauver Carthage: exploration et conservation de la cité punique, romaine et byzantine", author="Abdelmajid Ennabli (ed.)", year=1992),
]
