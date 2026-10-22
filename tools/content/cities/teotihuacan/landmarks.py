# Teotihuacan: monuments across five eras. Positions come from the turned grid of geo.py (G(u, v): u metres
# along the Avenue of the Dead from the Moon pyramid, v metres across it, east positive).
import math

T, M, X, C, A = "tzacualli-100", "miccaotli-250", "xolalpan-450", "collapse-650", "aztec-1500"
ALL = [T, M, X, C, A]

P0 = (19.6996, -98.8440)
_A = math.radians(15.5)
KY, KX = 110850.0, 111320.0 * math.cos(math.radians(19.70))


def G(u, v):
    n = u * math.cos(_A) - v * math.sin(_A)
    e = u * math.sin(_A) + v * math.cos(_A)
    return (round(P0[0] + n / KY, 6), round(P0[1] + e / KX, 6))


# rotations: facing down the avenue (south-south-west), facing west across it, facing east across it
SOUTH, WEST, EAST = 15.5, 105.5, -74.5

SOURCES = [
    dict(id="millon-1973", title="Urbanization at Teotihuacan, Mexico, vol. 1: The Teotihuacan Map", author="René Millon, R. Bruce Drewitt and George L. Cowgill", year=1973),
    dict(id="cowgill-2015", title="Ancient Teotihuacan: Early Urbanism in Central Mexico", author="George L. Cowgill", year=2015),
    dict(id="sugiyama-2005", title="Human Sacrifice, Militarism, and Rulership: Materialization of State Ideology at the Feathered Serpent Pyramid, Teotihuacan", author="Saburo Sugiyama", year=2005),
    dict(id="sugiyama-cabrera-2007", title="The Moon Pyramid Project and the Teotihuacan State Polity", author="Saburo Sugiyama and Rubén Cabrera Castro", year=2007, note="Ancient Mesoamerica 18"),
    dict(id="sugiyama-sun-2013", title="Inside the Sun Pyramid at Teotihuacan, Mexico: 2008–2011 Excavations and Preliminary Results", author="Nawa Sugiyama, Saburo Sugiyama and Alejandro Sarabia", year=2013, note="Latin American Antiquity 24"),
    dict(id="manzanilla", title="Teotihuacan, ciudad excepcional de Mesoamérica", author="Linda R. Manzanilla", year=2017),
    dict(id="berrin-pasztory", title="Teotihuacan: Art from the City of the Gods", author="Kathleen Berrin and Esther Pasztory (eds.)", year=1993),
    dict(id="pasztory-1997", title="Teotihuacan: An Experiment in Living", author="Esther Pasztory", year=1997),
    dict(id="headrick", title="The Teotihuacan Trinity: The Sociopolitical Structure of an Ancient Mesoamerican City", author="Annabeth Headrick", year=2007),
    dict(id="spence-1992", title="Tlailotlacan, a Zapotec Enclave in Teotihuacan", author="Michael W. Spence", year=1992, note="in J. C. Berlo (ed.), Art, Ideology, and the City of Teotihuacan"),
    dict(id="rattray-1987", title="Los barrios foráneos de Teotihuacan", author="Evelyn C. Rattray", year=1987, note="in E. McClung de Tapia and E. C. Rattray (eds.), Teotihuacan: nuevos datos, nuevas síntesis, nuevos problemas"),
    dict(id="sahagun", title="Florentine Codex, Book 7 (the birth of the Sun and Moon at Teotihuacan) and Book 10", author="Bernardino de Sahagún", year="c. 1577", url="https://en.wikipedia.org/wiki/Florentine_Codex"),
    dict(id="batres-1906", title="Teotihuacán, memoria que presenta Leopoldo Batres", author="Leopoldo Batres", year=1906),
    dict(id="wiki-sun", title="Pyramid of the Sun", author="Wikipedia", url="https://en.wikipedia.org/wiki/Pyramid_of_the_Sun"),
    dict(id="wiki-moon", title="Pyramid of the Moon", author="Wikipedia", url="https://en.wikipedia.org/wiki/Pyramid_of_the_Moon"),
    dict(id="wiki-feathered-serpent", title="Temple of the Feathered Serpent, Teotihuacan", author="Wikipedia", url="https://en.wikipedia.org/wiki/Temple_of_the_Feathered_Serpent,_Teotihuacan"),
    dict(id="wiki-teotihuacan", title="Teotihuacan", author="Wikipedia", url="https://en.wikipedia.org/wiki/Teotihuacan"),
    dict(id="wiki-quetzalpapalotl", title="Quetzalpapalotl", author="Wikipedia", url="https://en.wikipedia.org/wiki/Quetzalpapalotl"),
    dict(id="wiki-talud-tablero", title="Talud-tablero", author="Wikipedia", url="https://en.wikipedia.org/wiki/Talud-tablero"),
    dict(id="wiki-great-goddess", title="Great Goddess of Teotihuacan", author="Wikipedia", url="https://en.wikipedia.org/wiki/Great_Goddess_of_Teotihuacan"),
    dict(id="wiki-tlalocan", title="Tlalocan", author="Wikipedia", url="https://en.wikipedia.org/wiki/Tlalocan"),
    dict(id="wiki-zapotec", title="Zapotec civilization", author="Wikipedia", url="https://en.wikipedia.org/wiki/Zapotec_civilization"),
    dict(id="wiki-feathered-serpent-deity", title="Feathered Serpent", author="Wikipedia", url="https://en.wikipedia.org/wiki/Feathered_Serpent"),
]

