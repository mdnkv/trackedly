from django.urls import path

from customers import views

app_name = 'customers'

urlpatterns = [
    path('create/', views.CustomerCreateView.as_view(), name='customer_create_view'),
    path('update/<uuid:pk>/', views.CustomerUpdateView.as_view(), name='customer_update_view'),
    path('delete/<uuid:pk>/', views.CustomerDeleteView.as_view(), name='customer_delete_view'),
    path('list/', views.CustomersListView.as_view(), name='customers_list_view'),
]