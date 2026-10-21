# Venice: city, frame, eras and the geography of the lagoon city (see tools/content/cities/FORMAT.md).
# The lagoon is one wide WATER path of concentric loops round the islands (generated from LAND below,
# so it is a single stroke that stops at the shore); the Grand Canal and the larger rii are drawn on the land.

E, D, R, C, S = "early-900", "dandolo-1204", "republic-1400", "cinquecento-1580", "serenissima-1780"
ALL = [E, D, R, C, S]
MEDIEVAL = [E, D, R]
LATER = [D, R, C, S]
LATE = [R, C, S]
MODERN = [C, S]

CITY = dict(
    name="Venice", subtitle="The City in the Lagoon",
    description="Venice and its lagoon from the first doges at Rivoalto to the fall of the Republic in 1797: the islands round the Grand Canal, San Marco and the Rialto, the Arsenal to the east, Cannaregio and the Ghetto to the north-west, the Giudecca and San Giorgio across the water to the south. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId=R,
    world=dict(heightScale=1.0, walls=["#E9D9BE", "#E2C3A0", "#D9A98A", "#EADFCB", "#C98E6E"], roofs=["#B4634A", "#A65A42", "#C07A5A"], props="venetian"),
    camera=dict(target=(45.4362, 12.3375), distance=38),
)
FRAME = ((45.4525, 12.3070), (45.4200, 12.3650))

PALETTE = dict(parchment="#E7D5AC", ink="#6A4A33", water="#5E8A8C", hill="#7A7F5E", road="#8A6A4A")
COMPASS = (45.4492, 12.3610)
CARTOUCHE = (45.4212, 12.3085)

SOURCES = [
    dict(id="wiki-venice-history", title="History of the Republic of Venice", author="Wikipedia", url="https://en.wikipedia.org/wiki/History_of_the_Republic_of_Venice"),
    dict(id="wiki-venetian-lagoon", title="Venetian Lagoon", author="Wikipedia", url="https://en.wikipedia.org/wiki/Venetian_Lagoon"),
    dict(id="wiki-grand-canal", title="Grand Canal (Venice)", author="Wikipedia", url="https://en.wikipedia.org/wiki/Grand_Canal_(Venice)"),
    dict(id="wiki-giudecca", title="Giudecca", author="Wikipedia", url="https://en.wikipedia.org/wiki/Giudecca"),
    dict(id="wiki-giudecca-canal", title="Giudecca Canal", author="Wikipedia", url="https://en.wikipedia.org/wiki/Giudecca_Canal"),
    dict(id="wiki-sestieri", title="Sestieri of Venice", author="Wikipedia", url="https://en.wikipedia.org/wiki/Sestieri_of_Venice"),
    dict(id="wiki-cannaregio-canal", title="Cannaregio Canal", author="Wikipedia", url="https://en.wikipedia.org/wiki/Cannaregio_Canal"),
    dict(id="wiki-san-michele", title="Isola di San Michele", author="Wikipedia", url="https://en.wikipedia.org/wiki/Isola_di_San_Michele"),
    dict(id="wiki-ponte-dei-pugni", title="Ponte dei Pugni", author="Wikipedia", url="https://en.wikipedia.org/wiki/Ponte_dei_Pugni"),
    dict(id="wiki-bridge-of-sighs", title="Bridge of Sighs", author="Wikipedia", url="https://en.wikipedia.org/wiki/Bridge_of_Sighs"),
    dict(id="de-barbari", title="View of Venice (Venetie MD)", author="Jacopo de' Barbari", year=1500, url="https://en.wikipedia.org/wiki/View_of_Venice"),
    dict(id="lane", title="Venice: A Maritime Republic", author="Frederic C. Lane", year=1973),
    dict(id="howard", title="The Architectural History of Venice", author="Deborah Howard", year=2002, note="revised edition"),
    dict(id="dorigo", title="Venezia origini: fondamenti, ipotesi, metodi", author="Wladimiro Dorigo", year=1983),
    dict(id="crouzet-pavan", title="Venice Triumphant: The Horizons of a Myth", author="Elisabeth Crouzet-Pavan", year=2002),
    dict(id="schulz", title="The New Palaces of Medieval Venice", author="Juergen Schulz", year=2004),
    dict(id="madden", title="Venice: A New History", author="Thomas F. Madden", year=2012),
]

PERIODS = [
    dict(id=E, label="Rivoalto", year=900, startYear=811, endYear=1093,
         summary="In 810–811 the doges moved their seat from Malamocco to the islets of Rivoalto, safer from the Franks. Around 900 Venice is a scatter of muddy islets in the lagoon, each with its parish church, timber houses, boatyards, salt and fish. The doge lives in a fortified castle by the water; beside it his chapel holds the body of Saint Mark, stolen from Alexandria in 828.",
         population="perhaps 15,000–30,000 (very uncertain)",
         feel="Reeds hissing on the mudflats, the slap of oars, woodsmoke from timber houses, gulls over the fish baskets at the Rialto landing.",
         style="medieval",
         houses=dict(title="Timber houses on the islets", text="Houses of wood and wattle on piles and rubble footings, thatched or shingled, one or two storeys round a yard with a rain-cistern, a boat tied at the door. Only the churches and the doge's castle are of brick and stone."),
         outskirts=dict(title="Mudflats, salt pans and orchards", text="Barene (salt marsh) cut by creeks, fish ponds, salt pans, vineyards and kitchen gardens round the parish churches. Firewood, lime and stone all came by boat from the mainland.")),
    dict(id=D, label="The Crusaders' Venice", year=1204, startYear=1094, endYear=1299,
         summary="Enrico Dandolo's Venice: a sea power with quarters in Constantinople and the ports of the east. Doge Sebastiano Ziani (1172–78) has laid out the Piazza and rebuilt the palace; the new San Marco, consecrated in 1094, is being clad in marble and in loot from Constantinople after 1204. The Rialto is the market of the city, reached by a bridge of boats; the Arsenal builds the state's galleys.",
         population="perhaps 60,000–80,000",
         feel="Shipwrights' mallets, Greek and Arabic on the quays, pepper, wax and cotton swung ashore at the Rialto, the bells of some sixty parishes.",
         style="medieval",
         houses=dict(title="Byzantine-style merchants' houses", text="Merchants' houses of brick with a water-gate on the canal, a ground-floor warehouse behind an arcaded portico and a long hall above, stilted round arches trimmed in white Istrian stone. Ordinary houses are still largely of timber."),
         outskirts=dict(title="Islets still being made", text="Gardens, vineyards, boatyards and marsh at the edges of the islands. New land is made by driving piles, building a wall of planks and filling behind it with mud, rubble and rubbish.")),
    dict(id=R, label="The Lagoon Republic", year=1400, startYear=1300, endYear=1499,
         summary="One of Europe's largest and richest cities, ruled since 1297 by the closed patriciate of the Great Council. The Gothic lagoon wing of the Doge's Palace is finished; the friars' churches of the Frari and Santi Giovanni e Paolo are rising in brick. Convoys of state galleys sail from the enlarged Arsenal to Alexandria, Beirut and Flanders. Venice has come through the Black Death and the war of Chioggia.",
         population="about 85,000–110,000, recovering from the plague of 1348",
         feel="Boatmen's cries at blind corners, spices and hot pitch on the air, bells everywhere, Latin, German, Greek and Tuscan in the crowd at the Rialto.",
         style="medieval",
         houses=dict(title="Gothic houses and palazzi", text="Brick houses of three storeys, plastered and coloured, with pointed windows in white Istrian stone, a water-gate and a portego (hall) running through each floor, funnel chimneys and tiled roofs; rows of small terrace houses for artisans and sailors."),
         outskirts=dict(title="Gardens and squeri", text="Walled convent gardens and orchards, boatyards (squeri) with their slipways, rope-walks and timber stacks at the city's edges, above all in Castello, northern Cannaregio and on the Giudecca.")),
    dict(id=C, label="Renaissance Venice", year=1580, startYear=1500, endYear=1699,
         summary="After the shock of Agnadello (1509) and the Portuguese spice route, Venice builds in stone: Sansovino's Library and Loggetta on the Piazza, Palladio's San Giorgio and, after the plague of 1575–77, his Redentore. The Ghetto (1516) encloses the Jews; printers, glassmakers and silk weavers fill the city. The Rialto bridge is still of wood: its stone successor follows in 1588–91.",
         population="about 170,000 before the plague of 1575–77, which killed perhaps a quarter to a third",
         feel="Presses thumping, gold leaf and incense, courtesans' perfume, the Arsenal bell calling two thousand workers at dawn.",
         style="early-modern",
         houses=dict(title="Palazzi and terrace houses", text="Tall houses of brick and Istrian stone, up to five storeys in the crowded centre, with balconies and wooden roof terraces (altane); classical palazzi on the Grand Canal; long rows of identical rented houses built by the scuole and the state for workers and widows."),
         outskirts=dict(title="Orchards, convents and the Giudecca", text="Convent gardens, patrician pleasure gardens on the Giudecca, timber and boat yards on the Zattere, vegetable plots in the far corners of Cannaregio and Castello.")),
    dict(id=S, label="The Last Years of the Serenissima", year=1780, startYear=1700, endYear=1797,
         summary="A city of pleasure and slow decline: the Republic is neutral and shrinking, but Carnival lasts for months, the Piazza is the salon of Europe and theatres and casinos run all night. The Salute (1631–87) closes the view down the Grand Canal; the Rialto has been of stone since 1591. On 12 May 1797 the Great Council votes itself out of existence before Napoleon's army.",
         population="about 140,000",
         feel="Masked crowds in the Piazza, coffee and chocolate under the arcades, violins from the girls' choirs of the ospedali, black gondolas waiting in rows.",
         style="early-modern",
         houses=dict(title="Refaced houses and rented palazzi", text="Old Gothic houses refaced and plastered in ochre, pink and white, storeys added on top, balconies with iron railings; patrician palazzi let out by the floor. The poor live in damp ground-floor rooms that flood at acqua alta."),
         outskirts=dict(title="Gardens and boatyards", text="Kitchen gardens and vineyards in Castello and on the Giudecca, convents behind high walls, timber yards and squeri, the meadows and convent of Sant'Elena.")),
]

