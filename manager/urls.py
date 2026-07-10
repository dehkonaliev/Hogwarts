from django.urls import path
from .views import CreateGroupView

urlpatterns = [
    path('groups', CreateGroupView.as_view(), name='mg-group-list'),
]

