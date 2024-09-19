from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response
        
    def __call__(self, request):
        if not request.user.is_authenticated:
            allowed_urls = [
                reverse('login'),
                reverse('password_reset'),
                reverse('password_reset_done'),
            ]
            
            if not any(request.path.startswith(url) for url in allowed_urls):
                return redirect(f'{settings.LOGIN_URL}?next={request.path}')
        return self._get_response(request)
