from typing import Optional

from fastapi import APIRouter

from scale import Scale
from utils import String, map_scale_to_strings

router = APIRouter(prefix="/api")


@router.get("/string/{open_note}")
async def return_string(open_note: Optional[str] = 'E0'):
    return String(open_note)

@router.get("/scale/{scale}/")
async def return_scale(scale: str, key: str, tuning: str):
    scale = Scale(scale, key)
    strings = [String(a) for a in tuning.split(',')]
    map_scale_to_strings(scale, strings)
    return strings