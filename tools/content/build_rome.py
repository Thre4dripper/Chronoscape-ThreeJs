"""
Assemble content/cities/rome/city.json from the writers' data modules plus the
geography defined here. Positions are given as (lat, lon) and projected onto the
local map grid (metres, origin top-left, y down).

    python3 tools/content/build_rome.py
"""
import json, os, sys, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, "rome"))

import landmarks_a, landmarks_b, life_spots, life_events  # noqa: E402
for m in (landmarks_a, landmarks_b, life_spots, life_events):
    importlib.reload(m)

# ---------------------------------------------------------------- projection
LON0, LAT0 = 12.447, 41.918          # top-left corner
KX, KY = 82790.0, 111200.0           # metres per degree at Rome's latitude
SIZE = [6050, 5450]

def P(latlon):
    lat, lon = latlon
    return [round((lon - LON0) * KX), round((LAT0 - lat) * KY)]

def path(*pts):
    return [P(p) for p in pts]

ALL = ["kingdom-600bce", "republic-200bce", "republic-50bce", "empire-100ce", "empire-215ce", "late-400ce", "medieval-1300", "renaissance-1560"]
ANC = ["republic-200bce", "republic-50bce", "empire-100ce", "empire-215ce", "late-400ce"]
REG_ANC = ["kingdom-600bce"] + ANC
IMP = ["empire-100ce", "empire-215ce", "late-400ce"]
LATE_ON = ["late-400ce", "medieval-1300", "renaissance-1560"]
LATER = ["medieval-1300", "renaissance-1560"]
SERVIAN = ["republic-200bce", "republic-50bce", "empire-100ce", "empire-215ce"]

# ---------------------------------------------------------------- geography
TIBER = path((41.9180, 12.4745), (41.9120, 12.4745), (41.9080, 12.4735), (41.9050, 12.4715), (41.9030, 12.4690), (41.9015, 12.4660),
             (41.8995, 12.4645), (41.8975, 12.4650), (41.8955, 12.4665), (41.8935, 12.4690), (41.8920, 12.4715), (41.8912, 12.4745),
             (41.8908, 12.4775), (41.8895, 12.4795), (41.8875, 12.4790), (41.8850, 12.4780), (41.8820, 12.4760), (41.8790, 12.4745),
             (41.8750, 12.4735), (41.8700, 12.4740))

blurbs = {x["id"]: x.get("blurb", "") for x in life_events.ROADS + life_events.HILLS + life_events.WATER}
descs = {d["id"]: d for d in life_events.DISTRICTS}

def road(id, name, periods, pts, width=10, style="major", labelled=False):
    return dict(id=id, name=name, path=path(*pts), width=width, style=style, labelled=labelled, periods=periods, blurb=blurbs.get(id, ""))

