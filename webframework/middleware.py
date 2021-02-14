from urllib.parse import parse_qsl


class BaseMiddleware:
    alias = None


class RequestMethod(BaseMiddleware):
    alias = "RequestMethod"

    def __call__(self, request: dict, environ: dict, *args, **kwargs):
        method = environ.get("REQUEST_METHOD")
        if method == "GET":
            request.update(self.parse_get_query(environ.get("QUERY_STRING")))
        elif method == "POST":
            request.update(self.parse_post_query(environ))
        request["method"] = method

    def parse_post_query(self, environ: dict) -> dict:
        length = int(environ.get("CONTENT_LENGTH", "0"))
        return dict(
            parse_qsl(environ.get("wsgi.input", b"").read(length).decode(), True)
        )

    def parse_get_query(self, data: str) -> dict:
        return dict(parse_qsl(data))
