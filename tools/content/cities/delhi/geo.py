# Delhi, "City of Cities": the northern triangle between the Ridge and the Yamuna,
# from Firoz Shah's Firozabad to Bahadur Shah Zafar's Shahjahanabad.
ALL = ["tughlaq-1380", "surid-1545", "humayun-1570", "shahjahan-1660", "zafar-1850"]
SULTANATE = ["tughlaq-1380"]
DINPANAH = ["surid-1545", "humayun-1570"]
EARLY = ["tughlaq-1380", "surid-1545", "humayun-1570"]
MUGHAL_CITY = ["shahjahan-1660", "zafar-1850"]
PRE_1850 = ["tughlaq-1380", "surid-1545", "humayun-1570", "shahjahan-1660"]
FROM_SURID = ["surid-1545", "humayun-1570", "shahjahan-1660", "zafar-1850"]
FROM_HUMAYUN = ["humayun-1570", "shahjahan-1660", "zafar-1850"]
ZAFAR = ["zafar-1850"]

CITY = dict(
    name="Delhi", subtitle="City of Cities",
    description="Five moments in the northern Delhi triangle between the Ridge and the Yamuna, from Firoz Shah's Firozabad (1380) through Din Panah and Humayun's Tomb to Shah Jahan's walled Shahjahanabad (1660) and Bahadur Shah Zafar's city on the eve of 1857. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="shahjahan-1660",
    world=dict(heightScale=1.0, walls=["#E4D2B0", "#DCC7A2", "#E8DCC4", "#D6B994", "#CDB08A"], roofs=["#D9C4A0", "#CDB48E"]),
    camera=dict(target=(28.6540, 77.2320), distance=40, maxDistance=150),
)
FRAME = ((28.6930, 77.1960), (28.5850, 77.2680))
RESOLUTION = 4096
PALETTE = dict(parchment="#E8D5AC", ink="#6B4A33", water="#66898A", hill="#7C7B58", road="#8C6A48")
COMPASS = (28.6870, 77.2600)
CARTOUCHE = (28.5880, 77.1990)

PERIODS = [
    dict(id="tughlaq-1380", label="Firozabad", year=1380, startYear=1354, endYear=1397,
         summary="Firoz Shah Tughlaq has left the old hill cities to the south and built Firozabad on the Yamuna: a palace-citadel, the Kotla, with a stepped pavilion crowned by an Ashokan pillar he had floated down the river, mosques of rubble and lime plaster, hunting lodges on the Ridge. A spread of mohallas, gardens and villages rather than a walled city, ruled by an old, pious sultan.",
         population="perhaps 150,000 (Firozabad and its suburbs)",
         feel="Lime kilns and rubble masons, the river slapping at the Kotla's ghats, the call to prayer from rough grey domes.",
         style="courtyard",
         houses=dict(title="Mohallas of Firozabad", text="Rubble-and-mud houses round small courts, one or two storeys, flat roofs of earth on timber, whitewashed lime plaster on the better ones. Lanes bend between them to a mosque and a well; the sultan's nobles have walled compounds with gardens."),
         outskirts=dict(title="Gardens and villages", text="Mud-walled villages, orchards watered from wells by bullock-wheels, Firoz's new gardens and the scattered tombs of earlier sultans' men.")),
    dict(id="surid-1545", label="Din Panah and Shergarh", year=1545, startYear=1533, endYear=1555,
         summary="Humayun founded Din Panah, 'refuge of the faith', on the ancient mound of Indarpat in 1533; Sher Shah Sur drove him out in 1540, rebuilt the citadel in grey quartzite and red sandstone and laid out a larger city, Shergarh, reaching north to the Kotla. Sher Shah's mosque in the fort is the finest building of its day. Firozabad is half-abandoned and quarried for stone.",
         population="perhaps 100,000",
         feel="Masons dressing red sandstone at the gates, horsemen of the royal post on the Agra road, a city that has changed masters twice in ten years.",
         style="courtyard",
         houses=dict(title="Houses of Shergarh", text="Rubble and brick courtyard houses with flat roofs, a few of the richer with red sandstone door frames, packed along the roads from the fort gates. Many are new-built on old Firozabad foundations with stone carted from the ruins."),
         outskirts=dict(title="Ruins and villages", text="Fields among the ruined mohallas of Firozabad, grazing on the riverbank, the village round Nizamuddin's shrine.")),
    dict(id="humayun-1570", label="Humayun's Tomb", year=1570, startYear=1556, endYear=1638,
         summary="Humayun died in the Purana Qila in 1556; his widow Haji Begum built his tomb by Nizamuddin's shrine, the first great garden-tomb of India, in red sandstone and white marble, finished about 1572. Akbar rules from Agra, so Delhi is a provincial city of courtiers' tombs, mosques and serais; Maham Anga's madrasa faces the fort, and the Arab Sarai houses Haji Begum's dependants, by tradition Arabs.",
         population="perhaps 80,000",
         feel="Quiet after the court has gone: pilgrims to the shrine, Persian masons' chisels at the tomb, the old fort's gates locked at dusk.",
         style="courtyard",
         houses=dict(title="Houses round the old fort", text="Flat-roofed rubble and brick houses round courts, two storeys at most, along the roads between the Purana Qila, Nizamuddin's village and the tomb garden; nobles' compounds have red sandstone gateways and walled gardens."),
         outskirts=dict(title="Tomb gardens and fields", text="Walled gardens round nobles' tombs, wheat and sugar-cane fields, villages under the ruins of Firozabad.")),
    dict(id="shahjahan-1660", label="Shahjahanabad", year=1660, startYear=1639, endYear=1802,
         summary="Shah Jahan's new capital, built 1639–1648 on the river north of Firozabad: the red-walled fort of Qila-i-Mubarak with marble palaces on the water, the Jama Masjid on its rocky hill, Chandni Chowk with a canal down its middle, Faiz Bazaar, Jahanara's serai and garden, all ringed by a stone wall with fourteen gates. Aurangzeb has just taken the throne.",
         population="perhaps 400,000",
         feel="Elephants and palanquins in Chandni Chowk, the canal glinting under the trees, kettledrums from the Naubat Khana marking the hours.",
         style="courtyard",
         houses=dict(title="Havelis and katras of Shahjahanabad", text="Nobles' havelis of brick and red sandstone round several courts, with zenana quarters and roof terraces; between them, mohallas and katras (gated markets with shops below, rooms above) reached by narrow kuchas closed by wooden gates at night."),
         outskirts=dict(title="Suburbs and gardens", text="Walled gardens of princesses and nobles, grain markets at Paharganj and Sabzi Mandi, potters, washermen and herders' hamlets beyond the walls.")),
    dict(id="zafar-1850", label="Zafar's Delhi", year=1850, startYear=1803, endYear=1857,
         summary="The British have held Delhi since 1803; the Mughal emperor Bahadur Shah Zafar, a poet, keeps court in the Red Fort on a pension, watched by a British Agent. Delhi College teaches Arabic and English in the old Residency, Dara Shikoh's library; St James' Church, the Magazine and bungalows cluster by Kashmiri Gate, and the troops live in cantonments behind the Ridge. A bridge of boats crosses the Yamuna.",
         population="about 150,000",
         feel="Mushairas by lamplight, pigeons wheeling over the rooftops, the church bell by Kashmiri Gate answering the azan.",
         style="courtyard",
         houses=dict(title="Mohallas of late Mughal Delhi", text="Old havelis subdivided among families and tenants, katras rebuilt with stuccoed fronts, carved wooden balconies and doorways; behind Chandni Chowk lanes of two- and three-storey brick houses round tiny courts, roofs given over to kites and pigeons."),
         outskirts=dict(title="Bungalows, gardens and lines", text="British bungalows in walled compounds north of Kashmiri Gate, cantonment lines behind the Ridge, old Mughal gardens, villages and brick kilns.")),
]

