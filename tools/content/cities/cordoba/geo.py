# Córdoba: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
# Positions from OpenStreetMap and Wikipedia; the river is drawn from the OSM riverbank polygon.
ALL = ["roman-150", "abd-al-rahman-800", "caliphal-950", "castilian-1300", "habsburg-1600"]
ROMAN = ["roman-150"]
ISLAMIC = ["abd-al-rahman-800", "caliphal-950"]
MEDIEVAL_ON = ["abd-al-rahman-800", "caliphal-950", "castilian-1300", "habsburg-1600"]
LATER = ["castilian-1300", "habsburg-1600"]

SOURCES = [
    dict(id="wiki-history-cordoba", title="History of Córdoba, Spain", author="Wikipedia", url="https://en.wikipedia.org/wiki/C%C3%B3rdoba,_Spain#History"),
    dict(id="wiki-corduba", title="Corduba", author="Wikipedia (es)", url="https://es.wikipedia.org/wiki/Corduba"),
    dict(id="wiki-caliphate-cordoba", title="Umayyad state of Córdoba", author="Wikipedia", url="https://en.wikipedia.org/wiki/Umayyad_state_of_C%C3%B3rdoba"),
    dict(id="wiki-guadalquivir", title="Guadalquivir", author="Wikipedia", url="https://en.wikipedia.org/wiki/Guadalquivir"),
    dict(id="wiki-axerquia", title="Axerquía", author="Wikipedia", url="https://en.wikipedia.org/wiki/Axerqu%C3%ADa"),
    dict(id="wiki-medina-azahara", title="Madinat al-Zahra", author="Wikipedia", url="https://en.wikipedia.org/wiki/Madinat_al-Zahra"),
    dict(id="kennedy-muslim-spain", title="Muslim Spain and Portugal: A Political History of al-Andalus", author="Hugh Kennedy", year=1996),
    dict(id="menocal-ornament", title="The Ornament of the World: How Muslims, Jews and Christians Created a Culture of Tolerance in Medieval Spain", author="María Rosa Menocal", year=2002),
    dict(id="levi-provencal", title="Histoire de l'Espagne musulmane (3 vols)", author="Évariste Lévi-Provençal", year="1950–1953"),
    dict(id="acien-vallejo", title="Urbanismo y estado islámico: de Corduba a Qurtuba-Madinat al-Zahra", author="Manuel Acién Almansa and Antonio Vallejo Triano", year=1998),
    dict(id="escobar-camacho", title="Córdoba en la Baja Edad Media: evolución urbana de la ciudad", author="José Manuel Escobar Camacho", year=1989),
    dict(id="ventura-corduba", title="Colonia Patricia Corduba: una reflexión arqueológica", author="Pilar León (ed.); Ángel Ventura and others", year=1996),
    dict(id="osm", title="OpenStreetMap", author="OpenStreetMap contributors", url="https://www.openstreetmap.org/"),
]

CITY = dict(
    name="Córdoba", subtitle="Corduba, Qurtuba",
    description="Seventeen centuries of Córdoba on the north bank of the Guadalquivir: the Roman capital of Baetica, the Umayyad emirs' and caliphs' Qurtuba with its Great Mosque, the Castilian city of parishes after 1236, and the Renaissance cathedral rising inside the mosque. Madinat al-Zahra, the caliphs' palace city, lies 7 km west, beyond the frame. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="caliphal-950",
    world=dict(heightScale=1.0, walls=["#EFE7D6", "#E6D8BC", "#F3EEE2", "#DCC9A6", "#E9DDC5"], roofs=["#B9774F", "#C9A27C"]),
    camera=dict(target=(37.8805, -4.7790), distance=38),
)

# north-west corner, south-east corner: the western suburbs to San Lorenzo, the Sierra's foot to the river loop
FRAME = ((37.8960, -4.8040), (37.8660, -4.7540))

PALETTE = dict(parchment="#E8D5AC", ink="#6E4B33", water="#668C88", hill="#8A8460", road="#8B6B4A")
COMPASS = (37.8935, -4.7575)
CARTOUCHE = (37.8668, -4.8032)