# --- LAND ---
# The islands as they were from about 1300 (outline used to generate the lagoon). Earlier shores are shown by marsh.
MAIN = [
    (45.4310, 12.3120), (45.4330, 12.3108), (45.4352, 12.3115), (45.4372, 12.3135), (45.4388, 12.3155), (45.4402, 12.3162),
    (45.4420, 12.3172), (45.4440, 12.3180), (45.4457, 12.3192), (45.4468, 12.3210), (45.4473, 12.3240), (45.4473, 12.3280),
    (45.4471, 12.3320), (45.4467, 12.3350), (45.4458, 12.3372), (45.4446, 12.3388), (45.4434, 12.3405), (45.4425, 12.3425),
    (45.4418, 12.3445), (45.4411, 12.3465), (45.4405, 12.3485), (45.4403, 12.3510), (45.4402, 12.3545), (45.4400, 12.3575),
    (45.4392, 12.3590), (45.4380, 12.3605), (45.4370, 12.3625), (45.4355, 12.3632), (45.4340, 12.3628), (45.4328, 12.3612),
    (45.4310, 12.3600), (45.4292, 12.3590), (45.4282, 12.3578), (45.4290, 12.3555), (45.4304, 12.3533), (45.4314, 12.3510),
    (45.4320, 12.3490), (45.4325, 12.3465), (45.4328, 12.3440), (45.4330, 12.3415), (45.43285, 12.3398), (45.4327, 12.3382),
    (45.4325, 12.3370), (45.4318, 12.3370), (45.4307, 12.3373), (45.4299, 12.3364), (45.4296, 12.3340), (45.4295, 12.3310),
    (45.4296, 12.3280), (45.4299, 12.3245), (45.4303, 12.3205), (45.4306, 12.3165), (45.4308, 12.3135),
]
GIUDECCA = [
    (45.4276, 12.3155), (45.4278, 12.3185), (45.4276, 12.3230), (45.4272, 12.3270), (45.4268, 12.3305), (45.4265, 12.3335),
    (45.4266, 12.3365), (45.4267, 12.3392), (45.4261, 12.3410), (45.4250, 12.3412), (45.4240, 12.3395), (45.4232, 12.3360),
    (45.4228, 12.3310), (45.4232, 12.3260), (45.4240, 12.3215), (45.4252, 12.3180), (45.4265, 12.3155),
]
SAN_GIORGIO = [(45.4302, 12.3418), (45.4304, 12.3440), (45.4300, 12.3462), (45.4290, 12.3472), (45.4280, 12.3465), (45.4278, 12.3440), (45.4285, 12.3418)]
SANT_ELENA = [(45.4280, 12.3592), (45.4284, 12.3615), (45.4275, 12.3645), (45.4258, 12.3648), (45.4255, 12.3620), (45.4265, 12.3597)]
SAN_MICHELE = [(45.4490, 12.3440), (45.4492, 12.3478), (45.4485, 12.3495), (45.4470, 12.3492), (45.4466, 12.3460), (45.4475, 12.3440)]
LAND = [MAIN, GIUDECCA, SAN_GIORGIO, SANT_ELENA, SAN_MICHELE]
# --- END LAND ---

LAGOON_BLURB = "A shallow tidal lagoon about 50 km long behind the sand bars of the Lido and Pellestrina, mostly under a metre deep at low tide. Its channels were the city's streets and walls: the Republic dredged them, marked them with stakes and diverted whole rivers to keep the lagoon from silting up."

