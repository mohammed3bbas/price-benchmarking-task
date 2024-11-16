from fastapi import FastAPI
from app.api import upload_csv_api

app = FastAPI()

app.include_router(upload_csv_api.router, prefix="/upload", tags=["upload"])