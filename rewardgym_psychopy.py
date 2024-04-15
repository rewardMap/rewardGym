import json
import os

from psychopy import core, event, gui, visual

from rewardgym import ENVIRONMENTS, get_configs, get_env, unpack_conditions
from rewardgym.psychopy_render import ExperimentLogger, WaitTime, get_psychopy_info

outdir = "data/"

if not os.path.isdir(outdir):
    os.mkdir(outdir)

exp_dict = {"participant_id": "001", "run": 1, "task": ENVIRONMENTS}

dlg = gui.DlgFromDict(exp_dict)

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
)


logger_name = "sub-{0}_task-{1}_run-{2}_beh.tsv".format(
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
Wait = WaitTime(win, Logger)

task = exp_dict["task"]

info_dict = get_psychopy_info(task)
env, conditions = get_env(task)

try:
    settings = get_configs(task)
    if settings["condition_target"] == "location":
        conditions = (conditions[0], settings["condition"])
    elif settings["condition_target"] == "condition":
        conditions = (settings["condition"], conditions[1])

    n_episodes = settings["ntrials"]

    config_save = "sub-{0}_task-{1}_run-{2}_config.json".format(
        exp_dict["participant_id"], exp_dict["task"], exp_dict["run"]
    )

    with open(os.path.join(outdir, config_save), "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

except NotImplementedError:
    settings = None
    n_episodes = 5

if task == "risk-sensitive":
    action_map = env.condition_dict
else:
    action_map = None

if task == "mid":
    win_trials = 0

for k in info_dict.keys():
    [i.setup(win, action_map=action_map) for i in info_dict[k]["psychopy"]]

env.info_dict = info_dict

actions = []

# Begin the experiment
# TODO: Add instruction screen
instruction = visual.TextStim(
    win=win, text=f"Hi\nyou are playing:\n{Logger.task}", color=[1, 1, 1]
)

instruction.draw()
win.flip()
event.waitKeys()
win.flip()

# Recycling instruction
instruction.setText("Please respond faster!")


for episode in range(n_episodes):

    condition, starting_position = unpack_conditions(conditions, episode)

    # Update timings
    if settings["update"] is not None and len(settings["update"]) > 0:
        for k in settings["update"]:
            for jj in info_dict.keys():
                for ii in info_dict[jj]["psychopy"]:
                    if ii.name == k:
                        ii.duration = settings[k][episode]

    obs, info = env.reset(starting_position, condition=condition)
    Logger.trial = episode
    Logger.setTrialTime()
    Logger.trial_type = condition
    Logger.start_position = starting_position
    Logger.current_location = env.agent_location

    reward = None
    action = None

    for ii in info["psychopy"]:
        out = ii.display(
            win=win,
            logger=Logger,
            wait=Wait,
            reward=env.reward,
            condition=condition,
            starting_position=starting_position,
            action=None,
            total_reward=env.cumulative_reward,
        )

    if out is not None:
        action = out
        done = False
        actions.append(action)

    else:
        done = True
        instruction.draw()
        win.flip()
        core.wait(1.0)
        win.flip()

    while not done:
        next_obs, reward, terminated, truncated, info = env.step(action)
        Logger.current_location = env.agent_location
        for ii in info["psychopy"]:
            out = ii.display(
                win=win,
                logger=Logger,
                wait=Wait,
                reward=env.reward,
                condition=condition,
                starting_position=starting_position,
                action=action,
                total_reward=env.cumulative_reward,
            )

        done = terminated or truncated

        if out is None and not done and task == "two-step":
            instruction.draw()
            win.flip()
            core.wait(1.0)
            win.flip()
            done = True

        elif out is not None:
            action = out

    if task == "mid":

        win_trials += 1 if starting_position in [3, 4] else 0

        if (sum(actions) / (episode + 1)) < 0.4 and (win_trials % 3) == 0:
            info_dict[0]["psychopy"][-1].duration -= 0.025
        elif (win_trials % 3) == 0:
            info_dict[0]["psychopy"][-1].duration += 0.25

    Logger.logEvent(
        {"event_type": "TrialEnd", "total_reward": env.cumulative_reward},
        reward=env.reward,
    )


Logger.close()
win.close()
core.quit()
