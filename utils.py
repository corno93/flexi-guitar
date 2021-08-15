from dataclasses import dataclass, field
from typing import List
import json
from itertools import islice

FRET_NUMBERS = 15

"""
relationship between string length, string mass per unit length (kg/m) and pitch (freq)

freq depends on string length and string tension

"""

# TODO: refactor later - use dataclass and string file

def get_linear_density(mass_of_string, length_of_string):
    return mass_of_string / length_of_string

def get_string_length():
    """
    Different guitars have different lengths
    https://en.wikipedia.org/wiki/Scale_length_(string_instruments)
    Gibson: 630mm
    Fender: 650mm
    :return:
    """
    return 630

def get_mass_of_string(density, string_length, string_guage):
    """
    TODO: do we assume a constant density?
    :return:
    """
    return density * string_length * string_guage


def return_string_using_formula(open_note_freq, fret_numbers, string_guage):
    """
    Return all the notes and their frequencies for a string.
    TODO: improve name
    TODO: add diameter?

    :param open_note_freq:
    :param fret_numbers:
    :return:
    """

    # first simple formula: http://techlib.com/reference/musical_note_frequencies.htm
    freqs = [open_note_freq]
    for fret in range(1, fret_numbers):
        next_feq = open_note_freq * pow(fret/12)
        freqs.append(next_feq)

    # second more complex formula


@dataclass
class String:
    open_note: str = field(repr=False)
    notes: list = field(init=False, default_factory=list)

    def __post_init__(self):
        with open('notes.json') as f:
            note_data = json.load(f)
        starting_index = list(note_data.keys()).index(self.open_note)
        note_names = list(islice(note_data, starting_index, starting_index + FRET_NUMBERS))
        for note_name in note_names:
            self.notes.append({"name":note_name, "frequency":note_data[note_name]})





