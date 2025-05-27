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


def simple_rt_simulation(agent, env, obs, info):
    key = agent.get_action(obs, info["avail-actions"])
    probs = agent.get_probs(obs, info["avail-actions"])
    probs = probs[key]

    if env.name == "gonogo":
        rt_extra = key * 2.0
    else:
        rt_extra = 0

    return key, (1 - probs) / 2 + rt_extra
