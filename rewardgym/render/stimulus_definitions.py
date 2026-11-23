from dataclasses import dataclass, fields
from typing import ClassVar

from numpy.typing import ArrayLike


@dataclass(kw_only=True)
class StimulusDefinition:
    name: str
    autoDraw: bool | None = None
    opacity: float | None = None
    pos: tuple | None = None
    units: str | None = None
    stimulus_type: ClassVar[str] = None

    def get_kwargs(self):
        return {
            field.name: getattr(self, field.name)
            for field in fields(self)
            if (getattr(self, field.name) is not None and field.name != "autoDraw")
        }


@dataclass(kw_only=True)
class ImageDefinition(StimulusDefinition):
    image: str | None | ArrayLike
    size: tuple | None = None
    stimulus_type: ClassVar[str] = "image"


@dataclass(kw_only=True)
class TextDefinition(StimulusDefinition):
    text: str
    height: float | int | None
    color: str | list | ArrayLike | None = None
    font: str | None = None
    alignText: str | None = None
    anchorHoriz: str | None = None
    ori: float | None = None
    stimulus_type: ClassVar[str] = "text"


@dataclass(kw_only=True)
class RectangleDefinition(StimulusDefinition):
    width: float | None = None
    height: float | None = None
    lineColor: str | list | tuple | ArrayLike | None = None
    fillColor: str | list | tuple | ArrayLike | None = None
    lineWidth: float | None = None
    stimulus_type: ClassVar[str] = "rectangle"
