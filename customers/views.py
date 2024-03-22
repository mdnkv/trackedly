from django.shortcuts import render

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from customers.models import Customer
from customers.forms import (CustomerForm,)

class CustomerCreateView(LoginRequiredMixin, generic.CreateView):

    form_class = CustomerForm
    success_url = reverse_lazy('customers:customers_list_view')
    template_name = 'customers/customer_create_view.html'

    def form_valid(self, form):
        customer = form.save(commit=False)
        customer.owner = self.request.user
        customer.save()
        return super().form_valid(form)

class CustomerUpdateView(LoginRequiredMixin, generic.UpdateView):

    form_class = CustomerForm
    success_url = reverse_lazy('customers:customers_list_view')
    template_name = 'customers/customer_update_view.html'
    # queryset = Customer.objects.all()
    context_object_name = 'customer'

    def get_queryset(self):
        return Customer.objects.filter(owner = self.request.user)

class CustomerDeleteView(LoginRequiredMixin, generic.DeleteView):

    success_url = reverse_lazy('customers:customers_list_view')
    template_name = 'customers/customer_delete_view.html'
    queryset = Customer.objects.all()
    context_object_name = 'customer'

    def get_queryset(self):
        return Customer.objects.filter(owner = self.request.user)

class CustomersListView(LoginRequiredMixin, generic.ListView):

    template_name = 'customers/customers_list_view.html'
    context_object_name = 'customers'

    def get_queryset(self):
        return Customer.objects.filter(owner=self.request.user)