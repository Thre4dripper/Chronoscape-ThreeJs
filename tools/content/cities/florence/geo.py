# Florence: city, frame, eras and the map's geography (see tools/content/cities/FORMAT.md).
# The Arno runs from east-south-east to west-north-west through the middle of the frame; the Roman square,
# the medieval city and the Medici city grow on the right (north) bank, the Oltrarno climbs the Boboli hill
# and the hill of San Miniato on the left bank.
R, C, M, G = "florentia-100", "comune-1300", "medici-1490", "grand-ducal-1600"
ALL = [R, C, M, G]
LATER = [C, M, G]
LATE = [M, G]

CITY = dict(
    name="Florence", subtitle="Florentia to the Grand Duchy",
    description="Florence from the Roman colony on the Arno to the grand dukes of Tuscany: the Roman square under the medieval centre, the city of the guilds and towers, Brunelleschi's dome and the Medici city, the Uffizi, the Pitti and the Boboli, inside the walls of 1284–1333 on both banks with San Miniato on its hill. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId=M,
    world=dict(heightScale=1.0, walls=["#E8D9BC", "#D9C29A", "#E2CBA4", "#EADFC8", "#D6B27A"], roofs=["#B5603F", "#A9563A", "#C27350"]),
    camera=dict(target=(43.7708, 11.2552), distance=38),
)
FRAME = ((43.7890, 11.2290), (43.7570, 11.2780))
PALETTE = dict(parchment="#E8D5AB", ink="#664631", water="#638A8C", hill="#7B7F58", road="#8C6B48")
COMPASS = (43.7862, 11.2745)
CARTOUCHE = (43.7582, 11.2302)

PERIODS = [
    dict(id=R, label="Roman Florentia", year=100, startYear=-59, endYear=570,
         summary="Florentia, a colony of veterans on the north bank of the Arno where the Via Cassia crossed the river: a walled square about 500 by 420 m on a regular grid, the forum and Capitolium at the crossing of cardo and decumanus, baths, a theatre and, outside the walls to the east, an amphitheatre. Brick, local sandstone, plaster and red tile.",
         population="perhaps 10,000",
         feel="Carts rumbling over the timber bridge, smoke from the bath furnaces, fullers treading cloth in tubs by the river.",
         style="antique",
         houses=dict(title="Houses of Florentia", text="Insulae of the gridded colony: brick and rubble houses round small courts and shops opening on the porticoed streets, plastered and roofed with red tile; richer domus with mosaics and gardens near the forum."),
         outskirts=dict(title="Centuriated fields", text="The plain was divided into square fields by the Roman survey; farmhouses, vineyards and potters' kilns along the roads to Faesulae, Pisa and Rome, tombs lining the roads out of the gates.")),
    dict(id=C, label="Dante's Florence", year=1300, startYear=571, endYear=1349,
         summary="The commune at its height: a banking and wool city of about 100,000 under the priors of the guilds, still bristling with the stone towers of the magnate families. The new cathedral rises round old Santa Reparata, the Palazzo dei Priori is being built, the friars build Santa Croce and Santa Maria Novella, and a third, far larger circuit of walls is going up.",
         population="about 100,000 (Villani's figures suggest 90,000–120,000)",
         feel="Bells of a hundred churches, the clatter of looms and fulling mills, Guelf and Ghibelline shouting in the narrow streets under the towers.",
         style="medieval",
         houses=dict(title="Case-torri and botteghe", text="Narrow houses of stone and plaster three or four storeys high over open shops (botteghe) with wooden shutters, crowded round the stone towers of the great families, cut down to 29 m by the commune in 1250; wooden balconies and sporti jut over the lanes."),
         outskirts=dict(title="Borghi and orti", text="Ribbon suburbs (borghi) along the roads out of the gates, the friars' new convents, and wide orchards and vegetable gardens (orti) inside the line of the new walls.")),
    dict(id=M, label="The Medici city", year=1490, startYear=1350, endYear=1529,
         summary="Florence under Lorenzo the Magnificent, unofficial ruler of a republic: Brunelleschi's dome (closed 1436) over the city, the new palaces of the bankers with rusticated stone fronts, the Innocenti, San Lorenzo and Santo Spirito in the new style, the workshops of painters and sculptors. The city fills only part of its walls, with gardens between the convents.",
         population="about 70,000",
         feel="Hammering from the marble yards, the smell of dye vats and wool grease along the river, friars preaching to crowds in the piazzas.",
         style="early-modern",
         houses=dict(title="Botteghe and palazzi", text="Rows of plastered houses over shops, now joined by the bankers' palazzi: a block of pietra forte with a rusticated ground floor, round-arched windows in pairs, a deep cornice, an arcaded courtyard and a bench along the street front."),
         outskirts=dict(title="Convent gardens and orti", text="Inside the walls, the gardens and orchards of the convents and the vegetable plots of the market gardeners; beyond, villas and farms on the hills, olive groves and vines.")),
    dict(id=G, label="Grand-ducal Florence", year=1600, startYear=1530, endYear=1737,
         summary="The capital of the Medici grand dukes of Tuscany after the fall of the republic in 1530: the Fortezza da Basso over the city, the Uffizi offices and Vasari's corridor from the Palazzo Vecchio to the Pitti, the Boboli Gardens on the hill behind it, Forte Belvedere above them, new bridges by Ammannati. In October 1600 the Pitti saw the first surviving opera.",
         population="about 70,000–75,000",
         feel="Court carriages on the new bridges, goldsmiths' hammers on the Ponte Vecchio, the bells of the convents and the snap of the grand duke's soldiers drilling in the fortress.",
         style="early-modern",
         houses=dict(title="Palazzi and case", text="Plastered houses of three to five storeys over shops, the old towers cut down and built into them; the courtiers' new palazzi along Via Maggio and Via Tornabuoni with rusticated doorways, kneeling windows and coats of arms."),
         outskirts=dict(title="Orti and Medici farms", text="Orchards and kitchen gardens of the convents inside the walls; outside, the grand duke's dairy farm and meadows at the Cascine, villas and podere on the hills.")),
]

