from django.contrib import admin
from django.urls import path

from task_manager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index')
]
