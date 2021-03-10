from typing import Any

from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader


class MiddlewareMetaclass(type):
    _middleware = list()

    def __new__(cls, clsname, bases, dct):
        middleware = super(ViewMetaclass, cls).__new__(cls, clsname, bases, dct)
        cls._middleware.append(middleware)
        return middleware


class ViewMetaclass(type):
    _routes = dict()
    _alias = dict()

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
                cls._routes[path], cls._alias[clsname] = (
                    super(ViewMetaclass, cls).__new__(cls, clsname, bases, dct),
                    path,
                )
                return
            elif isinstance(path, list):
                for el in path:
                    el = process_path(el)
                    cls._routes[el], cls._alias[clsname] = (
                        super(ViewMetaclass, cls).__new__(cls, clsname, bases, dct),
                        el,
                    )
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
    template_name: str,
    request: dict,
    context: dict = {},
    templates="templates",
    *args,
    **kwargs,
) -> str:
    env = Environment()
    env.loader = FileSystemLoader(templates)
    template = env.get_template(template_name)
    return template.render(**request, **context)


def reverse(name: str):
    return ViewMetaclass._alias.get(name)