# --- LAGOON (generated by lagoongen.py) ---
LAGOON_PATH = [(45.45005, 12.34612), (45.44991, 12.34366), (45.44975, 12.3432), (45.44952, 12.3429), (45.44929, 12.34273), (45.44897, 12.34267), (45.44745, 12.34267), (45.44724, 12.34272), (45.44698, 12.3429), (45.44675, 12.3432), (45.44585, 12.3452), (45.44573, 12.34551), (45.44567, 12.34582), (45.44568, 12.34628), (45.44609, 12.3495), (45.44623, 12.34996), (45.44648, 12.35031), (45.4467, 12.35046), (45.44691, 12.35053), (45.44853, 12.35083), (45.44886, 12.35073), (45.44905, 12.35058), (45.44929, 12.35021), (45.45008, 12.34827), (45.45014, 12.34781), (45.45005, 12.34612), (45.45005, 12.3429), (45.44656, 12.33798), (45.4476, 12.33537), (45.44804, 12.33199), (45.44824, 12.328), (45.44821, 12.32369), (45.44766, 12.32047), (45.44753, 12.32016), (45.44626, 12.31814), (45.44432, 12.31675), (45.44226, 12.31592), (45.43934, 12.31436), (45.4378, 12.31248), (45.43564, 12.31033), (45.43545, 12.31022), (45.43318, 12.30949), (45.43285, 12.30949), (45.43058, 12.31081), (45.43026, 12.31119), (45.43009, 12.31171), (45.42988, 12.31325), (45.42937, 12.32031), (45.42867, 12.32784), (45.42856, 12.33107), (45.42867, 12.33414), (45.429, 12.33675), (45.42909, 12.33706), (45.42926, 12.33737), (45.43015, 12.33837), (45.43047, 12.33859), (45.4308, 12.33862), (45.43166, 12.33839), (45.43178, 12.33844), (45.43206, 12.34151), (45.43187, 12.34382), (45.43157, 12.34628), (45.43114, 12.34843), (45.43055, 12.35042), (45.42961, 12.35256), (45.4282, 12.35481), (45.42732, 12.35734), (45.42723, 12.35807), (45.42625, 12.35842), (45.42587, 12.35872), (45.42569, 12.35903), (45.42464, 12.36148), (45.42457, 12.3621), (45.42488, 12.36502), (45.42499, 12.36548), (45.42517, 12.36579), (45.4255, 12.36606), (45.42582, 12.36613), (45.42766, 12.36581), (45.42788, 12.36572), (45.42813, 12.36548), (45.42836, 12.36502), (45.42928, 12.36195), (45.42933, 12.36133), (45.42921, 12.36056), (45.42928, 12.36048), (45.43058, 12.3612), (45.4322, 12.36227), (45.43339, 12.36381), (45.43361, 12.36401), (45.43382, 12.36411), (45.43556, 12.36453), (45.43729, 12.36377), (45.43761, 12.36351), (45.43869, 12.36142), (45.43995, 12.35979), (45.44077, 12.35826), (45.44091, 12.3578), (45.44114, 12.35457), (45.44124, 12.35104), (45.44141, 12.34889), (45.44196, 12.34704), (45.4433, 12.3432), (45.4441, 12.34142), (45.44656, 12.33798), (45.44659, 12.34351), (45.44561, 12.34566), (45.44561, 12.34827), (45.44118, 12.35457), (45.44118, 12.35841), (45.43739, 12.36379), (45.43696, 12.36394), (45.43685, 12.3641), (45.43653, 12.3641), (45.43642, 12.36425), (45.4362, 12.36425), (45.43577, 12.36456), (45.43199, 12.36456), (45.43188, 12.36471), (45.42874, 12.36471), (45.42809, 12.36563), (45.42788, 12.36579), (45.42766, 12.36579), (45.42755, 12.36594), (45.4269, 12.36594), (45.42679, 12.36609), (45.42593, 12.36609), (45.42582, 12.36625), (45.4255, 12.36625), (45.42496, 12.36548), (45.42485, 12.36517), (45.42485, 12.36471), (45.42474, 12.36456), (45.42474, 12.36364), (45.42463, 12.36348), (45.42463, 12.36271), (45.42452, 12.36256), (45.42452, 12.35595), (45.4308, 12.34704), (45.43101, 12.34643), (45.43101, 12.34597), (45.43112, 12.34582), (45.43112, 12.34535), (45.43123, 12.3452), (45.43123, 12.34474), (45.43134, 12.34459), (45.43134, 12.34182), (45.43112, 12.34151), (45.43104, 12.34121), (45.43089, 12.3409), (45.43058, 12.34058), (45.43026, 12.34047), (45.42842, 12.34047), (45.4282, 12.34054), (45.42793, 12.34075), (45.42766, 12.34121), (45.42693, 12.34351), (45.42687, 12.34382), (45.42708, 12.34674), (45.42714, 12.34704), (45.42728, 12.34735), (45.42755, 12.34767), (45.42863, 12.34843), (45.42907, 12.34853), (45.42928, 12.34847), (45.4295, 12.34833), (45.43058, 12.34724), (45.4308, 12.3469), (45.4309, 12.34658), (45.43132, 12.34428), (45.43133, 12.34382), (45.43112, 12.34151), (45.43112, 12.34121), (45.43069, 12.34059), (45.43047, 12.34044), (45.42831, 12.34044), (45.42761, 12.33952), (45.42763, 12.33906), (45.42744, 12.33353), (45.42854, 12.32308), (45.42874, 12.31847), (45.42849, 12.31509), (45.42831, 12.31463), (45.42809, 12.31437), (45.42788, 12.31423), (45.42766, 12.31417), (45.42647, 12.31417), (45.42615, 12.31427), (45.42582, 12.31458), (45.42442, 12.31727), (45.42315, 12.32093), (45.42229, 12.32569), (45.42186, 12.33107), (45.42229, 12.33629), (45.42318, 12.34013), (45.42433, 12.34213), (45.42452, 12.34235), (45.42485, 12.34251), (45.42506, 12.34253), (45.42625, 12.34231), (45.42647, 12.34222), (45.42669, 12.34204), (45.42691, 12.34167), (45.42761, 12.33952), (45.42766, 12.34044), (45.42744, 12.34075), (45.42744, 12.34182), (45.42679, 12.34382), (45.42679, 12.35396), (45.42452, 12.35718), (45.42452, 12.36486), (45.42539, 12.36609), (45.42561, 12.36609), (45.42571, 12.36625), (45.42842, 12.36625), (45.42892, 12.36702), (45.42925, 12.36655), (45.4295, 12.36603), (45.43036, 12.36318), (45.43154, 12.36394), (45.43253, 12.36526), (45.43307, 12.36574), (45.4335, 12.36595), (45.43523, 12.3664), (45.43566, 12.36642), (45.43599, 12.36635), (45.43772, 12.36556), (45.43826, 12.36518), (45.43865, 12.36471), (45.43968, 12.36271), (45.44096, 12.36103), (45.44187, 12.35933), (45.4421, 12.35872), (45.44225, 12.35795), (45.44246, 12.35488), (45.44257, 12.35119), (45.44272, 12.34935), (45.44318, 12.34781), (45.44447, 12.34413), (45.44516, 12.34259), (45.44572, 12.34177), (45.44582, 12.34182), (45.44456, 12.34459), (45.4444, 12.3452), (45.44433, 12.34597), (45.44437, 12.34658), (45.44482, 12.35012), (45.44495, 12.35058), (45.44513, 12.35104), (45.44561, 12.35176), (45.44605, 12.35213), (45.44648, 12.35234), (45.44821, 12.3527), (45.44886, 12.35269), (45.4494, 12.35246), (45.44994, 12.35199), (45.45037, 12.35132), (45.45125, 12.3492), (45.45137, 12.34873), (45.45146, 12.34812), (45.45146, 12.34751), (45.45123, 12.34336), (45.45109, 12.34274), (45.45092, 12.34228), (45.4507, 12.34186), (45.45045, 12.34151), (45.44994, 12.34106), (45.4494, 12.34082), (45.44908, 12.34078), (45.44745, 12.34077), (45.44702, 12.34085), (45.4467, 12.34098), (45.44626, 12.34129), (45.44583, 12.3418), (45.44579, 12.34167), (45.44758, 12.33921), (45.44867, 12.3366), (45.44892, 12.33568), (45.44933, 12.3326), (45.44957, 12.32815), (45.44957, 12.32385), (45.44951, 12.32323), (45.44899, 12.32016), (45.44888, 12.3197), (45.4487, 12.31924), (45.44734, 12.31698), (45.4468, 12.31638), (45.44486, 12.31501), (45.44269, 12.31412), (45.43999, 12.31267), (45.43858, 12.31094), (45.43653, 12.30888), (45.4361, 12.30854), (45.43566, 12.30834), (45.43328, 12.3076), (45.43274, 12.30759), (45.4322, 12.30778), (45.43004, 12.30908), (45.42965, 12.30941), (45.42928, 12.30989), (45.429, 12.31048), (45.42882, 12.3111), (45.42863, 12.31241), (45.42853, 12.31255), (45.4282, 12.31239), (45.42777, 12.31228), (45.42615, 12.31231), (45.42582, 12.31242), (45.42546, 12.31263), (45.42517, 12.31288), (45.42487, 12.31325), (45.42326, 12.31632), (45.42193, 12.32016), (45.42181, 12.32062), (45.42097, 12.32538), (45.42055, 12.33061), (45.42053, 12.33122), (45.42097, 12.3366), (45.42193, 12.34082), (45.42225, 12.34156), (45.42331, 12.34336), (45.42367, 12.34382), (45.42409, 12.34416), (45.42452, 12.34435), (45.42496, 12.34443), (45.4255, 12.34436), (45.42555, 12.34443), (45.42581, 12.34735), (45.42604, 12.34812), (45.42647, 12.34888), (45.4269, 12.34932), (45.42809, 12.35016), (45.42853, 12.35035), (45.42893, 12.35042), (45.42891, 12.35058), (45.42858, 12.35135), (45.42712, 12.35369), (45.42615, 12.35642), (45.42604, 12.35654), (45.42539, 12.35689), (45.42484, 12.35749), (45.42459, 12.35795), (45.42342, 12.36072), (45.42328, 12.36133), (45.42323, 12.3621), (45.42356, 12.36533), (45.42377, 12.36625), (45.42415, 12.36702), (45.42255, 12.36702), (45.42238, 12.3664), (45.42226, 12.36579), (45.42191, 12.36241), (45.42194, 12.36118), (45.42214, 12.36013), (45.42242, 12.35933), (45.42365, 12.35657), (45.42393, 12.35611), (45.42431, 12.35564), (45.42463, 12.35532), (45.42517, 12.35492), (45.42597, 12.35273), (45.42677, 12.35135), (45.42615, 12.35089), (45.42571, 12.35046), (45.42534, 12.34996), (45.425, 12.34935), (45.42476, 12.34873), (45.42455, 12.34797), (45.42444, 12.34735), (45.42435, 12.34628), (45.42377, 12.34601), (45.42333, 12.34574), (45.4229, 12.34536), (45.4225, 12.34489), (45.42112, 12.34259), (45.42084, 12.34197), (45.42064, 12.34136), (45.41967, 12.33706), (45.4192, 12.33137), (45.41922, 12.33045), (45.4197, 12.32477), (45.42052, 12.32016), (45.42074, 12.31932), (45.42214, 12.31528), (45.42359, 12.31248), (45.42396, 12.31186), (45.42431, 12.31144), (45.42466, 12.3111), (45.42506, 12.3108), (45.4255, 12.31058), (45.42625, 12.31039), (45.42755, 12.31038), (45.42788, 12.30944), (45.42819, 12.30879), (45.4286, 12.30818), (45.42907, 12.30768), (45.4295, 12.30734), (45.43177, 12.30599), (45.43231, 12.30577), (45.43296, 12.30568), (45.43372, 12.30578), (45.4361, 12.30654), (45.43664, 12.3068), (45.43722, 12.30726), (45.43934, 12.30938), (45.44064, 12.31097), (45.44313, 12.31233), (45.44534, 12.31325), (45.44734, 12.31464), (45.44778, 12.31501), (45.44811, 12.3154), (45.44843, 12.31586), (45.44962, 12.3178), (45.44999, 12.31862), (45.45029, 12.3197), (45.45088, 12.32339), (45.4509, 12.32815), (45.45067, 12.33276), (45.45016, 12.33644), (45.4499, 12.33737), (45.44934, 12.33875), (45.44934, 12.3389), (45.44983, 12.33902), (45.45026, 12.3392), (45.4507, 12.33948), (45.45113, 12.33987), (45.45148, 12.34028), (45.45178, 12.34075), (45.45209, 12.34136), (45.45231, 12.34197), (45.45247, 12.34259), (45.45258, 12.34336), (45.4528, 12.34751), (45.45276, 12.34858), (45.45256, 12.34966), (45.45236, 12.35027), (45.4516, 12.35211), (45.45111, 12.35304), (45.4507, 12.35356), (45.45026, 12.35397), (45.44972, 12.35432), (45.44918, 12.35453), (45.44864, 12.35462), (45.4481, 12.35459), (45.44637, 12.35424), (45.44583, 12.35404), (45.44529, 12.35371), (45.44475, 12.3532), (45.44432, 12.35262), (45.44399, 12.35202), (45.44389, 12.35196), (45.44388, 12.35186), (45.4438, 12.35488), (45.44358, 12.35811), (45.44345, 12.35898), (45.44323, 12.35976), (45.44291, 12.36052), (45.44189, 12.36241), (45.44071, 12.36394), (45.43988, 12.36558), (45.43957, 12.36609), (45.43912, 12.36664), (45.4387, 12.36702), (45.43195, 12.36702), (45.43101, 12.36587), (45.43064, 12.36702), (45.42111, 12.36702), (45.42093, 12.36594), (45.42057, 12.36241), (45.42061, 12.36102), (45.42081, 12.35979), (45.42119, 12.35857), (45.42247, 12.35565), (45.42281, 12.35503), (45.42323, 12.35445), (45.42366, 12.35396), (45.42418, 12.3535), (45.42477, 12.35181), (45.4242, 12.35098), (45.4237, 12.34996), (45.42336, 12.34889), (45.42312, 12.34772), (45.42225, 12.34703), (45.4216, 12.34629), (45.42119, 12.34566), (45.41987, 12.34336), (45.41962, 12.34274), (45.41938, 12.34197), (45.41857, 12.33848), (45.41857, 12.32336), (45.41926, 12.31955), (45.41955, 12.31847), (45.42099, 12.31432), (45.42279, 12.31086), (45.42316, 12.31033), (45.42356, 12.30987), (45.42398, 12.30946), (45.42452, 12.30907), (45.42506, 12.30879), (45.42561, 12.3086), (45.42615, 12.3085), (45.42669, 12.30848), (45.42736, 12.30726), (45.42809, 12.30633), (45.42885, 12.30568), (45.43005, 12.30495), (45.43697, 12.30495), (45.4375, 12.30529), (45.43804, 12.30576), (45.44021, 12.30793), (45.4414, 12.30936), (45.44356, 12.31053), (45.44583, 12.31148), (45.44832, 12.31325), (45.44886, 12.31381), (45.44929, 12.31438), (45.45059, 12.3165), (45.45097, 12.31724), (45.45132, 12.31816), (45.45156, 12.31914), (45.45214, 12.32262), (45.45224, 12.32385), (45.45223, 12.3283), (45.45201, 12.33276), (45.45153, 12.33644), (45.45127, 12.33767), (45.45135, 12.33783), (45.45189, 12.33831), (45.45243, 12.33895), (45.45286, 12.33962), (45.45319, 12.34028), (45.45348, 12.34105), (45.45373, 12.34197), (45.45388, 12.3429), (45.45394, 12.34379), (45.45394, 12.34976), (45.45378, 12.35042), (45.45352, 12.35119), (45.4527, 12.35319), (45.4524, 12.3538), (45.452, 12.35446), (45.45156, 12.355), (45.45113, 12.35544), (45.45059, 12.35586), (45.45005, 12.35616), (45.44951, 12.35637), (45.44897, 12.35648), (45.44843, 12.35651), (45.44789, 12.35646), (45.44615, 12.35611), (45.44518, 12.35572), (45.44508, 12.3558), (45.44484, 12.35887), (45.44463, 12.35995), (45.44433, 12.36087), (45.44399, 12.36163), (45.44302, 12.36345), (45.44259, 12.3641), (45.44172, 12.3652), (45.44078, 12.36702), (45.44244, 12.36702), (45.44269, 12.36651), (45.44351, 12.36548), (45.44399, 12.36475), (45.44507, 12.36274), (45.44537, 12.3621), (45.44571, 12.36118), (45.44597, 12.36026), (45.44616, 12.35918), (45.44626, 12.3581), (45.44637, 12.35807), (45.44799, 12.35838), (45.44875, 12.3584), (45.44972, 12.35824), (45.4507, 12.35785), (45.45167, 12.35719), (45.45254, 12.35632), (45.45333, 12.35519), (45.45394, 12.35393), (45.45394, 12.33851), (45.45351, 12.33781), (45.45283, 12.33691), (45.45335, 12.33276), (45.45357, 12.3283), (45.45356, 12.32354), (45.45344, 12.32216), (45.45285, 12.31862), (45.45254, 12.3174), (45.45214, 12.31632), (45.45167, 12.31539), (45.45027, 12.31309), (45.44969, 12.31233), (45.44908, 12.31169), (45.44853, 12.31125), (45.44637, 12.30975), (45.44583, 12.30948), (45.44399, 12.30874), (45.44204, 12.30767), (45.44107, 12.30649), (45.43955, 12.30495), (45.42716, 12.30495), (45.42655, 12.30572), (45.42604, 12.30655), (45.42593, 12.30663), (45.42485, 12.3069), (45.42387, 12.30741), (45.42293, 12.30818), (45.42214, 12.3091), (45.42155, 12.31002), (45.41989, 12.31325), (45.41959, 12.31402), (45.41857, 12.31697), (45.41857, 12.34397), (45.41909, 12.34505), (45.42046, 12.34735), (45.42117, 12.34826), (45.42198, 12.34904), (45.42222, 12.34996), (45.42247, 12.3507), (45.42279, 12.35147), (45.42313, 12.35211), (45.4221, 12.35334), (45.42139, 12.35454), (45.42003, 12.35764), (45.41976, 12.35841), (45.41955, 12.35919), (45.41929, 12.36072), (45.41923, 12.36225), (45.4193, 12.36333), (45.41972, 12.36702), (45.41976, 12.35918), (45.41857, 12.35753), (45.41892, 12.35657), (45.42013, 12.3538), (45.42069, 12.35273), (45.42131, 12.35181), (45.42131, 12.35165), (45.42086, 12.35027), (45.4202, 12.34958), (45.41966, 12.34889), (45.41857, 12.34713), (45.41857, 12.31269), (45.41901, 12.31171), (45.42052, 12.30882), (45.42101, 12.30802), (45.4215, 12.30736), (45.42225, 12.30654), (45.42305, 12.30587), (45.42387, 12.30536), (45.42485, 12.30495), (45.44185, 12.30495), (45.44277, 12.30603), (45.44442, 12.30694), (45.44626, 12.30768), (45.44692, 12.30802), (45.44929, 12.30968), (45.45016, 12.31044), (45.4507, 12.31105), (45.45118, 12.31171), (45.45278, 12.31432), (45.45343, 12.31571), (45.45394, 12.31728), (45.45394, 12.35705), (45.45329, 12.35789), (45.45264, 12.35857), (45.45188, 12.35918), (45.45102, 12.35969), (45.45016, 12.36005), (45.44929, 12.36025), (45.44853, 12.3603), (45.44745, 12.3602), (45.44737, 12.36026), (45.44693, 12.36195), (45.44641, 12.36333), (45.44512, 12.36579), (45.4443, 12.36702), (45.44614, 12.36702), (45.4475, 12.3644), (45.44789, 12.36348), (45.44832, 12.36221), (45.44983, 12.36206), (45.45059, 12.36185), (45.45135, 12.36154), (45.452, 12.36119), (45.45269, 12.36072), (45.45329, 12.36022), (45.45394, 12.35958), (45.45394, 12.31336), (45.452, 12.31018), (45.45126, 12.30925), (45.45048, 12.30847), (45.44972, 12.30786), (45.44745, 12.30629), (45.4467, 12.30589), (45.44486, 12.30515), (45.4445, 12.30495), (45.42152, 12.30495), (45.42074, 12.30579), (45.41999, 12.3068), (45.41944, 12.30771), (45.41857, 12.30937), (45.41857, 12.35003), (45.41909, 12.35073), (45.41962, 12.35135), (45.41967, 12.3515), (45.41912, 12.35254), (45.41857, 12.35376), (45.41857, 12.35473), (45.41879, 12.35503), (45.41879, 12.35611), (45.4189, 12.35626), (45.4189, 12.35688), (45.42539, 12.36609), (45.42561, 12.36609), (45.42571, 12.36625), (45.42766, 12.36625), (45.42777, 12.3664), (45.44734, 12.3664), (45.44782, 12.36702), (45.4486, 12.36548), (45.44918, 12.36407), (45.45048, 12.36382), (45.45167, 12.36338), (45.45286, 12.36271), (45.45394, 12.36188), (45.45394, 12.31042), (45.45279, 12.30864), (45.45167, 12.30732), (45.45059, 12.30636), (45.4486, 12.30495), (45.4194, 12.30495), (45.41857, 12.30621), (45.43155, 12.30618), (45.4322, 12.30526), (45.45135, 12.30526), (45.45154, 12.30495), (45.45282, 12.30618), (45.45394, 12.30759), (45.45394, 12.36406), (45.45308, 12.36465), (45.4521, 12.36517), (45.45113, 12.36556), (45.45005, 12.36584), (45.44948, 12.36702), (45.45243, 12.36702), (45.45394, 12.36618), (45.45394, 12.30503), (45.45388, 12.30495)]
# --- END LAGOON ---

