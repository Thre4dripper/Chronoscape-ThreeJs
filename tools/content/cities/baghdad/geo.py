# Baghdad: city, frame, eras and the map's geography. See tools/content/cities/FORMAT.md.
import math

ALL = ["mansur-770", "harun-800", "mamun-830", "abbasid-1200", "ottoman-1650"]
EARLY = ["mansur-770", "harun-800", "mamun-830"]
HM = ["harun-800", "mamun-830"]
LATE = ["abbasid-1200", "ottoman-1650"]
TO_1200 = ["mansur-770", "harun-800", "mamun-830", "abbasid-1200"]
FROM_800 = ["harun-800", "mamun-830", "abbasid-1200", "ottoman-1650"]

# The Round City: the usual reconstruction (after Le Strange, Herzfeld, Creswell and Lassner) on the west bank,
# between the Kazimayn shrine and Karkh. Its exact site is unknown; it lies under modern Baghdad.
ROUND_C = (33.3430, 44.3500)


def ring(c, r, n=32, start=0.0):
    """A circle of radius r metres round c = (lat, lon), as a closed list of (lat, lon)."""
    lat0, lon0 = c
    ky, kx = 110950.0, 111320.0 * math.cos(math.radians(lat0))
    return [(round(lat0 + r * math.sin(start + math.tau * i / n) / ky, 5), round(lon0 + r * math.cos(start + math.tau * i / n) / kx, 5)) for i in range(n)]


SOURCES = [
    dict(id="le-strange", title="Baghdad during the Abbasid Caliphate, from Contemporary Arabic and Persian Sources", author="Guy Le Strange", year=1900, url="https://archive.org/details/baghdadduringabb00lest"),
    dict(id="lassner-topography", title="The Topography of Baghdad in the Early Middle Ages: Text and Studies", author="Jacob Lassner", year=1970, note="with a translation of al-Khatib al-Baghdadi's topographical introduction"),
    dict(id="duri-ei2", title="Baghdad", author="A. A. Duri", year=1960, note="Encyclopaedia of Islam, 2nd edition, vol. 1"),
    dict(id="kennedy-baghdad", title="When Baghdad Ruled the Muslim World: The Rise and Fall of Islam's Greatest Dynasty", author="Hugh Kennedy", year=2004),
    dict(id="yaqubi-buldan", title="Kitab al-Buldan (Book of Countries)", author="al-Ya'qubi", year="c. 891", url="https://en.wikipedia.org/wiki/Al-Ya%27qubi"),
    dict(id="ibn-jubayr", title="Rihla (Travels), the visit to Baghdad", author="Ibn Jubayr", year="1184", url="https://en.wikipedia.org/wiki/Ibn_Jubayr"),
    dict(id="wiki-history-baghdad", title="History of Baghdad", author="Wikipedia", url="https://en.wikipedia.org/wiki/History_of_Baghdad"),
    dict(id="wiki-round-city", title="Round City of Baghdad", author="Wikipedia", url="https://en.wikipedia.org/wiki/Round_City_of_Baghdad"),
    dict(id="wiki-karkh", title="Karkh", author="Wikipedia", url="https://en.wikipedia.org/wiki/Karkh"),
    dict(id="wiki-nahr-isa", title="Nahr Isa", author="Wikipedia", url="https://en.wikipedia.org/wiki/Nahr_Isa"),
    dict(id="wiki-tigris", title="Tigris", author="Wikipedia", url="https://en.wikipedia.org/wiki/Tigris"),
    dict(id="wiki-gates-baghdad", title="Gates of Baghdad", author="Wikipedia", url="https://en.wikipedia.org/wiki/Gates_of_Baghdad"),
    dict(id="wiki-rusafa", title="Al-Rusafa, Iraq", author="Wikipedia", url="https://en.wikipedia.org/wiki/Al-Rusafa,_Iraq"),
    dict(id="wiki-kadhimiya", title="Kadhimiya", author="Wikipedia", url="https://en.wikipedia.org/wiki/Kadhimiya"),
    dict(id="wiki-adhamiyah", title="Adhamiyah", author="Wikipedia", url="https://en.wikipedia.org/wiki/Adhamiyah"),
    dict(id="wiki-pontoon", title="Pontoon bridge", author="Wikipedia", url="https://en.wikipedia.org/wiki/Pontoon_bridge"),
    dict(id="wiki-baghdad-eyalet", title="Baghdad Eyalet", author="Wikipedia", url="https://en.wikipedia.org/wiki/Baghdad_Eyalet"),
]

CITY = dict(
    name="Baghdad", subtitle="Madinat al-Salam, the City of Peace",
    description="Nine centuries of Baghdad on the Tigris: al-Mansur's Round City of 762 and its suburbs of Karkh, Harbiyya and Rusafa, the city of Harun al-Rashid and the House of Wisdom, the walled east city of the late caliphs, and the Ottoman town. The site of the Round City is unknown and is drawn after the usual scholarly reconstruction; the river follows its modern course, which has shifted since. Positions are projected from real coordinates; the drawing is an illustration, not a survey.",
    defaultPeriodId="harun-800",
    world=dict(heightScale=1.0, walls=["#D9C29A", "#CDB48A", "#E2D0AE", "#C8AA80", "#D4BC94"], roofs=["#C8B08A", "#BBA07A"]),
    camera=dict(target=(33.3475, 44.3600), distance=46),
)