ROADS = [
    road("via-sacra", "Via Sacra", ALL, [(41.8927, 12.4838), (41.8922, 12.4858), (41.8915, 12.4878), (41.8908, 12.4887), (41.8903, 12.4905), (41.8902, 12.4915)], 10, "major", True),
    road("clivus-capitolinus", "Clivus Capitolinus", REG_ANC, [(41.8925, 12.4840), (41.8928, 12.4830), (41.8930, 12.4822)], 8, "minor"),
    road("argiletum", "Argiletum", REG_ANC, [(41.8933, 12.4858), (41.8945, 12.4880), (41.8955, 12.4895), (41.8965, 12.4915)], 9, "major", True),
    road("vicus-tuscus", "Vicus Tuscus", REG_ANC, [(41.8921, 12.4850), (41.8910, 12.4845), (41.8900, 12.4835), (41.8893, 12.4820)], 7, "minor"),
    road("vicus-jugarius", "Vicus Jugarius", REG_ANC, [(41.8924, 12.4838), (41.8915, 12.4825), (41.8905, 12.4815)], 7, "minor"),
    road("via-lata", "Via Lata", ANC, [(41.8958, 12.4822), (41.8980, 12.4812), (41.9010, 12.4800), (41.9040, 12.4790), (41.9080, 12.4775), (41.9113, 12.4762)], 12, "major", True),
    road("corso", "Via del Corso", LATER, [(41.8958, 12.4822), (41.8980, 12.4812), (41.9010, 12.4800), (41.9040, 12.4790), (41.9080, 12.4775), (41.9113, 12.4762)], 12, "major", True),
    road("via-flaminia", "Via Flaminia", ANC + LATER, [(41.9113, 12.4762), (41.9180, 12.4755)], 12, "major"),
    road("via-appia", "Via Appia", ANC + LATER, [(41.8855, 12.4900), (41.8820, 12.4930), (41.8790, 12.4960), (41.8760, 12.4990), (41.8731, 12.5014), (41.8690, 12.5050)], 11, "major", True),
    road("via-ostiensis", "Via Ostiensis", ANC + LATER, [(41.8860, 12.4800), (41.8820, 12.4800), (41.8768, 12.4812), (41.8700, 12.4830)], 10, "major", True),
    road("via-tiburtina", "Via Tiburtina", ANC + LATER, [(41.8955, 12.5035), (41.8975, 12.5080), (41.8990, 12.5125), (41.9010, 12.5190)], 9, "minor"),
    road("via-labicana", "Via Labicana", ANC + LATER, [(41.8903, 12.4915), (41.8905, 12.4990), (41.8910, 12.5080), (41.8915, 12.5152), (41.8910, 12.5200)], 10, "major", True),
    road("via-nomentana", "Via Nomentana", ANC + LATER, [(41.9035, 12.4960), (41.9070, 12.5000), (41.9093, 12.5020), (41.9130, 12.5060)], 9, "minor"),
    road("via-salaria", "Via Salaria", ALL, [(41.9035, 12.4960), (41.9070, 12.4965), (41.9098, 12.4968), (41.9150, 12.4980)], 9, "minor"),
    road("via-aurelia", "Via Aurelia", ANC + LATER, [(41.8897, 12.4793), (41.8905, 12.4740), (41.8915, 12.4690), (41.8925, 12.4635), (41.8935, 12.4580)], 9, "minor"),
    road("via-triumphalis", "Via Triumphalis", ANC, [(41.8902, 12.4915), (41.8880, 12.4905), (41.8865, 12.4900), (41.8855, 12.4900)], 8, "minor"),
    road("alta-semita", "Alta Semita", REG_ANC, [(41.8960, 12.4850), (41.8990, 12.4880), (41.9020, 12.4920), (41.9035, 12.4960)], 8, "minor"),
    road("clivus-palatinus", "Clivus Palatinus", REG_ANC, [(41.8908, 12.4887), (41.8898, 12.4878), (41.8890, 12.4870)], 6, "minor"),
    road("via-papalis", "Via Papalis", LATER, [(41.9018, 12.4668), (41.9005, 12.4685), (41.8985, 12.4705), (41.8970, 12.4730), (41.8958, 12.4760), (41.8945, 12.4790), (41.8938, 12.4820), (41.8925, 12.4860), (41.8905, 12.4905), (41.8880, 12.4960), (41.8859, 12.5057)], 9, "major", True),
    road("via-giulia-road", "Via Giulia", ["renaissance-1560"], [(41.9000, 12.4662), (41.8960, 12.4683), (41.8925, 12.4703)], 9, "major", True),
    road("via-del-pellegrino", "Via del Pellegrino", LATER, [(41.8985, 12.4690), (41.8968, 12.4706), (41.8956, 12.4722)], 6, "minor"),
    road("via-dei-banchi", "Via dei Banchi", ["renaissance-1560"], [(41.9018, 12.4668), (41.9005, 12.4682), (41.8995, 12.4698)], 6, "minor"),
    road("via-recta", "Via Recta", LATER, [(41.9018, 12.4672), (41.9015, 12.4706), (41.9010, 12.4740), (41.9008, 12.4770)], 6, "minor"),
    road("lungaretta", "Via della Lungaretta", LATER, [(41.8897, 12.4790), (41.8894, 12.4740), (41.8894, 12.4697)], 6, "minor"),
    road("borgo-street", "Borgo Vecchio", LATER, [(41.9018, 12.4660), (41.9020, 12.4600), (41.9022, 12.4560)], 7, "minor"),
    road("via-latina", "Via Latina", ANC + LATER, [(41.8855, 12.4900), (41.8820, 12.4950), (41.8775, 12.5000), (41.8740, 12.5060)], 8, "minor"),
]

HILLS = [
    ("capitoline", "Capitoline", (41.8933, 12.4825), 150), ("palatine", "Palatine", (41.8890, 12.4868), 250), ("aventine-hill", "Aventine", (41.8835, 12.4815), 300),
    ("caelian-hill", "Caelian", (41.8865, 12.4960), 320), ("esquiline-hill", "Esquiline", (41.8950, 12.5010), 420), ("viminal", "Viminal", (41.9000, 12.4950), 220),
    ("quirinal", "Quirinal", (41.9000, 12.4880), 280), ("janiculum", "Janiculum", (41.8900, 12.4620), 350), ("pincian", "Pincian", (41.9100, 12.4820), 300),
    ("vatican-hill", "Vatican Hill", (41.9040, 12.4520), 250),
]
hills = [dict(id=i, name=n, center=P(c), radius=r, label=True, blurb=blurbs.get(i, "")) for i, n, c, r in HILLS]
hills.append(dict(id="testaccio-hill", name="Monte Testaccio", center=P((41.8760, 12.4752)), radius=90, label=True, blurb=blurbs.get("testaccio-hill", ""), periods=IMP + LATER))

SERVIAN_PATH = [(41.8935, 12.4805), (41.8960, 12.4810), (41.8990, 12.4840), (41.9020, 12.4900), (41.9035, 12.4960), (41.9000, 12.5030), (41.8945, 12.5040), (41.8905, 12.5015),
                (41.8870, 12.5000), (41.8845, 12.4930), (41.8830, 12.4900), (41.8810, 12.4860), (41.8790, 12.4800), (41.8810, 12.4765), (41.8850, 12.4775), (41.8880, 12.4785), (41.8905, 12.4800)]