SOURCES = [
    dict(id="wiki-florence-history", title="History of Florence", author="Wikipedia", url="https://en.wikipedia.org/wiki/History_of_Florence"),
    dict(id="wiki-florentia", title="Florentia (Roman city)", author="Wikipedia", url="https://en.wikipedia.org/wiki/History_of_Florence#Roman_origins"),
    dict(id="wiki-walls-florence", title="Walls of Florence", author="Wikipedia", url="https://en.wikipedia.org/wiki/Walls_of_Florence"),
    dict(id="wiki-arno", title="Arno", author="Wikipedia", url="https://en.wikipedia.org/wiki/Arno"),
    dict(id="wiki-mugnone", title="Mugnone", author="Wikipedia", url="https://en.wikipedia.org/wiki/Mugnone"),
    dict(id="wiki-cascine", title="Parco delle Cascine", author="Wikipedia", url="https://en.wikipedia.org/wiki/Parco_delle_Cascine"),
    dict(id="wiki-boboli", title="Boboli Gardens", author="Wikipedia", url="https://en.wikipedia.org/wiki/Boboli_Gardens"),
    dict(id="wiki-vasari-corridor", title="Vasari Corridor", author="Wikipedia", url="https://en.wikipedia.org/wiki/Vasari_Corridor"),
    dict(id="wiki-ponte-carraia", title="Ponte alla Carraia", author="Wikipedia", url="https://en.wikipedia.org/wiki/Ponte_alla_Carraia"),
    dict(id="villani", title="Nuova Cronica", author="Giovanni Villani", year="c. 1340", url="https://en.wikipedia.org/wiki/Nuova_Cronica"),
    dict(id="davidsohn", title="Storia di Firenze", author="Robert Davidsohn", year="1896–1927"),
    dict(id="goldthwaite", title="The Economy of Renaissance Florence", author="Richard A. Goldthwaite", year=2009),
    dict(id="fanelli", title="Firenze: architettura e città", author="Giovanni Fanelli", year=1973),
    dict(id="catena-map", title="Veduta della Catena (view of Florence)", author="attributed to Francesco Rosselli", year="c. 1471–82", url="https://en.wikipedia.org/wiki/Map_of_the_Chain"),
    dict(id="buonsignori", title="Nova pulcherrimae civitatis Florentiae topographia", author="Stefano Bonsignori", year=1584),
]

# ---------------------------------------------------------------- water
ARNO = [(43.7612, 11.2800), (43.7625, 11.2765), (43.7636, 11.2730), (43.7642, 11.2700), (43.7647, 11.2670), (43.7652, 11.2640), (43.7656, 11.2615),
        (43.7659, 11.2596), (43.7666, 11.2568), (43.7673, 11.2548), (43.7680, 11.2531), (43.7687, 11.2516), (43.7694, 11.2502), (43.7700, 11.2482),
        (43.7707, 11.2460), (43.7714, 11.2440), (43.7722, 11.2420), (43.7731, 11.2400), (43.7741, 11.2378), (43.7752, 11.2352), (43.7764, 11.2322), (43.7776, 11.2285)]

WATER = [
    dict(id="arno", name="Arno", path=ARNO, width=95,
         blurb="The Arnus of the Romans, a mountain river that is a trickle in August and a torrent in November. Its water washed and dyed the wool that made Florence rich; its weirs (pescaie) turned the mills and fulling stocks; its floods of 1177, 1333 and 1557 swept away the bridges."),
    dict(id="mugnone-roman", name="Mugnone", periods=[R], width=12,
         path=[(43.7890, 11.2560), (43.7850, 11.2545), (43.7810, 11.2527), (43.7775, 11.2514), (43.7745, 11.2509), (43.7720, 11.2507), (43.7697, 11.2503)],
         blurb="The torrent from Fiesole; in Roman times, on the usual reconstruction, it ran close under the west side of the colony to the Arno, roughly where Via de' Tornabuoni runs now."),
    dict(id="mugnone", name="Mugnone", periods=LATER, width=12,
         path=[(43.7890, 11.2570), (43.7868, 11.2535), (43.7845, 11.2490), (43.7830, 11.2450), (43.7810, 11.2420), (43.7790, 11.2390), (43.7770, 11.2365), (43.7757, 11.2345)],
         blurb="Diverted round the city in the Middle Ages, the Mugnone ran outside the north-west walls, filling their ditch, and joined the Arno below the Prato. It was moved again for the Fortezza da Basso in the 1530s."),
]

ISLANDS = []

HILLS = [
    dict(id="boboli", name="Boboli hill", center=(43.7624, 11.2492), radius=230,
         blurb="The hill behind the Pitti, quarried for the palace's stone. Cosimo I and Eleonora of Toledo bought it in 1549 and Tribolo, Ammannati and Buontalenti laid out the Boboli Gardens on its slope."),
    dict(id="san-miniato-hill", name="Monte alle Croci", center=(43.7598, 11.2640), radius=280,
         blurb="The hill of San Miniato, south-east of the city across the river, with the abbey church on its crest. Michelangelo fortified it with earth bastions during the siege of 1529–30."),
    dict(id="bellosguardo", name="Bellosguardo", center=(43.7612, 11.2370), radius=300,
         blurb="A hill of villas south-west of the walls, named for its view over the city."),
]

MARSH = [
    dict(name="Arno flats (west)", periods=[R], polygon=[(43.7735, 11.2470), (43.7760, 11.2420), (43.7775, 11.2370), (43.7760, 11.2345), (43.7742, 11.2385), (43.7724, 11.2440)]),
    dict(name="Low ground by the river (east)", periods=[R], polygon=[(43.7680, 11.2630), (43.7700, 11.2690), (43.7672, 11.2715), (43.7655, 11.2680), (43.7660, 11.2640)]),
]

