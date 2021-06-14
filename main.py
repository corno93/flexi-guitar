import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from utils import String

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/string/{open_note}")
def return_string(open_note: str = 'E0'):
    return String(open_note)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)