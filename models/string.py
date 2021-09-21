from typing import List

from pydantic import BaseModel

from models._common import CommonConfig, DateTimeModelMixin


class StringBase(BaseModel):
    open_note: str
    all_notes: List[str]

    class Config(CommonConfig):
        title = "String"
        schema_extra = {
            "example": {
                "open_note": "E2",
                "all_notes": [...]
            }
        }


class StringModel(StringBase, DateTimeModelMixin):
    pass
