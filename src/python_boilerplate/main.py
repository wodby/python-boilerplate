from collections.abc import Callable, Iterable
from http import HTTPStatus

StartResponse = Callable[[str, list[tuple[str, str]]], None]


def app(environ: dict, start_response: StartResponse) -> Iterable[bytes]:
    """Serve the application and health-check endpoints."""
    path = environ.get("PATH_INFO", "/")
    if path == "/healthz":
        status = HTTPStatus.OK
        body = b"ok\n"
        content_type = "text/plain; charset=utf-8"
    elif path == "/":
        status = HTTPStatus.OK
        body = b'{"message":"Hello from Wodby Python"}\n'
        content_type = "application/json"
    else:
        status = HTTPStatus.NOT_FOUND
        body = b'{"detail":"Not found"}\n'
        content_type = "application/json"

    start_response(
        f"{status.value} {status.phrase}",
        [
            ("Content-Type", content_type),
            ("Content-Length", str(len(body))),
        ],
    )
    return [body]
