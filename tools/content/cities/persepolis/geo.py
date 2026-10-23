# Persepolis (Parsa): the great terrace at the foot of Kuh-e Rahmat, the royal tombs above it, the fortifications,
# the lower town and paradises on the Marvdasht plain, from Darius I to the Sasanians (see tools/content/cities/FORMAT.md).
# Positions are written in metres from the centre of the terrace (x east, y north) and projected by L().
import math

ALL = ["darius-500", "xerxes-460", "burned-330", "sasanian-250"]
ACHAEMENID = ["darius-500", "xerxes-460"]
TOWN = ["darius-500", "xerxes-460", "burned-330"]
LATER = ["burned-330", "sasanian-250"]

C_LAT, C_LON = 29.93480, 52.89050          # centre of the Takht
M_LAT = 1.0 / 110860.0                      # degrees per metre north
M_LON = 1.0 / (111320.0 * math.cos(math.radians(C_LAT)))


def L(x, y):
    """Terrace-local metres (x east, y north) to (lat, lon)."""
    return (round(C_LAT + y * M_LAT, 6), round(C_LON + x * M_LON, 6))


def LS(pts):
    return [L(x, y) for x, y in pts]


CITY = dict(
    name="Persepolis", subtitle="Parsa, Terrace of the Achaemenid Kings",
    description="Persepolis from Darius I's new terrace (about 518 BCE) to the Sasanian kings who carved their names in its ruins: the Takht against Kuh-e Rahmat with its palaces and halls, the royal tombs cut in the mountain above, the fortifications, and the lower town, paradises and canals of the Marvdasht plain. Naqsh-e Rustam (6 km) and Istakhr (5 km) lie off the map to the north. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="darius-500",
    world=dict(heightScale=1.0, walls=["#CDAA7E", "#C29E74", "#D6BA90", "#B9966C", "#D0B38A"], roofs=["#A98D66", "#B39670"]),
    camera=dict(target=L(-120, -40), distance=30),
)
FRAME = (L(-2750, 1910), L(1500, -1975))
RESOLUTION = 4096
PALETTE = dict(parchment="#E8D5A8", ink="#6C4B32", water="#5F8A8C", hill="#857C5C", road="#8C6A48")
COMPASS = L(1150, 1650)
CARTOUCHE = L(-2700, -1930)