GC = [(45.4394, 12.3160), (45.4400, 12.3188), (45.4407, 12.3212), (45.4412, 12.3232), (45.4420, 12.3252), (45.4425, 12.3268), (45.4422, 12.3290),
      (45.4416, 12.3310), (45.4412, 12.3325), (45.4407, 12.3334), (45.4398, 12.3346), (45.4388, 12.3357), (45.4380, 12.3360), (45.4372, 12.3357),
      (45.4363, 12.3346), (45.4356, 12.3330), (45.4351, 12.3307), (45.4347, 12.3286), (45.4340, 12.3276), (45.4330, 12.3274), (45.4321, 12.3281),
      (45.4316, 12.3298), (45.4315, 12.3320), (45.4317, 12.3342), (45.4318, 12.3362), (45.4316, 12.3378)]

WATER = [
    dict(id="grand-canal", name="Canal Grande", path=GC, width=48,
         blurb="An old river channel winding through the islands in a reversed S, about 3.8 km long, 30–70 m wide and some 5 m deep. It was the city's main street: every great family built its palazzo with a water-gate on it, and until 1854 the Rialto was its only bridge."),
    dict(id="cannaregio-canal", name="Canale di Cannaregio", width=30,
         path=[(45.4424, 12.3266), (45.4432, 12.3260), (45.4442, 12.3250), (45.4452, 12.3235), (45.4462, 12.3218), (45.4474, 12.3200)],
         blurb="The second canal of the city and the old way in from the mainland: boats from Mestre and the rivers of the Veneto came this way before the railway bridge of 1846."),
    dict(id="rio-misericordia", name="Rio della Misericordia", width=12, periods=LATE,
         path=[(45.4455, 12.3240), (45.4454, 12.3275), (45.4452, 12.3310), (45.4452, 12.3340), (45.4455, 12.3368), (45.4460, 12.3380)],
         blurb="One of the three parallel canals of northern Cannaregio, dug as the marsh here was reclaimed in the 13th and 14th centuries, with the Scuola Grande della Misericordia on its bank."),
    dict(id="rio-sensa", name="Rio della Sensa", width=11, periods=LATE,
         path=[(45.4460, 12.3232), (45.4461, 12.3270), (45.4462, 12.3310), (45.4463, 12.3345)],
         blurb="The northernmost of the Cannaregio canals, lined with modest houses, gardens and the church of Madonna dell'Orto, where Tintoretto lived and is buried."),
    dict(id="rio-san-trovaso", name="Rio di San Trovaso", width=12,
         path=[(45.4323, 12.3278), (45.4314, 12.3270), (45.4304, 12.3265), (45.4293, 12.3262)],
         blurb="A canal from the Grand Canal down to the Zattere, with one of the last working squeri, the boatyard of San Trovaso, on its bank."),
    dict(id="rio-san-barnaba", name="Rio di San Barnaba", width=11,
         path=[(45.4336, 12.3270), (45.4335, 12.3250), (45.4331, 12.3228), (45.4320, 12.3216), (45.4304, 12.3212)],
         blurb="A canal through Dorsoduro from the Grand Canal toward the Zattere, crossed by the Ponte dei Pugni where the factions fought for the bridge."),
    dict(id="rio-palazzo", name="Rio di Palazzo", width=8,
         path=[(45.4327, 12.3412), (45.4342, 12.3412), (45.4351, 12.3413), (45.4359, 12.3410), (45.4367, 12.3400)],
         blurb="The narrow canal behind the Doge's Palace, between the palace and its prisons, running north past the canons' houses of San Marco."),
    dict(id="rio-mendicanti", name="Rio dei Mendicanti", width=12,
         path=[(45.4383, 12.34045), (45.4398, 12.34045), (45.4413, 12.3407), (45.4427, 12.3411)],
         blurb="The canal from the campo of Santi Giovanni e Paolo north to the lagoon, along the flank of the Scuola Grande di San Marco and the hospital of the Mendicanti."),
    dict(id="rio-arsenale", name="Rio dell'Arsenale", width=16, periods=LATER,
         path=[(45.4318, 12.3497), (45.4330, 12.3497), (45.4341, 12.3497)],
         blurb="The canal from the basin of San Marco to the water gate of the Arsenal, between two towers; every galley built inside came out this way."),
    dict(id="canale-san-pietro", name="Canale di San Pietro", width=34,
         path=[(45.4398, 12.3592), (45.4384, 12.3580), (45.4368, 12.3577), (45.4350, 12.3576), (45.4336, 12.3585), (45.4328, 12.3605)],
         blurb="The channel round the island of San Pietro di Castello, the ancient Olivolo, seat of the bishops of Venice from the 8th century and of the patriarch until 1807."),
    dict(id="rio-batario", name="Rio Batario", width=12, periods=[E],
         path=[(45.4352, 12.3380), (45.4342, 12.3381), (45.4331, 12.3382)],
         blurb="A canal that crossed the later Piazza in front of the church of San Geminiano. Doge Sebastiano Ziani had it filled in about 1172–78 to make the Piazza the size it is now."),
    dict(id="darsena-castello", name="Harbour of the doge's castle", width=26, periods=[E],
         path=[(45.4327, 12.33955), (45.4340, 12.33955)],
         blurb="Where the Piazzetta is now, a small harbour came up to the walls of the doge's castle; the reconstruction is uncertain, based on excavations and old descriptions."),
]
# filler channels too narrow for the lagoon's loops
WATER += [
    dict(id="rio-sant-elena", name="Rio di Sant'Elena", width=70,
         path=[(45.4300, 12.3614), (45.4287, 12.3595), (45.4276, 12.3584), (45.4266, 12.3580)],
         blurb="The channel between Castello and the island of Sant'Elena, with its convent of Olivetan monks and their meadows."),
    dict(id="giudecca-canal", name="Canale della Giudecca", width=220,
         path=[(45.4292, 12.3110), (45.4291, 12.3160), (45.4290, 12.3205), (45.4287, 12.3260), (45.4283, 12.3310), (45.4282, 12.3355), (45.4286, 12.3380), (45.4293, 12.3398)],
         blurb="The deep channel, 300–400 m wide, between the Zattere and the Giudecca, the way in for ships coming from the port of Malamocco. Timber rafts (zattere) once moored along the quay that took their name."),
]
WATER += [dict(id="lagoon", name="Laguna Veneta", path=LAGOON_PATH, width=200, blurb=LAGOON_BLURB)]