# ---------------------------------------------------------------- water
OLD_YAMUNA = [(28.6930, 77.2325), (28.6860, 77.2330), (28.6780, 77.2345), (28.6720, 77.2362), (28.6694, 77.2385), (28.6690, 77.2440), (28.6668, 77.2486),
              (28.6625, 77.2482), (28.6580, 77.2466), (28.6540, 77.2462), (28.6480, 77.2467), (28.6420, 77.2470), (28.6360, 77.2490), (28.6290, 77.2500),
              (28.6200, 77.2505), (28.6100, 77.2512), (28.6000, 77.2560), (28.5930, 77.2600), (28.5850, 77.2620)]
LATE_YAMUNA = [(28.6930, 77.2342), (28.6860, 77.2352), (28.6780, 77.2370), (28.6720, 77.2395), (28.6698, 77.2440), (28.6680, 77.2500), (28.6625, 77.2508),
               (28.6560, 77.2502), (28.6480, 77.2502), (28.6420, 77.2507), (28.6360, 77.2527), (28.6280, 77.2542), (28.6200, 77.2552), (28.6100, 77.2562),
               (28.6000, 77.2602), (28.5930, 77.2642), (28.5850, 77.2662)]
CHANDNI_CANAL = [(28.6567, 77.2226), (28.6568, 77.2250), (28.6573, 77.2285), (28.6568, 77.2300), (28.6561, 77.2340), (28.6562, 77.2381)]
FAIZ_CANAL = [(28.6517, 77.2405), (28.6460, 77.2403), (28.6405, 77.2400)]

WATER = [
    dict(id="yamuna", name="Yamuna", path=OLD_YAMUNA, width=340, periods=PRE_1850,
         blurb="The Yamuna ran close under the high ground here: Firoz Shah's Kotla, Purana Qila, Humayun's Tomb and the Red Fort were all built on its west bank, and in 1660 it lapped the fort's river wall below the marble palaces."),
    dict(id="yamuna-1850", name="Yamuna", path=LATE_YAMUNA, width=300, periods=ZAFAR,
         blurb="By the 19th century the river had drifted east, leaving a sandy flat (the bela) between the fort wall and the water where melons were grown and the bridge of boats landed."),
    dict(id="salimgarh-channel", name="Salimgarh channel", path=[(28.6672, 77.2405), (28.6640, 77.2418), (28.6618, 77.2432), (28.6614, 77.2470)], width=30, periods=FROM_SURID,
         blurb="A side arm of the Yamuna cut Salimgarh off from the mainland; Jahangir bridged it in 1622, and Shah Jahan's fort was set just south of it."),
    dict(id="nahr-i-faiz", name="Nahr-i-Faiz (Chandni Chowk canal)", path=CHANDNI_CANAL, width=6, periods=MUGHAL_CITY,
         blurb="Ali Mardan Khan's canal, brought from the Yamuna far upstream, ran along of Chandni Chowk in a stone channel with pools and trees, then under the Lahori Gate into the fort as the Nahr-i-Bihisht. It silted up in the 18th century and was restored by the British in 1820."),
    dict(id="faiz-canal", name="Faiz Bazaar canal", path=FAIZ_CANAL, width=5, periods=MUGHAL_CITY,
         blurb="A branch of the canal ran down the middle of Faiz Bazaar from the fort's Delhi Gate to the city's Delhi Gate."),
]

ISLANDS = []

HILLS = [
    dict(id="ridge", name="The Ridge", center=(28.6840, 77.2155), radius=380,
         blurb="The last spur of the Aravallis, a rocky quartzite ridge of thorn scrub. Firoz Shah built a hunting lodge on it; in 1857 the British army camped behind it for four months and shelled the city from its batteries at Hindu Rao's house."),
    dict(id="ridge-2", name="The Ridge", center=(28.6900, 77.2195), radius=300, label=False),
    dict(id="ridge-3", name="The Ridge", center=(28.6760, 77.2130), radius=360, label=False),
    dict(id="ridge-4", name="The Ridge", center=(28.6680, 77.2100), radius=320, label=False),
    dict(id="ridge-5", name="The Ridge", center=(28.6600, 77.2070), radius=300, label=False),
    dict(id="ridge-6", name="Jhandewalan ridge", center=(28.6500, 77.2040), radius=330, label=False),
    dict(id="ridge-7", name="Jhandewalan ridge", center=(28.6390, 77.2010), radius=330, label=False),
    dict(id="bhojla", name="Bhojla Pahari", center=(28.6507, 77.2334), radius=90,
         blurb="A low outcrop of rock in the middle of Shahjahanabad, chosen for the Jama Masjid so that it stands above the roofs of the city."),
]

# ---------------------------------------------------------------- roads
KASHMIRI, LAHORI, AJMERI, DELHI_GATE, MORI, KABULI, TURKMAN = (28.6670, 77.2290), (28.6585, 77.2183), (28.6424, 77.2227), (28.6400, 77.2406), (28.6662, 77.2245), (28.6618, 77.2198), (28.6408, 77.2322)

