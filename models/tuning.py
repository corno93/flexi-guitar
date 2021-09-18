from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

from _common import CommonConfig, DateTimeModelMixin


@dataclass(config=CommonConfig)
class TuningModel(BaseModel, DateTimeModelMixin):
    name: str = Field()
    notes: str = Field() # ; delimitered
    # TODO: add regex validation

    class Config:
        title = "Tuning"
        schema_extra = {
            "example": {
                "name": "Drop D",
                "notes": "D2;A2;D2;G3;B3;E4"
            }
        }