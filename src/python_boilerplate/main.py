import json
import platform
from collections.abc import Callable, Iterable, Mapping
from http import HTTPStatus
from importlib.resources import files

StartResponse = Callable[[str, list[tuple[str, str]]], object]

RESOURCE_ROOT = files("python_boilerplate").joinpath("resources")
INDEX_TEMPLATE = RESOURCE_ROOT.joinpath("index.html").read_text(encoding="utf-8")
STYLES = RESOURCE_ROOT.joinpath("styles.css").read_bytes()


def app(
    environ: Mapping[str, object],
    start_response: StartResponse,
) -> Iterable[bytes]:
    """Serve the framework-free WSGI starter."""
    method = str(environ.get("REQUEST_METHOD", "GET")).upper()
    path = environ.get("PATH_INFO", "/")

    if method not in {"GET", "HEAD"}:
        return send(
            start_response,
            HTTPStatus.METHOD_NOT_ALLOWED,
            json_body({"detail": "Method not allowed"}),
            "application/json; charset=utf-8",
            method=method,
            extra_headers=[("Allow", "GET, HEAD")],
        )

    if path == "/healthz":
        return send(
            start_response,
            HTTPStatus.OK,
            b"ok\n",
            "text/plain; charset=utf-8",
            method=method,
        )
    if path == "/api/status":
        return send(
            start_response,
            HTTPStatus.OK,
            json_body(
                {
                    "status": "ok",
                    "runtime": f"Python {platform.python_version()}",
                    "interface": "WSGI",
                }
            ),
            "application/json; charset=utf-8",
            method=method,
        )
    if path == "/assets/styles.css":
        return send(
            start_response,
            HTTPStatus.OK,
            STYLES,
            "text/css; charset=utf-8",
            method=method,
        )
    elif path == "/":
        body = INDEX_TEMPLATE.format(python_version=platform.python_version()).encode()
        return send(
            start_response,
            HTTPStatus.OK,
            body,
            "text/html; charset=utf-8",
            method=method,
        )

    return send(
        start_response,
        HTTPStatus.NOT_FOUND,
        json_body({"detail": "Not found"}),
        "application/json; charset=utf-8",
        method=method,
    )


def json_body(payload: Mapping[str, str]) -> bytes:
    """Encode a compact JSON response body."""
    return f"{json.dumps(payload, separators=(',', ':'))}\n".encode()


def send(
    start_response: StartResponse,
    status: HTTPStatus,
    body: bytes,
    content_type: str,
    *,
    method: str,
    extra_headers: list[tuple[str, str]] | None = None,
) -> Iterable[bytes]:
    """Start a WSGI response and suppress HEAD bodies."""
    headers = [
        ("Content-Type", content_type),
        ("Content-Length", str(len(body))),
    ]
    if extra_headers:
        headers.extend(extra_headers)
    start_response(
        f"{status.value} {status.phrase}",
        headers,
    )
    return [] if method == "HEAD" else [body]
