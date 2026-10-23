# Lisbon: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
# Positions from OpenStreetMap and Wikipedia. The Tagus is one very wide path offset 1200 m from the
# 1800 shoreline; the older, more inland shores (the Ribeira before the Pombaline quays, the Roman and
# Moorish beach at the foot of the Baixa) are added as narrower strips for their eras.
ALL = ["olisipo-50", "moorish-1100", "manueline-1550", "pre-earthquake-1750", "pombaline-1800"]
ROMAN = ["olisipo-50"]
MOORISH = ["moorish-1100"]
ANCIENT = ["olisipo-50", "moorish-1100"]
FERN = ["manueline-1550", "pre-earthquake-1750"]            # the walled city of the kings, before 1755
CHRISTIAN = ["manueline-1550", "pre-earthquake-1750", "pombaline-1800"]
LATE = ["pre-earthquake-1750", "pombaline-1800"]
POMBAL = ["pombaline-1800"]

SOURCES = [
    dict(id="wiki-history-lisbon", title="History of Lisbon", author="Wikipedia", url="https://en.wikipedia.org/wiki/History_of_Lisbon"),
    dict(id="wiki-olisipo", title="Olisipo", author="Wikipedia", url="https://en.wikipedia.org/wiki/Olisipo"),
    dict(id="wiki-tagus", title="Tagus", author="Wikipedia", url="https://en.wikipedia.org/wiki/Tagus"),
    dict(id="wiki-walls-lisbon", title="Walls of Lisbon", author="Wikipedia", url="https://en.wikipedia.org/wiki/Walls_of_Lisbon"),
    dict(id="wiki-muralhas-fernandinas", title="Muralhas fernandinas", author="Wikipedia (pt)", url="https://pt.wikipedia.org/wiki/Muralhas_fernandinas"),
    dict(id="wiki-cerca-moura", title="Cerca moura", author="Wikipedia (pt)", url="https://pt.wikipedia.org/wiki/Cerca_moura"),
    dict(id="wiki-alfama", title="Alfama", author="Wikipedia", url="https://en.wikipedia.org/wiki/Alfama"),
    dict(id="wiki-mouraria", title="Mouraria", author="Wikipedia (pt)", url="https://pt.wikipedia.org/wiki/Mouraria"),
    dict(id="wiki-bairro-alto", title="Bairro Alto", author="Wikipedia", url="https://en.wikipedia.org/wiki/Bairro_Alto"),
    dict(id="wiki-baixa", title="Lisbon Baixa", author="Wikipedia", url="https://en.wikipedia.org/wiki/Lisbon_Baixa"),
    dict(id="wiki-rossio", title="Rossio", author="Wikipedia", url="https://en.wikipedia.org/wiki/Rossio"),
    dict(id="wiki-aqueduct", title="Águas Livres Aqueduct", author="Wikipedia", url="https://en.wikipedia.org/wiki/%C3%81guas_Livres_Aqueduct"),
    dict(id="wiki-passeio-publico", title="Passeio Público", author="Wikipedia", url="https://en.wikipedia.org/wiki/Passeio_P%C3%BAblico"),
    dict(id="wiki-estrela", title="Estrela Basilica", author="Wikipedia", url="https://en.wikipedia.org/wiki/Estrela_Basilica"),
    dict(id="wiki-pombaline", title="Pombaline style", author="Wikipedia", url="https://en.wikipedia.org/wiki/Pombaline_style"),
    dict(id="wiki-gaiola", title="Gaiola (construction)", author="Wikipedia", url="https://en.wikipedia.org/wiki/Gaiola_(construction)"),
    dict(id="oliveira-marques", title="History of Portugal (2 vols)", author="A. H. de Oliveira Marques", year=1972),
    dict(id="kennedy-muslim-spain", title="Muslim Spain and Portugal: A Political History of al-Andalus", author="Hugh Kennedy", year=1996),
    dict(id="gois-descriptio", title="Urbis Olisiponis Descriptio (Description of the City of Lisbon)", author="Damião de Góis", year=1554),
    dict(id="oliveira-sumario", title="Sumário em que brevemente se contêm algumas coisas assim eclesiásticas como seculares que há na cidade de Lisboa", author="Cristóvão Rodrigues de Oliveira", year="1551–1554"),
    dict(id="global-city", title="The Global City: On the Streets of Renaissance Lisbon", author="Annemarie Jordan Gschwend and K. J. P. Lowe (eds.)", year=2015),
    dict(id="franca-pombalina", title="Lisboa Pombalina e o Iluminismo", author="José-Augusto França", year=1965),
    dict(id="maxwell-pombal", title="Pombal: Paradox of the Enlightenment", author="Kenneth Maxwell", year=1995),
    dict(id="osm", title="OpenStreetMap", author="OpenStreetMap contributors", url="https://www.openstreetmap.org/"),
]

CITY = dict(
    name="Lisbon", subtitle="Olisipo, al-Ushbuna, Lisboa",
    description="Lisbon on the Tagus estuary from Roman Olisipo to the city Pombal rebuilt after the earthquake of 1755: the castle hill with the Alfama below it, the Baixa valley from the Rossio down to the river, the Chiado and Bairro Alto to the west and Graça to the north-east. Belém, where the India fleets sailed from, lies 6 km west, beyond the frame. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="manueline-1550",
    world=dict(heightScale=1.0, walls=["#EFE6D2", "#E9D2B4", "#F2EDE2", "#E3C9A0", "#DDE0D8", "#EAD9BE"], roofs=["#B8694A", "#C27E5A", "#A95E43"]),
    camera=dict(target=(38.7100, -9.1370), distance=38),
)

# north-west corner, south-east corner: the Amoreiras and the Rato to the Madre de Deus shore, the Tagus below
FRAME = ((38.7260, -9.1600), (38.7000, -9.1160))

PALETTE = dict(parchment="#E7D5AE", ink="#6B4A33", water="#5F8890", hill="#7E805C", road="#8A6A4A")
COMPASS = (38.7040, -9.1215)
CARTOUCHE = (38.7008, -9.1590)

