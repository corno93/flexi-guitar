from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

from models._common import CommonConfig, DateTimeModelMixin
from typing import List


class TuningBase(BaseModel):
    name: str = Field()
    notes: List[str] = Field()
    # TODO: add regex validation

    class Config(CommonConfig):
        title = "Tuning"
        schema_extra = {
            "example": {
                "name": "Drop D",
                "notes": ["D2","A2","D2","G3","B3","E4"]
            }
        }


class TuningModel(TuningBase, DateTimeModelMixin):
    pass
