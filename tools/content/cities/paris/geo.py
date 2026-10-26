# Paris: city, frame, eras and the map's geography (see tools/content/cities/FORMAT.md).
ALL = ["lutetia-200", "capetian-1000", "philippe-1250", "valois-1550", "louis-1789"]
EARLY = ["lutetia-200", "capetian-1000"]
MEDIEVAL = ["capetian-1000", "philippe-1250", "valois-1550"]
WALLED = ["philippe-1250", "valois-1550"]
LATER = ["philippe-1250", "valois-1550", "louis-1789"]
PRE_1614 = ["lutetia-200", "capetian-1000", "philippe-1250", "valois-1550"]

CITY = dict(
    name="Paris", subtitle="Lutetia to the Revolution",
    description="Paris from Roman Lutetia on the left bank to the eve of the Revolution: the Seine and its islands, the Cité, the right-bank Ville and the left-bank University, inside the walls of Philippe Auguste and Charles V. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="philippe-1250",
    world=dict(heightScale=1.0, walls=["#E4D8C0", "#D9CBB0", "#EAE0CC", "#CFC0A2"], roofs=["#5C6068", "#6A6E74", "#8A6A5A"]),
    camera=dict(target=(48.8545, 2.3480), distance=38),
)
FRAME = ((48.8745, 2.3170), (48.8365, 2.3800))
PALETTE = dict(parchment="#E7D6AE", ink="#5F4532", water="#6A8C93", hill="#7A7F5E", road="#8A6A4A")
COMPASS = (48.8712, 2.3760)
CARTOUCHE = (48.8385, 2.3190)

PERIODS = [
    dict(id="lutetia-200", label="Roman Lutetia", year=200, startYear=-52, endYear=486,
         summary="Lutetia of the Parisii: a modest Gallo-Roman town laid out on a grid on the left-bank slope of Mons Lucotitius, with a forum astride the cardo, three public baths fed by an aqueduct from Wissous, an arena, and a quarter of temples and houses on the island. Limestone quarried on the spot, timber and tile; a wooden bridge at each end of the island.",
         population="perhaps 6,000–8,000",
         feel="Boatmen calling on the river, smoke from the baths' furnaces, the clink of stonecutters working the local limestone.",
         style="antique",
         houses=dict(title="Houses of Lutetia", text="Rectangular houses of rubble and timber framing on stone footings, plastered and roofed with red tile, set along the gridded streets of the left bank; shops open onto the street, small gardens and wells behind."),
         outskirts=dict(title="Vineyards and villas", text="Vines and gardens on the slopes of the hill, a few villas, potters' kilns and the cemeteries lining the roads south toward Orléans and Italy.")),
    dict(id="capetian-1000", label="Capetian Paris", year=1000, startYear=487, endYear=1189,
         summary="Clovis made Paris his seat about 508; the Vikings besieged the Cité in 885–86. Around 1000, under Robert the Pious, the town is still mostly the island inside its Roman wall, with the palace at one end and the cathedral of Saint-Étienne at the other. Walled abbeys stand in the fields; small bourgs grow round the right-bank port and the churches of the left bank.",
         population="perhaps 20,000 around 1000, growing fast in the 12th century",
         feel="Monastery bells across the meadows, the creak of mill wheels under the Grand Pont, mud and woodsmoke in the island's lanes.",
         style="gothic",
         houses=dict(title="Houses of the Cité", text="Narrow timber-framed houses with wattle-and-daub infill on stone cellars, two or three storeys, thatched or shingled, packed along the lanes of the island and the little bourgs at the bridgeheads."),
         outskirts=dict(title="Bourgs, vineyards and marsh", text="Clusters of houses round the abbeys and parish churches, enclosed vineyards (clos) on the left-bank hill, and the drained marsh gardens of the right bank.")),
    dict(id="philippe-1250", label="Gothic Paris", year=1250, startYear=1190, endYear=1355,
         summary="The largest city in Christian Europe, inside the new wall of Philippe Auguste (1190–1215). Saint Louis reigns; Notre-Dame is nearly finished and the Sainte-Chapelle has just been consecrated (1248). Three towns in one: the Cité of king and bishop, the merchants' Ville on the right bank with the Halles and the Grève, and the University's Latin Quarter on the left.",
         population="perhaps 150,000–200,000",
         feel="Students arguing in Latin, criers calling wine and baths through the streets, cart wheels on the new paving, the reek of the Grande Boucherie.",
         style="gothic",
         houses=dict(title="Gabled houses of the Ville", text="Tall, narrow timber-framed houses, gable end to the street, on stone ground floors with shop counters folding down onto the street; plastered fronts, jettied upper storeys, tile or slate roofs. Courtyards, wells and privies behind."),
         outskirts=dict(title="Faubourgs and clos", text="Outside the wall: abbey bourgs, vineyards and walled clos, market gardens in the drained Marais, windmills, and hamlets strung along the roads.")),
    dict(id="valois-1550", label="Renaissance Paris", year=1550, startYear=1356, endYear=1660,
         summary="The capital of Henri II, now behind the right-bank wall of Charles V with the Bastille at its east gate. Pierre Lescot is rebuilding the Louvre in the new Italian manner, the Hôtel de Ville is rising on the Grève, and the Pont Notre-Dame carries a street of uniform houses. Printers fill the rue Saint-Jacques; religious war is coming.",
         population="perhaps 250,000–300,000",
         feel="Presses thumping in the rue Saint-Jacques, hawkers' cries, church bells by the hundred, the stink of the tanneries and the river.",
         style="gothic",
         houses=dict(title="Houses of Renaissance Paris", text="Gabled timber-framed houses of four and five storeys, many now plastered over against fire, on stone ground floors with shops; noble hôtels of stone between court and garden appear in the Marais and the faubourg Saint-Germain."),
         outskirts=dict(title="Faubourgs", text="Suburbs spilling past the gates: the fair-town of Saint-Germain, tanners and dyers on the Bièvre, market gardens of the Marais, windmills on the mounds.")),
    dict(id="louis-1789", label="Paris on the Eve of the Revolution", year=1789, startYear=1661, endYear=1799,
         summary="The walls are gone, turned into tree-lined boulevards; the Farmers-General customs wall (1785–90) lies far out of frame. Place Louis XV opens west of the Tuileries gardens, the new church of Sainte-Geneviève (the Panthéon) is nearly done, the Pont Neuf is the city's street. On 14 July 1789 the crowd takes the Bastille.",
         population="about 600,000–650,000",
         feel="Coaches rattling on paving stones, newsboys crying pamphlets, café talk at the Palais-Royal, mud and horse dung everywhere.",
         style="early-modern",
         houses=dict(title="Houses of 18th-century Paris", text="Five- and six-storey houses of pale limestone or plaster over timber, regular windows, mansard roofs with dormers; shops on the ground floor, the bourgeois on the first floor, the poor in the garrets. Building height is capped by royal regulation."),
         outskirts=dict(title="Faubourgs and gardens", text="Aristocratic hôtels with long gardens in the faubourg Saint-Germain, artisans' courts in the faubourg Saint-Antoine, convent gardens and market plots toward the customs wall.")),
]