PERIODS = [
    dict(id="olisipo-50", label="Felicitas Julia Olisipo", year=50, startYear=-138, endYear=713,
         summary="Olisipo, an Iron Age town on the hill above the Tagus, becomes a Roman base after Decimus Junius Brutus' campaign of 138 BCE and a town of Roman citizens, Felicitas Julia, probably under Caesar or Augustus. Houses climb the castle hill, a theatre faces the river below the summit, and fish-salting works line the beach of the Baixa. The range runs on through the Suebi and Visigoths to about 714.",
         population="perhaps 20,000–30,000 (estimates vary widely)",
         feel="Brine and rotting fish from the salting vats on the beach, amphorae of fish sauce stacked on the quay, Latin in the forum and the old Lusitanian tongue in the market.",
         style="antique",
         houses=dict(title="Terraced houses of Olisipo", text="Houses of rubble and mortar under tiled roofs, packed on terraces cut into the slope between the summit and the river; the richer ones with painted walls and mosaic floors, as found under the cathedral cloister and in the Baixa."),
         outskirts=dict(title="Salting works and villas", text="Along the beach of the Baixa, fish-salting tanks and potteries; on the slopes beyond, farms, villas and tombs beside the roads west along the estuary and north toward Scallabis (Santarém).")),
    dict(id="moorish-1100", label="al-Ushbuna", year=1100, startYear=714, endYear=1147,
         summary="Taken by Arab and Berber armies around 714, al-Ushbuna is a frontier port of al-Andalus, ruled from Córdoba, then by the taifa kings of Badajoz and from 1111 by the Almoravids. The alcáçova (citadel) crowns the hill and the walled medina runs down to the river, with the main mosque on the slope and suburbs at Alfama and in the Baixa. Afonso Henriques takes it in October 1147.",
         population="perhaps 15,000–20,000 (estimates vary)",
         feel="The call to prayer over flat roofs, fishing boats drawn up on the beach, steam from the hot springs of Alfama, and lookouts watching the river for Norse and Christian sails.",
         style="courtyard",
         houses=dict(title="Courtyard houses of the medina", text="Houses of rubble, rammed earth and brick, whitewashed, turned inward round a small patio with a well or cistern; blank walls on the lanes. Excavations inside the castle have found such 11th–12th century houses, with latrines and red-painted plaster."),
         outskirts=dict(title="Alfama and the gardens", text="Alfama (from al-hamma, 'the hot springs') below the walls to the east; orchards, threshing floors and olive groves on the slopes; the marshy valley of the Baixa with its stream and a scatter of houses.")),
    dict(id="manueline-1550", label="Port of the Indies", year=1550, startYear=1148, endYear=1579,
         summary="Since Vasco da Gama's return in 1499, pepper and spices from India pass through the Casa da Índia beside the king's riverside palace, and ships are built at the Ribeira das Naus next door. Inside King Fernando's wall (1373–75) live about 100,000 people, one in ten of them enslaved. The range runs from the Christian conquest of 1147 to Philip II's takeover in 1580.",
         population="about 100,000 (the count of 1551)",
         feel="Pepper dust and tar on the Ribeira, African, Flemish, Italian and Indian voices in the Rua Nova, the bells of the parish churches and the shipwrights' mallets.",
         style="early-modern",
         houses=dict(title="Tall narrow houses", text="Narrow fronts of three to five storeys, stone below and timber frame above, shops at street level, upper floors jutting over the older streets; tiled roofs, and glazed tiles (azulejos) on the stairs of the richer houses. In the Alfama the Moorish lanes keep their twists and dead ends."),
         outskirts=dict(title="Quintas and the new Bairro Alto", text="Beyond the wall, the Bairro Alto rises on a grid laid out from 1513; elsewhere quintas (farmsteads), orchards, olive groves, windmills and convents on the hills, and rope-walks, kilns and boatyards along the shore.")),
    dict(id="pre-earthquake-1750", label="Baroque Lisbon", year=1750, startYear=1580, endYear=1755,
         summary="After sixty years of Spanish kings (1580–1640) and the Restoration, Brazilian gold pays for João V's works: the Patriarchal church in the Paço da Ribeira, the Águas Livres aqueduct (water from 1748), the gilded chapels of São Roque. José I opens the Ópera do Tejo in March 1755. On 1 November 1755 an earthquake, a tsunami and fire destroy the centre.",
         population="perhaps 200,000",
         feel="Processions with gilded floats, sedan chairs in the lanes, the river crowded with the Brazil fleets, water-carriers shouting at every fountain.",
         style="early-modern",
         houses=dict(title="Houses on medieval plots", text="Four and five storeys of rubble masonry, plastered and painted, on narrow medieval plots; blue-and-white tiled entrances and stairs, iron balconies, tiled roofs. The lanes are still medieval, so narrow that fire jumps across them."),
         outskirts=dict(title="Convents and quintas", text="Convents with walled gardens and noble quintas on the hills, orchards and olive groves; the new aqueduct arrives at the Amoreiras from its arches across the Alcântara valley, beyond the frame.")),
    dict(id="pombaline-1800", label="Pombaline Lisbon", year=1800, startYear=1756, endYear=1807,
         summary="Pombal's engineers Manuel da Maia, Eugénio dos Santos and Carlos Mardel rebuilt the Baixa from 1758 on a grid of straight streets, with uniform four-storey blocks round a timber cage (gaiola) meant to ride out earthquakes. The Praça do Comércio replaces the palace square; the Carmo stands roofless; the Estrela basilica (1779–1790) rises at the map's western edge. The range ends with the French invasion of 1807.",
         population="perhaps 180,000–200,000",
         feel="Builders' carts and stacks of cut stone in half-finished streets, goldsmiths' and silversmiths' signs on the new shopfronts, coffee and gossip in the Rossio.",
         style="early-modern",
         houses=dict(title="Pombaline blocks", text="Four storeys of identical fronts with plain stone frames, iron balconies on the first floor and dormers in the roof; behind the plaster a lattice of timber (the gaiola) braces the walls, and fire walls rise above the roofs between the houses."),
         outskirts=dict(title="The old quarters", text="Outside the Baixa the old quarters were patched rather than replanned: Alfama and Mouraria keep their lanes; quintas, convents and the Passeio Público garden (1764) fill the edges.")),
]

# ---------------------------------------------------------------- the Tagus
TEJO_BLURB = "The Tagus (Latin Tagus, Arabic Tājuh, Portuguese Tejo) widens here into an estuary 2–3 km across, opening east into the 'Sea of Straw' (Mar da Palha) and narrowing west to the sea at Belém. Its sheltered water made Lisbon a port for Phoenicians, Romans, Moors and the India fleets."

