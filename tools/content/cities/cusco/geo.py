# Cusco / Qusqu: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
import math

KILLKE = ["killke-1300"]
IMPERIAL = ["pachacuti-1470", "huayna-1530"]
COLONIAL = ["colonial-1650"]
INCA = KILLKE + IMPERIAL
LATER = IMPERIAL + COLONIAL
ALL = KILLKE + IMPERIAL + COLONIAL

# The core of Cusco is laid out on a grid turned about 45 degrees: streets run north-west to
# south-east (u) and south-west to north-east (v). UV(u, v) gives (lat, lon) for a point u metres
# south-east and v metres north-east of the middle of the Plaza de Armas (Haukaypata).
P0 = (-13.5166, -71.9787)
KX, KY = 111320.0 * math.cos(math.radians(13.52)), 110950.0


def UV(u, v):
    e = 0.7071 * (u + v)
    n = 0.7071 * (v - u)
    return (round(P0[0] + n / KY, 5), round(P0[1] + e / KX, 5))


def Q(u0, u1, v0, v1):
    """A block of the turned grid between u0..u1 and v0..v1."""
    return [UV(u0, v0), UV(u1, v0), UV(u1, v1), UV(u0, v1)]


CITY = dict(
    name="Cusco", subtitle="Qusqu, Navel of the Inca World",
    description="Cusco from the small Killke-period town of the early Incas to the Spanish city rebuilt after the earthquake of 1650: the core between the canalised Saphy and Tullumayo, Sacsayhuamán on the hill above, and the four roads leaving for the four quarters of Tawantinsuyu. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="huayna-1530",
    world=dict(heightScale=1.0, walls=["#B9AE98", "#AFA38B", "#C4B9A2"], roofs=["#A8925C", "#9C8854"]),
    camera=dict(target=(-13.5160, -71.9785), distance=34),
)
FRAME = ((-13.4980, -72.0020), (-13.5380, -71.9520))
PALETTE = dict(parchment="#E6D4AC", ink="#634634", water="#5F8688", hill="#7A7A58", road="#8A6A4A")
COMPASS = (-13.5020, -71.9570)
CARTOUCHE = (-13.5372, -72.0010)

