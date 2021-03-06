
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from templates import templates
from api import router
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from odmantic import AIOEngine

app = FastAPI()
app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def fretboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.on_event("startup")
async def startup_db_client():
    client = AsyncIOMotorClient(settings.DB_URL)
    app.engine = AIOEngine(motor_client=client, database=settings.DB_NAME)

    mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = mongodb_client[settings.DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.engine.client.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT)
