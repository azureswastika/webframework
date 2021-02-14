from .errors import error_405
from .tools import ViewMetaclass, render


class BaseView(metaclass=ViewMetaclass):
    route = None


class TemplateView(BaseView):
    template = None

    def get(self, request: str):
        return render(self.template, request)

    def __call__(self, request: str, *args, **kwargs) -> tuple:
        if request.get("method") == "GET":
            return "200 OK", [self.get(request).encode("utf-8")]
        return error_405()()


class View(TemplateView):
    def post(self, request: str):
        return render(self.template, request)

    def __call__(self, request: str, *args, **kwargs) -> tuple:
        if request.get("method") == "GET":
            return "200 OK", [self.get(request).encode("utf-8")]
        elif request.get("method") == "POST":
            return "200 OK", [self.post(request).encode("utf-8")]
        return error_405()()
