from __future__ import annotations

from .passive_displays import BaseStimulus

try:
    from psychopy.visual import ImageStim, TextStim, Window
    from psychopy.visual.rect import Rect
except ModuleNotFoundError:
    from .psychopy_stubs import ImageStim, Rect, TextStim, Window

from ..protocols import InputProtocol, LoggerProtocol
from ..stimuli import generate_stimulus_properties, make_card_stimulus
from ..timing import simulation_wait, wait
from ..utils import check_random_state


class ActionStimulus(BaseStimulus):
    """
    Stimulus class, for when actions are required by the participants.
    """

    def __init__(
        self,
        duration: float,
        key_dict: dict | None = None,
        name: str = "response",
        timeout_action: int | None = None,
        name_timeout="response-time-out",
        rl_label: str | None = None,
        noflip: bool = False,
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

        if key_dict is None:
            key_dict = {"left": 0, "right": 1}
        super().__init__(name=name, duration=duration, rl_label=rl_label, noflip=noflip)

        self.key_list = list(key_dict.keys())
        self.key_dict = key_dict
        self.timeout_action = timeout_action
        self.name_timeout = name_timeout
        self.entity = "action"

    def _setup(self, win: Window = None, **kwargs):
        """
        Does not need a special setup, including the function, to make easy looping possible.

        Parameters
        ----------
        win : Window, optional
            The psychopy window object that is used for displaying stimuli, by default None
        """

    def display(
        self,
        win: Window,
        logger: LoggerProtocol,
        input_handler: InputProtocol,
        info: dict,
        **kwargs,
    ) -> tuple[int | None, float | None] | None:
        """
        Calls the stimulus object. In this case waiting for a specific response,
        returning it and logging the process. Flipping the window in the end.


        Parameters
        ----------
        win : Window
            The psychopy window object that is used for displaying stimuli.
        logger : LoggerProtocol
            The logger associated with the experiment.

        Returns
        -------
        Union[int, str]
            The response issued by the participant, interpretable by the environment.
        """
        input_handler.key_strokes(logger=logger)

        response_window_onset = logger.get_time()

        response = self._response_handling(
            input_handler=input_handler,
            logger=logger,
            response_window_onset=response_window_onset,
            info=info,
        )

        if not self.noflip:
            win.flip()

        return response

    def _response_handling(
        self,
        input_handler: InputProtocol,
        logger: LoggerProtocol,
        response_window_onset: float,
        key_dict=None,
        info=None,
    ) -> tuple[int | None, float | None] | None:
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

    def simulate(
        self,
        logger: LoggerProtocol,
        key: str | None = None,
        rt: float | None = None,
        info: dict | None = None,
        **kwargs,
    ):
        response_window_onset = logger.get_time()
        response = self._simulate_response(
            logger,
            key,
            rt,
            response_window_onset=response_window_onset,
            info=info,
        )

        return response

    def _simulate_response(
        self,
        logger: LoggerProtocol,
        response_key,
        rt: float,
        response_window_onset,
        info,
    ):
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


class ActionStimulusTooEarly(ActionStimulus):
    """
    Stimulus class, for when actions are required by the participants.
    """

    def __init__(
        self,
        duration: float,
        key_dict: dict | None = None,
        name: str = "response",
        timeout_action: int | None = None,
        name_timeout="response-timeout",
        name_tooearly="response-too-early",
        text_tooearly=None,
        rl_label: str | None = None,
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

        if text_tooearly is None:
            text_tooearly = {
                "text": "Don't press too early!",
                "pos": (0, -150),
                "height": 28,
                "color": "white",
            }
        if key_dict is None:
            key_dict = {"left": 0, "right": 1}
        super().__init__(
            name=name,
            duration=duration,
            key_dict=key_dict,
            timeout_action=timeout_action,
            name_timeout=name_timeout,
            rl_label=rl_label,
        )

        self.name_tooearly = name_tooearly
        self.text_tooearly = text_tooearly

    def _setup(self, win: Window = None, **kwargs):
        """
        Does not need a special setup, including the function, to make easy looping possible.

        Parameters
        ----------
        win : Window, optional
            The psychopy window object that is used for displaying stimuli, by default None
        """

        self.text_stim = TextStim(win=win, **self.text_tooearly)

    def display(
        self,
        win: Window,
        logger: LoggerProtocol,
        input_handler: InputProtocol,
        info: dict,
        **kwargs,
    ) -> int | str:
        """
        Calls the stimulus object. In this case waiting for a specific response,
        returning it and logging the process. Flipping the window in the end.


        Parameters
        ----------
        win : Window
            The psychopy window object that is used for displaying stimuli.
        logger : LoggerProtocol
            The logger associated with the experiment.

        Returns
        -------
        Union[int, str]
            The response issued by the participant, interpretable by the environment.
        """

        response_window_onset = logger.get_time()

        key_list = list(self.key_dict.keys())
        responses = input_handler.get_keys()
        response = input_handler.interpret_keys(
            responses, logger=logger, key_list=key_list
        )

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
        input_handler.key_strokes(logger=logger)

        response = self._response_handling(
            input_handler, logger, response_window_onset, info=info
        )

        if response is not None:
            response_key, remaining = response

            if RTE:
                response_key = self.timeout_action
                self.text_stim.draw()
            else:
                win.flip()

            return response_key, remaining

        else:
            return response


class TwoStimuliWithResponseAndSelection(ActionStimulus):
    def __init__(
        self,
        duration: float,
        key_dict: dict | None = None,
        name: str = "response",
        name_phase1: str | None = None,
        name_phase2: str | None = None,
        duration_phase1: float = 0.0,
        duration_phase2: float = 0.0,
        timeout_action: int | None = None,
        name_timeout="response-time-out",
        positions=((0, 0), (0, 0)),
        images=None,
        flip_probability=0.5,
        random_state=111,
        rl_label: str | None = None,
        rl_label_phase1: str | None = None,
        rl_label_phase2: str | None = None,
    ):
        if images is None:
            images = [
                make_card_stimulus(generate_stimulus_properties(12)),
                make_card_stimulus(generate_stimulus_properties(23)),
            ]
        if key_dict is None:
            key_dict = {"left": 0, "right": 1}
        super().__init__(
            name=name,
            duration=duration,
            key_dict=key_dict,
            timeout_action=timeout_action,
            name_timeout=name_timeout,
            rl_label=rl_label,
        )

        self.images = images
        self.positions = positions
        self.name_phase1 = name_phase1
        self.name_phase2 = name_phase2
        self.duration_phase1 = duration_phase1
        self.duration_phase2 = duration_phase2
        self.rl_label_phase1 = rl_label_phase1
        self.rl_label_phase2 = rl_label_phase2
        self.flip_probability = flip_probability
        self.random_state = check_random_state(random_state)

    def _setup(self, win, **kwargs):
        self.image_class = []
        for img, pos in zip(self.images, self.positions):
            if isinstance(img, str):
                self.image_class.append(ImageStim(win=win, image=img, pos=pos))
            else:
                self.image_class.append(
                    ImageStim(
                        win, image=img, size=(img.shape[1], img.shape[0]), pos=pos
                    )
                )

    def display(self, win, logger, input_handler, info, **kwargs):
        if self.random_state.random() < self.flip_probability:
            flip = True
            flip_key_dict = {key: 1 - value for key, value in self.key_dict.items()}

        else:
            flip_key_dict = self.key_dict
            flip = False

        self._draw_stimulus(
            win,
            logger,
            input_handler=input_handler,
            action=None,
            name=self.name_phase1,
            duration=self.duration_phase1,
            flip=flip,
            rl_label=self.rl_label_phase1,
        )

        input_handler.key_strokes(logger=logger)

        response_window_onset = logger.get_time()

        response = self._response_handling(
            input_handler,
            logger,
            response_window_onset,
            key_dict=flip_key_dict,
            info=info,
        )

        if response is not None:
            self._draw_stimulus(
                win,
                logger,
                input_handler=input_handler,
                action=response[0],
                name=self.name_phase2,
                duration=self.duration_phase2,
                flip=flip,
                rl_label=self.rl_label_phase2,
            )

        return response

    def simulate(
        self,
        logger: LoggerProtocol,
        key: str | None = None,
        rt: float | None = None,
        info: dict | None = None,
        **kwargs,
    ):
        stim_onset = logger.get_time()

        simulation_wait(logger.clock, time=self.duration_phase1, start=stim_onset)

        logger.log_event(
            {
                "event_type": self.name_phase1,
                "expected_duration": self.duration_phase1,
                "rl_label": self.rl_label_phase1,
            },
            onset=stim_onset,
        )

        response_window_onset = logger.get_time()
        out = self._simulate_response(
            logger, key, rt, response_window_onset=response_window_onset, info=info
        )

        if out is None:
            raise ValueError("Simulated response shouldn't be None")
        else:
            response_key, remaining = out

        stim_onset = logger.get_time()

        simulation_wait(logger.clock, time=self.duration_phase2, start=stim_onset)

        logger.log_event(
            {
                "event_type": self.name_phase2,
                "expected_duration": self.duration_phase2,
                "rl_label": self.rl_label_phase2,
            },
            onset=stim_onset,
        )

        return response_key, remaining

    def _draw_stimulus(
        self,
        win,
        logger,
        input_handler,
        action,
        name,
        duration,
        flip=False,
        rl_label=None,
    ):
        stim_onset = logger.get_time()

        # Reset image positions
        for im, po in zip(self.image_class, self.positions):
            im.setPos(po)

        imgA = self.image_class[0]
        imgA.setOpacity(1.0)

        imgB = self.image_class[1]
        imgB.setOpacity(1.0)

        if flip:
            posA = imgA.pos
            posB = imgB.pos
            imgA.setPos(posB)
            imgB.setPos(posA)

        if action == 0:
            feedback = Rect(
                win=win,
                width=imgA.size[0],
                height=imgA.size[1],
                lineColor="white",
                lineWidth=7,
                pos=imgA.pos,
            )

            imgB.setOpacity(0.25)
            feedback.draw()

        elif action == 1:
            feedback = Rect(
                win=win,
                width=imgB.size[0],
                height=imgB.size[1],
                lineColor="white",
                lineWidth=7,
                pos=imgB.pos,
            )

            imgA.setOpacity(0.25)

            feedback.draw()

        imgA.draw()
        imgB.draw()

        for img in self.image_class[2:]:
            img.draw()

        win.flip()

        wait(
            logger=logger,
            input_handler=input_handler,
            time=duration,
            start=stim_onset,
            poll_keys=self.poll_keys,
        )

        self._log_event(
            logger=logger,
            stim_onset=stim_onset,
            extra_info={
                "misc": f"flip-{flip}",
                "event_type": name,
                "expected_duration": duration,
                "rl_label": rl_label,
            },
        )


class StimuliWithResponse(ActionStimulus):
    def __init__(
        self,
        duration: float,
        key_dict: dict | None = None,
        name: str = "response",
        target_name: str | None = None,
        target_duration: float = 0.0,
        target_rl_label: str | None = None,
        timeout_action: int | None = None,
        name_timeout="response-time-out",
        positions=((0, 0), (0, 0)),
        images=None,
        flip_probability=0.5,
        flip_dir: str = "horiz",
        random_state=111,
        rl_label: str | None = None,
    ):
        if images is None:
            images = [
                make_card_stimulus(generate_stimulus_properties(12)),
                make_card_stimulus(generate_stimulus_properties(23)),
            ]
        if key_dict is None:
            key_dict = {"left": 0, "right": 1}
        super().__init__(
            name=name,
            duration=duration,
            key_dict=key_dict,
            timeout_action=timeout_action,
            name_timeout=name_timeout,
            rl_label=rl_label,
        )

        self.images = images
        self.positions = positions
        self.target_name = target_name
        self.target_duration = target_duration
        self.flip_probability = flip_probability
        self.flip_dir = flip_dir
        self.target_rl_label = target_rl_label
        self.rng = check_random_state(random_state)

    def _setup(self, win, **kwargs):
        self.imageStims = []
        for img, pos in zip(self.images, self.positions):
            if isinstance(img, str):
                self.imageStims.append(ImageStim(win=win, image=img, pos=pos))
            else:
                self.imageStims.append(
                    ImageStim(
                        win, image=img, size=(img.shape[1], img.shape[0]), pos=pos
                    )
                )

    def display(self, win, logger, input_handler: InputProtocol, info, **kwargs):
        input_handler.key_strokes(logger=logger)

        self._draw_stimulus(win, logger, input_handler=input_handler)
        win.flip()

        response_window_onset = logger.get_time()

        response = self._response_handling(
            input_handler,
            logger,
            response_window_onset,
            key_dict=self.key_dict,
            info=info,
        )

        return response

    def simulate(
        self,
        logger: LoggerProtocol,
        key: str | None = None,
        rt: float | None = None,
        info: dict | None = None,
        **kwargs,
    ):
        stim_onset = logger.get_time()

        simulation_wait(logger.clock, time=self.target_duration, start=stim_onset)

        self._log_event(
            logger=logger,
            stim_onset=stim_onset,
            extra_info={
                "event_type": self.target_name,
                "duration": self.target_duration,
                "rl_label": self.target_rl_label,
            },
        )

        response = self._simulate_response(
            logger,
            key,
            rt,
            response_window_onset=stim_onset,
            info=info,
        )

        return response

    def _draw_stimulus(self, win, logger, input_handler: InputProtocol, flip=False):
        stim_onset = logger.get_time()

        flip = self.rng.random() < self.flip_probability

        # So that images are drawn on top
        for ii in self.imageStims:
            ii.autoDraw = True
            if self.flip_dir == "vert":
                ii.flip = [flip, False]
            elif self.flip_dir == "horiz":
                ii.flip = [False, flip]

        win.flip()

        for ii in self.imageStims:
            ii.autoDraw = False

        wait(
            logger,
            time=self.target_duration,
            start=stim_onset,
            poll_keys=True,
            input_handler=input_handler,
        )

        self._log_event(
            logger=logger,
            stim_onset=stim_onset,
            extra_info={
                "misc": f"flip-{flip}",
                "event_type": self.target_name,
                "expected_duration": self.target_duration,
                "rl_label": self.target_rl_label,
            },
        )


class LingeringAction(ActionStimulus):
    def __init__(
        self,
        duration: float,
        key_dict: dict | None = None,
        name: str = "response",
        name_phase1: str | None = None,
        name_phase2: str | None = None,
        duration_phase1: float = 0.0,
        duration_phase2: float = 0.0,
        timeout_action: int | None = None,
        name_timeout="response-time-out",
        positions_phase1=((0, 0), (0, 0)),
        positions_phase2=((0, 0), (0, 0)),
        images_phase1=None,
        images_phase2=None,
        random_state=111,
        rl_label: str | None = None,
        rl_label_phase1: str | None = None,
        rl_label_phase2: str | None = None,
        autodraw: bool = False,
    ):
        if images_phase2 is None:
            images_phase2 = [
                make_card_stimulus(generate_stimulus_properties(12)),
                make_card_stimulus(generate_stimulus_properties(23)),
            ]
        if images_phase1 is None:
            images_phase1 = [
                make_card_stimulus(generate_stimulus_properties(12)),
                make_card_stimulus(generate_stimulus_properties(23)),
            ]
        if key_dict is None:
            key_dict = {"left": 0, "right": 1}
        super().__init__(
            name=name,
            duration=duration,
            key_dict=key_dict,
            timeout_action=timeout_action,
            name_timeout=name_timeout,
            rl_label=rl_label,
        )

        self.images_phase1 = images_phase1
        self.images_phase2 = images_phase2
        self.positions_phase1 = positions_phase1
        self.positions_phase2 = positions_phase2
        self.name_phase1 = name_phase1
        self.name_phase2 = name_phase2
        self.duration_phase1 = duration_phase1
        self.duration_phase2 = duration_phase2
        self.rl_label_phase1 = rl_label_phase1
        self.rl_label_phase2 = rl_label_phase2
        self.random_state = check_random_state(random_state)
        self.autodraw = autodraw

    def _setup(self, win, **kwargs):
        self.image_class_phase1 = []
        for img, pos in zip(self.images_phase1, self.positions_phase1):
            if isinstance(img, str):
                self.image_class_phase1.append(ImageStim(win=win, image=img, pos=pos))
            else:
                self.image_class_phase1.append(
                    ImageStim(
                        win, image=img, size=(img.shape[1], img.shape[0]), pos=pos
                    )
                )

        self.image_class_phase2 = []
        for img, pos in zip(self.images_phase2, self.positions_phase2):
            if isinstance(img, str):
                self.image_class_phase2.append(ImageStim(win=win, image=img, pos=pos))
            else:
                self.image_class_phase2.append(
                    ImageStim(
                        win, image=img, size=(img.shape[1], img.shape[0]), pos=pos
                    )
                )

    def display(
        self, win, logger: LoggerProtocol, input_handler: InputProtocol, info, **kwargs
    ):
        self._draw_stimulus(
            win,
            logger,
            input_handler=input_handler,
            phase=1,
            name=self.name_phase1,
            duration=self.duration_phase1,
            rl_label=self.rl_label_phase1,
        )

        input_handler.key_strokes(logger)

        response_window_onset = logger.get_time()

        response = self._response_handling(
            input_handler, logger, response_window_onset, info=info
        )

        self._draw_stimulus(
            win,
            logger,
            input_handler=input_handler,
            phase=2,
            name=self.name_phase2,
            duration=self.duration_phase2,
            rl_label=self.rl_label_phase2,
        )

        return response

    def simulate(
        self,
        logger: LoggerProtocol,
        key: str | None = None,
        rt: float | None = None,
        info: dict | None = None,
        **kwargs,
    ):
        stim_onset = logger.get_time()

        simulation_wait(logger.clock, time=self.duration_phase1, start=stim_onset)

        logger.log_event(
            {
                "event_type": self.name_phase1,
                "expected_duration": self.duration_phase1,
                "rl_label": self.rl_label_phase1,
            },
            onset=stim_onset,
        )

        response_window_onset = logger.get_time()

        out = self._simulate_response(
            logger, key, rt, response_window_onset=response_window_onset, info=info
        )

        if out is None:
            raise ValueError("Output shouldn't be None")
        else:
            response_key, remaining = out

        stim_onset = logger.get_time()

        simulation_wait(logger.clock, time=self.duration_phase2, start=stim_onset)

        logger.log_event(
            {
                "event_type": self.name_phase2,
                "expected_duration": self.duration_phase2,
                "rl_label": self.rl_label_phase2,
            },
            onset=stim_onset,
        )

        return response_key, remaining

    def _draw_stimulus(
        self, win, logger, input_handler, name, duration, phase=1, rl_label=None
    ):
        stim_onset = logger.get_time()

        if phase == 1:
            # So that images are drawn on top
            for ii in self.image_class_phase1:
                ii.autoDraw = True

            win.flip()

            for ii in self.image_class_phase1:
                ii.autoDraw = self.autodraw

        elif phase == 2:
            for ii in self.image_class_phase2:
                ii.autoDraw = True

            win.flip()

            for ii in self.image_class_phase2:
                ii.autoDraw = self.autodraw

        wait(
            logger,
            duration,
            stim_onset,
            input_handler=input_handler,
            poll_keys=self.poll_keys,
        )

        self._log_event(
            logger=logger,
            stim_onset=stim_onset,
            extra_info={
                "event_type": name,
                "rl_label": rl_label,
                "expected_duration": duration,
            },
        )
