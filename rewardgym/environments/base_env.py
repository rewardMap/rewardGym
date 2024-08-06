from collections import defaultdict
from typing import Dict, Union

try:
    from gymnasium import Env
    from gymnasium.spaces import Discrete
except ModuleNotFoundError:
    from .gymnasium_stubs import Env
    from .gymnasium_stubs import Discrete

from typing import Tuple, Union

import numpy as np

from ..utils import check_seed


class BaseEnv(Env):
    """
    The basic environment class for the rewardGym module.
    """

    metadata = {"render_modes": ["human"]}

    def __init__(
        self,
        environment_graph: Dict,
        reward_locations: Dict,
        render_mode: str = None,
        info_dict: Dict = defaultdict(int),
        seed: Union[int, np.random.Generator] = 1000,
        name: str = None,
    ):
        """
        The core environment used for modeling and in part for displays.

        Parameters
        ----------
        environment_graph : dict
            The main graph showing the asssociation between states and actions.
        reward_locations : dict
            Which location in the graph are associated with a reward.
        render_mode : str, optional
            If using rendering or not, by default None
        info_dict : dict, optional
            Additional information, that should be associated with a node, by default defaultdict(int)
        seed : Union[int, np.random.Generator], optional
            The random seed associated with the environment, creates a generator, by default 1000
        """

        # It should be posssible to use wrapper for one-hot, so no box and other handling necessary (might need an
        # implementation though).

        self.n_actions = max(
            [len(i) for i in environment_graph.values()]
        )  # Approach for action spaces, not sure if great
        self.n_states = len(
            environment_graph
        )  # Assuming nodes are states (different from neuro-nav)
        self.action_space = Discrete(self.n_actions)
        self.observation_space = Discrete(self.n_states)

        self.rng = check_seed(seed)
        self.reward_locations = reward_locations

        self.info_dict = info_dict
        self.graph = environment_graph
        self.agent_location = None

        self.cumulative_reward = 0

        assert render_mode is None or render_mode in self.metadata["render_modes"]

        self.render_mode = render_mode
        self.window = None
        self.clock = None
        self.reward = None
        self.name = name

    def _get_obs(self) -> int:
        """
        Method to transform the observation, here it is just returning the
        agent's location.

        Returns
        -------
        int
            Location of the agent.
        """
        return (
            self.agent_location
        )  # needs to have some other implementation for one hot, I fear

    def _get_info(self) -> dict:
        """
        Returns the info stored in the info_dict.

        Returns
        -------
        dict
            Info dict at current node
        """
        return self.info_dict[self.agent_location]

    def reset(
        self, agent_location: int = None, condition: int = None
    ) -> Tuple[Union[int, np.array], Dict]:
        """
        Resetting the environment, moving everything to start.
        Using conditions and agent_locations to specify task features.

        Parameters
        ----------
        agent_location : int, optional
            Where in the graph the agent should be placed, by default None
        condition : int, optional
            Setting a potential condition for the trial, by default None

        Returns
        -------
        Tuple[Union[int, np.array], dict]
            The observation at that node in the graph and the associated info.
        """

        self.agent_location = agent_location
        self.condition = condition
        observation = self._get_obs()

        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame(info)

        return observation, info

    def step(
        self, action: int = None, step_reward: bool = False
    ) -> Tuple[Union[int, np.array], int, bool, bool, dict]:
        """
        Stepping through the graph - acquire a new observation in the graph.

        Parameters
        ----------
        action : int, optional
            the action made by an agent, by default None
        step_reward : bool, optional
            Only necessary, if rewards are episode sensitive, if True calls
            all reward objects, not only the selected one (while ignoring their output),
            by default False

        Returns
        -------
        Tuple[Union[int, np.array], int, bool, bool, dict]
            The new observation, the reward associated with an action, if the
            episode is terminated, if the episode has been truncated (False),
            and the new observation's info.
        """

        # Can do jumps now, if probabilistic end positions
        if isinstance(self.graph[self.agent_location], tuple):
            stochasticiy = self.graph[self.agent_location][1]

            if self.rng.random() <= stochasticiy:
                next_position = self.graph[self.agent_location][0][action]
            else:
                possible_locs = self.graph[self.agent_location][0][:]
                possible_locs.pop(action)
                next_position = self.rng.choice(possible_locs)
        else:
            next_position = self.graph[self.agent_location][action]

        self.agent_location = next_position

        if len(self.graph[next_position]) == 0:
            terminated = True
        else:
            terminated = False

        if terminated:
            reward = self.reward_locations[self.agent_location](self.condition)
            self.reward = reward

            # Stepping rewards, e.g. if the whole environment changes (as in two-step task)
            if step_reward:
                for rw in self.reward_locations.keys():
                    if self.agent_location != rw:
                        self.reward_locations[rw](self.condition)

        else:
            self.reward = 0

        observation = self._get_obs()
        info = self._get_info()

        self.cumulative_reward += self.reward

        if self.render_mode == "human":
            self._render_frame(info)

        return observation, self.reward, terminated, False, info

    def _render_frame(self, info: Dict):
        """
        Rendering method, not implemented for BaseEnvironment.

        Parameters
        ----------
        info : dict
            info associate with an observation.

        Raises
        ------
        NotImplementedError
            BaseEnv does not allow for rendering.
        """
        raise NotImplementedError("Not implemented in basic environments")

    def add_info(self, new_info: Dict) -> None:
        self.info_dict.update(new_info)