PERIODS = [
    dict(id="roman-150", label="Colonia Patricia", year=150, startYear=-169, endYear=710,
         summary="Corduba, founded by Marcus Claudius Marcellus in the 160s or 150s BCE and refounded as Colonia Patricia under Augustus, is the capital of the province of Baetica. A walled grid of about 78 hectares runs from the Baetis bridge up the slope: a colonial forum, a marble temple by the east gate, a great theatre. The range runs on through the Visigoths to 711.",
         population="perhaps 30,000–50,000",
         feel="Carts of olive oil rolling to the river quays, Latin and Punic in the forum, marble from the quarries being dressed for the temple, the smell of garum and woodsmoke.",
         style="antique",
         houses=dict(title="Domus and insulae of Patricia", text="Single-storey houses of the well-off round atria and peristyles with mosaic floors, as excavated under the modern centre; tabernae open to the streets; rubble and brick walls under tiled roofs, the grid laid out in blocks between the cardo and decumanus."),
         outskirts=dict(title="Tombs and villas", text="Along the roads out of the gates, tombs and mausolea like the round one by the west gate; beyond them farms and villas among olive groves and the clay pits of the potters.")),
    dict(id="abd-al-rahman-800", label="Qurtuba of the emirs", year=800, startYear=711, endYear=928,
         summary="Taken by the Arabs in 711, Córdoba becomes the capital of al-Andalus. In 756 Abd al-Rahman I, a Umayyad prince escaped from the Abbasid massacre in Syria, makes himself emir here; he rebuilds the governors' palace (the old Visigothic one) by the river and in 786 begins the Great Mosque. The Roman walls still enclose the medina; suburbs grow outside, on the south bank too.",
         population="perhaps 50,000–100,000",
         feel="The call to prayer from a new minaret, Syrian and Berber soldiers in the market, Latin-speaking Christians at their churches, water-wheels creaking on the river.",
         style="courtyard",
         houses=dict(title="Courtyard houses of the medina", text="Houses of rammed earth, rubble and brick turned inward round a patio with a well and a cistern, the street walls blank but for a bent entrance; flat or low-pitched tiled roofs. Many reuse Roman stone; the Roman grid starts to break into lanes and dead ends."),
         outskirts=dict(title="Suburbs and munyas", text="Outside the walls, new suburbs (arrabales) of craftsmen and soldiers, cemeteries, and the munyas, country estates with orchards and water-wheels, like the emir's own Rusafa north of the city.")),
    dict(id="caliphal-950", label="Umayyad capital", year=950, startYear=929, endYear=1235,
         summary="In 929 Abd al-Rahman III proclaims himself caliph. Córdoba, with a medina and some twenty suburbs, is the largest city of western Europe; the caliph builds Madinat al-Zahra 7 km west and a new minaret, and al-Hakam II extends the mosque and gathers a great library. The range runs on through the Fitna (1009–1013), taifas, Almoravids and Almohads to 1235.",
         population="perhaps 100,000–250,000 (estimates vary widely)",
         feel="Paper and parchment in the booksellers' lanes, Greek and Latin envoys riding to Madinat al-Zahra, the smell of tanned leather and orange blossom, hundreds of mosques and baths.",
         style="courtyard",
         houses=dict(title="Patio houses of Qurtuba", text="Excavated houses of the western suburbs are each built round a patio, with a hall, a latrine and a well, the walls of stone or rammed earth plastered white or red-painted at the base; lanes of the same houses in the medina, two storeys at most."),
         outskirts=dict(title="The western arrabales", text="Planned suburbs stretch west along the road to Madinat al-Zahra: streets of patio houses, mosques, baths and workshops, with munyas and gardens along the river. Abandoned after the Fitna of 1009–1013 and left as ruins and fields.")),
    dict(id="castilian-1300", label="Castilian Córdoba", year=1300, startYear=1236, endYear=1491,
         summary="Ferdinand III of Castile takes Córdoba on 29 June 1236. The mosque is consecrated as the cathedral; the city is divided into fourteen parishes, whose new Gothic churches (the 'Fernandine' churches) rise in the Villa and the walled Axerquía. Alfonso XI builds the new Alcázar from 1328; the Jewish quarter by the Almodóvar gate gets its synagogue in 1315. The city has lost most of its people since the caliphate.",
         population="perhaps 20,000–30,000",
         feel="Church bells where the call to prayer was, Castilian, Arabic and Hebrew in the same street, knights of the frontier with Granada, leather and wool on market days at the Corredera.",
         style="medieval",
         houses=dict(title="Patio houses of the Villa", text="The Castilian settlers moved into the Andalusi houses and kept their plan: a bent entrance, rooms round a patio with a well, cistern and flowerpots. New houses keep it too, with tiled roofs, a first floor gallery and a coat of whitewash."),
         outskirts=dict(title="Huertas and the river", text="Beyond the walls, market gardens and orchards on the old suburbs' ruins, water mills along the river weirs, and the small suburb of the Campo de la Verdad at the bridgehead.")),
    dict(id="habsburg-1600", label="Renaissance Córdoba", year=1600, startYear=1492, endYear=1750,
         summary="A provincial Habsburg city of nobles, convents and the Inquisition, which has its seat in the Alcázar from 1482. In 1523 the chapter begins a Renaissance cathedral nave in the middle of the mosque; it is still being vaulted in 1600 (finished 1607). Hernán Ruiz III rebuilds the Puerta del Puente (1572) and encases the minaret in a bell tower. Cervantes knows the inn at the Plaza del Potro.",
         population="perhaps 40,000–50,000",
         feel="Masons' hammers inside the mosque, horse dealers at the Potro, processions of the brotherhoods in Holy Week, the bells of forty convents.",
         style="early-modern",
         houses=dict(title="Houses round patios", text="Two-storey whitewashed houses with tiled roofs, stone portals carved with the owners' arms, and the patio, now often arcaded on marble columns, with a fountain, flowers and a well; the noble houses have several patios in a row."),
         outskirts=dict(title="Convents and orchards", text="Outside the walls, convent gardens, orchards and the potters', tanners' and dyers' sheds near the river; the western suburbs of the caliphs lie buried under fields.")),
]

# ---------------------------------------------------------------- the Guadalquivir (centre line and widths from the OSM riverbank)
RIVER_BLURB = "The Guadalquivir (Latin Baetis, Arabic al-Wadi al-Kabir, 'the great river') was navigable for river boats up to Córdoba in Roman times, carrying Baetica's oil to Hispalis and the sea. Its weirs drove a chain of mills and water-wheels; reedy islets, the sotos, lie below the Roman bridge."

