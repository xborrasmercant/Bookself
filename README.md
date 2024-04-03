# bookSELF
bookSELF is an online platform where you can store, manage, and share you favourite books with other users.

1. Create a new virtual environment in the root directory of the project:
WINDOWS: `python3 -m venv venv`

2. Activate the virtual environment:
WINDOWS: `.\venv\Scripts\activate`
Make sure your system have permission to execute ps scripts
`Set-ExecutionPolicy RemoteSigned`

3. Install the needed dependencies:
`pip install fastapi uvicorn autopep8 jinja2 psycopg2 python-multipart`



docker run --name bookself-postgres -p 5432:5432 -e POSTGRES_PASSWORD=bookself -d postgres
