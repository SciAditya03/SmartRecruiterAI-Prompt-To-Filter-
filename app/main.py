from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.database import engine, Base
from app.api.routes import search
from pathlib import Path

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmartRecruit AI")

# Include routes
app.include_router(search.router)

# Serve Frontend
# This dynamically finds the 'frontend' folder at the root of your project
frontend_path = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_path = frontend_path / "index.html"
    return html_path.read_text()