ROADS = [
    # Shahjahanabad
    dict(id="chandni-chowk", name="Chandni Chowk", path=[(28.6562, 77.2383), (28.6561, 77.2340), (28.6568, 77.2300), (28.6573, 77.2285), (28.6568, 77.2250), (28.6567, 77.2226)],
         width=36, style="major", labelled=True, periods=MUGHAL_CITY,
         blurb="Jahanara's processional avenue from the fort's Lahori Gate to the Fatehpuri Masjid, about 1.3 km long and 40 yards wide, with the canal and shade trees down its middle and arcaded shops on both sides; named after the moonlit pool in its octagonal square."),
    dict(id="faiz-bazaar", name="Faiz Bazaar", path=[(28.6517, 77.2410), (28.6460, 77.2408), (28.6402, 77.2406)], width=30, style="major", labelled=True, periods=MUGHAL_CITY,
         blurb="The second great avenue, from the fort's Delhi Gate south to the city's Delhi Gate, laid out by Akbarabadi Begum with a canal down the centre. Daryaganj lay to its east."),
    dict(id="khas-bazaar", name="Khas Bazaar", path=[(28.6510, 77.2342), (28.6525, 77.2368), (28.6545, 77.2386)], width=14, periods=MUGHAL_CITY,
         blurb="The bazaar between the Jama Masjid's east gate and the fort, where nobles' retinues waited; Urdu Bazaar ran beside it."),
    dict(id="dariba", name="Dariba Kalan", path=[(28.6559, 77.2346), (28.6540, 77.2342), (28.6520, 77.2338)], width=8, periods=MUGHAL_CITY,
         blurb="The 'street of the incomparable pearl', a lane of jewellers and silversmiths from Chandni Chowk to the Jama Masjid."),
    dict(id="chawri", name="Chawri Bazaar", path=[(28.6503, 77.2326), (28.6498, 77.2295), (28.6492, 77.2265)], width=12, periods=MUGHAL_CITY,
         blurb="From the Jama Masjid west to Hauz Qazi; in the 18th and 19th centuries the quarter of brass-sellers and of the courtesans' salons."),
    dict(id="lal-kuan", name="Lal Kuan", path=[(28.6492, 77.2265), (28.6525, 77.2245), (28.6560, 77.2228)], width=10, periods=MUGHAL_CITY,
         blurb="The street of the red well, from Hauz Qazi north to the Fatehpuri Masjid."),
    dict(id="hauz-qazi-ajmeri", name="Ajmeri Bazaar", path=[(28.6492, 77.2265), (28.6460, 77.2250), (28.6426, 77.2228)], width=10, periods=MUGHAL_CITY),
    dict(id="khari-baoli", name="Khari Baoli", path=[(28.6567, 77.2215), (28.6577, 77.2198), (28.6585, 77.2185)], width=14, periods=MUGHAL_CITY,
         blurb="West of the Fatehpuri Masjid to the Lahori Gate, named after a brackish step-well; later the city's great spice and grain market."),
    dict(id="esplanade-road", name="Road to Kashmiri Gate", path=[(28.6575, 77.2378), (28.6610, 77.2345), (28.6640, 77.2310), (28.6668, 77.2292)], width=10, periods=MUGHAL_CITY),
    dict(id="turkman-road", name="Road to Turkman Gate", path=[(28.6498, 77.2320), (28.6450, 77.2322), (28.6410, 77.2322)], width=8, periods=MUGHAL_CITY),
    # roads out of the gates
    dict(id="karnal-road", name="Road to Karnal and Lahore", path=[(28.6672, 77.2290), (28.6740, 77.2275), (28.6800, 77.2255), (28.6870, 77.2232), (28.6930, 77.2222)],
         width=14, style="major", labelled=True, periods=MUGHAL_CITY,
         blurb="The imperial highway north to Panipat, Karnal and Lahore left Kashmiri Gate along the river past the gardens; the British Civil Lines grew along it."),
    dict(id="lahore-road", name="Road to Sabzi Mandi", path=[(28.6585, 77.2183), (28.6610, 77.2130), (28.6650, 77.2075), (28.6700, 77.2020), (28.6760, 77.1960)], width=12, style="major", periods=MUGHAL_CITY,
         blurb="From the Lahori and Kabuli gates past the vegetable market of Sabzi Mandi and through the gap in the Ridge towards the Grand Trunk Road."),
    dict(id="mori-road", name="Road to Roshanara Bagh", path=[(28.6662, 77.2245), (28.6700, 77.2180), (28.6760, 77.2090), (28.6795, 77.2040)], width=8, periods=MUGHAL_CITY),
    dict(id="ajmer-road", name="Road to Ajmer", path=[(28.6422, 77.2232), (28.6395, 77.2225), (28.6360, 77.2180), (28.6300, 77.2100), (28.6220, 77.2020), (28.6150, 77.1960)],
         width=12, style="major", labelled=True, periods=MUGHAL_CITY,
         blurb="South-west from Ajmeri Gate past Paharganj and Jaisinghpura towards Ajmer and the shrine of Muinuddin Chishti."),
    dict(id="paharganj-road", name="Paharganj road", path=[(28.6440, 77.2196), (28.6450, 77.2140), (28.6460, 77.2080)], width=8, periods=MUGHAL_CITY),
    dict(id="mathura-road", name="Road to Mathura and Agra", path=[DELHI_GATE, (28.6385, 77.2408), (28.6250, 77.2410), (28.6118, 77.2410), (28.6050, 77.2424), (28.5960, 77.2447), (28.5850, 77.2472)],
         width=16, style="major", labelled=True, periods=MUGHAL_CITY,
         blurb="Out of the Delhi Gate past the ruins of Firozabad, the Purana Qila and Humayun's Tomb, to Mathura and Agra: the road of every Mughal march south."),
    dict(id="mehrauli-road", name="Road to Mehrauli", path=[(28.6380, 77.2390), (28.6280, 77.2330), (28.6150, 77.2270), (28.6000, 77.2200), (28.5850, 77.2140)], width=10, periods=MUGHAL_CITY,
         blurb="South-west through the old ruin-field to the Qutb and the first cities of Delhi."),
    dict(id="nizamuddin-lane", name="Road to Nizamuddin", path=[(28.5960, 77.2447), (28.5935, 77.2435), (28.5922, 77.2432)], width=6, periods=ALL),
    # Firozabad
    dict(id="firozabad-road", name="Road to Old Delhi and Jahanpanah", path=[(28.6380, 77.2420), (28.6280, 77.2340), (28.6150, 77.2280), (28.6000, 77.2200), (28.5850, 77.2140)],
         width=12, style="major", labelled=True, periods=SULTANATE,
         blurb="Firozabad's road south-west to the older cities at Siri, Jahanpanah and Mehrauli, about ten miles off; Firoz lined such roads with serais and wells."),
    dict(id="kushk-road", name="Road to the Kushk-i-Shikar", path=[(28.6420, 77.2410), (28.6520, 77.2340), (28.6620, 77.2250), (28.6700, 77.2180), (28.6735, 77.2150)], width=8, periods=SULTANATE,
         blurb="North from the Kotla through the suburbs to the sultan's hunting palace on the Ridge."),
    dict(id="river-road-sultanate", name="River road to Kilokhri", path=[(28.6340, 77.2430), (28.6200, 77.2420), (28.6100, 77.2405), (28.6000, 77.2420), (28.5925, 77.2440), (28.5850, 77.2470)],
         width=10, style="major", periods=SULTANATE),
    # Din Panah and Shergarh
    dict(id="agra-road", name="Sher Shah's road to Agra", path=[(28.6385, 77.2408), (28.6250, 77.2410), (28.6118, 77.2410), (28.6050, 77.2424), (28.5960, 77.2447), (28.5850, 77.2472)],
         width=14, style="major", labelled=True, periods=DINPANAH,
         blurb="Sher Shah rebuilt the great road from Bengal to the Indus with serais, wells and post-horses every few miles; through Delhi it ran under the walls of his fort."),
    dict(id="shergarh-north-road", name="Road to Firozabad", path=[(28.6385, 77.2408), (28.6450, 77.2380), (28.6560, 77.2330), (28.6700, 77.2200)], width=8, periods=DINPANAH),
    dict(id="shergarh-mehrauli", name="Road to Mehrauli", path=[(28.6250, 77.2410), (28.6150, 77.2300), (28.6000, 77.2200), (28.5850, 77.2140)], width=10, periods=DINPANAH),
]

