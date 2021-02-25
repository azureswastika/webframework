from typing import Any

from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader


class ViewMetaclass(type):
    _routes = {}
    _alias = {}

    def __new__(cls, clsname, bases, dct):
        def process_path(path: str):
            if not path.startswith("/"):
                path = "/{}".format(path)
            if not path.endswith("/"):
                path = "{}/".format(path)
            return path

        if path := dct.get("route"):
            if isinstance(path, str):
                path = process_path(path)
                cls._routes[path] = super(ViewMetaclass, cls).__new__(
                    cls, clsname, bases, dct
                )
                cls._alias[clsname] = path
                dct["route"] = path
                return
            elif isinstance(path, list):
                for el in path:
                    el = process_path(el)
                    cls._routes[el] = super(ViewMetaclass, cls).__new__(
                        cls, clsname, bases, dct
                    )
                    cls._alias[clsname] = el
                dct["route"] = path
                return
        return super(ViewMetaclass, cls).__new__(cls, clsname, bases, dct)


class PathDescriptor:
    def __set__(self, obj, value: str) -> None:
        if not value.endswith("/"):
            value = "{}/".format(value)
        obj.__dict__[self.name] = value

    def __set_name__(self, owner, name) -> None:
        self.name = name


class HttpQuery:
    def __init__(self, *args, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def __getattr__(self, name: str) -> Any:
        return self.__dict__.get(name)


def render(
    template_name: str, request: dict, context: dict = {}, templates="templates", *args, **kwargs
) -> str:
    env = Environment()
    env.loader = FileSystemLoader(templates)
    template = env.get_template(template_name)
    return template.render(**request, **context)


def reverse(name: str):
    return ViewMetaclass._alias.get(name)
