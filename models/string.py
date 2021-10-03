from typing import List

from pydantic import BaseModel

from models._common import CommonConfig, DateTimeModelMixin

class FretModel(BaseModel):
    note: str

    class Config(CommonConfig):
        title = "String"
        schema_extra = {
            "example": {
                "note": "E0"
            }
        }

class StringBase(BaseModel):
    open_note: str
    frets: List[FretModel]

    class Config(CommonConfig):
        title = "String"
        schema_extra = {
            "example": {
                "open_note": "E0",
                "notes": ["E0",
                            "F0",
                            "F#0",
                            "G0",
                            "G#0",
                            "A0",
                            "A#0",
                            "B0",
                            "C1",
                            "C#1",
                            "D1",
                            "D#1",
                            "E1"
                          ]
            }
        }

class StringModel(StringBase, DateTimeModelMixin):
    pass

