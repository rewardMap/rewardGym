from psylog import BaseLogger, DictLogOutput, LogMode

from ..protocols import ClockProtocol, LoggerProtocol
from .rewardmap_categories import get_rewardmap_defaults


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
