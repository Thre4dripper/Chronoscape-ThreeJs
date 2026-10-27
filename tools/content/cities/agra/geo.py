# Agra: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.

LODI, BABUR, AKBAR, SHAHJAHAN, LATE = "lodi-1505", "babur-1530", "akbar-1580", "shahjahan-1650", "jat-maratha-1780"
ALL = [LODI, BABUR, AKBAR, SHAHJAHAN, LATE]
EARLY = [LODI, BABUR]
MUGHAL = [AKBAR, SHAHJAHAN, LATE]
FROM_BABUR = [BABUR, AKBAR, SHAHJAHAN, LATE]
TAJ_ERAS = [SHAHJAHAN, LATE]

CITY = dict(
    name="Agra", subtitle="City of the Taj",
    description="Agra on both banks of the Yamuna, from Sikandar Lodi's brick fort (1505) through the Mughal capital to the decline under the Jats and Marathas (1780): the fort, the old city, Taj Ganj, and the garden-tombs and gardens along both banks. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId=SHAHJAHAN,
    world=dict(heightScale=1.0, walls=["#D9C3A0", "#C99E78", "#E3D3B6", "#B97F5E", "#CDB08A"], roofs=["#BFA584", "#C7AE8A"]),
    camera=dict(target=(27.1775, 78.0320), distance=40),
)
FRAME = ((27.2150, 77.9900), (27.1600, 78.0550))

PALETTE = dict(parchment="#E8D5AC", ink="#6E4A33", water="#6A8C88", hill="#7C805C", road="#8C6B4B")
COMPASS = (27.2095, 78.0500)
CARTOUCHE = (27.1625, 77.9930)

SOURCES = [
    dict(id="koch-taj", title="The Complete Taj Mahal and the Riverfront Gardens of Agra", author="Ebba Koch", year=2006),
    dict(id="koch-mughal", title="Mughal Architecture: An Outline of Its History and Development (1526–1858)", author="Ebba Koch", year=1991),
    dict(id="asher", title="Architecture of Mughal India (The New Cambridge History of India I.4)", author="Catherine B. Asher", year=1992),
    dict(id="baburnama", title="The Baburnama: Memoirs of Babur, Prince and Emperor", author="Babur, trans. Wheeler M. Thackston", year=1996, url="https://en.wikipedia.org/wiki/Baburnama"),
    dict(id="pelsaert", title="Jahangir's India: The Remonstrantie of Francisco Pelsaert", author="Francisco Pelsaert, trans. W. H. Moreland & P. Geyl", year=1925, note="written in Agra, 1626"),
    dict(id="bernier", title="Travels in the Mogul Empire, AD 1656–1668", author="François Bernier", year=1670, url="https://en.wikipedia.org/wiki/Fran%C3%A7ois_Bernier"),
    dict(id="latif", title="Agra, Historical and Descriptive", author="Syad Muhammad Latif", year=1896, url="https://archive.org/details/agrahistoricalde00latiuoft"),
    dict(id="wiki-agra", title="Agra", author="Wikipedia", url="https://en.wikipedia.org/wiki/Agra"),
    dict(id="wiki-yamuna", title="Yamuna", author="Wikipedia", url="https://en.wikipedia.org/wiki/Yamuna"),
]

