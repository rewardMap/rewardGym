import time
from collections import deque

import pygame

from ....logging import ExperimentLogger
from ....protocols import DisplayProtocol
from ...input_handling import BaseInputHandler
from ...timing import wait
from ..backend_base import EnvironmentContext, RewardGymBackend
from .factory_pygame import PygameFactory


class PygameBackend(RewardGymBackend):
    mode = "pygame"

    def setup(self, context: EnvironmentContext):
        if context.window is None:
            context.window = PygameWindow()

        if context.input_handler is None:
            context.input_handler = PygameInput(win=context.window)

        if context.logger is None:
            from psylog.interfaces import SystemClock

            context.logger = ExperimentLogger(file_name=None, clock=SystemClock())

        if context.render is None:
            context.render = PygameDisplay(context.window)

        context.stimuli = PygameFactory()


class PygameDisplay(DisplayProtocol):
    def __init__(self, window, **kwargs):
        self.win = window

    def flip(self):
        self.win.flip()

    def schedule_on_flip(
        self,
        callback,
        *args,
        **kwargs,
    ):
        self.win.callOnFlip(
            callback,
            *args,
            **kwargs,
        )

    def wait(self, *args, **kwargs):
        return wait(
            *args,
            **kwargs,
        )


class PygameWindow:
    def __init__(
        self,
        size=(1200, 800),
        color=(128, 128, 128),
        caption="Experiment",
    ):
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


class PygameInput(BaseInputHandler):
    def __init__(self, win=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_time = time.perf_counter()
        self.win = win

    def get_keys(self):
        out = []

        now = time.perf_counter() - self.start_time

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                out.append(
                    (
                        pygame.key.name(event.key),
                        now,
                    )
                )

            elif event.type == pygame.QUIT:
                out.append(
                    (
                        self.kill_switch,
                        now,
                    )
                )

        return out

    def _close(self):
        if self.win is not None:
            self.win.close()
        pygame.quit()

        raise ExperimentQuit()


class ExperimentQuit(Exception):
    pass
