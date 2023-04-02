from django.test import TestCase
from django.urls import reverse

from statuses.models import Status
from users.models import User


class TestStatuses(TestCase):

    fixtures = ['users.yaml',
                'statuses.yaml']

    def setUp(self):

        self.user = User.objects.get(pk=1)
        self.first_status = Status.objects.get(pk=1)
        self.second_status = Status.objects.get(pk=2)

    def test_list_statuses(self):

        self.client.force_login(self.user)
        response = self.client.get(reverse('list_statuses'))
        list_of_statuses = list(response.context['statuses'])

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list_of_statuses, [self.first_status,
                                                    self.second_status])

    def test_create_status(self):

        self.client.force_login(self.user)
        status = {'name': 'Отложить'}

        data = self.client.post(reverse('create_status'),
                                status, follow=True)
        current_status = Status.objects.get(name=status['name'])

        self.assertRedirects(data, reverse('list_statuses'))
        self.assertEqual(current_status.name, 'Отложить')

    def test_update_status(self):

        self.client.force_login(self.user)
        url = reverse('update_status', args=(self.first_status.pk,))
        status = {'name': 'В работе'}
        response = self.client.post(url, status, follow=True)

        self.assertEqual(Status.objects.get(pk=self.first_status.id),
                         self.first_status)
        self.assertRedirects(response, reverse('list_statuses'))

    def test_delete_status(self):

        self.client.force_login(self.user)
        url = reverse('delete_status', args=(self.second_status.pk,))
        response = self.client.post(url, follow=True)

        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(pk=self.second_status.id)

        self.assertRedirects(response, reverse('list_statuses'))

    def test_unauthorized_user(self):
        response = self.client.get(reverse('list_statuses'))
        self.assertRedirects(response, reverse('login'))