WATER = [
    # the river, drawn 1200 m off the shore of 1800 (the Praça do Comércio quay is the furthest seaward line)
    dict(id="tejo", name="Tagus (Tejo)", width=2400, blurb=TEJO_BLURB,
         path=[(38.69441, -9.16712), (38.69481, -9.15912), (38.69503, -9.15468), (38.69543, -9.15062), (38.69562, -9.14741), (38.69578, -9.14491), (38.69578, -9.14235),
               (38.69570, -9.14029), (38.69558, -9.13794), (38.69558, -9.13321), (38.69689, -9.12831), (38.69808, -9.12564), (38.69890, -9.12358), (38.70029, -9.12052),
               (38.70168, -9.11803), (38.70356, -9.11485), (38.70647, -9.11048), (38.71061, -9.10634), (38.71468, -9.10363), (38.71810, -9.10155), (38.72132, -9.09954), (38.72640, -9.09650)]),
    dict(id="mar-da-palha", name="Mar da Palha", width=1600,
         blurb="East of the city the estuary opens into a shallow inland sea some 10 km wide, the 'Sea of Straw', perhaps named for the river's flotsam or the colour of its water at sunset.",
         path=[(38.6920, -9.1250), (38.6960, -9.1100), (38.7050, -9.1000)]),
    # the shore before the Pombaline quays: the Ribeira, the Terreiro do Paço's beach, the Ribeira Velha
    dict(id="ribeira-shore", name="Tagus: the Ribeira", width=200, periods=FERN,
         blurb="Before 1755 the shore in front of the palace was a working beach and a row of wooden and stone landings: the Ribeira, where boats unloaded fish, grain, wood and the cargo of the India ships. Pombal's square and quays pushed it out by 50–100 m.",
         path=[(38.70571, -9.14385), (38.70590, -9.14190), (38.70600, -9.13936), (38.70631, -9.13728), (38.70662, -9.13523), (38.70704, -9.13344), (38.70755, -9.13162), (38.70806, -9.12976), (38.70891, -9.12745), (38.70986, -9.12555), (38.71137, -9.12292)]),
    # the ancient shore, 100–250 m further inland at the Baixa
    dict(id="ancient-shore", name="Tagus: the ancient shore", width=400, periods=ANCIENT,
         blurb="In Roman and Moorish times the river came up to the foot of the castle hill: the beach of the Baixa lay roughly along today's Rua da Conceição and the Moorish sea wall ran along the Rua dos Bacalhoeiros. Silt and centuries of landfill have since pushed the shore out.",
         path=[(38.70421, -9.16378), (38.70481, -9.15574), (38.70542, -9.14964), (38.70604, -9.14550), (38.70664, -9.14248), (38.70699, -9.14034), (38.70690, -9.13865), (38.70679, -9.13650),
               (38.70690, -9.13433), (38.70701, -9.13266), (38.70737, -9.13054), (38.70807, -9.12821), (38.70910, -9.12592), (38.71042, -9.12371), (38.71212, -9.12138), (38.71395, -9.11914), (38.71575, -9.11694)]),
    dict(id="esteiro", name="Esteiro da Baixa", width=35, periods=ANCIENT,
         blurb="A tidal creek ran up the Baixa valley toward the Rossio, fed by the streams of Valverde and Arroios. Its course is the usual reconstruction from boreholes and excavations; the valley floor was marshy until it was drained and built over.",
         path=[(38.7088, -9.1361), (38.7100, -9.1363), (38.7114, -9.1370), (38.7128, -9.1380), (38.7140, -9.1388), (38.7158, -9.1398), (38.7185, -9.1418), (38.7215, -9.1440), (38.7262, -9.1470)]),
]
ISLANDS = []

HILLS = [
    dict(id="castle-hill", name="Castle hill (São Jorge)", center=(38.7136, -9.1333), radius=230,
         blurb="The highest point of old Lisbon, about 110 m above the river: the Iron Age settlement, the Roman town's summit, the Moorish alcáçova and the castle of the kings."),
    dict(id="sao-vicente-hill", name="São Vicente", center=(38.7150, -9.1268), radius=190,
         blurb="The hill east of the castle where Afonso Henriques' German and Flemish crusaders camped in 1147 and where he founded the monastery of São Vicente 'outside the walls'."),
    dict(id="graca-hill", name="Graça (Santo André)", center=(38.7180, -9.1313), radius=250,
         blurb="The hill north-east of the castle, crowned by the Augustinian convent of Graça (from 1271) and the chapel of Senhora do Monte; the Castilians besieged the city from here in 1384."),
    dict(id="santana-hill", name="Sant'Ana", center=(38.7208, -9.1388), radius=250,
         blurb="The hill north of the Rossio between the valleys of Valverde and Arroios, a place of convents and quintas."),
    dict(id="sao-roque-hill", name="São Roque", center=(38.7142, -9.1458), radius=250,
         blurb="The high ground west of the Baixa where the Bairro Alto was laid out from 1513 and the Jesuits built São Roque."),
    dict(id="chagas-hill", name="Chagas", center=(38.7097, -9.1428), radius=150,
         blurb="The spur above the Ribeira between the Chiado and the river, named after the church of the Chagas (the Holy Wounds), built for the sailors of the India run."),
    dict(id="santa-catarina-hill", name="Santa Catarina", center=(38.7094, -9.1478), radius=180,
         blurb="The headland west of the Chiado with a view over the river, long a lookout for ships coming in from the sea."),
    dict(id="estrela-hill", name="Estrela", center=(38.7128, -9.1562), radius=280,
         blurb="The heights of the Estrela and the Lapa west of the old city, open country of quintas until the 18th century."),
]

