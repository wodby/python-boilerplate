# Python starter for Wodby

A dependency-free WSGI application for the [Wodby Python service](https://github.com/wodby/service-python) and [Python stack](https://github.com/wodby/stack-python).

It demonstrates:

- a standards-based WSGI callable
- packaged HTML and CSS resources
- JSON, health, not-found, and method-not-allowed responses
- correct GET and HEAD behavior
- pytest, Ruff, Gunicorn, and Wodby CI

## Local development

```shell
uv sync
uv run pytest
uv run gunicorn --bind 0.0.0.0:8080 python_boilerplate.main:app
```

Open <http://localhost:8080>. Useful endpoints are:

- `/` — the packaged HTML landing page
- `/assets/styles.css` — a packaged resource
- `/api/status` — a standard-library JSON response
- `/healthz` — the deployment health endpoint

## Start building

`src/python_boilerplate/main.py` intentionally exposes the WSGI protocol
without introducing another framework. Its small response helper is suitable
for learning or a tiny service; use the dedicated Flask, FastAPI, or Django
starter when the application needs framework features.

HTML and CSS live under `src/python_boilerplate/resources/` and are loaded with
`importlib.resources`, so they continue to work from an installed wheel.

PostgreSQL, Valkey, and SMTP links are optional. When enabled, their connection
values are supplied through Wodby's documented environment variables.
