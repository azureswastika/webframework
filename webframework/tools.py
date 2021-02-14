from jinja2 import Template


class PathDescriptor:
    def __set__(self, obj, value: str) -> None:
        if not value.endswith("/"):
            value = value + "/"
        obj.__dict__[self.name] = value

    def __set_name__(self, owner, name) -> None:
        self.name = name


def render(path: str, context: dict) -> str:
    with open(path, encoding="utf-8") as f:
        template = Template(f.read())
        return template.render(**context)