# ---------------------------------------------------------------- streets and roads
ROMAN_WEST = [(38.7092, -9.1385), (38.7098, -9.1410), (38.7097, -9.1440), (38.7092, -9.1480), (38.7088, -9.1530), (38.7082, -9.1600)]
ROMAN_NORTH = [(38.7128, -9.1352), (38.7150, -9.1360), (38.7180, -9.1362), (38.7215, -9.1356), (38.7262, -9.1350)]
ROMAN_CARDO = [(38.7090, -9.1338), (38.7100, -9.1338), (38.7110, -9.1333), (38.7122, -9.1330), (38.7131, -9.1331)]
ROMAN_EAST = [(38.7093, -9.1335), (38.7097, -9.1310), (38.7105, -9.1290), (38.7116, -9.1268), (38.7132, -9.1245)]
MEDINA_STREET = [(38.7104, -9.1340), (38.7112, -9.1336), (38.7122, -9.1331), (38.7130, -9.1328)]
MOORISH_WEST = [(38.7104, -9.1340), (38.7106, -9.1365), (38.7108, -9.1395), (38.7108, -9.1425), (38.7112, -9.1460), (38.7120, -9.1510), (38.7130, -9.1560), (38.7138, -9.1610)]
MOORISH_NORTH = [(38.7128, -9.1353), (38.7148, -9.1362), (38.7175, -9.1362), (38.7215, -9.1356), (38.7262, -9.1350)]
ALFAMA_LANE = [(38.7101, -9.1297), (38.7110, -9.1278), (38.7120, -9.1260), (38.7134, -9.1242), (38.7150, -9.1225), (38.7172, -9.1205)]
RUA_NOVA = [(38.7093, -9.1386), (38.7094, -9.1366), (38.7092, -9.1350)]
BAIXA_STREET = [(38.7090, -9.1375), (38.7105, -9.1382), (38.7118, -9.1388), (38.7129, -9.1392)]
SINTRA_ROAD = [(38.7106, -9.1423), (38.7108, -9.1445), (38.7112, -9.1475), (38.7118, -9.1505), (38.7125, -9.1540), (38.7132, -9.1575), (38.7138, -9.1610)]
VALVERDE_ROAD = [(38.7156, -9.1392), (38.7175, -9.1405), (38.7200, -9.1428), (38.7230, -9.1450), (38.7262, -9.1468)]
ARROIOS_ROAD = [(38.7162, -9.1368), (38.7190, -9.1360), (38.7225, -9.1352), (38.7262, -9.1350)]
XABREGAS_ROAD = [(38.7128, -9.1240), (38.7148, -9.1218), (38.7172, -9.1195), (38.7205, -9.1168), (38.7240, -9.1150), (38.7270, -9.1135)]
RUA_DA_ROSA = [(38.7104, -9.1447), (38.7125, -9.1450), (38.7150, -9.1458)]
GRACA_ROAD = [(38.7168, -9.1318), (38.7178, -9.1310), (38.7195, -9.1300), (38.7230, -9.1290), (38.7262, -9.1285)]

ROADS = [
    # ---- Olisipo
    dict(id="roman-cardo", name="Street up to the summit", path=ROMAN_CARDO, width=8, style="major", labelled=True, periods=ROMAN,
         blurb="The main street climbed from the river past the forum, by the usual reconstruction near the later cathedral, to the theatre and the summit. Stretches of Roman paving have been found under the cathedral cloister."),
    dict(id="roman-west-road", name="Road west along the estuary", path=ROMAN_WEST, width=8, style="major", labelled=True, periods=ROMAN,
         blurb="West across the Baixa beach and along the river toward the mouth of the Tagus and the coast; the Antonine Itinerary's road to Emerita left Olisipo by the river crossing upstream."),
    dict(id="roman-north-road", name="Road north to Scallabis", path=ROMAN_NORTH, width=8, style="major", labelled=True, periods=ROMAN,
         blurb="Up the Arroios valley toward Scallabis (Santarém), the seat of the judicial district (conventus) to which Olisipo belonged, and on to Bracara and Emerita."),
    dict(id="roman-shore-road", name="Shore road east", path=ROMAN_EAST, width=6, style="minor", periods=ROMAN,
         blurb="Along the shore below the hill to the hot springs and the fish-salting works east of the town."),
    # ---- al-Ushbuna
    dict(id="medina-street", name="Street of the medina", path=MEDINA_STREET, width=6, style="major", labelled=True, periods=MOORISH,
         blurb="From the Porta do Ferro up past the main mosque toward the gate of the alcáçova: the spine of the walled town, with the market and the mosque at its lower end."),
    dict(id="moorish-west-road", name="Road west to Shintara (Sintra)", path=MOORISH_WEST, width=8, style="major", labelled=True, periods=MOORISH,
         blurb="Out of the Porta do Ferro, across the creek and the marshy Baixa, up the far slope and west toward Sintra, the hill fortress that guarded the coast."),
    dict(id="moorish-north-road", name="Road north to Shantarin (Santarém)", path=MOORISH_NORTH, width=8, style="major", labelled=True, periods=MOORISH,
         blurb="From the Porta de Alfofa north up the Arroios valley to Santarém, the next fortress up the Tagus; Afonso Henriques took it by surprise in March 1147, seven months before Lisbon."),
    dict(id="alfama-lane", name="Lanes of Alfama", path=ALFAMA_LANE, width=5, style="minor", labelled=True, periods=["moorish-1100"] + CHRISTIAN,
         blurb="The winding way from the Porta de Alfama past the hot springs and down to the shore: the Alfama's lanes, stairs and blind alleys keep their Moorish pattern to this day."),
    # ---- the kings' city, 1148–1755
    dict(id="rua-nova", name="Rua Nova dos Mercadores", path=RUA_NOVA, width=12, style="major", labelled=True, periods=FERN,
         blurb="The 'New Street of the Merchants', paved and arcaded in part, ran across the Baixa parallel to the river: the richest street of the city, with goldsmiths, booksellers, mercers and the shops of foreign merchants. It vanished in 1755."),
    dict(id="baixa-street", name="Streets of the Baixa", path=BAIXA_STREET, width=8, style="major", periods=FERN,
         blurb="Streets and lanes wound through the Baixa between the river and the Rossio. Their trade names (goldsmiths, harness-makers, gilders, shoemakers, cloth-sellers) were carried over to the streets of the Pombaline grid."),
    dict(id="sintra-road", name="Road to Sintra", path=SINTRA_ROAD, width=8, style="major", labelled=True, periods=CHRISTIAN,
         blurb="Out of the Porta de Santa Catarina at the Chiado, along the Calçada do Combro and past the Estrela toward Sintra and the royal palace there."),
    dict(id="valverde-road", name="Road up the Valverde", path=VALVERDE_ROAD, width=8, style="major", labelled=True, periods=CHRISTIAN,
         blurb="North out of the Porta de Santo Antão up the valley of Valverde, between orchards and quintas; Pombal's Passeio Público was laid out along it in 1764, and the Avenida da Liberdade follows it today."),
    dict(id="arroios-road", name="Road to Arroios and Santarém", path=ARROIOS_ROAD, width=8, style="major", periods=CHRISTIAN,
         blurb="From the Porta da Mouraria up the Arroios valley, the old road north to Sacavém and Santarém."),
    dict(id="xabregas-road", name="Road to Xabregas", path=XABREGAS_ROAD, width=8, style="minor", labelled=True, periods=CHRISTIAN,
         blurb="Out of the Porta da Cruz along the shore past Santa Apolónia to the convent of Madre de Deus (1509) and the royal palace of Xabregas."),
    dict(id="rua-da-rosa", name="Rua da Rosa", path=RUA_DA_ROSA, width=6, style="minor", labelled=True, periods=CHRISTIAN,
         blurb="One of the long straight streets of the Bairro Alto, laid out from 1513 on the lands of the Andrade family: the first planned grid in Lisbon."),
    dict(id="graca-road", name="Road through Graça", path=GRACA_ROAD, width=6, style="minor", periods=CHRISTIAN,
         blurb="Out of the Porta de Santo André past the Graça convent and north along the ridge."),
    # ---- Pombaline Baixa
    dict(id="rua-augusta", name="Rua Augusta", path=[(38.7086, -9.1366), (38.7129, -9.1384)], width=14, style="major", labelled=True, periods=POMBAL,
         blurb="The central street of Pombal's grid, from the Praça do Comércio to the Rossio, assigned to the cloth merchants. The triumphal arch at its end was designed in the 1750s–60s but only finished in 1875."),
    dict(id="rua-aurea", name="Rua Áurea (Rua do Ouro)", path=[(38.7086, -9.1378), (38.7130, -9.1397)], width=12, style="major", labelled=True, periods=POMBAL,
         blurb="The 'golden street' of the goldsmiths, one of the three long streets of the Pombaline Baixa; the plan of 1758 gave each street its trade."),
    dict(id="rua-da-prata", name="Rua da Prata", path=[(38.7086, -9.1354), (38.7131, -9.1372)], width=12, style="major", labelled=True, periods=POMBAL,
         blurb="The 'silver street' of the silversmiths, along the east side of the Baixa grid toward the market square on the site of the old hospital."),
    dict(id="rua-do-comercio", name="Rua do Comércio", path=[(38.7091, -9.1387), (38.7095, -9.1347)], width=10, style="minor", periods=POMBAL,
         blurb="A cross street of the grid, one block back from the square."),
    dict(id="rua-da-conceicao", name="Rua da Conceição", path=[(38.7101, -9.1391), (38.7105, -9.1350)], width=10, style="minor", periods=POMBAL,
         blurb="A cross street of the grid, near the line of the old Rua Nova dos Mercadores."),
    dict(id="rua-da-vitoria", name="Rua da Vitória", path=[(38.7114, -9.1396), (38.7118, -9.1356)], width=10, style="minor", periods=POMBAL,
         blurb="A cross street of the grid toward the north end of the Baixa."),
    dict(id="rua-do-arsenal", name="Rua do Arsenal", path=[(38.7079, -9.1376), (38.7081, -9.1400), (38.7081, -9.1430), (38.7078, -9.1455)], width=10, style="major", periods=POMBAL,
         blurb="The new street west from the Praça do Comércio past the rebuilt Arsenal to the Cais do Sodré, over the ground where the palace, the Casa da Índia and the opera stood."),
]

