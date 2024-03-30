from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse
from django.contrib.auth import get_user_model

from faker import Faker

User = get_user_model()
faker = Faker()


class UserAPITest(APITestCase):

    def test_signup_api_view_validates_user_already_exists(self):
        """
        SignupAPIView does not create a new user if the email already is assigned to another user
        """
        email = faker.email()
        User.objects.create_user(email=email, password=faker.password())
        url = reverse('users:signup_api_view')
        data = {
            'email': email,
            'first_name': faker.first_name(),
            'last_name': faker.last_name(),
            'password': faker.password()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_api_view_validates_password(self):
        """
        SignupAPIView performs password validation
        """
        url = reverse('users:signup_api_view')
        data = {
            'email': faker.email(),
            'first_name': faker.first_name(),
            'last_name': faker.last_name(),
            'password': 'secret'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_api_view_creates_user(self):
        """
        SignupAPIView creates a new user
        """
        url = reverse('users:signup_api_view')
        data = {
            'email': faker.email(),
            'first_name': faker.first_name(),
            'last_name': faker.last_name(),
            'password': faker.password()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_retrieve_update_api_view_updates_user(self):
        """
        When the PUT request is performed,
        UserRetrieveUpdateAPIView updates current user's first name and last name
        """
        user = User.objects.create_user(email=faker.email(), password=faker.password())
        url = reverse('users:user_retrieve_update_api_view')
        self.client.force_authenticate(user=user)
        data = {
            'first_name': faker.first_name(),
            'last_name': faker.last_name()
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = User.objects.get(pk=user.pk)
        self.assertEqual(result.first_name, data['first_name'])
        self.assertEqual(result.last_name, data['last_name'])

    def test_user_retrieve_update_api_view_returns_current_user_data(self):
        """
        When the GET request is performed,
        UserRetrieveUpdateAPIView returns data for the current user
        """
        user = User.objects.create_user(email=faker.email(), password=faker.password())
        url = reverse('users:user_retrieve_update_api_view')
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_update_api_view_validates_password(self):
        """
        PasswordUpdateAPIView validates password
        """
        user = User.objects.create_user(email=faker.email(), password=faker.password())
        url = reverse('users:password_update_api_view')
        data = {'password': 'secret'}
        self.client.force_authenticate(user=user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_update_api_view_updates_password(self):
        """
        PasswordUpdateAPIView updates the password for the current user
        """
        user = User.objects.create_user(email=faker.email(), password=faker.password())
        url = reverse('users:password_update_api_view')
        data = {'password': faker.password()}
        self.client.force_authenticate(user=user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = User.objects.get(pk=user.pk)
        self.assertTrue(result.check_password(data['password']))