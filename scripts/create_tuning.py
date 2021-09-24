import asyncio
import sys

from motor.motor_asyncio import AsyncIOMotorClient

sys.path.insert(0,'/home/alex/Code/alex/guitar-spell/flexi-guitar/')
from config import settings
from models import TuningModel

mongodb_client = AsyncIOMotorClient(settings.DB_URL)
mongodb = mongodb_client[settings.DB_NAME]
tunings = mongodb.tunings

opens = [('Open A', ['E2', 'A2', 'C♯3', 'E3', 'A3', 'E4'], 'Open'), ('Open B', ['B2', 'F2♯', 'B3', 'F♯3', 'B4', 'D♯4'], 'Open'), ('Open C', ['C2', 'G2', 'C3', 'G3', 'C3', 'E4'], 'Open'), ('Open D', ['D2', 'A2', 'D3', 'F♯3', 'A3', 'D4'], 'Open'), ('Open E', ['E2', 'B2', 'E3', 'G♯3', 'B3', 'E4'], 'Open'), ('Open F', ['C2', 'F2', 'C3', 'F3', 'A3', 'F4'], 'Open'), ('Open G', ['D2', 'G2', 'D3', 'G3', 'B3', 'D4'], 'Open')]

TUNINGS = opens

# dict(name="C Standard", notes=["C4", "G3", "D#3", "A#2", "F2", "C2"])

async def create_tuning():

    for name, notes, category in TUNINGS:
        tuning_to_create = TuningModel(name=name, notes=notes, category=category)

        if not await tunings.find_one({"name": tuning_to_create.name}):
            await tunings.insert_one(tuning_to_create.dict())



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_tuning())