# ---------------------------------------------------------------- walls and gates
CERCA_MOURA = [(38.7150, -9.1340), (38.7140, -9.1350), (38.7128, -9.1353), (38.7115, -9.1346), (38.7104, -9.1341), (38.7094, -9.1341), (38.7090, -9.1336),
               (38.7090, -9.1328), (38.7091, -9.1315), (38.7099, -9.1305), (38.7101, -9.1297), (38.7112, -9.1300), (38.7121, -9.1302), (38.7132, -9.1308),
               (38.7142, -9.1312), (38.7150, -9.1322)]
FERNANDINA = [(38.7080, -9.1450), (38.7088, -9.1436), (38.7106, -9.1423), (38.7118, -9.1424), (38.7130, -9.1422), (38.7142, -9.1412), (38.7150, -9.1398),
              (38.7155, -9.1388), (38.7160, -9.1375), (38.7163, -9.1366), (38.7168, -9.1350), (38.7170, -9.1332), (38.7168, -9.1318), (38.7163, -9.1300),
              (38.7155, -9.1288), (38.7146, -9.1285), (38.7140, -9.1275), (38.7134, -9.1258), (38.7128, -9.1236), (38.7118, -9.1252), (38.7108, -9.1272),
              (38.7099, -9.1290), (38.7093, -9.1305), (38.7088, -9.1322), (38.7084, -9.1345), (38.7086, -9.1365), (38.7088, -9.1384), (38.7089, -9.1396),
              (38.7077, -9.1408), (38.7079, -9.1430)]

WALLS = [
    dict(id="medina-walls", name="Walls of al-Ushbuna", path=CERCA_MOURA, closed=True, periods=MOORISH,
         blurb="The wall of the medina, probably on the line of a late Roman wall, ran from the alcáçova down the slope to the river and back: some 16 hectares with gates on every side. The crusaders of 1147 attacked it with siege towers from the west and the east."),
    dict(id="cerca-moura", name="Cerca Moura (the old wall)", path=CERCA_MOURA, closed=True, periods=FERN,
         blurb="After 1147 the old Moorish wall stayed standing inside the growing city, its gates (do Ferro, de Alfofa, do Mar, de Alfama, do Sol) still in use and houses built against it on both sides. Long stretches survive inside later buildings."),
    dict(id="fernandine-wall", name="Cerca Fernandina", path=FERNANDINA, closed=True, periods=FERN,
         blurb="King Fernando I walled the whole city in 1373–75, after a Castilian army burned the open suburbs: about 5 km of wall with some 77 towers and more than thirty gates. The riverside stretch is the least certain; by 1550 the palace and quays had broken through it."),
]

