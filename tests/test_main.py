from python_boilerplate.main import app


def request(path: str) -> tuple[str, bytes]:
    response = {}

    def start_response(status, _headers):
        response["status"] = status

    body = b"".join(app({"PATH_INFO": path}, start_response))
    return response["status"], body


def test_index():
    status, body = request("/")

    assert status == "200 OK"
    assert body == b'{"message":"Hello from Wodby Python"}\n'


def test_healthz():
    status, body = request("/healthz")

    assert status == "200 OK"
    assert body == b"ok\n"
