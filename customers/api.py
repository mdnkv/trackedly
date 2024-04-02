from rest_framework import generics

from customers.serializers import CustomerSerializer
from customers.models import Customer


class CustomerCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomerSerializer


class CustomerUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return Customer.objects.filter(owner=self.request.user)


class CustomerListAPIView(generics.ListAPIView):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return Customer.objects.filter(owner=self.request.user)


class CustomerDeleteAPIView(generics.DestroyAPIView):

    def get_queryset(self):
        return Customer.objects.filter(owner=self.request.user)
