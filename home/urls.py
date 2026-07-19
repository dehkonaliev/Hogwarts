from django.urls import path
from .views import no_access, home_page, LoginView

urlpatterns = [
    path('', home_page, name='home'),
    path('no-access', no_access, name='no-access'),
    path('login', LoginView.as_view(), name='login')
]