SOURCES = [
    dict(id="wiki-paris-history", title="History of Paris", author="Wikipedia", url="https://en.wikipedia.org/wiki/History_of_Paris"),
    dict(id="wiki-lutetia", title="Lutetia", author="Wikipedia", url="https://en.wikipedia.org/wiki/Lutetia"),
    dict(id="wiki-wall-philippe", title="Wall of Philippe II Augustus", author="Wikipedia", url="https://en.wikipedia.org/wiki/Wall_of_Philip_II_Augustus"),
    dict(id="wiki-wall-charles-v", title="Wall of Charles V", author="Wikipedia", url="https://en.wikipedia.org/wiki/Wall_of_Charles_V"),
    dict(id="wiki-ile-de-la-cite", title="Île de la Cité", author="Wikipedia", url="https://en.wikipedia.org/wiki/%C3%8Ele_de_la_Cit%C3%A9"),
    dict(id="wiki-ile-saint-louis", title="Île Saint-Louis", author="Wikipedia", url="https://en.wikipedia.org/wiki/%C3%8Ele_Saint-Louis"),
    dict(id="wiki-ile-louviers", title="Île Louviers", author="Wikipedia", url="https://en.wikipedia.org/wiki/%C3%8Ele_Louviers"),
    dict(id="wiki-bievre", title="Bièvre (river)", author="Wikipedia", url="https://en.wikipedia.org/wiki/Bi%C3%A8vre_(river)"),
    dict(id="wiki-grands-boulevards", title="Grands Boulevards", author="Wikipedia", url="https://en.wikipedia.org/wiki/Grands_Boulevards"),
    dict(id="busson", title="Lutèce: Paris de César à Clovis / Le Paris antique", author="Didier Busson", year=2001),
    dict(id="lombard-jourdan", title="Aux origines de Paris: la genèse de la rive droite jusqu'en 1223", author="Anne Lombard-Jourdan", year=1985),
    dict(id="boussard", title="Nouvelle histoire de Paris: De la fin du siège de 885–886 à la mort de Philippe Auguste", author="Jacques Boussard", year=1976),
    dict(id="cazelles", title="Nouvelle histoire de Paris: De la fin du règne de Philippe Auguste à la mort de Charles V", author="Raymond Cazelles", year=1972),
    dict(id="jones-paris", title="Paris: Biography of a City", author="Colin Jones", year=2004),
    dict(id="hillairet", title="Dictionnaire historique des rues de Paris", author="Jacques Hillairet", year=1963),
    dict(id="turgot-plan", title="Plan de Paris (the Turgot plan)", author="Louis Bretez for Michel-Étienne Turgot", year=1739, url="https://en.wikipedia.org/wiki/Turgot_map_of_Paris"),
    dict(id="truschet-hoyau", title="Plan de Paris (the Truschet and Hoyau or 'Basel' plan)", author="Olivier Truschet and Germain Hoyau", year="c. 1550", url="https://fr.wikipedia.org/wiki/Plan_de_Truschet_et_Hoyau"),
]

# ---------------------------------------------------------------- water and islands
# Draw order matters: small arms first, then the south arm, then the main stream; islands are painted on top.
WATER = [
    dict(id="bras-louviers", name="Bras de Grammont", path=[(48.8516, 2.3640), (48.8500, 2.3670), (48.8486, 2.3682), (48.8476, 2.3662)], width=40,
         blurb="The narrow arm between the right bank and the Île Louviers, a timber yard for most of its history; it was filled in in 1843 and is now the boulevard Morland."),
    dict(id="seine-petit-bras", name="Seine (petit bras)", path=[(48.8574, 2.3392), (48.8568, 2.3400), (48.8560, 2.3410), (48.8551, 2.3428), (48.8545, 2.3444), (48.8536, 2.3464), (48.8532, 2.3478), (48.8524, 2.3496), (48.8517, 2.3518), (48.8511, 2.3545), (48.8505, 2.3575), (48.8501, 2.3598), (48.8500, 2.3615)], width=150,
         blurb="The south arm of the Seine, narrow and shallow, between the Cité and the left bank. The Petit Pont has crossed it since Roman times, always on the line of the rue Saint-Jacques."),
    dict(id="seine", name="Seine", path=[(48.8635, 2.3160), (48.8627, 2.3200), (48.8614, 2.3260), (48.8602, 2.3300), (48.8592, 2.3340), (48.8584, 2.3378), (48.8582, 2.3420), (48.8574, 2.3450), (48.8567, 2.3470), (48.8562, 2.3490), (48.8555, 2.3510), (48.8545, 2.3530), (48.8537, 2.3550), (48.8530, 2.3575), (48.8524, 2.3600), (48.8514, 2.3625), (48.8496, 2.3637), (48.8475, 2.3645), (48.8441, 2.3664), (48.8405, 2.3705), (48.8360, 2.3785)], width=175,
         blurb="Sequana to the Romans. The river made Paris: the merchants of the water (the nautae, later the marchands de l'eau) ran its trade, and the city's arms are still a ship. Wine, wood, grain and hay came down it to the right-bank ports of the Grève and the École."),
    dict(id="bievre", name="Bièvre", path=[(48.8362, 2.3505), (48.8378, 2.3530), (48.8398, 2.3552), (48.8420, 2.3580), (48.8438, 2.3612), (48.8452, 2.3635)], width=10,
         blurb="A little river from the south, lined from the 15th century with tanners, dyers and the Gobelins tapestry works, and thick with their waste. The monks of Saint-Victor diverted part of it through their abbey in the 12th century."),
]

ISLANDS = [
    dict(name="Île de la Cité", periods=EARLY, polygon=[
        (48.8576, 2.3418), (48.8576, 2.3432), (48.8573, 2.3448), (48.8567, 2.3470), (48.8562, 2.3490), (48.8555, 2.3505), (48.8545, 2.3513),
        (48.8533, 2.3517), (48.8524, 2.3514), (48.8521, 2.3504), (48.8526, 2.3487), (48.8532, 2.3474), (48.8538, 2.3460), (48.8545, 2.3446),
        (48.8554, 2.3430), (48.8563, 2.3418), (48.8570, 2.3414)]),
    dict(name="Île de la Cité", periods=WALLED, polygon=[
        (48.8577, 2.3415), (48.8578, 2.3430), (48.8574, 2.3448), (48.8567, 2.3470), (48.8562, 2.3490), (48.8555, 2.3506), (48.8544, 2.3517),
        (48.8532, 2.3524), (48.8521, 2.3527), (48.8516, 2.3520), (48.8521, 2.3504), (48.8526, 2.3487), (48.8532, 2.3474), (48.8538, 2.3460),
        (48.8545, 2.3446), (48.8554, 2.3428), (48.8563, 2.3413), (48.8571, 2.3410)]),
    dict(name="Île de la Cité", periods=["louis-1789"], polygon=[
        (48.8575, 2.3388), (48.8580, 2.3402), (48.8578, 2.3430), (48.8574, 2.3448), (48.8567, 2.3470), (48.8562, 2.3490), (48.8555, 2.3506),
        (48.8544, 2.3517), (48.8532, 2.3524), (48.8521, 2.3529), (48.8515, 2.3520), (48.8521, 2.3504), (48.8526, 2.3487), (48.8532, 2.3474),
        (48.8538, 2.3460), (48.8545, 2.3446), (48.8554, 2.3428), (48.8563, 2.3408), (48.8569, 2.3395)]),
    dict(name="Île aux Juifs", periods=PRE_1614, polygon=[(48.8577, 2.3393), (48.8579, 2.3405), (48.8576, 2.3411), (48.8571, 2.3404), (48.8572, 2.3395)]),
    dict(name="Île du Patriarche", periods=PRE_1614, polygon=[(48.8569, 2.3398), (48.8570, 2.3407), (48.8566, 2.3410), (48.8564, 2.3403)]),
    dict(name="Île Notre-Dame", periods=PRE_1614, polygon=[
        (48.8527, 2.3536), (48.8533, 2.3550), (48.8533, 2.3565), (48.8530, 2.3578), (48.8513, 2.3578), (48.8512, 2.3562), (48.8516, 2.3546)]),
    dict(name="Île aux Vaches", periods=PRE_1614, polygon=[
        (48.8528, 2.3584), (48.8524, 2.3604), (48.8515, 2.3627), (48.8506, 2.3634), (48.8501, 2.3622), (48.8505, 2.3598), (48.8510, 2.3584)]),
    dict(name="Île Saint-Louis", periods=["louis-1789"], polygon=[
        (48.8527, 2.3535), (48.8533, 2.3550), (48.8533, 2.3570), (48.8528, 2.3592), (48.8523, 2.3607), (48.8515, 2.3627), (48.8506, 2.3634),
        (48.8501, 2.3622), (48.8505, 2.3598), (48.8510, 2.3570), (48.8513, 2.3555), (48.8516, 2.3544)]),
    dict(name="Île Louviers", polygon=[(48.8512, 2.3643), (48.8505, 2.3660), (48.8489, 2.3676), (48.8483, 2.3672), (48.8496, 2.3652), (48.8506, 2.3638)]),
]