PERIODS = [
    dict(id="darius-500", label="Darius' terrace", year=-500, startYear=-518, endYear=-486,
         summary="Parsa under Darius I. Since about 518 BCE gangs of workers have been cutting and filling the rock at the foot of Kuh-e Rahmat into a limestone terrace 12 to 18 m high. By 500 the first treasury and Darius' own palace, the Tachara, stand; the Apadana's columns rise on their platform. Below, a lower town of officials, workshops and gardens spreads over the Marvdasht plain.",
         population="unknown; the ration tablets list thousands of workers in the region",
         feel="Chisels ringing on grey limestone, ox-carts hauling column drums up the ramps, clerks pressing Elamite into wet clay, the sour smell of barley beer at the ration store.",
         style="courtyard",
         houses=dict(title="Mud-brick houses of officials and workers", text="Rooms of sun-dried mud brick on stone footings round small courts, flat roofs of poplar beams, reeds and packed earth, mud-plastered walls. The tablets list the people who live here by trade and household, with their monthly barley, wine and beer."),
         outskirts=dict(title="Paradises and fields of the Marvdasht", text="Walled gardens (pairidaeza) of trees and water channels round pavilions, barley fields fed by canals and qanats, vineyards, flocks on the stubble, and the villages of the estates that feed the court.")),
    dict(id="xerxes-460", label="The terrace of Xerxes", year=-460, startYear=-485, endYear=-331,
         summary="The terrace completed by Xerxes (486–465 BCE) and his son Artaxerxes I. Visitors climb the double stair to the Gate of All Nations and its stone bulls; the Apadana is finished, Xerxes' palace and harem stand on the south terrace, and the Hall of a Hundred Columns is rising. Persepolis is a ceremonial and treasury city; the court also lives at Susa, Babylon and Ecbatana.",
         population="unknown; a royal city of perhaps several tens of thousands with its plain",
         feel="Painted cedar ceilings and gold leaf, guards calling in Persian, tribute horses at the foot of the stair, gardeners opening sluices in the paradise.",
         style="courtyard",
         houses=dict(title="Houses of the royal city", text="Mud-brick courtyard houses of officials, scribes and craftsmen below the terrace, some with columned porches on stone bases and painted plaster; smaller rooms of workers' families in rows, flat roofs used for sleeping in summer."),
         outskirts=dict(title="Royal paradises and estates", text="Pavilions in walled paradises of plane, cypress and fruit trees, irrigated barley and wheat, vineyards and orchards along the canals, horse pastures and the storehouses of the royal economy.")),
    dict(id="burned-330", label="After the fire", year=-330, startYear=-330, endYear=223,
         summary="In 330 BCE Alexander emptied the treasury and burned the palaces. The cedar roofs fell; mud-brick walls slumped round the stone door frames and the columns that still stand. Macedonian satraps, then from the 3rd century BCE local dynasts of Persis, rule the plain. The lower town shrinks to villages, and Istakhr, 5 km to the north, becomes the town of the district.",
         population="a few villages",
         feel="Wind through roofless halls, soot on the stone, shepherds watering flocks in the terrace cisterns, kites circling over the fallen bulls.",
         style="courtyard",
         houses=dict(title="Village houses below the ruins", text="Mud-brick farmhouses round yards with ovens, storerooms and animal pens, flat roofs of beams and earth; the old officials' quarter is half empty, its walls melting back into the soil."),
         outskirts=dict(title="Fields of the Marvdasht", text="Barley and wheat on the canal-fed plain, orchards where the royal paradises were, threshing floors and flocks; the old royal estates now farmed for new masters.")),
    dict(id="sasanian-250", label="Sasanian Persis", year=250, startYear=224, endYear=651,
         summary="Ardashir I, from a priestly family of Istakhr, has overthrown the Parthians (224 CE). Istakhr, 5 km north, is the dynasty's home city; Persepolis is a revered ruin of ancient kings. Sasanian princes visit it, feast in the roofless Tachara and cut Middle Persian inscriptions on its door frames. Below, villages farm the plain, and at Naqsh-e Rustam the new kings carve their reliefs beneath the Achaemenid tombs.",
         population="villages in the plain; the town is Istakhr",
         feel="Fire-temple smoke from the direction of Istakhr, priests murmuring Avestan prayers, goats grazing among fallen bull capitals.",
         style="courtyard",
         houses=dict(title="Sasanian farmhouses", text="Mud-brick farmhouses with barrel-vaulted rooms and small domes round a walled yard, an oven, a storeroom of grain jars; walls plastered with mud and straw, some footings of stone taken from the old buildings."),
         outskirts=dict(title="Villages and canals", text="Irrigated barley, wheat and cotton, orchards and vines along the canals, qanat outlets feeding cisterns, mud-walled villages under the mountain.")),
]

