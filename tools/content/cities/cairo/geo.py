# Cairo: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
ALL = ["fustat-700", "tulunid-880", "fatimid-1050", "mamluk-1350", "ottoman-1600"]
EARLY = ["fustat-700", "tulunid-880"]
FATIMID_ON = ["fatimid-1050", "mamluk-1350", "ottoman-1600"]
LATER = ["mamluk-1350", "ottoman-1600"]
TO_FATIMID = ["fustat-700", "tulunid-880", "fatimid-1050"]


def west(pts, dlon):
    """The centre line of a river drawn as a wide stroke whose east edge is the bank line pts."""
    return [(lat, round(lon - dlon, 5)) for lat, lon in pts]


SOURCES = [
    dict(id="raymond-cairo", title="Cairo", author="André Raymond", year=2000, note="trans. Willard Wood; Harvard University Press"),
    dict(id="abu-lughod", title="Cairo: 1001 Years of the City Victorious", author="Janet L. Abu-Lughod", year=1971),
    dict(id="behrens-abouseif", title="Islamic Architecture in Cairo: An Introduction", author="Doris Behrens-Abouseif", year=1989),
    dict(id="maqrizi-khitat", title="al-Mawa'iz wa'l-I'tibar fi Dhikr al-Khitat wa'l-Athar (the Khitat)", author="al-Maqrizi", year="c. 1420s", url="https://en.wikipedia.org/wiki/Al-Maqrizi"),
    dict(id="nasir-khusraw", title="Safarnama (Book of Travels)", author="Nasir-i Khusraw", year="1047–1050 (written c. 1052)", url="https://en.wikipedia.org/wiki/Safarnama"),
    dict(id="kubiak-fustat", title="Al-Fustat: Its Foundation and Early Urban Development", author="Władysław B. Kubiak", year=1987),
    dict(id="lane-egyptians", title="An Account of the Manners and Customs of the Modern Egyptians", author="Edward William Lane", year=1836, url="https://en.wikipedia.org/wiki/Edward_William_Lane"),
    dict(id="wiki-history-cairo", title="Cairo", author="Wikipedia", url="https://en.wikipedia.org/wiki/Cairo"),
    dict(id="wiki-fustat", title="Fustat", author="Wikipedia", url="https://en.wikipedia.org/wiki/Fustat"),
    dict(id="wiki-al-qatai", title="Al-Qata'i", author="Wikipedia", url="https://en.wikipedia.org/wiki/Al-Qata%27i"),
    dict(id="wiki-al-askar", title="Al-Askar", author="Wikipedia", url="https://en.wikipedia.org/wiki/Al-Askar"),
    dict(id="wiki-khalij", title="Canal of Cairo (Khalij)", author="Wikipedia", url="https://en.wikipedia.org/wiki/Khalij_(Cairo)"),
    dict(id="wiki-roda", title="Roda Island", author="Wikipedia", url="https://en.wikipedia.org/wiki/Roda_Island"),
    dict(id="wiki-mokattam", title="Mokattam", author="Wikipedia", url="https://en.wikipedia.org/wiki/Mokattam"),
    dict(id="wiki-walls-of-cairo", title="Walls of Cairo", author="Wikipedia", url="https://en.wikipedia.org/wiki/Fortifications_of_Cairo"),
    dict(id="wiki-bulaq", title="Bulaq", author="Wikipedia", url="https://en.wikipedia.org/wiki/Boulaq"),
    dict(id="wiki-azbakiyya", title="Ezbekiyya", author="Wikipedia", url="https://en.wikipedia.org/wiki/Azbakeya"),
    dict(id="wiki-city-of-the-dead", title="City of the Dead (Cairo)", author="Wikipedia", url="https://en.wikipedia.org/wiki/City_of_the_Dead_(Cairo)"),
]

CITY = dict(
    name="Cairo", subtitle="Misr, Mother of the World",
    description="Twelve centuries of Cairo between the Nile and the Muqattam hills: from the Arab garrison town of Fustat beside the Roman fortress of Babylon, through Ibn Tulun's al-Qata'i and the Fatimid palace city of al-Qahira, to the Mamluk Citadel and Ottoman Bulaq. The river's east bank moved west over these centuries and is drawn per era. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="fatimid-1050",
    world=dict(heightScale=1.15, walls=["#E2D2B2", "#D8C49E", "#EAE0CA", "#CFB78F", "#C9AE84"], roofs=["#CDB993", "#BFA67E"]),
    camera=dict(target=(30.0380, 31.2520), distance=42),
)

# north-west corner, south-east corner: Bulaq and Bab al-Futuh to Babylon, Giza bank to the Muqattam
FRAME = ((30.0655, 31.2040), (30.0000, 31.2800))

PALETTE = dict(parchment="#E9D7AE", ink="#6B4A30", water="#5F8A88", hill="#9A8A62", road="#8C6A48")
COMPASS = (30.0615, 31.2770)
CARTOUCHE = (30.0030, 31.2060)

