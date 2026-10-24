# Carthage: monuments. Positions (lat, lon); footprints in metres (w east-west, d north-south before rotation).
# Buildings on the Roman street grid are turned with it (rotation 30: the model's x axis runs along the
# decumani toward the sea, its y axis along the cardines). UV() is the grid of geo.py.
import math

P400 = ["punic-400"]
P150 = ["punic-150"]
PUNIC = ["punic-400", "punic-150"]
ROM_LATE = ["roman-200", "vandal-480"]
RUINS = ["ruins-1600"]
LATER = ["punic-150", "roman-200", "vandal-480", "ruins-1600"]
ALL = PUNIC + ROM_LATE + RUINS

P0 = (36.8528, 10.3237)
KX, KY = 111320.0 * math.cos(math.radians(36.853)), 110950.0


def UV(u, v):
    """(lat, lon) of a point u m along the decumani (east-south-east) and v m along the cardines (north-north-east) from the Byrsa summit."""
    e = 0.8660254 * u + 0.5 * v
    n = -0.5 * u + 0.8660254 * v
    return (round(P0[0] + n / KY, 5), round(P0[1] + e / KX, 5))


SOURCES = [
    dict(id="wiki-byrsa", title="Byrsa", author="Wikipedia", url="https://en.wikipedia.org/wiki/Byrsa"),
    dict(id="wiki-eshmun", title="Eshmun", author="Wikipedia", url="https://en.wikipedia.org/wiki/Eshmun"),
    dict(id="wiki-punic-ports", title="Carthage Punic Ports", author="Wikipedia", url="https://en.wikipedia.org/wiki/Carthage_Punic_Ports"),
    dict(id="wiki-cothon", title="Cothon", author="Wikipedia", url="https://en.wikipedia.org/wiki/Cothon"),
    dict(id="wiki-tophet", title="Carthage tophet", author="Wikipedia", url="https://en.wikipedia.org/wiki/Carthage_tophet"),
    dict(id="wiki-tophet-general", title="Tophet", author="Wikipedia", url="https://en.wikipedia.org/wiki/Tophet"),
    dict(id="wiki-antonine-baths", title="Baths of Antoninus", author="Wikipedia", url="https://en.wikipedia.org/wiki/Baths_of_Antoninus"),
    dict(id="wiki-amphitheatre", title="Carthage amphitheatre", author="Wikipedia", url="https://en.wikipedia.org/wiki/Carthage_amphitheatre"),
    dict(id="wiki-circus", title="Circus of Carthage", author="Wikipedia", url="https://en.wikipedia.org/wiki/Circus_of_Carthage"),
    dict(id="wiki-la-malga", title="Cisterns of La Malga", author="Wikipedia", url="https://en.wikipedia.org/wiki/Cisterns_of_La_Malga"),
    dict(id="wiki-zaghouan", title="Zaghouan Aqueduct", author="Wikipedia", url="https://en.wikipedia.org/wiki/Zaghouan_Aqueduct"),
    dict(id="wiki-damous", title="Basilica of Damous El Karita", author="Wikipedia", url="https://en.wikipedia.org/wiki/Basilica_of_Damous_El_Karita"),
    dict(id="wiki-roman-carthage", title="Roman Carthage", author="Wikipedia", url="https://en.wikipedia.org/wiki/Roman_Carthage"),
    dict(id="wiki-archaeological-site", title="Archaeological site of Carthage", author="Wikipedia", url="https://en.wikipedia.org/wiki/Archaeological_site_of_Carthage"),
    dict(id="wiki-acropolium", title="Acropolium of Carthage", author="Wikipedia", url="https://en.wikipedia.org/wiki/Acropolium_of_Carthage"),
    dict(id="wiki-sidi-bou-said", title="Sidi Bou Said", author="Wikipedia", url="https://en.wikipedia.org/wiki/Sidi_Bou_Said"),
    dict(id="wiki-punic-architecture", title="Punic architecture", author="Wikipedia", url="https://en.wikipedia.org/wiki/Punic_architecture"),
    dict(id="appian", title="Roman History, Book 8: The Punic Wars (Punica) 95–135", author="Appian", year="2nd century CE", url="https://en.wikipedia.org/wiki/Appian"),
    dict(id="victor-vita", title="History of the Vandal Persecution 1.8", author="Victor of Vita", year="c. 489", url="https://en.wikipedia.org/wiki/Victor_of_Vita"),
    dict(id="al-bakri", title="Book of Roads and Kingdoms (description of Carthage)", author="al-Bakri", year="1068", url="https://en.wikipedia.org/wiki/Abu_Abdullah_al-Bakri"),
    dict(id="apuleius-florida", title="Florida 18 and 20 (speeches in the theatre of Carthage)", author="Apuleius", year="2nd century CE", url="https://en.wikipedia.org/wiki/Apuleius"),
    dict(id="lancel", title="Carthage: A History", author="Serge Lancel", year=1995),
    dict(id="lancel-byrsa", title="Byrsa I–II: Mission archéologique française à Carthage", author="Serge Lancel (ed.)", year="1979–1982"),
    dict(id="hurst", title="The Sanctuary of Tanit at Carthage in the Roman Period; Excavations at Carthage: The British Mission II (the circular harbour)", author="Henry Hurst", year="1994–1999"),
    dict(id="hurst-ports", title="Excavations at Carthage 1974–1977: the Punic and Roman harbours (Antiquaries Journal)", author="Henry Hurst", year="1975–1979"),
    dict(id="stager", title="Child Sacrifice at Carthage: Religious Rite or Population Control? (Biblical Archaeology Review 10.1)", author="Lawrence Stager and Samuel Wolff", year=1984),
    dict(id="schwartz", title="Skeletal Remains from Punic Carthage Do Not Support Systematic Sacrifice of Infants (PLoS ONE 5)", author="Jeffrey Schwartz et al.", year=2010),
    dict(id="smith", title="Age estimations attest to infant sacrifice at the Carthage Tophet (Antiquity 87)", author="Patricia Smith et al.", year=2013),
    dict(id="rakob", title="Karthago I–III: Die deutschen Ausgrabungen in Karthago", author="Friedrich Rakob (ed.)", year="1991–1999"),
    dict(id="humphrey", title="Roman Circuses: Arenas for Chariot Racing", author="John H. Humphrey", year=1986),
    dict(id="lezine", title="Les thermes d'Antonin à Carthage", author="Alexandre Lézine", year=1969),
    dict(id="ennabli", title="Pour sauver Carthage: exploration et conservation de la cité punique, romaine et byzantine", author="Abdelmajid Ennabli (ed.)", year=1992),
    dict(id="ennabli-lb", title="Carthage chrétienne / Les basiliques chrétiennes de Carthage", author="Liliane Ennabli", year=1997),
    dict(id="bullo", title="Le Damous el-Karita / Roman villas of Carthage (Parc des villas romaines)", author="Institut National du Patrimoine (Tunisia)", year="various"),
    dict(id="delattre", title="Les tombeaux puniques de Carthage (the necropolis of Juno hill and Douimès)", author="Alfred-Louis Delattre", year="1890–1905"),
]

