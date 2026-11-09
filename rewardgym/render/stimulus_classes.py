from dataclasses import dataclass
from enum import Enum

from numpy.typing import ArrayLike

from ..protocols import WindowProtocol

Stimuli = Enum("stimuli", names="IMAGE RECTANGLE TEXT")


@dataclass(kw_only=True)
class StimulusDefinition:
    window: WindowProtocol
    name: str | None
    autoDraw: bool = False
    opacity: float = 1.0
    pos: tuple | None = (0, 0)
    units: str | None = None
    setup_protocol = None

    def get_kwargs(self) -> dict | None:
        pass


@dataclass(kw_only=True)
class Image(StimulusDefinition):
    image: str | None | ArrayLike
    size: tuple | None = None
    setup_protocol = Stimuli.IMAGE


@dataclass(kw_only=True)
class Text(StimulusDefinition):
    text: str
    height: float | int | None
    color: str | list | ArrayLike = "white"
    font: str | None = None
    alignText = None
    anchorHoriz = None
    setup_protocol = Stimuli.TEXT


@dataclass(kw_only=True)
class Rectangle(StimulusDefinition):
    width = None
    height = None
    lineColor = None
    fillColor = None
    lineWidth = None
    setup_protocol = Stimuli.RECTANGLE
