from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import time

from entries.models import Entry
from entries.serializers import EntryListSerializer

from faker import Faker

User = get_user_model()
faker = Faker()


class EntryAPITest(APITestCase):

    def test_entry_create_api_view_creates_entry(self):
        """
        Verify that EntryCreateAPIView creates a new entry for a current user
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        self.client.force_authenticate(user=user)
        url = reverse("entries:entry_create_api_view")
        base_date = faker.date()
        start_time = time(10, 30, 00)
        finish_time = time(11, 30, 00)
        data = {
            'start_date': base_date,
            'finish_date': base_date,
            'start_time': start_time,
            'finish_time': finish_time,
            'description': 'Hello entry',
            'project': ''
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        result = Entry.objects.filter(owner=user).first()
        self.assertIsNotNone(result)

    def test_entry_update_api_view_only_owner(self):
        """
        Verify that EntryUpdateAPIView can update only an entry that belongs to a current user or 404 returned
        """
        user1 = User.objects.create_user(email=faker.email(), password="secret1234")
        user2 = User.objects.create_user(email=faker.email(), password="secret1234")
        entry = Entry.objects.create(
            description="some entry",
            owner=user1,
            start_date=faker.date(),
            finish_date=faker.date(),
            start_time=faker.time(),
            finish_time=faker.time()
        )
        base_date = faker.date()
        start_time = time(10, 30, 00)
        finish_time = time(11, 30, 00)
        data = {
            'start_date': base_date,
            'finish_date': base_date,
            'start_time': start_time,
            'finish_time': finish_time,
            'description': 'Hello entry',
            'project': ''
        }
        self.client.force_authenticate(user=user2)
        url = reverse('entries:entry_update_api_view', kwargs={'pk': entry.pk})
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_entry_update_api_view_updates_entry(self):
        """
        Verify that EntryUpdateAPIView updates an entry
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        entry = Entry.objects.create(
            description="some entry",
            owner=user,
            start_date=faker.date(),
            finish_date=faker.date(),
            start_time=faker.time(),
            finish_time=faker.time()
        )
        base_date = faker.date()
        start_time = time(10, 30, 00)
        finish_time = time(11, 30, 00)
        data = {
            'start_date': base_date,
            'finish_date': base_date,
            'start_time': start_time,
            'finish_time': finish_time,
            'description': 'Hello entry',
            'project': ''
        }
        self.client.force_authenticate(user=user)
        url = reverse('entries:entry_update_api_view', kwargs={'pk': entry.pk})
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = Entry.objects.get(pk=entry.pk)
        self.assertEqual(result.description, data['description'])
        self.assertEqual(result.start_time, start_time)
        self.assertEqual(result.finish_time, finish_time)

    def test_entry_delete_api_view_only_owner(self):
        """
        Verify that EntryDeleteAPIView can delete only an entry that belongs to a current user or 404 returned
        """
        user1 = User.objects.create_user(email=faker.email(), password="secret1234")
        user2 = User.objects.create_user(email=faker.email(), password="secret1234")
        entry = Entry.objects.create(
            description="some entry",
            owner=user1,
            start_date=faker.date(),
            finish_date=faker.date(),
            start_time=faker.time(),
            finish_time=faker.time()
        )
        self.client.force_authenticate(user=user2)
        url = reverse('entries:entry_delete_api_view', kwargs={'pk': entry.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_entry_delete_api_view_deletes_entry(self):
        """
        Verify that EntryDeleteAPIView deletes an entry
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        entry = Entry.objects.create(
            description="some entry",
            owner=user,
            start_date=faker.date(),
            finish_date=faker.date(),
            start_time=faker.time(),
            finish_time=faker.time()
        )
        self.client.force_authenticate(user=user)
        url = reverse('entries:entry_delete_api_view', kwargs={'pk': entry.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        result = Entry.objects.filter(id=entry.pk).exists()
        self.assertFalse(result)

    def test_entries_list_api_view_returns_entries(self):
        """
        Verify that EntriesListAPIView returns a list of entries that belong to a current user
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        Entry.objects.create(
            description="some entry",
            owner=user,
            start_date=faker.date(),
            finish_date=faker.date(),
            start_time=faker.time(),
            finish_time=faker.time()
        )
        Entry.objects.create(
            description="some entry",
            owner=user,
            start_date=faker.date(),
            finish_date=faker.date(),
            start_time=faker.time(),
            finish_time=faker.time()
        )
        Entry.objects.create(
            description="some entry",
            owner=user,
            start_date=faker.date(),
            finish_date=faker.date(),
            start_time=faker.time(),
            finish_time=faker.time()
        )
        self.client.force_authenticate(user=user)
        url = reverse('entries:entries_list_api_view')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = EntryListSerializer(data=response.data, many=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(len(serializer.data), Entry.objects.filter(owner=user).count())
