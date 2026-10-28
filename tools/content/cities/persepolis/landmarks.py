# Persepolis landmarks (see tools/content/cities/FORMAT.md). Positions in metres from the centre of the terrace, projected by L().
import math

ALL = ["darius-500", "xerxes-460", "burned-330", "sasanian-250"]
FROM_XERXES = ["xerxes-460", "burned-330", "sasanian-250"]
LATER = ["burned-330", "sasanian-250"]

C_LAT, C_LON = 29.93480, 52.89050
M_LAT = 1.0 / 110860.0
M_LON = 1.0 / (111320.0 * math.cos(math.radians(C_LAT)))


def L(x, y):
    return (round(C_LAT + y * M_LAT, 6), round(C_LON + x * M_LON, 6))


SOURCES = [
    dict(id="wiki-persepolis", title="Persepolis", author="Wikipedia", url="https://en.wikipedia.org/wiki/Persepolis"),
    dict(id="wiki-apadana", title="Apadana", author="Wikipedia", url="https://en.wikipedia.org/wiki/Apadana"),
    dict(id="wiki-gate-all-nations", title="Gate of All Nations", author="Wikipedia", url="https://en.wikipedia.org/wiki/Gate_of_All_Nations"),
    dict(id="wiki-tachara", title="Tachara", author="Wikipedia", url="https://en.wikipedia.org/wiki/Tachara"),
    dict(id="wiki-achaemenid-architecture", title="Achaemenid architecture", author="Wikipedia", url="https://en.wikipedia.org/wiki/Achaemenid_architecture"),
    dict(id="wiki-persian-column", title="Persian column", author="Wikipedia", url="https://en.wikipedia.org/wiki/Persian_column"),
    dict(id="wiki-lamassu", title="Lamassu", author="Wikipedia", url="https://en.wikipedia.org/wiki/Lamassu"),
    dict(id="wiki-pfa", title="Persepolis Administrative Archives", author="Wikipedia", url="https://en.wikipedia.org/wiki/Persepolis_Administrative_Archives"),
    dict(id="wiki-artaxerxes-ii", title="Artaxerxes II", author="Wikipedia", url="https://en.wikipedia.org/wiki/Artaxerxes_II"),
    dict(id="wiki-artaxerxes-iii", title="Artaxerxes III", author="Wikipedia", url="https://en.wikipedia.org/wiki/Artaxerxes_III"),
    dict(id="wiki-naqsh-e-rostam", title="Naqsh-e Rostam", author="Wikipedia", url="https://en.wikipedia.org/wiki/Naqsh-e_Rostam"),
    dict(id="wiki-persian-garden", title="Persian gardens", author="Wikipedia", url="https://en.wikipedia.org/wiki/Persian_gardens"),
    dict(id="wiki-pasargadae", title="Pasargadae", author="Wikipedia", url="https://en.wikipedia.org/wiki/Pasargadae"),
    dict(id="wiki-xerxes", title="Xerxes I", author="Wikipedia", url="https://en.wikipedia.org/wiki/Xerxes_I"),
    dict(id="wiki-darius", title="Darius the Great", author="Wikipedia", url="https://en.wikipedia.org/wiki/Darius_the_Great"),
    dict(id="schmidt-persepolis", title="Persepolis I–III", author="Erich F. Schmidt", year="1953–1970"),
    dict(id="mousavi-persepolis", title="Persepolis: Discovery and Afterlife of a World Wonder", author="Ali Mousavi", year=2012),
    dict(id="roaf-1983", title="Sculptures and Sculptors at Persepolis", author="Michael Roaf", year=1983),
    dict(id="tilia-1972", title="Studies and Restorations at Persepolis and Other Sites of Fars", author="Ann Britt Tilia", year="1972–1978"),
    dict(id="briant", title="From Cyrus to Alexander: A History of the Persian Empire", author="Pierre Briant", year=2002),
    dict(id="diodorus-17", title="Library of History, Book 17", author="Diodorus Siculus", year="1st century BCE", url="https://en.wikipedia.org/wiki/Bibliotheca_historica"),
]