HILLS = [
    dict(id="montagne", name="Montagne Sainte-Geneviève", center=(48.8462, 2.3478), radius=420, label=False,
         blurb="The limestone hill of the left bank, Mons Lucotitius to the Romans, who built their forum on its shoulder. Saint Geneviève was buried on the summit in the early 6th century; the abbey named after her, then the colleges of the University, covered it."),
    dict(id="butte-saint-roch", name="Butte Saint-Roch", center=(48.8660, 2.3330), radius=150, periods=PRE_1614,
         blurb="A mound of rubbish and spoil outside the Saint-Honoré gate, crowned with windmills; Joan of Arc was wounded attacking the city near here in 1429. It was levelled from the 1660s for the new quarter round the rue de Richelieu."),
    dict(id="monceau-saint-gervais", name="Monceau Saint-Gervais", center=(48.8558, 2.3540), radius=90, label=False, periods=EARLY,
         blurb="A low gravel rise on the right bank, safe from the floods, where the first settlement north of the river grew round the church of Saint-Gervais."),
]

MARSH = [
    dict(name="The Marais (marsh)", periods=["lutetia-200"], polygon=[(48.8590, 2.3540), (48.8640, 2.3500), (48.8690, 2.3560), (48.8690, 2.3680), (48.8620, 2.3720), (48.8560, 2.3680)]),
    dict(name="The Marais (draining marsh)", periods=["capetian-1000"], polygon=[(48.8620, 2.3560), (48.8670, 2.3540), (48.8700, 2.3600), (48.8690, 2.3690), (48.8640, 2.3720), (48.8600, 2.3660)]),
    dict(name="Bièvre meadows", periods=["lutetia-200", "capetian-1000"], polygon=[(48.8372, 2.3500), (48.8400, 2.3530), (48.8430, 2.3585), (48.8420, 2.3600), (48.8392, 2.3565), (48.8366, 2.3530)]),
]

# ---------------------------------------------------------------- roads
ROADS = [
    # Roman Lutetia
    dict(id="cardo", name="Cardo maximus (rue Saint-Jacques)", periods=["lutetia-200"], width=12, style="major", labelled=True,
         path=[(48.8565, 2.3492), (48.8545, 2.3482), (48.8532, 2.3475), (48.8515, 2.3468), (48.8500, 2.3459), (48.8485, 2.3450), (48.8466, 2.3438), (48.8440, 2.3424), (48.8410, 2.3411), (48.8366, 2.3397)],
         blurb="The main north–south street of Lutetia, paved and colonnaded, crossing the island and climbing the hill toward Orléans. The rue Saint-Jacques still follows it."),
    dict(id="cardo-west", name="Western cardo (boulevard Saint-Michel line)", periods=["lutetia-200"], width=8, style="minor",
         path=[(48.8532, 2.3440), (48.8505, 2.3427), (48.8475, 2.3410), (48.8440, 2.3390), (48.8400, 2.3375)],
         blurb="A parallel street to the west, past the Cluny baths; the line of the medieval rue de la Harpe and today's boulevard Saint-Michel."),
    dict(id="decumanus", name="Decumanus (rue des Écoles line)", periods=["lutetia-200"], width=8, style="minor",
         path=[(48.8495, 2.3400), (48.8492, 2.3440), (48.8488, 2.3480), (48.8483, 2.3520)],
         blurb="An east–west street of the Roman grid; its exact line is reconstructed from scattered finds."),
    dict(id="via-italia", name="Road to Italy (rue Mouffetard)", periods=["lutetia-200", "capetian-1000", "philippe-1250", "valois-1550", "louis-1789"], width=10, style="major", labelled=True,
         path=[(48.8510, 2.3478), (48.8500, 2.3486), (48.8485, 2.3490), (48.8465, 2.3492), (48.8448, 2.3495), (48.8425, 2.3498), (48.8395, 2.3502), (48.8365, 2.3507)],
         blurb="The Roman road south-east toward Lyon and Italy, up the Montagne and down the far side; the rue de la Montagne-Sainte-Geneviève, rue Descartes and rue Mouffetard follow it."),
    dict(id="via-senlis", name="Road to Senlis (rue Saint-Martin)", periods=["lutetia-200", "capetian-1000"], width=9, style="major",
         path=[(48.8568, 2.3497), (48.8590, 2.3502), (48.8612, 2.3510), (48.8640, 2.3525), (48.8665, 2.3546), (48.8692, 2.3566), (48.8745, 2.3590)],
         blurb="The Roman road north from the Grand Pont, along a gravel ridge above the marsh; the rue Saint-Martin follows it."),
    dict(id="via-melun", name="Road to Melun (rue Saint-Antoine)", periods=["lutetia-200", "capetian-1000"], width=8, style="minor",
         path=[(48.8565, 2.3510), (48.8556, 2.3560), (48.8545, 2.3610), (48.8540, 2.3680), (48.8525, 2.3740), (48.8505, 2.3800)],
         blurb="The road east along the right bank toward Melun and Sens; later the rue Saint-Antoine."),
    dict(id="cite-street", name="Rue de la Juiverie (the island's high street)", periods=["capetian-1000", "philippe-1250", "valois-1550", "louis-1789"], width=9, style="major",
         path=[(48.8532, 2.3475), (48.8545, 2.3482), (48.8556, 2.3488), (48.8562, 2.3492)],
         blurb="The street across the Cité from the Petit Pont to the bridge over the north arm, on the line of the Roman cardo: the rue du Marché-Palu, the rue de la Juiverie (the Jews' street until their expulsion in 1182) and the rue de la Lanterne."),
    # medieval and later
    dict(id="rue-saint-jacques", name="Rue Saint-Jacques", periods=["capetian-1000", "philippe-1250", "valois-1550", "louis-1789"], width=11, style="major", labelled=True,
         path=[(48.8527, 2.3474), (48.8515, 2.3468), (48.8500, 2.3459), (48.8485, 2.3450), (48.8466, 2.3438), (48.8440, 2.3424), (48.8410, 2.3411), (48.8366, 2.3397)],
         blurb="The Roman cardo, and the pilgrims' road to Compostela: the great street of the University, of the Dominicans (the 'Jacobins'), and from the 1470s of the printers and booksellers."),
    dict(id="rue-saint-martin", name="Rue Saint-Martin", periods=LATER, width=10, style="major", labelled=True,
         path=[(48.8568, 2.3497), (48.8590, 2.3502), (48.8612, 2.3510), (48.8640, 2.3525), (48.8665, 2.3546), (48.8692, 2.3566), (48.8745, 2.3590)],
         blurb="The old Roman road north, past Saint-Merry and the priory of Saint-Martin-des-Champs toward Senlis and Flanders."),
    dict(id="rue-saint-denis", name="Rue Saint-Denis", periods=["capetian-1000", "philippe-1250", "valois-1550", "louis-1789"], width=11, style="major", labelled=True,
         path=[(48.8584, 2.3479), (48.8600, 2.3485), (48.8610, 2.3490), (48.8640, 2.3501), (48.8670, 2.3515), (48.8700, 2.3528), (48.8745, 2.3546)],
         blurb="The Grande Rue: the royal way from the Châtelet to the abbey of Saint-Denis, taken by kings entering Paris and by their funerals leaving it."),
    dict(id="rue-saint-honore", name="Rue Saint-Honoré", periods=["capetian-1000", "philippe-1250", "valois-1550", "louis-1789"], width=10, style="major", labelled=True,
         path=[(48.8603, 2.3472), (48.8608, 2.3440), (48.8615, 2.3410), (48.8628, 2.3372), (48.8648, 2.3325), (48.8663, 2.3280), (48.8685, 2.3220), (48.8700, 2.3170)],
         blurb="The road west from the Halles toward Normandy, past Saint-Honoré's church and, outside the gate, the hospital of the Quinze-Vingts. By the 18th century the richest shopping street in Paris."),
    dict(id="rue-saint-antoine", name="Rue Saint-Antoine", periods=LATER, width=14, style="major", labelled=True,
         path=[(48.8565, 2.3530), (48.8556, 2.3560), (48.8547, 2.3605), (48.8541, 2.3650), (48.8540, 2.3680), (48.8536, 2.3710), (48.8524, 2.3745), (48.8505, 2.3800)],
         blurb="The widest street of medieval Paris, used for tournaments and royal entries; Henri II was mortally wounded jousting here in 1559. It runs out past the Bastille to the abbey of Saint-Antoine."),
    dict(id="rue-du-temple", name="Rue du Temple", periods=LATER, width=8, style="minor", labelled=True,
         path=[(48.8572, 2.3532), (48.8600, 2.3546), (48.8628, 2.3565), (48.8652, 2.3590), (48.8680, 2.3618)],
         blurb="The street from the Grève to the Templars' enclosure, through the Marais."),
    dict(id="rue-montmartre", name="Rue Montmartre", periods=LATER, width=8, style="minor",
         path=[(48.8642, 2.3458), (48.8665, 2.3448), (48.8692, 2.3440), (48.8745, 2.3428)],
         blurb="The road north from Saint-Eustache toward the hill and abbey of Montmartre."),
    dict(id="rue-de-la-verrerie", name="Rue de la Verrerie", periods=LATER, width=7, style="minor",
         path=[(48.8594, 2.3488), (48.8590, 2.3515), (48.8582, 2.3545), (48.8570, 2.3580)],
         blurb="The glassmakers' street, the old east–west route behind the Grève through the parish of Saint-Merry."),
    dict(id="rue-galande", name="Rue Galande and rue Saint-Victor", periods=["capetian-1000", "philippe-1250", "valois-1550", "louis-1789"], width=8, style="minor",
         path=[(48.8522, 2.3474), (48.8515, 2.3485), (48.8505, 2.3500), (48.8492, 2.3522), (48.8478, 2.3548), (48.8462, 2.3580)],
         blurb="From the Petit Pont past the place Maubert and the rue du Fouarre, where arts students sat on straw at their lectures, to the abbey of Saint-Victor."),
    dict(id="rue-de-la-harpe", name="Rue de la Harpe", periods=["capetian-1000", "philippe-1250", "valois-1550", "louis-1789"], width=8, style="minor",
         path=[(48.8536, 2.3446), (48.8515, 2.3432), (48.8500, 2.3424), (48.8485, 2.3414), (48.8460, 2.3400)],
         blurb="The University's western street, from the Pont Saint-Michel past the Cluny ruins to the Porte Saint-Michel."),
    dict(id="rue-saint-andre", name="Rue Saint-André-des-Arts and rue de Buci", periods=["capetian-1000", "philippe-1250", "valois-1550", "louis-1789"], width=8, style="minor",
         path=[(48.8536, 2.3442), (48.8534, 2.3420), (48.8533, 2.3395), (48.8536, 2.3375), (48.8537, 2.3360)],
         blurb="The road from the Cité bridges west to the abbey of Saint-Germain-des-Prés and its fair."),
    dict(id="rue-de-vaugirard", name="Rue de Vaugirard", periods=["valois-1550", "louis-1789"], width=8, style="minor",
         path=[(48.8478, 2.3405), (48.8488, 2.3370), (48.8475, 2.3300), (48.8450, 2.3230), (48.8425, 2.3170)],
         blurb="The road to the village of Vaugirard (today the longest street in Paris), past the Luxembourg palace (1615)."),
    dict(id="rue-dauphine", name="Rue Dauphine", periods=["louis-1789"], width=9, style="minor",
         path=[(48.8558, 2.3399), (48.8547, 2.3390), (48.8536, 2.3382)],
         blurb="Cut in 1607 through the gardens of the Grands-Augustins to carry the traffic of the new Pont Neuf to the faubourg Saint-Germain."),
    dict(id="rue-de-richelieu", name="Rue de Richelieu", periods=["louis-1789"], width=9, style="minor",
         path=[(48.8635, 2.3372), (48.8665, 2.3378), (48.8695, 2.3385), (48.8716, 2.3388)],
         blurb="The street laid out over the levelled Butte Saint-Roch beside Richelieu's palace (the Palais-Royal), home of the royal library."),
    dict(id="rue-de-grenelle", name="Rue du Bac and rue de Grenelle", periods=["louis-1789"], width=9, style="minor",
         path=[(48.8604, 2.3283), (48.8575, 2.3265), (48.8545, 2.3255), (48.8535, 2.3215), (48.8545, 2.3170)],
         blurb="The rue du Bac, named after the ferry that the Pont Royal replaced, and the rue de Grenelle: streets of the faubourg Saint-Germain, the quarter of aristocratic hôtels between court and garden."),
    dict(id="boulevards", name="The Boulevards (Nouveau Cours)", periods=["louis-1789"], width=36, style="major", labelled=True,
         path=[(48.8532, 2.3700), (48.8570, 2.3688), (48.8610, 2.3672), (48.8642, 2.3653), (48.8668, 2.3630), (48.8686, 2.3585), (48.8698, 2.3528), (48.8706, 2.3470), (48.8712, 2.3410), (48.8712, 2.3345), (48.8705, 2.3270), (48.8698, 2.3240)],
         blurb="Louis XIV had the right-bank wall levelled from 1670 and planted with four rows of elms: a promenade for coaches, then the theatres, cafés and puppet shows of the boulevard du Temple."),
    dict(id="cours-la-reine", name="Champs-Élysées", periods=["louis-1789"], width=30, style="major",
         path=[(48.8656, 2.3218), (48.8665, 2.3192), (48.8676, 2.3168)],
         blurb="Le Nôtre's avenue (1667) continuing the Tuileries axis west across the Place Louis XV into the country."),
]