ISLANDS = []
HILLS = []
WALLS = []
GATES = []
AQUEDUCTS = []

# ---------------------------------------------------------------- streets: calli, salizade and fondamente
MERCERIE = [(45.4347, 12.3392), (45.4352, 12.3392), (45.4359, 12.3386), (45.4365, 12.3378), (45.4372, 12.3373), (45.4378, 12.3370), (45.4381, 12.33655)]
ROADS = [
    dict(id="path-rialto-san-marco", name="Path from Rivoalto to San Marco", path=MERCERIE, width=5, style="minor", periods=[E]),
    dict(id="mercerie", name="Mercerie", path=MERCERIE, width=7, style="major", labelled=True, periods=LATER,
         blurb="The chain of shopping streets from the clock tower to the Rialto, the city's high street: silk, spices, glass, books and jewels sold from ground-floor shops under the signs of their makers."),
    dict(id="ruga-rialto", name="Ruga degli Orefici and Ruga Vecchia", width=6, style="major", labelled=True, periods=LATER,
         path=[(45.4380, 12.3352), (45.4385, 12.3347), (45.4384, 12.3335), (45.4380, 12.3318), (45.4376, 12.3304), (45.4368, 12.3290), (45.4362, 12.3277)],
         blurb="From the foot of the Rialto bridge past the goldsmiths' arcades to Campo San Polo and on toward the Frari: the main walk of the San Polo side."),
    dict(id="path-san-polo", name="Path through Rivoalto", width=5, style="minor", periods=[E],
         path=[(45.4380, 12.3352), (45.4385, 12.3347), (45.4384, 12.3335), (45.4380, 12.3318)]),
    dict(id="riva-schiavoni", name="Riva degli Schiavoni", width=12, style="major", labelled=True, periods=LATE,
         path=[(45.43312, 12.3414), (45.43292, 12.3440), (45.43262, 12.3465), (45.43215, 12.3490), (45.4316, 12.3505)],
         blurb="The quay along the basin of San Marco, named after the Dalmatian (Slav) sailors and merchants who moored here. Ships unloaded at the Riva into the 18th century; it was paved in stone and widened in 1780–82."),
    dict(id="salizada-san-lio", name="Salizada San Lio and Ruga Giuffa", width=6, style="minor", periods=LATER,
         path=[(45.43815, 12.3369), (45.4381, 12.3385), (45.4379, 12.3399), (45.4376, 12.3410), (45.4366, 12.3420), (45.4352, 12.3426), (45.4341, 12.3430), (45.4333, 12.3431)]),
    dict(id="calle-san-moise", name="Calle Larga San Moisè and Santo Stefano", width=6, style="minor", periods=LATE,
         path=[(45.4342, 12.33725), (45.4340, 12.3360), (45.4337, 12.3346), (45.4339, 12.3330), (45.4341, 12.3315), (45.4339, 12.3302)]),
    dict(id="calle-castello", name="Calle to the Arsenal", width=6, style="minor", periods=LATER,
         path=[(45.4334, 12.3440), (45.4337, 12.3460), (45.4339, 12.3478), (45.4340, 12.3490)]),
    dict(id="calli-cannaregio", name="Calli of Santi Apostoli, Santa Fosca and San Marcuola", width=6, style="minor", periods=LATE,
         path=[(45.4396, 12.3372), (45.4410, 12.3366), (45.4418, 12.3345), (45.4424, 12.3318), (45.4430, 12.3293), (45.4432, 12.3275)]),
    dict(id="lista-di-spagna", name="Calli of San Geremia", width=6, style="minor", periods=LATE,
         path=[(45.4429, 12.3258), (45.4422, 12.3236), (45.4414, 12.3214), (45.4410, 12.3195)]),
    dict(id="calli-santa-croce", name="Calli of San Giacomo dall'Orio", width=6, style="minor", periods=LATER,
         path=[(45.4378, 12.3303), (45.4386, 12.3285), (45.4394, 12.3268), (45.4398, 12.3245), (45.4402, 12.3226)]),
    dict(id="zattere", name="Fondamenta delle Zattere", width=10, style="major", labelled=True, periods=MODERN,
         path=[(45.42992, 12.3362), (45.42976, 12.3340), (45.42966, 12.3310), (45.42976, 12.3280), (45.4301, 12.3245), (45.4305, 12.3205), (45.4308, 12.3165)],
         blurb="The long quay facing the Giudecca, paved in 1519, where timber rafts floated down from the Alps were moored and broken up; salt warehouses and boatyards lined it."),
    dict(id="fondamente-nove", name="Fondamente Nove", width=10, style="major", labelled=True, periods=[S],
         path=[(45.4445, 12.33885), (45.4433, 12.3406), (45.4424, 12.3426), (45.4417, 12.3446), (45.4410, 12.3466)],
         blurb="The 'new quays' built from 1589 along the northern edge of the city, looking out over the lagoon to San Michele and Murano."),
    dict(id="fondamenta-giudecca", name="Fondamenta of the Giudecca", width=8, style="minor", periods=MODERN,
         path=[(45.4275, 12.3190), (45.4271, 12.3255), (45.4267, 12.3295), (45.42635, 12.3335), (45.42645, 12.3375)]),
]