# north-west corner, south-east corner: the Kazimayn shrine and Shammasiyya to Karkh and Bab al-Sharqi (7.5 x 7.5 km)
FRAME = ((33.3880, 44.3335), (33.3205, 44.4140))

PALETTE = dict(parchment="#E9D6AC", ink="#6A4A30", water="#5F8A88", hill="#9A8A62", road="#8C6A48")
COMPASS = (33.3700, 44.4085)
CARTOUCHE = (33.3792, 44.3895)

PERIODS = [
    dict(id="mansur-770", label="Al-Mansur's Round City", year=770, startYear=762, endYear=785,
         summary="The second Abbasid caliph, al-Mansur, founds Madinat al-Salam in 762 on the west bank of the Tigris where canals from the Euphrates come close: a perfectly round city of sun-dried brick, about 2.4 km across in most reconstructions, with three walls, four gates and his palace and mosque alone in a vast central plaza. Markets crowd the gate arcades until 773, when they are moved out to Karkh.",
         population="unknown; tens of thousands of soldiers, officials and builders at first, growing fast",
         feel="Brickmakers' kilns smoking along the canals, Khurasani soldiers in black, and the Green Dome rising over a city still smelling of wet clay.",
         style="courtyard",
         houses=dict(title="Fiefs of the Round City", text="Inside the walls, the ring between the main and inner walls was divided by streets into blocks granted to the caliph's officers, kinsmen and freedmen: courtyard houses of mud brick on fired-brick footings, flat roofs of palm trunks and reed mats plastered with clay."),
         outskirts=dict(title="The fiefs outside the gates", text="Outside each gate the caliph granted land (qati'a) to generals and their regiments: the Harbiyya to the north, Karkh to the south. Loose compounds of brick and reed among palm groves and canals.")),
    dict(id="harun-800", label="Harun al-Rashid's Baghdad", year=800, startYear=786, endYear=811,
         summary="The capital of an empire from the Maghreb to Central Asia under Harun al-Rashid (786–809), and perhaps the largest city in the world. The caliph lives in the Khuld palace by the river; the Barmakid viziers build palaces on the east bank; Rusafa, Shammasiyya and Mukharrim fill the east side, Karkh and Harbiyya the west, joined by bridges of boats. Paper, made here from the 790s, is changing the bureaucracy.",
         population="perhaps 300,000–500,000; medieval and modern estimates run much higher",
         feel="Boats from Basra unloading Indian pepper and Chinese silk, the clatter of the paper mills, muezzins answering one another across the river.",
         style="courtyard",
         houses=dict(title="Courtyard houses of Karkh", text="Houses of mud brick and fired brick turned inward round a court with a pool or a palm, flat roofs where families slept in summer, a wind-catcher (badhanj) catching the north wind, and a cool cellar (sardab) below for the hottest hours."),
         outskirts=dict(title="Palm groves and canals", text="Between the quarters lay date palms, orchards and vegetable gardens watered by the canals, brick kilns, the estates of the great families and the tents and huts of newcomers.")),
    dict(id="mamun-830", label="Al-Ma'mun's City of Learning", year=830, startYear=812, endYear=944,
         summary="Baghdad rebuilds after the civil war of 811–813, in which al-Ma'mun's armies besieged his brother al-Amin and wrecked the Round City and Karkh. Al-Ma'mun (813–833, in Baghdad from 819) patronises the translators and scholars of the House of Wisdom and the observatory at Shammasiyya. The caliphs leave for Samarra in 836 and return in 892; the palaces of the caliphate now stand on the east bank.",
         population="perhaps several hundred thousand",
         feel="Scholars arguing over Galen and Ptolemy in Syriac, Greek and Arabic, scaffolding over burnt quarters, the scratch of reed pens on new paper.",
         style="courtyard",
         houses=dict(title="Rebuilt houses", text="Quarters burnt in the siege were rebuilt in fired brick set in gypsum mortar, two storeys round a court; rich houses had painted stucco, wind-catchers on the roof and a sardab half underground."),
         outskirts=dict(title="Gardens and ruins", text="Beyond the rebuilt quarters, burnt-out lots, new gardens and the camps of soldiers; on the east bank the estates and palaces of officials along the river.")),
    dict(id="abbasid-1200", label="The Late Caliphate", year=1200, startYear=945, endYear=1258,
         summary="After 945 Buyid and then Seljuk sultans rule Baghdad in the caliph's name; from 1180 al-Nasir revives the caliph's power. The city has shifted to the east bank, walled about 1095–1123 with four gates round the vast Dar al-Khilafa. The Round City is a ruin and a quarter; Karkh, Bab al-Basra and Harbiyya are separate towns. The Mongols sack Baghdad in February 1258.",
         population="perhaps 100,000–200,000 by the 12th century",
         feel="Sufi lodges, madrasa students in black turbans, the caliph's processions through the Bab al-Nubi, and quarters fighting quarters across the river.",
         style="courtyard",
         houses=dict(title="Houses of the walled east city", text="Brick courtyard houses packed along winding lanes and dead-end alleys behind gates closed at night; fired brick with gypsum plaster, wind-catchers, deep sardabs, and timber screens over the upper windows."),
         outskirts=dict(title="Mounds and separate towns", text="West of the river, the old quarters had become separate walled towns among ruin mounds, cemeteries and gardens: Karkh, Bab al-Basra, Harbiyya and the shrine town of the Kazimayn.")),
    dict(id="ottoman-1650", label="Ottoman Baghdad", year=1650, startYear=1534, endYear=1749,
         summary="A frontier city fought over by Ottomans and Safavid Persians: taken by Suleiman in 1534, by Shah Abbas in 1623, and retaken for good by Sultan Murad IV in 1638. The walled east town with its citadel and governor's palace, the small west-bank suburb of Karkh and a bridge of boats; the shrines of the Kazimayn, Abu Hanifa and Abd al-Qadir draw pilgrims.",
         population="perhaps 50,000–100,000",
         feel="Janissaries at the citadel gate, coffee in the khans, Persian pilgrims bound for the Kazimayn, and shanashil balconies leaning over the lanes.",
         style="courtyard",
         houses=dict(title="Shanashil houses", text="Brick courtyard houses of two storeys whose upper rooms project over the lane on timber brackets behind latticed shanashil windows; wind-catchers on the roof, and the family sleeping on the roof or in the sardab in summer."),
         outskirts=dict(title="Palm groves and cemeteries", text="Inside the old walls whole districts were gardens, cemeteries and ruin mounds; outside, palm groves along the river and the villages of the Kazimayn and al-A'zamiyya.")),
]

