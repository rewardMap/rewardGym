import sys
from typing import Tuple

import pygame


class BaseDisplay:
    def __init__(
        self,
        image: str,
        time: int,
        name: str = None,
        background: Tuple[int] = (127, 127, 127),
    ) -> None:
        self.image_path = image
        self.time = time
        self.image = None
        self.name = name
        self.display_type = "image"
        self.background = background

    def __call__(
        self,
        window: type[pygame.surface.Surface],
        clock: type[pygame.time.Clock] = None,
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
        pygame.time.delay(self.time)

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
        window: type[pygame.surface.Surface],
        clock: type[pygame.time.Clock] = None,
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
        time: int,
        name: str = None,
        background: Tuple[int, int, int] = (127, 127, 127),
        fontcolor: Tuple[int, int, int] = (0, 0, 0),
        fontsize: int = 36,
        textposition: Tuple[int, int] = (0, 0),
    ):
        self.font = None
        self.text = text
        self.time = time
        self.name = name
        self.display_type = "text"
        self.textposition = textposition
        self.background = background
        self.fontsize = fontsize
        self.text_surface = None
        self.fontcolor = fontcolor

    def __call__(
        self,
        window: type[pygame.surface.Surface],
        clock: type[pygame.time.Clock] = None,
        condition: int = None,
        **kwargs
    ) -> None:

        window.fill(self.background)

        if self.font is None:
            self.font = pygame.font.Font(pygame.font.get_default_font(), self.fontsize)
            self.text_surface = self.font.render(self.text, True, self.fontcolor)
            self.text_rect = self.text_surface.get_rect(center=self.textposition)

        window.blit(self.text_surface, self.text_rect)

        pygame.event.pump()
        pygame.display.update()
        pygame.time.delay(self.time)

        return None
