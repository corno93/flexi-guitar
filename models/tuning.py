from typing import List

from pydantic import BaseModel

from models._common import CommonConfig, DateTimeModelMixin


class TuningBase(BaseModel):
    name: str
    notes: List[str]
    category: str

    class Config(CommonConfig):
        title = "Tuning"
        schema_extra = {
            "example": {
                "name": "Drop D",
                "notes": ["D2","A2","D2","G3","B3","E4"],
                "category": "Dropped"
            }
        }


class TuningModel(TuningBase, DateTimeModelMixin):
    pass