PERIODS = [
    dict(id=LODI, label="Sikandar Lodi's Agra", year=1505, startYear=1504, endYear=1525,
         summary="Sikandar Lodi, sultan of Delhi, moves his court to Agra in about 1504–06 to watch the Rajput chiefs of Gwalior and Dholpur. The town gathers round Badalgarh, an older brick fort on a rise of the Yamuna's west bank. Houses are of brick and mud, with nobles' compounds and a few mosques; the far bank is fields. In 1505 a great earthquake brings much of it down.",
         population="a few tens of thousands at most (no count survives)",
         feel="Brick dust and wet mortar, camel trains on the Gwalior road, ferrymen calling across a river that is wide and slow in the dry months.",
         style="courtyard",
         houses=dict(title="Brick and mud houses round Badalgarh", text="Mostly one-storey houses of mud and burnt brick round small courts, flat roofs of beaten earth on timber joists, sheds of thatch for cattle. Lanes are unpaved; a noble's compound has a gate, a court, a well and a small mosque."),
         outskirts=dict(title="Hamlets and wells", text="Mud-walled hamlets among wheat, barley and indigo, wells worked by bullocks, tanks and groves. Sikandra, the sultan's new village and garden, lies off the map to the north-west.")),
    dict(id=BABUR, label="Babur's Agra", year=1530, startYear=1526, endYear=1555,
         summary="After Panipat (April 1526) Babur takes Agra and makes it the first Mughal capital. Finding the plain joyless, he crosses the Yamuna and lays out walled gardens with wells, stepped channels and baths on the east bank, the first Mughal charbaghs in India; his begs copy him. The Lodi town and Badalgarh carry on. Babur dies here in December 1530; Humayun and then Sher Shah's Suris hold the city.",
         population="unknown; perhaps a few tens of thousands",
         feel="Creaking Persian wheels and the smell of wet earth in the new gardens; Turki and Persian among the tents and brick pavilions, Hindavi in the bazaar.",
         style="courtyard",
         houses=dict(title="Courtyard houses of the Lodi town", text="Brick houses round courts, a few of two storeys, with flat roofs and parapets for sleeping out in summer. The newcomers camp in tents or build quickly in rubble and brick plastered with lime."),
         outskirts=dict(title="Gardens across the river", text="Walled charbaghs with wells and channels, young orchards, villages between. Babur writes that the Hindustanis called this bank, with its Kabuli-style gardens, 'Kabul'.")),
    dict(id=AKBAR, label="Akbar's Agra", year=1580, startYear=1556, endYear=1627,
         summary="Akbar rebuilds the fort in red sandstone (1565–73) and Agra becomes one of Asia's great cities, though the court lives at Fatehpur Sikri from 1571 to 1585. Nobles' mansions and gardens line both banks; bazaars, sarais and mohallas spread west and north of the fort. Jesuits build a church here in 1599. Under Jahangir Agra is the capital again, and Nur Jahan builds her father's tomb across the river.",
         population="perhaps several hundred thousand; Ralph Fitch (1585) thought Agra and Fatehpur each much greater than London",
         feel="Red sandstone dust from the fort works, elephants at the gates, bales of indigo and cotton on the riverbank, the call to prayer and temple bells in the same lanes.",
         style="courtyard",
         houses=dict(title="Havelis and katras", text="Merchants' and officers' havelis of brick and red sandstone, two or three storeys round courts, carved jharokhas over the lane. Behind them, katras: walled clusters of single rooms round a shared yard with one gate."),
         outskirts=dict(title="Riverside mansions and orchards", text="Nobles' walled gardens and mansions along the Yamuna, mango orchards, brick kilns, indigo vats, and mud-walled villages along the roads out.")),
    dict(id=SHAHJAHAN, label="Akbarabad, City of the Taj", year=1650, startYear=1628, endYear=1707,
         summary="Agra, now Akbarabad, at its height. The Taj Mahal (1632–48) stands in its garden on the riverbank with the markets of Taj Ganj behind it; Shah Jahan has rebuilt the fort palaces in white marble, and Jahanara's Jama Masjid (1648) faces the fort across a new square. In 1648 the court leaves for Shahjahanabad, but Agra stays a vast city of havelis and riverfront gardens on both banks.",
         population="perhaps 500,000–700,000 (travellers' guesses)",
         feel="The rasp of marble polishers in Taj Ganj, boats and water-wheels along the river, carts of indigo and saltpetre, the naubat drums sounding the watches from the fort.",
         style="courtyard",
         houses=dict(title="Havelis, katras and riverfront mansions", text="Brick havelis faced with lime plaster or red sandstone, two to four storeys round one or more courts, with roof terraces and carved jharokhas. Katras of single rooms round shared yards. Nobles' mansions on the river with terraces down to the water."),
         outskirts=dict(title="Gardens, suburbs and sarais", text="Walled riverfront gardens with pavilions and corner towers, mango and citrus orchards, sarais on the roads out, potters' and tanners' quarters, and mud-walled villages.")),
    dict(id=LATE, label="Agra of the Jats and Marathas", year=1780, startYear=1708, endYear=1803,
         summary="Agra has lost its emperors. The Jats of Bharatpur took the city in 1761 and held the fort until 1774; the Mughal general Najaf Khan retook it, and from 1785 Mahadji Scindia's Marathas rule it. Riverfront gardens are abandoned or farmed, havelis stand half empty, Taj Ganj has shrunk, and the Taj garden is overgrown; the tomb stands, though tradition says the Jats carried off its silver doors.",
         population="much reduced; no reliable count (perhaps under 100,000)",
         feel="Jackals in the empty gardens at night, cavalry camped below the fort, cloth, grain and gold lace still haggled over in the bazaars by the Jama Masjid.",
         style="courtyard",
         houses=dict(title="Old havelis, divided", text="Mughal havelis split among many families or left to fall in; new houses are low, built of reused brick and stone. The bazaars round the Jama Masjid stay crowded while the outer mohallas thin into rubble and fields."),
         outskirts=dict(title="Ruined gardens", text="Garden walls breached, pavilions roofless, beds turned over to melons and vegetables; ruined sarais and tombs along the roads and soldiers' camps on the open ground.")),
]

