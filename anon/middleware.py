from django.http import QueryDict
import logging

logger = logging.getLogger("apps")


class PutAsPostMiddleware:
    """
    Middleware to handle PUT requests with multipart/form-data
    by converting them to POST for Django's request parsing.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'PUT' and request.content_type.startswith('multipart/form-data'):
            try:
                request.PUT = QueryDict(request.body, encoding=request.encoding)
                logger.info(f"Parsed PUT data: {request.PUT}")
                request.method = 'POST'
            except Exception as e:
                logger.error(f"Error parsing PUT request: {e}")
                raise
        response = self.get_response(request)
        if hasattr(request, 'PUT'):
            request.method = 'PUT'

        return response
