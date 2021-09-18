from datetime import datetime
from typing import Optional

from fastapi.openapi.models import Schema
from pydantic import BaseModel


class CommonConfig:
    anystr_strip_whitespace = True
    allow_mutation = False

# class DateTimeModelMixin(BaseModel):
#     created_at: Optional[datetime] = Schema(...)
#     updated_at: Optional[datetime] = Schema(...)

