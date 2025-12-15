"""Cross-platform starter for the app.

On Windows this runs Uvicorn directly (since Gunicorn requires Unix fcntl).
On Unix-like environments it will exec Gunicorn with Uvicorn workers.
"""
import os
import platform
import sys
import subprocess

HOST = os.environ.get("HOST", "127.0.0.1")
PORT = os.environ.get("PORT", "8000")

is_windows = platform.system().lower().startswith("win")

if is_windows:
    # Use uvicorn on Windows
    try:
        import uvicorn
    except ImportError:
        print("uvicorn not installed. Install with: pip install uvicorn[standard]")
        sys.exit(1)

    uvicorn.run("app.main:app", host=HOST, port=int(PORT), reload=True)
else:
    # Prefer gunicorn on Unix-like systems
    cmd = [
        "gunicorn",
        "-k",
        "uvicorn.workers.UvicornWorker",
        "app.main:app",
        "--bind",
        f"0.0.0.0:{PORT}",
    ]
    print("Running:", " ".join(cmd))
    os.execvp(cmd[0], cmd)
