from dataclasses import dataclass, field
from enum import Enum
from typing import List

from utils import find_required_notes_for_scale


class Step(int, Enum):
    HALF = 1
    WHOLE = 2
    WHOLE_AND_HALF = 3
    TWO_WHOLE = 4


scale_db = {"minor-pentatonic": {"steps": [Step.WHOLE_AND_HALF, Step.WHOLE, Step.WHOLE, Step.WHOLE_AND_HALF, Step.WHOLE]}}


class Fretboard:
    def __init__(self, strings):
        ...





def construct_scale(scale_notes, strings):

    # get first note
    first_fret = strings[0].notes[min([strings[0].notes.index(a) for a in scale_notes])]

    # re-order so we start from the second note
    first_note_idx = scale_notes.index(first_fret.note)
    scale_notes = scale_notes[first_note_idx+1:] + scale_notes[:first_note_idx+1]

    for note in scale_notes:
        for string in strings:
            string_dict = {k: v for k, v in string}




    group_id = 0
    potential_path = [(first_fret, 0)]
    for note in scale_notes:
        for idx, string in enumerate(strings):
            for fret in string.notes:
                if fret == note:
                    potential_path.append((fret, idx+(fret.number-potential_path[0][0].number)))
                    break









    for scale_note in scale_notes:
        for string in strings:
            g = 1


    #

    g = 1
    pass


@dataclass
class Scale:
    scale: str
    key: str
    notes: List[str] = field(init=False, default_factory=list)

    def __post_init__(self):
        scale_steps = scale_db.get(self.scale)['steps']
        self.notes = find_required_notes_for_scale(self.key, scale_steps)
