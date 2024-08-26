try:
    from psychopy.visual import ImageStim
    from psychopy.visual.rect import Rect
except ModuleNotFoundError:
    from .psychopy_stubs import Rect, ImageStim

from ..utils import check_seed
from .default_images import (
    fixation_cross,
    generate_stimulus_properties,
    make_card_stimulus,
)
from .stimuli import ActionStimulus, BaseStimulus, FeedBackStimulus, ImageStimulus


class RiskSensitiveDisplay(BaseStimulus):
    def __init__(
        self,
        duration,
        name=None,
        image_position=(0, 0),
        image_shift=350,
        with_action=False,
        image_map={
            1: make_card_stimulus(generate_stimulus_properties(1)),
            2: make_card_stimulus(generate_stimulus_properties(2)),
            3: make_card_stimulus(generate_stimulus_properties(3)),
            4: make_card_stimulus(generate_stimulus_properties(4)),
            5: make_card_stimulus(generate_stimulus_properties(5)),
        },
    ):
        super().__init__(name=name, duration=duration)

        self.image_position = image_position
        self.image_map = image_map
        self.image_shift = image_shift
        self.with_action = with_action

    def setup(self, win, **kwargs):
        self.image_dict = {}

        for kk in self.image_map.keys():
            if isinstance(self.image_map[kk], str):
                self.image_dict[kk] = ImageStim(win=win, image=self.image_map[kk])
            else:
                self.image_dict[kk] = ImageStim(
                    win,
                    image=self.image_map[kk],
                    size=(self.image_map[kk].shape[1], self.image_map[kk].shape[0]),
                )

    def display(self, win, logger, condition, action=None, **kwargs):
        state1 = condition[0][0] if 0 in condition[0].keys() else None
        state2 = condition[0][1] if 1 in condition[0].keys() else None

        logger.key_strokes(win)
        stim_onset = logger.get_time()

        if state1 is not None:
            imgA = self.image_dict[state1]
            imgA.pos = (-self.image_shift, self.image_position[1])
            imgA.setOpacity(1.0)
        else:
            imgA = None

        if state2 is not None:
            imgB = self.image_dict[state2]
            imgB.pos = (self.image_shift, self.image_position[1])
            imgB.setOpacity(1.0)
        else:
            imgB = None

        if self.with_action:
            if action == 0:
                feedback = Rect(
                    win=win,
                    width=imgA.size[0],
                    height=imgA.size[1],
                    lineColor="white",
                    lineWidth=7,
                    pos=imgA.pos,
                )

                if imgB is not None:
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

                if imgA is not None:
                    imgA.setOpacity(0.25)

            feedback.draw()

        if imgA is not None:
            imgA.draw()

        if imgB is not None:
            imgB.draw()

        win.flip()

        logger.wait(win, self.duration, stim_onset)

        logger.log_event(
            {"event_type": self.name, "expected_duration": self.duration},
            onset=stim_onset,
        )

        return None


def get_info_dict(seed=111, key_dict={"left": 0, "right": 1}, **kwargs):
    random_state = check_seed(seed)

    stim_properties = [generate_stimulus_properties(random_state) for _ in range(5)]
    image_map = {}
    stimuli = {}

    for n in range(5):
        image_map[n + 1] = make_card_stimulus(stim_properties[n])
        stimuli[n + 1] = stim_properties[n]

    reward_feedback = FeedBackStimulus(
        1.0, text="{0}", target="reward", name="reward", position=(0, 120)
    )
    total_reward_feedback = FeedBackStimulus(
        1.0,
        text="Total: {0}",
        target="total_reward",
        name="reward-total",
        position=(0, 120),
        font_height=35,
    )
    base_stim = ImageStimulus(
        image_paths=[fixation_cross()], duration=0.1, name=None, autodraw=True
    )
    fix_iti = BaseStimulus(duration=1.5, name="iti")

    cue_disp = RiskSensitiveDisplay(0.05, name="cue", image_map=image_map)
    sel_disp = RiskSensitiveDisplay(
        1.5, with_action=True, name="selected", image_map=image_map
    )

    final_step = [sel_disp, reward_feedback, total_reward_feedback, fix_iti]

    info_dict = {
        0: {
            "psychopy": [
                base_stim,
                cue_disp,
                ActionStimulus(duration=2.0, timeout_action=None, key_dict=key_dict),
            ]
        },
        1: {"psychopy": final_step},
        2: {"psychopy": final_step},
        3: {"psychopy": final_step},
        4: {"psychopy": final_step},
        5: {"psychopy": final_step},
    }

    return info_dict, stimuli