PERIODS = [
    dict(id="fustat-700", label="Umayyad Fustat", year=700, startYear=641, endYear=867,
         summary="The Arab army's camp-town of Fustat, laid out in 641–642 by Amr ibn al-As in tribal plots (khitat) round his mosque, beside the Roman fortress of Babylon with its Coptic churches. A garrison and tax capital of mud brick, palm timber and reused stone on the Nile bank; Roda Island has a shipyard and a nilometer, and Amr's re-dug canal carries grain to Arabia.",
         population="perhaps 30,000–40,000",
         feel="Arabic and Coptic in the same lane, camels at the river landing, palm-trunk columns in a crowded mosque, and church bells from inside the Roman walls.",
         style="courtyard",
         houses=dict(title="Tribal plots of Fustat", text="Each Arab clan settled its own khitta: walled compounds of mud brick and palm beams round yards, a mosque and a cemetery of its own, lanes left between plots. By 700 the plots had filled with two-storey houses of brick on stone footings."),
         outskirts=dict(title="Palm groves and monasteries", text="Beyond the plots, palm groves, threshing floors and Coptic monasteries ran out toward the desert edge and the tombs of the Qarafa under the Muqattam.")),
    dict(id="tulunid-880", label="Ibn Tulun's al-Qata'i", year=880, startYear=868, endYear=968,
         summary="Ahmad ibn Tulun, Turkish governor turned independent ruler, builds a new royal quarter, al-Qata'i ('the wards'), north-east of Fustat and al-Askar: a palace and polo ground under the Muqattam, a hospital, an aqueduct, and the vast brick mosque on Jabal Yashkur. Fustat keeps the trade, the river and the crowds. The Abbasids raze al-Qata'i in 905, sparing only the mosque.",
         population="perhaps 100,000 in the three towns",
         feel="Drums from the palace maydan, polo ponies on the dust, bricklayers on scaffolds round the great mosque, Fustat's markets roaring by the river.",
         style="courtyard",
         houses=dict(title="Brick houses of Fustat and al-Askar", text="Courtyard houses of fired and mud brick, two and three storeys, with wind-catchers on the roofs; in Fustat the first tall tenements crowd the lanes near the river. Excavated houses had water channels, latrines and painted plaster."),
         outskirts=dict(title="Wards of the soldiers", text="Al-Qata'i was laid out in wards for each regiment and group of servants: Sudanese, Greeks, Turks. Loose blocks of barracks, stables and gardens round the palace and its maydan.")),
    dict(id="fatimid-1050", label="Fatimid Cairo", year=1050, startYear=969, endYear=1170,
         summary="Two cities: al-Qahira, the walled palace city founded by the Fatimid caliphs in 969, with its two great palaces, Al-Azhar and the processional street Bayn al-Qasrayn; and Fustat (Misr), the commercial city on the Nile at its richest, as Nasir-i Khusraw saw it in 1047. Brick and timber, stone for mosques and gates, gardens along the canal; Fustat burned in 1168.",
         population="perhaps 200,000–300,000",
         feel="Lamps hung by the thousand in the Mosque of Amr, porters with Nile water, caliphal processions with gold parasols, glass and lustre pottery in the market.",
         style="courtyard",
         houses=dict(title="Tall houses of Misr", text="Nasir-i Khusraw thought Fustat's houses looked like mountains: brick tenements of five, seven, by his count even fourteen storeys, with roof gardens. In al-Qahira, courtyard houses of officials and soldiers filled the quarters named after the caliph's regiments."),
         outskirts=dict(title="Gardens on the canal", text="Between the two cities and along the Khalij lay pleasure gardens, orchards, belvederes and the ruins of al-Qata'i; at al-Maqs, al-Qahira's river port, shipyards and warehouses.")),
    dict(id="mamluk-1350", label="Mamluk Cairo", year=1350, startYear=1171, endYear=1516,
         summary="Saladin's Citadel (begun 1176) on its Muqattam spur is the seat of the Mamluk sultans, slave-soldiers who rule Egypt and Syria. Al-Qahira, now the whole city's heart, is packed with stone madrasas, mausoleums and hospitals of the sultans and amirs; the city spreads to the Citadel and across the canal. The Black Death of 1348 has just killed perhaps a third of its people.",
         population="perhaps 400,000 before the plague of 1348, far fewer after",
         feel="Striped stone facades and carved domes, the call to prayer from a hundred minarets, Qur'an reciters at the tombs, funeral biers in the streets of 1348.",
         style="courtyard",
         houses=dict(title="Rab' and qa'a", text="Ordinary Cairenes rented rooms in the rab', a stone-and-brick tenement of three or four storeys over shops, with duplex flats round a stair. The rich lived in courtyard houses with a lofty qa'a hall, wind-catchers and turned-wood mashrabiya screens."),
         outskirts=dict(title="Ruins and new suburbs", text="Old Fustat shrank to a river town among rubbish mounds; new suburbs grew at Husayniyya, round the Birkat al-Fil pond with amirs' palaces, and on the new land at Bulaq.")),
    dict(id="ottoman-1600", label="Ottoman Cairo", year=1600, startYear=1517, endYear=1798,
         summary="After Selim I's conquest in 1517 Cairo is a provincial capital of the Ottoman empire, ruled by a pasha in the Citadel and the old Mamluk households. Still the biggest city of the Arab world: Bulaq is the Nile port, caravans and coffee from Yemen fill hundreds of wikalas, and coffee houses are new. Ottoman pencil minarets rise among Mamluk domes.",
         population="perhaps 250,000–300,000",
         feel="Coffee roasting in the Khan, Yemeni bales on Bulaq's quays, janissaries at the Citadel gate, mashrabiyas over every lane.",
         style="courtyard",
         houses=dict(title="Mashrabiya houses", text="Two- and three-storey houses of stone ground floors and brick or timber upper storeys, the upper floors corbelled out over the lane behind turned-wood mashrabiya screens; a court, a malqaf wind-catcher and a qa'a inside. Tenements (rab') over shops in the markets."),
         outskirts=dict(title="Ponds and gardens", text="Round the seasonal ponds of Azbakiyya and al-Fil, houses of the beys and gardens flooded each summer; at Bulaq warehouses and boatyards; south, old Fustat's potters among the mounds.")),
]

# ---------------------------------------------------------------- the Nile, whose east bank moved west over the centuries
BANK_EARLY = [(29.9970, 31.2290), (30.0060, 31.2292), (30.0082, 31.2294), (30.0100, 31.2299), (30.0160, 31.2324), (30.0220, 31.2344), (30.0280, 31.2362), (30.0340, 31.2385),
              (30.0400, 31.2406), (30.0460, 31.2426), (30.0520, 31.2446), (30.0580, 31.2466), (30.0690, 31.2496)]