# ---------------------------------------------------------------- walls and gates
CITY_WALL = [KASHMIRI, (28.6690, 77.2318), (28.6668, 77.2345), (28.6650, 77.2370), (28.6632, 77.2392), (28.6608, 77.2410), (28.6606, 77.2440),
             (28.6518, 77.2441), (28.6480, 77.2444), (28.6440, 77.2446), (28.6400, 77.2446), DELHI_GATE, TURKMAN, (28.6418, 77.2260), AJMERI,
             (28.6440, 77.2195), (28.6520, 77.2180), LAHORI, KABULI, (28.6648, 77.2208), MORI]

WALLS = [
    dict(id="shahjahanabad-wall", name="Wall of Shahjahanabad", path=CITY_WALL, closed=True, periods=MUGHAL_CITY,
         blurb="First an earthen rampart (1650), rebuilt in stone in 1651–58: about six kilometres round, with bastions every few hundred yards and fourteen gates. The British repaired and strengthened its northern face with new bastions in the early 19th century; it held them off for four months in 1857."),
    dict(id="shergarh-wall", name="Wall of Shergarh", path=[(28.6118, 77.2402), (28.6200, 77.2398), (28.6300, 77.2395), (28.6385, 77.2402), (28.6392, 77.2432)], closed=False, periods=DINPANAH,
         blurb="Sher Shah's city wall ran from the Purana Qila north to the Kabuli Darwaza opposite the Kotla; only its two gates survive and its line is conjectural."),
    dict(id="shergarh-wall-ruin", name="Ruined wall of Shergarh", path=[(28.6118, 77.2402), (28.6200, 77.2398), (28.6300, 77.2395), (28.6385, 77.2402)], closed=False, periods=["shahjahan-1660"],
         blurb="By Shah Jahan's day the Surid wall was a crumbling bank between fields, its stone taken for the new city."),
]

GATES = [
    dict(id="mori-gate", name="Mori Gate", position=MORI, periods=MUGHAL_CITY),
    dict(id="kabuli-gate", name="Kabuli Gate", position=KABULI, periods=MUGHAL_CITY),
    dict(id="farrash-khana-gate", name="Farrash Khana Gate", position=(28.6520, 77.2180), periods=MUGHAL_CITY),
    dict(id="turkman-gate", name="Turkman Gate", position=TURKMAN, periods=MUGHAL_CITY),
    dict(id="raj-ghat-gate", name="Raj Ghat Gate", position=(28.6440, 77.2446), periods=MUGHAL_CITY),
    dict(id="khizri-gate", name="Khizri Gate", position=(28.6480, 77.2444), periods=MUGHAL_CITY),
    dict(id="nigambodh-gate", name="Nigambodh Gate", position=(28.6650, 77.2370), periods=MUGHAL_CITY),
    dict(id="kela-ghat-gate", name="Kela Ghat Gate", position=(28.6632, 77.2392), periods=MUGHAL_CITY),
    dict(id="badar-rau-gate", name="Badar Rau Gate", position=(28.6668, 77.2345), periods=MUGHAL_CITY),
    dict(id="water-bastion", name="Water Bastion", position=(28.6690, 77.2318), periods=ZAFAR),
    dict(id="kabuli-darwaza", name="Kabuli Darwaza (Khuni Darwaza)", position=(28.6388, 77.2402), periods=["surid-1545", "humayun-1570", "shahjahan-1660", "zafar-1850"]),
]

BRIDGES = [
    dict(id="salimgarh-bridge", name="Salimgarh bridge", path=[(28.6625, 77.2441), (28.6605, 77.2441)], build="stone", arches=5, landmarkId="salimgarh", periods=["shahjahan-1660", "zafar-1850"],
         blurb="Jahangir's bridge of 1622 across the channel to Salimgarh; Shah Jahan linked it to the fort, and Bahadur Shah Zafar is said to have left the fort this way in September 1857."),
    dict(id="bridge-of-boats", name="Bridge of boats", path=[(28.6648, 77.2462), (28.6648, 77.2540)], build="timber", arches=12, periods=ZAFAR,
         blurb="A pontoon bridge on moored boats carried the road to Meerut across the Yamuna below Salimgarh; on 11 May 1857 the mutineers from Meerut rode over it into Delhi."),
]

AQUEDUCTS = [
    dict(name="Ali Mardan Khan's canal", path=[(28.6830, 77.1960), (28.6740, 77.2040), (28.6680, 77.2110), (28.6640, 77.2170), (28.6618, 77.2198)], periods=MUGHAL_CITY),
]