WATER = [
    dict(id="guadalquivir-upper", name="Guadalquivir", width=80, blurb=RIVER_BLURB,
         path=[(37.8703, -4.7451), (37.8683, -4.7469), (37.8674, -4.7483), (37.8666, -4.7505), (37.8658, -4.7534), (37.8655, -4.7564), (37.8657, -4.7603), (37.8666, -4.7640), (37.8675, -4.7662)]),
    dict(id="guadalquivir-loop", name="Guadalquivir", width=110, blurb=RIVER_BLURB,
         path=[(37.8675, -4.7662), (37.8684, -4.7676), (37.8692, -4.7687), (37.8704, -4.7696), (37.8715, -4.7703), (37.8730, -4.7706), (37.8738, -4.7705), (37.8758, -4.7700), (37.8777, -4.7699), (37.8789, -4.7702)]),
    dict(id="guadalquivir-bend", name="Guadalquivir", width=85, blurb=RIVER_BLURB,
         path=[(37.8789, -4.7702), (37.8798, -4.7714), (37.8800, -4.7721), (37.8800, -4.7733), (37.8798, -4.7739), (37.8787, -4.7758), (37.8776, -4.7772)]),
    dict(id="guadalquivir-sotos", name="Guadalquivir: the sotos of the Albolafia", width=210,
         blurb="Below the Roman bridge the river spreads over islets (sotos) of reeds, tamarisk and poplars between mill weirs: the Albolafia, Pápalo, Enmedio and San Antonio mills stood here. The weirs are probably Islamic in origin.",
         path=[(37.8776, -4.7772), (37.8771, -4.7779), (37.8762, -4.7784), (37.8751, -4.7797), (37.8738, -4.7803)]),
    dict(id="guadalquivir-lower", name="Guadalquivir", width=130, blurb=RIVER_BLURB,
         path=[(37.8738, -4.7803), (37.8728, -4.7809), (37.8720, -4.7821), (37.8711, -4.7829), (37.8698, -4.7835), (37.8674, -4.7851), (37.8617, -4.7895)]),
]

ISLANDS = [
    dict(name="Soto de la Albolafia", polygon=[(37.8757, -4.7776), (37.8754, -4.7788), (37.8746, -4.7798), (37.8738, -4.7803), (37.8740, -4.7794), (37.8746, -4.7784), (37.8752, -4.7774)]),
    dict(name="Islet of the San Rafael mills", polygon=[(37.8723, -4.7819), (37.8722, -4.7828), (37.8716, -4.7829), (37.8715, -4.7821)]),
    dict(name="Soto of the Alegría mill", polygon=[(37.8707, -4.7823), (37.8703, -4.7832), (37.8693, -4.7842), (37.8695, -4.7834), (37.8701, -4.7826)]),
]

HILLS = [
    dict(id="sierra", name="Foothills of the Sierra Morena", center=(37.8948, -4.8005), radius=340,
         blurb="The Sierra Morena rises a few kilometres north of the city: the source of its building stone, firewood and spring water, carried down by Roman and caliphal aqueducts. Madinat al-Zahra was built on its lower slopes, 7 km west."),
]

# ---------------------------------------------------------------- streets and roads
CARDO = [(37.8889, -4.7794), (37.8866, -4.7795), (37.8845, -4.7796), (37.8820, -4.7793), (37.8800, -4.7790), (37.8784, -4.7789), (37.8777, -4.7790)]
DECUMANUS = [(37.8848, -4.7757), (37.8847, -4.7780), (37.8845, -4.7796), (37.8841, -4.7822), (37.8837, -4.7846)]
WEST_ROAD = [(37.8837, -4.7846), (37.8842, -4.7900), (37.8850, -4.7960), (37.8860, -4.8040)]
NORTH_ROAD = [(37.8889, -4.7794), (37.8915, -4.7800), (37.8960, -4.7806)]
EAST_ROAD = [(37.8848, -4.7757), (37.8851, -4.7720), (37.8849, -4.7670), (37.8853, -4.7600), (37.8858, -4.7540)]
SOUTH_ROAD = [(37.8759, -4.7769), (37.8735, -4.7772), (37.8705, -4.7780), (37.8660, -4.7792)]
RIBERA = [(37.8771, -4.7806), (37.8775, -4.7797), (37.8779, -4.7786), (37.8784, -4.7774), (37.8790, -4.7765), (37.8797, -4.7756), (37.8804, -4.7742), (37.8809, -4.7728)]
MEDINA_STREET = [(37.8889, -4.7794), (37.8866, -4.7795), (37.8845, -4.7796), (37.8820, -4.7793), (37.8802, -4.7790), (37.8800, -4.7791), (37.8786, -4.7782), (37.8780, -4.7785), (37.8777, -4.7790)]