AUREL_E = [(41.9113, 12.4762), (41.9125, 12.4800), (41.9115, 12.4850), (41.9105, 12.4910), (41.9098, 12.4968), (41.9080, 12.5030), (41.9075, 12.5090), (41.9040, 12.5110), (41.8990, 12.5125),
           (41.8950, 12.5140), (41.8915, 12.5152), (41.8880, 12.5160), (41.8860, 12.5120), (41.8840, 12.5080), (41.8805, 12.5000), (41.8775, 12.5000), (41.8731, 12.5014), (41.8720, 12.4950),
           (41.8735, 12.4890), (41.8745, 12.4840), (41.8768, 12.4812), (41.8760, 12.4760), (41.8755, 12.4740)]
AUREL_W = [(41.8765, 12.4725), (41.8800, 12.4690), (41.8850, 12.4650), (41.8890, 12.4615), (41.8925, 12.4635), (41.8960, 12.4650), (41.8990, 12.4645), (41.9000, 12.4650)]
LEONINE = [(41.9000, 12.4652), (41.9040, 12.4600), (41.9060, 12.4540), (41.9040, 12.4500), (41.9000, 12.4520), (41.8990, 12.4600), (41.9005, 12.4650)]

walls = [
    dict(id="agger", name="Agger (earth rampart)", path=path(*SERVIAN_PATH[5:8]), closed=False, periods=["kingdom-600bce"]),
    dict(id="servian-wall", name="Servian Wall", path=path(*SERVIAN_PATH), closed=True, periods=SERVIAN),
    dict(id="aurelian-wall", name="Aurelian Wall", path=path(*AUREL_E), closed=False, periods=LATE_ON),
    dict(id="aurelian-wall-trastevere", name="Aurelian Wall (Trastevere)", path=path(*AUREL_W), closed=False, periods=LATE_ON),
    dict(id="leonine-wall", name="Leonine Wall", path=path(*LEONINE), closed=False, periods=LATER),
]

gates = [
    dict(id="porta-flaminia", name="Porta Flaminia", position=P((41.9113, 12.4762)), periods=LATE_ON),
    dict(id="porta-salaria", name="Porta Salaria", position=P((41.9098, 12.4968)), periods=LATE_ON),
    dict(id="porta-tiburtina", name="Porta Tiburtina", position=P((41.8990, 12.5125)), periods=LATE_ON),
    dict(id="porta-asinaria", name="Porta Asinaria", position=P((41.8840, 12.5080)), periods=LATE_ON),
    dict(id="porta-metronia", name="Porta Metronia", position=P((41.8805, 12.5000)), periods=LATE_ON),
    dict(id="porta-latina", name="Porta Latina", position=P((41.8775, 12.5000)), periods=LATE_ON),
    dict(id="porta-ostiensis", name="Porta Ostiensis", position=P((41.8768, 12.4812)), periods=LATE_ON),
    dict(id="porta-portuensis", name="Porta Portuensis", position=P((41.8800, 12.4690)), periods=LATE_ON),
    dict(id="porta-aurelia", name="Porta Aurelia", position=P((41.8925, 12.4635)), periods=LATE_ON),
    dict(id="porta-capena", name="Porta Capena", position=P((41.8855, 12.4900)), periods=SERVIAN),
    dict(id="porta-esquilina", name="Porta Esquilina", position=P((41.8955, 12.5035)), periods=SERVIAN),
    dict(id="porta-collina", name="Porta Collina", position=P((41.9035, 12.4960)), periods=SERVIAN),
    dict(id="porta-carmentalis", name="Porta Carmentalis", position=P((41.8920, 12.4805)), periods=SERVIAN),
]

