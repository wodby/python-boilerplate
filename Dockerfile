FROM wodby/python:dev

ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_CACHE=1

COPY --chown=wodby:wodby pyproject.toml uv.lock /usr/src/app/
COPY --chown=wodby:wodby src /usr/src/app/src
RUN uv sync

CMD ["uv", "run", "python", "src/python_boilerplate/main.py"]