# ---------------------------------------------------------------- water

YAMUNA = [(27.2175, 78.0220), (27.2120, 78.0275), (27.2070, 78.0300), (27.2010, 78.0305), (27.1950, 78.0290), (27.1900, 78.0278),
          (27.1850, 78.0268), (27.1805, 78.0262), (27.1775, 78.0272), (27.1762, 78.0308), (27.1765, 78.0360), (27.1772, 78.0420),
          (27.1778, 78.0470), (27.1798, 78.0510), (27.1840, 78.0538), (27.1890, 78.0555), (27.1950, 78.0575)]

WATER = [
    dict(id="yamuna", name="Yamuna (Jamna)", path=YAMUNA, width=260,
         blurb="The Yamuna swings south past the fort and turns east to the Taj. Mughal Agra was built along it: some forty walled gardens and mansions on the two banks, with terraces and towers on the water. Low and sandy in winter, it runs a kilometre wide in the monsoon."),
]

# ---------------------------------------------------------------- roads

ROADS = [
    dict(id="fatehpur-road", name="Road to Fatehpur Sikri and Ajmer", path=[(27.1803, 78.0186), (27.1800, 78.0100), (27.1815, 78.0030), (27.1830, 77.9890)], width=18, style="major", labelled=True,
         blurb="The road west from the fort's Delhi Gate toward Bayana, Fatehpur Sikri and Ajmer, the pilgrim road to the shrine of Muin al-Din Chishti that Akbar walked on foot."),
    dict(id="sikandra-road", name="Road to Sikandra and Delhi", path=[(27.1800, 78.0100), (27.1860, 78.0085), (27.1920, 78.0060), (27.1990, 78.0010), (27.2070, 77.9950), (27.2150, 77.9893)], width=18, style="major", labelled=True,
         blurb="The imperial highway north-west to Sikandra, Mathura and Delhi, later lined with kos minars marking every two miles."),
    dict(id="gwalior-road", name="Road to Gwalior", path=[(27.1760, 78.0205), (27.1720, 78.0190), (27.1660, 78.0170), (27.1600, 78.0150)], width=16, style="major", labelled=True,
         blurb="South from the fort toward Dholpur, Gwalior and the Deccan: the road of armies and of the Deccan trade."),
    dict(id="belanganj-street", name="Riverside street", path=[(27.1812, 78.0186), (27.1845, 78.0200), (27.1880, 78.0218), (27.1920, 78.0238), (27.1970, 78.0250), (27.2030, 78.0255), (27.2090, 78.0235), (27.2150, 78.0195)], width=12, style="minor", labelled=False,
         periods=[AKBAR, SHAHJAHAN, LATE],
         blurb="The street behind the riverfront mansions north of the fort, where the gates of the havelis faced the town and their gardens faced the river."),
    dict(id="lodi-river-lane", name="Lane along the river", path=[(27.1812, 78.0186), (27.1845, 78.0200), (27.1880, 78.0218)], width=8, style="minor", periods=[LODI, BABUR]),
    dict(id="rauza-road", name="Road of the Rauza", path=[(27.1752, 78.0228), (27.1735, 78.0290), (27.1728, 78.0360), (27.1718, 78.0398), (27.1712, 78.0412)], width=14, style="major", labelled=True,
         periods=TAJ_ERAS,
         blurb="From the fort along the backs of the riverfront havelis to the west gate of the Taj's forecourt. The emperor himself more often went to the tomb by boat."),
    dict(id="tajganj-road", name="Taj Ganj road", path=[(27.1680, 78.0405), (27.1690, 78.0330), (27.1715, 78.0260), (27.1745, 78.0215)], width=12, style="minor", labelled=False, periods=TAJ_ERAS,
         blurb="The road from the city to the bazaars and sarais of Taj Ganj (Mumtazabad)."),
    dict(id="fatehabad-road", name="Road to Fatehabad", path=[(27.1672, 78.0436), (27.1660, 78.0500), (27.1645, 78.0550)], width=12, style="minor", labelled=False, periods=TAJ_ERAS),
    dict(id="firozabad-road", name="Road to Firozabad and Etawah", path=[(27.1870, 78.0300), (27.1875, 78.0340), (27.1895, 78.0420), (27.1925, 78.0500), (27.1955, 78.0550)], width=14, style="major", labelled=True,
         blurb="From the river crossing east across the doab toward Firozabad, Etawah and the road to Bengal."),
    dict(id="garden-lane", name="Lane of the gardens", path=[(27.1875, 78.0340), (27.1930, 78.0337), (27.1980, 78.0362), (27.2040, 78.0372), (27.2100, 78.0367), (27.2150, 78.0338)], width=10, style="minor", labelled=False, periods=FROM_BABUR,
         blurb="The lane behind the east-bank gardens: their gates opened onto it, their terraces onto the river."),
    dict(id="mehtab-lane", name="Lane to the Mahtab Bagh", path=[(27.1893, 78.0410), (27.1850, 78.0418), (27.1815, 78.0421)], width=8, style="minor", periods=TAJ_ERAS),
    dict(id="kachhpura-lane", name="Kachhpura lane", path=[(27.1895, 78.0420), (27.1860, 78.0470), (27.1852, 78.0490)], width=6, style="minor", periods=ALL),
]