bridges = [
    dict(id="pons-sublicius", name="Pons Sublicius", path=path((41.8882, 12.4770), (41.8878, 12.4797)), periods=REG_ANC, build="timber", arches=6,
         blurb="Rome's oldest bridge, a timber deck on wooden piles, built by tradition under King Ancus Marcius. Religious rule kept iron out of it; the priests who maintained it, the pontifices, took their name from bridge-making. Horatius Cocles held it against the Etruscans while it was cut down behind him."),
    dict(id="pons-aemilius-bridge", name="Pons Aemilius", path=path((41.8899, 12.4780), (41.8896, 12.4806)), periods=ANC + LATER, arches=6, landmarkId="pons-aemilius",
         blurb="Rome's first stone bridge: piers of 179 BCE, arches finished in 142 BCE. It carried traffic from the cattle market to Trastevere for seventeen centuries; floods broke it in 1598 and one arch, the Ponte Rotto, still stands in the river."),
    dict(id="pons-fabricius-bridge", name="Pons Fabricius", path=path((41.8915, 12.4775), (41.8910, 12.4790)), periods=["republic-50bce"] + IMP + LATER, arches=2, landmarkId="pons-fabricius",
         blurb="Two broad arches from the Campus Martius to the Tiber Island, built in 62 BCE by Lucius Fabricius, curator of roads, whose name is still cut on it. It is the oldest Roman bridge in Rome still in use as built."),
    dict(id="pons-cestius", name="Pons Cestius", path=path((41.8908, 12.4762), (41.8905, 12.4776)), periods=["republic-50bce"] + IMP + LATER, arches=3,
         blurb="The bridge from the Tiber Island to Trastevere, built in the 1st century BCE and rebuilt in 370 CE by the emperors Valentinian, Valens and Gratian with stone from the Theatre of Marcellus. A single main arch with two small flood arches."),
    dict(id="pons-aelius-bridge", name="Pons Aelius", path=path((41.9030, 12.4668), (41.9014, 12.4668)), periods=["empire-215ce"] + LATE_ON, arches=3, landmarkId="ponte-sant-angelo",
         blurb="Hadrian's bridge of 134 CE, leading straight to the gate of his mausoleum. Pilgrims later crossed it to St Peter's; in the Jubilee crush of 1450 its parapets gave way and nearly two hundred people died."),
    dict(id="pons-neronianus", name="Pons Neronianus", path=path((41.8998, 12.4640), (41.8992, 12.4660)), periods=["empire-100ce", "empire-215ce"], arches=4,
         blurb="A bridge to the imperial gardens and Nero's circus on the Vatican plain, probably built by Caligula or Nero. It was already in ruins by late antiquity; low piers still show in the river when the water is low."),
    dict(id="pons-agrippae", name="Pons Agrippae", path=path((41.8926, 12.4697), (41.8921, 12.4716)), periods=["empire-100ce", "empire-215ce", "late-400ce"], arches=5, landmarkId="ponte-sisto",
         blurb="A crossing from the Campus Martius to Trastevere, attributed to Agrippa and known from an inscription; its piers were found in the riverbed in 1887. A later bridge near here, the Pons Aurelius, was rebuilt as the Ponte Sisto."),
    dict(id="ponte-sisto-bridge", name="Ponte Sisto", path=path((41.8926, 12.4697), (41.8921, 12.4716)), periods=["renaissance-1560"], arches=4, landmarkId="ponte-sisto",
         blurb="Built for Pope Sixtus IV in 1473 to 1479 on the ruined piers of the ancient Pons Aurelius: the first new bridge over the Tiber since antiquity, with a round oculus in the central pier to let flood water through."),
]

aqueducts = [
    dict(name="Aqua Claudia / Anio Novus", path=path((41.8915, 12.5152), (41.8890, 12.5100), (41.8870, 12.5040), (41.8865, 12.4990), (41.8880, 12.4930), (41.8890, 12.4890)), periods=IMP + LATER),
    dict(name="Aqua Marcia", path=path((41.8930, 12.5170), (41.8955, 12.5035), (41.8990, 12.4960), (41.9000, 12.4880), (41.8940, 12.4825)), periods=["republic-50bce"] + IMP),
    dict(name="Aqua Virgo", path=path((41.9080, 12.4950), (41.9040, 12.4880), (41.9009, 12.4833), (41.8985, 12.4780)), periods=IMP + LATER),
    dict(name="Aqua Appia", path=path((41.8870, 12.5050), (41.8855, 12.4900), (41.8830, 12.4830)), periods=ANC),
]

def poly(*pts):
    return [P(p) for p in pts]

