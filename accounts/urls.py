from django.contrib.auth.views import PasswordChangeView
from django.urls import path, include

from accounts.views import RegistrationUsersView, LoginUsersView, logout_user, UserForgotPasswordView

urlpatterns = [
    path('registration/', RegistrationUsersView.as_view(), name='registration'),
    path('login/', LoginUsersView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('forgot-password/', UserForgotPasswordView.as_view(), name='forgot-password'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
    path('', include('django.contrib.auth.urls')),
]