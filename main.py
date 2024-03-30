from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return "Hola"

if __name__ == "__main__":
    print("================================\n"
          "         INICIO UVICORN\n"
          "================================")
    uvicorn.run(app, host="localhost", port=8000)