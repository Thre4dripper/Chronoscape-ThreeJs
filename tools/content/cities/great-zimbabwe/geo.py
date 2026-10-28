# Great Zimbabwe: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
ALL = ["early-1100", "zenith-1350", "decline-1500"]
STONE = ["zenith-1350", "decline-1500"]

SOURCES = [
    dict(id="garlake-gz", title="Great Zimbabwe", author="Peter Garlake", year=1973),
    dict(id="huffman-symbols", title="Symbols in Stone: Unravelling the Mystery of Great Zimbabwe", author="Thomas N. Huffman", year=1987),
    dict(id="pikirayi-zimbabwe-culture", title="The Zimbabwe Culture: Origins and Decline of Southern Zambezian States", author="Innocent Pikirayi", year=2001),
    dict(id="chirikure-pikirayi", title="Inside and outside the dry stone walls: revisiting the material culture of Great Zimbabwe", author="Shadreck Chirikure and Innocent Pikirayi", year=2008, note="Antiquity 82"),
    dict(id="chirikure-2017", title="New pathways of sociopolitical complexity in southern Africa: Great Zimbabwe's chronology", author="Shadreck Chirikure et al.", year=2017, note="PLoS ONE / African Archaeological Review papers on the site's dating"),
    dict(id="unesco-gz", title="Great Zimbabwe National Monument (World Heritage List no. 364)", author="UNESCO World Heritage Centre", year=1986, url="https://whc.unesco.org/en/list/364/"),
    dict(id="wiki-great-zimbabwe", title="Great Zimbabwe", author="Wikipedia", url="https://en.wikipedia.org/wiki/Great_Zimbabwe"),
    dict(id="wiki-kingdom-gz", title="Kingdom of Great Zimbabwe", author="Wikipedia", url="https://en.wikipedia.org/wiki/Kingdom_of_Great_Zimbabwe"),
    dict(id="wiki-mapungubwe", title="Kingdom of Mapungubwe", author="Wikipedia", url="https://en.wikipedia.org/wiki/Kingdom_of_Mapungubwe"),
    dict(id="wiki-mutapa", title="Mutapa Empire", author="Wikipedia", url="https://en.wikipedia.org/wiki/Mutapa_Empire"),
    dict(id="wiki-khami", title="Khami", author="Wikipedia", url="https://en.wikipedia.org/wiki/Khami"),
    dict(id="wiki-lake-mutirikwe", title="Lake Mutirikwe", author="Wikipedia", url="https://en.wikipedia.org/wiki/Lake_Mutirikwe"),
    dict(id="wiki-sofala", title="Sofala", author="Wikipedia", url="https://en.wikipedia.org/wiki/Sofala"),
]

CITY = dict(
    name="Great Zimbabwe", subtitle="Dzimba dza mabwe, the houses of stone",
    description="Four centuries of Great Zimbabwe in the granite hills of the southern Zimbabwean plateau: the first walls on the hill, the stone city of the 14th century with its Great Enclosure, Hill Complex and Valley Ruins among thousands of daga houses, and the half-empty court of the 16th century. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="zenith-1350",
    world=dict(heightScale=1.0, walls=["#A87E58", "#9C7350", "#B48A62", "#A2795A", "#B08C68"], roofs=["#B39A5E", "#A88E58", "#BFA56A"]),
    camera=dict(target=(-20.2705, 30.9338), distance=26),
)

# north-west corner, south-east corner: the hills north of the Hill Complex, the streams draining south-east toward the Mutirikwi
FRAME = ((-20.2550, 30.9160), (-20.2850, 30.9490))

PALETTE = dict(parchment="#E8D6AE", ink="#5E4632", water="#62878A", hill="#8C8A6A", road="#8A6A4A")
COMPASS = (-20.2575, 30.9465)
CARTOUCHE = (-20.2843, 30.9168)