# ---------------------------------------------------------------- roads
GATE_N = (43.7731, 11.2542)
ROADS = [
    # Roman Florentia
    dict(id="cardo", name="Cardo maximus (Via Roma, Via Calimala)", periods=[R], width=10, style="major", labelled=True,
         path=[GATE_N, (43.7714, 11.2541), (43.7697, 11.2540), (43.7684, 11.2540)],
         blurb="The main north–south street of the colony, from the north gate past the forum to the south gate and the river; Via Roma, Via Calimala and Via Por Santa Maria still follow it."),
    dict(id="decumanus", name="Decumanus maximus (Via Strozzi, Via del Corso)", periods=[R], width=10, style="major", labelled=True,
         path=[(43.7714, 11.2516), (43.7714, 11.2541), (43.7715, 11.2570)],
         blurb="The east–west street through the forum, between the west and east gates; Via degli Strozzi, Via degli Speziali and Via del Corso keep its line."),
    dict(id="roman-grid-n", name="Street of the grid", periods=[R], width=6, style="minor",
         path=[(43.7722, 11.2517), (43.7722, 11.2569)]),
    dict(id="roman-grid-s", name="Street of the grid", periods=[R], width=6, style="minor",
         path=[(43.7705, 11.2517), (43.7705, 11.2569)]),
    dict(id="roman-grid-w", name="Street of the grid", periods=[R], width=6, style="minor",
         path=[(43.7729, 11.2529), (43.7697, 11.2529)]),
    dict(id="roman-grid-e", name="Street of the grid", periods=[R], width=6, style="minor",
         path=[(43.7729, 11.2556), (43.7697, 11.2556)]),
    dict(id="via-cassia-s", name="Via Cassia (to Rome)", periods=[R], width=9, style="major", labelled=True,
         path=[(43.7672, 11.2536), (43.7655, 11.2512), (43.7630, 11.2480), (43.7605, 11.2455), (43.7570, 11.2425)],
         blurb="The consular road from Rome, which crossed the Arno here; the reason the colony was put on this spot."),
    dict(id="via-faesulae", name="Road to Faesulae", periods=[R], width=8, style="major",
         path=[GATE_N, (43.7760, 11.2555), (43.7800, 11.2575), (43.7845, 11.2595), (43.7890, 11.2615)],
         blurb="North-east to the old Etruscan hill town of Faesulae (Fiesole), and on over the Apennines toward Bononia."),
    dict(id="via-pisana-r", name="Road to Pisa", periods=[R], width=8, style="major",
         path=[(43.7714, 11.2516), (43.7722, 11.2480), (43.7738, 11.2440), (43.7752, 11.2400), (43.7770, 11.2350), (43.7790, 11.2290)],
         blurb="West along the river toward Pistoria and Pisa."),
    dict(id="via-arretium", name="Road east", periods=[R], width=7, style="minor",
         path=[(43.7715, 11.2570), (43.7712, 11.2620), (43.7708, 11.2680), (43.7705, 11.2780)]),

    # Medieval and later streets
    dict(id="calimala", name="Via Calimala and Por Santa Maria", periods=LATER, width=9, style="major", labelled=True,
         path=[(43.7733, 11.2543), (43.7714, 11.2541), (43.7697, 11.2539), (43.76837, 11.25342)],
         blurb="The old cardo, the spine of the merchants' city: the cloth-finishers of the Calimala guild, the bankers at the Mercato Nuovo, the silk guild at Por Santa Maria, and the Ponte Vecchio at the end."),
    dict(id="calzaiuoli", name="Via de' Calzaiuoli", periods=LATER, width=9, style="major", labelled=True,
         path=[(43.7728, 11.2553), (43.7712, 11.2551), (43.7699, 11.2552), (43.7694, 11.2554)],
         blurb="The street of the hosiers between the cathedral and the Piazza della Signoria, past Orsanmichele: the processional way between church and state, widened in the 1380s."),
    dict(id="corso", name="Via del Corso and Borgo degli Albizi", periods=LATER, width=7, style="minor",
         path=[(43.7714, 11.2541), (43.7716, 11.2575), (43.7718, 11.2610), (43.7717, 11.2650)],
         blurb="The Roman decumanus continued east toward San Pier Maggiore, lined with the houses of the Albizi."),
    dict(id="strozzi", name="Via degli Strozzi", periods=LATER, width=7, style="minor",
         path=[(43.7714, 11.2541), (43.7714, 11.2513)]),
    dict(id="tornabuoni", name="Via de' Tornabuoni", periods=LATER, width=10, style="major",
         path=[(43.76984, 11.25052), (43.7712, 11.2511), (43.7727, 11.2511), (43.7737, 11.2504)],
         blurb="From the Ponte Santa Trinita north toward Santa Maria Novella, along the line of the Roman west wall; the street of the Strozzi, Rucellai and Tornabuoni palaces."),
    dict(id="via-larga", name="Via Larga", periods=LATER, width=12, style="major", labelled=True,
         path=[(43.7737, 11.2556), (43.7752, 11.2562), (43.7778, 11.2580), (43.7815, 11.2588), (43.7853, 11.2593)],
         blurb="The 'wide street' north from the cathedral past the Medici palace and San Marco toward the Porta San Gallo; the Medici built their palace on it in the 1440s. Today Via Cavour."),
    dict(id="via-dei-servi", name="Via de' Servi", periods=LATER, width=8, style="minor",
         path=[(43.7736, 11.2572), (43.7750, 11.2588), (43.7763, 11.2600)],
         blurb="From the cathedral to the church of the Servites at the Santissima Annunziata, lined with the palaces of their patrons."),
    dict(id="borgo-la-croce", name="Borgo la Croce", periods=LATER, width=8, style="major",
         path=[(43.7718, 11.2610), (43.7716, 11.2650), (43.7714, 11.2690), (43.7713, 11.2717), (43.7714, 11.2780)],
         blurb="East through Sant'Ambrogio to the Porta alla Croce and the road to Arezzo; condemned men went out this way to the gallows at the Porta alla Giustizia."),
    dict(id="ghibellina", name="Via Ghibellina", periods=LATER, width=7, style="minor",
         path=[(43.7702, 11.2585), (43.7703, 11.2630), (43.7705, 11.2680)]),
    dict(id="benci", name="Via de' Benci", periods=LATER, width=7, style="minor",
         path=[(43.7700, 11.2605), (43.7682, 11.2602), (43.76642, 11.25981)],
         blurb="From Santa Croce down to the Ponte alle Grazie, past the palaces of the Alberti."),
    dict(id="ognissanti", name="Borgo Ognissanti and Via il Prato", periods=LATER, width=8, style="major",
         path=[(43.7712, 11.2470), (43.7722, 11.2448), (43.7735, 11.2425), (43.7752, 11.2410), (43.7779, 11.2403)],
         blurb="West past the Umiliati's wool workshops at Ognissanti to the Prato, the meadow inside the gate where races and fairs were held."),
    dict(id="via-della-scala", name="Via della Scala", periods=LATER, width=7, style="minor",
         path=[(43.7740, 11.2486), (43.7755, 11.2455), (43.7770, 11.2420)]),
    dict(id="faenza", name="Via Faenza", periods=LATER, width=7, style="minor",
         path=[(43.7752, 11.2535), (43.7775, 11.2510), (43.7803, 11.2462)]),
    dict(id="san-gallo", name="Via San Gallo", periods=LATER, width=7, style="minor",
         path=[(43.7765, 11.2555), (43.7810, 11.2575), (43.7853, 11.2593)]),
    dict(id="pinti", name="Borgo Pinti", periods=LATER, width=7, style="minor",
         path=[(43.7725, 11.2612), (43.7760, 11.2640), (43.7812, 11.2668)]),
    dict(id="guicciardini", name="Via Guicciardini", periods=LATER, width=8, style="major",
         path=[(43.76757, 11.25284), (43.7668, 11.2520), (43.7660, 11.2508)],
         blurb="From the Ponte Vecchio past Santa Felicita to the Piazza de' Pitti."),
    dict(id="maggio", name="Via Maggio and Via Romana", periods=LATER, width=9, style="major", labelled=True,
         path=[(43.76896, 11.24988), (43.7678, 11.2490), (43.7660, 11.2478), (43.7640, 11.2468), (43.7618, 11.2455), (43.7593, 11.2444)],
         blurb="Via Maggio, the 'greater street' of the Oltrarno, from the Ponte Santa Trinita south, continued by Via Romana to the Porta Romana and the road to Siena and Rome."),
    dict(id="san-frediano", name="Borgo San Frediano", periods=LATER, width=7, style="minor",
         path=[(43.76896, 11.24988), (43.7695, 11.2470), (43.7700, 11.2440), (43.7708, 11.2400)],
         blurb="The street of the poorest wool workers, the dyers' and weavers' quarter of the Oltrarno, out to the Porta San Frediano and the road to Pisa."),
    dict(id="bardi", name="Via de' Bardi and Via San Niccolò", periods=LATER, width=6, style="minor",
         path=[(43.76757, 11.25284), (43.7668, 11.2545), (43.7660, 11.2570), (43.7652, 11.2610), (43.7640, 11.2645)],
         blurb="Along the left bank under the hill, past the towers of the Bardi, the bankers ruined in the 1340s."),
    dict(id="costa", name="Costa San Giorgio", periods=LATER, width=5, style="minor",
         path=[(43.7668, 11.2530), (43.7650, 11.2540), (43.7628, 11.2547)]),
    dict(id="monte-alle-croci", name="Via del Monte alle Croci", periods=LATER, width=5, style="minor",
         path=[(43.7621, 11.2605), (43.7610, 11.2625), (43.7603, 11.2640)],
         blurb="The steep path up to San Miniato, lined with the stations of the cross that gave the hill its name."),
    dict(id="road-pisa", name="Road to Pisa", periods=LATER, width=8, style="major",
         path=[(43.7708, 11.2400), (43.7705, 11.2350), (43.7700, 11.2290)]),
    dict(id="road-prato", name="Road to Prato and Pistoia", periods=LATER, width=8, style="major",
         path=[(43.7779, 11.2403), (43.7790, 11.2370), (43.7805, 11.2330), (43.7820, 11.2290)]),
    dict(id="road-bologna", name="Road to Bologna", periods=LATER, width=8, style="major",
         path=[(43.7853, 11.2593), (43.7870, 11.2600), (43.7890, 11.2605)]),
    dict(id="road-siena", name="Road to Siena", periods=LATER, width=8, style="major",
         path=[(43.7593, 11.2444), (43.7580, 11.2430), (43.7570, 11.2422)]),
    dict(id="uffizi-street", name="Strada degli Uffizi", periods=[G], width=6, style="minor",
         path=[(43.7689, 11.2554), (43.7679, 11.2551)]),
]

