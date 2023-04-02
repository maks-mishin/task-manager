from django.urls import path

from labels.views import (LabelListView, LabelCreateView,
                          LabelUpdateView, LabelDeleteView)


urlpatterns = [
    path('', LabelListView.as_view(), name='list_labels'),
    path('create/', LabelCreateView.as_view(), name='create_label'),
    path('<int:pk>/update/', LabelUpdateView.as_view(), name='update_label'),
    path('<int:pk>/delete/', LabelDeleteView.as_view(), name='delete_label'),
]
