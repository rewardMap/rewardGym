from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class KeysProtocol(Protocol):
    name: str
    rt: float
    tDown: float
    duration: float


@runtime_checkable
class KeyboardProtocol(Protocol):
    def getKeys(
        self, keyList=None, waitRelease=True, clear=True
    ) -> list[KeysProtocol]: ...


@runtime_checkable
class InputProtocol(Protocol):
    """
    Protocol for Keyboard handling
    """

    def get_keys(self) -> list[tuple[str, float]]: ...

    def simulate_keys(self, key, rt) -> list[tuple[str, float]]: ...

    def interpret_keys(
        self,
        key_presses: list[tuple[str, float]],
        logger,
        key_list: None | list[str] = None,
        **kwargs,
    ) -> tuple[str, float] | None: ...

    def key_strokes(
        self, logger, key_list: None | list[str] = None
    ) -> tuple[str, float] | None: ...


@runtime_checkable
class ClockProtocol(Protocol):
    def getTime(self) -> float: ...

    def reset(self) -> None: ...


@runtime_checkable
class LoggerProtocol(Protocol):
    clock: ClockProtocol
    na: str

    def get_time(self) -> float: ...

    def log_event(self, info_dict: dict, onset: float | None = None) -> None: ...

    def close(self) -> None: ...


@runtime_checkable
class DisplayProtocol(Protocol):
    def schedule_on_flip(self, callback, *args, **kwargs) -> Any: ...

    def flip(self) -> Any: ...

    def wait(self, **kwargs) -> Any: ...


@runtime_checkable
class FactoryProtocol:
    def image(self, **kwargs) -> Any: ...

    def rectangle(self, **kwargs) -> Any: ...

    def text(self, **kwargs) -> Any: ...


@runtime_checkable
class WindowProtocol:
    def flip(self, **kwargs) -> Any: ...

    def callOnFlip(self, **kwargs) -> Any: ...

    def close(self): ...
