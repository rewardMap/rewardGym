from typing import Protocol, runtime_checkable

try:
    from psychopy import core
except ImportError:
    core = None


@runtime_checkable
class KeysProtocol(Protocol):
    name: str
    rt: float
    tDown: float
    duration: float


@runtime_checkable
class KeyboardProtocol(Protocol):
    def getKeys(
        self, keyList=None, waitRelease=True, clear=True
    ) -> list[KeysProtocol]: ...


@runtime_checkable
class InputProtocol(Protocol):
    """
    Protocol for Keyboard handling
    """

    def get_keys(self) -> list[tuple[str, float]]: ...

    def simulate_keys(self, key, rt) -> list[tuple[str, float]]: ...

    def interpret_keys(
        self, key_presses: list[tuple[str, float]], keylist: list[str], logger, **kwargs
    ) -> tuple[str, float] | None: ...


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
        self, key_presses, keylist: list[str], logger, **kwargs
    ) -> tuple[str, float] | None:
        response = None

        if key_presses:
            for resp in key_presses:
                if resp[0] == self.kill_switch:
                    # Closes the window, closes the file and quits psychopy.
                    logger.close()
                    self._close(**kwargs)

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

                elif resp[0] in keylist:
                    # Potentially dangerous - if press is in list, return!
                    response = (resp[0], resp[1])

                else:
                    logger.log_event(
                        {
                            "event_type": "button-press",
                            "response_button": resp[0],
                            "response_time": resp[1] - logger._trial_start,
                        },
                    )

            return response
        else:
            return response

    def _close(self, **kwargs):
        pass


class PsychoPyInput(BaseInputHandler):
    def __init__(
        self,
        clock,
        keyboard: KeysProtocol | None = None,
        kill_switch: str = "q",
        mr_trigger: str = "5",
        repetition_time: float = 2,
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

    def get_keys(self) -> list[tuple[str, float]]:
        keys = [(i.name, i.rt) for i in self.interface.getKeys()]
        return keys

    def _close(self, win=None, **kwargs):
        if win is not None:
            win.close()
        if core is not None:
            core.quit()
