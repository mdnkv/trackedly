from django.urls import path

from projects import (views, api)

app_name = 'projects'

urlpatterns = [
    path('create/', views.ProjectCreateView.as_view(), name='project_create_view'),
    path('update/<uuid:pk>/', views.ProjectUpdateView.as_view(), name='project_update_view'),
    path('delete/<uuid:pk>/', views.ProjectDeleteView.as_view(), name='project_delete_view'),
    path('list/', views.ProjectsListView.as_view(), name='projects_list_view'),
    path('export/csv/', views.projects_to_csv_view, name='projects_to_csv_view'),
    path('api/create/', api.ProjectCreateAPIView.as_view(), name='project_create_api_view'),
    path('api/update/<uuid:pk>/', api.ProjectUpdateAPIView.as_view(), name='project_update_api_view'),
    path('api/delete/<uuid:pk>/', api.ProjectDeleteAPIView.as_view(), name='project_delete_api_view'),
    path('api/list/', api.ProjectsListAPIView.as_view(), name='projects_list_api_view'),
]