try:
    from psychopy.visual import TextStim
except ModuleNotFoundError:
    from ..psychopy_render.psychopy_stubs import TextStim, Window

from typing import Dict

import numpy as np

from ..psychopy_render.psychopy_stubs import Window
from ..tasks import get_configs
from .psychopy_plugins import (
    AddRemainder,
    DelayUpdateHcp,
    MiscUpdateMid,
    MiscUpdateTwoStep,
    StairCaseMid,
    TimeUpdateMid,
    break_point,
    draw_response_reminder,
    simple_rt_simulation,
)
from .psychopy_utils import apply_plugins, update_psychopy_trials

plugin_registry = {
    "mid": {
        "pre-trial": [MiscUpdateMid(), TimeUpdateMid()],
        "post-trial": [AddRemainder(), StairCaseMid(0)],
    },
    "hcp": {
        "post-action": [DelayUpdateHcp()],
    },
    "risk-sensitive": {"post-trial": [AddRemainder()]},
    "two-step": {"pre-trial": [MiscUpdateTwoStep()], "post-trial": [AddRemainder()]},
    "posner": {"post-trial": [AddRemainder()]},
    "gonogo": {"post-trial": [AddRemainder()]},
}


def pspy_run_task(
    env,
    logger,
    win=None,
    settings=None,
    seed=111,
    agent=None,
    n_episodes=None,
    plugins: Dict = plugin_registry,
):
    if settings is None:
        settings = get_configs(env.name)(seed)

    if win is None:
        win = Window()

    plugins = plugins[env.name]

    if n_episodes is None:
        n_episodes = settings["ntrials"]

    if env.render_mode == "psychopy-simulate":
        break_countdown_limit = np.inf
    else:
        break_countdown_limit = 30

    response_reminder = TextStim(
        win=win,
        text="Please respond faster!",
        color=[1, 1, 1],
        pos=(0, 100),
        height=25,
    )
    break_text = TextStim(
        win=win,
        text="Have a break.",
        color=[1, 1, 1],
        pos=(0, 100),
        height=25,
    )

    actions = []

    for episode in range(n_episodes):
        done = False

        logger.update_trial_info(
            trial=episode,
            start_position=0,
            misc="n/a",
        )

        apply_plugins(
            plugins=plugins,
            entry_point="pre-trial",
            env=env,
            logger=logger,
            settings=settings,
            episode=episode,
            actions=actions,
            win=win,
        )

        update_psychopy_trials(settings, env, episode)

        logger.set_trial_time()
        logger.update_trial_info(
            trial_type=settings["condition"][episode],
        )

        obs, info = env.reset(
            0, condition=settings["condition_dict"][settings["condition"][episode]]
        )
        if env.action is None and agent is None:
            done = draw_response_reminder(win, response_reminder, logger)

        while not done:
            if agent is not None:
                if hasattr(agent, "get_rt_action") and callable(agent.get_rt_action):
                    key, rt = agent.get_rt_action(obs, info["avail-actions"])
                else:
                    key, rt = simple_rt_simulation(agent, env, obs, info)

                env.simulate_action(info, key, rt)

            apply_plugins(
                plugins=plugins,
                entry_point="post-action",
                env=env,
                logger=logger,
                settings=settings,
                episode=episode,
                actions=actions,
                win=win,
            )

            next_obs, reward, terminated, truncated, info = env.step(
                env.action, step_reward=env.name in ["two-step"]
            )
            actions.append(env.previous_action)
            logger.current_location = env.agent_location

            done = terminated or truncated
            # TODO check if this should be action, not previous action!
            if agent is None:
                if env.action is None and not done:
                    done = draw_response_reminder(win, response_reminder, logger)

            elif not (done and env.previous_action is None):
                agent.update(
                    obs, env.previous_action, reward, terminated, next_obs, info=info
                )
                obs = next_obs

            apply_plugins(
                plugins=plugins,
                entry_point="post-trial",
                env=env,
                logger=logger,
                settings=settings,
                episode=episode,
                actions=actions,
                win=win,
            )

        logger.log_event(
            {"event_type": "trial-end", "total_reward": env.cumulative_reward},
            reward=env.reward,
        )

        break_point(
            win,
            break_text,
            logger,
            settings,
            episode,
            countdown_cutoff=break_countdown_limit,
        )

    return logger, env, agent
