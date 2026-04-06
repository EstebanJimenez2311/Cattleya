import time
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.admin.forms import AdminAuthenticationForm
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse


class CattleyaAdminAuthenticationForm(AdminAuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        label="Mantener sesion activa",
        help_text="Conserva la sesion entre cierres del navegador en este dispositivo.",
    )

    error_messages = {
        **AdminAuthenticationForm.error_messages,
        "invalid_login": (
            "Credenciales invalidas o sin permisos para acceder al panel."
        ),
    }


class AdminSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._should_expire_session(request):
            auth.logout(request)
            messages.warning(
                request,
                "Tu sesion expiro por inactividad. Ingresa nuevamente para continuar.",
            )
            login_url = self._build_login_redirect(request)
            return HttpResponseRedirect(login_url)

        response = self.get_response(request)
        self._refresh_session(request)
        return response

    def _is_admin_request(self, request):
        return request.path.startswith("/admin/")

    def _is_authenticated_staff(self, request):
        return (
            bool(getattr(request, "user", None))
            and request.user.is_authenticated
            and request.user.is_staff
        )

    def _should_expire_session(self, request):
        if not self._is_admin_request(request) or not self._is_authenticated_staff(request):
            return False

        timeout_seconds = getattr(settings, "ADMIN_SESSION_IDLE_TIMEOUT", 0)
        if timeout_seconds <= 0:
            return False

        last_activity = request.session.get("admin_last_activity_at")
        if last_activity is None:
            return False

        return (time.time() - float(last_activity)) > timeout_seconds

    def _refresh_session(self, request):
        if not self._is_admin_request(request) or not self._is_authenticated_staff(request):
            return

        remember_me = request.session.get("admin_remember_me")
        if request.path == "/admin/login/" and request.method == "POST":
            remember_me = request.POST.get("remember_me") == "on"
            request.session["admin_remember_me"] = remember_me

        expiry = (
            settings.ADMIN_REMEMBER_ME_AGE
            if remember_me
            else settings.ADMIN_SESSION_COOKIE_AGE
        )
        request.session.set_expiry(expiry)
        request.session["admin_last_activity_at"] = time.time()

    def _build_login_redirect(self, request):
        query = urlencode({"next": request.get_full_path()})
        return f"{reverse('admin:login')}?{query}"