# ---------------------------------------------------------------- walls and gates
WALLS = [
    dict(id="mur-gallo-romain", name="Late Roman wall of the Cité", periods=["capetian-1000"], closed=True,
         path=[(48.8573, 2.3422), (48.8570, 2.3448), (48.8563, 2.3470), (48.8558, 2.3490), (48.8550, 2.3503), (48.8536, 2.3510), (48.8526, 2.3506), (48.8530, 2.3488), (48.8536, 2.3473), (48.8548, 2.3446), (48.8560, 2.3425)],
         blurb="Built about 300 CE of reused stone from the forum and the arena, it shrank Lutetia to the island. Repaired, it held the Vikings off in 885–86 and still girdled the Cité around 1000."),
    dict(id="enceinte-philippe-rd", name="Wall of Philippe Auguste (right bank)", periods=["philippe-1250"],
         path=[(48.8595, 2.3385), (48.8610, 2.3388), (48.8618, 2.3402), (48.8632, 2.3418), (48.8645, 2.3432), (48.8655, 2.3450), (48.8650, 2.3472), (48.8644, 2.3500), (48.8634, 2.3524), (48.8622, 2.3550), (48.8612, 2.3572), (48.8590, 2.3592), (48.8565, 2.3601), (48.8545, 2.3606), (48.8532, 2.3608)],
         blurb="Built 1190–1209 on the king's order before he left on crusade, paid for by the burghers: about 2.5 km on this bank, 2.5 to 3 m thick and 6 to 8 m high, a round tower every 70 m or so, gates on every road out."),
    dict(id="enceinte-philippe-rg", name="Wall of Philippe Auguste (left bank)", periods=WALLED,
         path=[(48.8574, 2.3373), (48.8560, 2.3378), (48.8538, 2.3382), (48.8520, 2.3392), (48.8500, 2.3400), (48.8486, 2.3411), (48.8465, 2.3437), (48.8455, 2.3455), (48.8452, 2.3480), (48.8455, 2.3495), (48.8464, 2.3512), (48.8478, 2.3528), (48.8492, 2.3540), (48.8503, 2.3550)],
         blurb="The left-bank half, built about 1200–1215 by the king himself, from the Tour de Nesle over the shoulder of the Montagne to the Tournelle. It enclosed the University and still stood, ditched anew, in the 16th century."),
    dict(id="enceinte-charles-v", name="Wall of Charles V", periods=["valois-1550"],
         path=[(48.8601, 2.3343), (48.8625, 2.3352), (48.8640, 2.3360), (48.8660, 2.3395), (48.8675, 2.3430), (48.8685, 2.3465), (48.8696, 2.3525), (48.8690, 2.3570), (48.8680, 2.3605), (48.8665, 2.3632), (48.8640, 2.3655), (48.8600, 2.3672), (48.8560, 2.3683), (48.8538, 2.3688), (48.8520, 2.3680), (48.8506, 2.3664)],
         blurb="Begun in 1356 by the provost Étienne Marcel and finished under Charles V about 1383: an earth rampart faced with stone behind a double ditch, enclosing the new right-bank suburbs and the Louvre, with the Bastille guarding the east."),
]

