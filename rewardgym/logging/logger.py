from psylog import BaseLogger, CategoryConfig, DictLogOutput, LogMode

from ..protocols import ClockProtocol, LoggerProtocol


class ExperimentLogger(BaseLogger, LoggerProtocol):
    """
    Logger class to log what is going on during the experiment.
    """

    def __init__(
        self,
        file_name: str | None,
        clock: ClockProtocol | None = None,
        participant_id: str = "n/a",
        task: str = "hcp",
        run: int = 1,
        sep: str = "\t",
        na: str = "n/a",
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
        sep : str, optional
            What kind of separator to use in output file, by default "\t"
        na : str, optional
            How NaN values are written to file, by default "n/a"
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

    def update_trial_info(self, **kwargs):
        """Update trial-related state information."""
        self.set_trial_time()

        for k, v in kwargs.items():
            if (
                k in self.categories_dict
                and self.categories_dict[k].mode == LogMode.STATE
            ):
                self.categories_dict[k].set_state(v)


class SimulationLogger(ExperimentLogger, LoggerProtocol):
    """Simulation version that stores data in memory instead of writing to file."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override the output to use DictLogOutput
        self._output = DictLogOutput()  # From codebase.txt


def get_rewardmap_defaults():
    categories = [
        CategoryConfig(
            name="onset",
            default="n/a",
            mode=LogMode.IMPLIED,
            description="Event onset time",
            units="seconds",
            data_type=(float),
        ),
        CategoryConfig(
            name="duration",
            default="n/a",
            mode=LogMode.IMPLIED,
            description="Event duration",
            units="seconds",
            data_type=(float),
        ),
        CategoryConfig(
            "trial_type",
            "n/a",
            mode=LogMode.STATE,
            description="Type of the trial, e.g., the condition in ",
            units="n/a",
        ),
        CategoryConfig(
            "event_type",
            default="n/a",
            mode=LogMode.EVENT,
            description="BIDS is a bit weird in this regard, so this is now the specific event in the trial.",
            units="n/a",
        ),
        CategoryConfig(
            "response_time",
            "n/a",
            mode=LogMode.EVENT,
            description="Time between stimulus and response",
            units="seconds",
            data_type=(float),
        ),
        CategoryConfig(
            "response_button",
            "n/a",
            mode=LogMode.EVENT,
            description="Button pressed in response",
            units="n/a",
        ),
        CategoryConfig(
            "response_late",
            "n/a",
            mode=LogMode.EVENT,
            description="Whether response was too late",
            units="n/a",
        ),
        CategoryConfig(
            "action",
            "n/a",
            mode=LogMode.EVENT,
            description="Action taken by participant",
            units="n/a",
        ),
        CategoryConfig(
            "reward",
            None,
            mode=LogMode.EVENT,
            description="Reward received",
            units="arbitrary unit",
            data_type=None,
        ),
        CategoryConfig(
            "trial",
            -1,
            mode=LogMode.STATE,
            description="Trial",
            units="arbitrary unit",
            data_type=(int),
        ),
        CategoryConfig(
            "current_location",
            "n/a",
            mode=LogMode.STATE,
            description="Current location in environment",
            units="n/a",
        ),
        CategoryConfig(
            "trial_time",
            "n/a",
            mode=LogMode.IMPLIED,
            description="Time since trial start",
            units="seconds",
            data_type=(float),
        ),
        CategoryConfig(
            "total_reward",
            "n/a",
            mode=LogMode.STATE,
            description="Cumulative reward received",
            units="arbitrary unit",
        ),
        CategoryConfig(
            "avail_actions",
            "n/a",
            mode=LogMode.STATE,
            description="Available actions at this point",
            units="n/a",
        ),
        CategoryConfig(
            "misc",
            "n/a",
            mode=LogMode.STATE,
            description="Miscellaneous information",
            units="n/a",
        ),
        CategoryConfig(
            "TR",
            0,
            mode=LogMode.STATE,
            description="MRI volume acquisition number",
            units="n/a",
            data_type=(int),
        ),
        CategoryConfig(
            "expected_duration",
            "n/a",
            mode=LogMode.EVENT,
            description="Expected duration of event",
            units="seconds",
            data_type=(float, int),
        ),
        CategoryConfig(
            "start_position",
            "n/a",
            mode=LogMode.STATE,
            description="Starting position for trial",
            units="n/a",
        ),
        CategoryConfig(
            "rl_label",
            "n/a",
            mode=LogMode.EVENT,
            description="Reinforcement learning label",
            units="n/a",
        ),
    ]

    return categories