# ---------------------------------------------------------------- the Tigris (its modern course; it has shifted since the Abbasid period)
TIGRIS = [(33.3913, 44.3298), (33.3874, 44.3311), (33.3855, 44.3337), (33.3860, 44.3371), (33.3879, 44.3414), (33.3903, 44.3460), (33.3911, 44.3488), (33.3913, 44.3528),
          (33.3896, 44.3560), (33.3872, 44.3591), (33.3851, 44.3607), (33.3823, 44.3608), (33.3798, 44.3597), (33.3769, 44.3574), (33.3749, 44.3554), (33.3732, 44.3537),
          (33.3706, 44.3514), (33.3681, 44.3499), (33.3659, 44.3491), (33.3630, 44.3489), (33.3604, 44.3500), (33.3594, 44.3530), (33.3602, 44.3564), (33.3610, 44.3595),
          (33.3618, 44.3646), (33.3620, 44.3675), (33.3611, 44.3703), (33.3597, 44.3725), (33.3568, 44.3729), (33.3543, 44.3728), (33.3502, 44.3715), (33.3474, 44.3712),
          (33.3445, 44.3724), (33.3431, 44.3750), (33.3428, 44.3782), (33.3421, 44.3809), (33.3406, 44.3840), (33.3388, 44.3860), (33.3370, 44.3884), (33.3350, 44.3912),
          (33.3334, 44.3937), (33.3313, 44.3969), (33.3293, 44.3993), (33.3263, 44.4027), (33.3238, 44.4055), (33.3211, 44.4080), (33.3187, 44.4101), (33.3163, 44.4116)]

TIGRIS_BLURB = "Dijla, the Tigris: Baghdad's highway to Basra and the Gulf, and to Mosul and the north. Al-Mansur chose the site, the story goes, because 'here is the Tigris, with nothing between us and China'. It flooded in spring, sometimes disastrously; its bed has moved since the Abbasid centuries, and it is drawn here on its modern course."

SARAT = [(33.3290, 44.3335), (33.3300, 44.3420), (33.3305, 44.3500), (33.3312, 44.3590), (33.3328, 44.3640), (33.3352, 44.3672), (33.3385, 44.3712), (33.3410, 44.3758), (33.3424, 44.3790)]
ISA = [(33.3220, 44.3335), (33.3228, 44.3450), (33.3238, 44.3560), (33.3255, 44.3680), (33.3270, 44.3790), (33.3282, 44.3890), (33.3292, 44.3975)]

WATER = [
    dict(id="tigris", name="Dijla (the Tigris)", path=TIGRIS, width=250, blurb=TIGRIS_BLURB),
    dict(id="sarat", name="Nahr al-Sarat", path=SARAT, width=18, periods=TO_1200,
         blurb="A canal from the Isa canal that ran past the Kufa and Basra gates of the Round City into the Tigris. Al-Mansur built the city where the Euphrates canals come closest to the Tigris; brick bridges crossed the Sarat to Karkh."),
    dict(id="isa", name="Nahr Isa", path=ISA, width=24,
         blurb="The great navigable canal from the Euphrates, named after an Abbasid prince, which brought barges of grain from Syria and the Euphrates towns into the Tigris at the south end of Karkh. Mills and markets lined its banks."),
]

HILLS = []

