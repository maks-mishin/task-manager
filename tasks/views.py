from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django_filters.views import FilterView

from task_manager.mixins import CheckLoginMixin
from tasks.filters import TaskFilter
from tasks.forms import TaskForm
from tasks.models import Task
from users.models import User


class TaskListView(LoginRequiredMixin, CheckLoginMixin,
                   SuccessMessageMixin, FilterView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskCreateView(LoginRequiredMixin, CheckLoginMixin,
                     SuccessMessageMixin, CreateView):
    model = Task
    template_name = 'tasks/create.html'
    form_class = TaskForm
    success_message = gettext_lazy('Задача успешно создана')
    success_url = reverse_lazy('list_tasks')

    def form_valid(self, form):
        author = User.objects.get(pk=self.request.user.pk)
        form.instance.author = author
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, CheckLoginMixin,
                     SuccessMessageMixin, UpdateView):
    model = Task
    template_name = 'tasks/update.html'
    form_class = TaskForm
    success_message = gettext_lazy('Задача успешно изменена')
    success_url = reverse_lazy('list_tasks')


class TaskDeleteView(LoginRequiredMixin, CheckLoginMixin,
                     SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('list_tasks')
    success_message = gettext_lazy('Задача успешно удалена')

    def form_valid(self, form):
        if self.request.user != self.get_object().author:
            messages.error(self.request, gettext_lazy('Задачу может удалить\
                                                       только её автор'))
        else:
            super().form_valid(form)
        return redirect(self.success_url)


class TaskDetailView(LoginRequiredMixin, CheckLoginMixin,
                     SuccessMessageMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'