PERIODS = [
    dict(id="killke-1300", label="Killke-period Qusqu", year=1300, startYear=1100, endYear=1437,
         summary="Before the empire, Cusco is one small polity among several in the valley. The Inca lineages live in fieldstone compounds on the tongue of land between the Saphy and Tullumayo streams, with the early Inticancha, the sun's enclosure, at its lower end. The valley floor is wet; villages of other groups sit on the slopes. Killke pottery, with its black and red geometric designs, marks the period.",
         population="a few thousand at most (archaeological guess)",
         feel="Smoke from dung fires, the gurgle of the unchannelled streams, dogs barking from compound to compound, and frogs in the reed beds where the great plaza will be.",
         style="andean",
         houses=dict(title="Fieldstone compounds of the early Incas", text="A few rooms of rough fieldstone set in mud, under steep ichu-grass thatch, round a small walled yard with a grinding stone and a hearth. Guinea pigs run along the walls; maize dries on the roof."),
         outskirts=dict(title="Hamlets of the valley", text="Clusters of round and square houses of other groups, the Alcabizas, Sañu and Ayarmaca among them, beside potato and maize plots on the slopes above the marsh.")),
    dict(id="pachacuti-1470", label="Pachacuti's rebuilding", year=1470, startYear=1438, endYear=1492,
         summary="After beating the Chanka (traditionally in 1438), Pachacuti Inca Yupanqui rebuilt Cusco as an imperial capital. The Saphy and Tullumayo were walled into stone channels, the marsh drained into a great plaza, and the city laid out in blocks of kancha in fitted ashlar. The Coricancha was rebuilt and sheathed in gold; Sacsayhuamán was begun with labour drafted from the provinces.",
         population="perhaps 20,000–40,000 in the core and the valley (estimates vary widely)",
         feel="Ringing of stone hammers from dawn, the rumble of blocks dragged on ramps by gangs singing work songs, dust over the half-built walls, and the drums of a victory feast in the plaza.",
         style="andean",
         houses=dict(title="New kancha of fitted stone", text="Rectangular walled compounds, each with three to eight one-room houses round a court, built for the royal lineages and the lords of the conquered provinces. The best are of fitted andesite with trapezoidal doors; others of fieldstone and clay, plastered and painted."),
         outskirts=dict(title="Terraces and resettled villages", text="Pachacuti moved the valley's old inhabitants out to make room. Their villages now sit beyond the rivers among new terraces of maize, and new suburbs house the people sent from the provinces.")),
    dict(id="huayna-1530", label="Navel of the Inca world", year=1530, startYear=1493, endYear=1533,
         summary="The capital of Tawantinsuyu at its height under Huayna Capac and in the civil war after his death. Royal compounds of fitted stone line the streets, each dead Inca kept in his palace by his lineage. The double plaza of Haukaypata and Kusipata, with its ushnu, can hold the whole city; Sacsayhuamán's three zigzag walls and towers stand above, and four roads leave for the four quarters.",
         population="perhaps 100,000 or more in the valley (Spanish estimates; very uncertain)",
         feel="Gold glinting on the Coricancha's band at noon, conch trumpets and drums in the plaza, the sour smell of chicha from every house, and lines of llamas jingling in from the roads.",
         style="andean",
         houses=dict(title="Royal and noble kancha", text="Compounds of fitted stone with battered walls, trapezoidal doors and niches, single rooms round a court under steep ichu thatch tied down with rope. A lineage lived, cooked, brewed and stored together inside; only one or two doors gave onto the narrow street with its stone gutter."),
         outskirts=dict(title="Suburbs of the provinces", text="Around the core lived the lords of the conquered peoples, each group in its own quarter in its own dress and headgear, among terraces, storehouses and the houses of servants, potters and stonemasons.")),
    dict(id="colonial-1650", label="Spanish Cusco after the earthquake", year=1650, startYear=1534, endYear=1720,
         summary="Spanish Cusco stands on Inca foundations: Santo Domingo on the Coricancha, La Compañía on Amarukancha, Santa Catalina in the Aqllawasi, the cathedral on Kiswarkancha. Mansions with carved balconies and tile roofs rise on Inca walls, and Haukaypata is cut down into the Plaza de Armas. The earthquake of 31 March 1650 throws much of it down; the city is rebuilt in baroque over the next fifty years.",
         population="perhaps 20,000–30,000",
         feel="Church bells answering each other across the tile roofs, Quechua and Spanish shouted together in the market, incense and candle smoke, and chicha jars hanging from poles over tavern doors.",
         style="early-modern",
         houses=dict(title="Casonas on Inca walls", text="Two-storey houses round arcaded patios, built of adobe and reused stone on the lower courses of Inca walls, with carved wooden balconies over the street and roofs of red tile. Shops and chicherías open in the ground-floor rooms."),
         outskirts=dict(title="Indian parishes", text="Around the centre lie the parishes of the native people, San Blas, Santa Ana, Belén, San Cristóbal and the Hospital de Naturales, each with its church and plaza: adobe houses with tile or thatch, gardens and workshops of potters, weavers and painters.")),
]

# ---------------------------------------------------------------- water and hills
# Points along the Saphy (Huatanay) canal on the south-west side of the core, upstream to downstream
SAPHY = [(-13.4980, -71.9832), (-13.5040, -71.9850), (-13.5090, -71.9862), (-13.5125, -71.9850), (-13.5150, -71.9826), UV(-150, -75), UV(0, -78), UV(150, -80),
         UV(300, -82), UV(450, -82), UV(600, -80), (-13.5222, -71.9735)]
TULLUMAYO = [(-13.4980, -71.9688), (-13.5050, -71.9702), (-13.5100, -71.9716), (-13.5140, -71.9725), (-13.5185, -71.9727), (-13.5222, -71.9735)]
HUATANAY = [(-13.5222, -71.9735), (-13.5252, -71.9692), (-13.5290, -71.9632), (-13.5325, -71.9575), (-13.5350, -71.9520)]
CHUNCHULMAYO = [(-13.5300, -71.9960), (-13.5290, -71.9880), (-13.5275, -71.9800), (-13.5262, -71.9730), (-13.5266, -71.9670)]