# ---------------------------------------------------------------- walls and gates
ROMAN_WALL = [(43.7730, 11.2516), (43.7730, 11.2569), (43.7697, 11.2569), (43.7697, 11.2516)]
WALL_1172_N = [(43.7713, 11.2463), (43.7724, 11.2472), (43.7738, 11.2482), (43.7745, 11.2505), (43.7758, 11.2525), (43.7766, 11.2548), (43.7767, 11.2575),
               (43.7760, 11.2600), (43.7745, 11.2614), (43.7725, 11.2617), (43.7703, 11.2614), (43.7682, 11.2606), (43.76655, 11.2601)]
WALL_1172_S = [(43.7702, 11.2456), (43.7688, 11.2458), (43.7672, 11.2467), (43.7660, 11.2488), (43.7655, 11.2520), (43.7652, 11.2560), (43.7650, 11.2585), (43.76545, 11.2600)]
WALL_N = [(43.7748, 11.2368), (43.7765, 11.2390), (43.7779, 11.2403), (43.7792, 11.2428), (43.7803, 11.2462), (43.7820, 11.2505), (43.7835, 11.2540),
          (43.7848, 11.2575), (43.7853, 11.2593), (43.7843, 11.2618), (43.7828, 11.2645), (43.7812, 11.2668), (43.7790, 11.2690), (43.7765, 11.2705),
          (43.7738, 11.2713), (43.7713, 11.2717), (43.7690, 11.2721), (43.7667, 11.2722), (43.7646, 11.2716)]