GATES = [
    dict(id="porta-do-ferro", name="Porta do Ferro", position=(38.7104, -9.1341), periods=["moorish-1100"] + FERN),
    dict(id="porta-de-alfofa", name="Porta de Alfofa", position=(38.7128, -9.1353), periods=["moorish-1100"] + FERN),
    dict(id="porta-do-mar", name="Porta do Mar", position=(38.7090, -9.1328), periods=["moorish-1100"] + FERN),
    dict(id="porta-de-alfama", name="Porta de Alfama", position=(38.7101, -9.1297), periods=["moorish-1100"] + FERN),
    dict(id="porta-santa-catarina", name="Porta de Santa Catarina", position=(38.7106, -9.1423), periods=FERN),
    dict(id="porta-mouraria", name="Porta da Mouraria", position=(38.7163, -9.1366), periods=FERN),
    dict(id="porta-santo-andre", name="Porta de Santo André", position=(38.7168, -9.1318), periods=FERN),
    dict(id="porta-sao-vicente", name="Porta de São Vicente", position=(38.7146, -9.1285), periods=FERN),
    dict(id="porta-da-cruz", name="Porta da Cruz", position=(38.7128, -9.1236), periods=FERN),
]

BRIDGES = []

AQUEDUCTS = [
    dict(name="Aqueduto das Águas Livres", path=[(38.7300, -9.1700), (38.7268, -9.1640), (38.7246, -9.1600), (38.7232, -9.1566)], periods=LATE),
    dict(name="Galeria do Loreto (water gallery)", path=[(38.7232, -9.1566), (38.7212, -9.1545), (38.7185, -9.1515), (38.7160, -9.1490), (38.7135, -9.1468)], periods=LATE),
]

# ---------------------------------------------------------------- built-up areas
# Olisipo
OL_WEST = [(38.7128, -9.1352), (38.7129, -9.1336), (38.7112, -9.1337), (38.7100, -9.1342), (38.7092, -9.1343), (38.7091, -9.1352), (38.7105, -9.1356), (38.7118, -9.1357)]
OL_EAST = [(38.7130, -9.1327), (38.7131, -9.1310), (38.7121, -9.1300), (38.7108, -9.1300), (38.7100, -9.1312), (38.7096, -9.1326), (38.7100, -9.1334), (38.7112, -9.1329)]
OL_BEACH = [(38.7090, -9.1385), (38.7100, -9.1386), (38.7103, -9.1368), (38.7095, -9.1357), (38.7089, -9.1364)]
OL_CHIADO = [(38.7102, -9.1398), (38.7122, -9.1402), (38.7126, -9.1428), (38.7104, -9.1437)]
OL_HOTSPRINGS = [(38.7118, -9.1298), (38.7128, -9.1288), (38.7126, -9.1266), (38.7116, -9.1270), (38.7108, -9.1287)]
# al-Ushbuna
MED_W = [(38.7127, -9.1351), (38.7130, -9.1333), (38.7120, -9.1335), (38.7111, -9.1339), (38.7105, -9.1343), (38.7115, -9.1347)]
MED_E = [(38.7131, -9.1324), (38.7132, -9.1310), (38.7121, -9.1304), (38.7102, -9.1300), (38.7097, -9.1307), (38.7092, -9.1316), (38.7091, -9.1330), (38.7095, -9.1338),
         (38.7104, -9.1337), (38.7112, -9.1334), (38.7121, -9.1329)]
ALFAMA_N = [(38.7106, -9.1294), (38.7113, -9.1280), (38.7123, -9.1264), (38.7136, -9.1250), (38.7145, -9.1262), (38.7140, -9.1288), (38.7128, -9.1300), (38.7115, -9.1299)]
ALFAMA_E = [(38.7140, -9.1240), (38.7150, -9.1232), (38.7146, -9.1250), (38.7138, -9.1252)]
BAIXA_S_M = [(38.7091, -9.1395), (38.7104, -9.1396), (38.7104, -9.1368), (38.7097, -9.1367), (38.7091, -9.1369)]
BAIXA_N_M = [(38.7112, -9.1399), (38.7128, -9.1402), (38.7127, -9.1384), (38.7113, -9.1372)]
# the city of the kings
BAIXA_W = [(38.7096, -9.1399), (38.7128, -9.1403), (38.7128, -9.1396), (38.7117, -9.1391), (38.7104, -9.1386), (38.7096, -9.1382)]
BAIXA_E = [(38.7096, -9.1372), (38.7106, -9.1378), (38.7120, -9.1385), (38.7128, -9.1388), (38.7128, -9.1372), (38.7115, -9.1360), (38.7101, -9.1353), (38.7096, -9.1353)]
MADALENA = [(38.7128, -9.1366), (38.7136, -9.1364), (38.7130, -9.1354), (38.7120, -9.1351), (38.7108, -9.1350), (38.7101, -9.1348), (38.7110, -9.1358)]
CHIADO = [(38.7100, -9.1419), (38.7128, -9.1417), (38.7140, -9.1408), (38.7130, -9.1403), (38.7100, -9.1402)]
CORPO_SANTO = [(38.7084, -9.1446), (38.7100, -9.1440), (38.7103, -9.1427), (38.7092, -9.1420), (38.7084, -9.1430)]
MOURARIA = [(38.7158, -9.1370), (38.7164, -9.1352), (38.7160, -9.1340), (38.7150, -9.1343), (38.7140, -9.1352), (38.7142, -9.1366)]
GRACA = [(38.7166, -9.1330), (38.7166, -9.1312), (38.7158, -9.1296), (38.7149, -9.1300), (38.7147, -9.1318), (38.7153, -9.1332)]
SAO_VICENTE = [(38.7145, -9.1294), (38.7146, -9.1284), (38.7138, -9.1268), (38.7130, -9.1278), (38.7135, -9.1294)]
BA_E = [(38.7110, -9.1440), (38.7150, -9.1446), (38.7150, -9.1425), (38.7140, -9.1420), (38.7128, -9.1428), (38.7112, -9.1430)]
BA_W = [(38.7116, -9.1455), (38.7150, -9.1462), (38.7152, -9.1492), (38.7121, -9.1492)]
CHAGAS = [(38.7101, -9.1440), (38.7105, -9.1462), (38.7106, -9.1500), (38.7084, -9.1500), (38.7077, -9.1462)]
MADRAGOA = [(38.7080, -9.1507), (38.7110, -9.1507), (38.7120, -9.1558), (38.7085, -9.1578), (38.7068, -9.1560)]
LAPA = [(38.7088, -9.1584), (38.7124, -9.1566), (38.7127, -9.1600), (38.7075, -9.1600)]
SANTA_APOLONIA = [(38.7152, -9.1248), (38.7168, -9.1226), (38.7183, -9.1207), (38.7176, -9.1200), (38.7154, -9.1222), (38.7142, -9.1242)]
ANJOS = [(38.7176, -9.1372), (38.7250, -9.1362), (38.7255, -9.1386), (38.7182, -9.1394)]
SANTANA = [(38.7166, -9.1384), (38.7198, -9.1404), (38.7208, -9.1386), (38.7178, -9.1374)]
RATO = [(38.7152, -9.1466), (38.7180, -9.1476), (38.7186, -9.1512), (38.7156, -9.1506)]
GRACA_N = [(38.7172, -9.1325), (38.7196, -9.1312), (38.7200, -9.1330), (38.7178, -9.1340)]
# Pombaline Baixa (between the three long streets)
PB_W = [(38.7087, -9.1390), (38.7128, -9.1407), (38.7129, -9.1400), (38.7087, -9.1382)]
PB_1 = [(38.7087, -9.1375), (38.7129, -9.1394), (38.7129, -9.1387), (38.7087, -9.1369)]
PB_2 = [(38.7087, -9.1363), (38.7129, -9.1381), (38.7130, -9.1375), (38.7087, -9.1357)]
PB_E = [(38.7087, -9.1351), (38.7131, -9.1369), (38.7128, -9.1358), (38.7100, -9.1347), (38.7088, -9.1345)]

