from typing import Callable


class error_404:
    def __call__(self, start_response: Callable, *args, **kwargs):
        start_response("404 Not Found", [("Content-Type", "text/html")])
        return "<h1>404 Page Not Found</h1>"


class error_405:
    def __call__(self, start_response: Callable, *args, **kwargs):
        start_response("405 Method Not Allowed", [("Content-Type", "text/html")])
        return "<h1>405 Method Not Allowed</h1>"
