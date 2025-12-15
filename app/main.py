from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1 import router as v1_router
from app.db.session import Base, engine


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="API's for Social Media App.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount(
    "/projects",
    StaticFiles(directory="generated_sites", html=True),
    name="projects",
)


@app.get("/check", summary="Public Endpoint to Check the Server Health.")
async def check():
    return {"Status": "Good"}


# Register Routes
app.include_router(v1_router, prefix="/api/v1", tags=["Version 1 API"])