LANDMARKS = [
    # ------------------------------------------------------------ the north end: the Moon
    dict(id="pyramid-of-the-moon", placeId="pyramid-of-the-moon", name="Pyramid of the Moon", category="temple",
         latlon=G(-10, 0), rotation=SOUTH, footprint=(150, 160), scale=1.0, model="teotihuacan/pyramid-of-the-moon",
         activePeriods=ALL,
         variants={
             T: dict(model="teotihuacan/pyramid-of-the-moon-100", note="The first buildings: a platform some 23 m square (Building 1), soon enclosed in larger ones. The site at the head of the future avenue is already sacred.", confidence="reconstruction"),
             M: dict(note="Building 4, about 89 m a side, is dedicated around 200–250 with sacrificed captives and animals; the pyramid is approaching its final size."),
             X: dict(note="The final pyramid (Building 7), some 43 m high, with the talud-tablero platform added in front, closing the north end of the avenue below Cerro Gordo."),
             C: dict(model="teotihuacan/pyramid-of-the-moon-650", note="The temple on top and the buildings at its foot burned in the destruction of the centre; the pyramid itself stands, its stucco cracking.", confidence="interpretation"),
             A: dict(model="teotihuacan/pyramid-of-the-moon-1500", name="Metztli Itzacual, the Moon's pyramid", note="A grassy hill of rubble. The Aztecs called it the pyramid of the Moon: here, they said, Tecuciztecatl became the moon.", confidence="interpretation"),
         },
         summary="The pyramid at the north end of the Avenue of the Dead, raised in seven stages over three centuries and framed by Cerro Gordo behind it; a stage for the city's state rituals.",
         details=[
             "Tunnels dug by Saburo Sugiyama and Rubén Cabrera (1998–2004) found seven nested buildings, from a small platform of about 100 CE to the final pyramid of about 43 m. Each enlargement was dedicated with offerings: sacrificed men, often foreigners, with pumas, wolves, eagles and rattlesnakes buried alive or as offerings, obsidian and greenstone figures.",
             "The miniature shows the final form: four stepped bodies with the five-tiered talud-tablero adosada platform on the front, a stair up both, and a temple on top. The temple is lost; its form, colours and the flat roof with merlons follow painted and sculpted models of Teotihuacan temples.",
         ],
         built="c. 100–400 CE in seven stages", function="Temple platform at the head of the avenue", confidence="reconstruction",
         sourceIds=["wiki-moon", "sugiyama-cabrera-2007", "cowgill-2015", "millon-1973"], activity=dict(figures=40, radius=120)),

    dict(id="moon-plaza", placeId="moon-plaza", name="Plaza of the Moon", category="religious",
         latlon=G(-175, 0), rotation=SOUTH, footprint=(210, 170), scale=1.0, model="teotihuacan/moon-plaza",
         activePeriods=[M, X, C, A],
         variants={
             T: dict(note="Open ground before the early Moon platform, perhaps with a few small shrines; the plaza is laid out with the avenue in the next centuries.", confidence="interpretation"),
             M: dict(note="The plaza takes shape with the enlarged Moon pyramid: a paved square ringed by temple platforms of talud-tablero, an altar platform at its centre."),
             X: dict(note="A dozen or so temple platforms frame the plaza, painted red; the central platform and its altar mark the point where the avenue begins."),
             C: dict(model="teotihuacan/moon-plaza-650", note="Burned with the rest of the centre; temples on the platforms gone, stones and sculptures thrown into the plaza.", confidence="interpretation"),
             A: dict(model="teotihuacan/moon-plaza-1500", note="A ring of overgrown mounds. Aztec tradition put the gods' great fire here, into which Nanahuatzin leapt to become the Sun.", confidence="interpretation"),
         },
         summary="The great square at the foot of the Moon pyramid, closed by temple platforms on three sides, where the Avenue of the Dead begins; the setting for the city's largest gatherings in the north.",
         details=[
             "The plaza measures roughly 140 m across. Its platforms, mostly three-tiered talud-tablero bases for small temples, are grouped in threes on the east and west sides, a 'three-temple' arrangement found across the city. At the centre stands a square platform with an altar, and beside it a smaller structure divided inside into compartments.",
             "The miniature shows the stuccoed paving, the platforms with stairs facing the plaza, small flat-roofed temples on top and the central altar. Which platforms carried temples, and their colours, are reconstruction.",
         ],
         built="c. 200–350 CE", function="Ceremonial plaza", confidence="reconstruction",
         sourceIds=["wiki-moon", "wiki-teotihuacan", "millon-1973", "cowgill-2015"], activity=dict(figures=70, radius=110)),

    dict(id="palace-of-quetzalpapalotl", placeId="quetzalpapalotl", name="Palace of Quetzalpapalotl", category="civic",
         latlon=G(-205, -152), rotation=SOUTH, footprint=(60, 70), scale=1.0, model="teotihuacan/palace-of-quetzalpapalotl",
         activePeriods=[X, C],
         variants={
             M: dict(name="Building of the Feathered Shells", note="Not yet built: on this spot stands an earlier temple painted with feathered conch shells and green birds, later buried under the palace's platform.", confidence="reconstruction"),
             X: dict(note="An elite residence off the south-west corner of the Moon plaza, its patio framed by square pillars carved with quetzal-butterfly birds with inlaid obsidian eyes."),
             C: dict(model="teotihuacan/palace-of-quetzalpapalotl-650", note="Burned with the ceremonial centre; the roof beams fell into the rooms, where archaeologists found their charcoal.", confidence="interpretation"),
             A: dict(note="Buried under a low mound; it was dug out and rebuilt only in 1962–64.", confidence="interpretation"),
         },
         summary="A palace of priests or lords beside the Moon plaza, famous for its patio of carved pillars with birds in relief and its red painted walls.",
         details=[
             "The palace was excavated and largely rebuilt by Jorge Acosta in 1962–64. Its pillars show birds, read as quetzals or owls, in profile and frontal view, once with obsidian eyes; red-painted bands and almenas (roof ornaments) with year signs crown the walls. Beneath it lie the Palace of the Jaguars and the older Building of the Feathered Shells.",
             "The miniature shows the porticoed patio with its carved pillars, rooms on three sides, flat roofs edged with almenas and a stair up from the plaza. The roof ornaments are restored from fragments; the room plan follows Acosta's rebuilding.",
         ],
         built="c. 450–550 CE (dates vary)", function="Elite residence, perhaps of priests", confidence="reconstruction",
         sourceIds=["wiki-quetzalpapalotl", "wiki-teotihuacan", "berrin-pasztory", "cowgill-2015"], activity=dict(figures=14, radius=40)),

    dict(id="plaza-of-the-columns", placeId="plaza-of-the-columns", name="Plaza of the Columns complex", category="civic",
         latlon=G(-600, -190), rotation=EAST, footprint=(220, 170), scale=1.0, model="teotihuacan/plaza-of-the-columns",
         activePeriods=[M, X, C],
         variants={
             T: dict(note="Not yet built; scattered houses on the west side of the early ceremonial way.", confidence="interpretation"),
             M: dict(note="A large plaza west of the avenue enclosed by platforms on three sides, opening east toward the Sun pyramid."),
             X: dict(note="Perhaps the seat of the city's rulers: feasting debris, Maya-style murals and Maya pottery found here suggest receptions of foreign envoys around 350–450.", confidence="interpretation"),
             C: dict(model="teotihuacan/plaza-of-the-columns-650", note="Burned and abandoned with the rest of the avenue.", confidence="interpretation"),
             A: dict(note="Low mounds under fields, never fully excavated.", confidence="interpretation"),
         },
         summary="A great walled plaza west of the Avenue of the Dead between the Moon and the Sun, still mostly unexcavated, now thought by some to have been a palace of the city's rulers.",
         details=[
             "The complex is a plaza some 120 m across closed by a large platform on the west and long platforms on the north and south, with buildings behind. Excavations led by Saburo Sugiyama since 2015 have found broken Maya-style murals, Maya pottery and the remains of large feasts, buried around 350–450 CE.",
             "The miniature shows the plaza with a pyramid platform at the back, side platforms with temples, and residential buildings behind them. Almost everything above the ground plan is reconstruction by analogy with the excavated compounds.",
         ],
         built="c. 200–350 CE", function="Administrative or palace complex (debated)", confidence="interpretation",
         sourceIds=["wiki-teotihuacan", "cowgill-2015", "millon-1973"], activity=dict(figures=30, radius=90)),

    # ------------------------------------------------------------ the Sun
    dict(id="pyramid-of-the-sun", placeId="pyramid-of-the-sun", name="Pyramid of the Sun", category="temple",
         latlon=G(-705, 180), rotation=WEST, footprint=(240, 290), scale=1.0, model="teotihuacan/pyramid-of-the-sun",
         activePeriods=ALL,
         variants={
             T: dict(model="teotihuacan/pyramid-of-the-sun-100", note="Under construction: a core of earth, adobe and rubble rising in cells over a cave, with gangs carrying baskets up ramps. Its start is dated variously from about 100 to 170.", confidence="reconstruction"),
             M: dict(note="Finished by about 200–250: some 225 m a side and 65 m high, with its stair facing west toward the avenue and the setting sun."),
             X: dict(note="The largest building in the city, stuccoed and painted, with a platform (adosada) on its front and a temple on top, inside a vast walled enclosure."),
             C: dict(model="teotihuacan/pyramid-of-the-sun-650", note="The temple on the summit burned and the stairs and platforms at its foot were wrecked in the destruction of the centre.", confidence="interpretation"),
             A: dict(model="teotihuacan/pyramid-of-the-sun-1500", name="Tonatiuh Itzacual, the Sun's pyramid", note="A huge overgrown hill. Here, the Aztecs said, Nanahuatzin rose as the Sun after the gods' sacrifice; pilgrims climbed it to make offerings.", confidence="interpretation"),
         },
         summary="The largest structure of the city and one of the largest in ancient America: a stepped pyramid about 225 m a side and 65 m high, built over a cave and facing the setting sun.",
         details=[
             "Its core of earth, adobe and rubble was faced with stone and lime plaster. A cave-like tunnel found under it in 1971 runs about 100 m to a chamber below the centre. Leopoldo Batres stripped several metres of its outer face in 1905–10 and rebuilt it with five bodies; whether the original had tableros, as he restored, is uncertain.",
             "The miniature shows the usual reconstruction: five talud-tablero bodies, a stair broken at each terrace, the adosada platform in front and a temple with merlons on the summit. The temple's form, its colours and the exact profile are reconstruction.",
         ],
         built="c. 100–250 CE (dates debated)", function="Temple platform, perhaps of the storm or fire god", confidence="reconstruction",
         sourceIds=["wiki-sun", "sugiyama-sun-2013", "batres-1906", "millon-1973", "cowgill-2015"], activity=dict(figures=60, radius=160)),

    dict(id="xalla", placeId="xalla", name="Xalla", category="civic",
         latlon=G(-260, 420), rotation=SOUTH, footprint=(130, 120), scale=1.0, model="teotihuacan/xalla",
         activePeriods=[X, C],
         variants={
             M: dict(note="Earlier buildings stood here; the compound in its known form belongs to the following centuries.", confidence="interpretation"),
             X: dict(note="A walled complex of four large buildings round a plaza with a small temple at its centre, perhaps a palace of the city's rulers (Manzanilla's hypothesis)."),
             C: dict(model="teotihuacan/xalla-650", note="Burned around 550 with the centre; its sculptures were broken and scattered, which suggests the fire was aimed at the rulers.", confidence="interpretation"),
             A: dict(note="Buried under low mounds north of the Sun pyramid.", confidence="interpretation"),
         },
         summary="A walled palace compound north of the Sun pyramid, with four large buildings round a central plaza and temple, which Linda Manzanilla has argued was the residence of the city's rulers.",
         details=[
             "Excavated by Manzanilla and Leonardo López Luján from 1997, Xalla covers about 1.5 ha. Its buildings stand on talud-tablero platforms round a plaza; finds include stone sculptures of a lion-like feline, a figure of a god of fire and foreign stone. All were burned and smashed in the 6th century.",
             "The miniature shows four platforms with long porticoed buildings, the central temple and the enclosing wall. The superstructures are reconstruction.",
         ],
         built="c. 350–550 CE", function="Palace (probably)", confidence="interpretation",
         sourceIds=["wiki-teotihuacan", "manzanilla", "cowgill-2015"], activity=dict(figures=16, radius=60)),

    dict(id="tepantitla", placeId="tepantitla", name="Tepantitla", category="district",
         latlon=G(-400, 560), rotation=SOUTH, footprint=(60, 60), scale=1.0, model="teotihuacan/tepantitla",
         activePeriods=[X, C],
         variants={
             M: dict(note="An apartment compound may already stand here; the painted rooms belong to the later rebuildings.", confidence="interpretation"),
             X: dict(note="An apartment compound east of the Sun pyramid whose portico walls carry the mural Alfonso Caso called Tlalocan: a goddess above a paradise of water, trees and playing figures."),
             C: dict(note="Still standing, perhaps still lived in; some date its murals as late as 550–650.", confidence="interpretation"),
             A: dict(note="Buried in the fields; excavated in 1942.", confidence="interpretation"),
         },
         summary="An apartment compound behind the Sun pyramid painted with one of the most famous murals of ancient America: the so-called Tlalocan, with a goddess above and tiny figures playing, swimming and singing below.",
         details=[
             "Caso read the painting as Tlalocan, the rain god's paradise; many now see the central figure as the Great Goddess, with water and seeds flowing from her hands. The lower register shows more than a hundred small figures playing ball with sticks, swimming, chasing butterflies and singing, with speech scrolls.",
             "The miniature shows a walled compound with flat roofs, rooms round porticoed patios and red mural bands in the main portico. The plan is simplified.",
         ],
         built="c. 450–650 CE (murals; dates debated)", function="Apartment compound", confidence="reconstruction",
         sourceIds=["wiki-tlalocan", "wiki-great-goddess", "berrin-pasztory", "pasztory-1997"], activity=dict(figures=10, radius=40)),

    dict(id="tetitla", placeId="tetitla", name="Tetitla", category="district",
         latlon=G(-800, -480), rotation=SOUTH, footprint=(64, 64), scale=1.0, model="teotihuacan/tetitla",
         activePeriods=[X, C],
         variants={
             M: dict(note="An earlier compound stood here; the excavated building is mainly of the 4th to 6th centuries.", confidence="interpretation"),
             X: dict(note="A wealthy compound some 500 m west of the avenue, its rooms painted with goddesses scattering jade and water, jaguars, and some Maya-style glyphs."),
             C: dict(note="Still occupied for a time after the centre burned; rooms were later abandoned and filled with rubble.", confidence="interpretation"),
             A: dict(note="Under the fields; excavated by Laurette Séjourné in 1963–64.", confidence="interpretation"),
         },
         summary="A large apartment compound west of the Avenue of the Dead with more than a hundred mural fragments, among them the 'Jade Goddess' scattering water and treasures.",
         details=[
             "Excavated by Laurette Séjourné in 1963–64, Tetitla has some 120 painted walls: goddesses with outstretched hands dropping jade and streams of water, coyotes and jaguars in headdresses, and a group of paintings with Maya-style figures and glyphs, perhaps made by or for Maya visitors.",
             "The miniature shows the walled compound with several patios, the porticoes painted red, a small temple on the main patio and the outer wall's sloping base. Room layout is simplified.",
         ],
         built="c. 350–650 CE", function="Apartment compound", confidence="reconstruction",
         sourceIds=["wiki-teotihuacan", "wiki-great-goddess", "berrin-pasztory", "pasztory-1997"], activity=dict(figures=10, radius=40)),

    dict(id="atetelco", placeId="atetelco", name="Atetelco", category="district",
         latlon=G(-900, -950), rotation=SOUTH, footprint=(64, 64), scale=1.0, model="teotihuacan/atetelco",
         activePeriods=[X, C],
         variants={
             M: dict(note="The first part, the White Patio, may date from about 300–400; the rest is later.", confidence="interpretation"),
             X: dict(note="A compound whose White Patio has three porticoes painted in red with processions of coyotes, jaguars and warriors in feathered costume."),
             C: dict(note="Probably abandoned or dwindling after the burning of the centre.", confidence="interpretation"),
             A: dict(note="Buried in the fields; excavated and restored in the 1940s and 1950s.", confidence="interpretation"),
         },
         summary="An apartment compound on the western side of the city, known for its White Patio, where porticoes on three sides were painted with netted jaguars and coyotes and armed warriors.",
         details=[
             "The White Patio has a small altar at its centre and a temple platform on each of three sides, its porticoes painted with red-and-white net patterns enclosing coyotes and jaguars, and processions of richly dressed figures with spearthrowers. They are read as images of military orders.",
             "The miniature shows the walled compound with its three-temple patio, the red mural bands, rooms round other patios, and flat roofs. Details of the rear rooms are simplified.",
         ],
         built="c. 300–550 CE", function="Apartment compound", confidence="reconstruction",
         sourceIds=["wiki-teotihuacan", "headrick", "berrin-pasztory"], activity=dict(figures=10, radius=40)),

    # ------------------------------------------------------------ the avenue
    dict(id="avenue-of-the-dead", placeId="avenue-of-the-dead", name="Avenue of the Dead: the sunken plazas", category="monument",
         latlon=G(-1150, 0), rotation=SOUTH, footprint=(130, 440), scale=1.0, model="teotihuacan/avenue-of-the-dead",
         activePeriods=[M, X, C, A],
         variants={
             T: dict(note="A way probably already ran here between the river and the new Sun pyramid, but the platforms and sunken plazas are not yet built.", confidence="interpretation"),
             M: dict(note="The avenue is paved and closed by cross-walls into a stair of sunken plazas, each lower than the next to the north; temple platforms line both sides."),
             X: dict(note="The busiest stretch of the avenue: the Street of the Dead complex, the Superposed Buildings and the Viking group line it, all painted red and white."),
             C: dict(model="teotihuacan/avenue-of-the-dead-650", note="Its temples burned, their sculptures smashed and scattered on the paving; heaps of debris block the plazas.", confidence="interpretation"),
             A: dict(model="teotihuacan/avenue-of-the-dead-1500", name="Miccaotli", note="A path between lines of grassy mounds, which the Aztecs took for the tombs of ancient kings.", confidence="interpretation"),
         },
         summary="The stretch of the Avenue of the Dead between the Sun pyramid and the San Juan river, where cross-walls divide the 40 m wide avenue into sunken plazas lined with temple platforms.",
         details=[
             "The avenue rises about 30 m from the Ciudadela to the Moon. North of the river it is crossed by walls with stairs on both sides that divide it into sunken plazas. Along its sides stand the Street of the Dead complex, a group of palaces and temples, the Superposed Buildings and the Viking group, named after the Viking Fund that paid for its excavation, where sheets of mica lay under a floor.",
             "The miniature shows a section of about 440 m: the paved avenue, four cross-walls with stairs, and talud-tablero platforms with small temples along both sides. The number of platforms is simplified.",
         ],
         built="c. 200–450 CE", function="Processional avenue and temple platforms", confidence="reconstruction",
         sourceIds=["wiki-teotihuacan", "millon-1973", "cowgill-2015"], activity=dict(figures=80, radius=200)),

    dict(id="san-juan-crossing", placeId="san-juan-crossing", name="Crossing of the Río San Juan", category="monument",
         latlon=G(-1650, 0), rotation=SOUTH, footprint=(120, 90), scale=1.0, model="teotihuacan/san-juan-crossing",
         activePeriods=[M, X, C],
         variants={
             T: dict(note="The river still winds through its natural bed here; it will be straightened to the grid.", confidence="interpretation"),
             M: dict(note="The river runs straight across the avenue in a channel at right angles to it, bent from its old course to fit the city's grid."),
             X: dict(note="A stone-lined channel crossing the avenue, with platforms on both banks."),
             C: dict(note="Unmaintained; silt and debris from the burned buildings fill the channel.", confidence="interpretation"),
             A: dict(note="The canalised bed survives, its banks overgrown with willows.", confidence="interpretation"),
         },
         summary="The point where the canalised San Juan river crosses the Avenue of the Dead at right angles, evidence that the builders reshaped even the river to fit their grid.",
         details=[
             "Millon's survey showed that the San Juan runs straight and at right angles to the avenue where it crosses the centre of the city, unlike its course upstream and downstream; the river was deliberately canalised. How the avenue crossed it, by a bridge, a ford or a culvert, is not known.",
             "The miniature shows a stone-lined channel, the avenue's paving stepping down to it, a crossing of stone slabs and platforms on the banks. The crossing itself is a guess.",
         ],
         built="c. 200–300 CE", function="River channel and crossing", confidence="interpretation",
         sourceIds=["wiki-teotihuacan", "millon-1973", "cowgill-2015"], activity=dict(figures=12, radius=50)),

    # ------------------------------------------------------------ the Ciudadela and the Great Compound
    dict(id="ciudadela", placeId="ciudadela", name="The Ciudadela", category="civic",
         latlon=G(-1960, 225), rotation=WEST, footprint=(400, 400), scale=1.0, model="teotihuacan/ciudadela",
         activePeriods=[M, X, C, A],
         variants={
             T: dict(note="Not yet built; the ground east of the river is open, with scattered houses.", confidence="interpretation"),
             M: dict(note="Built round 200: a vast square enclosure of platforms carrying fifteen small temple-pyramids, round a plaza with the Feathered Serpent Pyramid at its back."),
             X: dict(note="The political centre of the city, with residential compounds beside the Feathered Serpent Pyramid, perhaps the rulers' palaces."),
             C: dict(model="teotihuacan/ciudadela-650", note="Burned and wrecked with the rest of the centre; the temples on its platforms gone.", confidence="interpretation"),
             A: dict(model="teotihuacan/ciudadela-1500", note="A great square of grassy ridges; the Spanish later called it the Ciudadela, 'citadel', taking it for a fortress.", confidence="interpretation"),
         },
         summary="A walled enclosure about 400 m square on the east side of the avenue, its platforms topped by fifteen temple-pyramids round a plaza that could hold tens of thousands; the setting of the Feathered Serpent Pyramid.",
         details=[
             "The Ciudadela's broad platforms, about 7 m high, enclose a sunken plaza of some 4.4 ha; Millon estimated that it could hold 100,000 people. Behind the Feathered Serpent Pyramid stood two residential compounds, often taken for the rulers' palaces, though this is debated.",
             "The miniature shows the enclosing platforms, a broad stair from the avenue, fifteen small talud-tablero pyramids with stairs facing the plaza, and the compounds at the back. The Feathered Serpent Pyramid is a separate model.",
         ],
         built="c. 200–250 CE", function="Ceremonial and political enclosure", confidence="reconstruction",
         sourceIds=["wiki-feathered-serpent", "wiki-teotihuacan", "sugiyama-2005", "millon-1973"], activity=dict(figures=50, radius=180)),

    dict(id="temple-of-the-feathered-serpent", placeId="feathered-serpent-pyramid", name="Temple of the Feathered Serpent", category="temple",
         latlon=G(-1960, 300), rotation=WEST, footprint=(80, 100), scale=1.0, model="teotihuacan/temple-of-the-feathered-serpent",
         activePeriods=[M, X, C, A],
         variants={
             T: dict(note="Not yet built.", confidence="interpretation"),
             M: dict(note="Newly finished: six talud-tablero tiers carved with feathered serpents and headdress heads, painted, with some 200 sacrificed people buried in and around it."),
             X: dict(model="teotihuacan/temple-of-the-feathered-serpent-adosada", note="Around 350 a plain talud-tablero platform (the adosada) was built against its front, hiding the carved facade, and many sculptures were torn down: a political change, perhaps.", confidence="reconstruction"),
             C: dict(model="teotihuacan/temple-of-the-feathered-serpent-650", note="The temple on the adosada burned with the rest of the centre.", confidence="interpretation"),
             A: dict(model="teotihuacan/temple-of-the-feathered-serpent-1500", note="A grassy mound in the Ciudadela; its carved front stayed hidden until excavated in 1917–20.", confidence="interpretation"),
         },
         summary="The third-largest pyramid of Teotihuacan, its six tiers covered with the projecting heads of feathered serpents and of a headdress-serpent, dedicated with about 200 human sacrifices.",
         details=[
             "Built about 200–250 CE, it measured about 65 m a side and 20 m high. Its tableros carry undulating feathered serpents in relief with hundreds of tenoned heads: the serpent with its feather collar alternating with a mosaic headdress, read as Cipactli or a war serpent. Sugiyama and others found some 200 sacrificed men and women buried in groups, many dressed as warriors.",
             "The miniature shows the six tiers with their relief and projecting heads, the stair with serpent-headed balustrades and the temple on top. The colours follow traces of paint; the temple's form is reconstruction. Variant: the plainer adosada platform of c. 350 covering the front.",
         ],
         built="c. 200–250 CE; adosada c. 350", function="Temple of the Feathered Serpent", confidence="reconstruction",
         sourceIds=["wiki-feathered-serpent", "sugiyama-2005", "wiki-talud-tablero", "wiki-feathered-serpent-deity"], activity=dict(figures=24, radius=60)),

    dict(id="great-compound", placeId="great-compound", name="The Great Compound", category="commercial",
         latlon=G(-1960, -235), rotation=EAST, footprint=(380, 370), scale=1.0, model="teotihuacan/great-compound",
         activePeriods=[M, X, C],
         variants={
             T: dict(note="Not yet built; open ground west of the way.", confidence="interpretation"),
             M: dict(note="Two great platforms flank a plaza opening onto the avenue, facing the Ciudadela across it."),
             X: dict(note="Perhaps the city's great market, as Millon proposed: the largest open space in the city, opposite the political centre.", confidence="interpretation"),
             C: dict(note="Abandoned as a public space after the destruction of the centre.", confidence="interpretation"),
             A: dict(note="Ploughed fields with two long low ridges.", confidence="interpretation"),
         },
         summary="The largest complex of the city, across the avenue from the Ciudadela: two huge platforms flanking an open plaza that René Millon thought was the main marketplace.",
         details=[
             "The Great Compound is barely excavated. Its plaza is bigger than the Ciudadela's, and unlike most complexes it has few temples; with the Ciudadela it marks the centre of the cross formed by the Avenue of the Dead and the East and West avenues. A market is a hypothesis: no stalls have been excavated.",
             "The miniature shows the two platforms with long buildings on top, the plaza with market mats and awnings, and stairs facing the avenue. Everything above the platforms is interpretation.",
         ],
         built="c. 200–300 CE", function="Marketplace or administrative centre (hypothesis)", confidence="interpretation",
         sourceIds=["wiki-teotihuacan", "millon-1973", "cowgill-2015"], activity=dict(figures=90, radius=170)),

    # ------------------------------------------------------------ the foreign barrios
    dict(id="oaxaca-barrio", placeId="tlailotlacan", name="Tlailotlacan, the Oaxaca barrio", category="district",
         latlon=G(-1500, -2400), rotation=SOUTH, footprint=(120, 120), scale=1.0, model="teotihuacan/oaxaca-barrio",
         activePeriods=[M, X],
         variants={
             T: dict(note="Fields on the western edge of the settlement; the Zapotec settlers have not yet come.", confidence="interpretation"),
             M: dict(note="Zapotec families from the Valley of Oaxaca settle here around 200–250, in compounds of local style but keeping their pottery and tombs."),
             X: dict(note="Some 600 to 1,000 people of Zapotec descent, still burying their dead in stone tombs with Oaxacan urns."),
             C: dict(note="The enclave seems to break up after the collapse of the centre; some families perhaps returned to Oaxaca.", confidence="interpretation"),
         },
         summary="An enclave of Zapotec families from Oaxaca on the western edge of the city, who lived in Teotihuacan-style compounds but kept their own burial customs for four centuries.",
         details=[
             "Excavations by Michael Spence and Evelyn Rattray found Oaxacan grey pottery made locally, funerary urns, and a stone-lined tomb with a carved jamb in Zapotec style. Bones show that some people were born in Oaxaca or moved back and forth. The barrio lay some 2–3 km west of the avenue.",
             "The miniature shows a walled compound with its patios, a Zapotec-style tomb entrance in the main patio, a carved stela, and a smaller compound with fields. Layout simplified.",
         ],
         built="c. 200 CE", function="Residential barrio", confidence="reconstruction",
         sourceIds=["wiki-teotihuacan", "wiki-zapotec", "spence-1992", "rattray-1987"], activity=dict(figures=16, radius=70)),

    dict(id="merchants-barrio", placeId="merchants-barrio", name="The Merchants' barrio", category="district",
         latlon=G(-900, 1700), rotation=SOUTH, footprint=(140, 120), scale=1.0, model="teotihuacan/merchants-barrio",
         activePeriods=[M, X],
         variants={
             T: dict(note="Fields on the eastern edge of the settlement.", confidence="interpretation"),
             M: dict(note="Families from the Gulf coast and the Maya lowlands settle here, building round adobe houses unlike anything else in the city."),
             X: dict(note="A trading quarter on the road east, with Gulf-coast and Maya pottery, round houses and Teotihuacan-style compounds side by side."),
             C: dict(note="Abandoned or nearly so after the collapse of the city's long-distance trade.", confidence="interpretation"),
         },
         summary="A barrio on the eastern edge of the city where Evelyn Rattray found round adobe buildings and pottery from the Gulf coast and the Maya lowlands: probably the home of foreign traders.",
         details=[
             "The round structures, up to 10 m across, are without parallel elsewhere in the city; the pottery includes fine wares from Veracruz and the Maya area. The barrio stood near the routes east toward the Gulf, and its people are thought to have been merchants or their agents.",
             "The miniature shows round adobe houses with conical thatch beside a rectangular compound, bales and jars of trade goods. The round houses' roofs are a guess.",
         ],
         built="c. 200–550 CE", function="Residential barrio of foreign traders", confidence="interpretation",
         sourceIds=["wiki-teotihuacan", "rattray-1987", "cowgill-2015"], activity=dict(figures=16, radius=70)),
]
