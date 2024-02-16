import sys
from typing import Tuple, Type

import pygame


class BaseDisplay:
    def __init__(
        self,
        image: str,
        duration: int,
        name: str = None,
        background: Tuple[int] = (127, 127, 127),
    ) -> None:
        self.image_path = image
        self.duration = duration
        self.image = None
        self.name = name
        self.display_type = "image"
        self.background = background

    def __call__(
        self,
        window: Type[pygame.surface.Surface],
        clock: Type[pygame.time.Clock] = None,
        condition: int = None,
        **kwargs
    ) -> None:

        window.fill(self.background)

        if self.image_path is not None:
            if self.image is None:
                self.image = pygame.image.load(self.image_path).convert()

            window.blit(
                self.image, self.image.get_rect(center=window.get_rect().center)
            )

        pygame.event.pump()
        pygame.display.update()
        pygame.time.delay(self.duration)

        return None


class BaseAction:
    def __init__(
        self, action_map: dict = {pygame.K_LEFT: 0, pygame.K_RIGHT: 1}, name: str = None
    ):
        self.action_map = action_map
        self.allowed_keys = action_map.keys()
        self.display_type = "action"
        self.name = name

    def __call__(
        self,
        window: Type[pygame.surface.Surface],
        clock: Type[pygame.time.Clock] = None,
        condition: int = None,
        **kwargs
    ) -> int:

        pygame.event.clear()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_q:
                        pygame.display.quit()
                        pygame.quit()
                        sys.exit()

                    elif event.key in self.allowed_keys:
                        return self.action_map[event.key]


class BaseText:
    def __init__(
        self,
        text: str,
        duration: int,
        name: str = None,
        fontcolor: Tuple[int, int, int] = (0, 0, 0),
        fontsize: int = 36,
        textposition: Tuple[int, int] = (0, 0),
    ):
        self.font = None
        self.text = text
        self.duration = duration
        self.name = name
        self.display_type = "text"
        self.textposition = textposition
        self.fontsize = fontsize
        self.text_surface = None
        self.fontcolor = fontcolor

    def __call__(
        self,
        window: Type[pygame.surface.Surface],
        clock: Type[pygame.time.Clock] = None,
        condition: int = None,
        **kwargs
    ) -> None:

        if self.font is None:
            self.font = pygame.font.Font(pygame.font.get_default_font(), self.fontsize)
            self.text_surface = self.font.render(self.text, True, self.fontcolor)
            self.text_rect = self.text_surface.get_rect(center=self.textposition)

        window.blit(self.text_surface, self.text_rect)

        pygame.event.pump()
        pygame.display.update()
        pygame.time.delay(self.duration)

        return None


class TimedAction:
    def __init__(
        self,
        duration: int,
        action_map: dict = {pygame.K_SPACE: 0},
        timeout_action: int = 1,
        name: str = None,
    ):
        self.action_map = action_map
        self.allowed_keys = action_map.keys()
        self.display_type = "action"
        self.duration = duration
        self.name = name
        self.timeout_action = timeout_action

    def __call__(
        self,
        window: Type[pygame.surface.Surface],
        clock: Type[pygame.time.Clock] = None,
        **kwargs
    ) -> int:

        pygame.event.clear()
        current_time = pygame.time.get_ticks()
        response = None

        while current_time + self.duration >= pygame.time.get_ticks():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_q:
                        pygame.display.quit()
                        pygame.quit()
                        sys.exit()

                    elif event.key in self.allowed_keys:
                        response = True
                        return self.action_map[event.key]

        if response is None:
            return self.timeout_action