BRIDGES = [
    dict(id="bridge-of-boats", name="Bridge of boats", path=[(27.1870, 78.0252), (27.1870, 78.0296)], build="timber", arches=12,
         blurb="A pontoon bridge of boats lashed together and planked over, linking the city to the east bank; travellers describe it in the 17th century. It was taken up when the river rose.",
         periods=[AKBAR, SHAHJAHAN, LATE]),
]

AQUEDUCTS = [
    dict(name="Taj waterworks aqueduct", path=[(27.1752, 78.0392), (27.1745, 78.0405), (27.1742, 78.0412)], periods=TAJ_ERAS),
]

# ---------------------------------------------------------------- built-up areas

KINARI = [(27.1840, 78.0095), (27.1840, 78.0145), (27.1915, 78.0145), (27.1915, 78.0075), (27.1860, 78.0093)]
RAWATPARA = [(27.1840, 78.0150), (27.1840, 78.0190), (27.1870, 78.0205), (27.1915, 78.0225), (27.1915, 78.0150)]
DELHI_GATE = [(27.1808, 78.0105), (27.1835, 78.0105), (27.1835, 78.0180), (27.1810, 78.0182)]
BELANGANJ = [(27.1850, 78.0210), (27.1850, 78.0252), (27.1900, 78.0263), (27.1990, 78.0280), (27.1990, 78.0258), (27.1920, 78.0244), (27.1880, 78.0226)]
INNER_NORTH = [(27.1920, 78.0145), (27.1920, 78.0228), (27.1985, 78.0242), (27.1985, 78.0145)]
WAZIRPURA = [(27.1925, 78.0085), (27.1925, 78.0140), (27.1985, 78.0140), (27.1985, 78.0050), (27.1950, 78.0072)]
LOHAMANDI = [(27.1825, 78.0035), (27.1812, 78.0090), (27.1850, 78.0082), (27.1905, 78.0058), (27.1940, 78.0025), (27.1900, 77.9990), (27.1840, 78.0000)]
SHAHGANJ = [(27.1838, 77.9930), (27.1835, 77.9995), (27.1900, 77.9985), (27.1890, 77.9925)]
NAI_KI_MANDI = [(27.1790, 78.0095), (27.1790, 78.0140), (27.1700, 78.0140), (27.1700, 78.0095)]
CHHIPITOLA = [(27.1790, 78.0145), (27.1790, 78.0180), (27.1740, 78.0182), (27.1700, 78.0168), (27.1700, 78.0145)]
RIVERSIDE_SOUTH = [(27.1747, 78.0250), (27.1752, 78.0290), (27.1748, 78.0360), (27.1750, 78.0395), (27.1730, 78.0398), (27.1738, 78.0360), (27.1745, 78.0290)]
TAJGANJ_N = [(27.1718, 78.0340), (27.1710, 78.0400), (27.1692, 78.0400), (27.1698, 78.0340)]
TAJGANJ_E = [(27.1705, 78.0442), (27.1705, 78.0480), (27.1675, 78.0480), (27.1680, 78.0442)]
TAJGANJ_S = [(27.1660, 78.0380), (27.1662, 78.0428), (27.1640, 78.0480), (27.1625, 78.0400)]
EAST_LANDING = [(27.1884, 78.0300), (27.1912, 78.0302), (27.1912, 78.0328), (27.1884, 78.0330)]
EAST_SOUTH = [(27.1835, 78.0300), (27.1862, 78.0300), (27.1862, 78.0360), (27.1835, 78.0368)]
BEHIND_RIVER_S = [(27.1732, 78.0255), (27.1724, 78.0300), (27.1719, 78.0332), (27.1700, 78.0332), (27.1712, 78.0290), (27.1722, 78.0262)]
KACHHPURA = [(27.1828, 78.0478), (27.1850, 78.0478), (27.1850, 78.0510), (27.1828, 78.0510)]
LODI_NORTH = [(27.1840, 78.0150), (27.1840, 78.0190), (27.1870, 78.0205), (27.1870, 78.0150)]
LODI_RIVER = [(27.1850, 78.0212), (27.1850, 78.0250), (27.1890, 78.0258), (27.1890, 78.0232)]

