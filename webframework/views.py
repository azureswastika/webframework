from typing import Callable
from .errors import error_405
from .tools import ViewMetaclass, render


class BaseView(metaclass=ViewMetaclass):
    route = None


class TemplateView(BaseView):
    template = None

    def get(self, request: str):
        return render(self.template, request)

    def __call__(self, start_response: Callable, request: str, *args, **kwargs) -> tuple:
        if request.get("method") == "GET":
            start_response("200 OK", [("Content-Type", "text/html")])
            return self.get(request)
        return error_405()()


class View(TemplateView):
    def post(self, request: str):
        return render(self.template, request)

    def __call__(self, start_response: Callable, request: str, *args, **kwargs) -> tuple:
        if request.get("method") == "GET":
            start_response("200 OK", [("Content-Type", "text/html")])
            return self.get(request)
        elif request.get("method") == "POST":
            start_response("201 Created", [("Content-Type", "text/html")])
            return self.post(request)
        return error_405()()