ROADS = [
    # ---- the Round City's four roads
    dict(id="khurasan-road", name="Khurasan road (Bab Khurasan to the Bridge)", path=[(33.3507, 44.3591), (33.3528, 44.3640), (33.3545, 44.3690), (33.3552, 44.3710)], width=22, style="major", labelled=True, periods=EARLY,
         blurb="From the Khurasan Gate, the gate of the east and of the caliph's Khurasani army, past the Khuld palace to the main bridge of boats and Bab al-Taq."),
    dict(id="kufa-road", name="Kufa road", path=[(33.3354, 44.3409), (33.3320, 44.3385), (33.3270, 44.3360), (33.3215, 44.3345)], width=16, style="major", labelled=True, periods=EARLY,
         blurb="Out of the Kufa Gate (south-west) toward Kufa and the pilgrim road to Mecca, over the Sarat and the Isa canals."),
    dict(id="basra-road", name="Basra road", path=[(33.3354, 44.3591), (33.3330, 44.3620), (33.3290, 44.3650), (33.3250, 44.3690), (33.3210, 44.3720)], width=16, style="major", labelled=True, periods=EARLY,
         blurb="Out of the Basra Gate (south-east) into Karkh and on south to Wasit and Basra."),
    dict(id="sham-road", name="Road of Bab al-Sham", path=[(33.3507, 44.3409), (33.3560, 44.3395), (33.3640, 44.3405), (33.3720, 44.3405), (33.3772, 44.3395)], width=16, style="major", labelled=True, periods=EARLY,
         blurb="Out of the Syria Gate (north-west) through the Harbiyya to the cemetery of the Quraysh and the road to Anbar, Raqqa and Syria."),
    # ---- the east bank, 770-944
    dict(id="bab-al-taq", name="Street of Bab al-Taq", path=[(33.3552, 44.3750), (33.3575, 44.3790), (33.3620, 44.3830), (33.3690, 44.3880), (33.3720, 44.3900)], width=18, style="major", labelled=True, periods=EARLY,
         blurb="From the head of the main bridge under the great arch (taq) named after Asma, a princess of the Abbasid house, north-east toward Shammasiyya and the Khurasan road. The busiest street of the east bank."),
    dict(id="rusafa-street", name="Street to Rusafa", path=[(33.3638, 44.3660), (33.3655, 44.3660), (33.3670, 44.3640)], width=12, style="minor", periods=EARLY,
         blurb="From the upper bridge to the mosque and palace of Rusafa."),
    dict(id="mukharrim-street", name="Street of al-Mukharrim", path=[(33.3552, 44.3750), (33.3510, 44.3790), (33.3460, 44.3860), (33.3420, 44.3915), (33.3380, 44.3960)], width=14, style="major", periods=EARLY,
         blurb="South along the east bank from Bab al-Taq through al-Mukharrim to the palaces of the Barmakids, later the caliphs' Dar al-Khilafa."),
    dict(id="harbiyya-street", name="Road from Bab al-Basra to the river", path=[(33.3354, 44.3591), (33.3390, 44.3660), (33.3440, 44.3690), (33.3462, 44.3698)], width=10, style="minor", periods=EARLY,
         blurb="From the Basra Gate to the lower bridge of boats, through the quarter later called Bab al-Basra."),
    # ---- the late caliphate and the Ottoman town
    dict(id="bridge-street-east", name="Street of the Bridge (Suq al-Thulatha)", path=[(33.3398, 44.3891), (33.3420, 44.3925), (33.3455, 44.3960), (33.3490, 44.4005), (33.3512, 44.4040)], width=12, style="major", labelled=True, periods=LATE,
         blurb="From the bridge of boats past the Tuesday Market (Suq al-Thulatha) and the Mustansiriya to the Zafariyya gate, later Bab al-Wastani."),
    dict(id="sultan-street", name="Street of Bab al-Sultan", path=[(33.3500, 44.3845), (33.3465, 44.3880), (33.3430, 44.3930), (33.3400, 44.3975), (33.3365, 44.3995)], width=12, style="major", labelled=True, periods=LATE,
         blurb="The street from the north gate (Bab al-Sultan, later Bab al-Mu'azzam) south through the markets to the gates of the caliph's palace."),
    dict(id="halba-street", name="Street of Bab al-Halba", path=[(33.3411, 44.4122), (33.3400, 44.4060), (33.3393, 44.4000), (33.3390, 44.3975)], width=10, style="major", periods=LATE,
         blurb="From the Gate of the Racecourse (Bab al-Halba, the Talisman Gate) west into the city past the shrine of Abd al-Qadir."),
    dict(id="sharqi-street", name="Road of Bab al-Basaliyya", path=[(33.3301, 44.4122), (33.3320, 44.4080), (33.3345, 44.4045), (33.3370, 44.4010)], width=10, style="minor", periods=LATE,
         blurb="From the south-east gate (Bab al-Basaliyya, later Bab al-Sharqi) along the palace walls into the city."),
    dict(id="karkh-street", name="Street of Karkh", path=[(33.3367, 44.3864), (33.3350, 44.3820), (33.3345, 44.3780), (33.3345, 44.3720), (33.3360, 44.3650)], width=10, style="major", periods=LATE,
         blurb="From the west end of the bridge through the markets of Karkh."),
    dict(id="mashhad-road", name="Road to the Mashhad of the Kazimayn", path=[(33.3360, 44.3650), (33.3400, 44.3640), (33.3460, 44.3645), (33.3540, 44.3640), (33.3580, 44.3470), (33.3660, 44.3420), (33.3740, 44.3405), (33.3778, 44.3395)], width=10, style="major", labelled=True, periods=LATE,
         blurb="The pilgrims' road from Karkh past the mounds of the Round City and through the Harbiyya to the shrine of the two imams."),
    dict(id="azamiyya-road", name="Road to al-A'zamiyya", path=[(33.3500, 44.3845), (33.3540, 44.3810), (33.3600, 44.3770), (33.3660, 44.3700), (33.3700, 44.3640)], width=8, style="minor", periods=LATE,
         blurb="North out of Bab al-Sultan to the tomb of Abu Hanifa and the old Rusafa, by then a cemetery town."),
]

