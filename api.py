from typing import Optional, List

from fastapi import APIRouter, Request

from scale import Scale
from utils import String, map_scale_to_strings
from models import TuningModel

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

@router.get("/tunings/", response_description="List all tunings", response_model=List[TuningModel])
async def return_tuning(request: Request):
    tunings = []
    cursor = request.app.mongodb['tunings'].find()
    async for document in cursor:
        tunings.append(document)
    return tunings