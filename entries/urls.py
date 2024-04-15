from django.urls import path

from entries import (views, api)

app_name = 'entries'

urlpatterns = [
    path('create/', views.EntryCreateView.as_view(), name='entry_create_view'),
    path('update/<uuid:pk>/', views.EntryUpdateView.as_view(), name='entry_update_view'),
    path('delete/<uuid:pk>/', views.EntryDeleteView.as_view(), name='entry_delete_view'),
    path('list/', views.EntriesListView.as_view(), name='entries_list_view'),
    path('view/<uuid:pk>/', views.EntryDetailView.as_view(), name='entry_detail_view'),
    path('export/csv/', views.entries_to_csv_view, name='entries_to_csv_view'),
    path('api/create/', api.EntryCreateAPIView.as_view(), name='entry_create_api_view'),
    path('api/update/<uuid:pk>/', api.EntryUpdateAPIView.as_view(), name='entry_update_api_view'),
    path('api/delete/<uuid:pk>/', api.EntryDeleteAPIView.as_view(), name='entry_delete_api_view'),
    path('api/list/', api.EntryListAPIView.as_view(), name='entries_list_api_view'),
]