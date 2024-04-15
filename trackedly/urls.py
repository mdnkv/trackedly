from django.contrib import admin
from django.views.i18n import JavaScriptCatalog
from django.urls import (path, include)

import django.contrib.auth.views as auth_views

from trackedly.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('users/', include('users.urls', namespace='users')),
    path('customers/', include('customers.urls', namespace='customers')),
    path('projects/', include('projects.urls', namespace='projects')),
    path('entries/', include('entries.urls', namespace='entries')),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', home_view, name='home_view')
]
