from psylog import BaseLogger, DictLogOutput, LogMode

from .rewardmap_categories import get_rewardmap_defaults

try:
    from psychopy import core
    from psychopy.core import Clock
    from psychopy.event import getKeys
    from psychopy.visual import Window
except ModuleNotFoundError:
    from ..psychopy_render import psychopy_stubs as core
    from ..psychopy_render.psychopy_stubs import Clock, Window, getKeys


class ExperimentLogger(BaseLogger):
    """
    Logger class to log what is going on during the experiment.
    """

    def __init__(
        self,
        file_name: str,
        clock: Clock = None,
        participant_id: str = "n/a",
        task: str = "hcp",
        run: int = 1,
        seq_tr: float = 0.752,
        sep: str = "\t",
        na: str = "n/a",
        kill_switch: str = "q",
        mr_trigger: str = "5",
        categories=None,
    ):
        """
        Logger class to help with logging during a potential fMRI experiment,
        which is implemented in PsychoPy.

        Parameters
        ----------
        file_name : str
            Name of the output file.
        global_clock : core.Clock
            Clock that is used by the experiment.
        participant_id : str
            The participant id (logged as its own persistent column)
        task : str, optional
            The task, also logged as persistent column, by default "hcp"
        run : int, optional
            The run, also logged as persistent column, by default 1
        seq_tr : float, optional
            If it is an fMRI experiment, this is echo time. Used to calculate the expected collection between acquisitions, by default 0.752
        sep : str, optional
            What kind of separator to use in output file, by default "\t"
        na : str, optional
            How NaN values are written to file, by default "n/a"
        kill_switch : str, optional
            Button to press to exit the experiment, by default "q"
        mr_trigger : str, optional
            Trigger of the MRI (assuming that it is transformed to a key press), by default "5"
        """

        if categories is None:
            categories = get_rewardmap_defaults()

        # Initialize ParentLogger with base parameters
        super().__init__(
            file_name=file_name,
            sep=sep,
            na=na,
            categories=get_rewardmap_defaults(),
            static_columns={
                "participant_id": participant_id,
                "task": task,
                "run": run,
            },
            clock=clock,
        )

        # Experiment-specific parameters
        self.seq_tr = seq_tr
        self.kill_switch = kill_switch
        self.mr_trigger = mr_trigger

        # Initialize trial tracking
        self.trial_start = None
        self.tr = 0

    def key_strokes(
        self, win: Window, keyList: list[str] | None = None
    ) -> tuple[str, float] | None:
        """
        Check for key strokes in the keyboard buffer. Checking for MR-triggers,
        close commands (kill_switch), or other allowed responses.

        Parameters
        ----------
        win : Window
            Psychopy window object, used to display the task.
        keyList : List[str], optional
            List of allowed keys., by default []

        Returns
        -------
        Union[Tuple[str, float], None]
            _description_
        """

        if keyList is None:
            keyList = []
        presses = getKeys(timeStamped=self.clock)
        response = None

        if presses:
            for resp in presses:
                if resp[0] == self.kill_switch:
                    # Closes the window, closes the file and quits psychopy.
                    win.close()
                    self.close()
                    core.quit()

                elif resp[0] == self.mr_trigger:
                    self.tr += 1
                    expected_time = self.clock.getTime() - (self.tr * self.seq_tr)
                    # ugly fix!
                    self.log_event(
                        {
                            "event_type": "TR",
                            "response_button": resp[0],
                            "response_time": self.clock.getTime(),
                            "expected_duration": expected_time,
                        },
                    )

                elif resp[0] in keyList:
                    # Potentially dangerous - if press is in list, return!
                    response = (resp[0], resp[1])

                else:
                    self.log_event(
                        {
                            "event_type": "button-press",
                            "response_button": resp[0],
                            "response_time": resp[1] - self._trial_start,
                        },
                    )

            return response

        else:
            return response

    def update_trial_info(self, **kwargs):
        """Update trial-related state information."""
        self.set_trial_time()

        for k, v in kwargs.items():
            if (
                k in self.categories_dict
                and self.categories_dict[k].mode == LogMode.STATE
            ):
                self.categories_dict[k].set_state(v)


class SimulationLogger(ExperimentLogger):
    """Simulation version that stores data in memory instead of writing to file."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override the output to use DictLogOutput
        self._output = DictLogOutput()  # From codebase.txt

    def key_strokes(self, key, rt) -> tuple[str, float] | None:
        """Override to work with simulation."""
        return (key, rt)
