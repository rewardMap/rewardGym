from .contexts import StepContext
from ..environments.base_env import ActionLayout


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
    layout = ActionLayout(actions)  # context.info['action-layout']

    for name in routine.state_definition_map.values():
        routine.stimuli[name.name].setOpacity(1.0)

    if routine.border_name is not None:
        border = routine.stimuli[routine.border_name]

    for _, act in enumerate(actions):
        if act is not None:
            state_name = routine.state_definition_map[act].name
            stim = routine.stimuli[state_name]
            stim.pos = routine.position_map[layout.graph_to_action[act]]
            routine.draw_list.append(state_name)

            if routine.selection:
                if context.previous_action == act:
                    if routine.border_name is not None:
                        set_border(border, stim)
                        routine.draw_list.append(routine.border_name)

                else:
                    stim.setOpacity(0.25)


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
