from .contexts import StepContext


def conditioned_text(routine, context: StepContext):
    if routine.update_target == "action":
        conditioned_text = routine.condition_text[context.previous_action]
    elif routine.update_target == "reward":
        conditioned_text = routine.condition_text[context.reward]

    conditioned_text = context.env_context.random_state.choice(conditioned_text)
    routine.stimuli[routine.text_name].setText(conditioned_text)


def set_border(border, stim, opacity=0.25):
    border.width = stim.size[0]
    border.height = stim.size[1]
    border.pos = stim.pos
    border.setOpacity(opacity)


def state_selection_with_highlight(routine, context):
    routine.draw_list = []
    condition = context.condition

    actions = list(condition[0].keys())

    left_action = actions[0]
    right_action = actions[1]

    if routine.border_name is not None:
        border = routine.stimuli[routine.border_name]

    state1 = condition[0][left_action]
    state2 = condition[0][right_action]

    if state1 is not None:
        stim_name_left = routine.state_definition_map[state1].name
        stim_left = routine.stimuli[stim_name_left]
        stim_left.pos = (-routine.stimulus_shift[0], stim_left.pos[1])
        routine.draw_list.append(stim_name_left)

    if state2 is not None:
        stim_name_right = routine.state_definition_map[state2].name
        stim_right = routine.stimuli[stim_name_right]
        stim_right.pos = (routine.stimulus_shift[0], stim_right.pos[1])
        routine.draw_list.append(stim_name_right)

    if routine.selection:
        if context.previous_action == left_action:
            if routine.border_name is not None:
                set_border(border, stim_left)

            if state2 is not None:
                stim_right.setOpacity(0.25)

        else:
            if routine.border_name is not None:
                set_border(border, stim_right)

            if state1 is not None:
                stim_left.setOpacity(0.25)

        routine.draw_list.append(routine.border_name)


def reward_update_routine(routine, context):
    routine.draw_list = []

    reward = context.reward
    reward_outcome = f"+{reward:5.1f}" if reward > 0 else f"{reward:5.1f}"

    total_reward = context.total_reward

    if routine.component_names["reward_total"] is not None:
        reward_outcome_total = (
            f"+{total_reward:5.1f}" if total_reward > 0 else f"{total_reward:5.1f}"
        )
        total_reward_string = routine.total_reward_text_template.format(
            reward=reward_outcome_total
        )

    reward_string = routine.reward_text_template.format(reward=reward_outcome)

    if reward > 0:
        feedback_img = "stim_win"
    elif reward < 0:
        feedback_img = "stim_lose"
    else:
        feedback_img = "stim_zero"

    routine.stimuli[routine.component_names["reward"]].setText(reward_string)
    routine.draw_list.append(routine.component_names["reward"])

    if routine.component_names["reward_total"] is not None:
        routine.stimuli[routine.component_names["reward_total"]].setText(
            total_reward_string
        )
        routine.draw_list.append(routine.component_names["reward_total"])

    if routine.component_names[feedback_img] is not None:
        routine.draw_list.append(routine.component_names[feedback_img])

    if routine.component_names["bar"] is not None:
        bar = routine.stimuli[routine.component_names["bar"]]
        bar_indicator = routine.stimuli[routine.component_names["indicator"]]
        move_bar = int((total_reward / routine.bar_total) * bar.width)
        move_bar = min([max([move_bar, 0]), bar.width])
        bar_indicator.setPos((-bar.width // 2 + move_bar, 350))
