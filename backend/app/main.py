from fastapi import FastAPI
from app.api import runs, stream

def create_app() -> FastAPI:
    app = FastAPI(title="Agent Bench")
    app.include_router(runs.router)
    app.include_router(stream.router)
    return app

app = create_app()