PERIODS = [
    dict(id="early-1100", label="The first walls on the hill", year=1100, startYear=1000, endYear=1289,
         summary="Farmers and cattle-keepers, speakers of an early form of Shona (archaeologists' Gumanye phase of the Zimbabwe culture; earlier Gokomere-tradition pottery is also found here), live on and around the granite hill. Daga houses crowd its top; around 1100, it is usually thought, the first rough stone walls go up among the boulders. Cattle, sorghum and a little gold and ivory for trade.",
         population="a few hundred, perhaps a thousand (no reliable estimate)",
         feel="Cattle lowing in the valley at dawn, smoke from the hilltop hearths, the knock of iron hoes in the fields after the first rains.",
         style="kraal",
         houses=dict(title="Daga houses on the hill", text="Round houses of daga, a mud-and-gravel plaster over a frame of poles, under conical grass thatch, set close together on terraces among the boulders, each family's houses round a swept yard (dare)."),
         outskirts=dict(title="Homesteads and cattle pens", text="Scattered homesteads of a few round houses, granaries on stilts and a pole-and-thorn pen for cattle and goats, with sorghum and finger-millet fields cleared from the woodland.")),
    dict(id="zenith-1350", label="The stone city", year=1350, startYear=1290, endYear=1449,
         summary="The capital of the Zimbabwe state at its height. In the usual reading, the king's court has moved down from the hill to the Great Enclosure, whose outer wall, 11 m high and 250 m long, is laid in courses of dressed granite without mortar. Gold and ivory from the plateau go to the Swahili coast at Sofala and Kilwa; Chinese celadon, Persian faience and glass beads come back.",
         population="perhaps 10,000 (older estimates up to 18,000)",
         feel="Gongs and drums from the Great Enclosure, the clink of masons dressing granite blocks, woodsmoke and cattle dung, the bright clay of new daga houses after the rains.",
         style="kraal",
         houses=dict(title="Daga houses in their yards", text="Round daga houses with conical thatch, the better ones of solid daga with moulded thresholds, benches and raised floors, grouped round a swept yard (dare) and linked by low daga walls; inside the stone enclosures the houses of the court stand on platforms."),
         outskirts=dict(title="Homesteads of the commoners", text="Most of the people live outside the stone walls in homesteads of a few huts with granaries and cattle pens, the houses of daga and poles, the fields of sorghum and millet spreading down the valleys.")),
    dict(id="decline-1500", label="The emptying court", year=1500, startYear=1450, endYear=1600,
         summary="Power has moved north to the Mutapa state on the Zambezi and west to Khami, and the trade with it. Great Zimbabwe is largely abandoned by around 1450; its walls still stand, a smaller community lives on in the valley, and Portuguese writers at Sofala hear of a stone 'Symbaoe' kept by a royal officer, with a tower 'more than twelve fathoms high'.",
         population="a few hundred to a few thousand (estimates vary)",
         feel="Wind in the grass on top of the walls, fig roots prising at the stones, a few cattle in the old kraal, the hill shrine still visited.",
         style="kraal",
         houses=dict(title="Fewer houses in the valley", text="Round daga houses with conical thatch in the Valley and below the Great Enclosure, some built against the old walls; the large platforms of the court lie empty and their houses melt back into mounds of daga."),
         outskirts=dict(title="Bush returning", text="Old fields going back to msasa woodland and grass, a few homesteads with granaries and cattle pens, paths still worn between the empty stone enclosures.")),
]

# ---------------------------------------------------------------- water: two narrow streams draining the valley toward the Mutirikwi
WEST_STREAM = [(-20.2550, 30.9235), (-20.2610, 30.9248), (-20.2660, 30.9262), (-20.2715, 30.9282), (-20.2750, 30.9322), (-20.2772, 30.9350),
               (-20.2800, 30.9395), (-20.2830, 30.9440), (-20.2850, 30.9468)]
EAST_STREAM = [(-20.2550, 30.9445), (-20.2620, 30.9450), (-20.2670, 30.9440), (-20.2730, 30.9452), (-20.2790, 30.9448), (-20.2830, 30.9442)]

