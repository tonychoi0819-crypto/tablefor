from django.utils.deprecation import MiddlewareMixin

class RequestLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        pass
