from ..reward_classes import BaseReward


class HCPReward(BaseReward):
    def __init__(self, reward_range=[-0.5, 0.0, 1.0]):
        self.reward_range = reward_range

    def _reward_function(self, condition):
        reward = self.reward_range[condition]
        return reward

    def __call__(self, condition):
        return self._reward_function(condition)


def get_hcp(conditions=None, render_backend=None, window_size=None, reward=HCPReward()):

    environment_graph = {
        0: [1, 2],  # go - win
        1: [],  # no go win
        2: [],  # go - no punish
    }

    reward_structure = {1: reward, 2: reward}

    if conditions is None:
        condition_out = (([0, 1, 2], [0.45, 0.1, 0.45]), [0])

    if render_backend is None:
        info_dict = {}

    elif render_backend == "pygame":

        if window_size is None:
            return ValueError("window_size needs to be defined!")

        from ..pygame_render.stimuli import BaseAction, BaseDisplay, BaseText
        from ..pygame_render.task_stims import FormatText

        base_postion = (window_size // 2, window_size // 2)

        left_text = {1: [5], 2: [1, 2, 3, 4], 0: [6, 7, 8, 9]}
        right_text = {1: [5], 0: [1, 2, 3, 4], 2: [6, 7, 8, 9]}

        reward_text = {0: [-0.5], 1: [0], 2: [1]}
        reward_disp = FormatText(
            "You gain: {0}", 1000, condition_text=reward_text, textposition=base_postion
        )

        earnings_text = FormatText(
            "You have gained: {0}", 500, condition_text=None, textposition=base_postion
        )

        info_dict = {
            0: {
                "human": [
                    BaseDisplay(None, 1),
                    BaseText("+", 1000, textposition=base_postion),
                    BaseDisplay(None, 1),
                    BaseText("< or >", 500, textposition=base_postion),
                    BaseAction(),
                ]
            },
            1: {
                "human": [
                    BaseDisplay(None, 1),
                    BaseText("<", 1000, textposition=base_postion),
                    FormatText(
                        "Card: {0}",
                        1000,
                        condition_text=left_text,
                        textposition=base_postion,
                    ),
                    reward_disp,
                    earnings_text,
                ]
            },
            2: {
                "human": [
                    BaseDisplay(None, 1),
                    BaseText(">", 1000, textposition=base_postion),
                    FormatText(
                        "Card: {0}",
                        1000,
                        condition_text=right_text,
                        textposition=base_postion,
                    ),
                    reward_disp,
                    earnings_text,
                ]
            },
        }

    elif render_backend == "psychopy":
        raise NotImplementedError("Psychopy integration still under deliberation.")

    return environment_graph, reward_structure, condition_out, info_dict
