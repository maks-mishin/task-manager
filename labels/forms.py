from django.forms import ModelForm
from django.utils.translation import gettext_lazy

from labels.models import Label


class LabelForm(ModelForm):

    class Meta:
        model = Label
        fields = ('name', )
        labels = {'name': gettext_lazy('Имя')}
