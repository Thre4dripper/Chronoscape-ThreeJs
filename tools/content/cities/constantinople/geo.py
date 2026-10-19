# Constantinople, "Queen of Cities": the historic peninsula from the Theodosian Land Walls to
# Seraglio Point, the Golden Horn, Galata and Pera, and the mouth of the Bosphorus, from
# Constantine's refoundation to Süleyman's Istanbul.
ALL = ["constantine-337", "justinian-562", "komnenian-1150", "palaiologan-1453", "suleyman-1560"]
BYZ = ["constantine-337", "justinian-562", "komnenian-1150", "palaiologan-1453"]
THEO = ["justinian-562", "komnenian-1150", "palaiologan-1453", "suleyman-1560"]      # after the Theodosian walls
THEO_BYZ = ["justinian-562", "komnenian-1150", "palaiologan-1453"]
EARLY = ["constantine-337", "justinian-562"]
MIDDLE = ["justinian-562", "komnenian-1150"]
LATE = ["komnenian-1150", "palaiologan-1453"]
OTT = ["suleyman-1560"]
GALATA = ["palaiologan-1453", "suleyman-1560"]

CITY = dict(
    name="Constantinople", subtitle="Queen of Cities",
    description="Constantinople from Constantine's refoundation (330) to Süleyman's Istanbul (1560): the historic peninsula between the Theodosian Land Walls and Seraglio Point, the Golden Horn with Galata and Pera on its north shore, and the mouth of the Bosphorus. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="komnenian-1150",
    world=dict(scale=0.01, heightScale=1.0, walls=["#DCC8A4", "#CFAE86", "#E4D6BA", "#C49A78", "#D8BC96"], roofs=["#B5694C", "#A85E44", "#C27E5C"]),
    camera=dict(target=(41.0105, 28.9700), distance=40, maxDistance=150),
)
FRAME = ((41.0440, 28.9080), (40.9890, 28.9960))
RESOLUTION = 4096
PALETTE = dict(parchment="#E7D4AB", ink="#6C4A33", water="#5F8790", hill="#787C59", road="#8A6A4A")
COMPASS = (40.9935, 28.9880)
CARTOUCHE = (40.9902, 28.9095)

PERIODS = [
    dict(id="constantine-337", label="Constantine's New Rome", year=337, startYear=324, endYear=361,
         summary="Constantine refounds the Greek town of Byzantion as his capital in 324–330: a new land wall about 3 km west of the old one, an oval forum round his porphyry column, the colonnaded Mese, an enlarged Hippodrome joined to a new palace, a Senate house and baths. Brick and rubble faced with marble taken from older cities; much is built in haste and land inside the wall is still empty.",
         population="perhaps 50,000, growing fast",
         feel="Lime dust and scaffolding, statues carted in from every Greek city, and free bread handed out from the steps since 332.",
         style="antique",
         houses=dict(title="Brick houses of the new capital", text="Two- and three-storey houses of brick and mortared rubble with timber floors and tiled roofs, shops opening under the colonnades of the main streets. Officials and senators lured from Rome build courtyard mansions; the old town of Byzantion round the acropolis is denser and poorer."),
         outskirts=dict(title="Villas and vineyards", text="Beyond the new wall: villas, market gardens, vineyards and roadside tombs along the Via Egnatia. Across the Golden Horn the small town of Sykai faces the city.")),
    dict(id="justinian-562", label="Justinian's City", year=562, startYear=361, endYear=1080,
         summary="After the Nika riot burned the centre in 532, Justinian rebuilt it: Hagia Sophia (537, its second dome 562), Hagia Irene, the Basilica Cistern, the bronze-roofed Chalke. The Theodosian land walls of 413 enclose 14 km²; aqueducts and open cisterns feed perhaps half a million people, though the plague of 542 has killed a great many. Brick, marble revetment, lead-covered domes.",
         population="perhaps 400,000–500,000 before the plague of 542",
         feel="No bells yet: wooden semantra clack for prayers, the Blues and Greens chant in the Hippodrome, and the Mese smells of bread, incense and harbour fish.",
         style="antique",
         houses=dict(title="Brick and timber houses", text="Houses of two to four storeys, brick and stone below, timber above, with balconies jutting over streets; Zeno's building law (about 474) tried to keep streets twelve feet wide and balconies high. Shops at street level, families above, a court with a cistern behind."),
         outskirts=dict(title="Between the walls", text="Between Constantine's wall and Theodosius' wall: monasteries, three great open cisterns, market gardens, cemeteries and villas. This belt was never fully built over.")),
    dict(id="komnenian-1150", label="Queen of Cities", year=1150, startYear=1081, endYear=1204,
         summary="Under the Komnenian emperors the court moves to Blachernae in the north-west corner, Manuel I adds a new wall and palace hall there, and John II founds the Pantokrator monastery. Italian merchants hold walled quarters on the Golden Horn: Venetians since 1082, then Pisans and Genoese. Silk, relics and gold coin make it the richest city in Christendom, until the crusaders sack it in 1204.",
         population="perhaps 300,000–400,000",
         feel="Semantra and chanting, Venetian and Pisan voices on the quays, and a skyline of lead domes above red tile.",
         style="medieval",
         houses=dict(title="Byzantine town houses", text="Two- and three-storey houses in bands of brick and stone, the upper storeys of timber jutting over the lanes on beams, tiled roofs, a small court with a well or cistern. Lanes wind between monastery walls; the Italian quarters pack warehouses and houses tight along the quays."),
         outskirts=dict(title="Gardens and monastery estates", text="Orchards, vegetable plots and vineyards inside the land walls, worked by monasteries and hamlets; across the Horn, Pera with its Jewish silk-workers' quarter and the tower that holds the chain.")),
    dict(id="palaiologan-1453", label="The Last Byzantine City", year=1453, startYear=1261, endYear=1453,
         summary="Retaken from the Latins in 1261, the city never recovers: perhaps 50,000 people live in villages separated by fields inside the walls. The emperors live at Blachernae; the Great Palace is a ruin. Genoese Galata across the Horn is richer than its host. On 29 May 1453 Mehmed II's army breaks through the land walls near the Gate of St Romanus.",
         population="perhaps 40,000–50,000",
         feel="Cockcrow and church bells over orchards, goats among broken colonnades, and the Genoese tower watching from across the water.",
         style="medieval",
         houses=dict(title="Houses among ruins", text="Small one- and two-storey houses of reused brick and stone built against older ruins and monastery walls, with vegetable plots between them. The Castilian Pero Tafur, here in 1437, found the city thinly settled and its people poor."),
         outskirts=dict(title="Villages within the walls", text="Orchards, wheat fields and vineyards fill much of the space inside the land walls; clusters of houses round a church or monastery form separate villages.")),
    dict(id="suleyman-1560", label="Ottoman Istanbul", year=1560, startYear=1454, endYear=1566,
         summary="Mehmed II resettled the empty city after 1453 with Muslims, Greeks, Armenians and Jews; under Süleyman it is again the largest city in Europe. Sinan's mosques crown the hills, Topkapı Palace holds the old acropolis, the Bedesten and hans fill the commercial centre, and Galata is a busy port. Timber houses, lead domes, cut stone for mosques.",
         population="perhaps 400,000–500,000",
         feel="The call to prayer from scores of minarets, porters shouting in the bazaar lanes, and the new smell of coffee in Tahtakale.",
         style="courtyard",
         houses=dict(title="Ottoman timber houses", text="Two-storey houses of timber framing filled with brick or mud and plastered, the upper floor jutting on brackets with latticed windows, tiled roofs. Houses turn inward to a garden court behind a blank wall; whole quarters burn in the frequent fires."),
         outskirts=dict(title="Bostans and cemeteries", text="Walled market gardens (bostans) in the Lycus valley and in the old open cisterns, cypress-shaded cemeteries outside the gates, and the vineyards of Pera above Galata.")),
]

