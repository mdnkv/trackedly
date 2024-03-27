from django.shortcuts import render
from django.http import request

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from customers.models import Customer
from customers.forms import (CustomerForm,)

from djqscsv import render_to_csv_response

class CustomerCreateView(LoginRequiredMixin, generic.CreateView):

    form_class = CustomerForm
    success_url = reverse_lazy('customers:customers_list_view')
    template_name = 'customers/views/customer_create_view.html'

    def form_valid(self, form):
        customer = form.save(commit=False)
        customer.owner = self.request.user
        customer.save()
        return super().form_valid(form)

class CustomerUpdateView(LoginRequiredMixin, generic.UpdateView):

    form_class = CustomerForm
    success_url = reverse_lazy('customers:customers_list_view')
    template_name = 'customers/views/customer_update_view.html'
    context_object_name = 'customer'

    def get_queryset(self):
        return Customer.objects.filter(owner = self.request.user)

class CustomerDeleteView(LoginRequiredMixin, generic.DeleteView):

    success_url = reverse_lazy('customers:customers_list_view')
    template_name = 'customers/views/customer_delete_view.html'
    queryset = Customer.objects.all()
    context_object_name = 'customer'

    def get_queryset(self):
        return Customer.objects.filter(owner = self.request.user)

class CustomersListView(LoginRequiredMixin, generic.ListView):

    template_name = 'customers/views/customers_list_view.html'
    context_object_name = 'customers'
    paginate_by = 15

    def get_queryset(self):
        return Customer.objects.filter(owner=self.request.user)

@login_required()
def customers_to_csv_view(request):
    customers = Customer.objects.filter(owner=request.user)
    return render_to_csv_response(customers)