from difflib import get_close_matches


class UnknownTaskError(ValueError):
    pass


class UnknownBackendError(ValueError):
    pass


class UnknownStimulusError(ValueError):
    pass


class ClockMismatchError(ValueError):
    pass


error_registry = {
    "backend": UnknownBackendError,
    "task": UnknownTaskError,
}


def available_backends():
    from .render.backends import BACKENDS

    return list(BACKENDS.keys())


def available_tasks():
    from . import _task_registry

    return list(_task_registry.keys())


def get_available(kind: str):
    if kind == "backend":
        return available_backends()

    if kind == "task":
        return available_tasks()

    raise ValueError(f"{kind} is not implemented as availability")


def suggest_matches(input_arg, available, n=3):
    return get_close_matches(input_arg, available, n=n)


def check_availability(input_arg, kind, fail=True):
    available = get_available(kind)

    if input_arg in available:
        return True

    if fail:
        suggestions = suggest_matches(input_arg, available)

        hint = ""

        if suggestions:
            suggestion_text = ", ".join(repr(i) for i in suggestions)
            hint = f"\nDid you mean: {suggestion_text}?"

        raise error_registry[kind](
            f"{input_arg} is not a registered {kind}.{hint}\nRegistered as {kind} are: {available}"
        )

    return False