WATER = [
    dict(id="saphy", name="Saphy (Huatanay)", path=SAPHY, width=10, periods=LATER,
         blurb="The 'root' stream, coming down past Sacsayhuamán and through the city between the two plazas. Pachacuti had it walled into a stone channel with stone-paved bed, crossed by slab bridges; in the colonial city it became a smelly open sewer and was later vaulted over under the Avenida El Sol."),
    dict(id="saphy-killke", name="Saphy stream", path=SAPHY, width=18, periods=KILLKE,
         blurb="Still a wandering mountain stream, spreading into marsh on the flat ground where the great plaza would later be laid out."),
    dict(id="tullumayo", name="Tullumayo", path=TULLUMAYO, width=9, periods=LATER,
         blurb="The 'bone river' on the east side of the core, also walled into a stone channel. The puma-shaped plan of the usual reading sets the city's body between it and the Saphy."),
    dict(id="tullumayo-killke", name="Tullumayo stream", path=TULLUMAYO, width=14, periods=KILLKE),
    dict(id="huatanay", name="Huatanay", path=HUATANAY, width=16,
         blurb="Below the meeting of the two streams at Pumachupan the river runs south-east down the valley toward Lake Muina and the Vilcanota. Its banks were terraced and irrigated maize land."),
    dict(id="chunchulmayo", name="Chunchulmayo", path=CHUNCHULMAYO, width=8,
         blurb="A stream draining the slopes of Puquín south-west of the city, joining the Huatanay below the city."),
]

HILLS = [
    dict(id="sacsayhuaman-hill", name="Sacsayhuamán hill", center=(-13.5092, -71.9818), radius=260, label=False,
         blurb="The steep hill north of the city, the puma's head in the usual reading of the plan. Its summit carries the towers of Sacsayhuamán; its gentler north side, the zigzag walls."),
    dict(id="suchuna", name="Suchuna (Rodadero)", center=(-13.5060, -71.9805), radius=200,
         blurb="The polished rock dome across the esplanade from Sacsayhuamán's walls, cut with terraces and a carved 'throne of the Inca' facing the ramparts."),
    dict(id="picchu", name="Picchu", center=(-13.5135, -71.9935), radius=360,
         blurb="The hill west of the city over which the Chinchaysuyu road climbed. From its top, observers watched the sun set behind pillars on the horizon to fix the time of planting."),
    dict(id="puquin", name="Puquín", center=(-13.5268, -71.9905), radius=380,
         blurb="A hill south-west of Cusco, sacred to the Inca with a shrine where the Cuntisuyu road left the valley; its slopes are cut with terraces."),
    dict(id="socorro", name="Qenqo hill", center=(-13.5075, -71.9735), radius=220, label=False,
         blurb="Limestone outcrops north-east of the city, carved into shrines of which Qenqo is the largest."),
    dict(id="mantoqalla", name="Mantoqalla", center=(-13.5015, -71.9625), radius=330,
         blurb="The hill over which the Antisuyu road climbed toward Pisac and the forests of the east."),
    dict(id="huanacauri", name="Toward Huanacauri", center=(-13.5368, -71.9655), radius=420,
         blurb="The ridge south of the valley rising toward Huanacauri, the mountain where, in the founding legend, one of the Ayar brothers turned to stone; it was one of the most sacred shrines of the Inca, some 9 km south-east of the city."),
]

MARSH = [
    dict(name="Marsh of the valley floor", polygon=Q(-140, 120, -70, 70), periods=KILLKE),
    dict(name="Wet ground at Pumachupan", polygon=[UV(640, -40), UV(780, -20), UV(800, 120), UV(660, 100)], periods=KILLKE),
]