# ---------------------------------------------------------------- water
# The sea is one wide path offset 800 m from the shore (Marmara, round Seraglio Point and up the
# Bosphorus); the Golden Horn is a second path offset from its south shore, drawn after it.
WATER = [
    dict(id="propontis", name="Sea of Marmara (Propontis)", width=1600,
         path=[(40.97380, 28.88987), (40.97804, 28.89930), (40.98027, 28.90641), (40.98222, 28.91425), (40.98416, 28.92071), (40.98615, 28.92651), (40.98830, 28.93106), (40.98963, 28.93442), (40.99100, 28.93919), (40.99225, 28.94452), (40.99327, 28.95013), (40.99488, 28.96056), (40.99512, 28.96398), (40.99461, 28.96835), (40.99460, 28.96956), (40.99472, 28.97390), (40.99487, 28.97513), (40.99514, 28.97632), (40.99646, 28.98021), (40.99838, 28.98727), (40.99881, 28.98838), (40.99934, 28.98941), (41.00157, 28.99275), (41.00226, 28.99360), (41.00303, 28.99432), (41.00548, 28.99616), (41.00678, 28.99697), (41.00769, 28.99731), (41.01091, 28.99805), (41.01185, 28.99812), (41.01279, 28.99803), (41.01602, 28.99722), (41.01691, 28.99682), (41.01776, 28.99628), (41.01948, 28.99477), (41.02370, 28.99233), (41.02690, 28.99554), (41.03010, 28.99910), (41.03250, 29.00287), (41.03650, 29.01016), (41.04210, 29.01799), (41.04290, 29.01883), (41.04370, 29.01947), (41.04530, 29.02026), (41.04690, 29.02052), (41.04850, 29.02032)],
         blurb="The Propontis, the small sea between the Dardanelles and the Bosphorus. Grain ships from Egypt (until the 7th century) and later from the Black Sea anchored off the southern harbours; the sea walls rise straight from its shore."),
    dict(id="keras", name="Golden Horn (Keras)", width=520,
         path=[(41.05041, 28.93947), (41.04631, 28.94354), (41.04322, 28.94646), (41.04088, 28.94900), (41.03823, 28.95127), (41.03495, 28.95333), (41.03209, 28.95495), (41.02991, 28.95698), (41.02445, 28.96291), (41.02244, 28.96594), (41.02117, 28.96921), (41.02026, 28.97284), (41.01950, 28.97708), (41.01917, 28.97999), (41.01953, 28.98286), (41.01950, 28.98380)],
         blurb="A drowned river valley 7 km long, the finest natural harbour of the Mediterranean world. In war a chain of iron links on wooden floats was stretched across its mouth from the Tower of Eugenius to the Kastellion of Galata."),
    dict(id="theodosian-harbour", name="Harbour of Theodosius", width=230, periods=["justinian-562"],
         path=[(41.00100, 28.95120), (41.00330, 28.95100), (41.00480, 28.95020)],
         blurb="The largest harbour of the city, built under Theodosius I at the mouth of the Lycus. It silted up from the 7th century; excavations for the Yenikapı station (2004–2013) found 37 shipwrecks in its mud."),
    dict(id="harbour-of-sophia", name="Harbour of Julian (Sophia, Kontoskalion)", width=170, periods=THEO,
         path=[(41.00140, 28.96900), (41.00330, 28.96870)],
         blurb="Built by Julian in 362, rebuilt by Justin II and named after his wife Sophia; dredged and walled by Michael VIII as the Kontoskalion base of the Palaiologan fleet, and under the Ottomans the Kadırga ('galley') harbour."),
    dict(id="lycus", name="Lycus (Lykos)", width=10,
         path=[(41.03050, 28.90750), (41.02800, 28.91700), (41.02420, 28.92680), (41.02000, 28.93300), (41.01500, 28.94000), (41.01150, 28.94550), (41.00850, 28.94950), (41.00500, 28.95020)],
         blurb="The only stream of the peninsula, entering under the land walls in the valley between the Gates of St Romanus and Charisius and running to the Marmara at Vlanga. The walls are weakest where they cross it."),
    dict(id="aetius-cistern", name="Cistern of Aetius", width=85, periods=MIDDLE,
         path=[(41.02640, 28.93800), (41.02660, 28.93990)],
         blurb="An open reservoir of 421, about 244 × 85 m and 15 m deep, one of three great open cisterns between the walls. Its floor is now a football ground."),
    dict(id="aspar-cistern", name="Cistern of Aspar", width=150, periods=MIDDLE,
         path=[(41.02620, 28.94780), (41.02620, 28.94800)],
         blurb="An open reservoir of 459, about 152 m square, on the fifth hill; later a sunken village and garden (Çukurbostan)."),
    dict(id="mocius-cistern", name="Cistern of Mocius", width=150, periods=MIDDLE,
         path=[(41.00440, 28.93300), (41.00440, 28.93330)],
         blurb="The largest open cistern, about 170 × 147 m, built under Anastasius (491–518) on the seventh hill."),
]
ISLANDS = []

