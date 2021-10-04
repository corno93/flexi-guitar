from typing import Optional, List

from fastapi import APIRouter, Request

from models import Fretboard, Scale, Note, String, Fret, Tuning
from utils import find_required_notes_for_scale

router = APIRouter(prefix="/api")

DEFAULT_TOTAL_FRET_NUMBERS = 12


@router.get("/string/{open_note}", response_description="A string" ,response_model=String)
async def return_string(request: Request, open_note: str, total_fret_number: Optional[int] = DEFAULT_TOTAL_FRET_NUMBERS):
    # could optimise this
    notes = []
    async for note in request.app.engine.find(Note):
        notes.append(note.name)

    starting_note_idx = notes.index(open_note)
    frets = [Fret(note=note) for note in notes[starting_note_idx: starting_note_idx + total_fret_number + 1]]
    string = String(open_note=open_note, frets=frets)

    return string


@router.get("/scales/", response_description="List all scales", response_model=List[Scale], response_model_exclude_unset=True)
async def return_scale(request: Request):
    scales = []
    async for scale in request.app.engine.find(Scale):
        scales.append(scale)
    return scales


async def return_strings(request, open_notes):
    strings = []
    for open_note in open_notes:
        string = await return_string(request, open_note)
        strings.append(string)
    return strings


@router.get("/fretboard/{tuning}", response_description="A fretboard (strings go from high to low)", response_model=Fretboard)
async def return_fretboard(request: Request, tuning: str, scale: Optional[str] = None, key: Optional[str] = None, total_fret_number: Optional[int]=DEFAULT_TOTAL_FRET_NUMBERS):

    # get fretboard from db and return if it exists
    query_params = [Fretboard.tuning == tuning, Fretboard.key == key]
    if scale:
        scale = await request.app.engine.find_one(Scale, Scale.name == scale)
        query_params.append(Fretboard.scale_id == scale.id)
    if fretboard := await request.app.engine.find_one(Fretboard, *query_params):
        return fretboard

    if scale:
        scale_notes = find_required_notes_for_scale(key, scale.intervals)
        strings = await return_strings(request, tuning.split(","))
        for string in strings:
            for fret in string.frets:
                if fret.note[:-1] in scale_notes:
                    fret.meta['is_in_scale'] = True
                if fret.note[:-1] == key:
                    fret.meta['is_root_note'] = True

    fretboard = Fretboard(tuning=tuning, strings=strings, scale_id=scale.id, key=key)
    await request.app.engine.save(fretboard)

    return fretboard


@router.get("/tunings/", response_description="List all tunings", response_model=List[Tuning], response_model_exclude_unset=True)
async def return_tunings(request: Request):
    tunings = []
    async for tuning in request.app.engine.find(Tuning):
        tunings.append(tuning)
    return tunings


@router.get("/notes/", response_description="List all notes", response_model=List[Note], response_model_exclude_unset=True)
async def return_notes(request: Request, keys_only: Optional[bool]=False):
    notes = []
    async for note in request.app.engine.find(Note):
        notes.append(note)

    if keys_only:
        keys = []
        for note in notes[:12]:
            note.name = note.name[:-1]
            keys.append(note)
        notes = keys

    return notes