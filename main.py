import os
import logging
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from routers import chat, files, setup
from utils.threads import create_thread
from fastapi.exceptions import HTTPException


logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Optional startup logic
    yield
    # Optional shutdown logic

app = FastAPI(lifespan=lifespan)

# Mount routers
app.include_router(chat.router)
app.include_router(files.router)
app.include_router(setup.router)

# Mount static files (e.g., CSS, JS)
app.mount("/static", StaticFiles(directory=os.path.join(os.getcwd(), "static")), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "error_message": str(exc)},
        status_code=500
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error: {exc.detail}")
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "error_message": exc.detail},
        status_code=exc.status_code
    )


# TODO: Implement some kind of thread id storage or management logic to allow
# user to load an old thread, delete an old thread, etc. instead of start new
@app.get("/")
async def read_home(request: Request, thread_id: str = None, messages: list = []):
    logger.info("Home page requested")
    
    # Check if environment variables are missing
    load_dotenv(override=True)
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("ASSISTANT_ID"):
        return RedirectResponse(url=app.url_path_for("read_setup"))
    
    # Create a new assistant chat thread if no thread ID is provided
    if not thread_id or thread_id == "None" or thread_id == "null":
        thread_id: str = await create_thread()
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "assistant_id": os.getenv("ASSISTANT_ID"),
            "messages": messages,
            "thread_id": thread_id
        }
    )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
