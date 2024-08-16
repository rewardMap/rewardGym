from typing import Literal

import numpy as np
import pygame

from .stimuli import BaseText


class FormatText(BaseText):
    def __init__(
        self,
        text,
        duration,
        name=None,
        fontcolor=(0, 0, 0),
        fontsize=36,
        textposition=(0, 0),
        condition_text={1: 5, 0: [1, 2, 3, 4], 2: [6, 7, 8, 9]},
    ):
        super().__init__(text, duration, name, fontcolor, fontsize, textposition)

        self.condition_text = condition_text

    def display(self, window, clock=None, condition=None, total_reward=None, **kwargs):
        if self.font is None:
            self.font = pygame.font.Font(pygame.font.get_default_font(), self.fontsize)

        if self.condition_text is not None:
            card = np.random.choice(self.condition_text[condition])
            display_text = self.text.format(card)

        self.text_surface = self.font.render(display_text, True, self.fontcolor)
        self.text_rect = self.text_surface.get_rect(center=self.textposition)

        window.blit(self.text_surface, self.text_rect)

        pygame.event.pump()
        pygame.display.update()
        pygame.time.delay(self.duration)

        return None


class FormatTextReward(FormatText):
    def __init__(
        self,
        text,
        duration,
        name=None,
        fontcolor=(0, 0, 0),
        fontsize=36,
        textposition=(0, 0),
        target: Literal["reward", "total_reward"] = "total_reward",
    ):
        super().__init__(text, duration, name, fontcolor, fontsize, textposition)

        self.target = target

    def display(
        self,
        window,
        clock=None,
        condition=None,
        reward=None,
        total_reward=None,
        **kwargs,
    ):
        if self.font is None:
            self.font = pygame.font.Font(pygame.font.get_default_font(), self.fontsize)

        if reward is not None and self.target == "reward":
            display_text = self.text.format(reward)
        else:
            display_text = ""

        if total_reward is not None and self.target == "total_reward":
            display_text = self.text.format(total_reward)
        else:
            display_text = ""

        self.text_surface = self.font.render(display_text, True, self.fontcolor)
        self.text_rect = self.text_surface.get_rect(center=self.textposition)

        window.blit(self.text_surface, self.text_rect)

        pygame.event.pump()
        pygame.display.update()
        pygame.time.delay(self.duration)

        return None


class FormatTextRiskSensitive(BaseText):
    def __init__(
        self,
        text,
        duration,
        name=None,
        fontcolor=(0, 0, 0),
        fontsize=36,
        textposition=(0, 0),
        condition_text={1: 5, 0: [1, 2, 3, 4], 2: [6, 7, 8, 9]},
        letter_map={0: "A", 1: "B", 2: "C", 3: "D", 4: "E"},
    ):
        super().__init__(text, duration, name, fontcolor, fontsize, textposition)

        self.condition_text = condition_text
        self.letter_map = letter_map

    def display(self, window, clock=None, condition=None, **kwargs):
        if self.font is None:
            self.font = pygame.font.Font(pygame.font.get_default_font(), self.fontsize)

        if self.condition_text is not None:
            if len(self.condition_text[condition].keys()) == 1:
                letA = self.letter_map[self.condition_text[condition][0]]
                letB = ""
            else:
                letA = self.letter_map[self.condition_text[condition][0]]
                letB = self.letter_map[self.condition_text[condition][1]]

            display_text = self.text.format(letA, letB)

        self.text_surface = self.font.render(display_text, True, self.fontcolor)
        self.text_rect = self.text_surface.get_rect(center=self.textposition)

        window.blit(self.text_surface, self.text_rect)

        pygame.event.pump()
        pygame.display.update()
        pygame.time.delay(self.duration)

        return None


def feedback_block(center, duration_reward=1000, duration_total=500):
    cur_reward = FormatTextReward(
        "You gain: {0}",
        duration_reward,
        target="reward",
        textposition=center,
    )

    total_reward = FormatTextReward(
        "You have gained: {0}",
        duration_total,
        textposition=center,
        target="total_reward",
    )

    return cur_reward, total_reward
