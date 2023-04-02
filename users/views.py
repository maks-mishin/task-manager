from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView, UpdateView, DeleteView

from django.contrib import messages

from django.utils.translation import gettext

from users.forms import UserCreateForm, UserLoginForm
from task_manager.mixins import CheckLoginMixin, CheckUpdateMixin, CheckDeleteMixin
from users.models import User


class UserListView(ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'


class UserCreateView(CreateView, SuccessMessageMixin, FormView):
    model = User
    template_name = 'users/create.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    success_message = gettext('Пользователь успешно зарегистрирован')


class UserLoginView(SuccessMessageMixin, LoginView):
    model = User
    template_name = 'users/sign_in.html'
    form_class = UserLoginForm
    next_page = reverse_lazy('index')
    success_message = gettext('Вы залогинены')


class UserLogoutView(LogoutView, SuccessMessageMixin):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.SUCCESS,
                             gettext('Вы разлогинены'))
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(LoginRequiredMixin, CheckLoginMixin,
                     CheckUpdateMixin, SuccessMessageMixin,
                     UpdateView, FormView):
    model = User
    template_name = 'users/update.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('list_users')
    success_message = gettext('Пользователь успешно изменён')
    redirect_error_update = 'list_users'
    error_update_message = 'У вас нет прав для изменения другого пользователя.'


class UserDeleteView(LoginRequiredMixin, CheckLoginMixin, CheckUpdateMixin,
                     CheckDeleteMixin, SuccessMessageMixin,
                     DeleteView, FormView):
    model = User
    template_name = 'users/delete.html'
    redirect_error_update = 'list_users'
    error_update_message = 'У вас нет прав для изменения другого пользователя.'
    error_delete_message = 'Невозможно удалить пользователя, ' \
                           'потому что он используется'
    success_delete_message = 'Пользователь успешно удалён'
    redirect_delete_url = 'list_users'
    context_object_name = 'user'