EAST_WALL = [(33.3460, 44.3728), (33.3482, 44.3790), (33.3500, 44.3845), (33.3512, 44.3930), (33.3516, 44.3990), (33.3514, 44.4046), (33.3478, 44.4098), (33.3440, 44.4123),
             (33.3411, 44.4129), (33.3360, 44.4134), (33.3301, 44.4129), (33.3262, 44.4105), (33.3242, 44.4066)]

WALLS = [
    dict(id="round-city-wall", name="Walls of Madinat al-Salam", path=ring(ROUND_C, 1150, 40), closed=True, periods=EARLY,
         blurb="Three circuits in the usual reading of the sources: an outer wall behind a moat, the great main wall of mud brick with towers, and an inner wall round the central plaza. The main wall is said to have been about 30 m high at the gates; numbers in the sources vary."),
    dict(id="east-wall", name="Walls of the East Side", path=EAST_WALL, periods=LATE,
         blurb="Begun about 1095 under the caliph al-Mustazhir and finished under al-Mustarshid in the 1120s: a semicircle of brick with a moat, from the river at the north to the river at the south, with four gates. Al-Nasir rebuilt its gates about 1221. The Ottomans kept it in repair until the 19th century."),
]

GATES = [
    dict(id="bab-al-sultan", name="Bab al-Sultan (Bab al-Mu'azzam)", position=(33.3500, 44.3845), periods=LATE),
    dict(id="bab-al-basaliyya", name="Bab al-Basaliyya (Bab al-Sharqi)", position=(33.3301, 44.4129), periods=LATE),
]

BRIDGES = [
    dict(id="main-bridge", name="The main bridge of boats (al-Jisr)", path=[(33.3552, 44.3708), (33.3552, 44.3752)], build="timber", arches=10, landmarkId="bridge-of-boats", periods=EARLY,
         blurb="Boats lashed side by side and decked with planks, chained to iron rings on brick piers on each bank, joining the Khurasan road to Bab al-Taq."),
    dict(id="upper-bridge", name="Upper bridge of boats", path=[(33.3598, 44.3660), (33.3640, 44.3660)], build="timber", arches=10, periods=EARLY,
         blurb="A second bridge of boats upriver, toward Rusafa and the Shammasiyya."),
    dict(id="lower-bridge", name="Lower bridge of boats", path=[(33.3462, 44.3696), (33.3462, 44.3740)], build="timber", arches=10, periods=HM,
         blurb="The third bridge of boats, from the quarter of Bab al-Basra to al-Mukharrim. Harun's Baghdad had three bridges; after the 9th century usually only one or two were kept."),
    dict(id="late-bridge", name="Bridge of boats (al-Jisr)", path=[(33.3366, 44.3862), (33.3396, 44.3894)], build="timber", arches=12, periods=LATE,
         blurb="By the 12th century one bridge of boats joined Karkh to the Tuesday Market on the east side; Ibn Jubayr crossed it in 1184 among crowds of men and women. The Ottoman bridge stood near the same place, near today's al-Shuhada bridge."),
    dict(id="old-bridge", name="al-Qantara al-'Atiqa (the Old Bridge)", path=[(33.3300, 44.3592), (33.3324, 44.3590)], build="stone", arches=2, periods=TO_1200,
         blurb="The oldest of the brick bridges over the Sarat, by the Basra Gate, said to date from the time of the Persian kings."),
    dict(id="new-bridge", name="al-Qantara al-Jadida (the New Bridge)", path=[(33.3340, 44.3672), (33.3363, 44.3655)], build="stone", arches=2, periods=TO_1200,
         blurb="A brick bridge over the Sarat into Karkh."),
]

AQUEDUCTS = []

