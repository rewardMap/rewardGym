from collections import defaultdict
from dataclasses import dataclass
from typing import Any
from ..render.contexts import StepContext


@dataclass
class ActionLayout:
    """
    This class contains and creates the different level mappings in the
    toolbox.
    The first mapping is from available actions to exposed actions.
    To recap the graph:
    A non terminal node is associated with a list of follow nodes, which
    are indexed by their list position.
    E.g. 0: [1, 2], indicates that action 0 goes to state 1  and action
    1 goes to state 2.
    In most cases, the graph-action maps directly to the agents actions.
    E.g. agent issues 0 -> 0 in the graph space.
    There are environments, where the action space is reduced:
    E.g. 0: [1, 2, 3, 4], but only two actions are available (for example
    only two choices). So a mapping might be 0 -> 3, 1 -> 1 (if [3, 1] are available).

    self.graph_to_action does the mapping 3 -> 0 and self.action_to_graph the
    mapping 0 -> 3.

    Adding a key-dictionary introduces the mapping of the agent, as index in the available
    action list: {left: 0, right: 1}.

    self.graph_to_key, takes one from 3 -> [left], self.key_to_graph from left -> 3.
    self.action_to_key takes one from 0 -> [left] and self.key_to_action is only a more
    verbose mapping of left -> 0 and right -> 1.
    Pay attention to the lists.

    Parameters
    ----------
    available_actions : list[int]
        The actions available to the agent.
    """

    available_graph_actions: list[int]

    def __post_init__(self):
        self.action_to_graph = {
            n: i for n, i in enumerate(self.available_graph_actions)
        }
        self.graph_to_action = {
            i: n for n, i in enumerate(self.available_graph_actions)
        }

    def add_keys(self, key_dict: dict[str, int]):
        self.key_dict = key_dict

        self.key_to_graph = {}
        for k, v in self.key_dict.items():
            if v in self.action_to_graph:
                self.key_to_graph[k] = self.action_to_graph[v]

        self.graph_to_key = defaultdict(list)
        self.action_to_key = defaultdict(list)
        self.key_to_action = key_dict

        for k, v in self.key_dict.items():
            if v in self.action_to_graph:
                self.graph_to_key[self.action_to_graph[v]].append(k)

            self.action_to_key[v].append(k)

    @property
    def avail_actions(self):
        return [i for i in self.available_graph_actions if i is not None]


@dataclass
class Step:
    """
    Dataclass to keep track of steps in the environment - and addition to
    info for now.
    """

    events: list | None = None
    obs: Any | None = None
    next_obs: Any | None = None
    reward: Any | None = None
    action: Any | None = None
    reaction_time: Any | None = None

    def __post_init__(self):
        if self.events is None:
            self.events = []


@dataclass
class Event:
    """
    Dataclass to keep track of a single event
    """

    frame: Any | None = None
    duration: Any | None = None
    reaction_time: float | None = None
    action: Any | None = None
    name: str | None = None


class EnviromentTracker:
    def __init__(self):
        self.steps = []

    def add_step(self, obs: Any | None = None):
        self.steps.append(Step(obs=obs))

    def add_event(
        self, action=None, frame=None, reaction_time=None, duration=None, name=None
    ):
        current_step = self.steps[-1]
        event = Event(
            frame=frame,
            action=action,
            reaction_time=reaction_time,
            duration=duration,
            name=name,
        )
        current_step.events.append(event)

        if event.action is not None and current_step.action is None:
            current_step.action = event.action

        if event.reaction_time is not None and current_step.reaction_time is None:
            current_step.action = event.action

    def finalize_step(
        self, reward: int | float or None = None, next_obs: Any | None = None
    ):
        current_step = self.steps[-1]
        current_step.reward = reward
        current_step.next_obs = next_obs


@dataclass
class ResponsePending:
    index: int
    step: StepContext