HILLS = [
    dict(id="first-hill", name="First Hill (Akropolis)", center=(41.0112, 28.9828), radius=380, blurb="The acropolis of Greek Byzantion, later Topkapı Palace."),
    dict(id="second-hill", name="Second Hill", center=(41.0090, 28.9712), radius=240, blurb="Crowned by the Forum and Column of Constantine."),
    dict(id="third-hill", name="Third Hill", center=(41.0140, 28.9625), radius=380, blurb="The Forum of Theodosius below, the Süleymaniye above."),
    dict(id="fourth-hill", name="Fourth Hill", center=(41.0182, 28.9500), radius=360, blurb="The Church of the Holy Apostles, then the Fatih Mosque."),
    dict(id="fifth-hill", name="Fifth Hill", center=(41.0272, 28.9478), radius=300, blurb="The Cistern of Aspar; later the Selim mosque."),
    dict(id="sixth-hill", name="Sixth Hill", center=(41.0300, 28.9365), radius=420, blurb="The ridge behind Blachernae and the Gate of Charisius, highest point of the city at about 76 m."),
    dict(id="seventh-hill", name="Seventh Hill (Xerolophos)", center=(41.0050, 28.9360), radius=520, blurb="The 'dry hill', with the Forum and Column of Arcadius."),
    dict(id="galata-hill", name="Galata Hill", center=(41.0278, 28.9748), radius=420, blurb="The steep hill of Sykai, Pera and Galata across the Golden Horn."),
]

# ---------------------------------------------------------------- streets
MESE = [(41.00828, 28.97735), (41.00860, 28.97450), (41.00870, 28.97140), (41.00930, 28.96900), (41.01000, 28.96550), (41.01020, 28.96400), (41.01080, 28.96050), (41.01180, 28.95750), (41.01250, 28.95550)]
MESE_N = [(41.01250, 28.95550), (41.01450, 28.95250), (41.01700, 28.94800), (41.01950, 28.94600), (41.02250, 28.94200), (41.02500, 28.93850), (41.02720, 28.93550), (41.02900, 28.93270), (41.03200, 28.92500), (41.03500, 28.91500), (41.03800, 28.90600)]
MESE_S = [(41.01250, 28.95550), (41.01050, 28.95100), (41.00850, 28.94650), (41.00600, 28.93950), (41.00350, 28.93400), (41.00050, 28.92900), (40.99750, 28.92550), (40.99430, 28.92250), (40.99450, 28.91500), (40.99250, 28.90500)]
ROADS = [
    dict(id="mese", name="Mese", path=MESE, width=26, style="major", labelled=True, periods=BYZ,
         blurb="The 'Middle Street', 25 m wide between two-storey colonnades with shops, the processional way from the Milion past the fora to the land gates."),
    dict(id="divan-yolu", name="Divan Yolu", path=MESE, width=18, style="major", labelled=True, periods=OTT,
         blurb="The 'Council Road', the Mese narrowed by encroaching shops, along which viziers rode to the Divan at Topkapı."),
    dict(id="mese-north", name="Mese (north branch)", path=MESE_N, width=18, style="major", labelled=True, periods=BYZ,
         blurb="From the Philadelphion past the Holy Apostles to the Gate of Charisius and the road to Adrianople."),
    dict(id="edirnekapi-road", name="Road to Edirnekapı", path=MESE_N, width=14, style="major", labelled=True, periods=OTT,
         blurb="From Şehzadebaşı past the Fatih complex to the Edirne gate and the road to Edirne."),
    dict(id="mese-south", name="Mese and Via Egnatia", path=MESE_S, width=18, style="major", labelled=True, periods=BYZ,
         blurb="The southern branch through the Forum of the Ox and the Forum of Arcadius to the Golden Gate, continuing as the Via Egnatia to Thessalonica and the Adriatic."),
    dict(id="yedikule-road", name="Road to Yedikule", path=MESE_S, width=12, style="major", labelled=True, periods=OTT,
         blurb="Aksaray to Avratpazarı and Yedikule, along the old southern Mese."),
    dict(id="pege-road", name="Road to the Pege Gate", path=[(41.00600, 28.93950), (41.00620, 28.93000), (41.00620, 28.91640), (41.00650, 28.90700)], width=10, periods=THEO_BYZ,
         blurb="To the Gate of the Spring, named after the healing spring and shrine of the Virgin outside it."),
    dict(id="silivrikapi-road", name="Road to Silivrikapı", path=[(41.00600, 28.93950), (41.00620, 28.93000), (41.00620, 28.91640), (41.00650, 28.90700)], width=10, periods=OTT),
    dict(id="rhegion-road", name="Road to the Gate of Rhegion", path=[(41.00850, 28.94650), (41.01050, 28.93500), (41.01250, 28.91700), (41.01300, 28.90700)], width=10, periods=THEO_BYZ),
    dict(id="romanus-road", name="Road to the Gate of St Romanus", path=[(41.01050, 28.95100), (41.01400, 28.94000), (41.01700, 28.93000), (41.01930, 28.92120), (41.02100, 28.90800)], width=12, labelled=True, periods=THEO_BYZ,
         blurb="Down the Lycus valley to the Gate of St Romanus, where the walls were breached in 1453."),
    dict(id="topkapi-road", name="Road to Topkapı", path=[(41.01050, 28.95100), (41.01400, 28.94000), (41.01700, 28.93000), (41.01930, 28.92120), (41.02100, 28.90800)], width=12, labelled=True, periods=OTT),
    dict(id="makros-embolos", name="Makros Embolos", path=[(41.01020, 28.96600), (41.01300, 28.96700), (41.01550, 28.96820), (41.01800, 28.97050)], width=10, periods=BYZ,
         blurb="The 'Long Portico', a colonnaded street from the Mese down to the Golden Horn quays; the Ottoman Uzun Çarşı follows it."),
    dict(id="uzun-carsi", name="Uzun Çarşı", path=[(41.01020, 28.96600), (41.01300, 28.96700), (41.01550, 28.96820), (41.01800, 28.97050)], width=8, periods=OTT,
         blurb="The 'Long Market' from the Bedesten down to the Golden Horn, lined with shops of turners, cobblers and haberdashers."),
    dict(id="strategion-road", name="Road to the Strategion", path=[(41.00828, 28.97735), (41.00950, 28.97690), (41.01150, 28.97730), (41.01400, 28.97750), (41.01620, 28.97700)], width=10, periods=BYZ,
         blurb="From the Augusteion down to the old harbours of Byzantion on the Golden Horn."),
    dict(id="horn-road", name="Golden Horn shore road", path=[(41.01620, 28.97989), (41.01661, 28.97635), (41.01742, 28.97178), (41.01845, 28.96769), (41.02001, 28.96373), (41.02238, 28.96013), (41.02813, 28.95386), (41.03066, 28.95154), (41.03657, 28.94809), (41.03919, 28.94585), (41.04100, 28.94380)], width=8, periods=["komnenian-1150", "palaiologan-1453", "suleyman-1560"],
         blurb="Behind the sea walls, past the Italian quarters, the Phanar and the Petrion to Blachernae."),
    dict(id="blachernae-road", name="Road to Blachernae", path=[(41.01950, 28.94600), (41.02400, 28.94450), (41.02900, 28.94350), (41.03400, 28.94350), (41.03650, 28.94450)], width=10, periods=LATE,
         blurb="From the Holy Apostles along the ridge to the Komnenian palace."),
    dict(id="hippodrome-road", name="Road to the Boukoleon", path=[(41.00790, 28.97760), (41.00680, 28.97750), (41.00620, 28.97760), (41.00560, 28.98050), (41.00450, 28.98200)], width=8, periods=EARLY),
    dict(id="galata-street", name="Main street of Galata", path=[(41.02320, 28.97530), (41.02460, 28.97490), (41.02560, 28.97440)], width=8, periods=GALATA),
    dict(id="pera-road", name="Road to Pera", path=[(41.02560, 28.97440), (41.02850, 28.97470), (41.03200, 28.97900), (41.03500, 28.98300), (41.03700, 28.98550)], width=10, labelled=True, periods=GALATA,
         blurb="Up from the Galata Tower over the vineyards of Pera; the later Grande Rue de Péra (İstiklal Caddesi)."),
    dict(id="tophane-road", name="Tophane shore road", path=[(41.02350, 28.97700), (41.02500, 28.98050), (41.02800, 28.98350), (41.03200, 28.98750), (41.03500, 28.99050)], width=8, periods=OTT),
]