REP = ["republic-200bce", "republic-50bce"]
blocks = [
    # Regal Rome: villages of huts on the hills
    dict(name="Palatine village", polygon=poly((41.8902, 12.4848), (41.8902, 12.4888), (41.8878, 12.4893), (41.8874, 12.4850)), density="loose", periods=["kingdom-600bce"]),
    dict(name="Quirinal hamlet", polygon=poly((41.8998, 12.4865), (41.9010, 12.4905), (41.8990, 12.4915), (41.8982, 12.4878)), density="loose", periods=["kingdom-600bce"]),
    dict(name="Esquiline hamlet", polygon=poly((41.8955, 12.4950), (41.8965, 12.4990), (41.8945, 12.5000), (41.8938, 12.4960)), density="loose", periods=["kingdom-600bce"]),
    dict(name="Velabrum settlement", polygon=poly((41.8920, 12.4838), (41.8925, 12.4858), (41.8908, 12.4862), (41.8905, 12.4842)), density="loose", periods=["kingdom-600bce"]),
    # Republic
    dict(name="Subura", polygon=poly((41.8935, 12.4880), (41.8975, 12.4885), (41.8995, 12.4960), (41.8950, 12.4985), (41.8925, 12.4925)), density="dense", periods=REP),
    dict(name="Velabrum", polygon=poly((41.8922, 12.4812), (41.8922, 12.4852), (41.8890, 12.4848), (41.8885, 12.4808)), density="dense", periods=REP),
    dict(name="Palatine houses", polygon=poly((41.8905, 12.4842), (41.8905, 12.4895), (41.8872, 12.4898), (41.8870, 12.4845)), density="loose", periods=REP),
    dict(name="Aventine", polygon=poly((41.8862, 12.4795), (41.8860, 12.4865), (41.8812, 12.4875), (41.8798, 12.4800)), density="loose" , periods=["republic-200bce"]),
    dict(name="Aventine", polygon=poly((41.8862, 12.4795), (41.8860, 12.4865), (41.8812, 12.4875), (41.8798, 12.4800)), density="dense", periods=["republic-50bce"]),
    dict(name="Quirinal", polygon=poly((41.8965, 12.4840), (41.9035, 12.4890), (41.9035, 12.4950), (41.8985, 12.4945), (41.8960, 12.4880)), density="loose", periods=["republic-200bce"]),
    dict(name="Quirinal", polygon=poly((41.8965, 12.4840), (41.9035, 12.4890), (41.9035, 12.4950), (41.8985, 12.4945), (41.8960, 12.4880)), density="dense", periods=["republic-50bce"]),
    dict(name="Esquiline", polygon=poly((41.8925, 12.4925), (41.8990, 12.4955), (41.8995, 12.5030), (41.8935, 12.5030)), density="loose", periods=REP),
    dict(name="Caelian", polygon=poly((41.8895, 12.4925), (41.8900, 12.5000), (41.8850, 12.5010), (41.8848, 12.4935)), density="loose", periods=REP),
    dict(name="Campus Martius", polygon=poly((41.8945, 12.4725), (41.9000, 12.4740), (41.9010, 12.4800), (41.8960, 12.4825), (41.8935, 12.4785)), density="loose", periods=["republic-50bce"]),
    dict(name="Trastevere", polygon=poly((41.8925, 12.4690), (41.8915, 12.4745), (41.8885, 12.4760), (41.8868, 12.4705)), density="loose", periods=REP),
    # Empire and late antiquity: a city of a million, built up inside the walls
    dict(name="Subura and Esquiline", polygon=poly((41.8930, 12.4878), (41.8980, 12.4885), (41.9005, 12.4980), (41.8990, 12.5090), (41.8925, 12.5100), (41.8905, 12.4950)), density="dense", periods=IMP),
    dict(name="Quirinal and Viminal", polygon=poly((41.8960, 12.4835), (41.9045, 12.4870), (41.9065, 12.4990), (41.9010, 12.5030), (41.8975, 12.4975), (41.8955, 12.4880)), density="dense", periods=IMP),
    dict(name="Campus Martius", polygon=poly((41.8935, 12.4705), (41.9000, 12.4700), (41.9060, 12.4735), (41.9090, 12.4790), (41.9030, 12.4830), (41.8960, 12.4830), (41.8935, 12.4790)), density="dense", periods=IMP),
    dict(name="Velabrum", polygon=poly((41.8922, 12.4812), (41.8922, 12.4852), (41.8890, 12.4848), (41.8885, 12.4808)), density="dense", periods=IMP),
    dict(name="Aventine", polygon=poly((41.8862, 12.4790), (41.8862, 12.4870), (41.8800, 12.4885), (41.8785, 12.4800)), density="dense", periods=IMP),
    dict(name="Caelian", polygon=poly((41.8900, 12.4925), (41.8905, 12.5070), (41.8840, 12.5090), (41.8825, 12.4935)), density="dense", periods=IMP),
    dict(name="Emporium warehouses", polygon=poly((41.8830, 12.4735), (41.8830, 12.4795), (41.8770, 12.4805), (41.8755, 12.4745)), density="dense", periods=IMP),
    dict(name="Trastevere", polygon=poly((41.8945, 12.4660), (41.8925, 12.4745), (41.8880, 12.4765), (41.8845, 12.4700), (41.8870, 12.4650)), density="dense", periods=IMP),
    dict(name="Porta Capena suburb", polygon=poly((41.8850, 12.4880), (41.8850, 12.4950), (41.8770, 12.5000), (41.8745, 12.4930)), density="dense", periods=IMP),
    dict(name="Pincian villas", polygon=poly((41.9070, 12.4760), (41.9120, 12.4790), (41.9115, 12.4860), (41.9065, 12.4850)), density="loose", periods=IMP),
    dict(name="Vatican suburb", polygon=poly((41.9045, 12.4560), (41.9045, 12.4640), (41.9000, 12.4650), (41.8995, 12.4570)), density="loose", periods=["late-400ce"]),
    # Medieval: the abitato in the river bend, the disabitato beyond
    dict(name="Abitato", polygon=poly((41.9035, 12.4690), (41.9060, 12.4760), (41.9010, 12.4815), (41.8955, 12.4835), (41.8925, 12.4800), (41.8918, 12.4740), (41.8945, 12.4690), (41.8992, 12.4660)), density="dense", periods=["medieval-1300"]),
    dict(name="Trastevere", polygon=poly((41.8925, 12.4688), (41.8912, 12.4760), (41.8878, 12.4762), (41.8870, 12.4700)), density="dense", periods=["medieval-1300"]),
    dict(name="Borgo", polygon=poly((41.9042, 12.4560), (41.9042, 12.4640), (41.9002, 12.4650), (41.9000, 12.4560)), density="loose", periods=["medieval-1300"]),
    dict(name="Monti", polygon=poly((41.8940, 12.4875), (41.8968, 12.4895), (41.8960, 12.4950), (41.8932, 12.4930)), density="loose", periods=["medieval-1300"]),
    dict(name="Lateran settlement", polygon=poly((41.8880, 12.5020), (41.8885, 12.5090), (41.8845, 12.5095), (41.8840, 12.5030)), density="loose", periods=["medieval-1300"]),
    # Renaissance: the abitato grows, Borgo fills, new streets in Monti
    dict(name="Abitato", polygon=poly((41.9045, 12.4685), (41.9075, 12.4770), (41.9020, 12.4830), (41.8955, 12.4845), (41.8920, 12.4805), (41.8912, 12.4740), (41.8940, 12.4685), (41.8992, 12.4655)), density="dense", periods=["renaissance-1560"]),
    dict(name="Tridente", polygon=poly((41.9075, 12.4770), (41.9112, 12.4765), (41.9100, 12.4820), (41.9060, 12.4820)), density="loose", periods=["renaissance-1560"]),
    dict(name="Trastevere", polygon=poly((41.8930, 12.4685), (41.8915, 12.4762), (41.8875, 12.4765), (41.8865, 12.4700)), density="dense", periods=["renaissance-1560"]),
    dict(name="Borgo", polygon=poly((41.9045, 12.4560), (41.9045, 12.4645), (41.9000, 12.4655), (41.8998, 12.4560)), density="dense", periods=["renaissance-1560"]),
    dict(name="Monti", polygon=poly((41.8940, 12.4875), (41.8975, 12.4895), (41.8970, 12.4960), (41.8935, 12.4935)), density="loose", periods=["renaissance-1560"]),
    dict(name="Via Pia", polygon=poly((41.9000, 12.4880), (41.9045, 12.4930), (41.9040, 12.4980), (41.9000, 12.4940)), density="loose", periods=["renaissance-1560"]),
]