SOURCES = [
    dict(id="wiki-persepolis", title="Persepolis", author="Wikipedia", url="https://en.wikipedia.org/wiki/Persepolis"),
    dict(id="wiki-achaemenid-architecture", title="Achaemenid architecture", author="Wikipedia", url="https://en.wikipedia.org/wiki/Achaemenid_architecture"),
    dict(id="wiki-pfa", title="Persepolis Administrative Archives", author="Wikipedia", url="https://en.wikipedia.org/wiki/Persepolis_Administrative_Archives"),
    dict(id="wiki-marvdasht", title="Marvdasht", author="Wikipedia", url="https://en.wikipedia.org/wiki/Marvdasht"),
    dict(id="wiki-istakhr", title="Istakhr", author="Wikipedia", url="https://en.wikipedia.org/wiki/Istakhr"),
    dict(id="wiki-naqsh-e-rostam", title="Naqsh-e Rostam", author="Wikipedia", url="https://en.wikipedia.org/wiki/Naqsh-e_Rostam"),
    dict(id="wiki-persian-garden", title="Persian gardens", author="Wikipedia", url="https://en.wikipedia.org/wiki/Persian_gardens"),
    dict(id="wiki-qanat", title="Qanat", author="Wikipedia", url="https://en.wikipedia.org/wiki/Qanat"),
    dict(id="wiki-persis", title="Persis", author="Wikipedia", url="https://en.wikipedia.org/wiki/Persis"),
    dict(id="schmidt-persepolis", title="Persepolis I–III", author="Erich F. Schmidt", year="1953–1970"),
    dict(id="mousavi-persepolis", title="Persepolis: Discovery and Afterlife of a World Wonder", author="Ali Mousavi", year=2012),
    dict(id="briant", title="From Cyrus to Alexander: A History of the Persian Empire", author="Pierre Briant", year=2002),
    dict(id="hallock", title="Persepolis Fortification Tablets", author="Richard T. Hallock", year=1969),
    dict(id="sumner-1986", title="Achaemenid Settlement in the Persepolis Plain", author="William M. Sumner", year=1986),
    dict(id="arrian", title="Anabasis of Alexander, Book 3", author="Arrian", year="2nd century CE", url="https://en.wikipedia.org/wiki/Anabasis_of_Alexander"),
]

# ---------------------------------------------------------------- water
WATER = [
    dict(id="pulvar", name="Pulvar (Medus)", width=30,
         path=LS([(-1450, 1910), (-1620, 1700), (-1800, 1500), (-1980, 1330), (-2150, 1200), (-2350, 1080), (-2560, 990), (-2750, 940)]),
         blurb="The river of Pasargadae, which the Greeks called the Medus, comes down past Naqsh-e Rustam and Istakhr and crosses the Marvdasht plain to join the Kur. Its course across the plain has shifted since antiquity; the line here is approximate."),
    dict(id="royal-canal", name="Canal of the plain", width=6,
         path=LS([(-1900, 1420), (-1650, 1050), (-1400, 700), (-1250, 300), (-1150, -100), (-1050, -500), (-950, -1000), (-880, -1500), (-850, -1975)]),
         blurb="Achaemenid engineers dammed the Pulvar and the Kur and led canals across the plain; traces of ancient canals and dams survive. This line stands for that network rather than one surveyed channel."),
    dict(id="town-canal", name="Branch canal of the lower town", width=4, periods=TOWN,
         path=LS([(-1250, 300), (-1060, 0), (-1030, -300), (-980, -620), (-900, -760), (-600, -770), (-450, -720), (-260, -700)]),
         blurb="A smaller channel feeding the gardens and houses of the lower town; water was also brought from the mountain by qanats, underground channels dug from a mother well, which surface as open runnels."),
    dict(id="village-canal", name="Village canal", width=4, periods=["sasanian-250"],
         path=LS([(-1150, -100), (-900, -260), (-650, -420), (-490, -500)]),
         blurb="A Sasanian-period channel serving the villages at the foot of the ruins; the plain was intensively irrigated in Sasanian times."),
]

