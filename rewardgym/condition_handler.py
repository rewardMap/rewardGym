from collections import defaultdict


class BaseCondition:
    def __init__(
        self,
        conditions=[],
        condition_map={
            "initial_state": defaultdict(int),
            "condition_value": defaultdict(int),
        },
    ):

        if len(conditions) == 0:
            self.step = None
        else:
            self.step = None

        self.conditions = conditions
        self.condition_map = condition_map

    def __call__(self):

        if len(self.conditions) == 0:
            initial_state = 0
            condition = 0
        else:
            initial_state = self.condition_map["initial_state"][
                self.conditions[self.step]
            ]
            condition = self.condition_map["condition_value"][
                self.conditions[self.step]
            ]

            self.step += 1

            if self.step == len(self.order):
                self.step = 0

        return initial_state, condition
