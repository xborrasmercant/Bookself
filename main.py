import datetime
import random
from typing import Annotated
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from psycopg2 import Date
import uvicorn

from connector import Connector

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

# ===============
# GET ENDPOINTS
# ===============

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/login", response_class=HTMLResponse)
def login_endpoint(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/register", response_class=HTMLResponse)
def register_endpoint(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")

@app.get("/hub", response_class=HTMLResponse)
def hub_endpoint(request: Request):
    return templates.TemplateResponse(request=request, name="hub.html")

@app.get("/books/create", response_class=HTMLResponse)
def register_endpoint(request: Request):
    return templates.TemplateResponse(request=request, name="book_form.html")


# ===============
# POST ENDPOINTS
# ===============

@app.post("/login/request", response_class=HTMLResponse)
def login_request(request: Request, username_or_email: Annotated[str, Form()], password: Annotated[str, Form()]):
    connector = Connector()
    
    try:
        if connector.user_login(username_or_email, password):    
            connector.end_session()
            return templates.TemplateResponse(request=request, name="hub.html")
        else:
            return f"[ERROR] User or password are not correct."

    except Exception as e:
        print(e)
        return "Login failed"


@app.post("/register/request", response_class=HTMLResponse)
def register_request(request: Request, username: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()], confirm_password: Annotated[str, Form()]):
    connector = Connector()

    if password != confirm_password:
        return "Passwords are not equal"
    
    try:
        connector.user_register(username, email, password)
        connector.end_session()
        return templates.TemplateResponse(request=request, name="hub.html")

    except Exception as e:
        print(e)
        return "Registration failed"


@app.post("/users_list", response_class=HTMLResponse)
def hub_endpoint(request: Request):
    connector = Connector()

    registered_users = str(connector.get_registered_users())
    connector.end_session()

    return registered_users


@app.post("/books/create/submit", response_class=HTMLResponse)
def register_endpoint(request: Request,
                      name: Annotated[str, Form()],
                      description: Annotated[str, Form()],
                      author: Annotated[str, Form()],
                      editor: Annotated[str, Form()],
                      publication_date: Annotated[Date, Form()],
                      page_qty: Annotated[int, Form()],
                      book_cover_uri: Annotated[str, Form()],
                      ):

    connector = Connector()

    book_id = random.randint(0, 9999999999)
    connector.insert_book(book_id, name, description, author, publication_date, page_qty, book_cover_uri)
    connector.insert_user_book(book_id, username, datetime.datetime.now(), datetime.datetime.now())



    return templates.TemplateResponse(request=request, name="book_form.html")



if __name__ == "__main__":
    print("===================================================\n"
          "                STARTING UVICORN...\n"
          "===================================================")
    uvicorn.run(app, host="localhost", port=8000)