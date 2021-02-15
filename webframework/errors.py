class error_404:
    def __call__(self, *args, **kwargs):
        return "404 Not Found", "<h1>404 Page Not Found</h1>"


class error_405:
    def __call__(self, *args, **kwargs):
        return "404 Not Found", "<h1>405 Method Not Allowed</h1>"