BLOCKS = [
    # ---- 770: fiefs outside the gates
    dict(name="The Harbiyya fiefs", polygon=[(33.3560, 44.3355), (33.3715, 44.3355), (33.3715, 44.3462), (33.3560, 44.3462)], density="loose", periods=["mansur-770"]),
    dict(name="Karkh", polygon=[(33.3250, 44.3620), (33.3300, 44.3600), (33.3330, 44.3700), (33.3330, 44.3800), (33.3295, 44.3850), (33.3268, 44.3800)], density="loose", periods=["mansur-770"]),
    dict(name="Fiefs by the Kufa Gate", polygon=[(33.3245, 44.3345), (33.3280, 44.3345), (33.3290, 44.3470), (33.3245, 44.3470)], density="loose", periods=["mansur-770"]),
    dict(name="Rusafa camp", polygon=[(33.3640, 44.3580), (33.3725, 44.3600), (33.3730, 44.3710), (33.3640, 44.3710)], density="loose", periods=["mansur-770"]),
    dict(name="al-Mukharrim", polygon=[(33.3462, 44.3768), (33.3530, 44.3772), (33.3525, 44.3870), (33.3458, 44.3880)], density="loose", periods=["mansur-770"]),
    # ---- 800 and 830
    dict(name="al-Harbiyya", polygon=[(33.3555, 44.3355), (33.3705, 44.3355), (33.3705, 44.3462), (33.3555, 44.3462)], density="dense", periods=HM),
    dict(name="By the cemetery of the Quraysh", polygon=[(33.3715, 44.3355), (33.3778, 44.3355), (33.3778, 44.3462), (33.3715, 44.3462)], density="loose", periods=HM),
    dict(name="Karkh", polygon=[(33.3250, 44.3640), (33.3312, 44.3618), (33.3345, 44.3675), (33.3345, 44.3760), (33.3330, 44.3840), (33.3295, 44.3900), (33.3262, 44.3830)], density="dense", periods=HM),
    dict(name="Bab al-Basra", polygon=[(33.3375, 44.3640), (33.3455, 44.3640), (33.3452, 44.3688), (33.3410, 44.3700)], density="dense", periods=HM),
    dict(name="Bab al-Kufa", polygon=[(33.3245, 44.3345), (33.3280, 44.3345), (33.3290, 44.3470), (33.3245, 44.3470)], density="dense", periods=HM),
    dict(name="Fiefs of the Isa canal", polygon=[(33.3245, 44.3480), (33.3290, 44.3480), (33.3298, 44.3600), (33.3252, 44.3610)], density="loose", periods=HM),
    dict(name="al-Rusafa", polygon=[(33.3640, 44.3575), (33.3725, 44.3600), (33.3735, 44.3712), (33.3640, 44.3712)], density="dense", periods=HM),
    dict(name="al-Shammasiyya", polygon=[(33.3745, 44.3650), (33.3870, 44.3655), (33.3870, 44.3790), (33.3745, 44.3790)], density="loose", periods=HM),
    dict(name="Bab al-Taq", polygon=[(33.3562, 44.3762), (33.3610, 44.3752), (33.3648, 44.3722), (33.3700, 44.3742), (33.3700, 44.3850), (33.3562, 44.3850)], density="dense", periods=HM),
    dict(name="al-Mukharrim", polygon=[(33.3462, 44.3768), (33.3540, 44.3772), (33.3540, 44.3880), (33.3458, 44.3880)], density="dense", periods=HM),
    dict(name="Palaces of the Barmakids", polygon=[(33.3368, 44.3955), (33.3430, 44.3905), (33.3450, 44.4000), (33.3362, 44.4040)], density="loose", periods=HM),
    # ---- 1200: west-bank towns
    dict(name="al-Karkh", polygon=[(33.3250, 44.3630), (33.3320, 44.3628), (33.3360, 44.3690), (33.3378, 44.3780), (33.3360, 44.3860), (33.3312, 44.3925), (33.3268, 44.3880)], density="dense", periods=["abbasid-1200"]),
    dict(name="Bab al-Basra", polygon=[(33.3375, 44.3640), (33.3455, 44.3640), (33.3452, 44.3688), (33.3410, 44.3700)], density="dense", periods=["abbasid-1200"]),
    dict(name="al-Harbiyya", polygon=[(33.3555, 44.3355), (33.3705, 44.3355), (33.3705, 44.3462), (33.3555, 44.3462)], density="dense", periods=["abbasid-1200"]),
    dict(name="Mashhad of the Kazimayn", polygon=[(33.3722, 44.3355), (33.3785, 44.3355), (33.3785, 44.3462), (33.3722, 44.3462)], density="dense", periods=["abbasid-1200"]),
    dict(name="Bab al-Kufa ruins", polygon=[(33.3245, 44.3345), (33.3280, 44.3345), (33.3290, 44.3470), (33.3245, 44.3470)], density="loose", periods=["abbasid-1200"]),
    # ---- 1200: the walled east city
    dict(name="Bab al-Sultan", polygon=[(33.3452, 44.3792), (33.3480, 44.3800), (33.3495, 44.3860), (33.3442, 44.3880)], density="dense", periods=["abbasid-1200"]),
    dict(name="Suq al-Thulatha", polygon=[(33.3405, 44.3895), (33.3442, 44.3888), (33.3448, 44.3958), (33.3392, 44.3975)], density="dense", periods=LATE),
    dict(name="Darb Zakhi and al-Ma'muniyya", polygon=[(33.3452, 44.3900), (33.3505, 44.3880), (33.3510, 44.4030), (33.3462, 44.4050)], density="dense", periods=["abbasid-1200"]),
    dict(name="al-Rayyan", polygon=[(33.3395, 44.3985), (33.3445, 44.3970), (33.3452, 44.4028), (33.3400, 44.4032)], density="dense", periods=LATE),
    dict(name="Bab al-Azaj", polygon=[(33.3372, 44.4040), (33.3440, 44.4035), (33.3442, 44.4112), (33.3378, 44.4118)], density="dense", periods=["abbasid-1200"]),
    dict(name="Behind the palace walls", polygon=[(33.3300, 44.4050), (33.3360, 44.4050), (33.3360, 44.4118), (33.3306, 44.4118)], density="loose", periods=["abbasid-1200"]),
    dict(name="Rusafa and the tomb of Abu Hanifa", polygon=[(33.3660, 44.3580), (33.3740, 44.3600), (33.3740, 44.3700), (33.3660, 44.3700)], density="loose", periods=["abbasid-1200"]),
    dict(name="al-Shammasiyya", polygon=[(33.3745, 44.3650), (33.3870, 44.3655), (33.3870, 44.3790), (33.3745, 44.3790)], density="loose", periods=["abbasid-1200"]),
    # ---- 1650: the Ottoman town
    dict(name="Bab al-Mu'azzam", polygon=[(33.3466, 44.3842), (33.3492, 44.3852), (33.3495, 44.3900), (33.3445, 44.3890)], density="dense", periods=["ottoman-1650"]),
    dict(name="al-Haydarkhana", polygon=[(33.3452, 44.3900), (33.3505, 44.3880), (33.3508, 44.3980), (33.3458, 44.3995)], density="dense", periods=["ottoman-1650"]),
    dict(name="Bab al-Shaykh", polygon=[(33.3348, 44.4045), (33.3420, 44.4040), (33.3425, 44.4105), (33.3352, 44.4110)], density="dense", periods=["ottoman-1650"]),
    dict(name="al-Saray and the river quarters", polygon=[(33.3315, 44.3985), (33.3375, 44.3965), (33.3385, 44.4030), (33.3320, 44.4040)], density="dense", periods=["ottoman-1650"]),
    dict(name="Eastern quarters", polygon=[(33.3270, 44.4045), (33.3340, 44.4045), (33.3340, 44.4115), (33.3285, 44.4115)], density="loose", periods=["ottoman-1650"]),
    dict(name="Karkh", polygon=[(33.3318, 44.3772), (33.3378, 44.3778), (33.3362, 44.3858), (33.3315, 44.3910)], density="dense", periods=["ottoman-1650"]),
    dict(name="al-Kazimiyya", polygon=[(33.3740, 44.3355), (33.3790, 44.3355), (33.3790, 44.3450), (33.3740, 44.3450)], density="dense", periods=["ottoman-1650"]),
    dict(name="al-A'zamiyya", polygon=[(33.3680, 44.3580), (33.3745, 44.3600), (33.3745, 44.3680), (33.3680, 44.3680)], density="loose", periods=["ottoman-1650"]),
]

