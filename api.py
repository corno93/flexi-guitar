from typing import Optional, List

from fastapi import APIRouter, Request

from models import TuningModel, NoteModel, ScaleModel, StringModel, FretModel
from utils import find_required_notes_for_scale

router = APIRouter(prefix="/api")

DEFAULT_TOTAL_FRET_NUMBERS = 12


@router.get("/string/{open_note}", response_description="A string" ,response_model=StringModel)
async def return_string(request: Request, open_note: str, total_fret_number: Optional[int] = DEFAULT_TOTAL_FRET_NUMBERS):
    string = await request.app.mongodb["strings"].find_one({'open_note': open_note})

    # create the string if it doesnt exist
    if not string:
        # DUPLICATE OF return_notes:
        notes = []
        cursor = request.app.mongodb['notes'].find(projection=["name"])
        async for document in cursor:
            notes.append(document["name"])

        starting_note_idx = notes.index(open_note)
        frets = [FretModel(note=note) for note in notes[starting_note_idx: starting_note_idx + total_fret_number + 1]]
        string = StringModel(open_note=open_note, frets=frets)
        await request.app.mongodb['strings'].insert_one(string.dict())

    return string


@router.get("/scales/", response_description="List all scales", response_model=List[ScaleModel], response_model_exclude_unset=True)
async def return_scale(request: Request):
    scales = []
    cursor = request.app.mongodb['scales'].find(projection=["name", "intervals"])
    async for document in cursor:
        scales.append(document)
    return scales


@router.get("/fretboard/{tuning}")
async def return_fretboard(request: Request, tuning: str, scale: Optional[str] = None, key: Optional[str] = None, total_fret_number: Optional[int]=DEFAULT_TOTAL_FRET_NUMBERS):
    # get scale from db
    scale = await request.app.mongodb['scales'].find_one({'name': scale})

    # find notes
    notes = find_required_notes_for_scale(key, scale['intervals'])

    # find strings
    strings = [await return_string(request, open_note) for open_note in tuning.split(',')]

    # map strings onto scale notes
    for string in strings:
        for fret in string['frets']:
            if fret['note'][:-1] in notes:
                fret['is_apart_of_scale'] = True
            if fret['note'][:-1] == key:
                fret['is_root_note'] = True

        # remove '_id' field
        del string['_id']

    return strings


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