BLOCKS = [
    dict(name="Mohallas by the Delhi Gate", polygon=DELHI_GATE, density="dense"),
    dict(name="Kinari and Johri Bazaars", polygon=KINARI, density="dense", periods=MUGHAL),
    dict(name="Rawatpara", polygon=RAWATPARA, density="dense", periods=MUGHAL),
    dict(name="North of Badalgarh", polygon=LODI_NORTH, density="loose", periods=EARLY),
    dict(name="Riverside hamlet", polygon=LODI_RIVER, density="loose", periods=EARLY),
    dict(name="Belanganj and the riverfront havelis", polygon=BELANGANJ, density="dense", periods=[AKBAR, SHAHJAHAN]),
    dict(name="Belanganj", polygon=BELANGANJ, density="loose", periods=[LATE]),
    dict(name="Mohallas behind the river", polygon=INNER_NORTH, density="dense", periods=[SHAHJAHAN]),
    dict(name="Mohallas behind the river", polygon=INNER_NORTH, density="loose", periods=[AKBAR, LATE]),
    dict(name="Wazirpura and Padritola", polygon=WAZIRPURA, density="loose", periods=MUGHAL),
    dict(name="Lohamandi", polygon=LOHAMANDI, density="dense", periods=[SHAHJAHAN]),
    dict(name="Lohamandi", polygon=LOHAMANDI, density="loose", periods=[AKBAR, LATE]),
    dict(name="Shahganj", polygon=SHAHGANJ, density="loose", periods=[SHAHJAHAN, LATE]),
    dict(name="Nai ki Mandi", polygon=NAI_KI_MANDI, density="dense", periods=[AKBAR, SHAHJAHAN]),
    dict(name="Nai ki Mandi", polygon=NAI_KI_MANDI, density="loose", periods=[LATE]),
    dict(name="Hamlet west of Badalgarh", polygon=NAI_KI_MANDI, density="loose", periods=EARLY),
    dict(name="Village on the Sikandra road", polygon=[(27.1925, 78.0085), (27.1925, 78.0125), (27.1958, 78.0125), (27.1958, 78.0078)], density="loose", periods=EARLY),
    dict(name="Lohamandi hamlet", polygon=[(27.1840, 78.0020), (27.1825, 78.0060), (27.1860, 78.0070), (27.1880, 78.0030)], density="loose", periods=[BABUR]),
    dict(name="Chhipitola", polygon=CHHIPITOLA, density="dense", periods=MUGHAL),
    dict(name="Huts south of Badalgarh", polygon=CHHIPITOLA, density="loose", periods=EARLY),
    dict(name="Riverfront havelis south of the fort", polygon=RIVERSIDE_SOUTH, density="loose", periods=MUGHAL),
    dict(name="Mohallas behind the river havelis", polygon=BEHIND_RIVER_S, density="dense", periods=[SHAHJAHAN]),
    dict(name="Mohallas behind the river havelis", polygon=BEHIND_RIVER_S, density="loose", periods=[AKBAR, LATE]),
    dict(name="Taj Ganj (Mumtazabad)", polygon=TAJGANJ_N, density="dense", periods=[SHAHJAHAN]),
    dict(name="Taj Ganj", polygon=TAJGANJ_N, density="loose", periods=[LATE]),
    dict(name="Taj Ganj, east", polygon=TAJGANJ_E, density="dense", periods=[SHAHJAHAN]),
    dict(name="Taj Ganj, east", polygon=TAJGANJ_E, density="loose", periods=[LATE]),
    dict(name="Villages south of Taj Ganj", polygon=TAJGANJ_S, density="loose", periods=TAJ_ERAS),
    dict(name="East-bank landing", polygon=EAST_LANDING, density="loose", periods=MUGHAL),
    dict(name="East-bank village", polygon=EAST_SOUTH, density="loose"),
    dict(name="Kachhpura", polygon=KACHHPURA, density="loose"),
]