ROADS = [
    dict(id="cardo", name="Cardo maximus", path=CARDO, width=12, style="major", labelled=True, periods=ROMAN,
         blurb="The colony's main north–south street, from the north gate past the colonial forum down to the bridge gate. Colonnaded in places; its line survives roughly in today's streets of Cruz Conde and the Tendillas."),
    dict(id="decumanus", name="Decumanus maximus", path=DECUMANUS, width=12, style="major", labelled=True, periods=ROMAN,
         blurb="The east–west street from the east gate, where the Via Augusta came in beside the provincial temple, across the cardo to the west gate."),
    dict(id="via-augusta-east", name="Via Augusta (to Castulo and Rome)", path=EAST_ROAD, width=10, style="major", labelled=True, periods=ROMAN,
         blurb="Augustus' road from the Pyrenees down the Baetis valley, marked with milestones; it entered Corduba from the east and left over the bridge for Astigi and Gades."),
    dict(id="via-augusta-south", name="Via Augusta (to Astigi and Gades)", path=SOUTH_ROAD, width=10, style="major", periods=ROMAN,
         blurb="South of the bridge the Via Augusta struck off across the plain toward Astigi (Écija), Hispalis and Gades."),
    dict(id="hispalis-road", name="Road west to Hispalis", path=WEST_ROAD, width=8, style="minor", periods=ROMAN,
         blurb="The road down the north bank of the Baetis toward Hispalis (Seville), lined outside the gate with tombs."),
    dict(id="emerita-road", name="Road north to Emerita", path=NORTH_ROAD, width=8, style="minor", periods=ROMAN,
         blurb="Over the Sierra Morena to Emerita Augusta (Mérida), capital of Lusitania, and to the mines of the sierra."),
    dict(id="medina-street", name="Main street of the medina", path=MEDINA_STREET, width=10, style="major", labelled=True, periods=MEDIEVAL_ON,
         blurb="The old cardo, now a market street running from the north gate past the Great Mosque's east side to the Bridge Gate. Shops of the cloth, perfume and book trades crowded the lanes beside the mosque."),
    dict(id="gallegos-street", name="Street of the western gate", path=DECUMANUS, width=8, style="minor", periods=MEDIEVAL_ON,
         blurb="The old decumanus, cutting across the medina from the east gate to the western gate (later the Puerta de Gallegos)."),
    dict(id="rasif", name="al-Rasif (the riverside causeway)", path=RIBERA, width=14, style="major", labelled=True, periods=ISLAMIC,
         blurb="The raised esplanade along the river in front of the Alcázar and the mosque, built up against the floods; parades, executions and public ceremonies took place here, before the palace gates."),
    dict(id="ribera", name="La Ribera", path=RIBERA, width=12, style="major", labelled=True, periods=LATER,
         blurb="The riverside road along the walls from the Alcázar past the Puerta del Puente to the Axerquía, with the mills below and the Potro's tanners and dyers at its east end."),
    dict(id="zahra-road", name="Road to Madinat al-Zahra", path=WEST_ROAD, width=12, style="major", labelled=True, periods=["caliphal-950"],
         blurb="The road through the western suburbs to the caliph's palace city, 7 km west at the foot of the sierra; envoys, officials and supplies went along it daily."),
    dict(id="west-road", name="Road west", path=WEST_ROAD, width=8, style="minor", periods=["abd-al-rahman-800"] + LATER,
         blurb="The old road west along the north bank toward Almodóvar and Seville."),
    dict(id="north-road", name="Road north to the sierra", path=NORTH_ROAD, width=8, style="minor", periods=MEDIEVAL_ON,
         blurb="North to the sierra, its springs and quarries, and in the emirs' time to the munya of al-Rusafa, Abd al-Rahman I's country palace about 3 km north of the city."),
    dict(id="east-road", name="Road east (to Toledo and Jaén)", path=EAST_ROAD, width=10, style="major", periods=MEDIEVAL_ON,
         blurb="The main road east up the valley toward Jaén, Toledo and, after 1236, Castile; in the walled Axerquía it ran through the Puerta Nueva."),
    dict(id="south-road", name="Road south (to Écija and Seville)", path=SOUTH_ROAD, width=10, style="major", periods=MEDIEVAL_ON,
         blurb="Over the Roman bridge and past the bridgehead toward Écija, Seville and, for the caliphs' armies, the frontier."),
    dict(id="feria", name="Calle de la Feria", path=[(37.8884, -4.7759), (37.8865, -4.7754), (37.8848, -4.7752), (37.8830, -4.7754), (37.8814, -4.7758), (37.8798, -4.7757)], width=10, style="major", labelled=True, periods=LATER,
         blurb="The street along the old wall between the Villa and the Axerquía, where the city's fairs were held; today Calle San Fernando."),
    dict(id="potro-street", name="Street of the Potro", path=[(37.8814, -4.7758), (37.8812, -4.7745), (37.8813, -4.7720), (37.8822, -4.7695), (37.8828, -4.7675)], width=8, style="minor", periods=LATER,
         blurb="From the Feria past the Plaza del Potro, with its inn and its colt fountain (1577), east through the Axerquía to the Puerta de Baeza."),
    dict(id="santa-marina-street", name="Street of Santa Marina", path=[(37.8915, -4.7760), (37.8898, -4.7752), (37.8880, -4.7745), (37.8860, -4.7742), (37.8851, -4.7720)], width=8, style="minor", periods=LATER,
         blurb="From the Puerta del Colodro south through the parish of Santa Marina, a quarter of nobles and later of bullfighters, toward San Pablo."),
    dict(id="judios-street", name="Calle de los Judíos", path=[(37.8805, -4.7838), (37.8798, -4.7833), (37.8794, -4.7820), (37.8794, -4.7810)], width=6, style="minor", labelled=True, periods=LATER,
         blurb="The street of the Jewish quarter from the Puerta de Almodóvar toward the cathedral, with the synagogue of 1315 on it."),
    dict(id="almodovar-road", name="Road to Almodóvar", path=[(37.8806, -4.7845), (37.8810, -4.7900), (37.8815, -4.7980), (37.8818, -4.8040)], width=8, style="minor", periods=MEDIEVAL_ON,
         blurb="West from the Almodóvar gate toward the castle of Almodóvar del Río and Seville."),
    dict(id="sevilla-road", name="Road from the Puerta de Sevilla", path=[(37.8754, -4.7860), (37.8750, -4.7920), (37.8742, -4.8000), (37.8738, -4.8040)], width=8, style="minor", periods=LATER,
         blurb="Out of the Alcázar Viejo along the river toward Seville, past orchards and the river mills."),
    dict(id="andujar-road", name="Road to Andújar", path=[(37.8892, -4.7668), (37.8903, -4.7600), (37.8912, -4.7540)], width=8, style="minor", periods=LATER,
         blurb="North-east out of the Axerquía toward Andújar, Toledo and Castile."),
]

