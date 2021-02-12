from jinja2 import Template


class BaseView:
    route = None
    template = None

    def __call__(self, request, *args, **kwargs):
        with open(self.template, encoding="utf-8") as f:
            template = Template(f.read())
            template = [template.render(**request).encode("utf-8")]
        return "200 OK", template
