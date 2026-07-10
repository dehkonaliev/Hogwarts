from django.urls import path
from .views import no_access

urlpatterns = [
    path('no-access', no_access, name='no-access')
]