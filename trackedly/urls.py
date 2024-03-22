from django.contrib import admin
from django.urls import (path, include)

from trackedly.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('customers/', include('customers.urls', namespace='customers')),
    path('projects/', include('projects.urls', namespace='projects')),
    path('entries/', include('entries.urls', namespace='entries')),
    path('', home_view, name='home_view')
]
