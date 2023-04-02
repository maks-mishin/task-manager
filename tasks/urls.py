from django.urls import path

from tasks.views import (TaskCreateView, TaskDeleteView, TaskDetailView,
                         TaskListView, TaskUpdateView)

urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='create_task'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='update_task'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='delete_task'),
    path('<int:pk>/', TaskDetailView.as_view(), name='view_task'),
    path('', TaskListView.as_view(), name='list_tasks'),
]
