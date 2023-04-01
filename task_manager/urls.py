from django.contrib import admin
from django.urls import path

from task_manager.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index')
]