BLOCKS = [
    # ---- Olisipo
    dict(name="Olisipo: the western slope", polygon=OL_WEST, density="dense", periods=ROMAN),
    dict(name="Olisipo: the theatre quarter", polygon=OL_EAST, density="dense", periods=ROMAN),
    dict(name="Salting works on the beach", polygon=OL_BEACH, density="loose", periods=ROMAN),
    dict(name="Houses on the western slope", polygon=OL_CHIADO, density="loose", periods=ROMAN),
    dict(name="Houses by the hot springs", polygon=OL_HOTSPRINGS, density="loose", periods=ROMAN),
    # ---- al-Ushbuna
    dict(name="Medina: below the alcáçova", polygon=MED_W, density="dense", periods=MOORISH),
    dict(name="Medina: round the main mosque", polygon=MED_E, density="dense", periods=MOORISH),
    dict(name="Alfama", polygon=ALFAMA_N, density="dense", periods=MOORISH),
    dict(name="Western suburb by the beach", polygon=BAIXA_S_M, density="loose", periods=MOORISH),
    dict(name="Houses along the creek", polygon=BAIXA_N_M, density="loose", periods=MOORISH),
    # ---- the city of the kings (1550 and 1750)
    dict(name="Old town under the castle", polygon=MED_W, density="dense", periods=CHRISTIAN),
    dict(name="Sé and Santa Maria Madalena", polygon=MED_E, density="dense", periods=CHRISTIAN),
    dict(name="Alfama", polygon=ALFAMA_N, density="dense", periods=CHRISTIAN),
    dict(name="Alfama: São Miguel and Santo Estêvão", polygon=ALFAMA_E, density="dense", periods=CHRISTIAN),
    dict(name="Baixa: São Nicolau and São Julião", polygon=BAIXA_W, density="dense", periods=FERN),
    dict(name="Baixa: the Judiaria and the Rua Nova", polygon=BAIXA_E, density="dense", periods=FERN),
    dict(name="Madalena", polygon=MADALENA, density="dense", periods=CHRISTIAN),
    dict(name="Chiado and the Carmo", polygon=CHIADO, density="dense", periods=CHRISTIAN),
    dict(name="Corpo Santo", polygon=CORPO_SANTO, density="dense", periods=CHRISTIAN),
    dict(name="Mouraria", polygon=MOURARIA, density="dense", periods=CHRISTIAN),
    dict(name="Graça", polygon=GRACA, density="loose", periods=["manueline-1550"]),
    dict(name="Graça", polygon=GRACA, density="dense", periods=LATE),
    dict(name="São Vicente", polygon=SAO_VICENTE, density="loose", periods=["manueline-1550"]),
    dict(name="São Vicente", polygon=SAO_VICENTE, density="dense", periods=LATE),
    dict(name="Bairro Alto", polygon=BA_E, density="dense", periods=CHRISTIAN),
    dict(name="Bairro Alto", polygon=BA_W, density="loose", periods=["manueline-1550"]),
    dict(name="Bairro Alto", polygon=BA_W, density="dense", periods=LATE),
    dict(name="Chagas and Santa Catarina", polygon=CHAGAS, density="loose", periods=["manueline-1550"]),
    dict(name="Chagas and Santa Catarina", polygon=CHAGAS, density="dense", periods=LATE),
    dict(name="Boavista and the Mocambo", polygon=MADRAGOA, density="loose", periods=["manueline-1550"]),
    dict(name="Mocambo (Madragoa)", polygon=MADRAGOA, density="dense", periods=LATE),
    dict(name="Lapa", polygon=LAPA, density="loose", periods=LATE),
    dict(name="Santa Apolónia", polygon=SANTA_APOLONIA, density="loose", periods=CHRISTIAN),
    dict(name="Anjos", polygon=ANJOS, density="loose", periods=CHRISTIAN),
    dict(name="Sant'Ana", polygon=SANTANA, density="loose", periods=LATE),
    dict(name="Rato and the Cotovia", polygon=RATO, density="loose", periods=LATE),
    dict(name="Graça: Senhora do Monte", polygon=GRACA_N, density="loose", periods=LATE),
    # ---- the Pombaline Baixa
    dict(name="Baixa Pombalina: Rua dos Fanqueiros", polygon=PB_E, density="dense", periods=POMBAL),
    dict(name="Baixa Pombalina: between Augusta and Prata", polygon=PB_2, density="dense", periods=POMBAL),
    dict(name="Baixa Pombalina: between Ouro and Augusta", polygon=PB_1, density="dense", periods=POMBAL),
    dict(name="Baixa Pombalina: west of the Rua do Ouro", polygon=PB_W, density="dense", periods=POMBAL),
]

