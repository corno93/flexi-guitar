from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

from models._common import CommonConfig
from typing import List


class NoteBase(BaseModel):
    name: str = Field()

    class Config(CommonConfig):
        title = "Note"
        schema_extra = {
            "example": {
                "name": "A#2",
            }
        }


class NoteModel(NoteBase, DateTimeModelMixin):
    pass
