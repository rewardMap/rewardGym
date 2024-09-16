import json

from psychopy import core, event, visual

from rewardgym import get_configs, get_env
from rewardgym.psychopy_core import run_task
from rewardgym.psychopy_extras import set_up_experiment, show_instructions
from rewardgym.psychopy_render import ExperimentLogger, get_psychopy_info

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
    ) = set_up_experiment()

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
        show_instructions(
            win,
            "assets/instructions/risk-sensitive.png",
            key_map=exp_dict["key_map"],
            mode=mode,
        )

    if mode == "fmri":
        scanner_info = visual.TextStim(
            win=win,
            text="Waiting for scanner...",
            color=[1, 1, 1],
        )

        scanner_info.draw()
        win.flip()
        event.waitKeys(keyList=["5"])
        win.flip()

    Logger.global_clock.reset()

    env.setup(window=win, logger=Logger)

    run_task(env=env, win=win, logger=Logger, settings=settings, n_episodes=3)

    win.to_Draw = []

    final = visual.TextStim(
        win=win,
        text="You are done!\nThank you!",
        color=[1, 1, 1],
        pos=(150, 0.0),
        height=20,
    )
    final.draw()
    win.flip()
    event.waitKeys()
    win.flip()

    Logger.close()
    win.close()
    core.quit()
