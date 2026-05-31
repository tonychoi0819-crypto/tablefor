from .models import PageView
from django.utils.deprecation import MiddlewareMixin

class RequestLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'GET' and not request.path.startswith(('/static/', '/media/', '/admin/')):
            try:
                PageView.objects.create(
                    url=request.path,
                    user=request.user if request.user.is_authenticated else None,
                    ip_address=self.get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:200]
                )
            except Exception:
                pass
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