BANK_FATIMID = [(29.9970, 31.2290), (30.0060, 31.2292), (30.0082, 31.2294), (30.0100, 31.2299), (30.0160, 31.2324), (30.0220, 31.2340), (30.0280, 31.2352), (30.0340, 31.2370),
                (30.0400, 31.2388), (30.0460, 31.2406), (30.0520, 31.2424), (30.0580, 31.2443), (30.0690, 31.2470)]
BANK_MAMLUK = [(29.9970, 31.2290), (30.0060, 31.2293), (30.0100, 31.2300), (30.0160, 31.2308), (30.0220, 31.2314), (30.0272, 31.2318), (30.0340, 31.2326),
               (30.0400, 31.2334), (30.0460, 31.2340), (30.0520, 31.2336), (30.0580, 31.2322), (30.0690, 31.2308)]
BANK_OTTOMAN = [(29.9970, 31.2288), (30.0060, 31.2290), (30.0100, 31.2295), (30.0160, 31.2302), (30.0220, 31.2310), (30.0272, 31.2315), (30.0340, 31.2318),
                (30.0400, 31.2320), (30.0460, 31.2316), (30.0520, 31.2302), (30.0580, 31.2292), (30.0690, 31.2276)]

KHALIJ_COURSE = [(30.0300, 31.2395), (30.0335, 31.2428), (30.0370, 31.2460), (30.0410, 31.2494), (30.0444, 31.2526), (30.0490, 31.2546), (30.0530, 31.2560),
                 (30.0566, 31.2578), (30.0605, 31.2618), (30.0640, 31.2688), (30.0680, 31.2750)]

NILE_BLURB = "The Nile rose every summer from July to September; Cairo's year turned on the flood. Its east bank has moved about a kilometre west since 641: Fustat and the Roman fortress once stood on the water's edge, and Bulaq is land the river left behind in the 14th century."

WATER = [
    dict(id="nile", name="The Nile (al-Nil)", path=west(BANK_EARLY, 0.0083), width=1600, blurb=NILE_BLURB, periods=EARLY),
    dict(id="nile", name="The Nile (al-Nil)", path=west(BANK_FATIMID, 0.0078), width=1500, blurb=NILE_BLURB, periods=["fatimid-1050"]),
    dict(id="nile", name="The Nile (al-Nil)", path=west(BANK_MAMLUK, 0.00675), width=1300, blurb=NILE_BLURB, periods=["mamluk-1350"]),
    dict(id="nile", name="The Nile (al-Nil)", path=west(BANK_OTTOMAN, 0.00623), width=1200, blurb=NILE_BLURB, periods=["ottoman-1600"]),
    dict(id="nile-west", name="Western arm of the Nile", path=[(30.0430, 31.2212), (30.0500, 31.2172), (30.0580, 31.2138), (30.0690, 31.2100)], width=240,
         blurb="The channel west of the new island of Bulaq (later Gezira), which the river built up from the 14th century.", periods=["ottoman-1600"]),
    dict(id="khalij", name="al-Khalij (the Canal of Cairo)", path=[(30.0250, 31.2343)] + KHALIJ_COURSE, width=24,
         blurb="Khalij Amir al-Mu'minin: an ancient canal to the Red Sea that Amr ibn al-As re-dug in 641–642 to ship Egyptian grain to Medina. Silted beyond Cairo after the 8th century, it still filled each summer when its dam was cut at the Nile's flood, and ran past al-Qahira's west wall.",
         periods=TO_FATIMID),
    dict(id="khalij", name="al-Khalij (the Canal of Cairo)", path=[(30.0284, 31.2316), (30.0292, 31.2360)] + KHALIJ_COURSE, width=24,
         blurb="The Khalij, now fed from a mouth at Fumm al-Khalig beside the aqueduct's intake. Cut open each August at the Wafa al-Nil festival, it watered the ponds and gardens of the city and stank when it dried. Filled in 1897; Port Said Street follows it.",
         periods=LATER),
    dict(id="birkat-al-fil", name="Birkat al-Fil (Elephant Pond)", path=[(30.0374, 31.2484), (30.0386, 31.2522)], width=300,
         blurb="A pond filled by the Khalij at the flood and dry and green by spring. Mamluk amirs built palaces round it; boats with lanterns crossed it on flood nights.",
         periods=FATIMID_ON),
    dict(id="birkat-al-azbakiyya", name="Birkat al-Azbakiyya", path=[(30.0524, 31.2474), (30.0542, 31.2498)], width=280,
         blurb="A pond made by the amir Azbak from 1476 round his mosque, ringed by the houses of the Ottoman beys; a lake at flood time, a garden in spring.",
         periods=["ottoman-1600"]),
]

ISLANDS = [
    dict(name="Jazirat al-Rawda (Roda Island)", polygon=[(30.0050, 31.2251), (30.0068, 31.2266), (30.0100, 31.2276), (30.0150, 31.2286), (30.0200, 31.2294), (30.0250, 31.2301),
                                                       (30.0300, 31.2305), (30.0340, 31.2300), (30.0366, 31.2288), (30.0380, 31.2270), (30.0362, 31.2246), (30.0310, 31.2231),
                                                       (30.0250, 31.2226), (30.0190, 31.2227), (30.0130, 31.2232), (30.0085, 31.2238), (30.0060, 31.2243)]),
    dict(name="Jazirat Bulaq (Gezira)", polygon=[(30.0425, 31.2252), (30.0470, 31.2262), (30.0530, 31.2256), (30.0600, 31.2240), (30.0670, 31.2220), (30.0670, 31.2150),
                                                   (30.0590, 31.2168), (30.0520, 31.2193), (30.0460, 31.2224)], periods=["ottoman-1600"]),
]