# ---------------------------------------------------------------- walls and gates
THEODOSIAN = [(40.99250, 28.92190), (40.99410, 28.92229), (40.99650, 28.92050), (41.00030, 28.91820), (41.00400, 28.91680), (41.00620, 28.91640), (41.01000, 28.91650), (41.01250, 28.91700),
              (41.01600, 28.91880), (41.01930, 28.92120), (41.02180, 28.92380), (41.02420, 28.92680), (41.02680, 28.93000), (41.02900, 28.93270), (41.03180, 28.93700), (41.03380, 28.93980),
              (41.03520, 28.94080), (41.03720, 28.94200), (41.03950, 28.94300), (41.04180, 28.94400)]
WALLS = [
    dict(id="constantinian-wall", name="Wall of Constantine", periods=EARLY,
         path=[(41.03000, 28.95350), (41.02550, 28.94700), (41.02050, 28.94400), (41.01500, 28.94250), (41.00900, 28.94100), (41.00400, 28.94000), (40.99950, 28.93950)],
         blurb="Built 324–328 about 3 km west of the old wall of Byzantion. Almost nothing survives and its trace is known only from texts; this follows the usual reconstruction. It decayed after 413 and was gone by the 9th century."),
    dict(id="theodosian-walls", name="Theodosian Land Walls", path=THEODOSIAN, periods=THEO,
         blurb="Built 405–413 under Theodosius II and doubled after the earthquake of 447: a moat, an outer wall and a 12 m inner wall with 96 towers, 5.7 km from the Marmara to the Golden Horn. They held for a thousand years until the cannon of 1453."),
    dict(id="marmara-walls", name="Sea walls of the Marmara", periods=THEO,
         path=[(40.99267, 28.92186), (40.99467, 28.92607), (40.99638, 28.93039), (40.99799, 28.93591), (40.99939, 28.94193), (41.00049, 28.94794), (41.00220, 28.95896), (41.00260, 28.96451), (41.00199, 28.96895), (41.00209, 28.97291), (41.00328, 28.97640), (41.00513, 28.98327), (41.00688, 28.98596), (41.00934, 28.98779), (41.01188, 28.98833), (41.01410, 28.98777), (41.01589, 28.98618)],
         blurb="A single wall with 188 towers along the Marmara, rising from the water or from a narrow beach; strong currents made landings here difficult."),
    dict(id="horn-walls", name="Sea walls of the Golden Horn", periods=THEO,
         path=[(41.01582, 28.98628), (41.01700, 28.98316), (41.01660, 28.97997), (41.01701, 28.97645), (41.01781, 28.97193), (41.01882, 28.96790), (41.02035, 28.96403), (41.02266, 28.96051), (41.02838, 28.95429), (41.03090, 28.95197), (41.03680, 28.94852), (41.03947, 28.94622), (41.04167, 28.94380)],
         blurb="A wall of 110 towers set back from the quays, pierced by gates to the landing stages. The Venetians stormed it in 1203 and 1204 from ladders on their ships."),
    dict(id="galata-walls", name="Walls of Galata", closed=True, periods=GALATA,
         path=[(41.02580, 28.96780), (41.02600, 28.97100), (41.02575, 28.97417), (41.02480, 28.97720), (41.02380, 28.97980), (41.02190, 28.97960), (41.02220, 28.97700), (41.02270, 28.97400), (41.02330, 28.97150), (41.02390, 28.96950), (41.02450, 28.96800)],
         blurb="The Genoese colony's walls, built in stages from 1304 and crowned by the Galata Tower in 1348. Mehmed II had the landward walls partly torn down after 1453."),
]
GATES = [
    dict(id="golden-gate-g", name="Golden Gate", position=(40.99410, 28.92229), periods=THEO_BYZ),
    dict(id="xylokerkos", name="Gate of Xylokerkos", position=(41.00030, 28.91820), periods=THEO_BYZ),
    dict(id="pege-gate", name="Gate of the Spring (Pege)", position=(41.00620, 28.91640), periods=THEO_BYZ),
    dict(id="rhegion-gate", name="Gate of Rhegion", position=(41.01250, 28.91700), periods=THEO_BYZ),
    dict(id="romanus-gate", name="Gate of St Romanus", position=(41.01930, 28.92120), periods=THEO_BYZ),
    dict(id="charisius-gate", name="Gate of Charisius", position=(41.02900, 28.93270), periods=THEO_BYZ),
    dict(id="kaligaria-gate", name="Gate of Kaligaria", position=(41.03520, 28.94080), periods=LATE),
    dict(id="eugenius-gate", name="Gate of Eugenius", position=(41.01650, 28.98200), periods=THEO_BYZ),
    dict(id="perama-gate", name="Gate of Perama", position=(41.01700, 28.97450), periods=THEO_BYZ),
    dict(id="drungarios-gate", name="Gate of the Drungarios", position=(41.01860, 28.96880), periods=THEO_BYZ),
    dict(id="phanar-gate", name="Gate of the Phanar", position=(41.03100, 28.95180), periods=THEO_BYZ),
    dict(id="psamathia-gate", name="Gate of Psamathia", position=(40.99760, 28.93500), periods=THEO_BYZ),
    dict(id="yedikule-g", name="Yedikule Kapı", position=(40.99410, 28.92229), periods=OTT),
    dict(id="belgrad-kapi", name="Belgrad Kapı", position=(41.00030, 28.91820), periods=OTT),
    dict(id="silivri-kapi", name="Silivri Kapı", position=(41.00620, 28.91640), periods=OTT),
    dict(id="mevlevihane-kapi", name="Mevlevihane Kapı", position=(41.01250, 28.91700), periods=OTT),
    dict(id="top-kapi", name="Topkapı", position=(41.01930, 28.92120), periods=OTT),
    dict(id="edirne-kapi", name="Edirnekapı", position=(41.02900, 28.93270), periods=OTT),
    dict(id="egri-kapi", name="Eğrikapı", position=(41.03520, 28.94080), periods=OTT),
    dict(id="balikpazari-kapi", name="Balıkpazarı Kapı", position=(41.01700, 28.97450), periods=OTT),
    dict(id="fener-kapi", name="Fener Kapı", position=(41.03100, 28.95180), periods=OTT),
    dict(id="samatya-kapi", name="Samatya Kapı", position=(40.99760, 28.93500), periods=OTT),
    dict(id="azap-kapi", name="Azapkapı", position=(41.02580, 28.96780), periods=OTT),
]
BRIDGES = [
    dict(id="pontoon-1453", name="Mehmed II's pontoon bridge", path=[(41.04020, 28.94360), (41.04620, 28.95030)], build="timber", arches=12, periods=["palaiologan-1453"],
         blurb="During the siege the Ottomans floated a road of barrels lashed together across the inner Golden Horn, to bring guns against the walls by the Kynegion."),
]
AQUEDUCTS = [
    dict(name="Water channel of Valens", path=[(41.03300, 28.90800), (41.03050, 28.92000), (41.02850, 28.93200), (41.02450, 28.94100), (41.02000, 28.94550), (41.01700, 28.94950)], periods=THEO),
    dict(name="Channel to the Nymphaeum", path=[(41.01450, 28.96070), (41.01250, 28.96250), (41.01100, 28.96300)], periods=THEO_BYZ),
]