# ---------------------------------------------------------------- roads
_IMP = [
    dict(id="chinchaysuyu", name="Road to Chinchaysuyu", width=12, style="major", labelled=True,
         path=[UV(-90, -58), UV(-200, -59), (-13.5146, -71.9822), (-13.5141, -71.9832), (-13.5134, -71.9845), (-13.5130, -71.9868), (-13.5115, -71.9905), (-13.5085, -71.9960), (-13.5040, -72.0020)],
         blurb="The road of the north-western quarter, the largest, climbing over Carmenca toward Xaquixaguana, Vilcashuamán, Cajamarca and Quito, 2,000 km away. Chaskis covered it in relays."),
    dict(id="antisuyu", name="Road to Antisuyu", width=10, style="major", labelled=True,
         path=[UV(75, 62), UV(95, 330), UV(110, 455), (-13.5132, -71.9735), (-13.5130, -71.9730), (-13.5126, -71.9717), (-13.5110, -71.9690), (-13.5070, -71.9640), (-13.5020, -71.9580), (-13.4982, -71.9535)],
         blurb="The road of the north-eastern quarter, up past Toqokachi and over the hills to Pisac, Paucartambo and the forests of the Amazon slope, source of coca, feathers and hardwoods."),
    dict(id="collasuyu", name="Road to Collasuyu", width=12, style="major", labelled=True,
         path=[UV(90, -70), UV(300, -71), UV(470, -70), UV(600, -66), UV(760, -30), UV(800, -20), UV(850, -5), (-13.5238, -71.9690), (-13.5268, -71.9630), (-13.5305, -71.9570), (-13.5332, -71.9520)],
         blurb="The road of the south-eastern quarter, down the Huatanay valley and on to Lake Titicaca, Potosí's future mountain and Chile. Huayna Capac's armies and the llama trains of the Altiplano came in along it."),
    dict(id="cuntisuyu", name="Road to Cuntisuyu", width=10, style="major", labelled=True,
         path=[UV(-30, -65), UV(-30, -95), (-13.5190, -71.9822), (-13.5215, -71.9840), (-13.5260, -71.9865), (-13.5320, -71.9905), (-13.5378, -71.9950)],
         blurb="The road of the south-western quarter, the smallest, leaving Kusipata past Puquín toward Arequipa and the Pacific coast."),
    dict(id="hatun-rumiyoc-st", name="Street of Hatun Rumiyoc", width=6, style="minor",
         path=[UV(75, 62), UV(95, 330)],
         blurb="A narrow street walled on both sides with the finest fitted masonry in the city, the palace of Inca Roca on one side."),
    dict(id="loreto-st", name="Intikijllu (street of the sun)", width=6, style="minor",
         path=[UV(90, 17), UV(480, 20)],
         blurb="A walled lane between Amarukancha and the Aqllawasi leading from Haukaypata toward the Coricancha; Calle Loreto today. Its Inca walls still stand."),
    dict(id="arequipa-st", name="Street of the Aqllawasi", width=6, style="minor", path=[UV(190, -66), UV(190, 300)]),
    dict(id="maruri-st", name="Street of Pucamarca", width=6, style="minor", path=[UV(385, -66), UV(385, 300)]),
    dict(id="sacsayhuaman-way", name="Way up to Sacsayhuamán", width=6, style="minor",
         path=[UV(-90, 62), (-13.5140, -71.9800), (-13.5120, -71.9800), (-13.5106, -71.9808)]),
    dict(id="qenqo-way", name="Path to Qenqo", width=5, style="minor",
         path=[(-13.5106, -71.9808), (-13.5095, -71.9780), (-13.5085, -71.9748), (-13.5083, -71.9733)]),
]
ROADS = [dict(r, periods=IMPERIAL) for r in _IMP] + [
    # Killke tracks
    dict(id="killke-track-n", name="Track to the north", width=5, style="minor", periods=KILLKE,
         path=[UV(200, 60), UV(60, 200), (-13.5140, -71.9800), (-13.5100, -71.9818), (-13.5040, -71.9850)]),
    dict(id="killke-track-se", name="Track down the valley", width=5, style="minor", periods=KILLKE,
         path=[UV(470, -64), UV(600, -66), UV(760, -30), UV(850, -5), (-13.5238, -71.9690), (-13.5268, -71.9630), (-13.5305, -71.9570), (-13.5332, -71.9520)]),
    dict(id="killke-track-w", name="Track to Carmenca", width=5, style="minor", periods=KILLKE,
         path=[UV(200, 60), UV(-90, -50), (-13.5146, -71.9822), (-13.5134, -71.9845), (-13.5130, -71.9868), (-13.5115, -71.9905)]),
] + [dict(r, periods=COLONIAL) for r in [
    dict(id="camino-lima", name="Camino Real to Lima", width=12, style="major", labelled=True,
         path=[UV(-90, -58), UV(-200, -59), (-13.5146, -71.9822), (-13.5141, -71.9832), (-13.5134, -71.9845), (-13.5130, -71.9868), (-13.5115, -71.9905), (-13.5085, -71.9960), (-13.5040, -72.0020)],
         blurb="The old Chinchaysuyu road, now the royal road to Lima, leaving past the parish church of Santa Ana on Carmenca hill and its arch."),
    dict(id="camino-potosi", name="Camino Real to Potosí", width=12, style="major", labelled=True,
         path=[UV(90, -70), UV(300, -71), UV(470, -70), UV(600, -66), UV(760, -30), UV(800, -20), UV(850, -5), (-13.5238, -71.9690), (-13.5268, -71.9630), (-13.5305, -71.9570), (-13.5332, -71.9520)],
         blurb="The old Collasuyu road, now the route of the mule trains to Potosí's silver mines and of Cusco's cloth, sugar and coca to the Altiplano."),
    dict(id="camino-arequipa", name="Road to Arequipa", width=10, style="major",
         path=[UV(-30, -65), UV(-30, -95), (-13.5190, -71.9822), (-13.5215, -71.9840), (-13.5260, -71.9865), (-13.5320, -71.9905), (-13.5378, -71.9950)]),
    dict(id="camino-paucartambo", name="Road to Paucartambo", width=10, style="major",
         path=[UV(75, 62), UV(95, 330), UV(110, 455), (-13.5132, -71.9735), (-13.5130, -71.9730), (-13.5126, -71.9717), (-13.5110, -71.9690), (-13.5070, -71.9640), (-13.5020, -71.9580), (-13.4982, -71.9535)]),
    dict(id="calle-triunfo", name="Calle del Triunfo and Hatun Rumiyoc", width=7, style="minor", labelled=True, path=[UV(75, 62), UV(95, 330)]),
    dict(id="calle-loreto", name="Calle Loreto", width=6, style="minor", labelled=True, path=[UV(90, 17), UV(480, 20)]),
    dict(id="calle-arequipa", name="Calle Arequipa", width=6, style="minor", path=[UV(190, -66), UV(190, 300)]),
    dict(id="calle-maruri", name="Calle Maruri", width=6, style="minor", path=[UV(385, -66), UV(385, 300)]),
    dict(id="calle-mantas", name="Calle Mantas", width=7, style="minor", path=[UV(-80, -95), UV(-120, -230), UV(-170, -380)]),
    dict(id="cuesta-san-cristobal", name="Cuesta de San Cristóbal", width=6, style="minor",
         path=[UV(-90, 62), (-13.5140, -71.9800), (-13.5120, -71.9800), (-13.5106, -71.9808)]),
    dict(id="calle-plateros", name="Calle Plateros and Saphy", width=6, style="minor", path=[UV(-180, -45), UV(-300, -40), UV(-420, -50)]),
]]

