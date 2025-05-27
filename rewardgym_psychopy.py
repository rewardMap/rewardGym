import json

from psychopy import core, event, visual

from assets import show_instructions
from rewardgym import get_configs, get_env
from rewardgym.psychopy_render import ExperimentLogger, get_psychopy_info
from rewardgym.runner import pspy_run_task, pspy_set_up_experiment
from rewardgym.tasks import FULLPOINTS

if __name__ == "__main__":
    (
        logger_name,
        config_save,
        key_dict,
        task,
        fullscreen,
        mode,
        stimulus_set,
        exp_dict,
    ) = pspy_set_up_experiment()

    globalClock = core.Clock()

    win = visual.Window(
        size=[1680, 1050],
        fullscr=fullscreen,
        winType="pyglet",
        allowGUI=True,
        color=[-0.5, -0.5, -0.5],
        colorSpace="rgb",
        units="pix",
    )

    Logger = ExperimentLogger(
        logger_name,
        globalClock,
        participant_id=exp_dict["participant_id"],
        run=exp_dict["run"],
        task=exp_dict["task"],
        mr_clock=globalClock,
    )
    Logger.create()

    info_dict, stimulus_info = get_psychopy_info(
        task, seed=stimulus_set, key_dict=key_dict
    )
    settings = get_configs(task)(stimulus_set)

    exp_dict["setting"] = settings
    exp_dict["stimulus_info"] = stimulus_info

    with open(config_save, "w", encoding="utf-8") as f:
        json.dump(exp_dict, f, ensure_ascii=False, indent=4)

    env = get_env(
        task,
        window=win,
        logger=Logger,
        render_backend="psychopy",
    )

    env.add_info(info_dict)

    if exp_dict["instructions"]:
        show_instructions(task, win, key_map=key_dict)

    if mode == "fmri":
        scanner_info = visual.TextStim(
            win=win,
            text="Waiting for scanner...",
            color=[1, 1, 1],
            height=24,
        )

        scanner_info.draw()
        win.flip()
        event.waitKeys(keyList=["5"])
        win.flip()
    else:
        scanner_info = visual.TextStim(
            win=win,
            text="Are you ready?\nPress any key to begin!",
            color=[1, 1, 1],
            height=24,
        )

        scanner_info.draw()
        win.flip()
        event.waitKeys()
        win.flip()

    Logger.global_clock.reset()

    env.setup(window=win, logger=Logger)

    pspy_run_task(env=env, win=win, logger=Logger, settings=settings, n_episodes=None)

    win.to_Draw = []
    proportion = max([min([env.cumulative_reward / FULLPOINTS[task], 1.0]), 0])

    final = visual.TextStim(
        win=win,
        text=f"You are done!\nThank you!\nYou got {env.cumulative_reward} points!\nWhich is a score of {proportion:4.2f} %!",
        color=[1, 1, 1],
        pos=(0, 150),
        height=24,
    )
    final.draw()
    win.flip()
    event.waitKeys(keyList=["space"])
    win.flip()

    Logger.close()
    win.close()
    core.quit()
