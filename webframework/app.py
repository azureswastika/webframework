from typing import Callable
from wsgiref.simple_server import WSGIRequestHandler, WSGIServer

from .errors import error_404
from .middleware import BaseMiddleware
from .tools import PathDescriptor
from .views import BaseView


class Application:
    path = PathDescriptor()

    def __init__(self, ip: str = "", port: int = 8000) -> None:
        self.routes = BaseView.routes()
        self.middleware = [middleware for middleware in BaseMiddleware.__subclasses__()]
        try:
            self.server = WSGIServer((ip, port), WSGIRequestHandler)
            self.server.set_app(self.__call__)
            self.server.serve_forever()
        except (OSError, NameError):
            pass

    def __call__(self, environ: dict, start_response: Callable):
        return self.wsgi(environ, start_response)

    def wsgi(self, environ: dict, start_response: Callable):
        self.path = environ.get("PATH_INFO")
        view = self.routes.get(self.path, error_404)()
        request = {}
        for middleware in self.middleware:
            middleware()(request, environ)
        code, body = view(request)
        start_response(code, [("Content-Type", "text/html")])

        return body
