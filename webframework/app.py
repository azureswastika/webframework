from wsgiref.simple_server import WSGIRequestHandler, WSGIServer

from .views import BaseView
from .middleware import user


class PathDescriptor:
    def __set__(self, obj, value: str):
        if not value.startswith("/"):
            value = "/" + value
        if not value.endswith("/"):
            value = value + "/"
        obj.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Application:
    path = PathDescriptor()

    def __init__(self, ip="", port=8000) -> None:
        self.routes = dict([(view.route, view) for view in BaseView.__subclasses__()])
        self.middleware = [user]

        self.server = WSGIServer((ip, port), WSGIRequestHandler)
        self.server.set_app(self.__call__)
        self.server.serve_forever()

    def __call__(self, environ, start_response):
        self.path = environ["PATH_INFO"]
        if self.path in self.routes:
            view = self.routes[self.path]()
        else:
            view = error_404
        request = {}
        for middleware in self.middleware:
            middleware(request)
        code, body = view(request)
        start_response(code, [("Content-Type", "text/html")])

        return body


def error_404(request):
    return "404 Not Found", [b'<h1>404 Page Not Found</h1>']
