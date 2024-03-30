from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/login", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

if __name__ == "__main__":
    print("================================\n"
          "         INICIO UVICORN\n"
          "================================")
    uvicorn.run(app, host="localhost", port=8000)