# ---------------------------------------------------------------- walls and gates
VILLA = [(37.8790, -4.7762), (37.8784, -4.7774), (37.8779, -4.7785), (37.8777, -4.7791), (37.8773, -4.7800), (37.8770, -4.7806), (37.8763, -4.7813),
         (37.8767, -4.7819), (37.8768, -4.7834), (37.8782, -4.7830), (37.8794, -4.7835), (37.8806, -4.7841), (37.8812, -4.7843), (37.8837, -4.7846),
         (37.8860, -4.7845), (37.8876, -4.7841), (37.8886, -4.7815), (37.8889, -4.7794), (37.8888, -4.7775), (37.8885, -4.7764), (37.8865, -4.7757),
         (37.8848, -4.7756), (37.8830, -4.7758), (37.8814, -4.7762), (37.8800, -4.7763)]
AXERQUIA = [(37.8885, -4.7764), (37.8905, -4.7770), (37.8915, -4.7773), (37.8915, -4.7757), (37.8920, -4.7720), (37.8926, -4.7703), (37.8931, -4.7696),
            (37.8915, -4.7661), (37.8892, -4.7668), (37.8849, -4.7670), (37.8828, -4.7672), (37.8808, -4.7697), (37.8806, -4.7716), (37.8805, -4.7732),
            (37.8800, -4.7748), (37.8790, -4.7762)]
ALCAZAR_VIEJO = [(37.8768, -4.7834), (37.8771, -4.7857), (37.8755, -4.7857), (37.8744, -4.7856), (37.8737, -4.7845), (37.8740, -4.7829), (37.8750, -4.7819), (37.8760, -4.7809)]

WALLS = [
    dict(id="roman-walls", name="Walls of Colonia Patricia", path=VILLA, closed=True, periods=ROMAN,
         blurb="The Republican town's wall enclosed the higher northern part; under Augustus the circuit was pushed south to the river, giving about 78 hectares. Stone curtains with towers and ditch; stretches survive along Calle Cairuán and the Ronda de los Tejares."),
    dict(id="medina-walls", name="Walls of the medina", path=VILLA, closed=True, periods=ISLAMIC,
         blurb="The Umayyads kept and repaired the Roman circuit; Abd al-Rahman I rebuilt it in 766 and the walls were repaired again after the floods and wars. Its seven gates are named by the geographer al-Idrisi; the Bridge Gate (Bab al-Qantara) faced the river."),
    dict(id="villa-walls", name="Walls of the Villa", path=VILLA, closed=True, periods=LATER,
         blurb="After 1236 the old medina became 'la Villa', walled off from the Axerquía; the wall along Calle San Fernando divided the two until the 19th century, pierced by the Portillo in the 14th century."),
    dict(id="axerquia-walls", name="Walls of the Axerquía", path=AXERQUIA, closed=False, periods=LATER,
         blurb="The eastern suburb (al-Sharqiyya, 'the eastern') was walled probably in the 11th or 12th century, after the Fitna; the Castilians kept and repaired the circuit and added the Malmuerta tower (1404–1408) at its north-west corner."),
    dict(id="alcazar-viejo-walls", name="Walls of the Alcázar Viejo", path=ALCAZAR_VIEJO, closed=False, periods=LATER,
         blurb="Alfonso XI walled the quarter west of the new Alcázar, the Alcázar Viejo (San Basilio), in the 14th century, with the Puerta de Sevilla and the Huerta del Alcázar inside."),
]

GATES = [
    dict(id="roman-north-gate", name="North gate", position=(37.8889, -4.7794), periods=ROMAN),
    dict(id="roman-east-gate", name="East gate (Via Augusta)", position=(37.8848, -4.7756), periods=ROMAN),
    dict(id="roman-west-gate", name="West gate", position=(37.8837, -4.7846), periods=ROMAN),
    dict(id="puerta-osario", name="Puerta de Osario", position=(37.8889, -4.7794), periods=MEDIEVAL_ON),
    dict(id="puerta-gallegos", name="Puerta de Gallegos", position=(37.8837, -4.7846), periods=MEDIEVAL_ON),
    dict(id="east-gate-medina", name="East gate of the medina", position=(37.8848, -4.7756), periods=ISLAMIC),
    dict(id="puerta-rincon", name="Puerta del Rincón", position=(37.8885, -4.7764), periods=LATER),
    dict(id="portillo", name="Arco del Portillo", position=(37.8814, -4.7762), periods=LATER),
    dict(id="puerta-colodro", name="Puerta del Colodro", position=(37.8915, -4.7757), periods=LATER),
    dict(id="puerta-plasencia", name="Puerta de Plasencia", position=(37.8892, -4.7668), periods=LATER),
    dict(id="puerta-nueva", name="Puerta Nueva", position=(37.8849, -4.7670), periods=LATER),
    dict(id="puerta-baeza", name="Puerta de Baeza", position=(37.8828, -4.7672), periods=LATER),
    dict(id="puerta-martos", name="Puerta de Martos", position=(37.8808, -4.7697), periods=LATER),
]

