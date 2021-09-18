from typing import Optional, List

from fastapi import APIRouter, Request
from pymongo import ReturnDocument
from scale import Scale
from utils import String, map_scale_to_strings
from models import TuningModel, NoteModel

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


@router.get("/tunings/", response_description="List all tunings", response_model=List[TuningModel], response_model_exclude_unset=True)
async def return_tunings(request: Request):
    tunings = []
    cursor = request.app.mongodb['tunings'].find(projection=["name", "notes"])
    async for document in cursor:
        tunings.append(document)
    return tunings


@router.get("/notes/", response_description="List all notes", response_model=List[NoteModel], response_model_exclude_unset=True)
async def return_notes(request: Request):
    notes = []
    cursor = request.app.mongodb['notes'].find(projection=["name"])
    async for document in cursor:
        notes.append(document)
    return notes