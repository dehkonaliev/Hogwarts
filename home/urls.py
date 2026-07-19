from django.urls import path
from .views import no_access, home_page, LoginView, SignUpView, UpdateMeView

urlpatterns = [
    path('', home_page, name='home'),
    path('no-access', no_access, name='no-access'),
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('update-me', UpdateMeView.as_view(), name='update-me')
]