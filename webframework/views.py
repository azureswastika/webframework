from .tools import render
from .errors import error_405


class BaseView:
    route = None

    @staticmethod
    def routes():
        def get_subclasses(cls=BaseView):
            return set(cls.__subclasses__()).union(
                [s for c in cls.__subclasses__() for s in get_subclasses(c)]
            )

        return dict([(view.route, view) for view in get_subclasses() if view.route])


class TemplateView(BaseView):
    template = None

    def get(self, request):
        return render(self.template, request)

    def __call__(self, request, *args, **kwargs) -> tuple:
        if request["method"] == "GET":
            return "200 OK", [self.get(request).encode("utf-8")]
        return error_405()()


class View(TemplateView):
    def post(self, request):
        return render(self.template, request)

    def __call__(self, request, *args, **kwargs) -> tuple:
        if request["method"] == "GET":
            return "200 OK", [self.get(request).encode("utf-8")]
        elif request["method"] == "POST":
            return "200 OK", [self.post(request).encode("utf-8")]
        return error_405()()