GARDENS = [
    dict(name="Orchards of the hill of Santo André", polygon=[(38.7166, -9.1338), (38.7192, -9.1322), (38.7186, -9.1292), (38.7160, -9.1300)], kind="orchard", periods=ANCIENT),
    dict(name="Olive groves of the western slopes", polygon=[(38.7130, -9.1440), (38.7160, -9.1450), (38.7165, -9.1500), (38.7125, -9.1500)], kind="orchard", periods=ANCIENT),
    dict(name="Gardens of Valverde", polygon=[(38.7170, -9.1418), (38.7215, -9.1450), (38.7210, -9.1470), (38.7165, -9.1430)], kind="orchard", periods=["moorish-1100", "manueline-1550"]),
    dict(name="Quintas of the Rato and Amoreiras", polygon=[(38.7200, -9.1500), (38.7252, -9.1488), (38.7252, -9.1580), (38.7212, -9.1590)], kind="orchard"),
    dict(name="Quintas of Sant'Ana", polygon=[(38.7212, -9.1400), (38.7250, -9.1398), (38.7252, -9.1428), (38.7215, -9.1425)], kind="orchard"),
    dict(name="Olive groves of Arroios", polygon=[(38.7205, -9.1340), (38.7252, -9.1335), (38.7252, -9.1300), (38.7210, -9.1300)], kind="orchard"),
    dict(name="Vineyards of the Estrela", polygon=[(38.7135, -9.1520), (38.7175, -9.1525), (38.7180, -9.1590), (38.7140, -9.1595)], kind="vineyard", periods=["olisipo-50", "moorish-1100", "manueline-1550"]),
    dict(name="Passeio Público", polygon=[(38.7160, -9.1402), (38.7192, -9.1425), (38.7189, -9.1432), (38.7157, -9.1409)], kind="park", periods=POMBAL),
]

MARSH = [
    dict(name="Marshes of the Baixa", polygon=[(38.7104, -9.1392), (38.7126, -9.1398), (38.7142, -9.1398), (38.7140, -9.1380), (38.7124, -9.1366), (38.7108, -9.1360), (38.7103, -9.1372)], periods=ROMAN),
]

DISTRICTS = [
    dict(id="olisipo", name="Olisipo", polygon=[(38.7150, -9.1345), (38.7140, -9.1356), (38.7120, -9.1358), (38.7091, -9.1352), (38.7088, -9.1330), (38.7096, -9.1300), (38.7120, -9.1297), (38.7145, -9.1315)], periods=ROMAN,
         description="The Roman town on the south face of the castle hill: the summit, the forum by the usual reconstruction near the later cathedral, the theatre, baths and houses on terraces down to the river."),
    dict(id="medina", name="al-Madina", polygon=CERCA_MOURA, periods=MOORISH,
         description="The walled town of al-Ushbuna between the alcáçova and the river: the main mosque, the market and the houses of the Muslim and Mozarabic Christian population, about 16 hectares."),
    dict(id="alfama-m", name="al-Hamma (Alfama)", polygon=ALFAMA_N, periods=MOORISH,
         description="The suburb outside the medina's east gate, named after its hot springs, a quarter of fishermen, craftsmen and baths."),
    dict(id="alfama", name="Alfama", polygon=ALFAMA_N, periods=CHRISTIAN,
         description="The old quarter of fishermen and sailors below the castle on the east, with its Moorish lanes; the Judiaria de Alfama lay here before 1497. It came through the earthquake better than the Baixa, being built on rock."),
    dict(id="mouraria", name="Mouraria", polygon=MOURARIA, periods=CHRISTIAN,
         description="The quarter assigned to the Muslims who stayed after 1147, outside the old walls on the north-west slope of the castle hill; in 1497 the Muslims were expelled or forcibly converted and the name remained."),
    dict(id="baixa", name="Baixa", polygon=[(38.7088, -9.1400), (38.7130, -9.1404), (38.7131, -9.1352), (38.7090, -9.1347)], periods=FERN,
         description="The low town in the valley between the castle hill and the Chiado: the Rua Nova, the Judiaria Grande (until 1497), the goldsmiths', cloth and harness-makers' streets, crowded on drained marsh."),
    dict(id="baixa-pombalina", name="Baixa Pombalina", polygon=[(38.7087, -9.1400), (38.7130, -9.1407), (38.7131, -9.1352), (38.7087, -9.1345)], periods=POMBAL,
         description="The low town rebuilt after 1755 on a grid of straight streets between the Rossio and the Praça do Comércio, the first large city district in Europe built to an anti-seismic design."),
    dict(id="bairro-alto", name="Bairro Alto", polygon=[(38.7104, -9.1440), (38.7152, -9.1446), (38.7153, -9.1495), (38.7118, -9.1495)], periods=CHRISTIAN,
         description="The 'high quarter', laid out from 1513 as the Vila Nova de Andrade on a grid of long streets; home of sailors, craftsmen, nobles and, after 1553, the Jesuits of São Roque."),
]

LABELS = [
    dict(text="Tagus", position=(38.7010, -9.1420), size="lg", rotation=-4, periods=ANCIENT),
    dict(text="Rio Tejo", position=(38.7010, -9.1420), size="lg", rotation=-4, periods=CHRISTIAN),
    dict(text="Mar da Palha", position=(38.7070, -9.1185), size="md", rotation=-35),
    dict(text="Olisipo", position=(38.7118, -9.1310), size="lg", periods=ROMAN),
    dict(text="al-Ushbuna", position=(38.7160, -9.1318), size="lg", periods=MOORISH),
    dict(text="Lixboa", position=(38.7195, -9.1420), size="lg", periods=["manueline-1550"]),
    dict(text="Lisboa", position=(38.7195, -9.1420), size="lg", periods=LATE),
    dict(text="Alfama", position=(38.7122, -9.1272), size="md", periods=["moorish-1100"] + CHRISTIAN),
    dict(text="Mouraria", position=(38.7155, -9.1358), size="sm", periods=CHRISTIAN),
    dict(text="Baixa", position=(38.7110, -9.1385), size="sm", periods=CHRISTIAN),
    dict(text="Bairro Alto", position=(38.7135, -9.1470), size="md", periods=CHRISTIAN),
    dict(text="Chiado", position=(38.7114, -9.1414), size="sm", periods=CHRISTIAN),
    dict(text="Graça", position=(38.7175, -9.1300), size="sm", periods=CHRISTIAN),
    dict(text="Madragoa", position=(38.7096, -9.1540), size="sm", periods=LATE),
    dict(text="Rossio", position=(38.7139, -9.1394), size="sm", periods=CHRISTIAN),
    dict(text="← Belém, 6 km", position=(38.7070, -9.1575), size="sm", periods=CHRISTIAN),
    dict(text="Estrela", position=(38.7140, -9.1580), size="sm", periods=POMBAL),
    dict(text="to Almada and Cacilhas", position=(38.7025, -9.1360), size="sm", periods=CHRISTIAN),
    dict(text="Valverde", position=(38.7205, -9.1450), size="sm"),
]