GARDENS = [
    dict(name="Riverfront gardens of the east bank", polygon=[(27.1790, 78.0290), (27.1828, 78.0290), (27.1828, 78.0392), (27.1790, 78.0395)], kind="orchard", periods=[BABUR, AKBAR, SHAHJAHAN]),
    dict(name="Overgrown gardens of the east bank", polygon=[(27.1790, 78.0290), (27.1828, 78.0290), (27.1828, 78.0392), (27.1790, 78.0395)], kind="orchard", periods=[LATE]),
    dict(name="Gardens by Itimad-ud-Daulah", polygon=[(27.1942, 78.0306), (27.1988, 78.0318), (27.1988, 78.0345), (27.1942, 78.0340)], kind="orchard", periods=MUGHAL),
    dict(name="Gardens of Babur's begs", polygon=[(27.1915, 78.0302), (27.1988, 78.0318), (27.1988, 78.0345), (27.1915, 78.0335)], kind="orchard", periods=[BABUR]),
    dict(name="Babur's garden quarter", polygon=[(27.2015, 78.0325), (27.2045, 78.0322), (27.2045, 78.0355), (27.2015, 78.0355)], kind="orchard", periods=FROM_BABUR),
    dict(name="Mango groves", polygon=[(27.1950, 77.9940), (27.1985, 77.9975), (27.2020, 77.9935), (27.1985, 77.9905)], kind="orchard"),
    dict(name="Orchards of Sikandra road", polygon=[(27.2005, 78.0060), (27.2005, 78.0130), (27.2060, 78.0130), (27.2060, 78.0020)], kind="orchard", periods=MUGHAL),
    dict(name="Gardens north of the city", polygon=[(27.2000, 78.0150), (27.2000, 78.0230), (27.2070, 78.0220), (27.2070, 78.0150)], kind="orchard", periods=[AKBAR, SHAHJAHAN]),
    dict(name="Fields of the east bank", polygon=[(27.1950, 78.0390), (27.1950, 78.0470), (27.2050, 78.0470), (27.2050, 78.0400)], kind="orchard", periods=EARLY),
]

