from typing import Callable
from wsgiref.simple_server import make_server

from .errors import error_404
from .tools import PathDescriptor, ViewMetaclass, MiddlewareMetaclass


class Application:
    path = PathDescriptor()

    def __init__(self, ip: str = "", port: int = 8000) -> None:
        self.ip = ip
        self.port = port
        self.routes = ViewMetaclass._routes
        self.middleware = MiddlewareMetaclass._middleware

    def __call__(self, environ: dict, start_response: Callable):
        return self.wsgi(environ, start_response)

    def wsgi(self, environ: dict, start_response: Callable):
        self.path = environ.get("PATH_INFO")
        request = {"path": self.path}
        for middleware in self.middleware:
            middleware()(request, environ)
        view = self.routes.get(self.path, error_404)()
        body, code, headers = view(request)
        start_response(code, headers)
        return [body.encode("utf-8")]

    def start(self):
        try:
            with make_server(self.ip, self.port, self) as server:
                server.serve_forever()
        except (OSError, NameError):
            pass
