try:
    from psychopy.visual import TextStim
except ModuleNotFoundError:
    from .psychopy_render.psychopy_stubs import TextStim

import numpy as np

from . import get_configs
from .utils import update_psychopy_trials


def draw_response_reminder(win, text_update, logger, reminder_duration=1.0):
    text_update.setAutoDraw(True)
    win.flip()
    reminder_onset = logger.get_time()
    logger.wait(win=win, time=reminder_duration, start=reminder_onset)
    text_update.setAutoDraw(False)
    win.flip()

    logger.log_event(
        {"event_type": "reminder", "expected_duration": reminder_duration},
        onset=reminder_onset,
    )

    return True


def break_point(win, text_update, logger, settings, episode, countdown_cutoff=30):
    if not ("breakpoints" in settings.keys() and "break_duration" in settings.keys()):
        pass

    elif (
        episode in settings["breakpoints"]
        and settings["break_duration"] < countdown_cutoff
    ):
        break_onset = logger.get_time()
        logger.wait(win, settings["break_duration"], break_onset)

        logger.log_event(
            {"event_type": "break", "expected_duration": settings["break_duration"]},
            onset=break_onset,
        )

    elif episode in settings["breakpoints"]:
        break_onset = logger.get_time()
        break_text = "Short break. Keep lying as still as possible!\n"
        while logger.get_time() < (break_onset + settings["break_duration"]):
            time_left = settings["break_duration"] - (logger.get_time() - break_onset)
            minutes = int(time_left / 60)
            seconds = int(time_left - minutes * 60)
            text_update.setText(break_text + f"{minutes}:{seconds:02d}")
            text_update.draw()
            win.flip()

        logger.log_event(
            {"event_type": "break", "expected_duration": settings["break_duration"]},
            onset=break_onset,
        )


def run_task(env, win, logger, settings=None, seed=111, agent=None, n_episodes=None):
    if settings is None:
        settings = get_configs(env.name)(seed)

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
        # Update timings
        if env.name == "mid":
            settings["reward"][episode] = (
                settings["reward"][episode] - env.info_dict[1]["psychopy"][-1].duration
            )
            misc = env.info_dict[1]["psychopy"][-1].duration
        elif env.name == "two-step":
            misc = [round(ii.p, 5) for ii in env.reward_locations.values()]
        else:
            misc = "n/a"

        update_psychopy_trials(settings, env, episode)

        logger.set_trial_time()
        logger.update_trial_info(
            trial_type=settings["condition"][episode],
            trial=episode,
            start_position=0,
            misc=misc,
        )

        obs, info = env.reset(
            0, condition=settings["condition_dict"][settings["condition"][episode]]
        )

        if env.action is None and agent is None:
            done = draw_response_reminder(win, response_reminder, logger)

        while not done:
            if agent is not None:
                # TODO Make this nicer
                key = agent.get_action(obs, info["avail-actions"])
                probs = agent.get_probs(obs, info["avail-actions"])
                probs = probs[key]

                if env.name == "gonogo":
                    rt_extra = key * 2.0
                else:
                    rt_extra = 0

                env.simulate_action(info, key, (1 - probs) / 2 + rt_extra)

            if env.name == "hcp":
                settings["wait"][episode] = env.remainder
                update_psychopy_trials(settings, env, episode)

            next_obs, reward, terminated, truncated, info = env.step(
                env.action, step_reward=env.name in ["two-step"]
            )
            actions.append(env.previous_action)
            logger.current_location = env.agent_location

            done = terminated or truncated

            if env.previous_action is None and not done:
                done = draw_response_reminder(win, response_reminder, logger)

            if agent is not None:
                agent.update(
                    obs, env.previous_remap_action, reward, terminated, next_obs
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
                new_duration = np.max([np.min([new_duration, 0.5]), 0.15])
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
