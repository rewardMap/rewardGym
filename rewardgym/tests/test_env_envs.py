from rewardgym.environments import BaseEnv


class TestBaseEnv:
    def test_initialization(self):
        environment_graph = {0: [1, 2], 1: [0], 2: [0]}
        reward_locations = {1: lambda: 1, 2: lambda: 2}
        env = BaseEnv(environment_graph, reward_locations)
        assert env.n_actions == 2
        assert env.n_states == 3
        assert env.agent_location is None
        assert env.cumulative_reward == 0

    def test_reset(self):
        environment_graph = {0: [1, 2], 1: [0], 2: [0]}
        reward_locations = {1: lambda: 1, 2: lambda: 2}
        env = BaseEnv(environment_graph, reward_locations)
        obs, info = env.reset(agent_location=0)
        print(info)
        assert obs == 0
        assert info == {"avail-actions": [0, 1], "skip-node": False, "obs": 0}

    def test_step(self):
        environment_graph = {0: [1, 2], 1: [], 2: []}
        reward_locations = {1: lambda: 1, 2: lambda: 2}
        env = BaseEnv(environment_graph, reward_locations)
        env.reset(agent_location=0)
        obs, reward, terminated, truncated, info = env.step(action=0)
        assert obs == 1
        assert reward == 1
        assert terminated is True
        assert truncated is False
        assert env.cumulative_reward == 1
