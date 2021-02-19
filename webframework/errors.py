class error_404:
    def __call__(self, *args, **kwargs):
        return (
            "<h1>404 Page Not Found</h1>",
            "404 Not Found",
            [("Content-Type", "text/html")],
        )


class error_405:
    def __call__(self, *args, **kwargs):
        return (
            "<h1>405 Method Not Allowed</h1>",
            "405 Method Not Allowed",
            [("Content-Type", "text/html")],
        )
