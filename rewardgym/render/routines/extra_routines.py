from ..contexts import StepContext
from ..events import log_event
from .base_routine import BaseRoutine


class InstructionRoutine(BaseRoutine):
    def __init__(
        self,
        name: str,
        stimulus_definitions,
    ):
        super().__init__(
            name=name,
            duration=None,
            stimulus_definitions=stimulus_definitions,
            flip=True,
            poll_keys=False,
        )

    def display(self, context):
        for stim in self.stimuli.values():
            if stim.opacity > 0:
                stim.draw()

        context.render.flip()


class AutoAction(BaseRoutine):
    def __init__(self, name: str, key_dict: dict, rl_label: str | None = None):
        super().__init__(
            name=name,
            duration=None,
            rl_label=rl_label,
            flip=False,
            poll_keys=False,
            stimulus_definitions=None,
        )
        self.key_dict = key_dict
        self.returns_action = True

    def display(self, context: StepContext):
        key, action = next(iter(self.key_dict.items()))
        layout = context.info["action-layout"]

        env_action = layout.action_to_graph[action]

        response = (action, None)

        context.tracker.add_event(
            frame=None,
            duration=None,
            action=response[0],
            reaction_time=response[1],
            name=self.rl_label,
        )

        log_event(
            self,
            logger=context.logger,
            extra_info={
                "response_button": key,
                "response_time": None,
                "action": env_action,
            },
        )

        return response