BRIDGES = [
    dict(id="kusipata-bridge", name="Bridge between the plazas", path=[UV(-30, -66), UV(-30, -92)], build="stone", arches=1, periods=LATER,
         blurb="Flat slabs laid across the stone-walled Saphy joined Haukaypata and Kusipata; on great feast days the two plazas, and the river between them, were one crowd."),
    dict(id="carmenca-bridge", name="Carmenca bridge", path=[(-13.5141, -71.9832), (-13.5134, -71.9845)], build="stone", arches=1, periods=LATER,
         blurb="Where the Chinchaysuyu road crossed the Saphy on its way up Carmenca hill."),
    dict(id="pumachupan-bridge", name="Pumachupan bridge", path=[UV(800, -20), UV(850, -5)], build="stone", arches=1, periods=LATER,
         blurb="At the puma's tail, just above the meeting of the two rivers, the Collasuyu road crossed the Tullumayo."),
    dict(id="toqokachi-bridge", name="Toqokachi bridge", path=[(-13.5130, -71.9730), (-13.5126, -71.9717)], build="stone", arches=1, periods=LATER,
         blurb="The Antisuyu road's crossing of the Tullumayo below the hill of Toqokachi, later the parish of San Blas."),
    dict(id="killke-ford", name="Stepping stones", path=[(-13.5141, -71.9832), (-13.5134, -71.9845)], build="timber", arches=1, periods=KILLKE),
]

