# middleware.py
import re
from django.conf import settings
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.shortcuts import redirect,HttpResponseRedirect
from django.urls import resolve, reverse

IGNORE_PATHS = [
    re.compile(url.lstrip("/")) for url in getattr(settings, 'LOGIN_REQUIRED_IGNORE_PATHS', [])
]

# IGNORE_VIEW_NAMES = [
#     name for name in getattr(settings, 'LOGIN_REQUIRED_IGNORE_VIEW_NAMES', [])
# ]


class LoginRequiredMiddleware(AuthenticationMiddleware):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            return
        # resolver = resolve(path)
        # views = ((name == resolver.view_name) for name in IGNORE_VIEW_NAMES)

        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in IGNORE_PATHS):
                return redirect('{}'.format(reverse('users:login')))
