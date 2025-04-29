import numpy as np
from psychopy.visual import ImageStim, Line, TextBox2

from rewardgym.stimuli.alien_images import draw_alien
from rewardgym.stimuli.spaceship_images import draw_spaceship


def twostep_instructions():
    card3 = draw_alien(0, 300, 300, (0, 0, 200))
    card4 = draw_alien(1, 300, 300, (0, 0, 200))
    card5 = draw_alien(2, 300, 300, (200, 200, 0))
    card6 = draw_alien(3, 300, 300, (200, 200, 0))

    card1 = draw_spaceship(0, 400, 400, (0, 150, 200))
    card2 = draw_spaceship(1, 400, 400, (0, 150, 200))

    def part_0(win, instructions):
        part_0_0 = TextBox2(
            win=win,
            text=instructions["two-step"]["0.0"],
            letterHeight=28,
            pos=(0, 200),
        )

        size = (100, 100)
        img_card1 = ImageStim(win=win, image=card3, pos=(-320, -60), size=size)
        img_card2 = ImageStim(win=win, image=card4, pos=(-120, -60), size=size)
        img_card3 = ImageStim(win=win, image=card5, pos=(120, -60), size=size)
        img_card4 = ImageStim(win=win, image=card6, pos=(320, -60), size=size)

        part_0_1 = TextBox2(
            win=win,
            text=instructions["two-step"]["0.1"],
            letterHeight=28,
            pos=(-320, -130),
            size=(100, None),
        )
        part_0_2 = TextBox2(
            win=win,
            text=instructions["two-step"]["0.2"],
            letterHeight=28,
            pos=(-120, -130),
            size=(100, None),
        )
        part_0_3 = TextBox2(
            win=win,
            text=instructions["two-step"]["0.3"],
            letterHeight=28,
            pos=(120, -130),
            size=(100, None),
        )
        part_0_4 = TextBox2(
            win=win,
            text=instructions["two-step"]["0.4"],
            letterHeight=28,
            pos=(320, -130),
            size=(100, None),
        )

        for i in [
            img_card1,
            img_card2,
            img_card3,
            img_card4,
            part_0_0,
            part_0_1,
            part_0_2,
            part_0_3,
            part_0_4,
        ]:
            i.draw()

    def part_1(win, instructions):
        part_1_0 = TextBox2(
            win=win,
            text=instructions["two-step"]["1.0"],
            letterHeight=28,
            pos=(0, 250),
        )
        part_1_1 = TextBox2(
            win=win,
            text=instructions["two-step"]["1.1"],
            letterHeight=28,
            pos=(0, 80),
        )
        part_1_2 = TextBox2(
            win=win,
            text=instructions["two-step"]["1.2"],
            letterHeight=28,
            pos=(0, -175),
        )
        size = (100, 100)
        img_card1 = ImageStim(win=win, image=card3, pos=(-120, 150), size=size)
        img_card2 = ImageStim(win=win, image=card4, pos=(120, 150), size=size)
        img_card3 = ImageStim(win=win, image=card5, pos=(-120, 0), size=size)
        img_card4 = ImageStim(win=win, image=card6, pos=(120, 0), size=size)

        for i in [
            img_card1,
            img_card2,
            img_card3,
            img_card4,
            part_1_0,
            part_1_1,
            part_1_2,
        ]:
            i.draw()

    def part_2(win, instructions):
        part_2_0 = TextBox2(
            win=win,
            text=instructions["two-step"]["2.0"],
            letterHeight=28,
            pos=(0, 250),
        )
        part_2_1 = TextBox2(
            win=win,
            text=instructions["two-step"]["2.1"],
            letterHeight=28,
            pos=(0, -20),
        )
        part_2_2 = TextBox2(
            win=win,
            text=instructions["two-step"]["2.2"],
            letterHeight=28,
            pos=(0, -200),
        )
        size = (100, 100)
        img_card1 = ImageStim(win=win, image=card3, pos=(-120, 50), size=size)
        img_card2 = ImageStim(win=win, image=card4, pos=(120, 50), size=size)
        img_card3 = ImageStim(win=win, image=card5, pos=(-120, -100), size=size)
        img_card4 = ImageStim(win=win, image=card6, pos=(120, -100), size=size)

        img_door1 = ImageStim(win=win, image=card1, pos=(-510, 90), size=(100, 150))
        img_door2 = ImageStim(win=win, image=card2, pos=(-510, -80), size=(100, 150))

        for i in [
            img_card1,
            img_card2,
            img_card3,
            img_card4,
            part_2_0,
            part_2_1,
            part_2_2,
            img_door1,
            img_door2,
        ]:
            i.draw()

    def part_3(win, instructions):
        y_offset = 60
        part_3_0 = TextBox2(
            win=win,
            text=instructions["two-step"]["3.0"],
            letterHeight=28,
            pos=(0, 350),
        )

        part_3_1 = TextBox2(
            win=win,
            text=instructions["two-step"]["3.1"],
            letterHeight=28,
            pos=(0, -250),
        )

        small_shape1 = np.array(card1.shape[:2])[::-1] // 2
        small_shape2 = np.array(card4.shape[:2])[::-1] // 2

        img_card1 = ImageStim(
            win=win, image=card1, pos=(-100, 175 + y_offset), size=small_shape1
        )
        img_card2 = ImageStim(
            win=win, image=card2, pos=(100, 175 + y_offset), size=small_shape1
        )

        img_card3 = ImageStim(
            win=win, image=card3, pos=(-320, -125 + y_offset), size=small_shape2
        )
        img_card4 = ImageStim(
            win=win, image=card4, pos=(-150, -125 + y_offset), size=small_shape2
        )

        img_card5 = ImageStim(
            win=win, image=card5, pos=(150, -125 + y_offset), size=small_shape2
        )
        img_card6 = ImageStim(
            win=win, image=card6, pos=(320, -125 + y_offset), size=small_shape2
        )

        line1 = Line(
            win=win,
            start=(-100, 70 + y_offset),
            end=((-460) // 2 - 5, -55 + y_offset),
            lineWidth=20,
            color=[0.25, 0.25, 0.25],
        )
        line2 = Line(
            win=win,
            start=(-100, 70 + y_offset),
            end=((440) // 2 - 5, -55 + y_offset),
            lineWidth=10,
            color=[0.25, 0.25, 0.25],
        )
        line3 = Line(
            win=win,
            start=(100, 70 + y_offset),
            end=((-440) // 2 + 5, -55 + y_offset),
            lineWidth=10,
            color=[0.25, 0.25, 0.25],
        )
        line4 = Line(
            win=win,
            start=(100, 70 + y_offset),
            end=((460) // 2 + 5, -55 + y_offset),
            lineWidth=20,
            color=[0.25, 0.25, 0.25],
        )

        for i in [
            line1,
            line2,
            line3,
            line4,
            img_card1,
            img_card2,
            img_card3,
            img_card4,
            img_card5,
            img_card6,
            part_3_0,
            part_3_1,
        ]:
            i.draw()

    def part_4(win, instructions):
        part_4_0 = TextBox2(
            win=win,
            text=instructions["two-step"]["4.0"],
            letterHeight=28,
            pos=(0, 75),
        )
        part_4_0.draw()

    return [part_0, part_1, part_2, part_3, part_4]
