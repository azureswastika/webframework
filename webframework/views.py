from .errors import error_405
from .tools import ViewMetaclass, render


class BaseView(metaclass=ViewMetaclass):
    route = None


class TemplateView(BaseView):
    template = None

    def get(self, request: dict):
        return render(self.template, request)

    def __call__(self, request: dict, *args, **kwargs) -> tuple:
        if request.get("method") == "GET":
            return self.get(request), "200 OK", [("Content-Type", "text/html")]
        return error_405()()


class View(TemplateView):
    def post(self, request: dict):
        """Post request"""

    def __call__(self, request: dict, *args, **kwargs) -> tuple:
        if request.get("method") == "GET":
            return self.get(request), "200 OK", [("Content-Type", "text/html")]
        elif request.get("method") == "POST":
            return self.post(request), "201 Created", [("Content-Type", "text/html")]
        return error_405()()
