from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from customers.models import Customer
from faker import Faker

User = get_user_model()
faker = Faker()

class CustomerViewsTests(TestCase):

    def test_customer_update_view_is_rendered(self):
        """
        Verify that CustomerUpdateView is rendered successfully,
        if
        1. the user is authenticated and
        2. the user accesses the Customer that is owned by the user
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        customer = Customer.objects.create(name="Customer", owner=user)
        url = reverse("customers:customer_update_view", kwargs={'pk': customer.pk})
        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customers/views/customer_update_view.html")

    def test_customer_update_view_update_only_owned_customer(self):
        """
        Verify that user can update only the owned Customer object.
        If user tries to call the customer update view for Customer that belongs to another user,
        the 404 response is returned
        """
        user1 = User.objects.create_user(email=faker.email(), password='secret1234')
        user2 = User.objects.create_user(email=faker.email(), password='secret1234')
        customer = Customer.objects.create(name="Customer for user1", owner=user1)
        url = reverse("customers:customer_update_view", kwargs={"pk": customer.pk})
        self.client.force_login(user2)
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_customer_update_view_updates_customer(self):
        """
        Verify that CustomerUpdateView can update the customer object
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        customer = Customer.objects.create(name="Customer", owner=user)
        url = reverse("customers:customer_update_view", kwargs={'pk': customer.pk})
        self.client.force_login(user)
        data = {'name': 'new customer name'}
        response = self.client.post(url, data)
        result = Customer.objects.get(pk=customer.pk)
        self.assertEqual(result.name, data['name'])

    def test_customer_delete_view_is_rendered(self):
        """
        Verify that CustomerDeleteView is rendered successfully,
        if
        1. the user is authenticated and
        2. the user accesses the Customer that is owned by the user
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        customer = Customer.objects.create(name="Customer", owner=user)
        url = reverse("customers:customer_delete_view", kwargs={'pk': customer.pk})
        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customers/views/customer_delete_view.html")

    def test_customer_delete_view_delete_only_owned_customer(self):
        """
        Verify that user can delete only the owned Customer object.
        If user tries to call the customer delete view for Customer that belongs to another user,
        the 404 response is returned
        """
        user1 = User.objects.create_user(email=faker.email(), password='secret1234')
        user2 = User.objects.create_user(email=faker.email(), password='secret1234')
        customer = Customer.objects.create(name="Customer for user1", owner=user1)
        url = reverse("customers:customer_delete_view", kwargs={"pk": customer.pk})
        self.client.force_login(user2)
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_customer_delete_view_deletes_the_customer(self):
        """
        Verify that CustomerDeleteView deletes the customer object
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        customer = Customer.objects.create(name="Customer", owner=user)
        url = reverse("customers:customer_delete_view", kwargs={'pk': customer.pk})
        self.client.force_login(user)
        response = self.client.post(url)
        result = Customer.objects.filter(pk=customer.pk).exists()
        self.assertFalse(result)

    def test_customers_list_view_is_rendered(self):
        """
        Verify that CustomersListView is rendered correctly
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        url = reverse('customers:customers_list_view')
        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customers/views/customers_list_view.html")

    def test_customer_create_view_is_rendered(self):
        """
        Verify that CustomerCreateView is rendered correctly
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        url = reverse('customers:customer_create_view')
        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customers/views/customer_create_view.html")

    def test_customer_create_view_creates_customer(self):
        """
        Verify that CustomerCreateView creates new customer
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        url = reverse('customers:customer_create_view')
        self.client.force_login(user)
        data = {'name': 'customer name'}
        response = self.client.post(url, data)
        result = Customer.objects.filter(owner=user).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.name, data['name'])