gardens = [
    dict(name="Horti Sallustiani", polygon=poly((41.9060, 12.4900), (41.9100, 12.4930), (41.9090, 12.4980), (41.9050, 12.4960)), periods=IMP),
    dict(name="Horti Luculliani", polygon=poly((41.9080, 12.4800), (41.9110, 12.4830), (41.9095, 12.4870), (41.9065, 12.4840)), periods=IMP),
    dict(name="Horti Maecenatis", polygon=poly((41.8935, 12.4990), (41.8960, 12.5010), (41.8945, 12.5050), (41.8920, 12.5030)), periods=IMP),
    dict(name="Vineyards of the disabitato", kind="vineyard", polygon=poly((41.8940, 12.4870), (41.9020, 12.4900), (41.9020, 12.5100), (41.8850, 12.5080), (41.8800, 12.4900), (41.8860, 12.4830)), periods=LATER),
    dict(name="Vineyards on the Aventine", kind="vineyard", polygon=poly((41.8860, 12.4790), (41.8860, 12.4860), (41.8800, 12.4870), (41.8790, 12.4790)), periods=LATER),
]

marsh = [
    dict(name="Caprae Palus", polygon=poly((41.9000, 12.4740), (41.9010, 12.4790), (41.8980, 12.4800), (41.8970, 12.4760)), periods=["kingdom-600bce", "republic-200bce"]),
    dict(name="Velabrum marsh", polygon=poly((41.8915, 12.4815), (41.8918, 12.4845), (41.8898, 12.4848), (41.8895, 12.4815)), periods=["kingdom-600bce"]),
]