HILLS = [
    dict(id="kuh-e-rahmat", name="Kuh-e Rahmat", center=L(700, 100), radius=520,
         blurb="The 'Mountain of Mercy' (the Achaemenid name is unknown) rises behind the terrace to about 2,500 m. Its limestone was quarried for the terrace, its slope was walled, and the tombs of later kings were cut into its face above the palaces."),
    dict(id="rahmat-north", name="Kuh-e Rahmat (north spur)", center=L(620, 900), radius=480, label=False,
         blurb="The northern spur of the mountain, crossed by the fortification walls and the quarry roads."),
    dict(id="rahmat-south", name="Kuh-e Rahmat (south spur)", center=L(660, -720), radius=500, label=False,
         blurb="The southern spur. A third, unfinished royal tomb is cut into the rock about 500 m south of the terrace."),
    dict(id="rahmat-high", name="Kuh-e Rahmat (summit ridge)", center=L(1250, 250), radius=620, label=False,
         blurb="The high ridge of the mountain, bare limestone with scrub and wild almond."),
    dict(id="rahmat-far-south", name="Kuh-e Rahmat (south)", center=L(1150, -1400), radius=560, label=False,
         blurb="The mountain running south-east along the edge of the plain."),
    dict(id="rahmat-far-north", name="Kuh-e Rahmat (north)", center=L(950, 1650), radius=460, label=False,
         blurb="The mountain running north toward the gorge of the Pulvar and Istakhr."),
]

# ---------------------------------------------------------------- roads
ROADS = [
    dict(id="approach", name="Processional approach to the stair", width=18, style="major", labelled=True,
         path=LS([(-168, 160), (-300, 160), (-460, 160)]),
         blurb="The broad way from the plain to the foot of the double stair, where delegations dismounted and formed up before climbing to the Gate."),
    dict(id="susa-road", name="Royal road to Susa", width=12, style="major", labelled=True,
         path=LS([(-460, 160), (-1000, 330), (-1800, 620), (-2750, 960)]),
         blurb="The road north-west through the Persian Gates to Susa, about 550 km away, with way stations every day's march. The Fortification Tablets record travel rations for couriers and travellers carrying the king's sealed authorisations."),
    dict(id="pasargadae-road", name="Road to Istakhr and Pasargadae", width=12, style="major", labelled=True,
         path=LS([(-460, 160), (-500, 650), (-540, 1250), (-580, 1910)]),
         blurb="North past Istakhr and the rock of Naqsh-e Rustam, where Darius and three of his successors are buried, and up the Pulvar valley to Cyrus' capital at Pasargadae, about 45 km away."),
    dict(id="town-street", name="Main street of the lower town", width=10, style="major", periods=TOWN,
         path=LS([(-460, 160), (-470, -300), (-560, -900), (-700, -1500), (-820, -1975)]),
         blurb="The spine of Parsa's lower town, running south along the edge of the paradises toward the southern plain; its line is inferred from the scatter of buildings found on the plain."),
    dict(id="south-track", name="Track south across the plain", width=7, style="minor", periods=["sasanian-250"],
         path=LS([(-460, 160), (-470, -300), (-560, -900), (-700, -1500), (-820, -1975)]),
         blurb="The old town street reduced to a farm track between the villages."),
    dict(id="terrace-foot", name="Road along the terrace foot", width=9, style="minor",
         path=LS([(-205, 240), (-205, -265), (180, -265)]),
         blurb="The road under the west and south faces of the terrace. Darius' inscriptions are cut into the south wall, where the first approach to the terrace may have been."),
    dict(id="garden-avenue", name="Avenue of the paradises", width=8, style="minor", periods=TOWN,
         path=LS([(-470, -300), (-1000, -330), (-1600, -380)]),
         blurb="A road between the walled gardens and estates west of the town."),
    dict(id="cross-street", name="Street of the officials", width=7, style="minor", periods=TOWN,
         path=LS([(-205, -40), (-460, -40)]),
         blurb="A street through the quarter of officials' houses below the terrace."),
    dict(id="quarry-road", name="Quarry road", width=8, style="minor", periods=ACHAEMENID,
         path=LS([(60, 240), (220, 420), (300, 700), (330, 1000)]),
         blurb="The haul road from the limestone quarries on the mountain north of the terrace; blocks were cut close by, sledged and carted down to the building sites."),
    dict(id="army-road", name="Army road", width=8, style="minor", periods=["xerxes-460", "burned-330"],
         path=LS([(-85, 160), (-20, 162), (47, 164)]),
         blurb="The modern name for the paved way across the north of the terrace from the Gate of All Nations toward the Hall of a Hundred Columns."),
    dict(id="tomb-path-north", name="Path to the tomb of Artaxerxes II", width=5, style="minor", periods=LATER,
         path=LS([(155, 95), (228, 95)]),
         blurb="A climb up the mountain slope from the terrace to the rock-cut tomb."),
    dict(id="tomb-path-south", name="Path to the tomb of Artaxerxes III", width=5, style="minor", periods=LATER,
         path=LS([(155, -120), (220, -120)]),
         blurb="A climb up the mountain slope from the terrace to the southern rock-cut tomb."),
]

