import asyncio
import sys

from motor.motor_asyncio import AsyncIOMotorClient

sys.path.insert(0,'/home/alex/Code/alex/guitar-spell/flexi-guitar/')
from config import settings
from models import TuningModel

mongodb_client = AsyncIOMotorClient(settings.DB_URL)
mongodb = mongodb_client[settings.DB_NAME]
tunings = mongodb.tunings


async def create_tuning():
    tuning_to_create = TuningModel(name="E Standard", notes=["E2", "A2", "D3", "G3", "B3", "E4"])

    if not await tunings.find_one({"name": tuning_to_create.name}):
        await tunings.insert_one(tuning_to_create.dict())



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_tuning())