BRIDGES = [
    dict(id="roman-bridge", name="Roman bridge", path=[(37.87757, -4.77899), (37.87591, -4.77691)], build="stone", arches=12, landmarkId="roman-bridge",
         blurb="The bridge over the Baetis, built probably under Augustus for the Via Augusta and rebuilt again and again: by the governor al-Samh in 720 and many times since. Some 250 metres long on sixteen arches; until the 20th century Córdoba's only bridge."),
]

AQUEDUCTS = [
    dict(name="Aqua Augusta (Aqua Vetus)", path=[(37.8955, -4.7960), (37.8925, -4.7905), (37.8898, -4.7862), (37.8880, -4.7838)], periods=ROMAN),
]

# ---------------------------------------------------------------- built-up areas
V_NW = [(37.8873, -4.7837), (37.8883, -4.7813), (37.8886, -4.7799), (37.8849, -4.7799), (37.8849, -4.7840), (37.8860, -4.7841)]
V_NE = [(37.8886, -4.7791), (37.8886, -4.7776), (37.8882, -4.7766), (37.8864, -4.7760), (37.8850, -4.7760), (37.8849, -4.7791)]
V_SW = [(37.8843, -4.7842), (37.8843, -4.7799), (37.8803, -4.7799), (37.8797, -4.7808), (37.8789, -4.7812), (37.8786, -4.7826), (37.8796, -4.7832), (37.8810, -4.7840)]
V_SE = [(37.8843, -4.7791), (37.8843, -4.7761), (37.8815, -4.7765), (37.8800, -4.7766), (37.8792, -4.7768), (37.8787, -4.7778), (37.8803, -4.7787)]
V_RIVER = [(37.8800, -4.7805), (37.8800, -4.7792), (37.8787, -4.7780), (37.8780, -4.7792), (37.8775, -4.7803), (37.8781, -4.7814), (37.8790, -4.7813)]
JUDERIA = [(37.8806, -4.7838), (37.8806, -4.7820), (37.8797, -4.7811), (37.8787, -4.7813), (37.8784, -4.7826), (37.8794, -4.7833)]
SAN_BASILIO = [(37.8771, -4.7839), (37.8771, -4.7855), (37.8757, -4.7855), (37.8752, -4.7847), (37.8762, -4.7839)]
AX_N = [(37.8905, -4.7767), (37.8912, -4.7742), (37.8917, -4.7718), (37.8866, -4.7718), (37.8866, -4.7752), (37.8884, -4.7757)]
AX_NE = [(37.8918, -4.7712), (37.8924, -4.7701), (37.8913, -4.7674), (37.8866, -4.7676), (37.8866, -4.7712)]
AX_C = [(37.8860, -4.7750), (37.8860, -4.7718), (37.8818, -4.7718), (37.8809, -4.7731), (37.8804, -4.7750), (37.8815, -4.7754)]
AX_SE = [(37.8860, -4.7712), (37.8860, -4.7679), (37.8831, -4.7680), (37.8813, -4.7699), (37.8813, -4.7712)]
WEST_IN = [(37.8890, -4.7866), (37.8890, -4.7930), (37.8800, -4.7930), (37.8795, -4.7866), (37.8838, -4.7856)]
WEST_MID = [(37.8890, -4.7936), (37.8890, -4.7990), (37.8805, -4.7990), (37.8800, -4.7936)]
WEST_OUT = [(37.8915, -4.7996), (37.8915, -4.8036), (37.8790, -4.8036), (37.8790, -4.7996)]
SOUTHWEST = [(37.8789, -4.7866), (37.8789, -4.7990), (37.8748, -4.7990), (37.8742, -4.7872), (37.8758, -4.7862)]
NORTH_SUB = [(37.8948, -4.7860), (37.8948, -4.7802), (37.8904, -4.7790), (37.8893, -4.7815), (37.8881, -4.7852), (37.8896, -4.7864)]
NORTHEAST_SUB = [(37.8952, -4.7782), (37.8952, -4.7695), (37.8934, -4.7686), (37.8921, -4.7742), (37.8915, -4.7778)]
EAST_SUB = [(37.8920, -4.7660), (37.8890, -4.7590), (37.8825, -4.7610), (37.8814, -4.7665), (37.8850, -4.7664)]
SHAQUNDA = [(37.8744, -4.7760), (37.8738, -4.7774), (37.8722, -4.7790), (37.8705, -4.7800), (37.8690, -4.7790), (37.8695, -4.7760), (37.8725, -4.7745), (37.8743, -4.7752)]

