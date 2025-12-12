from django.shortcuts import redirect

class SessionLoginRequiredMiddleware:
    """
    Middleware that redirects to login if 'user_id' is not in session for protected paths.
    Add this middleware after SessionMiddleware and before your views.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Paths that do NOT require login
        self.allowed_prefixes = [
            '/login', '/signup', '/joinus', '/static', '/media', '/admin', '/api', '/favicon.ico'
        ]

    def __call__(self, request):
        path = request.path.rstrip('/') or '/'
        # Always allow root
        if path == '/':
            return self.get_response(request)
        # Allow if path matches or starts with any allowed prefix
        for prefix in self.allowed_prefixes:
            if path == prefix or path.startswith(prefix + '/'):
                return self.get_response(request)
        # Allow if user is authenticated (session user_id set)
        if request.session.get('user_id'):
            return self.get_response(request)
        # Otherwise, redirect to login
        return redirect('/login/')
