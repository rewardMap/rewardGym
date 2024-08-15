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

    metadata = {"render_modes": ["pygame", "psychopy", "psychopy-simulate"]}

    def __init__(
        self,
        environment_graph: Dict,
        reward_locations: Dict,
        render_mode: str = None,
        info_dict: Dict = None,
        seed: Union[int, np.random.Generator] = 1000,
        name: str = None,
        n_actions: int = None,
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

        if n_actions is None:
            self.n_actions = max(
                [len(i) for i in environment_graph.values()]
            )  # Approach for action spaces, not sure if great
        else:
            self.n_actions = n_actions

        self.n_states = len(
            environment_graph
        )  # Assuming nodes are states (different from neuro-nav)
        self.action_space = Discrete(self.n_actions)
        self.observation_space = Discrete(self.n_states)

        self.rng = check_seed(seed)
        self.reward_locations = reward_locations

        if info_dict is None:
            info_dict = {}

        self.info_dict = info_dict

        self.graph = environment_graph
        self.full_graph, self.skip_nodes = self._unpack_graph(self.graph)

        for ke in self.graph.keys():
            if ke not in self.info_dict.keys():
                self.info_dict[ke] = {}

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
        node_info_dict = self.info_dict[self.agent_location]
        node_info_dict["skip-node"] = self.skip_nodes[self.agent_location]

        if self.condition is None:
            avail_actions = list(self.full_graph[self.agent_location].keys())
        elif self.agent_location in self.condition.keys():
            c2s = {v: k for k, v in self.condition[self.agent_location].items()}
            g2s = {
                v: k
                for k, v in self.full_graph[self.agent_location].items()
                for v in (v[0] if isinstance(v, tuple) else [v])
            }
            c2g = {c2s[k]: g2s[k] for k in c2s.keys() if k in g2s.keys()}
            g2c = {v: k for k, v in c2g.items()}
            node_info_dict["remap-actions"] = c2g
            node_info_dict["unmap-actions"] = g2c
            avail_actions = list(c2g.values())
        else:
            avail_actions = list(self.full_graph[self.agent_location].keys())

        node_info_dict["avail-actions"] = avail_actions
        node_info_dict["obs"] = self.agent_location

        return node_info_dict

    def reset(
        self, agent_location: int = 0, condition: int = None
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

        if self.agent_location is None:
            self.agent_location = 0
        else:
            self.agent_location = agent_location

        if condition is not None:
            self.condition = condition
        elif self.n_actions < len(self.full_graph[self.agent_location]):
            locs = self.rng.choice(
                list(self.full_graph[self.agent_location].keys()), size=self.n_actions
            )
            self.condition = {
                self.agent_location: {
                    n: self.full_graph[self.agent_location][i]
                    for n, i in enumerate(locs)
                }
            }
        else:
            self.condition = None

        self.reward = 0
        observation = self._get_obs()

        info = self._get_info()
        if self.render_mode in ["psychopy", "pygame", "psychopy-simulate"]:
            self._render_frame(info)

        if info["skip-node"]:
            observation, _, _, _, info = self.step(info["avail-actions"][0], False)

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

        if self.condition is not None and self.agent_location in self.condition.keys():
            current_graph = self.condition[self.agent_location]

        else:
            current_graph = self.full_graph[self.agent_location]

        if action not in current_graph.keys():
            next_position = self.agent_location
        elif isinstance(current_graph[action], tuple):

            stochasticiy = current_graph[action][1]

            if self.rng.random() <= stochasticiy:
                next_position = current_graph[action][0][0]
            else:
                possible_locs = current_graph[action][0][1:]
                next_position = self.rng.choice(possible_locs)
        else:
            next_position = current_graph[action]

        self.agent_location = next_position

        if len(self.graph[next_position]) == 0:
            terminated = True
        else:
            terminated = False

        if terminated:
            if self.condition is not None and "reward" in self.condition.keys():
                self.reward = self.condition["reward"]
            else:
                self.reward = self.reward_locations[self.agent_location]()
            # Stepping rewards, e.g. if the whole environment changes (as in two-step task)
            if step_reward:
                for rw in self.reward_locations.keys():
                    if self.agent_location != rw:
                        self.reward_locations[rw]()
        else:
            self.reward = 0

        observation = self._get_obs()
        info = self._get_info()

        self.cumulative_reward += self.reward

        if self.render_mode in ["psychopy", "pygame", "psychopy-simulate"]:
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

    @staticmethod
    def _unpack_graph(graph):
        """
        Unpacks the environment graph into the full format separating dummy nodes.

        Parameters
        ----------
        graph : dict
            The original environment graph dictionary.

        Returns
        -------
        tuple of dict
            A tuple containing two dictionaries:
            - full_graph: dict
                The transformed environment graph.
            - skip_nodes: dict
                A dictionary indicating which nodes have the 'skip' attribute.
        """
        full_graph = {}
        skip_nodes = {}

        for node, content in graph.items():
            full_graph[node] = {}
            if isinstance(content, dict):
                for sub_key, sub_value in content.items():
                    if sub_key == "skip":
                        skip_nodes[node] = sub_value
                    else:
                        full_graph[node][sub_key] = sub_value
                        skip_nodes[node] = False
            else:
                skip_nodes[node] = False
                if isinstance(content, tuple):
                    sub_nodes, weight = content
                    full_graph[node][0] = (sub_nodes, weight)
                    if len(sub_nodes) > 1:
                        for idx, sub_node in enumerate(sub_nodes[1:], start=1):
                            full_graph[node][idx] = (
                                [sub_node] + sub_nodes[:idx],
                                weight,
                            )
                elif isinstance(content, list):
                    for idx, sub_node in enumerate(content):
                        full_graph[node][idx] = sub_node
                else:
                    full_graph[node][0] = content

        return full_graph, skip_nodes
