from django.urls import path

from entries import views

app_name = 'entries'

urlpatterns = [
    path('create/', views.EntryCreateView.as_view(), name='entry_create_view'),
    path('update/<uuid:pk>/', views.EntryUpdateView.as_view(), name='entry_update_view'),
    path('delete/<uuid:pk>/', views.EntryDeleteView.as_view(), name='entry_delete_view'),
    path('list/', views.EntriesListView.as_view(), name='entries_list_view'),
    path('export/csv', views.entries_to_csv_view, name='entries_to_csv_view')
]