HILLS = [
    dict(id="muqattam", name="Jabal al-Muqattam", center=(30.0150, 31.2745), radius=900,
         blurb="The limestone ridge east of the city, quarried for building stone since the pharaohs. Copts tell of the Muqattam moved by prayer in the 10th century; Muslims of the tombs of saints and the Qarafa cemetery at its foot."),
    dict(id="muqattam-north", name="al-Muqattam (northern spur)", center=(30.0330, 31.2765), radius=650, label=False,
         blurb="The ridge continuing north-east behind the Citadel, its cliffs honeycombed with quarries and hermits' caves."),
    dict(id="citadel-spur", name="The Citadel spur (Qubbat al-Hawa)", center=(30.0293, 31.2622), radius=330,
         blurb="A spur of the Muqattam overlooking the city, where an Abbasid governor built a breezy pavilion, the Qubbat al-Hawa ('Dome of the Wind'), in the 9th century, and Saladin began his Citadel in 1176."),
    dict(id="yashkur", name="Jabal Yashkur", center=(30.0288, 31.2495), radius=150, label=False,
         blurb="The low rock on which Ibn Tulun set his mosque, named after an Arab clan; legend placed Noah's ark here after the Flood."),
]

ROADS = [
    dict(id="babylon-road", name="Road to Babylon and the south", path=[(30.0090, 31.2356), (30.0060, 31.2334), (30.0020, 31.2336), (29.9985, 31.2342)], width=12, style="major",
         blurb="The old road along the river past the Roman fortress to Upper Egypt and the Birkat al-Habash."),
    dict(id="fustat-north", name="Road north to Ayn Shams", path=[(30.0118, 31.2384), (30.0160, 31.2402), (30.0230, 31.2425), (30.0300, 31.2448), (30.0370, 31.2480), (30.0450, 31.2510), (30.0560, 31.2560), (30.0660, 31.2600)],
         width=12, style="major", labelled=True, blurb="The way from Fustat north across the desert edge to Heliopolis (Ayn Shams) and the Delta.", periods=["fustat-700"]),
    dict(id="great-street", name="The Great Street (al-Shari' al-A'zam)", path=[(30.0118, 31.2384), (30.0160, 31.2402), (30.0230, 31.2425), (30.0310, 31.2450), (30.0330, 31.2480), (30.0345, 31.2520), (30.0385, 31.2550), (30.0424, 31.2571)],
         width=14, style="major", labelled=True,
         blurb="The main road between Fustat and the northern towns: through al-Askar and al-Qata'i, and from 969 on to Bab Zuwayla. South of the gate in Mamluk times it was the Qasaba's continuation, lined with markets.",
         periods=["tulunid-880"] + FATIMID_ON),
    dict(id="saliba-tulunid", name="Avenue of al-Qata'i", path=[(30.0335, 31.2428), (30.0316, 31.2470), (30.0306, 31.2512), (30.0303, 31.2536)], width=16, style="major", labelled=True,
         blurb="Ibn Tulun's avenue from al-Askar past his mosque to the palace gate and the maydan below the Muqattam. Shari' al-Saliba later follows much the same line.", periods=["tulunid-880"]),
    dict(id="saliba", name="Shari' al-Saliba", path=[(30.0335, 31.2428), (30.0316, 31.2470), (30.0306, 31.2512), (30.0302, 31.2545), (30.0298, 31.2574)], width=12, style="major", labelled=True,
         blurb="The street of the Cross (saliba): from the Khalij past the Mosque of Ibn Tulun to the Rumayla square below the Citadel, lined with the domes and sabils of Mamluk amirs.", periods=LATER),
    dict(id="qasaba", name="al-Qasaba (Bayn al-Qasrayn)", path=[(30.0545, 31.2629), (30.0532, 31.2622), (30.0520, 31.2615), (30.0505, 31.2611), (30.0490, 31.2609), (30.0475, 31.2605), (30.0461, 31.2597), (30.0448, 31.2590), (30.0437, 31.2578)],
         width=10, style="major", labelled=True,
         blurb="The spine of al-Qahira from Bab al-Futuh to Bab Zuwayla. Between the two Fatimid palaces it widened into Bayn al-Qasrayn, 'between the two palaces', a parade ground said to hold ten thousand soldiers; under the Mamluks the city's grandest street of madrasas and tombs.",
         periods=FATIMID_ON),
    dict(id="futuh-road", name="Road from Bab al-Futuh", path=[(30.0555, 31.2631), (30.0600, 31.2640), (30.0670, 31.2652)], width=10, style="minor", periods=FATIMID_ON,
         blurb="Out of the 'Gate of Conquests' toward the Delta and Syria, past cemeteries and, later, the suburb of Husayniyya."),
    dict(id="nasr-road", name="Road from Bab al-Nasr", path=[(30.0558, 31.2650), (30.0600, 31.2682), (30.0670, 31.2735)], width=10, style="minor", periods=FATIMID_ON,
         blurb="Out of the 'Gate of Victory' along which armies and the pilgrim caravan left for Syria and Mecca."),
    dict(id="qantara-street", name="Street of Bab al-Qantara", path=[(30.0521, 31.2614), (30.0526, 31.2590), (30.0528, 31.2578), (30.0540, 31.2530), (30.0563, 31.2482), (30.0590, 31.2455)],
         width=10, style="minor", periods=FATIMID_ON, blurb="West from the Qasaba through the 'Gate of the Bridge' over the Khalij to al-Maqs, al-Qahira's port on the Nile."),
    dict(id="bulaq-road", name="Road to Bulaq", path=[(30.0563, 31.2482), (30.0576, 31.2410), (30.0584, 31.2335)], width=10, style="major", periods=LATER,
         blurb="Across the new land left by the river to the port of Bulaq, busy with camels and donkeys carrying grain and goods from the boats."),
    dict(id="darb-al-ahmar", name="Darb al-Ahmar", path=[(30.0424, 31.2580), (30.0400, 31.2590), (30.0370, 31.2598), (30.0340, 31.2604), (30.0326, 31.2600)], width=9, style="major", labelled=True,
         blurb="The 'Red Road' from Bab Zuwayla to the Citadel, built up by Mamluk amirs with mosques, palaces and markets once the sultans moved to the Citadel.", periods=LATER),
    dict(id="qarafa-road", name="Road to the Qarafa", path=[(30.0130, 31.2398), (30.0150, 31.2470), (30.0170, 31.2550), (30.0200, 31.2620)], width=8, style="minor",
         blurb="Out to the great cemetery of the Qarafa and the Muqattam: Fustat's people walked it on Fridays and feast days to visit their dead and the saints' tombs."),
    dict(id="river-street", name="Street to the river landing", path=[(30.0132, 31.2398), (30.0126, 31.2360), (30.0124, 31.2328)], width=8, style="minor", periods=TO_FATIMID,
         blurb="From the markets north of the Mosque of Amr down to the Nile landing and the bridge of boats to Roda."),
    dict(id="fumm-road", name="Road along the aqueduct", path=[(30.0280, 31.2336), (30.0272, 31.2400), (30.0262, 31.2470)], width=8, style="minor", periods=LATER,
         blurb="From the canal mouth and Old Cairo's river landings to the Citadel, along the arches of the aqueduct."),
]