# ---------------------------------------------------------------- built-up areas
# zones of the peninsula, reused by era (the generator keeps roads, walls, water and monuments clear)
EMINONU = [(41.01850, 28.97000), (41.01780, 28.97650), (41.01720, 28.98000), (41.01500, 28.98120), (41.01150, 28.98000), (41.00950, 28.97900), (41.00900, 28.97700), (41.00950, 28.97000)]
ACROPOLIS = [(41.01760, 28.98200), (41.01620, 28.98650), (41.01400, 28.98820), (41.00950, 28.98820), (41.00670, 28.98620), (41.00800, 28.98250), (41.01100, 28.98050), (41.01500, 28.98150)]
PALACE_QUARTER = [(41.00800, 28.97700), (41.00780, 28.98250), (41.00550, 28.98400), (41.00400, 28.98000), (41.00310, 28.97650), (41.00190, 28.97300), (41.00180, 28.96950), (41.00820, 28.96950)]
BAZAAR_NORTH = [(41.00980, 28.97050), (41.01850, 28.97000), (41.01920, 28.96780), (41.02080, 28.96400), (41.02300, 28.96050), (41.02350, 28.95850), (41.01600, 28.95800), (41.01150, 28.95900), (41.01050, 28.96350)]
KUMKAPI = [(41.00820, 28.96950), (41.00180, 28.96950), (41.00230, 28.96450), (41.00200, 28.95900), (41.00130, 28.95400), (41.00950, 28.95400), (41.01050, 28.96000), (41.00980, 28.96550)]
ZEYREK = [(41.01600, 28.95750), (41.02350, 28.95800), (41.02600, 28.95600), (41.02880, 28.95300), (41.03100, 28.95050), (41.03000, 28.94600), (41.02000, 28.94650), (41.01350, 28.95200), (41.01250, 28.95650)]
AKSARAY = [(41.01150, 28.95350), (41.00130, 28.95350), (41.00030, 28.94800), (40.99930, 28.94200), (41.00600, 28.94200), (41.01000, 28.94600), (41.01250, 28.95100)]
PHANAR = [(41.04150, 28.94450), (41.03950, 28.94680), (41.03680, 28.94880), (41.03400, 28.95050), (41.03150, 28.95150), (41.03030, 28.94550), (41.03030, 28.94150), (41.03380, 28.94100), (41.03700, 28.94300), (41.04000, 28.94400)]
EDIRNEKAPI = [(41.03000, 28.94100), (41.03000, 28.94550), (41.02000, 28.94550), (41.01850, 28.94050), (41.02000, 28.93400), (41.02420, 28.92850), (41.02850, 28.93400), (41.03250, 28.93850)]
LYCUS = [(41.02000, 28.93350), (41.01850, 28.94000), (41.02000, 28.94500), (41.01350, 28.95100), (41.01000, 28.94550), (41.00650, 28.94150), (41.00800, 28.93100), (41.01250, 28.92300), (41.01850, 28.92350)]
PSAMATHIA = [(41.00650, 28.94150), (40.99930, 28.94150), (40.99780, 28.93600), (40.99620, 28.93050), (40.99500, 28.92650), (40.99700, 28.92250), (41.00050, 28.92000), (41.00650, 28.91900), (41.00800, 28.93000)]
GALATA_IN = [(41.02560, 28.96810), (41.02580, 28.97100), (41.02555, 28.97400), (41.02465, 28.97700), (41.02365, 28.97950), (41.02210, 28.97935), (41.02240, 28.97700), (41.02290, 28.97400), (41.02350, 28.97150), (41.02405, 28.96960), (41.02460, 28.96830)]
PERA = [(41.02620, 28.97000), (41.03000, 28.96900), (41.03500, 28.97400), (41.03750, 28.98200), (41.03600, 28.98600), (41.03100, 28.98250), (41.02750, 28.97900), (41.02620, 28.97500)]
TOPHANE = [(41.02450, 28.97950), (41.02750, 28.98000), (41.03150, 28.98350), (41.03500, 28.98700), (41.03420, 28.99050), (41.03050, 28.98750), (41.02650, 28.98350), (41.02450, 28.98150)]
KASIMPASA = [(41.02800, 28.96900), (41.03200, 28.96500), (41.03700, 28.96150), (41.04000, 28.96200), (41.03900, 28.96800), (41.03400, 28.97100), (41.02950, 28.97150)]
HASKOY = [(41.04150, 28.95550), (41.04350, 28.95250), (41.04400, 28.95700), (41.04200, 28.96000)]
SYKAI = [(41.02380, 28.97050), (41.02600, 28.97100), (41.02560, 28.97600), (41.02380, 28.97900), (41.02230, 28.97800), (41.02270, 28.97400)]

