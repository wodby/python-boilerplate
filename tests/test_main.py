from python_boilerplate.main import app


def request(
    path: str,
    method: str = "GET",
) -> tuple[str, dict[str, str], bytes]:
    response = {}

    def start_response(status, headers):
        response["status"] = status
        response["headers"] = dict(headers)

    body = b"".join(
        app(
            {"PATH_INFO": path, "REQUEST_METHOD": method},
            start_response,
        )
    )
    return response["status"], response["headers"], body


def test_index():
    status, headers, body = request("/")

    assert status == "200 OK"
    assert headers["Content-Type"] == "text/html; charset=utf-8"
    assert b"Your Python app is running" in body


def test_static_asset():
    status, headers, body = request("/assets/styles.css")

    assert status == "200 OK"
    assert headers["Content-Type"] == "text/css; charset=utf-8"
    assert body.startswith(b":root")


def test_status():
    status, headers, body = request("/api/status")

    assert status == "200 OK"
    assert headers["Content-Type"] == "application/json; charset=utf-8"
    assert b'"interface":"WSGI"' in body


def test_healthz():
    status, _, body = request("/healthz")

    assert status == "200 OK"
    assert body == b"ok\n"


def test_not_found():
    status, _, body = request("/missing")

    assert status == "404 Not Found"
    assert body == b'{"detail":"Not found"}\n'


def test_method_not_allowed():
    status, headers, body = request("/", method="POST")

    assert status == "405 Method Not Allowed"
    assert headers["Allow"] == "GET, HEAD"
    assert body == b'{"detail":"Method not allowed"}\n'


def test_head():
    status, headers, body = request("/", method="HEAD")

    assert status == "200 OK"
    assert int(headers["Content-Length"]) > 0
    assert body == b""