# ---------------------------------------------------------------- built-up areas
BLOCKS = [
    # killke-1300: the small town on the ridge and the hamlets around it
    dict(name="Early Inca compounds", polygon=Q(150, 470, -40, 120), density="dense", periods=KILLKE),
    dict(name="Upper compounds", polygon=Q(20, 250, 130, 300), density="loose", periods=KILLKE),
    dict(name="Compounds by the Inticancha", polygon=Q(480, 640, -50, 90), density="dense", periods=KILLKE),
    dict(name="Hamlet of Carmenca", polygon=[(-13.5118, -71.9880), (-13.5110, -71.9850), (-13.5130, -71.9852), (-13.5140, -71.9880)], density="loose", periods=KILLKE),
    dict(name="Hamlet of Toqokachi", polygon=[(-13.5150, -71.9765), (-13.5135, -71.9750), (-13.5125, -71.9765), (-13.5140, -71.9780)], density="loose", periods=KILLKE),
    dict(name="Hamlet of Cayaocache", polygon=[(-13.5200, -71.9850), (-13.5195, -71.9820), (-13.5220, -71.9815), (-13.5228, -71.9845)], density="loose", periods=KILLKE),
    dict(name="Hamlet of Coripata", polygon=[(-13.5240, -71.9760), (-13.5235, -71.9720), (-13.5255, -71.9715), (-13.5262, -71.9755)], density="loose", periods=KILLKE),

    # pachacuti-1470 and huayna-1530: the royal core between the rivers
    dict(name="Hanan Qusqu", polygon=Q(-90, 65, 66, 340), density="dense", periods=IMPERIAL),
    dict(name="Kancha of the north-west", polygon=Q(-320, -95, -48, 120), density="dense", periods=IMPERIAL),
    dict(name="Kancha below Qollqampata", polygon=Q(-330, -95, 125, 300), density="dense", periods=IMPERIAL),
    dict(name="Kancha east of the Aqllawasi", polygon=Q(85, 380, 22, 330), density="dense", periods=IMPERIAL),
    dict(name="Hurin Qusqu", polygon=Q(90, 480, -64, 13), density="dense", periods=IMPERIAL),
    dict(name="Kancha toward the Tullumayo", polygon=Q(390, 640, 22, 300), density="dense", periods=IMPERIAL),
    dict(name="Kancha round the Coricancha", polygon=Q(480, 700, -62, 18), density="dense", periods=IMPERIAL),
    dict(name="Toqokachi", polygon=[(-13.5150, -71.9768), (-13.5132, -71.9748), (-13.5118, -71.9762), (-13.5122, -71.9788), (-13.5138, -71.9790)], density="loose", periods=IMPERIAL),
    dict(name="Carmenca", polygon=[(-13.5122, -71.9895), (-13.5114, -71.9858), (-13.5128, -71.9852), (-13.5142, -71.9862), (-13.5145, -71.9895)], density="loose", periods=IMPERIAL),
    dict(name="Cayaocache", polygon=[(-13.5205, -71.9860), (-13.5195, -71.9830), (-13.5222, -71.9818), (-13.5240, -71.9848)], density="loose", periods=IMPERIAL),
    dict(name="Quarter beyond Kusipata", polygon=Q(-60, 180, -270, -110), density="loose", periods=IMPERIAL),
    dict(name="Coripata", polygon=[(-13.5245, -71.9770), (-13.5236, -71.9718), (-13.5258, -71.9708), (-13.5268, -71.9760)], density="loose", periods=IMPERIAL),
    dict(name="Munaysenqa", polygon=[(-13.5170, -71.9722), (-13.5150, -71.9700), (-13.5172, -71.9690), (-13.5195, -71.9712)], density="loose", periods=IMPERIAL),
    dict(name="Pumamarka", polygon=[(-13.5205, -71.9715), (-13.5195, -71.9690), (-13.5225, -71.9690), (-13.5228, -71.9712)], density="loose", periods=["huayna-1530"]),

    # colonial-1650: the Spanish traza on the Inca core, and the Indian parishes
    dict(name="Traza north of the plaza", polygon=Q(-90, 65, 66, 340), density="dense", periods=COLONIAL),
    dict(name="Traza west of the plaza", polygon=Q(-320, -95, -48, 120), density="dense", periods=COLONIAL),
    dict(name="San Cristóbal", polygon=Q(-330, -95, 125, 300), density="dense", periods=COLONIAL),
    dict(name="Santa Catalina and San Agustín", polygon=Q(85, 380, 22, 330), density="dense", periods=COLONIAL),
    dict(name="Calle Mantas and the university", polygon=Q(90, 480, -64, 13), density="dense", periods=COLONIAL),
    dict(name="Toward the Tullumayo", polygon=Q(390, 640, 22, 300), density="dense", periods=COLONIAL),
    dict(name="Santo Domingo quarter", polygon=Q(480, 700, -62, 18), density="dense", periods=COLONIAL),
    dict(name="Regocijo and the cabildo", polygon=Q(-60, 90, -260, -100), density="dense", periods=COLONIAL),
    dict(name="San Francisco and Santa Clara", polygon=Q(90, 260, -380, -100), density="dense", periods=COLONIAL),
    dict(name="Behind San Francisco", polygon=Q(-320, -70, -520, -360), density="dense", periods=COLONIAL),
    dict(name="Below the Saphy", polygon=Q(-240, -70, -330, -120), density="dense", periods=COLONIAL),
    dict(name="San Blas", polygon=[(-13.5150, -71.9768), (-13.5132, -71.9742), (-13.5114, -71.9752), (-13.5118, -71.9788), (-13.5138, -71.9792)], density="loose", periods=COLONIAL),
    dict(name="Santa Ana", polygon=[(-13.5122, -71.9895), (-13.5114, -71.9858), (-13.5128, -71.9852), (-13.5142, -71.9862), (-13.5145, -71.9895)], density="loose", periods=COLONIAL),
    dict(name="Belén", polygon=[(-13.5225, -71.9880), (-13.5210, -71.9845), (-13.5235, -71.9832), (-13.5250, -71.9865)], density="loose", periods=COLONIAL),
    dict(name="Hospital de Naturales", polygon=[(-13.5205, -71.9850), (-13.5198, -71.9835), (-13.5212, -71.9828), (-13.5218, -71.9842)], density="loose", periods=COLONIAL),
    dict(name="San Sebastián road", polygon=[(-13.5245, -71.9690), (-13.5236, -71.9660), (-13.5262, -71.9645), (-13.5270, -71.9680)], density="loose", periods=COLONIAL),
    dict(name="Beyond the Tullumayo", polygon=[(-13.5170, -71.9722), (-13.5150, -71.9700), (-13.5172, -71.9690), (-13.5195, -71.9712)], density="loose", periods=COLONIAL),
]

