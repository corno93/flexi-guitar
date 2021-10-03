from typing import Optional, List

from odmantic import Field, Model, Reference, EmbeddedModel, ObjectId

from typing_extensions import TypedDict

from scale import Step


class Scale(Model):
    name: str
    intervals: List[Step]
    description: Optional[str] = Field(init=False, repr=False)


class Tuning(Model):
    name: str
    notes: List[str]
    category: str

class FretMeta(TypedDict):
    is_root_note: bool
    is_in_scale: bool

class Fret(EmbeddedModel):
    note: str
    meta: Optional[FretMeta] = Field(default_factory=lambda: dict(is_root_note=False, is_in_scale=False))

class String(EmbeddedModel):
    open_note: str
    frets: List[Fret]

class Fretboard(Model):
    tuning: str
    strings: List[String]
    scale_id: Optional[ObjectId] = None
    key: Optional[str]



class Note(Model):
    name: str