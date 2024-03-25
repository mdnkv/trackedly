from django.test import TestCase
from django.contrib.auth import get_user_model

from datetime import date, time

from entries.models import Entry
from entries.utils import (map_entry_as_duration, get_total_duration, get_total_duration_as_hours)

from faker import Faker

User = get_user_model()
faker = Faker()


class EntryUtilsTest(TestCase):

    def test_map_entry_as_duration(self):
        """
        Validate that map_entry_as_duration() returns a duration of an entry
        """
        user = User.objects.create_user(email=faker.email(), password='secret1234')
        start_date = date(year=2024, month=3, day=25)
        finish_date = date(year=2024, month=3, day=25)
        start_time = time(10, 00, 00)
        finish_time = time(10, 35, 00)
        entry = Entry.objects.create(
            owner=user,
            start_date=start_date,
            finish_date=finish_date,
            start_time=start_time,
            finish_time=finish_time,
            description=faker.paragraph(nb_sentences=1)
        )
        duration = map_entry_as_duration(entry)
        self.assertEqual('0:35:00', str(duration))

    def test_get_total_duration(self):
        """
        Validate that get_total_duration() returns a duration of all entries in the list
        """
        user = User.objects.create_user(email=faker.email(), password='secret1234')
        Entry.objects.create(
            owner=user,
            start_date=date(year=2024, month=3, day=25),
            finish_date=date(year=2024, month=3, day=25),
            start_time=time(9, 00, 00),
            finish_time=time(10, 00, 00),
            description=faker.paragraph(nb_sentences=1)
        )
        Entry.objects.create(
            owner=user,
            start_date=date(year=2024, month=3, day=25),
            finish_date=date(year=2024, month=3, day=25),
            start_time=time(11, 00, 00),
            finish_time=time(11, 30, 00),
            description=faker.paragraph(nb_sentences=1)
        )
        Entry.objects.create(
            owner=user,
            start_date=date(year=2024, month=3, day=25),
            finish_date=date(year=2024, month=3, day=25),
            start_time=time(12, 00, 00),
            finish_time=time(12, 35, 00),
            description=faker.paragraph(nb_sentences=1)
        )
        duration = get_total_duration(user.entries.all())
        self.assertEqual("2:05:00", str(duration))

    def test_get_total_duration_as_hours(self):
        """
        Validate that get_total_duration_as_hours() returns a duration of all entries as the integer of hours
        """
        user = User.objects.create_user(email=faker.email(), password='secret1234')
        Entry.objects.create(
            owner=user,
            start_date=date(year=2024, month=3, day=25),
            finish_date=date(year=2024, month=3, day=25),
            start_time=time(9, 00, 00),
            finish_time=time(10, 00, 00),
            description=faker.paragraph(nb_sentences=1)
        )
        Entry.objects.create(
            owner=user,
            start_date=date(year=2024, month=3, day=25),
            finish_date=date(year=2024, month=3, day=25),
            start_time=time(11, 00, 00),
            finish_time=time(11, 30, 00),
            description=faker.paragraph(nb_sentences=1)
        )
        Entry.objects.create(
            owner=user,
            start_date=date(year=2024, month=3, day=25),
            finish_date=date(year=2024, month=3, day=25),
            start_time=time(12, 00, 00),
            finish_time=time(12, 35, 00),
            description=faker.paragraph(nb_sentences=1)
        )
        duration = get_total_duration_as_hours(user.entries.all())
        self.assertEqual(2, duration)
