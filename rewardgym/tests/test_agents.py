def test_Qagent_smokescreens():
    from .. import ENVIRONMENTS, get_env
    from ..agents import base_agent
    from ..utils import run_single_episode, unpack_conditions

    for envname in ENVIRONMENTS:
        n_episodes = 20
        env, conditions = get_env(envname)

        agent = base_agent.QAgent(
            learning_rate=0.25,
            temperature=1.0,
            discount_factor=0.99,
            action_space=env.action_space.n,
            state_space=env.n_states,
        )

        for ne in range(n_episodes):

            condition, starting_position = unpack_conditions(conditions, ne)

            if envname == "risk-sensitive":
                avail_actions = list(env.condition_dict[condition].values())
            else:
                avail_actions = None

            a = run_single_episode(
                env,
                agent,
                starting_position,
                condition,
                step_reward=envname == "two-step",
                avail_actions=avail_actions,
            )


def test_ValenceQagent_smokescreens():
    from .. import ENVIRONMENTS, get_env
    from ..agents import base_agent
    from ..utils import run_single_episode, unpack_conditions

    for lrs in [[0.5, 0.5], [0.2, 0.5], [0.5, 0.2]]:

        for envname in ENVIRONMENTS:
            n_episodes = 20
            env, conditions = get_env(envname)

            agent = base_agent.ValenceQAgent(
                learning_rate_pos=lrs[0],
                learning_rate_neg=lrs[1],
                temperature=1.0,
                discount_factor=0.99,
                action_space=env.action_space.n,
                state_space=env.n_states,
            )

            for ne in range(n_episodes):

                condition, starting_position = unpack_conditions(conditions, ne)

                if envname == "risk-sensitive":
                    avail_actions = list(env.condition_dict[condition].values())
                else:
                    avail_actions = None

                a = run_single_episode(
                    env,
                    agent,
                    starting_position,
                    condition,
                    step_reward=envname == "two-step",
                    avail_actions=avail_actions,
                )


def test_RandomAgent_smokescreens():
    from .. import ENVIRONMENTS, get_env
    from ..agents import base_agent
    from ..utils import run_single_episode, unpack_conditions

    for bias in [0.25, 0.5, 0.75]:

        for envname in ENVIRONMENTS:
            n_episodes = 20
            env, conditions = get_env(envname)

            agent = base_agent.RandomAgent(
                bias=bias,
                action_space=env.action_space.n,
                state_space=env.n_states,
            )

            for ne in range(n_episodes):

                condition, starting_position = unpack_conditions(conditions, ne)

                if envname == "risk-sensitive":
                    avail_actions = list(env.condition_dict[condition].values())
                else:
                    avail_actions = None

                a = run_single_episode(
                    env,
                    agent,
                    starting_position,
                    condition,
                    step_reward=envname == "two-step",
                    avail_actions=avail_actions,
                )
