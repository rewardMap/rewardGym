try:
    from psychopy.visual import TextStim
except ModuleNotFoundError:
    from ..psychopy_render.psychopy_stubs import TextStim, Window

from typing import Dict

import numpy as np

from ..psychopy_render.psychopy_stubs import Window
from ..tasks.utils import get_configs
from .psychopy_plugins import break_point, draw_response_reminder, simple_rt_simulation
from .psychopy_utils import update_psychopy_trials


class PsyPyPlugin:
    def __init__(self):
        pass

    def modify(self, **kwargs):
        pass


class MiscUpdateMid(PsyPyPlugin):
    def modify(self, *, env, logger, **kwargs):
        misc = env.info_dict[1]["psychopy"][-1].duration
        logger.update_trial_info(
            misc=misc,
        )
        return None


class MiscUpdateTwoStep(PsyPyPlugin):
    def modify(self, *, env, logger, **kwargs):
        misc = [round(ii.p, 5) for ii in env.reward_locations.values()]
        logger.update_trial_info(
            misc=misc,
        )
        return None


class TimeUpdateMid(PsyPyPlugin):
    def modify(self, *, episode, settings, env, **kwargs):
        settings["reward"][episode] = (
            settings["reward"][episode] - env.info_dict[1]["psychopy"][-1].duration
        )

        return None


class DelayUpdateHcp(PsyPyPlugin):
    def modify(self, *, settings, env, episode, **kwargs):
        settings["delay"][episode] = env.remainder
        update_psychopy_trials(settings, env, episode)

        return None


class StairCaseMid(PsyPyPlugin):
    def __init__(self, trial_counter=0):
        self.trial_counter = trial_counter

    def modify(self, *, settings, episode, env, actions, **kwargs):
        if settings["condition"][episode] in ["win-large", "win-small"]:
            self.trial_counter += 1

            if (self.trial_counter % 3) == 0:
                adjustment = (
                    -0.025 if (np.nansum(actions) / (episode + 1)) < 0.4 else 0.025
                )
            else:
                adjustment = 0

            # Duration is at minimum 150 ms and at max 500 ms, need to only update first occurence
            # of first stimulus, as it's reused
            new_duration = env.info_dict[1]["psychopy"][-1].duration + adjustment
            new_duration = np.max([np.min([new_duration, 0.5]), 0.20])
            env.info_dict[1]["psychopy"][-1].duration = new_duration


class AddRemainder(PsyPyPlugin):
    def modify(self, *, env, settings, win, logger, **kwargs):
        if env.remainder > 0 and settings["add_remainder"]:
            rm_onset = logger.get_time()
            logger.wait(win, env.remainder, rm_onset)

            logger.log_event(
                {"event_type": "adjusting-time", "expected_duration": env.remainder},
                onset=rm_onset,
            )


# Plugins use different entrypoints:

{
    "pre-trial": [],
    "after-action": [],
    "post-trial": [],
}

plugin_registry = {
    "mid": {
        "pre-trial": [MiscUpdateMid(), TimeUpdateMid()],
        "post-trial": [AddRemainder(), StairCaseMid(0)],
    }
}


def pspy_run_task(
    env,
    logger,
    win=None,
    settings=None,
    seed=111,
    agent=None,
    n_episodes=None,
    plugins: Dict = None,
):
    if settings is None:
        settings = get_configs(env.name)(seed)

    if win is None:
        win = Window()

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

    win_trials = 0
    actions = []

    for episode in range(n_episodes):
        done = False

        logger.update_trial_info(
            trial=episode,
            start_position=0,
            misc="n/a",
        )

        # Update timings
        if env.name == "mid":
            settings["reward"][episode] = (
                settings["reward"][episode] - env.info_dict[1]["psychopy"][-1].duration
            )
            misc = env.info_dict[1]["psychopy"][-1].duration
        elif env.name == "two-step":
            misc = [round(ii.p, 5) for ii in env.reward_locations.values()]

        print(misc)  # Going to remove in next commit
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

            if env.name == "hcp":
                settings["delay"][episode] = env.remainder
                update_psychopy_trials(settings, env, episode)

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

        # TODO: Also a different function?
        if env.remainder > 0 and settings["add_remainder"]:
            rm_onset = logger.get_time()
            logger.wait(win, env.remainder, rm_onset)

            logger.log_event(
                {"event_type": "adjusting-time", "expected_duration": env.remainder},
                onset=rm_onset,
            )

        # TODO how to deal with this nicely?
        if env.name == "mid":
            if settings["condition"][episode] in ["win-large", "win-small"]:
                win_trials += 1

                if (win_trials % 3) == 0:
                    adjustment = (
                        -0.025 if (np.nansum(actions) / (episode + 1)) < 0.4 else 0.025
                    )
                else:
                    adjustment = 0

                # Duration is at minimum 150 ms and at max 500 ms, need to only update first occurence
                # of first stimulus, as it's reused
                new_duration = env.info_dict[1]["psychopy"][-1].duration + adjustment
                new_duration = np.max([np.min([new_duration, 0.5]), 0.20])
                env.info_dict[1]["psychopy"][-1].duration = new_duration

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
