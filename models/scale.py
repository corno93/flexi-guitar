from typing import List, Optional

from odmantic import Model, Field

from models._common import CommonConfig, DateTimeModelMixin
from scale import Step

class Scale(Model, DateTimeModelMixin):
    name: str
    intervals: List[Step]
    description: Optional[str] = Field(init=False, repr=False)

    class Config(CommonConfig):
        title = "Scale"
        schema_extra = {
            "example": {
                "name": "Minor Pentatonic",
                "intervals": [Step.WHOLE_AND_HALF, Step.WHOLE, Step.WHOLE, Step.WHOLE_AND_HALF, Step.WHOLE]
            }
        }