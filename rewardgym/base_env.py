from collections import defaultdict

import gymnasium as gym
import numpy as np
from gymnasium import spaces


class BaseEnv(gym.Env):

    metadata = {"render_modes": ["human"]}

    def __init__(
        self,
        environment_graph,
        condition_logic,
        reward_locations,
        render_mode=None,
        info_dict=defaultdict(int),
        seed=1000,
    ):

        # It should be posssible to use wrapper for one-hot, so no box and other handling necessary.
        self.n_actions = max(
            [len(i) for i in environment_graph.values()]
        )  # Approach for action spaces, not sure if great
        self.n_states = len(
            environment_graph
        )  # Assuming nodes are states (different from neuro-nav)
        self.action_space = spaces.Discrete(self.n_actions)
        self.observation_space = spaces.Discrete(self.n_states)

        if isinstance(seed, np.random.Generator):
            self.rng = seed
        else:
            self.rng = np.random.default_rng(seed)

        self.reward_locations = reward_locations
        self.condition_logic = condition_logic

        self.info_dict = info_dict

        self.graph = environment_graph
        self.agent_location = None

        assert render_mode is None or render_mode in self.metadata["render_modes"]

        self.render_mode = render_mode
        self.window = None
        self.clock = None

    def _get_obs(self):
        return (
            self.agent_location
        )  # needs to have some other implementation for one hot, I fear

    def _get_info(self):
        return [self.info_dict[self.agent_location]]

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        self.agent_location, self.condition = self.condition_logic()

        # Needs some condition logic
        observation = self._get_obs()

        info = self._get_info()

        if self.render_mode == "human":
            self.human_action, self.human_reward_modifier = self._render_frame(info)

        return observation, info

    def step(self, action=None):

        # Can do jumps now, if probabilistic end positions
        if isinstance(self.graph[self.agent_location], tuple):
            stochasticiy = self.graph[self.agent_location][1]

            if self.rng.rand() <= stochasticiy:
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
        else:
            reward = 0

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self.human_action, self.human_reward_modifier = self._render_frame(info)
            reward = reward * self.human_reward_modifier

        return observation, reward, terminated, False, info

    def _render_frame(self, info):
        raise NotImplementedError("Not implemented in Basic Agents")
