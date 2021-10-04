from typing import List

from odmantic import Model

from models._common import CommonConfig, DateTimeModelMixin


class TuningBase(Model):
    name: str
    notes: List[str]
    category: str

class Tuning(Model, DateTimeModelMixin):
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