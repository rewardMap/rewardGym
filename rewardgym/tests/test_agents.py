from rewardgym import ENVIRONMENTS, get_env
from rewardgym.agents import base_agent
from rewardgym.utils import run_single_episode


def test_Qagent_smokescreens():
    for envname in ENVIRONMENTS:
        n_episodes = 20
        env = get_env(envname)

        agent = base_agent.QAgent(
            learning_rate=0.25,
            temperature=1.0,
            discount_factor=0.99,
            action_space=env.action_space.n,
            state_space=env.n_states,
        )

        for _ in range(n_episodes):
            run_single_episode(
                env,
                agent,
                0,
                None,
                step_reward=envname == "two-step",
            )


def test_ValenceQagent_smokescreens():
    for lrs in [[0.5, 0.5], [0.2, 0.5], [0.5, 0.2]]:
        for envname in ENVIRONMENTS:
            n_episodes = 20
            env = get_env(envname)

            agent = base_agent.ValenceQAgent(
                learning_rate_pos=lrs[0],
                learning_rate_neg=lrs[1],
                temperature=1.0,
                discount_factor=0.99,
                action_space=env.action_space.n,
                state_space=env.n_states,
            )

            for _ in range(n_episodes):
                run_single_episode(
                    env,
                    agent,
                    0,
                    None,
                    step_reward=envname == "two-step",
                )


def test_RandomAgent_smokescreens():
    for bias in [0.25, 0.5, 0.75]:
        for envname in ENVIRONMENTS:
            n_episodes = 20
            env = get_env(envname)

            agent = base_agent.RandomAgent(
                bias=bias,
                action_space=env.action_space.n,
                state_space=env.n_states,
            )

            for _ in range(n_episodes):
                run_single_episode(
                    env,
                    agent,
                    0,
                    None,
                    step_reward=envname == "two-step",
                )
