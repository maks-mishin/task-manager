from django.forms import ModelForm
from statuses.models import Status
from django.utils.translation import gettext_lazy


class StatusForm(ModelForm):

    class Meta:
        model = Status
        fields = ['name']
        labels = {'name': gettext_lazy('Имя')}
