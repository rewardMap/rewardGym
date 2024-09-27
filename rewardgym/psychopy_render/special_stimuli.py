from typing import Dict, Union

from .stimuli import ActionStimulus

try:
    from psychopy.visual import TextStim, Window
except ModuleNotFoundError:
    from .psychopy_stubs import Window, TextStim

from .logger import ExperimentLogger


class ActionStimulusTooEarly(ActionStimulus):
    """
    Stimulus class, for when actions are required by the participants.
    """

    def __init__(
        self,
        duration: float,
        key_dict: Dict = {"left": 0, "right": 1},
        name: str = "response",
        timeout_action: int = None,
        name_timeout="response-time-out",
        name_tooearly="response-too-early",
        text_tooearly={
            "text": "Don't press too early!",
            "pos": (0, -150),
            "height": 28,
            "color": "white",
        },
    ):
        """
        Setting up the action object.

        Parameters
        ----------
        duration : float
            Duration of the response window.
        key_dict : dict, optional
            Dictionary to map keyboard responses to actions recognized by the environment, by default {"left": 0, "right": 1}
        name : str, optional
            name of the object, will be used for logging, by default None
        timeout_action : int, optional
            Behavior of the object if the response window times out, making it possible that no response is also a distinc action, by default None
        """

        super().__init__(
            name=name,
            duration=duration,
            key_dict=key_dict,
            timeout_action=timeout_action,
            name_timeout=name_timeout,
        )

        self.name_tooearly = name_tooearly
        self.text_tooearly = text_tooearly

    def setup(self, win: Window = None, **kwargs):
        """
        Does not need a special setup, including the function, to make easy looping possible.

        Parameters
        ----------
        win : Window, optional
            The psychopy window object that is used for displaying stimuli, by default None
        """

        self.text_stim = TextStim(win=win, **self.text_tooearly)

    def display(
        self, win: Window, logger: ExperimentLogger, **kwargs
    ) -> Union[int, str]:
        """
        Calls the stimulus object. In this case waiting for a specific response,
        returning it and logging the process. Flipping the window in the end.


        Parameters
        ----------
        win : Window
            The psychopy window object that is used for displaying stimuli.
        logger : ExperimentLogger
            The logger associated with the experiment.

        Returns
        -------
        Union[int, str]
            The response issued by the participant, interpretable by the environment.
        """

        response_window_onset = logger.get_time()
        response_window = response_window_onset + self.duration
        response_present = False
        remaining = None

        response = logger.key_strokes(win, keyList=self.key_list)

        if response:
            RTE = response[1] - response_window_onset
            logger.log_event(
                {
                    "event_type": self.name_tooearly,
                    "response_button": response[0],
                    "response_time": RTE,
                },
                onset=response_window_onset,
            )
            self.text_stim.draw()
        else:
            RTE = False

        # clearing buffer
        logger.key_strokes(win)

        # Main loop, keeping time and waiting for response.
        while response_window > logger.get_time() and response_present is False:
            response = logger.key_strokes(win, keyList=self.key_list)

            if response:
                RT = response[1] - response_window_onset
                logger.log_event(
                    {
                        "event_type": self.name,
                        "response_button": response[0],
                        "response_time": RT,
                    },
                    onset=response_window_onset,
                )
                response_present = True
                response_key = self.key_dict[response[0]]

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
                    "response_button": response_key,
                },
                onset=response_window_onset,
            )

            if response_key == logger.na:
                return None

        if RTE:
            response_key = self.timeout_action
            self.text_stim.draw()
        else:
            win.flip()

        return response_key, remaining
