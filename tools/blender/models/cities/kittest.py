"""Kit smoke test: one of each part, side by side (not a real city)."""
from chronokit import Model
from worldkit import *


def sampler():
    m = Model("kittest")
    m.add(0, mosque("mosque", 60, 50, (0, 0, 0), plinth=3))
    m.add(0, move(tomb("tomb", 20, 14, (0, 0, 0), plinth=4, minarets=4), 80, 0, 0))
    m.add(0, move(gatehouse("gate", 20, 12, 14), 130, 0, 0))
    m.add(0, move(stupa("stupa", 12), 160, 0, 0))
    m.add(0, move(pagoda("pagoda", 9, 5), 190, 0, 0))
    m.add(0, move(east_asian_hall("hall", 26, 14, 6, double=True), 0, 70, 0))
    m.add(0, move(gothic_church("church", 70, 26, 22, towers=2), 60, 70, 0))
    m.add(0, move(step_pyramid("pyr", 40, 40, 4, 22, twin=True, stair_face="S"), 130, 70, 0))
    m.add(0, move(ziggurat("zig", 40, 34, 3), 190, 70, 0))
    m.add(0, move(pylon("pylon", 30, 16, 8), 0, 130, 0))
    m.add(0, move(hypostyle("hypo", 30, 20, 8), 40, 130, 0))
    m.add(0, move(adobe_mosque("adobe", 36, 26), 90, 130, 0))
    m.add(0, move(great_enclosure("enc", 22, 16, 8), 140, 130, 0))
    m.add(0, move(stele("stele", 2.6, 24), 175, 130, 0))
    m.add(0, move(castle_keep("keep", 16, 13, 4), 200, 130, 0))
    m.add(0, move(domed_basilica("hagia", 50, 46, minarets=4), 0, 190, 0))
    m.add(0, move(palazzo("palazzo", 30, 26, 16, tower=True), 60, 190, 0))
    m.add(0, move(kancha("kancha", 24, 20), 100, 190, 0))
    m.add(0, move(shikhara_temple("shik", 8, 22), 140, 190, 0))
    m.add(0, move(apadana("apadana", 30, 30, 12), 180, 190, 0))
    m.add(0, move(campanile("camp", 8, 40), 215, 190, 0))
    m.add(0, move(torii("torii", 8, 7), 215, 70, 0))
    m.add(0, move(ballcourt("ball", 40, 10), 100, 240, 0))
    m.add(0, move(charbagh("bagh", 50, 50), 30, 250, 0))
    m.add(0, move(wall_run("wall", [(0, 0), (40, 0), (40, 30)], 8, 3), 150, 230, 0))
    return m


BUILDERS = {"kittest/sampler": sampler}
