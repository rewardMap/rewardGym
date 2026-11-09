from .contexts import StepContext
from .passive_routines import DynamicRoutine


def conditioned_text(routine: DynamicRoutine, context: StepContext):
    if routine.update_target == "action":
        conditioned_text = routine.condition_text[context.previous_action]
    elif routine.update_target == "reward":
        conditioned_text = routine.condition_text[context.reward]

    conditioned_text = context.env_context.random_state.choice(conditioned_text)
    routine.stimuli[routine.text_name].setText(conditioned_text)
