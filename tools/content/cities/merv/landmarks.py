# Merv landmarks. See tools/content/cities/FORMAT.md.
ALL = ["achaemenid-500", "sasanian-500", "seljuk-1100", "ruins-1250", "timurid-1450"]
SK_ON = ["seljuk-1100", "ruins-1250", "timurid-1450"]
AFTER = ["ruins-1250", "timurid-1450"]

SOURCES = [
    dict(id="herrmann-merv", title="Monuments of Merv: Traditional Buildings of the Karakum", author="Georgina Herrmann", year=1999),
    dict(id="williams-merv", title="Ancient Merv: Queen of Cities (and the reports of the Ancient Merv Project)", author="Tim Williams et al., UCL Institute of Archaeology", year="1992–2016"),
    dict(id="hillenbrand", title="Islamic Architecture: Form, Function and Meaning", author="Robert Hillenbrand", year=1994),
    dict(id="pugachenkova", title="Puti razvitiya arkhitektury Yuzhnogo Turkmenistana pory rabovladeniya i feodalizma", author="G. A. Pugachenkova", year=1958),
    dict(id="koshelenko", title="Excavations of the Buddhist complex at Gyaur Kala (reports of the YuTAKE expedition)", author="G. A. Koshelenko et al.", year="1960s–1970s"),
    dict(id="le-strange", title="The Lands of the Eastern Caliphate", author="Guy Le Strange", year=1905),
    dict(id="istakhri", title="Kitab al-Masalik wa'l-Mamalik", author="al-Istakhri", year="c. 950", url="https://en.wikipedia.org/wiki/Istakhri"),
    dict(id="wiki-merv", title="Merv", author="Wikipedia", url="https://en.wikipedia.org/wiki/Merv"),
    dict(id="wiki-sanjar-tomb", title="Tomb of Ahmad Sanjar", author="Wikipedia", url="https://en.wikipedia.org/wiki/Tomb_of_Ahmad_Sanjar"),
    dict(id="wiki-ahmad-sanjar", title="Ahmad Sanjar", author="Wikipedia", url="https://en.wikipedia.org/wiki/Ahmad_Sanjar"),
    dict(id="wiki-great-kyz-kala", title="Great Kyz Kala", author="Wikipedia", url="https://en.wikipedia.org/wiki/Great_Kyz_Kala"),
    dict(id="wiki-kushk", title="Kushk", author="Wikipedia", url="https://en.wikipedia.org/wiki/Kushk"),
    dict(id="wiki-yakhchal", title="Yakhchāl", author="Wikipedia", url="https://en.wikipedia.org/wiki/Yakhch%C4%81l"),
    dict(id="wiki-buddhism-central-asia", title="Buddhism in Central Asia", author="Wikipedia", url="https://en.wikipedia.org/wiki/Buddhism_in_Central_Asia"),
    dict(id="wiki-margiana", title="Margiana", author="Wikipedia", url="https://en.wikipedia.org/wiki/Margiana"),
    dict(id="wiki-shah-rukh", title="Shah Rukh", author="Wikipedia", url="https://en.wikipedia.org/wiki/Shah_Rukh"),
    dict(id="wiki-seljuk-architecture", title="Great Seljuk architecture", author="Wikipedia", url="https://en.wikipedia.org/wiki/Great_Seljuk_architecture"),
    dict(id="wiki-murghab", title="Marghab River", author="Wikipedia", url="https://en.wikipedia.org/wiki/Marghab_River"),
]

