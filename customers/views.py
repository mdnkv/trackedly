from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext as _

from customers.models import Customer
from customers.forms import (CustomerForm, )
from entries.models import Entry

from djqscsv import render_to_csv_response


class CustomerCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = CustomerForm
    success_url = reverse_lazy('customers:customers_list_view')
    template_name = 'customers/views/customer_create_view.html'

    def form_valid(self, form):
        customer = form.save(commit=False)
        customer.owner = self.request.user
        customer.save()
        message = _('Customer was created successfully!')
        messages.success(self.request, message)
        return super().form_valid(form)


class CustomerUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = CustomerForm
    success_url = reverse_lazy('customers:customers_list_view')
    template_name = 'customers/views/customer_update_view.html'
    context_object_name = 'customer'

    def get_queryset(self):
        return Customer.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        message = _('Customer was updated successfully!')
        messages.success(self.request, message)
        return super().form_valid(form)


class CustomerDeleteView(LoginRequiredMixin, generic.DeleteView):
    success_url = reverse_lazy('customers:customers_list_view')
    template_name = 'customers/views/customer_delete_view.html'
    queryset = Customer.objects.all()
    context_object_name = 'customer'

    def get_queryset(self):
        return Customer.objects.filter(owner=self.request.user)


class CustomerDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'customers/views/customer_detail_view.html'
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        customer = self.get_object()
        data['time_entries'] = Entry.objects.filter(project__customer=customer)
        return data

    def get_queryset(self):
        return Customer.objects.filter(owner=self.request.user)


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