WATER = [
    dict(id="west-stream", name="Stream of the western valley", path=WEST_STREAM, width=10,
         blurb="A small stream running down the west side of the Hill and round below the Great Enclosure toward the Mutirikwi, full in the rains (November to March) and a string of pools in the dry season. Its course is drawn approximately."),
    dict(id="east-stream", name="Stream below the eastern ridge", path=EAST_STREAM, width=8,
         blurb="A seasonal stream along the foot of the eastern ridge, joining the western stream on the way to the Mutirikwi. Springs and seepage pits (dhaka pits) round the site stored the rest of the town's water."),
]

HILLS = [
    dict(id="the-hill", name="The Hill (granite kopje)", center=(-20.2668, 30.9334), radius=300,
         blurb="A granite hill rising about 80 m above the valley, its top a jumble of huge rounded boulders, its southern face a sheer cliff. The Hill Complex is built among the boulders on its summit; it was the first part of the site to be settled and walled."),
    dict(id="eastern-ridge", name="Eastern ridge", center=(-20.2690, 30.9410), radius=220,
         blurb="A low granite ridge on the east side of the valley, with stone enclosures (the Eastern Ruins) on its slope and homesteads below."),
    dict(id="northern-hills", name="Northern hills", center=(-20.2585, 30.9215), radius=300,
         blurb="Wooded granite hills north-west of the site; the paths to the gold-bearing plateau and the inland chiefdoms ran past them."),
    dict(id="western-kopje", name="Western kopje", center=(-20.2680, 30.9215), radius=200, label=False,
         blurb="A smaller granite dome west of the Hill, among msasa woodland."),
    dict(id="southern-kopjes", name="Southern kopjes", center=(-20.2820, 30.9225), radius=250,
         blurb="Bare granite domes and boulder heaps south of the valley; granite exfoliates naturally into slabs, which builders split further, probably with fire and water, into the blocks of the walls."),
    dict(id="south-east-kopje", name="South-eastern kopje", center=(-20.2780, 30.9470), radius=150, label=False,
         blurb="A granite outcrop above the streams on the way down toward the Mutirikwi valley."),
]

ROADS = [
    dict(id="coast-path", name="Path toward Sofala and the coast", path=[(-20.2738, 30.9352), (-20.2745, 30.9400), (-20.2770, 30.9450), (-20.2805, 30.9490)], width=7, style="major", labelled=True,
         blurb="The way out to the south-east, down toward the Save river and, some 400 km away, the Swahili port of Sofala, where gold and ivory were traded for cloth and beads. Goods probably passed through several hands on the way.",
         periods=STONE),
    dict(id="plateau-path", name="Path to the goldfields of the plateau", path=[(-20.2694, 30.9305), (-20.2660, 30.9265), (-20.2620, 30.9222), (-20.2595, 30.9160)], width=7, style="major", labelled=True,
         blurb="The way north-west onto the high plateau, where gold was dug from shallow shafts on the reefs and washed from river sands, and where many smaller zimbabwes of the state stood.",
         periods=STONE),
    dict(id="plateau-track", name="Track to the plateau", path=[(-20.2694, 30.9305), (-20.2660, 30.9265), (-20.2620, 30.9222), (-20.2595, 30.9160)], width=5, style="minor",
         blurb="A herders' and hunters' track north-west toward the plateau.", periods=["early-1100"]),
    dict(id="valley-path", name="Path through the Valley", path=[(-20.2694, 30.9324), (-20.2703, 30.9332), (-20.2712, 30.9340), (-20.2722, 30.9346)], width=6, style="minor", labelled=False,
         blurb="The path from the foot of the Hill's Ancient Ascent through the Valley to the north entrance of the Great Enclosure.", periods=STONE),
    dict(id="kraal-path", name="Path to the cattle kraal", path=[(-20.2730, 30.9334), (-20.2742, 30.9312), (-20.2752, 30.9300)], width=5, style="minor",
         blurb="Cattle were driven along it from the kraal to the grazing; cattle were the measure of a man's wealth and the core of the court's power.", periods=ALL),
    dict(id="ridge-path", name="Path to the eastern ridge", path=[(-20.2708, 30.9362), (-20.2705, 30.9380), (-20.2698, 30.9392)], width=5, style="minor",
         blurb="Up from the Valley to the enclosures on the eastern ridge.", periods=STONE),
    dict(id="fields-path", name="Path to the southern fields", path=[(-20.2738, 30.9338), (-20.2765, 30.9318), (-20.2785, 30.9306)], width=5, style="minor",
         blurb="Down to the fields of sorghum and finger millet south of the town.", periods=STONE),
    dict(id="north-path", name="Path north round the Hill", path=[(-20.2652, 30.9348), (-20.2610, 30.9345), (-20.2550, 30.9340)], width=5, style="minor",
         blurb="Round the back of the Hill to the northern homesteads and fields.", periods=ALL),
    dict(id="east-fields-path", name="Path to the eastern homesteads", path=[(-20.2738, 30.9365), (-20.2750, 30.9385), (-20.2770, 30.9405)], width=5, style="minor",
         blurb="From the Great Enclosure toward the homesteads and fields by the eastern stream.", periods=ALL),
]

