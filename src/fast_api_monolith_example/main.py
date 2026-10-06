from fastapi import FastAPI

app = FastAPI(title="Fast API Monolith Example", version="0.1.0")



@app.get("/")
def read_root():
    return {"title": "Fast API Monolith Example", "version": "0.1.0"}