from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext


class CheckLoginMixin(AccessMixin):
    redirect_login_name = 'login'
    error_login_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'
    request = ''

    def handle_no_permission(self):
        messages.error(self.request, gettext(self.error_login_message))
        return redirect(reverse(self.redirect_login_name))


class CheckUpdateMixin(AccessMixin):
    redirect_error_update = ''
    error_update_message = ''

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object():
            messages.error(self.request,
                           gettext(self.error_update_message))
            return redirect(reverse(self.redirect_error_update))
        return super().dispatch(request, *args, **kwargs)


class CheckDeleteMixin(AccessMixin):
    error_delete_message = ''
    success_delete_message = ''
    redirect_delete_url = ''

    def form_valid(self, form):
        try:
            self.object.delete()
        except ProtectedError:
            messages.error(self.request,
                           gettext(self.error_delete_message))
        else:
            messages.success(self.request,
                             gettext(self.success_delete_message))
        return redirect(reverse(self.redirect_delete_url))
