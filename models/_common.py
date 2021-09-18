from datetime import datetime
from typing import Optional

from fastapi.openapi.models import Schema
from pydantic import BaseModel


class CommonConfig:
    anystr_strip_whitespace = True
    allow_mutation = False


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.datetime.now()