# Minimal Python boilerplate

Minimal WSGI application for the [Wodby Python service](https://github.com/wodby/service-python) and [Python stack](https://github.com/wodby/stack-python).

The project uses [uv](https://docs.astral.sh/uv/) for dependency management and includes a Wodby CI pipeline.

## Local development

```shell
uv sync
uv run pytest
uv run gunicorn --bind 0.0.0.0:8080 python_boilerplate.main:app
```

Open http://localhost:8080. A health endpoint is available at `/healthz`.
