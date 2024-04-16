from django.urls import path

from django.contrib.auth.views import (LoginView, LogoutView,)
from rest_framework.authtoken.views import obtain_auth_token

from users.views import (SignupView, UserUpdateView, PasswordUpdateView, UserDetailView,
                         UserDeleteView, confirm_email_view)
from users import api

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/views/login_view.html'), name='login_view'),
    path('logout/', LogoutView.as_view(template_name='users/views/logout_view.html'), name='logout_view'),
    path('signup/', SignupView.as_view(), name='signup_view'),
    path('update/', UserUpdateView.as_view(), name='user_update_view'),
    path('password/', PasswordUpdateView.as_view(), name='password_update_view'),
    path('me/', UserDetailView.as_view(), name='user_detail_view'),
    path('delete/', UserDeleteView.as_view(), name='user_delete_view'),
    path('confirm-email/', confirm_email_view, name='confirm_email_view'),
    path('api/signup/', api.SignupAPIView.as_view(), name='signup_api_view'),
    path('api/profile/', api.UserRetrieveUpdateAPIView.as_view(), name='user_retrieve_update_api_view'),
    path('api/password/', api.PasswordUpdateAPIView.as_view(), name='password_update_api_view'),
    path('api/login/', obtain_auth_token, name='login_api_view'),
    path('api/logout/', api.LogoutAPIView.as_view(), name='logout_api_view'),
    path('api/email-confirm/', api.SendEmailConfirmationAPIView.as_view(), name='send_email_confirmation_api_view'),
]