# ---------------------------------------------------------------- built-up areas
SHAHJAHAN, LATER_RUINS = ["shahjahan-1660"], ["humayun-1570", "shahjahan-1660", "zafar-1850"]
BLOCKS = [
    # Firozabad, 1380
    dict(name="Firozabad", polygon=[(28.6440, 77.2335), (28.6440, 77.2432), (28.6380, 77.2432), (28.6330, 77.2425), (28.6320, 77.2355), (28.6380, 77.2315)], density="dense", periods=SULTANATE),
    dict(name="Firozabad, northern mohallas", polygon=[(28.6560, 77.2255), (28.6555, 77.2420), (28.6452, 77.2430), (28.6452, 77.2285)], density="loose", periods=SULTANATE),
    dict(name="Firozabad, southern suburbs", polygon=[(28.6318, 77.2370), (28.6318, 77.2440), (28.6200, 77.2440), (28.6200, 77.2365)], density="loose", periods=SULTANATE),
    dict(name="Firozabad, by the Ridge", polygon=[(28.6700, 77.2180), (28.6700, 77.2260), (28.6620, 77.2280), (28.6610, 77.2210)], density="loose", periods=SULTANATE),
    dict(name="Firozabad, western mohallas", polygon=[(28.6450, 77.2200), (28.6450, 77.2280), (28.6330, 77.2310), (28.6330, 77.2230)], density="loose", periods=SULTANATE),
    dict(name="Indarpat", polygon=[(28.6130, 77.2412), (28.6130, 77.2462), (28.6060, 77.2462), (28.6060, 77.2412)], density="loose", periods=SULTANATE),
    # Shergarh and Din Panah
    dict(name="Shergarh", polygon=[(28.6250, 77.2416), (28.6250, 77.2472), (28.6132, 77.2472), (28.6130, 77.2416)], density="dense", periods=DINPANAH),
    dict(name="Shergarh, west of the road", polygon=[(28.6300, 77.2370), (28.6300, 77.2400), (28.6130, 77.2402), (28.6130, 77.2375)], density="dense", periods=["surid-1545"]),
    dict(name="Shergarh, north", polygon=[(28.6378, 77.2414), (28.6378, 77.2432), (28.6330, 77.2434), (28.6258, 77.2470), (28.6258, 77.2416)], density="loose", periods=DINPANAH),
    dict(name="Old Firozabad", polygon=[(28.6460, 77.2330), (28.6460, 77.2440), (28.6395, 77.2440), (28.6395, 77.2330)], density="loose", periods=DINPANAH),
    dict(name="Shergarh, west of the road", polygon=[(28.6300, 77.2370), (28.6300, 77.2400), (28.6130, 77.2402), (28.6130, 77.2375)], density="loose", periods=["humayun-1570"]),
    dict(name="Nobles' houses by Nizamuddin", polygon=[(28.5985, 77.2448), (28.5985, 77.2466), (28.5958, 77.2468), (28.5956, 77.2452)], density="loose", periods=FROM_HUMAYUN),
    dict(name="Arab Sarai", polygon=[(28.5905, 77.2460), (28.5905, 77.2494), (28.5880, 77.2494), (28.5880, 77.2460)], density="dense", periods=FROM_HUMAYUN),
    # villages of every era
    dict(name="Ghiyaspur (Nizamuddin basti)", polygon=[(28.5945, 77.2395), (28.5945, 77.2440), (28.5895, 77.2440), (28.5895, 77.2395)], density="dense", periods=ALL),
    dict(name="Raisina", polygon=[(28.6172, 77.2040), (28.6170, 77.2082), (28.6140, 77.2085), (28.6138, 77.2042)], density="loose", periods=ALL),
    dict(name="Chandrawal", polygon=[(28.6918, 77.2282), (28.6918, 77.2318), (28.6893, 77.2318), (28.6892, 77.2286)], density="loose", periods=ALL),
    dict(name="Sarai Kale Khan", polygon=[(28.5902, 77.2528), (28.5902, 77.2562), (28.5870, 77.2562), (28.5870, 77.2530)], density="loose", periods=FROM_SURID),
    dict(name="Kotla village", polygon=[(28.6330, 77.2420), (28.6330, 77.2465), (28.6300, 77.2465), (28.6300, 77.2420)], density="loose", periods=LATER_RUINS),
    dict(name="Indarpat village", polygon=[(28.6060, 77.2400), (28.6060, 77.2416), (28.6030, 77.2425), (28.6030, 77.2400)], density="loose", periods=MUGHAL_CITY),
    # remains of the earlier cities
    dict(name="Ruins of Firozabad", polygon=[(28.6392, 77.2330), (28.6392, 77.2398), (28.6335, 77.2418), (28.6305, 77.2365)], density="loose", periods=LATER_RUINS),
    dict(name="Ruins of Shergarh", polygon=[(28.6250, 77.2416), (28.6250, 77.2470), (28.6186, 77.2470), (28.6185, 77.2416)], density="loose", periods=MUGHAL_CITY),
    # Shahjahanabad inside the walls, packed between the main streets
    dict(name="Katra Neel and Fatehpuri", polygon=[(28.6582, 77.2190), (28.6616, 77.2204), (28.6644, 77.2213), (28.6656, 77.2245), (28.6658, 77.2270), (28.6587, 77.2270), (28.6576, 77.2238), (28.6572, 77.2226)], density="dense", periods=MUGHAL_CITY),
    dict(name="Mansions by Kashmiri Gate", polygon=[(28.6658, 77.2273), (28.6666, 77.2295), (28.6684, 77.2318), (28.6664, 77.2343), (28.6646, 77.2367), (28.6630, 77.2386), (28.6627, 77.2338), (28.6627, 77.2273)], density="dense", periods=SHAHJAHAN),
    dict(name="British quarter by Kashmiri Gate", polygon=[(28.6658, 77.2273), (28.6666, 77.2295), (28.6684, 77.2318), (28.6664, 77.2343), (28.6646, 77.2367), (28.6630, 77.2386), (28.6627, 77.2338), (28.6627, 77.2273)], density="loose", periods=ZAFAR),
    dict(name="Chhatta Shah Ji and Bhagirath", polygon=[(28.6625, 77.2338), (28.6628, 77.2384), (28.6611, 77.2398), (28.6600, 77.2372), (28.6568, 77.2372), (28.6566, 77.2338)], density="dense", periods=MUGHAL_CITY),
    dict(name="Shops north of the chowk", polygon=[(28.6584, 77.2268), (28.6585, 77.2336), (28.6568, 77.2336), (28.6577, 77.2292), (28.6575, 77.2268)], density="dense", periods=MUGHAL_CITY),
    dict(name="Farrash Khana and Kucha Pati Ram", polygon=[(28.6560, 77.2214), (28.6546, 77.2192), (28.6520, 77.2185), (28.6446, 77.2199), (28.6432, 77.2228), (28.6442, 77.2246), (28.6492, 77.2261), (28.6526, 77.2243), (28.6559, 77.2226)], density="dense", periods=MUGHAL_CITY),
    dict(name="Ballimaran and Kucha Rahman", polygon=[(28.6564, 77.2232), (28.6566, 77.2252), (28.6569, 77.2285), (28.6563, 77.2302), (28.6556, 77.2336), (28.6522, 77.2332), (28.6507, 77.2322), (28.6497, 77.2268), (28.6526, 77.2248)], density="dense", periods=MUGHAL_CITY),
    dict(name="Kinari Bazaar and Dariba", polygon=[(28.6556, 77.2340), (28.6558, 77.2369), (28.6528, 77.2371), (28.6516, 77.2346)], density="dense", periods=MUGHAL_CITY),
    dict(name="Urdu Bazaar and Khas Bazaar", polygon=[(28.6514, 77.2346), (28.6526, 77.2373), (28.6514, 77.2400), (28.6500, 77.2400), (28.6498, 77.2346)], density="dense", periods=MUGHAL_CITY),
    dict(name="Sita Ram Bazaar and Hauz Qazi", polygon=[(28.6494, 77.2268), (28.6501, 77.2324), (28.6440, 77.2330), (28.6413, 77.2324), (28.6421, 77.2263), (28.6431, 77.2236), (28.6443, 77.2250)], density="dense", periods=MUGHAL_CITY),
    dict(name="Matia Mahal and Chitli Qabar", polygon=[(28.6497, 77.2333), (28.6497, 77.2397), (28.6406, 77.2397), (28.6413, 77.2333)], density="dense", periods=MUGHAL_CITY),
    dict(name="Daryaganj", polygon=[(28.6512, 77.2419), (28.6512, 77.2437), (28.6406, 77.2441), (28.6406, 77.2419)], density="dense", periods=SHAHJAHAN),
    dict(name="Daryaganj", polygon=[(28.6512, 77.2419), (28.6512, 77.2437), (28.6406, 77.2441), (28.6406, 77.2419)], density="loose", periods=ZAFAR),
    # suburbs outside the walls
    dict(name="Paharganj", polygon=[(28.6520, 77.2085), (28.6515, 77.2168), (28.6455, 77.2178), (28.6426, 77.2150), (28.6431, 77.2085)], density="loose", periods=SHAHJAHAN),
    dict(name="Paharganj", polygon=[(28.6520, 77.2085), (28.6515, 77.2168), (28.6455, 77.2178), (28.6426, 77.2150), (28.6431, 77.2085)], density="dense", periods=ZAFAR),
    dict(name="Mughalpura", polygon=[(28.6612, 77.2102), (28.6600, 77.2170), (28.6545, 77.2172), (28.6530, 77.2108)], density="loose", periods=SHAHJAHAN),
    dict(name="Kishanganj and Teliwara", polygon=[(28.6612, 77.2102), (28.6600, 77.2170), (28.6545, 77.2172), (28.6530, 77.2108)], density="dense", periods=ZAFAR),
    dict(name="Sabzi Mandi", polygon=[(28.6735, 77.1972), (28.6730, 77.2040), (28.6690, 77.2060), (28.6650, 77.2050), (28.6645, 77.1976)], density="loose", periods=SHAHJAHAN),
    dict(name="Sabzi Mandi", polygon=[(28.6735, 77.1972), (28.6730, 77.2040), (28.6690, 77.2060), (28.6650, 77.2050), (28.6645, 77.1976)], density="dense", periods=ZAFAR),
    dict(name="Jaisinghpura", polygon=[(28.6290, 77.2050), (28.6280, 77.2110), (28.6220, 77.2120), (28.6230, 77.2060)], density="loose", periods=MUGHAL_CITY),
    dict(name="Serai and houses outside Delhi Gate", polygon=[(28.6392, 77.2402), (28.6392, 77.2432), (28.6372, 77.2434), (28.6372, 77.2414)], density="loose", periods=MUGHAL_CITY),
    dict(name="Mehndiyan", polygon=[(28.6395, 77.2345), (28.6395, 77.2392), (28.6372, 77.2392), (28.6372, 77.2350)], density="loose", periods=ZAFAR),
    dict(name="Village on the Ajmer road", polygon=[(28.6395, 77.2150), (28.6395, 77.2192), (28.6368, 77.2195), (28.6366, 77.2152)], density="loose", periods=MUGHAL_CITY),
    dict(name="Village on the Mehrauli road", polygon=[(28.6088, 77.2220), (28.6088, 77.2258), (28.6060, 77.2260), (28.6060, 77.2222)], density="loose", periods=ALL),
    dict(name="Civil Lines", polygon=[(28.6880, 77.2235), (28.6870, 77.2300), (28.6760, 77.2318), (28.6740, 77.2270)], density="loose", periods=ZAFAR),
    dict(name="Cantonment lines", polygon=[(28.6925, 77.1990), (28.6925, 77.2120), (28.6880, 77.2110), (28.6880, 77.1990)], density="loose", periods=ZAFAR),
]

