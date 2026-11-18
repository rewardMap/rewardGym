import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
from networkx import NetworkXException

from ..utils import get_starting_nodes, get_stripped_graph
from ..render import EnvironmentContext, StepContext

from .env_parts import EnviromentTracker, Event


def plot_env_graph(env):
    strip_graph = get_stripped_graph(env.graph)

    starting_node = get_starting_nodes(env.graph)
    reward_nodes = [ii for (ii, jj) in env.graph.items() if len(jj) == 0]
    nodes = list(env.graph.keys())

    other_nodes = list(set(nodes) - set(reward_nodes) - set(starting_node))

    nd = nx.DiGraph(strip_graph)

    try:
        pos = nx.planar_layout(nd, dim=2)
    except NetworkXException:
        pos = nx.shell_layout(nd, dim=2)

    nx.draw_networkx_nodes(
        nd,
        pos,
        node_size=200,
        nodelist=reward_nodes,
        node_color="tab:orange",
        node_shape="s",
    )
    nx.draw_networkx_nodes(
        nd,
        pos,
        node_size=200,
        nodelist=starting_node,
        node_color="tab:blue",
        node_shape="D",
    )
    nx.draw_networkx_nodes(
        nd, pos, node_size=200, nodelist=other_nodes, node_color="tab:green"
    )
    nx.draw_networkx_edges(nd, pos, alpha=0.5, width=2)

    labels = {ii: f"{ii}" for ii in nodes}
    nx.draw_networkx_labels(nd, pos, labels=labels)

    rew_patch = mpatches.Patch(color="tab:orange", label="reward locations")
    start_patch = mpatches.Patch(color="tab:blue", label="starting locations")
    misc_patch = mpatches.Patch(color="tab:green", label="other")

    plt.legend(handles=[rew_patch, start_patch, misc_patch])


def preview_routine(routine, mode="simulation", step_context=None) -> list[Event]:
    """
    Small functions, to return the values of a routine. Might be used
    for documentation and later testing etc. Set's up a default environment
    context and step_context can be populated.

    Parameters
    ----------
    routine : _type_
        _description_
    mode : str, optional
        _description_, by default "simulation"
    step_context : _type_, optional
        _description_, by default None

    Returns
    -------
    list[Event]
        Events that were triggered in that routine.
    """
    context_default = {
        "condition": None,
        "total_reward": None,
        "reward": None,
        "location": 0,
        "previous_action": None,
        "reaction_time": None,
        "info": None,
    }

    if step_context is not None:
        context_default.update(step_context)

    tracker = EnviromentTracker()
    ec = EnvironmentContext(mode=mode)
    st = StepContext(env_context=ec, tracker=tracker, **context_default)

    tracker.add_step()
    routine.setup(ec)
    routine.present(st)

    return tracker.steps[-1]
