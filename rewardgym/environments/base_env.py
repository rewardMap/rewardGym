from collections import defaultdict
from typing import Union

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

    metadata = {"render_modes": ["human"]}

    def __init__(
        self,
        environment_graph: dict,
        reward_locations: dict,
        render_mode: str = None,
        info_dict: dict = defaultdict(int),
        seed: Union[int, np.random.Generator] = 1000,
    ):

        # It should be posssible to use wrapper for one-hot, so no box and other handling necessary.
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

    def _get_obs(self) -> int:
        return (
            self.agent_location
        )  # needs to have some other implementation for one hot, I fear

    def _get_info(self) -> dict:
        return self.info_dict[self.agent_location]

    def reset(
        self, agent_location: int = None, condition: int = None
    ) -> Tuple[Union[int, np.array], dict]:
        # We need the following line to seed self.np_random
        self.agent_location = agent_location
        self.condition = condition  # Needs some condition logic
        observation = self._get_obs()

        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame(info)

        return observation, info

    def step(
        self, action: int = None
    ) -> Tuple[Union[int, np.array], int, bool, bool, dict]:

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
        else:
            self.reward = 0

        observation = self._get_obs()
        info = self._get_info()

        self.cumulative_reward += self.reward

        if self.render_mode == "human":
            self._render_frame(info)

        return observation, self.reward, terminated, False, info

    def _render_frame(self, info: dict):
        raise NotImplementedError("Not implemented in Basic Agents")


class MultiChoiceEnv(BaseEnv):

    metadata = {"render_modes": ["human"]}

    def __init__(
        self,
        environment_graph: dict,
        reward_locations: dict,
        condition_dict: dict,
        render_mode: str = None,
        info_dict: dict = defaultdict(int),
        seed: Union[int, np.random.Generator] = 1000,
    ):

        super().__init__(
            environment_graph=environment_graph,
            reward_locations=reward_locations,
            render_mode=render_mode,
            info_dict=info_dict,
            seed=seed,
        )

        self.condition_dict = condition_dict

    def step(
        self, action: int = None
    ) -> Tuple[Union[int, np.array], int, bool, bool, dict]:

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
            else:
                self.reward = 0

            observation = self._get_obs()
            info = self._get_info()

            self.cumulative_reward += reward

            if self.render_mode == "human":
                self._render_frame(info)

        return observation, reward, terminated, False, info
