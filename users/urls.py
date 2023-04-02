from django.urls import path
from users.views import UserListView, UserCreateView, UserUpdateView, \
    UserDeleteView, UserLoginView, UserLogoutView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('create/', UserCreateView.as_view(), name='create_user'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update_user'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete_user'),
    path('', UserListView.as_view(), name='list_users'),
]

