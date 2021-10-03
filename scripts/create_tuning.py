import asyncio
import sys

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from models import Tuning

sys.path.insert(0,'/home/alex/Code/alex/guitar-spell/flexi-guitar/')
from config import settings

client = AsyncIOMotorClient(settings.DB_URL)
engine = AIOEngine(motor_client=client, database=settings.DB_NAME)



standard = [('Standard E', ["E2", "A2", "D3", "G3", "B3", "E4"], "Standard")]
opens = [('Open A', ['E2', 'A2', 'E3', 'A3', 'C#4 ', 'E4'], 'Open'), ('Open B', ['B2', 'F#2', 'B3', 'F#3', 'B4', 'D#4'], 'Open'), ('Open C', ['C2', 'G2', 'C3', 'G3', 'C3', 'E4'], 'Open'), ('Open D', ['D2', 'A2', 'D3', 'F#3', 'A3', 'D4'], 'Open'), ('Open E', ['E2', 'B2', 'E3', 'G#3', 'B3', 'E4'], 'Open'), ('Open F', ['C2', 'F2', 'C3', 'F3', 'A3', 'F4'], 'Open'), ('Open G', ['D2', 'G2', 'D3', 'G3', 'B3', 'D4'], 'Open')]
dropped = [('Half Step Down', ['D#2', ' G#2', ' C#3', ' F#3', ' A#3', ' D#4'], 'Dropped'), ('Full Step Down', ['D2', ' G2', ' C3', ' F3', ' A3', ' D4'], 'Dropped'), ('1 and 1/2 Steps Down', ['C#2', ' F#2', ' B3', ' E3', ' G#3', ' C#4'], 'Dropped'), ('Drop A', ['A1', ' E2', ' A3', ' D3', ' F#3', ' B4'], 'Dropped'), ('Drop B', ['B1', ' F#2', ' B3', ' E3', ' G#3', ' C#4'], 'Dropped'), ('Drop C', ['C1', ' G2', ' C3', ' F3', ' A3', ' D4'], 'Dropped'), ('Drop D', ['D2', ' A2', ' D3', ' G3', ' B3', 'E4'], 'Dropped'), ('Drop E', ['E1', ' B2', ' E2', ' A2', ' C#3', ' F3#'], 'Dropped'), ('Half Step Down', ['D#2', ' G#2', ' C#3', ' F#3', ' A#3', ' D#4'], 'Dropped'), ('Full Step Down', ['D2', ' G2', ' C3', ' F3', ' A3', ' D4'], 'Dropped'), ('1 and 1/2 Steps Down', ['C#2', ' F#2', ' B3', ' E3', ' G#3', ' C#4'], 'Dropped'), ('Drop A', ['A1', ' E2', ' A3', ' D3', ' F#3', ' B4'], 'Dropped'), ('Drop B', ['B1', ' F#2', ' B3', ' E3', ' G#3', ' C#4'], 'Dropped'), ('Drop C', ['C1', ' G2', ' C3', ' F3', ' A3', ' D4'], 'Dropped'), ('Drop D', ['D2', ' A2', ' D3', ' G3', ' B3', 'E4'], 'Dropped'), ('Drop E', ['E1', ' B2', ' E2', ' A2', ' C#3', ' F3#'], 'Dropped')]

TUNINGS = standard + opens + dropped

# dict(name="C Standard", notes=["C4", "G3", "D#3", "A#2", "F2", "C2"])

async def create_tuning():

    tunings_to_create = []

    for name, notes, category in TUNINGS:
        tuning_to_create = Tuning(name=name, notes=notes, category=category)

        if not await engine.find_one(Tuning, Tuning.name == name):
            tunings_to_create.append(tuning_to_create)

    await engine.save_all(tunings_to_create)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_tuning())