WALL_S = [(43.7726, 11.2402), (43.7708, 11.2400), (43.7690, 11.2402), (43.7660, 11.2406), (43.7630, 11.2418), (43.7608, 11.2432), (43.7593, 11.2444),
          (43.7598, 11.2462), (43.7603, 11.2480), (43.7610, 11.2498), (43.7620, 11.2514), (43.7627, 11.2521), (43.7628, 11.2547), (43.7624, 11.2575),
          (43.7621, 11.2605), (43.7628, 11.2627), (43.7637, 11.2645), (43.7644, 11.2651)]

WALLS = [
    dict(id="roman-wall", name="Wall of Florentia", periods=[R], closed=True, path=ROMAN_WALL,
         blurb="The colony's wall, roughly 1.8 km round, with round towers and a gate on each side; traces turn up under the streets that follow its line, Via de' Tornabuoni on the west and Via del Proconsolo on the east."),
    dict(id="walls-1172-n", name="Walls of 1172 (right bank)", periods=[C], path=WALL_1172_N,
         blurb="The second circuit of the commune, built 1172–75, roughly on the usual reconstruction: it took in the suburbs round San Lorenzo and the cathedral but left the friars' new churches outside. By 1300 the city had spilled far beyond it and a third circuit was being built."),
    dict(id="walls-1172-s", name="Walls of 1172 (Oltrarno)", periods=[C], path=WALL_1172_S,
         blurb="The first wall round the Oltrarno, built with the 1172 circuit and approximate here: it enclosed the bridgeheads, Borgo San Jacopo and the streets round Santo Spirito."),
    dict(id="walls-n", name="Walls of 1284–1333 (right bank)", periods=LATE, path=WALL_N,
         blurb="The third and last circuit, begun in 1284 and finished in 1333: 8.5 km in all, about 11.6 m high, a tower every 115 m or so and a moat. It enclosed so much land that the city did not fill it before the 19th century."),
    dict(id="walls-s", name="Walls of 1284–1333 (Oltrarno)", periods=LATE, path=WALL_S,
         blurb="The left-bank half of the last walls, climbing from the river at San Frediano over the hills to San Niccolò. Michelangelo strengthened the hill stretch with earthworks in 1529; Forte Belvedere was built into it in the 1590s."),
]

GATES = [
    dict(id="porta-roman-n", name="North gate", position=GATE_N, periods=[R]),
    dict(id="porta-roman-s", name="South gate", position=(43.7697, 11.2540), periods=[R]),
    dict(id="porta-roman-w", name="West gate", position=(43.7714, 11.2516), periods=[R]),
    dict(id="porta-roman-e", name="East gate", position=(43.7715, 11.2569), periods=[R]),
    dict(id="porta-al-prato", name="Porta al Prato", position=(43.7779, 11.2403), periods=LATER),
    dict(id="porta-faenza", name="Porta Faenza", position=(43.7803, 11.2462), periods=[M]),
    dict(id="porta-san-gallo", name="Porta San Gallo", position=(43.7853, 11.2593), periods=LATER),
    dict(id="porta-a-pinti", name="Porta a Pinti", position=(43.7812, 11.2668), periods=LATE),
    dict(id="porta-alla-croce", name="Porta alla Croce", position=(43.7713, 11.2717), periods=LATER),
    dict(id="porta-alla-giustizia", name="Porta alla Giustizia", position=(43.7667, 11.2722), periods=LATE),
    dict(id="porta-san-niccolo", name="Porta San Niccolò", position=(43.7637, 11.2645), periods=LATE),
    dict(id="porta-san-miniato", name="Porta San Miniato", position=(43.7621, 11.2605), periods=LATE),
    dict(id="porta-san-giorgio", name="Porta San Giorgio", position=(43.7628, 11.2547), periods=LATE),
    dict(id="porta-san-frediano", name="Porta San Frediano", position=(43.7708, 11.2400), periods=LATE),
]

# ---------------------------------------------------------------- bridges
PV = [(43.76757, 11.25284), (43.76837, 11.25342)]
TRINITA = [(43.76896, 11.24988), (43.76984, 11.25052)]
GRAZIE = [(43.76538, 11.25939), (43.76642, 11.25981)]
CARRAIA = [(43.77025, 11.24571), (43.77115, 11.24629)]

BRIDGES = [
    dict(id="roman-bridge", name="Roman bridge", path=[(43.7672, 11.2536), (43.7684, 11.2541)], build="timber", arches=5, periods=[R],
         blurb="The bridge of the Via Cassia, probably on stone piers with a timber deck, a little upstream of the later Ponte Vecchio on the line of the cardo; its exact position is a reconstruction."),
    dict(id="ponte-vecchio-b", name="Ponte Vecchio", path=PV, build="stone", arches=3, landmarkId="ponte-vecchio", periods=LATER,
         blurb="The 'old bridge', for centuries the only one."),
    dict(id="ponte-santa-trinita-b", name="Ponte Santa Trinita", path=TRINITA, build="stone", arches=3, landmarkId="ponte-santa-trinita", periods=LATER,
         blurb="The bridge from Via de' Tornabuoni to Via Maggio."),
    dict(id="ponte-alle-grazie-b", name="Ponte alle Grazie", path=GRAZIE, build="stone", arches=9, landmarkId="ponte-alle-grazie", periods=LATER,
         blurb="The bridge of Rubaconte, 1237."),
    dict(id="ponte-carraia", name="Ponte alla Carraia", path=CARRAIA, build="stone", arches=5, periods=LATER,
         blurb="Built 1218–20 as the Ponte Nuovo, the second bridge of the city, for the carts (carri) of the wool trade. In 1304 it collapsed under a crowd watching a play of Hell staged on boats; rebuilt after the floods of 1333 and 1557, the second time by Ammannati."),
]