BLOCKS = [
    # ---- Colonia Patricia
    dict(name="Northern insulae", polygon=V_NW, density="dense", periods=ROMAN),
    dict(name="Insulae by the forum", polygon=V_NE, density="dense", periods=ROMAN),
    dict(name="Southern insulae", polygon=V_SW, density="dense", periods=ROMAN),
    dict(name="Insulae by the theatre", polygon=V_SE, density="dense", periods=ROMAN),
    dict(name="Riverside quarter", polygon=V_RIVER, density="dense", periods=ROMAN),
    dict(name="Suburbium of the west gate", polygon=WEST_IN, density="loose", periods=ROMAN),
    dict(name="Suburbium of the Via Augusta", polygon=AX_C, density="loose", periods=ROMAN),
    dict(name="Northern suburbium", polygon=NORTH_SUB, density="loose", periods=ROMAN),
    # ---- the emirs' medina and its first suburbs
    dict(name="Medina: northern quarters", polygon=V_NW, density="dense", periods=ISLAMIC),
    dict(name="Medina: quarter of the old forum", polygon=V_NE, density="dense", periods=ISLAMIC),
    dict(name="Medina: western quarters", polygon=V_SW, density="dense", periods=ISLAMIC),
    dict(name="Medina: markets east of the mosque", polygon=V_SE, density="dense", periods=ISLAMIC),
    dict(name="Shaqunda", polygon=SHAQUNDA, density="dense", periods=["abd-al-rahman-800"]),
    dict(name="Eastern suburbs", polygon=AX_C, density="dense", periods=["abd-al-rahman-800"]),
    dict(name="Eastern suburbs", polygon=AX_N, density="loose", periods=["abd-al-rahman-800"]),
    dict(name="Eastern suburbs", polygon=AX_SE, density="loose", periods=["abd-al-rahman-800"]),
    dict(name="Western suburbs", polygon=WEST_IN, density="loose", periods=["abd-al-rahman-800"]),
    dict(name="Northern suburbs", polygon=NORTH_SUB, density="loose", periods=["abd-al-rahman-800"]),
    # ---- the caliphal city at its height
    dict(name="al-Sharqiyya (eastern suburbs)", polygon=AX_N, density="dense", periods=["caliphal-950"]),
    dict(name="al-Sharqiyya (eastern suburbs)", polygon=AX_NE, density="dense", periods=["caliphal-950"]),
    dict(name="al-Sharqiyya (eastern suburbs)", polygon=AX_C, density="dense", periods=["caliphal-950"]),
    dict(name="al-Sharqiyya (eastern suburbs)", polygon=AX_SE, density="dense", periods=["caliphal-950"]),
    dict(name="Suburbs beyond the east", polygon=EAST_SUB, density="loose", periods=["caliphal-950"]),
    dict(name="Western arrabales", polygon=WEST_IN, density="dense", periods=["caliphal-950"]),
    dict(name="Western arrabales", polygon=WEST_MID, density="dense", periods=["caliphal-950"]),
    dict(name="Arrabales toward Madinat al-Zahra", polygon=WEST_OUT, density="loose", periods=["caliphal-950"]),
    dict(name="Arrabales by the river", polygon=SOUTHWEST, density="loose", periods=["caliphal-950"]),
    dict(name="Northern arrabales", polygon=NORTH_SUB, density="dense", periods=["caliphal-950"]),
    dict(name="Northern arrabales", polygon=NORTHEAST_SUB, density="loose", periods=["caliphal-950"]),
    # ---- Castilian and Habsburg Córdoba: the Villa, the Axerquía and the Alcázar Viejo
    dict(name="Villa: San Miguel and San Nicolás", polygon=V_NW, density="dense", periods=LATER),
    dict(name="Villa: Santa María and the Ayuntamiento", polygon=V_NE, density="dense", periods=LATER),
    dict(name="Villa: San Juan and Omnium Sanctorum", polygon=V_SW, density="dense", periods=LATER),
    dict(name="Villa: around the cathedral", polygon=V_SE, density="dense", periods=LATER),
    dict(name="Judería", polygon=JUDERIA, density="dense", periods=LATER),
    dict(name="Alcázar Viejo (San Basilio)", polygon=SAN_BASILIO, density="dense", periods=LATER),
    dict(name="Axerquía: Santa Marina", polygon=AX_N, density="dense", periods=LATER),
    dict(name="Axerquía: San Lorenzo", polygon=AX_NE, density="dense", periods=LATER),
    dict(name="Axerquía: San Pedro and the Potro", polygon=AX_C, density="dense", periods=LATER),
    dict(name="Axerquía: Santiago and San Andrés", polygon=AX_SE, density="dense", periods=LATER),
    dict(name="Campo de la Verdad", polygon=SHAQUNDA, density="loose", periods=LATER),
    dict(name="Huertas and convents outside the walls", polygon=WEST_IN, density="loose", periods=["habsburg-1600"]),
    dict(name="Campo de la Merced", polygon=NORTH_SUB, density="loose", periods=LATER),
]

