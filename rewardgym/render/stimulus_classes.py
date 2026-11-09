from dataclasses import dataclass, fields
from enum import StrEnum, auto

from typing import ClassVar

from numpy.typing import ArrayLike

from ..protocols import WindowProtocol


class Stimuli(StrEnum):
    IMAGE = auto()
    RECTANGLE = auto()
    TEXT = auto()


@dataclass(kw_only=True)
class StimulusDefinition:
    window: WindowProtocol
    name: str | None
    autoDraw: bool | None = None
    opacity: float | None = None
    pos: tuple | None = None
    units: str | None = None
    setup_protocol: ClassVar[Stimuli] = None

    def get_kwargs(self):
        return {
            field.name: getattr(self, field.name)
            for field in fields(self)
            if getattr(self, field.name) is not None
        }


@dataclass(kw_only=True)
class ImageDefinition(StimulusDefinition):
    image: str | None | ArrayLike
    size: tuple | None = None
    setup_protocol: ClassVar[Stimuli] = Stimuli.IMAGE


@dataclass(kw_only=True)
class TextDefinition(StimulusDefinition):
    text: str
    height: float | int | None
    color: str | list | ArrayLike | None = None
    font: str | None = None
    alignText: str | None = None
    anchorHoriz: str | None = None
    setup_protocol: ClassVar[Stimuli] = Stimuli.TEXT


@dataclass(kw_only=True)
class RectangleDefinition(StimulusDefinition):
    width: float | None = None
    height: float | None = None
    lineColor: str | list | tuple | ArrayLike | None = None
    fillColor: str | list | tuple | ArrayLike | None = None
    lineWidth: float | None = None
    setup_protocol: ClassVar[Stimuli] = Stimuli.RECTANGLE