# ---------------------------------------------------------------- walls and gates
TERRACE = [(-150, -228), (-150, 228), (140, 228), (150, 205), (152, -200), (140, -228)]
WALLS = [
    dict(id="terrace-wall", name="Retaining wall of the Takht", closed=True, path=LS(TERRACE),
         blurb="The terrace face of huge polygonal and squared limestone blocks fitted without mortar and held with iron clamps set in lead, rising 12 to 18 m above the plain; the platform behind is part cut rock, part fill. In Achaemenid times a mud-brick wall with towers crowned its edge."),
    dict(id="mountain-wall", name="Fortification on Kuh-e Rahmat", periods=ACHAEMENID,
         path=LS([(140, 228), (260, 300), (380, 260), (430, 80), (410, -150), (300, -280), (140, -228)]),
         blurb="A mud-brick wall on stone footings with towers climbed the mountain behind the terrace, closing the side the terrace face did not protect. The Fortification Tablets were found in its north-east corner, used as fill."),
    dict(id="mountain-wall-ruin", name="Ruined fortification on Kuh-e Rahmat", periods=LATER,
         path=LS([(140, 228), (260, 300), (380, 260), (430, 80), (410, -150), (300, -280), (140, -228)]),
         blurb="Fallen mud brick and stone footings on the slope, the towers reduced to mounds."),
]

GATES = [
    dict(id="great-stair", name="Great double stair", position=L(-158, 162)),
]

AQUEDUCTS = []

# ---------------------------------------------------------------- built-up blocks
OFFICIALS = [(-225, 140), (-440, 140), (-440, -20), (-225, -20)]
WORKERS = [(-225, -60), (-445, -60), (-450, -245), (-225, -245)]
SOUTH = [(-180, -290), (170, -290), (150, -500), (-180, -480)]
WEST = [(-490, 140), (-950, 290), (-980, -280), (-500, -280)]
NORTH = [(-230, 270), (-440, 270), (-445, 600), (-240, 600)]
EAST_TOWN = [(-490, -330), (-900, -360), (-900, -700), (-560, -700)]
BLOCKS = [
    dict(name="Officials' houses below the terrace", periods=ACHAEMENID, density="dense", polygon=LS(OFFICIALS)),
    dict(name="Workers' quarter (kurtash)", periods=ACHAEMENID, density="dense", polygon=LS(WORKERS)),
    dict(name="Houses south of the terrace", periods=ACHAEMENID, density="loose", polygon=LS(SOUTH)),
    dict(name="Western lower town", periods=ACHAEMENID, density="loose", polygon=LS(WEST)),
    dict(name="Northern suburb", periods=["xerxes-460"], density="loose", polygon=LS(NORTH)),
    dict(name="Southern lower town", periods=["xerxes-460"], density="dense", polygon=LS(EAST_TOWN)),
    dict(name="Village in the old officials' quarter", periods=["burned-330"], density="loose", polygon=LS(OFFICIALS)),
    dict(name="Village below the terrace", periods=["burned-330"], density="loose", polygon=LS(WORKERS)),
    dict(name="Western village", periods=["burned-330"], density="loose", polygon=LS([(-500, 120), (-760, 200), (-780, -200), (-510, -250)])),
    dict(name="Village below the ruins", periods=["sasanian-250"], density="loose", polygon=LS([(-230, -60), (-420, -60), (-420, -240), (-230, -240)])),
    dict(name="Village of the canal", periods=["sasanian-250"], density="loose", polygon=LS([(-700, -460), (-1000, -460), (-1000, -700), (-720, -700)])),
    dict(name="Village on the plain", periods=ALL, density="loose", polygon=LS([(-1700, -100), (-2100, -100), (-2100, -320), (-1700, -320)])),
    dict(name="Northern village", periods=LATER, density="loose", polygon=LS([(-250, 700), (-440, 700), (-450, 900), (-260, 900)])),
]

