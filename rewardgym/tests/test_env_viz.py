from .. import ENVIRONMENTS, get_env
from ..environments.visualizations import plot_env_graph


def test_plot_graph_env():

    for ii in ENVIRONMENTS:
        plot_env_graph(get_env(ii)[0])