GATES = [
    dict(id="porte-st-honore-pa", name="Porte Saint-Honoré", position=(48.8618, 2.3402), periods=["philippe-1250"]),
    dict(id="porte-montmartre-pa", name="Porte Montmartre", position=(48.8655, 2.3450), periods=["philippe-1250"]),
    dict(id="porte-st-denis-pa", name="Porte Saint-Denis (aux Peintres)", position=(48.8642, 2.3502), periods=["philippe-1250"]),
    dict(id="porte-st-martin-pa", name="Porte Saint-Martin", position=(48.8636, 2.3522), periods=["philippe-1250"]),
    dict(id="porte-du-temple-pa", name="Porte Barbette", position=(48.8592, 2.3591), periods=["philippe-1250"]),
    dict(id="porte-baudoyer", name="Porte Baudoyer (Saint-Antoine)", position=(48.8548, 2.3605), periods=["philippe-1250"]),
    dict(id="porte-de-buci", name="Porte de Buci", position=(48.8535, 2.3384), periods=WALLED),
    dict(id="porte-st-michel", name="Porte Saint-Michel (d'Enfer)", position=(48.8486, 2.3411), periods=WALLED),
    dict(id="porte-st-jacques", name="Porte Saint-Jacques", position=(48.8465, 2.3437), periods=WALLED),
    dict(id="porte-bordelles", name="Porte Bordelles (Saint-Marcel)", position=(48.8455, 2.3494), periods=WALLED),
    dict(id="porte-st-victor", name="Porte Saint-Victor", position=(48.8478, 2.3528), periods=WALLED),
    dict(id="porte-st-honore-c5", name="Porte Saint-Honoré", position=(48.8636, 2.3357), periods=["valois-1550"]),
    dict(id="porte-montmartre-c5", name="Porte Montmartre", position=(48.8683, 2.3448), periods=["valois-1550"]),
    dict(id="porte-st-denis-c5", name="Porte Saint-Denis", position=(48.8697, 2.3527), periods=["valois-1550"]),
    dict(id="porte-st-martin-c5", name="Porte Saint-Martin", position=(48.8691, 2.3566), periods=["valois-1550"]),
    dict(id="porte-du-temple-c5", name="Porte du Temple", position=(48.8667, 2.3628), periods=["valois-1550"]),
    dict(id="porte-st-antoine", name="Porte Saint-Antoine", position=(48.8541, 2.3683), periods=["valois-1550"]),
]

BRIDGES = [
    dict(id="petit-pont-early", name="Petit Pont", path=[(48.8528, 2.3473), (48.8535, 2.3476)], build="timber", arches=3, periods=EARLY,
         blurb="The short bridge over the south arm, on the line of the cardo. Swept away by floods again and again and rebuilt in timber or stone; in 885 its tower was the last post to fall to the Vikings."),
    dict(id="petit-pont", name="Petit Pont", path=[(48.8528, 2.3473), (48.8535, 2.3476)], build="stone", arches=3, periods=LATER,
         blurb="Rebuilt in stone by Bishop Maurice de Sully in 1185 and many times after, lined with houses, guarded at its left-bank end by the Petit Châtelet, the provost's prison."),
    dict(id="grand-pont-roman", name="Grand Pont", path=[(48.8561, 2.3491), (48.8570, 2.3496)], build="timber", arches=5, periods=["lutetia-200"],
         blurb="The Roman bridge over the north arm, on the line of the cardo where the Pont Notre-Dame now stands."),
    dict(id="grand-pont", name="Grand Pont", path=[(48.8566, 2.3469), (48.8576, 2.3471)], build="timber", arches=5, periods=["capetian-1000"],
         blurb="Rebuilt in the 9th century a little downstream, on the line of the later Pont au Change, with water mills beneath it and a tower at its right-bank head (the future Grand Châtelet)."),
    dict(id="pont-au-change-b", name="Pont au Change", path=[(48.8566, 2.3469), (48.8576, 2.3471)], build="stone", arches=6, landmarkId="pont-au-change", periods=LATER,
         blurb="The bridge of the money-changers and goldsmiths."),
    dict(id="pont-notre-dame-b", name="Pont Notre-Dame", path=[(48.8561, 2.3491), (48.8570, 2.3496)], build="stone", arches=5, landmarkId="pont-notre-dame", periods=["valois-1550", "louis-1789"],
         blurb="The bridge of houses, rebuilt in stone 1500–1512."),
    dict(id="pont-saint-michel", name="Pont Saint-Michel", path=[(48.8539, 2.3443), (48.8547, 2.3447)], build="stone", arches=4, periods=["valois-1550", "louis-1789"],
         blurb="First built 1378–87, lined with houses, carried away by ice and floods several times and rebuilt in stone in 1616–24, still with houses on it in 1789."),
    dict(id="pont-neuf-b", name="Pont Neuf", path=[(48.8586, 2.3421), (48.8558, 2.3400)], build="stone", arches=12, landmarkId="pont-neuf", periods=["louis-1789"],
         blurb="The 'new bridge' of 1578–1607."),
    dict(id="pont-marie", name="Pont Marie", path=[(48.8541, 2.3578), (48.8532, 2.3574)], build="stone", arches=5, periods=["louis-1789"],
         blurb="Built 1614–35 by the developer Christophe Marie to open the new Île Saint-Louis; houses lined it until 1788."),
    dict(id="pont-de-la-tournelle", name="Pont de la Tournelle", path=[(48.8514, 2.3557), (48.8503, 2.3553)], build="stone", arches=5, periods=["louis-1789"],
         blurb="Stone bridge of 1656 from the Île Saint-Louis to the quai de la Tournelle."),
    dict(id="pont-rouge", name="Pont Rouge", path=[(48.8524, 2.3526), (48.8526, 2.3537)], build="timber", arches=3, periods=["louis-1789"],
         blurb="A wooden footbridge, painted red, between the Cité and the Île Saint-Louis."),
    dict(id="pont-au-double", name="Pont au Double", path=[(48.8522, 2.3492), (48.8517, 2.3491)], build="stone", arches=1, periods=["louis-1789"],
         blurb="Built 1634 for the Hôtel-Dieu; the toll was a double denier."),
    dict(id="pont-royal", name="Pont Royal", path=[(48.8612, 2.3293), (48.8596, 2.3287)], build="stone", arches=5, periods=["louis-1789"],
         blurb="Louis XIV's stone bridge of 1685–89 from the Tuileries to the faubourg Saint-Germain, replacing a wooden one."),
]

AQUEDUCTS = [
    dict(name="Aqueduct of Lutetia (from Wissous)", periods=["lutetia-200"], path=[(48.8366, 2.3380), (48.8400, 2.3395), (48.8440, 2.3410), (48.8475, 2.3425), (48.8500, 2.3437)]),
]

