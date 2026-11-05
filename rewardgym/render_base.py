from abc import ABC, abstractmethod

from .environments import StepContext
from .protocols import InputProtocol, LoggerProtocol


class PresentationRoutine(ABC):
    """Base class for all stimuli with context-aware presentation"""

    def __init__(
        self,
        name: str | None = None,
        duration: float | None = None,
        rl_label: str | None = None,
        noflip=False,
    ):
        self.name = name
        self.duration = duration
        self.rl_label = rl_label
        self.is_setup = False
        self.noflip = noflip
        self.returns_action = False

    def present(self, context: StepContext):
        """Public method that handles context-aware presentation"""
        if "simulate" in context.env_context.mode:
            return self.simulate(context)
        return self.display(context)

    def setup(self, win, **kwargs):
        """Setup the stimulus with required resources"""
        self._setup(win, **kwargs)
        self.is_setup = True

    @abstractmethod
    def _setup(self, win, **kwargs):
        """Internal setup implementation"""

    @abstractmethod
    def display(self, context: StepContext):
        """Actual display implementation"""

    @abstractmethod
    def simulate(self, context: StepContext):
        """Simulation implementation"""

    def _log_event(self, logger, stim_onset=None, extra_info=None):
        """Common logging functionality"""
        base_dict = {
            "event_type": self.name,
            "expected_duration": self.duration,
            "rl_label": self.rl_label,
        }

        if extra_info:
            base_dict.update(extra_info)

        logger.log_event(base_dict, onset=stim_onset)


class ActionRoutine(PresentationRoutine):
    def __init__(
        self, name, duration, key_dict, rl_label, timeout_action, name_timeout, noflip
    ):
        super().__init__(name=name, duration=duration, rl_label=rl_label, noflip=noflip)

        self.key_dict = key_dict
        self.timeout_action = timeout_action
        self.name_timeout = name_timeout
        self.returns_action = True

    def _response_handling(
        self,
        input_handler: InputProtocol,
        logger: LoggerProtocol,
        response_window_onset: float,
        key_dict=None,
        info=None,
    ) -> tuple[int | None, float | None] | None:
        if self.duration is None:
            raise ValueError(f"{self.duration} needs to be defined.")

        response_window = response_window_onset + self.duration
        response_present = False
        remaining = None
        response_key = None

        if key_dict is None:
            key_dict = self.key_dict

        key_list = list(key_dict.keys())
        # Main loop, keeping time and waiting for response.
        while response_window > logger.get_time() and response_present is False:
            responses = input_handler.get_keys()
            response = input_handler.interpret_keys(
                responses, logger=logger, key_list=key_list
            )

            if response:
                RT = response[1] - response_window_onset
                response_present = True

                if info is not None and "behav_remap" in info:
                    action = info["behav_remap"][key_dict[response[0]]]
                else:
                    action = None

                response_key = key_dict[response[0]]

                logger.log_event(
                    {
                        "event_type": self.name,
                        "response_button": response[0],
                        "response_time": RT,
                        "action": action,
                        "rl_label": self.rl_label,
                    },
                    onset=response_window_onset,
                )

                remaining = self.duration - RT

        # What todo if response window timed out and now response has been given.
        if response_present is False:
            RT = None

            response_key = self.timeout_action

            if response_key is None:
                response_key = logger.na

            logger.log_event(
                {
                    "event_type": self.name_timeout,
                    "response_late": True,
                    "response_time": RT,
                    "response_button": logger.na,
                    "action": self.timeout_action,
                    "rl_label": self.rl_label,
                },
                onset=response_window_onset,
            )

            if response_key == logger.na:
                return None

        return response_key, remaining

    def _simulate_response(
        self,
        logger: LoggerProtocol,
        response_key,
        rt: float,
        response_window_onset,
        info,
    ):
        if self.duration is None:
            raise ValueError(f"{self.duration} needs to be defined.")

        if info is not None and "behav_remap" in info:
            response_button = [
                n for n, b in enumerate(info["behav_remap"]) if b == response_key
            ]
            if len(response_button) == 1:
                response_button = response_button[0]
            else:
                response_button = response_key

        else:
            response_button = response_key

        if rt is None:
            raise ValueError(
                "Simulations should run with `expose_last_stim=True`. rt cannot be 'None'!"
            )

        logger.clock.time += min([rt, self.duration])

        if rt > self.duration:
            if response_key is None:
                response_key = logger.na
                response_button = logger.na

            logger.log_event(
                {
                    "event_type": self.name_timeout,
                    "response_late": True,
                    "response_time": rt,
                    "response_button": response_button,
                    "action": response_key,
                    "rl_label": self.rl_label,
                },
                onset=response_window_onset,
            )
            response_key = self.timeout_action
            remaining = None

            if response_key is None:
                return None

        else:
            logger.log_event(
                {
                    "event_type": self.name,
                    "response_button": response_button,
                    "response_time": rt,
                    "action": response_key,
                    "rl_label": self.rl_label,
                },
                onset=response_window_onset,
            )
            remaining = self.duration - rt

        return response_key, remaining