# ---------------------------------------------------------------- bridges
BRIDGES = [
    dict(id="rialto-pontoon", name="Ponte della Moneta (bridge of boats)", path=[(45.43803, 12.33563), (45.43797, 12.33631)], build="timber", arches=1, landmarkId="rialto-bridge", periods=[D],
         blurb="A bridge of boats laid across the Grand Canal about 1181, traditionally credited to Nicolò Barattieri; the tolls went to the mint, hence its name."),
    dict(id="rialto-wood", name="Ponte di Rialto (timber)", path=[(45.43803, 12.33563), (45.43797, 12.33631)], build="timber", arches=3, landmarkId="rialto-bridge", periods=[R, C],
         blurb="The timber bridge with shops and a central drawbridge that could be raised for masted ships. It collapsed under a crowd in 1444 and was rebuilt the same way."),
    dict(id="rialto-stone", name="Ponte di Rialto", path=[(45.43803, 12.33563), (45.43797, 12.33631)], build="stone", arches=1, landmarkId="rialto-bridge", periods=[S],
         blurb="Antonio da Ponte's single stone arch of 1588–91, 28 m wide, carrying three streets and two rows of shops."),
    dict(id="ponte-paglia", name="Ponte della Paglia", path=[(45.43308, 12.34095), (45.43308, 12.34145)], build="stone", arches=1, periods=LATE,
         blurb="The bridge on the Riva over the Rio di Palazzo, named, it is said, after the barges of straw that moored here; rebuilt in stone in 1360."),
    dict(id="ponte-sospiri", name="Ponte dei Sospiri", path=[(45.43405, 12.34103), (45.43405, 12.34137)], build="stone", arches=1, periods=[S],
         blurb="The covered bridge of 1600–03 between the palace and the New Prisons. The 'sighs' are a Romantic invention of the 19th century."),
    dict(id="ponte-guglie", name="Ponte delle Guglie", path=[(45.44281, 12.32601), (45.44295, 12.32643)], build="stone", arches=1, periods=MODERN,
         blurb="The bridge over the Cannaregio canal near its mouth on the Grand Canal: of timber from 1285, rebuilt in stone in 1580 and named after the obelisks at its corners."),
    dict(id="ponte-guglie-wood", name="Ponte di San Geremia", path=[(45.44281, 12.32601), (45.44295, 12.32643)], build="timber", arches=1, periods=[R]),
    dict(id="ponte-tre-archi", name="Ponte dei Tre Archi", path=[(45.44556, 12.32249), (45.44584, 12.32281)], build="stone", arches=3, periods=[S],
         blurb="The only three-arched bridge in Venice, built over the Cannaregio canal in 1688 by Andrea Tirali."),
    dict(id="ponte-pugni", name="Ponte dei Pugni", path=[(45.43355, 12.32465), (45.43335, 12.32475)], build="stone", arches=1, periods=MODERN,
         blurb="The 'bridge of the fists': without parapets, it was a battleground where Castellani and Nicolotti fought to push each other into the canal, until the fights were banned in 1705. Marble footprints mark the starting places."),
    dict(id="ponte-san-pietro", name="Ponte di San Pietro", path=[(45.4357, 12.35725), (45.4357, 12.3580)], build="timber", arches=1, periods=ALL),
]

# ---------------------------------------------------------------- built-up areas
G = GC
CANNAREGIO = G[0:11] + [(45.4405, 12.3365), (45.4425, 12.3395), (45.4440, 12.3392), (45.4455, 12.3378), (45.4466, 12.3350), (45.4470, 12.3300),
                        (45.4471, 12.3240), (45.4466, 12.3212), (45.4455, 12.3194), (45.4438, 12.3182), (45.4418, 12.3172), (45.4402, 12.3164)]
