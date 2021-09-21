from typing import Optional, List

from fastapi import APIRouter, Request

from models import TuningModel, NoteModel, ScaleModel
from scale import Scale
from utils import String, map_scale_to_strings, find_required_notes_for_scale

router = APIRouter(prefix="/api")


@router.get("/string/{open_note}")
async def return_string(open_note: Optional[str] = 'E0'):
    return String(open_note)

# NEW
# @router.get("/string/{open_note}")
# async def get_or_create_string(request: Request, open_note: Optional[str] = 'E2'):
#     string = request.app.mongodb["strings"].find_one({'open_note': open_note})
#     if not string:
#
#     return String(open_note)


@router.get("/scales/", response_description="List all scales", response_model=List[ScaleModel], response_model_exclude_unset=True)
async def return_scale(request: Request):
    scales = []
    cursor = request.app.mongodb['scales'].find(projection=["name", "intervals"])
    async for document in cursor:
        scales.append(document)
    return scales


@router.get("/fretboard/{tuning}")
async def return_fretboard(request: Request, tuning: str, scale: Optional[str], key: Optional[str], total_fret_number: Optional[int]):
    # get scale from db
    scale = request.app.mongodb['scales'].find_one({'name': scale})

    # find notes
    notes = find_required_notes_for_scale(key, scale)

    # find strings


    # map strings onto scale notes

    # return strings
    return




# @router.get("/old_scale/{scale}/")
# async def return_scale_with_strings(scale: str, key: str, tuning: str):
#     scale = Scale(scale, key)
#     strings = [String(a) for a in tuning.split(',')]
#     map_scale_to_strings(scale, strings)
#     return strings



@router.get("/tunings/", response_description="List all tunings", response_model=List[TuningModel], response_model_exclude_unset=True)
async def return_tunings(request: Request):
    tunings = []
    cursor = request.app.mongodb['tunings'].find(projection=["name", "notes"])
    async for document in cursor:
        tunings.append(document)
    return tunings


@router.get("/notes/", response_description="List all notes", response_model=List[NoteModel], response_model_exclude_unset=True)
async def return_notes(request: Request, keys_only: Optional[bool]=False):
    notes = []
    cursor = request.app.mongodb['notes'].find(projection=["name"])
    async for document in cursor:
        notes.append(document)

    if keys_only:
        notes = [{"name": note["name"][:-1]} for note in notes[:12]]

    return notes