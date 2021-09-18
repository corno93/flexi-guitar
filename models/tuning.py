from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

from models._common import CommonConfig
from typing import List


# @dataclass(config=CommonConfig)
class TuningModel(BaseModel):
    name: str = Field()
    notes: List[str] = Field()
    # TODO: add regex validation

    class Config:
        title = "Tuning"
        schema_extra = {
            "example": {
                "name": "Drop D",
                "notes": "D2;A2;D2;G3;B3;E4"
            }
        }