GARDENS = [
    dict(name="Terraces below Sacsayhuamán", kind="vineyard", polygon=[(-13.5112, -71.9800), (-13.5105, -71.9780), (-13.5120, -71.9772), (-13.5130, -71.9790)], periods=LATER),
    dict(name="Terraces of Carmenca", kind="vineyard", polygon=[(-13.5105, -71.9900), (-13.5095, -71.9875), (-13.5110, -71.9862), (-13.5118, -71.9890)], periods=LATER),
    dict(name="Maize terraces of the Huatanay", kind="vineyard", polygon=[(-13.5260, -71.9720), (-13.5280, -71.9660), (-13.5300, -71.9665), (-13.5280, -71.9725)], periods=LATER),
    dict(name="Terraces of Puquín", kind="vineyard", polygon=[(-13.5250, -71.9930), (-13.5240, -71.9895), (-13.5262, -71.9885), (-13.5272, -71.9920)], periods=LATER),
]

DISTRICTS = [
    dict(id="hanan", name="Hanan Qusqu (Upper Cusco)", polygon=Q(-350, 70, -55, 420), periods=INCA,
         description="The upper half of the city, toward Sacsayhuamán. Its lineages, the panaca of the later Incas from Inca Roca on, ranked above those of Hurin; the usual account makes the division a dual organisation found all over the Andes."),
    dict(id="hurin", name="Hurin Qusqu (Lower Cusco)", polygon=Q(70, 820, -80, 300), periods=INCA,
         description="The lower half of the city, toward the Coricancha and Pumachupan, home of the panaca of the first Incas, from Manco Capac to Capac Yupanqui, the usual king-list says."),
    dict(id="kusipata", name="Kusipata", polygon=Q(-200, 60, -260, -95), periods=IMPERIAL,
         description="'Terrace of joy', the half of the great plaza across the Saphy from Haukaypata. Its earth, the chroniclers say, was carried away and replaced with earth from every province of the empire."),
    dict(id="san-blas", name="Parish of San Blas", polygon=[(-13.5152, -71.9770), (-13.5130, -71.9738), (-13.5110, -71.9750), (-13.5115, -71.9790), (-13.5140, -71.9795)], periods=COLONIAL,
         description="The old Toqokachi on the slope north-east of the plaza, one of the parishes for the native people founded in the 1560s; later the quarter of the woodcarvers and painters."),
    dict(id="santa-ana", name="Parish of Santa Ana", polygon=[(-13.5120, -71.9900), (-13.5110, -71.9852), (-13.5130, -71.9845), (-13.5148, -71.9862), (-13.5148, -71.9900)], periods=COLONIAL,
         description="Carmenca, on the Lima road, where the parish church's paintings show the Corpus Christi processions of the 1670s."),
]

