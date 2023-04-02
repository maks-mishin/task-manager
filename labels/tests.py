from django.test import TestCase
from django.urls import reverse, reverse_lazy

from labels.models import Label
from tasks.models import Task
from users.models import User


class TestStatus(TestCase):

    fixtures = ['users.yaml',
                'tasks.yaml',
                'labels.yaml',
                'statuses.yaml']

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.first_task = Task.objects.get(pk=1)
        self.second_task = Task.objects.get(pk=2)
        self.first_label = Label.objects.get(pk=1)
        self.second_label = Label.objects.get(pk=2)

    def test_list_of_labels(self):

        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('list_labels'))
        labels_list = list(response.context['labels'])

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(labels_list, [self.first_label,
                                               self.second_label])

    def test_create_label(self):

        self.client.force_login(self.user)
        label = {'name': 'Метка'}
        new_data = self.client.post(reverse_lazy('create_label'),
                                    label,
                                    follow=True)
        created_status = Label.objects.get(name=label['name'])

        self.assertRedirects(new_data, reverse('list_labels'))
        self.assertEqual(created_status.name, 'Метка')

    def test_change_label(self):

        self.client.force_login(self.user)
        url = reverse('update_label', args=(self.second_label.pk,))
        label = {'name': 'Другое'}
        response = self.client.post(url, label, follow=True)

        self.assertEqual(Label.objects.get(pk=self.second_label.id),
                         self.second_label)
        self.assertRedirects(response, reverse('list_labels'))

    def test_delete_label(self):

        self.client.force_login(self.user)
        url = reverse_lazy('delete_label', args=(self.second_label.pk,))
        response = self.client.post(url, follow=True)

        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(pk=self.second_label.pk)

        self.assertRedirects(response, reverse('list_labels'))

    def test_delete_label_with_task(self):

        self.client.force_login(self.user)
        url = reverse_lazy('delete_label', args=(self.first_label.pk,))
        response = self.client.post(url, follow=True)

        self.assertTrue(Label.objects.filter(pk=self.first_label.id).exists())
        self.assertRedirects(response, reverse('list_labels'))

    def test_status_list_without_authorization(self):

        response = self.client.get(reverse_lazy('list_labels'))
        self.assertRedirects(response, reverse('login'))