GARDENS = [
    dict(name="Begum Bagh (Sahibabad)", polygon=[(28.6625, 77.2272), (28.6625, 77.2335), (28.6588, 77.2335), (28.6585, 77.2272)], kind="park", periods=SHAHJAHAN),
    dict(name="Begum Bagh", polygon=[(28.6625, 77.2272), (28.6625, 77.2335), (28.6600, 77.2335), (28.6598, 77.2302), (28.6586, 77.2272)], kind="park", periods=ZAFAR),
    dict(name="Roshanara Bagh", polygon=[(28.6830, 77.1990), (28.6830, 77.2045), (28.6780, 77.2045), (28.6780, 77.1990)], kind="park", periods=MUGHAL_CITY),
    dict(name="Tis Hazari Bagh", polygon=[(28.6700, 77.2160), (28.6700, 77.2205), (28.6665, 77.2215), (28.6668, 77.2165)], kind="orchard", periods=MUGHAL_CITY),
    dict(name="Orchards north of the city", polygon=[(28.6760, 77.2185), (28.6758, 77.2240), (28.6712, 77.2246), (28.6710, 77.2192)], kind="orchard", periods=MUGHAL_CITY),
    dict(name="Qudsia Bagh", polygon=[(28.6750, 77.2285), (28.6745, 77.2335), (28.6705, 77.2340), (28.6705, 77.2300)], kind="park", periods=ZAFAR),
    dict(name="Mahaldar Khan's garden", polygon=[(28.6690, 77.2050), (28.6690, 77.2085), (28.6668, 77.2088), (28.6668, 77.2052)], kind="orchard", periods=ZAFAR),
    dict(name="Bagh-i-Firoz", polygon=[(28.6300, 77.2330), (28.6300, 77.2365), (28.6250, 77.2365), (28.6250, 77.2330)], kind="orchard", periods=SULTANATE),
    dict(name="Orchards of Firozabad", polygon=[(28.6600, 77.2280), (28.6600, 77.2340), (28.6565, 77.2345), (28.6565, 77.2280)], kind="orchard", periods=SULTANATE),
    dict(name="Firoz Shah's gardens by the Ridge", polygon=[(28.6740, 77.2172), (28.6740, 77.2240), (28.6706, 77.2250), (28.6706, 77.2176)], kind="orchard", periods=SULTANATE),
    dict(name="Bu Halima's garden", polygon=[(28.5945, 77.2487), (28.5945, 77.2496), (28.5935, 77.2496), (28.5935, 77.2487)], kind="park", periods=FROM_SURID),
    dict(name="Fields of Indarpat", polygon=[(28.6040, 77.2280), (28.6040, 77.2370), (28.5970, 77.2380), (28.5970, 77.2290)], kind="orchard", periods=ALL),
    dict(name="Tomb gardens of Akbar's nobles", polygon=[(28.6035, 77.2386), (28.6035, 77.2424), (28.5995, 77.2430), (28.5995, 77.2388)], kind="park", periods=FROM_HUMAYUN),
    dict(name="Tomb garden north of Humayun's", polygon=[(28.5985, 77.2472), (28.5985, 77.2520), (28.5960, 77.2525), (28.5960, 77.2472)], kind="park", periods=FROM_HUMAYUN),
    dict(name="Orchards by Nizamuddin", polygon=[(28.5965, 77.2330), (28.5965, 77.2385), (28.5935, 77.2385), (28.5935, 77.2332)], kind="orchard", periods=ALL),
    dict(name="Tomb garden by the Mathura road", polygon=[(28.6320, 77.2380), (28.6320, 77.2402), (28.6290, 77.2402), (28.6290, 77.2376)], kind="park", periods=MUGHAL_CITY),
    dict(name="Orchards among the ruins", polygon=[(28.6290, 77.2420), (28.6290, 77.2462), (28.6256, 77.2466), (28.6256, 77.2420)], kind="orchard", periods=MUGHAL_CITY),
    dict(name="Tomb gardens south of Shergarh", polygon=[(28.6180, 77.2420), (28.6180, 77.2468), (28.6140, 77.2470), (28.6140, 77.2420)], kind="park", periods=MUGHAL_CITY),
    dict(name="Orchards west of the Mathura road", polygon=[(28.6260, 77.2340), (28.6260, 77.2395), (28.6200, 77.2398), (28.6195, 77.2345)], kind="orchard", periods=["humayun-1570", "shahjahan-1660", "zafar-1850"]),
    dict(name="Gardens below the Ridge", polygon=[(28.6180, 77.2300), (28.6180, 77.2380), (28.6126, 77.2384), (28.6120, 77.2310)], kind="orchard", periods=MUGHAL_CITY),
    dict(name="Orchards round the baoli", polygon=[(28.6300, 77.2200), (28.6300, 77.2280), (28.6230, 77.2285), (28.6225, 77.2210)], kind="orchard", periods=ALL),
    dict(name="Gardens of Jaisinghpura", polygon=[(28.6340, 77.2030), (28.6345, 77.2090), (28.6300, 77.2075), (28.6290, 77.2025)], kind="orchard", periods=MUGHAL_CITY),
    dict(name="Orchards of Raisina", polygon=[(28.6100, 77.2100), (28.6100, 77.2200), (28.6040, 77.2200), (28.6040, 77.2100)], kind="orchard", periods=ALL),
    dict(name="Orchards on the Ajmer road", polygon=[(28.6240, 77.2130), (28.6240, 77.2190), (28.6190, 77.2192), (28.6188, 77.2132)], kind="orchard", periods=ALL),
    dict(name="Fields of the plain", polygon=[(28.5960, 77.2100), (28.5960, 77.2200), (28.5900, 77.2205), (28.5900, 77.2100)], kind="orchard", periods=ALL),
    dict(name="Fields by Ghiyaspur", polygon=[(28.5930, 77.2250), (28.5930, 77.2330), (28.5880, 77.2332), (28.5880, 77.2252)], kind="orchard", periods=ALL),
    dict(name="Fields of Shahdara", polygon=[(28.6920, 77.2500), (28.6920, 77.2620), (28.6845, 77.2625), (28.6840, 77.2510)], kind="orchard", periods=ALL),
    dict(name="Fields of Shahdara", polygon=[(28.6550, 77.2600), (28.6550, 77.2670), (28.6400, 77.2670), (28.6400, 77.2605)], kind="orchard", periods=ALL),
    dict(name="Melon fields on the bela", polygon=[(28.6600, 77.2450), (28.6600, 77.2475), (28.6520, 77.2480), (28.6520, 77.2450)], kind="vineyard", periods=ZAFAR),
]