CANNAREGIO_S = G[0:11] + [(45.4405, 12.3365), (45.4425, 12.3395), (45.4440, 12.3392), (45.4446, 12.3370), (45.4448, 12.3300), (45.4448, 12.3250),
                          (45.4455, 12.3194), (45.4438, 12.3182), (45.4418, 12.3172), (45.4402, 12.3164)]
CANNAREGIO_N = [(45.4448, 12.3250), (45.4448, 12.3300), (45.4446, 12.3370), (45.4440, 12.3392), (45.4455, 12.3378), (45.4466, 12.3350),
                (45.4470, 12.3300), (45.4471, 12.3240), (45.4466, 12.3212), (45.4455, 12.3194)]
SAN_MARCO = G[10:26] + [(45.4328, 12.3382), (45.4330, 12.3410), (45.4345, 12.34125), (45.4359, 12.3408), (45.4372, 12.3402), (45.4390, 12.3385), (45.4405, 12.3365)]
CASTELLO_W = [(45.4330, 12.3415), (45.4345, 12.34125), (45.4359, 12.3408), (45.4372, 12.3402), (45.4390, 12.3385), (45.4405, 12.3365), (45.4425, 12.3395),
              (45.4437, 12.3403), (45.4428, 12.3420), (45.4419, 12.3443), (45.4412, 12.3463), (45.4406, 12.3484), (45.4403, 12.3496),
              (45.4340, 12.3494), (45.4321, 12.3490), (45.4326, 12.3465), (45.4329, 12.3440)]
CASTELLO_E = [(45.4403, 12.3496), (45.4403, 12.3510), (45.4402, 12.3545), (45.4399, 12.3574), (45.4391, 12.3589), (45.4379, 12.3604), (45.4369, 12.3623),
              (45.4355, 12.3630), (45.4341, 12.3626), (45.4329, 12.3610), (45.4311, 12.3598), (45.4293, 12.3588), (45.4284, 12.3577), (45.4291, 12.3555),
              (45.4305, 12.3533), (45.4315, 12.3510), (45.4321, 12.3490), (45.4340, 12.3494)]
SP_SC = G[0:19] + [(45.4345, 12.3265), (45.4348, 12.3240), (45.4352, 12.3200), (45.4353, 12.3150), (45.4352, 12.3117), (45.4368, 12.3130), (45.4380, 12.3145), (45.4388, 12.3155)]
DORSODURO = G[18:25] + [(45.4307, 12.3372), (45.4299, 12.3364), (45.4296, 12.3340), (45.4295, 12.3310), (45.4296, 12.3280), (45.4299, 12.3245), (45.4303, 12.3205),
                        (45.4306, 12.3165), (45.4308, 12.3135), (45.4310, 12.3120), (45.4330, 12.3108), (45.4352, 12.3117), (45.4353, 12.3150), (45.4352, 12.3200),
                        (45.4348, 12.3240), (45.4345, 12.3265)]
GIUDECCA_N = [(45.4276, 12.3158), (45.4278, 12.3185), (45.4276, 12.3230), (45.4272, 12.3270), (45.4268, 12.3305), (45.4265, 12.3335), (45.4266, 12.3365),
              (45.4267, 12.3392), (45.4258, 12.3402), (45.4252, 12.3360), (45.4252, 12.3300), (45.4256, 12.3250), (45.4262, 12.3200), (45.4266, 12.3165)]
GIUDECCA_S = [(45.4258, 12.3402), (45.4249, 12.3410), (45.4240, 12.3395), (45.4232, 12.3360), (45.4228, 12.3310), (45.4232, 12.3260), (45.4240, 12.3215),
              (45.4252, 12.3180), (45.4266, 12.3165), (45.4262, 12.3200), (45.4256, 12.3250), (45.4252, 12.3300), (45.4252, 12.3360)]
SAN_GIORGIO_E = [(45.4303, 12.3437), (45.4300, 12.3460), (45.4290, 12.3470), (45.4281, 12.3463), (45.4280, 12.3440), (45.4289, 12.3437)]

BLOCKS = [
    # 900: the islets of Rivoalto, each round its church
    dict(name="Rivoalto", density="loose", periods=[E], polygon=[(45.4398, 12.3328), (45.4392, 12.3348), (45.4381, 12.3352), (45.4368, 12.3336), (45.4374, 12.3314), (45.4390, 12.3314)]),
    dict(name="San Bartolomeo", density="loose", periods=[E], polygon=[(45.4392, 12.3366), (45.4386, 12.3385), (45.4370, 12.3386), (45.4366, 12.3364), (45.4377, 12.3365)]),
    dict(name="San Marco and San Zaccaria", density="loose", periods=[E], polygon=[(45.4362, 12.3383), (45.4362, 12.3436), (45.4334, 12.3442), (45.4331, 12.3414), (45.4350, 12.3412), (45.4353, 12.3386)]),
    dict(name="Olivolo", density="loose", periods=[E], polygon=[(45.4372, 12.3586), (45.4367, 12.3618), (45.4351, 12.3624), (45.4339, 12.3611), (45.4346, 12.3588)]),
    dict(name="Dorsoduro", density="loose", periods=[E], polygon=[(45.4322, 12.3150), (45.4324, 12.3250), (45.4314, 12.3300), (45.4302, 12.3290), (45.4304, 12.3200), (45.4309, 12.3150)]),
    dict(name="Luprio", density="loose", periods=[E], polygon=[(45.4405, 12.3252), (45.4402, 12.3284), (45.4386, 12.3286), (45.4385, 12.3256)]),
    dict(name="Sant'Aponal", density="loose", periods=[E], polygon=[(45.4378, 12.3298), (45.4370, 12.3328), (45.4360, 12.3322), (45.4364, 12.3294)]),
    dict(name="San Geremia", density="loose", periods=[E], polygon=[(45.4442, 12.3240), (45.4437, 12.3292), (45.4428, 12.3295), (45.4431, 12.3252)]),
    dict(name="Gemini (Santi Apostoli)", density="loose", periods=[E], polygon=[(45.4421, 12.3348), (45.4416, 12.3382), (45.4401, 12.3381), (45.4407, 12.3352)]),
    dict(name="Spinalunga", density="loose", periods=[E], polygon=[(45.4271, 12.3240), (45.4266, 12.3330), (45.4255, 12.3330), (45.4258, 12.3240)]),
    # 1204: the core is filling in
    dict(name="Rialto", density="dense", periods=[D], polygon=[(45.4402, 12.3320), (45.4394, 12.3352), (45.4380, 12.3355), (45.4364, 12.3340), (45.4362, 12.3300), (45.4380, 12.3290), (45.4395, 12.3300)]),
    dict(name="San Bartolomeo and San Salvador", density="dense", periods=[D], polygon=[(45.4398, 12.3360), (45.4392, 12.3392), (45.4370, 12.3400), (45.4352, 12.3392), (45.4352, 12.3380), (45.4364, 12.3352), (45.4380, 12.3364)]),
    dict(name="San Marco", density="dense", periods=[D], polygon=[(45.4352, 12.3380), (45.4362, 12.3352), (45.4356, 12.3332), (45.4340, 12.3330), (45.4328, 12.3340), (45.4328, 12.3382)]),
    dict(name="San Zaccaria and Santa Maria Formosa", density="dense", periods=[D], polygon=[(45.4392, 12.3392), (45.4385, 12.3430), (45.4362, 12.3440), (45.4334, 12.3445), (45.4331, 12.3414), (45.4352, 12.3412), (45.4370, 12.3400)]),
    dict(name="Castello", density="loose", periods=[D], polygon=[(45.4385, 12.3430), (45.4400, 12.3470), (45.4380, 12.3490), (45.4340, 12.3492), (45.4322, 12.3488), (45.4328, 12.3445), (45.4362, 12.3440)]),
    dict(name="Olivolo", density="dense", periods=[D], polygon=[(45.4375, 12.3584), (45.4369, 12.3620), (45.4352, 12.3627), (45.4337, 12.3612), (45.4345, 12.3586)]),
    dict(name="Sant'Anna and San Domenico", density="loose", periods=[D], polygon=[(45.4320, 12.3555), (45.4336, 12.3580), (45.4330, 12.3605), (45.4310, 12.3596), (45.4295, 12.3585), (45.4300, 12.3560)]),
    dict(name="Cannaregio", density="loose", periods=[D], polygon=G[0:11] + [(45.4405, 12.3365), (45.4425, 12.3395), (45.4440, 12.3392), (45.4446, 12.3330), (45.4448, 12.3260), (45.4455, 12.3194), (45.4438, 12.3182), (45.4418, 12.3172), (45.4402, 12.3164)]),
    dict(name="Santa Croce and San Polo", density="loose", periods=[D], polygon=G[0:8] + [(45.4402, 12.3320), (45.4380, 12.3290), (45.4362, 12.3300), (45.4352, 12.3260), (45.4352, 12.3150), (45.4368, 12.3130), (45.4380, 12.3145), (45.4388, 12.3155)]),
    dict(name="Dorsoduro", density="loose", periods=[D], polygon=[(45.4340, 12.3276), (45.4321, 12.3290), (45.4316, 12.3330), (45.4302, 12.3345), (45.4297, 12.3300), (45.4302, 12.3220), (45.4307, 12.3150), (45.4330, 12.3115), (45.4348, 12.3150), (45.4350, 12.3240)]),
    dict(name="Spinalunga", density="loose", periods=[D], polygon=GIUDECCA_N),
    # 1400 onward
    dict(name="Cannaregio", density="dense", periods=[R], polygon=CANNAREGIO_S),
    dict(name="Northern Cannaregio", density="loose", periods=[R], polygon=CANNAREGIO_N),
    dict(name="Cannaregio", density="dense", periods=MODERN, polygon=CANNAREGIO),
    dict(name="San Marco", density="dense", periods=LATE, polygon=SAN_MARCO),
    dict(name="Castello", density="dense", periods=LATE, polygon=CASTELLO_W),
    dict(name="Eastern Castello", density="loose", periods=[R], polygon=CASTELLO_E),
    dict(name="Eastern Castello", density="dense", periods=MODERN, polygon=CASTELLO_E),
    dict(name="San Polo and Santa Croce", density="dense", periods=LATE, polygon=SP_SC),
    dict(name="Dorsoduro", density="dense", periods=LATE, polygon=DORSODURO),
    dict(name="Giudecca", density="loose", periods=[R], polygon=GIUDECCA_N),
    dict(name="Giudecca", density="dense", periods=MODERN, polygon=GIUDECCA_N),
    dict(name="Monastery of San Giorgio", density="loose", periods=LATER, polygon=SAN_GIORGIO_E),
    dict(name="Sant'Elena", density="loose", periods=LATE, polygon=SANT_ELENA),
]

