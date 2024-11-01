from django.urls import path

from users.views import (UserLoginView, UserRegistrationView)


app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='index'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
]
