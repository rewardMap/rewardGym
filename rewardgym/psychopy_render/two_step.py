import os

try:
    from psychopy.visual import ImageStim
    from psychopy.visual.rect import Rect
except ModuleNotFoundError:
    from .psychopy_stubs import Rect, ImageStim

import matplotlib.pyplot as plt
import numpy as np

from ..utils import check_seed
from . import STIMPATH
from .default_images import (
    fixation_cross,
    generate_stimulus_properties,
    make_card_stimulus,
)
from .stimuli import ActionStimulus, BaseStimulus, FeedBackStimulus, ImageStimulus


class TwoStepDisplay(BaseStimulus):
    def __init__(
        self,
        duration,
        name=None,
        positions=((0, 0), (0, 0)),
        selected=None,
        images=[
            os.path.join(STIMPATH, "risk_sensitive", "stim1.png"),
            os.path.join(STIMPATH, "risk_sensitive", "stim2.png"),
        ],
    ):
        super().__init__(name=name, duration=duration)

        self.positions = positions
        self.images = images
        self.selected = selected

    def setup(self, win, **kwargs):
        self.image_class = []
        for img, pos in zip(self.images, self.positions):
            if isinstance(img, str):
                self.image_class.append(ImageStim(win=win, image=img, pos=pos))
            else:
                self.image_class.append(
                    ImageStim(
                        win, image=img, size=(img.shape[1], img.shape[0]), pos=pos
                    )
                )

    def display(self, win, logger, action, **kwargs):
        logger.key_strokes(win)
        stim_onset = logger.get_time()

        # Reset image positions
        for im, po in zip(self.image_class, self.positions):
            im.setPos(po)

        imgA = self.image_class[0]
        imgA.setOpacity(1.0)

        imgB = self.image_class[1]
        imgB.setOpacity(1.0)

        if action is not None:
            if action == 0:
                feedback = Rect(
                    win=win,
                    width=imgA.size[0],
                    height=imgA.size[1],
                    lineColor="white",
                    lineWidth=7,
                    pos=imgA.pos,
                )

                imgB.setOpacity(0.25)

            else:
                feedback = Rect(
                    win=win,
                    width=imgB.size[0],
                    height=imgB.size[1],
                    lineColor="white",
                    lineWidth=7,
                    pos=imgB.pos,
                )

                imgA.setOpacity(0.25)

            feedback.draw()

        imgA.draw()
        imgB.draw()

        for img in self.image_class[2:]:
            img.draw()

        win.flip()

        logger.wait(win, self.duration, stim_onset)

        logger.log_event(
            {"event_type": self.name, "expected_duration": self.duration},
            onset=stim_onset,
        )

        return None


def get_info_dict(seed=None, **kwargs):
    seed = check_seed(seed)
    colors = [tuple([int(i * 255) for i in c]) for c in plt.cm.tab10.colors[:5]]
    set_colors = seed.choice(np.arange(len(colors[:-1])), 3, replace=False)

    stim_set = {}
    for n in range(3):
        stim_set[n] = [
            generate_stimulus_properties(
                random_state=seed,
                colors=[tuple(colors[set_colors[n]])] * 4,
                patterns=[(1, 1), (2, 2)],
            )
            for i in range(2)
        ]
        stim_set[n] = [
            make_card_stimulus(stim_set[n][k], width=300, height=300) for k in range(2)
        ]

    reward_feedback = FeedBackStimulus(
        1.0, text="You gain: {0}", target="reward", name="reward"
    )
    total_reward_feedback = FeedBackStimulus(
        1.0, text="You have gained: {0}", target="total_reward", name="reward-total"
    )

    fix = ImageStimulus(
        image_paths=[fixation_cross()],
        duration=0.1,
        autodraw=True,
        name="initial-fixation",
    )
    fix_iti = BaseStimulus(duration=1.5, name="iti")

    fix2 = ImageStimulus(
        image_paths=[fixation_cross()],
        duration=0.5,
        autodraw=True,
        name="transition",
    )

    image_shift = 300

    final_step = [reward_feedback, total_reward_feedback, fix_iti]

    info_dict = {
        0: {
            "psychopy": [
                fix,
                TwoStepDisplay(
                    duration=0.1,
                    name="decision-0",
                    images=[
                        stim_set[0][0],
                        stim_set[0][1],
                    ],
                    positions=[(-image_shift, 0), (image_shift, 0)],
                ),
                ActionStimulus(duration=2.0),
            ]
        },
        1: {
            "psychopy": [
                TwoStepDisplay(
                    duration=0.75,
                    name="environment-select",
                    images=[
                        stim_set[0][0],
                        stim_set[0][1],
                    ],
                    positions=[(-image_shift, 0), (image_shift, 0)],
                ),
                fix2,
                ImageStimulus(
                    duration=0.1,
                    name="environment-decision",
                    image_paths=[
                        stim_set[1][0],
                        stim_set[1][1],
                    ],
                    positions=[(-image_shift, 0), (image_shift, 0)],
                ),
                ActionStimulus(duration=2.0),
            ]
        },
        2: {
            "psychopy": [
                TwoStepDisplay(
                    duration=0.75,
                    name="environment-select",
                    images=[
                        stim_set[0][0],
                        stim_set[0][1],
                    ],
                    positions=[(-image_shift, 0), (image_shift, 0)],
                ),
                fix2,
                ImageStimulus(
                    duration=0.1,
                    name="environment-decision",
                    image_paths=[
                        stim_set[2][0],
                        stim_set[2][1],
                    ],
                    positions=[(-image_shift, 0), (image_shift, 0)],
                ),
                ActionStimulus(duration=2.0),
            ]
        },
        3: {
            "psychopy": [
                TwoStepDisplay(
                    duration=0.5,
                    name="stimulus-select",
                    images=[
                        stim_set[1][0],
                        stim_set[1][1],
                    ],
                    positions=[(-image_shift, 0), (image_shift, 0)],
                )
            ]
            + final_step
        },
        4: {
            "psychopy": [
                TwoStepDisplay(
                    duration=0.5,
                    name="stimulus-select",
                    images=[
                        stim_set[1][0],
                        stim_set[1][1],
                    ],
                    positions=[(-image_shift, 0), (image_shift, 0)],
                )
            ]
            + final_step
        },
        5: {
            "psychopy": [
                TwoStepDisplay(
                    duration=0.5,
                    name="stimulus-select",
                    images=[
                        stim_set[2][0],
                        stim_set[2][1],
                    ],
                    positions=[(-image_shift, 0), (image_shift, 0)],
                )
            ]
            + final_step
        },
        6: {
            "psychopy": [
                TwoStepDisplay(
                    duration=0.5,
                    name="stimulus-select",
                    images=[
                        stim_set[2][0],
                        stim_set[2][1],
                    ],
                    positions=[(-image_shift, 0), (image_shift, 0)],
                )
            ]
            + final_step
        },
    }

    return info_dict, None
