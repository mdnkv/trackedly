from django.urls import path

from projects import views

app_name = 'projects'

urlpatterns = [
    path('create/', views.ProjectCreateView.as_view(), name='project_create_view'),
    path('update/<uuid:pk>/', views.ProjectUpdateView.as_view(), name='project_update_view'),
    path('delete/<uuid:pk>/', views.ProjectDeleteView.as_view(), name='project_delete_view'),
    path('list/', views.ProjectsListView.as_view(), name='projects_list_view'),
]