GARDENS = [
    dict(name="Gardens of the Giudecca", kind="orchard", periods=LATE, polygon=GIUDECCA_S),
    dict(name="Vineyards of Spinalunga", kind="vineyard", periods=[E, D], polygon=GIUDECCA_S),
    dict(name="Monastery gardens of San Michele", kind="park", periods=LATER, polygon=SAN_MICHELE),
]

MARSH = [
    # 900: barene between the islets
    dict(name="Marshes of Cannaregio", periods=[E], polygon=[(45.4471, 12.3215), (45.4472, 12.3300), (45.4466, 12.3352), (45.4452, 12.3382), (45.4436, 12.3402), (45.4424, 12.3420),
                                                              (45.4412, 12.3440), (45.4400, 12.3420), (45.4405, 12.3390), (45.4425, 12.3392), (45.4435, 12.3370), (45.4440, 12.3330),
                                                              (45.4448, 12.3300), (45.4448, 12.3235), (45.4457, 12.3200)]),
    dict(name="Marshes of Castello and the Zemelle", periods=[E], polygon=[(45.4410, 12.3450), (45.4404, 12.3490), (45.4402, 12.3545), (45.4399, 12.3574), (45.4385, 12.3582),
                                                                           (45.4340, 12.3582), (45.4320, 12.3560), (45.4310, 12.3520), (45.4320, 12.3488), (45.4326, 12.3455),
                                                                           (45.4360, 12.3445), (45.4390, 12.3438)]),
    dict(name="Marshes of Santa Croce", periods=[E], polygon=[(45.4398, 12.3168), (45.4405, 12.3215), (45.4402, 12.3245), (45.4380, 12.3250), (45.4365, 12.3240), (45.4355, 12.3200),
                                                              (45.4352, 12.3125), (45.4372, 12.3138), (45.4388, 12.3157)]),
    dict(name="Marshes of Sant'Elena", periods=[E, D], polygon=SANT_ELENA),
    dict(name="Marshes of Dorsoduro", periods=[E], polygon=[(45.4346, 12.3205), (45.4345, 12.3262), (45.4332, 12.3268), (45.4327, 12.3252), (45.4327, 12.3150), (45.4350, 12.3128)]),
    dict(name="Marshes of Santi Apostoli", periods=[E], polygon=[(45.4442, 12.3302), (45.4436, 12.3345), (45.4426, 12.3345), (45.4424, 12.3330), (45.4430, 12.3302)]),
    dict(name="Marshes of Spinalunga", periods=[E], polygon=[(45.4276, 12.3160), (45.4277, 12.3230), (45.4262, 12.3230), (45.4266, 12.3165)]),
    dict(name="Marshes of San Michele", periods=[E], polygon=SAN_MICHELE),
    # 1204: the fringes
    dict(name="Northern marshes", periods=[D], polygon=[(45.4450, 12.3260), (45.4448, 12.3330), (45.4442, 12.3395), (45.4455, 12.3378), (45.4466, 12.3350), (45.4470, 12.3300),
                                                        (45.4471, 12.3240), (45.4466, 12.3212), (45.4457, 12.3198)]),
    dict(name="Marshes of the Celestia", periods=[D], polygon=[(45.4430, 12.3410), (45.4422, 12.3430), (45.4412, 12.3460), (45.4405, 12.3485), (45.4402, 12.3495), (45.4396, 12.3475), (45.4402, 12.3470), (45.4410, 12.3430)]),
]

DISTRICTS = [
    dict(id="cannaregio", name="Cannaregio", periods=LATER, polygon=CANNAREGIO,
         description="The northern sestiere, named after the canal of reeds (canne) that leads into it: parish churches, long fondamente, the Ghetto, gardens and the houses of boatmen and artisans."),
    dict(id="san-marco", name="San Marco", periods=LATER, polygon=SAN_MARCO,
         description="The sestiere of government and money: the Piazza, the Doge's Palace, the Mercerie and the richest shops, inside the last bend of the Grand Canal."),
    dict(id="castello", name="Castello", periods=LATER, polygon=CASTELLO_W[:13] + CASTELLO_E[1:-1] + CASTELLO_W[15:],
         description="The eastern sestiere, named after the castle of Olivolo: the cathedral of San Pietro, the Arsenal and the dense parishes of its shipwrights, sailors and Dalmatian and Greek merchants."),
    dict(id="san-polo", name="San Polo and Santa Croce", periods=LATER, polygon=SP_SC,
         description="The two sestieri on the inside of the Grand Canal's great bend, from the Rialto market to the western edge of the city, with the Frari and the Scuola of San Rocco."),
    dict(id="dorsoduro", name="Dorsoduro", periods=LATER, polygon=DORSODURO + [(45.4296, 12.3280)],
         description="The 'hard back', the firmest ground of the islands, from the Punta della Dogana to the fishermen's parish of San Nicolò dei Mendicoli; the Giudecca belonged to it."),
]

LABELS = [
    dict(text="Laguna Veneta", position=(45.4500, 12.3200), size="lg", rotation=-4),
    dict(text="Canal Grande", position=(45.4349, 12.3296), size="sm", rotation=-15, periods=LATER),
    dict(text="Rivo Alto", position=(45.4349, 12.3296), size="sm", rotation=-15, periods=[E]),
    dict(text="Canale della Giudecca", position=(45.4285, 12.3240), size="md", rotation=4),
    dict(text="Bacino di San Marco", position=(45.4312, 12.3445), size="md", rotation=-6),
    dict(text="Giudecca", position=(45.4243, 12.3300), size="md", rotation=4, periods=LATE),
    dict(text="Spinalunga", position=(45.4243, 12.3300), size="md", rotation=4, periods=[E, D]),
    dict(text="San Giorgio", position=(45.4272, 12.3455), size="sm", rotation=0),
    dict(text="San Michele", position=(45.4500, 12.3468), size="sm", rotation=0),
    dict(text="Sant'Elena", position=(45.4247, 12.3622), size="sm", rotation=0),
    dict(text="to Murano", position=(45.4515, 12.3530), size="sm", rotation=0),
    dict(text="to the Lido", position=(45.4235, 12.3580), size="sm", rotation=-20),
    dict(text="to Mestre and the mainland", position=(45.4490, 12.3110), size="sm", rotation=-20),
]
