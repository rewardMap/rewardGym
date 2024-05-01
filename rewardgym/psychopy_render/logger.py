""" Logger classes used by the experiment."""

from typing import Dict, List, Tuple, Union

try:
    from psychopy import core
    from psychopy.core import Clock
    from psychopy.event import getKeys
    from psychopy.visual import Window
except ModuleNotFoundError:
    from . import psychopy_stubs as core
    from .psychopy_stubs import Clock, Window, getKeys


class ExperimentLogger:
    """
    Logger class to log what is going on during the experiment.
    """

    def __init__(
        self,
        file_name: str,
        global_clock: Clock,
        participant_id: str,
        task: str = "hcp",
        run: int = 1,
        seq_tr: float = 0.752,
        sep: str = "\t",
        na: str = "n/a",
        kill_switch: str = "q",
        mr_trigger: str = "5",
        mr_clock: Clock = Clock,
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
            If it is an fMRI experiment, this is echo time. Used to calculate the expected collection between acqusitions, by default 0.752
        sep : str, optional
            What kind of seperator to use in output file, by default "\t"
        na : str, optional
            How NaN values are written to file, by default "n/a"
        kill_switch : str, optional
            Button to press to exit the experiment, by default "q"
        mr_trigger : str, optional
            Trigger of the MRI (assuming that it is transformed to a key press), by default "5"
        """

        self.file_name = file_name
        self.global_clock = global_clock
        self.mr_clock = mr_clock

        self.sep = sep
        self.na = na

        self.participant_id = participant_id
        self.task = task
        self.run = run

        self.seq_tr = seq_tr
        self.reward = 0
        self.kill_switch = kill_switch
        self.mr_trigger = mr_trigger

        self.trial_type = self.na
        self.start_position = self.na
        self.current_location = self.na

        self.trial = -1
        self.tr = 0

        self.tmp_dict = {}

        self.categories = [
            "onset",
            "duration",
            "trial_type",
            "start_position",
            "event_type",
            "response_time",
            "response_button",
            "response_late",
            "reward",
            "delta_reward",
            "trial",
            "TR",
            "task",
            "run",
            "participant_id",
            "expexted_duration",
            "trial_time",
            "total_reward",
            "current_location",
        ]

        # Create a dictionary of nans to be used later.
        self.nan_dict = {ii: self.na for ii in self.categories}

    def _default_logging(self, reward: float = None) -> Dict:
        """
        Populates dictionary with default values.

        Parameters
        ----------
        reward : float, optional
            The reward received in the trial, by default None

        Returns
        -------
        Dict
            dictionary populated with default values.
        """
        tmp_dict = self.nan_dict.copy()
        tmp_dict["onset"] = self.global_clock.getTime()
        tmp_dict["reward"] = self.reward
        tmp_dict["trial"] = self.trial
        tmp_dict["trial_time"] = self.global_clock.getTime() - self.trial_start
        tmp_dict["participant_id"] = self.participant_id
        tmp_dict["trial_type"] = self.trial_type
        tmp_dict["start_position"] = self.start_position
        tmp_dict["current_location"] = self.current_location
        tmp_dict["TR"] = self.tr
        tmp_dict["run"] = self.run

        # Update reward
        if reward is not None:
            tmp_dict["delta_reward"] = reward - self.reward
            self.reward = reward
        else:
            tmp_dict["delta_reward"] = 0

        return tmp_dict

    def log_event(self, info_dict: Dict, reward: float = None, onset: float = None):
        """
        Logs the current event.

        Parameters
        ----------
        info_dict : Dict
            the dictionary that contains the current information of the trial.
        reward : float, optional
            reward received in the trial, by default None
        onset : float, optional
            The real onset of the event, duration is
                calculated between onset and current time, by default None

        Raises
        ------
        ValueError
            Returns an error if onset is after the current time.
        """

        tmp_dict = self._default_logging(reward)

        if onset:
            if onset <= tmp_dict["onset"]:
                tmp_dict["duration"] = tmp_dict["onset"] - onset
                tmp_dict["onset"] = onset
            else:
                raise ValueError(
                    "User defined onset needs to be before" + " automatic onest!"
                )

        # TODO check, that onset is not in info_dict!
        if info_dict is not None:
            for key in info_dict.keys():
                tmp_dict[key] = info_dict[key]

        tmp_values = self._create_log_list(tmp_dict)

        self._write_to_file(tmp_values)

    def _create_log_list(self, tmp_dict: Dict) -> List[str]:
        """
        Creates a list of strs from dictionary. Only keeps entries that are
        prespecified.

        Parameters
        ----------
        tmp_dict : Dict
            Dictionary to be transformed.

        Returns
        -------
        List[str]
            List of strings.
        """

        logList = [str(tmp_dict[kk]) for kk in self.categories]
        return logList

    def _write_to_file(self, tmp_values: List[float]):
        """
        Converts all values in value_list to string and writes them
        to the log file.

        Parameters
        ----------
        tmp_values : List[float]
            List of strings to write to file.
        """

        if tmp_values:
            self.log_file.write(self.sep.join(tmp_values) + "\n")

    def create(self, mode: str = "w"):
        """
        Creates new file with the given columns. Or opens to append.

        Parameters
        ----------
        mode : str, optional
            mode (str, optional): Writing mode, by default "w"
        """

        self.log_file = open(self.file_name, mode)
        # set trial start to not break stuff
        self.set_trial_time()

        if mode == "w":
            self._write_to_file(self.categories)

    def close(self):
        """
        Closes the file.
        """
        self.log_file.close()

    def set_trial_time(self):
        """
        Set the trial's start using the global clock.
        """
        self.trial_start = self.global_clock.getTime()

    def get_time(self) -> float:
        """
        Get the current time from the global clock.

        Returns
        -------
        float
            time passed sine last reset
        """
        return self.global_clock.getTime()

    def key_strokes(
        self, win: Window, keyList: List[str] = []
    ) -> Union[Tuple[str, float], None]:
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

        presses = getKeys(timeStamped=self.global_clock)
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
                    expected_time = self.mr_clock.getTime() - (self.tr * self.seq_tr)
                    # ugly fix!
                    self.log_event(
                        {
                            "event_type": "TR",
                            "response_button": resp[0],
                            "response_time": self.mr_clock.getTime(),
                            "expected_duration": expected_time,
                        },
                        reward=self.reward,
                    )

                elif resp[0] in keyList:
                    # Potentially dangerous - if press is in list, return!
                    response = (resp[0], resp[1])

                else:
                    self.log_event(
                        {
                            "event_type": "ButtonPress",
                            "response_button": resp[0],
                            "response_time": resp[1] - self.trial_start,
                        },
                        reward=self.reward,
                    )

            return response

        else:
            return response


class MinimalLogger(ExperimentLogger):
    """
    Emulates the experiment logger, to keep stimuli classes working, does not write to file (uses stubs)
    """

    def __init__(
        self,
        global_clock: Clock,
        seq_tr: float = 0.752,
        na: str = "n/a",
        kill_switch: str = "q",
        mr_trigger: str = "5",
        mr_clock: Clock = Clock,
    ):
        """
        Logger class to help with logging during a potential fMRI experiment,
        which is implemented in PsychoPy.

        Parameters
        ----------
        global_clock : Clock
            Clock that is used by the experiment.
        seq_tr : float, optional
            If it is an fMRI experiment, this is echo time. Used to calculate the expected collection between acqusitions, by default 0.752
        na : str, optional
            How NaN values are written to file, by default "n/a"
        kill_switch : str, optional
            Button to press to exit the experiment, by default "q"
        mr_trigger : str, optional
            Trigger of the MRI (assuming that it is transformed to a key press), by default "5"
        """

        self.global_clock = global_clock
        self.mr_clock = mr_clock

        self.na = na

        self.seq_tr = seq_tr
        self.reward = 0
        self.kill_switch = kill_switch
        self.mr_trigger = mr_trigger

        self.trial_type = self.na
        self.start_position = self.na
        self.current_location = self.na

        self.trial = -1
        self.tr = 0

    def log_event(self, *args, **kwargs):
        """
        Log event stub.
        """

        pass

    def _write_to_file(self, tmp_values: List[float]):
        """
        Write stub
        """
        pass

    def create(self, *args, **kwargs):
        """
        Create stub.
        """

        self.set_trial_time()

    def close(self):
        """
        Close stub.
        """
        pass


class SimulationLogger(ExperimentLogger):
    def _write_to_file(self, tmp_values: List[float]):

        for n, ii in enumerate(self.categories):
            self.df[ii].append(tmp_values[n])

    def create(self, mode: str = "w"):
        self.df = {ii: [] for ii in self.categories}

    def key_strokes(
        self,
        key,
        rt,
    ) -> Union[Tuple[str, float], None]:

        return (key, rt)

    def close(self):
        return self.df
