from labels.forms import LabelForm
from labels.models import Label
from task_manager.mixins import CheckLoginMixin, CheckDeleteMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import (ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  FormView)


class LabelListView(LoginRequiredMixin, CheckLoginMixin, ListView):
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'


class LabelCreateView(SuccessMessageMixin, CheckLoginMixin, CreateView):
    model = Label
    template_name = 'labels/create.html'
    form_class = LabelForm
    success_message = gettext_lazy('Метка успешно создана')
    success_url = reverse_lazy('list_labels')


class LabelUpdateView(LoginRequiredMixin, CheckLoginMixin,
                      SuccessMessageMixin, UpdateView, FormView):
    model = Label
    template_name = 'labels/update.html'
    form_class = LabelForm
    success_message = gettext_lazy('Метка успешно изменена')
    success_url = reverse_lazy('list_labels')


class LabelDeleteView(LoginRequiredMixin, CheckLoginMixin, CheckDeleteMixin,
                      SuccessMessageMixin, DeleteView, FormView):
    model = Label
    template_name = 'labels/delete.html'
    error_delete_message = 'Невозможно удалить метку,\
                            потому что она используется'
    success_delete_message = 'Метка успешно удалена'
    redirect_delete_url = 'list_labels'
