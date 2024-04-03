from typing import Annotated
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

from connector import Connector

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/login", response_class=HTMLResponse)
def login_endpoint(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.post("/login/request", response_class=HTMLResponse)
def login_request(username_or_email: Annotated[str, Form()], password: Annotated[str, Form()]):
    connector = Connector()
    
    try:
        connector.user_login(username_or_email, password)
        connector.end_session()
        return f"Login succeeded: {username_or_email, password}"

    except Exception as e:
        print(e)
        return "Login failed"

@app.get("/register", response_class=HTMLResponse)
def register_endpoint(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")

@app.post("/register/request", response_class=HTMLResponse)
def register_request(username: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()], confirm_password: Annotated[str, Form()]):
    connector = Connector()

    if password != confirm_password:
        return "Passwords are not equal"
    
    try:
        connector.user_register(username, email, password)
        connector.end_session()
        return "Registration succeeded"

    except Exception as e:
        print(e)
        return "Registration failed"


if __name__ == "__main__":
    print("===================================================\n"
          "                STARTING UVICORN...\n"
          "===================================================")
    uvicorn.run(app, host="localhost", port=8000)