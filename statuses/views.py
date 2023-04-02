from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import (CreateView, DeleteView, FormView, ListView,
                                  UpdateView)

from statuses.forms import StatusForm
from statuses.models import Status
from task_manager.mixins import CheckDeleteMixin, CheckLoginMixin


class StatusListView(LoginRequiredMixin, CheckLoginMixin, ListView):
    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, CheckLoginMixin,
                       SuccessMessageMixin, CreateView, FormView):
    model = Status
    template_name = 'statuses/create.html'
    form_class = StatusForm
    success_message = gettext('Статус успешно создан')
    success_url = reverse_lazy('list_statuses')


class StatusUpdateView(LoginRequiredMixin, CheckLoginMixin,
                       SuccessMessageMixin, UpdateView):
    model = Status
    template_name = 'statuses/update.html'
    form_class = StatusForm
    success_message = gettext('Статус успешно изменён')
    success_url = reverse_lazy('list_statuses')


class StatusDeleteView(LoginRequiredMixin, CheckLoginMixin, CheckDeleteMixin,
                       SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    error_delete_message = 'Невозможно удалить статус,\
                                потому что он используется'
    success_delete_message = 'Статус успешно удалён'
    redirect_delete_url = 'list_statuses'
    context_object_name = 'status'
