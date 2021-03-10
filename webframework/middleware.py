from typing import Union
from urllib.parse import parse_qsl

from .tools import HttpQuery, MiddlewareMetaclass


class BaseMiddleware(metaclass=MiddlewareMetaclass):
    """Base Middleware"""


class RequestMethod(BaseMiddleware):
    def __call__(self, request: dict, environ: dict, *args, **kwargs):
        method = environ.get("REQUEST_METHOD")
        if method == "GET":
            request["GET"] = self.parse_get_query(environ)
        elif method == "POST":
            request["POST"] = self.parse_post_query(environ)
        request["method"] = method

    def parse_post_query(self, environ: dict) -> Union[HttpQuery, None]:
        length = int(environ.get("CONTENT_LENGTH", "0"))
        data = dict(
            parse_qsl(environ.get("wsgi.input", b"").read(length).decode(), True)
        )
        if data != dict():
            return HttpQuery(**data)

    def parse_get_query(self, environ: dict) -> Union[HttpQuery, None]:
        data = dict(parse_qsl(environ.get("QUERY_STRING")))
        if data != dict():
            return HttpQuery(**data)
