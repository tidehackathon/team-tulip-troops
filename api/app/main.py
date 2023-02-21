from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health, analyse

app = FastAPI(
    title="Hackathon NATO Tide",
    description='description',
    version="0.0.1",
    terms_of_service="https://www.nato.int/",
    license_info={
        "name": "All rights reserved",
        "url": "https://www.nato.int/",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(analyse.router, tags=['Analyse'], prefix='/analyse')
app.include_router(health.router, tags=['Health'], prefix='/health')