# ---------------------------------------------------------------- built-up blocks
BLOCKS = [
    # Lutetia
    dict(name="Island quarter", periods=["lutetia-200"], density="dense", polygon=[(48.8572, 2.3424), (48.8568, 2.3460), (48.8558, 2.3488), (48.8545, 2.3505), (48.8528, 2.3508), (48.8532, 2.3480), (48.8545, 2.3450), (48.8560, 2.3428)]),
    dict(name="Lutetia, west of the cardo", periods=["lutetia-200"], density="dense", polygon=[(48.8528, 2.3442), (48.8522, 2.3466), (48.8495, 2.3452), (48.8470, 2.3436), (48.8470, 2.3412), (48.8500, 2.3428)]),
    dict(name="Lutetia, east of the cardo", periods=["lutetia-200"], density="dense", polygon=[(48.8522, 2.3472), (48.8512, 2.3484), (48.8492, 2.3486), (48.8475, 2.3484), (48.8472, 2.3446), (48.8496, 2.3460)]),
    dict(name="Lutetia, south", periods=["lutetia-200"], density="loose", polygon=[(48.8468, 2.3405), (48.8468, 2.3485), (48.8445, 2.3490), (48.8430, 2.3430), (48.8440, 2.3400)]),
    dict(name="Lutetia, west slope", periods=["lutetia-200"], density="loose", polygon=[(48.8535, 2.3395), (48.8530, 2.3432), (48.8500, 2.3420), (48.8475, 2.3405), (48.8480, 2.3385), (48.8510, 2.3385)]),
    dict(name="Right-bank landing", periods=["lutetia-200"], density="loose", polygon=[(48.8572, 2.3500), (48.8590, 2.3505), (48.8585, 2.3540), (48.8565, 2.3540), (48.8562, 2.3515)]),
    dict(name="Saint-Marcel", periods=["lutetia-200", "capetian-1000"], density="loose", polygon=[(48.8400, 2.3505), (48.8415, 2.3535), (48.8395, 2.3560), (48.8380, 2.3530)]),
    # Capetian
    dict(name="The Cité", periods=["capetian-1000"], density="dense", polygon=[(48.8571, 2.3425), (48.8567, 2.3462), (48.8558, 2.3487), (48.8546, 2.3504), (48.8530, 2.3508), (48.8533, 2.3482), (48.8545, 2.3452), (48.8560, 2.3428)]),
    dict(name="Saint-Germain-l'Auxerrois", periods=["capetian-1000"], density="loose", polygon=[(48.8595, 2.3395), (48.8612, 2.3400), (48.8610, 2.3445), (48.8590, 2.3448)]),
    dict(name="Grève and Saint-Gervais", periods=["capetian-1000"], density="dense", polygon=[(48.8572, 2.3500), (48.8585, 2.3505), (48.8580, 2.3550), (48.8562, 2.3565), (48.8557, 2.3530)]),
    dict(name="Grand Pont bridgehead and Saint-Merry", periods=["capetian-1000"], density="dense", polygon=[(48.8583, 2.3465), (48.8605, 2.3470), (48.8610, 2.3500), (48.8590, 2.3500), (48.8580, 2.3480)]),
    dict(name="Champeaux", periods=["capetian-1000"], density="loose", polygon=[(48.8605, 2.3440), (48.8630, 2.3440), (48.8635, 2.3485), (48.8612, 2.3483)]),
    dict(name="Beaubourg", periods=["capetian-1000"], density="loose", polygon=[(48.8595, 2.3505), (48.8630, 2.3510), (48.8625, 2.3545), (48.8590, 2.3545)]),
    dict(name="Saint-Séverin and Saint-Julien", periods=["capetian-1000"], density="dense", polygon=[(48.8530, 2.3440), (48.8525, 2.3470), (48.8510, 2.3492), (48.8500, 2.3468), (48.8510, 2.3440)]),
    dict(name="Bourg Saint-Germain", periods=["capetian-1000"], density="loose", polygon=[(48.8558, 2.3320), (48.8555, 2.3370), (48.8530, 2.3372), (48.8525, 2.3325)]),
    dict(name="Bourg Sainte-Geneviève", periods=["capetian-1000"], density="loose", polygon=[(48.8495, 2.3470), (48.8490, 2.3505), (48.8470, 2.3500), (48.8475, 2.3462)]),
    # Inside the walls, Paris was packed: big polygons per walled area (the generator keeps streets, river, walls and landmarks clear)
    dict(name="The Cité", periods=["philippe-1250", "valois-1550"], density="dense", polygon=[(48.8576, 2.3418), (48.8576, 2.3432), (48.8572, 2.3448), (48.8566, 2.3470), (48.8560, 2.3490), (48.8553, 2.3505), (48.8543, 2.3515), (48.8531, 2.3521), (48.8521, 2.3524), (48.8518, 2.3519), (48.8523, 2.3504), (48.8528, 2.3487), (48.8534, 2.3474), (48.8540, 2.3460), (48.8547, 2.3446), (48.8556, 2.3429), (48.8564, 2.3415), (48.8571, 2.3413)]),
    dict(name="La Ville inside the wall", periods=["philippe-1250"], density="dense", polygon=[
        (48.8597, 2.3392), (48.8610, 2.3395), (48.8628, 2.3418), (48.8643, 2.3436), (48.8650, 2.3452), (48.8645, 2.3472), (48.8639, 2.3500), (48.8630, 2.3522),
        (48.8618, 2.3548), (48.8608, 2.3568), (48.8588, 2.3586), (48.8563, 2.3595), (48.8540, 2.3600), (48.8538, 2.3580), (48.8547, 2.3552), (48.8556, 2.3530),
        (48.8566, 2.3505), (48.8574, 2.3478), (48.8584, 2.3450), (48.8592, 2.3420)]),
    dict(name="The University inside the wall", periods=["philippe-1250", "valois-1550"], density="dense", polygon=[
        (48.8566, 2.3380), (48.8540, 2.3388), (48.8521, 2.3398), (48.8502, 2.3406), (48.8488, 2.3417), (48.8468, 2.3441), (48.8459, 2.3458), (48.8457, 2.3480),
        (48.8460, 2.3494), (48.8468, 2.3510), (48.8480, 2.3524), (48.8494, 2.3535), (48.8502, 2.3540), (48.8508, 2.3520), (48.8514, 2.3498), (48.8522, 2.3478),
        (48.8527, 2.3464), (48.8535, 2.3446), (48.8541, 2.3430), (48.8550, 2.3412), (48.8562, 2.3392)]),
    # faubourgs of 1250, strung along the roads out
    dict(name="Bourg Saint-Germain", periods=["philippe-1250"], density="dense", polygon=[(48.8556, 2.3318), (48.8556, 2.3368), (48.8528, 2.3374), (48.8522, 2.3322)]),
    dict(name="Faubourg Saint-Germain", periods=["philippe-1250"], density="loose", polygon=[(48.8522, 2.3322), (48.8528, 2.3374), (48.8520, 2.3392), (48.8500, 2.3360), (48.8505, 2.3310)]),
    dict(name="Faubourg Saint-Jacques", periods=["philippe-1250"], density="loose", polygon=[(48.8460, 2.3400), (48.8452, 2.3448), (48.8395, 2.3425), (48.8400, 2.3392)]),
    dict(name="Bourg Saint-Marcel", periods=["philippe-1250"], density="loose", polygon=[(48.8445, 2.3478), (48.8440, 2.3520), (48.8410, 2.3555), (48.8378, 2.3540), (48.8375, 2.3485), (48.8415, 2.3478)]),
    dict(name="Faubourg Saint-Honoré", periods=["philippe-1250"], density="loose", polygon=[(48.8615, 2.3340), (48.8650, 2.3310), (48.8670, 2.3250), (48.8682, 2.3260), (48.8660, 2.3330), (48.8632, 2.3405), (48.8612, 2.3390)]),
    dict(name="Faubourg Montmartre", periods=["philippe-1250"], density="loose", polygon=[(48.8655, 2.3432), (48.8720, 2.3420), (48.8722, 2.3445), (48.8658, 2.3462)]),
    dict(name="Faubourgs Saint-Denis and Saint-Martin", periods=["philippe-1250"], density="loose", polygon=[(48.8648, 2.3482), (48.8700, 2.3505), (48.8740, 2.3530), (48.8740, 2.3605), (48.8690, 2.3580), (48.8640, 2.3545), (48.8638, 2.3510)]),
    dict(name="Saint-Paul and the faubourg Saint-Antoine", periods=["philippe-1250"], density="loose", polygon=[(48.8560, 2.3612), (48.8558, 2.3700), (48.8548, 2.3800), (48.8530, 2.3800), (48.8535, 2.3690), (48.8532, 2.3615)]),
    # 1550: the right bank fills the wall of Charles V
    dict(name="La Ville inside the wall of Charles V", periods=["valois-1550"], density="dense", polygon=[
        (48.8605, 2.3350), (48.8625, 2.3358), (48.8638, 2.3366), (48.8656, 2.3398), (48.8670, 2.3432), (48.8679, 2.3465), (48.8689, 2.3522), (48.8684, 2.3566),
        (48.8674, 2.3600), (48.8660, 2.3626), (48.8637, 2.3647), (48.8600, 2.3664), (48.8580, 2.3668), (48.8580, 2.3638), (48.8546, 2.3638), (48.8538, 2.3605),
        (48.8545, 2.3552), (48.8553, 2.3530), (48.8563, 2.3510), (48.8570, 2.3490), (48.8575, 2.3470), (48.8582, 2.3450), (48.8590, 2.3420), (48.8596, 2.3380)]),
    dict(name="Hôtel Saint-Pol and the Célestins", periods=["valois-1550"], density="loose", polygon=[(48.8546, 2.3642), (48.8548, 2.3684), (48.8524, 2.3672), (48.8531, 2.3612)]),
    dict(name="Bourg Saint-Germain", periods=["valois-1550"], density="dense", polygon=[(48.8558, 2.3310), (48.8564, 2.3374), (48.8520, 2.3392), (48.8500, 2.3360), (48.8505, 2.3310)]),
    dict(name="Faubourg Saint-Germain", periods=["valois-1550"], density="loose", polygon=[(48.8505, 2.3220), (48.8556, 2.3215), (48.8558, 2.3306), (48.8505, 2.3306)]),
    dict(name="Faubourg Saint-Jacques", periods=["valois-1550"], density="loose", polygon=[(48.8462, 2.3398), (48.8452, 2.3450), (48.8385, 2.3425), (48.8392, 2.3388)]),
    dict(name="Faubourg Saint-Marcel", periods=["valois-1550"], density="dense", polygon=[(48.8448, 2.3475), (48.8442, 2.3525), (48.8410, 2.3560), (48.8375, 2.3545), (48.8372, 2.3482), (48.8415, 2.3475)]),
    dict(name="Saint-Victor and Saint-Bernard", periods=["valois-1550"], density="loose", polygon=[(48.8500, 2.3555), (48.8490, 2.3600), (48.8478, 2.3590), (48.8480, 2.3542)]),
    dict(name="Faubourg Saint-Honoré", periods=["valois-1550"], density="loose", polygon=[(48.8628, 2.3330), (48.8648, 2.3300), (48.8672, 2.3240), (48.8690, 2.3250), (48.8665, 2.3330), (48.8648, 2.3368)]),
    dict(name="Faubourgs Montmartre, Saint-Denis and Saint-Martin", periods=["valois-1550"], density="loose", polygon=[(48.8682, 2.3420), (48.8740, 2.3410), (48.8740, 2.3620), (48.8692, 2.3600), (48.8694, 2.3520), (48.8686, 2.3462)]),
    dict(name="Faubourg du Temple", periods=["valois-1550"], density="loose", polygon=[(48.8670, 2.3630), (48.8740, 2.3640), (48.8735, 2.3710), (48.8665, 2.3660)]),
    dict(name="Faubourg Saint-Antoine", periods=["valois-1550"], density="loose", polygon=[(48.8560, 2.3700), (48.8565, 2.3795), (48.8510, 2.3795), (48.8520, 2.3705)]),
    # 1789: built up to the edges of the frame, round the gardens
    dict(name="The Cité", periods=["louis-1789"], density="dense", polygon=[(48.8576, 2.3395), (48.8578, 2.3430), (48.8572, 2.3448), (48.8566, 2.3470), (48.8560, 2.3490), (48.8553, 2.3505), (48.8543, 2.3515), (48.8531, 2.3521), (48.8521, 2.3526), (48.8518, 2.3519), (48.8523, 2.3504), (48.8528, 2.3487), (48.8534, 2.3474), (48.8540, 2.3460), (48.8547, 2.3446), (48.8556, 2.3429), (48.8564, 2.3410), (48.8570, 2.3398)]),
    dict(name="Île Saint-Louis", periods=["louis-1789"], density="dense", polygon=[(48.8527, 2.3540), (48.8531, 2.3555), (48.8531, 2.3572), (48.8526, 2.3592), (48.8521, 2.3607), (48.8513, 2.3625), (48.8506, 2.3630), (48.8503, 2.3620), (48.8507, 2.3597), (48.8512, 2.3570), (48.8515, 2.3555), (48.8518, 2.3546)]),
    dict(name="Faubourg Saint-Honoré", periods=["louis-1789"], density="loose", polygon=[(48.8740, 2.3175), (48.8740, 2.3262), (48.8672, 2.3262), (48.8672, 2.3175)]),
    dict(name="Saint-Roch, the Place Vendôme and the Carrousel", periods=["louis-1789"], density="dense", polygon=[(48.8740, 2.3262), (48.8740, 2.3365), (48.8628, 2.3365), (48.8612, 2.3360), (48.8610, 2.3330), (48.8632, 2.3333), (48.8668, 2.3302), (48.8672, 2.3262)]),
    dict(name="Palais-Royal and the rue de Richelieu", periods=["louis-1789"], density="dense", polygon=[(48.8740, 2.3365), (48.8740, 2.3445), (48.8615, 2.3445), (48.8612, 2.3400), (48.8628, 2.3365), (48.8650, 2.3365), (48.8650, 2.3394), (48.8675, 2.3394), (48.8675, 2.3365)]),
    dict(name="Saint-Germain-l'Auxerrois", periods=["louis-1789"], density="dense", polygon=[(48.8612, 2.3390), (48.8615, 2.3460), (48.8600, 2.3480), (48.8586, 2.3470), (48.8590, 2.3420), (48.8594, 2.3392)]),
    dict(name="Les Halles, Saint-Denis and Saint-Martin", periods=["louis-1789"], density="dense", polygon=[(48.8740, 2.3445), (48.8740, 2.3600), (48.8600, 2.3570), (48.8580, 2.3532), (48.8571, 2.3500), (48.8580, 2.3472), (48.8615, 2.3445)]),
    dict(name="The Marais and the Grève", periods=["louis-1789"], density="dense", polygon=[(48.8740, 2.3600), (48.8705, 2.3620), (48.8668, 2.3640), (48.8610, 2.3675), (48.8545, 2.3690), (48.8534, 2.3660), (48.8538, 2.3600), (48.8545, 2.3555), (48.8556, 2.3530), (48.8571, 2.3505), (48.8600, 2.3570)]),
    dict(name="Faubourg du Temple and Popincourt", periods=["louis-1789"], density="loose", polygon=[(48.8740, 2.3622), (48.8740, 2.3792), (48.8562, 2.3792), (48.8550, 2.3702), (48.8610, 2.3684), (48.8668, 2.3650), (48.8705, 2.3630)]),
    dict(name="Faubourg Saint-Antoine", periods=["louis-1789"], density="dense", polygon=[(48.8556, 2.3702), (48.8558, 2.3795), (48.8502, 2.3795), (48.8512, 2.3702)]),
    dict(name="The Arsenal and the Rapée", periods=["louis-1789"], density="loose", polygon=[(48.8525, 2.3662), (48.8530, 2.3700), (48.8500, 2.3795), (48.8420, 2.3795), (48.8440, 2.3712), (48.8488, 2.3688)]),
    dict(name="Faubourg Saint-Germain", periods=["louis-1789"], density="loose", polygon=[(48.8605, 2.3175), (48.8608, 2.3300), (48.8592, 2.3330), (48.8530, 2.3325), (48.8510, 2.3175)]),
    dict(name="Saint-Germain, Saint-Sulpice and the Odéon", periods=["louis-1789"], density="dense", polygon=[(48.8592, 2.3330), (48.8578, 2.3375), (48.8562, 2.3394), (48.8520, 2.3402), (48.8496, 2.3404), (48.8496, 2.3345), (48.8530, 2.3325)]),
    dict(name="The Latin Quarter", periods=["louis-1789"], density="dense", polygon=[(48.8562, 2.3396), (48.8540, 2.3445), (48.8527, 2.3470), (48.8518, 2.3495), (48.8505, 2.3545), (48.8482, 2.3558), (48.8456, 2.3540), (48.8446, 2.3500), (48.8450, 2.3410), (48.8486, 2.3402), (48.8520, 2.3402)]),
    dict(name="Faubourg Saint-Marcel", periods=["louis-1789"], density="dense", polygon=[(48.8446, 2.3462), (48.8446, 2.3555), (48.8424, 2.3560), (48.8370, 2.3560), (48.8370, 2.3462)]),
    dict(name="Faubourg Saint-Jacques and the Val-de-Grâce", periods=["louis-1789"], density="dense", polygon=[(48.8450, 2.3406), (48.8446, 2.3460), (48.8370, 2.3460), (48.8370, 2.3392), (48.8433, 2.3398)]),
    dict(name="Vaugirard and the convents", periods=["louis-1789"], density="loose", polygon=[(48.8510, 2.3175), (48.8530, 2.3322), (48.8494, 2.3343), (48.8465, 2.3322), (48.8433, 2.3337), (48.8370, 2.3338), (48.8370, 2.3175)]),
    dict(name="Saint-Bernard and the Halle aux Vins", periods=["louis-1789"], density="loose", polygon=[(48.8496, 2.3555), (48.8488, 2.3612), (48.8464, 2.3638), (48.8462, 2.3566)]),
    dict(name="The Salpêtrière road", periods=["louis-1789"], density="loose", polygon=[(48.8420, 2.3585), (48.8426, 2.3648), (48.8370, 2.3720), (48.8370, 2.3570)]),
]

