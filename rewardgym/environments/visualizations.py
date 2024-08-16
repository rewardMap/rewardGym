import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx

from ..utils import get_starting_nodes


def plot_env_graph(env):
    strip_graph = {
        ii: (jj[0] if isinstance(jj, tuple) else jj) for ii, jj in env.graph.items()
    }

    starting_node = get_starting_nodes(env.graph)
    reward_nodes = [ii for (ii, jj) in env.graph.items() if len(jj) == 0]
    nodes = list(env.graph.keys())

    other_nodes = list(set(nodes) - set(reward_nodes) - set(starting_node))

    nd = nx.DiGraph(strip_graph)
    pos = nx.planar_layout(nd, dim=2)
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