GARDENS = [
    dict(name="Gardens of the Khuld", polygon=[(33.3470, 44.3640), (33.3540, 44.3640), (33.3540, 44.3698), (33.3470, 44.3698)], kind="park", periods=HM),
    dict(name="Palm groves of the Isa canal", polygon=[(33.3208, 44.3360), (33.3222, 44.3360), (33.3232, 44.3560), (33.3215, 44.3560)], kind="orchard"),
    dict(name="Palm groves of Qatrabbul road", polygon=[(33.3790, 44.3350), (33.3830, 44.3350), (33.3830, 44.3440), (33.3790, 44.3440)], kind="orchard", periods=EARLY),
    dict(name="Fields of the Shammasiyya", polygon=[(33.3740, 44.3800), (33.3875, 44.3800), (33.3875, 44.3885), (33.3740, 44.3885)], kind="orchard"),
    dict(name="East-bank orchards", polygon=[(33.3560, 44.3870), (33.3700, 44.3870), (33.3700, 44.4000), (33.3560, 44.4000)], kind="orchard"),
    dict(name="Orchards of the Round City mounds", polygon=[(33.3470, 44.3640), (33.3540, 44.3640), (33.3540, 44.3698), (33.3470, 44.3698)], kind="orchard", periods=LATE),
    dict(name="Gardens inside the walls", polygon=[(33.3445, 44.4060), (33.3495, 44.4062), (33.3478, 44.4098), (33.3445, 44.4115)], kind="orchard", periods=["ottoman-1650"]),
    dict(name="Palm groves of Karkh", polygon=[(33.3212, 44.3700), (33.3240, 44.3700), (33.3255, 44.3880), (33.3220, 44.3900)], kind="orchard"),
]

MARSH = []