AQUEDUCTS = [
    dict(name="Aqueduct of Florentia", periods=[R], path=[(43.7890, 11.2470), (43.7840, 11.2490), (43.7790, 11.2505), (43.7745, 11.2515), (43.7731, 11.2524)]),
    dict(name="Vasari Corridor", periods=[G], path=[(43.7679, 11.2550), (43.7681, 11.2543), (43.76837, 11.25342)]),
    dict(name="Vasari Corridor", periods=[G], path=[(43.76757, 11.25284), (43.7670, 11.2524), (43.7666, 11.2518), (43.7660, 11.2510), (43.7656, 11.2505)]),
]

# ---------------------------------------------------------------- built-up blocks
OLTRARNO_1300 = [(43.7700, 11.2460), (43.7689, 11.2490), (43.7684, 11.2510), (43.7673, 11.2528), (43.7664, 11.2555), (43.7656, 11.2585),
                 (43.7651, 11.2582), (43.7652, 11.2540), (43.7657, 11.2510), (43.7665, 11.2488), (43.7680, 11.2468), (43.7695, 11.2456)]
BLOCKS = [
    # Roman Florentia: four quarters of the grid and the suburbs
    dict(name="Florentia, north-west", periods=[R], density="dense", polygon=[(43.7729, 11.2517), (43.7729, 11.2539), (43.7716, 11.2539), (43.7716, 11.2517)]),
    dict(name="Florentia, north-east", periods=[R], density="dense", polygon=[(43.7729, 11.2543), (43.7729, 11.2568), (43.7716, 11.2568), (43.7716, 11.2543)]),
    dict(name="Florentia, south-west", periods=[R], density="dense", polygon=[(43.7712, 11.2517), (43.7712, 11.2539), (43.7698, 11.2539), (43.7698, 11.2517)]),
    dict(name="Florentia, south-east", periods=[R], density="dense", polygon=[(43.7712, 11.2543), (43.7712, 11.2568), (43.7698, 11.2568), (43.7698, 11.2543)]),
    dict(name="Suburb of the theatre and amphitheatre", periods=[R], density="loose", polygon=[(43.7722, 11.2573), (43.7720, 11.2622), (43.7682, 11.2622), (43.7680, 11.2573)]),
    dict(name="Riverside below the colony", periods=[R], density="loose", polygon=[(43.7694, 11.2519), (43.7694, 11.2568), (43.7676, 11.2560), (43.7686, 11.2520)]),
    dict(name="Bridgehead on the left bank", periods=[R], density="loose", polygon=[(43.7672, 11.2522), (43.7667, 11.2545), (43.7658, 11.2540), (43.7662, 11.2518)]),
    dict(name="Along the road to Faesulae", periods=[R], density="loose", polygon=[(43.7735, 11.2545), (43.7762, 11.2560), (43.7758, 11.2574), (43.7733, 11.2566)]),
    dict(name="West of the walls", periods=[R], density="loose", polygon=[(43.7728, 11.2490), (43.7728, 11.2511), (43.7701, 11.2511), (43.7703, 11.2494)]),
    # Dante's Florence: dense inside the 1172 walls, borghi outside
    dict(name="San Lorenzo and the cathedral quarter", periods=[C], density="dense", polygon=[(43.7739, 11.2486), (43.7745, 11.2506), (43.7757, 11.2526), (43.7763, 11.2545), (43.7735, 11.2545), (43.7717, 11.2540), (43.7717, 11.2490), (43.7728, 11.2477)]),
    dict(name="San Pier Maggiore and the Corso", periods=[C], density="dense", polygon=[(43.7764, 11.2550), (43.7765, 11.2575), (43.7758, 11.2598), (43.7743, 11.2611), (43.7717, 11.2612), (43.7717, 11.2545), (43.7735, 11.2548)]),
    dict(name="Santa Trinita and Por Santa Maria", periods=[C], density="dense", polygon=[(43.7712, 11.2468), (43.7712, 11.2538), (43.7687, 11.2538), (43.7701, 11.2502)]),
    dict(name="San Piero Scheraggio and the Bargello", periods=[C], density="dense", polygon=[(43.7712, 11.2544), (43.7712, 11.2611), (43.7690, 11.2608), (43.7670, 11.2601), (43.7676, 11.2560), (43.7684, 11.2544)]),
    dict(name="Oltrarno inside the walls", periods=[C], density="dense", polygon=OLTRARNO_1300),
    dict(name="Borgo Ognissanti", periods=[C], density="loose", polygon=[(43.7720, 11.2465), (43.7733, 11.2425), (43.7746, 11.2403), (43.7755, 11.2413), (43.7740, 11.2452), (43.7728, 11.2476)]),
    dict(name="Borgo San Lorenzo and San Gallo", periods=[C], density="loose", polygon=[(43.7768, 11.2548), (43.7805, 11.2568), (43.7805, 11.2585), (43.7768, 11.2578)]),
    dict(name="Borgo Pinti and Borgo la Croce", periods=[C], density="loose", polygon=[(43.7745, 11.2620), (43.7730, 11.2690), (43.7705, 11.2700), (43.7705, 11.2620)]),
    dict(name="Borgo San Frediano", periods=[C], density="loose", polygon=[(43.7700, 11.2452), (43.7713, 11.2412), (43.7700, 11.2405), (43.7684, 11.2448)]),
    dict(name="San Niccolò", periods=[C], density="loose", polygon=[(43.7652, 11.2598), (43.7644, 11.2635), (43.7637, 11.2633), (43.7644, 11.2596)]),
    dict(name="Via Romana", periods=[C], density="loose", polygon=[(43.7658, 11.2484), (43.7640, 11.2466), (43.7615, 11.2452), (43.7612, 11.2462), (43.7638, 11.2474), (43.7650, 11.2486)]),
    # The Medici city and grand-ducal Florence: the old centre packed, the new circuit filled in part
    dict(name="Santa Maria Novella and San Lorenzo", periods=LATE, density="dense", polygon=[(43.7728, 11.2442), (43.7745, 11.2470), (43.7760, 11.2505), (43.7775, 11.2540), (43.7735, 11.2545), (43.7717, 11.2540), (43.7717, 11.2470)]),
    dict(name="San Giovanni", periods=LATE, density="dense", polygon=[(43.7775, 11.2548), (43.7780, 11.2585), (43.7768, 11.2600), (43.7745, 11.2640), (43.7717, 11.2640), (43.7717, 11.2545), (43.7735, 11.2548)]),
    dict(name="Santa Trinita and the Mercato Nuovo", periods=LATE, density="dense", polygon=[(43.7713, 11.2463), (43.7713, 11.2538), (43.7687, 11.2538), (43.7701, 11.2502), (43.7708, 11.2476)]),
    dict(name="Santa Croce", periods=LATE, density="dense", polygon=[(43.7712, 11.2544), (43.7712, 11.2665), (43.7690, 11.2668), (43.7662, 11.2642), (43.7664, 11.2610), (43.7676, 11.2560), (43.7684, 11.2544)]),
    dict(name="Ognissanti", periods=LATE, density="dense", polygon=[(43.7720, 11.2463), (43.7733, 11.2425), (43.7745, 11.2405), (43.7758, 11.2414), (43.7745, 11.2455), (43.7728, 11.2474)]),
    dict(name="Oltrarno", periods=LATE, density="dense", polygon=[(43.7722, 11.2406), (43.7703, 11.2460), (43.7689, 11.2490), (43.7684, 11.2510), (43.7673, 11.2528), (43.7664, 11.2555),
                                                                     (43.7656, 11.2585), (43.7649, 11.2585), (43.7649, 11.2520), (43.7658, 11.2490), (43.7662, 11.2455), (43.7680, 11.2420), (43.7705, 11.2404)]),
    dict(name="San Niccolò", periods=LATE, density="loose", polygon=[(43.7652, 11.2595), (43.7644, 11.2638), (43.7636, 11.2636), (43.7644, 11.2592)]),
    dict(name="Via Romana and San Pier Gattolino", periods=LATE, density="loose", polygon=[(43.7656, 11.2468), (43.7640, 11.2455), (43.7612, 11.2440), (43.7606, 11.2448), (43.7630, 11.2462), (43.7648, 11.2472)]),
    dict(name="Sant'Ambrogio and Borgo la Croce", periods=LATE, density="loose", polygon=[(43.7745, 11.2645), (43.7740, 11.2705), (43.7700, 11.2712), (43.7698, 11.2672), (43.7715, 11.2645)]),
    dict(name="Cafaggio and the Annunziata", periods=LATE, density="loose", polygon=[(43.7782, 11.2590), (43.7800, 11.2620), (43.7790, 11.2655), (43.7760, 11.2655), (43.7750, 11.2630)]),
    dict(name="Via San Gallo", periods=LATE, density="loose", polygon=[(43.7780, 11.2550), (43.7840, 11.2570), (43.7840, 11.2586), (43.7782, 11.2580)]),
    dict(name="Via della Scala and the Prato", periods=LATE, density="loose", polygon=[(43.7750, 11.2462), (43.7760, 11.2455), (43.7768, 11.2438), (43.7778, 11.2445), (43.7770, 11.2488), (43.7760, 11.2505)]),
]