# the floodplain (khadar) along the river, shaped to each era's course
MARSH = [
    dict(name="Khadar north of the bend", polygon=[(28.6928, 77.2352), (28.6880, 77.2350), (28.6830, 77.2356), (28.6780, 77.2366), (28.6735, 77.2380), (28.6712, 77.2400), (28.6708, 77.2440), (28.6698, 77.2480), (28.6703, 77.2518), (28.6740, 77.2510), (28.6775, 77.2470), (28.6800, 77.2432), (28.6850, 77.2416), (28.6895, 77.2394), (28.6928, 77.2402)], periods=PRE_1850),
    dict(name="Shahdara khadar", polygon=[(28.6660, 77.2512), (28.6620, 77.2503), (28.6575, 77.2488), (28.6530, 77.2482), (28.6470, 77.2486), (28.6420, 77.2490), (28.6380, 77.2500), (28.6362, 77.2512), (28.6376, 77.2546), (28.6420, 77.2561), (28.6480, 77.2552), (28.6530, 77.2566), (28.6580, 77.2548), (28.6630, 77.2557), (28.6662, 77.2536)], periods=PRE_1850),
    dict(name="Patparganj khadar", polygon=[(28.6320, 77.2520), (28.6250, 77.2524), (28.6180, 77.2526), (28.6110, 77.2533), (28.6050, 77.2560), (28.5990, 77.2585), (28.5930, 77.2622), (28.5870, 77.2640), (28.5855, 77.2672), (28.5920, 77.2668), (28.5990, 77.2650), (28.6060, 77.2620), (28.6130, 77.2590), (28.6200, 77.2585), (28.6270, 77.2572), (28.6315, 77.2550)], periods=PRE_1850),
    dict(name="Sandbanks below Purana Qila", polygon=[(28.6180, 77.2484), (28.6100, 77.2492), (28.6040, 77.2520), (28.5990, 77.2540), (28.5960, 77.2558), (28.5975, 77.2535), (28.6030, 77.2500), (28.6090, 77.2475), (28.6170, 77.2468)], periods=PRE_1850),
    dict(name="Khadar north of the bend", polygon=[(28.6928, 77.2368), (28.6870, 77.2370), (28.6800, 77.2385), (28.6745, 77.2405), (28.6725, 77.2440), (28.6706, 77.2490), (28.6702, 77.2535), (28.6740, 77.2525), (28.6780, 77.2480), (28.6820, 77.2445), (28.6880, 77.2425), (28.6928, 77.2420)], periods=ZAFAR),
    dict(name="Shahdara khadar", polygon=[(28.6660, 77.2530), (28.6600, 77.2525), (28.6540, 77.2520), (28.6480, 77.2520), (28.6420, 77.2526), (28.6375, 77.2545), (28.6385, 77.2580), (28.6440, 77.2590), (28.6500, 77.2575), (28.6560, 77.2588), (28.6620, 77.2575), (28.6662, 77.2560)], periods=ZAFAR),
    dict(name="Patparganj khadar", polygon=[(28.6300, 77.2560), (28.6220, 77.2568), (28.6140, 77.2575), (28.6060, 77.2605), (28.6000, 77.2622), (28.5950, 77.2650), (28.5900, 77.2668), (28.5960, 77.2676), (28.6040, 77.2665), (28.6120, 77.2640), (28.6200, 77.2620), (28.6280, 77.2598)], periods=ZAFAR),
    dict(name="The bela below Kotla and Purana Qila", polygon=[(28.6340, 77.2505), (28.6250, 77.2525), (28.6150, 77.2537), (28.6060, 77.2560), (28.5990, 77.2585), (28.5940, 77.2615), (28.5930, 77.2590), (28.5980, 77.2560), (28.6050, 77.2530), (28.6140, 77.2500), (28.6240, 77.2492), (28.6330, 77.2480)], periods=ZAFAR),
]

DISTRICTS = [
    dict(id="firozabad", name="Firozabad", polygon=[(28.6560, 77.2250), (28.6560, 77.2440), (28.6320, 77.2440), (28.6320, 77.2320)], periods=SULTANATE,
         description="Firoz Shah's capital, founded 1354: not a walled town but a string of mohallas, eighteen villages and gardens round the Kotla, said by his chronicler Afif to stretch five kos along the river, with eight public mosques."),
    dict(id="din-panah", name="Din Panah and Shergarh", polygon=[(28.6385, 77.2395), (28.6385, 77.2440), (28.6060, 77.2470), (28.6060, 77.2400)], periods=DINPANAH,
         description="Humayun's 'refuge of the faith' (1533) on the old mound of Indarpat, refounded by Sher Shah as Shergarh with a citadel and a city wall reaching north to the Kabuli Darwaza."),
    dict(id="ghiyaspur", name="Ghiyaspur", polygon=[(28.5950, 77.2390), (28.5950, 77.2445), (28.5890, 77.2445), (28.5890, 77.2390)], periods=ALL,
         description="The village round the khanqah of Nizamuddin Auliya (d. 1325), where pilgrims, qawwals and the dead of every dynasty gather; now Nizamuddin Basti."),
    dict(id="daryaganj", name="Daryaganj", polygon=[(28.6515, 77.2415), (28.6515, 77.2440), (28.6402, 77.2446), (28.6402, 77.2415)], periods=MUGHAL_CITY,
         description="The riverside quarter east of Faiz Bazaar, of nobles' mansions on the water; from 1803 the first British cantonment, later a quarter of bungalows and old havelis."),
    dict(id="chandni-chowk", name="Chandni Chowk", polygon=[(28.6600, 77.2230), (28.6600, 77.2370), (28.6520, 77.2370), (28.6520, 77.2230)], periods=MUGHAL_CITY,
         description="The commercial heart of Shahjahanabad: the avenue, its katras and kuchas, the bankers' and jewellers' lanes of Dariba and Kinari Bazaar."),
    dict(id="civil-lines", name="Civil Lines", polygon=[(28.6900, 77.2220), (28.6900, 77.2320), (28.6720, 77.2340), (28.6720, 77.2260)], periods=ZAFAR,
         description="North of Kashmiri Gate along the river: the bungalows of British officials (Ludlow Castle, Metcalfe House) in large walled compounds, built after the troops moved out to the Ridge in 1828."),
    dict(id="paharganj", name="Paharganj", polygon=[(28.6510, 77.2090), (28.6510, 77.2175), (28.6425, 77.2180), (28.6425, 77.2090)], periods=MUGHAL_CITY,
         description="The 'hill market' outside Ajmeri Gate, the city's wholesale grain market under the Mughals."),
    dict(id="sabzi-mandi", name="Sabzi Mandi", polygon=[(28.6730, 77.2000), (28.6730, 77.2130), (28.6620, 77.2130), (28.6620, 77.2000)], periods=MUGHAL_CITY,
         description="The vegetable market and gardens outside the Kabuli and Lahori gates, in 1857 a no-man's-land of walled gardens fought over between the city and the Ridge."),
]

