from django.urls import path

from django.contrib.auth.views import (LoginView, LogoutView,)

from users.views import (SignupView, UserUpdateView, PasswordUpdateView, UserDetailView, UserDeleteView)

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login_view.html'), name='login_view'),
    path('logout/', LogoutView.as_view(template_name='users/logout_view.html'), name='logout_view'),
    path('signup/', SignupView.as_view(), name='signup_view'),
    path('update/', UserUpdateView.as_view(), name='user_update_view'),
    path('password/', PasswordUpdateView.as_view(), name='password_update_view'),
    path('me/', UserDetailView.as_view(), name='user_detail_view'),
    path('delete/', UserDeleteView.as_view(), name='user_delete_view')
]