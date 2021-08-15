from typing import Optional

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from templates import templates
from api import router
app = FastAPI()
app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def fretboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)