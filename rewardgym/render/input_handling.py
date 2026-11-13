import time

from ..optional_dependencies import core, pygame, require_pygame
from ..protocols import InputProtocol, KeyboardProtocol


class BaseInputHandler(InputProtocol):
    def __init__(
        self, kill_switch: str = "q", mr_trigger: str = "5", repetition_time: float = 2
    ) -> None:
        self.kill_switch = kill_switch
        self.mr_trigger = mr_trigger
        self.interface = None
        self.tr_pulses = 0
        self.repetition_time = repetition_time

    def get_keys(self) -> list[tuple[str, float]]:
        raise NotImplementedError("Use one of the other classes to get keys")

    def simulate_keys(self, key, rt) -> list[tuple[str, float]]:
        return [(key, rt)]

    def interpret_keys(
        self, key_presses, logger, key_list: None | list[str] = None, **kwargs
    ) -> tuple[str, float] | None:
        response = None
        if key_presses:
            for resp in key_presses:
                if resp[0] == self.kill_switch:
                    # Closes the window, closes the file and quits psychopy.
                    logger.close()
                    self._close()

                elif resp[0] == self.mr_trigger:
                    self.tr_pulses += 1
                    expected_time = logger.get_time() - (
                        self.tr_pulses * self.repetition_time
                    )
                    # ugly fix!
                    logger.log_event(
                        {
                            "event_type": "TR",
                            "response_button": resp[0],
                            "response_time": logger.get_time(),
                            "expected_duration": expected_time,
                            "TR": self.tr_pulses,
                        },
                    )

                elif (key_list is not None) and (resp[0] in key_list):
                    # Potentially dangerous - if press is in list, return!
                    response = (resp[0], resp[1])
                    return response

                else:
                    logger.log_event(
                        {
                            "event_type": "button-press",
                            "response_button": resp[0],
                            "response_time": resp[1] - logger._trial_start,
                        },
                    )

        else:
            return response

    def key_strokes(
        self, logger, key_list: list[str] | None = None
    ) -> tuple[str, float] | None:
        responses = self.get_keys()
        response = self.interpret_keys(responses, logger=logger, key_list=key_list)

        return response

    def _close(self):
        pass


class SimulationInput(BaseInputHandler):
    def get_keys(self) -> list[tuple[str, float]]:
        return []


class PsychoPyInput(BaseInputHandler):
    def __init__(
        self,
        clock,
        keyboard: KeyboardProtocol | None = None,
        kill_switch: str = "q",
        mr_trigger: str = "5",
        repetition_time: float = 2,
        win=None,
    ) -> None:
        if keyboard is None:
            from psychopy.hardware.keyboard import Keyboard

            keyboard = Keyboard(clock=clock)

        super().__init__(
            kill_switch=kill_switch,
            mr_trigger=mr_trigger,
            repetition_time=repetition_time,
        )

        self.interface = keyboard
        self.win = win

    def get_keys(self) -> list[tuple[str, float]]:
        keys = [(i.name, i.rt) for i in self.interface.getKeys()]
        return keys

    def _close(self):
        if self.win is not None:
            self.win.close()
        if core is not None:
            core.quit()


class PygameInput(BaseInputHandler):
    def __init__(self, win=None, *args, **kwargs):
        require_pygame()

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
