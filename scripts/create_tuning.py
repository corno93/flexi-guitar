import asyncio
import os
import sys

from motor.motor_asyncio import AsyncIOMotorClient

sys.path.insert(0,'/home/alex/Code/alex/guitar-spell/flexi-guitar/')
from config import settings
from models import TuningModel

mongodb_client = AsyncIOMotorClient(settings.DB_URL)
mongodb = mongodb_client[settings.DB_NAME]


async def create_tuning():
    e_standard = TuningModel(name="Drop D", notes=["D2", "A2", "D3", "G3", "B3", "E4"])
    await mongodb["tunings"].insert_one(e_standard.dict())



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_tuning())