LANDMARKS = [
    # ------------------------------------------------------------ the Mausoleum of Sultan Sanjar
    dict(id="sanjar-mausoleum", placeId="sanjar-mausoleum", name="Mausoleum of Sultan Sanjar", category="monument",
         latlon=(37.6643, 62.1637), rotation=0, footprint=(40, 40), scale=1.0, model="merv/sanjar-mausoleum",
         activePeriods=SK_ON,
         variants={
             "sasanian-500": dict(note="Canal-side fields and gardens west of the walled city. The Seljuk city of Sultan Kala does not yet exist."),
             "seljuk-1100": dict(note="Raised about 1157, late in this era, at the heart of Sultan Kala beside the Friday mosque: Sanjar's tomb, its outer dome said to have been visible a day's ride away."),
             "ruins-1250": dict(note="Looted by the Mongols in 1221 but left standing: the one great building still upright in the emptied city, a landmark for every traveller on the plain."),
             "timurid-1450": dict(note="A shrine among fields and ruins north of Shah Rukh's new town; its outer dome and tiles weathering, the inner dome intact."),
         },
         summary="The tomb of the last great Seljuk sultan, about 1157: a cube of fired brick 27 metres square under an arcaded gallery and a double dome rising some 38 metres.",
         details=["Sanjar (r. 1118–1157) built his tomb in the centre of his capital. A square hall of fired brick carries an octagonal zone and an open gallery of arches, and above it two domes, an inner one painted with stucco and an outer shell. An inscription in the dome names the builder, Muhammad ibn Atsiz of Sarakhs.",
                  "The miniature shows the plain lower cube with its blind niches, the gallery of arches round the upper storey, the drum and the outer dome glazed turquoise, as Yaqut and later writers describe it; the tiling is hedged, since only fragments survive. The attached mosque and palace buildings are left out."],
         built="c. 1157", function="Mausoleum of Sultan Ahmad Sanjar", confidence="documented",
         sourceIds=["wiki-sanjar-tomb", "wiki-ahmad-sanjar", "hillenbrand", "herrmann-merv"], activity=dict(figures=30, radius=120)),

    # ------------------------------------------------------------ the Friday mosque of Sultan Kala
    dict(id="friday-mosque", placeId="friday-mosque", name="Friday Mosque of Sultan Kala", category="religious",
         latlon=(37.6643, 62.1615), rotation=0, footprint=(110, 90), scale=1.0, model="merv/friday-mosque",
         activePeriods=["seljuk-1100"],
         variants={
             "sasanian-500": dict(note="Fields along the Majan canal. Abu Muslim's first mosque of the new city (748) stood somewhere nearby on the canal."),
             "seljuk-1100": dict(note="The congregational mosque of the Seljuk capital, beside Sanjar's mausoleum, with a library in its care.", confidence="interpretation"),
             "ruins-1250": dict(note="Burned and abandoned after 1221: low mounds of brick west of the standing mausoleum."),
         },
         summary="The congregational mosque of Seljuk Merv, next to Sanjar's mausoleum: a court with four iwans and a brick dome over the prayer hall, as the usual Seljuk plan suggests.",
         details=["Writers place Merv's Friday mosque on the Majan canal in the new city, and excavation found a large mosque beside Sanjar's mausoleum. Its full plan is not known. Yaqut says one of Merv's waqf libraries, with some 12,000 volumes, was kept in the Friday mosque.",
                  "The miniature follows the four-iwan court mosque of Seljuk Iran (Isfahan, Zavareh): a brick dome chamber on the qibla (west) side, iwans on the axes, arcades round the court and one minaret. It is an interpretation, not a plan of the excavated building."],
         built="11th–12th century", function="Congregational (Friday) mosque", confidence="interpretation",
         sourceIds=["wiki-merv", "le-strange", "wiki-seljuk-architecture", "williams-merv"], activity=dict(figures=50, radius=150)),

    # ------------------------------------------------------------ Shahriyar Ark
    dict(id="shahriyar-ark", placeId="shahriyar-ark", name="Shahriyar Ark", category="military",
         latlon=(37.6712, 62.1740), rotation=0, footprint=(360, 380), scale=1.0, model="merv/shahriyar-ark",
         activePeriods=SK_ON,
         variants={
             "sasanian-500": dict(note="Gardens and fields on the canals west of Gyaur Kala; no citadel here yet."),
             "seljuk-1100": dict(note="The Seljuk citadel in the north-east of Sultan Kala: the sultan's palace, the treasury and a garrison behind its own walls."),
             "ruins-1250": dict(model="merv/shahriyar-ark-ruin", name="Shahriyar Ark (ruined)", note="Stormed and burned in 1221; the palace roofs gone, the walls breached. Squatters camp in its courts."),
             "timurid-1450": dict(model="merv/shahriyar-ark-ruin", name="Shahriyar Ark (ruined)", note="An empty walled mound north of the new town, mined for brick."),
         },
         summary="The walled citadel of Seljuk Merv, about 12 hectares in the north-east corner of Sultan Kala, with the palace of the sultans, a pavilion-keep and the curious Kepter Khana.",
         details=["Built in the 11th century and enlarged under Sanjar, the Ark had its own walls with closely set towers. Excavated buildings include a palace of four iwans round a court and the Kepter Khana, a building lined with rows of small niches, explained as a dovecote, a library or a strong-room.",
                  "The miniature shows the walls, a gate, the palace court and a tall keep with corrugated walls in the manner of the koshks: that keep, the inner buildings and their arrangement are a reconstruction. The ruined variant follows the mounds seen today."],
         built="11th–12th century", function="Citadel and palace of the Seljuk sultans", confidence="reconstruction",
         sourceIds=["wiki-merv", "williams-merv", "herrmann-merv"], activity=dict(figures=40, radius=250)),

    # ------------------------------------------------------------ the walls of Sultan Kala
    dict(id="sultan-kala-walls", placeId="sultan-kala-walls", name="Walls of Sultan Kala (south gate)", category="military",
         latlon=(37.6519, 62.1640), rotation=0, footprint=(300, 90), scale=1.0, model="merv/sultan-kala-walls",
         activePeriods=SK_ON,
         variants={
             "sasanian-500": dict(note="Open country on the Herat road; the canals and fields of the western oasis."),
             "seljuk-1100": dict(note="Begun under Malik Shah about 1080 and strengthened by Sanjar: a high wall with towers every few dozen metres, an outer wall, a ditch and a fortified south gate on the Herat road."),
             "ruins-1250": dict(model="merv/sultan-kala-walls-ruin", name="Walls of Sultan Kala (breached)", note="Breached in 1221 and left to the weather: towers slumped into cones, the gate a gap between mounds."),
             "timurid-1450": dict(model="merv/sultan-kala-walls-ruin", name="Walls of Sultan Kala (ruined)", note="Still a tall earthen ridge round fields and ruins; the road from the new town runs through the old gate gap."),
         },
         summary="The massive mud-brick walls of the Seljuk city, with half-round towers set close together, an outer wall and a ditch: here the south gate where the Herat road came in.",
         details=["The Seljuk walls of Sultan Kala ran for several kilometres. Excavation shows a main wall of mud brick and pakhsa on a sloping base, with an inner gallery and arrow-slits, towers at short intervals, a lower outer wall in front and a ditch. The walls were rebuilt several times in the 12th century.",
                  "The miniature shows a 300-metre stretch: ditch, outer wall, glacis and main wall with towers about 15 metres apart, and a gate between two big towers. Heights and the gate plan are reconstructed; the ruined variant shows the ridges that still stand."],
         built="c. 1080 and 12th century", function="City walls and gate", confidence="documented",
         sourceIds=["wiki-merv", "williams-merv", "herrmann-merv"], activity=dict(figures=25, radius=200)),

    # ------------------------------------------------------------ Gyaur Kala walls
    dict(id="gyaur-kala-walls", placeId="gyaur-kala-walls", name="Walls of Gyaur Kala (south gate)", category="military",
         latlon=(37.6544, 62.1930), rotation=0, footprint=(240, 70), scale=1.0, model="merv/gyaur-kala-walls",
         activePeriods=["sasanian-500", "seljuk-1100", "ruins-1250", "timurid-1450"],
         variants={
             "achaemenid-500": dict(note="Fields and the road south from Erk Kala. The square city will be laid out here in Hellenistic times."),
             "sasanian-500": dict(name="Walls of Antiochia Margiana", note="The square city's walls, raised in Hellenistic times and thickened by Parthians and Sasanians, with closely set towers and a gallery for archers."),
             "seljuk-1100": dict(name="Walls of the shahristan", note="Still standing round the half-emptied old city, now east of the busy new one."),
             "ruins-1250": dict(model="merv/gyaur-kala-walls-ruin", name="Ruined walls of Gyaur Kala", note="Long abandoned walls slumped into ridges, their towers worn round."),
             "timurid-1450": dict(model="merv/gyaur-kala-walls-ruin", name="Ruined walls of Gyaur Kala", note="Earthen ridges among fields north of Shah Rukh's town."),
         },
         summary="The walls of Gyaur Kala, the square Hellenistic city of Antiochia Margiana, nearly two kilometres a side, rebuilt over a thousand years; here the south gate.",
         details=["Antiochus I's square city (about 280 BCE) took in Erk Kala as its citadel. Its walls were thickened again and again until they formed a rampart many metres thick, with towers at close intervals and, in Sasanian times, a vaulted gallery for archers inside. A gate in the middle of each side led to the two main streets.",
                  "The miniature shows a 240-metre stretch of mud-brick wall on a sloping base, with towers, arrow-slits and a gate flanked by two towers. Details of the gate are reconstructed."],
         built="c. 280 BCE, rebuilt to the 6th century CE", function="City walls", confidence="documented",
         sourceIds=["wiki-merv", "williams-merv", "wiki-margiana"], activity=dict(figures=20, radius=180)),

    # ------------------------------------------------------------ Beni Makhan mosque
    dict(id="beni-makhan", placeId="beni-makhan", name="Beni Makhan Mosque", category="religious",
         latlon=(37.6618, 62.1915), rotation=0, footprint=(70, 60), scale=1.0, model="merv/beni-makhan",
         activePeriods=["seljuk-1100"],
         variants={
             "sasanian-500": dict(note="Houses at the crossing of the two main streets of Gyaur Kala; Islam has not yet reached Merv."),
             "seljuk-1100": dict(note="An old mosque in the half-empty shahristan, still used by the potters and craftsmen who stayed in the old city.", confidence="reconstruction"),
             "ruins-1250": dict(note="Abandoned; its cistern and walls survive as low mounds near the centre of Gyaur Kala."),
         },
         summary="An early mosque at the centre of Gyaur Kala, traditionally linked with the Arab settlers of the 8th century, with a large cistern beside it.",
         details=["Excavation in the centre of the old city uncovered a mosque and a big domed cistern. Its name is linked with an Arab tribal group (the Banu Mahan); its date is uncertain, usually put in the 8th century and later rebuilt.",
                  "The miniature shows a modest court mosque: a flat-roofed prayer hall of piers on the qibla side, an arcaded court, a square minaret and a domed cistern. The plan is a reconstruction."],
         built="8th century? (rebuilt)", function="Mosque", confidence="reconstruction",
         sourceIds=["wiki-merv", "williams-merv"], activity=dict(figures=15, radius=100)),

    # ------------------------------------------------------------ the Buddhist stupa
    dict(id="stupa", placeId="gyaur-kala-stupa", name="Buddhist stupa and monastery", category="religious",
         latlon=(37.6560, 62.2010), rotation=0, footprint=(90, 90), scale=1.0, model="merv/stupa",
         activePeriods=["sasanian-500"],
         variants={
             "achaemenid-500": dict(note="Fields south of the citadel; Buddhism reaches Merv only centuries later."),
             "sasanian-500": dict(note="A stupa of mud brick on a square base with a monastery of cells beside it, the westernmost Buddhist foundation known in Central Asia."),
             "seljuk-1100": dict(note="Long gone: a low mound in a deserted corner of the old city."),
         },
         summary="The westernmost Buddhist sanctuary excavated in Central Asia: a mud-brick stupa and a monastery round a court in the south-east corner of Gyaur Kala, in use about the 4th–6th centuries.",
         details=["Soviet excavators found the stupa, a monastery of cells round a court and a sanctuary with a large clay Buddha head. In the stupa lay a vase holding Buddhist texts in Sanskrit on birch bark. It shows Buddhists living in Sasanian Merv beside Zoroastrians and Christians.",
                  "The miniature shows a square stepped base, a dome (anda) with a harmika and parasols, and the monastery's ring of cells. Its height and the finish of the dome are reconstructed."],
         built="c. 4th–5th century", function="Stupa and monastery", confidence="reconstruction",
         sourceIds=["wiki-merv", "wiki-buddhism-central-asia", "koshelenko"], activity=dict(figures=12, radius=90)),

    # ------------------------------------------------------------ Erk Kala
    dict(id="erk-kala", placeId="erk-kala", name="Erk Kala", category="military",
         latlon=(37.6712, 62.1928), rotation=0, footprint=(520, 520), scale=1.0, model="merv/erk-kala",
         activePeriods=["achaemenid-500", "sasanian-500", "seljuk-1100", "ruins-1250", "timurid-1450"],
         variants={
             "achaemenid-500": dict(name="Erk Kala, citadel of Margu", note="The round fortress of the satrapy of Margiana: a high mud-brick wall on its rampart, the governor's hall, granaries and houses."),
             "sasanian-500": dict(name="Erk Kala, citadel of Marw", note="Now the citadel on the north side of Gyaur Kala, seat of the marzban, the Sasanian governor of the frontier."),
             "seljuk-1100": dict(model="merv/erk-kala-ruin", name="Erk Kala (abandoned)", note="The government has moved to the Shahriyar Ark; the old citadel is a high, empty ring of ramparts."),
             "ruins-1250": dict(model="merv/erk-kala-ruin", name="Erk Kala (ruins)", note="A ring of eroded earth over the deserted old city."),
             "timurid-1450": dict(model="merv/erk-kala-ruin", name="Erk Kala (ruins)", note="A grass-grown ring of ramparts, used as a lookout by herders."),
         },
         summary="The oldest of Merv's cities: a round citadel of about 20 hectares on a high rampart, founded in the Achaemenid period and later the citadel of Gyaur Kala.",
         details=["Erk Kala was probably built in the 6th century BCE as the fortress of Margu, the Achaemenid province named at Behistun. Its walls were raised again and again on their own ruins until the ramparts rose about 30 metres above the plain. The Sasanian governors still ruled from it.",
                  "The miniature shows the ring wall on its rampart with towers, a gate, the governor's hall, granaries and houses inside. The buildings inside are a reconstruction; the ruined variant is the ring of ramparts that survives."],
         built="6th century BCE, rebuilt to the 7th century CE", function="Citadel", confidence="reconstruction",
         sourceIds=["wiki-merv", "wiki-margiana", "williams-merv"], activity=dict(figures=25, radius=300)),

    # ------------------------------------------------------------ the Kyz Kalas
    dict(id="great-kyz-kala", placeId="great-kyz-kala", name="Great Kyz Kala", category="monument",
         latlon=(37.6551, 62.1526), rotation=0, footprint=(52, 58), scale=1.0, model="merv/great-kyz-kala",
         activePeriods=SK_ON,
         variants={
             "sasanian-500": dict(note="Probably not yet built: dates proposed for the Kyz Kalas run from the 6th to the 9th century."),
             "seljuk-1100": dict(note="An old koshk outside the west wall of the Seljuk city, perhaps still lived in by a landowning family."),
             "ruins-1250": dict(note="Abandoned; its upper floor and roof timbers gone, the corrugated walls still standing."),
             "timurid-1450": dict(note="Already an old ruin with a legend: the 'Maidens' Castle'."),
         },
         summary="The 'Great Maidens' Castle': a fortified two-storey manor (koshk) of mud brick about 42 by 37 metres, its walls ribbed with tall half-round corrugations.",
         details=["The Great Kyz Kala stands on a high sloping plinth. Its outer walls are formed by closely packed half-columns of mud brick, which strengthened the walls and gave them their striking corrugated look. Inside, two storeys of rooms surround a small court. Its date is debated: proposals run from the 6th to the 9th century.",
                  "The miniature shows the plinth, the corrugated walls, a ramp to the door and the court. The upper parapet is reconstructed."],
         built="7th–8th century? (debated)", function="Fortified manor (koshk)", confidence="documented",
         sourceIds=["wiki-great-kyz-kala", "wiki-kushk", "herrmann-merv"], activity=dict(figures=8, radius=80)),
    dict(id="small-kyz-kala", placeId="small-kyz-kala", name="Small Kyz Kala", category="monument",
         latlon=(37.6566, 62.1543), rotation=0, footprint=(30, 28), scale=1.0, model="merv/small-kyz-kala",
         activePeriods=SK_ON,
         variants={
             "sasanian-500": dict(note="Probably not yet built; the estates of dihqans dot the oasis."),
             "seljuk-1100": dict(note="The smaller koshk beside the Great Kyz Kala, close to the Hurmuzfarra canal."),
             "ruins-1250": dict(note="Abandoned and roofless."),
             "timurid-1450": dict(note="A crumbling ruin beside its larger neighbour."),
         },
         summary="The smaller of the two 'Maidens' Castles', a corrugated-walled koshk near the Great Kyz Kala.",
         details=["Built in the same way as its larger neighbour, with corrugated mud-brick walls on a plinth and rooms round a central space, but much smaller. Koshks like these were the fortified homes of landowners throughout the oasis.",
                  "The miniature uses the same corrugated-wall technique on a smaller body; its height is approximate."],
         built="7th–8th century? (debated)", function="Fortified manor (koshk)", confidence="documented",
         sourceIds=["wiki-great-kyz-kala", "wiki-merv", "herrmann-merv"], activity=dict(figures=5, radius=60)),

    # ------------------------------------------------------------ Muhammad ibn Zayd
    dict(id="muhammad-ibn-zayd", placeId="muhammad-ibn-zayd", name="Mausoleum of Muhammad ibn Zayd", category="religious",
         latlon=(37.6800, 62.1640), rotation=0, footprint=(24, 30), scale=1.3, model="merv/muhammad-ibn-zayd",
         activePeriods=SK_ON,
         variants={
             "sasanian-500": dict(note="Fields north of the later walls."),
             "seljuk-1100": dict(note="Newly built in 1112–1113 over the grave of an Alid saint, north of the city walls; a place of pilgrimage."),
             "ruins-1250": dict(note="Spared, or soon repaired: a shrine with a keeper amid the abandoned northern suburbs."),
             "timurid-1450": dict(note="Still a shrine, later remodelled with a new entrance."),
         },
         summary="A small Seljuk mausoleum of fired brick dated by its inscription to 1112–1113, over the grave of a descendant of the Prophet called Muhammad ibn Zayd.",
         details=["A square domed chamber with a deep entrance, built of fine fired brick; a band of Kufic inscription in carved brick gives the date. Which Muhammad ibn Zayd lies here is unclear; the shrine has been venerated ever since.",
                  "The miniature shows the square chamber, the dome on its octagonal zone and the inscription band. Later additions are left out."],
         built="1112–1113", function="Shrine and mausoleum", confidence="documented",
         sourceIds=["wiki-merv", "herrmann-merv", "pugachenkova"], activity=dict(figures=8, radius=60)),

    # ------------------------------------------------------------ ice house
    dict(id="yakhdan", placeId="yakhdan", name="Ice house (yakhdan)", category="civic",
         latlon=(37.6500, 62.1540), rotation=0, footprint=(60, 44), scale=1.0, model="merv/yakhdan",
         activePeriods=SK_ON,
         variants={
             "sasanian-500": dict(note="Fields by the Hurmuzfarra canal."),
             "seljuk-1100": dict(note="One of several ice houses round the city, storing winter ice for the summer drinks of the rich.", confidence="interpretation"),
             "ruins-1250": dict(note="Derelict: the shade wall slumping, the ice pit full of sand."),
             "timurid-1450": dict(note="In use again as the canals run once more.", confidence="interpretation"),
         },
         summary="A conical domed ice house of mud brick: water from the canal froze in shallow pools on winter nights, shaded by a high wall, and the ice was stacked in a deep pit under the dome.",
         details=["Several ice houses survive round Merv, with steep stepped domes of mud brick over pits several metres deep. Their dates are hard to fix and some may be quite late; ice houses of this kind were used across Iran and Central Asia for centuries.",
                  "The miniature shows the conical dome, its door, the freezing pools and the long shade wall to the south of them. The pairing with this era is an interpretation."],
         built="date uncertain", function="Ice store", confidence="interpretation",
         sourceIds=["wiki-yakhchal", "herrmann-merv", "wiki-merv"], activity=dict(figures=6, radius=60)),

    # ------------------------------------------------------------ the Askhab
    dict(id="askhab", placeId="askhab", name="Askhab Mausolea", category="religious",
         latlon=(37.6480, 62.1625), rotation=0, footprint=(60, 44), scale=1.0, model="merv/askhab",
         activePeriods=["timurid-1450"],
         variants={
             "ruins-1250": dict(note="Two graves of Companions of the Prophet, visited by pilgrims among the ruins; no great buildings yet."),
             "timurid-1450": dict(note="Two tall Timurid iwans now stand behind the graves of al-Hakam and Buraydah, and a small mosque serves the pilgrims."),
         },
         summary="The graves of two Companions of the Prophet who died at Merv, al-Hakam ibn Amr al-Ghifari and Buraydah ibn al-Husayb, framed by two Timurid iwans.",
         details=["The two Companions came with the Arab armies and died at Merv in the 7th century. In the 15th century two great brick portals (iwans) were built behind their tombs, which stand in the open before them.",
                  "The miniature shows the twin iwans with tiled frames and the two raised tombs on a paved terrace. The tile colours are simplified."],
         built="graves 7th century; iwans 15th century", function="Shrine", confidence="documented",
         sourceIds=["wiki-merv", "herrmann-merv"], activity=dict(figures=15, radius=80)),

    # ------------------------------------------------------------ Abdullah Khan Kala
    dict(id="abdullah-khan-kala", placeId="abdullah-khan-kala", name="Walls of Abdullah Khan Kala (north gate)", category="military",
         latlon=(37.6473, 62.1736), rotation=180, footprint=(200, 60), scale=1.0, model="merv/abdullah-khan-kala",
         activePeriods=["timurid-1450"],
         variants={
             "ruins-1250": dict(note="Open, half-abandoned fields south of the ruined Seljuk city."),
             "timurid-1450": dict(note="The new walls of Shah Rukh's town, fresh mud brick on a pakhsa base, with a gate facing the old cities to the north."),
         },
         summary="The walls of the Timurid town founded south of the old cities, by the usual account in 1409, later named after the 16th-century Uzbek khan Abdullah.",
         details=["Shah Rukh, ruling from Herat, had the Murghab dam rebuilt and a new town laid out. Its walls enclose a rough square of some 600 metres with towers and gates; a citadel stood in one corner. In the 18th century Bairam Ali Khan Kala was added beside it.",
                  "The miniature shows a stretch of wall with round towers and a gate with a pointed arch. The date of 1409 and the gate design are hedged."],
         built="c. 1409", function="Town walls", confidence="reconstruction",
         sourceIds=["wiki-merv", "wiki-shah-rukh", "williams-merv"], activity=dict(figures=20, radius=150)),

    # ------------------------------------------------------------ Majan dam
    dict(id="majan-dam", placeId="majan-dam", name="Weir of the Majan canal", category="civic",
         latlon=(37.6400, 62.1669), rotation=0, footprint=(70, 40), scale=1.0, model="merv/majan-dam",
         activePeriods=["seljuk-1100", "timurid-1450"],
         variants={
             "sasanian-500": dict(note="An earlier timber and brushwood weir regulated the canal here."),
             "seljuk-1100": dict(note="A brick weir with sluices where the mir-ab's men measured the city's share of water.", confidence="interpretation"),
             "ruins-1250": dict(note="Broken: the canals silt up and the oasis shrinks."),
             "timurid-1450": dict(note="Rebuilt as part of Shah Rukh's restoration of the irrigation.", confidence="interpretation"),
         },
         summary="A brick weir and sluices on the Majan canal south of the city, standing for the water works that made Merv possible.",
         details=["All of Merv lived on the Murghab's water, divided by dams and weirs into the four canals. Istakhri says the official in charge of water had some 10,000 workers, more than the governor. Where exactly the Majan's sluices stood is not known.",
                  "The miniature shows a brick weir across the canal with sluice gates, a gatekeeper's hut and stores of brushwood. It is an interpretation built from descriptions of water control, not a known structure."],
         built="unknown", function="Weir and sluices", confidence="interpretation",
         sourceIds=["istakhri", "le-strange", "wiki-murghab"], activity=dict(figures=12, radius=80)),
]
