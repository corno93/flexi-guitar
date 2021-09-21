import asyncio
import sys

from motor.motor_asyncio import AsyncIOMotorClient

from scale import Step

sys.path.insert(0,'/home/alex/Code/alex/guitar-spell/flexi-guitar/')
from config import settings
from models import ScaleModel

mongodb_client = AsyncIOMotorClient(settings.DB_URL)
mongodb = mongodb_client[settings.DB_NAME]
scales = mongodb.scales

SCALES = [
            ("Minor Pentatonic", [Step.WHOLE_AND_HALF, Step.WHOLE, Step.WHOLE, Step.WHOLE_AND_HALF, Step.WHOLE]),
            ("Gypsy scale", [Step.WHOLE, Step.HALF, Step.WHOLE_AND_HALF, Step.HALF, Step.HALF, Step.WHOLE, Step.WHOLE]),
            ("Insen scale", [Step.HALF, Step.TWO_WHOLE, Step.WHOLE, Step.WHOLE_AND_HALF, Step.WHOLE]),
            ("Dorian mode", [Step.WHOLE, Step.HALF, Step.WHOLE, Step.WHOLE, Step.WHOLE, Step.HALF, Step.WHOLE])
          ]

async def create_scale():

    for name, intervals in SCALES:

        scale_to_create = ScaleModel(name=name, intervals=intervals)

        if not await scales.find_one({"name": scale_to_create.name}):
            await scales.insert_one(scale_to_create.dict())



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_scale())