DISTRICTS = [
    dict(id="madinat-al-salam", name="Madinat al-Salam (the Round City)", polygon=ring(ROUND_C, 1200, 24), periods=EARLY,
         description="Al-Mansur's round city of 762–766: three walls, four gates, a ring of residential streets for his officers and kin, and in the empty centre his palace and mosque. After the siege of 812–813 and the caliphs' move east it slowly decayed."),
    dict(id="madinat-al-mansur", name="Madinat al-Mansur (ruins)", polygon=ring(ROUND_C, 1200, 24), periods=["abbasid-1200"],
         description="By the 12th century the Round City was a quarter among mounds, its walls fallen, still known for al-Mansur's mosque where Friday prayer was held for the west side."),
    dict(id="karkh", name="al-Karkh", polygon=[(33.3245, 44.3600), (33.3330, 44.3618), (33.3380, 44.3700), (33.3385, 44.3800), (33.3320, 44.3940), (33.3245, 44.3860)],
         description="The market suburb south of the Round City, between the Sarat and Isa canals, where al-Mansur moved the markets in 773. In later centuries a largely Shi'i quarter of merchants, often at odds with Sunni Bab al-Basra next door."),
    dict(id="harbiyya", name="al-Harbiyya", polygon=[(33.3550, 44.3345), (33.3710, 44.3345), (33.3710, 44.3470), (33.3550, 44.3470)], periods=TO_1200,
         description="The fiefs north of the Syria Gate given to the general Harb ibn Abdallah and the Khurasani soldiers; in the 12th century a walled Hanbali quarter of its own."),
    dict(id="kazimayn", name="Maqabir Quraysh (al-Kazimayn)", polygon=[(33.3715, 44.3345), (33.3845, 44.3345), (33.3845, 44.3470), (33.3715, 44.3470)],
         description="The cemetery of the Quraysh, laid out by al-Mansur, where the seventh and ninth imams of the Twelver Shi'a, Musa al-Kazim (d. 799) and Muhammad al-Jawad (d. 835), were buried. The town of the shrine grew round them."),
    dict(id="rusafa", name="al-Rusafa", polygon=[(33.3635, 44.3570), (33.3745, 44.3590), (33.3745, 44.3720), (33.3635, 44.3720)], periods=TO_1200,
         description="The east-bank camp and palace city built from 768 for al-Mansur's son and heir al-Mahdi, with its own mosque. Later the burial place of caliphs and of Abu Hanifa."),
    dict(id="azamiyya", name="al-A'zamiyya", polygon=[(33.3635, 44.3570), (33.3745, 44.3590), (33.3745, 44.3720), (33.3635, 44.3720)], periods=["ottoman-1650"],
         description="The town round the tomb of Abu Hanifa, 'the greatest imam' (al-imam al-a'zam), on the site of old Rusafa. Suleiman the Magnificent rebuilt the tomb and mosque after 1534."),
    dict(id="shammasiyya", name="al-Shammasiyya", polygon=[(33.3745, 44.3640), (33.3875, 44.3640), (33.3875, 44.3800), (33.3745, 44.3800)],
         description="The open ground upriver on the east bank, named after a deacon (shammas) of a Christian monastery there; parade ground, monastery gardens, and the site of al-Ma'mun's observatory of 828."),
    dict(id="mukharrim", name="al-Mukharrim", polygon=[(33.3450, 44.3760), (33.3550, 44.3765), (33.3540, 44.3900), (33.3440, 44.3900)], periods=EARLY,
         description="The east-bank quarter between Bab al-Taq and the palaces to the south, settled by soldiers and officials; its southern part became the core of the later walled east city."),
    dict(id="east-side", name="al-Jānib al-Sharqī (the East Side)", polygon=EAST_WALL, periods=LATE,
         description="The walled east city: the caliph's palace precinct along the river, the Tuesday Market, madrasas and Sufi lodges; from 1534 the Ottoman town with its citadel and governor's palace."),
]

LABELS = [
    dict(text="Dijla", position=(33.3720, 44.3527), size="lg", rotation=-55),
    dict(text="Dijla", position=(33.3272, 44.4015), size="lg", rotation=45),
    dict(text="Madinat al-Salam", position=(33.3562, 44.3520), size="md", periods=EARLY),
    dict(text="Madinat al-Mansur", position=(33.3562, 44.3520), size="sm", periods=["abbasid-1200"]),
    dict(text="al-Karkh", position=(33.3268, 44.3735), size="lg"),
    dict(text="al-Harbiyya", position=(33.3640, 44.3408), size="md", rotation=-90, periods=TO_1200),
    dict(text="al-Rusafa", position=(33.3712, 44.3665), size="md", periods=TO_1200),
    dict(text="al-A'zamiyya", position=(33.3712, 44.3665), size="sm", periods=["ottoman-1650"]),
    dict(text="al-Shammasiyya", position=(33.3820, 44.3725), size="md"),
    dict(text="al-Mukharrim", position=(33.3500, 44.3830), size="sm", periods=EARLY),
    dict(text="Bab al-Taq", position=(33.3620, 44.3800), size="sm", periods=EARLY),
    dict(text="Maqabir Quraysh", position=(33.3752, 44.3420), size="sm", periods=["mansur-770", "harun-800", "mamun-830"]),
    dict(text="Mashhad al-Kazimayn", position=(33.3752, 44.3420), size="sm", periods=["abbasid-1200"]),
    dict(text="al-Kazimiyya", position=(33.3752, 44.3420), size="sm", periods=["ottoman-1650"]),
    dict(text="Nahr Isa", position=(33.3242, 44.3500), size="sm", rotation=-5),
    dict(text="Nahr al-Sarat", position=(33.3368, 44.3700), size="sm", rotation=-45, periods=TO_1200),
    dict(text="Baghdad", position=(33.3460, 44.4000), size="lg", periods=LATE),
]