DISTRICT_GEO = {
    "subura": [(41.8935, 12.4885), (41.8975, 12.4890), (41.8990, 12.4960), (41.8950, 12.4975), (41.8925, 12.4925)],
    "campus-martius": [(41.8940, 12.4700), (41.9050, 12.4740), (41.9070, 12.4820), (41.8990, 12.4840), (41.8945, 12.4790)],
    "velabrum": [(41.8920, 12.4815), (41.8922, 12.4848), (41.8895, 12.4848), (41.8890, 12.4815)],
    "forum-boarium": [(41.8905, 12.4795), (41.8905, 12.4820), (41.8880, 12.4825), (41.8878, 12.4795)],
    "aventine": [(41.8860, 12.4790), (41.8860, 12.4870), (41.8805, 12.4880), (41.8795, 12.4790)],
    "trastevere": [(41.8940, 12.4660), (41.8925, 12.4745), (41.8865, 12.4765), (41.8850, 12.4660)],
    "esquiline": [(41.8925, 12.4940), (41.8990, 12.4960), (41.9000, 12.5080), (41.8920, 12.5070)],
    "caelian": [(41.8900, 12.4930), (41.8905, 12.5000), (41.8840, 12.5030), (41.8835, 12.4930)],
    "testaccio": [(41.8830, 12.4735), (41.8830, 12.4800), (41.8750, 12.4810), (41.8745, 12.4735)],
    "borgo": [(41.9055, 12.4520), (41.9055, 12.4640), (41.9000, 12.4650), (41.8995, 12.4520)],
    "abitato": [(41.9030, 12.4690), (41.9055, 12.4760), (41.9015, 12.4815), (41.8955, 12.4835), (41.8925, 12.4800), (41.8920, 12.4740), (41.8945, 12.4690), (41.8990, 12.4660)],
    "disabitato": [(41.8930, 12.4860), (41.9000, 12.4880), (41.9000, 12.5100), (41.8800, 12.5050), (41.8790, 12.4820), (41.8870, 12.4830)],
    "ghetto-district": [(41.8935, 12.4765), (41.8935, 12.4790), (41.8920, 12.4790), (41.8920, 12.4765)],
    "palatine-district": [(41.8905, 12.4840), (41.8905, 12.4895), (41.8870, 12.4895), (41.8870, 12.4840)],
    "capitoline-district": [(41.8945, 12.4810), (41.8945, 12.4840), (41.8920, 12.4840), (41.8920, 12.4810)],
}
districts = [dict(id=d["id"], name=d["name"], polygon=poly(*DISTRICT_GEO[d["id"]]), description=d.get("description", ""), periods=d["periods"]) for d in life_events.DISTRICTS]

labels = [
    dict(text="Tiberis", position=P((41.9000, 12.4635)), size="lg", rotation=-80, periods=REG_ANC),
    dict(text="Tevere", position=P((41.9000, 12.4635)), size="lg", rotation=-80, periods=LATER),
    dict(text="Campus Martius", position=P((41.9010, 12.4760)), size="md", periods=REG_ANC),
    dict(text="Campo Marzio", position=P((41.9010, 12.4760)), size="md", periods=LATER),
    dict(text="Subura", position=P((41.8962, 12.4925)), size="md", periods=ANC),
    dict(text="Trans Tiberim", position=P((41.8890, 12.4705)), size="md", periods=ANC),
    dict(text="Trastevere", position=P((41.8890, 12.4705)), size="md", periods=LATER),
    dict(text="Ager Vaticanus", position=P((41.9050, 12.4560)), size="sm", periods=REG_ANC),
    dict(text="Borgo", position=P((41.9030, 12.4580)), size="md", periods=LATER),
    dict(text="Emporium", position=P((41.8800, 12.4770)), size="sm", periods=ANC),
    dict(text="Campo Vaccino", position=P((41.8925, 12.4862)), size="sm", periods=LATER),
    dict(text="Disabitato", position=P((41.8850, 12.5000)), size="lg", periods=LATER),
    dict(text="Monti", position=P((41.8955, 12.4925)), size="sm", periods=["renaissance-1560"]),
    dict(text="Castra Praetoria", position=P((41.9055, 12.5075)), size="sm", periods=["late-400ce"]),
    dict(text="Velabrum", position=P((41.8905, 12.4830)), size="sm", periods=ANC),
    dict(text="Carinae", position=P((41.8922, 12.4920)), size="sm", periods=ANC),
]

MAP = dict(
    size=SIZE,
    resolution=4096,
    water=[dict(id="tiber", name="Tiber", path=TIBER, width=90, blurb=blurbs.get("tiber", ""))],
    islands=[dict(name="Tiber Island", polygon=poly((41.8919, 12.4772), (41.8915, 12.4779), (41.8905, 12.4783), (41.8897, 12.4781), (41.8899, 12.4775), (41.8910, 12.4770)))],
    hills=hills, roads=ROADS, walls=walls, gates=gates, bridges=bridges, aqueducts=aqueducts, blocks=blocks, gardens=gardens, marsh=marsh,
    districts=districts, labels=labels,
    compass=P((41.8745, 12.5120)),
    cartouche=P((41.8745, 12.4495)),
)

# ---------------------------------------------------------------- landmarks
def fallback_for(lm, model_key):
    w, d = lm["footprint"]
    key = model_key.split("/")[-1]
    cat = lm["category"]
    if "colosseum" in key:
        return dict(kit="amphitheater", radiusX=w / 2, radiusY=d / 2, tiers=3, tierHeight=14)
    if "theatre" in key:
        return dict(kit="amphitheater", radiusX=w / 2, radiusY=w / 2, tiers=2, tierHeight=12, arc=180)
    if "circus" in key or "stadium" in key or "navona" in key:
        return dict(kit="circus", length=w, width=d, obelisks=1 if "circus" in key else 0)
    if "arch" in key:
        return dict(kit="arch", width=w, height=max(12, w * 1.1), depth=d)
    if "castel" in key or "castra" in key or "porta" in key or "milizie" in key:
        return dict(kit="fort", width=w, depth=d, wallHeight=max(10, min(w, d) * 0.3), bastions=8)
    if cat == "temple":
        return dict(kit="temple", width=w, depth=d, columnsFront=6, columnsSide=0, podium=max(2, min(w, d) * 0.12), columnHeight=max(6, min(w, d) * 0.45))
    if cat == "district" or "forum" in key or "emporium" in key or "ghetto" in key or "porticus" in key:
        return dict(kit="cluster", plaza=dict(width=w, depth=d), buildings=[dict(offset=[-w * 0.25, -d * 0.25], width=w * 0.3, depth=d * 0.3, height=12), dict(offset=[w * 0.25, d * 0.2], width=w * 0.3, depth=d * 0.3, height=10)])
    if "pons" in key or "ponte" in key:
        return dict(kit="cluster", buildings=[dict(offset=[0, 0], width=w, depth=d, height=4, roof="flat")])
    if "column" in key or "pyramid" in key or "mausoleum" in key:
        return dict(kit="hall", width=w, depth=d, height=max(20, w * 1.2), roof="dome" if "mausoleum" in key else "flat")
    return dict(kit="hall", width=w, depth=d, height=max(10, min(w, d) * 0.4), roof="pitched")