BLOCKS = [
    # ---- c. 1100: houses on the Hill's slopes and a few homesteads in the valley
    dict(name="Homesteads below the Hill, north", polygon=[(-20.2636, 30.9295), (-20.2636, 30.9375), (-20.2648, 30.9375), (-20.2648, 30.9295)], density="loose", periods=["early-1100"]),
    dict(name="Homesteads of the valley", polygon=[(-20.2694, 30.9290), (-20.2694, 30.9340), (-20.2710, 30.9340), (-20.2710, 30.9292)], density="loose", periods=["early-1100"]),
    dict(name="Homesteads by the eastern stream", polygon=[(-20.2716, 30.9398), (-20.2716, 30.9428), (-20.2738, 30.9428), (-20.2738, 30.9398)], density="loose", periods=["early-1100"]),
    # ---- 1350: the town round the stone enclosures
    dict(name="The Valley, west", polygon=[(-20.2693, 30.9285), (-20.2693, 30.9340), (-20.2712, 30.9340), (-20.2712, 30.9292)], density="dense", periods=["zenith-1350"]),
    dict(name="The Valley, east", polygon=[(-20.2693, 30.9345), (-20.2693, 30.9395), (-20.2708, 30.9395), (-20.2714, 30.9345)], density="dense", periods=["zenith-1350"]),
    dict(name="Below the Great Enclosure", polygon=[(-20.2738, 30.9318), (-20.2738, 30.9372), (-20.2760, 30.9378), (-20.2760, 30.9342)], density="dense", periods=["zenith-1350"]),
    dict(name="The eastern slopes", polygon=[(-20.2715, 30.9395), (-20.2715, 30.9430), (-20.2745, 30.9430), (-20.2745, 30.9390)], density="loose", periods=["zenith-1350"]),
    dict(name="Homesteads north of the Hill", polygon=[(-20.2634, 30.9290), (-20.2634, 30.9380), (-20.2648, 30.9380), (-20.2648, 30.9290)], density="loose", periods=["zenith-1350"]),
    dict(name="West of the stream", polygon=[(-20.2690, 30.9236), (-20.2690, 30.9262), (-20.2730, 30.9272), (-20.2730, 30.9246)], density="loose", periods=["zenith-1350"]),
    dict(name="Toward the streams' meeting", polygon=[(-20.2765, 30.9385), (-20.2765, 30.9420), (-20.2788, 30.9425), (-20.2788, 30.9398)], density="loose", periods=["zenith-1350"]),
    dict(name="Below the eastern ridge", polygon=[(-20.2655, 30.9385), (-20.2655, 30.9420), (-20.2672, 30.9420), (-20.2672, 30.9385)], density="loose", periods=["zenith-1350"]),
    # ---- 1500: a smaller community in the valley
    dict(name="The Valley", polygon=[(-20.2694, 30.9300), (-20.2694, 30.9390), (-20.2708, 30.9390), (-20.2712, 30.9300)], density="loose", periods=["decline-1500"]),
    dict(name="Below the Great Enclosure", polygon=[(-20.2740, 30.9322), (-20.2740, 30.9365), (-20.2756, 30.9370), (-20.2756, 30.9340)], density="loose", periods=["decline-1500"]),
    dict(name="Homesteads north of the Hill", polygon=[(-20.2636, 30.9310), (-20.2636, 30.9365), (-20.2647, 30.9365), (-20.2647, 30.9310)], density="loose", periods=["decline-1500"]),
]