WALLS = [
    dict(id="qahira-walls", name="Walls of al-Qahira",
         path=[(30.0556, 31.2590), (30.0549, 31.2631), (30.0552, 31.2648), (30.0540, 31.2695), (30.0500, 31.2690), (30.0460, 31.2675), (30.0428, 31.2655), (30.0428, 31.2610),
               (30.0430, 31.2573), (30.0440, 31.2545), (30.0500, 31.2565)],
         closed=True, periods=FATIMID_ON,
         blurb="Jawhar's walls of 969 were mud brick; in 1087–1092 the vizier Badr al-Jamali rebuilt them a little wider in stone with the gates of Zuwayla, al-Futuh and al-Nasr. Saladin extended them toward the Citadel and Fustat."),
    dict(id="ayyubid-wall", name="Saladin's wall", path=[(30.0428, 31.2655), (30.0390, 31.2650), (30.0350, 31.2640), (30.0322, 31.2628)], periods=LATER,
         blurb="Part of the circuit Saladin began in 1176 to join al-Qahira, the Citadel and Fustat in one enclosure. Never finished; this eastern stretch, later buried under rubbish mounds, has been excavated in al-Azhar Park."),
]

GATES = [
    dict(id="bab-al-qantara", name="Bab al-Qantara", position=(30.0528, 31.2578), periods=FATIMID_ON),
    dict(id="bab-al-barqiyya", name="Bab al-Barqiyya", position=(30.0490, 31.2687), periods=FATIMID_ON),
    dict(id="bab-al-shariyya", name="Bab al-Sha'riyya", position=(30.0555, 31.2594), periods=LATER),
    dict(id="bab-al-mahruq", name="Bab al-Mahruq", position=(30.0447, 31.2668), periods=LATER),
    dict(id="bab-al-khalq", name="Bab al-Khalq", position=(30.0441, 31.2547), periods=LATER),
    dict(id="bab-al-wazir", name="Bab al-Wazir", position=(30.0348, 31.2638), periods=LATER),
]

BRIDGES = [
    dict(id="roda-bridge", name="Bridge of boats to Roda", path=[(30.0098, 31.2312), (30.0098, 31.2268)], build="timber", arches=6, periods=TO_FATIMID,
         blurb="A bridge of moored boats joined Fustat to Roda Island, and a second one Roda to Giza: the crossing of the Nile for armies, pilgrims and caravans to the west. Later the crossing was made by ferry."),
    dict(id="giza-bridge", name="Bridge of boats to Giza", path=[(30.0150, 31.2230), (30.0150, 31.2150)], build="timber", arches=8, periods=TO_FATIMID,
         blurb="The second half of the boat-bridge, from Roda to Giza on the west bank, taken up when the flood ran high."),
    dict(id="qanatir-al-siba", name="Qanatir al-Siba'", path=[(30.0339, 31.2423), (30.0330, 31.2434)], build="stone", arches=2, periods=LATER,
         blurb="The 'Bridge of the Lions', built over the Khalij by Sultan Baybars, whose emblem was a lion, near the shrine of Sayyida Zaynab."),
]

AQUEDUCTS = [
    dict(name="Aqueduct of the Citadel", path=[(30.0272, 31.2336), (30.0262, 31.2400), (30.0250, 31.2470), (30.0246, 31.2520), (30.0256, 31.2562), (30.0270, 31.2590)], periods=LATER),
]

