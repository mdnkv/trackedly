from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from faker import Faker

User = get_user_model()
faker = Faker()


class UserViewTest(TestCase):

    def test_user_update_view_is_rendered(self):
        """
        UserUpdateView is rendered correctly
        """
        user = User.objects.create_user(email=faker.email(), password='secret1234')
        self.client.force_login(user)
        url = reverse('users:user_update_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_update_view.html')

    def test_user_update_view_updates_user(self):
        """
        UserUpdateView updates user's first name and last name
        """
        user = User.objects.create_user(
            email=faker.email(), password='secret1234',
            first_name=faker.first_name(),
            last_name=faker.last_name()
        )
        self.client.force_login(user)
        url = reverse('users:user_update_view')
        body = {'first_name': faker.first_name(), 'last_name': faker.last_name()}
        response = self.client.post(url, body)
        result = User.objects.get(pk=user.pk)
        self.assertIsNotNone(result)
        self.assertEqual(body['first_name'], result.first_name)
        self.assertEqual(body['last_name'], result.last_name)

    def test_password_update_view_is_rendered(self):
        """
        PasswordUpdateView is rendered correctly
        """
        user = User.objects.create_user(email=faker.email(), password='secret1234')
        self.client.force_login(user)
        url = reverse('users:password_update_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/password_update_view.html')

    def test_password_update_view_updates_password(self):
        """
        PasswordUpdateView updates the user password
        """
        user = User.objects.create_user(email=faker.email(), password='secret1234')
        new_password = 'secret4321'
        self.client.force_login(user)
        data = {'new_password1': new_password, 'new_password2': new_password}
        url = reverse('users:password_update_view')
        response = self.client.post(url, data)
        result = User.objects.get(pk=user.pk)
        self.assertTrue(result.check_password(new_password))

    def test_user_detail_view_is_rendered(self):
        """
        UserDetailView is rendered correctly
        """
        user = User.objects.create_user(email=faker.email(), password='secret1234')
        self.client.force_login(user)
        url = reverse('users:user_detail_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_detail_view.html')

    def test_user_delete_view_is_rendered(self):
        """
        UserDeleteView is rendered correctly
        """
        user = User.objects.create_user(email=faker.email(), password='secret1234')
        self.client.force_login(user)
        url = reverse('users:user_delete_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_delete_view.html')

    def test_user_delete_view_deletes_user(self):
        """
        When submitted, the UserDeleteView deletes the current user
        """
        user = User.objects.create_user(email=faker.email(), password='secret1234')
        self.client.force_login(user)
        url = reverse('users:user_delete_view')
        response = self.client.post(url)
        result = User.objects.filter(id=user.pk).exists()
        self.assertFalse(result)
