from enum import Enum


class HttpMethod(Enum):
    """
    Enum for HTTP methods.
    """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"