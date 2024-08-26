import json
import os

import numpy as np
from psychopy import core, event, gui, visual

from rewardgym import ENVIRONMENTS, get_configs, get_env
from rewardgym.psychopy_render import ExperimentLogger, get_psychopy_info
from rewardgym.utils import update_psychopy_trials

outdir = "data/"

if not os.path.isdir(outdir):
    os.mkdir(outdir)

exp_dict = {
    "participant_id": "001",
    "run": 1,
    "task": ENVIRONMENTS,
    "condition_set": 20,
    "stimulus_set": 22,
    "mode": ["behavior", "fmri"],
}

dlg = gui.DlgFromDict(
    exp_dict,
    order=["participant_id", "task", "run", "condition_set", "stimulus_set", "mode"],
)

if dlg.OK is False:
    core.quit()  # user pressed cancel

globalClock = core.Clock()

win = visual.Window(
    size=[1680, 1050],
    fullscr=False,
    screen=0,
    winType="pyglet",
    allowGUI=True,
    color=[-0.5, -0.5, -0.5],
    colorSpace="rgb",
    units="pix",
    waitBlanking=False,
    useFBO=False,
    checkTiming=True,
)

if exp_dict["mode"] == "fmri":
    extension = "events.tsv"
    key_dict = {"9": 0, "7": 1}
elif exp_dict["mode"] == "behavior":
    extension = "beh.tsv"
    key_dict = {"left": 0, "right": 1, "space": 0}  # Just use default

logger_name = "sub-{0}_task-{1}_run-{2}_{3}.tsv".format(
    exp_dict["participant_id"], exp_dict["task"], exp_dict["run"], extension
)

config_save = "sub-{0}_task-{1}_run-{2}_config.json".format(
    exp_dict["participant_id"], exp_dict["task"], exp_dict["run"]
)

Logger = ExperimentLogger(
    os.path.join(outdir, logger_name),
    globalClock,
    participant_id=exp_dict["participant_id"],
    run=exp_dict["run"],
    task=exp_dict["task"],
)
Logger.create()

task = exp_dict["task"]

info_dict, stimulus_info = get_psychopy_info(
    task, seed=exp_dict["stimulus_set"], key_dict=key_dict
)

exp_dict["stimulus_info"] = stimulus_info

env = get_env(
    task,
    window=win,
    logger=Logger,
    render_backend="psychopy",
)

settings = get_configs(task)(exp_dict["stimulus_set"])

n_episodes = settings["ntrials"]
exp_dict["setting"] = settings


with open(os.path.join(outdir, config_save), "w", encoding="utf-8") as f:
    json.dump(exp_dict, f, ensure_ascii=False, indent=4)


if task == "mid":
    win_trials = 0

env.add_info(info_dict)

actions = []

# Begin the experiment
# TODO: Add instruction screen
instruction = visual.TextStim(
    win=win,
    text=f"Hi\nyou are playing:\n{Logger.task}\nPress 5 to continue.",
    color=[1, 1, 1],
)

instruction.draw()
win.flip()
event.waitKeys(keyList=["5"])
win.flip()
Logger.global_clock.reset()

# Recycling instruction
instruction.setText("Please respond faster!")
env.setup_render(window=win, logger=Logger)


for episode in range(n_episodes):
    # Update timings
    if task == "mid":
        settings["reward"][episode] = (
            settings["reward"][episode] - info_dict[1]["psychopy"][-1].duration
        )
        print("reward duration:", settings["reward"][episode])

    update_psychopy_trials(settings, env, episode)

    Logger.trial = episode
    Logger.set_trial_time()
    Logger.trial_type = settings["condition"][episode]
    Logger.start_position = 0

    obs, info = env.reset(
        0, condition=settings["condition_dict"][settings["condition"][episode]]
    )

    reward = None
    remainder = None
    done = False

    if env.action is None:
        done = True
        instruction.draw()
        win.flip()
        core.wait(1.0)
        win.flip()

    while not done:
        next_obs, reward, terminated, truncated, info = env.step(env.action)
        actions.append(env.previous_action)
        Logger.current_location = env.agent_location

        done = terminated or truncated

        if env.action is None and not done:
            instruction.draw()
            win.flip()
            core.wait(1.0)
            win.flip()
            done = True

    if env.remainder > 0:
        rm_onset = Logger.get_time()
        Logger.wait(win, env.remainder, rm_onset)

        Logger.log_event(
            {"event_type": "adjusting-time", "expected_duration": env.remainder},
            onset=rm_onset,
        )

    if task == "mid":
        win_trials += (
            1 if settings["condition"][episode] in ["win-large", "win-small"] else 0
        )
        adjust = (
            1 if settings["condition"][episode] in ["win-large", "win-small"] else 0
        )

        if (
            (np.nansum(actions) / (episode + 1)) < 0.4
            and (win_trials % 3) == 0
            and adjust
        ):
            for stim in [1, 2, 3, 4, 5]:
                if (info_dict[stim]["psychopy"][-1].duration - 0.025) >= 0.15:
                    info_dict[stim]["psychopy"][-1].duration -= 0.025
            adjust = 0
        elif (win_trials % 3) == 0 and adjust:
            for stim in [1, 2, 3, 4, 5]:
                if (info_dict[stim]["psychopy"][-1].duration + 0.025) <= 0.5:
                    info_dict[stim]["psychopy"][-1].duration += 0.025
            adjust = 0

    Logger.log_event(
        {"event_type": "trial-end", "total_reward": env.cumulative_reward},
        reward=env.reward,
    )


final = visual.TextStim(win=win, text="You are done!\nThank you!", color=[1, 1, 1])

final.draw()
win.flip()
event.waitKeys()
win.flip()


Logger.close()
win.close()
core.quit()
