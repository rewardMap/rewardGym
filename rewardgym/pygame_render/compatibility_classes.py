from collections import deque

from ..optional_dependencies import pygame, require_pygame


class PygameWindow:
    def __init__(
        self,
        size=(1200, 800),
        color=(128, 128, 128),
        caption="Experiment",
    ):
        require_pygame()

        pygame.init()
        pygame.font.init()

        self.width = size[0]
        self.height = size[1]

        self.background_color = color

        self.screen = pygame.display.set_mode(size)

        pygame.display.set_caption(caption)

        self._draw_queue = []
        self._auto_draw = []
        self._flip_callbacks = deque()

    def register_draw(self, stim):
        self._draw_queue.append(stim)

    def register_auto_draw(self, stim):
        self._auto_draw.append(stim)

    def unregister_auto_draw(self, stim):
        try:
            self._auto_draw.remove(stim)
        except ValueError:
            pass

    def callOnFlip(self, callback, *args, **kwargs):
        self._flip_callbacks.append((callback, args, kwargs))

    def flip(self):
        self.screen.fill(self.background_color)

        for stim in self._auto_draw:
            stim._render()

        for stim in self._draw_queue:
            stim._render()

        self._draw_queue.clear()

        pygame.display.flip()

        while self._flip_callbacks:
            callback, args, kwargs = self._flip_callbacks.popleft()
            callback(*args, **kwargs)

    def close(self):
        pygame.display.quit()

    def psychopy_to_pygame(self, pos):
        x = self.width / 2 + pos[0]
        y = self.height / 2 - pos[1]

        return x, y
