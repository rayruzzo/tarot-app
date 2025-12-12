from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
import uuid

class DevSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'dev_session_id' not in request.session:
            request.session['dev_session_id'] = str(uuid.uuid4())

class EnsureUserIdMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'user_id' not in request.session:
            return JsonResponse({'error': 'User is not authenticated'}, status=401)

class ValidateReadingTypeMiddleware(MiddlewareMixin):
    def process_view(self, request):
        reading_type = request.POST.get('reading_type') or request.GET.get('reading_type')
        from tarot.utils import TEMPLATE_DISPATCH
        if reading_type and reading_type not in TEMPLATE_DISPATCH:
            return JsonResponse({'error': 'Invalid reading type'}, status=400)