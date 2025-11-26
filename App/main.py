# app/main.py
import logging
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine, Base
from app.api import tasks, auth
from app.websocket.manager import WebSocketManager
from app.models.task import Task  # needed for DB creation
from app.auth import router as auth_router




# ------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scrapyflow")

# ------------------------------------------------------------------
# WebSocket Manager (singleton)
# ------------------------------------------------------------------
websocket_manager = WebSocketManager()

# ------------------------------------------------------------------
# Lifespan events – create tables + warm-up
# ------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables ready")
    yield
    # Shutdown
    await websocket_manager.disconnect_all()
    logger.info("Shutdown complete")

# ------------------------------------------------------------------
# FastAPI app
# ------------------------------------------------------------------
app = FastAPI(
    title="ScrapyFlow – Real-Time Web Scraping Platform",
    description="Dynamic, per-user task queue with live monitoring",
    version="1.0.0",
    lifespan=lifespan,
)

# ------------------------------------------------------------------
# Mount static files & templates
# ------------------------------------------------------------------
app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")
templates = Jinja2Templates(directory="dashboard/templates")

# ------------------------------------------------------------------
# Include routers
# ------------------------------------------------------------------
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# ------------------------------------------------------------------
# WebSocket endpoint
# ------------------------------------------------------------------
from fastapi import WebSocket, WebSocketDisconnect
from app.auth.dependencies import get_current_user_optional

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user=Depends(get_current_user_optional)):
    await websocket_manager.connect(websocket, user)
    try:
        while True:
            data = await websocket.receive_json()
            # Optional: allow client to ping or send messages
            await websocket_manager.broadcast({"type": "pong"}, user=user)
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, user)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        websocket_manager.disconnect(websocket, user)

# ------------------------------------------------------------------
# Public routes
# ------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def root(request: Request, user=Depends(auth.get_current_user_optional)):
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user}
    )

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "ScrapyFlow"}

# ------------------------------------------------------------------
# Global exception handlers (optional but nice)
# ------------------------------------------------------------------
@app.exception_handler(404)
async def not_found(request: Request, exc):
    return templates.TemplateResponse(
        "404.html", {"request": request}, status_code=404
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)