BLOCKS = [
    # Constantine: the old town and the new monumental centre are built up; west of the Forum of the Ox it is still filling in
    dict(name="Old Byzantion", polygon=EMINONU, density="dense", periods=["constantine-337"]),
    dict(name="Akropolis", polygon=ACROPOLIS, density="dense", periods=["constantine-337"]),
    dict(name="Palace quarter", polygon=PALACE_QUARTER, density="dense", periods=["constantine-337"]),
    dict(name="Mese north", polygon=BAZAAR_NORTH, density="dense", periods=["constantine-337"]),
    dict(name="Mese south", polygon=KUMKAPI, density="dense", periods=["constantine-337"]),
    dict(name="New quarters", polygon=ZEYREK, density="loose", periods=["constantine-337"]),
    dict(name="New quarters", polygon=AKSARAY, density="loose", periods=["constantine-337"]),
    dict(name="Sykai", polygon=SYKAI, density="loose", periods=["constantine-337"]),
    # Justinian: dense to Constantine's wall, loose between the walls
    dict(name="Chalkoprateia and the harbours", polygon=EMINONU, density="dense", periods=["justinian-562"]),
    dict(name="Akropolis", polygon=ACROPOLIS, density="dense", periods=["justinian-562"]),
    dict(name="Palace quarter", polygon=PALACE_QUARTER, density="dense", periods=["justinian-562", "komnenian-1150"]),
    dict(name="Artopoleia and Makros Embolos", polygon=BAZAAR_NORTH, density="dense", periods=["justinian-562", "komnenian-1150"]),
    dict(name="Kontoskalion quarter", polygon=KUMKAPI, density="dense", periods=["justinian-562", "komnenian-1150"]),
    dict(name="Fourth hill", polygon=ZEYREK, density="dense", periods=["justinian-562", "komnenian-1150"]),
    dict(name="Forum of the Ox", polygon=AKSARAY, density="dense", periods=["justinian-562"]),
    dict(name="Petrion and Phanar", polygon=PHANAR, density="loose", periods=["justinian-562"]),
    dict(name="Between the walls", polygon=EDIRNEKAPI, density="loose", periods=["justinian-562", "komnenian-1150"]),
    dict(name="Lycus valley", polygon=LYCUS, density="loose", periods=["justinian-562", "komnenian-1150", "palaiologan-1453"]),
    dict(name="Psamathia", polygon=PSAMATHIA, density="loose", periods=["justinian-562", "komnenian-1150", "palaiologan-1453"]),
    dict(name="Sykai (Justinianae)", polygon=SYKAI, density="dense", periods=["justinian-562"]),
    # Komnenian: the Italian quarters on the Horn, Blachernae built up
    dict(name="Venetian, Amalfitan and Pisan quarters", polygon=EMINONU, density="dense", periods=["komnenian-1150"]),
    dict(name="Mangana", polygon=ACROPOLIS, density="loose", periods=["komnenian-1150", "palaiologan-1453"]),
    dict(name="Forum of the Ox", polygon=AKSARAY, density="dense", periods=["komnenian-1150"]),
    dict(name="Petrion, Phanar and Blachernae", polygon=PHANAR, density="dense", periods=["komnenian-1150", "palaiologan-1453"]),
    dict(name="Pera", polygon=SYKAI, density="loose", periods=["komnenian-1150"]),
    # Palaiologan: villages in a shrunken city
    dict(name="Venetian quarter", polygon=EMINONU, density="dense", periods=["palaiologan-1453"]),
    dict(name="Ruins of the palace quarter", polygon=PALACE_QUARTER, density="loose", periods=["palaiologan-1453"]),
    dict(name="Market quarter", polygon=BAZAAR_NORTH, density="dense", periods=["palaiologan-1453"]),
    dict(name="Kontoskalion", polygon=KUMKAPI, density="loose", periods=["palaiologan-1453"]),
    dict(name="Pantokrator village", polygon=ZEYREK, density="loose", periods=["palaiologan-1453"]),
    dict(name="Forum of the Ox", polygon=AKSARAY, density="loose", periods=["palaiologan-1453"]),
    dict(name="Fields by the walls", polygon=EDIRNEKAPI, density="loose", periods=["palaiologan-1453"]),
    dict(name="Genoese Galata", polygon=GALATA_IN, density="dense", periods=["palaiologan-1453"]),
    # Ottoman Istanbul
    dict(name="Eminönü and Tahtakale", polygon=EMINONU, density="dense", periods=OTT),
    dict(name="Sultanahmet and Kadırga", polygon=PALACE_QUARTER, density="dense", periods=OTT),
    dict(name="Bazaar quarter", polygon=BAZAAR_NORTH, density="dense", periods=OTT),
    dict(name="Kumkapı", polygon=KUMKAPI, density="dense", periods=OTT),
    dict(name="Fatih and Zeyrek", polygon=ZEYREK, density="dense", periods=OTT),
    dict(name="Aksaray", polygon=AKSARAY, density="dense", periods=OTT),
    dict(name="Fener and Balat", polygon=PHANAR, density="dense", periods=OTT),
    dict(name="Karagümrük", polygon=EDIRNEKAPI, density="dense", periods=OTT),
    dict(name="Lycus bostans", polygon=LYCUS, density="loose", periods=OTT),
    dict(name="Samatya and Kocamustafapaşa", polygon=PSAMATHIA, density="loose", periods=OTT),
    dict(name="Galata", polygon=GALATA_IN, density="dense", periods=OTT),
    dict(name="Pera vineyards", polygon=PERA, density="loose", periods=GALATA),
    dict(name="Tophane", polygon=TOPHANE, density="dense", periods=OTT),
    dict(name="Kasımpaşa", polygon=KASIMPASA, density="dense", periods=OTT),
    dict(name="Hasköy", polygon=HASKOY, density="loose", periods=OTT),
]
GARDENS = [
    dict(name="Vineyards beyond the wall", polygon=[(41.03000, 28.94550), (41.02000, 28.94450), (41.01300, 28.94200), (41.00600, 28.94050), (40.99950, 28.93800), (40.99600, 28.92700), (41.01000, 28.92000), (41.02500, 28.92900), (41.03100, 28.93800)], kind="vineyard", periods=["constantine-337"]),
    dict(name="Vineyards of Pera", polygon=PERA, kind="vineyard", periods=["constantine-337", "justinian-562", "komnenian-1150"]),
    dict(name="Philopation", polygon=[(41.03500, 28.91000), (41.02700, 28.91000), (41.02200, 28.91800), (41.02700, 28.92450), (41.03200, 28.92900), (41.03700, 28.92000)], kind="park", periods=THEO_BYZ),
    dict(name="Orchards of the Lycus", polygon=[(41.01850, 28.92400), (41.02200, 28.92900), (41.01950, 28.93300), (41.01500, 28.93200)], kind="orchard", periods=["palaiologan-1453"]),
    dict(name="Vlanga gardens", polygon=[(41.00650, 28.94800), (41.00650, 28.95300), (41.00250, 28.95300), (41.00150, 28.94900)], kind="orchard", periods=["palaiologan-1453", "suleyman-1560"]),
    dict(name="Çukurbostan", polygon=[(41.02700, 28.94650), (41.02700, 28.94950), (41.02540, 28.94950), (41.02540, 28.94650)], kind="orchard", periods=["palaiologan-1453", "suleyman-1560"]),
    dict(name="Palace gardens (Gülhane)", polygon=[(41.01700, 28.98250), (41.01580, 28.98620), (41.01380, 28.98760), (41.01000, 28.98780), (41.00900, 28.98600), (41.01180, 28.98480), (41.01350, 28.98250)], kind="park", periods=OTT),
    dict(name="Vineyards outside the walls", polygon=[(41.03600, 28.91000), (41.02800, 28.91200), (41.02100, 28.91400), (41.01400, 28.91100), (41.00600, 28.91000), (41.00000, 28.91200), (40.99800, 28.91000), (41.00500, 28.90900), (41.02000, 28.90900), (41.03500, 28.90900)], kind="vineyard", periods=OTT),
]
MARSH = [
    dict(name="Silted harbour of Theodosius", polygon=[(41.00130, 28.95020), (41.00500, 28.94950), (41.00550, 28.95150), (41.00150, 28.95250)], periods=["komnenian-1150"]),
]
DISTRICTS = [
    dict(id="augusteion", name="Augusteion", polygon=[(41.00870, 28.97780), (41.00860, 28.97950), (41.00740, 28.97920), (41.00740, 28.97780)], periods=BYZ,
         description="The ceremonial square between Hagia Sophia, the Senate house and the Chalke gate of the palace, with Justinian's bronze equestrian statue on a column from 543."),
    dict(id="venetian-quarter", name="Venetian quarter", periods=LATE,
         polygon=[(41.01850, 28.96900), (41.01790, 28.97420), (41.01600, 28.97420), (41.01650, 28.96900)],
         description="Granted by Alexios I in 1082 for Venetian help against the Normans: quays, warehouses, a bakery, churches and houses between the Gate of the Drungarios and the Perama. Arrested en masse in 1171; restored and kept until 1453."),
    dict(id="pisan-quarter", name="Pisan and Genoese quarters", periods=["komnenian-1150"],
         polygon=[(41.01790, 28.97420), (41.01720, 28.98000), (41.01560, 28.98000), (41.01600, 28.97420)],
         description="East of the Venetians toward the Neorion and Prosphorion: the Pisan embolos (from 1111) and, after 1155, a Genoese landing stage. Both quarters were sacked in the massacre of the Latins of 1182."),
    dict(id="blachernae-quarter", name="Blachernae", periods=LATE,
         polygon=[(41.04150, 28.94420), (41.03700, 28.94800), (41.03350, 28.94550), (41.03380, 28.94050), (41.03720, 28.94220)],
         description="The north-west corner round the church of the Virgin of Blachernae and its holy spring; from Alexios I the main residence of the emperors."),
    dict(id="genoese-galata", name="Genoese Galata", periods=["palaiologan-1453"],
         polygon=GALATA_IN,
         description="Granted to Genoa by Michael VIII in 1267 and walled from 1304: a self-governing colony under a podestà, with its own churches, loggia and arsenal, trading in Black Sea grain, slaves and alum."),
    dict(id="topkapi-district", name="Saray-ı Cedid", periods=OTT,
         polygon=ACROPOLIS,
         description="Mehmed II's 'New Palace' on the old acropolis, walled off from the city by the Sur-ı Sultani, with gardens running down to the point."),
    dict(id="balat-jewish", name="Balat", periods=OTT,
         polygon=[(41.04150, 28.94450), (41.03700, 28.94880), (41.03400, 28.94700), (41.03700, 28.94300)],
         description="Jewish quarter by the Golden Horn, home to Romaniote Jews and to Sephardim who came after the expulsion from Spain in 1492, with synagogues named after their towns of origin."),
]
LABELS = [
    dict(text="PROPONTIS", position=(40.99300, 28.95200), size="lg", rotation=-8, periods=BYZ),
    dict(text="MARMARA DENİZİ", position=(40.99300, 28.95200), size="lg", rotation=-8, periods=OTT),
    dict(text="BOSPOROS", position=(41.03500, 28.99450), size="md", rotation=-55, periods=BYZ),
    dict(text="BOĞAZİÇİ", position=(41.03500, 28.99450), size="md", rotation=-55, periods=OTT),
    dict(text="KERAS", position=(41.02700, 28.96050), size="md", rotation=-42, periods=BYZ),
    dict(text="HALİÇ", position=(41.02700, 28.96050), size="md", rotation=-42, periods=OTT),
    dict(text="Sykai", position=(41.02700, 28.97300), size="md", periods=EARLY),
    dict(text="Pera", position=(41.02800, 28.97500), size="md", periods=["komnenian-1150"]),
    dict(text="Galata", position=(41.02420, 28.97250), size="md", periods=GALATA),
    dict(text="Pera", position=(41.03300, 28.97900), size="sm", periods=GALATA),
    dict(text="Blachernai", position=(41.03650, 28.94050), size="sm", periods=LATE),
    dict(text="Psamathia", position=(40.99950, 28.93250), size="sm", periods=THEO_BYZ),
    dict(text="Vlanga", position=(41.00500, 28.95400), size="sm", periods=["palaiologan-1453", "suleyman-1560"]),
    dict(text="Hebdomon road", position=(40.99550, 28.91150), size="sm", periods=BYZ),
    dict(text="Kasımpaşa", position=(41.03450, 28.96650), size="sm", periods=OTT),
    dict(text="Tophane", position=(41.02850, 28.98450), size="sm", periods=OTT),
    dict(text="Philopation", position=(41.03100, 28.91600), size="sm", periods=THEO_BYZ),
]

