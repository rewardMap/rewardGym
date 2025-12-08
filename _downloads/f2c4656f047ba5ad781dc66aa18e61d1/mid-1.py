from rewardgym import get_env
from rewardgym.environments.visualizations import plot_env_graph
env = get_env("mid")
plot_env_graph(env)