LANDMARKS = [
    # ---------------------------------------------------------------- heroes
    dict(id="byrsa", placeId="byrsa-summit", name="Byrsa citadel and temple of Eshmun", category="temple",
         latlon=UV(0, 0), rotation=30, footprint=(230, 170), scale=1.0, model="carthage/byrsa",
         activePeriods=ALL,
         variants={
             "punic-400": dict(note="The citadel on its hill, walled, with the temple of Eshmun, the god of healing whom the Greeks called Asclepius, on the summit. The slopes below still hold old tombs and metal workshops."),
             "punic-150": dict(note="Appian's 'richest of temples', reached by a stair of sixty steps. In 146 BCE 900 Roman deserters made their last stand in it and burned it over their own heads."),
             "roman-200": dict(model="carthage/byrsa-forum", name="Forum and Capitol on the Byrsa", confidence="reconstruction",
                               note="Augustus' engineers cut the summit down and walled the slopes to make a terrace of about 3 ha: the forum of the colony, with porticoes, the great judicial basilica and a temple, probably the Capitolium."),
             "vandal-480": dict(model="carthage/byrsa-forum", name="Forum and palace on the Byrsa", confidence="interpretation",
                                note="The proconsul's palace here becomes the palace of the Vandal kings after 439. Belisarius sits down in it in 533 to the dinner cooked for King Gelimer (Procopius)."),
             "ruins-1600": dict(model="carthage/byrsa-ruins", name="The hill of Byrsa", confidence="interpretation",
                                note="A bare hill of ruins and fallen columns, quarried for Tunis. Tradition places here the death of Louis IX, who died of dysentery in his crusading camp in August 1270."),
         },
         summary="The citadel hill at the heart of Carthage, crowned by the temple of Eshmun; after 146 BCE levelled by the Romans for the forum of their colony.",
         details=["The Byrsa held the oldest settlement and later the citadel and the city's richest temple, that of Eshmun. Nothing Punic survives on the summit: in about 29 BCE Augustus' builders shaved off the hilltop and dumped the spoil on the slopes, burying the Punic houses below, to carry a terrace for the forum.",
                  "The Punic miniature is an interpretation: a walled hilltop with the temple on a high podium, an Egyptian-style cavetto cornice as on Punic stelae and naiskoi, and the stair of sixty steps from Appian. The temple's real plan and size are unknown."],
         built="citadel from the 8th century BCE; Roman terrace c. 29 BCE", function="Citadel and sanctuary; later the forum", confidence="interpretation",
         sourceIds=["wiki-byrsa", "wiki-eshmun", "appian", "lancel", "lancel-byrsa", "wiki-acropolium"], activity=dict(figures=40, radius=220)),

    dict(id="cothon", placeId="admiralty-island", name="Circular naval harbour (Cothon)", category="military",
         latlon=UV(457, -594), rotation=30, footprint=(330, 330), scale=1.0, model="carthage/cothon",
         activePeriods=LATER,
         variants={
             "punic-400": dict(note="Not yet dug in this form: its excavator dates the round harbour to the 2nd century BCE, though some put it earlier. Warships were probably drawn up on slipways and beaches nearer the sea."),
             "punic-150": dict(note="The closed war harbour: ship sheds round the basin and the island, each fronted by two Ionic columns, stores above, and the admiral's tower on the island, hidden behind a double wall."),
             "roman-200": dict(model="carthage/cothon-roman", name="Circular harbour", confidence="interpretation",
                               note="Rebuilt for trade: a colonnade round the quays and, on the island, a hexagonal court with a temple or monument, perhaps a lighthouse. The grain fleet for Rome berths in both harbours."),
             "vandal-480": dict(model="carthage/cothon-roman", name="Circular harbour", confidence="interpretation",
                                note="Still in use but silting; the Vandal fleet, which raided Rome in 455, and later Byzantine ships lie here. Quays patched with reused blocks."),
             "ruins-1600": dict(model="carthage/cothon-silted", name="The round lagoon", confidence="interpretation",
                                note="A silted round pool with a low island in the middle, the shape still plain to travellers: 'the Cothon' that 18th- and 19th-century visitors identified with Appian's description."),
         },
         summary="The round naval harbour of the Punic city, about 325 m across, ringed with ship sheds round the basin and its island, where the admiral watched from his tower.",
         details=["Appian (Punica 96) describes 220 berths under porticoes of Ionic columns, with tackle stores above, round the basin and an island, where the admiral's house rose high enough to see out to sea. Henry Hurst's excavations (1970s) found the slipways and dated the harbour in this form to the 2nd century BCE.",
                  "The miniature follows Hurst's reconstruction: about 30 sheds on the island and some 135 round the rim, sloping slipways, a loft above, columns at the water's edge, the tower at the centre and the entrance from the merchant harbour to the south. Appian's 220 and the excavated total do not agree; the count is debated."],
         built="2nd century BCE (Hurst); some argue earlier", function="Naval base for the war fleet", confidence="reconstruction",
         sourceIds=["wiki-punic-ports", "wiki-cothon", "appian", "hurst", "hurst-ports", "lancel"], activity=dict(figures=36, radius=200)),

    dict(id="antonine-baths", placeId="thermes-antonin", name="Antonine Baths", category="civic",
         latlon=UV(800, 680), rotation=-60, footprint=(200, 110), scale=1.0, model="carthage/antonine-baths",
         activePeriods=ROM_LATE + RUINS,
         variants={
             "punic-150": dict(note="Before the baths: the seaside quarter of the Punic city, its houses and the sea wall on this shore."),
             "roman-200": dict(note="The largest baths in Roman Africa, built 145–162 under Antoninus Pius on a basement along the shore: the cold hall at the centre, hot rooms facing the sea, exercise courts at the sides."),
             "vandal-480": dict(note="Still working, fed from the Bordj Djedid cisterns; the Vandal nobles, Procopius says, spent their days in baths and banquets. Repairs in brick patch the vaults."),
             "ruins-1600": dict(model="carthage/antonine-baths-ruin", name="Ruins of the Antonine Baths", confidence="documented",
                                note="Only the vaulted service basement stands, half buried in sand; the halls above have fallen and their marble has gone to the lime kilns and to Tunis."),
         },
         summary="The great imperial baths on the shore of Carthage, built 145–162 CE: a symmetrical complex about 200 m long, among the largest baths of the Roman world.",
         details=["Begun under Hadrian's successor Antoninus Pius and dedicated in 162, the baths stood on a basement of vaulted service rooms at the water's edge. Above, the frigidarium's vaults rested on columns of grey granite with shafts over 12 m long, one of which has been set up again on the site. Water came from cisterns on the Bordj Djedid hill.",
                  "The miniature follows Lézine's reconstruction of the main floor: symmetrical cold halls, pools and hot rooms with domed and vaulted roofs facing the sea, palaestrae with colonnades at each end. The upper parts are a reconstruction; only the basement survives."],
         built="145–162 CE", function="Public baths", confidence="reconstruction",
         sourceIds=["wiki-antonine-baths", "lezine", "wiki-roman-carthage", "ennabli"], activity=dict(figures=40, radius=170)),

    # ---------------------------------------------------------------- Punic
    dict(id="commercial-harbour", placeId="rectangular-harbour", name="Rectangular commercial harbour", category="commercial",
         latlon=UV(679, -985), rotation=30, footprint=(300, 400), scale=1.0, model="carthage/commercial-harbour",
         activePeriods=ALL,
         variants={
             "punic-400": dict(note="The merchant harbour's long rectangular basin may date in this form only from the 2nd century; in the 4th century a broad channel dug inland here served the ships (Hurst)."),
             "punic-150": dict(note="Merchant ships at the quays, tackle and goods stacked in the stores; the entrance from the sea, about 20 m wide, closed with iron chains. In 147 BCE Scipio blocked it with a mole."),
             "roman-200": dict(note="The commercial harbour of the Roman city, with quays and warehouses for the grain and oil shipped to Rome under the annona."),
             "vandal-480": dict(note="Still in use, though silting; the Vandal and Byzantine fleets and merchant ships share it."),
             "ruins-1600": dict(model="carthage/harbour-silted", name="The long lagoon", confidence="interpretation",
                                note="A shallow pool in a marsh, choked by sand, with stone from the quays robbed; fishermen pull their boats up on its banks."),
         },
         summary="The merchant harbour, a rectangular dug basin with quays, joined to the sea by a channel and to the closed naval harbour behind it.",
         details=["Appian says the two harbours shared one entrance from the sea, 70 feet wide, closed with iron chains, and that a double wall hid the naval harbour from the merchants. The basin, about 450 by 350 m in the usual reconstruction, survives as a lagoon at Salammbo.",
                  "The miniature shows the basin with stone quays, warehouses along the sides, moored merchant ships, and chain towers at the channel to the sea in the south-east. Its exact shape is uncertain; the modern lagoon was reshaped in the 19th century."],
         built="probably 2nd century BCE in this form; reused to the 7th century CE", function="Merchant harbour", confidence="reconstruction",
         sourceIds=["wiki-punic-ports", "appian", "hurst-ports", "lancel"], activity=dict(figures=30, radius=220)),

    dict(id="tophet", placeId="tophet-salammbo", name="Tophet of Salammbo", category="religious",
         latlon=UV(440, -1110), rotation=30, footprint=(70, 90), scale=1.0, model="carthage/tophet",
         activePeriods=PUNIC,
         variants={
             "punic-400": dict(note="Urns of burnt bones of infants and young animals buried under stone markers and stelae carved with the sign of Tanit, vowed to Baal Hammon and Tanit."),
             "punic-150": dict(note="Stager estimated that some 20,000 urns were laid here between 400 and 200 BCE; the stelae are mostly thin pointed slabs of limestone carved with the sign of Tanit, a hand or a palm tree."),
             "roman-200": dict(note="Buried under Roman vaulted buildings; the rite has ended, though Baal Hammon lives on as Saturn, worshipped across Roman Africa."),
         },
         summary="The open-air sanctuary of Baal Hammon and Tanit, where urns of the cremated bones of infants and young animals were buried under stelae from the 8th century to 146 BCE.",
         details=["Greek and Roman writers and the Bible say the Phoenicians sacrificed children; the Tophet's inscriptions record vows (molk) fulfilled. Whether the infants were sacrificed, or were children who died young and were buried here, is still debated: two osteological studies of the same urns (Schwartz 2010, Smith 2013) reached opposite conclusions.",
                  "The miniature shows the precinct as excavated from 1921 onward: low walls, terraces of stelae and urns at several levels, the pointed and pedimented stelae of the later centuries and a small shrine. Its full size is unknown."],
         built="8th century BCE to 146 BCE", function="Sanctuary of Baal Hammon and Tanit", confidence="reconstruction",
         sourceIds=["wiki-tophet", "wiki-tophet-general", "stager", "schwartz", "smith", "lancel"], activity=dict(figures=10, radius=70)),

    dict(id="sea-wall", placeId="magon-quarter", name="Punic sea wall and sea gate", category="military",
         latlon=(36.8510, 10.33321), rotation=34, footprint=(30, 240), scale=1.0, model="carthage/sea-wall",
         activePeriods=PUNIC,
         variants={
             "punic-400": dict(note="Built in the 5th century BCE of big sandstone blocks along the beach, with a monumental sea gate opening onto a street of the seaside quarter."),
             "punic-150": dict(note="Rebuilt and strengthened with towers; the houses behind are rebuilt on the same plots. In 146 BCE the Romans broke in from the harbour side, not here."),
             "roman-200": dict(note="Gone: razed in 146 BCE and later built over by the houses and streets of the Roman grid."),
         },
         summary="A stretch of the Punic city wall along the shore, with towers and a sea gate, excavated in the seaside quarter by the German mission.",
         details=["The German excavations (Rakob, 1970s–1990s) found the sea wall of the 5th century BCE about 25 m from the ancient shore, with a monumental gate, rebuilt in the 4th and 3rd centuries; houses inside were rebuilt again and again along the same streets until 146 BCE.",
                  "The miniature shows about 240 m of wall with rectangular towers on the sea side and a gate with a cavetto cornice. The height of the wall and of the towers is a reconstruction."],
         built="5th century BCE, rebuilt 4th–3rd century BCE", function="City wall", confidence="reconstruction",
         sourceIds=["rakob", "wiki-punic-architecture", "lancel", "appian"], activity=dict(figures=12, radius=140)),

    dict(id="hannibal-quarter", placeId="byrsa-south-slope", name="Hannibal quarter", category="district",
         latlon=UV(31, -251), rotation=30, footprint=(120, 80), scale=1.0, model="carthage/hannibal-quarter",
         activePeriods=P150,
         variants={
             "punic-400": dict(note="The slope still holds old tombs and, from the 5th century, workshops of metal-workers with their furnaces."),
             "punic-150": dict(note="New blocks of houses laid out early in the 2nd century, probably in Hannibal's time: courtyards, cisterns, stairs to upper floors and shops on the streets."),
             "roman-200": dict(note="Buried several metres deep under the earth the Romans pushed off the summit to build their forum terrace, which is why its walls survive to the height of a storey."),
         },
         summary="The houses on the south slope of the Byrsa built in the early 2nd century BCE, burned in 146 BCE and buried by the Roman terrace: the best-known Punic houses.",
         details=["Excavated by Serge Lancel's French mission from 1974: blocks of houses on a regular plan, divided by straight streets with steps and drains. Houses had a court, a cistern shaped like a bottle, a small bath or basin, mosaic floors of red mortar with white chips, and stairs to an upper floor.",
                  "The miniature shows three blocks of courtyard houses of two storeys with flat roofs, a stepped street and the cistern mouths in the courts. Upper storeys are reconstructed; Appian speaks of six-storey houses near here."],
         built="early 2nd century BCE", function="Houses", confidence="reconstruction",
         sourceIds=["lancel-byrsa", "lancel", "appian", "wiki-byrsa"], activity=dict(figures=18, radius=90)),

    dict(id="juno-necropolis", placeId="juno-hill", name="Necropolis of Juno hill", category="monument",
         latlon=(36.8556, 10.3270), rotation=0, footprint=(80, 60), scale=1.0, model="carthage/juno-necropolis",
         activePeriods=PUNIC,
         variants={
             "punic-400": dict(note="An old cemetery by now: shaft tombs of the 7th–6th centuries with stone chambers at the bottom; burials have moved to the coast hills of Sainte-Monique."),
             "punic-150": dict(note="The old tombs lie under the gardens and new houses creeping up the hill."),
             "roman-200": dict(note="Built over by the Roman city; a temple of Juno Caelestis was once supposed to have stood here, hence the name."),
         },
         summary="An archaic Punic cemetery on the hill north-east of the Byrsa: shafts cut into the rock with burial chambers of stone slabs at the bottom.",
         details=["Excavated by Father Delattre and others in the 1890s, the necropoleis of Juno, Douimès and the Byrsa slopes held family shaft tombs with grave goods: Egyptian amulets, Greek and Etruscan pottery, razors, masks and lamps.",
                  "The miniature shows the hillside with tomb shafts, slab covers and small stone markers. Above-ground markers of this date are poorly known; they are reconstructed."],
         built="7th–6th century BCE", function="Cemetery", confidence="interpretation",
         sourceIds=["delattre", "lancel", "wiki-archaeological-site"], activity=dict(figures=6, radius=60)),

    # ---------------------------------------------------------------- Roman
    dict(id="amphitheatre", name="Amphitheatre", category="entertainment",
         latlon=(36.8561, 10.3151), rotation=30, footprint=(120, 94), scale=1.0, model="carthage/amphitheatre",
         activePeriods=ROM_LATE + RUINS,
         variants={
             "punic-150": dict(note="Open country beyond the city, west of the Byrsa."),
             "roman-200": dict(note="Built in the 1st century CE and enlarged in the 2nd, with an arena of about 65 by 37 m. Here Perpetua and Felicity died in 203."),
             "vandal-480": dict(note="Still used for shows; hunts and animal fights outlast the gladiators, banned by Christian emperors."),
             "ruins-1600": dict(model="carthage/amphitheatre-ruin", name="Ruins of the amphitheatre", confidence="documented",
                                note="Al-Bakri in 1068 still saw tiers of arches and carvings of men and animals; by now it is quarried to the lowest storey."),
         },
         summary="The amphitheatre of Roman Carthage on the western edge of the city, where gladiators fought, beasts were hunted and the Christians Perpetua and Felicity died in 203 CE.",
         details=["An ellipse about 120 by 94 m with seats for perhaps 30,000. The geographer al-Bakri (1068) described its fifty arches to a storey and the figures carved on its walls. Robbed of nearly all its stone later, it survives as the arena with its cellars.",
                  "The miniature restores three storeys of arcades round the cavea, the arena wall and the gates on the long axis, from comparison with other amphitheatres in Africa such as El Jem."],
         built="1st–2nd century CE", function="Amphitheatre", confidence="reconstruction",
         sourceIds=["wiki-amphitheatre", "al-bakri", "wiki-roman-carthage"], activity=dict(figures=30, radius=110)),

    dict(id="theatre", name="Theatre", category="entertainment",
         latlon=UV(170, 598), rotation=30, footprint=(105, 75), scale=1.0, model="carthage/theatre",
         activePeriods=["roman-200"],
         variants={
             "punic-150": dict(note="A hillside of the Punic city, with tombs and houses."),
             "roman-200": dict(note="Built in the 2nd century CE against the hill; here Apuleius gave his speeches to the people of Carthage, packed in the tiers."),
             "vandal-480": dict(note="Destroyed: Victor of Vita says Gaiseric's men pulled down the theatre and the odeon. Its stone goes to new buildings."),
         },
         summary="The Roman theatre on the slope of the Odeon hill, of the 2nd century CE, where Apuleius lectured; restored today for the Carthage festival.",
         details=["A cavea about 104 m across set into the hillside, with a stage building richly decorated in coloured marbles. Apuleius in his Florida praises the audience and the building. Heavily robbed, it was excavated in the early 20th century and the seating rebuilt.",
                  "The miniature shows the semicircular cavea, the orchestra and the stage with a columned scaenae frons; the height of the stage front is a reconstruction."],
         built="2nd century CE", function="Theatre", confidence="reconstruction",
         sourceIds=["apuleius-florida", "victor-vita", "wiki-roman-carthage"], activity=dict(figures=26, radius=90)),

    dict(id="odeon", name="Odeon", category="entertainment",
         latlon=UV(119, 900), rotation=30, footprint=(95, 80), scale=1.0, model="carthage/odeon",
         activePeriods=["roman-200"],
         variants={
             "punic-150": dict(note="A hill of Punic tombs, later covered by houses."),
             "roman-200": dict(note="Just built, probably for the Pythian Games of the early 3rd century: a roofed theatre for music and recitals, said to be the largest in Africa."),
             "vandal-480": dict(note="Pulled down under Gaiseric, says Victor of Vita, with the theatre and the temple of Memory."),
         },
         summary="The roofed hall for music and recitals on the hill north of the theatre, built in the early 3rd century CE for the Pythian Games.",
         details=["Tertullian mentions the Pythian Games at Carthage; the odeon is thought to have been built for them around 207 CE. Its foundations cut through Punic tombs. Little more than the substructures remains.",
                  "The miniature restores a semicircular auditorium inside a rectangular walled hall with a timber roof, like the odeon of Lyon or Aphrodisias. Its roof form is uncertain."],
         built="c. 207 CE", function="Concert hall", confidence="interpretation",
         sourceIds=["victor-vita", "wiki-roman-carthage", "ennabli"], activity=dict(figures=14, radius=70)),

    dict(id="circus", name="Circus", category="entertainment",
         latlon=(36.8508, 10.3137), rotation=30, footprint=(520, 90), scale=1.0, model="carthage/circus",
         activePeriods=ROM_LATE,
         variants={
             "punic-150": dict(note="Fields and gardens on the plain toward the lake."),
             "roman-200": dict(note="One of the largest circuses outside Rome, over 500 m long. Curse tablets buried here named rival charioteers and horses and begged the demons to break them."),
             "vandal-480": dict(note="Races go on under the Vandal kings, who loved them; the Byzantine governors keep the Blues and Greens."),
             "ruins-1600": dict(note="Only a long low bank and a hollow in the fields mark the track."),
         },
         summary="The chariot-racing circus in the south-west of the Roman city, more than 500 m long: after Rome's Circus Maximus, one of the largest in the empire.",
         details=["Built probably in the 2nd century CE, it had a spina about 300 m long down the middle and seats for perhaps 60,000 or more. Dozens of lead curse tablets against charioteers and horses have been found here.",
                  "The miniature shows the stands round the arena, the starting gates (carceres) at the west end, and the spina with turning posts and an obelisk. Seating and gates follow other African circuses."],
         built="2nd century CE", function="Chariot racing", confidence="reconstruction",
         sourceIds=["wiki-circus", "humphrey", "wiki-roman-carthage"], activity=dict(figures=40, radius=260)),

    dict(id="la-malga", name="Cisterns of La Malga", category="civic",
         latlon=(36.8593, 10.3189), rotation=30, footprint=(130, 105), scale=1.0, model="carthage/la-malga",
         activePeriods=ROM_LATE + RUINS,
         variants={
             "punic-150": dict(note="Gardens of the Megara; water came from rain cisterns under every house."),
             "roman-200": dict(note="The aqueduct from the springs of Zaghouan, 132 km away, ends here in fifteen parallel vaulted tanks, each about 100 m long, from which pipes fed the city."),
             "vandal-480": dict(note="Still filled by the aqueduct; it will be cut during sieges and restored by the Byzantines."),
             "ruins-1600": dict(model="carthage/la-malga-ruin", name="La Malga", confidence="documented",
                                note="The hamlet of La Malga: families and their animals live inside the broken vaults, as 19th-century travellers still saw."),
         },
         summary="The great reservoir at the end of the Zaghouan aqueduct: fifteen parallel vaulted tanks holding perhaps 50,000 m³ of water for the Roman city.",
         details=["Built with the aqueduct under Hadrian and Antoninus Pius, in the 2nd century CE. The water ran 132 km by channel and arcade from the springs of Zaghouan and Jouggar; here it settled and was distributed. Several tanks still stand, partly roofed.",
                  "The miniature shows the row of barrel-vaulted tanks with a distribution gallery across their heads and the aqueduct arriving on arches from the west."],
         built="2nd century CE", function="Reservoir", confidence="documented",
         sourceIds=["wiki-la-malga", "wiki-zaghouan", "wiki-roman-carthage"], activity=dict(figures=8, radius=90)),

    dict(id="villa-aviary", placeId="villas-romaines", name="Villa of the Aviary", category="district",
         latlon=UV(323, 865), rotation=30, footprint=(50, 45), scale=1.0, model="carthage/villa-aviary",
         activePeriods=ROM_LATE,
         variants={
             "punic-150": dict(note="A hillside of Punic tombs and, below, houses of the seaside quarter."),
             "roman-200": dict(note="A rich town house on the slope above the sea: rooms round a peristyle garden whose mosaic floor shows birds among vine and acanthus scrolls, the 'aviary'."),
             "vandal-480": dict(note="Still lived in, divided and redecorated; houses like this were taken over by Vandal nobles after 439."),
             "ruins-1600": dict(note="Buried under olive groves; only the mosaics will come back to light in the 20th century excavations."),
         },
         summary="A peristyle town house in the park of Roman villas on the Odeon hill, named after its mosaic of birds in a garden.",
         details=["The houses on the slope between the Odeon and the sea were excavated from the 1950s and form today's park of Roman villas. The Villa of the Aviary (Maison de la Volière) had a garden court with columns, a mosaic of birds among foliage round it, and reception rooms opening off it.",
                  "The miniature shows the peristyle and garden, tiled roofs over the rooms and a terrace toward the sea. Room plans are simplified."],
         built="2nd–3rd century CE", function="Town house", confidence="reconstruction",
         sourceIds=["wiki-archaeological-site", "bullo", "ennabli"], activity=dict(figures=8, radius=50)),

    # ---------------------------------------------------------------- late antique and later
    dict(id="damous-el-karita", name="Basilica of Damous el Karita", category="religious",
         latlon=(36.8614, 10.3311), rotation=30, footprint=(150, 70), scale=1.0, model="carthage/damous-el-karita",
         activePeriods=["vandal-480"],
         variants={
             "roman-200": dict(note="Not yet built: a cemetery outside the city, where Christians will later be buried around their martyrs."),
             "vandal-480": dict(note="The largest church of Carthage: nine aisles, a semicircular court and an underground rotunda for a martyr's relics; rebuilt and enlarged after the Byzantine reconquest of 533."),
             "ruins-1600": dict(note="Gone to the lime kilns; a field of column bases and broken capitals, its name, from domus caritatis, 'house of charity', kept by the villagers."),
         },
         summary="The greatest Christian basilica of Carthage, outside the old city to the north: nine aisles, a semicircular atrium and a rotunda over a martyr's crypt.",
         details=["Built in the later 4th century and remodelled in the 6th, it measured about 65 by 45 m, with columns of reused marble. A great semicircular court opened from it toward an underground rotunda. Which martyrs it honoured is not known for certain.",
                  "The miniature shows the nine-aisled hall with its clerestoried nave, the forecourt, and the domed rotunda beyond the hemicycle. The roofs are reconstructed."],
         built="later 4th century, rebuilt 6th century", function="Church and martyrs' shrine", confidence="reconstruction",
         sourceIds=["wiki-damous", "ennabli-lb", "victor-vita"], activity=dict(figures=20, radius=110)),

    dict(id="sidi-bou-said", placeId="jebel-manar", name="Sidi Bou Said", category="religious",
         latlon=(36.8712, 10.3475), rotation=0, footprint=(90, 70), scale=1.0, model="carthage/sidi-bou-said",
         activePeriods=RUINS,
         variants={
             "vandal-480": dict(note="A bare headland, perhaps with a lookout or beacon over the gulf."),
             "ruins-1600": dict(note="The white village round the zawiya of Abu Said al-Baji (died 1231), a Sufi teacher who came to the beacon hill to pray and watch for corsairs."),
         },
         summary="The village on the cliff at the tip of the peninsula, grown up round the shrine of the 13th-century Sufi saint Abu Said al-Baji.",
         details=["The saint, called Sidi Bou Said, settled on Jebel Manar and was buried there in 1231; his zawiya drew pilgrims and the village grew round it. Its houses were built partly with stone from the ruins of Carthage below.",
                  "The miniature shows the domed zawiya and minaret among whitewashed courtyard houses. The blue-and-white look of today dates from the 20th century; here doors and grilles are left dark."],
         built="13th century onward", function="Shrine and village", confidence="interpretation",
         sourceIds=["wiki-sidi-bou-said"], activity=dict(figures=12, radius=70)),
]
