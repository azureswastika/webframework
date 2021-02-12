from wsgiref.simple_server import WSGIRequestHandler, WSGIServer

from jinja2 import Template


class BaseView:
    route = None
    template = None

    def __call__(self, request, *args, **kwargs):
        with open(self.template, encoding="utf-8") as f:
            template = Template(f.read())
            template = [
                line.encode("utf-8") for line in template.render(**request).split("\n")
            ]
        return "200 OK", template


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
        code, body = view(request)
        start_response(code, [("Content-Type", "text/html")])

        return body


def error_404(request):
    return "404 Not Found", [b"404 Page Not Found"]
