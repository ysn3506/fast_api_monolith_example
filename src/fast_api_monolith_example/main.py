from fastapi import FastAPI
from config.logging_config import configure_logging

app = FastAPI(title="Fast API Monolith Example", version="0.1.0")

configure_logging()

@app.get("/")
def read_root():
    return {"title": "Fast API Monolith Example", "version": "0.1.0"}