import numpy as np

from .psychopy_utils import update_psychopy_trials


def draw_response_reminder(context, text_update, reminder_duration=1.0):
    text_update.setAutoDraw(True)
    context.render.flip()
    reminder_onset = context.logger.get_time()

    context.render.wait(
        logger=context.logger,
        time=reminder_duration,
        start=reminder_onset,
        poll_keys=False,
    )
    text_update.setAutoDraw(False)
    context.render.flip()

    context.logger.log_event(
        {"event_type": "reminder", "expected_duration": reminder_duration},
        onset=reminder_onset,
    )

    return True


def break_point(context, text_update, settings, episode, countdown_cutoff=30):
    if not ("breakpoints" in settings and "break_duration" in settings):
        pass

    elif (
        episode in settings["breakpoints"]
        and settings["break_duration"] < countdown_cutoff
    ):
        break_onset = context.logger.get_time()

        context.render.wait(
            logger=context.logger,
            time=settings["break_duration"],
            start=break_onset,
            poll_keys=True,
            input_handler=context.input_handler,
        )

        context.logger.log_event(
            {"event_type": "break", "expected_duration": settings["break_duration"]},
            onset=break_onset,
        )

    elif episode in settings["breakpoints"]:
        break_onset = context.logger.get_time()
        break_text = "Short break. Keep lying as still as possible!\n"
        while context.logger.get_time() < (break_onset + settings["break_duration"]):
            time_left = settings["break_duration"] - (
                context.logger.get_time() - break_onset
            )
            minutes = int(time_left / 60)
            seconds = int(time_left - minutes * 60)
            text_update.setText(break_text + f"{minutes}:{seconds:02d}")
            text_update.draw()
            context.win.flip()

        context.logger.log_event(
            {"event_type": "break", "expected_duration": settings["break_duration"]},
            onset=break_onset,
        )


def simple_rt_simulation(agent, env, obs, info):
    key = agent.get_action(obs, info["action-layout"].avail_actions)
    probs = agent.get_probs(obs, info["action-layout"].avail_actions)
    probs = probs[key]

    if env.name in ["gonogo", "robotfactory"]:
        rt_extra = key * 2.0
    else:
        rt_extra = 0

    return key, (1 - probs) / 2 + rt_extra


class PsyPyPlugin:
    def __init__(self):
        pass

    def modify(self, **kwargs):
        pass


class MiscUpdateMid(PsyPyPlugin):
    def modify(self, *, env, logger, **kwargs):
        misc = env.info_dict[1]["render"][-1].duration
        logger.update_trial_info(
            misc=misc,
        )


class MiscUpdateTwoStep(PsyPyPlugin):
    def modify(self, *, env, logger, **kwargs):
        misc = [round(ii.p, 5) for ii in env.reward_locations.values()]
        logger.update_trial_info(
            misc=misc,
        )


class TimeUpdateMid(PsyPyPlugin):
    def modify(self, *, episode, settings, env, **kwargs):
        settings["reward"][episode] = (
            settings["reward"][episode] - env.info_dict[1]["render"][-1].duration
        )


class DelayUpdateHcp(PsyPyPlugin):
    def modify(self, *, settings, env, episode, **kwargs):
        settings["delay"][episode] = env.remainder
        update_psychopy_trials(settings, env, episode)


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
            new_duration = env.info_dict[1]["render"][-1].duration + adjustment
            new_duration = np.max([np.min([new_duration, 0.5]), 0.20])
            env.info_dict[1]["render"][-1].duration = new_duration


class AddRemainder(PsyPyPlugin):
    def modify(self, *, env, settings, logger, input_handler, **kwargs):
        if env.remainder > 0 and settings["add_remainder"]:
            rm_onset = logger.get_time()

            env.context.render.wait(
                logger=logger,
                time=env.remainder,
                start=rm_onset,
                input_handler=input_handler,
                poll_keys=True,
            )

            logger.log_event(
                {"event_type": "adjusting-time", "expected_duration": env.remainder},
                onset=rm_onset,
            )
