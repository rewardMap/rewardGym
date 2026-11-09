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
    condition = context.condition

    actions = list(condition[0].keys())

    left_action = actions[0]
    right_action = actions[1]

    for stim in routine.state_definition_map:
        routine.stimuli[stim].setOpacity(0.0)

    if routine.border_name is not None:
        border = routine.stimuli[routine.border_name]
        border.setOpacity(0.0)

    state1 = condition[0][left_action]
    state2 = condition[0][right_action]

    if state1 is not None:
        stim_name_left = routine.state_definition_map[state1].name
        stim_left = routine.stimuli[stim_name_left]
        stim_left.pos = (-routine.stimulus_shift[0], stim_left.pos[1])
        stim_left.setOpacity(1.0)

    if state2 is not None:
        stim_name_right = routine.state_definition_map[state2].name
        stim_right = routine.stimuli[stim_name_right]
        stim_right.pos = (routine.stimulus_shift[0], stim_right.pos[1])
        stim_right.setOpacity(1.0)

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
