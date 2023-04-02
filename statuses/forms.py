from django.forms import ModelForm
from django.utils.translation import gettext_lazy

from statuses.models import Status


class StatusForm(ModelForm):

    class Meta:
        model = Status
        fields = ['name']
        labels = {'name': gettext_lazy('Имя')}
