from django.urls import path
from .views import no_access, home_page, LoginView, SignUpView, UpdateMeView, my_profile_view

urlpatterns = [
    path('', home_page, name='home'),
    path('no-access', no_access, name='no-access'),
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('update-me', UpdateMeView.as_view(), name='update-me'),
    path('my-profile', my_profile_view, name='my-profile')
]