import numpy as np
import pygame

from .stimuli import BaseText


class FormatText(BaseText):
    def __init__(
        self,
        text,
        time,
        name=None,
        background=(127, 127, 127),
        fontcolor=(0, 0, 0),
        fontsize=36,
        textposition=(0, 0),
        condition_text={1: 5, 0: [1, 2, 3, 4], 2: [6, 7, 8, 9]},
    ):
        super().__init__(
            text, time, name, background, fontcolor, fontsize, textposition
        )

        self.condition_text = condition_text

    def __call__(self, window, clock=None, condition=None, reward=None, **kwargs):

        window.fill(self.background)

        if self.font is None:
            self.font = pygame.font.Font(pygame.font.get_default_font(), self.fontsize)

        if self.condition_text is not None:
            card = np.random.choice(self.condition_text[condition])
            display_text = self.text.format(card)

        elif reward is not None:
            display_text = self.text.format(reward)

        self.text_surface = self.font.render(display_text, True, self.fontcolor)
        self.text_rect = self.text_surface.get_rect(center=self.textposition)

        window.blit(self.text_surface, self.text_rect)

        pygame.event.pump()
        pygame.display.update()
        pygame.time.delay(self.time)

        return None


class FormatTextMid(FormatText):
    def __call__(self, window, clock=None, condition=None, reward=None, location=None):

        window.fill(self.background)

        if self.font is None:
            self.font = pygame.font.Font(pygame.font.get_default_font(), self.fontsize)

        if self.condition_text is not None:
            card = np.random.choice(self.condition_text[location])
            display_text = self.text.format(card)

        elif reward is not None:
            display_text = self.text.format(reward)

        self.text_surface = self.font.render(display_text, True, self.fontcolor)
        self.text_rect = self.text_surface.get_rect(center=self.textposition)

        window.blit(self.text_surface, self.text_rect)

        pygame.event.pump()
        pygame.display.update()
        pygame.time.delay(self.time)

        return None
