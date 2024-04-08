import os

from psychopy import core, gui, visual

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
    size=[1200, 1000],
    fullscr=False,
    screen=0,
    winType="pyglet",
    allowGUI=True,
    color=[-0.7, -0.7, -0.7],
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

except NotImplementedError:
    settings = None
    n_episodes = 5

if task == "risk-sensitive":
    action_map = env.condition_dict
else:
    action_map = None

for k in info_dict.keys():
    [i.setup(win, action_map=action_map) for i in info_dict[k]["psychopy"]]

env.info_dict = info_dict

actions = []

for episode in range(n_episodes):

    condition, starting_position = unpack_conditions(conditions, episode)

    # Update timings
    if len(settings["update"]) > 0 and settings is not None:
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
    reward = None

    for ii in info["psychopy"]:
        out = ii(
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

    # play one episode
    while not done:
        next_obs, reward, terminated, truncated, info = env.step(action)

        for ii in info["psychopy"]:
            out = ii(
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

    print("performance", sum(actions) / (episode + 1))

    if task == "mid":
        if (sum(actions) / (episode + 1)) < 0.4:
            info_dict[0]["psychopy"][-1].duration -= 0.1
        else:
            info_dict[0]["psychopy"][-1].duration += 0.1

    Logger.logEvent({"event_type": "TrialEnd"}, reward=reward)