BLOCKS = [
    # ---- Fustat, 641-700: tribal plots round the mosque and the fortress
    dict(name="Ahl al-Raya", polygon=[(30.0088, 31.2322), (30.0150, 31.2336), (30.0150, 31.2398), (30.0088, 31.2398)], density="dense", periods=["fustat-700"]),
    dict(name="Tujib and Lakhm", polygon=[(30.0052, 31.2322), (30.0086, 31.2322), (30.0086, 31.2400), (30.0052, 31.2400)], density="dense", periods=["fustat-700"]),
    dict(name="Rashida and Banu Wa'il", polygon=[(30.0000, 31.2298), (30.0049, 31.2300), (30.0049, 31.2385), (30.0000, 31.2385)], density="dense", periods=["fustat-700"]),
    dict(name="al-Hamra", polygon=[(30.0152, 31.2340), (30.0215, 31.2356), (30.0215, 31.2420), (30.0152, 31.2420)], density="loose", periods=["fustat-700"]),
    dict(name="Eastern khitat", polygon=[(30.0000, 31.2392), (30.0150, 31.2405), (30.0150, 31.2465), (30.0000, 31.2460)], density="loose", periods=["fustat-700"]),
    # ---- Fustat grown, 880 and 1050
    dict(name="Ahl al-Raya", polygon=[(30.0086, 31.2318), (30.0152, 31.2334), (30.0152, 31.2400), (30.0086, 31.2400)], density="dense", periods=["tulunid-880", "fatimid-1050"]),
    dict(name="Tujib and Lakhm", polygon=[(30.0052, 31.2320), (30.0084, 31.2320), (30.0084, 31.2400), (30.0052, 31.2400)], density="dense", periods=["tulunid-880", "fatimid-1050"]),
    dict(name="Rashida and Banu Wa'il", polygon=[(30.0000, 31.2298), (30.0049, 31.2300), (30.0049, 31.2400), (30.0000, 31.2400)], density="dense", periods=["tulunid-880", "fatimid-1050"]),
    dict(name="al-Hamra", polygon=[(30.0154, 31.2334), (30.0220, 31.2350), (30.0220, 31.2420), (30.0154, 31.2405)], density="dense", periods=["tulunid-880", "fatimid-1050"]),
    dict(name="Suq Wardan and the eastern lanes", polygon=[(30.0000, 31.2405), (30.0125, 31.2405), (30.0140, 31.2460), (30.0000, 31.2470)], density="dense", periods=["tulunid-880", "fatimid-1050"]),
    dict(name="al-Askar", polygon=[(30.0222, 31.2352), (30.0282, 31.2368), (30.0300, 31.2440), (30.0234, 31.2422)], density="dense", periods=["tulunid-880", "fatimid-1050"]),
    dict(name="Upper Fustat", polygon=[(30.0160, 31.2412), (30.0228, 31.2432), (30.0228, 31.2480), (30.0160, 31.2470)], density="dense", periods=["fatimid-1050"]),
    dict(name="Upper Fustat", polygon=[(30.0160, 31.2412), (30.0228, 31.2432), (30.0228, 31.2480), (30.0160, 31.2470)], density="loose", periods=["tulunid-880"]),
    dict(name="Toward the Qarafa", polygon=[(30.0000, 31.2478), (30.0140, 31.2470), (30.0160, 31.2520), (30.0000, 31.2530)], density="loose", periods=["tulunid-880", "fatimid-1050"]),
    # ---- al-Qata'i (870-905)
    dict(name="Wards of al-Qata'i", polygon=[(30.0302, 31.2444), (30.0360, 31.2468), (30.0360, 31.2530), (30.0312, 31.2532)], density="dense", periods=["tulunid-880"]),
    dict(name="Southern wards", polygon=[(30.0232, 31.2486), (30.0274, 31.2486), (30.0274, 31.2560), (30.0232, 31.2560)], density="loose", periods=["tulunid-880"]),
    dict(name="Northern wards", polygon=[(30.0366, 31.2482), (30.0420, 31.2505), (30.0420, 31.2548), (30.0366, 31.2540)], density="loose", periods=["tulunid-880"]),
    dict(name="Ruins of al-Qata'i", polygon=[(30.0302, 31.2444), (30.0360, 31.2468), (30.0350, 31.2540), (30.0312, 31.2560)], density="loose", periods=["fatimid-1050"]),
    # ---- al-Qahira, 1050
    dict(name="Harat Zuwayla", polygon=[(30.0442, 31.2551), (30.0488, 31.2567), (30.0490, 31.2596), (30.0450, 31.2588), (30.0438, 31.2580)], density="dense", periods=["fatimid-1050"]),
    dict(name="al-Batiliyya", polygon=[(30.0432, 31.2596), (30.0470, 31.2603), (30.0472, 31.2650), (30.0434, 31.2652)], density="dense", periods=["fatimid-1050"]),
    dict(name="al-Barqiyya", polygon=[(30.0470, 31.2652), (30.0512, 31.2652), (30.0512, 31.2685), (30.0466, 31.2670)], density="dense", periods=["fatimid-1050"]),
    dict(name="Harat Baha' al-Din", polygon=[(30.0522, 31.2585), (30.0553, 31.2594), (30.0546, 31.2612), (30.0522, 31.2610)], density="dense", periods=["fatimid-1050"]),
    dict(name="al-Utufiyya", polygon=[(30.0512, 31.2626), (30.0533, 31.2628), (30.0538, 31.2688), (30.0512, 31.2688)], density="dense", periods=["fatimid-1050"]),
    dict(name="al-Maqs", polygon=[(30.0560, 31.2452), (30.0625, 31.2465), (30.0625, 31.2530), (30.0560, 31.2528)], density="loose", periods=["fatimid-1050"]),
    dict(name="Gardens between the cities", polygon=[(30.0400, 31.2512), (30.0436, 31.2528), (30.0430, 31.2560), (30.0396, 31.2550)], density="loose", periods=["fatimid-1050"]),
    # ---- Mamluk and Ottoman: old Fustat shrunk to the river
    dict(name="Misr al-Qadima by the river", polygon=[(30.0000, 31.2300), (30.0050, 31.2302), (30.0050, 31.2380), (30.0000, 31.2380)], density="dense", periods=LATER),
    dict(name="Misr al-Qadima by the river", polygon=[(30.0088, 31.2312), (30.0200, 31.2318), (30.0200, 31.2372), (30.0090, 31.2390)], density="dense", periods=LATER),
    dict(name="Qasr al-Sham' lanes", polygon=[(30.0052, 31.2320), (30.0084, 31.2322), (30.0084, 31.2370), (30.0052, 31.2370)], density="loose", periods=LATER),
    dict(name="Potteries of Fustat", polygon=[(30.0060, 31.2405), (30.0140, 31.2412), (30.0140, 31.2455), (30.0060, 31.2450)], density="loose", periods=LATER),
    # ---- Mamluk and Ottoman: al-Qahira full, the city grown south to the Citadel and west over the canal
    dict(name="Harat Zuwayla", polygon=[(30.0442, 31.2551), (30.0488, 31.2567), (30.0490, 31.2596), (30.0450, 31.2588), (30.0438, 31.2580)], density="dense", periods=LATER),
    dict(name="al-Ghuriya and al-Batiliyya", polygon=[(30.0432, 31.2596), (30.0470, 31.2603), (30.0472, 31.2650), (30.0434, 31.2652)], density="dense", periods=LATER),
    dict(name="al-Barqiyya", polygon=[(30.0472, 31.2650), (30.0512, 31.2650), (30.0512, 31.2685), (30.0466, 31.2670)], density="dense", periods=LATER),
    dict(name="Khan al-Khalili and al-Husayn", polygon=[(30.0486, 31.2616), (30.0510, 31.2616), (30.0510, 31.2648), (30.0486, 31.2648)], density="dense", periods=LATER),
    dict(name="Harat Baha' al-Din", polygon=[(30.0510, 31.2570), (30.0553, 31.2592), (30.0546, 31.2612), (30.0510, 31.2610)], density="dense", periods=LATER),
    dict(name="al-Gamaliyya", polygon=[(30.0512, 31.2626), (30.0533, 31.2628), (30.0538, 31.2688), (30.0512, 31.2688)], density="dense", periods=LATER),
    dict(name="Darb al-Ahmar and al-Tabbana", polygon=[(30.0335, 31.2578), (30.0426, 31.2592), (30.0426, 31.2650), (30.0360, 31.2638)], density="dense", periods=LATER),
    dict(name="Khayamiyya and Suq al-Silah", polygon=[(30.0336, 31.2524), (30.0424, 31.2554), (30.0424, 31.2570), (30.0336, 31.2570)], density="dense", periods=LATER),
    dict(name="al-Saliba and Ibn Tulun", polygon=[(30.0240, 31.2452), (30.0330, 31.2440), (30.0326, 31.2540), (30.0240, 31.2540)], density="dense", periods=LATER),
    dict(name="Sayyida Zaynab", polygon=[(30.0302, 31.2396), (30.0360, 31.2440), (30.0336, 31.2470), (30.0300, 31.2440)], density="dense", periods=LATER),
    dict(name="al-Khalifa", polygon=[(30.0190, 31.2520), (30.0238, 31.2520), (30.0250, 31.2580), (30.0200, 31.2595)], density="loose", periods=LATER),
    dict(name="Round the Birkat al-Fil", polygon=[(30.0400, 31.2480), (30.0436, 31.2524), (30.0430, 31.2550), (30.0398, 31.2535)], density="loose", periods=LATER),
    dict(name="Bab al-Luq", polygon=[(30.0350, 31.2350), (30.0450, 31.2366), (30.0450, 31.2470), (30.0360, 31.2440)], density="loose", periods=LATER),
    dict(name="al-Maqs", polygon=[(30.0470, 31.2380), (30.0555, 31.2400), (30.0555, 31.2470), (30.0470, 31.2470)], density="loose", periods=["mamluk-1350"]),
    dict(name="al-Husayniyya", polygon=[(30.0562, 31.2638), (30.0640, 31.2648), (30.0640, 31.2712), (30.0562, 31.2662)], density="loose", periods=LATER),
    dict(name="Bulaq", polygon=[(30.0545, 31.2345), (30.0640, 31.2333), (30.0640, 31.2385), (30.0545, 31.2390)], density="loose", periods=["mamluk-1350"]),
    dict(name="Bulaq", polygon=[(30.0530, 31.2310), (30.0645, 31.2296), (30.0645, 31.2370), (30.0530, 31.2372)], density="dense", periods=["ottoman-1600"]),
    dict(name="Azbakiyya", polygon=[(30.0500, 31.2440), (30.0560, 31.2450), (30.0560, 31.2470), (30.0500, 31.2470)], density="loose", periods=["ottoman-1600"]),
    dict(name="Bab al-Bahr", polygon=[(30.0555, 31.2500), (30.0600, 31.2510), (30.0600, 31.2570), (30.0555, 31.2560)], density="dense", periods=["ottoman-1600"]),
]

