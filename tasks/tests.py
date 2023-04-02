from django.test import TestCase
from django.urls import reverse
from django_filters import FilterSet

from statuses.models import Status
from tasks.models import Task
from users.models import User


class TestTask(TestCase):

    fixtures = ['users.yaml',
                'tasks.yaml',
                'labels.yaml',
                'statuses.yaml']

    def setUp(self) -> None:
        self.first_user = User.objects.get(pk=1)
        self.second_user = User.objects.get(pk=2)
        self.first_status = Status.objects.get(pk=1)
        self.second_status = Status.objects.get(pk=2)
        self.first_task = Task.objects.get(pk=1)
        self.second_task = Task.objects.get(pk=2)

    def test_list_of_tasks(self):
        self.client.force_login(self.first_user)
        response = self.client.get(reverse('list_tasks'))
        tasks_list = list(response.context['tasks'])

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(tasks_list, [self.first_task,
                                              self.second_task])

    def test_create_tasks(self):
        self.client.force_login(self.first_user)
        task = {'name': 'Написать тесты',
                'description': 'Тесты к tasks',
                'author': 1,
                'executor': 2,
                'status': 1}

        response = self.client.post(reverse('create_task'), task, follow=True)
        created_task = Task.objects.get(name=task['name'])

        self.assertRedirects(response, reverse('list_tasks'))
        self.assertEqual(created_task.name, 'Написать тесты')

    def test_update_task(self):
        self.client.force_login(self.first_user)
        url = reverse('update_task', args=(self.first_task.pk,))
        task = {
            'name': 'Обновлённая задача',
            'description': 'Обновлённое описание',
            'author': 2,
            'executor': 1,
            'status': 2
        }

        response = self.client.post(url, task, follow=True)
        created_task = Task.objects.get(name=task['name'])

        self.assertRedirects(response, reverse('list_tasks'))
        self.assertEqual(created_task.name, 'Обновлённая задача')

    def test_delete_task(self):
        self.client.force_login(self.first_user)
        url = reverse('delete_task', args=(self.first_task.id,))
        response = self.client.post(url, follow=True)

        self.assertRedirects(response, reverse('list_tasks'))

    def test_delete_task_by_non_author(self):
        self.client.force_login(self.second_user)
        url = reverse('delete_task', args=(self.first_task.pk,))
        response = self.client.post(url, follow=True)

        self.assertTrue(Task.objects.filter(pk=self.first_task.pk).exists())
        self.assertRedirects(response, reverse('list_tasks'))

    def test_filter_status(self):

        status = Task._meta.get_field('status')
        result = FilterSet.filter_for_field(status, 'status')
        self.assertEqual(result.field_name, 'status')

    def test_filter_executor(self):

        status = Task._meta.get_field('executor')
        result = FilterSet.filter_for_field(status, 'executor')

        self.assertEqual(result.field_name, 'executor')

    def test_filter_label(self):

        status = Task._meta.get_field('labels')
        result = FilterSet.filter_for_field(status, 'labels')
        self.assertEqual(result.field_name, 'labels')
