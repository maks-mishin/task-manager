from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'password1', 'password2'
                  ]


class UserLoginForm(AuthenticationForm):
    username = User.username
    password = User.password
    fields = ['username', 'password1']
