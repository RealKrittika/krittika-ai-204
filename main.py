"""Top-level wrapper so `uvicorn main:app` works from the project root.

This simply re-exports the `app` object defined in `app/main.py`.
"""
from app.main import app  # re-export for uvicorn

__all__ = ["app"]