GARDENS = [
    dict(name="Vineyards of the hill", periods=["lutetia-200"], kind="vineyard", polygon=[(48.8440, 2.3500), (48.8445, 2.3560), (48.8420, 2.3570), (48.8410, 2.3510)]),
    dict(name="Fields west of Lutetia", periods=["lutetia-200"], kind="orchard", polygon=[(48.8555, 2.3300), (48.8560, 2.3370), (48.8520, 2.3380), (48.8500, 2.3320)]),
    dict(name="Clos de Laas", periods=["capetian-1000"], kind="vineyard", polygon=[(48.8550, 2.3375), (48.8545, 2.3425), (48.8520, 2.3430), (48.8520, 2.3380)]),
    dict(name="Clos Bruneau and Clos Mauvoisin", periods=["capetian-1000"], kind="vineyard", polygon=[(48.8495, 2.3420), (48.8495, 2.3460), (48.8470, 2.3455), (48.8470, 2.3420)]),
    dict(name="Pré-aux-Clercs", periods=["capetian-1000", "philippe-1250", "valois-1550"], kind="park", polygon=[(48.8590, 2.3220), (48.8590, 2.3300), (48.8565, 2.3305), (48.8560, 2.3225)]),
    dict(name="Abbey vineyards of Sainte-Geneviève", periods=["capetian-1000", "philippe-1250", "valois-1550"], kind="vineyard", polygon=[(48.8448, 2.3452), (48.8445, 2.3474), (48.8425, 2.3474), (48.8428, 2.3452)]),
    dict(name="Cultures of the Marais", periods=["philippe-1250"], kind="orchard", polygon=[(48.8620, 2.3580), (48.8670, 2.3570), (48.8680, 2.3660), (48.8620, 2.3680), (48.8600, 2.3630)]),
    dict(name="Abbey of Saint-Victor", periods=["capetian-1000", "philippe-1250", "valois-1550"], kind="orchard", polygon=[(48.8478, 2.3540), (48.8475, 2.3585), (48.8455, 2.3590), (48.8458, 2.3545)]),
    dict(name="Tuileries gardens", periods=["louis-1789"], kind="park", polygon=[(48.8655, 2.3235), (48.8665, 2.3290), (48.8632, 2.3310), (48.8610, 2.3302), (48.8618, 2.3250), (48.8642, 2.3228)]),
    dict(name="Place Louis XV", periods=["louis-1789"], kind="park", polygon=[(48.8665, 2.3200), (48.8668, 2.3228), (48.8648, 2.3233), (48.8645, 2.3205)]),
    dict(name="Luxembourg gardens", periods=["louis-1789"], kind="park", polygon=[(48.8492, 2.3345), (48.8485, 2.3395), (48.8440, 2.3400), (48.8435, 2.3340), (48.8465, 2.3325)]),
    dict(name="Jardin du Roi", periods=["louis-1789"], kind="park", polygon=[(48.8460, 2.3560), (48.8452, 2.3620), (48.8430, 2.3640), (48.8422, 2.3575)]),
    dict(name="Palais-Royal garden", periods=["louis-1789"], kind="park", polygon=[(48.8655, 2.3370), (48.8672, 2.3374), (48.8670, 2.3390), (48.8653, 2.3386)]),
    dict(name="Gardens of the Hôtel des Tournelles", periods=["valois-1550"], kind="park", polygon=[(48.8570, 2.3640), (48.8575, 2.3670), (48.8552, 2.3678), (48.8550, 2.3648)]),
]

