from pydantic import BaseModel, Field

from models._common import CommonConfig, DateTimeModelMixin


class NoteBase(BaseModel):
    name: str = Field()

    class Config(CommonConfig):
        title = "Note"
        schema_extra = {
            "example": {
                "name": "C0",
            }
        }


class NoteModel(NoteBase, DateTimeModelMixin):
    pass