def convert_model(lm, key):
    return dict(glb=f"models/{key}.glb", fallback=fallback_for(lm, key))

PLAN_MANIFEST = os.path.join(ROOT, "assets", "models", "plans", "manifest.json")
PLANS = json.load(open(PLAN_MANIFEST)) if os.path.exists(PLAN_MANIFEST) else {}


def footprint_for(lm):
    """Footprint from the actual model's plan when it has been rendered, so map, hover and 3D agree."""
    p = PLANS.get(lm["model"])
    if p and p.get("w") and p.get("d"):
        return [round(p["w"], 1), round(p["d"], 1)]
    return list(lm["footprint"])


def landmark(lm):
    out = dict(
        id=lm["id"], placeId=lm["placeId"], name=lm["name"], category=lm["category"], position=P(lm["latlon"]), rotation=lm["rotation"],
        footprint=footprint_for(lm), scale=lm["scale"], model=convert_model(lm, lm["model"]), reveal="assemble", activePeriods=lm["activePeriods"],
        variants={}, summary=lm["summary"], details=lm["details"], built=lm["built"], function=lm["function"], confidence=lm["confidence"],
        sourceIds=lm["sourceIds"], activity=lm.get("activity"),
    )
    if "focus" in lm:
        out["focus"] = lm["focus"]
    for pid, v in lm["variants"].items():
        vv = {k: val for k, val in v.items() if k != "model" and val != ""}
        if "model" in v:
            vv["model"] = convert_model(lm, v["model"])
        out["variants"][pid] = vv
    return out

def spot(s):
    out = dict(id=s["id"], name=s["name"], kind=s["kind"], position=P(s["latlon"]), activePeriods=s["activePeriods"], summary=s["summary"], details=s["details"],
               confidence=s["confidence"], sourceIds=s["sourceIds"], vignettes=s["vignettes"], variants={})
    for pid, v in s.get("variants", {}).items():
        out["variants"][pid] = {k: val for k, val in v.items() if val != ""}
    return out

def event(e):
    at = dict(e["at"])
    if "latlon" in at:
        at = dict(position=P(at["latlon"]))
    return dict(id=e["id"], title=e["title"], periodId=e["periodId"], date=e["date"], kind=e["kind"], at=at, effect=e["effect"], text=e["text"], sourceIds=e["sourceIds"])

def story(s):
    steps = []
    for st in s["steps"]:
        d = {k: v for k, v in st.items() if v not in ("", None)}
        steps.append(d)
    return dict(id=s["id"], title=s["title"], periodId=s["periodId"], summary=s["summary"], steps=steps, sourceIds=s["sourceIds"])

sources = {}
for mod in (landmarks_a, landmarks_b, life_spots, life_events):
    for src in mod.SOURCES:
        sources.setdefault(src["id"], src)

city = dict(
    id="rome",
    name="Roma",
    subtitle="Eternal City",
    description="Rome from the Tarquin kings to Michelangelo: the walled city between the Vatican and the Lateran, drawn as an illustrated atlas plate. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="empire-100ce",
    world=dict(scale=0.01),
    camera=dict(projection="perspective", start=dict(target=P((41.8918, 12.4858)), distance=38, tilt=52, heading=0), minDistance=1.6, maxDistance=130),
    map=MAP,
    periods=[dict(p) for p in life_spots.PERIODS],
    landmarks=[landmark(l) for l in landmarks_a.LANDMARKS + landmarks_b.LANDMARKS],
    spots=[spot(s) for s in life_spots.SPOTS],
    events=[event(e) for e in life_events.EVENTS],
    stories=[story(s) for s in life_events.STORIES],
    sources=list(sources.values()),
)

out = os.path.join(ROOT, "content", "cities", "rome", "city.json")
with open(out, "w") as f:
    json.dump(city, f, indent=1, ensure_ascii=False)
print(f"wrote {out}: {len(city['landmarks'])} landmarks, {len(city['spots'])} spots, {len(city['events'])} events, {len(city['stories'])} stories, {len(city['sources'])} sources, {os.path.getsize(out)//1024} KB")