GARDENS = [
    dict(name="Sorghum and finger-millet fields", polygon=[(-20.2768, 30.9238), (-20.2768, 30.9275), (-20.2800, 30.9282), (-20.2800, 30.9245)], kind="orchard"),
    dict(name="Fields by the eastern stream", polygon=[(-20.2780, 30.9420), (-20.2780, 30.9439), (-20.2810, 30.9439), (-20.2810, 30.9422)], kind="orchard", periods=STONE),
    dict(name="Northern fields", polygon=[(-20.2575, 30.9310), (-20.2575, 30.9362), (-20.2600, 30.9362), (-20.2600, 30.9310)], kind="orchard"),
]

DISTRICTS = [
    dict(id="the-hill", name="The Hill", polygon=[(-20.2655, 30.9300), (-20.2655, 30.9375), (-20.2685, 30.9375), (-20.2690, 30.9300)],
         description="The granite hill and its summit enclosures, the oldest part of the site: dwelling of the first rulers, then, many think, a place of ritual and the ancestors, where the soapstone birds stood."),
    dict(id="the-valley", name="The Valley", polygon=[(-20.2693, 30.9285), (-20.2693, 30.9395), (-20.2715, 30.9395), (-20.2715, 30.9285)], periods=STONE,
         description="The ground between the Hill and the Great Enclosure, filled in the 14th and 15th centuries with smaller stone enclosures (the Valley Ruins) and the daga houses of the court's people. Boundaries approximate."),
    dict(id="great-enclosure-precinct", name="Great Enclosure", polygon=[(-20.2718, 30.9328), (-20.2718, 30.9362), (-20.2740, 30.9362), (-20.2740, 30.9328)], periods=STONE,
         description="The great walled residence of the king and his household, with the conical tower and the platforms of the court, surrounded by the houses of officials and craftsmen."),
    dict(id="outer-town", name="The homesteads", polygon=[(-20.2738, 30.9300), (-20.2738, 30.9430), (-20.2790, 30.9430), (-20.2790, 30.9300)], periods=["zenith-1350"],
         description="The outer town where most people lived, in homesteads of daga houses, granaries and cattle pens. Excavation has found houses well beyond the stone walls; how far the town spread is debated."),
]

LABELS = [
    dict(text="Dzimba dza mabwe", position=(-20.2600, 30.9395), size="lg", periods=STONE),
    dict(text="The Hill", position=(-20.2645, 30.9334), size="md", periods=["early-1100"]),
    dict(text="The Hill", position=(-20.2658, 30.9334), size="sm", periods=STONE),
    dict(text="The Valley", position=(-20.2704, 30.9395), size="sm", periods=STONE),
    dict(text="to Sofala and the coast", position=(-20.2815, 30.9455), size="sm", rotation=-40, periods=STONE),
    dict(text="to the goldfields", position=(-20.2610, 30.9185), size="sm", rotation=40, periods=STONE),
    dict(text="toward the Mutirikwi", position=(-20.2840, 30.9405), size="sm"),
    dict(text="msasa woodland", position=(-20.2565, 30.9420), size="sm"),
    dict(text="granite kopjes", position=(-20.2820, 30.9225), size="sm"),
]
