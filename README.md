# FastAPI Web UI Example
````markdown
# FastAPI Web UI Example

This is a minimal FastAPI project with a small web-based UI served using Jinja2 templates and static assets.

## Quick start (Windows)

1. Create a virtual environment and activate it (recommended):

```cmd
python -m venv .venv
\.venv\Scripts\activate
```

2. Install dependencies:

```cmd
pip install -r requirements.txt
```

3. Run the app:

```cmd
run.bat
```

4. Open http://127.0.0.1:8000 in your browser.

## What you get

- `app/main.py` — FastAPI application mounting static files and rendering `index.html`.
- `app/templates/` — Jinja2 templates.
- `app/static/` — CSS and JS assets used by the UI.

Feel free to extend the API and UI.

## Deploy to Azure App Service (Linux)

This project includes a `Procfile` and `startup.txt` so it can be started using `gunicorn` with Uvicorn workers on Azure App Service (Linux). Follow these steps to deploy using the Azure CLI.

1. Create a resource group and App Service plan (Linux):

```cmd
az group create --name myResourceGroup --location eastus
az appservice plan create --name myPlan --resource-group myResourceGroup --sku B1 --is-linux
```

2. Create a web app (specify Python version, e.g. 3.11):

```cmd
az webapp create --resource-group myResourceGroup --plan myPlan --name <YOUR_UNIQUE_APP_NAME> --runtime "PYTHON:3.11"
```

3. Deploy using ZIP deploy (from project root):

```cmd
cd /d d:\temp\fastapi_webapp
zip -r deploy.zip .
az webapp deployment source config-zip --resource-group myResourceGroup --name <YOUR_UNIQUE_APP_NAME> --src deploy.zip
```

4. (Optional) Set the startup command in Azure Portal or via CLI to the `startup.txt` content, or let Azure use the `Procfile` automatically. CLI example to set startup command:

```cmd
az webapp config set --resource-group myResourceGroup --name <YOUR_UNIQUE_APP_NAME> --startup-file "gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:$PORT"
```

Notes:
- The web app binds to the `$PORT` environment variable that Azure sets at runtime.
- Use the Linux App Service plan — Windows App Service expects different (IIS/wfastcgi) configuration.
- To enable live reload during development, run locally with `--reload` rather than using reload in production on Azure.

If you'd like, I can add a small `azure-pipelines.yml` or GitHub Actions workflow to automate the deploy.

````


## Windows: gunicorn "fcntl" error (local fix)

If you tried `gunicorn -k uvicorn.workers.UvicornWorker ...` on Windows you may see:

```
ModuleNotFoundError: No module named 'fcntl'
```

That's because `gunicorn` uses `fcntl`, which is only available on Unix-like systems. To run locally on Windows use one of these options:

- Use `uvicorn` directly (recommended for local development):

```cmd
cd /d d:\temp\fastapi_webapp
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- Use the provided cross-platform starter which uses `uvicorn` on Windows and `gunicorn` on Linux/WSL:

```cmd
cd /d d:\temp\fastapi_webapp
.venv\Scripts\activate
python start.py   # or run start.bat from cmd.exe
```

- Test gunicorn in a Linux environment (WSL or Docker) if you need parity with Azure:

WSL example:
```bash
# inside WSL
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

If you'd like, I can add a `Dockerfile` so you can run the same Linux container locally for parity with Azure.

## Notes about running with Uvicorn

- If you run `uvicorn main:app --reload` from the project root you may see:

  "Error loading ASGI app. Could not import module \"main\"."

  This happens because the real app is inside the `app/` package (`app/main.py`). There are two fixes:

  1. Recommended: run Uvicorn pointing to the package module:

	  ```cmd
	  python -m uvicorn app.main:app --reload
	  ```

  2. If you prefer the shorthand `uvicorn main:app`, there's a top-level wrapper `main.py` included that re-exports the app. Make sure you run the command from the project root:

	  ```cmd
	  cd /d d:\temp\fastapi_webapp
	  python -m uvicorn main:app --reload
	  ```

  Use whichever is more convenient for your workflow; both start the same ASGI `app`.