GARDENS = [
    dict(name="Centuriated fields north", periods=[R], kind="orchard", polygon=[(43.7745, 11.2580), (43.7800, 11.2600), (43.7860, 11.2640), (43.7860, 11.2720), (43.7770, 11.2700), (43.7740, 11.2630)]),
    dict(name="Centuriated fields north-west", periods=[R], kind="orchard", polygon=[(43.7745, 11.2470), (43.7790, 11.2460), (43.7850, 11.2470), (43.7860, 11.2530), (43.7790, 11.2520), (43.7750, 11.2510)]),
    dict(name="Vineyards of the hills", periods=[R], kind="vineyard", polygon=[(43.7660, 11.2470), (43.7650, 11.2530), (43.7625, 11.2560), (43.7600, 11.2500), (43.7615, 11.2450), (43.7645, 11.2440)]),
    dict(name="Vineyards of Monte alle Croci", periods=[R, C], kind="vineyard", polygon=[(43.7640, 11.2580), (43.7625, 11.2660), (43.7600, 11.2700), (43.7585, 11.2620), (43.7605, 11.2575)]),
    dict(name="Orti of Cafaggio", periods=[C], kind="orchard", polygon=[(43.7770, 11.2588), (43.7805, 11.2600), (43.7810, 11.2650), (43.7760, 11.2655), (43.7750, 11.2625)]),
    dict(name="Orti by the new walls (west)", periods=[C], kind="orchard", polygon=[(43.7745, 11.2470), (43.7765, 11.2425), (43.7790, 11.2440), (43.7785, 11.2500), (43.7760, 11.2515)]),
    dict(name="Prato d'Ognissanti", periods=ALL[1:], kind="park", polygon=[(43.7763, 11.2398), (43.7777, 11.2406), (43.7773, 11.2419), (43.7761, 11.2413)]),
    dict(name="Orti of Oltrarno", periods=[C, M], kind="orchard", polygon=[(43.7660, 11.2420), (43.7655, 11.2450), (43.7625, 11.2440), (43.7630, 11.2420)]),
    dict(name="Hillside vineyards behind the Pitti", periods=[C, M], kind="vineyard", polygon=[(43.7645, 11.2478), (43.7645, 11.2520), (43.7625, 11.2515), (43.7612, 11.2495), (43.7615, 11.2472)]),
    dict(name="Medici garden at San Marco", periods=[M], kind="park", polygon=[(43.7790, 11.2585), (43.7800, 11.2588), (43.7798, 11.2602), (43.7789, 11.2598)]),
    dict(name="Orti of Pinti and Cafaggio", periods=LATE, kind="orchard", polygon=[(43.7800, 11.2622), (43.7825, 11.2640), (43.7810, 11.2665), (43.7792, 11.2660)]),
    dict(name="Convent gardens of the north-west", periods=LATE, kind="orchard", polygon=[(43.7774, 11.2492), (43.7795, 11.2440), (43.7800, 11.2455), (43.7790, 11.2520), (43.7778, 11.2520)]),
    dict(name="Orti Oricellari", periods=LATE, kind="park", polygon=[(43.7750, 11.2445), (43.7758, 11.2428), (43.7765, 11.2434), (43.7757, 11.2452)]),
    dict(name="Orti of the Oltrarno walls", periods=LATE, kind="orchard", polygon=[(43.7690, 11.2408), (43.7680, 11.2420), (43.7640, 11.2440), (43.7618, 11.2436), (43.7640, 11.2418), (43.7665, 11.2410)]),
    dict(name="Giardino dei Semplici", periods=[G], kind="park", polygon=[(43.7795, 11.2600), (43.7805, 11.2602), (43.7803, 11.2617), (43.7796, 11.2614)]),
    dict(name="Boboli Gardens", periods=[G], kind="park", polygon=[(43.7645, 11.2476), (43.7646, 11.2518), (43.7636, 11.2516), (43.7624, 11.2510), (43.7614, 11.2496), (43.7610, 11.2482), (43.7618, 11.2472), (43.7633, 11.2468)]),
    dict(name="Le Cascine", periods=[G], kind="park", polygon=[(43.7795, 11.2368), (43.7775, 11.2352), (43.7778, 11.2325), (43.7790, 11.2298), (43.7810, 11.2300), (43.7812, 11.2345)]),
    dict(name="Vineyards of San Miniato", periods=LATE, kind="vineyard", polygon=[(43.7618, 11.2660), (43.7600, 11.2700), (43.7585, 11.2680), (43.7582, 11.2620), (43.7600, 11.2610)]),
    dict(name="Bellosguardo", periods=LATER, kind="vineyard", polygon=[(43.7640, 11.2330), (43.7630, 11.2395), (43.7600, 11.2410), (43.7585, 11.2360), (43.7600, 11.2320)]),
]