GARDENS = [
    dict(name="Royal paradise (pairidaeza)", periods=ACHAEMENID, kind="park",
         polygon=LS([(-220, -320), (-445, -320), (-445, -660), (-220, -640)])),
    dict(name="Orchards where the paradise was", periods=LATER, kind="orchard",
         polygon=LS([(-220, -320), (-445, -320), (-445, -660), (-220, -640)])),
    dict(name="Northern paradise", periods=ACHAEMENID, kind="park",
         polygon=LS([(-620, 700), (-1000, 760), (-1000, 1200), (-620, 1150)])),
    dict(name="Orchards of the plain", kind="orchard",
         polygon=LS([(-1250, -450), (-1700, -450), (-1700, -900), (-1250, -900)])),
    dict(name="Vineyards", kind="vineyard",
         polygon=LS([(-1100, 480), (-1300, 560), (-1250, 900), (-1050, 880)])),
    dict(name="Orchards toward the river", kind="orchard",
         polygon=LS([(-2000, 500), (-2500, 650), (-2500, 300), (-2050, 200)])),
    dict(name="Gardens south of the town", kind="orchard", periods=["xerxes-460", "burned-330", "sasanian-250"],
         polygon=LS([(-30, -560), (-250, -720), (-200, -1000), (60, -950)])),
]

DISTRICTS = [
    dict(id="takht", name="The Takht (terrace)", polygon=LS(TERRACE),
         description="The royal terrace, about 455 by 300 m and 12 to 18 m above the plain, holding the audience halls, palaces, treasury and barracks. Modern Persians call it Takht-e Jamshid, the Throne of Jamshid; the Greeks called the city Persepolis, the Persians Parsa."),
    dict(id="lower-town", name="Parsa (lower town)", periods=TOWN,
         polygon=LS([(-210, 300), (-1000, 340), (-1000, -720), (-210, -720)]),
         description="The town on the plain: houses of officials, scribes and craftsmen, workshops, storehouses, palaces and paradises. Mostly unexcavated; surveys and soundings show buildings scattered over several square kilometres."),
    dict(id="kurtash", name="Workers' quarter", periods=ACHAEMENID,
         polygon=LS(WORKERS),
         description="Where some of the kurtash, the dependent workers of the tablets, may have lived: stonecutters, carpenters, smiths and their families from across the empire. The location is a guess; the tablets do not say where they slept."),
]

LABELS = [
    dict(text="Pārsa", position=L(-700, 420), size="lg", periods=TOWN),
    dict(text="Ruins of Parsa", position=L(-700, 420), size="lg", periods=["sasanian-250"]),
    dict(text="Takht", position=L(-20, -205), size="sm"),
    dict(text="Kuh-e Rahmat", position=L(800, 120), size="lg", rotation=-80),
    dict(text="Marvdasht plain", position=L(-1700, -1200), size="md"),
    dict(text="Pulvar", position=L(-2100, 1300), size="sm", rotation=40),
    dict(text="to Istakhr (5 km) and Naqsh-e Rustam (6 km)", position=L(-560, 1820), size="sm", rotation=-86),
    dict(text="to Susa", position=L(-2500, 790), size="sm", rotation=-20),
    dict(text="Paradise", position=L(-330, -560), size="sm", periods=ACHAEMENID),
    dict(text="Royal tombs", position=L(330, 0), size="sm", periods=LATER),
]
