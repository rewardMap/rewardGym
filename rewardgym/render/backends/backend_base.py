from ..contexts import EnvironmentContext


class RewardGymBackend:
    mode: str

    def setup(self, context: EnvironmentContext):
        raise NotImplementedError
