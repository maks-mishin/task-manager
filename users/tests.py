from django.test import TestCase, Client
from django.urls import reverse
from users.models import User


class TestApplicationUsers(TestCase):
    fixtures = ['users.yaml']

    def setUp(self):
        self.first_user = User.objects.get(pk=1)
        self.second_user = User.objects.get(pk=2)
        self.client: Client = Client()

    def test_create_user(self):
        url = reverse('create_user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Регистрация')

        new_user = {
            'first_name': 'test',
            'last_name': 'test',
            'username': 'test',
            'password1': 'Test123!#',
            'password2': 'Test123!#',
        }
        count_users_before = User.objects.count()
        response = self.client.post(url, new_user, follow=True)
        self.assertRedirects(response, reverse('login'))
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'Пользователь успешно зарегистрирован')

        self.assertEqual(User.objects.count(), count_users_before + 1)
        created_user = User.objects.last()
        self.assertEqual(created_user.first_name, new_user['first_name'])
        self.assertEqual(created_user.last_name, new_user['last_name'])
        self.assertEqual(created_user.username, new_user['username'])

    def test_login_user(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        credentials = {'username': 'user_for_test',
                       'password': 'FakePass654!#'}
        User.objects.create_user(**credentials)
        response = self.client.post(reverse('login'), credentials, follow=True)
        self.assertRedirects(response, reverse('index'))

        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'Вы авторизованы')

        fake_credentials = {'username': 'yeltsin_fake',
                            'password': 'FakePass654!#_fake'}
        response = self.client.post(reverse('login'), fake_credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        errors = response.context['errors']
        self.assertEqual(
            str(errors[0]),
            'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.'
        )

    def test_logout_user(self):
        response = self.client.post(reverse('logout'), follow=True)
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(response.status_code, 200)

        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'Вы вышли из системы')

    def test_update(self):
        user = self.first_user
        self.client.force_login(user)
        url = reverse('update_user', args=(user.id, ))

        change_user = {
            'first_name': "Vladimir",
            'last_name': user.last_name,
            'username': user.username,
            'password1': 'Test321!#',
            'password2': 'Test321!#',
        }

        response = self.client.post(url, change_user, follow=True)
        changed_user = User.objects.get(username=user.username)

        self.assertRedirects(response, reverse('list_users'))
        self.assertTrue(changed_user.check_password('Test321!#'))

    def test_delete_user(self):
        user = self.second_user
        self.client.force_login(user)
        url = reverse('delete_user', args=(user.id,))
        response = self.client.post(url, follow=True)

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=user.id)

        self.assertRedirects(response, reverse('list_users'))
