import django_filters
from django import forms
from django.db.models import Value
from django.db.models.functions import Concat
from django.utils.translation import gettext_lazy

from labels.models import Label
from statuses.models import Status
from tasks.models import Task
from users.models import User


class TaskFilter(django_filters.FilterSet):
    statuses = Status.objects.values_list('id', 'name', named=True).all()
    status = django_filters.ChoiceFilter(label=gettext_lazy('Статус'),
                                         choices=statuses)

    executors = User.objects.values_list(
        'id',
        Concat('first_name', Value(' '), 'last_name'),
        named=True
    )
    executor = django_filters.ChoiceFilter(label=gettext_lazy('Исполнитель'),
                                           choices=executors)

    all_labels = Label.objects.values_list('id', 'name', named=True).all()
    labels = django_filters.ChoiceFilter(label=gettext_lazy('Метка'),
                                         choices=all_labels)

    my_tasks = django_filters.BooleanFilter(
        label=gettext_lazy('Только свои задачи'),
        widget=forms.CheckboxInput(),
        method='only_my_tasks',
        field_name='my_tasks'
    )

    def only_my_tasks(self, queryset, name, value):
        if value:
            queryset = queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
