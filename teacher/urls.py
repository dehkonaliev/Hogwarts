from django.urls import path
from .views import group_list_view, GroupDetailView

urlpatterns = [
    path('my-groups', group_list_view, name='tr-group-list'),
    path('my-group/<int:pk>', GroupDetailView.as_view(), name='tr-group-detail')
]