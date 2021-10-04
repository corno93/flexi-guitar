from typing import Optional, List

from odmantic import Field, Model, EmbeddedModel, ObjectId

from typing_extensions import TypedDict

from models._common import DateTimeModelMixin, CommonConfig


class FretMeta(TypedDict):
    is_root_note: bool
    is_in_scale: bool

class Fret(EmbeddedModel):
    note: str
    meta: Optional[FretMeta] = Field(default_factory=lambda: dict(is_root_note=False, is_in_scale=False))

class String(EmbeddedModel):
    open_note: str
    frets: List[Fret]

class Fretboard(Model, DateTimeModelMixin):
    tuning: str
    strings: List[String]
    scale_id: Optional[ObjectId] = None
    key: Optional[str]

    class Config(CommonConfig):
        title = "Fretboard"