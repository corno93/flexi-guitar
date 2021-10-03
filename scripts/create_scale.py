import asyncio
import sys

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from scale import Step

sys.path.insert(0,'/home/alex/Code/alex/guitar-spell/flexi-guitar/')
from config import settings
from models import Scale

client = AsyncIOMotorClient(settings.DB_URL)
engine = AIOEngine(motor_client=client, database=settings.DB_NAME)


# scales from wikipedia -> https://en.wikipedia.org/wiki/List_of_musical_scales_and_modes
SCALES = [('Acoustic scale', 'W-W-W-H-W-H-W'),
('Aeolian mode or natural minor scale', 'W-H-W-W-H-W-W'),
('Algerian scale', 'W-H-3H-H-H-3H-H-W-H-W'),
('Altered scale or Super Locrian scale', 'H-W-H-W-W-W-W'),
('Augmented scale', '3H-H-3H-H-3H-H'),
('Bebop dominant scale', 'W-W-H-W-W-H-H-H'),
('Blues scale', '3H-W-H-H-3H-W'),
('Chromatic scale', 'H-H-H-H-H-H-H-H-H-H-H-H'),
('Dorian mode', 'W-H-W-W-W-H-W'),
('Double harmonic scale', 'H-3H-H-W-H-3H-H'),
('Enigmatic scale', 'H-3H-W-W-W-H-H'),
('Flamenco mode', 'H-3H-H-W-H-3H-H'),
('Gypsy scale', 'W-H-3H-H-H-W-W'),
('Half diminished scale', 'W-H-W-H-W-W-W'),
('Harmonic major scale', 'W-W-H-W-H-3H-H'),
('Harmonic minor scale', 'W-H-W-W-H-3H-H'),
('Hirajoshi scale', '2W-W-H-2W-H'),
('Hungarian "Gypsy" scale/Hungarian minor scale', 'W-H-3H-H-H-3H-H'),
('Hungarian major scale', '3H-H-W-H-W-H-W'),
('In scale', 'H-2W-W-H-2W'),
('Insen scale', 'H-2W-W-3H-W'),
('Ionian mode or major scale', 'W-W-H-W-W-W-H'),
('Istrian scale', 'H-W-H-W-'),
('Iwato scale', 'H-2W-H-2W-W'),
('Locrian mode', 'H-W-W-H-W-W-W'),
('Lydian augmented scale', 'W-W-W-W-H-W-H'),
('Lydian mode', 'W-W-W-H-W-W-H'),
('Major Locrian scale', 'W-W-H-H-W-W-W'),
('Major pentatonic scale', 'W-W-3H-W-3H'),
('Melodic minor scale', 'W-H-W-W-W-W-H'),
('Minor pentatonic scale', '3H-W-W-3H-W'),
('Mixolydian mode or Adonai malakh mode', 'W-W-H-W-W-H-W'),
('Neapolitan major scale', 'H-W-W-W-W-W-H'),
('Neapolitan minor scale', 'H-W-W-W-H-3H-H'),
('Persian scale', 'H-3H-H-H-W-3H-H'),
('Phrygian dominant scale', 'H-3H-H-W-H-W-W'),
('Phrygian mode', 'H-W-W-W-H-W-W'),
('Prometheus scale', 'W-W-W-3H-H-W'),
('Scale of harmonics', '3H-H-H-W-W-3H'),
('Tritone scale', 'H-3H-W-H-3H-W'),
('Two-semitone tritone scale', 'H-H-2W-H-H-2W'),
('Ukrainian Dorian scale', 'W-H-3H-H-W-H-W'),
('Whole tone scale', 'W-W-W-W-W-W'),
('Yo scale', '3H-W-W-3H-W')]

async def create_scale():

    scales_to_create = []

    for name, intervals in SCALES:

        # parse intervals
        parsed_intervals = []
        for interval in intervals.split('-'):
            if interval == 'H':
                parsed_intervals.append(Step.HALF)
            elif interval == 'W':
                parsed_intervals.append(Step.WHOLE)
            elif interval == '3H':
                parsed_intervals.append(Step.WHOLE_AND_HALF)
            elif interval == '2W':
                parsed_intervals.append(Step.TWO_WHOLE)

        if not await engine.find_one(Scale, Scale.name == name):
            scales_to_create.append(Scale(name=name, intervals=parsed_intervals))

    await engine.save_all(scales_to_create)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_scale())
