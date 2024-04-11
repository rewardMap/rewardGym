""" Logger classes used by the experiment."""

from typing import Dict, List, Tuple, Union

from psychopy import core, event, visual


class ExperimentLogger:
    """
    Logger for both active and passive runs, to simplify writing to files.
    TODO: Input checks and validation.
    TODO: Dictionaries are not in order...
    """

    def __init__(
        self,
        fileName: str,
        globalClock: core.Clock,
        participant_id: str,
        task: str = "hcp",
        run: int = 1,
        seq_tr: float = 0.752,
        sep: str = "\t",
        na: str = "n/a",
        killSwitch: str = "q",
        mr_trigger: str = "5",
    ):

        self.fileName = fileName
        self.globalClock = globalClock
        self.mrClock = core.Clock()

        self.sep = sep
        self.na = na

        self.participant_id = participant_id
        self.task = task
        self.run = run

        self.seq_tr = seq_tr
        self.reward = 0
        self.killSwitch = killSwitch
        self.mr_trigger = mr_trigger

        self.trial_type = self.na
        self.start_position = self.na

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
        ]

        # Create a dictionary of nans to be used later.
        self.nan_dict = {ii: self.na for ii in self.categories}

    def defaultLogging(self, reward: float = None) -> Dict:
        """Populates dictionary with default values.

        Args:
            reward (float, optional): reward. Defaults to None.

        Returns:
            Dict: Default dict.
        """
        tmp_dict = self.nan_dict.copy()
        tmp_dict["onset"] = self.globalClock.getTime()
        tmp_dict["reward"] = self.reward
        tmp_dict["trial"] = self.trial
        tmp_dict["trial_time"] = self.globalClock.getTime() - self.trial_start
        tmp_dict["participant_id"] = self.participant_id
        tmp_dict["trial_type"] = self.trial_type
        tmp_dict["start_position"] = self.start_position
        tmp_dict["TR"] = self.tr
        tmp_dict["run"] = self.run

        # Update reward
        if reward is not None:
            tmp_dict["delta_reward"] = reward - self.reward
            self.reward = reward
        else:
            tmp_dict["delta_reward"] = 0

        return tmp_dict

    def logEvent(self, info_dict: Dict, reward: float = None, onset: float = None):
        """Logs a given event.

        Args:
            info_dict (Dict): Which fields to update.
            reward (float, optional): If reward is given, update reward.
                Defaults to None.
            onset (float, optional): The real onset of the event, duration is
                calculated between onset and current time. Defaults to None.

        Raises:
            ValueError: Onset needs to be smaller than the onset current time.
        """

        tmp_dict = self.defaultLogging(reward)

        if onset:
            if onset < tmp_dict["onset"]:
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

        tmp_values = self.createLogList(tmp_dict)

        self.writeToFile(tmp_values)

    def createLogList(self, tmp_dict: Dict) -> List[str]:
        """Creates a list of strs from dictionary. Only keeps entries that are
        prespecified.

        Args:
            tmp_dict (Dict): Dictionary to be transformed.

        Returns:
            List[str]: List of strings.
        """

        logList = [str(tmp_dict[kk]) for kk in self.categories]
        return logList

    def writeToFile(self, tmp_values: List[float]):
        """Converts all values in value_list to string and writes them
        to the log file.

        Args:
            value_list (List): List of strings to write to file.
        """
        if tmp_values:
            self.log_file.write(self.sep.join(tmp_values) + "\n")

    def create(self, mode: str = "w"):
        """Creates new file with the given columns. Or opens to append.

        Args:
            mode (str, optional): Writing mode.. Defaults to 'w'.
        """
        self.log_file = open(self.fileName, mode)
        # set trial start to not break stuff
        self.setTrialTime()

        if mode == "w":
            self.writeToFile(self.categories)

    def close(self):
        """Closes the current file."""
        self.log_file.close()

    def setTrialTime(self):
        """Reset the time of the current trial."""
        self.trial_start = self.globalClock.getTime()

    def getTime(self) -> float:
        """Get time from the global clock.

        Returns:
            float: Returns the curren time.
        """

        return self.globalClock.getTime()

    def keyStrokes(
        self, win: visual.Window, keyList: List[str] = []
    ) -> Union[Tuple[str, float], None]:
        """Checks for key strokes, TRs, and values in the keyList.

        Args:
            win (visual.Window): Psychopy window class.
            keyList (List[str], optional): List of allowed keys. Defaults to [].

        Returns:
            Union[Tuple[str, float], None]: None or (key, response time (in s))
        """

        presses = event.getKeys(timeStamped=self.globalClock)
        response = None

        if presses:
            # Assuming that last press is most important! (could have issues - need more checks)
            for resp in presses:

                if resp[0] == self.killSwitch:
                    # Closes the window, closes the file and quits psychopy.
                    win.close()
                    self.close()
                    core.quit()

                elif resp[0] == self.mr_trigger:
                    # Timing based on trial time:
                    # expected duration:
                    self.tr += 1
                    expected_time = self.mrClock.getTime() - (self.tr * self.seq_tr)
                    # ugly fix!
                    self.logEvent(
                        {
                            "event_type": "TR",
                            "response_button": resp[0],
                            "response_time": self.mrClock.getTime(),
                            "expected_duration": expected_time,
                        },
                        reward=self.reward,
                    )

                elif resp[0] in keyList:
                    # Potentially dangerous - if press is in list, return!
                    response = (resp[0], resp[1])

                else:
                    self.logEvent(
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