MARSH = [
    dict(name="Sandy floodplain (khadar)", polygon=[(27.1742, 78.0470), (27.1768, 78.0490), (27.1785, 78.0530), (27.1760, 78.0548), (27.1730, 78.0520)]),
    dict(name="Floodplain below Kachhpura", polygon=[(27.1812, 78.0438), (27.1822, 78.0452), (27.1818, 78.0466), (27.1808, 78.0458)]),
]

DISTRICTS = [
    dict(id="old-city", name="The old city (Kinari Bazaar and Rawatpara)", polygon=[(27.1838, 78.0090), (27.1838, 78.0195), (27.1915, 78.0228), (27.1915, 78.0072)], periods=MUGHAL,
         description="The dense heart of Mughal Agra north-west of the fort: the Jama Masjid, the Kinari, Johri and cloth bazaars, temples and mosques, and katras of merchants and craftsmen packed along narrow lanes."),
    dict(id="badalgarh-town", name="The Lodi town", polygon=[(27.1700, 78.0095), (27.1700, 78.0185), (27.1870, 78.0205), (27.1870, 78.0100)], periods=EARLY,
         description="Sikandar Lodi's capital: a town of brick and mud houses gathered round the Badalgarh fort on the west bank, with the houses of the sultan's Afghan nobles."),
    dict(id="belanganj", name="The riverfront north of the fort", polygon=BELANGANJ, periods=MUGHAL,
         description="Mansions of princes and nobles stood shoulder to shoulder along the west bank here, each with a garden on the water; behind them, the grain and timber markets of the river trade."),
    dict(id="taj-ganj", name="Taj Ganj (Mumtazabad)", polygon=[(27.1718, 78.0335), (27.1705, 78.0480), (27.1660, 78.0480), (27.1660, 78.0335)], periods=TAJ_ERAS,
         description="The town built with the Taj: sarais and bazaars whose rents paid for the tomb's upkeep, and the houses of the marble cutters, inlayers and masons who stayed on."),
    dict(id="across-the-jamna", name="Across the Jamna ('Kabul')", polygon=[(27.1830, 78.0300), (27.2130, 78.0300), (27.2130, 78.0390), (27.1830, 78.0390)], periods=FROM_BABUR,
         description="The east bank, where Babur laid out the first Mughal gardens; his memoir says the Hindustanis called it Kabul. Later the site of Nur Jahan's gardens and the tombs of Itimad-ud-Daulah and Afzal Khan."),
]

LABELS = [
    dict(text="Jamna", position=(27.1925, 78.0287), size="lg", rotation=-78),
    dict(text="Yamuna", position=(27.1768, 78.0395), size="md", rotation=-6),
    dict(text="To Sikandra and Delhi", position=(27.2085, 77.9960), size="sm", rotation=38),
    dict(text="To Fatehpur Sikri", position=(27.1847, 77.9945), size="sm", rotation=-6),
    dict(text="To Gwalior", position=(27.1640, 78.0185), size="sm", rotation=70),
    dict(text="To Firozabad", position=(27.1935, 78.0520), size="sm", rotation=-30),
    dict(text="Kachhpura", position=(27.1858, 78.0495), size="sm"),
    dict(text="Rawatpara", position=(27.1895, 78.0190), size="sm", periods=MUGHAL),
    dict(text="Belanganj", position=(27.1960, 78.0230), size="sm", periods=MUGHAL),
    dict(text="Lohamandi", position=(27.1870, 78.0030), size="sm", periods=MUGHAL),
    dict(text="Nai ki Mandi", position=(27.1745, 78.0118), size="sm", periods=MUGHAL),
    dict(text="Taj Ganj", position=(27.1650, 78.0360), size="sm", periods=TAJ_ERAS),
    dict(text="Across the Jamna", position=(27.1985, 78.0430), size="md", periods=FROM_BABUR),
    dict(text="Agra of the Lodis", position=(27.1735, 78.0110), size="md", periods=EARLY),
]
