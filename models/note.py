from odmantic import Model

from models._common import CommonConfig


class Note(Model):
    name: str

    class Config(CommonConfig):
        title = "Note"
        schema_extra = {
            "example": {
                "name": "C0",
            }
        }