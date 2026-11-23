from ..protocols import InputProtocol


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
