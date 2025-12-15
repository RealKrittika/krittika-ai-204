from pathlib import Path
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="FastAPI Web UI Example")

# Templates and static files (serve from app/templates and app/static)
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/", response_class=None)
async def index(request: Request):
    """Render the single-page UI."""
    # Read the `test` env variable (set via App Service configuration later)
    test_value = os.environ.get("test")
    return templates.TemplateResponse("index.html", {"request": request, "test": test_value})


@app.get("/api/ping")
async def api_ping():
    return JSONResponse({"message": "pong"})


if __name__ == "__main__":
    import os
    import platform
    import shutil
    import sys
    import subprocess

    # Default: run using Uvicorn when executing this file directly.
    # If you want to run Gunicorn from this script (useful in Linux/containers),
    # set the environment variable `USE_GUNICORN=1` before running.
    use_gunicorn = os.environ.get("USE_GUNICORN", "0") == "1"
    is_windows = platform.system().lower().startswith("win")

    if use_gunicorn and not is_windows:
        # Prefer to exec gunicorn if available and explicitly requested.
        gunicorn_path = shutil.which("gunicorn")
        if gunicorn_path:
            cmd = [
                gunicorn_path,
                "-k",
                "uvicorn.workers.UvicornWorker",
                "app.main:app",
                "--bind",
                "0.0.0.0:8000",
            ]
            # Replace the current process with gunicorn for proper signal handling
            os.execv(gunicorn_path, cmd)
        else:
            print("gunicorn requested via USE_GUNICORN=1 but gunicorn is not installed.")
            print("Falling back to running Uvicorn directly.")

    # Run Uvicorn directly (good for local development and Windows).
    # Enable reload if DEV_RELOAD=1 (default to 1 for convenience when developing).
    dev_reload = os.environ.get("DEV_RELOAD", "1") == "1"
    try:
        import uvicorn

        uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=dev_reload)
    except Exception as exc:
        print("Failed to start Uvicorn:", exc, file=sys.stderr)
        sys.exit(1)
