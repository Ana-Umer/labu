# main.py
from fastapi import FastAPI
from database import create_db_and_tables
from routers.plate import router as plates_router

app = FastAPI(title="Car Plate API", version="1.0")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(plates_router)
app.include_router(plates_router)

# @app.get("/")
# def root():
#     return {"status": "ok"}


