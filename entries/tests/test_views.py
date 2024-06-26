from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from datetime import time, date

from entries.models import Entry
from faker import Faker

User = get_user_model()
faker = Faker()


class EntryViewTest(TestCase):

    def test_entry_update_view_is_rendered(self):
        """
        Verify that EntryUpdateView is rendered successfully,
        if
        1. the user is authenticated and
        2. the user accesses the Entry that is owned by the user
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
        url = reverse("entries:entry_update_view", kwargs={"pk": entry.pk})
        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "entries/views/entry_update_view.html")

    def test_entry_update_view_update_only_owned_entry(self):
        """
        Verify that user can update only the owned Entry object.
        If user tries to call the entry update view for Entry that belongs to another user,
        the 404 response is returned
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
        self.client.force_login(user2)
        url = reverse("entries:entry_update_view", kwargs={"pk": entry.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_entry_update_view_updates_entry(self):
        """
        Verify that EntryUpdateView updates a time entry object
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
        url = reverse("entries:entry_update_view", kwargs={"pk": entry.pk})
        self.client.force_login(user)
        date = faker.date()
        start_time = time(10, 30, 00)
        finish_time = time(11, 30, 00)
        data = {
            'start_date': date,
            'finish_date': date,
            'start_time': start_time,
            'finish_time': finish_time,
            'description': 'Hello entry'
        }
        response = self.client.post(url, data)
        result = Entry.objects.get(pk=entry.pk)
        self.assertEqual(result.description, data['description'])

    def test_entry_delete_view_is_rendered(self):
        """
        Verify that EntryDeleteView is rendered successfully,
        if
        1. the user is authenticated and
        2. the user accesses the Entry that is owned by the user
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
        url = reverse("entries:entry_delete_view", kwargs={"pk": entry.pk})
        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "entries/views/entry_delete_view.html")

    def test_entry_delete_view_deletes_only_owned_entry(self):
        """
        Verify that user can delete only the owned Entry object.
        If user tries to call the entry delete view for Entry that belongs to another user,
        the 404 response is returned
        """
        user1 = User.objects.create_user(email=faker.email(), password="secret1234")
        user2 = User.objects.create_user(email=faker.email(), password="secret1234")
        entry = Entry.objects.create(
            description="Some entry",
            owner=user1,
            start_date=faker.date(),
            finish_date=faker.date(),
            start_time=faker.time(),
            finish_time=faker.time()
        )
        self.client.force_login(user2)
        url = reverse("entries:entry_delete_view", kwargs={"pk": entry.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_entry_delete_view_deletes_entry(self):
        """
        Verify that EntryDeleteView deletes an entry
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
        url = reverse("entries:entry_delete_view", kwargs={"pk": entry.pk})
        self.client.force_login(user)
        response = self.client.post(url)
        result = Entry.objects.filter(pk=entry.pk).exists()
        self.assertFalse(result)

    def test_entry_create_view_is_rendered(self):
        """
        Verify that EntryCreateView is rendered correctly
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        self.client.force_login(user)
        url = reverse("entries:entry_create_view")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "entries/views/entry_create_view.html")

    def test_entry_create_view_creates_entry(self):
        """
        Verify that EntryCreateView creates an entry object
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        self.client.force_login(user)
        url = reverse("entries:entry_create_view")
        date = faker.date()
        start_time = time(10, 30, 00)
        finish_time = time(11, 30, 00)
        data = {
            'start_date': date,
            'finish_date': date,
            'start_time': start_time,
            'finish_time': finish_time,
            'description': 'Hello entry'
        }
        self.client.post(url, data)
        result = Entry.objects.filter(owner=user).first()
        self.assertIsNotNone(result)

    def test_entry_create_view_validates_input(self):
        """
        Verify that EntryCreateView validates that:
        - finish date should be after start date or same day
        - finish time should be after start time
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        self.client.force_login(user)
        url = reverse("entries:entry_create_view")
        start_date = date(2024, 3, 25)
        finish_date = date(2024, 3, 24)
        start_time = time(10, 30, 00)
        finish_time = time(11, 30, 00)
        data = {
            'start_date': start_date,
            'finish_date': finish_date,
            'start_time': start_time,
            'finish_time': finish_time,
            'description': 'Hello entry'
        }
        self.client.post(url, data)
        result = Entry.objects.filter(owner=user).first()
        self.assertIsNone(result)

    def test_entries_list_view_is_rendered(self):
        """
        Verify that EntriesListView is rendered correctly
        """
        user = User.objects.create_user(email=faker.email(), password="secret1234")
        self.client.force_login(user)
        url = reverse("entries:entries_list_view")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "entries/views/entries_list_view.html")

    def test_entry_detail_view_is_rendered(self):
        """
        Verify that EntryDetailView is rendered successfully,
        if
        1. the user is authenticated and
        2. the user accesses the Entry that is owned by the user
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
        url = reverse("entries:entry_detail_view", kwargs={"pk": entry.pk})
        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "entries/views/entry_detail_view.html")

    def test_entry_detail_view_shows_only_owned_entry(self):
        """
        Verify that user can view only the owned Entry object.
        If user tries to call the entry detail view for Entry that belongs to another user,
        the 404 response is returned
        """
        user1 = User.objects.create_user(email=faker.email(), password="secret1234")
        user2 = User.objects.create_user(email=faker.email(), password="secret1234")
        entry = Entry.objects.create(
            description="Some entry",
            owner=user1,
            start_date=faker.date(),
            finish_date=faker.date(),
            start_time=faker.time(),
            finish_time=faker.time()
        )
        self.client.force_login(user2)
        url = reverse("entries:entry_detail_view", kwargs={"pk": entry.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
