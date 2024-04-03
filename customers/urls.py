from django.urls import path

from customers import (views, api)

app_name = 'customers'

urlpatterns = [
    path('create/', views.CustomerCreateView.as_view(), name='customer_create_view'),
    path('update/<uuid:pk>/', views.CustomerUpdateView.as_view(), name='customer_update_view'),
    path('delete/<uuid:pk>/', views.CustomerDeleteView.as_view(), name='customer_delete_view'),
    path('list/', views.CustomersListView.as_view(), name='customers_list_view'),
    path('view/<uuid:pk>/', views.CustomerDetailView.as_view(), name='customer_detail_view'),
    path('export/csv/', views.customers_to_csv_view, name='customers_to_csv_view'),
    path('api/create/', api.CustomerCreateAPIView.as_view(), name='customer_create_api_view'),
    path('api/update/<uuid:pk>/', api.CustomerUpdateAPIView.as_view(), name='customer_update_api_view'),
    path('api/delete/<uuid:pk>/', api.CustomerDeleteAPIView.as_view(), name='customer_delete_api_view'),
    path('api/list/', api.CustomerListAPIView.as_view(), name='customers_list_api_view'),
]