LABELS = [
    dict(text="Saphy", position=(-13.5108, -71.9866), size="sm", rotation=-75),
    dict(text="Tullumayo", position=(-13.5160, -71.9718), size="sm", rotation=-88),
    dict(text="Huatanay", position=(-13.5290, -71.9618), size="md", rotation=-32),
    dict(text="Pumachupan (the puma's tail)", position=(-13.5232, -71.9748), size="sm", periods=LATER),
    dict(text="Haukaypata", position=UV(0, 20), size="md", periods=IMPERIAL),
    dict(text="Kusipata", position=UV(-70, -175), size="md", periods=IMPERIAL),
    dict(text="Plaza de Armas", position=UV(0, 20), size="sm", periods=COLONIAL),
    dict(text="Regocijo", position=UV(-40, -175), size="sm", periods=COLONIAL),
    dict(text="Hanan Qusqu", position=UV(-200, 200), size="lg", periods=INCA),
    dict(text="Hurin Qusqu", position=UV(420, 160), size="lg", periods=INCA),
    dict(text="Qusqu", position=UV(300, 40), size="lg", periods=KILLKE),
    dict(text="Cuzco", position=UV(300, 160), size="lg", periods=COLONIAL),
    dict(text="Chinchaysuyu", position=(-13.5060, -71.9975), size="md", rotation=-48, periods=IMPERIAL),
    dict(text="Antisuyu", position=(-13.5030, -71.9615), size="md", rotation=45, periods=IMPERIAL),
    dict(text="Collasuyu", position=(-13.5300, -71.9590), size="md", rotation=-35, periods=IMPERIAL),
    dict(text="Cuntisuyu", position=(-13.5330, -71.9935), size="md", rotation=50, periods=IMPERIAL),
    dict(text="Carmenca", position=(-13.5150, -71.9878), size="sm", periods=INCA),
    dict(text="Santa Ana", position=(-13.5150, -71.9878), size="sm", periods=COLONIAL),
    dict(text="Toqokachi", position=(-13.5122, -71.9775), size="sm", periods=INCA),
    dict(text="San Blas", position=(-13.5122, -71.9775), size="sm", periods=COLONIAL),
    dict(text="Belén", position=(-13.5245, -71.9880), size="sm", periods=COLONIAL),
]

SOURCES = [
    dict(id="wiki-cusco", title="Cusco", author="Wikipedia", url="https://en.wikipedia.org/wiki/Cuzco"),
    dict(id="wiki-history-cusco", title="History of Cusco", author="Wikipedia", url="https://en.wikipedia.org/wiki/History_of_Cusco"),
    dict(id="wiki-killke", title="Killke culture", author="Wikipedia", url="https://en.wikipedia.org/wiki/Killke_culture"),
    dict(id="wiki-inca-road", title="Inca road system", author="Wikipedia", url="https://en.wikipedia.org/wiki/Inca_road_system"),
    dict(id="wiki-tawantinsuyu", title="Inca Empire", author="Wikipedia", url="https://en.wikipedia.org/wiki/Inca_Empire"),
    dict(id="wiki-ceque", title="Ceque system", author="Wikipedia", url="https://en.wikipedia.org/wiki/Ceque_system"),
    dict(id="hyslop", title="Inka Settlement Planning", author="John Hyslop", year=1990),
    dict(id="gasparini-margolies", title="Inca Architecture", author="Graziano Gasparini and Luise Margolies", year=1980),
    dict(id="bauer-cusco", title="Ancient Cuzco: Heartland of the Inca", author="Brian S. Bauer", year=2004),
    dict(id="dean-cusco", title="Inka Bodies and the Body of Christ: Corpus Christi in Colonial Cuzco, Peru", author="Carolyn Dean", year=1999),
    dict(id="garcilaso", title="Comentarios reales de los Incas", author="Inca Garcilaso de la Vega", year=1609, url="https://en.wikipedia.org/wiki/Inca_Garcilaso_de_la_Vega"),
]
