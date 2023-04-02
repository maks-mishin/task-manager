from django.db import models

from labels.models import Label
from statuses.models import Status
from users.models import User


class Task(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status,
                               on_delete=models.PROTECT,
                               null=True,
                               related_name='task_status')
    author = models.ForeignKey(User,
                               on_delete=models.PROTECT,
                               null=False,
                               related_name='task_author')
    executor = models.ForeignKey(User,
                                 null=True,
                                 blank=True,
                                 on_delete=models.PROTECT,
                                 related_name='task_executor')
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(Label,
                                    related_name='task_label',
                                    blank=True,
                                    through='TaskLabels',
                                    through_fields=('task', 'label'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


class TaskLabels(models.Model):
    task = models.ForeignKey(Task,
                             on_delete=models.CASCADE)
    label = models.ForeignKey(Label,
                              on_delete=models.PROTECT)