DISTRICTS = [
    dict(id="la-cite", name="La Cité", periods=["capetian-1000", "philippe-1250", "valois-1550"], polygon=[(48.8577, 2.3415), (48.8574, 2.3448), (48.8562, 2.3490), (48.8544, 2.3517), (48.8521, 2.3527), (48.8521, 2.3504), (48.8538, 2.3460), (48.8563, 2.3413)],
         description="The island of king and bishop: the royal palace at the west end, Notre-Dame and the Hôtel-Dieu at the east, and between them a maze of lanes and well over a dozen small parish churches."),
    dict(id="la-ville", name="La Ville", periods=["philippe-1250", "valois-1550"], polygon=[(48.8595, 2.3385), (48.8655, 2.3450), (48.8634, 2.3524), (48.8590, 2.3592), (48.8532, 2.3608), (48.8570, 2.3490)],
         description="The right bank of the merchants: the ports of the Grève, the Halles, the butchers, the changers and the Hôtel de Ville of the provost of the merchants."),
    dict(id="universite", name="L'Université", periods=["philippe-1250", "valois-1550"], polygon=[(48.8574, 2.3373), (48.8500, 2.3400), (48.8452, 2.3480), (48.8503, 2.3550), (48.8525, 2.3480)],
         description="The left bank of masters and students, who spoke Latin, hence the Latin Quarter: colleges, convents of the friars, booksellers and parchment-makers inside the wall."),
    dict(id="faubourg-st-germain", name="Faubourg Saint-Germain", periods=["louis-1789"], polygon=[(48.8595, 2.3200), (48.8595, 2.3330), (48.8530, 2.3320), (48.8515, 2.3200)],
         description="The aristocracy's quarter since Louis XIV: grand hôtels between court and garden on the rue de Grenelle, rue de Varenne and rue de l'Université."),
    dict(id="faubourg-st-antoine", name="Faubourg Saint-Antoine", periods=["louis-1789"], polygon=[(48.8560, 2.3700), (48.8560, 2.3795), (48.8505, 2.3795), (48.8512, 2.3705)],
         description="The furniture-makers' faubourg outside the Bastille, free of guild rules under the abbey's protection; its workmen marched on the fortress in July 1789."),
]

LABELS = [
    dict(text="Lutetia", position=(48.8485, 2.3395), size="lg", periods=["lutetia-200"]),
    dict(text="Mons Lucotitius", position=(48.8448, 2.3480), size="sm", periods=["lutetia-200"]),
    dict(text="Montagne Sainte-Geneviève", position=(48.8440, 2.3470), size="sm", periods=["capetian-1000", "philippe-1250", "valois-1550", "louis-1789"]),
    dict(text="La Cité", position=(48.8548, 2.3462), size="md", rotation=-28, periods=["louis-1789"]),
    dict(text="Le Marais", position=(48.8610, 2.3620), size="md", periods=["capetian-1000", "philippe-1250", "valois-1550", "louis-1789"]),
    dict(text="Palus", position=(48.8640, 2.3620), size="sm", periods=["lutetia-200"]),
    dict(text="Pré-aux-Clercs", position=(48.8582, 2.3262), size="sm", periods=["capetian-1000", "philippe-1250", "valois-1550"]),
    dict(text="Île Notre-Dame", position=(48.8537, 2.3555), size="sm", rotation=-20, periods=MEDIEVAL),
    dict(text="Île aux Vaches", position=(48.8530, 2.3612), size="sm", rotation=-30, periods=MEDIEVAL),
    dict(text="Île Saint-Louis", position=(48.8535, 2.3590), size="sm", rotation=-25, periods=["louis-1789"]),
]
