from threading import local
import uuid

class RequestThreadlocal(local):
    request = object()

class RequestLoggingMiddleware(object):
    """
    RequestLoggingMiddleware enables better logging of Django requests.

    It assigns a unique ID to each request, using the Python uuid module, and
    keeps a threadlocal reference to the request that logging filters or
    adapters can use to access request attributes.

    It should be installed first in your MIDDLEWARE_CLASSES setting, so that
    the request information is available for logging as early as possible.
    """
    
    context = RequestThreadlocal()

    def process_request(self, request):
        request.uuid = uuid.uuid4().hex
        self.context.request = request
        return None
