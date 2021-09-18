from datetime import datetime
from typing import Optional

from fastapi.openapi.models import Schema
from pydantic import BaseModel, validator, Field


class CommonConfig:
    anystr_strip_whitespace = True
    allow_mutation = False


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = Field(default_factory=datetime.now, hidden=True)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, hidden=True)