LABELS = [
    dict(text="Yamuna", position=(28.6300, 77.2505), size="lg", rotation=80, periods=PRE_1850),
    dict(text="Yamuna", position=(28.6300, 77.2545), size="lg", rotation=80, periods=ZAFAR),
    dict(text="Jamuna", position=(28.6800, 77.2352), size="md", rotation=75, periods=MUGHAL_CITY),
    dict(text="Firozabad", position=(28.6400, 77.2365), size="lg", periods=SULTANATE),
    dict(text="Shergarh", position=(28.6215, 77.2440), size="lg", periods=DINPANAH),
    dict(text="Shahjahanabad", position=(28.6470, 77.2290), size="lg", periods=MUGHAL_CITY),
    dict(text="The Ridge", position=(28.6800, 77.2115), size="md", rotation=-55, periods=ALL),
    dict(text="Ghiyaspur", position=(28.5960, 77.2405), size="sm", periods=ALL),
    dict(text="Indarpat", position=(28.6040, 77.2440), size="sm", periods=SULTANATE),
    dict(text="Daryaganj", position=(28.6470, 77.2428), size="sm", rotation=-85, periods=MUGHAL_CITY),
    dict(text="Paharganj", position=(28.6470, 77.2125), size="sm", periods=MUGHAL_CITY),
    dict(text="Sabzi Mandi", position=(28.6690, 77.2030), size="sm", periods=MUGHAL_CITY),
    dict(text="Civil Lines", position=(28.6820, 77.2275), size="sm", periods=ZAFAR),
    dict(text="Cantonment", position=(28.6905, 77.2050), size="sm", periods=ZAFAR),
    dict(text="Shahdara", position=(28.6700, 77.2620), size="sm", periods=ALL),
    dict(text="Raisina", position=(28.6150, 77.2070), size="sm", periods=ALL),
    dict(text="Ruins of Firozabad", position=(28.6355, 77.2365), size="sm", periods=["humayun-1570", "shahjahan-1660", "zafar-1850"]),
    dict(text="Ruins of Shergarh", position=(28.6220, 77.2443), size="sm", periods=MUGHAL_CITY),
    dict(text="Jaisinghpura", position=(28.6265, 77.2085), size="sm", periods=MUGHAL_CITY),
    dict(text="Mughalpura", position=(28.6572, 77.2138), size="sm", periods=["shahjahan-1660"]),
    dict(text="Kishanganj", position=(28.6572, 77.2138), size="sm", periods=ZAFAR),
    dict(text="Chandrawal", position=(28.6922, 77.2300), size="sm", periods=ALL),
    dict(text="Sarai Kale Khan", position=(28.5862, 77.2546), size="sm", periods=FROM_SURID),
    dict(text="Arab Sarai", position=(28.5872, 77.2477), size="sm", periods=FROM_HUMAYUN),
    dict(text="Tis Hazari", position=(28.6705, 77.2188), size="sm", periods=MUGHAL_CITY),
    dict(text="Ballimaran", position=(28.6538, 77.2280), size="sm", periods=MUGHAL_CITY),
    dict(text="Matia Mahal", position=(28.6455, 77.2365), size="sm", periods=MUGHAL_CITY),
    dict(text="Katra Neel", position=(28.6612, 77.2235), size="sm", periods=MUGHAL_CITY),
    dict(text="Sita Ram Bazaar", position=(28.6460, 77.2285), size="sm", periods=MUGHAL_CITY),
    dict(text="Gardens and tombs", position=(28.6160, 77.2345), size="sm", periods=["humayun-1570", "shahjahan-1660", "zafar-1850"]),
    dict(text="Orchards and wells", position=(28.6070, 77.2150), size="sm", periods=ALL),
    dict(text="Khadar", position=(28.6470, 77.2545), size="sm", periods=ALL),
    dict(text="Bela", position=(28.6560, 77.2468), size="sm", periods=ZAFAR),
    dict(text="Kushk-i-Shikar", position=(28.6715, 77.2120), size="sm", periods=SULTANATE),
    dict(text="Old Firozabad", position=(28.6430, 77.2385), size="sm", periods=DINPANAH),
]

SOURCES = [
    dict(id="blake", title="Shahjahanabad: The Sovereign City in Mughal India, 1639–1739", author="Stephen P. Blake", year=1991),
    dict(id="gupta", title="Delhi Between Two Empires, 1803–1931", author="Narayani Gupta", year=1981),
    dict(id="peck", title="Delhi: A Thousand Years of Building", author="Lucy Peck", year=2005),
    dict(id="sharma", title="Delhi and its Neighbourhood", author="Y. D. Sharma (Archaeological Survey of India)", year=1974),
    dict(id="carr-stephen", title="The Archaeology and Monumental Remains of Delhi", author="Carr Stephen", year=1876, url="https://archive.org/details/archaeologyandm00stepgoog"),
    dict(id="sayyid-ahmad", title="Asar-us-Sanadid (Monuments of Delhi)", author="Sayyid Ahmad Khan", year=1847),
    dict(id="liddle", title="Chandni Chowk: The Mughal City of Old Delhi", author="Swapna Liddle", year=2017),
    dict(id="dalrymple", title="The Last Mughal: The Fall of a Dynasty, Delhi 1857", author="William Dalrymple", year=2006),
    dict(id="welch-crane", title="The Tughluqs: Master Builders of the Delhi Sultanate", author="Anthony Welch & Howard Crane", year=1983, note="Muqarnas 1"),
    dict(id="wiki-shahjahanabad", title="Shahjahanabad", author="Wikipedia", url="https://en.wikipedia.org/wiki/Shahjahanabad"),
    dict(id="wiki-yamuna", title="Yamuna", author="Wikipedia", url="https://en.wikipedia.org/wiki/Yamuna"),
    dict(id="wiki-delhi-ridge", title="Delhi Ridge", author="Wikipedia", url="https://en.wikipedia.org/wiki/Delhi_Ridge"),
]
