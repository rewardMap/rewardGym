from rewardgym.stimuli import draw_alien, draw_robot, draw_spaceship


def test_draw_robot():
    draw_robot()


def test_draw_alien_0():
    draw_alien(version=0)


def test_draw_alien_1():
    draw_alien(version=1)


def test_draw_alien_2():
    draw_alien(version=2)


def test_draw_alien_3():
    draw_alien(version=3)


def test_draw_spaceship_0():
    draw_spaceship(version=0)


def test_draw_spaceship_1():
    draw_spaceship(version=1)
