from django.conf import settings
from django.contrib.auth.views import LoginView
from django.shortcuts import resolve_url, reverse
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
)
from django.http import HttpResponseRedirect

class CustomLoginView(LoginView):
    
    def get_success_url(self):
        url = self.get_redirect_url()
        if self.request.user.is_staff:
            return url or resolve_url(settings.LOGIN_REDIRECT_URL)
        elif not self.request.user.is_staff:
            return reverse("api_view")
        else:
            return reverse("login_url")