SOURCES = [
    dict(id="wiki-constantinople", title="Constantinople", author="Wikipedia", url="https://en.wikipedia.org/wiki/Constantinople"),
    dict(id="wiki-walls", title="Walls of Constantinople", author="Wikipedia", url="https://en.wikipedia.org/wiki/Walls_of_Constantinople"),
    dict(id="wiki-golden-horn", title="Golden Horn", author="Wikipedia", url="https://en.wikipedia.org/wiki/Golden_Horn"),
    dict(id="wiki-harbour-theodosius", title="Harbour of Theodosius", author="Wikipedia", url="https://en.wikipedia.org/wiki/Harbour_of_Theodosius"),
    dict(id="wiki-mese", title="Mese (Constantinople)", author="Wikipedia", url="https://en.wikipedia.org/wiki/Mese_(Constantinople)"),
    dict(id="mango-developpement", title="Le développement urbain de Constantinople (IVe–VIIe siècles)", author="Cyril Mango", year=1985),
    dict(id="mueller-wiener", title="Bildlexikon zur Topographie Istanbuls", author="Wolfgang Müller-Wiener", year=1977),
    dict(id="janin", title="Constantinople byzantine: développement urbain et répertoire topographique", author="Raymond Janin", year=1964, note="2nd edition"),
    dict(id="magdalino", title="Constantinople médiévale: études sur l'évolution des structures urbaines", author="Paul Magdalino", year=1996),
    dict(id="van-millingen", title="Byzantine Constantinople: The Walls of the City and Adjoining Historical Sites", author="Alexander van Millingen", year=1899),
]
