try:
    from psychopy.core import quit
    from psychopy.event import getKeys
    from psychopy.gui import Dlg, DlgFromDict
    from psychopy.visual import ImageStim, TextStim
except ModuleNotFoundError:
    from .psychopy_render.psychopy_stubs import (
        TextStim,
        ImageStim,
        DlgFromDict,
        Dlg,
        getKeys,
        quit,
    )

import os

import matplotlib.pyplot as plt
import numpy as np

from . import ENVIRONMENTS, get_configs
from .utils import update_psychopy_trials


def show_instructions(
    win,
    image_path,
    view_height=500,
    scroll_speed=50,
    width_scale=1.0,
    key_map=["left", "right", "down"],
    mode="behavior",
):
    image = plt.imread(image_path)[::-1, :, :]

    img_shape = image.shape
    y_pos = img_shape[0] - view_height

    button = ImageStim(
        win, image="assets/instructions/buttonbox.png", pos=(0, -view_height // 2 - 50)
    )
    button.setAutoDraw(True)

    if mode == "behavior":
        press_button = key_map[-1]
    elif mode == "fmri":
        press_button = "\n the third button (ring finger)."

    text = TextStim(
        win,
        text=f"To begin the task press {press_button}",
        pos=(0, -view_height // 2 - 100),
        height=20,
    )

    trigger = False

    while True:
        # Draw the image
        img = ImageStim(
            win,
            image=image[y_pos : view_height + y_pos, :],
            size=(int(img_shape[1] * width_scale), view_height),
        )
        img.draw()
        win.flip()

        # Check for keypresses
        keys = getKeys()

        if key_map[0] in keys:
            if (y_pos + view_height + scroll_speed) <= img_shape[0]:
                y_pos += scroll_speed

        elif key_map[1] in keys:
            if (y_pos - scroll_speed) >= 0:
                y_pos -= scroll_speed
            else:
                trigger = True

        elif key_map[2] in keys:
            # Exit the loop
            break

        if trigger:
            text.draw()

    button.setAutoDraw(False)
    win.flip()


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


def break_point(win, logger, settings, episode):
    if not ("breakpoints" in settings.keys() and "break_duration" in settings.keys()):
        pass

    elif episode in settings["breakpoints"]:
        break_onset = logger.get_time()
        logger.wait(win, settings["break_duration"], break_onset)

        logger.log_event(
            {"event_type": "break", "expected_duration": settings["break_duration"]},
            onset=break_onset,
        )


def set_up_experiment(outdir="data/"):
    exp_dict = {
        "participant_id": "001",
        "run": 1,
        "task": ENVIRONMENTS,
        "session": "01",
        "stimulus_set": 22,
        "mode": ["behavior", "fmri"],
        "fullscreen": False,
        "instructions": True,
        "outdir": outdir,
    }

    dlg = DlgFromDict(
        exp_dict,
        order=[
            "participant_id",
            "task",
            "run",
            "session",
            "stimulus_set",
            "mode",
            "fullscreen",
            "instructions",
            "outdir",
        ],
    )

    outdir = exp_dict["outdir"]

    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    if dlg.OK is False:
        quit()  # user pressed cancel

    if exp_dict["mode"] == "fmri":
        extension = "events"
        key_dict = {"9": 0, "8": 1}
        key_map = ["9", "8", "7"]

    elif exp_dict["mode"] == "behavior":
        extension = "beh"
        key_dict = {"left": 0, "right": 1, "space": 0}  # Just use default
        key_map = ["left", "right", "space"]

    exp_dict["key_map"] = key_map

    logger_name = "sub-{0}_ses-{1}_task-{2}_run-{3}_{4}.tsv".format(
        exp_dict["participant_id"],
        exp_dict["session"],
        exp_dict["task"],
        exp_dict["run"],
        extension,
    )
    logger_name = os.path.join(outdir, logger_name)

    config_save = "sub-{0}_ses-{1}_task-{2}_run-{3}_config.json".format(
        exp_dict["participant_id"],
        exp_dict["session"],
        exp_dict["task"],
        exp_dict["run"],
    )
    config_save = os.path.join(outdir, config_save)

    if os.path.isfile(logger_name):
        warning_dialog = Dlg(title=f"File Already Exists: {logger_name}")
        warning_dialog.addField("Overwrite", choices=["Yes", "No"])
        warning_data = warning_dialog.show()
        # Step 4: Handle the user's response
        if warning_data[0] == "Yes":
            pass
        else:
            quit()

    return (
        logger_name,
        config_save,
        key_dict,
        exp_dict["task"],
        exp_dict["fullscreen"],
        exp_dict["mode"],
        exp_dict["stimulus_set"],
        exp_dict,
    )


def run_task(env, win, logger, settings=None, seed=111, agent=None, n_episodes=None):
    if settings is None:
        settings = get_configs(env.name)(seed)

    if n_episodes is None:
        n_episodes = settings["ntrials"]

    response_reminder = TextStim(
        win=win,
        text="Please respond faster!",
        color=[1, 1, 1],
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

        if env.action is None:
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
                env.action, step_reward=env.name == "two-step"
            )
            actions.append(env.previous_action)
            logger.current_location = env.agent_location

            done = terminated or truncated

            if env.action is None and not done:
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

        break_point(win, logger, settings, episode)