GARDENS = [
    dict(name="Roda orchards", polygon=[(30.0150, 31.2240), (30.0300, 31.2240), (30.0300, 31.2290), (30.0150, 31.2280)], kind="orchard"),
    dict(name="Fields of Giza", polygon=[(30.0000, 31.2060), (30.0280, 31.2060), (30.0280, 31.2120), (30.0000, 31.2120)], kind="orchard"),
    dict(name="al-Bustan al-Kafuri", polygon=[(30.0488, 31.2568), (30.0520, 31.2580), (30.0518, 31.2587), (30.0488, 31.2586)], kind="park", periods=["fatimid-1050"]),
    dict(name="Gardens of al-Maqs", polygon=[(30.0440, 31.2440), (30.0500, 31.2450), (30.0500, 31.2510), (30.0440, 31.2500)], kind="orchard", periods=["fatimid-1050"]),
    dict(name="Palm groves", polygon=[(30.0440, 31.2440), (30.0520, 31.2460), (30.0520, 31.2520), (30.0440, 31.2500)], kind="orchard", periods=EARLY),
    dict(name="Gardens of Bulaq island", polygon=[(30.0480, 31.2200), (30.0580, 31.2185), (30.0580, 31.2230), (30.0480, 31.2245)], kind="orchard", periods=["ottoman-1600"]),
]

