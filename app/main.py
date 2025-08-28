from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.endpoints import email

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")
app.include_router(email.router)
@app.get("/")
def serve_index():
    return FileResponse("frontend/index.html")