from rewardgym import get_env
from rewardgym.environments.visualizations import plot_env_graph
env, conditions = get_env("risk-sensitive")
plot_env_graph(env)