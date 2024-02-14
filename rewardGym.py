import os

from psychopy import core, gui, visual

from rewardgym import ENVIRONMENTS, unpack_conditions
from rewardgym.psychopy_render.helper import get_env
from rewardgym.psychopy_render.logger import ExperimentLogger
from rewardgym.psychopy_render.stimuli import WaitTime

outdir = "data/"

exp_dict = {"participant_id": "001", "run": 1, "task": ENVIRONMENTS}

dlg = gui.DlgFromDict(exp_dict)

if dlg.OK is False:
    core.quit()  # user pressed cancel

globalClock = core.Clock()

win = visual.Window(
    size=[700, 500],
    fullscr=False,
    screen=0,
    winType="pyglet",
    allowGUI=True,
    monitor=None,
    color=[-1, -1, -1],
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

if task == "hcp":
    from rewardgym.psychopy_render.hcp import info_dict
elif task == "mid":
    from rewardgym.psychopy_render.mid import info_dict
elif task == "risk-sensitive":
    from rewardgym.psychopy_render.risk_sensitive import info_dict
elif task == "two-step":
    from rewardgym.psychopy_render.two_step import info_dict
elif task == "gonogo":
    from rewardgym.psychopy_render.gonogo import info_dict
elif task == "posner":
    from rewardgym.psychopy_render.posner import info_dict


env, conditions = get_env(task)

if task == "risk-sensitive":
    action_map = env.condition_dict
else:
    action_map = None

for k in info_dict.keys():
    [i.setup(win, action_map=action_map) for i in info_dict[k]["psychopy"]]


env.info_dict = info_dict

n_episodes = 5

actions = []

for episode in range(n_episodes):

    condition, starting_position = unpack_conditions(conditions, episode)

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
