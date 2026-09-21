from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings

from app.api.upload import router as upload_router
from app.api.chat import router as chat_router


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Multi-Agent AI Chatbot for "
        "Document and PPT Generation"
    ),
)


# -----------------------------------------
# CORS
# -----------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------
# API routes
# -----------------------------------------

app.include_router(
    upload_router
)

app.include_router(
    chat_router
)


# -----------------------------------------
# Static generated files
# -----------------------------------------

app.mount(
    "/storage",
    StaticFiles(
        directory="storage"
    ),
    name="storage",
)


# -----------------------------------------
# Root
# -----------------------------------------

@app.get("/")
def root():

    return {
        "message": (
            "Multi-Agent Document AI "
            "API is running"
        ),
        "version": settings.app_version,
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }