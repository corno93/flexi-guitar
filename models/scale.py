from typing import List, Optional

from pydantic import BaseModel, Field

from models._common import CommonConfig, DateTimeModelMixin
from scale import Step


class ScaleBase(BaseModel):
    name: str
    intervals: List[Step]
    description: Optional[str] = Field(init=False, repr=False)
    tags: Optional[List[str]] = Field(default_factory=list, repr=False)

    class Config(CommonConfig):
        title = "Scale"
        use_enum_values = True
        schema_extra = {
            "example": {
                "name": "Minor Pentatonic",
                "intervals": [Step.WHOLE_AND_HALF, Step.WHOLE, Step.WHOLE, Step.WHOLE_AND_HALF, Step.WHOLE]
            }
        }


class ScaleModel(ScaleBase, DateTimeModelMixin):
    pass