DISTRICTS = [
    dict(id="fustat", name="Fustat (Misr)", polygon=[(30.0000, 31.2296), (30.0225, 31.2345), (30.0225, 31.2480), (30.0000, 31.2480)],
         description="The first Arab capital, founded 641 as a camp round the Mosque of Amr; the commercial city of Egypt for five centuries, with glassworks, potteries and tall houses. Burned in 1168 and left to decay; its southern part lived on as Misr al-Qadima."),
    dict(id="qasr-al-sham", name="Qasr al-Sham' (Babylon)", polygon=[(30.0048, 31.2296), (30.0080, 31.2296), (30.0080, 31.2322), (30.0048, 31.2322)],
         description="The Roman fortress of Babylon, home of Coptic Christians and Jews through every era: churches built into its walls and the Ben Ezra synagogue."),
    dict(id="al-askar", name="al-Askar", polygon=[(30.0222, 31.2350), (30.0300, 31.2372), (30.0300, 31.2460), (30.0222, 31.2440)], periods=["tulunid-880", "fatimid-1050"],
         description="'The Cantonment': the Abbasid governors' town of 750, with their palace and mosque, absorbed into Fustat by the 10th century."),
    dict(id="al-qatai", name="al-Qata'i", polygon=[(30.0230, 31.2440), (30.0420, 31.2480), (30.0420, 31.2585), (30.0230, 31.2585)], periods=["tulunid-880", "fatimid-1050"],
         description="Ibn Tulun's royal city of 870, divided into wards (qata'i) for his regiments. The Abbasid army destroyed it in 905; only the mosque survived."),
    dict(id="al-qahira", name="al-Qahira", polygon=[(30.0556, 31.2590), (30.0549, 31.2631), (30.0552, 31.2648), (30.0540, 31.2695), (30.0500, 31.2690), (30.0460, 31.2675), (30.0428, 31.2655), (30.0428, 31.2610), (30.0430, 31.2573), (30.0440, 31.2545), (30.0500, 31.2565)],
         periods=FATIMID_ON, description="'The Victorious': the Fatimid palace city of 969, closed to commoners at first; under the Mamluks the crowded heart of the whole city, its main street lined with madrasas and markets."),
    dict(id="roda", name="Jazirat al-Rawda", polygon=[(30.0050, 31.2251), (30.0150, 31.2286), (30.0300, 31.2305), (30.0380, 31.2270), (30.0250, 31.2226), (30.0085, 31.2238)],
         description="Roda Island: a Byzantine fort, then the Arab shipyard and the Nilometer; gardens, and in the 1240s the Ayyubid sultan's island citadel for his Bahri Mamluks."),
    dict(id="qarafa", name="al-Qarafa", polygon=[(30.0040, 31.2490), (30.0230, 31.2560), (30.0240, 31.2640), (30.0040, 31.2640)],
         description="The Southern Cemetery, the City of the Dead under the Muqattam, with tombs of saints and caliphs' families, visited on Fridays and feast days."),
    dict(id="darb-al-ahmar", name="Darb al-Ahmar", polygon=[(30.0326, 31.2560), (30.0428, 31.2575), (30.0428, 31.2650), (30.0330, 31.2630)], periods=LATER,
         description="The quarter between Bab Zuwayla and the Citadel, filled after 1300 with the mosques, palaces and markets of Mamluk amirs."),
    dict(id="husayniyya", name="al-Husayniyya", polygon=[(30.0558, 31.2630), (30.0655, 31.2640), (30.0655, 31.2720), (30.0558, 31.2665)], periods=LATER,
         description="The suburb outside Bab al-Futuh and Bab al-Nasr, settled in the 13th century by soldiers and Mongol refugees; butchers and caravan trades."),
    dict(id="bulaq", name="Bulaq", polygon=[(30.0530, 31.2300), (30.0655, 31.2290), (30.0655, 31.2385), (30.0530, 31.2390)], periods=LATER,
         description="Land the Nile left behind after 1300, Cairo's main river port from the 15th century: wikalas, granaries, boatyards and customs."),
    dict(id="northern-cemetery", name="Sahra' al-Mamalik (Northern Cemetery)", polygon=[(30.0380, 31.2705), (30.0560, 31.2715), (30.0560, 31.2800), (30.0380, 31.2800)], periods=LATER,
         description="The desert east of al-Qahira where Mamluk sultans built great funerary complexes from the 14th century, the tomb of Qaitbay among them."),
]

LABELS = [
    dict(text="al-Nil", position=(30.0030, 31.2213), size="lg", rotation=-80),
    dict(text="Bahr al-Nil", position=(30.0480, 31.2345), size="lg", rotation=-70, periods=TO_FATIMID),
    dict(text="Bahr al-Nil", position=(30.0405, 31.2262), size="md", rotation=-70, periods=LATER),
    dict(text="Jazirat al-Rawda", position=(30.0220, 31.2263), size="sm", rotation=-80),
    dict(text="al-Muqattam", position=(30.0150, 31.2730), size="md", rotation=-60),
    dict(text="Fustat", position=(30.0185, 31.2392), size="lg", periods=TO_FATIMID),
    dict(text="Misr al-Qadima", position=(30.0150, 31.2345), size="md", periods=LATER),
    dict(text="al-Qahira", position=(30.0470, 31.2560), size="lg", periods=FATIMID_ON),
    dict(text="al-Khalij", position=(30.0415, 31.2485), size="sm", rotation=-45),
    dict(text="al-Qata'i", position=(30.0345, 31.2495), size="md", periods=["tulunid-880"]),
    dict(text="al-Askar", position=(30.0260, 31.2400), size="sm", periods=["tulunid-880", "fatimid-1050"]),
    dict(text="al-Qarafa", position=(30.0110, 31.2560), size="md"),
    dict(text="al-Jiza", position=(30.0160, 31.2090), size="md"),
    dict(text="Bulaq", position=(30.0615, 31.2370), size="md", periods=LATER),
    dict(text="al-Maqs", position=(30.0600, 31.2500), size="sm", periods=["fatimid-1050"]),
    dict(text="Birkat al-Fil", position=(30.0362, 31.2500), size="sm", periods=FATIMID_ON),
    dict(text="Azbakiyya", position=(30.0512, 31.2486), size="sm", periods=["ottoman-1600"]),
    dict(text="al-Husayniyya", position=(30.0610, 31.2675), size="sm", periods=LATER),
    dict(text="Qarafat al-Mamalik", position=(30.0500, 31.2755), size="sm", rotation=-80, periods=LATER),
]