DISTRICTS = [
    dict(id="castrum", name="Colonia Florentia", periods=[R], polygon=ROMAN_WALL,
         description="The walled colony: four quarters of a regular grid round the forum, the houses of veterans and traders, shops under the porticoes of the cardo."),
    dict(id="oltrarno-1300", name="Oltrarno", periods=[C], polygon=OLTRARNO_1300,
         description="The sesto across the river, walled in 1173: the Bardi and Frescobaldi bankers along the bank, the Augustinians at Santo Spirito, dyers and weavers toward San Frediano."),
    dict(id="santo-spirito-q", name="Quartiere di Santo Spirito", periods=LATE, polygon=[(43.7726, 11.2402), (43.7703, 11.2460), (43.7680, 11.2531), (43.7659, 11.2596), (43.7644, 11.2651), (43.7621, 11.2605), (43.7627, 11.2521), (43.7593, 11.2444), (43.7660, 11.2406)],
         description="The Oltrarno, one of the four quarters into which the city was divided from 1343: palaces of old families along Via Maggio, the Pitti, and the workers' streets of San Frediano."),
    dict(id="santa-croce-q", name="Quartiere di Santa Croce", periods=LATE, polygon=[(43.7712, 11.2541), (43.7718, 11.2610), (43.7713, 11.2717), (43.7646, 11.2716), (43.7659, 11.2596), (43.7684, 11.2540)],
         description="The south-east quarter, from the Piazza della Signoria to the Franciscans: the dyers and wool-workers of the Corso dei Tintori, the Bargello and the Stinche prison."),
    dict(id="san-giovanni-q", name="Quartiere di San Giovanni", periods=LATE, polygon=[(43.7714, 11.2541), (43.7733, 11.2543), (43.7853, 11.2593), (43.7812, 11.2668), (43.7713, 11.2717), (43.7718, 11.2610)],
         description="The quarter of the Baptistery: the cathedral, the Medici palace on Via Larga, San Marco and the Annunziata with the Innocenti."),
    dict(id="santa-maria-novella-q", name="Quartiere di Santa Maria Novella", periods=LATE, polygon=[(43.7714, 11.2541), (43.7733, 11.2543), (43.7853, 11.2593), (43.7803, 11.2462), (43.7748, 11.2368), (43.7707, 11.2460)],
         description="The north-west quarter: the Dominicans, San Lorenzo, the Rucellai and Strozzi palaces, the Umiliati at Ognissanti and the meadow of the Prato."),
]

LABELS = [
    dict(text="Arnus", position=(43.7702, 11.2470), size="lg", rotation=-22, periods=[R]),
    dict(text="Arno", position=(43.7702, 11.2470), size="lg", rotation=-22, periods=LATER),
    dict(text="Arno", position=(43.7640, 11.2700), size="md", rotation=-15, periods=ALL),
    dict(text="Florentia", position=(43.7745, 11.2600), size="lg", periods=[R]),
    dict(text="Oltrarno", position=(43.7670, 11.2430), size="md", periods=LATER),
    dict(text="Mugnone", position=(43.7838, 11.2468), size="sm", rotation=40, periods=LATER),
    dict(text="Pescaia di Santa Rosa", position=(43.7734, 11.2385), size="sm", rotation=-25, periods=LATER),
    dict(text="Pescaia di San Niccolò", position=(43.7652, 11.2672), size="sm", rotation=-12, periods=LATER),
    dict(text="Boboli", position=(43.7628, 11.2488), size="md", periods=[G]),
    dict(text="Le Cascine", position=(43.7790, 11.2318), size="sm", periods=[G]),
    dict(text="Il Prato", position=(43.7775, 11.2420), size="sm", periods=LATER),
    dict(text="Monte alle Croci", position=(43.7585, 11.2660), size="sm", periods=ALL),
    dict(text="Bellosguardo", position=(43.7600, 11.2350), size="sm", periods=ALL),
    dict(text="Via Cassia", position=(43.7620, 11.2445), size="sm", rotation=45, periods=[R]),
]
