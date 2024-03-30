from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from customers.models import Customer
from customers.serializers import CustomerSerializer

from faker import Faker

User = get_user_model()
faker = Faker()


class CustomerAPITest(APITestCase):

    def test_customer_create_api_view_creates_customer(self):
        """
        Verify that CustomerCreateAPIView creates a new customer for a current user
        """
        data = {'name': 'my customer'}
        user = User.objects.create_user(email=faker.email(), password=faker.password())
        self.client.force_authenticate(user=user)
        url = reverse('customers:customer_create_api_view')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        result = Customer.objects.filter(owner=user).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.name, data['name'])

    def test_customer_update_api_view_only_owner(self):
        """
        Verify that CustomerUpdateAPIView can update only a customer that belongs to a current user or 404 returned
        """
        user1 = User.objects.create_user(email=faker.email(), password=faker.password())
        user2 = User.objects.create_user(email=faker.email(), password=faker.password())
        customer = Customer.objects.create(name='name', owner=user1)
        self.client.force_authenticate(user=user2)
        data = {'name': 'new name'}
        url = reverse('customers:customer_update_api_view', kwargs={'pk': customer.pk})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customer_update_api_view_updates_customer(self):
        """
        Verify that CustomerUpdateAPIView updates a customer
        """
        user = User.objects.create_user(email=faker.email(), password=faker.password())
        customer = Customer.objects.create(name='name', owner=user)
        self.client.force_authenticate(user=user)
        data = {'name': 'new name'}
        url = reverse('customers:customer_update_api_view', kwargs={'pk': customer.pk})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = Customer.objects.get(pk=customer.pk)
        self.assertEqual(result.name, data.get('name'))

    def test_customer_delete_api_view_only_owner(self):
        """
        Verify that CustomerDeleteAPIView can delete only a customer that belongs to a current user or 404 returned
        """
        user1 = User.objects.create_user(email=faker.email(), password=faker.password())
        user2 = User.objects.create_user(email=faker.email(), password=faker.password())
        customer = Customer.objects.create(name='name', owner=user1)
        self.client.force_authenticate(user=user2)
        url = reverse('customers:customer_delete_api_view', kwargs={'pk': customer.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customer_delete_api_view_deletes_customer(self):
        """
        Verify that CustomerDeleteAPIView deletes a customer
        """
        user = User.objects.create_user(email=faker.email(), password=faker.password())
        customer = Customer.objects.create(name='name', owner=user)
        self.client.force_authenticate(user=user)
        url = reverse('customers:customer_delete_api_view', kwargs={'pk': customer.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        result = Customer.objects.filter(pk=customer.pk).exists()
        self.assertFalse(result)

    def test_customers_list_api_view_returns_customers(self):
        """
        Verify that CustomerListAPIView returns a list of customers that belong to a current user
        """
        user = User.objects.create_user(email=faker.email(), password=faker.password())
        Customer.objects.create(name='name', owner=user)
        Customer.objects.create(name='name', owner=user)
        self.client.force_authenticate(user=user)
        url = reverse('customers:customers_list_api_view')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CustomerSerializer(data=response.data, many=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(len(serializer.data), Customer.objects.filter(owner=user).count())