LANDMARKS = [
    # ------------------------------------------------------------ the terrace
    dict(id="takht", name="The Takht and the Great Stair", category="monument",
         latlon=L(-146, 162), rotation=90, footprint=(136, 40), scale=1.0, model="persepolis/takht",
         activePeriods=ALL,
         variants={
             "darius-500": dict(model="persepolis/takht-500", note="The terrace is being built. The double stair is a building site, its lower flights laid, the upper ones a ramp of earth; it may date to late Darius or to Xerxes.", confidence="reconstruction"),
             "xerxes-460": dict(note="Finished: two mirrored flights of shallow steps climb the west face to the landing before the Gate of All Nations. A mud-brick wall with towers crowns the terrace edge."),
             "burned-330": dict(model="persepolis/takht-ruin", note="The stair and the stone face survive the fire; the mud-brick parapet and towers are crumbling.", confidence="reconstruction"),
             "sasanian-250": dict(model="persepolis/takht-ruin", note="The great stair still leads up into the ruins, worn and half buried at its foot by washed-down earth.", confidence="reconstruction"),
         },
         summary="The royal terrace of Persepolis, about 455 by 300 m and some 12 m high at the stair, cut and built against Kuh-e Rahmat from about 518 BCE, climbed by a double stair of shallow steps.",
         details=["Darius I had the rock levelled and the hollows filled, then faced the platform with huge limestone blocks fitted without mortar and tied with iron clamps; drains cut in the rock carried off the rain. His inscriptions on the south wall ask Ahuramazda to protect the land from the hostile army, from famine and from the Lie. The double stair climbs the west face in two mirrored pairs of flights.",
                  "The steps are only about 10 cm high and very deep, so it is often said a horse could be ridden up them. The miniature shows a stretch of the west face with the stair, the parapet and the mud-brick wall with towers that crowned the edge, and the corner where the fortification turns east along the north side. The height of the wall and its towers is a reconstruction."],
         built="c. 518–480 BCE", function="Royal terrace and its monumental entrance", confidence="documented",
         sourceIds=["wiki-persepolis", "schmidt-persepolis", "mousavi-persepolis"], activity=dict(figures=40, radius=120)),

    dict(id="gate-all-nations", name="Gate of All Nations", category="monument",
         latlon=L(-98, 160), rotation=90, footprint=(26, 30), scale=1.0, model="persepolis/gate-all-nations",
         activePeriods=FROM_XERXES,
         variants={
             "darius-500": dict(note="Not yet built: the top of the stair, if it exists yet, opens onto a bare forecourt. Xerxes will raise the gate."),
             "xerxes-460": dict(note="New: a square hall with four tall columns, its west door guarded by two colossal bulls, its east door by two human-headed winged bulls, a third door south toward the Apadana."),
             "burned-330": dict(model="persepolis/gate-all-nations-ruin", note="Roofless after the fire; the mud-brick walls are falling, but the stone bulls and some of the columns stand.", confidence="reconstruction"),
             "sasanian-250": dict(model="persepolis/gate-all-nations-ruin", note="The bulls still guard an empty doorway. Some of its columns will survive into modern times, and later travellers will carve their names on the bulls.", confidence="reconstruction"),
         },
         summary="Xerxes' entrance hall at the top of the great stair, guarded by colossal stone bulls on the west and human-headed winged bulls on the east.",
         details=["Xerxes' trilingual inscription (Old Persian, Elamite, Babylonian) above the bulls says that by the favour of Ahuramazda he built this 'gate of all lands'. The hall was about 25 m square, with four columns about 16.5 m high, a wooden roof and mud-brick walls; its stone door jambs carried the bulls, which look back to the Assyrian lamassu of Nineveh.",
                  "The miniature shows the hall with its four fluted columns and capitals, the stone doorways with simplified winged bulls on the west and east, and the stepped parapet. The ruin keeps the bulls, two columns and the stumps of the walls. The roof height and parapet are reconstructed."],
         built="c. 480 BCE", function="Monumental gateway and waiting hall", confidence="documented",
         sourceIds=["wiki-gate-all-nations", "wiki-lamassu", "schmidt-persepolis"], activity=dict(figures=16, radius=40)),

    dict(id="apadana", name="Apadana (audience hall)", category="civic",
         latlon=L(-54, 64), rotation=180, footprint=(124, 124), scale=1.0, model="persepolis/apadana",
         activePeriods=ALL,
         variants={
             "darius-500": dict(model="persepolis/apadana-500", note="Under construction since about 515: the platform and the gold and silver foundation tablets are in place, the first columns rise among timber cranes and the stair reliefs are being carved.", confidence="reconstruction"),
             "xerxes-460": dict(note="Complete under Xerxes: 72 columns, a cedar roof, painted reliefs on the north and east stairs, and four corner towers."),
             "burned-330": dict(model="persepolis/apadana-burned", note="The roof burned and fell in 330; the mud-brick walls are slumping, but most of the stone columns still stand, blackened, among the debris.", confidence="reconstruction"),
             "sasanian-250": dict(model="persepolis/apadana-ruin", note="A field of standing columns over the buried stairs; earthquakes and stone-robbers have brought many down. Thirteen still stand today.", confidence="reconstruction"),
         },
         summary="Darius' and Xerxes' great audience hall: 72 slender fluted columns about 20 m tall with double-bull capitals, on a platform reached by stairs carved with the peoples of the empire bringing gifts.",
         details=["Begun about 515 BCE and finished under Xerxes. The square hall, about 60 m a side, had 36 columns; porticoes of 12 columns opened on the north, east and west, with towers at the corners and storerooms on the south. Under the corners Darius buried stone boxes with gold and silver tablets naming his empire 'from Scythia beyond Sogdiana to Kush, from India to Sardis'.",
                  "The north and east stairs are carved with Persian and Median guards and 23 delegations leading horses, camels and lions and carrying cloth, vessels and gold. The miniature shows the platform, the 72 columns with bell bases and double-bull capitals, the cedar roof and corner towers, and the reliefs as raised bands. Wall height, roof and colours are reconstructed."],
         built="c. 515–480 BCE", function="Audience hall of the king", confidence="documented",
         sourceIds=["wiki-apadana", "wiki-persian-column", "schmidt-persepolis", "roaf-1983"], activity=dict(figures=60, radius=90)),

    dict(id="hundred-columns", name="Hall of a Hundred Columns", category="civic",
         latlon=L(62, 76), rotation=180, footprint=(72, 92), scale=1.0, model="persepolis/hundred-columns",
         activePeriods=FROM_XERXES,
         variants={
             "darius-500": dict(note="Open ground at the foot of the mountain. Xerxes will begin the great hall here."),
             "xerxes-460": dict(note="Begun by Xerxes and being completed by Artaxerxes I: the columns stand, the roof timbers are going up, and the carved stone doorways are finished."),
             "burned-330": dict(model="persepolis/hundred-columns-ruin", note="Burned so fiercely that its columns cracked and fell; the stone doorways still stand round a field of drums and ash.", confidence="reconstruction"),
             "sasanian-250": dict(model="persepolis/hundred-columns-ruin", note="Doorways in a field of column bases. Sasanian Persians seem to have called the ruins Sad Stun, 'the Hundred Columns'.", confidence="reconstruction"),
         },
         summary="The largest hall on the terrace, 70 m square with ten rows of ten columns, a porch of sixteen columns between colossal bulls, and eight carved stone doorways.",
         details=["Begun by Xerxes and finished by Artaxerxes I, it is sometimes called the Throne Hall: the reliefs of its doorways show the king enthroned under a canopy, his throne lifted by figures of the subject peoples, and the king as hero stabbing lions and monsters. Its use is unknown; when Alexander came, it may have stored treasure and armour.",
                  "The miniature shows the square hall with its hundred columns, the north porch between two colossal bulls, the stone door frames with Egyptian-style cavetto cornices and the flat cedar roof. The ruin keeps the doorways, the column bases and a few stumps. Column height (about 14 m) and the roof are reconstructed."],
         built="c. 470–450 BCE", function="Reception and throne hall", confidence="documented",
         sourceIds=["wiki-persepolis", "wiki-achaemenid-architecture", "schmidt-persepolis"], activity=dict(figures=40, radius=80)),

    dict(id="unfinished-gate", name="Unfinished Gate", category="monument",
         latlon=L(62, 165), rotation=0, footprint=(30, 30), scale=1.0, model="persepolis/unfinished-gate",
         activePeriods=LATER,
         variants={
             "xerxes-460": dict(note="A walled forecourt north of the Hall of a Hundred Columns; the gate on this spot was begun only in the last decades of the empire."),
             "burned-330": dict(note="Abandoned when Alexander came: column drums and roughed-out blocks for the bulls lie where the masons left them."),
             "sasanian-250": dict(note="The unfinished blocks still lie in the court, a lesson in how the stone was worked."),
         },
         summary="A gatehouse on the court before the Hall of a Hundred Columns, begun late in the Achaemenid period and left unfinished in 330 BCE, with its column drums and rough bull blocks still lying about.",
         details=["It was to repeat the Gate of All Nations: a square hall with four columns and doorways guarded by bulls. Work had reached the walls and door jambs when it stopped; the half-cut stones show how the Persian masons worked, roughing out with a point and finishing with claw chisels and abrasives.",
                  "The miniature shows the column bases with a few drums set up, the jambs and wall footings, rough bull blocks and loose drums on the ground. The date of the start (Artaxerxes III or Darius III) is not certain."],
         built="c. 340–330 BCE (unfinished)", function="Gateway, never completed", confidence="documented",
         sourceIds=["wiki-persepolis", "schmidt-persepolis", "roaf-1983"], activity=dict(figures=8, radius=30)),

    dict(id="tachara", name="Tachara (Palace of Darius)", category="civic",
         latlon=L(-72, -26), rotation=0, footprint=(32, 44), scale=1.0, model="persepolis/tachara",
         activePeriods=ALL,
         variants={
             "darius-500": dict(note="Darius' own palace, newly finished or nearly so, its doorways and windows framed in polished dark stone; Xerxes will complete its decoration."),
             "xerxes-460": dict(note="Finished, with inscriptions of Darius and Xerxes; it was used for the king's private receptions and banquets, perhaps."),
             "burned-330": dict(model="persepolis/tachara-ruin", note="The roof and walls are gone; the stone door and window frames stand alone, still polished like mirrors.", confidence="reconstruction"),
             "sasanian-250": dict(model="persepolis/tachara-ruin", note="Sasanian princes picnic in the roofless hall; around 311 CE Shapur Sakanshah, governor of Sakastan, has his visit cut on a door jamb in Middle Persian.", confidence="reconstruction"),
         },
         summary="Darius' private palace on the west edge of the terrace, a small hall of twelve columns behind a portico, with stone doors and windows so polished it was later called the Hall of Mirrors.",
         details=["Its Old Persian name taçara appears in Darius' inscription on the building. A south portico of eight columns led through stone doorways into a hall of twelve columns, with small rooms round it; reliefs show servants carrying food and the king walking under a parasol. Artaxerxes III added a western stair.",
                  "The miniature shows the low terrace with its relief-carved stair, the portico, the mud-brick walls with dark stone door and window frames under cavetto cornices, and the flat roof. In the ruin only the stone frames stand, as they do today. The roof and parapet are reconstructed."],
         built="c. 510–480 BCE", function="Palace of Darius I", confidence="documented",
         sourceIds=["wiki-tachara", "schmidt-persepolis", "mousavi-persepolis"], activity=dict(figures=16, radius=40)),

    dict(id="tripylon", name="Tripylon (Council Hall)", category="civic",
         latlon=L(24, -10), rotation=180, footprint=(26, 26), scale=1.0, model="persepolis/tripylon",
         activePeriods=FROM_XERXES,
         variants={
             "darius-500": dict(note="Open court between the Apadana and the future hall; the small central building may have been begun at the end of Darius' reign."),
             "xerxes-460": dict(note="A small hall of four columns with three doorways, at the hinge of the terrace between the public halls and the palaces."),
             "burned-330": dict(model="persepolis/tripylon-ruin", note="Burned; the carved door jambs and the north stair survive.", confidence="reconstruction"),
             "sasanian-250": dict(model="persepolis/tripylon-ruin", note="Door jambs with the enthroned king stand over the rubble.", confidence="reconstruction"),
         },
         summary="A small central hall with three doorways (hence 'Tripylon'), perhaps a council chamber, joining the audience halls to the palaces; its stair is carved with Persian and Median nobles.",
         details=["Built late in Darius' reign or under Xerxes and perhaps finished by Artaxerxes I. Its door jambs show the king on a throne carried by the peoples of the empire, the crown prince behind him; the stair (now in the National Museum in Tehran) shows nobles climbing as if to a banquet. Its function, council hall or guard post, is a guess.",
                  "The miniature shows the square hall with four columns, its three doorways, the north stair with relief bands, and the flat roof with a stepped parapet. Dimensions are approximate."],
         built="c. 490–460 BCE", function="Central hall, perhaps a council chamber", confidence="reconstruction",
         sourceIds=["wiki-persepolis", "schmidt-persepolis", "roaf-1983"], activity=dict(figures=10, radius=30)),

    dict(id="hadish", name="Hadish (Palace of Xerxes)", category="civic",
         latlon=L(-30, -92), rotation=180, footprint=(42, 58), scale=1.0, model="persepolis/hadish",
         activePeriods=FROM_XERXES,
         variants={
             "darius-500": dict(note="The highest part of the rock, still unbuilt. Xerxes will put his palace here."),
             "xerxes-460": dict(note="Xerxes' palace, twice the size of his father's: a hall of 36 columns behind a north portico, reached by double stairs."),
             "burned-330": dict(model="persepolis/hadish-ruin", note="The most heavily burned building on the terrace; some ancient writers say the fire was set in Xerxes' palace, in revenge for his burning of Athens.", confidence="reconstruction"),
             "sasanian-250": dict(model="persepolis/hadish-ruin", note="Ash-filled ruin with its door frames and column bases.", confidence="reconstruction"),
         },
         summary="Xerxes' palace on the highest level of the terrace, a hall of 36 columns with a north portico, called hadish ('seat, residence') in its inscription.",
         details=["Built about 480 BCE. Its stairs and doorways show servants bringing kids, wineskins and covered dishes, and Xerxes with parasol bearers. Excavators found its floor thick with ash and charred cedar: it burned more fiercely than any other building, perhaps because the fire was set here.",
                  "The miniature shows the raised platform with double stairs, the north portico, the square hall with 36 columns, stone door frames with cavetto cornices and the flat roof. The ruin keeps door frames and bases. Heights are reconstructed."],
         built="c. 486–465 BCE", function="Palace of Xerxes", confidence="documented",
         sourceIds=["wiki-persepolis", "wiki-xerxes", "schmidt-persepolis"], activity=dict(figures=14, radius=40)),

    dict(id="harem", name="Harem of Xerxes", category="civic",
         latlon=L(32, -95), rotation=180, footprint=(56, 90), scale=1.0, model="persepolis/harem",
         activePeriods=FROM_XERXES,
         variants={
             "darius-500": dict(note="Building ground south of the future Tripylon; the first part of this block may already be going up."),
             "xerxes-460": dict(note="An L-shaped block of a columned hall and rows of small apartments, perhaps for the women of the court; the name is the excavators' guess."),
             "burned-330": dict(model="persepolis/harem-ruin", note="Burned and abandoned; its walls slump into mounds.", confidence="reconstruction"),
             "sasanian-250": dict(model="persepolis/harem-ruin", note="Low mounds and door frames. In the 1930s excavators will rebuild part of it as their house; it is now the site museum.", confidence="reconstruction"),
         },
         summary="An L-shaped palace block south of the Tripylon, a main hall of twelve columns and rows of small suites, which its excavators called the harem of Xerxes.",
         details=["Built by Xerxes, perhaps begun under Darius. The main hall with a portico opens onto a court; behind it and along the west wing lie some 22 apartments of a small columned room and side chambers. That women lived here is an inference from the plan, not from texts.",
                  "The miniature shows the main hall with its portico and stone door frames, the wing of suites with flat roofs and small courts, and the mud-brick parapet. The layout is simplified."],
         built="c. 486–470 BCE", function="Palace wing, probably residential", confidence="reconstruction",
         sourceIds=["wiki-persepolis", "schmidt-persepolis", "mousavi-persepolis"], activity=dict(figures=10, radius=40)),

    dict(id="treasury", name="Treasury", category="commercial",
         latlon=L(104, -128), rotation=0, footprint=(76, 130), scale=1.0, model="persepolis/treasury",
         activePeriods=ALL,
         variants={
             "darius-500": dict(note="Built in the first years of the terrace and already being enlarged: a mud-brick block of storerooms and columned halls."),
             "xerxes-460": dict(note="Full of the empire's silver, gifts and booty; its clerks issue silver payments to workers, recorded on the Treasury Tablets until 458."),
             "burned-330": dict(model="persepolis/treasury-ruin", note="Emptied by Alexander, who carried off the silver on thousands of mules and camels, then burned.", confidence="reconstruction"),
             "sasanian-250": dict(model="persepolis/treasury-ruin", note="A low field of mud-brick mounds against the mountain.", confidence="reconstruction"),
         },
         summary="The royal treasury in the south-east corner of the terrace, a mud-brick block of storerooms and halls with forests of painted wooden columns, emptied by Alexander in 330 BCE.",
         details=["Built by Darius and enlarged twice, it measured about 130 by 78 m behind walls up to 3 m thick, with halls of 99 and 100 wooden columns on stone bases, plastered and painted. Here excavators found the two great audience reliefs, stone vessels, weapons and the Elamite Treasury Tablets of 492–458 BCE. Ancient writers say Alexander found 120,000 talents of silver.",
                  "The miniature shows the thick mud-brick walls, the courts and roofed halls with wooden columns, and the plain parapet. The internal plan is simplified."],
         built="c. 510–480 BCE", function="Treasury and storehouse", confidence="documented",
         sourceIds=["wiki-persepolis", "wiki-pfa", "schmidt-persepolis", "diodorus-17"], activity=dict(figures=20, radius=60)),

    dict(id="garrison", name="Garrison quarters", category="military",
         latlon=L(128, 130), rotation=0, footprint=(40, 120), scale=1.0, model="persepolis/garrison",
         activePeriods=FROM_XERXES,
         variants={
             "darius-500": dict(note="The north-east corner of the terrace, against the fortification; buildings here are only beginning."),
             "xerxes-460": dict(note="Barracks of mud brick between the Hall of a Hundred Columns and the mountain wall, for the guards of the terrace."),
             "burned-330": dict(model="persepolis/garrison-ruin", note="Abandoned and burned, the rooms filled with fallen brick.", confidence="reconstruction"),
             "sasanian-250": dict(model="persepolis/garrison-ruin", note="Long mounds by the mountain.", confidence="reconstruction"),
         },
         summary="Rows of mud-brick rooms in the north-east corner of the terrace, which the excavators took for the barracks of the royal guard.",
         details=["A plain block of corridors and rooms against the fortification wall. Arrowheads and weapons were found here and in the treasury. The guard that the Greeks called the Immortals, 10,000 men, cannot all have lodged on the terrace; most soldiers lived in the plain.",
                  "The miniature shows long ranges of rooms round narrow courts, flat roofs and a towered wall on the mountain side. The plan is simplified and the identification uncertain."],
         built="c. 490–460 BCE", function="Guard quarters (probably)", confidence="reconstruction",
         sourceIds=["wiki-persepolis", "schmidt-persepolis"], activity=dict(figures=16, radius=50)),

    # ------------------------------------------------------------ the royal tombs
    dict(id="tomb-artaxerxes-ii", name="Tomb of Artaxerxes II", category="monument",
         latlon=L(245, 95), rotation=90, footprint=(44, 30), scale=1.0, model="persepolis/royal-tomb",
         activePeriods=LATER,
         variants={
             "xerxes-460": dict(note="Bare mountain. The kings are still buried at Naqsh-e Rustam, 6 km north; this tomb will be cut about a century later."),
             "burned-330": dict(note="Cut for Artaxerxes II (died 358 BCE), the first king buried above the terrace; the tomb chambers have been opened and robbed."),
             "sasanian-250": dict(note="An empty tomb in the cliff, its relief of the king before the fire altar still clear."),
         },
         summary="A rock-cut royal tomb in the mountain above the Hall of a Hundred Columns, usually attributed to Artaxerxes II, with the cross-shaped façade of the Achaemenid kings' tombs.",
         details=["Like the tombs at Naqsh-e Rustam, the face is a cross: a plain lower arm, a palace front with four engaged columns with double-bull capitals and a central door, and above it two tiers of throne-bearers representing the subject peoples lifting a dais where the king stands before a fire altar under the winged figure of Ahuramazda.",
                  "The miniature shows the cliff with the cut façade, the palace front with columns and dark door, and the relief register above. The attribution to Artaxerxes II rather than another late king is conventional."],
         built="c. 358 BCE", function="Royal tomb", confidence="documented",
         sourceIds=["wiki-persepolis", "wiki-artaxerxes-ii", "wiki-naqsh-e-rostam", "schmidt-persepolis"], activity=dict(figures=4, radius=30)),

    dict(id="tomb-artaxerxes-iii", name="Tomb of Artaxerxes III", category="monument",
         latlon=L(238, -120), rotation=90, footprint=(44, 30), scale=1.0, model="persepolis/royal-tomb",
         activePeriods=LATER,
         variants={
             "xerxes-460": dict(note="Bare mountain above the treasury."),
             "burned-330": dict(note="Cut for Artaxerxes III, poisoned in 338 BCE; eight years later Alexander's army is camped below."),
             "sasanian-250": dict(note="An empty tomb in the cliff above the ruins."),
         },
         summary="The southern rock-cut tomb above the terrace, usually attributed to Artaxerxes III (died 338 BCE), with the same cross-shaped palace façade and relief of the king before the fire altar.",
         details=["Its façade copies Darius' tomb at Naqsh-e Rustam: engaged columns with bull capitals framing a door into a vaulted chamber with burial cists cut in the rock. A third, unfinished tomb farther south is sometimes given to Darius III, who died in flight in 330 and was buried, Arrian says, by Alexander's order in the royal tombs.",
                  "The miniature uses the same model as the northern tomb. The attribution is conventional."],
         built="c. 338 BCE", function="Royal tomb", confidence="documented",
         sourceIds=["wiki-persepolis", "wiki-artaxerxes-iii", "schmidt-persepolis"], activity=dict(figures=4, radius=30)),

    # ------------------------------------------------------------ the plain
    dict(id="plain-palace", name="Pavilion palace in the paradise", category="civic",
         latlon=L(-350, -420), rotation=0, footprint=(100, 100), scale=1.0, model="persepolis/plain-palace",
         activePeriods=["darius-500", "xerxes-460", "burned-330"],
         variants={
             "darius-500": dict(note="A columned pavilion in a walled garden of trees and stone water channels below the terrace, of the kind built at Pasargadae."),
             "xerxes-460": dict(note="Pavilions and porches in the paradise, used by the court and high officials; the tablets speak of paradises (partetaš) in Fars."),
             "burned-330": dict(model="persepolis/plain-palace-ruin", note="Probably burned or abandoned with the court; the channels silt up and the trees are cut.", confidence="interpretation"),
             "sasanian-250": dict(note="Orchards and fields over the buried column bases."),
         },
         summary="A columned pavilion palace in a walled paradise garden on the plain below the terrace: a reconstruction based on buildings excavated in the lower town and on Cyrus' garden palaces at Pasargadae.",
         details=["Surveys and soundings in the plain have found column bases, stone door frames and mud-brick buildings below and to the south and west of the terrace, some of them palaces. The Persian paradise (pairidaeza, Elamite partetaš) was a walled park of trees and flowers watered by channels, often with a pavilion; the tablets record workers and rations at several in Fars.",
                  "The miniature shows a hall with porticoes on stone bases, stone-lined channels dividing beds of trees, and the garden wall. Its form, size and position are an interpretation, not a plan of one excavated building."],
         built="c. 500 BCE", function="Garden palace and pavilion", confidence="interpretation",
         sourceIds=["wiki-persian-garden", "wiki-pasargadae", "tilia-1972", "briant"], activity=dict(figures=14, radius=60)),
]