GARDENS = [
    dict(name="Huertas east of the city", polygon=[(37.8795, -4.7680), (37.8800, -4.7560), (37.8700, -4.7560), (37.8685, -4.7650), (37.8720, -4.7678)], kind="orchard"),
    dict(name="Olive groves of the campiña", polygon=[(37.8688, -4.7748), (37.8688, -4.7695), (37.8664, -4.7705), (37.8664, -4.7760)], kind="orchard"),
    dict(name="Olive groves", polygon=[(37.8890, -4.7936), (37.8890, -4.7990), (37.8805, -4.7990), (37.8800, -4.7936)], kind="orchard", periods=ROMAN),
    dict(name="Munyas by the river", polygon=[(37.8742, -4.7872), (37.8738, -4.7990), (37.8705, -4.7990), (37.8712, -4.7885)], kind="park", periods=ISLAMIC),
    dict(name="Huertas of the old arrabales", polygon=WEST_MID, kind="orchard", periods=LATER),
    dict(name="Huertas of the old arrabales", polygon=WEST_OUT, kind="orchard", periods=LATER),
    dict(name="Huertas of the old arrabales", polygon=WEST_IN, kind="orchard", periods=["castilian-1300"]),
    dict(name="Huerta del Alcázar", polygon=[(37.8759, -4.7819), (37.8750, -4.7840), (37.8742, -4.7832), (37.8745, -4.7820), (37.8752, -4.7813)], kind="orchard", periods=LATER),
    dict(name="Mulberry and olive gardens", polygon=SOUTHWEST, kind="orchard", periods=["abd-al-rahman-800"] + LATER),
]

DISTRICTS = [
    dict(id="corduba", name="Colonia Patricia Corduba", polygon=VILLA, periods=ROMAN,
         description="The walled Roman colony, capital of Baetica: a grid of insulae with the colonial forum at its centre, the provincial temple by the east gate and the theatre on the slope above the river."),
    dict(id="medina", name="al-Madina", polygon=VILLA, periods=ISLAMIC,
         description="The walled inner city of Qurtuba, inside the Roman circuit: the Great Mosque and the Alcázar by the river, the markets (suq) round them, and dense lanes of patio houses."),
    dict(id="villa", name="La Villa", polygon=VILLA, periods=LATER,
         description="The old medina after 1236: the cathedral-mosque, the Alcázar, the Judería and the seven parishes of the upper town, home of the cathedral chapter, the nobles and the city council."),
    dict(id="axerquia", name="La Axerquía", polygon=AXERQUIA, periods=LATER,
         description="From Arabic al-Sharqiyya, 'the eastern': the walled lower town of craftsmen and traders, with seven parishes, the Corredera and the Potro, tanners, dyers and potters near the river."),
    dict(id="sharqiyya", name="al-Sharqiyya", polygon=AXERQUIA, periods=["caliphal-950"],
         description="The eastern suburbs of the caliphal city, crowded with craftsmen and markets; walled only later, after the Fitna."),
    dict(id="shaqunda", name="Shaqunda", polygon=SHAQUNDA, periods=["abd-al-rahman-800"],
         description="The suburb of Secunda on the south bank at the bridgehead, crowded with artisans and scholars. After its revolt in 818 al-Hakam I razed it and forbade anyone to build there again."),
    dict(id="juderia", name="Judería", polygon=JUDERIA, periods=LATER,
         description="The Jewish quarter between the Almodóvar gate and the cathedral, with the synagogue of 1315. The Jews of Córdoba were attacked in 1391 and expelled from Castile in 1492."),
    dict(id="western-arrabales", name="Western arrabales", polygon=[(37.8915, -4.7866), (37.8915, -4.8036), (37.8748, -4.8036), (37.8742, -4.7872), (37.8838, -4.7856)], periods=["caliphal-950"],
         description="The planned suburbs of the 10th century along the road to Madinat al-Zahra: excavations since the 1990s have found street after street of patio houses, mosques, baths and cemeteries. Destroyed or abandoned in the Fitna of 1009–1013."),
]

LABELS = [
    dict(text="Baetis", position=(37.8705, -4.7845), size="lg", rotation=-40, periods=ROMAN),
    dict(text="al-Wadi al-Kabir", position=(37.8705, -4.7845), size="lg", rotation=-40, periods=ISLAMIC),
    dict(text="Guadalquivir", position=(37.8705, -4.7845), size="lg", rotation=-40, periods=LATER),
    dict(text="Corduba", position=(37.8866, -4.7822), size="lg", periods=ROMAN),
    dict(text="Qurtuba", position=(37.8866, -4.7822), size="lg", periods=ISLAMIC),
    dict(text="La Villa", position=(37.8866, -4.7822), size="md", periods=LATER),
    dict(text="La Axerquía", position=(37.8875, -4.7705), size="md", periods=LATER),
    dict(text="al-Sharqiyya", position=(37.8875, -4.7705), size="md", periods=["caliphal-950"]),
    dict(text="Western arrabales", position=(37.8862, -4.7965), size="md", periods=["caliphal-950"]),
    dict(text="Madinat al-Zahra, 7 km →", position=(37.8885, -4.8010), size="sm", rotation=-5, periods=["caliphal-950"]),
    dict(text="Shaqunda", position=(37.8718, -4.7775), size="sm", periods=["abd-al-rahman-800"]),
    dict(text="Campo de la Verdad", position=(37.8712, -4.7772), size="sm", periods=LATER),
    dict(text="Judería", position=(37.8799, -4.7822), size="sm", periods=LATER),
    dict(text="San Basilio", position=(37.8763, -4.7863), size="sm", periods=LATER),
    dict(text="Sierra Morena", position=(37.8950, -4.7975), size="sm"),
    dict(text="to Hispalis", position=(37.8858, -4.8015), size="sm", periods=ROMAN),
    dict(text="Sotos de la Albolafia", position=(37.8745, -4.7812), size="sm", rotation=-35),
]