class MultiChoiceEnv(BaseEnv):
    """
    Special class of the BaseEnv, which allows and additional mapping of actions.
    This env is used, when there are many possible outcomes, but only a few
    actions are available (as in the implementation of the risk-sensitive task).
    """

    metadata = {"render_modes": ["human"]}

    def __init__(
        self,
        environment_graph: Dict,
        reward_locations: Dict,
        condition_dict: Dict,
        render_mode: str = None,
        info_dict: Dict = defaultdict(int),
        seed: Union[int, np.random.Generator] = 1000,
        name: str = None,
    ):
        """
        Special class for limited action spaces, but multiple outcomes.

        Parameters
        ----------
        environment_graph : dict
            The main graph showing the asssociation between states and actions.
        reward_locations : dict
            Which location in the graph are associated with a reward.
        condition_dict : dict
            A mapping between the condition and the possible outcomes of a response. E.g. in the risk-sensitive task,
            condition_dict[1] = {0 : 4, 1: 2} would say that in condition 1, a "left" response would lead to outcome 4,
            a "right" response to outcome 2.
        render_mode : str, optional
            If using rendering or not, by default None
        info_dict : dict, optional
            Additional information, that should be associated with a node, by default defaultdict(int)
        seed : Union[int, np.random.Generator], optional
            The random seed associated with the environment, creates a generator, by default 1000
        """

        super().__init__(
            environment_graph=environment_graph,
            reward_locations=reward_locations,
            render_mode=render_mode,
            info_dict=info_dict,
            seed=seed,
            name=name,
        )

        self.condition_dict = condition_dict

    def step(
        self, action: int = None, step_reward: bool = False
    ) -> Tuple[Union[int, np.array], int, bool, bool, Dict]:
        """
        Stepping through the graph - acquire a new observation in the graph. In
        this case also maps condition specific actions to outcomes.

        Parameters
        ----------
        action : int, optional
            the action made by an agent, by default None
        step_reward : bool, optional
            Only necessary, if rewards are episode sensitive, if True calls
            all reward objects, not only the selected one (while ignoring their output),
            by default False

        Returns
        -------
        Tuple[Union[int, np.array], int, bool, bool, dict]
            The new observation, the reward associated with an action, if the
            episode is terminated, if the episode has been truncated (False),
            and the new observation's info.
        """

        if action not in self.condition_dict[self.condition].keys():
            observation = self._get_obs()
            reward = 0
            terminated = False
            info = self._get_info()

        else:
            action = self.condition_dict[self.condition][action]
            next_position = self.graph[self.agent_location][action]

            self.agent_location = next_position

            if len(self.graph[next_position]) == 0:
                terminated = True
            else:
                terminated = False

            if terminated:
                reward = self.reward_locations[self.agent_location](self.condition)
                self.reward = reward

                if step_reward:
                    for rw in self.reward_locations.keys():
                        if self.agent_location != rw:
                            self.reward_locations[rw](self.condition)

            else:
                self.reward = 0

            observation = self._get_obs()
            info = self._get_info()

            self.cumulative_reward += reward

            if self.render_mode == "human":
                self._render_frame(info)

        return observation, reward, terminated, False, info
