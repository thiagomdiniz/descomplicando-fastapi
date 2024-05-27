from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from fastapi.staticfiles import StaticFiles

from .routes import main_router
from .config import settings

app = FastAPI(
    title="Pamps",
    version="0.1.0",
    description="Pamps is a posting app",
    contact={
        "name": "Contact Name",
        "url": "http://localhost",
        "email": "contact@localhost.com",
    }
)


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(main_router)

#app.mount("/static", StaticFiles(directory="app/static"), name="static")